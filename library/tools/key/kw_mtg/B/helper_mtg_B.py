import sys, json, os
# usage: helper_mtg_B.py <game> <tagsfile> <batch names...>
g, tf = sys.argv[1], sys.argv[2]; batches = sys.argv[3:]
base = f'/home/claude/three-bases/library/tools/key/kw_{g}'
tags = {}
for line in open(tf, encoding='utf-8'):
    line = line.rstrip('\n')
    if not line.strip(): continue
    i, c, w = [x.strip() for x in line.split('||', 2)]
    tags.setdefault(i, []).append([c, w])
for b in batches:
    out = {}
    for l in open(f'{base}/{b}.txt', encoding='utf-8'):
        if l.strip(): out[l.split(' | ')[0].strip()] = tags.get(l.split(' | ')[0].strip(), [])
    json.dump(out, open(f'{base}/B/{b}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    open(f'{base}/B/progress.txt', 'a').write(f'done {b}\n')
    print(b, len(out))
