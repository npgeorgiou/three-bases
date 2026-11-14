# Chooses each faction's borrowed mechanics by fit (Kaptain, 15 Nov 2026): fit first, partners second. Run from the repo root; writes work/assign.tsv.
# Fit of a mechanic for a faction (Claude's method, agreed in outline):
#   radii = the mechanic's highest share of its cards on one of the faction's radii (library/cards_db/wheel/measured.tsv);
#   link  = the mechanic is linked in the library with one of the faction's two owned mechanics (cards 1.5+, or cards and
#           decks 1.2+, or decks 1.5+: library/cards_db/wheel/links.tsv).
# A mechanic is borrowed when radii >= 25% and link holds; the best by radii, at most 4; never a mechanic the faction owns.
import csv,re,sys
W='library/cards_db/wheel/'; F='factions/wheel/'
OWN={};SH0={}
for l in open(F+'work/assign.tsv'):
    k,o,s=l.rstrip('\n').split('\t'); OWN[k]=o.split(','); SH0[k]=s.split(',')
SHAPE={l.split('\t')[0]:[x.split('=')[0] for x in l.strip().split('\t')[1].split(',')] for l in open(F+'work/shapes.tsv')}
M={}
for l in list(open(W+'measured.tsv'))[1:]:
    p=l.rstrip('\n').split('\t'); M[p[0]]={a:int(b) for a,b in re.findall(r'(\w+) (\d+)%',p[-1])}
LK={}
for x in csv.DictReader(open(W+'links.tsv'),delimiter='\t'):
    n=(float(x['cards'] or 0),float(x['decks'] or 0)); LK[(x['a'],x['b'])]=LK[(x['b'],x['a'])]=n
ok=lambda n:n[0]>=1.5 or (n[0]>=1.2 and n[1]>=1.2) or n[1]>=1.5
MIN,MAX=25,4
out=[]
for k in OWN:
    c=[]
    for m in M:
        if m in OWN[k]: continue
        r=max([(M[m].get(x,0),x) for x in SHAPE[k]])
        lk=[o for o in OWN[k] if ok(LK.get((m,o),(0,0)))]
        if r[0]>=MIN and lk: c.append((r[0],m,r[1],lk))
    c.sort(reverse=True); pick=c[:MAX]
    out.append(f"{k}\t{','.join(OWN[k])}\t{','.join(p[1] for p in pick)}")
    if '-v' in sys.argv:
        print(k,'owns',','.join(OWN[k]),'| borrows',' '.join(f"{m}({x} {r}%, with {'/'.join(lk)})" for r,m,x,lk in pick),'| was',','.join(SH0[k]))
if '--write' in sys.argv: open(F+'work/assign.tsv','w').write('\n'.join(out)+'\n')
