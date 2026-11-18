# Probe input (made by script)

## D9: "deathtouch" + "death_count" (only real decks join them)

### Pair 28 (faeria, deck Sac (Seasonal Cup Seifer 2019))
- **Shaytan Assassin** (has "deathtouch"). Text: "Deathtouch Gift - You may sacrifice another creature to give this creature Protection."
  Rows: KW: Deathtouch | WHEN always DO give_keyword self <Deathtouch> for permanent | WHEN played of self DO sacrifice chosen mine unit in board [card not Shaytan Assassin] THEN give_keyword self <Protection> for permanent
- **Soul Eater** (has "death_count"). Text: "Flying, Charge 3 Gains +1/+1 for each friendly creature that has died this game (while in your deck or hand)."
  Rows: KW: Flying, Charge | WHEN always DO give_keyword self <Flying> for permanent THEN give_keyword self <Charge> (amount=3) for permanent | WHEN always DO stat_change self (power=event_count of (dies of mine unit) this_game, health=event_count of (dies of mine unit) this_game) for while
- Lines the library draws between them: type: makes your units die

### Pair 29 (faeria, deck GY sacrifice march 2017 Meta)
- **Death Walker** (has "deathtouch"). Text: "Deathtouch You must sacrifice another creature to summon this creature."
  Rows: KW: Deathtouch | WHEN always DO give_keyword self <Deathtouch> for permanent | WHEN played of self DO sacrifice chosen mine unit in board [card not Death Walker]
- **Soul Eater** (has "death_count"). Text: "Flying, Charge 3 Gains +1/+1 for each friendly creature that has died this game (while in your deck or hand)."
  Rows: KW: Flying, Charge | WHEN always DO give_keyword self <Flying> for permanent THEN give_keyword self <Charge> (amount=3) for permanent | WHEN always DO stat_change self (power=event_count of (dies of mine unit) this_game, health=event_count of (dies of mine unit) this_game) for while
- Lines the library draws between them: type: makes your units die

### Pair 30 (faeria, deck MC17 - Shamanic Dance Sac)
- **Shaytan Assassin** (has "deathtouch"). Text: "Deathtouch Gift - You may sacrifice another creature to give this creature Protection."
  Rows: KW: Deathtouch | WHEN always DO give_keyword self <Deathtouch> for permanent | WHEN played of self DO sacrifice chosen mine unit in board [card not Shaytan Assassin] THEN give_keyword self <Protection> for permanent
- **Swarming Carassius** (has "death_count"). Text: "Flying Can be summoned adjacent to friendly creatures. Gift - Summon a Swarming Carassius for each friendly one that died this game."
  Rows: KW: Flying | WHEN always DO give_keyword self <Flying> for permanent | WHEN always DO can self to position [position is bordering] (event=summoned) for while | WHEN played of self DO summon <Swarming Carassius> (amount=event_count of (dies of mine unit [card is Swarming Carassius]) this_game)
- Lines the library draws between them: none

## D10: "haste" + "attack_lock" (only real decks join them)

### Pair 31 (duelyst, deck One Lizard Army (Patreon))
- **Makantor Warbeast** (has "haste"). Text: "Keywords: Frenzy, Rush."
  Rows: KW: Frenzy, Rush
- **Vaath's Brutality** (has "attack_lock"). Text: "Stun an enemy minion. Give your General +1 Attack."
  Rows: WHEN played of self DO give_keyword chosen enemy unit in board <Stunned> for next_own_turn THEN stat_change mine player (power=1) for permanent
- Lines the library draws between them: none

### Pair 32 (duelyst, deck Self-Harm Vaath)
- **Elucidator** (has "haste"). Text: "Keywords: Rush. Opening Gambit: Deal 4 damage to your General."
  Rows: KW: Rush, Opening Gambit | WHEN played of self DO damage mine player (amount=4)
- **Vaath's Brutality** (has "attack_lock"). Text: "Stun an enemy minion. Give your General +1 Attack."
  Rows: WHEN played of self DO give_keyword chosen enemy unit in board <Stunned> for next_own_turn THEN stat_change mine player (power=1) for permanent
- Lines the library draws between them: none

### Pair 33 (duelyst, deck Midrange Vaath)
- **Makantor Warbeast** (has "haste"). Text: "Keywords: Frenzy, Rush."
  Rows: KW: Frenzy, Rush
- **Saurian Finality** (has "attack_lock"). Text: "Stun the enemy General. Your General gains +3 Attack. Both players lose 3 mana. Restore 10 Health to your General."
  Rows: WHEN played of self DO give_keyword enemy player <Stunned> for next_own_turn THEN stat_change mine player (power=3) for permanent THEN spend_mana mine mana (amount=3) THEN spend_mana enemy mana (amount=3) THEN heal mine player (amount=10)
- Lines the library draws between them: none

## D11: "attack_now" + "attack_lock" (only real decks join them)

### Pair 34 (duelyst, deck Wanderer Ragnora (SonOfMakuta))
- **Makantor Warbeast** (has "attack_now"). Text: "Keywords: Frenzy, Rush."
  Rows: KW: Frenzy, Rush
- **Saurian Finality** (has "attack_lock"). Text: "Stun the enemy General. Your General gains +3 Attack. Both players lose 3 mana. Restore 10 Health to your General."
  Rows: WHEN played of self DO give_keyword enemy player <Stunned> for next_own_turn THEN stat_change mine player (power=3) for permanent THEN spend_mana mine mana (amount=3) THEN spend_mana enemy mana (amount=3) THEN heal mine player (amount=10)
- Lines the library draws between them: none

### Pair 35 (duelyst, deck Wizard Vaath)
- **Homeostatic Rebuke** (has "attack_now"). Text: "ALL minions attack themselves."
  Rows: WHEN played of self DO strike all unit in board to it
- **Saurian Finality** (has "attack_lock"). Text: "Stun the enemy General. Your General gains +3 Attack. Both players lose 3 mana. Restore 10 Health to your General."
  Rows: WHEN played of self DO give_keyword enemy player <Stunned> for next_own_turn THEN stat_change mine player (power=3) for permanent THEN spend_mana mine mana (amount=3) THEN spend_mana enemy mana (amount=3) THEN heal mine player (amount=10)
- Lines the library draws between them: none

### Pair 36 (duelyst, deck Midrange Vaath)
- **Lavaslasher** (has "attack_now"). Text: "Opening Gambit: This minion fights a nearby enemy minion."
  Rows: KW: Opening Gambit | WHEN played of self DO start_attack self to chosen enemy unit in board [position is surrounding]
- **Saurian Finality** (has "attack_lock"). Text: "Stun the enemy General. Your General gains +3 Attack. Both players lose 3 mana. Restore 10 Health to your General."
  Rows: WHEN played of self DO give_keyword enemy player <Stunned> for next_own_turn THEN stat_change mine player (power=3) for permanent THEN spend_mana mine mana (amount=3) THEN spend_mana enemy mana (amount=3) THEN heal mine player (amount=10)
- Lines the library draws between them: none

## D12: "cost_reduction" + "cost_increase" (only real decks join them)

## D13: "multi_attack" + "lifesteal" (only real decks join them)

### Pair 37 (duelyst, deck Wanderer Lilithe (Niklaren))
- **Vorpal Reaver** (has "multi_attack"). Text: "Keywords: Celerity. Dying Wish: Summon six Wraithlings on random spaces."
  Rows: KW: Celerity, Dying Wish | WHEN dies of self DO summon to random position <Wraithling> (amount=6)
- **Desolator** (has "lifesteal"). Text: "Opening Gambit: Steal 2 Health from the enemy General. Dying Wish: Return Desolator to your action bar."
  Rows: KW: Dying Wish, Opening Gambit | WHEN played of self DO damage enemy player (amount=2) THEN heal mine player (amount=event_amount) | WHEN dies of self DO return_to_hand self
- Lines the library draws between them: none

## D14: "damage_reduction" + "forced_attack" (only real decks join them)

### Pair 38 (runeterra, deck Thresh Viego)
- **Spirit's Refuge** (has "damage_reduction"). Text: "Give an ally Barrier and Lifesteal this round."
  Rows: WHEN played of self DO give_keyword chosen mine unit in board <Barrier> for this_round THEN give_keyword it <Lifesteal> for this_round
- **Thresh** (has "forced_attack"). Text: "Keywords: Challenger. Level up: I've seen 6+ units die."
  Rows: KW: Challenger | WHEN always IF event_count dies of unit ge 6 this_game DO level_up self
- Lines the library draws between them: none

### Pair 39 (runeterra, deck Fiora Shen Jarvan IV)
- **Shen** (has "damage_reduction"). Text: "Keywords: Barrier, Support. Support: Give my supported ally Barrier this round. Level up: I've seen allies gain Barrier 5 times."
  Rows: KW: Barrier, Support | WHEN supports by self DO give_keyword right_of_self <Barrier> for this_round | WHEN always IF event_count given_keyword of mine unit [keyword is Barrier] ge 5 this_game DO level_up self
- **Fleetfeather Tracker** (has "forced_attack"). Text: "When you summon another ally, grant me Challenger."
  Rows: WHEN summoned by mine player of it mine unit [card not Fleetfeather Tracker] DO give_keyword self <Challenger> for permanent
- Lines the library draws between them: none

### Pair 40 (runeterra, deck Miss Fortune Quinn Sculptor)
- **Chain Vest** (has "damage_reduction"). Text: "Grant an ally Tough."
  Rows: WHEN played of self DO give_keyword chosen mine unit in board <Tough> for permanent
- **Fleetfeather Tracker** (has "forced_attack"). Text: "When you summon another ally, grant me Challenger."
  Rows: WHEN summoned by mine player of it mine unit [card not Fleetfeather Tracker] DO give_keyword self <Challenger> for permanent
- Lines the library draws between them: none

## D15: "strikes_with_defence" + "taunt" (only real decks join them)

### Pair 41 (faeria, deck [NO DLC] BG PewPew - The Big Boy Siege Engine Enchant)
- **Gabrian Enchantress** (has "strikes_with_defence"). Text: "Gift - Another creature's Attack becomes equal to its Life."
  Rows: WHEN played of self DO stat_set chosen unit in board [card not Gabrian Enchantress] (power=stat health of (it))
- **Shamanic Dance** (has "taunt"). Text: "Give a creature +0/+4 and Taunt."
  Rows: WHEN played of self DO stat_change chosen unit in board (health=4) for permanent THEN give_keyword it <Taunt> for permanent
- Lines the library draws between them: stronger: more health

### Pair 42 (faeria, deck [NO DLC] BG PewPew - The Big Boy Siege Engine Enchant)
- **Gabrian Enchantment** (has "strikes_with_defence"). Text: "A creature's Attack becomes equal to its Life. Draw a card."
  Rows: WHEN played of self DO stat_set chosen unit in board (power=stat health of (it)) THEN draw mine card in deck_top (amount=1)
- **Shamanic Dance** (has "taunt"). Text: "Give a creature +0/+4 and Taunt."
  Rows: WHEN played of self DO stat_change chosen unit in board (health=4) for permanent THEN give_keyword it <Taunt> for permanent
- Lines the library draws between them: stronger: more health

### Pair 43 (faeria, deck Time of Tarum)
- **Gabrian Enchantment** (has "strikes_with_defence"). Text: "A creature's Attack becomes equal to its Life. Draw a card."
  Rows: WHEN played of self DO stat_set chosen unit in board (power=stat health of (it)) THEN draw mine card in deck_top (amount=1)
- **Living Willow** (has "taunt"). Text: "Taunt"
  Rows: KW: Taunt | WHEN always DO give_keyword self <Taunt> for permanent
- Lines the library draws between them: none

## D16: "strikes_with_defence" + "forced_attack" (only real decks join them)

### Pair 44 (runeterra, deck Galio Elder Dragon Morgana)
- **Petricite Hound** (has "strikes_with_defence"). Text: "Keywords: Formidable."
  Rows: KW: Formidable
- **Mageseeker Inquisitor** (has "forced_attack"). Text: "Keywords: Challenger. When I'm summoned, Curse your opponent with Suppression."
  Rows: KW: Challenger | WHEN summoned of self DO give_keyword enemy player <Suppression Curse> for unstated
- Lines the library draws between them: none

### Pair 45 (runeterra, deck Galio Elder Dragon Morgana)
- **Galio** (has "strikes_with_defence"). Text: "Keywords: Formidable, SpellShield. When I'm summoned, grant other allies +0|+3. Level up: Round End: Your allies have 25+ total Health."
  Rows: KW: Formidable, SpellShield | WHEN summoned of self DO stat_change all mine unit in board [card not Galio] (health=3) for permanent | WHEN round_end IF stat all mine unit in board health ge 25 DO level_up self
- **Mageseeker Inquisitor** (has "forced_attack"). Text: "Keywords: Challenger. When I'm summoned, Curse your opponent with Suppression."
  Rows: KW: Challenger | WHEN summoned of self DO give_keyword enemy player <Suppression Curse> for unstated
- Lines the library draws between them: none

### Pair 46 (runeterra, deck Galio Elder Dragon Morgana)
- **Petricite Hound** (has "strikes_with_defence"). Text: "Keywords: Formidable."
  Rows: KW: Formidable
- **Enraged Firespitter** (has "forced_attack"). Text: "Keywords: Challenger. Play: Deal 2 to an enemy and 2 to the enemy Nexus."
  Rows: KW: Challenger | WHEN played of self DO damage chosen enemy unit in board (amount=2) THEN damage enemy player (amount=2)
- Lines the library draws between them: none

## D17: "forced_attack" + "regeneration" (only real decks join them)

### Pair 47 (runeterra, deck Jarvan IV Garen)
- **Jarvan IV** (has "forced_attack"). Text: "Keywords: Barrier. When you attack, pay my cost to summon me Challenging the strongest enemy. Level up: Allies have survived 3+ strikes from enemy blockers."
  Rows: KW: Barrier | WHEN attacks by mine player DO spend_mana mine mana (amount=stat cost of (self)) THEN summon self THEN challenge highest enemy unit by power in board to self | WHEN always IF event_count survives_damage by enemy unit [state is blocking] of mine unit ge 3 this_game DO level_up self
- **Garen** (has "regeneration"). Text: "Keywords: Regeneration. When I'm summoned, give other allies +1|+1 this round. Level up: I've struck twice."
  Rows: KW: Regeneration | WHEN summoned of self DO stat_change all mine unit in board [card not Garen] (power=1, health=1) for this_round | WHEN always IF event_count strikes by self ge 2 this_game DO level_up self
- Lines the library draws between them: none

### Pair 48 (runeterra, deck Garen Jarvan IV Galio)
- **Swiftwing Lancer** (has "forced_attack"). Text: "Keywords: Last Breath, Challenger. Last Breath: Create a random Elite in hand."
  Rows: KW: Last Breath, Challenger | WHEN dies of self DO create random mine unit [type is Elite] in hand
- **Garen** (has "regeneration"). Text: "Keywords: Regeneration. When I'm summoned, give other allies +1|+1 this round. Level up: I've struck twice."
  Rows: KW: Regeneration | WHEN summoned of self DO stat_change all mine unit in board [card not Garen] (power=1, health=1) for this_round | WHEN always IF event_count strikes by self ge 2 this_game DO level_up self
- Lines the library draws between them: none

### Pair 49 (runeterra, deck Trundle Braum)
- **Braum** (has "forced_attack"). Text: "Keywords: Challenger, Regeneration. The first time I survive damage, summon a Mighty Poro. Level up: I've survived 10+ total damage."
  Rows: KW: Challenger, Regeneration | WHEN survives_damage of self [once_per_game] DO summon in board <Mighty Poro> | WHEN always IF event_count survives_damage of self damage ge 10 this_game DO level_up self
- **Trundle** (has "regeneration"). Text: "Keywords: Regeneration. When I'm summoned, create an Ice Pillar in hand. Level up: I've seen you play Ice Pillar."
  Rows: KW: Regeneration | WHEN summoned of self DO create in hand <Ice Pillar> | WHEN always IF event_count played by mine player of card [card is Ice Pillar] ge 1 this_game DO level_up self
- Lines the library draws between them: none

## D18: "cost_type" + "generate_cards" (only real decks join them)

### Pair 50 (faeria, deck MapQuest)
- **Time of Legends** (has "cost_type"). Text: "Draw the top legend in your deck. If there are no legends to answer the call, add 1 random legend to your hand. It becomes wild land."
  Rows: WHEN played of self DO draw mine card in deck [rarity is legendary] (amount=1) THEN create random mine card in hand [rarity is legendary] in hand THEN give_keyword it <Wild> for permanent
- **Message in a Bottle** (has "generate_cards"). Text: "Shuffle 2 Treasure Maps into your deck and draw a card."
  Rows: WHEN played of self DO create in deck <Treasure Map> (amount=2) THEN draw mine card in deck_top (amount=1)
- Lines the library draws between them: none

### Pair 51 (faeria, deck Mono Green Events)
- **Seek Shelter** (has "cost_type"). Text: "Discover a creature with Taunt. It becomes wild land and gets +0/+3."
  Rows: WHEN played of self DO keyword_action mine unit in hand [keyword is Taunt] in hand <Discover> for unstated THEN give_keyword it <Wild> for permanent THEN stat_change it (health=3) for permanent
- **Ruunin's Presence** (has "generate_cards"). Text: "Add a random green creature to your hand. Give it +6/+6."
  Rows: WHEN played of self DO create random mine unit in hand [region is Green] in hand THEN stat_change it (power=6, health=6) for permanent
- Lines the library draws between them: none

### Pair 52 (faeria, deck 3 Wish Value Deck [Fun])
- **Magda, Queen of Meroval** (has "cost_type"). Text: "Your Legends cost 1 faeria less. Production - Add a random Legend to your hand. It becomes wild land."
  Rows: KW: Production | WHEN always DO cost_change all mine card in hand [rarity is legendary] (cost=-1) for while | WHEN turn_start by mine player DO create random mine card in hand [rarity is legendary] in hand THEN give_keyword it <Wild> for permanent
- **Bloomsprite** (has "generate_cards"). Text: "Last Words - Add a random green card to your hand. It costs 3 faeria less."
  Rows: WHEN dies of self DO create random mine card in hand [region is Green] in hand THEN cost_change it (cost=-3) for permanent
- Lines the library draws between them: none

## D19: "attack_lock" + "copy" (only real decks join them)

### Pair 53 (duelyst, deck Lodestah Stunnah)
- **Saurian Finality** (has "attack_lock"). Text: "Stun the enemy General. Your General gains +3 Attack. Both players lose 3 mana. Restore 10 Health to your General."
  Rows: WHEN played of self DO give_keyword enemy player <Stunned> for next_own_turn THEN stat_change mine player (power=3) for permanent THEN spend_mana mine mana (amount=3) THEN spend_mana enemy mana (amount=3) THEN heal mine player (amount=10)
- **Alcuin Loremaster** (has "copy"). Text: "Opening Gambit: Put a copy of the most recently cast spell into your action bar."
  Rows: KW: Opening Gambit | WHEN played of self DO copy top mine spell in discard in hand
- Lines the library draws between them: none

### Pair 54 (duelyst, deck Faie Blood Taura)
- **Icy** (has "attack_lock"). Text: "Opening Gambit: Stun a nearby enemy."
  Rows: KW: Opening Gambit | WHEN played of self DO give_keyword chosen enemy unit in board [position is surrounding] <Stunned> for next_own_turn
- **Alcuin Loremaster** (has "copy"). Text: "Opening Gambit: Put a copy of the most recently cast spell into your action bar."
  Rows: KW: Opening Gambit | WHEN played of self DO copy top mine spell in discard in hand
- Lines the library draws between them: none

### Pair 55 (duelyst, deck Ilena MKII)
- **Icy** (has "attack_lock"). Text: "Opening Gambit: Stun a nearby enemy."
  Rows: KW: Opening Gambit | WHEN played of self DO give_keyword chosen enemy unit in board [position is surrounding] <Stunned> for next_own_turn
- **Essence Sculpt** (has "copy"). Text: "Choose a Stunned minion. Put a copy of that card into your action bar."
  Rows: WHEN played of self DO copy chosen unit in board [state is stunned] in hand
- Lines the library draws between them: type: makes units get a keyword or status: Essence Sculpt copys them

## D20: "hand_disruption" + "sacrifice" (only real decks join them)

### Pair 56 (marvel_snap, deck Knull Death Bucky)
- **Yondu** (has "hand_disruption"). Text: "On Reveal: Banish the card that costs the least in your opponent's deck."
  Rows: KW: On Reveal | WHEN played of self DO obliterate lowest_cost enemy card in deck
- **Venom** (has "sacrifice"). Text: "On Reveal: Destroy your other cards here. Add their Power to this card."
  Rows: KW: On Reveal | WHEN played of self DO kill all mine unit in board [position is same_lane] [card not Venom] THEN stat_change self (power=stat power of (it)) for permanent
- Lines the library draws between them: none

### Pair 57 (gwent, deck Nekker Ruehin Накер Рюхин)
- **Matta Hu'uri** (has "hand_disruption"). Text: "Deploy (Ranged): If neither player has passed and your opponent's hand is not full, they draw the lowest-cost card, and you draw the highest-cost card."
  Rows: WHEN played of self IF keyword_condition Ranged; have player [state is passed] not; have enemy card in hand [state is full] not DO draw lowest_cost enemy card in deck THEN draw highest_cost mine card in deck
- **Giant Toad** (has "sacrifice"). Text: "Deploy: Consume an allied unit. When you play a Deathwish unit on your Ranged row, Summon self from your graveyard to the same row, Consume it and gain Doomed."
  Rows: KW: Deploy | WHEN played of self DO keyword_action chosen mine unit in board to self <Consume> for unstated | WHEN played of mine unit in board [keyword is Deathwish] [position is back_row] DO summon self to chosen mine position [position is same_row] in board <Giant Toad> THEN keyword_action it to self <Consume> for unstated THEN give_keyword self <Doomed> for permanent
- Lines the library draws between them: none

### Pair 58 (gwent, deck Rat Raid Board Fill Deck)
- **Matta Hu'uri** (has "hand_disruption"). Text: "Deploy (Ranged): If neither player has passed and your opponent's hand is not full, they draw the lowest-cost card, and you draw the highest-cost card."
  Rows: WHEN played of self IF keyword_condition Ranged; have player [state is passed] not; have enemy card in hand [state is full] not DO draw lowest_cost enemy card in deck THEN draw highest_cost mine card in deck
- **Barghest** (has "sacrifice"). Text: "Deploy: Consume an allied unit. Order (Dominance): Consume an allied unit."
  Rows: KW: Deploy | WHEN played of self DO keyword_action chosen mine unit in board <Consume> for unstated | WHEN activated of self IF keyword_condition Dominance DO keyword_action chosen mine unit in board <Consume> for unstated
- Lines the library draws between them: none