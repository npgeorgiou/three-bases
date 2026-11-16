# Checks the wheel chat's files on real numbers (factions/START_DESIGN-1-wheel.md, "The check script"). Run from the
# repo root; prints FAIL lines and PASS or FAILED.
import csv,collections,itertools,re,os
R='factions/wheel/'; W='library/cards_db/wheel/'
fails=[]
def fail(s): fails.append(s)
def tsv(p): return [l.rstrip('\n').split('\t') for l in open(p)][1:]
strong=lambda n:n[0]>=1.5 or (n[0]>=1.2 and n[1]>=1.2)
RL={}
for x in csv.DictReader(open(W+'radius_links.tsv'),delimiter='\t'):
    c=float(x['cards'] or 0); d=float(x['decks'] or 0); RL[(x['a'],x['b'])]=RL[(x['b'],x['a'])]=(d if 'spellpay' in (x['a'],x['b']) else c,d)
ML={}
for x in csv.DictReader(open(W+'links.tsv'),delimiter='\t'):
    ML[(x['a'],x['b'])]=ML[(x['b'],x['a'])]=(float(x['cards'] or 0),float(x['decks'] or 0))
ARG=set()
for k,a,b,f,_ in tsv(R+'arguments.tsv'): ARG|={(k,f,a,b),(k,f,b,a)}
MECH={p[0] for p in tsv(R+'mechanics.tsv')}
NUM={'strong','tough','together'}
SHAPE={}
for l in open(R+'work/shapes.tsv'):
    k,v=l.rstrip('\n').split('\t'); SHAPE[k]={p.split('=')[0]:float(p.split('=')[1]) for p in v.split(',')}
OWN={};EX={}
for l in open(R+'work/assign.tsv'):
    k,o,s=l.rstrip('\n').split('\t'); OWN[k]=o.split(','); EX[k]=s.split(',')
CIRC=list(SHAPE)
A={k:OWN[k]+EX[k] for k in CIRC}
if len(CIRC)!=20: fail(f'{len(CIRC)} factions')
# shapes: 3-6 radii, each joined, no two the same
for k in CIRC:
    r=[x for x in SHAPE[k] if x not in NUM]
    if not 3<=len(SHAPE[k])<=6: fail(f'{k}: {len(SHAPE[k])} radii')
    for a in r:
        if not any(strong(RL.get((a,b),(0,0))) or ('radius',k,a,b) in ARG for b in r if b!=a): fail(f'{k}: radius {a} joined to nothing')
for x,y in itertools.combinations(CIRC,2):
    if SHAPE[x]==SHAPE[y]: fail(f'{x}={y}: same shape')
# signatures and extras
sig=collections.Counter(m for k in CIRC for m in OWN[k]); ex=collections.Counter(m for k in CIRC for m in EX[k])
for k in CIRC:
    if len(OWN[k])!=2: fail(f'{k}: {len(OWN[k])} signatures')
    if not 2<=len(EX[k])<=4: fail(f'{k}: {len(EX[k])} extras')
    for m in A[k]:
        if m not in MECH: fail(f'{k}: {m} is not in mechanics.tsv')
    if set(OWN[k])&set(EX[k]): fail(f'{k}: a signature is also its extra')
for m,n in sig.items():
    if n>1: fail(f'{m}: signature of {n} factions')
for m,n in ex.items():
    if n>3: fail(f'{m}: extra in {n} factions')
# each faction's mechanics one connected group
for k in CIRC:
    g=collections.defaultdict(set)
    for a,b in itertools.combinations(A[k],2):
        n=ML.get((a,b),(0,0))
        if strong(n) or n[1]>=1.5 or ('mechanic',k,a,b) in ARG: g[a].add(b); g[b].add(a)
    seen={A[k][0]}; st=[A[k][0]]
    while st:
        for y in g[st.pop()]-seen: seen.add(y); st.append(y)
    if len(seen)<len(A[k]): fail(f'{k}: mechanics not joined: {sorted(set(A[k])-seen)}')
# themes (step 7): one per faction, all different
import os
def need(f):
    if os.path.exists(R+f): return tsv(R+f)
    fail(f'{f} missing (step 7 not done)'); return []
TH={p[0]:p[1] for p in need('themes.tsv') if len(p)>1}
for k in CIRC:
    if not TH.get(k,'').strip(): fail(f'{k}: no theme')
for v,n in collections.Counter(t.lower() for t in TH.values()).items():
    if n>1: fail(f'theme of {n} factions: {v}')
# tools (step 7): faction, tool, mechanic, feeds (tools of the same faction), cells (played out cell by cell), source, new rule
TOOLS=collections.defaultdict(dict)
CELLS=r"front|middle|back|row|cell|column|lane"
for p in need('tools.tsv'):
    p+=['']*(7-len(p)); k,t,m,feeds,cells,src=p[:6]
    if k not in A: fail(f'tools.tsv: no faction {k}'); continue
    if t.lower() in TOOLS[k]: fail(f'{k}: tool {t} twice')
    TOOLS[k][t.lower()]=(m,[x.strip().lower() for x in feeds.split(',') if x.strip()],cells,src)
for k in CIRC:
    T=TOOLS[k]
    if not 2<=len(T)<=4: fail(f'{k}: {len(T)} tools')
    for t,(m,feeds,cells,src) in T.items():
        if m not in A[k]: fail(f'{k}: tool {t} grows from {m}, not its mechanic')
        if not any(f in T and f!=t for f in feeds): fail(f'{k}: tool {t} feeds no other tool of its faction')
        if len(cells)<40 or not re.search(CELLS,cells,re.I): fail(f'{k}: tool {t} not played out cell by cell')
        if not src.strip(): fail(f'{k}: tool {t} has no source (a library card or CLAUDE)')
    for m in OWN[k]:
        if not any(v[0]==m for v in T.values()): fail(f'{k}: signature {m} has no tool')
for t,n in collections.Counter(t for k in CIRC for t in TOOLS[k]).items():
    if n>1: fail(f'tool {t} in {n} factions')
# combos: every pair rated once, 10+ partners (STRONG or OK)
C=tsv(R+'combos.tsv'); best={}
order={'STRONG':4,'OK':3,'WEAK':2,'NONE':1,'AGAINST':0}
for p in C:
    key=frozenset(p[:2])
    if p[2] not in order: fail(f'{p[0]}{p[1]}: rating {p[2]}')
    if p[2]!='AGAINST': best[key]=max(best.get(key,0),order.get(p[2],0))
for x,y in itertools.combinations(CIRC,2):
    if frozenset((x,y)) not in best: fail(f'{x}{y}: no combo line')
P=collections.Counter()
for key,v in best.items():
    if v>=3:
        for k in key: P[k]+=1
for k in CIRC:
    if P[k]<10: fail(f'{k}: {P[k]} partners')
# the seven answers: present, all different, front removal by its own mechanic, blind spot outside its mechanics
ANS={p[0]:p for p in tsv(R+'answers.tsv')}
cols=['archetype','wins','front','front_key','backrow','lanes','holds','place','blind_key','blind']
for k in CIRC:
    if k not in ANS: fail(f'{k}: no answers'); continue
    a=dict(zip(cols,ANS[k][1:]))
    for c in cols:
        if not a.get(c,'').strip(): fail(f'{k}: no {c}')
    if a.get('front_key') not in A[k]: fail(f'{k}: front removal uses {a.get("front_key")}, not its mechanic')
    if a.get('blind_key') in A[k] or a.get('blind_key') not in MECH: fail(f'{k}: blind spot {a.get("blind_key")} is its own or no mechanic')
for i,c in enumerate(cols):
    if c=='front_key': continue
    for v,n in collections.Counter(ANS[k][i+1].lower() for k in ANS).items():
        if n>1: fail(f'{c} on {n} factions: {v[:60]}')
# 10. rule check of the words: things this game doesn't have (summary/05-06: who starts alternates, an attacked unit
#     doesn't hit back, nothing is placed at round end)
import re
BAD=r"(move|moves|play|plays|act|acts|go|goes) first|strikes? (him |it |them )?first|first strike|placed at round end|place[sd]? .{0,20}at round end"
for t in ('so I move first next round','my hidden unit strikes him first','a unit placed at round end has struck'):
    assert re.search(BAD,t,re.I), t  # the three errors Kaptain's Stop 1 had (15 Nov 2026)
for f in ('answers.tsv','tools.tsv','themes.tsv'):
    for row in (tsv(R+f) if os.path.exists(R+f) else []):
        for cell in row:
            if re.search(BAD,cell,re.I): fail(f'{f} {row[0]}: breaks a rule of this game: {cell[:70]}')
for s in fails: print('FAIL',s)
print('partners:',' '.join(f'{k}{P[k]}' for k in CIRC))
print('PASS' if not fails else f'FAILED ({len(fails)})')
