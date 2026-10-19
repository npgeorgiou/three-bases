import sys,json,re
n=sys.argv[1]; no=set(sys.argv[2].split(',')) if len(sys.argv)>2 and sys.argv[2] else set()
out={}
for l in open(f'{n}.txt'):
    m=re.match(r'^(\d+)\*?\s*\|',l)
    if m: out[m.group(1)]='no' if m.group(1) in no else 'yes'
assert no<=set(out), no-set(out)
json.dump(out,open(f'A/{n}.json','w'),indent=0)
open('A/progress_043.txt','a').write(f'done {n}\n')
print(n,len(out),sum(v=='no' for v in out.values()))
