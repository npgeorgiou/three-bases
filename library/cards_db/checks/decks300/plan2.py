import pickle,collections,re,source
from lor_deckcodes import LoRDeck
out=pickle.load(open('/home/claude/work/plan.pkl','rb'))
c=source.lib()
rn={r[0]:r[1] for r in c.execute('select ext_id,name from entities where game="runeterra"')}
by=collections.defaultdict(list)
for k,v in rn.items():
  if re.fullmatch(r'\d\d[A-Z]{2}\d{3}',k): by[v].append(k)
R={'DE':'Demacia','FR':'Freljord','IO':'Ionia','NX':'Noxus','PZ':'Piltover','SI':'Shadow Isles','BW':'Bilgewater','SH':'Shurima','MT':'Targon','BC':'Bandle City'}
def main(codes_counts):
  cnt=collections.Counter()
  for x,k in codes_counts:
    r=x[2:4]
    if r in R: cnt[r]+=k
  top=[r for r,_ in cnt.most_common(2) if _>=4]
  return '+'.join(sorted(top)) or 'other'
ex=[l.rstrip('\n').split('\t') for l in open('decks.tsv') if l.startswith('runeterra\t')]
now=collections.Counter(main([(by[n][0],1) for n in p[3].split(', ') if by.get(n)]) for p in ex)
keep=out['runeterra'][2]
for d in keep: d['col']=main(d['cards'])
# plan: cap 4 per main pair, prefer pairs fewer now
grp=collections.defaultdict(list)
for d in keep: grp[d['col']].append(d)
plan=[]
for k,v in grp.items(): plan+=v[:4]
extra=[d for k,v in grp.items() for d in v[4:]]
plan+=extra[:max(0,200-len(plan))]
plan=plan[:200]
pc=collections.Counter(d['col'] for d in plan)
keys=sorted(set(now)|set(pc),key=lambda k:-(now[k]+pc[k]))
print('runeterra pairs:',len(keys),'now',sum(now.values()),'planned new',len(plan))
for k in keys: print(f'{k}\t{now[k]}\t{pc[k]}\t{now[k]+pc[k]}')
yrs=collections.Counter(d['dt'][:4] for d in plan); print('years',dict(yrs))
print('sources posts',len({d['slug'] for d in plan}))
out['runeterra_plan']=plan; out['runeterra_now']=now
pickle.dump(out,open('/home/claude/work/plan.pkl','wb'))
