"""Regression set: known-correct and known-wrong tags, taken from Claude's hand reviews.
  regression.py <db> make    -> writes lib/regression.tsv from lib/reviews/*.json and lib/snap_review.json
  regression.py <db> enforce -> re-applies the reviewed drops (build step after kw_sync and propagate)
  regression.py <db> check   -> checks every line against the database; exit code 1 on any failure (a 'present' parent also holds
                             through a narrower concept, see parent_rule.py)
Lines: game, entity id, entity name, concept, role ('*' = any role), expect (present|absent).
A review 'add' means the tag must be present; a 'drop' means it must be absent. Keyword corrections are also
checked on one entry that has the keyword (inheritance via kw_sync must agree with the keyword)."""
import json, sqlite3, sys, os, glob, csv
db, mode = sys.argv[1:3]
here = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(here, 'regression.tsv')
c = sqlite3.connect(db); q = lambda s, *a: c.execute(s, a).fetchall()
# entries merged by dedupe.py resolve to the entry that kept their mechanic
kept = dict(q('SELECT old_id, kept_id FROM merged_entities')) if q("SELECT 1 FROM sqlite_master WHERE name='merged_entities'") else {}
res = lambda i: kept.get(int(i), int(i))
if mode == 'make':
    files = [(os.path.basename(f)[:-5], f) for f in sorted(glob.glob(os.path.join(here, 'reviews', '*.json')))] + [('marvel_snap', os.path.join(here, 'snap_review.json'))]
    later = [(os.path.basename(f)[:-5], f) for f in sorted(glob.glob(os.path.join(here, 'reviews_outcome', '*.json')))]   # applied after the outcome tree: override earlier reviews
    rows = set()
    for game, f in files:
        for key, r in json.load(open(f, encoding='utf-8')).items():
            ids = [(res(key),)] if key.isdigit() else q('select id from entities where game=? and name=?', game, key)
            for (i,) in ids:
                e = q('select name, category from entities where id=? and game=?', i, game)
                if not e: continue
                for exp, items in (('present', r.get('add', [])), ('absent', r.get('drop', []))):
                    for it in items:
                        con, role = (it.split(':') + [None])[:2]
                        role = role or ('does' if exp == 'present' else '*')
                        rows.add((game, i, e[0][0], con, role, exp))
    for game, f in later:
        for key, r in json.load(open(f, encoding='utf-8')).items():
            i = res(key)
            e = q('select name from entities where id=? and game=?', i, game)
            if not e: continue
            for it in r.get('drop', []):
                con, role = (it.split(':') + [None])[:2]
                rows = {x for x in rows if not (x[1] == i and x[3] == con and (role is None or x[4] == role))}
                rows.add((game, i, e[0][0], con, role or '*', 'absent'))
            for it in r.get('add', []):
                con, role = (it.split(':') + ['does'])[:2]
                rows = {x for x in rows if not (x[1] == i and x[3] == con and x[5] == 'absent')}
                rows.add((game, i, e[0][0], con, role, 'present'))
    # an add and a drop of the same tag on one entry (later review overrides): keep what the database holds now
    keys = {}
    for r in rows: keys.setdefault(r[:5], set()).add(r[5])
    final = []
    for k, exps in keys.items():
        if len(exps) == 2:
            have = q('select 1 from entity_concepts where entity=? and concept=?' + ('' if k[4] == '*' else ' and role=?'), k[1], k[3], *([] if k[4] == '*' else [k[4]]))
            exps = {'present' if have else 'absent'}
        final.append(k + (exps.pop(),))
    # a role-less drop next to a role-specific add of the same concept on one entry: the add is the narrower decision, keep it
    pres = {(r[1], r[3]) for r in final if r[5] == 'present'}
    final = [r for r in final if not (r[5] == 'absent' and r[4] == '*' and (r[1], r[3]) in pres)]
    with open(out, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh, delimiter='\t'); w.writerow(['game', 'entity', 'name', 'concept', 'role', 'expect'])
        for r in sorted(final, key=lambda r: (r[0], r[1], r[3])): w.writerow(r)
    print('regression lines:', len(final))
elif mode == 'enforce':
    # re-applies the reviewed drops after kw_sync/propagate, which re-inherit keyword concepts the reviewer had removed
    n = 0
    for r in csv.DictReader(open(out, encoding='utf-8'), delimiter='\t'):
        if r['expect'] != 'absent': continue
        rs = [] if r['role'] == '*' else [r['role']]
        n += c.execute('delete from entity_concepts where entity=? and concept=?' + (' and role=?' if rs else ''), (res(r['entity']), r['concept'], *rs)).rowcount
        if not rs: c.execute('delete from trigger_effect where entity=? and (trigger=? or effect=?)', (res(r['entity']), r['concept'], r['concept']))
    c.commit(); print('reviewed drops re-applied:', n)
else:
    bad = []; n = 0
    for r in csv.DictReader(open(out, encoding='utf-8'), delimiter='\t'):
        n += 1
        args = [res(r['entity']), r['concept']] + ([] if r['role'] == '*' else [r['role']])
        have = bool(q('select 1 from entity_concepts where entity=? and concept=?' + ('' if r['role'] == '*' else ' and role=?'), *args))
        if not have and r['expect'] == 'present':   # parent and child rule: a reviewed parent is kept by a narrower concept
            have = bool(q('select 1 from entity_concepts where entity=? and concept in (select id from concept_tree where root=?)' + ('' if r['role'] == '*' else ' and role=?'), *args))
        if have != (r['expect'] == 'present'): bad.append(r)
    print(f'regression: {n - len(bad)}/{n} pass')
    for r in bad[:40]: print('  FAIL', r['game'], r['name'][:40], r['concept'], r['role'], 'expected', r['expect'])
    sys.exit(1 if bad else 0)
