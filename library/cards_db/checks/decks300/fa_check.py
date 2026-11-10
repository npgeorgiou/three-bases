import sys,source,csv,collections
c=source.lib()
code2name={r[0]:r[1] for r in c.execute('select ext_id,name from entities where game="faeria"')}
ex=[l.rstrip('\n').split('\t') for l in open('decks.tsv') if l.startswith('faeria\t')]
exnames={e[1] for e in ex}
exsets=[collections.Counter(dict((n,1) for n in e[3].split(', '))) for e in ex]
exids=set()
import re
for e in ex:
  m=re.search(r'/deck/(\d+)',e[2]); 
  if m: exids.add(m.group(1))
rows=[]; unk=collections.Counter(); bad=0
for l in open('/home/claude/work/faeria_pick.txt'):
  i,n,a,dt,lk,cs=l.rstrip('\n').split('|')
  cards=[]
  for t in cs.split():
    cid,_,k=t.partition('x'); cards.append((cid,int(k or 1)))
  tot=sum(k for _,k in cards)
  miss=[x for x,_ in cards if x not in code2name]
  for m in miss: unk[m]+=1
  rows.append((i,n,a,dt,lk,cards,tot,miss))
print(len(rows),'tot!=30:',sum(r[6]!=30 for r in rows),'with unknown:',sum(bool(r[7]) for r in rows),'in existing by id:',sum(r[0] in exids for r in rows))
print('unknown ids',unk.most_common(40))
