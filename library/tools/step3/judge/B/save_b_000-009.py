import json,sys
n=sys.argv[1]; s=sys.argv[2].split()
d={s[i]:("yes" if s[i+1]=="y" else "no") for i in range(0,len(s),2)}
qs=[l.split(' | ')[0].rstrip('*') for l in open(f'b_{n}.txt') if l[0].isdigit()]
assert set(qs)==set(d) and len(qs)==len(d),(set(qs)^set(d))
json.dump(d,open(f'B/b_{n}.json','w'),indent=0)
open('B/progress_000.txt','a').write(f'done {n}\n')
