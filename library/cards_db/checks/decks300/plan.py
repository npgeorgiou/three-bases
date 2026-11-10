import source,collections,re
from lor_deckcodes import LoRDeck
c=source.lib()
def names(g): return {r[0]:r[1] for r in c.execute('select ext_id,name from entities where game=?',(g,))}
ex=collections.defaultdict(list)
for l in open('decks.tsv'):
  p=l.rstrip('\n').split('\t')
  if p[0]!='game': ex[p[0]].append(p)
def sim(a,b): return len(a&b)/max(len(a),len(b))
# archetype from the source's own label words (word list is Claude's)
AR=[('rush',r'\b(rush|aggro|face|burn|swarm|tempo|weenie|blitz|dash|fast)\b'),('control',r'\b(control|controll?ol|mill|lock|handlock)\b'),
    ('combo',r'\b(combo|otk|wombo)\b'),('ramp',r'\b(ramp|big)\b'),('midrange',r'\b(mid-?range|mid|value)\b')]
def arch(name):
  s=name.lower()
  for a,r in AR:
    if re.search(r,s): return a
  return 'not labelled'
out={}
# FAERIA
fn=names('faeria'); col={}
for e,f in c.execute('select ext_id,faction from entities where game="faeria"'):
  col[e]={'Blue':'B','Green':'G','Red':'R','Yellow':'Y'}.get(f)
n2code={v:k for k,v in fn.items()}
exs=[set(p[3].split(', ')) for p in ex['faeria']]
exnames={p[1] for p in ex['faeria']}
exids={m.group(1) for p in ex['faeria'] for m in [re.search(r'/deck/(\d+)',p[2])] if m}
def fcol(cards): return ''.join(sorted({col.get(x) for x in cards if col.get(x)})) or 'N'
cand=[]
for l in open('/home/claude/work/faeria_pick.txt'):
  i,n,a,dt,lk,cs=l.rstrip('\n').split('|')
  cards=[(t.partition('x')[0],int(t.partition('x')[2] or 1)) for t in cs.split()]
  s={fn[x] for x,_ in cards}
  if i in exids or any(sim(s,e)>0.8 for e in exs): continue
  cand.append(dict(i=i,n=n,a=a,dt=dt,lk=int(lk),cards=cards,s=s,col=fcol([x for x,_ in cards]),ar=arch(n)))
keep=[]
for d in cand:
  if all(sim(d['s'],k['s'])<=0.8 for k in keep): keep.append(d)
nowc=collections.Counter(); nowa=collections.Counter()
for p in ex['faeria']:
  nowc[fcol([n2code.get(x) for x in p[3].split(', ')])]+=1; nowa[arch(p[1])]+=1
out['faeria']=(nowc,nowa,keep)
# RUNETERRA
rn=names('runeterra'); reg={e:f for e,f in c.execute('select ext_id,faction from entities where game="runeterra"')}
rn2={v:k for k,v in rn.items()}
exs=[set(p[3].split(', ')) for p in ex['runeterra']]
def rreg(codes):
  r=sorted({x[2:4] for x in codes})
  return '+'.join(r)
cand=[]; seen=set()
for l in open('/home/claude/work/rt_pick.txt'):
  code,dt,slug=l.strip().split('|')
  if code in seen: continue
  seen.add(code)
  try: cards=[(x.card_code,x.count) for x in LoRDeck.from_deckcode(code).cards]
  except Exception: continue
  s={rn.get(x,'?'+x) for x,_ in cards}
  if any(sim(s,e)>0.8 for e in exs): continue
  cand.append(dict(code=code,dt=dt,slug=slug,cards=cards,s=s,col=rreg([x for x,_ in cards]),ar='not labelled'))
keep=[]
for d in cand:
  if all(sim(d['s'],k['s'])<=0.8 for k in keep): keep.append(d)
nowc=collections.Counter()
for p in ex['runeterra']:
  nowc[rreg([rn2[x] for x in p[3].split(', ') if x in rn2])]+=1
out['runeterra']=(nowc,collections.Counter({'not labelled':len(ex['runeterra'])}),keep)
import pickle; pickle.dump(out,open('/home/claude/work/plan.pkl','wb'))
for g,(nc,na,k) in out.items():
  print(g,'now',sum(nc.values()),'candidates',len(k))
  print(' colours now',dict(nc.most_common()))
  print(' colours cand',dict(collections.Counter(d['col'] for d in k).most_common()))
  print(' arch now',dict(na),' cand',dict(collections.Counter(d['ar'] for d in k)))
