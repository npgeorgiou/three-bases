# Stored rows of 19 cards, made by check_table.py
Every table as stored; card, keyword, type and name-part ids are shown as names. Other ids join the tables.

## card (19 rows)

| id | game | name | category | speed | cost | power | health | regions | rarity | is_keyword | is_stub | text (library, not stored here) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 750652 | runeterra | Jae Medarda | unit |  | 6.0 | 5.0 | 5.0 | Piltover & Zaun | epic | 0 | 0 | When I'm targeted, draw 1. |
| 750699 | runeterra | Ashe | hero |  | 4.0 | 5.0 | 3.0 | Freljord | champion | 0 | 0 | Attack: Frostbite the strongest enemy. Level up: You've reduced the Power of 5+ enemies to 0. When I level up, create a Crystal Arrow on top of deck. |
| 750744 | runeterra | Soul Shepherd | unit |  | 2.0 | 2.0 | 3.0 | Shadow Isles | common | 0 | 0 | When you summon an Ephemeral ally, grant it +1/+1. |
| 750797 | runeterra | Insightful Investigator | unit |  | 4.0 | 3.0 | 4.0 | Piltover & Zaun | rare | 0 | 0 | When you play a 2 cost card, draw 1 and grant it Fleeting. |
| 750811 | runeterra | Shipwreck Hoarder | unit |  | 7.0 | 7.0 | 5.0 | Bilgewater | epic | 0 | 0 | Keywords: Deep. When I'm summoned, Toss 2 and create 2 Treasures in your deck. |
| 750869 | runeterra | Ursine Spiritwalker | unit |  | 5.0 | 4.0 | 6.0 | Freljord | common | 0 | 0 | Keywords: Plunder. Plunder: I transform into Stormclaw Ursine. |
| 750893 | runeterra | Concerted Strike | spell | fast | 5.0 |  |  | Demacia | common | 0 | 0 | Pick an enemy. 2 allies strike it one after another. |
| 750908 | runeterra | Eye of the Dragon | unit |  | 2.0 | 1.0 | 3.0 | Ionia | epic | 0 | 0 | Keywords: Attune, Flow. Round Start: Flow: Summon a Dragonling. |
| 751162 | runeterra | Hibernating Rockbear | building |  | 2.0 |  |  | Shurima | common | 0 | 0 | Keywords: Countdown, Landmark. Countdown 3: Summon a Grumpy Rockbear. |
| 751440 | runeterra | Inner Beast | spell | burst | 2.0 |  |  | Freljord | common | 0 | 0 | Give an ally +1/+1 this round. Create a Stance Swap in hand. |
| 751550 | runeterra | Petricite Broadwing | unit |  | 2.0 | 0.0 | 3.0 | Demacia | rare | 0 | 0 | Keywords: Formidable. When you summon another ally, grant me Challenger. |
| 751917 | runeterra | All-Seeing Oracle | unit |  | 4.0 | 4.0 | 3.0 | Ionia | rare | 0 | 0 | Play: Pick 1 of 3 Fast or Slow spells in the enemy's hand or deck. Create a Carvings of Divination for it. |
| 752095 | runeterra | Brynhir Thundersong | unit |  | 3.0 | 3.0 | 3.0 | Freljord | epic | 0 | 0 | Play: Obliterate a unit in hand to summon a Stormcarved Spire that has Countdown equal to its cost and summons an exact copy of the unit. (minimum 1) |
| 796508 | runeterra | Zoe (level 2) | hero |  | 1.0 |  |  | Targon |  | 0 | 0 | Keywords: Elusive, Missing Translation. When I level up, grant your Nexus "When you summon an ally, grant its keywords to all allies." Nexus Strike: Create a Behold the Infinite that costs 0 in hand. |
| 796535 | runeterra | Malphite (level 2) | hero |  | 7.0 |  |  | Targon |  | 0 | 0 | Keywords: Tough. Play: Stun an enemy. When I'm summoned or Round Start: If you have the attack token, create an Unstoppable Force in hand. |
| 796575 | runeterra | Samira (level 2) | hero |  | 2.0 |  |  | Noxus |  | 0 | 0 | Keywords: Quick Attack, Plunder. Plunder or strike: Create a Flair in hand if you don't already have one. When you play 6 cards, Rally. Resets when you start a round with the attack token. |
| 796926 | runeterra | Bouncing Bomb (created) | spell |  | 3.0 |  |  | Bandle City |  | 0 | 0 | Keywords: Slow. Deal 2 to a unit. |
| 797064 | runeterra | Xolaani | unit |  | 6.0 |  |  | Shurima |  | 0 | 0 | Keywords: Overwhelm, Last Breath. To play me, kill an ally. Last Breath: Create a The Darkin Bloodletters in hand. |
| 797134 | runeterra | Maryam, Temple Caretaker (created) | unit |  | 2.0 |  |  | Piltover & Zaun |  | 0 | 0 | Play: Updraft 1 to refill your spell mana. |

## card_keyword (15 rows)

| card | keyword |
|---|---|
| Shipwreck Hoarder | Deep |
| Ursine Spiritwalker | Plunder |
| Eye of the Dragon | Attune |
| Eye of the Dragon | Flow |
| Hibernating Rockbear | Countdown |
| Hibernating Rockbear | Landmark |
| Petricite Broadwing | Formidable |
| Zoe (level 2) | Elusive |
| Zoe (level 2) | Missing Translation |
| Malphite (level 2) | Tough |
| Samira (level 2) | Quick Attack |
| Samira (level 2) | Plunder |
| Bouncing Bomb (created) | Slow |
| Xolaani | Overwhelm |
| Xolaani | Last Breath |

## card_type (2 rows)

| card | type |
|---|---|
| Shipwreck Hoarder | Sea Monster |
| Xolaani | Darkin |

## card_link (29 rows)

| src | rel | dst |
|---|---|---|
| Ashe | generates | Ashe (level 2) |
| Ashe | generates | Crystal Arrow |
| Ashe | generates | Ashe's Flash Freeze |
| Ashe | transforms_into | Ashe (level 2) |
| Shipwreck Hoarder | generates | Keelbreaker |
| Shipwreck Hoarder | generates | Treasure Trove |
| Shipwreck Hoarder | generates | Vicious Platewyrm |
| Shipwreck Hoarder | generates | Platewyrm Egg |
| Ursine Spiritwalker | generates | Stormclaw Ursine |
| Eye of the Dragon | generates | Dragonling |
| Inner Beast | generates | Stance Swap |
| Inner Beast | generates | Ram Stance |
| Inner Beast | generates | Wildclaw Stance |
| Inner Beast | generates | Boar Stance |
| Inner Beast | generates | Bear Stance |
| All-Seeing Oracle | generates | Carvings of Divination |
| Brynhir Thundersong | generates | Stormcarved Spire |
| Zoe (level 2) | generates | Paddle Star |
| Zoe (level 2) | generates | Behold the Infinite |
| Zoe (level 2) | generates | Zoe |
| Zoe (level 2) | generates | Zoe's Sleepy Trouble Bubble |
| Malphite (level 2) | generates | Malphite |
| Malphite (level 2) | generates | Unstoppable Force |
| Malphite (level 2) | generates | Malphite's Ground Slam |
| Malphite (level 2) | generates | Rockslide |
| Samira (level 2) | generates | Samira |
| Samira (level 2) | generates | Flair |
| Samira (level 2) | generates | Samira's All Out |
| Xolaani | generates | The Darkin Bloodletters |

## ability (29 rows)

| id | card | seq | event | lim | given_by_effect |
|---|---|---|---|---|---|
| 176 | Jae Medarda | 0 | 201 |  |  |
| 223 | Ashe | 0 | 253 |  |  |
| 224 | Ashe | 1 | 254 |  |  |
| 225 | Ashe | 2 | 256 |  |  |
| 268 | Soul Shepherd | 0 | 301 |  |  |
| 324 | Insightful Investigator | 0 | 368 |  |  |
| 336 | Shipwreck Hoarder | 0 | 381 |  |  |
| 412 | Ursine Spiritwalker | 0 | 466 |  |  |
| 436 | Concerted Strike | 0 | 492 |  |  |
| 454 | Eye of the Dragon | 0 | 514 |  |  |
| 760 | Hibernating Rockbear | 0 | 853 |  |  |
| 1123 | Inner Beast | 0 | 1284 |  |  |
| 1265 | Petricite Broadwing | 0 | 1453 |  |  |
| 1729 | All-Seeing Oracle | 0 | 1963 |  |  |
| 1979 | Brynhir Thundersong | 0 | 2240 |  |  |
| 1980 |  | 0 | 2241 |  | 2808 |
| 2087 | Zoe (level 2) | 0 | 2360 |  |  |
| 2088 |  | 0 | 2361 |  | 2958 |
| 2089 | Zoe (level 2) | 1 | 2362 |  |  |
| 2141 | Malphite (level 2) | 0 | 2418 |  |  |
| 2142 | Malphite (level 2) | 1 | 2419 |  |  |
| 2143 | Malphite (level 2) | 2 | 2420 |  |  |
| 2223 | Samira (level 2) | 0 | 2507 |  |  |
| 2224 | Samira (level 2) | 1 | 2508 |  |  |
| 2225 | Samira (level 2) | 2 | 2509 |  |  |
| 2591 | Bouncing Bomb (created) | 0 | 2893 |  |  |
| 2720 | Xolaani | 0 | 3030 |  |  |
| 2721 | Xolaani | 1 | 3031 |  |  |
| 2799 | Maryam, Temple Caretaker (created) | 0 | 3110 |  |  |

## event (31 rows)

| id | event | actor | object |
|---|---|---|---|
| 201 | targeted |  | 434 |
| 253 | attacks | 546 |  |
| 254 | always |  |  |
| 255 | stat_changed | 548 | 549 |
| 256 | levels_up |  | 551 |
| 301 | summoned | 646 | 647 |
| 368 | played | 780 | 781 |
| 381 | summoned |  | 812 |
| 466 | played |  | 985 |
| 492 | played |  | 1035 |
| 514 | round_start |  |  |
| 853 | countdown_done |  | 1832 |
| 1284 | played |  | 2719 |
| 1453 | summoned |  | 3112 |
| 1963 | played |  | 4308 |
| 2240 | played |  | 4914 |
| 2241 | countdown_done |  | 4918 |
| 2360 | levels_up |  | 5177 |
| 2361 | summoned | 5179 | 5180 |
| 2362 | strikes_nexus | 5183 |  |
| 2418 | played |  | 5307 |
| 2419 | summoned |  | 5309 |
| 2420 | round_start |  |  |
| 2507 | played |  | 5516 |
| 2508 | strikes | 5518 |  |
| 2509 | played | 5520 |  |
| 2510 | played | 5521 |  |
| 2893 | played |  | 6458 |
| 3030 | played |  | 6847 |
| 3031 | dies |  | 6849 |
| 3110 | played |  | 7034 |

## cond (9 rows)

| id | ability | keyword | test | of_target | attr | op | n | span | event | ref_keyword | value |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 42 | 224 |  | event_count |  |  | ge | 275 | this_game | 255 |  |  |
| 80 | 412 |  | keyword_condition |  |  |  |  |  |  | Plunder |  |
| 88 | 454 |  | keyword_condition |  |  |  |  |  |  | Flow |  |
| 532 | 2142 |  | attack_token |  |  | is |  |  |  |  |  |
| 533 | 2143 |  | attack_token |  |  | is |  |  |  |  |  |
| 557 | 2223 |  | keyword_condition |  |  |  |  |  |  | Plunder |  |
| 558 | 2223 |  | have | 5517 |  | not |  |  |  |  |  |
| 559 | 2224 |  | have | 5519 |  | not |  |  |  |  |  |
| 560 | 2225 |  | event_count |  |  | ge | 2548 | this_game | 2510 |  |  |

## effect (37 rows)

| id | ability | seq | act | on_target | to_target | zone | card_ref | keyword_ref | type_ref | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 220 | 176 | 0 | draw | 435 |  |  |  |  |  |  |  |
| 281 | 223 | 0 | keyword_action | 547 |  |  |  | Frostbite |  |  |  |
| 282 | 224 | 0 | level_up | 550 |  |  |  |  |  |  |  |
| 283 | 225 | 0 | create | 552 |  | deck_top | Crystal Arrow |  |  |  |  |
| 336 | 268 | 0 | stat_change | 648 |  |  |  |  |  | permanent |  |
| 411 | 324 | 0 | draw | 782 |  |  |  |  |  |  |  |
| 412 | 324 | 1 | give_keyword | 783 |  |  |  | Fleeting |  | permanent | and |
| 428 | 336 | 0 | keyword_action | 813 |  |  |  | Toss |  |  |  |
| 429 | 336 | 1 | create |  |  | deck | Treasure |  |  |  | and |
| 525 | 412 | 0 | transform | 986 |  |  | Stormclaw Ursine |  |  |  |  |
| 554 | 436 | 0 | strike | 1036 | 1037 |  |  |  |  |  |  |
| 579 | 454 | 0 | summon |  |  | board | Dragonling |  |  |  |  |
| 1015 | 760 | 0 | summon |  |  | board | Grumpy Rockbear |  |  |  |  |
| 1519 | 1123 | 0 | stat_change | 2720 |  |  |  |  |  | this_round |  |
| 1520 | 1123 | 1 | create |  |  | hand | Stance Swap |  |  |  | and |
| 1735 | 1265 | 0 | give_keyword | 3113 |  |  |  | Challenger |  | permanent |  |
| 2461 | 1729 | 0 | choose_card | 4309 |  |  |  |  |  |  |  |
| 2462 | 1729 | 1 | create |  |  | hand | Carvings of Divination |  |  |  | then |
| 2806 | 1979 | 0 | obliterate | 4915 |  |  |  |  |  |  |  |
| 2807 | 1979 | 1 | summon | 4916 |  |  | Stormcarved Spire |  |  |  | if_done |
| 2808 | 1979 | 2 | give_ability | 4917 |  |  |  |  |  |  | and |
| 2809 | 1980 | 0 | copy | 4919 |  | board |  |  |  |  |  |
| 2958 | 2087 | 0 | give_ability | 5178 |  |  |  |  |  | permanent |  |
| 2959 | 2088 | 0 | copy_keywords | 5181 | 5182 |  |  |  |  | permanent |  |
| 2960 | 2089 | 0 | create |  |  | hand | Behold the Infinite |  |  |  |  |
| 2961 | 2089 | 1 | cost_set | 5184 |  |  |  |  |  | permanent | then |
| 3044 | 2141 | 0 | stun | 5308 |  |  |  |  |  | this_round |  |
| 3045 | 2142 | 0 | create |  |  | hand | Unstoppable Force |  |  |  |  |
| 3046 | 2143 | 0 | create |  |  | hand | Unstoppable Force |  |  |  |  |
| 3159 | 2223 | 0 | create |  |  | hand | Flair |  |  |  |  |
| 3160 | 2224 | 0 | create |  |  | hand | Flair |  |  |  |  |
| 3161 | 2225 | 0 | gain_attack_token | 5522 |  |  |  |  |  |  |  |
| 3786 | 2591 | 0 | damage | 6459 |  |  |  |  |  |  |  |
| 4018 | 2720 | 0 | kill | 6848 |  |  |  |  |  |  |  |
| 4019 | 2721 | 0 | create |  |  | hand | The Darkin Bloodletters |  |  |  |  |
| 4123 | 2799 | 0 | keyword_action | 7035 |  |  |  | Updraft |  |  |  |
| 4124 | 2799 | 1 | mana_gain | 7036 |  |  |  |  |  |  | if_done |

## param (13 rows)

| effect | param | amount | value |
|---|---|---|---|
| 220 | amount | 214 |  |
| 336 | power | 328 |  |
| 336 | health | 329 |  |
| 411 | amount | 391 |  |
| 428 | amount | 409 |  |
| 429 | amount | 410 |  |
| 1519 | power | 1250 |  |
| 1519 | health | 1251 |  |
| 2461 | options | 1989 |  |
| 2961 | cost | 2408 |  |
| 3786 | amount | 2939 |  |
| 4123 | amount | 3166 |  |
| 4124 | amount | 3167 |  |

## target (62 rows)

| id | kind | side | pick | n | zone | by_attr |
|---|---|---|---|---|---|---|
| 434 |  |  | self |  |  |  |
| 435 | card | mine |  |  | deck_top |  |
| 546 |  |  | self |  |  |  |
| 547 | unit | enemy | strongest |  | board |  |
| 548 | player | mine |  |  |  |  |
| 549 | unit | enemy |  |  |  |  |
| 550 |  |  | self |  |  |  |
| 551 |  |  | self |  |  |  |
| 552 | card | mine |  |  |  |  |
| 646 | player | mine |  |  |  |  |
| 647 | unit | mine |  |  |  |  |
| 648 |  |  | it |  |  |  |
| 780 | player | mine |  |  |  |  |
| 781 | card |  |  |  |  |  |
| 782 | card | mine |  |  | deck_top |  |
| 783 | card | mine | it |  | hand |  |
| 812 |  |  | self |  |  |  |
| 813 | card | mine | random |  | deck |  |
| 985 |  |  | self |  |  |  |
| 986 |  |  | self |  |  |  |
| 1035 |  |  | self |  |  |  |
| 1036 | unit | mine | chosen | 511 | board |  |
| 1037 | unit | enemy | chosen |  | board |  |
| 1832 |  |  | self |  |  |  |
| 2719 |  |  | self |  |  |  |
| 2720 | unit | mine | chosen |  | board |  |
| 3112 | unit | mine |  |  |  |  |
| 3113 |  |  | self |  |  |  |
| 4308 |  |  | self |  |  |  |
| 4309 | card | enemy |  |  | deck |  |
| 4914 |  |  | self |  |  |  |
| 4915 | card | mine | chosen |  | hand |  |
| 4916 | unit | mine |  |  |  |  |
| 4917 |  |  | it |  |  |  |
| 4918 |  |  | self |  |  |  |
| 4919 | card |  | it |  |  |  |
| 5177 |  |  | self |  |  |  |
| 5178 | player | mine |  |  |  |  |
| 5179 | player | mine |  |  |  |  |
| 5180 | unit | mine | all |  | board |  |
| 5181 | unit | mine | all |  | board |  |
| 5182 |  |  | it |  |  |  |
| 5183 |  |  | self |  |  |  |
| 5184 | card | mine |  |  | hand |  |
| 5307 |  |  | self |  |  |  |
| 5308 | unit | enemy | chosen |  | board |  |
| 5309 |  |  | self |  |  |  |
| 5516 |  |  | self |  |  |  |
| 5517 | card | mine |  |  | hand |  |
| 5518 |  |  | self |  |  |  |
| 5519 | card | mine |  |  | hand |  |
| 5520 | player | mine |  |  |  |  |
| 5521 | player | mine |  |  |  |  |
| 5522 | player | mine |  |  |  |  |
| 6458 |  |  | self |  |  |  |
| 6459 | unit | any | chosen |  | board |  |
| 6847 |  |  | self |  |  |  |
| 6848 | unit | mine | chosen |  | board |  |
| 6849 |  |  | self |  |  |  |
| 7034 |  |  | self |  |  |  |
| 7035 | card | mine |  |  | hand |  |
| 7036 | spell_mana | mine |  |  |  |  |

## filter (10 rows)

| id | target | attr | op | n | ref_card | ref_keyword | ref_type | ref_word | val |
|---|---|---|---|---|---|---|---|---|---|
| 115 | 549 | power | eq | 276 |  |  |  |  |  |
| 145 | 647 | state | is |  |  |  |  |  | ephemeral |
| 166 | 781 | cost | eq | 390 |  |  |  |  |  |
| 623 | 3112 | card | not |  | Petricite Broadwing |  |  |  |  |
| 917 | 4309 | category | in |  |  |  |  |  | fast_spell |
| 918 | 4309 | category | in |  |  |  |  |  | slow_spell |
| 1065 | 4915 | category | is |  |  |  |  |  | follower |
| 1115 | 5184 | card | is |  | Behold the Infinite |  |  |  |  |
| 1212 | 5517 | card | is |  | Flair |  |  |  |  |
| 1213 | 5519 | card | is |  | Flair |  |  |  |  |

## amount (18 rows)

| id | x | value | of_target | attr | event | span | inner |
|---|---|---|---|---|---|---|---|
| 214 | n | 1.0 |  |  |  |  |  |
| 275 | n | 5.0 |  |  |  |  |  |
| 276 | n | 0.0 |  |  |  |  |  |
| 328 | n | 1.0 |  |  |  |  |  |
| 329 | n | 1.0 |  |  |  |  |  |
| 390 | n | 2.0 |  |  |  |  |  |
| 391 | n | 1.0 |  |  |  |  |  |
| 409 | n | 2.0 |  |  |  |  |  |
| 410 | n | 2.0 |  |  |  |  |  |
| 511 | n | 2.0 |  |  |  |  |  |
| 1250 | n | 1.0 |  |  |  |  |  |
| 1251 | n | 1.0 |  |  |  |  |  |
| 1989 | n | 3.0 |  |  |  |  |  |
| 2408 | n | 0.0 |  |  |  |  |  |
| 2548 | n | 6.0 |  |  |  |  |  |
| 2939 | n | 2.0 |  |  |  |  |  |
| 3166 | n | 1.0 |  |  |  |  |  |
| 3167 | full |  |  |  |  |  |  |

## amount_item (0 rows)

| amount | item |
|---|---|
