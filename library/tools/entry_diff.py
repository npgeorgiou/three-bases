"""Per key entry of one game: the library tags the key calls wrong (with the method that made each, first 6 letters) and the key
concepts the library misses, scored as key.py does. Start here: it shows where each error comes from (text_pattern = a pattern,
claude_review = a review file, via_keyword = inherited from a keyword entry). Usage: entry_diff.py <db> <game> [category|all] [text chars]"""
import collections, os, sqlite3, sys
db, g = sys.argv[1], sys.argv[2]; cat = sys.argv[3] if len(sys.argv) > 3 else 'all'; mx = int(sys.argv[4]) if len(sys.argv) > 4 else 160
os.environ['TB_LIB'] = os.path.abspath(db); HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE, os.path.join(HERE, 'key')]
import key as K
c = sqlite3.connect(db); key = K.load(g); ids = [int(i) for i in key]
meth = collections.defaultdict(dict)
for e, k, m in c.execute('SELECT entity, concept, method FROM entity_concepts WHERE entity IN (%s)' % ','.join(map(str, ids))): meth[e][k] = m
L = K.lib_tags(c, ids); W = M = 0; byw = collections.Counter(); bym = collections.Counter()
for i in ids:
    r = c.execute('SELECT name, text, category FROM entities WHERE id=?', (i,)).fetchone()
    if not r or (cat != 'all' and r[2] != cat): continue
    Kt = K.narrow({k for k, _ in key[str(i)]['tags']})
    ok = set(Kt) | {a for k in Kt for a in K.ANC[k]} | {d for k in Kt for d in K.DESC[k]}
    wr = sorted(f'{l}({meth[i].get(l, "?")[:6]})' for l in L[i] if l not in ok and l not in K.GROUPS)
    mi = sorted(k for k in Kt if not (L[i] & ({k} | K.DESC[k] | (K.ANC[k] - K.GROUPS))))
    W += len(wr); M += len(mi); byw.update(wr); bym.update(mi)
    if wr or mi: print(f'[{i}] {r[0]} <{r[2]}> wrong: {" ".join(wr)}  missed: {" ".join(mi)}  key={sorted(Kt)}\n    {(r[1] or "")[:mx]!r}')
print('wrong', W, 'missed', M); print('wrong by concept(method):', byw.most_common(15)); print('missed by concept:', bym.most_common(15))
