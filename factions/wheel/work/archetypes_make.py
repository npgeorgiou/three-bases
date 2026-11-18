# Writes wheel/archetypes.tsv: every archetype of archetypes_kaptain.txt that can exist here, its parts (engine or brick) and
# the usable concepts that can do each (step 3, all Claude's). Usage: python3 work/archetypes_make.py work/concepts.tsv archetypes.tsv
import sys
R=[]
def A(key,name,what,parts):
    for p,k,c in parts: R.append([key,name,what,p,k,c])
ANS='destroy,damage,aoe_damage,board_wipe,fight_enemy,multi_target_attack,deathtouch,stat_loss,debuff,attack_zero,silence,disable,bounce_enemy,banish,forced_movement,polymorph'
FIND=('find the pieces','brick','tutor,draw,selection,card_quality,deck_position')
LOOP1=('a card that resets or repeats another card','engine','repeat_trigger,untap,return_to_hand,recycle,revive,free_play,cost_set,cost_reduction,copy,extra_turn,rule_change')
LOOP2=('a card that gains each time the first one works','engine','on_ally_play,on_spell,death_trigger,other_death_trigger,on_sacrifice,leave_trigger,other_leave_trigger,on_draw,on_discard,combo_sequence,count_payoff,permanent_growth')
NEED=('a card that needs the other piece in play or in hand','engine','card_presence_condition')
FILL='self_mill,discard,sacrifice,self_destruct,friendly_fire'
A('aggro','Aggro','cheap units take two bases in rounds 1-2, before the enemy has a board; each enemy removed also cuts his supply in that lane',[
 ('cheap units that hit at once','brick','haste,attack_now,attack_gain,excess_damage,territory_trigger,piercing'),
 ('cheap units, many of them','engine','summon,cost_reduction,cost_set,overload_debt'),
 ('units that gain when I play another card','engine','on_ally_play,count_payoff,cost_condition'),
 ('clear the unit cancelling my dot','engine','damage,ping,fight_enemy,forced_movement,bounce_enemy,polymorph')])
A('control','Control','remove every enemy unit that comes, then hold the bases late with a few big units',[
 ('answers to every enemy unit','engine',ANS),
 ('hits that set up the next one','engine','mark_target,condition_life,ping'),
 ('cards keep coming from the removal','engine','on_kill,other_death_trigger,death_count,count_payoff,draw,generate_cards,selection,recycle'),
 ('a few finishers that are hard to answer','brick','variable_stats,permanent_growth,immunity,protection,shield,regeneration,cheat_death')])
A('midrange','Midrange','units that are hard to remove and give more than one card\'s worth, with removal for any enemy; each enemy removed cuts his supply, so my units keep the base',[
 ('units that are hard to remove','brick','protection,shield,cheat_death,damage_reduction,block_armor,regeneration,immunity,heal'),
 ('units that give more than their body','engine','summon,draw,generate_cards,death_trigger,copy,permanent_growth'),
 ('removal for any enemy, much of it by my units fighting','engine','fight_enemy,destroy,damage,multi_target_attack,stat_loss,silence,bounce_enemy,on_kill')])
A('tempo','Tempo','cheap units take the front cells; cheap cards send back or stop the enemy units that could remove them, so he spends his supply and actions again',[
 ('cheap units that act at once','engine','haste,attack_now,attack_gain,stealth,cost_reduction,movement,cross_lane'),
 ('cheap cards that send back, move or stop enemy units','engine','bounce_enemy,forced_movement,swap,attack_lock,disable,immobilize,silence,stat_loss,attack_zero,cost_increase,hand_disruption'),
 ('cheap cards that keep my units alive','brick','protection,shield,immunity,return_to_hand')])
A('combo','Combo','a game is won only by holding bases, so the combo is two cards that set each other off again and again inside one action, and the loop takes the lane',[FIND,LOOP1,LOOP2,NEED])
A('aggro_combo','Aggro-Combo','cheap units take lanes early, then one play makes them much stronger at once and takes the last base',[
 ('early pressure: many cheap units','engine','summon,haste,on_ally_play,cost_reduction'),
 ('the sudden finish: grows with the units already there','engine','variable_stats,condition_count,count_payoff,stat_multiply,attack_gain,multi_attack,attack_now')])
A('control_combo','Control-Combo','remove every enemy unit early, then the loop of Combo',[('answers to every enemy unit','brick',ANS),FIND,LOOP1,LOOP2,NEED])
A('prison','Prison / Stax','a lock on both players that my cards ignore, plus locks only on him',[
 ('a lock on both players','engine','row_effects,terrain'),
 ('my cards ignore the lock','engine','immunity,free_play,cost_type,stealth'),
 ('locks only on him','brick','cost_increase,attack_lock,disable,immobilize,silence,attack_zero,hand_disruption,board_clog,junk_cards,donate,disruption')])
A('go_wide','Tokens / Go-Wide','many small units in a lane (each also gives supply there), and cards that make all of them stronger',[
 ('many small units','engine','summon,copy,generate_cards,revive,cost_reduction'),
 ('bonuses for all of them','engine','attack_gain,defence_gain,stat_gain,buff,assists_support,variable_stats,condition_count,count_payoff,on_ally_play,row_effects')])
A('voltron','Voltron','one unit gets bonus after bonus and holds a base alone',[
 ('bonuses piled on one unit','engine','attack_gain,defence_gain,stat_gain,buff,stat_multiply,multi_attack,excess_damage'),
 ('the unit gains more each time it gets one','engine','on_targeted,permanent_growth,stat_condition'),
 ('keep that unit alive','brick','protection,shield,immunity,stealth,cheat_death,regeneration,damage_reduction,heal,lifesteal,return_to_hand')])
A('counters','+1/+1 Counters','units that keep the strength or defence they gain, then gain it twice over',[
 ('units that grow and keep it','engine','permanent_growth,stat_gain,attack_gain,defence_gain,buff'),
 ('the growth is doubled, repeated or copied','engine','stat_multiply,repeat_trigger,copy,variable_stats'),
 ('cards that care about big stats','engine','stat_condition,level_up,strikes_with_defence')])
A('extra_combats','Extra Combats','a unit attacks more than once in a turn or a round',[
 ('attack again','engine','multi_attack,untap,attack_now,extra_turn,fight_enemy'),
 ('something happens each time it attacks','engine','on_attack,on_fight,on_kill,permanent_growth,combat_damage_threshold,excess_damage,lifesteal'),
 ('survive the attacks','brick','regeneration,heal,damage_reduction,cheat_death,shield')])
A('defenders','Defenders / Toughness Matters','units with high defence that hit with their defence',[
 ('high defence','engine','defence_gain,damage_reduction,block_armor,stat_condition'),
 ('hits as hard as its defence','engine','strikes_with_defence,counterattack'),
 ('make the enemy hit the walls','engine','taunt,forced_attack,on_damaged'),
 ('heal, and gain when healed','engine','heal,regeneration,on_lifegain')])
A('toolbox','Toolbox','fetch from the deck the unit that answers what the enemy has',[
 ('fetch a chosen card from the deck','engine','tutor,selection,deck_position,card_quality'),
 ('a different answer on each unit','brick','destroy,damage,aoe_damage,silence,disable,bounce_enemy,forced_movement,protection,shield,heal,polymorph'),
 ('fetch it again','engine','recycle,return_to_hand,revive')])
A('aristocrats','Aristocrats','I kill my own units, and other cards gain each time one dies',[
 ('units to kill: cheap, made or coming back','engine','summon,revive,self_destruct'),
 ('kill my own units','engine','sacrifice,friendly_fire,board_wipe'),
 ('gain when a unit dies','engine','death_trigger,other_death_trigger,on_sacrifice,death_count,count_payoff,permanent_growth,resource_gain')])
A('reanimator','Reanimator','big units go to the discard pile early, then come back for little supply',[
 ('put big units in the discard pile','engine',FILL),
 ('bring them back cheaply','engine','revive,return_to_hand,recycle,free_play,cost_set,cost_reduction')])
A('self_mill','Dredge / Self-Mill','cards go from my deck and hand to my discard pile, and other cards use them from there',[
 ('fill my discard pile','engine',FILL),
 ('use the cards there','engine','recycle,revive,return_to_hand,free_play,count_payoff,condition_count')])
A('delirium','Delirium / Threshold','once my discard pile holds enough cards, or enough different ones, or my deck is small, cards get a bonus',[
 ('fill my discard pile','engine',FILL),
 ('a bonus past a number','engine','condition_count,variety_payoff,count_payoff,death_count,level_up,variable_stats,deck_condition,quests')])
A('recursion','Graveyard Recursion','cards come back from the discard pile and are played again',[
 ('play cards again from the discard pile','engine','recycle,return_to_hand,revive,free_play,cost_reduction'),
 ('cards worth playing again','engine','summon,draw,damage,aoe_damage,resource_gain,death_trigger,on_ally_play')])
A('madness','Madness','I discard cards and gain from it',[
 ('discard my cards','engine','discard'),
 ('gain when a card is discarded','engine','on_discard,cost_type,free_play,permanent_growth,count_payoff,variable_stats'),
 ('refill the hand','engine','draw,generate_cards')])
A('spellslinger','Spellslinger / Prowess','many cheap spells, and units that gain from each',[
 ('many cheap spells','engine','cost_reduction,cost_set,generate_cards,in_hand_buff,upgrade'),
 ('gain from each spell','engine','on_spell,spells_played_condition,spell_power,count_payoff,combo_sequence,permanent_growth'),
 ('spells cast again or for free','engine','free_play,repeat_trigger,recycle,copy')])
A('storm','Storm','one action per turn, so "one turn" becomes one round: gains from how many cards I played this round',[
 ('play many cards','engine','cost_reduction,cost_set,free_play,draw,generate_cards,copy,return_to_hand,resource_gain,extra_turn,overload_debt'),
 ('gain from how many','engine','count_payoff,combo_sequence,on_ally_play,on_spell,spells_played_condition,condition_count,variable_stats,permanent_growth')])
A('blink','Blink / Flicker','a unit leaves and comes back, and its Place fires again (Place fires every time a unit enters)',[
 ('the unit leaves and comes back','engine','return_to_hand,revive,recycle,repeat_trigger,copy,free_play,cost_reduction'),
 ('what fires again','engine','leave_trigger,other_leave_trigger,on_ally_play,summon,draw,damage,destroy,generate_cards,resource_gain')])
A('discover','Cascade / Discover','without randomness: new cards picked from a set the player sees',[
 ('new cards picked from a set','engine','generate_cards,selection,copy,free_play,card_quality,deck_position'),
 ('gain from the made cards','engine','hand_size,variety_payoff,count_payoff,on_draw')])
A('clone','Clone / Copy','copy my best unit, often for its Place effect again, or the enemy\'s best unit',[
 ('copy a card, a unit or its stats','engine','copy,repeat_trigger,stat_fixed,generate_cards'),
 ('the unit worth copying','engine','death_trigger,on_ally_play,stat_condition,summon,draw,damage')])
A('cheat','Cheat-into-Play','big units come in without their supply paid',[
 ('put a unit in for free or for less','engine','free_play,cost_set,cost_reduction,cost_type,revive,in_hand_buff'),
 ('big units, and cards that care about them','engine','cost_condition,stat_condition,variable_stats,excess_damage')])
A('eggs','Eggs','cheap units die for value and come back to die again',[
 ('cheap units that die and give something','engine','self_destruct,sacrifice,friendly_fire,death_trigger,summon'),
 ('they come back','engine','return_to_hand,revive,recycle,cheat_death'),
 ('gain from all the dying and leaving','engine','other_death_trigger,death_count,count_payoff,on_sacrifice,leave_trigger')])
A('ramp','Ramp','more supply in a lane early (a lane holds at most 12; supply comes from my units there), then big spells',[
 ('more supply in a lane, or cards that cost less','engine','resource_gain,base_resource_gain,cost_reduction,cost_set,cost_type,summon'),
 ('big spells','engine','board_wipe,aoe_damage,spell_power,cost_condition,variable_stats'),
 ('survive until then','brick','protection,taunt,damage_reduction,shield')])
A('stompy','Stompy','aggro with cheap units that are big for their cost, made bigger',[
 ('cheap units big for their cost','engine','cost_reduction,cost_set,cost_condition,stat_condition'),
 ('bonuses on them','engine','attack_gain,defence_gain,buff,excess_damage,permanent_growth'),
 ('keep them alive','brick','protection,shield,immunity')])
A('discard_8rack','Discard / 8-Rack','empty the enemy\'s hand, then punish him for holding few cards',[
 ('take, see, discard or tax the cards in his hand','engine','hand_disruption,information,steal,cost_increase,mill'),
 ('punish a small hand','engine','hand_size,condition_count')])
A('wheels','Wheels','discard my hand and draw a new one, and cards gain from each draw and discard (hand limit 10)',[
 ('draw and discard many','engine','draw,discard,hand_size,recycle,generate_cards'),
 ('gain from draws and discards','engine','on_draw,on_discard,count_payoff,permanent_growth,variable_stats')])
A('cycling','Cycling','swap a card I don\'t want for a new one, and gain from the swap',[
 ('swap a card for a new one','engine','discard,draw,recycle'),
 ('gain from the swap','engine','on_discard,on_draw,count_payoff,permanent_growth')])
A('pillowfort','Pillowfort','no player to attack: enemies must attack my strong unit, and the attacker pays',[
 ('enemies must attack this unit','engine','taunt,forced_attack'),
 ('the attacker pays','engine','counterattack,on_damaged,deathtouch,on_enemy_enter'),
 ('attacking my units is pointless','brick','protection,shield,immunity,stealth,damage_reduction,block_armor,regeneration')])
A('turbo_fog','Turbo-Fog','no answers on the enemy\'s turn: with units already on the bases, on my turn I stop his attacks again and again',[
 ('stop his attacks or their damage','engine','attack_lock,disable,immobilize,attack_zero,forced_movement,damage_reduction,shield,protection,immunity'),
 ('get those cards again','engine','recycle,return_to_hand,copy,draw,generate_cards'),
 ('units that hold the bases','brick','defence_gain,taunt,regeneration')])
A('hatebears','Hatebears / Death & Taxes','small units that each bind the enemy, while mine come in anyway; his units gone cut his supply',[
 ('small units that tax or stop him','engine','cost_increase,silence,attack_lock,immobilize,disable,hand_disruption,stat_loss,on_enemy_enter,disruption'),
 ('my units come in anyway','engine','free_play,cost_reduction,haste'),
 ('his units gone, his supply down','brick','destroy,damage,ping,bounce_enemy,banish,steal,polymorph'),
 ('keep my small units alive','brick','protection,shield')])
A('theft','Theft','take the enemy\'s units or cards for myself',[
 ('take or copy enemy units or cards','engine','steal,copy,hand_disruption'),
 ('use what I took','engine','sacrifice,movement,on_ally_play')])
A('aikido','Aikido / Judo','the enemy\'s units, hits and spells turn against him, by triggers on my units, not answers',[
 ('his units hit where I want','engine','forced_attack,forced_movement,swap'),
 ('his hits and spells come back at him','engine','counterattack,on_damaged,on_targeted,deathtouch'),
 ('his own cards used against him','engine','steal,copy,bounce_enemy')])
A('extra_turns','Extra Turns','extra actions, played again and again',[
 ('extra actions','engine','extra_turn,untap'),
 ('play them again','engine','return_to_hand,recycle,copy,repeat_trigger,combo_sequence,generate_cards'),
 ('find them','brick','draw,tutor,selection')])
U=set(l.split('\t')[0] for l in open(sys.argv[1]) if l.split('\t')[3:4]==['usable'])
used=set()
for r in R:
    for c in r[5].split(','):
        used.add(c)
        if c not in U: print('NOT USABLE',r[0],c)
print('unused usable:',' '.join(sorted(U-used)))
with open(sys.argv[2],'w') as f:
    f.write('key\tname\tin_this_game\tpart\tkind\tconcepts\twhose\n')
    for r in R: f.write('\t'.join(r+["Claude's"])+'\n')
print(len(R),'rows',len(set(r[0] for r in R)),'archetypes')
