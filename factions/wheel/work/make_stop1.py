# Writes factions/wheel/STOP1.md (index) and STOP1-1..5.md: the 20 factions in plain words, one line per answer, one line
# per partner with how the combo plays and its rating. Run from the repo root after make_board.py and make_answers.py.
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
BV=collections.defaultdict(list); ID={}
for k,m,thing,ver,src,nr in [l.rstrip('\n').split('\t') for l in open('factions/wheel/board.tsv')][1:]:
    if m=='IDEA': ID[k]=ver
    else: BV[k].append(ver+(f' ({nr})' if nr not in ('-','') else ''))
RANK={'STRONG':0,'OK':1,'WEAK':2,'NONE':3,'AGAINST':4}
best={}
for l in list(open('factions/wheel/combos.tsv'))[1:]:
    x,y,r,c,how=l.rstrip('\n').split('\t')[:5]
    for a,b in ((x,y),(y,x)):
        if (a,b) not in best or RANK[r]<RANK[best[(a,b)][0]]: best[(a,b)]=(r,how)
    if r=='AGAINST': best[('!',x,y)]=(r,how)
GROUPS=['A T I L','M E D J','H Q G F','R N P C','S B K O']
idx=['# Stop 1: the 20 factions in plain words',
'Letters only, no themes yet. Everything is Claude\'s draft except the strong radii (measured on real factions).',
'Board versions: how the faction\'s mechanics work on this board (step 7; source in `board.tsv`). Combo ratings',
'(`combos.tsv`, judged by agents on this board): STRONG = both halves on many cards, helps take or hold a base, the',
'enemy\'s one action between can\'t easily stop it; OK = real but breakable; WEAK = barely a combo. Partners = STRONG',
'or OK. Playtests will fill the test column of combos.tsv; what doesn\'t work is dropped.','',
*[f'- `STOP1-{i}.md`: {g}' for i,g in enumerate(GROUPS,1)],'']
for gi,g in enumerate(GROUPS,1):
    o=[f'# Stop 1, part {gi}: {g}','See `STOP1.md` for what the ratings mean.','']
    for p in [t for t in T if t[0] in g.split()]:
        k,arch,radii,own,ex=p[0],p[3],p[4],p[5],p[6]
        ps=sorted([y for (a,y) in [q for q in best if len(q)==2] if a==k], key=lambda y:(RANK[best[(k,y)][0]],y))
        good=[y for y in ps if best[(k,y)][0] in ('STRONG','OK')]
        o+=[f'## {k}: {arch}',
            '- Strong in: '+', '.join(f"{RAD[r.split('=')[0]]} {r.split('=')[1]}" for r in radii.split(','))+'.',
            '- Builds on: '+'; '.join(NAME[m] for m in own.split(','))+'. Extras: '+'; '.join(NAME[m.split('(')[0]] for m in ex.split(','))+'.']
        o+=[f'- On the board: {v}.' for v in BV[k]]
        o+=[f'- Faction idea: {ID[k]}.',
            f'- Wins: {p[9]}.', f'- Removes: {p[10]}.', f'- Holds: {p[12]}.', f'- Feels good: {p[13]}.', f'- Never has: {p[7]}.',
            f'',f'Combos with {len(good)} factions ({sum(best[(k,y)][0]=="STRONG" for y in good)} strong):']
        o+=[f'- {y} {best[(k,y)][0]}: {best[(k,y)][1]}' for y in good]
        weak=[y for y in ps if best[(k,y)][0] in ('WEAK','NONE')]
        if weak: o.append('- Weak or none: '+' '.join(weak)+'.')
        ag=[(q[1] if q[2]==k else q[2],best[q][1]) for q in best if len(q)==3 and k in q[1:]]
        o+=[f'- Against {y}: {h}' for y,h in ag]
        o.append('')
    open(f'factions/wheel/STOP1-{gi}.md','w').write('\n'.join(o))
open('factions/wheel/STOP1.md','w').write('\n'.join(idx))
print('ok')
