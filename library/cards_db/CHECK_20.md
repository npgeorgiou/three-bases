# 19 random Runeterra cards with their rows (names put back by rows.py; the stored rows are in CHECK_20_RAW.txt)

**All-Seeing Oracle**
Card text: "Play: Pick 1 of 3 Fast or Slow spells in the enemy's hand or deck. Create a Carvings of Divination for it."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | choose_card | enemy card in deck [category in fast_spell] [category in slow_spell] |  |  | options=3 |  |
| played of self |  | then | create |  | hand | Carvings of Divination |  |  |

**Hibernating Rockbear**
Card text: "Keywords: Countdown, Landmark. Countdown 3: Summon a Grumpy Rockbear."

Keywords (their own rows are on the keyword entries): Countdown, Landmark

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| countdown_done of self |  |  | summon |  | board | Grumpy Rockbear |  |  |

**Ashe**
Card text: "Attack: Frostbite the strongest enemy. Level up: You've reduced the Power of 5+ enemies to 0. When I level up, create a Crystal Arrow on top of deck."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| attacks by self |  |  | keyword_action | strongest enemy unit in board |  | Frostbite |  |  |
| always | event_count stat_changed by mine player of enemy unit [power eq 0] ge 5 this_game |  | level_up | self |  |  |  |  |
| levels_up of self |  |  | create | mine card | deck_top | Crystal Arrow |  |  |

**Shipwreck Hoarder**
Card text: "Keywords: Deep. When I'm summoned, Toss 2 and create 2 Treasures in your deck."

Keywords (their own rows are on the keyword entries): Deep

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of self |  |  | keyword_action | random mine card in deck |  | Toss | amount=2 |  |
| summoned of self |  | and | create |  | deck | Treasure | amount=2 |  |

**Xolaani**
Card text: "Keywords: Overwhelm, Last Breath. To play me, kill an ally. Last Breath: Create a The Darkin Bloodletters in hand."

Keywords (their own rows are on the keyword entries): Overwhelm, Last Breath

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | kill | chosen mine unit in board |  |  |  |  |
| dies of self |  |  | create |  | hand | The Darkin Bloodletters |  |  |

**Eye of the Dragon**
Card text: "Keywords: Attune, Flow. Round Start: Flow: Summon a Dragonling."

Keywords (their own rows are on the keyword entries): Attune, Flow

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| round_start | keyword_condition Flow |  | summon |  | board | Dragonling |  |  |

**Brynhir Thundersong**
Card text: "Play: Obliterate a unit in hand to summon a Stormcarved Spire that has Countdown equal to its cost and summons an exact copy of the unit. (minimum 1)"

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | obliterate | chosen mine card in hand [category is follower] |  |  |  |  |
| played of self |  | if_done | summon | mine unit |  | Stormcarved Spire |  |  |
| played of self |  | and | give_ability | it |  |  |  |  |

**Soul Shepherd**
Card text: "When you summon an Ephemeral ally, grant it +1|+1."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned by mine player of mine unit [state is ephemeral] |  |  | stat_change | it |  |  | power=1, health=1 | permanent |

**Bouncing Bomb (created)**
Card text: "Keywords: Slow. Deal 2 to a unit."

Keywords (their own rows are on the keyword entries): Slow

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | chosen any unit in board |  |  | amount=2 |  |

**Inner Beast**
Card text: "Give an ally +1|+1 this round. Create a Stance Swap in hand."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stat_change | chosen mine unit in board |  |  | power=1, health=1 | this_round |
| played of self |  | and | create |  | hand | Stance Swap |  |  |

**Jae Medarda**
Card text: "When I'm targeted, draw 1."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| targeted of self |  |  | draw | mine card in deck_top |  |  | amount=1 |  |

**Ursine Spiritwalker**
Card text: "Keywords: Plunder. Plunder: I transform into Stormclaw Ursine."

Keywords (their own rows are on the keyword entries): Plunder

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self | keyword_condition Plunder |  | transform | self |  | Stormclaw Ursine |  |  |

**Samira (level 2)**
Card text: "Keywords: Quick Attack, Plunder. Plunder or strike: Create a Flair in hand if you don't already have one. When you play 6 cards, Rally. Resets when you start a round with the attack token."

Keywords (their own rows are on the keyword entries): Quick Attack, Plunder

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self | keyword_condition Plunder; have mine card in hand [card is Flair] not |  | create |  | hand | Flair |  |  |
| strikes by self | have mine card in hand [card is Flair] not |  | create |  | hand | Flair |  |  |
| played by mine player | event_count played by mine player ge 6 this_game |  | gain_attack_token | mine player |  |  |  |  |

**Zoe (level 2)**
Card text: "Keywords: Elusive, Missing Translation. When I level up, grant your Nexus "When you summon an ally, grant its keywords to all allies." Nexus Strike: Create a Behold the Infinite that costs 0 in hand."

Keywords (their own rows are on the keyword entries): Elusive, Missing Translation

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| levels_up of self |  |  | give_ability | mine player |  |  |  | permanent |
| strikes_nexus by self |  |  | create |  | hand | Behold the Infinite |  |  |
| strikes_nexus by self |  | then | cost_set | mine card in hand [card is Behold the Infinite] |  |  | cost=0 | permanent |

**Insightful Investigator**
Card text: "When you play a 2 cost card, draw 1 and grant it Fleeting."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played by mine player of card [cost eq 2] |  |  | draw | mine card in deck_top |  |  | amount=1 |  |
| played by mine player of card [cost eq 2] |  | and | give_keyword | it mine card in hand |  | Fleeting |  | permanent |

**Petricite Broadwing**
Card text: "Keywords: Formidable. When you summon another ally, grant me Challenger."

Keywords (their own rows are on the keyword entries): Formidable

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of mine unit [card not Petricite Broadwing] |  |  | give_keyword | self |  | Challenger |  | permanent |

**Concerted Strike**
Card text: "Pick an enemy. 2 allies strike it one after another."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | strike | 2 chosen mine unit in board to chosen enemy unit in board |  |  |  |  |

**Maryam, Temple Caretaker (created)**
Card text: "Play: Updraft 1 to refill your spell mana."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | keyword_action | mine card in hand |  | Updraft | amount=1 |  |
| played of self |  | if_done | mana_gain | mine spell_mana |  |  | amount=full |  |

**Malphite (level 2)**
Card text: "Keywords: Tough. Play: Stun an enemy. When I'm summoned or Round Start: If you have the attack token, create an Unstoppable Force in hand."

Keywords (their own rows are on the keyword entries): Tough

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stun | chosen enemy unit in board |  |  |  | this_round |
| summoned of self | attack_token is |  | create |  | hand | Unstoppable Force |  |  |
| round_start | attack_token is |  | create |  | hand | Unstoppable Force |  |  |

