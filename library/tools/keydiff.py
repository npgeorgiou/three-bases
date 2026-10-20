"""New wrong answer-key tags of a game, base vs another build, by concept and entry. Usage (from tools/): keydiff.py <game> <base.sqlite> <new.sqlite>"""
import collections, sqlite3, sys
sys.path.insert(0, 'key'); sys.path.insert(0, '.')
import key as K
g, A, B = sys.argv[1:4]
key = K.load(g)
def wrong(db):
    c = sqlite3.connect(db); live = {i for i, in c.execute('SELECT id FROM entities WHERE game=?', (g,))}
    ids = [int(i) for i in key if int(i) in live]; out = set(); nm = dict(c.execute('select id,name from entities where game=?', (g,)))
    T = collections.defaultdict(set)
    for e, k, m in c.execute('SELECT entity, concept, method FROM entity_concepts WHERE entity IN (%s)' % ','.join(map(str, ids))):
        if m in ('game_structure', 'data_rule'): continue
        if k in K.TREE and k not in K.NOT_IN_KEY: T[e].add(k)
    for i in ids:
        Kc = K.narrow({k for k, _ in key[str(i)]['tags']}); ok = set(Kc) | {a for k in Kc for a in K.ANC[k]} | {d for k in Kc for d in K.DESC[k]}
        for k in T[i]:
            if k not in ok and k not in K.GROUPS: out.add((i, nm[i], k))
    return out
a, b = wrong(A), wrong(B)
print('new wrong', len(b - a), collections.Counter(k for _, _, k in b - a).most_common(20))
for x in sorted(b - a, key=lambda x: x[2])[:60]: print('  +', x[2], '|', x[1])
print('fixed', len(a - b), collections.Counter(k for _, _, k in a - b).most_common(12))
