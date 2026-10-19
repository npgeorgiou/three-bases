# usage: python3 settle_wh_40k_10e_C.py <batch> <decisions>
# decisions lines: id concept concept=words concept@A ...   (bare concept: words from A, else B)
import json, sys, re, os
here = os.path.dirname(os.path.abspath(__file__)); gdir = os.path.dirname(here)
b, d = sys.argv[1], sys.argv[2]
ents, cur = {}, None
for ln in open(os.path.join(gdir, b + '.txt'), encoding='utf-8'):
    m = re.match(r'^(\d+) \| ', ln)
    if m: cur = m.group(1); ents[cur] = {'text': ln, 'A': [], 'B': []}; continue
    m = re.match(r'^\s+([AB]): (.*)$', ln)
    if m and cur: ents[cur][m.group(1)] = json.loads(m.group(2))
def norm(s): return re.sub(r'\s+', ' ', s.lower().replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')).strip()
out = {}
for ln in open(d, encoding='utf-8'):
    ln = ln.strip()
    if not ln: continue
    i, rest = ln.split(' ', 1) if ' ' in ln else (ln, '')
    tags = []
    for tok in re.findall(r'(\w+)(?:=("[^"]*"|\S+))?(?:@([AB]))?', rest):
        c, w, src = tok
        if w:
            w = w[1:-1] if w.startswith('"') else w
        else:
            srcs = [src] if src else ['A', 'B']
            w = next((x[1] for s in srcs for x in ents[i][s] if x[0] == c), None)
            if w is None: print('NO WORDS', i, c); continue
        if norm(w) not in norm(ents[i]['text']): print('BAD WORDS', i, c, w)
        tags.append([c, w])
    out[i] = tags
miss = set(ents) - set(out)
if miss: print('MISSING', miss)
json.dump(out, open(os.path.join(here, b + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('wrote', len(out))
