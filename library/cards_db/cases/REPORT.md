# Case tests: gwent

Made by `cases/run.py gwent`.
**275 of 275 cases pass.**

**Cases whose reason no line says any more (rewrite them): n605, n606, n607, n608, n609, n610, n611, n623, n624, n625, n627, n629, n630, n631, n671, n675, n686, n700**


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
| gw01 | cards that use, give or care about Deploy | 592 | 592 | 100% | 502 | yes |
| gw02 | cards that use, give or care about Initiative | 5 | 5 | 100% | 0 | yes |
| gw03 | cards that use, give or care about Order | 352 | 350 | 99% | 57 | yes |
| gw04 | cards that use, give or care about Melee | 142 | 141 | 99% | 27 | yes |
| gw05 | cards that use, give or care about Drain | 2 | 2 | 100% | 0 | yes |
| gw06 | cards that use, give or care about Ranged | 128 | 126 | 98% | 28 | yes |
| gw07 | cards that use, give or care about Reveal | 6 | 6 | 100% | 0 | yes |
| gw08 | cards that use, give or care about Lineage | 4 | 4 | 100% | 0 | yes |
| gw09 | cards that use, give or care about Timer | 16 | 16 | 100% | 0 | yes |
| gw10 | cards that use, give or care about Spawn | 256 | 248 | 97% | 109 | yes |
| gw11 | cards that use, give or care about Zeal | 106 | 106 | 100% | 15 | yes |
| gw12 | cards that use, give or care about Cooldown | 77 | 74 | 96% | 0 | yes |
| gw13 | cards that use, give or care about Adrenaline | 31 | 30 | 97% | 0 | yes |
| gw14 | cards that use, give or care about Summon | 72 | 72 | 100% | 157 | yes |
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
| rgw03 | Northern Realms | signature (library) | Order abilities | 5 | 109 | yes |
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
| dgw06 | Arachas Swarm: Tatterwing - 1 prov left for good luck | wild hunt cards: are or make them: ge'els;red riders. care about them: lara dorren | - | yes |
| dgw11 | Rage of the Sea: Fulmar rain ft. Otkell and Melusine | enemy units or players take damage: made by fulmar, little havfrue, melusine;torrential rain. use it: messenger of the sea;enemy units or players take damage: made by fulmar, little havfrue, melusine, melusine cultist, rage of the sea, rioghan the undying, svalblod priest, tempest, torrential rain | - | yes |

## Deck networks (a line must be there, or must not)

| case | deck | from | to | expect | found | pass |
|---|---|---|---|---|---|---|
| n545 | Nature's Gift: Devotion Symbiosis Good Version | Mahakam Pass | Naiad Fledgling | line which sets off Symbiosis | waits: plays a Nature card, which sets off Symbiosis: Naiad Fledgling waits for  | yes |
| n546 | Nature's Gift: Devotion Symbiosis Good Version | Mahakam Pass | Naiad Pondkeeper | none  | - | yes |
| n547 | Mobilization: NR Devotion Undead Army | Kerack Marine | Kaedweni Revenant | none  | - | yes |
| n548 | Mobilization: NR Devotion Undead Army | Poor Fucking Infantry | Kaedweni Revenant | none  | - | yes |
| n549 | Mobilization: NR Devotion Undead Army | Forbidden Magic | Kaedweni Revenant | line  | puts: summons | yes |
| n550 | Mobilization: NR Devotion Undead Army | Redanian Secret Service | Drakenborg | line  | type: puts your units into play | yes |
| n552 | Mobilization: NR Devotion Undead Army | Princess Adda | Redanian Secret Service | line  | waits: has Immunity | yes |
| n553 | Mobilization: NR Devotion Undead Army | Drakenborg | Vincent Meis | none  | - | yes |
| n554 | Mobilization: NR Devotion Undead Army | Drakenborg | Margarita Laux-Antille | none  | - | yes |
| n555 | Mobilization: NR Devotion Undead Army | Drakenborg | Botchling | none  | - | yes |
| n556 | Mobilization: NR Devotion Undead Army | Drakenborg | Bloody Baron | line  | type: changes units' stats: Bloody Baron gives them Bleeding | yes |
| n557 | Mobilization: NR Devotion Undead Army | Kaedweni Revenant | Vincent Meis | line  | waits: its 1 damage kills what it sets to strength 1 | yes |
| n558 | Mobilization: NR Devotion Undead Army | Redanian Archer | Vincent Meis | line  | waits: its 1 damage kills what it sets to strength 1 | yes |
| n559 | Mobilization: NR Devotion Undead Army | Voymir | Kaedweni Revenant | line copies itself | keyword: gives a unit's copies Armor, and Kaedweni Revenant copies itself; also  | yes |
| n560 | Mobilization: NR Devotion Undead Army | Voymir | Redanian Archer | line  | type: gives it Armor for its effect | yes |
| n561 | Mobilization: NR Devotion Undead Army | Sabrina Glevissig | Kaedweni Revenant | line  | waits: leaves weak units for its kill | yes |
| n562 | Mobilization: NR Devotion Undead Army | Philippa: Blind Fury | Kaedweni Revenant | line  | waits: leaves weak units for its kill | yes |
| n563 | Mobilization: NR Devotion Undead Army | Botchling | Princess Adda | line  | waits: is a Cursed whose summoning sets off its effect | yes |
| n565 | Shieldwall: Roegner Ale Damsel | Ale of the Ancestors | Knight-Errant | line  | stronger: can give it more strength | yes |
| n566 | Shieldwall: Roegner Ale Damsel | Ale of the Ancestors | Prince Anséis | line  | type: changes its stats for its effect | yes |
| n567 | Pincer Maneuver: Kimbolt's Temple Siege | Temple of Melitele: Congregation | Prince Anséis | line  | type: changes its stats for its effect | yes |
| n568 | White Frost: White Frost-EZ pro rank | Eredin Bréacc Glas | Caranthir: Golden Child | line  | type: damages units or players | yes |
| n569 | Arachas Swarm: Tatterwing - 1 prov left for good luck | Ge'els | Lara Dorren | line  | puts: puts it into play from the deck; also triggers: plays it: its effect goes  | yes |
| n570 | Enslave: Damage Enslave With Enforcers (+10 -1) | Battle Stations! | Impera Enforcers | none  | - | yes |
| n571 | Enslave: Damage Enslave With Enforcers (+10 -1) | Fercart | Impera Enforcers | line  | type: makes enemy units get Spying | yes |
| n572 | Enslave: Damage Enslave With Enforcers (+10 -1) | Stefan Skellen | Impera Enforcers | none  | - | yes |
| n573 | Enslave: Damage Enslave With Enforcers (+10 -1) | Buhurt | Fercart | line  | waits: is a spell whose playing sets off its effect | yes |
| n574 | Enslave: Damage Enslave With Enforcers (+10 -1) | Joachim de Wett | Coup de Grâce | line  | type: has Spying | yes |
| n575 | Tactical Decision: OP GN HyperThin | Doadrick Leumaerts | Albrich | line  | waits: moves it for its effect | yes |
| n576 | Tactical Decision: OP GN HyperThin | Maxii van Dekkar | Albrich | line  | waits: shuffles a card into the deck: its move effect goes off; also moves it fo | yes |
| n577 | Tactical Decision: OP GN HyperThin | Strays of Spalla | Albrich | line  | waits: shuffles a card into the deck: its move effect goes off | yes |
| n579 | Tactical Decision: OP GN HyperThin | Doadrick Leumaerts | Snowdrop | line  | waits: makes you draw cards | yes |
| n580 | Blood Money: Classical Bounty with Tamara, Drill | Vivaldi Bank | Conjurer's Candle | line  | type: lets you gain the second resource (Bones) | yes |
| n581 | Blood Money: Classical Bounty with Tamara, Drill | Royal Decree | Tamara Strenger | line  | waits: plays it: its effect goes off | yes |
| n582 | Onslaught: Pirates attack - Endless Voyage | Vabjorn | Raiding Fleet | line  | puts: puts it into play from the deck | yes |
| n583 | Onslaught: Pirates attack - Endless Voyage | Vabjorn | Abordage | line  | puts: puts it into play from the deck | yes |
| n584 | Rage of the Sea: Fulmar rain ft. Otkell and Melusine | Melusine | Messenger of the Sea | line  | waits: damages enemy units or players | yes |
| n585 | Rage of the Sea: Fulmar rain ft. Otkell and Melusine | Torrential Rain | Messenger of the Sea | line  | waits: damages enemy units or players | yes |
| n587 | Patricidal Fury: RnR Seagulls Sove Compass | Hammond | Ragh Nar Roog | line  | moves: moves an enemy unit into the row it hits | yes |
| n588 | Selective Mutation, Vesemir: Mentor | Selective Mutation | Vesemir: Mentor | none fills your hand | puts: draws it from the deck | yes |
| n589 | Griffin Witcher Mentor, Geralt: Quen | Griffin Witcher Mentor | Geralt: Quen | none fills your hand | - | yes |
| n590 | Pincer Maneuver, Temple of Melitele: Congregation | Pincer Maneuver | Temple of Melitele: Congregation | none fills your hand | - | yes |
| n591 | Ardal aep Dahy, Eskel | Ardal aep Dahy | Eskel | none fills your hand | - | yes |
| n592 | Battle Stations!, Geralt: Yrden | Battle Stations! | Geralt: Yrden | none fills your hand | waits: plays it: its effect goes off | yes |
| n593 | Birna Bran, Arnaghad | Birna Bran | Arnaghad | none fills your hand | - | yes |
| n594 | Eventide Plunder, Carlo Varese | Eventide Plunder | Carlo Varese | line fills your hand | waits: fills your hand | yes |
| n595 | Tamara Strenger, Kurt | Tamara Strenger | Kurt | none gives it more strength | - | yes |
| n596 | Octavia Hale, Witch Hunter | Octavia Hale | Witch Hunter | none can give it more strength | - | yes |
| n597 | Tamara Strenger, The Witchfinder | Tamara Strenger | The Witchfinder | none gives it more strength | - | yes |
| n598 | Octavia Hale, Moreelse | Octavia Hale | Moreelse | none can give it more strength | - | yes |
| n599 | Adrenaline Rush, Cave Troll | Adrenaline Rush | Cave Troll | none can give it more strength | - | yes |
| n600 | Bone Talisman, Cave Troll | Bone Talisman | Cave Troll | none gives it more strength | - | yes |
| n601 | Kelpie, Elder Bear | Kelpie | Elder Bear | none can give it more strength | - | yes |
| n602 | Nature's Rebuke, Weeping Willow | Nature's Rebuke | Weeping Willow | none can give it more strength | - | yes |
| n603 | Nature's Rebuke, Treant Boar | Nature's Rebuke | Treant Boar | none can give it more strength | - | yes |
| n604 | Vesemir: Mentor, Geralt of Rivia | Vesemir: Mentor | Geralt of Rivia | none gives it more strength | - | yes |
| n605 | Auberon: Conqueror, Aen Elle Conqueror | Auberon: Conqueror | Aen Elle Conqueror | none gives it more strength when it comes | - | yes |
| n606 | Auberon: Conqueror, Wild Hunt Rider | Auberon: Conqueror | Wild Hunt Rider | none gives it more strength when it comes | - | yes |
| n607 | White Frost, Naglfar Taskmaster | White Frost | Naglfar Taskmaster | none gives it more strength when it comes | - | yes |
| n608 | Auberon: Conqueror, Winter Queen | Auberon: Conqueror | Winter Queen | none gives it more strength when it comes | - | yes |
| n609 | Holger Blackhand, An Craite Longship | Holger Blackhand | An Craite Longship | none gives it more strength when it comes | - | yes |
| n610 | Holger Blackhand, Bjorn's Drakkar | Holger Blackhand | Bjorn's Drakkar | none gives it more strength when it comes | - | yes |
| n611 | Imposter, Roderick of Dun Tynne | Imposter | Roderick of Dun Tynne | none gives it more strength when it comes | - | yes |
| n612 | Arachas Behemoth, Arachas Queen | Arachas Behemoth | Arachas Queen | none  | - | yes |
| n613 | Kikimore Queen, Kikimore Stalker | Kikimore Queen | Kikimore Stalker | none more strength | waits: is an Insectoid whose summoning sets off its effect | yes |
| n614 | Imposter, False Ciri | Imposter | False Ciri | line its text reads its strength | stronger: more strength: its text reads its strength when it comes | yes |
| n615 | Vesemir: Mentor, Berengar | Vesemir: Mentor | Berengar | line is a Witcher it asks for | type: is a Witcher it asks for | yes |
| n616 | Holger Blackhand, Tidecloak Hideaway | Holger Blackhand | Tidecloak Hideaway | line is a Pirate it asks for | type: is a Pirate it asks for | yes |
| n617 | Imposter, Torres var Emreis: Founder | Imposter | Torres var Emreis: Founder | line creates cards | type: creates cards: Torres var Emreis: Founder copys them | yes |
| n618 | Vrygheff, Alba Armored Cavalry | Vrygheff | Alba Armored Cavalry | none repeats its effects | - | yes |
| n619 | Syanna, Alba Spearman | Syanna | Alba Spearman | line repeats its Deploy effects | repeats: repeats its Deploy effects; also repeats its effects | yes |
| n620 | Syanna, Aglaïs | Syanna | Aglaïs | line repeats its Deploy effects | repeats: repeats its Deploy effects; also repeats its effects | yes |
| n621 | Onslaught, Tidecloak Hideaway | Onslaught | Tidecloak Hideaway | none gives it Armor | - | yes |
| n622 | Onslaught, An Craite Longship | Onslaught | An Craite Longship | none gives it Armor | - | yes |
| n623 | Crach an Craite, Dimun Pirate | Crach an Craite | Dimun Pirate | none can give it Armor | - | yes |
| n624 | Crach an Craite, Deranged Corsair | Crach an Craite | Deranged Corsair | none can give it Armor | - | yes |
| n625 | Inspirational Ballad, Berengar | Inspirational Ballad | Berengar | none can give it Vitality | - | yes |
| n626 | Witch Hunter, Vigilantes | Witch Hunter | Vigilantes | line makes enemy units get Bounty | type: makes enemy units get Bounty | yes |
| n627 | Bernard Loredo, Northern Wind | Bernard Loredo | Northern Wind | none dies by its own effect: Northern Wind Banishes them | - | yes |
| n628 | Berengar, Hjalmar an Craite | Berengar | Hjalmar an Craite | line dies by its own effect: Hjalmar an Craite Banishes them | type: dies by its own effect: Hjalmar an Craite Banishes them | yes |
| n629 | Naiad Fledgling, Frog | Naiad Fledgling | Frog | none keeps the Vitality it gives itself off it | - | yes |
| n630 | Naiad Fledgling, Cat Witcher Adept | Naiad Fledgling | Cat Witcher Adept | none keeps the Vitality it gives itself off it | - | yes |
| n631 | Naiad Fledgling, Nature's Gift | Naiad Fledgling | Nature's Gift | none keeps the Vitality it gives itself off it | - | yes |
| n632 | Frog, Naiad Fledgling | Frog | Naiad Fledgling | line gives it Vitality, which it takes off for its own strength | keyword: gives it Vitality, which it takes off for its own strength (when next t | yes |
| n633 | Cat Witcher Adept, Naiad Fledgling | Cat Witcher Adept | Naiad Fledgling | line gives it Vitality, which it takes off for its own strength | keyword: gives it Vitality, which it takes off for its own strength | yes |
| n634 | Frog Mating Season, Naiad Fledgling | Frog Mating Season | Naiad Fledgling | line gives it Vitality, which it takes off for its own strength | keyword: gives it Vitality, which it takes off for its own strength | yes |
| n635 | Nature's Gift, Freixenet | Nature's Gift | Freixenet | line gives it Vitality for its effect | type: gives it Vitality for its effect; also makes stronger: does what it waits  | yes |
| n636 | Dwimveandra, Flotsam | Dwimveandra | Flotsam | line lets you use it again | waits: lets you use it again | yes |
| n637 | Naglfar Crew, Lara Dorren | Naglfar Crew | Lara Dorren | none kills it for its death effect | - | yes |
| n638 | Naglfar Crew, Nightwraith | Naglfar Crew | Nightwraith | none kills it for its death effect | - | yes |
| n639 | Red Riders: Charge, Lara Dorren | Red Riders: Charge | Lara Dorren | none kills it for its death effect | - | yes |
| n640 | Red Riders: Charge, Nightwraith | Red Riders: Charge | Nightwraith | none kills it for its death effect | - | yes |
| n641 | Ghoul, Dettlaff: Higher Vampire | Ghoul | Dettlaff: Higher Vampire | none kills it for its death effect | - | yes |
| n642 | Aen Elle Aristocrat, Endrega Eggs | Aen Elle Aristocrat | Endrega Eggs | none kills it for its death effect | - | yes |
| n643 | Biting Frost, Archespore | Biting Frost | Archespore | none kills it for its death effect | - | yes |
| n644 | Forktail, Bridge Troll | Forktail | Bridge Troll | line kills it for its death effect | waits: kills it for its death effect | yes |
| n645 | Ge'els, Lara Dorren | Ge'els | Lara Dorren | line puts it into play from the deck | puts: puts it into play from the deck; also triggers: plays it: its effect goes  | yes |
| n646 | Mobilization: NR Devotion Undead Army | Redanian Secret Service | Kaedweni Revenant | none  | - | yes |
| n647 | Mobilization: NR Devotion Undead Army | Sabrina Glevissig | Kaedweni Revenant | line leaves weak units for its kill | waits: leaves weak units for its kill | yes |
| n648 | Mobilization: NR Devotion Undead Army | Philippa: Blind Fury | Kaedweni Revenant | line leaves weak units for its kill | waits: leaves weak units for its kill | yes |
| n649 | Mobilization: NR Devotion Undead Army | Vernon Roche | Kaedweni Revenant | none  | - | yes |
| n650 | Mobilization: NR Devotion Undead Army | Drakenborg | Vincent Meis | none  | - | yes |
| n651 | Mobilization: NR Devotion Undead Army | Kaedweni Revenant | Vincent Meis | line its 1 damage kills what it sets to strength 1 | waits: its 1 damage kills what it sets to strength 1 | yes |
| n652 | Mobilization: NR Devotion Undead Army | Redanian Archer | Vincent Meis | line its 1 damage kills what it sets to strength 1 | waits: its 1 damage kills what it sets to strength 1 | yes |
| n653 | Patricidal Fury: RnR Seagulls Sove Compass | Hammond | Ragh Nar Roog | line moves an enemy unit into the row it hits | moves: moves an enemy unit into the row it hits | yes |
| n654 | Field Medic, Caravan Guard | Field Medic | Caravan Guard | none can give it more strength | - | yes |
| n655 | Shaping Nature: Vitality, Yennefer: Divination | Shaping Nature: Vitality | Yennefer: Divination | none can give it more strength | - | yes |
| n656 | Chimera, Ozzrel | Chimera | Ozzrel | none gives it more strength | type: makes your units die: Ozzrel Consumes them | yes |
| n657 | Squire, Redanian Knight | Squire | Redanian Knight | line more strength: its text reads its strength when it comes | stronger: more strength: its text reads its strength when it comes | yes |
| n658 | Anna Strenger, Redanian Knight | Anna Strenger | Redanian Knight | line can give it more strength | stronger: can give it more strength | yes |
| n659 | Tactical Advantage, Toad Prince | Tactical Advantage | Toad Prince | none give it more strength | - | yes |
| n660 | Bone Talisman, Kikimore Stalker | Bone Talisman | Kikimore Stalker | none gives it more strength | - | yes |
| n661 | Target Practice, Knight-Errant | Target Practice | Knight-Errant | line can give it more strength | type: Target Practice puts your units there, and Knight-Errant acts on units nex | yes |
| n662 | Squire, Knight-Errant | Squire | Knight-Errant | line its text reads its strength when it comes | stronger: more strength: its text reads its strength when it comes | yes |
| n664 | Coup de Grâce, Impera Enforcers | Coup de Grâce | Impera Enforcers | none leaves weak units for its kill | - | yes |
| n665 | Waylay, Milva: Sharpshooter | Waylay | Milva: Sharpshooter | none leaves weak units for its kill | - | yes |
| n668 | Sabrina Glevissig, Kaedweni Revenant | Sabrina Glevissig | Kaedweni Revenant | line leaves weak units for its kill | waits: leaves weak units for its kill | yes |
| n671 | Magic Compass, Gregoire de Gorgon | Magic Compass | Gregoire de Gorgon | none gives it units to kill | waits: plays it: its effect goes off | yes |
| n673 | Redanian Secret Service, Kaedweni Revenant | Redanian Secret Service | Kaedweni Revenant | none  | - | yes |
| n674 | Geralt: Professional, Wolfsbane | Geralt: Professional | Wolfsbane | line its 1 damage kills what it sets to strength 1 | waits: its 1 damage kills what it sets to strength 1 | yes |
| n675 | Drakenborg, Redanian Secret Service | Drakenborg | Redanian Secret Service | none puts it into play: its summon effect goes off | waits: makes your units get a keyword or status | yes |
| n676 | Drakenborg, Redanian Secret Service | Drakenborg | Redanian Secret Service | none does what it waits for or counts | waits: makes your units get a keyword or status | yes |
| n677 | Emhyr var Emreis, Impera Enforcers | Emhyr var Emreis | Impera Enforcers | none plays it: its effect goes off | type: makes enemy units get Spying | yes |
| n678 | Emhyr var Emreis, Impera Enforcers | Emhyr var Emreis | Impera Enforcers | none puts it into play from the hand | type: makes enemy units get Spying | yes |
| n679 | Fercart, Impera Enforcers | Fercart | Impera Enforcers | line makes enemy units get Spying | type: makes enemy units get Spying | yes |
| n680 | Treason, Impera Enforcers | Treason | Impera Enforcers | line makes enemy units get Spying | type: makes enemy units get Spying; also triggers: leaves weak units for its kil | yes |
| n681 | Damsel in Distress, Knight-Errant | Damsel in Distress | Knight-Errant | none puts it into play from the deck | type: Damsel in Distress puts your units there, and Knight-Errant acts on units  | yes |
| n682 | Damsel in Distress, Redanian Knight | Damsel in Distress | Redanian Knight | none puts it into play from the deck | type: Damsel in Distress puts your units there, and Redanian Knight acts on unit | yes |
| n685 | Rage of the Sea: Fulmar rain ft. Otkell and Melusine | Sigrdrifa's Rite | Rage of the Sea | none brings it back: its summon effect goes off | - | yes |
| n686 | Mobilization, Lyrian Arbalest | Mobilization | Lyrian Arbalest | none puts it into play: its summon effect goes off | waits: is a card whose playing sets off its effect | yes |
| n687 | Mobilization: NR Devotion Undead Army | Drakenborg | Vincent Meis | none  | - | yes |
| n688 | Fauve, Hamadryad | Fauve | Hamadryad | line sets off its Symbiosis | waits: plays a Nature card, which sets off its Symbiosis | yes |
| n689 | John Natalis, Battering Ram | John Natalis | Battering Ram | line sets off its Resupply | type: is a Soldier it asks for; also triggers: plays a Warfare card, which sets  | yes |
| n690 | Ferko the Sculptor, Sir Skewertooth | Ferko the Sculptor | Sir Skewertooth | line sets off its Intimidate | waits: plays a Crime card, which sets off its Intimidate | yes |
| n691 | Shady Vendor, Imperial Diviner | Shady Vendor | Imperial Diviner | line sets off its Assimilate | waits: creates a card, which sets off its Assimilate | yes |
| n693 | Mahakam Pass, Naiad Fledgling | Mahakam Pass | Naiad Fledgling | none  | - | yes |
| n694 | Fauve, Koshchey | Fauve | Koshchey | none  | - | yes |
| n697 | Lambert: Swordmaster, Kaedweni Revenant | Lambert: Swordmaster | Kaedweni Revenant | none copies itself | waits: leaves weak units for its kill | yes |
| n698 | Vilgefortz, Poor Fucking Infantry | Vilgefortz | Poor Fucking Infantry | none  | - | yes |
| n699 | Drakenborg, Poor Fucking Infantry | Drakenborg | Poor Fucking Infantry | none  | - | yes |
| n700 | Loc Feainn: Convergence, Pavko Gale | Loc Feainn: Convergence | Pavko Gale | none makes a unit it asks for | - | yes |
| n701 | Pavko Gale, Mysteries of Loc Feainn | Pavko Gale | Mysteries of Loc Feainn | line is a unit whose playing sets off its effect | waits: is a unit whose playing sets off its effect | yes |
