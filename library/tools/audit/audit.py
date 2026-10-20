"""Tag audit helpers (12 Oct 2026 handover: one worker per game). Prints counts and sampled lines only.
  audit.py defs                                  every concept as id | definition (load once per worker)
  audit.py sample <game>                         200 entries, seed 1: 150 work + 50 held-out -> audit/<game>_sample.json;
                                                 the held-out tags as they are now -> audit/<game>_before.json (workers never read it)
  audit.py show <game> <batch>                   work entries of batch 0, 1 or 2 (50 each): id | name | text | tags
  audit.py trial <game> add <concept> <role> <regex>    a new game pattern: entries of the game gaining the tag, 30 random gains
  audit.py trial <game> drop <concept> <regex>          a '!concept|regex' line: entries losing the tag, 30 random losses
  audit.py source <game> <concept>               where the game's tags of a concept come from: count per method, and for wording
                                                 patterns each pattern exactly as stored with how many tagged entries it matches
  audit.py confirm <game>                        every current tag of the work entries that the review does not drop is written into
                                                 the game's review as confirmed (add)
  audit.py blind <game>                          held-out entries with the tags before (snapshot) and after (database), shuffled
                                                 as A and B per entry -> audit/<game>_blind.txt; the key -> audit/<game>_key.json
  audit.py score <game> <judgments.json>         unblinds the checker's judgments: wrong tags and missed mechanics per 100 entries,
                                                 before and after, and correct tags lost
A trial also counts the changed entries whose locked decision it would undo (regression.tsv and the game's review file).
Judgments file: {"<id>": {"A": {"wrong": ["concept:role", ...], "missed": ["short note", ...]}, "B": {...}}, ...}
The database is library/three-bases-library.sqlite unless TB_LIB is set."""
import json, os, random, re, sqlite3, sys
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))); import reading as RD   # how patterns read text
here = os.path.dirname(os.path.abspath(__file__))
DB = os.environ.get('TB_LIB', os.path.join(os.path.dirname(os.path.dirname(here)), 'three-bases-library.sqlite'))
c = sqlite3.connect(DB); q = lambda s, *a: c.execute(s, a).fetchall()
f = lambda g, k: os.path.join(here, f'{g}_{k}')
rvf = lambda g: os.path.join(os.path.dirname(here), 'reviews', g + '.json')

def locked(g, con, exp):   # entries whose reviewed decision says concept con must be present / absent
    import csv
    out = {int(r['entity']) for r in csv.DictReader(open(os.path.join(os.path.dirname(here), 'regression.tsv'), encoding='utf-8'), delimiter='\t')
           if r['game'] == g and r['concept'] == con and r['expect'] == exp}
    if os.path.exists(rvf(g)):
        for k, r in json.load(open(rvf(g), encoding='utf-8')).items():
            if k.isdigit() and any(x.split(':')[0] == con for x in r.get('add' if exp == 'present' else 'drop', [])): out.add(int(k))
    return out

def tags(e):
    return sorted(k + ('' if r == 'does' else ':' + r) for k, r in q('SELECT concept, role FROM entity_concepts WHERE entity=?', e))

def line(e, ts=None):
    n, t = q('SELECT name, text FROM entities WHERE id=?', e)[0]
    return f"{e} | {n} | {re.sub(r'\s+', ' ', t or '')} | {', '.join(tags(e) if ts is None else ts)}"

def read(g, t, nm):   # as game_patterns.py reads an entry
    low = t.lower()
    low = RD.strip(g, low)
    for x in [nm] + nm.split(' // '):
        if len(x) > 2: low = low.replace(x.lower(), 'name')
    return low

cmd, *a = sys.argv[1:]
if cmd == 'defs':
    for i, d in q('SELECT id, description FROM concepts ORDER BY id'): print(i, '|', d)
elif cmd == 'sample':
    g = a[0]
    if os.path.exists(f(g, 'sample.json')): sys.exit('sample exists: ' + f(g, 'sample.json'))
    ids = [i for (i,) in q("SELECT id FROM entities WHERE game=? AND category != 'tribe' AND text IS NOT NULL ORDER BY id", g)]
    s = random.Random(1).sample(ids, 200)
    json.dump({'game': g, 'seed': 1, 'work': s[:150], 'held_out': s[150:]}, open(f(g, 'sample.json'), 'w'), indent=0)
    json.dump({str(e): tags(e) for e in s[150:]}, open(f(g, 'before.json'), 'w'), indent=0)
    print(g, 'entries', len(ids), 'work 150, held-out 50 saved')
elif cmd == 'show':
    g, b = a[0], int(a[1])
    for e in json.load(open(f(g, 'sample.json')))['work'][b * 50:(b + 1) * 50]:
        if q('SELECT 1 FROM entities WHERE id=?', e): print(line(e))
        else: print(e, '| (merged or removed)')
elif cmd == 'trial':
    g, mode = a[0], a[1]
    if mode == 'add': con, role, p = a[2], a[3], re.compile(a[4], re.I)
    else: con, role, p = a[2], None, re.compile(a[3], re.I)
    ch = []
    if mode == 'add':
        have = {e for (e,) in q('SELECT entity FROM entity_concepts WHERE concept=? AND role=?', con, role)}
        for e, t, nm in q("SELECT id, text, name FROM entities WHERE game=? AND text IS NOT NULL AND category != 'tribe'", g):
            if e not in have and p.search(read(g, t, nm)): ch.append(e)
    else:
        others = [(r, re.compile(x, re.I)) for x, r in q('SELECT pattern, role FROM concept_patterns WHERE concept=? AND (game IS NULL OR game=?)', con, g) if x != a[3]]
        for e, t, r in q("SELECT e.id, e.text, ec.role FROM entity_concepts ec JOIN entities e ON e.id=ec.entity WHERE e.game=? AND ec.concept=? AND ec.method='text_pattern'", g, con):
            low = (t or '').lower()
            if p.search(low) and not any(rr == r and o.search(low) for rr, o in others): ch.append(e)
    lk = locked(g, con, 'absent' if mode == 'add' else 'present')
    print(f"{'gaining' if mode == 'add' else 'losing'} {con}: {len(ch)} entries; undoing a locked decision: {len(set(ch) & lk)}")
    for e in random.Random(7).sample(ch, min(30, len(ch))): print(line(e))
elif cmd == 'source':
    g, con = a[0], a[1]
    print('methods:', q('SELECT ec.method, ec.role, count(*) FROM entity_concepts ec JOIN entities e ON e.id=ec.entity WHERE e.game=? AND ec.concept=? GROUP BY 1, 2 ORDER BY 3 DESC', g, con))
    rows = q("SELECT e.text, e.name FROM entity_concepts ec JOIN entities e ON e.id=ec.entity WHERE e.game=? AND ec.concept=? AND ec.method='text_pattern'", g, con)
    for p, gg, r in q('SELECT pattern, game, role FROM concept_patterns WHERE concept=? AND (game IS NULL OR game=?)', con, g):
        try: rx = re.compile(p, re.I)
        except re.error: continue
        k = sum(1 for t, nm in rows if rx.search(read(g, t or '', nm)))
        if k: print(f"{'general' if gg is None else 'game'} {r} {k} | {p}")
elif cmd == 'confirm':
    g = a[0]; s = json.load(open(f(g, 'sample.json'))); d = json.load(open(rvf(g), encoding='utf-8')) if os.path.exists(rvf(g)) else {}
    n = 0
    for e in s['work']:
        if not q('SELECT 1 FROM entities WHERE id=?', e): continue
        r = d.setdefault(str(e), {'add': [], 'drop': []}); r.setdefault('add', []); r.setdefault('drop', [])
        dropped = {x if ':' in x else x + ':does' for x in r['drop']} | {x for x in r['drop'] if ':' not in x}
        for t in tags(e):
            full = t if ':' in t else t + ':does'
            if t in dropped or full in dropped or t.split(':')[0] in dropped or t in r['add']: continue
            r['add'].append(t); n += 1
    json.dump(d, open(rvf(g), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(g, 'confirmed tags added to the review:', n)
elif cmd == 'blind':
    g = a[0]; s = json.load(open(f(g, 'sample.json'))); before = json.load(open(f(g, 'before.json')))
    rnd = random.Random(11); key = {}; out = []
    for e in s['held_out']:
        aft = tags(e) if q('SELECT 1 FROM entities WHERE id=?', e) else []
        v = [('before', before[str(e)]), ('after', aft)]; rnd.shuffle(v); key[str(e)] = {'A': v[0][0], 'B': v[1][0]}
        n, t = q('SELECT name, text FROM entities WHERE id=?', e)[0] if q('SELECT 1 FROM entities WHERE id=?', e) else ('?', '?')
        out.append(f"{e} | {n} | {re.sub(r'\s+', ' ', t or '')}\n  A: {', '.join(v[0][1]) or '(none)'}\n  B: {', '.join(v[1][1]) or '(none)'}")
    open(f(g, 'blind.txt'), 'w').write('\n'.join(out) + '\n'); json.dump(key, open(f(g, 'key.json'), 'w'), indent=0)
    print('blind file written:', f(g, 'blind.txt'), len(out), 'entries')
elif cmd == 'score':
    g = a[0]; j = json.load(open(a[1])); key = json.load(open(f(g, 'key.json'))); before = json.load(open(f(g, 'before.json')))
    s = json.load(open(f(g, 'sample.json')))
    desc = {}
    for r, i in q('SELECT root, id FROM concept_tree'): desc.setdefault(r, set()).add(i)
    w = {'before': 0, 'after': 0}; m = {'before': 0, 'after': 0}; lost = []
    for e in s['held_out']:
        k = key[str(e)]; jj = j.get(str(e), {})
        for v in 'AB':
            w[k[v]] += len(jj.get(v, {}).get('wrong', [])); m[k[v]] += len(jj.get(v, {}).get('missed', []))
        vb = 'A' if k['A'] == 'before' else 'B'
        wrong_b = set(jj.get(vb, {}).get('wrong', []))
        aft = set(tags(e)) if q('SELECT 1 FROM entities WHERE id=?', e) else set()
        aft_c = {x.split(':')[0] for x in aft}
        for t in before[str(e)]:
            if t in wrong_b or t in aft: continue
            base, role = (t.split(':') + ['does'])[:2]
            if any((d + ('' if role == 'does' else ':' + role)) in aft for d in desc.get(base, ()) if d != base): continue   # kept by a narrower concept
            lost.append(f'{e} {t}')
    n = len(s['held_out']) / 100
    print(f"wrong tags per 100: before {w['before'] / n:.1f} after {w['after'] / n:.1f}")
    print(f"missed mechanics per 100: before {m['before'] / n:.1f} after {m['after'] / n:.1f}")
    print('correct tags lost:', len(lost), ' '.join(lost[:20]))
