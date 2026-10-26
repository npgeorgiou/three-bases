"""Test candidate pattern lines against one game's answer key before putting them in a pattern file: per line, how many key entries
it would tag that the key has (right) or not (wrong), with the wrong matches. Reads text as the build does (lower case, own name as
'name'). Keyword entries pass their tags to every card that has them: the line also prints how many cards hold the matched
keywords. Usage: pattern_eval.py <db> <game> <file of concept|role|regex lines>"""
import os, re, sqlite3, sys
db, g, f = sys.argv[1:4]
os.environ['TB_LIB'] = os.path.abspath(db); HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE, os.path.join(HERE, 'key')]
import key as K
from concept_tree import TREE
c = sqlite3.connect(db); key = K.load(g)
holders = {d: n for d, n in c.execute("SELECT dst, count(*) FROM entity_links WHERE rel='has_keyword' GROUP BY dst")}
for line in open(f, encoding='utf-8'):
    if not line.strip() or line[0] in '#!': continue
    con, role, p = line.rstrip('\n').split('|', 2); rx = re.compile(p, re.I); R = W = H = 0; ws = []
    for i, n, t, cg in c.execute('SELECT id, name, text, category FROM entities WHERE game=?', (g,)):
        low = (t or '').lower(); low = low.replace(n.lower(), 'name') if len(n) > 2 else low
        m = rx.search(low)
        if not m: continue
        if cg == 'keyword': H += holders.get(i, 0)
        if str(i) not in key: continue
        Kt = K.narrow({k for k, _ in key[str(i)]['tags']})
        ok = set(Kt) | {a for k in Kt for a in K.ANC[k]} | {d for k in Kt for d in K.DESC[k]}
        if con in ok or (con not in TREE and any(con == x for x in Kt)): R += 1
        else: W += 1; ws.append(f'{n}: {low[max(0, m.start() - 30): m.end() + 15]!r}')
    print(f'{con:20} right {R:3} wrong {W:3} keyword holders {H:3}  {p[:70]}')
    for x in ws[:6]: print('     wrong', x[:160])
