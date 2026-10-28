# Stored rows of 19 cards (check_table.py)
One row per effect. The bold row above a card's rows is its text (not stored). Targets, events, conditions and amounts are written in place as their stored fields.

| card | ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Jae Medarda** | **When I'm targeted, draw 1.** | | | | | | | | | | | | | | | | |
| Jae Medarda | 0 | targeted |  | pick=self |  |  | 0 | draw | kind=card side=mine zone=deck_top |  |  |  |  |  | amount=1 |  |  |
| **Ashe** | **Attack: Frostbite the strongest enemy. Level up: You've reduced the Power of 5+ enemies to 0. When I level up, create a Crystal Arrow on top of deck.** | | | | | | | | | | | | | | | | |
| Ashe | 0 | attacks | pick=self |  |  |  | 0 | keyword_action | kind=unit side=enemy pick=strongest zone=board |  |  |  | Frostbite |  |  |  |  |
| Ashe | 1 | always |  |  |  | (test=event_count op=ge n=5 span=this_game event=(event=stat_changed actor=(kind=player side=mine) object=(kind=unit side=enemy with[power eq 0]))) | 0 | level_up | pick=self |  |  |  |  |  |  |  |  |
| Ashe | 2 | levels_up |  | pick=self |  |  | 0 | create | kind=card side=mine |  | deck_top | Crystal Arrow |  |  |  |  |  |
| **Soul Shepherd** | **When you summon an Ephemeral ally, grant it +1/+1.** | | | | | | | | | | | | | | | | |
| Soul Shepherd | 0 | summoned | kind=player side=mine | kind=unit side=mine with[state is ephemeral] |  |  | 0 | stat_change | pick=it |  |  |  |  |  | power=1; health=1 | permanent |  |
| **Insightful Investigator** | **When you play a 2 cost card, draw 1 and grant it Fleeting.** | | | | | | | | | | | | | | | | |
| Insightful Investigator | 0 | played | kind=player side=mine | kind=card with[cost eq 2] |  |  | 0 | draw | kind=card side=mine zone=deck_top |  |  |  |  |  | amount=1 |  |  |
| Insightful Investigator | 0 | played | kind=player side=mine | kind=card with[cost eq 2] |  |  | 1 | give_keyword | kind=card side=mine pick=it zone=hand |  |  |  | Fleeting |  |  | permanent | and |
| **Shipwreck Hoarder** | **Keywords: Deep. When I'm summoned, Toss 2 and create 2 Treasures in your deck.** (keywords: Deep) | | | | | | | | | | | | | | | | |
| Shipwreck Hoarder | 0 | summoned |  | pick=self |  |  | 0 | keyword_action | kind=card side=mine pick=top zone=deck_top |  |  |  | Toss |  | amount=2 |  |  |
| Shipwreck Hoarder | 0 | summoned |  | pick=self |  |  | 1 | create |  |  | deck | Treasure |  |  | amount=2 |  | and |
| **Ursine Spiritwalker** | **Keywords: Plunder. Plunder: I transform into Stormclaw Ursine.** (keywords: Plunder) | | | | | | | | | | | | | | | | |
| Ursine Spiritwalker | 0 | played |  | pick=self |  | (test=keyword_condition ref=Plunder) | 0 | transform | pick=self |  |  | Stormclaw Ursine |  |  |  |  |  |
| **Concerted Strike** | **Pick an enemy. 2 allies strike it one after another.** | | | | | | | | | | | | | | | | |
| Concerted Strike | 0 | played |  | pick=self |  |  | 0 | strike | kind=unit side=mine pick=chosen n=2 zone=board | kind=unit side=enemy pick=chosen zone=board |  |  |  |  |  |  |  |
| **Eye of the Dragon** | **Keywords: Attune, Flow. Round Start: Flow: Summon a Dragonling.** (keywords: Attune, Flow) | | | | | | | | | | | | | | | | |
| Eye of the Dragon | 0 | round_start |  |  |  | (test=keyword_condition ref=Flow) | 0 | summon |  |  | board | Dragonling |  |  |  |  |  |
| **Hibernating Rockbear** | **Keywords: Countdown, Landmark. Countdown 3: Summon a Grumpy Rockbear.** (keywords: Countdown, Landmark) | | | | | | | | | | | | | | | | |
| Hibernating Rockbear | 0 | countdown_done |  | pick=self |  |  | 0 | summon |  |  | board | Grumpy Rockbear |  |  |  |  |  |
| **Inner Beast** | **Give an ally +1/+1 this round. Create a Stance Swap in hand.** | | | | | | | | | | | | | | | | |
| Inner Beast | 0 | played |  | pick=self |  |  | 0 | stat_change | kind=unit side=mine pick=chosen zone=board |  |  |  |  |  | power=1; health=1 | this_round |  |
| Inner Beast | 0 | played |  | pick=self |  |  | 1 | create |  |  | hand | Stance Swap |  |  |  |  | and |
| **Petricite Broadwing** | **Keywords: Formidable. When you summon another ally, grant me Challenger.** (keywords: Formidable) | | | | | | | | | | | | | | | | |
| Petricite Broadwing | 0 | summoned |  | kind=unit side=mine with[card not Petricite Broadwing] |  |  | 0 | give_keyword | pick=self |  |  |  | Challenger |  |  | permanent |  |
| **All-Seeing Oracle** | **Play: Pick 1 of 3 Fast or Slow spells in the enemy's hand or deck. Create a Carvings of Divination for it.** | | | | | | | | | | | | | | | | |
| All-Seeing Oracle | 0 | played |  | pick=self |  |  | 0 | choose_card | kind=card side=enemy zone=deck with[category in fast_spell; category in slow_spell] |  |  |  |  |  | options=3 |  |  |
| All-Seeing Oracle | 0 | played |  | pick=self |  |  | 1 | create |  |  | hand | Carvings of Divination |  |  |  |  | then |
| **Brynhir Thundersong** | **Play: Obliterate a unit in hand to summon a Stormcarved Spire that has Countdown equal to its cost and summons an exact copy of the unit. (minimum 1)** | | | | | | | | | | | | | | | | |
| Brynhir Thundersong | 0 | played |  | pick=self |  |  | 0 | obliterate | kind=card side=mine pick=chosen zone=hand with[category is unit] |  |  |  |  |  |  |  |  |
| Brynhir Thundersong | 0 | played |  | pick=self |  |  | 1 | summon | kind=unit side=mine |  | board | Stormcarved Spire |  |  | amount={x=stat of=(pick=it) attr=cost} |  | if_done |
| Brynhir Thundersong | 0 | played |  | pick=self |  |  | 2 | copy | pick=it |  | board |  |  |  |  |  | and |
| **Zoe (level 2)** | **Keywords: Elusive, Missing Translation. When I level up, grant your Nexus "When you summon an ally, grant its keywords to all allies." Nexus Strike: Create a Behold the Infinite that costs 0 in hand.** (keywords: Elusive) | | | | | | | | | | | | | | | | |
| Zoe (level 2) | 0 | levels_up |  | pick=self |  |  | 0 | give_ability | kind=player side=mine |  |  |  |  |  |  | permanent |  |
| Zoe (level 2) | 0.0.1 (given by effect 0) | summoned | kind=player side=mine | kind=unit side=mine pick=all zone=board |  |  | 0 | copy_keywords | kind=unit side=mine pick=all zone=board | pick=it |  |  |  |  |  | permanent |  |
| Zoe (level 2) | 1 | strikes_nexus | pick=self |  |  |  | 0 | create |  |  | hand | Behold the Infinite |  |  |  |  |  |
| Zoe (level 2) | 1 | strikes_nexus | pick=self |  |  |  | 1 | cost_set | kind=card side=mine zone=hand with[card is Behold the Infinite] |  |  |  |  |  | cost=0 | permanent | then |
| **Malphite (level 2)** | **Keywords: Tough. Play: Stun an enemy. When I'm summoned or Round Start: If you have the attack token, create an Unstoppable Force in hand.** (keywords: Tough) | | | | | | | | | | | | | | | | |
| Malphite (level 2) | 0 | played |  | pick=self |  |  | 0 | stun | kind=unit side=enemy pick=chosen zone=board |  |  |  |  |  |  | this_round |  |
| Malphite (level 2) | 1 | summoned |  | pick=self |  | (test=attack_token op=is) | 0 | create |  |  | hand | Unstoppable Force |  |  |  |  |  |
| Malphite (level 2) | 2 | round_start |  |  |  | (test=attack_token op=is) | 0 | create |  |  | hand | Unstoppable Force |  |  |  |  |  |
| **Samira (level 2)** | **Keywords: Quick Attack, Plunder. Plunder or strike: Create a Flair in hand if you don't already have one. When you play 6 cards, Rally. Resets when you start a round with the attack token.** (keywords: Quick Attack, Plunder) | | | | | | | | | | | | | | | | |
| Samira (level 2) | 0 | played |  | pick=self |  | (test=keyword_condition ref=Plunder) and (test=have of=(kind=card side=mine zone=hand with[card is Flair]) op=not) | 0 | create |  |  | hand | Flair |  |  |  |  |  |
| Samira (level 2) | 1 | strikes | pick=self |  |  | (test=have of=(kind=card side=mine zone=hand with[card is Flair]) op=not) | 0 | create |  |  | hand | Flair |  |  |  |  |  |
| Samira (level 2) | 2 | played | kind=player side=mine |  |  | (test=event_count op=ge n=6 span=this_game event=(event=played actor=(kind=player side=mine))) | 0 | gain_attack_token | kind=player side=mine |  |  |  |  |  |  |  |  |
| **Bouncing Bomb (created)** | **Keywords: Slow. Deal 2 to a unit.** (keywords: Slow) | | | | | | | | | | | | | | | | |
| Bouncing Bomb (created) | 0 | played |  | pick=self |  |  | 0 | damage | kind=unit side=any pick=chosen zone=board |  |  |  |  |  | amount=2 |  |  |
| **Xolaani** | **Keywords: Overwhelm, Last Breath. To play me, kill an ally. Last Breath: Create a The Darkin Bloodletters in hand.** (keywords: Overwhelm, Last Breath) | | | | | | | | | | | | | | | | |
| Xolaani | 0 | played |  | pick=self |  |  | 0 | kill | kind=unit side=mine pick=chosen zone=board |  |  |  |  |  |  |  |  |
| Xolaani | 1 | dies |  | pick=self |  |  | 0 | create |  |  | hand | The Darkin Bloodletters |  |  |  |  |  |
| **Maryam, Temple Caretaker (created)** | **Play: Updraft 1 to refill your spell mana.** | | | | | | | | | | | | | | | | |
| Maryam, Temple Caretaker (created) | 0 | played |  | pick=self |  |  | 0 | keyword_action | kind=card side=mine zone=hand |  |  |  | Updraft |  | amount=1 |  |  |
| Maryam, Temple Caretaker (created) | 0 | played |  | pick=self |  |  | 1 | mana_gain | kind=spell_mana side=mine |  |  |  |  |  | amount={x=full} |  | if_done |
