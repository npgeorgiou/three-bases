import json,os,re
os.chdir('/home/claude/three-bases/library/tools/key')
def w(game,name,data):
    d=f'kw_{game}/C'; os.makedirs(d,exist_ok=True)
    ids=re.findall(r'^(\d+) \|',open(f'kw_{game}/{name}.txt',encoding='utf-8').read(),re.M)
    for k in data: assert k in ids,(game,k)
    json.dump({i:data.get(i,[]) for i in ids},open(f'{d}/{name}.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
    open(f'{d}/progress.txt','a').write(f'done {name}\n')
w('wh_40k_10e','settle_00',{
'784290':[["resource_gain","you gain Pain tokens as follows"],["turn_start","at the start of your Command phase"],["on_kill","each time an enemy unit is destroyed"],["temporary_buff","until the end of the phase, that unit is Empowered"]],
'784359':[["exhaust","can only shoot with this weapon once per battle"]],
'784376':[["stances","select one of the Ka'tah stances below"],["buff","Melee weapons equipped by models in this unit have the [SUSTAINED HITS 1] ability"]],
'784385':[["modal_choice","select one of the Doctrina Imperatives below"],["turn_start","At the start of the battle round"],["temporary_effect","Until the end of the battle round"],["stat_gain","Improve the Ballistic Skill characteristic of ranged weapons"]],
'784392':[["stat_condition","use the Toughness characteristic of the majority of the models"],["type_grant","all models in units with this ability are considered Infantry models"]],
'784423':[["buff","that Armiger model is affected by that Bondsman ability"],["temporary_effect","Until the start of your next Command phase"],["turn_start","In your Command phase"]],
'784550':[["ranged","eligible to shoot"],["flexibility","it can either shoot with its Pistols or with all of its other ranged weapons"]],
'784552':[["merge_attach","it is known as an Attached unit"],["bodyguard","that attack cannot be allocated to a Character model in that unit"]],
'784553':[["piercing","no saving throw of any kind can be made against that attack"],["damage","inflicts a number of mortal wounds on the target"]],
'784556':[["random_effect","you can re-roll that attack’s Wound roll"]],
'784557':[["tribal","against a target with the keyword"]],
'784558':[["damage","that attack scores a number of additional hits"]],
'784561':[["damage_reduction","that wound is ignored and is not lost"],["saving_throws","roll one D6"]],
'784562':[["random_effect","a random number of attacks"],["condition_count","for every five models"],["play_restriction","can never be used to make attacks against a unit that is within Engagement Range"]],
'784564':[["ranged","attacks can be made with them even if the target is not visible"],["debuff","subtract 1 from that attack’s Hit roll"]],
'784568':[["stat_gain","the Attacks characteristic of that weapon is increased"]],
'784570':[["movement","it can make a Normal move"],["start_of_game","at the start of the first battle round, before the first turn begins"]],
'784572':[["placement_rules","you can set up this unit anywhere on the battlefield"],["reserve_bench","set it up in Reserves"]],
'784573':[["death_trigger","When such a model is destroyed"],["aoe_damage","suffers a number of mortal wounds"],["random_effect","roll one D6"]],
'784574':[["debuff","subtract 1 from that attack’s Hit roll"]],
'784575':[["movement","it can move through models"]],
'784576':[["targeting_rules","can only be selected as the target of a ranged attack"]],
'784577':[["stances","declare which models from your army with this ability will be in Hover mode"],["stat_gain","its Move characteristic is changed"]],
'784578':[["first_strike","Fights First"]],
'784579':[["play_restriction","can only be used by Psykers"],["damage_types","Psychic Attack"]],
'784580':[["ranged","select one ranged weapon that embarked model is equipped with"]],
'784581':[["deckbuilding_effect","Your army may include up to three units with the Crucible ability"],["play_restriction","these units cannot be given Enhancements"]],
})
