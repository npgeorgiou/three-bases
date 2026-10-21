import json,sys
b=sys.argv[1]; y=sys.argv[2].split(); n=sys.argv[3].split()
d={q:"yes" for q in y}; d.update({q:"no" for q in n})
qs=[l.split('|')[0].strip().rstrip('*') for l in open(b+'.txt') if l[0].isdigit()]
assert set(qs)==set(d) and len(qs)==len(d) and not set(y)&set(n),(set(qs)^set(d))
json.dump(d,open('A/'+b+'.json','w'))
open('A/progress_033.txt','a').write('done '+b+'\n')
