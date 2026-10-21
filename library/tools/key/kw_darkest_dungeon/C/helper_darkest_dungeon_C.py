import json,os,re,sys
os.chdir('/home/claude/three-bases/library/tools/key')
def w(game,name,data):
    d=f'kw_{game}/C'; os.makedirs(d,exist_ok=True)
    ids=re.findall(r'^(\d+) \|',open(f'kw_{game}/{name}.txt',encoding='utf-8').read(),re.M)
    for k in data: assert k in ids,(game,k)
    out={i:data.get(i,[]) for i in ids}
    json.dump(out,open(f'{d}/{name}.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
    open(f'{d}/progress.txt','a').write(f'done {name}\n')
G='darkest_dungeon'
w(G,'settle_00',{
'759760':[["stress_morale","reaches 100 stress"],["autonomous_units","act on their own"],["stat_loss","stat penalties"]],
'759762':[["upgrade","can be upgraded"]],
'759766':[["stat_gain","stat increase"],["temporary_buff","A temporary stat increase"]],
'759767':[["rest_phase","Camping"],["activated","An ability used by a hero"]],
'759768':[["death_trigger","Most dead monsters leave a temporary corpse"],["targeting_rules","attack around the corpses"]],
'759769':[["damage","Critical hits do extra damage"],["stress_morale","stress damage"]],
'759771':[["cheat_death","A hero with 0 HP is at Death's Door"],["permanent_loss","permanently killing the hero"],["random_effect","has a chance"]],
'759772':[["stat_loss","stat decrease"],["temporary_effect","A temporary stat decrease"]],
'759774':[["debuff","debilitates the hero"],["rest_phase","treated in town at the Sanitarium"]],
'759776':[["merge_attach","equipped to a hero"],["upgrade","can be upgraded"]],
'759785':[["terrain","An object found in dungeons"],["friendly_fire","inflicts DMG and stress on the entire party"],["stress_morale","stress on the entire party"]],
'759786':[["damage_reduction","what percentage of incoming damage is mitigated"],["piercing","DOTs (bleed, blight) ignore PROT"]],
'759794':[["reveal_order","influences the order in which combatants act"],["random_effect","Initiative is re-rolled each round"]],
'759801':[["buff","Virtued heroes have buffs"]],
'759802':[["merge_attach","A type of equipment used by a hero"],["upgrade","Weapons can be upgraded"]],
})
G='dnd5e'
w(G,'settle_00',{
'761163':[["advantage","Attack rolls against you have Advantage"],["advantage","your attack rolls have Disadvantage"],["debuff","automatically fail any ability check that requires sight"]],
'761164':[["attack_lock","You can't attack the charmer"],["targeting_rules","target the charmer with damaging abilities"],["advantage","Advantage on ability checks to interact socially"]],
'761174':[["advantage","You have Disadvantage on attack rolls"],["advantage","An attack roll against you has Advantage"],["positional","if the attacker is within 5 feet of you"]],
'761178':[["ranged","make a ranged attack"],["upkeep","Each attack expends one piece of ammunition"]],
'761182':[["play_restriction","You can fire only one piece of ammunition"]],
'761184':[["ranged","adds 5 feet to your reach"],["zone_of_control","Opportunity Attacks"]],
'761188':[["multi_target_attack","make a melee attack roll with the weapon against a second creature"],["adjacency","within 5 feet of the first"]],
'761189':[["damage","deal damage to that creature equal to the ability modifier"],["damage_types","same type dealt by the weapon"]],
'761193':[["stat_loss","reduce its Speed by 10 feet"],["temporary_effect","until the start of your next turn"]],
'761194':[["saving_throws","Constitution saving throw"],["debuff","the creature has the Prone condition"]],
})
G='duelyst'
w(G,'settle_00',{
'741528':[["on_damaged","Whenever your General takes damage"],["self_destruct","It's destroyed at 0 Durability"]],
'741530':[["self_destruct","Only exists until end of turn"],["temporary_effect","until end of turn"]],
'741536':[["territory_trigger","while on the enemy side of the battlefield"],["buff","Gains a bonus"]],
'741542':[["death_trigger","When this dies"],["summon","leaves behind a 0/1 Egg"],["revive","hatches into the same minion"],["delayed","before your next turn"]],
'741552':[["flanking","When attacking from behind"],["damage","extra damage"]],
'741554':[["summon","Summon as a 0/10 Structure"],["transform","transforms into its true form"],["delayed","after a number of turns"]],
})
G='faeria'
w(G,'settle_00',{
'741074':[["placement_rules","Can only travel over lakes and ocean"],["self_destruct","drowns at end of turn on other land"]],
'741075':[["removal","Removes a creature from the game"],["death_trigger","until the swallower dies"]],
})
G='hs_battlegrounds'
w(G,'settle_00',{
'750346':[["generate_cards","Gives a temporary spell"],["on_play","when played"],["turn_start","start of each recruit phase"]],
'750351':[["items_consumables","Battlegrounds items"],["shop_gold","bought"]],
'750361':[["activated","pay gold to use the effect"],["cooldowns","Once per recruit turn"]],
'750363':[["random_effect","Randomly assigned"],["death_count","after three friendly aberrations die"],["generate_cards","added to hand"]],
'750365':[["shop_gold","A special shop"],["coin_economy","a second currency"],["resource_banking","carries over"],["turn_number","on set turns"]],
'750367':[["tribal","only in lobbies with pirates"]],
})
G='inscryption'
w(G,'settle_00',{
'740620':[["on_play","When a card bearing this sigil is played"],["summon","a Chime is created on each empty adjacent space"],["adjacency","each empty adjacent space"]],
'740622':[["on_kill","When a card with this kills an opposing card"],["temporary_buff","This power is removed after a battle ends"]],
'740623':[["death_trigger","When a card bearing this sigil perishes"],["merge_attach","gain the Detonator sigil"],["target_choice","its owner chooses a creature"]],
'740629':[["on_attack","After attacking"],["self_destruct","a card bearing this sigil perishes"]],
'740630':[["death_trigger","When a card bearing this sigil perishes"],["merge_attach","gain the Brittle sigil"],["target_choice","its owner chooses a creature"]],
'740633':[["movement","will move to that space to receive the strike instead"],["bodyguard","will move to that space to receive the strike instead"]],
'740638':[["death_trigger","When a Card bearing this Sigil dies"],["aoe_damage","all adjacent cards (those to the left, right and front of the card) are dealt 10 damage"],["adjacency","those to the left, right and front of the card"]],
'740640':[["death_trigger","When another creature you own dies"],["revive","it is returned to life and dies again immediately"],["repeat_trigger","triggering any on-death effects an additional time"]],
'740643':[["activated","Activate: Pay 1 Energy to deal 1 damage"],["ping","deal 1 damage to the creature across from a card bearing this sigil"]],
'740646':[["transform","transforms a card into a Hydra"],["deck_condition","represented in the Health of creatures in your deck"],["variety_payoff","a creature of each tribe in your deck"]],
'740651':[["death_trigger","When Gem Vessels on the owner's side of the board die"],["aoe_damage","are dealt 10 damage"],["friendly_fire","adjacent friendly creatures"]],
'740654':[["death_trigger","When a card bearing this sigil perishes"],["generate_cards","a random card is created in your hand"],["random_effect","a random card"]],
'740655':[["death_trigger","when it perishes"],["generate_cards","a random card is created in your hand"],["link_formation","within a circuit"],["random_effect","a random card"]],
'740657':[["on_play","When a card bearing this sigil is played"],["hand_deck_swap","discard your hand then draw a new hand of 4 cards"]],
'740672':[["link_formation","complete a circuit"],["null_body","provides no effect"]],
'740675':[["stat_gain","increased power"],["death_trigger","if a card bearing this sigil perishes"],["permanent_loss","permanently removed from your deck"]],
'740679':[["immunity","If a creature would attack a card bearing this sigil, it does not"]],
'740684':[["death_trigger","When a card bearing this sigil perishes"],["merge_attach","gain the Nano Armor sigil"],["target_choice","its owner chooses a creature"]],
'740695':[["on_damaged","After a card bearing this sigil is dealt damage"],["stat_gain","swap its Power and Health"]],
'740701':[["on_play","When a card bearing this sigil is played"],["items_consumables","a random item"],["random_effect","random item"]],
'740703':[["death_trigger","When a card bearing this sigil perishes"],["revive","a copy of it is created in your hand"]],
'740706':[["sacrifice","when a card bearing it is sacrificed"],["resource_gain","count as 3 Blood rather than 1 Blood"]],
})
G='into_the_breach'
w(G,'settle_00',{
'760829':[["placement_rules","positioned at any terrain tile, except mountains and other units"],["immunity","not affected by lava or A.C.I.D. tiles"]],
'760834':[["debuff","Weapon damage against this unit is doubled"],["silence","Natural Armor is disabled"]],
'760835':[["stat_gain","damage is increased by 1 on its next attack"],["heal","repairing while Boosted will heal 2 points"]],
'760837':[["disable","unable to move or attack"],["shield","Any damage to a frozen unit is negated"]],
'760851':[["damage_over_time","1 damage all friendly units every turn"],["aoe_damage","all friendly units"]],
'760853':[["movement","can walk in Water"]],
'760854':[["aura","enhancing all Vek"],["stat_gain","+1 HP"],["regeneration","regeneration"],["death_trigger","explode on death"]],
})
G='shadowverse'
w(G,'settle_00',{
'752303':[["transform","Evolve"]],'752309':[["cost_type","Accelerate"]],'752310':[["damage","Strike"]],
'752314':[["graveyard","Necromancy"]],'752326':[["deck_condition","Resonance"]],
})
G='sts1'
w(G,'settle_00',{
'757490':[["junk_cards","unplayable status cards"],["damage","damage you"]],
'757495':[["permanent_growth","Increases damage every turn"],["slots_queue","Orb"],["damage","deals damage to the enemy with the least HP"],["stat_condition","least HP"]],
'757498':[["stances","this stance"],["resource_gain","gain 3 Energy"],["stat_multiply","triple damage"],["turn_start","start of your next turn"]],
'757505':[["block_armor","Gains Block"],["slots_queue","Orb"]],
'757508':[["damage","Deals damage to random enemies"],["random_effect","random enemies"],["slots_queue","Orb"]],
'757511':[["resource_gain","Gains Energy"],["slots_queue","Orb"]],
'757512':[["damage_over_time","lose HP at the start of their turn"],["turn_start","at the start of their turn"]],
'757514':[["regeneration","heals HP at the end of your turn"],["turn_end","at the end of your turn"]],
'757516':[["permanent_growth","Gain Strength at the end of your turn"],["turn_end","at the end of your turn"]],
'757518':[["cost_set","0 cost"],["exhaust","which Exhaust"]],
'757526':[["stat_gain","Your next Attack deals additional damage"]],
})
