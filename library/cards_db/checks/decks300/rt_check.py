import source,collections
from lor_deckcodes import LoRDeck
c=source.lib()
code2name={r[0]:r[1] for r in c.execute('select ext_id,name from entities where game="runeterra"')}
bad=0; unk=collections.Counter(); n=0; ok=[]
for l in open('/home/claude/work/rt_pick.txt'):
  code,dt,slug=l.strip().split('|')
  try:
    d=LoRDeck.from_deckcode(code); cards=[(x.card_code,x.count) for x in d.cards]
  except Exception as e: bad+=1; print('BAD',code[:20],e); continue
  tot=sum(k for _,k in cards)
  if tot!=40: bad+=1; print('TOT',tot,code[:20]); continue
  m=[x for x,_ in cards if x not in code2name]
  for x in m: unk[x]+=1
  n+=1
print(n,bad,len(unk),unk.most_common(10))
