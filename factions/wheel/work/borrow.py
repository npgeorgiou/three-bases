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
ARG={(l.split('\t')[1],l.split('\t')[2]) for l in list(open(F+'arguments.tsv'))[1:] if l.startswith('mechanic')}
ARG|={(b,a) for a,b in ARG}
linked=lambda a,b: ok(LK.get((a,b),(0,0))) or (a,b) in ARG
MIN,MAX,CAP=25,4,3  # CAP: an extra in at most 3 factions (Kaptain, 15 Nov 2026); factions with the fewest choices pick first
# partners second: a tie on radii is broken by how many factions a strong library number joins it to (numbers only)
V={(a,b) for (a,b),n in LK.items() if ok(n)}
def partners(k,m): return len({j for j in OWN if j!=k and any((m,o) in V for o in OWN[j])})
CANDS={}
for k in OWN:
    c=[]
    for m in M:
        if m in OWN[k]: continue
        r=max([(M[m].get(x,0),x) for x in SHAPE[k]])
        lk=[o for o in OWN[k] if linked(m,o)]
        if r[0]>=15 and lk: c.append((r[0],partners(k,m),m,r[1],lk))
    c.sort(reverse=True); CANDS[k]=[(r,m,x,lk) for r,_,m,x,lk in c]
used={}; PICK={}
for k in sorted(OWN,key=lambda k:len(CANDS[k])):
    c=CANDS[k]; full=lambda t: used.get(t[1],0)>=CAP
    pick=[t for t in c if t[0]>=MIN and not full(t)][:MAX]
    if len(pick)<2: pick+=[t for t in c if t[0]<MIN and not full(t)][:2-len(pick)]  # fallback: 15%+ on its radii
    # every signature mechanic joined to the other or to an extra; else the last extra gives way to one linked to it
    for o in OWN[k]:
        other=[x for x in OWN[k] if x!=o][0]
        if not linked(o,other) and not any(o in t[3] for t in pick):
            alt=[t for t in c if o in t[3] and t not in pick and not full(t)]
            if alt: pick=pick[:-1]+alt[:1]
    for t in pick: used[t[1]]=used.get(t[1],0)+1
    PICK[k]=pick
out=[]
for k in OWN:
    pick=PICK[k]
    out.append(f"{k}\t{','.join(OWN[k])}\t{','.join(p[1] for p in pick)}")
    if '-v' in sys.argv:
        print(k,'owns',','.join(OWN[k]),'| borrows',' '.join(f"{m}({x} {r}%, with {'/'.join(lk)})" for r,m,x,lk in pick))
if '--write' in sys.argv: open(F+'work/assign.tsv','w').write('\n'.join(out)+'\n')
