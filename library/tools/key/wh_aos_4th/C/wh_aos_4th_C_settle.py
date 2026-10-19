import json,sys,re,os
# usage: script batchname decisions.txt
d=os.path.dirname(os.path.abspath(__file__))
batch=sys.argv[1]; dec=open(sys.argv[2]).read()
src=open(os.path.join(d,'..',batch+'.txt')).read().splitlines()
entries={};order=[];cur=None
for l in src:
    m=re.match(r'^(\d+) \| ',l)
    if m: cur=m.group(1);order.append(cur);entries[cur]={'text':l,'A':[],'B':[]};continue
    m=re.match(r'^\s+([AB]): (.*)$',l)
    if m and cur: entries[cur][m.group(1)]=json.loads(m.group(2))
decs={}
for line in dec.splitlines():
    line=line.strip()
    if not line: continue
    parts=line.split(' ;; ')
    decs[parts[0].split()[0]]=parts
out={}
for i in order:
    e=entries[i]
    p=decs.get(i,[i+' U'])
    head=p[0].split()
    base=head[1] if len(head)>1 else 'U'
    if base=='A': tags=list(e['A'])
    elif base=='B': tags=list(e['B'])
    elif base=='N': tags=[]
    else:
        tags=list(e['A']);seen={t[0] for t in tags}
        for t in e['B']:
            if t[0] not in seen: tags.append(t);seen.add(t[0])
    for op in head[2:]:
        if op.startswith('-'): tags=[t for t in tags if t[0]!=op[1:]]
    for op in p[1:]:
        c,w=op.split('|',1)
        if c.startswith('-'): tags=[t for t in tags if not (t[0]==c[1:] and t[1]==w)]; continue
        c=c.lstrip('+')
        tags=[t for t in tags if not (t[0]==c and op.startswith('='))] if False else tags
        if c.startswith('='): c=c[1:]; tags=[t for t in tags if t[0]!=c]
        tags.append([c,w])
    # dedupe
    seen=set();fin=[]
    for t in tags:
        k=(t[0],t[1])
        if k in seen: continue
        seen.add(k);fin.append(t)
    # verify words
    low=e['text'].split(' | ',1)[1]
    for t in fin:
        if t[1] not in low: print('WORDS?',i,t)
    out[i]=fin
json.dump(out,open(os.path.join(d,batch+'.json'),'w'),indent=0)
print('wrote',len(out))
