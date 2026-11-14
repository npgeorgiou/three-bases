# Writes factions/wheel/STOP1.md: the 20 factions in plain words for Kaptain's Stop 1. Run from the repo root after make_table.py.
import collections
NAME=dict(deathfeed='my units grow from deaths',lastwords='Death effects',sacrifice='my unit dies and takes an enemy with it',
selfhurt='I damage my own units',revive='my dead units come back',recycle='spent cards come back from the discard pile',
returnhand='my unit goes back to hand and is placed again',tokens='extra small units',countboard='cards that count my units',
allyplay='my units react when allies are placed',adjacency='units beside each other give each other more',
movement='I move my own units',push='I push enemy units',lanes='my cards act in another lane',cells='claimed cells (NEW RULE)',
onattack='my attacks do something extra',strikes='strike twice or first',overkill='the rest of a hit goes into the unit behind',
onkill='my unit gains when it kills',fight='my unit strikes a chosen enemy',ping='small fixed damage, often',
area='hits on a whole row or area',kill='destroy outright',spelldmg='damage spells',spellpay='spells make my cards stronger',
hurt='my unit acts when hit and it survives',silence='take an enemy\'s text away',weaken='take an enemy\'s strength away',
change='turn an enemy into another unit',hand='act on the enemy\'s hand and costs',junk='useless cards and units for the enemy',
supply='extra supply',cheaper='cheaper cards',inhand='cards grow in hand',draw='draw extra cards',create='create new cards',
copy='copy my cards',pick='pick cards from my deck',discard='discard my cards for an effect',heal='heal my units',
shield='shields',guard='my unit guards the others',hide='my unit can\'t be targeted',attach='attach a unit to a carrier (NEW RULE)',
roundstart='round start effects',leave='my units react when one leaves',bigstrength='units with strength 5+',
offering='my unit dies for supply, a card or strength')
RAD=dict(strong='strength',grows='grows strength',strikes='strikes more or first',textdmg="damage from units' text",kills='kills outright',
many='many at once',spelldmg='damage from spells',spellpay='rewards playing spells',stops='stops them',disrupts='breaks their plan',
one='one chosen',supply='more supply',cheaper='cheaper hand',cards='more cards',picks='picks and copies',back='brings back',
wide='many cheap units',spends='spends them',together='position and combos',heals='heals them',growsdef='grows defence',
protects='protects them',tough='defence',tall='a few big units')
T=[l.rstrip('\n').split('\t') for l in open('factions/wheel/table.tsv')][1:]
P=collections.defaultdict(list)
for l in list(open('factions/wheel/partners.tsv'))[1:]:
    x,y=l.split('\t')[:2]; P[x].append(y); P[y].append(x)
o=['# Stop 1: the 20 factions in plain words','Made from `table.tsv` and `partners.tsv` by `work/make_stop1.py`. Letters only, no themes yet. The five answers',
'and archetypes are Claude\'s draft. A value: 1 = an average real faction, 1.8 = much more than average.','']
for p in T:
    k,arch,radii,own,ex=p[0],p[3],p[4],p[5],p[6]
    o+=[f'## {k}: {arch}',
        'Strong in: '+', '.join(f"{RAD[r.split('=')[0]]} {r.split('=')[1]}" for r in radii.split(','))+'.',
        'Builds on: '+'; '.join(NAME[m] for m in own.split(','))+'. Extras: '+'; '.join(NAME[m.split('(')[0]] for m in ex.split(','))+'.',
        f'Wins by: {p[9]}. Removes: {p[10]}. Holds: {p[12]}. Feels good: {p[13]}. Never has: {p[7]}.',
        f'Combos with {len(P[k])} factions: '+' '.join(sorted(P[k]))+'.','']
open('factions/wheel/STOP1.md','w').write('\n'.join(o))
print(len(o),'lines')
