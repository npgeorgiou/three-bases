import csv, itertools, random
L={}
for x in csv.DictReader(open('/home/claude/three-bases/library/cards_db/wheel/radius_links.tsv'),delimiter='\t'):
    a,b=x['a'],x['b']
    v=float(x['decks'] or 0) if 'spellpay' in (a,b) else float(x['cards'] or 0)
    L[(a,b)]=L[(b,a)]=v
for line in open('factions/wheel/work/radius_verdicts.tsv'):
    p=line.rstrip('\n').split('\t')
    if p[2]=='DROP':
        a,b=p[0].split('+'); L[(a,b)]=L[(b,a)]=1.0
NUM={'strong','tough','together'}
F={}
for line in open('shapes.tsv'):
    k,v=line.rstrip('\n').split('\t'); F[k]={p.split('=')[0]:float(p.split('=')[1]) for p in v.split(',')}
def score(x,y):
    vals=[L.get((a,b),1.0) for a in F[x] for b in F[y] if a!=b and a not in NUM and b not in NUM]
    return sum(vals)/len(vals) if vals else 0
K=sorted(F); S={(x,y):score(x,y) for x in K for y in K if x!=y}
def tot(c): return sum(S[(c[i],c[(i+1)%len(c)])] for i in range(len(c)))
best=None
random.seed(1)
for t in range(400):
    c=K[:]; random.shuffle(c); imp=True
    while imp:
        imp=False
        for i in range(1,len(c)-1):
            for j in range(i+1,len(c)):
                d=c[:i]+c[i:j+1][::-1]+c[j+1:]
                if tot(d)>tot(c)+1e-9: c=d; imp=True
    if not best or tot(c)>tot(best): best=c
i=best.index('A'); best=best[i:]+best[:i]
print(' '.join(best), round(tot(best),2))
for n,x in enumerate(best):
    l,r=best[n-1],best[(n+1)%20]
    rank=sorted((y for y in K if y!=x), key=lambda y:-S[(x,y)])
    print(x, l, round(S[(x,l)],2), rank.index(l)+1, r, round(S[(x,r)],2), rank.index(r)+1, 'top:',' '.join(f'{y}{S[(x,y)]:.2f}' for y in rank[:4]))
