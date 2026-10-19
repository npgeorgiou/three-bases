"""Step 3 of the tag-fix plan: narrowed and new wording patterns (build step after concept_tree.py apply, before parent_rule.py).
Decisions are in tools/step3/decisions.tsv, one per line (concept ids are the tree v3 ids):
  narrow  <concept|role|game or *|old regex>  <games, comma-separated>  <new regex>
  new     <concept|role|game>                 <game>                    <new regex>
A narrowed pattern stops tagging the matches it drops, but a tag is removed only when
  - the tag came from wording patterns (method text_pattern),
  - no other pattern of the same concept and role (general or the game's own) still matches the entry,
  - the entry is not known right for that concept: neither the answer key (tools/key) nor a judged sample (tools/step3) says so.
Known-right entries keep the tag (evidence 'kept: judged right, step 3'). A narrowing is listed in decisions.tsv only after a
sample of the matches it drops was judged and found 90%+ wrong in that game (tools/step3/patterns3.py accept).
New patterns tag their matches (method text_pattern). The concept_patterns table shows the narrowed and new patterns, and table
pattern_fixes lists every decision. Idempotent: other steps may re-derive older tags, and this step removes them again.
Usage: pattern_fix.py <db>"""
import collections, json, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); S3 = os.path.join(HERE, 'step3')
sys.path.insert(0, S3)
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
dec = []
f = os.path.join(S3, 'decisions.tsv')
if os.path.exists(f):
    for line in open(f, encoding='utf-8'):
        if not line.strip() or line.startswith('#'): continue
        kind, p, games, new = line.rstrip('\n').split('\t')
        dec.append((kind, p, games.split(','), new))
sys.path.insert(0, HERE)
from step_games import step_games
ALLOW = step_games('pattern_fix')
if ALLOW is not None: dec = [(k, p, [g for g in gs if g in ALLOW], n) for k, p, gs, n in dec]
if not dec:
    print('pattern fixes: none'); sys.exit(0)
import patterns3 as P
known = collections.defaultdict(set)   # concept -> entity ids known right
ky = P.keys()
for g, kk in ky.items():
    for e, ks in kk.items():
        for k in ks | {a for x in ks for a in P.K.ANC[x] if a not in P.K.GROUPS}: known[k].add(e)
if os.path.exists(os.path.join(S3, 'questions.json')):
    Q, ans, _, _ = P.answers()
    for qid, (e, k, d) in Q['q'].items():
        if ans.get(qid) is True: known[k].add(e)
import csv
sys.path.insert(0, HERE)
from concept_tree import primary
mk = dict(q('SELECT old_id, kept_id FROM merged_entities'))
for r in csv.DictReader(open(os.path.join(HERE, 'regression.tsv'), encoding='utf-8'), delimiter='\t'):
    if r['expect'] == 'present':
        for k in primary(r['concept']): known[k].add(mk.get(int(r['entity']), int(r['entity'])))
from concept_tree import REMOVED
dropped = {(mk.get(int(r['entity']), int(r['entity'])), primary(r['concept'])[0]) for r in csv.DictReader(open(os.path.join(HERE, 'regression.tsv'), encoding='utf-8'), delimiter='\t') if r['expect'] == 'absent' and r['concept'] not in REMOVED}
reviewed = {(mk.get(int(r['entity']), int(r['entity'])), x) for r in csv.DictReader(open(os.path.join(HERE, 'regression.tsv'), encoding='utf-8'), delimiter='\t') if r['expect'] == 'present' for x in primary(r['concept'])}
ents = collections.defaultdict(list)
for i, g, n, t in q('SELECT id, game, name, text FROM entities'): ents[g].append((i, P.norm_text(g, n, t)))
games_all = [g for g, in q('SELECT id FROM games')]
c.execute('CREATE TABLE IF NOT EXISTS pattern_fixes(kind TEXT, concept TEXT, role TEXT, game TEXT, old TEXT, new TEXT)')
c.execute('DELETE FROM pattern_fixes')
removed = kept = added = 0
for kind, p, games, new in dec:
    k, role, g, pat = p.split('|', 3); nrx = re.compile(new, re.I)
    if kind == 'new':
        for gg in games:
            c.execute('INSERT OR IGNORE INTO concept_patterns VALUES(?,?,?,?)', (k, role, new, gg))
            for e, t in ents[gg]:
                m = nrx.search(t)
                if m and (e, k) not in dropped: added += c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (e, k, role, 'text_pattern', t[max(0, m.start() - 20): m.start() + 40])).rowcount
            c.execute('INSERT INTO pattern_fixes VALUES(?,?,?,?,?,?)', ('new', k, role, gg, None, new))
        continue
    orx = re.compile(pat, re.I)
    for gg in games:
        others = [re.compile(x, re.I) for x, in q('SELECT pattern FROM concept_patterns WHERE concept=? AND role=? AND (game IS NULL OR game=?) AND pattern!=?', k, role, gg, pat)]
        have = {e for e, in q("SELECT entity FROM entity_concepts WHERE concept=? AND role=? AND method='text_pattern'", k, role)}
        for e, t in ents[gg]:
            if not orx.search(t) or nrx.search(t): continue
            if e in known[k]:   # never where a hand review dropped the concept (regression.tsv 'absent', applied earlier)
                if (e, k) not in dropped: kept += c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (e, k, role, 'text_pattern', 'kept: judged right, step 3')).rowcount
                continue
            if any((e, x) in reviewed for x in P.K.ANC[k] - P.K.GROUPS): continue   # the tag is what keeps a reviewed broader concept
            if e in have and not any(o.search(t) for o in others):
                removed += c.execute("DELETE FROM entity_concepts WHERE entity=? AND concept=? AND role=? AND method='text_pattern'", (e, k, role)).rowcount
                if not q('SELECT 1 FROM entity_concepts WHERE entity=? AND concept=?', e, k):
                    c.execute('DELETE FROM trigger_effect WHERE entity=? AND (trigger=? OR effect=?)', (e, k, k))
        c.execute('INSERT INTO pattern_fixes VALUES(?,?,?,?,?,?)', ('narrow', k, role, gg, pat, new))
    reach = [g] if g != '*' else [x for x in games_all if x != 'marvel_snap']
    gnull = None if g == '*' else g
    if set(reach) <= set(games):
        c.execute('UPDATE concept_patterns SET pattern=? WHERE concept=? AND role=? AND pattern=? AND game IS ?', (new, k, role, pat, gnull))
    else:
        for gg in games: c.execute('INSERT OR IGNORE INTO concept_patterns VALUES(?,?,?,?)', (k, role, new, gg))
c.commit()
print('pattern fixes:', len(dec), 'decisions; tags removed', removed, ', known-right tags kept', kept, ', added by new patterns', added)
