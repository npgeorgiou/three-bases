import json,sys
b=sys.argv[1]; y=sys.argv[2].split(); n=sys.argv[3].split()
q=[l.split(' | ')[0].rstrip('*').strip() for l in open(b+'.txt') if l[0].isdigit()]
assert set(y+n)==set(q) and len(y+n)==len(q),(set(q)-set(y+n),set(y+n)-set(q),len(y+n),len(q))
json.dump({k:('yes' if k in y else 'no') for k in q},open('A/'+b+'.json','w'))
open('A/progress_003.txt','a').write('done '+b+'\n')
