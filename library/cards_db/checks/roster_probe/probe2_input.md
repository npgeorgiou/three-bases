# Probe input (made by script)

## D1: "damage_reduction" + "draw" (turbo_fog, no link in the library; pairs from real decks)

### Pair 1 (runeterra, deck Vladimir Braum)
- **Ruthless Raider** (has "damage_reduction"). Text: "Keywords: Overwhelm, Tough."
  Rows: KW: Overwhelm, Tough
- **Whispered Words** (has "draw"). Text: "Reputation: I cost 2 less. Draw 2."
  Rows: KW: Reputation | WHEN always IF keyword_condition Reputation DO cost_change self (cost=-2) for while | WHEN played of self DO draw mine card in deck_top (amount=2)
- Lines the library draws between them: none

### Pair 2 (faeria, deck Structures)
- **Ulani, Defender of Oversky** (has "damage_reduction"). Text: "Gift - If Ulani is your only creature, this gains Taunt, Protection and Divine."
  Rows: WHEN played of self IF have all mine unit in board [card not Ulani, Defender of Oversky] not DO give_keyword self <Taunt> for permanent THEN give_keyword self <Protection> for permanent THEN give_keyword self <Divine> for permanent
- **Curious Biomancer** (has "draw"). Text: "Gift - For each enemy creature, draw a non-blue creature from your deck."
  Rows: WHEN played of self DO draw mine unit in deck [region not Blue] (amount=count of (all enemy unit in board))
- Lines the library draws between them: none

## D2: "damage" + "selection" (control, no link in the library; pairs from real decks)

### Pair 3 (gwent, deck Patricidal Fury: RnR Seagulls Sove Compass)
- **Hammond** (has "damage"). Text: "Deploy: Move an enemy unit to the other row and give it Bleeding (2). Increase the Bleeding duration by 1 for each adjacent Pirate."
  Rows: KW: Deploy | WHEN played of self DO move chosen enemy unit in board to enemy position [position not same_row] THEN give_keyword it enemy unit in board <Bleeding> (amount=sum (2 + count of (all unit in board [position is sides] [type is Pirate]))) for permanent
- **Maxii van Dekkar** (has "selection"). Text: "Deploy: Look at your deck in order from top to bottom. You may shuffle your deck, then move a card to the bottom of it."
  Rows: KW: Deploy | WHEN played of self DO look all mine card in deck THEN shuffle_into_deck all mine card in deck THEN move chosen mine card in deck in deck_bottom
- Lines the library draws between them: type: Maxii van Dekkar moves Hammond and your units, and Hammond acts on units next to it

### Pair 4 (gwent, deck Лавк Эрланд Shupe Erland)
- **Prince Anséis** (has "damage"). Text: "Formation. Order: Damage an enemy unit by 4. Inspired: Duel an enemy unit instead."
  Rows: KW: Formation, Order, Inspired | WHEN always DO give_keyword self <Formation> for permanent | WHEN activated of self IF keyword_condition Inspired not DO damage chosen enemy unit in board (amount=4) | WHEN activated of self IF keyword_condition Inspired DO keyword_action chosen enemy unit in board to self <Duel> for unstated
- **Cintrian Envoy** (has "selection"). Text: "Formation. Order: Look at 3 random cards from your deck. You may move 1 to the top of it. Cooldown: 2"
  Rows: KW: Formation, Order | WHEN always DO give_keyword self <Formation> for permanent | WHEN activated of self DO look 3 random mine card in deck THEN choose_card chosen mine card in deck THEN put_on_top it card | WHEN always DO keyword_action <Cooldown> (amount=2)
- Lines the library draws between them: none

## D3: "card_presence_condition" + "leave_trigger" (combo, no link in the library; pairs from real decks)

### Pair 5 (gwent, deck Falibeer (by Lerio))
- **Redanian Knight** (has "card_presence_condition"). Text: "Barricade (Ranged): At the end of your turn, boost self by 1. Exposed: Move self to the Melee row, then damage the highest-power enemy unit by 2. Grace 8: Boost adjacent units by 1."
  Rows: KW: Grace | WHEN turn_end by mine player IF keyword_condition Barricade; keyword_condition Ranged DO stat_change self (strength=1) for permanent | WHEN keyword_removed of self [keyword is Armor] DO move self to mine position [position is front_row] THEN damage highest enemy unit by strength in board (amount=2) | WHEN stat_changed of self IF keyword_condition Grace 8 DO stat_change all unit in board [position is sides] (strength=1) for permanent
- **Damsel in Distress** (has "leave_trigger"). Text: "Doomed. Scenario: Progress whenever you play a Knight. Prologue: Summon a bronze Knight from your deck to this row. Chapter 1: Whenever an allied unit triggers Grace, boost its adjacent units by 2. Chapter 2: Spawn and play Mad Charge."
  Rows: KW: Doomed | WHEN always DO give_keyword self <Doomed> for permanent | WHEN played of mine unit in board [type is Knight] DO stage_advance self | WHEN played of self DO summon chosen mine card in deck [state is bronze] [type is Knight] to chosen mine position [position is same_row] in board | WHEN keyword_used of mine unit in board [keyword is Grace] IF stage 1 DO stat_change all mine unit in board [position is sides] (strength=2) for permanent | WHEN played of mine unit in board [type is Knight] IF stage 2 DO create in hand <Mad Charge> THEN play_card chosen mine card in hand [card is Mad Charge] in hand
- Lines the library draws between them: stronger: gives it more strength; type: Damsel in Distress puts your units there, and Redanian Knight acts on units next to it; waits: is a Knight whose playing sets off its effect; waits: uses Grace

### Pair 6 (gwent, deck For Temeriaaaaa)
- **Prince Anséis** (has "card_presence_condition"). Text: "Formation. Order: Damage an enemy unit by 4. Inspired: Duel an enemy unit instead."
  Rows: KW: Formation, Order, Inspired | WHEN always DO give_keyword self <Formation> for permanent | WHEN activated of self IF keyword_condition Inspired not DO damage chosen enemy unit in board (amount=4) | WHEN activated of self IF keyword_condition Inspired DO keyword_action chosen enemy unit in board to self <Duel> for unstated
- **Siege** (has "leave_trigger"). Text: "Doomed. Scenario: Progress whenever you play a Siege Engine. Prologue: Spawn a reinforced Trebuchet on your Ranged row. Chapter 1: Spawn a Battering Ram on your Ranged row. Chapter 2: Spawn and play Bombardment."
  Rows: KW: Doomed | WHEN always DO give_keyword self <Doomed> for permanent | WHEN played of self DO summon to mine position [position is back_row] <Reinforced Trebuchet> | WHEN played of mine unit [type is Siege Engine] IF stage 1 DO summon to mine position [position is back_row] <Battering Ram> | WHEN played of mine unit [type is Siege Engine] IF stage 2 DO create mine card in hand <Bombardment> THEN play_card it card
- Lines the library draws between them: none

## D4: "free_play" + "leave_trigger" (blink, no link in the library; pairs from real decks)

### Pair 7 (gwent, deck Soldiers Солдаты 11.7)
- **Roderick of Dun Tynne** (has "free_play"). Text: "Disloyal. Deploy: Look at 2 random gold cards from your deck, then play 1 of them."
  Rows: KW: Disloyal, Deploy | WHEN always DO give_keyword self <Disloyal> for permanent | WHEN played of self DO look 2 random mine card in deck [state is gold] THEN choose_card chosen mine card in deck THEN play_card it card
- **Aerondight** (has "leave_trigger"). Text: "Echo. Damage an enemy unit by 0, then boost the lowest-power allied unit by the excess damage dealt. At the end of your turn, if you have more points than your opponent, increase the damage by 1, wherever this card is."
  Rows: KW: Echo | WHEN always DO give_keyword self <Echo> for permanent | WHEN played of self DO damage chosen enemy unit in board (amount=0) THEN stat_change lowest mine unit by strength in board (strength=excess) for permanent | WHEN turn_end by mine player IF score gt DO increase_effect self (amount=1)
- Lines the library draws between them: none

### Pair 8 (gwent, deck МЕГА ЛИСТИК 11.6)
- **Elven Seer** (has "free_play"). Text: "When you target this unit with a bronze special card, Spawn and play a copy of that special card. Counter: 1"
  Rows: KW: Counter | WHEN targeted by mine spell [state is bronze] of self DO copy actor spell in hand THEN play_card it | WHEN always DO give_keyword self <Counter> (amount=1) for permanent
- **Spring Equinox** (has "leave_trigger"). Text: "Doomed. Boost an allied unit by 0. Increase the boost by 1 for each Nature card other than Spring Equinox in your starting deck."
  Rows: KW: Doomed | WHEN always DO give_keyword self <Doomed> for permanent | WHEN played of self DO stat_change chosen mine unit in board (strength=count of (mine card [state is started_in_deck] [type is Nature] [card not Spring Equinox])) for permanent
- Lines the library draws between them: waits: targets it for its effect

## D5: "damage_reduction" + "heal" (defenders, no link in the library; pairs from real decks)

### Pair 9 (duelyst, deck Wanderer Brome (4LW))
- **Dauntless Advance** (has "damage_reduction"). Text: "Your General and nearby friendly minions gain, "Takes no damage this turn.""
  Rows: WHEN played of self DO give_ability mine player for this_round THEN give_ability all mine unit in board [position is surrounding] for this_round
- **Trinity Oath** (has "heal"). Text: "Draw 3 cards and restore 3 Health to your General."
  Rows: WHEN played of self DO draw mine card in deck_top (amount=3) THEN heal mine player (amount=3)
- Lines the library draws between them: none

### Pair 10 (duelyst, deck Lodestah Stunnah)
- **Lodestar** (has "damage_reduction"). Text: "Keywords: Airdrop, Forcefield. At the end of BOTH players' turns, pull some things to this minion."
  Rows: KW: Airdrop, Forcefield | WHEN turn_end DO move random any to self
- **Invigoration** (has "heal"). Text: "Intensify: Restore 3 Health to your General."
  Rows: WHEN played of self DO heal mine player (amount=product (3 + event_count of (played of mine card [card is Invigoration]) this_game))
- Lines the library draws between them: none

## D6: "resource_gain" + "spell_power" (ramp, no link in the library; pairs from real decks)

### Pair 11 (runeterra, deck Veigar Senna (2))
- **Otterpus** (has "resource_gain"). Text: "Keywords: Attune. When I'm summoned, create a Prank in hand."
  Rows: KW: Attune | WHEN summoned of self DO create in hand <Prank>
- **Veigar** (has "spell_power"). Text: "When I'm summoned, create a Darkness in hand if you don't have one. Round Start: Grant your Darkness everywhere 1 extra damage. Level up: You've dealt 12+ damage with Darkness."
  Rows: WHEN summoned of self IF have mine card in hand [card is Darkness] not DO create in hand <Darkness> | WHEN round_start DO increase_effect all mine card in everywhere [card is Darkness] (amount=1) for permanent | WHEN always IF event_count damaged by mine spell [card is Darkness] damage ge 12 this_game DO level_up self
- Lines the library draws between them: none

### Pair 12 (sts1, deck Defect Reprogram (highgroundgaming))
- **Sunder** (has "resource_gain"). Text: "Deal 24 damage. If this kills an enemy, gain 3 energy."
  Rows: WHEN played of self DO damage chosen enemy unit in board (amount=24) | WHEN killed by self of enemy unit DO mana_gain mine mana (amount=3)
- **Hyperbeam** (has "spell_power"). Text: "Deal 26 damage to ALL enemies. Lose 3 Focus."
  Rows: WHEN played of self DO damage all enemy unit in board (amount=26) THEN give_keyword mine player <Focus> (amount=-3) for permanent
- Lines the library draws between them: cheaper: pays for it: more mana or a lower cost

## D7: "friendly_fire" + "leave_trigger" (eggs, no link in the library; pairs from real decks)

### Pair 13 (gwent, deck BURZA PLS NERF THIS DECK! (5))
- **Dimun Warship** (has "friendly_fire"). Text: "Whenever you play a Pirate, damage self and a random enemy unit by 1. Deathwish: Summon the highest-power bronze Pirate from your graveyard to this row."
  Rows: KW: Deathwish | WHEN played of mine unit [type is Pirate] DO damage self (amount=1) THEN damage random enemy unit in board (amount=1) | WHEN dies of self DO revive highest mine unit by strength in discard [state is bronze] [type is Pirate] to mine position [position is same_row]
- **Marlene de Trastamara** (has "leave_trigger"). Text: "Doomed. Order: If not Doomed, gain Resilience."
  Rows: KW: Doomed, Order | WHEN always DO give_keyword self <Doomed> for permanent | WHEN activated of self IF have self [keyword is Doomed] not DO give_keyword self <Resilience> for permanent
- Lines the library draws between them: none

### Pair 14 (gwent, deck Улула Воины Ulula Warriors)
- **Kaer Trolde** (has "friendly_fire"). Text: "Resilience. Deploy: Create and play a bronze an Craite unit. Order: Give an allied unit 6 Armor, then it Clashes with an enemy unit."
  Rows: KW: Resilience, Order, Deploy | WHEN always DO give_keyword self <Resilience> for permanent | WHEN played of self DO create chosen mine unit in board [state is bronze] [name_has is Craite] in hand THEN play_card it card | WHEN activated of self DO give_keyword chosen mine unit in board <Armor> (amount=6) for permanent THEN keyword_action it to chosen enemy unit in board <Clash> for unstated
- **Morkvarg** (has "leave_trigger"). Text: "When this unit enters your graveyard during the round, Summon it to your Melee row and give it Doomed."
  Rows: WHEN dies of self DO summon self to mine position [position is front_row] THEN give_keyword self <Doomed> for permanent | WHEN dies of self DO summon self to mine position [position is front_row] THEN give_keyword it <Doomed> for permanent
- Lines the library draws between them: waits: kills it for its death effect

## D8: "recycle" + "variable_stats" (rosters, no link in the library; pairs from real decks)

### Pair 15 (gwent, deck SPAM/спам (гайд))
- **Dies Irae** (has "recycle"). Text: "Echo. Damage an enemy unit by 3 and boost all allied Firesworn units by 1. Deathblow: Boost all allied units instead."
  Rows: KW: Echo | WHEN always DO give_keyword self <Echo> for permanent | WHEN played of self DO damage chosen enemy unit in board (amount=3) THEN stat_change all mine unit in board [type is Firesworn] (strength=1) for permanent | WHEN killed by self DO stat_change all mine unit in board (strength=1) for permanent
- **Fallen Knight** (has "variable_stats"). Text: "Veil. Intimidate. Whenever you Spawn a unit on your side of the battlefield, boost self by 1 for each unit Spawned."
  Rows: KW: Veil, Intimidate | WHEN always DO give_keyword self <Veil> for permanent | WHEN always DO give_keyword self <Veil> for permanent | WHEN always DO give_keyword self <Intimidate> for permanent | WHEN always DO give_keyword self <Intimidate> for permanent | WHEN summoned of mine unit in board DO stat_change self (strength=event_amount) for permanent | WHEN created of mine unit DO stat_change self (strength=event_amount) for permanent
- Lines the library draws between them: none

### Pair 16 (gwent, deck Nekker Firesworn Накер Дети Огня)
- **Dies Irae** (has "recycle"). Text: "Echo. Damage an enemy unit by 3 and boost all allied Firesworn units by 1. Deathblow: Boost all allied units instead."
  Rows: KW: Echo | WHEN always DO give_keyword self <Echo> for permanent | WHEN played of self DO damage chosen enemy unit in board (amount=3) THEN stat_change all mine unit in board [type is Firesworn] (strength=1) for permanent | WHEN killed by self DO stat_change all mine unit in board (strength=1) for permanent
- **Whoreson Senior** (has "variable_stats"). Text: "Intimidate. Deploy: Transform an adjacent unit into a Cutup Lackey. Tribute 3: Transform adjacent units into Cutup Lackeys instead."
  Rows: KW: Intimidate, Deploy | WHEN always DO give_keyword self <Intimidate> for permanent | WHEN played of self DO transform chosen unit in board [position is sides] <Cutup Lackey> THEN spend_mana mine secondary_resource (amount=3) THEN transform all unit in board [position is sides] <Cutup Lackey>
- Lines the library draws between them: none

## D9: "damage_reduction" + "recycle" (turbo_fog, no link in the library; pairs from real decks)

### Pair 17 (gwent, deck РЫЦАРИ(гайд)/Knights)
- **The Maiden's Shield** (has "damage_reduction"). Text: "Shield. Grace 8: Spawn Bronwen the Bold to the right of self. Grace 14: Boost the allied Bronwen the Bold by 3. Deathwish: Lock the allied Bronwen the Bold."
  Rows: KW: Shield, Deathwish, Grace | WHEN always DO give_keyword self <Shield> for permanent | WHEN stat_changed of self IF keyword_condition Grace 8 DO summon to right_of_self mine position <Bronwen the Bold> | WHEN stat_changed of self IF keyword_condition Grace 14 DO stat_change chosen mine unit in board [card is Bronwen the Bold] (strength=3) for permanent | WHEN dies of self DO give_keyword chosen mine unit in board [card is Bronwen the Bold] <Lock> for permanent
- **Amphibious Assault** (has "recycle"). Text: "Echo. Play a non-Neutral unit from your deck with a provision cost of 9 or less. Boost it by 1 for each provision below the limit."
  Rows: KW: Echo | WHEN always DO give_keyword self <Echo> for permanent | WHEN played of self DO play_card chosen mine unit in deck [region not Neutral] [cost le 9] THEN stat_change it (strength=sum (9 + minus (stat cost of (it)))) for permanent
- Lines the library draws between them: none

### Pair 18 (gwent, deck Scottish Meta Perturber)
- **Geralt: Quen** (has "damage_reduction"). Text: "Shield. Deploy: Play a Witcher from your deck. Adrenaline 4: Also give it a Shield."
  Rows: KW: Shield, Deploy, Adrenaline | WHEN always DO give_keyword self <Shield> for permanent | WHEN played of self IF keyword_condition Adrenaline not 4 DO play_card chosen mine card in deck [type is Witcher] | WHEN played of self IF keyword_condition Adrenaline 4 DO play_card chosen mine card in deck [type is Witcher] THEN give_keyword it <Shield> for permanent
- **Delirium** (has "recycle"). Text: "Echo. Choose between a random bronze Skellige Beast and a random bronze Skellige Human that were not in your starting deck, then Spawn and play the one you chose, and Spawn the other in your graveyard. When Doomed, choose between gold ones instead"
  Rows: KW: Echo | WHEN always DO give_keyword self <Echo> for permanent | WHEN played of self IF have self [keyword is Doomed] not DO choose_one OR create random mine card [state is bronze] [region is Skellige] [type is Beast] [state not started_in_deck] in hand OR create random mine card [state is bronze] [region is Skellige] [type is Human] [state not started_in_deck] in hand THEN play_card it THEN create it mine card [state not started_in_deck] in discard | WHEN played of self IF have self [keyword is Doomed] DO choose_one OR create random mine card [state is gold] [region is Skellige] [type is Beast] [state not started_in_deck] in hand OR create random mine card [state is gold] [region is Skellige] [type is Human] [state not started_in_deck] in hand THEN play_card it THEN create it mine card [state not started_in_deck] in discard
- Lines the library draws between them: none

## D10: "disable" + "generate_cards" (control, no link in the library; pairs from real decks)

### Pair 19 (runeterra, deck Zoe Aphelios)
- **Arachnoid Sentry** (has "disable"). Text: "Play: Stun an enemy."
  Rows: WHEN played of self DO stun chosen enemy unit in board for this_round
- **Mountain Goat** (has "generate_cards"). Text: "Strike: Create a Gem in hand."
  Rows: WHEN strikes by self DO create in hand <Gem>
- Lines the library draws between them: none

### Pair 20 (runeterra, deck Katarina Leona)
- **Solari Sunhawk** (has "disable"). Text: "Daybreak: Stun the strongest enemy."
  Rows: KW: Daybreak | WHEN played of self IF keyword_condition Daybreak DO stun highest enemy unit by power in board for this_round
- **Katarina** (has "generate_cards"). Text: "Keywords: Quick Attack. When I'm summoned, create a Fleeting Blade's Edge in hand. Level up: I've struck once. When I level up, Recall me."
  Rows: KW: Quick Attack | WHEN summoned of self DO create in hand <Blade's Edge> THEN give_keyword it <Fleeting> for permanent | WHEN always IF event_count strikes by self ge 1 this_game DO level_up self | WHEN levels_up of self DO keyword_action self <Recall> for unstated
- Lines the library draws between them: none

## D11: "cost_reduction" + "disable" (hatebears, no link in the library; pairs from real decks)

### Pair 21 (runeterra, deck Karma Master Yi)
- **Deep Meditation** (has "cost_reduction"). Text: "Keywords: Flow. Flow: I cost 2 less. Draw 2 other spells."
  Rows: KW: Flow | WHEN always IF keyword_condition Flow DO cost_change self (cost=-2) for while | WHEN played of self DO draw 2 random mine card in deck [category is spell] [card not Deep Meditation] (amount=2)
- **Concussive Palm** (has "disable"). Text: "Stun an enemy to summon a Tail of the Dragon."
  Rows: WHEN played of self DO stun chosen enemy unit in board for this_round THEN summon in board <Tail of the Dragon>
- Lines the library draws between them: none

### Pair 22 (duelyst, deck APEX BIGMAR)
- **Flash Reincarnation** (has "cost_reduction"). Text: "If the next card you play this turn is a minion, it costs 2 less and takes 2 damage."
  Rows: WHEN played of self DO give_ability mine player for this_round
- **Saurian Finality** (has "disable"). Text: "Stun the enemy General. Your General gains +3 Attack. Both players lose 3 mana. Restore 10 Health to your General."
  Rows: WHEN played of self DO give_keyword enemy player <Stunned> for next_own_turn THEN stat_change mine player (power=3) for permanent THEN spend_mana mine mana (amount=3) THEN spend_mana enemy mana (amount=3) THEN heal mine player (amount=10)
- Lines the library draws between them: none

## D12: "heal" + "taunt" (defenders, no link in the library; pairs from real decks)

### Pair 23 (duelyst, deck Titan (Squee9))
- **Healing Mystic** (has "heal"). Text: "Opening Gambit: Restore 2 Health to anything."
  Rows: KW: Opening Gambit | WHEN played of self DO heal chosen any in board (amount=2)
- **Inquisitor Kron** (has "taunt"). Text: "Keywords: Provoke. Whenever you replace a card, summon a 2/2 Prisoner with a random ability nearby."
  Rows: KW: Provoke | WHEN shuffled by mine player of mine card in hand DO summon to chosen position [position is surrounding] <Dispirited Prisoner> (power=2, health=2) THEN give_random_keyword it for permanent
- Lines the library draws between them: none

### Pair 24 (duelyst, deck Wanderer Lilithe (Sibon))
- **Healing Mystic** (has "heal"). Text: "Opening Gambit: Restore 2 Health to anything."
  Rows: KW: Opening Gambit | WHEN played of self DO heal chosen any in board (amount=2)
- **Primus Shieldmaster** (has "taunt"). Text: "Keywords: Provoke."
  Rows: KW: Provoke
- Lines the library draws between them: none

## D13: "damage_reduction" + "taunt" (defenders, no link in the library; pairs from real decks)

### Pair 25 (gwent, deck Harmony Nekker Fauve 2560 fMMR)
- **Dwarven Skirmisher** (has "damage_reduction"). Text: "Deploy (Melee): Damage an enemy unit by 3. If it survived, gain 1 Armor. Order (Barricade): Damage an enemy unit by 3."
  Rows: WHEN played of self IF keyword_condition Melee DO damage chosen enemy unit in board (amount=3) THEN give_keyword self <Armor> (amount=1) for permanent | WHEN activated of self IF keyword_condition Barricade DO damage chosen enemy unit in board (amount=3)
- **Figgis Merluzzo** (has "taunt"). Text: "Defender. Order: Move self to the other row."
  Rows: KW: Defender, Order | WHEN always DO give_keyword self <Defender> for permanent | WHEN activated of self DO move self to mine position [position not same_row]
- Lines the library draws between them: none

### Pair 26 (faeria, deck jungwoo GBR)
- **Majinata, Spirit of Everlife** (has "damage_reduction"). Text: "Protection, Divine Gift - A friendly creature swallows Majinata. Give it +5/+5, Flying and Charge 2."
  Rows: KW: Protection, Divine | WHEN always DO give_keyword self <Protection> for permanent THEN give_keyword self <Divine> for permanent | WHEN played of self DO capture self to chosen mine unit in board <Swallow> THEN stat_change it (power=5, health=5) for permanent THEN give_keyword it <Flying> for permanent THEN give_keyword it <Charge> (amount=2) for permanent
- **Shifting Octopus** (has "taunt"). Text: "Choose one: Gain +2/+0 / Gain +0/+2 / Gain Jump / Gain Taunt, twice: - Gain +2/+0 - Gain +0/+2 - Gain Jump - Gain Taunt"
  Rows: WHEN played of self DO choose_one (options=4, times=2) OR stat_change self (power=2) for permanent OR stat_change self (health=2) for permanent OR give_keyword self <Jump> for permanent OR give_keyword self <Taunt> for permanent
- Lines the library draws between them: none

## D14: "cost_set" + "self_destruct" (reanimator, no link in the library; pairs from real decks)

### Pair 27 (faeria, deck Yellow Tempo)
- **Khalim, Sky Prodigy** (has "cost_set"). Text: "Flying, Charge 2 When Khalim attacks a god, add a Khalim's Follower to your hand. It costs 0 faeria."
  Rows: KW: Flying, Charge | WHEN always DO give_keyword self <Flying> for permanent THEN give_keyword self <Charge> (amount=2) for permanent | WHEN strikes_nexus by self DO create in hand <Khalim's Follower> THEN cost_set it (cost=0) for permanent
- **Wind Soldier** (has "self_destruct"). Text: "Haste, Charge 3 Wind Soldier dies at end of turn."
  Rows: KW: Haste, Charge | WHEN always DO give_keyword self <Haste> for permanent THEN give_keyword self <Charge> (amount=3) for permanent | WHEN turn_end by mine player DO kill self
- Lines the library draws between them: none

### Pair 28 (runeterra, deck BC IO deck)
- **Treasured Trash** (has "cost_set"). Text: "Fill your hand with random cards. They cost 0 and areFleeting. You can only play 3 more cards this round."
  Rows: WHEN played of self DO create random mine card in hand (amount=full) THEN cost_set all mine card in hand (cost=0) for permanent THEN give_keyword all mine card in hand <Fleeting> for permanent THEN cant mine player to mine player (event=played, times=3) for this_round
- **Twin Wind Technique** (has "self_destruct"). Text: "Pick a follower. Summon an exact Ephemeral copy of it. If it's an enemy, Stun it."
  Rows: WHEN played of self DO copy chosen unit in board [category is follower] in board THEN give_keyword it <Ephemeral> for permanent THEN stun it enemy unit for this_round
- Lines the library draws between them: none

## D15: "leave_trigger" + "recycle" (blink, no link in the library; pairs from real decks)

### Pair 29 (gwent, deck NEW(old)AMBUSH/АМБУШ)
- **Oneiromancy** (has "leave_trigger"). Text: "Echo. Play any card from your deck."
  Rows: KW: Echo | WHEN always DO give_keyword self <Echo> for permanent | WHEN played of self DO play_card chosen mine card in deck
- **Maxii van Dekkar** (has "recycle"). Text: "Deploy: Look at your deck in order from top to bottom. You may shuffle your deck, then move a card to the bottom of it."
  Rows: KW: Deploy | WHEN played of self DO look all mine card in deck THEN shuffle_into_deck all mine card in deck THEN move chosen mine card in deck in deck_bottom
- Lines the library draws between them: waits: plays it: its effect goes off

### Pair 30 (gwent, deck Patricidal Fury: RnR Seagulls Sove Compass)
- **Ragh Nar Roog** (has "leave_trigger"). Text: "Doomed. Scenario: Progress whenever you play a gold unit. Prologue: Spawn Cataclysm on both enemy rows for 2 turns. Chapter 1: Damage an enemy unit by 5. Chapter 2: Spawn and play Clear Skies."
  Rows: KW: Doomed | WHEN always DO give_keyword self <Doomed> for permanent | WHEN played of chosen mine unit [state is gold] DO stage_advance self | WHEN played of self DO give_keyword all enemy position <Cataclysm> (turns=2) for n_turns | WHEN played of chosen mine unit [state is gold] IF stage 1 DO damage chosen enemy unit in board (amount=5) | WHEN played of chosen mine unit [state is gold] IF stage 2 DO create in hand <Clear Skies> THEN play_card chosen mine card in hand [card is Clear Skies]
- **Maxii van Dekkar** (has "recycle"). Text: "Deploy: Look at your deck in order from top to bottom. You may shuffle your deck, then move a card to the bottom of it."
  Rows: KW: Deploy | WHEN played of self DO look all mine card in deck THEN shuffle_into_deck all mine card in deck THEN move chosen mine card in deck in deck_bottom
- Lines the library draws between them: none

## D16: "cost_reduction" + "spell_power" (ramp, no link in the library; pairs from real decks)

### Pair 31 (duelyst, deck Creep Wizard Cass)
- **Abjudicator** (has "cost_reduction"). Text: "Opening Gambit: Lower the cost of all spells in your action bar by 1."
  Rows: KW: Opening Gambit | WHEN played of self DO cost_change all mine card in hand [category is spell] (cost=-1) for permanent
- **Abyssal Tormentor** (has "spell_power"). Text: "Keywords: Provoke. Your Shadow Creep deals damage equal to the number of friendly Shadow Creep."
  Rows: KW: Provoke | WHEN always DO increase_effect all mine position [terrain is damage_space] (amount=count of (mine position [terrain is damage_space]))
- Lines the library draws between them: none

### Pair 32 (duelyst, deck Mantra (Fanggod))
- **Mana Vortex** (has "cost_reduction"). Text: "The next spell you cast this turn costs 1 less."
  Rows: WHEN played of self DO cost_change mine card in hand [category is spell] (cost=-1) for next_card
- **Crescent Spear** (has "spell_power"). Text: "Your General gains +1 Attack. Spells you cast that deal damage deal +1 damage."
  Rows: WHEN always DO stat_change mine player (power=1) for while THEN increase_effect mine spell [does in damage] (amount=1) for while
- Lines the library draws between them: none