# Probe input (made by script)

## P1: "taunt" + "on_damaged" (pillowfort)

### Pair 1 (duelyst)
- **Wind Stopper** (has "taunt"). Text: "Ranged attackers must attack this minion first."
  Rows: KW: Ranged Provoke | WHEN always DO give_keyword self <Ranged Provoke> for permanent
- **Frostiva** (has "on_damaged"). Text: "Keywords: Forcefield. Whenever this minion attacks or is attacked, summon a 3/3 Vespyr Night Howler nearby."
  Rows: KW: Forcefield | WHEN attacks by self DO summon to chosen position [position is surrounding] <Night Howler> (power=3, health=3) | WHEN attacks of self DO summon to chosen position [position is surrounding] <Night Howler> (power=3, health=3)
- Lines the library draws between them: none

### Pair 2 (duelyst)
- **Treant** (has "taunt"). Text: "Keywords: Provoke."
  Rows: KW: Provoke
- **Horn of the Forsaken** (has "on_damaged"). Text: "Whenever your General deals damage, summon a 1/1 Wraithling nearby your General."
  Rows: WHEN damaged by mine player DO summon to position [position is surrounding] <Wraithling> (power=1, health=1)
- Lines the library draws between them: none

### Pair 3 (faeria)
- **Shamanic Dance** (has "taunt"). Text: "Give a creature +0/+4 and Taunt."
  Rows: WHEN played of self DO stat_change chosen unit in board (health=4) for permanent THEN give_keyword it <Taunt> for permanent
- **King's Faithful** (has "on_damaged"). Text: "Protection"
  Rows: KW: Protection | WHEN always DO give_keyword self <Protection> for permanent
- Lines the library draws between them: none

### Pair 4 (faeria)
- **Shifting Octopus** (has "taunt"). Text: "Choose one: Gain +2/+0 / Gain +0/+2 / Gain Jump / Gain Taunt, twice: - Gain +2/+0 - Gain +0/+2 - Gain Jump - Gain Taunt"
  Rows: WHEN played of self DO choose_one (options=4, times=2) OR stat_change self (power=2) for permanent OR stat_change self (health=2) for permanent OR give_keyword self <Jump> for permanent OR give_keyword self <Taunt> for permanent
- **Possessed Ursus** (has "on_damaged"). Text: "After this creature is dealt damage, double its Attack."
  Rows: WHEN damaged of self DO stat_set self (power=double (stat power of (self)))
- Lines the library draws between them: none

### Pair 5 (gwent)
- **Cave Troll** (has "taunt"). Text: "Defender."
  Rows: KW: Defender | WHEN always DO give_keyword self <Defender> for permanent
- **Kelpie** (has "on_damaged"). Text: "Deploy: Spawn Rain on an enemy row for 0 turns. This value is increased by 1 for every 3 Beasts in your starting deck. Whenever an enemy unit takes damage from Rain or Storm, boost a random unboosted allied Beast by 1."
  Rows: KW: Deploy | WHEN played of self DO give_keyword chosen enemy position <Rain> (turns=sum (0 + divided (count of (all mine unit in everywhere [type is Beast] [state is started_in_deck])) (3))) for n_turns | WHEN damaged by chosen position [keyword in Rain] [keyword in Storm] of enemy unit in board DO stat_change random mine unit in board [type is Beast] [boost eq 0] (strength=1) for permanent
- Lines the library draws between them: none

### Pair 6 (gwent)
- **Ffion var Gaernel** (has "taunt"). Text: "Defender. Deploy: Spawn and play Battle Preparation."
  Rows: KW: Defender, Deploy | WHEN always DO give_keyword self <Defender> for permanent | WHEN played of self DO create mine card in hand <Battle Preparation> THEN play_card it card
- **Hefty Helge** (has "on_damaged"). Text: "Shield. Order: Damage a unit by 2. Charge: 1 Whenever you play a Tactic, gain 1 Charge."
  Rows: KW: Shield, Charge, Order | WHEN always DO give_keyword self <Shield> for permanent | WHEN activated of self DO damage chosen unit in board (amount=2) | WHEN always DO give_keyword self <Charge> (amount=1) for permanent | WHEN played of mine card [type is Tactic] DO give_keyword self <Charge> (amount=1) for permanent
- Lines the library draws between them: none

## P2: "forced_attack" + "on_damaged" (pillowfort)

### Pair 7 (runeterra)
- **Confront** (has "forced_attack"). Text: "Grant an ally Challenger. If it's a Dragon, draw 1."
  Rows: WHEN played of self DO give_keyword chosen mine unit in board <Challenger> for permanent | WHEN played of self IF it_matches [type is Dragon] DO draw mine card in deck_top (amount=1)
- **Legion Veteran** (has "on_damaged"). Text: "When another ally survives damage, grant it +1|+0."
  Rows: WHEN survives_damage of mine unit [card not Legion Veteran] DO stat_change it (power=1) for permanent
- Lines the library draws between them: none

### Pair 8 (runeterra)
- **Diana (level 2)** (has "forced_attack"). Text: "Keywords: Quick Attack. Nightfall or when you activate another Nightfall: Give me +2|+0 and Challenger this round."
  Rows: KW: Quick Attack | WHEN always IF keyword_condition Nightfall DO stat_change self (power=2) for this_round THEN give_keyword self <Challenger> for this_round | WHEN keyword_used by mine player of [keyword is Nightfall] DO stat_change self (power=2) for this_round THEN give_keyword self <Challenger> for this_round
- **Gwen** (has "on_damaged"). Text: "Keywords: Hallowed, Quick Attack. Attack: When another ally gains Power from Hallowed, so do I. Drain 2 from the enemy Nexus. Level up: I've dealt 10+ damage."
  Rows: KW: Hallowed, Quick Attack, Attack | WHEN attacks by self DO keyword_action enemy player <Drain> (amount=2) for unstated | WHEN stat_changed of mine unit [card not Gwen] IF keyword_condition Hallowed DO stat_change self (power=event_amount) for while | WHEN always IF event_count damaged by self damage ge 10 this_game DO level_up self
- Lines the library draws between them: none

### Pair 9 (runeterra)
- **The Serpent** (has "forced_attack"). Text: "Keywords: Challenger."
  Rows: KW: Challenger
- **Towering Stonehorn** (has "on_damaged"). Text: "I don't take damage from enemy spells or Skills."
  Rows: WHEN damaged by enemy spell [category in spell] [category in skill] of self DO negate_damage self
- Lines the library draws between them: none

## P3: "taunt" + "deathtouch" (pillowfort)

### Pair 10 (faeria)
- **Shimmering Statue** (has "taunt"). Text: "Taunt Production - Gain 1 Life."
  Rows: KW: Taunt, Production | WHEN always DO give_keyword self <Taunt> for permanent | WHEN turn_start by mine player DO heal mine player (amount=1)
- **Lion Fish** (has "deathtouch"). Text: "Flying, Deathtouch"
  Rows: KW: Flying, Deathtouch | WHEN always DO give_keyword self <Flying> for permanent THEN give_keyword self <Deathtouch> for permanent
- Lines the library draws between them: none

### Pair 11 (faeria)
- **Shamanic Dance** (has "taunt"). Text: "Give a creature +0/+4 and Taunt."
  Rows: WHEN played of self DO stat_change chosen unit in board (health=4) for permanent THEN give_keyword it <Taunt> for permanent
- **Death Walker** (has "deathtouch"). Text: "Deathtouch You must sacrifice another creature to summon this creature."
  Rows: KW: Deathtouch | WHEN always DO give_keyword self <Deathtouch> for permanent | WHEN played of self DO sacrifice chosen mine unit in board [card not Death Walker]
- Lines the library draws between them: none

## P4: "rule_change" + "immunity" (prison)

### Pair 12 (gwent)
- **Usurper: Officer** (has "rule_change"). Text: "Deploy: Spawn an Operative on an enemy row and give it Spying. Zeal. Order: Seize all Spying Operatives. At the start of the round, while in hand or deck, evolve."
  Rows: KW: Zeal, Order, Deploy | WHEN played of self DO summon to chosen enemy position <Operative> THEN give_keyword it <Spying> for permanent | WHEN always DO give_keyword self <Zeal> for permanent | WHEN activated of self DO keyword_action all unit in board [keyword is Spying] [card is Operative] <Seize> for unstated | WHEN round_start IF have self in hand DO transform self | WHEN round_start IF have self in deck DO transform self
- **Sove** (has "immunity"). Text: "Deploy (Melee): Summon a Beast from your deck to the opposite row and Infuse it with "Deathwish: Boost the enemy Sove twice by own base power", then damage it by 1 for each damaged enemy unit and gain Immunity."
  Rows: WHEN played of self IF keyword_condition Melee DO summon chosen mine card in deck [type is Beast] to position [position is opposite_row] THEN give_ability it <Infused> THEN damage it (amount=count of (all enemy unit in board [state is damaged])) THEN give_keyword self <Immunity> for permanent
- Lines the library draws between them: none

### Pair 13 (gwent)
- **Cintrian Artificer** (has "rule_change"). Text: "Formation. Order: Give an allied unit a Shield."
  Rows: KW: Formation, Order | WHEN always DO give_keyword self <Formation> for permanent | WHEN activated of self DO give_keyword chosen mine unit in board <Shield> for permanent
- **Stolen Mutagens** (has "immunity"). Text: "Choose a mutagen: Red - Damage an enemy unit by 4. Blue - Poison an allied unit and gain 5 Coins. Green - Boost an allied unit by 4 and give it Veil. If you control at least 2 Salamandra units, also choose an additional mutagen."
  Rows: WHEN played of self DO choose_one OR damage chosen enemy unit in board (amount=4) OR give_keyword chosen mine unit in board <Poison> for permanent THEN mana_gain mine secondary_resource (amount=5) OR stat_change chosen mine unit in board (strength=4) for permanent THEN give_keyword it <Veil> for permanent | WHEN played of self IF count all mine unit in board [type is Salamandra] ge 2 DO choose_one OR damage chosen enemy unit in board (amount=4) OR give_keyword chosen mine unit in board <Poison> for permanent THEN mana_gain mine secondary_resource (amount=5) OR stat_change chosen mine unit in board (strength=4) for permanent THEN give_keyword it <Veil> for permanent
- Lines the library draws between them: none

### Pair 14 (into_the_breach)
- **Prospero** (has "rule_change"). Text: "Pilot ability: Flying: Mech gains Flying (1 power required)"
  Rows: KW: Flying | WHEN always DO give_keyword self <Flying> for permanent
- **Area Shift** (has "immunity"). Text: "Push self and all adjacent tiles. Power: Free. Upgrades: Shield Self (1 Reactor Core): Shield the user when activated; Shield Ally (2 Reactor Cores): Shield any Ally units affected by this skill."
  Rows: WHEN attacks by self DO move self to position [position is bordering] THEN move all unit_or_structure [position is bordering] to position [position is bordering] | WHEN attacks by self IF upgraded 1 DO give_keyword self <Energy Shield> for permanent | WHEN attacks by self IF upgraded 2 DO give_keyword all mine unit_or_structure [position is bordering] <Energy Shield> for permanent
- Lines the library draws between them: none

### Pair 15 (into_the_breach)
- **Control Mech** (has "rule_change"). Text: "Keywords: Flying. Health 2, move 4. Weapon: Control Shot: Temporarily control a unit, moving it a short distance (2 tiles). Power: Free. Upgrades: +1 Move (1 Reactor Core): Targeted unit can move one extra tile; +1 Move (2 Reactor Cores): Targeted unit can move one extra tile."
  Rows: KW: Flying
- **Camila Vera** (has "immunity"). Text: "Pilot ability: Evasion: Mech unaffected by Webbing and Smoke."
  Rows: WHEN always DO cant self <Webbed> (event=given_keyword) for while THEN cant self <Smoke> (event=given_keyword) for while
- Lines the library draws between them: none

### Pair 16 (faeria)
- **Manta Rider** (has "rule_change"). Text: "Flying Last Words - Summon a 2/2 Manta with Flying and Charge 2 where this died."
  Rows: KW: Flying | WHEN always DO give_keyword self <Flying> for permanent | WHEN dies of self DO summon to position [position is same_space] <Manta> (power=2, health=2) THEN give_keyword it <Flying> for permanent THEN give_keyword it <Charge> (amount=2) for permanent
- **Divine Guardian** (has "immunity"). Text: "Divine When you would take lethal damage, prevent it and destroy this instead."
  Rows: KW: Divine | WHEN always DO give_keyword self <Divine> for permanent | WHEN damaged of mine player IF amount event_amount ge stat health of (mine player) DO negate_damage mine player THEN kill self
- Lines the library draws between them: none

### Pair 17 (faeria)
- **Oradrim Fanatic** (has "rule_change"). Text: "Jump Gift - You may move a friendly creature."
  Rows: KW: Jump | WHEN always DO give_keyword self <Jump> for permanent | WHEN played of self DO move chosen mine unit in board
- **Kaios, Demented Overmind** (has "immunity"). Text: "Divine Kaios' Attack is always equal to his Life. Corrupt - Drain 1 life from EVERYTHING."
  Rows: KW: Divine, Corrupt | WHEN always DO give_keyword self <Divine> for permanent | WHEN always DO stat_set self (power=stat health of (self)) | WHEN moves_onto of self [position is same_space] [once_per_game] DO damage all anything (amount=1) THEN heal mine player (amount=event_amount)
- Lines the library draws between them: moves: moves it where it must be; moves: moves my units or land forward: they reach enemy ground; waits: moves it for its effect

## P5: "row_effects" + "immunity" (prison)

### Pair 18 (gwent)
- **Dragon's Dream** (has "row_effects"). Text: "Spawn Dragon's Dream on an enemy row for 3 turns."
  Rows: WHEN played of self DO give_keyword chosen enemy position <Dragon's Dream> (turns=3) for n_turns
- **Traveling Priestess** (has "immunity"). Text: "Veil. Deploy: Gain 1 Charges. Whenever this unit is moved back into your deck, increase the number of Charges by 2. Order: Boost an allied unit by 1. Whenever this unit is Inspired, gain Zeal. Charge: 0"
  Rows: KW: Veil, Charge, Order, Deploy | WHEN always DO give_keyword self <Veil> for permanent | WHEN played of self DO give_keyword self <Charge> (amount=1) for permanent | WHEN shuffled of self DO give_keyword self <Charge> (amount=2) for permanent | WHEN activated of self DO stat_change chosen mine unit in board (strength=1) for permanent | WHEN stat_changed of self IF keyword_condition Inspired DO give_keyword self <Zeal> for permanent | WHEN always DO give_keyword self <Charge> (amount=0) for permanent
- Lines the library draws between them: none

### Pair 19 (gwent)
- **Little Havfrue** (has "row_effects"). Text: "Deploy (Bonded): Increase this unit's base power by 2. Order: Damage self by 4 and Spawn Rain on an enemy row for 2 turns."
  Rows: KW: Order | WHEN played of self IF keyword_condition Bonded DO base_change self (strength=2) | WHEN activated of self DO damage self (amount=4) THEN give_keyword chosen enemy position <Rain> (turns=2) for n_turns
- **Ancient Foglet** (has "immunity"). Text: "Veil. Deploy: Boost self by the total duration of row effects on the opposite side. Whenever you apply a row effect, boost self by its duration."
  Rows: KW: Veil, Deploy | WHEN always DO give_keyword self <Veil> for permanent | WHEN played of self DO stat_change self (strength=sum keyword_amount of (all enemy position in board [keyword in Frost] [keyword in Fog] [keyword in Rain] [keyword in Storm] [keyword in Cataclysm] [keyword in Dragon's Dream] [keyword in Blood Moon])) for permanent | WHEN given_keyword by mine player of position [keyword in Frost] [keyword in Fog] [keyword in Rain] [keyword in Storm] [keyword in Cataclysm] [keyword in Dragon's Dream] [keyword in Blood Moon] DO stat_change self (strength=stat keyword_amount of (it position)) for permanent
- Lines the library draws between them: none

## P6: "rule_change" + "stealth" (prison)

### Pair 20 (runeterra)
- **Restored Sun Disc** (has "rule_change"). Text: "Keywords: Landmark. Immediately draw 1 of each of your Ascended allies. For the rest of the game, your level 2 Ascended allies are level 3."
  Rows: KW: Landmark | WHEN played of self DO draw mine card in deck [type is Ascended] (amount=distinct card of (mine card in deck [type is Ascended])) | WHEN always DO can mine unit [type is Ascended] for while
- **Pakaa Cub** (has "stealth"). Text: "Keywords: Fearsome. Ambush 1 Nexus Strike: Summon a Pakaa Protector."
  Rows: KW: Fearsome | WHEN always DO keyword_action <Ambush> (amount=1) | WHEN strikes_nexus by self DO summon <Pakaa Protector>
- Lines the library draws between them: none

### Pair 21 (runeterra)
- **Sejuani** (has "rule_change"). Text: "Keywords: Overwhelm. Play: Give an enemy Frostbite and Vulnerable this round. Level up: You've damaged the enemy Nexus in 5+ different rounds."
  Rows: KW: Overwhelm | WHEN played of self DO keyword_action chosen enemy unit in board <Frostbite> for unstated THEN give_keyword it enemy unit in board <Vulnerable> for this_round | WHEN always IF event_count nexus_damaged of enemy player ge 5 different_rounds DO level_up self
- **Towering Pairofant** (has "stealth"). Text: "Keywords: Overwhelm. Ambush 5"
  Rows: KW: Overwhelm | WHEN always DO keyword_action <Ambush> (amount=5)
- Lines the library draws between them: levels: damages the enemy player (levels it up)

## P7: "hand_disruption" + "hand_size" (discard_8rack)

### Pair 22 (duelyst)
- **Joseki** (has "hand_disruption"). Text: "Each player steals a random card from their opponent's deck."
  Rows: WHEN played of self DO steal random enemy card in deck THEN donate random mine card in deck
- **Dark Seed** (has "hand_size"). Text: "Deal 1 damage to the enemy General for each card in the opponent's action bar."
  Rows: WHEN played of self DO damage enemy player (amount=count of (all enemy card in hand))
- Lines the library draws between them: none

### Pair 23 (duelyst)
- **Scroll Bandit** (has "hand_disruption"). Text: "Backstab: (1). Whenever this backstabs, steal a spell from your opponent's deck."
  Rows: KW: Backstab | WHEN always DO give_keyword self <Backstab> (amount=1) for permanent | WHEN strikes by self IF keyword_condition Backstab DO steal random enemy spell in deck
- **Upper Hand** (has "hand_size"). Text: "Deal 1 damage to an enemy minion for each card in your opponent's action bar."
  Rows: WHEN played of self DO damage chosen enemy unit in board (amount=count of (all enemy card in hand))
- Lines the library draws between them: none

### Pair 24 (runeterra)
- **Watery Grave** (has "hand_disruption"). Text: "Obliterate 6 cards from the bottom of the enemy deck."
  Rows: WHEN played of self DO obliterate 6 bottom enemy card in deck_bottom
- **Trundle (level 2)** (has "hand_size"). Text: "Keywords: Overwhelm, Regeneration. When I'm summoned, create an Ice Pillar in hand. Attack: Grant me +1|+0 for each 8+ cost card you Behold."
  Rows: KW: Overwhelm, Regeneration, Attack | WHEN summoned of self DO create in hand <Ice Pillar> | WHEN attacks by self IF keyword_condition Behold mine card in hand [cost ge 8] DO stat_change self (power=count of (mine card in hand [cost ge 8])) for permanent
- Lines the library draws between them: none

### Pair 25 (runeterra)
- **Maokai (level 2)** (has "hand_disruption"). Text: "Keywords: Regeneration. When I level up, Obliterate the enemy deck, leaving 4 non-champions. Round Start: Summon a Sapling."
  Rows: KW: Regeneration | WHEN levels_up of self DO obliterate all enemy card in deck (except=4) | WHEN round_start DO summon mine unit in board <Sapling>
- **Jinx** (has "hand_size"). Text: "Keywords: Quick Attack. Level up: I see your hand is empty."
  Rows: KW: Quick Attack | WHEN always IF count all mine card in hand eq 0 now DO level_up self
- Lines the library draws between them: none

## P8: "extra_turn" + "recycle" (extra_turns)

### Pair 26 (runeterra)
- **Tianna Crownguard** (has "extra_turn"). Text: "Keywords: Tough. When I'm summoned, Rally."
  Rows: KW: Tough | WHEN summoned of self DO gain_attack_token mine player
- **Call the Wild** (has "recycle"). Text: "For the top 4 cards in your deck, draw each Yeti, Poro, and Elnuk. Then place the rest into your deck."
  Rows: WHEN played of self DO look 4 mine card in deck_top THEN draw all mine card in deck_top [type in Yeti] [type in Poro] [type in Elnuk] THEN shuffle_into_deck all mine card in deck_top
- Lines the library draws between them: none

### Pair 27 (runeterra)
- **Yordle Ranger** (has "extra_turn"). Text: "Keywords: Scout. Attack: Grant allies with equal or less power than me +0|+1."
  Rows: KW: Scout, Attack | WHEN attacks by self DO stat_change all mine unit in board [power le stat power of (self)] (health=1) for permanent
- **Station Archivist** (has "recycle"). Text: "Play: Pick a spell in the top 5 cards of your deck and create an exact Fleeting copy in hand, then place those top 5 cards into your deck"
  Rows: WHEN played of self DO copy 5 chosen mine spell in deck_top in hand THEN give_keyword it <Fleeting> for permanent THEN shuffle_into_deck 5 all mine card in deck_top
- Lines the library draws between them: none
