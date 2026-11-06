# Case tests: gwent

Made by `cases/run.py gwent`.
**152 of 174 cases pass.**


## Mechanics (expected cards from the texts)

| case | question | expected | found | recall | extra | pass |
|---|---|---|---|---|---|---|
| mx01 | a trigger on another unit dying is other_death_trigger | 4 | 4 | 100% | 6 | yes |
| mx02 | moving enemy units is forced_movement | 0 | 0 | 100% | 89 | yes |
| mx03 | a plain draw is one form: zone deck_top, no pick top | 28 | 28 | 100% | 17 | yes |
| mx10 | damage to the enemy player is Nexus damage (kinds kept, v30) | 0 | 0 | 100% | 51 | yes |
| mx11 | moving or pushing units makes units move (positions change, v30) | 0 | 0 | 100% | 94 | yes |
| mx12 | a unit that moves (onto a space) is the event's object, never its actor (N16, Sentry, v36, v38) | 0 | 0 | 100% | 6 | yes |
| mx13 | can't be targeted by spells: the cant is on the spells, the protected unit is "to" (N19, v37) | 0 | 0 | 100% | 0 | yes |
| mx14 | a dead unit put into play is revive, never summon from the discard (N20, v37) | 0 | 0 | 100% | 15 | yes |
| mx15 | a trigger that holds only "this turn" is an ability given to the player for this turn (v37, Duelyst) | 0 | 0 | 100% | 1 | yes |
| mx13 | an effect on the creature opposing it is about lanes (concept lanes from same_lane, v38) | 0 | 0 | 100% | 0 | yes |
| mx14 | a strike on the spaces beside the opposing one reaches other lanes (cross_lane, v38) | 0 | 0 | 100% | 0 | yes |
| mx15 | within a circuit is a formation (link_formation, v38) | 0 | 0 | 100% | 0 | yes |
| mx16 | more or faster base resource (base_resource_gain, v38) | 0 | 0 | 100% | 0 | yes |
| gw01 | cards that use, give or care about Deploy | 591 | 591 | 100% | 500 | yes |
| gw02 | cards that use, give or care about Initiative | 5 | 5 | 100% | 0 | yes |
| gw03 | cards that use, give or care about Order | 351 | 349 | 99% | 57 | yes |
| gw04 | cards that use, give or care about Melee | 142 | 141 | 99% | 27 | yes |
| gw05 | cards that use, give or care about Drain | 2 | 2 | 100% | 0 | yes |
| gw06 | cards that use, give or care about Ranged | 128 | 126 | 98% | 28 | yes |
| gw07 | cards that use, give or care about Reveal | 6 | 6 | 100% | 0 | yes |
| gw08 | cards that use, give or care about Lineage | 4 | 4 | 100% | 0 | yes |
| gw09 | cards that use, give or care about Timer | 16 | 16 | 100% | 0 | yes |
| gw10 | cards that use, give or care about Spawn | 256 | 248 | 97% | 108 | yes |
| gw11 | cards that use, give or care about Zeal | 106 | 106 | 100% | 15 | yes |
| gw12 | cards that use, give or care about Cooldown | 77 | 74 | 96% | 0 | yes |
| gw13 | cards that use, give or care about Adrenaline | 31 | 30 | 97% | 0 | yes |
| gw14 | cards that use, give or care about Summon | 72 | 72 | 100% | 156 | yes |
| gw15 | cards that use, give or care about Charge | 26 | 25 | 96% | 36 | yes |
| gw16 | cards that use, give or care about Cataclysm | 5 | 5 | 100% | 1 | yes |
| gw17 | cards that use, give or care about Heal | 21 | 20 | 95% | 0 | yes |
| gw18 | cards that use, give or care about Banish | 33 | 33 | 100% | 25 | yes |
| gw19 | cards that use, give or care about Doomed | 113 | 112 | 99% | 11 | yes |
| gw20 | cards that use, give or care about Storm | 11 | 11 | 100% | 1 | yes |
| gw21 | cards that use, give or care about Veil | 38 | 37 | 97% | 0 | yes |
| gw22 | cards that use, give or care about Frost | 19 | 19 | 100% | 1 | yes |
| gw23 | cards that use, give or care about Fog | 2 | 2 | 100% | 1 | yes |
| gw24 | cards that use, give or care about Rain | 14 | 14 | 100% | 1 | yes |
| gw25 | cards that use, give or care about Bloodthirst | 17 | 17 | 100% | 0 | yes |
| gw26 | cards that use, give or care about Lock | 29 | 29 | 100% | 4 | yes |
| gw27 | cards that use, give or care about Formation | 17 | 17 | 100% | 0 | yes |
| gw28 | cards that use, give or care about Inspired | 11 | 11 | 100% | 0 | yes |
| gw29 | cards that use, give or care about Bleeding | 48 | 48 | 100% | 1 | yes |
| gw30 | cards that use, give or care about Disloyal | 19 | 19 | 100% | 0 | yes |
| gw31 | cards that use, give or care about Coin | 21 | 21 | 100% | 114 | yes |
| gw32 | cards that use, give or care about Patience | 10 | 10 | 100% | 14 | yes |
| gw33 | cards that use, give or care about Deathwish | 43 | 43 | 100% | 13 | yes |
| gw34 | cards that use, give or care about Armor | 65 | 65 | 100% | 17 | yes |
| gw35 | cards that use, give or care about Crew | 12 | 12 | 100% | 0 | yes |
| gw36 | cards that use, give or care about Resupply | 6 | 6 | 100% | 0 | yes |
| gw37 | cards that use, give or care about Vitality | 35 | 35 | 100% | 0 | yes |
| gw38 | cards that use, give or care about Barricade | 21 | 21 | 100% | 0 | yes |
| gw39 | cards that use, give or care about Exposed | 9 | 9 | 100% | 1 | yes |
| gw40 | cards that use, give or care about Grace | 13 | 13 | 100% | 0 | yes |
| gw41 | cards that use, give or care about Shield | 28 | 28 | 100% | 0 | yes |
| gw42 | cards that use, give or care about Devotion | 28 | 28 | 100% | 0 | yes |
| gw43 | cards that use, give or care about Purify | 28 | 28 | 100% | 0 | yes |
| gw44 | cards that use, give or care about Immunity | 21 | 21 | 100% | 0 | yes |
| gw45 | cards that use, give or care about Consume | 25 | 25 | 100% | 0 | yes |
| gw46 | cards that use, give or care about Seize | 15 | 15 | 100% | 0 | yes |
| gw47 | cards that use, give or care about Thrive | 17 | 17 | 100% | 0 | yes |
| gw48 | cards that use, give or care about Infused | 2 | 2 | 100% | 26 | yes |
| gw49 | cards that use, give or care about Dominance | 9 | 9 | 100% | 0 | yes |
| gw50 | cards that use, give or care about Bonded | 28 | 28 | 100% | 0 | yes |
| gw51 | cards that use, give or care about Resilience | 40 | 40 | 100% | 0 | yes |
| gw52 | cards that use, give or care about Deathblow | 41 | 41 | 100% | 0 | yes |
| gw53 | cards that use, give or care about Ambush | 8 | 8 | 100% | 1 | yes |
| gw54 | cards that use, give or care about Spring | 8 | 8 | 100% | 1 | yes |
| gw55 | cards that use, give or care about Discard | 10 | 10 | 100% | 0 | yes |
| gw56 | cards that use, give or care about Veteran | 11 | 11 | 100% | 0 | yes |
| gw57 | cards that use, give or care about Berserk | 13 | 13 | 100% | 0 | yes |
| gw58 | cards that use, give or care about Echo | 14 | 14 | 100% | 0 | yes |
| gw59 | cards that use, give or care about Conspiracy | 5 | 5 | 100% | 0 | yes |
| gw60 | cards that use, give or care about Flanking | 9 | 9 | 100% | 0 | yes |
| gw61 | cards that use, give or care about Create | 44 | 44 | 100% | 69 | yes |
| gw62 | cards that use, give or care about Poison | 31 | 31 | 100% | 3 | yes |
| gw63 | cards that use, give or care about Predator | 4 | 4 | 100% | 0 | yes |
| gw64 | cards that use, give or care about Symbiosis | 9 | 9 | 100% | 0 | yes |
| gw65 | cards that use, give or care about Might | 5 | 5 | 100% | 0 | yes |
| gw66 | cards that use, give or care about Duel | 4 | 4 | 100% | 0 | yes |
| gw67 | cards that use, give or care about Harmony | 15 | 15 | 100% | 0 | yes |
| gw68 | cards that use, give or care about Dragon's Dream | 1 | 1 | 100% | 1 | yes |
| gw69 | cards that use, give or care about Blood Moon | 2 | 2 | 100% | 1 | yes |
| gw70 | cards that use, give or care about Assimilate | 9 | 9 | 100% | 0 | yes |
| gw71 | cards that use, give or care about Tribute | 32 | 32 | 100% | 46 | yes |
| gw72 | cards that use, give or care about Profit | 52 | 52 | 100% | 46 | yes |
| gw73 | cards that use, give or care about Fee | 48 | 47 | 98% | 31 | yes |
| gw74 | cards that use, give or care about Bounty | 19 | 19 | 100% | 0 | yes |
| gw75 | cards that use, give or care about Intimidate | 11 | 11 | 100% | 0 | yes |
| gw76 | cards that use, give or care about Insanity | 6 | 6 | 100% | 0 | yes |
| gw77 | cards that use, give or care about Hoard | 11 | 11 | 100% | 1 | yes |
| gw78 | cards that use, give or care about Defender | 6 | 6 | 100% | 0 | yes |
| gw79 | cards that use, give or care about Rupture | 2 | 2 | 100% | 0 | yes |
| gw80 | cards that use, give or care about Clash | 3 | 3 | 100% | 3 | yes |
| gw81 | cards that use, give or care about Sabbath | 7 | 7 | 100% | 0 | yes |
| gw82 | cards that use, give or care about Vice | 3 | 3 | 100% | 0 | yes |
| gw83 | cards that use, give or care about Counter | 20 | 20 | 100% | 0 | yes |
| gw84 | cards that use, give or care about Reset | 13 | 13 | 100% | 21 | yes |
| gw85 | cards that use, give or care about Spying | 23 | 22 | 96% | 28 | yes |

## Combos (the enabler must set off the payoff)

| case | enabler | payoff | why | found as | pass |
|---|---|---|---|---|---|
| cgw01 | Koshchey | Caranthir Ar-Feiniel | a large amount of points | state: created | yes |
| cgw02 | Joachim de Wett | Coup de Grâce | strong plays always available | keyword: Spying | yes |
| cgw03 | Iris von Everec | Iris' Companions | thinning for Round 3 | line: is the Iris von Everec it names | yes |

## Region identity (signature, splash, archetype)

| case | region | kind | mechanic | need | found | pass |
|---|---|---|---|---|---|---|
| rgw01 | Northern Realms | signature (library) | boosting friendly units | 5 | 96 | yes |
| rgw02 | Northern Realms | signature (library) | Zeal | 5 | 48 | yes |
| rgw03 | Northern Realms | signature (library) | Order abilities | 5 | 108 | yes |
| rgw04 | Nilfgaard | signature (library) | locking units | 5 | 12 | yes |
| rgw05 | Nilfgaard | signature (library) | spying on enemy hands | 5 | 12 | yes |
| rgw06 | Nilfgaard | signature (library) | stealing enemy units | 5 | 9 | yes |
| rgw07 | Nilfgaard | signature (library) | Spies on the opponent's board | 5 | 28 | yes |
| rgw08 | Nilfgaard | signature (library) | playing cards from the opponent's deck | 5 | 10 | yes |
| rgw09 | Monster | signature (library) | Consume devours weaker units | 5 | 29 | yes |
| rgw10 | Monster | signature (library) | Deathwish | 5 | 27 | yes |
| rgw11 | Monster | signature (library) | highest value on board | 5 | 22 | yes |
| rgw12 | Monster | signature (library) | weather | 5 | 15 | yes |
| rgw13 | Scoiatael | signature (library) | traps | 5 | 9 | yes |
| rgw14 | Scoiatael | signature (library) | ranged attacks | 5 | 7 | yes |
| rgw15 | Scoiatael | signature (library) | mobility | 5 | 18 | yes |
| rgw16 | Scoiatael | signature (library) | many small damage instances | 5 | 26 | yes |
| rgw17 | Scoiatael | signature (library) | playing cards straight from the deck | 5 | 10 | yes |
| rgw18 | Skellige | signature (library) | Berserk | 5 | 38 | yes |
| rgw19 | Skellige | signature (library) | damaging itself or allies for bonuses | 5 | 26 | yes |
| rgw20 | Skellige | signature (library) | reviving from the graveyard | 5 | 13 | yes |
| rgw21 | Skellige | signature (library) | damaging units many ways | 5 | 107 | yes |
| rgw22 | Syndicate | signature (library) | coins spent on effects | 5 | 21 | yes |
| rgw23 | Nilfgaard | archetype (library) | control and counterplay | 3 | 24 | yes |
| rgw24 | Nilfgaard | archetype (library) | limiting the opponent's options | 3 | 14 | yes |
| rgw25 | Monster | archetype (library) | swarm and devour | 3 | 71 | yes |
| rgw26 | Monster | archetype (library) | consume and Deathwish | 3 | 29 | yes |
| rgw27 | Scoiatael | archetype (library) | traps and ambush | 3 | 9 | yes |
| rgw28 | Skellige | archetype (library) | resurrection | 3 | 14 | yes |
| rgw29 | Skellige | archetype (library) | aggression | 3 | 53 | yes |
| rgw30 | Syndicate | archetype (library) | coin economy | 3 | 132 | yes |

## Guide decks (the explanation must say what the guide says)

| case | deck | must say | missing | pass |
|---|---|---|---|---|

## Deck networks (a line must be there, or must not)

| case | deck | from | to | expect | found | pass |
|---|---|---|---|---|---|---|
| n545 | Nature's Gift: Devotion Symbiosis Good Version | Mahakam Pass | Naiad Fledgling | line  | - | NO |
| n546 | Nature's Gift: Devotion Symbiosis Good Version | Mahakam Pass | Naiad Pondkeeper | line  | - | NO |
| n547 | Mobilization: NR Devotion Undead Army | Kerack Marine | Kaedweni Revenant | line  | - | NO |
| n548 | Mobilization: NR Devotion Undead Army | Poor Fucking Infantry | Kaedweni Revenant | line  | - | NO |
| n549 | Mobilization: NR Devotion Undead Army | Forbidden Magic | Kaedweni Revenant | line  | puts: summons | yes |
| n550 | Mobilization: NR Devotion Undead Army | Redanian Secret Service | Drakenborg | line  | type: puts your units into play | yes |
| n551 | Mobilization: NR Devotion Undead Army | Redanian Secret Service | Kaedweni Revenant | line  | - | NO |
| n552 | Mobilization: NR Devotion Undead Army | Princess Adda | Redanian Secret Service | line  | waits: has Immunity | yes |
| n553 | Mobilization: NR Devotion Undead Army | Drakenborg | Vincent Meis | line  | - | NO |
| n554 | Mobilization: NR Devotion Undead Army | Drakenborg | Margarita Laux-Antille | line  | - | NO |
| n555 | Mobilization: NR Devotion Undead Army | Drakenborg | Botchling | line  | - | NO |
| n556 | Mobilization: NR Devotion Undead Army | Drakenborg | Bloody Baron | line  | type: changes units' stats: Bloody Baron gives them Bleeding | yes |
| n557 | Mobilization: NR Devotion Undead Army | Kaedweni Revenant | Vincent Meis | line  | - | NO |
| n558 | Mobilization: NR Devotion Undead Army | Redanian Archer | Vincent Meis | line  | - | NO |
| n559 | Mobilization: NR Devotion Undead Army | Voymir | Kaedweni Revenant | line  | - | NO |
| n560 | Mobilization: NR Devotion Undead Army | Voymir | Redanian Archer | line  | type: gives it Armor for its effect | yes |
| n561 | Mobilization: NR Devotion Undead Army | Sabrina Glevissig | Kaedweni Revenant | line  | - | NO |
| n562 | Mobilization: NR Devotion Undead Army | Philippa: Blind Fury | Kaedweni Revenant | line  | - | NO |
| n563 | Mobilization: NR Devotion Undead Army | Botchling | Princess Adda | line  | waits: is a Cursed whose summoning sets off its effect | yes |
| n564 | Mobilization: NR Devotion Undead Army | Vernon Roche | Kaedweni Revenant | line  | - | NO |
| n565 | Shieldwall: Roegner Ale Damsel | Ale of the Ancestors | Knight-Errant | line  | - | NO |
| n566 | Shieldwall: Roegner Ale Damsel | Ale of the Ancestors | Prince Anséis | line  | type: changes its stats for its effect | yes |
| n567 | Pincer Maneuver: Kimbolt's Temple Siege | Temple of Melitele: Congregation | Prince Anséis | line  | type: changes its stats for its effect | yes |
| n568 | White Frost: White Frost-EZ pro rank | Eredin Bréacc Glas | Caranthir: Golden Child | line  | - | NO |
| n569 | Arachas Swarm: Tatterwing - 1 prov left for good luck | Ge'els | Lara Dorren | line  | puts: puts it into play from the deck; also triggers: plays it: its effect goes  | yes |
| n570 | Enslave: Damage Enslave With Enforcers (+10 -1) | Battle Stations! | Impera Enforcers | line  | - | NO |
| n571 | Enslave: Damage Enslave With Enforcers (+10 -1) | Fercart | Impera Enforcers | line  | type: makes enemy units get Spying | yes |
| n572 | Enslave: Damage Enslave With Enforcers (+10 -1) | Stefan Skellen | Impera Enforcers | line  | - | NO |
| n573 | Enslave: Damage Enslave With Enforcers (+10 -1) | Buhurt | Fercart | line  | waits: is a spell whose playing sets off its effect | yes |
| n574 | Enslave: Damage Enslave With Enforcers (+10 -1) | Joachim de Wett | Coup de Grâce | line  | type: has Spying | yes |
| n575 | Tactical Decision: OP GN HyperThin | Doadrick Leumaerts | Albrich | line  | waits: moves it for its effect | yes |
| n576 | Tactical Decision: OP GN HyperThin | Maxii van Dekkar | Albrich | line  | waits: moves it for its effect | yes |
| n577 | Tactical Decision: OP GN HyperThin | Strays of Spalla | Albrich | line  | - | NO |
| n578 | Tactical Decision: OP GN HyperThin | Summoning Circle | Imperial Golem | line  | - | NO |
| n579 | Tactical Decision: OP GN HyperThin | Doadrick Leumaerts | Snowdrop | line  | waits: makes you draw cards | yes |
| n580 | Blood Money: Classical Bounty with Tamara, Drill | Vivaldi Bank | Conjurer's Candle | line  | type: lets you gain the second resource (Bones) | yes |
| n581 | Blood Money: Classical Bounty with Tamara, Drill | Royal Decree | Tamara Strenger | line  | waits: plays it: its effect goes off | yes |
| n582 | Onslaught: Pirates attack - Endless Voyage | Vabjorn | Raiding Fleet | line  | puts: puts it into play from the deck | yes |
| n583 | Onslaught: Pirates attack - Endless Voyage | Vabjorn | Abordage | line  | puts: puts it into play from the deck | yes |
| n584 | Rage of the Sea: Fulmar rain ft. Otkell and Melusine | Melusine | Messenger of the Sea | line  | waits: damages enemy units or players | yes |
| n585 | Rage of the Sea: Fulmar rain ft. Otkell and Melusine | Torrential Rain | Messenger of the Sea | line  | waits: damages enemy units or players | yes |
| n586 | Patricidal Fury: RnR Seagulls Sove Compass | Seagull | Ragh Nar Roog | line  | - | NO |
| n587 | Patricidal Fury: RnR Seagulls Sove Compass | Hammond | Ragh Nar Roog | line  | - | NO |
