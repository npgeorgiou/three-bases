# Writes factions/roster/STOP1.md (index) and STOP1-1..5.md: the 20 factions in plain words. Run from the repo root
# after themes.tsv, tools.tsv, combos.tsv and answers.tsv exist.
import collections
NAME=dict(deathfeed='my units grow from deaths',lastwords='Death effects',sacrifice='my unit dies and takes an enemy with it',
selfhurt='I damage my own units',revive='my dead units come back',recycle='spent cards come back from the discard pile',
returnhand='my unit goes back to hand and is placed again',tokens='extra small units',countboard='cards that count my units',
allyplay='my units react when allies are placed',adjacency='units beside each other give each other more',
movement='I move my own units',push='I push enemy units',lanes='my cards act in another lane',cells='claimed cells (NEW RULE)',
onattack='my attacks do something extra',overkill='the rest of a hit goes into the unit behind',
onkill='my unit gains when it kills',fight='my unit strikes a chosen enemy',ping='small hits',
area='hits on a whole row or area',kill='destroy outright',spelldmg='damage spells',spellpay='spells make my cards stronger',
hurt='my unit grows when it is hit and survives',silence="take an enemy's text away",weaken="take an enemy's strength away",
change='turn an enemy into another unit',hand="act on the enemy's hand and costs",junk='useless cards for the enemy',
supply='extra supply',cheaper='cheaper cards',inhand='cards grow in hand',draw='draw extra cards',create='create new cards',
copy='copy my cards',pick='pick cards from my deck',discard='discard my cards for an effect',heal='heal my units',
shield='shields',guard='my unit guards the others',hide="my unit can't be targeted",attach='attach a unit to a carrier (NEW RULE)',
roundstart='round start effects',leave='my units react when one leaves',bigstrength='units with strength 5+',
offering='my unit dies for supply, a card or strength',steal='take an enemy unit or card (NEW RULE)',
enemyside='place my units in the enemy camp (NEW RULE)',haste='attack the turn it is placed',extraact='my unit acts again',
mark='mark an enemy for later hits',reach='hit from afar into the back rows')
F='factions/roster/'
def tsv(p): return [l.rstrip('\n').split('\t') for l in open(p)][1:]
OWN={};EX={}
for l in open(F+'work/assign.tsv'):
    k,o,s=l.rstrip('\n').split('\t'); OWN[k]=o.split(','); EX[k]=s.split(',')
TH={p[0]:p[1] for p in tsv(F+'themes.tsv')}
TL=collections.defaultdict(list)
for p in tsv(F+'tools.tsv'): TL[p[0]].append(p+['']*(7-len(p)))
ANS={p[0]:p for p in tsv(F+'answers.tsv')}
CO=collections.defaultdict(list); rank={'STRONG':0,'OK':1}
for p in tsv(F+'combos.tsv'):
    if p[2] in rank: CO[p[0]].append((p[1],p)); CO[p[1]].append((p[0],p))
def faction(k):
    a=ANS[k]; nr=lambda p: ' (NEW RULE)' if 'NEW RULE' in p[6] else ''
    o=[f'## {k}: {TH.get(k, "")}: {a[1]}',
       '- Builds on: '+'; '.join(NAME[m] for m in OWN[k])+'. Extras: '+'; '.join(NAME[m] for m in EX[k])+'.']
    o+=[f'- Tool, {p[1]} (from {NAME[p[2]]}; feeds {p[3]}): {p[4]}{nr(p)}' for p in TL[k]]
    o+=[f'- Wins: {a[2]}',f'- Removes the unit facing my dot: {a[3]}',f'- Removes back-row units: {a[5]}',
        f'- Between lanes: {a[6]}',f'- Holds: {a[7]}',f'- Feels good: {a[8]}',f'- Never has: {a[10]}','']
    best={}
    for y,p in CO[k]:
        if y not in best or rank[p[2]]<rank[best[y][2]]: best[y]=p
    o.append(f'Combos with {len(best)} factions ({sum(p[2]=="STRONG" for p in best.values())} strong):')
    o+=[f'- {y} {p[2]}: {p[4]}' for y,p in sorted(best.items(),key=lambda t:(rank[t[1][2]],t[0]))]
    return o+['']
L=list(ANS)
idx=['# Stop 1: the 20 factions in plain words','Everything here is Claude\'s draft from the library and this board.',
'Combos: STRONG = both halves on many cards, helps take or hold a base, the enemy\'s one',
'action between can\'t easily stop it; OK = real but breakable. Playtests decide later; what doesn\'t work is dropped.','']
for i in range(5):
    part=L[i*4:(i+1)*4]; name=f'STOP1-{i+1}.md'; idx.append(f'- `{name}`: '+' '.join(part))
    open(F+name,'w').write('\n'.join([f'# Stop 1, part {i+1}: '+' '.join(part),'See `STOP1.md` for what the ratings mean.','']+sum((faction(k) for k in part),[])))
open(F+'STOP1.md','w').write('\n'.join(idx)+'\n')
print('ok')
