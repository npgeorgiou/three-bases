# Step 5a: each faction's 2 signature mechanics (rule written in START_DESIGN-1-wheel.md step 5). Run from the repo root.
# Fit of a mechanic for a faction = sum over the faction's radii of (radius value x share of the mechanic's cards on that
# radius) (library/cards_db/wheel/measured.tsv). The two signatures must be linked: library level 1+ (any link made
# by the two) or decks 1.5+ or an argument in arguments.tsv. Each mechanic is a signature of one faction
# at most. A pair needs 3+ other mechanics on the faction's radii linked to it, so extras exist. Fixed by Kaptain: G = hurt + selfhurt. The best total fit over all 20 is found by an exact solver (milp).
import csv,re,itertools,sys
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds
W='library/cards_db/wheel/';F='factions/wheel/'
FIXED={'G':('hurt','selfhurt')}
SHAPE={}
for l in open(F+'work/shapes.tsv'):
    k,v=l.rstrip('\n').split('\t'); SHAPE[k]={p.split('=')[0]:float(p.split('=')[1]) for p in v.split(',')}
MECH=[l.split('\t')[0] for l in list(open(F+'mechanics.tsv'))[1:]]
SH={}
for l in list(open(W+'measured.tsv'))[1:]:
    p=l.rstrip('\n').split('\t'); SH[p[0]]={a:int(b)/100 for a,b in re.findall(r'(\w+) (\d+)%',p[-1])}
LK={}
for x in csv.DictReader(open(W+'links.tsv'),delimiter='\t'):
    n=(float(x['level'] or 0),float(x['decks'] or 0)); LK[(x['a'],x['b'])]=LK[(x['b'],x['a'])]=n
ARG=set()
for l in list(open(F+'arguments.tsv'))[1:]:
    p=l.split('\t')
    if p[0]=='mechanic': ARG|={(p[1],p[2]),(p[2],p[1])}
MINFIT=float(sys.argv[sys.argv.index("--min")+1]) if "--min" in sys.argv else 0.8  # every signature fits its faction at least this well
ok=lambda n:n[0]>=1 or n[1]>=1.5
linked=lambda a,b: ok(LK.get((a,b),(0,0))) or (a,b) in ARG
onr=lambda k,m: max([SH.get(m,{}).get(r,0) for r in SHAPE[k]]+[0])>=0.25
extras=lambda k,a,b: sum(1 for m in MECH if m not in (a,b) and onr(k,m) and (linked(m,a) or linked(m,b)))
fit=lambda k,m: sum(v*SH.get(m,{}).get(r,0) for r,v in SHAPE[k].items())
V=[]
for k in SHAPE:
    if k in FIXED: V.append((k,)+FIXED[k]); continue
    for a,b in itertools.combinations(MECH,2):
        if linked(a,b) and fit(k,a)>=MINFIT and fit(k,b)>=MINFIT and extras(k,a,b)>=3: V.append((k,a,b))
c=-np.array([fit(k,a)+fit(k,b) for k,a,b in V])
A=[];lo=[];hi=[]
for k in SHAPE: A.append([1 if v[0]==k else 0 for v in V]); lo.append(1); hi.append(1)
for m in MECH: A.append([1 if m in v[1:] else 0 for v in V]); lo.append(0); hi.append(1)
r=milp(c,constraints=LinearConstraint(np.array(A),lo,hi),integrality=np.ones(len(V)),bounds=Bounds(0,1))
if not r.success: sys.exit('no assignment: '+r.message)
pick={v[0]:v[1:] for v,x in zip(V,r.x) if x>0.5}
old={l.split('\t')[0]:l.rstrip('\n').split('\t')[2] for l in open(F+'work/assign.tsv')}
out=[]
for k in SHAPE:
    a,b=pick[k]; print(k,a,round(fit(k,a),2),b,round(fit(k,b),2))
    out.append(f'{k}\t{a},{b}\t{old.get(k,"")}')
if '--write' in sys.argv: open(F+'work/assign.tsv','w').write('\n'.join(out)+'\n')
