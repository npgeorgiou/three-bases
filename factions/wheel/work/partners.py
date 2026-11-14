import csv,collections,itertools
exec(open('factions/wheel/work/check_assign.py').read().split("for k in CIRC:")[0])
cand=collections.defaultdict(list)
for x,y in itertools.combinations(CIRC,2):
    for a in A[x]:
        for b in A[y]:
            if a!=b and strong(a,b) and (a in OWN[x] or b in OWN[y]):
                c,d=LK[(a,b)]; cand[(x,y)].append((c+(d or 0)*0.5,a,b,c,d))
pairs=collections.Counter()
top={}
for k,v in cand.items():
    v.sort(reverse=True); top[k]=v[:2]
    for t in v[:2]: pairs[tuple(sorted((t[1],t[2])))]+=1
n=collections.Counter()
for (x,y) in cand: n[x]+=1; n[y]+=1
print('partners by numbers:',dict(n))
print(len(pairs),'mechanic pairs')
open('factions/wheel/work/mpairs.txt','w').write(','.join(f'{a}+{b}' for a,b in pairs))
import json; json.dump({f'{x}{y}':[list(t[1:]) for t in v] for (x,y),v in top.items()},open('factions/wheel/work/top.json','w'))
