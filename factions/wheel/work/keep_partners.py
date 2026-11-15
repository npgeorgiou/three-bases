# Partners per faction counting only KEEP combos with a signature mechanic on one side (run from the repo root)
import collections,itertools
exec(open('factions/wheel/work/check_assign.py').read().split("for k in CIRC:")[0])
V={}
for p in [l.rstrip('\n').split('\t') for l in open('factions/wheel/work/mechanic_pair_verdicts.tsv')]:
    a,b=p[0].split('+'); V[(a,b)]=V[(b,a)]=p
P=collections.Counter(); rows=[]
for x,y in itertools.combinations(CIRC,2):
    found=[]
    for a in A[x]:
        for b in A[y]:
            if a!=b and V.get((a,b),[0,0,''])[2]=='KEEP' and (a in OWN[x] or b in OWN[y]):
                found.append(f'{a}+{b}')
    if found: P[x]+=1;P[y]+=1; rows.append((x,y,found))
print(' '.join(f'{k}{P[k]}' for k in CIRC))
print(len(rows),'pairs')
