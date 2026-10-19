import json
r={
"742363":[["selection","Choose one of three random cards"],["random_effect","random cards"]],
"742374":[["disable","cannot act or be interacted with until a condition is met"],["immunity","cannot act or be interacted with until a condition is met"]],
"742376":[["cheat_death","returns with 1 Health"]],
"742377":[["resource_gain","Death Knight resource gained when friendly minions die"],["death_count","when friendly minions die"]],
"742384":[["temporary_effect","Discarded at the end of your turn"],["turn_end","at the end of your turn"]],
"742391":[["merge_attach","Played next to a Mech, merges into it"],["tribal","Mech"]],
"742392":[["combo_sequence","Bonus if a card of the same type or school was played last turn"],["tribal","same type or school"]],
"742395":[["resource_banking","no unspent mana"]],
"742399":[["selection","Look at the bottom three cards of the deck and put one on top"],["deck_position","bottom three cards of the deck"]],
"742407":[["recycle","Can be replayed any number of times"]],
"742411":[],
"742413":[["hand_position","played the turn it entered your hand"]],
"742416":[["activated","uses one of three abilities once each"],["modal_choice","uses one of three abilities once each"]],
"742423":[["hand_position","both ends of the hand"],["distribute","splits into two halves"]],
"742428":[["free_play","Automatically cast for free when drawn"]],
"742429":[],
}
json.dump(r,open("kw_hearthstone/C/settle_00.json","w"),indent=0)
