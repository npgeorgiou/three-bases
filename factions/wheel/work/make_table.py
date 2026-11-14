# Writes factions/wheel/table.tsv (the 20 factions, Stop 1) and factions/wheel/partners.tsv (best read combo per faction pair). Run from the repo root.
import collections,itertools
exec(open('factions/wheel/work/check_assign.py').read().split("for k in CIRC:")[0])
SHAPE={l.split('\t')[0]:l.rstrip('\n').split('\t')[1] for l in open('factions/wheel/work/shapes.tsv')}
# Claude's draft of the five answers: identity | removal | holding | the play that feels good (Place) | blind spot words | blind spot key (mechanic or radius:<name>)
ANS={
'A':("my units die in the front cells and come back, and every death acts","a Death effect hits the enemy facing me","a front unit that dies comes back into its cell from the discard pile, so the dot is cancelled again at once","Place: an ally from my discard pile comes back into the cell behind me","shields","shield","death and return"),
'T':("my units pick their fights and grow from each kill","my unit strikes a chosen enemy","a unit that kills grows and stays in the front cell","Place: I strike the enemy facing me; if it dies I gain strength","area hits","area","duels"),
'I':("extra supply lands big units a round early","damage equal to the supply left in the lane","big units arrive before the enemy can cancel my dots and hold them by defence","Place: I add 1 to your carry-over","tokens","tokens","big units early"),
'L':("enemy units stay but lose their text and strength for good","strength and text taken away for good","the enemy facing my dot is weakened, so it can't kill my front unit","Place: the enemy facing me loses its text","revive","revive","weaken and silence"),
'M':("I turn the enemy's units and cards into useless ones","turn it into a weak unit","the enemy's next cards cost more or are useless, so his answer comes too late","Place: a useless card goes into the enemy's hand","+strength","radius:grows","change and junk"),
'E':("spells clear the lane and each spell makes my units stronger","damage spells","my units in the lane grow with each spell cast there","Place: I gain strength for each spell you cast this round","heal","heal","damage spells"),
'D':("I make more cards than my deck holds and spells pay for them","spells it creates","answers are created each round, so a lost front unit is always replaced","Place: a spell is created in your hand","strike twice or first","strikes","created cards"),
'J':("I find the exact card I need and play it twice","picks its removal from the deck","the holding card is picked from the deck when the base is in danger","Place: pick a card of your deck","silence","silence","pick and copy"),
'H':("I throw my own cards away for effect and play them again from the discard pile","a discarded card deals damage","discarded cards come back from the discard pile to replace lost units","Place: discard a card; it acts","guard","guard","discard and return"),
'Q':("small hits and pushes keep enemies off the cells facing my dots","push it out of the front row","an enemy placed facing my dot takes small damage at once","Place: push the enemy facing me one row back","return to hand","returnhand","push and ping"),
'G':("my front units strike first and win every trade","strikes first","an enemy that attacks my first striker dies before it hits","Place: I attack the enemy facing me at once, striking first","damage spells","spelldmg","first strike"),
'F':("wounded units heal, grow and hold the front","a healed unit grows and strikes","at round start my front units heal","Place: restore an ally's defence; it gains strength","offering","offering","heal and grow"),
'R':("units ride on carriers that can't be targeted","a carrier strikes with its riders' strength (NEW RULE)","a carrier that can't be targeted holds the front cell","Place: I attach to an ally; it gets my stats and text (NEW RULE)","ping","ping","riders"),
'N':("one guard takes every hit behind its shields","a shielded guard strikes back","a shielded guard in the front cell takes every enemy attack","Place: the ally beside me gets a shield","movement","movement","guard and shield"),
'P':("a few huge units whose hits go through to the row behind","the rest of the hit goes into the unit behind","few units with big defence hold two front cells each","Place: an ally with strength 5+ gets a shield","cheaper cards","cheaper","huge units"),
'C':("row hits clear many enemies, and every death grows my units","hit the whole front row","my units grow from every death on both sides, so the front gets harder to kill","Place: 1 damage to every enemy in the row facing me","one chosen","radius:one","row hits"),
'S':("I fill my camp, and every unit placed makes the others react","damage equal to my units in the lane","a full camp: every placement makes the units already there stronger","Place: my allies in this lane gain strength","pick and copy","pick,copy","full camp"),
'B':("my units die on purpose for supply and cards, and move to fill the gap","my unit dies and takes the enemy facing it","a back unit moves into the front cell the moment a front unit dies","Place: the ally behind me dies; its supply goes to your carry-over","draw","draw","offerings"),
'K':("I destroy outright and take my units back to hand to do it again","destroy outright, back to hand, again","a hurt front unit goes back to hand before it dies and is placed again","Place: the ally beside me goes back to your hand","defence growth","radius:growsdef","destroy and return"),
'O':("many small units stand together and give each other more","damage for each ally beside me","small units fill every front cell and each gains from the allies beside it","Place: a small unit appears beside me","units of cost 6+","radius:tall","small units together"),
}
RK=dict(A='lastwords',T='fight',I='supply',L='weaken',M='change',E='spelldmg',D='create',J='pick',H='discard',Q='push',G='strikes',F='heal',R='attach',N='guard',P='overkill',C='area',S='countboard',B='sacrifice',K='kill',O='adjacency')  # the mechanic each removal uses
def who(m): return owner.get(m,'SMALL')
rows=['faction\tleft\tright\tarchetype\tstrong radii\towns\tshared with left\tshared with right\tshared, small unowned\tblind spot\tblind key\tidentity\tremoval\tremoval mechanic\tholding\tthe play that feels good']
for k in CIRC:
    l,r=NB[k]; i,rem,hold,play,bw,bk,arch=ANS[k]
    sl=','.join(m for m in SH[k] if who(m)==l); sr=','.join(m for m in SH[k] if who(m)==r); ss=','.join(m for m in SH[k] if who(m)=='SMALL')
    rows.append('\t'.join([k,l,r,arch,SHAPE[k],','.join(OWN[k]),sl or '-',sr or '-',ss or '-',bw,bk,i,rem,RK[k],hold,play]))
open('factions/wheel/table.tsv','w').write('\n'.join(rows)+'\n')
V={}
for ln in open('factions/wheel/work/mechanic_pair_verdicts.tsv'):
    p=ln.rstrip('\n').split('\t'); a,b=p[0].split('+'); V[(a,b)]=V[(b,a)]=p
lib_ok=lambda n:(n[0] or 0)>=1.5 or ((n[0] or 0)>=1.2 and (n[1] or 0)>=1.2) or (n[1] or 0)>=1.5
out=['x\ty\tcombo (mechanic of x + mechanic of y)\tverdict\tcards\tdecks\tplayed sequence (agent, from the real pairs)\tsource']
for x,y in itertools.combinations(CIRC,2):
    c=[(lib_ok(LK.get((a,b),(0,0))),V[(a,b)][2]=='KEEP',LK.get((a,b),(0,0))[0] or 0,a,b) for a in A[x] for b in A[y] if a!=b and V.get((a,b),[0,0,''])[2] in ('KEEP','WEAK') and (a in OWN[x] or b in OWN[y])]
    if not c: continue
    c.sort(reverse=True)
    if not c[0][0]: continue
    *_,a,b=c[0]; p=V[(a,b)]; n=LK.get((a,b),(None,None))
    out.append('\t'.join([x,y,f'{a}+{b}',p[2],str(n[0]),str(n[1]),p[3],p[4]]))
open('factions/wheel/partners.tsv','w').write('\n'.join(out)+'\n')
print(len(rows)-1,'factions,',len(out)-1,'partner pairs')
