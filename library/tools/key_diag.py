"""Per concept, for one game: the library tags the key does not have (wrong) and the key concepts the library misses, most first,
with N examples each (name, text start, key concepts / library tags), scored as key.py score scores. TOP=<n> limits the concepts.
Usage: key_diag.py <db> <game> [N]"""
import sys, sqlite3, collections, os
sys.argv, args = sys.argv[:1], sys.argv[1:]
import os as _o; sys.path.insert(0, _o.path.join(_o.path.dirname(_o.path.abspath(__file__)), 'key')); import key as K
db, g = args[:2]; N = int(args[2]) if len(args) > 2 else 3
c = sqlite3.connect(db); key = K.load(g)
live = {i for i, in c.execute('SELECT id FROM entities WHERE game=?', (g,))}
ids = [int(i) for i in key if int(i) in live]; L = K.lib_tags(c, ids, False)
nm = dict(c.execute('SELECT id, name FROM entities WHERE game=?', (g,))); tx = dict(c.execute('SELECT id, text FROM entities WHERE game=?', (g,)))
W = collections.defaultdict(list); M = collections.defaultdict(list)
for i in ids:
    Kc = K.narrow({k for k, _ in key[str(i)]['tags']})
    ok = set(Kc) | {a for k in Kc for a in K.ANC[k]} | {d for k in Kc for d in K.DESC[k]}
    for l in L[i]:
        if l not in ok and l not in K.GROUPS: W[l].append(i)
    for k in Kc:
        if not (L[i] & ({k} | K.DESC[k] | (K.ANC[k] - K.GROUPS))): M[k].append((i, dict(key[str(i)]['tags']).get(k, '')))
print('WRONG (library tag not in key):')
for l, v in sorted(W.items(), key=lambda x: -len(x[1]))[:int(os.environ.get('TOP', 15))]:
    print(f' {len(v):3} {l}:', ' | '.join(f'{nm[i]}: {(tx[i] or "")[:90]!r} key={sorted(k for k,_ in key[str(i)]["tags"])}' for i in v[:N]))
print('MISSED (key concept not in library):')
for k, v in sorted(M.items(), key=lambda x: -len(x[1]))[:int(os.environ.get('TOP', 15))]:
    print(f' {len(v):3} {k}:', ' | '.join(f'{nm[i]} "{q}" lib={sorted(L[i])[:8]}' for i, q in v[:N]))
