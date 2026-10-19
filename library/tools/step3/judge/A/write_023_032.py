import json,sys,re
n=sys.argv[1]; yes=set(sys.argv[2].split(',')) if sys.argv[2] else set()
q=[l.split('|')[0].strip().rstrip('*') for l in open(f'{n}.txt') if l[0].isdigit()]
assert yes<=set(q), yes-set(q)
json.dump({k:('yes' if k in yes else 'no') for k in q},open(f'A/{n}.json','w'),indent=0)
open('A/progress_023.txt','a').write(f'done {n}\n'); print(len(q),len(yes))
