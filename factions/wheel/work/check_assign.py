import csv,collections
W='/home/claude/three-bases/library/cards_db/wheel/'
LK={}
for x in csv.DictReader(open(W+'links.tsv'),delimiter='\t'):
    a,b=x['a'],x['b']; f=lambda v: float(v) if v else None
    LK[(a,b)]=LK[(b,a)]=(f(x['level']),f(x['decks']))
def strong(a,b):
    c,d=LK.get((a,b),(None,None)); c=c or 0; d=d or 0
    return c>=1  # the library links them at all (level 1+)
def deck(a,b):
    c,d=LK.get((a,b),(None,None)); return (d or 0)>=1.5
CIRC='A T I L M E D J H Q G F R N P C S B K O'.split()
NB={k:(CIRC[i-1],CIRC[(i+1)%20]) for i,k in enumerate(CIRC)}
SIZE={l.split('\t')[0]:l.rstrip('\n').split('\t')[5] for l in list(open('/home/claude/three-bases/factions/wheel/mechanics.tsv'))[1:]}
A={};OWN={};SH={}
for l in open('factions/wheel/work/assign.tsv'):
    k,o,s=l.rstrip('\n').split('\t'); OWN[k]=o.split(','); SH[k]=s.split(','); A[k]=OWN[k]+SH[k]
owner={m:k for k in OWN for m in OWN[k]}
users=collections.defaultdict(list)
for k in A:
    for m in A[k]: users[m].append(k)
for k in CIRC:
    bad=[m for m in SH[k] if m in owner and owner[m] not in NB[k]]
    ms=A[k]; g=collections.defaultdict(set); argued=[]
    for i,a in enumerate(ms):
        for b in ms[i+1:]:
            if strong(a,b): g[a].add(b); g[b].add(a)
    def comps():
        seen=set(); cs=[]
        for m in ms:
            if m in seen: continue
            c={m}; st=[m]
            while st:
                x=st.pop()
                for y in g[x]-c: c.add(y); st.append(y)
            seen|=c; cs.append(c)
        return cs
    cs=comps()
    if len(cs)>1:
        for i,a in enumerate(ms):
            for b in ms[i+1:]:
                if deck(a,b) and not strong(a,b): g[a].add(b); g[b].add(a); argued.append(f'{a}-{b} decks {LK[(a,b)][1]}')
    cs2=comps()
    print(k, 'ok' if len(cs)==1 else ('decks-joined '+'; '.join(argued) if len(cs2)==1 else 'SPLIT '+str(cs2)), ('BAD SHARE '+str(bad)) if bad else '')
print('unowned OK:',[m for m in SIZE if SIZE[m]!='SMALL' and m not in owner])
print('small unowned users:',{m:users[m] for m in SIZE if m not in owner and users[m]})
