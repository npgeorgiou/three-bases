"""Per mechanic of the game file's ```mechanics block: the entries whose text matches its regex but lack its concept (or a narrower one),
N=<n> examples each (name | text start | tags). Usage: mechanic_gaps.py <db> <game> [mechanic name ...]"""
import sqlite3, sys, re, os, collections
import os as _o; sys.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import games, reading as RD
db, G, only = sys.argv[1], sys.argv[2], sys.argv[3:] 
c = sqlite3.connect(db); q = lambda s, *a: c.execute(s, a).fetchall()
tree = collections.defaultdict(set)
for r_, i_ in q('SELECT root, id FROM concept_tree'): tree[r_].add(i_)
ents = q("SELECT id, name, text FROM entities WHERE game=? AND category NOT IN ('keyword','tribe') AND text IS NOT NULL", G)
for ln in games.block(games.path(G), 'mechanics'):
    if not ln.strip() or ln.startswith('#'): continue
    name, con, rx = ln.rstrip('\n').split('|', 2)
    if only and name not in only: continue
    want = tree.get(con, {con}); r = re.compile(rx, re.I)
    miss = [(i, n, t) for i, n, t in ents if r.search(RD.strip(G, t.lower())) and not q('SELECT 1 FROM entity_concepts WHERE entity=? AND concept IN (%s)' % ','.join('?'*len(want)), i, *want)]
    print(f'== {name} ({con}) missing {len(miss)}')
    for i, n, t in miss[:int(os.environ.get('N', 12))]:
        tags = ','.join(sorted({k for k, in q('SELECT concept FROM entity_concepts WHERE entity=?', i)}))
        print(f'  {n} | {t[:160]!r} | {tags[:120]}')
