# Partners per faction from read combos: X and Y are partners when a mechanic of X and one of Y (one of them owned) have a KEEP or WEAK verdict.
import collections,itertools,sys
exec(open('factions/wheel/work/check_assign.py').read().split("for k in CIRC:")[0])
V={}
for l in open('factions/wheel/work/mechanic_pair_verdicts.tsv'):
    p=l.rstrip('\n').split('\t')
    if len(p)<3: continue
    a,b=p[0].split('+'); V[(a,b)]=V[(b,a)]=p[2].strip()
need_own='any' not in sys.argv
P=collections.defaultdict(set)
for x,y in itertools.combinations(CIRC,2):
    for a in A[x]:
        for b in A[y]:
            if a!=b and V.get((a,b)) in ('KEEP','WEAK') and (not need_own or a in OWN[x] or b in OWN[y]):
                P[x].add(y); P[y].add(x)
print(' '.join(f'{k}{len(P[k])}' for k in CIRC))
