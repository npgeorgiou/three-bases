"""Does the faction lead in a mechanic? Per case faction:concept, the share of the faction's cards with the concept (or a narrower
one) against the other factions' cards, from the answer key (what the card text shows) and from the library (roles does, grants,
cost, as signature.py counts). A case whose key ratio is under 1.5 cannot be met by honest tags: check the case and the key first.
Usage: case_lead.py <db> <game> <faction:concept> ..."""
import os, sqlite3, sys
db, g = sys.argv[1], sys.argv[2]
os.environ['TB_LIB'] = os.path.abspath(db); HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE, os.path.join(HERE, 'key')]
import key as K
from factions import members, tail
c = sqlite3.connect(db); q = lambda s, *a: c.execute(s, a).fetchall()
mem, allc = members(q, g); key = K.load(g); kt = {int(i): {t[0] for t in v['tags']} for i, v in key.items()}
for arg in sys.argv[3:]:
    f, k = arg.split(':'); ks = K.DESC[k] | {k}; F = mem[f]; O = allc - F
    lib = {e for e, in q(f"SELECT DISTINCT entity FROM entity_concepts WHERE role IN ('does','grants','cost') AND concept IN ({','.join('?' * len(ks))})", *ks)}
    for src, has in (('key', {i for i in allc if kt.get(i, set()) & ks}), ('library', lib & allc)):
        a, b = len(F & has), len(O & has); sf, so = a / len(F), b / max(len(O), 1)
        print(f'{f:14} {k:20} {src:8} {a:3}/{len(F):3} = {sf:4.2f}  rest {b:3}/{len(O):3} = {so:4.2f}  ratio {sf / so if so else float("inf"):5.2f}  p {tail(len(allc), len(has), len(F), a):.3f}')
