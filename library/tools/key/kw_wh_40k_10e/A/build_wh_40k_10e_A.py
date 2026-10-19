import json,sys,re,os
D=os.path.dirname(os.path.abspath(__file__)); G=os.path.dirname(D)
spec=open(os.path.join(D,'spec.txt')).read().split('\n')
out={}
for fn in sorted(f for f in os.listdir(G) if re.match(r'batch_\d+\.txt$',f)):
    ents={}
    for l in open(os.path.join(G,fn)):
        l=l.rstrip('\n')
        if not l.strip(): continue
        i,n,t=(l.split(' | ',2)+[''])[:3]; ents[i.strip()]=(n,t)
    out[fn[:-4]]={i:[] for i in ents}
    cur=None
    for s in spec:
        if s.startswith('#'):
            m=re.match(r'#(\w+)',s); continue
    out[fn[:-4]]['_ents']=ents
notkw=[]
for s in spec:
    s=s.strip()
    if not s or s.startswith('#'): continue
    if s.startswith('NOTKW'):
        notkw+=s.split()[1:]; continue
    i,c,w=[x.strip() for x in s.split('|',2)]
    done=False
    for b,d in out.items():
        if i in d:
            n,t=d['_ents'][i]
            if w not in n and w not in t: print('BAD',i,c,repr(w))
            d[i].append([c,w]); done=True
    if not done: print('NOID',i)
for b,d in out.items():
    d.pop('_ents'); json.dump(d,open(os.path.join(D,b+'.json'),'w'),indent=0,ensure_ascii=False)
    open(os.path.join(D,'progress.txt'),'a').write('done '+b+'\n')
json.dump(notkw,open(os.path.join(D,'notkw.json'),'w'))
