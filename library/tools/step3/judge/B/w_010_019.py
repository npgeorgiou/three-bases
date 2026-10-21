import sys,json,re
n=sys.argv[1]; yes=set(sys.argv[2].split(',')) if sys.argv[2] else set()
q=[l.split('|')[0].strip().rstrip('*') for l in open(f'b_{n}.txt') if re.match(r'^\d+\*?\s*\|',l)]
assert yes<=set(q),yes-set(q)
json.dump({k:('yes' if k in yes else 'no') for k in q},open(f'B/b_{n}.json','w'),indent=0)
open('B/progress_010.txt','a').write(f'done {n}\n'); print(len(q),len(yes))
