# Stored rows of 19 cards (check_table.py)

Each card: its name and text on one line, then its stored rows, one row per effect, then the rows of each keyword it has.
- ability: one numbered "when -> if -> do" unit of the card. Rows with the same ability number are one ability; they happen together, in effect order.
- effect: the step inside the ability. link says how a step joins the step before it: and = also; then = after it, using its result; if_done = only if it happened; or = instead (a choice); instead = replaces it.
- pick=it in a target = the thing the step before acted on (the drawn card, the summoned unit, the chosen enemy).
- A row labelled "keyword X" is what keyword X does; the card has it, so the card does it too.
- Targets, events, conditions and amounts are written in place as their stored fields.

**Jae Medarda**: When I'm targeted, draw 1.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | targeted |  | pick=self |  |  | 0 | draw | kind=card side=mine zone=deck_top |  |  |  |  |  | amount=1 |  |  |

**Ashe**: Attack: Frostbite the strongest enemy. Level up: You've reduced the Power of 5+ enemies to 0. When I level up, create a Crystal Arrow on top of deck.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self |  |  |  | 0 | keyword_action | kind=unit side=enemy pick=strongest zone=board |  |  |  | Frostbite |  |  | unstated |  |
| 1 | always |  |  |  | (test=event_count op=ge n=5 span=this_game event=(event=stat_changed actor=(kind=player side=mine) object=(kind=unit side=enemy with[power eq 0]))) | 0 | level_up | pick=self |  |  |  |  |  |  |  |  |
| 2 | levels_up |  | pick=self |  |  | 0 | create | kind=card side=mine |  | deck_top | Crystal Arrow |  |  |  |  |  |

**Soul Shepherd**: When you summon an Ephemeral ally, grant it +1|+1.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | summoned | kind=player side=mine | kind=unit side=mine with[state is ephemeral] |  |  | 0 | stat_change | pick=it |  |  |  |  |  | power=1; health=1 | permanent |  |

**Insightful Investigator**: When you play a 2 cost card, draw 1 and grant it Fleeting.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played | kind=player side=mine | kind=card with[cost eq 2] |  |  | 0 | draw | kind=card side=mine zone=deck_top |  |  |  |  |  | amount=1 |  |  |
| 0 | played | kind=player side=mine | kind=card with[cost eq 2] |  |  | 1 | give_keyword | kind=card side=mine pick=it zone=hand |  |  |  | Fleeting |  |  | permanent | and |

**Shipwreck Hoarder**: Keywords: Deep. When I'm summoned, Toss 2 and create 2 Treasures in your deck. (keywords: Deep)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | summoned |  | pick=self |  |  | 0 | keyword_action |  |  |  |  | Toss |  | amount=2 |  |  |
| 0 | summoned |  | pick=self |  |  | 1 | create |  |  | deck |  |  | Treasure | amount=2 |  | and |
| keyword Deep: 0 | always |  |  |  | (test=keyword_condition ref=Deep) | 0 | stat_change | pick=self zone=everywhere |  |  |  |  |  | power=3; health=3 | while |  |

**Ursine Spiritwalker**: Keywords: Plunder. Plunder: I transform into Stormclaw Ursine. (keywords: Plunder)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  | (test=keyword_condition ref=Plunder) | 0 | transform | pick=self |  |  | Stormclaw Ursine |  |  |  |  |  |
| keyword Plunder |  |  |  |  |  |  | (no rows: speed, type or reminder keyword) |  |  |  |  |  |  |  |  |  |

**Concerted Strike**: Pick an enemy. 2 allies strike it one after another.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | strike | kind=unit side=mine pick=chosen n=2 zone=board | kind=unit side=enemy pick=chosen zone=board |  |  |  |  |  |  |  |

**Eye of the Dragon**: Keywords: Attune, Flow. Round Start: Flow: Summon a Dragonling. (keywords: Attune, Flow)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | round_start |  |  |  | (test=keyword_condition ref=Flow) | 0 | summon |  |  | board | Dragonling |  |  |  |  |  |
| keyword Attune: 0 | summoned |  | pick=self |  |  | 0 | mana_gain | kind=spell_mana side=mine |  |  |  |  |  | amount=1 |  |  |
| keyword Flow |  |  |  |  |  |  | (no rows: speed, type or reminder keyword) |  |  |  |  |  |  |  |  |  |

**Hibernating Rockbear**: Keywords: Countdown, Landmark. Countdown 3: Summon a Grumpy Rockbear. (keywords: Countdown, Landmark)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | countdown_done |  | pick=self |  |  | 0 | summon |  |  | board | Grumpy Rockbear |  |  |  |  |  |
| keyword Countdown |  |  |  |  |  |  | (a trigger label: event countdown_done) |  |  |  |  |  |  |  |  |  |
| keyword Landmark: 0 | always |  |  |  |  | 0 | cant | pick=self |  |  |  |  |  | event=attacks | while |  |
| keyword Landmark: 0 | always |  |  |  |  | 1 | cant | pick=self |  |  |  |  |  | event=blocks | while | and |
| keyword Landmark: 0 | always |  |  |  |  | 2 | cant | pick=self |  |  |  |  |  | event=damaged | while | and |

**Inner Beast**: Give an ally +1|+1 this round. Create a Stance Swap in hand.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | stat_change | kind=unit side=mine pick=chosen zone=board |  |  |  |  |  | power=1; health=1 | this_round |  |
| 0 | played |  | pick=self |  |  | 1 | create |  |  | hand | Stance Swap |  |  |  |  | and |

**Petricite Broadwing**: Keywords: Formidable. When you summon another ally, grant me Challenger. (keywords: Formidable)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | summoned |  | kind=unit side=mine with[card not Petricite Broadwing] |  |  | 0 | give_keyword | pick=self |  |  |  | Challenger |  |  | permanent |  |
| keyword Formidable: 0 | always |  |  |  |  | 0 | strike_with | pick=self |  |  |  |  |  | attr=health | while |  |

**All-Seeing Oracle**: Play: Pick 1 of 3 Fast or Slow spells in the enemy's hand or deck. Create a Carvings of Divination for it.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | choose_card | kind=card side=enemy zone=deck with[category in fast_spell; category in slow_spell] |  |  |  |  |  | options=3 |  |  |
| 0 | played |  | pick=self |  |  | 1 | create |  |  | hand | Carvings of Divination |  |  |  |  | then |

**Brynhir Thundersong**: Play: Obliterate a unit in hand to summon a Stormcarved Spire that has Countdown equal to its cost and summons an exact copy of the unit. (minimum 1)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | obliterate | kind=card side=mine pick=chosen zone=hand with[category is unit] |  |  |  |  |  |  |  |  |
| 0 | played |  | pick=self |  |  | 1 | summon |  |  | board | Stormcarved Spire |  |  | rounds={x=stat of=(pick=it) attr=cost} |  | if_done |

**Zoe (level 2)**: Keywords: Elusive, Missing Translation. When I level up, grant your Nexus "When you summon an ally, grant its keywords to all allies." Nexus Strike: Create a Behold the Infinite that costs 0 in hand. (keywords: Elusive)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | levels_up |  | pick=self |  |  | 0 | give_ability | kind=player side=mine |  |  |  |  |  |  | permanent |  |
| 0.0.1 (given by effect 0) | summoned | kind=player side=mine | kind=unit side=mine pick=all zone=board |  |  | 0 | copy_keywords | kind=unit side=mine pick=all zone=board | pick=it |  |  |  |  |  | permanent |  |
| 1 | strikes_nexus | pick=self |  |  |  | 0 | create |  |  | hand | Behold the Infinite |  |  |  |  |  |
| 1 | strikes_nexus | pick=self |  |  |  | 1 | cost_set | kind=card side=mine zone=hand with[card is Behold the Infinite] |  |  |  |  |  | cost=0 | permanent | then |
| keyword Elusive: 0 | always |  |  |  |  | 0 | cant | kind=unit side=enemy pick=all with[keyword not Elusive] | pick=self |  |  |  |  | event=blocks | while |  |

**Malphite (level 2)**: Keywords: Tough. Play: Stun an enemy. When I'm summoned or Round Start: If you have the attack token, create an Unstoppable Force in hand. (keywords: Tough)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | stun | kind=unit side=enemy pick=chosen zone=board |  |  |  |  |  |  | this_round |  |
| 1 | summoned |  | pick=self |  | (test=attack_token op=is) | 0 | create |  |  | hand | Unstoppable Force |  |  |  |  |  |
| 2 | round_start |  |  |  | (test=attack_token op=is) | 0 | create |  |  | hand | Unstoppable Force |  |  |  |  |  |
| keyword Tough: 0 | always |  |  |  |  | 0 | damage_reduction | pick=self |  |  |  |  |  | amount=1 | while |  |

**Samira (level 2)**: Keywords: Quick Attack, Plunder. Plunder or strike: Create a Flair in hand if you don't already have one. When you play 6 cards, Rally. Resets when you start a round with the attack token. (keywords: Quick Attack, Plunder)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  | (test=keyword_condition ref=Plunder) and (test=have of=(kind=card side=mine zone=hand with[card is Flair]) op=not) | 0 | create |  |  | hand | Flair |  |  |  |  |  |
| 1 | strikes | pick=self |  |  | (test=have of=(kind=card side=mine zone=hand with[card is Flair]) op=not) | 0 | create |  |  | hand | Flair |  |  |  |  |  |
| 2 | played | kind=player side=mine |  |  | (test=event_count op=ge n=6 span=this_game event=(event=played actor=(kind=player side=mine))) | 0 | gain_attack_token | kind=player side=mine |  |  |  |  |  |  |  |  |
| keyword Quick Attack: 0 | attacks | pick=self |  |  |  | 0 | first_strike | pick=self |  |  |  |  |  |  | this_round |  |
| keyword Plunder |  |  |  |  |  |  | (no rows: speed, type or reminder keyword) |  |  |  |  |  |  |  |  |  |

**Bouncing Bomb (created)**: Keywords: Slow. Deal 2 to a unit. (keywords: Slow)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | damage | kind=unit side=any pick=chosen zone=board |  |  |  |  |  | amount=2 |  |  |
| keyword Slow |  |  |  |  |  |  | (no rows: speed, type or reminder keyword) |  |  |  |  |  |  |  |  |  |

**Xolaani**: Keywords: Overwhelm, Last Breath. To play me, kill an ally. Last Breath: Create a The Darkin Bloodletters in hand. (keywords: Overwhelm, Last Breath)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | kill | kind=unit side=mine pick=chosen zone=board |  |  |  |  |  |  |  |  |
| 1 | dies |  | pick=self |  |  | 0 | create |  |  | hand | The Darkin Bloodletters |  |  |  |  |  |
| keyword Overwhelm: 0 | strikes | pick=self |  |  |  | 0 | excess_damage | kind=player side=enemy |  |  |  |  |  |  |  |  |
| keyword Last Breath |  |  |  |  |  |  | (a trigger label: event dies) |  |  |  |  |  |  |  |  |  |

**Maryam, Temple Caretaker (created)**: Play: Updraft 1 to refill your spell mana.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | keyword_action | kind=card side=mine zone=hand |  |  |  | Updraft |  | amount=1 | unstated |  |
| 0 | played |  | pick=self |  |  | 1 | mana_gain | kind=spell_mana side=mine |  |  |  |  |  | amount={x=full} |  | if_done |

