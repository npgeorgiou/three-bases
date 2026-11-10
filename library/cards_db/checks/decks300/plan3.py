import pickle,collections
out=pickle.load(open('/home/claude/work/plan.pkl','rb'))
nowc,nowa,keep=out['faeria']
grp=collections.defaultdict(list)
for d in keep: grp[d['col']].append(d)
target=221
# trim the biggest groups first, dropping the least-liked
while sum(len(v) for v in grp.values())>target:
  k=max(grp,key=lambda k:len(grp[k])+nowc[k])
  v=grp[k]; v.remove(min(v,key=lambda d:d['lk']))
plan=[d for v in grp.values() for d in v]
pc=collections.Counter(d['col'] for d in plan)
NAME={'B':'blue','G':'green','R':'red','Y':'yellow','N':'neutral only'}
for k in sorted(set(nowc)|set(pc),key=lambda k:(len(k),k)):
  print('+'.join(NAME[x] for x in k) if k!='N' else 'neutral only',nowc[k],pc[k],nowc[k]+pc[k],sep='\t')
pa=collections.Counter(d['ar'] for d in plan)
for a in sorted(set(nowa)|set(pa)): print(a,nowa[a],pa[a],nowa[a]+pa[a],sep='\t')
print('years',dict(sorted(collections.Counter(d['dt'][-4:] for d in plan).items())),'authors',len({d['a'] for d in plan}))
out['faeria_plan']=plan; pickle.dump(out,open('/home/claude/work/plan.pkl','wb'))
