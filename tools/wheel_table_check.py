# Checks the wheel chat's files (factions/START_DESIGN-1-wheel.md step 8) on real numbers, not only columns. Run from the repo root; prints FAIL lines and PASS or FAILED.
import csv,collections,itertools,re
R='factions/wheel/'; W='library/cards_db/wheel/'
fails=[]; info=[]
def fail(s): fails.append(s)
def tsv(p): return [l.rstrip('\n').split('\t') for l in open(p)][1:]
# library numbers
RL={}
for x in csv.DictReader(open(W+'radius_links.tsv'),delimiter='\t'):
    c=float(x['cards'] or 0); d=float(x['decks'] or 0); RL[(x['a'],x['b'])]=RL[(x['b'],x['a'])]=(d if 'spellpay' in (x['a'],x['b']) else c,d)
for p in [l.rstrip('\n').split('\t') for l in open(R+'work/radius_verdicts.tsv')]:
    if p[2]=='DROP': a,b=p[0].split('+'); RL[(a,b)]=RL[(b,a)]=(1.0,RL.get((a,b),(0,0))[1])
ML={}
for x in csv.DictReader(open(W+'links.tsv'),delimiter='\t'):
    ML[(x['a'],x['b'])]=ML[(x['b'],x['a'])]=(float(x['cards'] or 0),float(x['decks'] or 0))
strong=lambda n:n[0]>=1.5 or (n[0]>=1.2 and n[1]>=1.2)
ARG={(k,f,a,b) for k,a,b,f,_ in tsv(R+'arguments.tsv')}|{(k,f,b,a) for k,a,b,f,_ in tsv(R+'arguments.tsv')}
SIZE={p[0]:p[5] for p in tsv(R+'mechanics.tsv')}
NUM={'strong','tough','together'}
T={p[0]:p for p in tsv(R+'table.tsv')}; CIRC=[p[0] for p in tsv(R+'table.tsv')]
if len(CIRC)!=20: fail(f'{len(CIRC)} factions, 20 wanted')
OWN={k:T[k][5].split(',') for k in CIRC}
SH={k:[m.split('(')[0] for m in T[k][6].split(',')] for k in CIRC}
A={k:OWN[k]+SH[k] for k in CIRC}
SHAPE={k:dict((v.split('=')[0],float(v.split('=')[1])) for v in T[k][4].split(',')) for k in CIRC}
# 1. shapes: 3-6 radii, each joined to another of them by a strong number or an argument; no two the same
for i,k in enumerate(CIRC):
    r=[x for x in SHAPE[k] if x not in NUM]
    if not 3<=len(SHAPE[k])<=6: fail(f'{k}: {len(SHAPE[k])} radii')
    for a in r:
        if not any(strong(RL.get((a,b),(0,0))) or ('radius',k,a,b) in ARG for b in r if b!=a): fail(f'{k}: radius {a} joined to nothing')
for x,y in itertools.combinations(CIRC,2):
    if SHAPE[x]==SHAPE[y]: fail(f'{x}={y}: same shape')
# 2. owners and shares
owner={}
for k in CIRC:
    if len(OWN[k])!=2: fail(f'{k}: owns {len(OWN[k])}')
    for m in OWN[k]:
        if m in owner: fail(f'{m}: owned by {owner[m]} and {k}')
        owner[m]=k
for m in SIZE:
    if SIZE[m]!='SMALL' and m not in owner: info.append(f'{m}: not SMALL and no owner')
for k in CIRC:
    if not 4<=len(A[k])<=6: fail(f'{k}: {len(A[k])} mechanics, 4-6 wanted')
# 3. each faction's mechanics one connected group (strong number, deck number 1.5+, or an argument)
for k in CIRC:
    g=collections.defaultdict(set)
    for a,b in itertools.combinations(A[k],2):
        n=ML.get((a,b),(0,0))
        if strong(n) or n[1]>=1.5 or ('mechanic',k,a,b) in ARG: g[a].add(b); g[b].add(a)
    seen={A[k][0]}; st=[A[k][0]]
    while st:
        for y in g[st.pop()]-seen: seen.add(y); st.append(y)
    if len(seen)<len(A[k]): fail(f'{k}: mechanics not joined: {sorted(set(A[k])-seen)}')
# 4. combos (combos.tsv): every pair of factions judged once on this board; a library combo names a KEEP verdict;
#    partners = STRONG or OK combos (WEAK, NONE, AGAINST don't count); 10+ partners
V={}
for p in [l.rstrip('\n').split('\t') for l in open(R+'work/mechanic_pair_verdicts.tsv')]:
    a,b=p[0].split('+'); V[(a,b)]=V[(b,a)]=p[2]
P=collections.defaultdict(set); seen=set()
for x,y,r,c,how,src,*_ in tsv(R+'combos.tsv'):
    seen.add(frozenset((x,y)))
    if r not in ('STRONG','OK','WEAK','NONE','AGAINST'): fail(f'{x}{y}: rating {r}')
    if r!='NONE' and not how.strip(): fail(f'{x}{y}: no played sequence')
    if 'LIBRARY KEEP' in src:
        ab=src.split('LIBRARY KEEP')[1].split()[0].strip(',;')
        if '+' in ab and V.get(tuple(ab.split('+')[:2]))!='KEEP': fail(f'{x}{y}: {ab} is not a KEEP verdict')
    if r in ('STRONG','OK'): P[x].add(y); P[y].add(x)
for x in CIRC:
    for y in CIRC:
        if x<y and frozenset((x,y)) not in seen: fail(f'{x}{y}: pair not judged')
for k in CIRC:
    if len(P[k])<10: fail(f'{k}: {len(P[k])} partners (STRONG or OK)')
# 4b. board versions (board.tsv, step 7): 1-3 per faction, each on one of its mechanics, none shared, one idea each
B=collections.defaultdict(list); texts=set()
for k,m,thing,ver,src,nr in tsv(R+'board.tsv'):
    if m=='IDEA': continue
    if m not in A[k]: fail(f'{k}: board version on {m}, not its mechanic')
    if ver in texts: fail(f'{k}: board version shared: {ver[:40]}')
    texts.add(ver); B[k].append(m)
for k in CIRC:
    if not 1<=len(B[k])<=3: fail(f'{k}: {len(B[k])} board versions')
# 5. the five answers: all different; removal by one of its own mechanics; blind spot outside what the faction owns, uses and its radii; all blind spots different
for c,name in ((3,'archetype'),(9,'identity'),(10,'removal'),(12,'holding'),(13,'play'),(8,'blind spot')):
    d=collections.Counter(T[k][c] for k in CIRC)
    for v,n in d.items():
        if n>1: fail(f'{name} on {n} factions: {v}')
for k in CIRC:
    if T[k][11] not in A[k]: fail(f'{k}: removal uses {T[k][11]}, not one of its mechanics')
    for b in T[k][8].split(','):
        if b.startswith('radius:'):
            if b[7:] in SHAPE[k]: fail(f'{k}: blind spot radius {b[7:]} is in its shape')
        elif b in A[k]: fail(f'{k}: blind spot {b} is one of its mechanics')
        elif b not in SIZE: fail(f'{k}: blind spot {b} is no mechanic')
for s in info: print('note:',s)
for s in fails: print('FAIL',s)
print('partners:',' '.join(f'{k}{len(P[k])}' for k in CIRC))
print('PASS' if not fails else f'FAILED ({len(fails)})')
