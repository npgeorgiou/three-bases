import sys,json,os
# usage: helper_mtg_A.py <game> <batch> <specfile>
game,batch,spec=sys.argv[1:4]
base='/home/claude/three-bases/library/tools/key/'
ents={}
for l in open(base+f'kw_{game}/{batch}.txt'):
    p=l.rstrip('\n').split(' | ',2)
    if len(p)<2: continue
    ents[p[0].strip()]=(p[1]+' '+(p[2] if len(p)>2 else ''), p[1], p[2] if len(p)>2 else '')
out={i:[] for i in ents}
for l in open(spec):
    l=l.strip()
    if not l or l.startswith('#'): continue
    parts=l.split(';')
    i=parts[0].strip()
    if i=='NOTKW':
        continue
    for t in parts[1:]:
        t=t.strip()
        if not t: continue
        c,w=t.split('=',1)
        c=c.strip();w=w.strip()
        e=ents[i]
        if w not in e[1] and w not in e[2]: print('BAD',i,c,w)
        out[i].append([c,w])
json.dump(out,open(base+f'kw_{game}/A/{batch}.json','w'),ensure_ascii=False)
open(base+f'kw_{game}/A/progress.txt','a').write(f'done {batch}\n')
print(len(out))
