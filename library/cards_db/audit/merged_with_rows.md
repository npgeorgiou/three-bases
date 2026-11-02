# Merged causes (old check) - 16 files: f1-f4 (Faeria), r1-r7 (Runeterra), s1-s2 (Slay the Spire), u1-u3 (Duelyst)
Format per cause: wrong thinking | rule broken | games | files | examples.
File reference "f1 c4" = cause 4 in causes_f1.md.

## A. Movement and reach

1. Wrong thinking: a card's own move keyword (Flying, Jump, Dash, Charge, Aquatic) moves my other units forward, so the other card reaches enemy ground / enemy well.
   Rule: L20, L2 (also L7 for Luduan "this harvests"). Games: Faeria. Files: f1 c1, f2 c1, f3 c1, f4 c8 (duplicates).
   - Ghost Dragon -> Lost Explorer: moves: moves my units or land forward: they reach enemy ground
        [faeria] line now: moves: moves my units or land forward: they reach enemy ground
        Ghost Dragon: KW: Flying, Charge, Protection | WHEN always DO give_keyword self <Flying> for permanent THEN give_keyword self <Charge> (amount=2) for permanent THEN give_keyword self <Protection> for permanent
        Lost Explorer: KW: Corrupt | WHEN moves_onto of self [position is same_space] [once_per_game] DO draw mine card in deck_top (amount=1) THEN mana_gain mine player (amount=1)
   - Windborne Emissary -> Luduan: moves: moves my units or land forward: they reach enemy ground
        [faeria] line now: moves: moves my units or land forward: they reach enemy ground
        Windborne Emissary: KW: Flying | WHEN always DO give_keyword self <Flying> for permanent | WHEN always IF have all mine unit in board [keyword is Flying] [card not Windborne Emissary] is DO stat_change self (power=2) for while
        Luduan: WHEN harvests by self of enemy position [terrain is resource_well] DO create random mine card in hand [region is Blue] in hand THEN cost_change it (cost=-2) for permanent
   - Airbot -> Imperial Trooper: moves into place: moves my units or land forward: they reach enemy ground
        [faeria] line now: moves: moves my units or land forward: they reach enemy ground
        Airbot: KW: Flying, Dash | WHEN always DO give_keyword self <Flying> for permanent THEN give_keyword self <Dash> (amount=2) for permanent
        Imperial Trooper: KW: Corrupt | WHEN moves_onto of self [position is same_space] [once_per_game] DO steal position [terrain is land] [position is same_space]
        case nfa04: expect none moves it (Claude, deck read: Airbot's own Dash moves Airbot, not the Trooper (its forward position h)

2. Wrong thinking: a card that moves nothing (land maker, land destroyer, turns land to lake, reactivates, moves only itself) is read as a mover.
   Rule: L1 (f1 also L20, L2). Games: Faeria, Duelyst. Files: f1 c1, f2 c3, f3 c1, u3 c9.
   - Wood Elemental -> Wavecrash Colossus: moves: moves my units or land forward: they reach enemy ground
        [faeria] line now: moves: moves my units or land forward: they reach enemy ground
        Wood Elemental: KW: Taunt | WHEN always DO give_keyword self <Taunt> for permanent | WHEN played of self DO set_terrain chosen position [terrain is ocean] to position [terrain is forest]
        Wavecrash Colossus: WHEN always DO cost_change self (cost=minus (event_count of (harvests by mine unit of enemy position [terrain is resource_well]) this_game), min=4) for while
   - Meteor -> Luduan: moves: moves my units or land forward: they reach enemy ground
        [faeria] line now: moves: moves my units or land forward: they reach enemy ground
        Meteor: WHEN played of self DO kill all unit_or_structure [position in same_space] [position in bordering] THEN set_terrain all position [terrain is land] [position in same_space] [position in bordering] to position [terrain is ocean]
        Luduan: WHEN harvests by self of enemy position [terrain is resource_well] DO create random mine card in hand [region is Blue] in hand THEN cost_change it (cost=-2) for permanent
   - Spirit of the Wild -> Avalanche: enables: Spirit of the Wild moves units, and Avalanche acts on units base's starting side or on your leader
        [duelyst] line now: type: Spirit of the Wild moves units, and Avalanche acts on units base's starting side or on your leader
        Spirit of the Wild: WHEN played of self DO ready all mine unit in board [position is starting_side]
        Avalanche: WHEN played of self DO damage all any in board [position is starting_side] (amount=4) THEN give_keyword it <Stunned> for next_own_turn

3. Wrong thinking: any teleport triggers Corrupt / reaches enemy ground, even a teleport to my own land.
   Rule: L1. Games: Faeria. Files: f2 c4.
   - Desert Twister -> Baldurion, Evil Archsmith: waits: moves it for its effect
        [faeria] line now: waits: moves it for its effect; moves: moves my units or land forward: they reach enemy ground; moves: moves it where it must be
        Desert Twister: WHEN played of self DO move chosen unit in board to chosen mine position [terrain is desert] <Teleport>
        Baldurion, Evil Archsmith: KW: Protection, Corrupt | WHEN always DO give_keyword self <Protection> for permanent | WHEN moves_onto of self [position is same_space] [once_per_game] DO create in hand <Hammer of Destruction>
   - Sagami Grovecaller -> Monstrous Hydra: waits: moves it for its effect
        [faeria] line now: waits: moves it for its effect; moves: moves my units or land forward: they reach enemy ground; moves: moves it where it must be
        Sagami Grovecaller: WHEN played of self DO move chosen mine unit in board [card not Sagami Grovecaller] to chosen mine position [terrain is forest] <Teleport>
        Monstrous Hydra: KW: Corrupt | WHEN moves_onto of self [position is same_space] [once_per_game] DO summon to all position [terrain is land] [position is bordering] <Hydra Head> (amount=count of (position [terrain is land] [position is bordering]), power=2, health=1) THEN give_keyword it <Haste> for permanent THEN give_ability it
   - Sagami Grovecaller -> Sapphire Yak: moves: moves my units or land forward: they reach enemy ground
        [faeria] line now: moves: moves my units or land forward: they reach enemy ground; moves: moves it where it must be
        Sagami Grovecaller: WHEN played of self DO move chosen mine unit in board [card not Sagami Grovecaller] to chosen mine position [terrain is forest] <Teleport>
        Sapphire Yak: WHEN harvests by mine unit [type is yak] of enemy position [terrain is resource_well] DO stat_change actor (power=2, health=2) for permanent

4. Wrong thinking: "it can enter where it needs to be" is given to cards whose need is only where they are summoned (Gift read once at summon), or about themselves (own land, act next to self), or ask a kind the mover is not.
   Rule: L2, L1, L20. Games: Faeria. Files: f1 c2, f2 c2, f3 c2.
   - Barrensky Vulture -> Triton Tactician: moves: moves my units or land forward: it can enter where it needs to be
        [faeria] line now: moves: moves my units or land forward: it can enter where it needs to be
        Barrensky Vulture: KW: Flying | WHEN always DO give_keyword self <Flying> for permanent | WHEN played of self DO kill chosen unit in board [health eq 1] THEN stat_change self (power=stat power of (it)) for permanent
        Triton Tactician: KW: Jump | WHEN always DO give_keyword self <Jump> for permanent | WHEN played of self DO stat_change self (power=count of (all mine unit in board [type is triton] [position is bordering])) for permanent
   - Spear of the Guardians -> Topaz Yak: moves: moves my units or land forward: it can enter where it needs to be
        [faeria] line now: moves: moves my units or land forward: it can enter where it needs to be
        Spear of the Guardians: KW: Divine, Flying, Dash | WHEN always DO give_keyword self <Divine> for permanent THEN give_keyword self <Flying> for permanent THEN give_keyword self <Dash> (amount=5) for permanent | WHEN always DO can self to position [position is bordering] (event=summoned) for while
        Topaz Yak: WHEN always DO can self to position [position is bordering] (event=summoned) for while | WHEN played of self IF have all mine unit in board [type is yak] [position is bordering] is DO give_keyword self <Haste> for permanent
   - Syland Horsemaster -> Bomb Slinger: moves into place: moves my units or land forward: it can enter where it needs to be
        [faeria] line now: moves: moves my units or land forward: it can enter where it needs to be
        Syland Horsemaster: WHEN played of self DO give_keyword chosen mine unit in board [card not Syland Horsemaster] <Charge> (amount=3) for this_round
        Bomb Slinger: WHEN played of self DO damage chosen enemy unit_or_structure [position is bordering] (amount=4)
        case nfa21: expect line moves: (Kaptain: Charge moves my units forward; land is built next to them, so the Slinger enters )

5. Wrong thinking: a unit's own movement keyword (Celerity, Flying, Dash, Jump) or help to any creature means "A moves your units, and B acts on units next to/around it", so it pairs with every positional card.
   Rule: L20, L1, L14 (f2 also Secret of Strength / Triton Banquet = help to any creature). Games: Faeria, Duelyst. Files: f1 c3, f2 c6, f3 c1 (Boar/Kodama part), u1 c9, u2 c8, u3 c9.
   - Demonic Salmon -> Tiki Adventurer: type: Demonic Salmon moves your units, and Tiki Adventurer acts on units next to it
        [faeria] line now: type: Demonic Salmon moves your units, and Tiki Adventurer acts on units next to it
        Demonic Salmon: KW: Haste, Flying, Charge | WHEN always DO give_keyword self <Haste> for permanent THEN give_keyword self <Flying> for permanent THEN give_keyword self <Charge> (amount=2) for permanent | WHEN always DO cant self (event=harvests) for while | WHEN strikes_nexus by self DO stat_change self (power=1, health=1) for permanent
        Tiki Adventurer: KW: Dash | WHEN always DO give_keyword self <Dash> (amount=1) for permanent | WHEN turn_end by mine player IF have enemy position [terrain is land] [position is same_space] is DO stat_change all mine unit in board [position is bordering] (power=1, health=1) for permanent
   - Dragonlark -> Vigilator: type: Dragonlark moves your units, and Vigilator acts on units around it
        [duelyst] line now: type: Dragonlark moves your units, and Vigilator acts on units around it
        Dragonlark: KW: Flying
        Vigilator: KW: Build | WHEN always DO give_keyword self <Build> (amount=1) for permanent | WHEN transformed of self DO stat_change all mine unit in board [position is surrounding] (health=3) for permanent
   - Azurite Lion -> Roar: enables: Azurite Lion moves your units, and Roar acts on units around your leader or base
        [duelyst] line now: type: Azurite Lion moves your units, and Roar acts on units around your leader or base
        Azurite Lion: KW: Celerity
        Roar: KW: Bloodbound Spell | WHEN played of self DO stat_change chosen mine unit in board [position is surrounding] (power=2) for permanent

6. Wrong thinking: a card that moves, teleports or gives Celerity only to the General is linked as moving the minion that needs to be moved behind an enemy / reactivated.
   Rule: L7. Games: Duelyst. Files: u1 c9 (second half), u2 c7.
   - Mist Walking -> Gore Horn: type: Mist Walking moves Gore Horn, and Gore Horn acts on units behind its target
        [duelyst] line now: type: Mist Walking moves Gore Horn, and Gore Horn acts on units behind its target
        Mist Walking: WHEN played of self DO move mine player (max=2)
        Gore Horn: KW: Backstab | WHEN always DO give_keyword self <Backstab> (amount=2) for permanent | WHEN attack_done by self DO stat_change self (power=1, health=1) for permanent
   - Silhouette Tracer -> Mizuchi: type: Silhouette Tracer moves Mizuchi, and Mizuchi acts on units behind its target
        [duelyst] line now: type: Silhouette Tracer moves Mizuchi, and Mizuchi acts on units behind its target
        Silhouette Tracer: KW: Opening Gambit | WHEN played of self DO move mine player (max=3)
        Mizuchi: KW: Flying, Backstab, Sentinel | WHEN attacks by player DO transform self | WHEN always DO give_keyword self <Backstab> (amount=2) for permanent | WHEN always DO give_keyword self <Sentinel> for permanent
   - Bombard -> Penumbraxx: waits: makes it attack for its effect
        [duelyst] line now: type: Bombard moves Penumbraxx, and Penumbraxx acts on units behind its target; waits: makes it attack for its effect
        Bombard: WHEN played of self DO ready all mine unit in board [keyword is Ranged]
        Penumbraxx: KW: Build, Backstab | WHEN always DO give_keyword self <Build> (amount=2) for permanent | WHEN always DO give_keyword self <Backstab> (amount=2) for permanent | WHEN attacks by self IF keyword_condition Backstab DO give_keyword self <Build> (amount=1) for permanent

7. Wrong thinking: moving a unit lets its Combat effect go off ("moves it where it must be" to Combat cards).
   Rule: L2, L4. Games: Faeria. Files: f2 c9 (f3 unsure raises the same).
   - Windborne Champion -> King's Guard: moves: moves it where it must be
        [faeria] line now: moves: moves it where it must be
        Windborne Champion: KW: Flying, Charge | WHEN always DO give_keyword self <Flying> for permanent THEN give_keyword self <Charge> (amount=5) for permanent | WHEN played of self DO move chosen unit in board
        King's Guard: KW: Taunt, Combat | WHEN always DO give_keyword self <Taunt> for permanent | WHEN fights by self DO draw mine card in deck_top (amount=1)
   - Spirit Spice -> Krog, the Ogre King: moves: moves it where it must be
        [faeria] line now: moves: moves it where it must be
        Spirit Spice: WHEN played of self DO stat_change chosen unit in board (power=3, health=3) for permanent THEN give_keyword it <Charge> (amount=3) for permanent THEN give_keyword it <Flying> for permanent | WHEN always DO cost_change self (cost=minus (product (3 + event_count of (dies of mine unit) this_round))) for while
        Krog, the Ogre King: KW: Combat | WHEN fights by self DO cost_change random mine card in hand (cost=-7) for permanent
   - Cloud Machine -> Herald of War: moves: moves it where it must be
        [faeria] line now: moves: moves it where it must be
        Cloud Machine: WHEN always DO stat_change all mine unit in board (power=1) for while THEN give_keyword all mine unit in board <Flying> for while THEN give_keyword all mine unit in board <Jump> for while
        Herald of War: KW: Combat | WHEN fights by self DO give_ability mine player

8. Wrong thinking: a need about the enemy god is fed by any creature that reaches or attacks the god (own Flying/Charge reach, any attack, any damage to the opponent); some lines point the wrong way (Defender wants to be attacked; War Yak/Exalted Ogre read Life).
   Rule: L2, L1, L20, L9, L18. Games: Faeria. Files: f1 c4, f2 c7.
   - Seed of Paradise -> Defender of the Homeland: moves: moves it within reach of the enemy player
        [faeria] line now: moves: moves it within reach of the enemy player
        Seed of Paradise: KW: Flying, Dash | WHEN always DO give_keyword self <Flying> for permanent THEN give_keyword self <Dash> (amount=1) for permanent | WHEN played of self DO choose_one (options=4) OR give_ability self OR give_ability self OR give_ability self OR give_ability self
        Defender of the Homeland: KW: Taunt | WHEN always DO give_keyword self <Taunt> for permanent | WHEN played of self IF event_count strikes_nexus by all enemy unit in board ge 1 last_round DO summon <Defender of the Homeland>
   - Demon Wing -> Zealous Crusader: moves: moves it within reach of the enemy player
        [faeria] line now: moves: moves it within reach of the enemy player
        Demon Wing: KW: Flying | WHEN always DO give_keyword self <Flying> for permanent
        Zealous Crusader: KW: Charge | WHEN always DO give_keyword self <Charge> (amount=2) for permanent | WHEN strikes_nexus by mine unit DO stat_change self (power=1, health=1) for permanent
   - Volcanic Colossus -> Oradrim Sagittarius: waits: makes your units hit the enemy player (by fighting)
        [faeria] line now: waits: makes your units hit the enemy player (by fighting)
        Volcanic Colossus: KW: Ranged Attack | WHEN always DO give_keyword self <Ranged Attack> for permanent | WHEN always DO cost_change self (cost=minus (event_count of (nexus_damaged by mine player of enemy player) different_rounds), min=5) for while
        Oradrim Sagittarius: KW: Ranged Attack | WHEN always DO give_keyword self <Ranged Attack> for permanent | WHEN strikes_nexus by mine unit DO mana_gain mine player (amount=1)

9. Wrong thinking: a transform (Frogify, The World's Tear) that removes B's text is linked as helping that text (new form has Jump/Flying).
   Rule: L1. Games: Faeria. Files: f2 c8.
   - Frogify -> Oradrim Monk: moves: moves it within reach of the enemy player
        [faeria] line now: moves: moves it within reach of the enemy player
        Frogify: WHEN played of self DO transform chosen unit in board <Frog> (power=2, health=2) THEN give_keyword it <Jump> for permanent
        Oradrim Monk: KW: Haste | WHEN always DO give_keyword self <Haste> for permanent | WHEN strikes_nexus by self DO draw mine card in deck_top (amount=1)
   - The World's Tear -> Krog, the Ogre King: moves: moves it where it must be
        [faeria] line now: moves: moves it where it must be
        The World's Tear: WHEN played of self DO transform chosen unit in board [state is struck_player_this_round] <Sky Swallower> (power=10, health=10) THEN give_keyword it <Flying> for permanent
        Krog, the Ogre King: KW: Combat | WHEN fights by self DO cost_change random mine card in hand (cost=-7) for permanent
   - Frogify -> Tax Collector: moves: moves it where it must be
        [faeria] line now: moves: moves it where it must be
        Frogify: WHEN played of self DO transform chosen unit in board <Frog> (power=2, health=2) THEN give_keyword it <Jump> for permanent
        Tax Collector: KW: Combat | WHEN fights by self DO mana_gain mine player (amount=1)

10. Wrong thinking: "transforms" is equated with "built" (Cloudcaller/Disciple of Yggdra/Eternity Painter feed Rescue-RX/Architect-T2K5/Manakite Drifter).
    Rule: L10, L1. Games: Duelyst. Files: u1 c13.
    - Cloudcaller -> Rescue-RX: waits: transforms it for its effect
        [duelyst] line now: waits: transforms it for its effect
        Cloudcaller: KW: Opening Gambit | WHEN played of self DO refresh mine player THEN transform mine spell [keyword is Bloodbound Spell] <Lesser Waterball> for this_round
        Rescue-RX: KW: Build | WHEN always DO give_keyword self <Build> (amount=2) for permanent | WHEN transformed of self DO heal mine player (amount=5)
    - Disciple of Yggdra -> Architect-T2K5: waits: transforms cards
        [duelyst] line now: waits: transforms cards
        Disciple of Yggdra: WHEN given_keyword of enemy unit [keyword is Stunned] DO transform self <Yggdra's Voracity>
        Architect-T2K5: KW: Build | WHEN always DO give_keyword self <Build> (amount=1) for permanent | WHEN transformed of mine unit in board DO draw mine card in deck_top (amount=1)
    - Eternity Painter -> Manakite Drifter: waits: transforms cards (for the ability it gives)
        [duelyst] line now: waits: transforms cards (for the ability it gives)
        Eternity Painter: WHEN turn_end by mine player DO transform all enemy unit in board [position is surrounding] <Panddo> (power=0, health=2) THEN cant all unit in board to all unit in board [card is Panddo] (event=attacks) for while
        Manakite Drifter: KW: Build | WHEN played of self DO give_ability mine player for this_round | WHEN always DO give_keyword self <Build> (amount=2) for permanent

11. Wrong thinking: a card that hits Flying creatures (Destructive Volley) is fed by my own Flying cards.
    Rule: L9. Games: Faeria. Files: f1 c12.
    - Astral Weapon -> Destructive Volley: type: has Flying
        [faeria] line now: type: has Flying
        Astral Weapon: KW: Flying | WHEN always DO give_keyword self <Flying> for permanent | WHEN played of self DO kill all unit_or_structure [position is bordering] THEN set_terrain all position [terrain is land] [position is bordering] to position [terrain is ocean]
        Destructive Volley: WHEN played of self DO damage chosen unit in board [keyword not Flying] (amount=2) THEN damage it unit in board [keyword is Flying] (amount=5)
    - Seed of Paradise -> Destructive Volley: type: makes units get Flying
        [faeria] line now: type: makes units get Flying; type: has Flying
        Seed of Paradise: KW: Flying, Dash | WHEN always DO give_keyword self <Flying> for permanent THEN give_keyword self <Dash> (amount=1) for permanent | WHEN played of self DO choose_one (options=4) OR give_ability self OR give_ability self OR give_ability self OR give_ability self
        Destructive Volley: WHEN played of self DO damage chosen unit in board [keyword not Flying] (amount=2) THEN damage it unit in board [keyword is Flying] (amount=5)

12. Wrong thinking: a neutral card gets "turns a land into the colour it needs".
    Rule: L22. Games: Faeria. Files: f1 c13.
    - Fire Elemental -> Path to Paradise: type: turns a land into the colour it needs: helps pay its land cost
        [faeria] line now: type: turns a land into the colour it needs: helps pay its land cost
        Fire Elemental: WHEN played of self DO set_terrain chosen position [terrain is ocean] to position [terrain is mountain]
        Path to Paradise: WHEN played of self DO choose_one (options=4) OR set_terrain chosen position [terrain is ocean] to position [terrain is forest] OR set_terrain chosen position [terrain is ocean] to position [terrain is lake] OR set_terrain chosen position [terrain is ocean] to position [terrain is mountain] OR set_terrain chosen position [terrain is ocean] to position [terrain is desert] THEN give_ability mine player for this_round
    - Ring of Dominion -> Path to Paradise: type: turns a land into the colour it needs: helps pay its land cost, and can take that land from the enemy
        [faeria] line now: type: turns a land into the colour it needs: helps pay its land cost, and can take that land from the enemy
        Ring of Dominion: WHEN played of self DO choose_one (options=4) OR set_terrain chosen position [terrain is land] to position [terrain is forest] THEN steal it OR set_terrain chosen position [terrain is land] to position [terrain is lake] THEN steal it OR set_terrain chosen position [terrain is land] to position [terrain is mountain] THEN steal it OR set_terrain chosen position [terrain is land] to position [terrain is desert] THEN steal it
        Path to Paradise: WHEN played of self DO choose_one (options=4) OR set_terrain chosen position [terrain is ocean] to position [terrain is forest] OR set_terrain chosen position [terrain is ocean] to position [terrain is lake] OR set_terrain chosen position [terrain is ocean] to position [terrain is mountain] OR set_terrain chosen position [terrain is ocean] to position [terrain is desert] THEN give_ability mine player for this_round

## B. Fighting, Nexus damage, credit

13. Wrong thinking: a unit's own fight keyword (Elusive, Overwhelm, Fearsome, Impact, Scout, Quick Attack) means it "damages the enemy player" / "helps it hit the enemy player" for every Plunder card and every Nexus-damage champion; also Plunder is checked when played, so helping the Plunder card later does nothing; many B are spells.
    Rule: L20, L2. Games: Runeterra. Files: r1 c2, r2 c1, r3 c14, r4 c1, r7 c3.
    - Alpha Wildclaw -> Snowy Razorclaw: damages the enemy player
        [runeterra] line now: type: damages the enemy player; type: helps it hit the enemy player
        Alpha Wildclaw: KW: Overwhelm
        Snowy Razorclaw: KW: Overwhelm, Plunder | WHEN played of self IF keyword_condition Plunder DO stat_set chosen mine unit in board (power=stat power of (self), health=stat health of (self))
    - Abyssal Eye -> Dashing Dandy: damages the enemy player
        [runeterra] line now: type: damages the enemy player; type: helps it hit the enemy player
        Abyssal Eye: KW: Elusive, Deep | WHEN strikes_nexus by self DO draw mine card in deck_top (amount=1)
        Dashing Dandy: KW: Plunder, Overwhelm | WHEN played of self IF keyword_condition Plunder DO stat_change self (power=stat power of (self)) for permanent
    - Necrotic Nestling -> Teenydactyl: type: helps it hit the enemy player
        [runeterra] line now: type: damages the enemy player; type: helps it hit the enemy player
        Necrotic Nestling: KW: Fearsome
        Teenydactyl: WHEN round_end IF event_count nexus_damaged of enemy player ge 1 this_round DO transform self <Terrordactyl>

14. Wrong thinking: fighting itself (any unit can attack/block, counterattack, Frenzy, Blast, "attack again") is counted as making units die / strike / hit the Nexus / attack, so every unit is a source.
    Rule: L1, L2, L9, L18. Games: Runeterra, Duelyst. Files: r1 c1, u1 c3, u2 c11, u3 c5 (Dispirited Prisoner part).
    - Ye Been Warned <- Affectionate Poro: makes enemy units die (by fighting)
    - Faie Bloodwing -> Resonance Scythe: waits: kills enemy units (by fighting)
        [duelyst] line now: waits: kills enemy units (by the game's rule: units counterattack); waits: kills enemy units (by fighting)
        Faie Bloodwing: KW: Bloodbound Spell
        Resonance Scythe: WHEN always DO stat_change mine player (power=1) for while | WHEN killed by mine player of enemy unit [keyword is Stunned] DO ready mine player
    - Piercing Mantis -> Gate to the Undervault: waits: makes units die
        [duelyst] line now: waits: makes units die
        Piercing Mantis: KW: Frenzy
        Gate to the Undervault: KW: Invulnerable, Build | WHEN always DO give_keyword self <Build> (amount=3) for permanent | WHEN dies of unit in board DO summon random unit in board to chosen position [position is surrounding]

15. Wrong thinking: A makes B and B acts on C, but A is credited with what B does.
    Rule: L3. Games: Runeterra. Files: r5 c9, r6 c8, r7 c4.
    - Aurelion Sol -> Braum: more health or protection: survives damage (levels it up)
        [runeterra] line now: levels: more health or protection: survives damage (levels it up); waits: more health or protection: survives damage
        Aurelion Sol: KW: Fury, SpellShield | WHEN played of self DO keyword_action mine card in hand [type is Celestial] [cost ge 7] <Invoke> for unstated | WHEN round_start DO create random mine card [type is Celestial] in hand | WHEN round_end IF stat all mine unit in board power ge 20 DO level_up self
        Braum: KW: Challenger, Regeneration | WHEN survives_damage of self [once_per_game] DO summon in board <Mighty Poro> | WHEN always IF event_count survives_damage of self damage ge 10 this_game DO level_up self
    - Captain Farron -> Swain (level 2): triggers: damages the enemy player; also helps it hit the enemy player
        [runeterra] line now: waits: damages the enemy player; waits: helps it hit the enemy player
        Captain Farron: KW: Overwhelm | WHEN summoned of self DO create in hand <Decimate> (amount=2)
        Swain (level 2): KW: Fearsome, Overwhelm | WHEN nexus_damaged by mine player of enemy player IF it_matches [origin not combat] DO stun highest enemy unit by power in board [state not in_combat] for this_round | WHEN strikes_nexus by self DO damage all enemy unit in board (amount=3) THEN damage enemy player (amount=3)
    - Tybaulk -> Snip Snip Snip!: makes stronger: its damage gets 1 more; also more power
        [runeterra] line now: stronger: its damage gets 1 more; stronger: more power
        Tybaulk: KW: Overwhelm | WHEN summoned of self DO stat_change all mine unit in everywhere (power=1) for permanent THEN give_ability mine player for permanent
        Snip Snip Snip!: KW: Skill | WHEN played of self DO keyword_action enemy player <Drain> (amount=1, times=half (stat power of (mine unit [card is Gwen])), max=50, min=2) for unstated

## C. Help (stats, keywords, heals, damage)

16. Wrong thinking: help or a tutor aimed at a kind/group (Flying, Jump, Combat, yak, 5+ Life, 1 cost, Yordle, Elite, Fae, Fearsome, tribe, Lurker, Vespyr) is linked to every card of that kind, though the receiving text does not use it.
    Rule: L14 (also L15, L18, L1b). Games: Faeria, Runeterra, Duelyst. Files: f1 c8, f3 c3, f4 c2, f4 c3, r1 c3, r2 c3, r3 c1, r6 c4, u3 c1 (f2 unsure).
    - Drakkar Skycaptain -> Airbot: makes stronger: gives it more power and health when it comes
        [faeria] line now: stronger: gives it more power and health when it comes
        Drakkar Skycaptain: KW: Flying | WHEN always DO give_keyword self <Flying> for permanent | WHEN drawn of mine card in hand [category is unit] [keyword is Flying] DO stat_change it (power=1, health=1) for permanent
        Airbot: KW: Flying, Dash | WHEN always DO give_keyword self <Flying> for permanent THEN give_keyword self <Dash> (amount=2) for permanent
    - Yordle Captain -> Aatrox: gives it more power and health when it comes
        [runeterra] line now: stronger: gives it more power and health when it comes
        Yordle Captain: WHEN summoned by mine player of mine unit [card not Yordle Captain] [power le stat power of (self)] DO stat_change it (power=1, health=1) for permanent
        Aatrox: WHEN played of self DO attach self <The Darkin Blade> | WHEN summoned of self DO heal mine player (amount=2) | WHEN summoned of self IF have mine card in hand [card is World Ender] not DO create in hand <World Ender> | WHEN strikes by self DO heal mine player (amount=2) | WHEN strikes by self IF have mine card in hand [card is World Ender] not DO create in hand <World Ender> | WHEN always IF event_count played by mine player of spell [card is World Ender] ge 1 this_game DO level_up self
    - Oakenheart -> Replicant: makes stronger: gives it more power and health
        [duelyst] line now: stronger: gives it more power and health
        Oakenheart: KW: Opening Gambit | WHEN played of self DO keyword_action <MECHAZ0R> (amount=20) | WHEN always DO stat_change all mine unit in board [type is Mech] [card not Oakenheart] (power=1, health=1) for while
        Replicant: KW: Opening Gambit | WHEN played of self DO draw chosen mine card in deck [card is Replicant] (amount=1)

17. Wrong thinking: every heal, power boost, keyword or damage protection for "your General" is linked to every General card, whose only text is a Bloodbound Spell; Generals are in every deck.
    Rule: L14, L18, L20 (also L1, L13, L16). Games: Duelyst. Files: u1 c1, u2 c5, u3 c2, u3 c3.
    - Aer Pridebeak -> Argeon Highmayne: heals: can heal it
        [duelyst] line now: heals: can heal it
        Aer Pridebeak: WHEN played of enemy spell DO heal mine player (amount=1)
        Argeon Highmayne: KW: Bloodbound Spell
    - Dawn's Eye -> Argeon Highmayne: stronger: can give it more power
        [duelyst] line now: stronger: can give it more power
        Dawn's Eye: WHEN always DO stat_change mine player (power=4) for while | WHEN turn_end by mine player DO heal all mine equipment (amount=full)
        Argeon Highmayne: KW: Bloodbound Spell
    - Cyclone Mask -> Shidai Stormblossom: gives keyword: can give it Ranged
        [duelyst] line now: keyword: can give it Ranged
        Cyclone Mask: WHEN always DO give_keyword mine player <Ranged> for while_attached
        Shidai Stormblossom: KW: Bloodbound Spell
        case ndu39: expect line  (Kaptain: Cyclone Mask gives the General Ranged)

18. Wrong thinking: a heal is linked to Provoke minions, though L18 lets only "more health" reach Taunt units.
    Rule: L14, L18. Games: Duelyst. Files: u1 c8 (u2 unsure, u3 unsure).
    - Lux Ignis -> Fireblazer: heals: can heal it
        [duelyst] line now: heals: can heal it (when around it)
        Lux Ignis: KW: Ranged | WHEN turn_end by mine player DO heal all mine unit in board [position is surrounding] (amount=2)
        Fireblazer: KW: Provoke
    - Sundrop Elixir -> Fireblazer: heals: can heal it
        [duelyst] line now: heals: can heal it
        Sundrop Elixir: WHEN played of self DO heal chosen any in board (amount=5)
        Fireblazer: KW: Provoke
    - Healing Mystic -> Lady Locke: heals: can heal it
        [duelyst] line now: heals: can heal it
        Healing Mystic: KW: Opening Gambit | WHEN played of self DO heal chosen any in board (amount=2)
        Lady Locke: KW: Provoke, Opening Gambit | WHEN played of self DO give_ability mine player for this_round

19. Wrong thinking: generic power/health is linked to a card whose text does not read its own stats, reads only the damage it deals/a fixed amount, or reads another card's stats (the General, equipment, a Tentacle).
    Rule: L18 (also L7). Games: Faeria, Runeterra, Duelyst. Files: f1 c7, r1 c7, r5 c8, u1 c7, u2 c6, u2 c12 (hits-several / splash part).
    - Path to Paradise -> Enslaved Priest: stronger: more power: its text uses the damage it deals when it comes
        [faeria] line now: stronger: more power: its text uses the damage it deals when it comes
        Path to Paradise: WHEN played of self DO choose_one (options=4) OR set_terrain chosen position [terrain is ocean] to position [terrain is forest] OR set_terrain chosen position [terrain is ocean] to position [terrain is lake] OR set_terrain chosen position [terrain is ocean] to position [terrain is mountain] OR set_terrain chosen position [terrain is ocean] to position [terrain is desert] THEN give_ability mine player for this_round
        Enslaved Priest: WHEN keyword_used by mine unit of keyword [keyword is Corrupt] DO damage enemy player (amount=2) THEN heal mine player (amount=event_amount)
    - Adept Weaponsmith -> The Tuskraider: more power
        [runeterra] line now: stronger: more health; stronger: more power
        Adept Weaponsmith: WHEN played of self DO keyword_action chosen mine unit in board <Forge> for unstated
        The Tuskraider: KW: Plunder | WHEN summoned of self DO draw mine card in deck [card is Sejuani] (amount=1) | WHEN played of self IF keyword_condition Plunder DO stat_set all mine unit in deck (power=double (stat power of (it)), health=double (stat health of (it))) for permanent
    - Mirkblood Devourer -> Drogon: stronger: more power
        [duelyst] line now: stronger: more power
        Mirkblood Devourer: WHEN summoned of mine unit [position is surrounding] DO stat_change it (power=1, health=1) for permanent
        Drogon: WHEN played of mine spell [keyword is Bloodbound Spell] DO stat_change mine player (power=stat power of (mine player)) for this_round

20. Wrong thinking: all health/stat help links to a card that reads only Power (and its own stats are not read).
    Rule: L15, L18. Games: Runeterra. Files: r2 c5.
    - Tiny Shield -> Xolaani the Bloodweaver: can give it more health
        [runeterra] line now: type: changes your units' stats; stronger: can give it more health
        Tiny Shield: KW: Focus | WHEN played of self DO stat_change chosen mine unit in board (health=1) for permanent
        Xolaani the Bloodweaver: KW: Overwhelm, Empowered | WHEN always DO stat_change self (power=double (event_count of (dies of mine unit [state is buffed]) this_game), health=double (event_count of (dies of mine unit [state is buffed]) this_game)) for while | WHEN always IF keyword_condition Empowered 16 DO transform self <Xolaani, Aspect's Bane>
    - Galio -> Xolaani the Bloodweaver: gives it more health
        [runeterra] line now: type: changes your units' stats; stronger: gives it more health
        Galio: KW: Formidable, SpellShield | WHEN summoned of self DO stat_change all mine unit in board [card not Galio] (health=3) for permanent | WHEN round_end IF stat all mine unit in board health ge 25 DO level_up self
        Xolaani the Bloodweaver: KW: Overwhelm, Empowered | WHEN always DO stat_change self (power=double (event_count of (dies of mine unit [state is buffed]) this_game), health=double (event_count of (dies of mine unit [state is buffed]) this_game)) for while | WHEN always IF keyword_condition Empowered 16 DO transform self <Xolaani, Aspect's Bane>
    - Bayou Brunch -> Xolaani the Bloodweaver: turns the Health it grows into Health
        [runeterra] line now: type: changes its stats for its effect; type: changes your units' stats; stronger: turns the Power it grows into Power; stronger: turns the Health it grows into Health; stronger: can give it more power and health
        Bayou Brunch: WHEN played of self DO capture chosen mine unit in board [card not Bayou Brunch] to chosen mine unit in board THEN stat_change chosen mine unit in board [card not Bayou Brunch] (power=stat power of (it), health=stat health of (it)) for permanent
        Xolaani the Bloodweaver: KW: Overwhelm, Empowered | WHEN always DO stat_change self (power=double (event_count of (dies of mine unit [state is buffed]) this_game), health=double (event_count of (dies of mine unit [state is buffed]) this_game)) for while | WHEN always IF keyword_condition Empowered 16 DO transform self <Xolaani, Aspect's Bane>

21. Wrong thinking: a stat boost on the board is linked to a card that already read its stats (Gift fight already happened, Play/summon effect already went off, card in hand vs played one, fight on summon).
    Rule: L18 (also L4, L14). Games: Faeria, Runeterra, Duelyst. Files: f1 c7 (Animated Banquet), f2 c13, r4 c3, u2 c12 (Lavaslasher).
    - Spirit Spice -> Barrensky Vermin: stronger: can give it more power and health
        [faeria] line now: stronger: can give it more power and health
        Spirit Spice: WHEN played of self DO stat_change chosen unit in board (power=3, health=3) for permanent THEN give_keyword it <Charge> (amount=3) for permanent THEN give_keyword it <Flying> for permanent | WHEN always DO cost_change self (cost=minus (product (3 + event_count of (dies of mine unit) this_round))) for while
        Barrensky Vermin: WHEN played of self DO start_attack self to enemy player <Fight>
    - Rising Spell Force -> Banana Blaster: stronger: more power
        [runeterra] line now: stronger: more power
        Rising Spell Force: WHEN played of self DO stat_change chosen mine unit in board (power=4) for this_round THEN give_keyword chosen mine unit in board <Quick Attack> for this_round
        Banana Blaster: WHEN played of self DO damage chosen unit in board (amount=stat power of (self))
    - Blood Rage -> Lavaslasher: stronger: can give it more power and health
        [duelyst] line now: stronger: can give it more power and health
        Blood Rage: WHEN played of self DO stat_change chosen mine unit in board (power=event_count of (damaged) this_round, health=event_count of (damaged) this_round) for permanent
        Lavaslasher: KW: Opening Gambit | WHEN played of self DO start_attack self to chosen enemy unit in board [position is surrounding]

22. Wrong thinking: a giver is linked as giving help it cannot give to B (narrow kind such as Ephemeral/1 cost, itself, enemies, only certain target, other card).
    Rule: L4, L8, L14, L9. Games: Runeterra. Files: r1 c8, r4 c4.
    - Here to Help -> Gangplank: more power: its text uses the damage it deals
        [runeterra] line now: stronger: more power: its text uses the damage it deals
        Here to Help: WHEN played of self DO stat_change chosen mine unit in board [state not damaged] (health=3) for this_round THEN stat_change it mine unit [state is damaged] (power=2, health=3) for this_round
        Gangplank: KW: Overwhelm | WHEN summoned of self DO summon in board <Powder Keg> | WHEN always IF event_count nexus_damaged of enemy player ge 5 different_rounds DO level_up self
    - Soul Shepherd -> Vi: stronger: more power
        [runeterra] line now: type: changes its stats for its effect; stronger: more power
        Soul Shepherd: WHEN summoned by mine player of mine unit [state is ephemeral] DO stat_change it (power=1, health=1) for permanent
        Vi: KW: Challenger, Tough | WHEN played by mine player of card [card not Vi] IF stat self power lt sum (stat base_power of (self) + 8) DO stat_change self (power=1) for permanent | WHEN always IF event_count strikes by self [damage ge 10] ge 1 this_game DO level_up self
    - Ornn (level 2) -> Wrought Colossus: stronger: more health / more power
        [runeterra] line now: stronger: more health; stronger: more power
        Ornn (level 2): KW: Tough, Attack | WHEN played of self DO choose_one OR copy chosen mine equipment in attached THEN attach it to self OR attach highest mine equipment by power in hand to self | WHEN attacks by self DO keyword_action self <Forge> (times=2) for unstated THEN summon mine unit in board <Spirit of the Ram> THEN stat_set it (power=stat power of (self), health=stat health of (self)) THEN start_attack it
        Wrought Colossus: KW: Overwhelm | WHEN equipped by equipment of self [once_per_game] DO copy self in hand THEN cost_change it (cost=4) for permanent THEN stat_change it (power=stat power of (actor equipment), health=stat health of (actor equipment)) for permanent

23. Wrong thinking: a stat change is linked to a card it cannot reach (structures Doomgate/Faeria Tree) or goes the wrong way (lowering Life where the card needs it to rise; a 6/6 stops Seedling).
    Rule: L8, L21. Games: Faeria. Files: f1 c6, f4 c4.
    - Tower of Curses -> Doomgate, Door to Oblivion: type: changes its stats for its effect
        [faeria] line now: type: changes its stats for its effect
        Tower of Curses: WHEN activated DO stat_change chosen unit in board (power=-1, health=-1) for permanent THEN damage self (amount=1)
        Doomgate, Door to Oblivion: WHEN always IF stat self health ge 13 DO kill self THEN summon to position [position is same_space] <Ostregoth> | WHEN activated DO sacrifice chosen mine unit in board THEN draw mine card in deck_top (amount=1) THEN stat_change self (health=2) for permanent
    - Aurora, Myth Maker -> Faeria Tree: type: changes its stats for its effect
        [faeria] line now: type: changes its stats for its effect
        Aurora, Myth Maker: WHEN played of self DO stat_set chosen mine unit in board [card not Aurora, Myth Maker] (power=6, health=6)
        Faeria Tree: KW: Production | WHEN turn_start by mine player DO stat_change self (health=1) for permanent | WHEN always IF stat self health ge 5 DO kill self THEN mana_gain mine player (amount=10)
    - The Emperor's Command -> Faeria Tree: enables: changes its stats for its effect
        [faeria] line now: type: changes its stats for its effect
        The Emperor's Command: WHEN played of self DO stat_change chosen unit in board (power=-2, health=-1) for permanent OR damage chosen landmark (amount=3) OR heal chosen player (amount=4)
        Faeria Tree: KW: Production | WHEN turn_start by mine player DO stat_change self (health=1) for permanent | WHEN always IF stat self health ge 5 DO kill self THEN mana_gain mine player (amount=10)

24. Wrong thinking: "spells deal 1 extra damage" / "double all damage" / "your damage boost" is linked to every spell or damage card (also to spells that deal no damage, to Last Breath/death effects, to champions that do not read damage).
    Rule: L18 (gives_lines: more damage alone is never a use; also L21, L4). Games: Runeterra, Duelyst. Files: r1 c4, r2 c4, r4 c6, r5 c20, r6 c1, r7 c1, u1 c15, u3 c4.
    - Powder Keg -> Advanced Intel: makes its effect bigger
        [runeterra] line now: stronger: makes its effect bigger
        Powder Keg: KW: Immobile, Vulnerable | WHEN always DO increase_effect all mine spell [category in spell] [category in skill] (amount=1) for while | WHEN damaged by mine spell [category in spell] [category in skill] of enemy any DO kill self
        Advanced Intel: WHEN played of self DO keyword_action 8 enemy card in deck_top <Flashbomb Trap Plant> (amount=2) THEN draw mine card in deck_top (amount=1)
    - Crescent Spear -> Phoenix Fire: stronger: makes its effect bigger
        [duelyst] line now: stronger: makes its effect bigger
        Crescent Spear: WHEN always DO stat_change mine player (power=1) for while THEN increase_effect mine spell [does in damage] (amount=1) for while
        Phoenix Fire: WHEN played of self DO damage chosen any in board (amount=3)
    - The Dreadway -> Decimate: makes stronger: doubles its damage
        [runeterra] line now: stronger: doubles its damage
        The Dreadway: KW: Fearsome | WHEN summoned of self DO draw mine card in deck [card is Gangplank] (amount=1) | WHEN damaged by mine spell DO damage it (amount=event_amount) | WHEN damaged by mine unit DO damage it (amount=event_amount)
        Decimate: WHEN played of self DO damage enemy player (amount=4)

25. Wrong thinking: a boost/non-damage card (Tybaulk, Might, The Dreadway) is read as dealing damage or killing itself.
    Rule: L1, L3 (r7: L1/L4/L18). Games: Runeterra. Files: r6 c2, r7 c2.
    - Tybaulk -> The Harrowing: enables: makes your units die: The Harrowing brings them back
        [runeterra] line now: type: makes your units die: The Harrowing brings them back
        Tybaulk: KW: Overwhelm | WHEN summoned of self DO stat_change all mine unit in everywhere (power=1) for permanent THEN give_ability mine player for permanent
        The Harrowing: WHEN played of self DO revive 6 highest mine unit by power in discard THEN give_keyword it <Ephemeral> for permanent
    - Might -> Scorched Earth: enables: more damage
        [runeterra] line now: type: more damage
        Might: WHEN played of self DO stat_change chosen mine unit in board (power=3) for this_round THEN give_keyword it <Overwhelm> for this_round
        Scorched Earth: WHEN played of self DO kill chosen unit in board [state is damaged] OR kill chosen landmark in board
    - The Dreadway -> Scorched Earth: enables: damages enemy units or players: Scorched Earth kills them
        [runeterra] line now: type: damages enemy units or players: Scorched Earth kills them
        The Dreadway: KW: Fearsome | WHEN summoned of self DO draw mine card in deck [card is Gangplank] (amount=1) | WHEN damaged by mine spell DO damage it (amount=event_amount) | WHEN damaged by mine unit DO damage it (amount=event_amount)
        Scorched Earth: WHEN played of self DO kill chosen unit in board [state is damaged] OR kill chosen landmark in board

26. Wrong thinking: removing enemy Block, keeping Block (Barricade), or more Block per Dexterity is linked to every Attack/Block card though none reads it.
    Rule: L14, L18. Games: Slay the Spire. Files: s2 c3, s2 c4, s2 c7.
    - Melter -> Hyperbeam: makes stronger: removes their Block: its damage gets through
        [sts1] line now: stronger: removes their Block: its damage gets through
        Melter: WHEN played of self DO remove_keyword chosen enemy unit in board <Block> THEN damage it enemy unit (amount=10)
        Hyperbeam: WHEN played of self DO damage all enemy unit in board (amount=26) THEN give_keyword mine player <Focus> (amount=-3) for permanent
    - Barricade -> Defend (Ironclad): makes stronger: keeps the Block it gives
        [sts1] line now: stronger: keeps the Block it gives
        Barricade: WHEN always DO cant mine keyword [keyword is Block] (event=keyword_removed) for while
        Defend (Ironclad): WHEN played of self DO give_keyword mine player <Block> (amount=5) for permanent
    - Kunai -> Reinforced Body: makes stronger: makes the Block it gives bigger
        [sts1] line now: stronger: makes the Block it gives bigger
        Kunai: WHEN played of mine spell [type is Attack] [once_per_round] IF event_count played of mine spell [type is Attack] every 3 this_round DO give_keyword mine player <Dexterity> (amount=1) for permanent
        Reinforced Body: WHEN played of self DO give_keyword mine player <Block> (amount=7, times=x_paid) for permanent

27. Wrong thinking: any stat change counts as Gwen's "gains Power from Hallowed" trigger or Bard's "increased total stats" (Frostbite, Gloom, Tybaulk +1|+0, self-buff keywords); Gwen is also read as giving/using any stat change.
    Rule: L15, L14, L4. Games: Runeterra. Files: r3 c2, r4 c5, r5 c7, r6 c3.
    - Rimetusk Shaman -> Gwen (level 2): waits: changes units' stats (for the ability it gives)
        [runeterra] line now: waits: changes units' stats (for the ability it gives)
        Rimetusk Shaman: WHEN round_start DO keyword_action highest enemy unit by power in board <Frostbite> for unstated
        Gwen (level 2): KW: Hallowed, Quick Attack, Attack | WHEN attacks by self DO give_ability self for this_round THEN keyword_action enemy player <Drain> (amount=1, times=half (stat power of (self))) for unstated
    - Bayou Brunch -> Gwen: changes your units' stats
        [runeterra] line now: waits: changes your units' stats; stronger: turns the Power it grows into Power; stronger: can give it more power and health
        Bayou Brunch: WHEN played of self DO capture chosen mine unit in board [card not Bayou Brunch] to chosen mine unit in board THEN stat_change chosen mine unit in board [card not Bayou Brunch] (power=stat power of (it), health=stat health of (it)) for permanent
        Gwen: KW: Hallowed, Quick Attack, Attack | WHEN attacks by self DO keyword_action enemy player <Drain> (amount=2) for unstated | WHEN stat_changed of mine unit [card not Gwen] IF keyword_condition Hallowed DO stat_change self (power=event_amount) for while | WHEN always IF event_count damaged by self damage ge 10 this_game DO level_up self
    - Tybaulk -> Gwen: triggers: changes your units' stats; also makes stronger: gives it more power
        [runeterra] line now: waits: changes your units' stats; stronger: gives it more power
        Tybaulk: KW: Overwhelm | WHEN summoned of self DO stat_change all mine unit in everywhere (power=1) for permanent THEN give_ability mine player for permanent
        Gwen: KW: Hallowed, Quick Attack, Attack | WHEN attacks by self DO keyword_action enemy player <Drain> (amount=2) for unstated | WHEN stat_changed of mine unit [card not Gwen] IF keyword_condition Hallowed DO stat_change self (power=event_amount) for while | WHEN always IF event_count damaged by self damage ge 10 this_game DO level_up self
        case n269: expect none (levels it up) (Kaptain 31 Oct 2026: +1|+0 does not level Gwen)

28. Wrong thinking: any stat change is linked to Out Of The Way, which only makes "this round" buffs permanent.
    Rule: none stated. Games: Runeterra. Files: r3 c3.
    - Starhound Pack -> Out Of The Way: type: changes your units' stats: Out Of The Way lets them do more
        [runeterra] line now: type: changes your units' stats: Out Of The Way lets them do more
        Starhound Pack: WHEN always DO stat_change all mine unit in everywhere [name_has is Starhound Pack] <Fated> for while
        Out Of The Way: WHEN played of self DO can all mine unit [state is buffed] [keyword not Barrier] for permanent THEN draw mine card in deck_top (amount=1)
    - Grotesque Gift -> Out Of The Way: type: changes your units' stats: Out Of The Way lets them do more
        [runeterra] line now: type: changes your units' stats: Out Of The Way lets them do more
        Grotesque Gift: KW: Spirit | WHEN summoned of enemy unit [once_per_game] DO give_keyword it <Gloom> for permanent
        Out Of The Way: WHEN played of self DO can all mine unit [state is buffed] [keyword not Barrier] for permanent THEN draw mine card in deck_top (amount=1)

29. Wrong thinking: an enemy debuff (Gloom) is read as "changes your units' stats" for champion level-ups.
    Rule: L9. Games: Runeterra. Files: r3 c4.
    - Grotesque Gift -> Aurelion Sol: levels: changes your units' stats (levels it up)
        [runeterra] line now: levels: changes your units' stats (levels it up)
        Grotesque Gift: KW: Spirit | WHEN summoned of enemy unit [once_per_game] DO give_keyword it <Gloom> for permanent
        Aurelion Sol: KW: Fury, SpellShield | WHEN played of self DO keyword_action mine card in hand [type is Celestial] [cost ge 7] <Invoke> for unstated | WHEN round_start DO create random mine card [type is Celestial] in hand | WHEN round_end IF stat all mine unit in board power ge 20 DO level_up self
    - Grotesque Gift -> Bard: levels: changes your units' stats (levels it up)
        [runeterra] line now: levels: changes your units' stats (levels it up)
        Grotesque Gift: KW: Spirit | WHEN summoned of enemy unit [once_per_game] DO give_keyword it <Gloom> for permanent
        Bard: KW: Attack | WHEN attacks by self DO keyword_action mine player in deck <Chime Plant> (amount=3) | WHEN always IF event_count stat_changed of mine unit total_stats ge 20 this_game DO level_up self
    - Grotesque Gift -> Galio: levels: changes your units' stats (levels it up)
        [runeterra] line now: levels: changes your units' stats (levels it up)
        Grotesque Gift: KW: Spirit | WHEN summoned of enemy unit [once_per_game] DO give_keyword it <Gloom> for permanent
        Galio: KW: Formidable, SpellShield | WHEN summoned of self DO stat_change all mine unit in board [card not Galio] (health=3) for permanent | WHEN round_end IF stat all mine unit in board health ge 25 DO level_up self

30. Wrong thinking: "grant keywords" / any keyword or status is matched to every card that counts, waits for or levels from one specific keyword/status (Trap, Plant, Curse, Stunned/Recalled, Block, Daybreak).
    Rule: L14, L16, L4. Games: Runeterra, Slay the Spire. Files: r2 c2, r2 c7 (Legion General part), r3 c7, r5 c6, s1 c4.
    - Papercraft Dragon (created) -> Teemo: makes units get Plant (levels it up)
        [runeterra] line now: levels: makes units get Plant (levels it up)
        Papercraft Dragon (created): KW: Attach, Double Attack | WHEN played of self DO attach self to chosen mine unit in board THEN stat_change attached_to (power=stat power of (self), health=stat health of (self)) for while_attached THEN copy_keywords attached_to to self for while_attached | WHEN leaves_play of attached_to DO keyword_action self <Recall> for unstated
        Teemo: KW: Elusive | WHEN strikes_nexus by self DO keyword_action 5 random enemy card in deck <Poison Puffcap Plant> (amount=5) | WHEN always IF event_count keyword_used by mine player of [keyword is Plant] [card is Poison Puffcap] ge 15 this_game DO level_up self
    - Acceleration Gate -> Caitlyn: makes units get Trap (levels it up)
        [runeterra] line now: levels: makes units get Trap (levels it up)
        Acceleration Gate: KW: Slow | WHEN played of self DO stat_change all mine unit in board (power=2) for this_round THEN give_keyword all mine unit in board [keyword not Quick Attack] [keyword not Double Attack] <Quick Attack> for this_round THEN give_random_keyword all mine unit in board [keyword in Quick Attack] [keyword in Double Attack] (amount=1) for this_round
        Caitlyn: KW: Quick Attack | WHEN strikes by self DO keyword_action 8 enemy card in deck_top <Flashbomb Trap Plant> (amount=2) | WHEN always IF event_count trap_activated of card [keyword is Trap] ge 5 this_game DO level_up self
    - Clockwork Souvenir -> Wave of the Hand: waits: makes units get a keyword or status (for the ability it gives)
        [sts1] line now: waits: makes units get a keyword or status (for the ability it gives)
        Clockwork Souvenir: WHEN combat_start DO give_keyword mine player <Artifact> (amount=1) for permanent
        Wave of the Hand: WHEN played of self DO give_ability mine player for this_round

## D. Draw, play, copy, make

31. Wrong thinking: draw/tutor/put by kind (or a single random draw) is linked to every card of that kind / every "when you draw X" card.
    Rule: L1b (also L14, L15, L21). Games: Faeria, Runeterra, Slay the Spire. Files: f1 c8, r1 c5, r7 c6, s1 c11, s1 c13.
    - Iona's Smile -> Astral Weapon: puts: draws it from the deck
        [faeria] line now: puts: draws it from the deck
        Iona's Smile: WHEN played of self DO draw mine card in deck [keyword is Flying] [category is unit] (amount=2)
        Astral Weapon: KW: Flying | WHEN always DO give_keyword self <Flying> for permanent | WHEN played of self DO kill all unit_or_structure [position is bordering] THEN set_terrain all position [terrain is land] [position is bordering] to position [terrain is ocean]
    - Realm Warp -> Aatrox: draws it and keeps it
        [runeterra] line now: puts: draws it and keeps it; waits: empties your hand
        Realm Warp: KW: Burst | WHEN played of self DO draw mine card in deck_top (amount=3) THEN discard it mine card in hand [category is follower]
        Aatrox: WHEN played of self DO attach self <The Darkin Blade> | WHEN summoned of self DO heal mine player (amount=2) | WHEN summoned of self IF have mine card in hand [card is World Ender] not DO create in hand <World Ender> | WHEN strikes by self DO heal mine player (amount=2) | WHEN strikes by self IF have mine card in hand [card is World Ender] not DO create in hand <World Ender> | WHEN always IF event_count played by mine player of spell [card is World Ender] ge 1 this_game DO level_up self
    - Gremlin Horn -> Fire Breathing: waits: makes you draw cards
        [sts1] line now: waits: makes you draw cards
        Gremlin Horn: WHEN dies of enemy unit DO mana_gain mine mana (amount=1) THEN draw mine card in deck_top (amount=1)
        Fire Breathing: WHEN drawn of mine card [type in Status] [type in Curse] DO damage all enemy unit in board (amount=6)

32. Wrong thinking: "create X if you don't have one / if you don't already have one" is read as "wants an empty hand".
    Rule: L5, L21, L1. Games: Runeterra. Files: r1 c6, r2 c7 (Catalogue part), r5 c1.
    - Realm Warp -> Aatrox: waits: empties your hand
        [runeterra] line now: puts: draws it and keeps it; waits: empties your hand
        Realm Warp: KW: Burst | WHEN played of self DO draw mine card in deck_top (amount=3) THEN discard it mine card in hand [category is follower]
        Aatrox: WHEN played of self DO attach self <The Darkin Blade> | WHEN summoned of self DO heal mine player (amount=2) | WHEN summoned of self IF have mine card in hand [card is World Ender] not DO create in hand <World Ender> | WHEN strikes by self DO heal mine player (amount=2) | WHEN strikes by self IF have mine card in hand [card is World Ender] not DO create in hand <World Ender> | WHEN always IF event_count played by mine player of spell [card is World Ender] ge 1 this_game DO level_up self
    - Spinning Axe -> Gnar: empties your hand
        [runeterra] line now: waits: empties your hand
        Spinning Axe: KW: Burst | WHEN played of self DO discard chosen mine card in hand (amount=1) THEN stat_change chosen mine unit in board (power=1) for this_round
        Gnar: KW: Quick Attack | WHEN strikes by self IF have mine card in hand [card is Pokey Stick] not DO create in hand <Pokey Stick> | WHEN strikes by self IF have mine card in hand [card is Pokey Stick] is DO cost_change mine card in hand [card is Pokey Stick] (cost=-2) for permanent | WHEN round_end IF event_count nexus_damaged of enemy player ge 1 this_round DO level_up self
    - Catalogue of Regrets -> Vayne / Veigar / Senna / Aphelios: empties your hand
        (cards not found by these names)

33. Wrong thinking: any card that makes cards, plays the top card, or is played feeds a card that reacts to "any card played" / "play N cards" / Orange Pellets (every type).
    Rule: L1 (also L19, L1b). Games: Runeterra, Slay the Spire. Files: r5 c3, r5 c4, r2 c8, s1 c1, s1 c9, s1 c10.
    - Annie -> Breakneck Husk: makes more cards to play
        [runeterra] line now: waits: makes more cards to play
        Annie: KW: Attack | WHEN attacks by self DO damage enemy unit in board [state is blocking] (amount=2) THEN damage enemy player (amount=2) | WHEN always IF event_count played by mine player of spell [category in fast_spell] [category in slow_spell] [category in skill] ge 6 this_game DO level_up self | WHEN levels_up of self DO create in hand <Tibbers>
        Breakneck Husk: KW: Immobile, Quick Attack | WHEN played by mine player of all mine unit in board DO kill self THEN stat_change it (power=stat power of (self), health=stat health of (self)) for permanent THEN copy_keywords it to self [state is positive] for permanent
    - Beta -> After Image+: waits: makes more cards to play
        [sts1] line now: waits: makes more cards to play
        Beta: KW: Exhaust | WHEN played of self DO create in deck <Omega>
        After Image+: KW: Innate | WHEN played of mine spell DO give_keyword mine player <Block> (amount=1) for permanent
    - Havoc -> Corruption: waits: is played
        [sts1] line now: waits: is played; waits: is a Skill whose playing sets off its effect
        Havoc: WHEN played of self DO play_card top mine card in deck_top THEN exhaust it
        Corruption: WHEN always DO cost_set all mine card [type is Skill] (cost=0) for while | WHEN played of mine spell [type is Skill] DO exhaust it

34. Wrong thinking: a copy or card put into the deck/hand/play (Nautilus, Dual Wield, Pack Attack, Radiant Standard, Mirror Meld) is a line, though it is by kind or the receiver has no summon/death effect (an Opening Gambit also does not go off from the deck).
    Rule: L19 (also L17). Games: Runeterra, Slay the Spire, Duelyst. Files: r3 c9, r3 c10, r5 c11, s1 c7, u1 c6.
    - Nautilus -> Bull Elnuk: puts: copies it
        [runeterra] line now: puts: copies it
        Nautilus: KW: Tough, Fearsome | WHEN always IF keyword_condition Deep DO level_up self | WHEN levels_up of self DO copy all mine unit in removed [cost ge 4] in deck
        Bull Elnuk: (no rows)
    - Dual Wield -> Body Slam: puts: copies it
        [sts1] line now: puts: copies it
        Dual Wield: WHEN played of self DO copy chosen mine card in hand [type in Attack] [type in Power] in hand
        Body Slam: WHEN played of self DO damage chosen enemy unit in board (amount=count of (mine keyword [keyword is Block]))
    - Radiant Standard -> Futureshaker: puts: puts it into play from the deck
        [duelyst] line now: puts: puts it into play from the deck
        Radiant Standard: WHEN always DO stat_change mine player (power=3) for while | WHEN attacks by mine player DO summon mine card in deck [cost eq 3] to position [position is surrounding]
        Futureshaker: (no rows)

35. Wrong thinking: a summoner/"puts your units into play" feeds a level-up or summon payoff that asks for a specific kind (Tech, multi-region, Mech, Vespyr, 1 or less Attack, action bar) or a stat filter, though the summoned card is not that kind.
    Rule: L20 (also L1b, L17). Games: Faeria, Runeterra, Duelyst. Files: f1 c10, r2 c6, u1 c5, u2 c10, u3 c8.
    - Mother of All Yaks -> Hate Seed: cheaper: puts your units into play
        [faeria] line now: cheaper: puts your units into play
        Mother of All Yaks: WHEN played of self DO summon to chosen position [position is bordering] <Yak Guard> (amount=2, power=4, health=4) THEN give_keyword it <Taunt> for permanent THEN give_keyword it <Flying> for permanent | WHEN always DO cost_change self (cost=minus (event_count of (dies of mine unit [type is yak]) this_game)) for while
        Hate Seed: WHEN always DO cost_change self (cost=minus (event_count of (summoned of mine unit [power gt stat health of (it)]) this_game)) for while
    - Island Navigator -> Heimerdinger: puts your units into play (levels it up)
        [runeterra] line now: levels: puts your units into play (levels it up)
        Island Navigator: KW: Scout | WHEN summoned of self DO summon random mine unit [cost eq 1] [category is follower] in board THEN give_keyword it <Scout> for permanent
        Heimerdinger: KW: Imbue | WHEN played by mine player of spell DO create mine card [name_has is Turret] [keyword is Fleeting] [cost eq stat cost of (it spell)] in hand THEN cost_set it (cost=0) | WHEN always IF event_count summoned of mine unit [type is Tech] power ge 12 this_game DO level_up self
    - Firestarter -> Hideatsu the Ebon Ox: waits: puts your units into play
        [duelyst] line now: waits: puts your units into play
        Firestarter: WHEN played of mine spell DO summon to random position [position is surrounding] <Spellspark> (power=1, health=1) THEN give_keyword it <Rush> for permanent
        Hideatsu the Ebon Ox: WHEN always IF amount distinct cost of (played of mine unit) this_game ge 7 DO can self (event=played) for permanent | WHEN summoned of mine unit DO damage chosen enemy any (amount=stat cost of (it))

36. Wrong thinking: "creates cards" / "fills your hand" is linked where the receiving text does not count made cards, wants a pick, wants another kind, or the cards go to the enemy.
    Rule: L1, L9, L19, L20, L10, L14, L21. Games: Faeria, Runeterra, Slay the Spire, Duelyst. Files: f1 c9, r5 c2, r7 c5, s1 c12, u1 c11 (Alcuin/Blue Conjurer part).
    - Amai Mapdealer -> Gemshell Tortoise: type: creates cards
        [faeria] line now: type: creates cards
        Amai Mapdealer: WHEN played of self DO create in deck <Treasure Map>
        Gemshell Tortoise: WHEN played of self DO draw mine card in deck_top (amount=1) THEN copy it in hand THEN cost_change all mine card in hand [state is created] (cost=-2) for permanent
    - Ashe -> Cunning Kitten: creates cards
        [runeterra] line now: type: creates cards
        Ashe: KW: Attack | WHEN attacks by self DO keyword_action highest enemy unit by power in board <Frostbite> for unstated | WHEN always IF event_count stat_changed by mine player of enemy unit [power eq 0] ge 5 this_game DO level_up self | WHEN levels_up of self DO create mine card in deck_top <Crystal Arrow>
        Cunning Kitten: WHEN summoned of self IF it_matches [state is created] DO draw mine card in deck_top (amount=1) THEN stat_change self (power=2, health=1) for permanent
    - Alcuin Fugitive -> Hideatsu the Ebon Ox: type: creates cards: more different cards to play
        [duelyst] line now: type: creates cards: more different cards to play
        Alcuin Fugitive: WHEN turn_end IF event_count played of mine spell ge 1 this_round DO copy top mine spell in discard in hand
        Hideatsu the Ebon Ox: WHEN always IF amount distinct cost of (played of mine unit) this_game ge 7 DO can self (event=played) for permanent | WHEN summoned of mine unit DO damage chosen enemy any (amount=stat cost of (it))

37. Wrong thinking: waiting for a card added to the deck (Eggs, Ceramic Fish, Darkstone Periapt, Omamori, Master Reality) is fed by cards made in combat or potions, and by the wrong kind.
    Rule: L13, L20. Games: Slay the Spire. Files: s1 c2.
    - Jack of All Trades -> Molten Egg: waits: creates cards
        [sts1] line now: waits: creates cards
        Jack of All Trades: KW: Exhaust | WHEN played of self DO create random card [region is Colorless] in hand (amount=1)
        Molten Egg: WHEN created of mine card in deck [type is Attack] DO keyword_action it <Upgrade> for unstated
    - Hello World -> Omamori: waits: creates cards
        [sts1] line now: waits: creates cards
        Hello World: KW: Innate | WHEN turn_start by mine player DO create random card [rarity is common] in hand
        Omamori: WHEN created of mine card [type is Curse] [n_times] DO counter it
    - Attack Potion -> Darkstone Periapt: waits: creates cards
        [sts1] line now: waits: creates cards
        Attack Potion: WHEN played of self DO choose_card 3 random card [type is Attack] THEN create chosen card in hand THEN cost_set it (cost=0) for this_round
        Darkstone Periapt: WHEN created of mine card [type is Curse] DO stat_change mine player (health=6) for this_run

38. Wrong thinking: a condition in the text (spell filter, "in combat", cost 0, "3 or less Attack", targets a friendly minion) is not checked.
    Rule: L21 (f1: L11; u3: "read like a player"). Games: Duelyst, Runeterra, Faeria. Files: u1 c11, u3 c6, r4 c7, f1 c5 (Blood Obelisk part).
    - Accumulonimbus -> The Scientist: waits: is a spell whose playing sets off its effect
        [duelyst] line now: waits: is a spell whose playing sets off its effect
        Accumulonimbus: WHEN played of self DO summon to position [position is surrounding] <Wind Dervish> (amount=product (2 + event_count of (played of mine card [card is Accumulonimbus]) this_game))
        The Scientist: WHEN played of mine spell [targets is ] DO draw mine card in deck_top (amount=1)
    - Plasma Storm -> Dagona: triggers: kills it for its death effect
        [duelyst] line now: waits: kills it for its death effect
        Plasma Storm: WHEN played of self DO kill all unit in board [power le 3]
        Dagona: KW: Dying Wish, Opening Gambit | WHEN played of self DO capture chosen unit in everywhere | WHEN dies of self DO summon it to position [position is same_space]
    - Nagakabouros' Tantrum -> Lux (level 2): waits: is a spell whose playing sets off its effect
        [runeterra] line now: waits: is a spell whose playing sets off its effect
        Nagakabouros' Tantrum: KW: Focus, Fleeting | WHEN played of self DO summon in board <Nagakabouros' Tentacle> (amount=4) THEN start_attack it mine unit in board
        Lux (level 2): KW: Barrier | WHEN mana_spent by mine player of spell IF amount event_amount ge 6 DO create in hand <Final Spark>

## E. Kills, deaths, sides, drawbacks

39. Wrong thinking: opponent-side triggers (Sentinel cards, Night Watcher, "your opponent casts") are fed by my own spells and summons.
    Rule: L9 (also L5, L21). Games: Duelyst. Files: u1 c4, u2 c1, u2 c2.
    - Lurking Fear -> Xerroloth: waits: is a spell whose playing sets off its effect
        [duelyst] line now: waits: is a spell whose playing sets off its effect
        Lurking Fear: WHEN played of self DO cost_change all mine card in hand [category is unit] [keyword is Dying Wish] (cost=-1) for permanent THEN cost_change all mine card in deck [category is unit] [keyword is Dying Wish] (cost=-1) for permanent
        Xerroloth: KW: Sentinel | WHEN played of spell DO transform self | WHEN played of enemy spell DO create in hand <Fiend> (power=4, health=4) | WHEN always DO give_keyword self <Sentinel> for permanent
    - Firestarter -> Night Watcher: waits: puts units into play
        [duelyst] line now: waits: puts units into play
        Firestarter: WHEN played of mine spell DO summon to random position [position is surrounding] <Spellspark> (power=1, health=1) THEN give_keyword it <Rush> for permanent
        Night Watcher: KW: Forcefield | WHEN summoned of unit in board [keyword is Rush] DO exhaust it
    - Gloomchaser -> Bound Tormentor: waits: puts units into play
        [duelyst] line now: waits: puts units into play
        Gloomchaser: KW: Opening Gambit | WHEN played of self DO summon to random position [position is surrounding] <Wraithling> (power=1, health=1)
        Bound Tormentor: KW: Sentinel | WHEN summoned of unit DO transform self THEN copy it in hand THEN cost_change it (cost=-2) for permanent | WHEN always DO give_keyword self <Sentinel> for permanent

40. Wrong thinking: kills/damage on one side feed a need on the other (enemy-only kills feed my Dying Wish; friendly-only kills feed "enemy dies"; Annie's enemy damage feeds my-unit death effects).
    Rule: L9, L11. Games: Duelyst, Runeterra. Files: u1 c14, u2 c3, u3 c7, r5 c18.
    - Deathmark -> Ironclad: waits: kills it for its death effect
        [duelyst] line now: waits: kills it for its death effect
        Deathmark: WHEN played of self DO damage chosen enemy unit in board (amount=1) THEN give_ability mine player for this_round
        Ironclad: KW: Dying Wish | WHEN dies of self DO silence all enemy unit in board
    - Darkfire Sacrifice -> Grasp of Agony: waits: makes units die (for the ability it gives)
        [duelyst] line now: waits: makes units die (for the ability it gives)
        Darkfire Sacrifice: WHEN played of self DO kill chosen mine unit in board THEN cost_change mine card in hand [category is unit] (cost=-2) for next_card
        Grasp of Agony: WHEN played of self DO give_ability chosen enemy unit in board
    - Annie -> Blades of the Fallen: makes units die (for the ability it gives)
        [runeterra] line now: waits: makes units die (for the ability it gives)
        Annie: KW: Attack | WHEN attacks by self DO damage enemy unit in board [state is blocking] (amount=2) THEN damage enemy player (amount=2) | WHEN always IF event_count played by mine player of spell [category in fast_spell] [category in slow_spell] [category in skill] ge 6 this_game DO level_up self | WHEN levels_up of self DO create in hand <Tibbers>
        Blades of the Fallen: WHEN played of self DO give_ability chosen mine unit in board for this_round

41. Wrong thinking: damage to the General is read as damage to the minion.
    Rule: L7. Games: Duelyst. Files: u1 c2.
    - Flameblood Warlock -> Lantern Fox: waits: damages it for its effect
        [duelyst] line now: waits: damages it for its effect
        Flameblood Warlock: KW: Opening Gambit | WHEN played of self DO damage all player (amount=3)
        Lantern Fox: WHEN damaged of self DO create in hand <Phoenix Fire>
    - Elucidator -> Juggernaut: waits: damages it for its effect
        [duelyst] line now: waits: damages it for its effect
        Elucidator: KW: Rush, Opening Gambit | WHEN played of self DO damage mine player (amount=4)
        Juggernaut: WHEN turn_start by mine player DO stat_change self (power=5, health=5) for permanent | WHEN damaged of self DO summon random unit in board [type is Golem] [name_has is Egg] to chosen position [position is surrounding] (amount=event_amount)
    - Dark Nemesis -> Deathstrike Seal: waits: damages units or players (for the ability it gives)
        [duelyst] line now: waits: damages units or players (for the ability it gives)
        Dark Nemesis: WHEN turn_start by mine player DO damage enemy player (amount=4) THEN stat_change self (power=4) for permanent
        Deathstrike Seal: WHEN played of self DO give_ability chosen mine unit in board

42. Wrong thinking: a plain hit on one target, removal, or ordinary attack damage feeds my own Last Words/death effect or "whenever an enemy dies".
    Rule: L11 (also L9, L21, L2). Games: Faeria, Slay the Spire, Duelyst. Files: f2 c11, s1 c6, u3 c5.
    - Flame Burst -> Imperial Guard: waits: kills it for its death effect
        [faeria] line now: waits: kills it for its death effect
        Flame Burst: WHEN played of self DO damage chosen anything (amount=3)
        Imperial Guard: KW: Taunt | WHEN always DO give_keyword self <Taunt> for permanent | WHEN dies of self DO heal mine player (amount=2)
    - Anger, Bash, Bite, Claw, Clothesline, Dash, Dagger Throw -> Gremlin Horn: waits: makes enemy units die
        (cards not found by these names)
    - Daemonic Lure -> Grasp of Agony: triggers: makes units die (for the ability it gives)
        [duelyst] line now: waits: makes units die (for the ability it gives)
        Daemonic Lure: WHEN played of self DO damage chosen enemy unit in board (amount=1) THEN move it to position
        Grasp of Agony: WHEN played of self DO give_ability chosen enemy unit in board

43. Wrong thinking: text that kills nothing, or kills something else (a well, a deck, a landmark; Snecko Skull; Earthfire Shaker counting only its own Gift), is read as a kill.
    Rule: L1, L3, L11, L9, L10. Games: Faeria, Slay the Spire, Runeterra. Files: f1 c5, f2 c10, s2 c5, r7 c9.
    - Solem -> Annoying Gnat: waits: kills it for its death effect
        [faeria] line now: waits: kills it for its death effect
        Solem: KW: Flying, Divine, Corrupt | WHEN always DO give_keyword self <Flying> for permanent THEN give_keyword self <Divine> for permanent | WHEN moves_onto of self [position is same_space] [once_per_game] DO kill chosen position [terrain is resource_well]
        Annoying Gnat: KW: Flying | WHEN always DO give_keyword self <Flying> for permanent | WHEN always DO cant self (event=harvests) for while | WHEN dies of self DO damage mine player (amount=2) THEN summon to random position <Annoying Gnat>
    - Void Guardian -> Village Elder: waits: kills it for its death effect
        [faeria] line now: waits: kills it for its death effect
        Void Guardian: WHEN played of self DO kill all mine card in deck
        Village Elder: WHEN dies of self DO draw mine card in deck_top (amount=1)
    - Snecko Skull -> Corpse Explosion: triggers: makes enemy units die
        [sts1] line now: waits: makes enemy units die
        Snecko Skull: WHEN given_keyword by mine player of enemy unit [keyword is Poison] DO give_keyword it <Poison> (amount=1) for permanent
        Corpse Explosion: WHEN played of self DO give_keyword chosen enemy unit in board <Poison> (amount=6) for permanent | WHEN dies of enemy unit DO damage all enemy unit in board (amount=stat health of (it))

44. Wrong thinking: a drawback (Last Words that helps the opponent, a status card that only hurts, a Play that curses itself, damage that helps the enemy) is linked as a need.
    Rule: L5 (f1 Hunted Outlaw; u2 also L9). Games: Faeria, Slay the Spire, Runeterra, Duelyst. Files: f1 c5, f2 c12, s2 c2, r3 c13, u2 c4.
    - Doom Scythe -> Hunted Outlaw: waits: kills it for its death effect
        [faeria] line now: waits: kills it for its death effect
        Doom Scythe: WHEN played of self DO kill chosen unit in board THEN summon to position [position is same_space] <Slaughtering Shadow> (power=6, health=1)
        Hunted Outlaw: WHEN dies of self DO draw enemy card in deck_top (amount=1) THEN mana_gain enemy player (amount=2)
    - Overclock -> Burn: puts it into play: creates
        [sts1] line now: NONE
        Overclock: WHEN played of self DO draw mine card in deck_top (amount=2) THEN create in discard <Burn>
        Burn: WHEN always DO cant self (event=played) for while | WHEN turn_end by mine player DO damage mine player (amount=unstated)
    - Riftwalker -> Haruspex: waits: damages it for its effect
        [duelyst] line now: waits: damages it for its effect
        Riftwalker: KW: Airdrop | WHEN played of self DO damage all any [position is surrounding] (amount=product (1 + event_count of (played of mine card [card is Riftwalker]) this_game))
        Haruspex: WHEN damaged of self DO draw enemy card in deck_top (amount=1)

45. Wrong thinking: text that does not exist is read as self-death, a keyword giver, or a given ability.
    Rule: L1. Games: Faeria. Files: f1 c11, f4 c5.
    - Baeru, the First Wave -> Bone Collector: waits: dies by its own effect
        [faeria] line now: waits: dies by its own effect
        Baeru, the First Wave: KW: Aquatic, Production | WHEN always DO give_keyword self <Aquatic> for permanent | WHEN turn_start by mine player DO set_terrain all position [terrain is land] [position is bordering] to position [terrain is lake]
        Bone Collector: WHEN dies of all unit in board [position is bordering] DO stat_change self (power=1, health=1) for permanent
    - Seed of Paradise -> Imperial Engineer: type: makes your units get Production
        [faeria] line now: type: makes your units get Production
        Seed of Paradise: KW: Flying, Dash | WHEN always DO give_keyword self <Flying> for permanent THEN give_keyword self <Dash> (amount=1) for permanent | WHEN played of self DO choose_one (options=4) OR give_ability self OR give_ability self OR give_ability self OR give_ability self
        Imperial Engineer: WHEN played of self DO repeat all mine unit_or_structure [keyword is Production]
    - Grappling Hook -> Imperial Engineer: enables: makes your units get Production
        [faeria] line now: type: makes your units get Production
        Grappling Hook: WHEN played of self DO give_keyword chosen unit in board <Ranged Attack> for this_round THEN give_ability it
        Imperial Engineer: WHEN played of self DO repeat all mine unit_or_structure [keyword is Production]

46. Wrong thinking: what every turn or every unit does (own summon, self-summon, turn end) is read as a trigger.
    Rule: L1. Games: Faeria, Runeterra. Files: f1 c14, r7 c8.
    - Doomsday -> Compass of Gagana: waits: makes this happen: your turn ends
        [faeria] line now: waits: makes this happen: your turn ends
        Doomsday: WHEN played of self DO stat_set mine mana (amount=0) THEN stat_set mine player (health=half (stat health of (mine player))) THEN kill all unit_or_structure THEN end_turn
        Compass of Gagana: WHEN turn_end by mine player DO put_on_top mine card in deck [card is Treasure Map] THEN create in deck <Treasure Map>
    - Jarvan IV -> Fleetfeather Tracker: triggers: puts your units into play
        [runeterra] line now: waits: puts your units into play
        Jarvan IV: KW: Barrier | WHEN attacks by mine player DO spend_mana mine mana (amount=stat cost of (self)) THEN summon self THEN challenge highest enemy unit by power in board to self | WHEN always IF event_count survives_damage by enemy unit [state is blocking] of mine unit ge 3 this_game DO level_up self
        Fleetfeather Tracker: WHEN summoned by mine player of it mine unit [card not Fleetfeather Tracker] DO give_keyword self <Challenger> for permanent

## F. Wording, direction, duplicates

47. Wrong thinking: the same reason is said two or three times for one pair (type + waits, triggers + helps it level up, movement rules joined).
    Rule: L10 (also L18). Games: all four. Files: f2 c5, f4 c8, r4 c2, r5 c13, r6 c6, s1 c8, s2 c6, u1 c17, u2 c14, u3 c10 (last part).
    - Celestial Tower -> Imperial Drakerider: triggers: moves it for its effect; also moves into place: moves my units or land forward: they reach enemy ground; also moves into place: moves it where it must be
        [faeria] line now: waits: moves it for its effect; moves: moves my units or land forward: they reach enemy ground; moves: moves it where it must be
        Celestial Tower: WHEN activated DO give_keyword chosen unit in board <Charge> (amount=3) for this_round THEN damage self (amount=1)
        Imperial Drakerider: KW: Flying, Charge, Corrupt | WHEN always DO give_keyword self <Flying> for permanent THEN give_keyword self <Charge> (amount=2) for permanent | WHEN moves_onto of self [position is same_space] [once_per_game] DO stat_change self (power=2, health=2) for permanent
    - Thunderclap -> Champion Belt: type: makes enemy units get Vulnerable / waits: makes enemy units get Vulnerable
        [sts1] line now: type: makes enemy units get Vulnerable; waits: makes enemy units get Vulnerable
        Thunderclap: WHEN played of self DO damage all enemy unit in board (amount=4) THEN give_keyword all enemy unit in board <Vulnerable> (amount=1) for permanent
        Champion Belt: WHEN given_keyword by mine player of enemy unit [keyword is Vulnerable] DO give_keyword it <Weak> (amount=1) for permanent
    - Chassis of MECHAZ0R -> Echo Deliverant: waits: is a Mech whose summoning sets off its effect, AND waits: puts your units into play
        [duelyst] line now: waits: is a Mech whose summoning sets off its effect; waits: puts your units into play
        Chassis of MECHAZ0R: KW: Forcefield, Opening Gambit | WHEN played of self DO keyword_action <MECHAZ0R> (amount=20)
        Echo Deliverant: WHEN summoned of mine unit in board [type is Mech] [card not Echo Deliverant] DO copy it to chosen position [position is surrounding] in board

48. Wrong thinking: the reason words do not match what the card does (wrong kind: triggers vs makes cheaper, summon vs plant, heal vs repair, stat word vs movement, replace vs shuffle, landmark vs units).
    Rule: L10 (also L8, L12, L13). Games: all four. Files: f3 c5, f4 c7, r5 c16, r5 c23, r6 c7, r7 c9, u1 c12 (Replace wording), u1 c18, u3 c10, s1 c5 (words "units"), u2 c14.
    - Mirror Phantasm -> Windstorm Archer: clears the way: clears its line of fire
        [faeria] line now: clears: clears its line of fire
        Mirror Phantasm: WHEN played of self DO transform chosen unit in board [card not Mirror Phantasm] <Mirror Phantasm> (power=5, health=5)
        Windstorm Archer: KW: Ranged Attack | WHEN always DO give_keyword self <Ranged Attack> for permanent | WHEN played of mine spell DO stat_change self (power=1) for this_round
    - Topaz Yak -> Mother of All Yaks: triggers: is a yak it counts when dies
        [faeria] line now: waits: is a yak it counts when dies
        Topaz Yak: WHEN always DO can self to position [position is bordering] (event=summoned) for while | WHEN played of self IF have all mine unit in board [type is yak] [position is bordering] is DO give_keyword self <Haste> for permanent
        Mother of All Yaks: WHEN played of self DO summon to chosen position [position is bordering] <Yak Guard> (amount=2, power=4, health=4) THEN give_keyword it <Taunt> for permanent THEN give_keyword it <Flying> for permanent | WHEN always DO cost_change self (cost=minus (event_count of (dies of mine unit [type is yak]) this_game)) for while
    - Manasoul Student -> Annie: helps it level up: is played (levels it up)
        [runeterra] line now: levels: is played (levels it up)
        Manasoul Student: WHEN played by mine player of spell [category in fast_spell] [category in slow_spell] [category in skill] [first_each_round] DO play_card <Magic Embers>
        Annie: KW: Attack | WHEN attacks by self DO damage enemy unit in board [state is blocking] (amount=2) THEN damage enemy player (amount=2) | WHEN always IF event_count played by mine player of spell [category in fast_spell] [category in slow_spell] [category in skill] ge 6 this_game DO level_up self | WHEN levels_up of self DO create in hand <Tibbers>

49. Wrong thinking: "puts it into play" is said for a card only put into hand, draw pile or discard pile.
    Rule: L10. Games: Slay the Spire. Files: s2 c1.
    - Blade Dance -> Shiv: puts it into play: creates
        [sts1] line now: NONE
        Blade Dance: WHEN played of self DO create in hand <Shiv> (amount=3)
        Shiv: (no rows)
    - Scrape -> Claw: puts it into play: draws it and keeps it
        [sts1] line now: puts: draws it and keeps it
        Scrape: WHEN played of self DO damage chosen enemy unit in board (amount=7) THEN draw mine card in deck_top (amount=4) THEN discard it mine card [cost gt 0]
        Claw: WHEN played of self DO damage chosen enemy unit in board (amount=3) THEN increase_effect all mine card [card is Claw] (amount=2) for permanent
        case nst29: expect line keeps it (Claude (audit): Scrape keeps the 0-cost cards it draws)
    - All for One -> Overclock: puts it into play: brings it back to your hand
        [sts1] line now: puts: brings it back to your hand
        All for One: WHEN played of self DO damage chosen enemy unit in board (amount=10) THEN return_card all mine card in discard [cost eq 0] in hand
        Overclock: WHEN played of self DO draw mine card in deck_top (amount=2) THEN create in discard <Burn>

50. Wrong thinking: the link direction is wrong (helper said to need what it helps; A named by B instead of B by A).
    Rule: L6, L14 (r5: none stated). Games: Faeria, Runeterra. Files: f3 c4, r5 c14, f1 c4 (Defender), u2 c12 (Scion's Third Wish -> Duskweaver note).
    - Ninja Toad -> Triton Trainer: enables: has Jump
        [faeria] line now: type: has Jump
        Ninja Toad: KW: Jump, Haste | WHEN always DO give_keyword self <Jump> for permanent THEN give_keyword self <Haste> for permanent
        Triton Trainer: KW: Jump | WHEN always DO give_keyword self <Jump> for permanent | WHEN played of self DO give_ability mine player
    - Battle Toads -> Triton Trainer: enables: makes your units get Jump
        [faeria] line now: type: makes your units get Jump; waits: puts units into play (for the ability it gives)
        Battle Toads: WHEN played of self DO summon <Frog> (amount=2, power=2, health=2) THEN give_keyword it <Jump> for permanent
        Triton Trainer: KW: Jump | WHEN always DO give_keyword self <Jump> for permanent | WHEN played of self DO give_ability mine player
    - Warlord's Palace -> Akshan: is the A it names
        [runeterra] line now: type: is a landmark it counts; type: is a landmark or structure it asks for; type: is the Warlord's Palace it names
        Warlord's Palace: KW: Countdown, Landmark | WHEN countdown_done of self DO create in hand <Relic of Power> | WHEN targeted by mine player of mine unit DO countdown_advance self (amount=1)
        Akshan: KW: Quick Attack | WHEN summoned of self IF have mine landmark [card is Warlord's Palace] not DO summon in board <Warlord's Palace> | WHEN summoned of self IF have mine landmark [card is Warlord's Palace] is DO countdown_advance mine landmark [card is Warlord's Palace] (amount=1) | WHEN strikes by self IF have mine landmark [card is Warlord's Palace] not DO summon in board <Warlord's Palace> | WHEN strikes by self IF have mine landmark [card is Warlord's Palace] is DO countdown_advance mine landmark [card is Warlord's Palace] (amount=1) | WHEN always IF event_count countdown_done of mine landmark [card is Warlord's Palace] ge 1 this_game DO level_up self | WHEN levels_up of self DO summon in board <Warlord's Hoard>

51. Wrong thinking: reasons that do not match B's text at all (Catalogue discard, Lee Sin -> Legion General, Ambush "hit the enemy player", Arena Bookie -> Samira).
    Rule: L1, L7, L10. Games: Runeterra. Files: r2 c7.
    - Catalogue of Regrets -> Ancient Warmonger: makes you discard cards
        [runeterra] line now: waits: makes you discard cards
        Catalogue of Regrets: KW: Landmark | WHEN round_start DO copy random mine spell in everywhere [keyword not Fleeting] [state is played_last_round] in hand THEN give_keyword it mine spell in hand <Fleeting> for permanent
        Ancient Warmonger: KW: Overwhelm | WHEN discarded of self DO stat_change highest mine unit by power in board (power=2) for permanent
    - Lee Sin -> Legion General: has Barrier
        [runeterra] line now: type: has Barrier; type: has Challenger
        Lee Sin: KW: Imbue | WHEN played by mine player of spell DO give_keyword self <Challenger> for this_round | WHEN played by mine player of spell IF event_count played by mine player of spell ge 2 this_round DO give_keyword self <Barrier> for this_round | WHEN always IF event_count played by mine player of spell ge 8 this_game DO level_up self
        Legion General: KW: Fearsome | WHEN summoned of self DO stat_change self (power=sum (event_count of (given_keyword by mine player of unit) this_game + event_count of (recalled by mine player of unit) this_game), health=sum (event_count of (given_keyword by mine player of unit) this_game + event_count of (recalled by mine player of unit) this_game)) for permanent
    - Arena Bookie -> Samira (level 2): empties your hand
        [runeterra] line now: waits: empties your hand
        Arena Bookie: WHEN round_start DO discard lowest_cost mine card in hand (amount=1) THEN draw mine card in deck_top (amount=1)
        Samira (level 2): KW: Quick Attack, Plunder | WHEN played of self IF keyword_condition Plunder; have mine card in hand [card is Flair] not DO create in hand <Flair> | WHEN strikes by self IF have mine card in hand [card is Flair] not DO create in hand <Flair> | WHEN played by mine player IF event_count played by mine player ge 6 this_game DO gain_attack_token mine player

## G. Single-game cards and misreadings

52. Out-of-combat healing (rest sites, shops, pickups) feeds Magic Flower, and the player is called "units".
    Rule: L13, L12. Games: Slay the Spire. Files: s1 c5.
    - Eternal Feather -> Magic Flower: waits: heals your units
        [sts1] line now: waits: heals your units
        Eternal Feather: WHEN run_event DO heal mine player (amount=3) | WHEN run_event DO run_rule mine player
        Magic Flower: WHEN healed of mine player DO heal mine player (amount=half (event_amount))
    - Meal Ticket -> Magic Flower: waits: heals your units
        [sts1] line now: waits: heals your units
        Meal Ticket: WHEN run_event DO heal mine player (amount=15)
        Magic Flower: WHEN healed of mine player DO heal mine player (amount=half (event_amount))
    - Lee's Waffle -> Magic Flower: waits: heals your units
        [sts1] line now: waits: heals your units
        Lee's Waffle: WHEN played of self DO stat_change mine player (health=7) for this_run THEN heal mine player (amount=full)
        Magic Flower: WHEN healed of mine player DO heal mine player (amount=half (event_amount))

53. A card's own Exhaust keyword feeds Sentinel ("If THIS card is Exhausted").
    Rule: L7. Games: Slay the Spire. Files: s1 c3.
    - Slimed -> Sentinel: waits: exhausts cards
        [sts1] line now: waits: exhausts cards
        Slimed: KW: Exhaust
        Sentinel: WHEN played of self DO give_keyword mine player <Block> (amount=5) for permanent | WHEN exhausted of self DO mana_gain mine mana (amount=2)
    - Reaper -> Sentinel: waits: exhausts cards
        [sts1] line now: waits: exhausts cards
        Reaper: KW: Exhaust | WHEN played of self DO damage all enemy unit in board (amount=4) THEN heal mine player (amount=event_amount)
        Sentinel: WHEN played of self DO give_keyword mine player <Block> (amount=5) for permanent | WHEN exhausted of self DO mana_gain mine mana (amount=2)
    - Exhume -> Sentinel: waits: exhausts cards
        [sts1] line now: waits: exhausts cards
        Exhume: KW: Exhaust | WHEN played of self DO return_card chosen mine card in exhausted in hand
        Sentinel: WHEN played of self DO give_keyword mine player <Block> (amount=5) for permanent | WHEN exhausted of self DO mana_gain mine mana (amount=2)

54. Kalista (level 2) read wrongly (bond as need for damage, revive linked to champions, revived attacker as another attack).
    Rule: L7, L4, L20. Games: Runeterra. Files: r1 c9.
    - Kalista (level 2) <- Absorb Soul: damages units or players (for the ability it gives)
    - Kalista (level 2) -> Ahri (level 2): makes it attack for its effect
        [runeterra] line now: waits: makes it attack for its effect
        Kalista (level 2): KW: Fearsome | WHEN attacks by self [first_each_round] DO revive highest mine unit by power in discard [category is follower] THEN give_keyword it <Ephemeral> for permanent THEN start_attack it THEN give_ability self for this_round
        Ahri (level 2): KW: Quick Attack, Elusive, Attack | WHEN recalled by mine player of mine unit DO cost_change it (cost=-1) for permanent | WHEN attacks by self DO give_ability self for this_round
    - Kalista (level 2) -> Quinn: another attack
        [runeterra] line now: levels: another attack (levels it up); type: another attack
        Kalista (level 2): KW: Fearsome | WHEN attacks by self [first_each_round] DO revive highest mine unit by power in discard [category is follower] THEN give_keyword it <Ephemeral> for permanent THEN start_attack it THEN give_ability self for this_round
        Quinn: KW: Scout | WHEN summoned of self DO summon in board <Valor> | WHEN always IF event_count attacks by mine player ge 4 this_game DO level_up self

55. Moving an ally to the deck (Bone Skewer top, Sugary Snare bottom) is read as moving toward the Nexus.
    Rule: L4. Games: Runeterra. Files: r1 c10.
    - Bone Skewer -> Darius: levels: moves it within reach of the enemy player (levels it up)
        [runeterra] line now: levels: moves it within reach of the enemy player (levels it up)
        Bone Skewer: WHEN played of self DO strike chosen mine unit in board to chosen enemy unit in board THEN move it in deck_top
        Darius: KW: Overwhelm | WHEN always IF stat enemy player health le half base_health of (enemy player) DO level_up self
        case n12: expect line  (Kaptain: Nexus damage levels Darius)
    - Sugary Snare -> Snowy Razorclaw: moves it within reach of the enemy player
        [runeterra] line now: moves: moves it within reach of the enemy player
        Sugary Snare: WHEN played of self DO move chosen mine unit in board in deck_bottom THEN summon top mine card in deck [category is unit]
        Snowy Razorclaw: KW: Overwhelm, Plunder | WHEN played of self IF keyword_condition Plunder DO stat_set chosen mine unit in board (power=stat power of (self), health=stat health of (self))
    - Bone Skewer -> Dashing Dandy: moves it within reach of the enemy player
        [runeterra] line now: moves: moves it within reach of the enemy player
        Bone Skewer: WHEN played of self DO strike chosen mine unit in board to chosen enemy unit in board THEN move it in deck_top
        Dashing Dandy: KW: Plunder, Overwhelm | WHEN played of self IF keyword_condition Plunder DO stat_change self (power=stat power of (self)) for permanent

56. Wrong doer: Challenger choosing a blocker is read as making enemy units block for Annie/Captive Greyback/Ziggs/Taliyah blocker-hit cards.
    Rule: L7. Games: Runeterra. Files: r3 c5, r2 c7 (Lee Sin -> Threaded Volley).
    - Laurent Protege -> Obeyed Order: type: makes enemy units block: Obeyed Order damages them
        [runeterra] line now: type: makes enemy units block: Obeyed Order damages them
        Laurent Protege: KW: Challenger
        Obeyed Order: KW: Skill | WHEN played of self DO damage chosen enemy unit in board [state is blocking] (amount=3) THEN damage enemy player (amount=3)
    - Trifarian Gloryseeker -> Threaded Volley: type: makes enemy units block: Threaded Volley damages them
        [runeterra] line now: type: makes enemy units block: Threaded Volley damages them
        Trifarian Gloryseeker: KW: Challenger, Can't Block
        Threaded Volley: KW: Elemental Skill | WHEN played of self DO damage it enemy unit [state is blocking] (amount=2) THEN damage enemy player (amount=2)
    - Lee Sin -> Threaded Volley: makes enemy units block: B damages them
        [runeterra] line now: type: makes enemy units block: Threaded Volley damages them
        Lee Sin: KW: Imbue | WHEN played by mine player of spell DO give_keyword self <Challenger> for this_round | WHEN played by mine player of spell IF event_count played by mine player of spell ge 2 this_round DO give_keyword self <Barrier> for this_round | WHEN always IF event_count played by mine player of spell ge 8 this_game DO level_up self
        Threaded Volley: KW: Elemental Skill | WHEN played of self DO damage it enemy unit [state is blocking] (amount=2) THEN damage enemy player (amount=2)

57. Challenger is read as targeting (for Ezreal).
    Rule: L15. Games: Runeterra. Files: r3 c6 (r5 unsure Braum -> Ezreal).
    - Laurent Protege -> Ezreal: levels: targets enemy cards (levels it up)
        [runeterra] line now: levels: targets enemy cards (levels it up)
        Laurent Protege: KW: Challenger
        Ezreal: KW: Elusive | WHEN strikes_nexus by self DO create in hand <Mystic Shot> THEN give_keyword it mine card in hand <Fleeting> for permanent | WHEN always IF event_count targeted by mine player of enemy unit ge 8 this_game DO level_up self
    - Fiora (level 2) -> Ezreal: levels: targets enemy cards (levels it up)
        [runeterra] line now: levels: targets enemy cards (levels it up)
        Fiora (level 2): KW: Challenger | WHEN always IF event_count killed by self of enemy unit ge 4 this_game DO win_game mine player
        Ezreal: KW: Elusive | WHEN strikes_nexus by self DO create in hand <Mystic Shot> THEN give_keyword it mine card in hand <Fleeting> for permanent | WHEN always IF event_count targeted by mine player of enemy unit ge 8 this_game DO level_up self
    - Trifarian Gloryseeker -> Ezreal: levels: targets enemy cards (levels it up)
        [runeterra] line now: levels: targets enemy cards (levels it up)
        Trifarian Gloryseeker: KW: Challenger, Can't Block
        Ezreal: KW: Elusive | WHEN strikes_nexus by self DO create in hand <Mystic Shot> THEN give_keyword it mine card in hand <Fleeting> for permanent | WHEN always IF event_count targeted by mine player of enemy unit ge 8 this_game DO level_up self

58. A faction/tribe/cost/stat filter is treated as narrower than a deck ("another Noxus ally", 1 cost ally, higher Attack than Life).
    Rule: L14, L17, L21. Games: Runeterra, Faeria. Files: r3 c8, r5 c12, f4 c6.
    - Reckless Trifarian -> Trifarian Hopeful: type: is a unit it asks for
        [runeterra] line now: type: is a unit it asks for
        Reckless Trifarian: KW: Can't Block
        Trifarian Hopeful: WHEN summoned of self IF have all mine unit in board [card not Trifarian Hopeful] [region is Noxus] is DO stat_change self (power=2) for permanent
    - Kinkou Wayfinder -> Annie: puts it into play from the deck
        [runeterra] line now: puts: puts it into play from the deck
        Kinkou Wayfinder: KW: Allegiance | WHEN summoned of self IF keyword_condition Allegiance DO summon random mine unit in deck [cost eq 1] in board
        Annie: KW: Attack | WHEN attacks by self DO damage enemy unit in board [state is blocking] (amount=2) THEN damage enemy player (amount=2) | WHEN always IF event_count played by mine player of spell [category in fast_spell] [category in slow_spell] [category in skill] ge 6 this_game DO level_up self | WHEN levels_up of self DO create in hand <Tibbers>
    - Demon Wrangler -> Firebringer: triggers: puts your units into play
        [faeria] line now: waits: puts your units into play
        Demon Wrangler: WHEN played of self DO sacrifice chosen mine unit in board [card not Demon Wrangler] THEN summon to position [position is same_space] <Demon Wing> (power=5, health=2) THEN give_keyword it <Flying> for permanent
        Firebringer: WHEN summoned of mine unit [power gt stat health of (it)] DO stat_change self (power=1, health=1) for permanent

59. Grandmaster at Arms (an Origin, a deckbuilding rule) is counted as a played spell and Jax "casts" it.
    Rule: none stated. Games: Runeterra. Files: r3 c11.
    - Grandmaster at Arms -> Annie: levels: is a spell it needs played for its count (levels it up)
        [runeterra] line now: levels: is a spell it needs played for its count (levels it up)
        Grandmaster at Arms: (no rows)
        Annie: KW: Attack | WHEN attacks by self DO damage enemy unit in board [state is blocking] (amount=2) THEN damage enemy player (amount=2) | WHEN always IF event_count played by mine player of spell [category in fast_spell] [category in slow_spell] [category in skill] ge 6 this_game DO level_up self | WHEN levels_up of self DO create in hand <Tibbers>
    - Grandmaster at Arms -> The Prefect: waits: is a spell whose playing sets off its effect
        [runeterra] line now: waits: is a spell whose playing sets off its effect
        Grandmaster at Arms: (no rows)
        The Prefect: KW: Overwhelm | WHEN played by mine player of spell [category in fast_spell] [category in slow_spell] [category in skill] DO stat_change self (power=1) for permanent
    - Jax -> Grandmaster at Arms: puts: casts its skill
        [runeterra] line now: puts: casts its skill
        Jax: WHEN played of self DO attach self <The Light of Icathia> | WHEN always IF event_count attacks by mine unit [state is equipped] power ge 16 this_game DO level_up self
        Grandmaster at Arms: (no rows)

60. A unit summoned for the opponent is linked as mine.
    Rule: L9. Games: Runeterra. Files: r3 c12.
    - Stalking Wolf -> Snow Hare: puts: summons
        [runeterra] line now: puts: summons
        Stalking Wolf: KW: Challenger | WHEN summoned of self DO summon in board <Snow Hare>
        Snow Hare: (no rows)

61. Flashbomb Trap (planted in the enemy deck) is read as hitting my side.
    Rule: L9, L7. Games: Runeterra. Files: r5 c5 (r2 unsure).
    - Caitlyn -> Kalista: through Flashbomb Trap: makes your units die (levels it up)
        [runeterra] line now: levels: through Flashbomb Trap: makes your units die (levels it up)
        Caitlyn: KW: Quick Attack | WHEN strikes by self DO keyword_action 8 enemy card in deck_top <Flashbomb Trap Plant> (amount=2) | WHEN always IF event_count trap_activated of card [keyword is Trap] ge 5 this_game DO level_up self
        Kalista: KW: Fearsome | WHEN always IF event_count dies of mine unit ge 3 this_game DO level_up self
    - Caitlyn -> Vladimir: through Flashbomb Trap: damages your units without killing them (levels it up)
        [runeterra] line now: levels: through Flashbomb Trap: damages your units without killing them (levels it up)
        Caitlyn: KW: Quick Attack | WHEN strikes by self DO keyword_action 8 enemy card in deck_top <Flashbomb Trap Plant> (amount=2) | WHEN always IF event_count trap_activated of card [keyword is Trap] ge 5 this_game DO level_up self
        Vladimir: KW: Fearsome | WHEN played of self DO damage count of (chosen mine unit in board) chosen mine unit in board (amount=1) THEN damage chosen enemy unit in board (amount=event_amount) | WHEN always IF event_count survives_damage of mine unit ge 5 this_game DO level_up self
    - Caitlyn -> Braum: through Flashbomb Trap: damages it without killing it, for its effect (levels it up)
        [runeterra] line now: levels: through Flashbomb Trap: damages it without killing it, for its effect (levels it up)
        Caitlyn: KW: Quick Attack | WHEN strikes by self DO keyword_action 8 enemy card in deck_top <Flashbomb Trap Plant> (amount=2) | WHEN always IF event_count trap_activated of card [keyword is Trap] ge 5 this_game DO level_up self
        Braum: KW: Challenger, Regeneration | WHEN survives_damage of self [once_per_game] DO summon in board <Mighty Poro> | WHEN always IF event_count survives_damage of self damage ge 10 this_game DO level_up self

62. "Mecha Yordle" is read as "Yordle" (Gnar is not a Mecha).
    Rule: none stated. Games: Runeterra. Files: r5 c10.
    - Gnar -> Skrappy's Partsapalooza: is a Mecha whose summoning sets off its effect
        [runeterra] line now: type: is a Yordle it asks for; waits: is a Mecha whose summoning sets off its effect
        Gnar: KW: Quick Attack | WHEN strikes by self IF have mine card in hand [card is Pokey Stick] not DO create in hand <Pokey Stick> | WHEN strikes by self IF have mine card in hand [card is Pokey Stick] is DO cost_change mine card in hand [card is Pokey Stick] (cost=-2) for permanent | WHEN round_end IF event_count nexus_damaged of enemy player ge 1 this_round DO level_up self
        Skrappy's Partsapalooza: KW: Landmark | WHEN discarded of self DO summon self | WHEN summoned by mine player of mine unit [type is Mecha] [type is Yordle] DO give_random_keyword it (amount=1) for permanent
    - Gnar -> Rumble (level 2): is a Yordle it asks for
        [runeterra] line now: type: is a Yordle it asks for
        Gnar: KW: Quick Attack | WHEN strikes by self IF have mine card in hand [card is Pokey Stick] not DO create in hand <Pokey Stick> | WHEN strikes by self IF have mine card in hand [card is Pokey Stick] is DO cost_change mine card in hand [card is Pokey Stick] (cost=-2) for permanent | WHEN round_end IF event_count nexus_damaged of enemy player ge 1 this_round DO level_up self
        Rumble (level 2): KW: Quick Attack, SpellShield, Impact | WHEN nexus_damaged by mine player of enemy player IF have mine card in hand [type is Mecha] [type is Yordle] not DO create random mine card [type is Mecha] [type is Yordle] in hand | WHEN nexus_damaged by mine player of enemy player IF have mine card in hand [type is Mecha] [type is Yordle] is DO stat_change all mine card in hand [type is Mecha] [type is Yordle] (power=1, health=1) for permanent THEN cost_change all mine card in hand [type is Mecha] [type is Yordle] (cost=-1) for permanent
    - Rumble (level 2) -> Gnar: makes it cheaper
        [runeterra] line now: levels: damages the enemy player (levels it up); stronger: gives it more power and health; cheaper: makes it cheaper
        Rumble (level 2): KW: Quick Attack, SpellShield, Impact | WHEN nexus_damaged by mine player of enemy player IF have mine card in hand [type is Mecha] [type is Yordle] not DO create random mine card [type is Mecha] [type is Yordle] in hand | WHEN nexus_damaged by mine player of enemy player IF have mine card in hand [type is Mecha] [type is Yordle] is DO stat_change all mine card in hand [type is Mecha] [type is Yordle] (power=1, health=1) for permanent THEN cost_change all mine card in hand [type is Mecha] [type is Yordle] (cost=-1) for permanent
        Gnar: KW: Quick Attack | WHEN strikes by self IF have mine card in hand [card is Pokey Stick] not DO create in hand <Pokey Stick> | WHEN strikes by self IF have mine card in hand [card is Pokey Stick] is DO cost_change mine card in hand [card is Pokey Stick] (cost=-2) for permanent | WHEN round_end IF event_count nexus_damaged of enemy player ge 1 this_round DO level_up self

63. Akshan only advances Warlord's Palace but is linked to every Countdown landmark.
    Rule: L1. Games: Runeterra. Files: r5 c15.
    - Akshan -> Dragon Roost: finishes countdowns
        [runeterra] line now: waits: finishes countdowns
        Akshan: KW: Quick Attack | WHEN summoned of self IF have mine landmark [card is Warlord's Palace] not DO summon in board <Warlord's Palace> | WHEN summoned of self IF have mine landmark [card is Warlord's Palace] is DO countdown_advance mine landmark [card is Warlord's Palace] (amount=1) | WHEN strikes by self IF have mine landmark [card is Warlord's Palace] not DO summon in board <Warlord's Palace> | WHEN strikes by self IF have mine landmark [card is Warlord's Palace] is DO countdown_advance mine landmark [card is Warlord's Palace] (amount=1) | WHEN always IF event_count countdown_done of mine landmark [card is Warlord's Palace] ge 1 this_game DO level_up self | WHEN levels_up of self DO summon in board <Warlord's Hoard>
        Dragon Roost: KW: Landmark, Countdown | WHEN countdown_done DO summon <Inviolus Vox>
    - Akshan -> Buried Armory: finishes countdowns
        [runeterra] line now: waits: finishes countdowns
        Akshan: KW: Quick Attack | WHEN summoned of self IF have mine landmark [card is Warlord's Palace] not DO summon in board <Warlord's Palace> | WHEN summoned of self IF have mine landmark [card is Warlord's Palace] is DO countdown_advance mine landmark [card is Warlord's Palace] (amount=1) | WHEN strikes by self IF have mine landmark [card is Warlord's Palace] not DO summon in board <Warlord's Palace> | WHEN strikes by self IF have mine landmark [card is Warlord's Palace] is DO countdown_advance mine landmark [card is Warlord's Palace] (amount=1) | WHEN always IF event_count countdown_done of mine landmark [card is Warlord's Palace] ge 1 this_game DO level_up self | WHEN levels_up of self DO summon in board <Warlord's Hoard>
        Buried Armory: KW: Landmark, Countdown | WHEN countdown_done DO create in hand <Treasure of the Sands>

64. Buried Sun Disc is linked as levelling or waking champions (it only counts Ascended level-ups).
    Rule: none stated. Games: Runeterra. Files: r5 c17.
    - Buried Sun Disc -> Akshan: makes champions level up (it levels up from what it then does)
        [runeterra] line now: levels: makes champions level up (it levels up from what it then does)
        Buried Sun Disc: KW: Countdown, Landmark | WHEN game_start IF have all mine card in deck [region not Shurima] not DO summon mine card in deck [card is Buried Sun Disc] in board <Buried Sun Disc> | WHEN countdown_done of self DO keyword_action <Restore the Sun Disc> | WHEN always DO countdown_advance self (amount=9, times=event_count of (levels_up of mine unit [type is Ascended]) this_game)
        Akshan: KW: Quick Attack | WHEN summoned of self IF have mine landmark [card is Warlord's Palace] not DO summon in board <Warlord's Palace> | WHEN summoned of self IF have mine landmark [card is Warlord's Palace] is DO countdown_advance mine landmark [card is Warlord's Palace] (amount=1) | WHEN strikes by self IF have mine landmark [card is Warlord's Palace] not DO summon in board <Warlord's Palace> | WHEN strikes by self IF have mine landmark [card is Warlord's Palace] is DO countdown_advance mine landmark [card is Warlord's Palace] (amount=1) | WHEN always IF event_count countdown_done of mine landmark [card is Warlord's Palace] ge 1 this_game DO level_up self | WHEN levels_up of self DO summon in board <Warlord's Hoard>
    - Buried Sun Disc -> Annie: makes champions level up
        [runeterra] line now: waits: makes champions level up
        Buried Sun Disc: KW: Countdown, Landmark | WHEN game_start IF have all mine card in deck [region not Shurima] not DO summon mine card in deck [card is Buried Sun Disc] in board <Buried Sun Disc> | WHEN countdown_done of self DO keyword_action <Restore the Sun Disc> | WHEN always DO countdown_advance self (amount=9, times=event_count of (levels_up of mine unit [type is Ascended]) this_game)
        Annie: KW: Attack | WHEN attacks by self DO damage enemy unit in board [state is blocking] (amount=2) THEN damage enemy player (amount=2) | WHEN always IF event_count played by mine player of spell [category in fast_spell] [category in slow_spell] [category in skill] ge 6 this_game DO level_up self | WHEN levels_up of self DO create in hand <Tibbers>

65. Twisted Catalyzer (boosts only "your Darkness") is linked to Annie and Gwen.
    Rule: none stated. Games: Runeterra. Files: r5 c19.
    - Annie -> Twisted Catalyzer: damages units or players (for the ability it gives)
        [runeterra] line now: waits: damages units or players (for the ability it gives)
        Annie: KW: Attack | WHEN attacks by self DO damage enemy unit in board [state is blocking] (amount=2) THEN damage enemy player (amount=2) | WHEN always IF event_count played by mine player of spell [category in fast_spell] [category in slow_spell] [category in skill] ge 6 this_game DO level_up self | WHEN levels_up of self DO create in hand <Tibbers>
        Twisted Catalyzer: WHEN strikes by self DO give_ability all mine card in everywhere [card is Darkness] for permanent
    - Gwen -> Twisted Catalyzer: damages units or players (for the ability it gives)
        [runeterra] line now: waits: damages units or players (for the ability it gives)
        Gwen: KW: Hallowed, Quick Attack, Attack | WHEN attacks by self DO keyword_action enemy player <Drain> (amount=2) for unstated | WHEN stat_changed of mine unit [card not Gwen] IF keyword_condition Hallowed DO stat_change self (power=event_amount) for while | WHEN always IF event_count damaged by self damage ge 10 this_game DO level_up self
        Twisted Catalyzer: WHEN strikes by self DO give_ability all mine card in everywhere [card is Darkness] for permanent

66. Strike spells are said to set off an Attack effect (a strike is not an attack).
    Rule: none stated. Games: Runeterra. Files: r5 c21.
    - Bone Skewer -> Gwen: makes it attack or strike again: its own effect goes off
        [runeterra] line now: waits: makes it attack or strike again: its own effect goes off
        Bone Skewer: WHEN played of self DO strike chosen mine unit in board to chosen enemy unit in board THEN move it in deck_top
        Gwen: KW: Hallowed, Quick Attack, Attack | WHEN attacks by self DO keyword_action enemy player <Drain> (amount=2) for unstated | WHEN stat_changed of mine unit [card not Gwen] IF keyword_condition Hallowed DO stat_change self (power=event_amount) for while | WHEN always IF event_count damaged by self damage ge 10 this_game DO level_up self

67. Twilit Protector's Nightfall buff to Nightfall allies is linked to Aphelios (Nightfall on Nightfall gives no line; Aphelios does not read Power).
    Rule: L15. Games: Runeterra. Files: r5 c22.
    - Twilit Protector -> Aphelios: gives it more power
        [runeterra] line now: stronger: gives it more power
        Twilit Protector: KW: Nightfall, Daybreak | WHEN played of self IF keyword_condition Daybreak DO stat_change all mine unit in board [keyword is Daybreak] (power=1, health=1) for this_round | WHEN played of self IF keyword_condition Nightfall DO stat_change all mine unit in board [keyword is Nightfall] (power=1) for permanent
        Aphelios: KW: Nightfall | WHEN played of self IF keyword_condition Nightfall DO choose_card mine card [name_has is Moon Weapon] (options=1) THEN create it in hand | WHEN played by mine player of [card not Aphelios] [first_each_round] IF event_count played by mine player ge 2 this_round; have mine card in hand [type is Moon Weapon] not DO create in hand | WHEN always IF event_count played by mine player of [name_has is Moon Weapon] ge 4 this_game DO level_up self

68. Level-up lines filed under "type" instead of "levels".
    Rule: none stated. Games: Runeterra. Files: r5 c23.
    - Gifts From Beyond -> Aphelios: makes a Moon Weapon it asks for
        [runeterra] line now: type: makes a Moon Weapon it asks for
        Gifts From Beyond: WHEN played of self DO create chosen mine card [type is Moon Weapon] in hand
        Aphelios: KW: Nightfall | WHEN played of self IF keyword_condition Nightfall DO choose_card mine card [name_has is Moon Weapon] (options=1) THEN create it in hand | WHEN played by mine player of [card not Aphelios] [first_each_round] IF event_count played by mine player ge 2 this_round; have mine card in hand [type is Moon Weapon] not DO create in hand | WHEN always IF event_count played by mine player of [name_has is Moon Weapon] ge 4 this_game DO level_up self
    - Spiderling -> Elise: is a Spider it asks for
        [runeterra] line now: type: is a Spider it asks for
        Spiderling: (no rows)
        Elise: KW: Fearsome, Attack | WHEN attacks by self DO summon in board <Spiderling> THEN start_attack it | WHEN round_start IF count mine unit in board [type is Spider] [card not Elise] ge 3 DO level_up self

69. Ashe's "changes enemy units' stats" list includes Husks, which grant stats to my own ally.
    Rule: none stated. Games: Runeterra. Files: r5 c24.
    - Breakneck Husk -> Ashe: changes enemy units' stats (levels it up)
        [runeterra] line now: levels: changes enemy units' stats (levels it up)
        Breakneck Husk: KW: Immobile, Quick Attack | WHEN played by mine player of all mine unit in board DO kill self THEN stat_change it (power=stat power of (self), health=stat health of (self)) for permanent THEN copy_keywords it to self [state is positive] for permanent
        Ashe: KW: Attack | WHEN attacks by self DO keyword_action highest enemy unit by power in board <Frostbite> for unstated | WHEN always IF event_count stat_changed by mine player of enemy unit [power eq 0] ge 5 this_game DO level_up self | WHEN levels_up of self DO create mine card in deck_top <Crystal Arrow>
    - Ashe -> Gwen (level 2): changes units' stats (for the ability it gives)
        [runeterra] line now: waits: changes units' stats (for the ability it gives)
        Ashe: KW: Attack | WHEN attacks by self DO keyword_action highest enemy unit by power in board <Frostbite> for unstated | WHEN always IF event_count stat_changed by mine player of enemy unit [power eq 0] ge 5 this_game DO level_up self | WHEN levels_up of self DO create mine card in deck_top <Crystal Arrow>
        Gwen (level 2): KW: Hallowed, Quick Attack, Attack | WHEN attacks by self DO give_ability self for this_round THEN keyword_action enemy player <Drain> (amount=1, times=half (stat power of (self))) for unstated

70. Station Archivist (discards nothing) is said to make you discard cards for cards that need themselves discarded.
    Rule: L1, L7. Games: Runeterra. Files: r7 c7.
    - Station Archivist -> Fallen Rider: triggers: makes you discard cards
        [runeterra] line now: waits: makes you discard cards
        Station Archivist: WHEN played of self DO copy 5 chosen mine spell in deck_top in hand THEN give_keyword it <Fleeting> for permanent THEN shuffle_into_deck 5 all mine card in deck_top
        Fallen Rider: KW: Fearsome | WHEN discarded of self DO create in hand <Risen Rider>
    - Station Archivist -> Flame Chompers!: triggers: makes you discard cards
        [runeterra] line now: waits: makes you discard cards
        Station Archivist: WHEN played of self DO copy 5 chosen mine spell in deck_top in hand THEN give_keyword it <Fleeting> for permanent THEN shuffle_into_deck 5 all mine card in deck_top
        Flame Chompers!: KW: Challenger | WHEN discarded of self DO summon self in board

71. Revival cards linked against their own limits (Zurael only last-turn enemy kills, Blood Echoes only own kills, Obelysk/Kujata kill nothing).
    Rule: L20, L21. Games: Duelyst. Files: u2 c9.
    - Darkfire Sacrifice -> Zurael, the Lifegiver: type: makes your units die: Zurael, the Lifegiver brings them back
        [duelyst] line now: type: makes your units die: Zurael, the Lifegiver brings them back
        Darkfire Sacrifice: WHEN played of self DO kill chosen mine unit in board THEN cost_change mine card in hand [category is unit] (cost=-2) for next_card
        Zurael, the Lifegiver: KW: Opening Gambit | WHEN played of self DO revive all mine unit in discard [state is dead_this_round] [state not token] to random position
    - Abhorrent Unbirth -> Blood Echoes: type: makes your units die: Blood Echoes brings them back
        [duelyst] line now: type: makes your units die: Blood Echoes brings them back
        Abhorrent Unbirth: WHEN played of self DO kill all mine unit in board THEN summon <Abomination> (power=1, health=1) THEN stat_change it (power=stat power of (all mine unit in discard), health=stat health of (all mine unit in discard)) for permanent THEN copy_keywords it to all mine unit in discard for permanent
        Blood Echoes: WHEN played of self DO kill all mine unit in board | WHEN turn_end by mine player [next_time] DO revive all mine unit in discard [state is dead_this_round] to random position
    - Simulacra Obelysk -> Keeper of the Vale: type: makes your units die
        [duelyst] line now: type: makes your units die: Keeper of the Vale brings them back
        Simulacra Obelysk: KW: Summon Dervish, Build | WHEN always DO give_keyword self <Build> (amount=2) for permanent | WHEN transformed of self DO summon to chosen position [position is surrounding] <Simulacra Obelysk>
        Keeper of the Vale: KW: Opening Gambit | WHEN played of self DO revive random mine unit in discard to chosen position [position is surrounding]

72. Internal follow-ups, placeholders and AI helpers are treated as cards a player owns/plays.
    Rule: L9. Games: Duelyst. Files: u2 c13.
    - Teleport (follow-up, FollowupTeleportMyGeneralBehindEnemy) -> Chakri Avatar: waits: is a spell whose playing sets off its effect
        [duelyst] line now: waits: is a spell whose playing sets off its effect
        Teleport (follow-up, FollowupTeleportMyGeneralBehindEnemy): WHEN played of self DO move chosen unit in board to chosen position [state is empty] [position is behind]
        Chakri Avatar: WHEN played of mine spell DO stat_change self (power=1, health=1) for permanent
    - Spell Damge -> Soul Grimwar: waits: makes units die (for the ability it gives)
        [duelyst] line now: waits: makes units die (for the ability it gives)
        Spell Damge: WHEN played of self DO damage chosen any (amount=unstated)
        Soul Grimwar: WHEN played of self DO give_ability mine player
    - Cascading Rebirth (follow-up) -> Sellsoul: waits: kills it for its death effect
        [duelyst] line now: waits: kills it for its death effect
        Cascading Rebirth (follow-up): WHEN played of self DO kill chosen mine unit in board THEN summon random unit in board [cost eq sum (stat cost of (it) + 1)] [region is Magmar Aspects]
        Sellsoul: KW: Dying Wish | WHEN dies of self DO damage mine player (amount=4)

73. "Another friendly minion" is read as the card itself (Oropsisaur).
    Rule: L7. Games: Duelyst. Files: u1 c10.
    - Owlbeast Sage -> Oropsisaur: waits: more health or protection: survives damage
        [duelyst] line now: waits: more health or protection: survives damage
        Owlbeast Sage: WHEN played of mine spell DO stat_change all mine unit in board [type is Arcanyst] (health=2) for permanent
        Oropsisaur: WHEN turn_start by mine player DO stat_change self (power=1, health=1) for permanent | WHEN survives_damage of mine unit [keyword is Grow] [card not Oropsisaur] DO grow it
    - Healing Mystic -> Oropsisaur: waits: more health or protection: survives damage
        [duelyst] line now: waits: more health or protection: survives damage
        Healing Mystic: KW: Opening Gambit | WHEN played of self DO heal chosen any in board (amount=2)
        Oropsisaur: WHEN turn_start by mine player DO stat_change self (power=1, health=1) for permanent | WHEN survives_damage of mine unit [keyword is Grow] [card not Oropsisaur] DO grow it
    - Mirkblood Devourer -> Oropsisaur: waits: more health or protection: survives damage
        [duelyst] line now: waits: more health or protection: survives damage
        Mirkblood Devourer: WHEN summoned of mine unit [position is surrounding] DO stat_change it (power=1, health=1) for permanent
        Oropsisaur: WHEN turn_start by mine player DO stat_change self (power=1, health=1) for permanent | WHEN survives_damage of mine unit [keyword is Grow] [card not Oropsisaur] DO grow it

74. Any card that adds cards to hand links to Theobule as "fills your hand" (it only replaces; replace is worded "shuffles cards into the deck").
    Rule: L21 (and L10 for wording). Games: Duelyst. Files: u1 c12 (u3 c10 wording, u3 unsure Replicant).
    - Aegis Barrier -> Theobule: waits: fills your hand
        [duelyst] line now: waits: fills your hand
        Aegis Barrier: WHEN played of self DO cant enemy spell to chosen mine unit in board (event=targeted) for permanent THEN draw mine card in deck_top (amount=1)
        Theobule: KW: Opening Gambit | WHEN played of self DO shuffle_into_deck all mine card in hand THEN draw mine card in deck_top (amount=count of (all mine card in hand))
    - Spelljammer -> Theobule: waits: fills your hand
        [duelyst] line now: waits: fills your hand
        Spelljammer: WHEN turn_end by mine player DO draw mine card in deck_top (amount=1) | WHEN turn_end by enemy player DO draw enemy card in deck_top (amount=1)
        Theobule: KW: Opening Gambit | WHEN played of self DO shuffle_into_deck all mine card in hand THEN draw mine card in deck_top (amount=count of (all mine card in hand))
    - Aethermaster -> White Widow: triggers: shuffles cards into the deck
        [duelyst] line now: waits: shuffles cards into the deck
        Aethermaster: WHEN always DO can mine player (event=shuffled) for while
        White Widow: WHEN shuffled by mine player of mine card in hand DO damage random enemy any (amount=2)
        case ndu13: expect line  (guide: more replaces set off White Widow (family 11))

75. Repairing artifacts is read as healing.
    Rule: L10. Games: Duelyst. Files: u1 c16.
    - Dawn's Eye -> Lightchaser: waits: heals units
        [duelyst] line now: waits: heals units
        Dawn's Eye: WHEN always DO stat_change mine player (power=4) for while | WHEN turn_end by mine player DO heal all mine equipment (amount=full)
        Lightchaser: WHEN healed DO stat_change self (power=1, health=1) for permanent
    - Dawn's Eye -> Gold Vitriol: heals: can heal it
        [duelyst] line now: waits: heals units; heals: can heal it
        Dawn's Eye: WHEN always DO stat_change mine player (power=4) for while | WHEN turn_end by mine player DO heal all mine equipment (amount=full)
        Gold Vitriol: WHEN healed DO damage random enemy any (amount=2)
    - Dawn's Eye -> Excelsious: type: heals units
        [duelyst] line now: type: heals units
        Dawn's Eye: WHEN always DO stat_change mine player (power=4) for while | WHEN turn_end by mine player DO heal all mine equipment (amount=full)
        Excelsious: KW: Provoke, Celerity | WHEN always DO stat_change self (power=event_count of (healed) this_game, health=event_count of (healed) this_game) for while

76. Stats on a move spell are linked as extra help where only the move matters.
    Rule: L18. Games: Duelyst. Files: u3 c11.
    - Mist Dragon Seal -> Bonereaper: ...; also makes stronger: can give it more power and health
        [duelyst] line now: type: Mist Dragon Seal moves Bonereaper, and Bonereaper acts on units around it; stronger: can give it more power and health
        Mist Dragon Seal: WHEN played of self DO stat_change chosen mine unit in board (power=1, health=1) for permanent THEN move it to position
        Bonereaper: KW: Provoke | WHEN turn_end by mine player DO damage all enemy unit in board [position is surrounding] (amount=2)

## H. Missed lines (a line that should exist)

77. Missing: Treasure Map makers (Amai Mapdealer, Aryana, Compass of Gagana, Gagana Treasure Seeker, Message in a Bottle) to cards that count Treasure Maps (Ancient Gargoyle, Triton Stargazer, Fugoro).
    Rule: L17 (f4). Games: Faeria. Files: f1 c15, f3 c6, f4 c9, f1 unsure.
    - (no line exists) Amai Mapdealer -> Ancient Gargoyle: puts Treasure Maps in your deck: it counts them
        [faeria] line now: NONE
        Amai Mapdealer: WHEN played of self DO create in deck <Treasure Map>
        Ancient Gargoyle: KW: Charge, Flying | WHEN always DO give_keyword self <Charge> (amount=3) for permanent THEN give_keyword self <Flying> for permanent | WHEN played of self DO kill all mine card in deck [card is Treasure Map] THEN stat_change self (power=event_amount, health=event_amount) for permanent
    - (no line exists) Amai Mapdealer -> Triton Stargazer
        [faeria] line now: NONE
        Amai Mapdealer: WHEN played of self DO create in deck <Treasure Map>
        Triton Stargazer: KW: Jump | WHEN always DO give_keyword self <Jump> for permanent | WHEN played of self IF have all mine card in hand [card is Treasure Map] is DO draw mine card in deck_top (amount=3) THEN stat_change self (power=2, health=2) for permanent
    - (no line exists) Message in a Bottle -> Triton Stargazer
        [faeria] line now: NONE
        Message in a Bottle: WHEN played of self DO create in deck <Treasure Map> (amount=2) THEN draw mine card in deck_top (amount=1)
        Triton Stargazer: KW: Jump | WHEN always DO give_keyword self <Jump> for permanent | WHEN played of self IF have all mine card in hand [card is Treasure Map] is DO draw mine card in deck_top (amount=3) THEN stat_change self (power=2, health=2) for permanent

78. Missing: Gift of Steel -> Grim Guard (+3/+3 to a Taunt Combat creature); lines exist in other decks.
    Rule: L18. Games: Faeria. Files: f3 c6.
    - (no line exists) Gift of Steel -> Grim Guard
        [faeria] line now: NONE
        Gift of Steel: WHEN played of self DO stat_change chosen unit in board [keyword not Combat] (power=3) for permanent THEN stat_change it unit in board [keyword is Combat] (power=3, health=3) for permanent
        Grim Guard: KW: Taunt, Combat | WHEN always DO give_keyword self <Taunt> for permanent | WHEN fights by self DO damage enemy player (amount=2)

79. Missing: Gagana, Rainbow Birdship / Magnus / Aurora's Dream -> Illusion of Grandeur (cost 0/1 creature), and "triggers" wording.
    Rule: none stated. Games: Faeria. Files: f3 c6.
    - (no line exists) Gagana, Rainbow Birdship -> Illusion of Grandeur
        [faeria] line now: NONE
        Gagana, Rainbow Birdship: KW: Flying | WHEN always DO give_keyword self <Flying> for permanent | WHEN always DO give_keyword all mine card in hand <Wild> for while | WHEN played of self DO create random mine card in hand [name_has is Gagana] in hand THEN cost_set it (cost=0) for permanent
        Illusion of Grandeur: KW: Charge | WHEN always DO give_keyword self <Charge> (amount=2) for permanent | WHEN summoned of mine unit [cost le 1] DO stat_change self (power=stat power of (it), health=stat health of (it)) for permanent

80. Missing: cards of a kind (events, Flying creatures) have no line to cards waiting for that kind to be drawn.
    Rule: L1b (case nfa09). Games: Faeria. Files: f4 c1.
    - (no line exists) Flame Burst -> Flamesilk Faerie
        [faeria] line now: NONE
        Flame Burst: WHEN played of self DO damage chosen anything (amount=3)
        Flamesilk Faerie: KW: Flying | WHEN always DO give_keyword self <Flying> for permanent | WHEN drawn of mine card in hand [category is spell] [once_per_game] DO stat_change self (power=3, health=1) for permanent THEN give_keyword self <Ranged Attack> for permanent
    - (no line exists) Soul Drain -> Sunsilk Faerie
        [faeria] line now: NONE
        Soul Drain: WHEN played of self DO damage chosen unit in board (amount=2) THEN heal mine player (amount=event_amount)
        Sunsilk Faerie: KW: Flying | WHEN always DO give_keyword self <Flying> for permanent | WHEN drawn of mine card in hand [category is spell] [once_per_game] DO stat_change self (power=3, health=1) for permanent THEN give_keyword self <Charge> (amount=3) for permanent
    - (no line exists) Airbot -> Drakkar Skycaptain
        [faeria] line now: NONE
        Airbot: KW: Flying, Dash | WHEN always DO give_keyword self <Flying> for permanent THEN give_keyword self <Dash> (amount=2) for permanent
        Drakkar Skycaptain: KW: Flying | WHEN always DO give_keyword self <Flying> for permanent | WHEN drawn of mine card in hand [category is unit] [keyword is Flying] DO stat_change it (power=1, health=1) for permanent

81. Missing: cards that make a card "by description" (Crystal Spice discovers 7+ cost cards; Yak Attack summons Angry Yaks) have no line to the card that counts/asks for it.
    Rule: L17. Games: Faeria. Files: f4 c9.
    - (no line exists) Crystal Spice -> Gabrian Archon
        [faeria] line now: NONE
        Crystal Spice: WHEN played of self DO keyword_action mine card in hand [rarity not legendary] [cost ge 7] in hand <Discover> (amount=2) for unstated THEN give_keyword it <Wild> for permanent
        Gabrian Archon: KW: Charge | WHEN always DO give_keyword self <Charge> (amount=2) for permanent | WHEN always IF event_count played by mine player of mine card in hand [cost ge 7] ge 2 this_game DO stat_change self (power=2, health=2) for while
    - (no line exists) Yak Attack -> Topaz Yak
        [faeria] line now: NONE
        Yak Attack: WHEN played of self DO summon <Angry Yak> (amount=3, power=2, health=2) THEN give_keyword it <Haste> for permanent
        Topaz Yak: WHEN always DO can self to position [position is bordering] (event=summoned) for while | WHEN played of self IF have all mine unit in board [type is yak] [position is bordering] is DO give_keyword self <Haste> for permanent

82. Missing: a need to stand on enemy land (Triton Adventurer "if this is on an enemy land") is not seen.
    Rule: none stated (cases nfa21, nfa27). Games: Faeria. Files: f4 c10.
    - (no line exists) Oradrim Fanatic -> Triton Adventurer
        [faeria] line now: NONE
        Oradrim Fanatic: KW: Jump | WHEN always DO give_keyword self <Jump> for permanent | WHEN played of self DO move chosen mine unit in board
        Triton Adventurer: KW: Jump | WHEN always DO give_keyword self <Jump> for permanent | WHEN played of self DO move self | WHEN turn_end by mine player IF have enemy position [terrain is land] [position is same_space] is DO draw mine card in deck_top (amount=1)

83. Missing: champion spells ("X's Spell ... Create an X in your deck") get no lines (made champion and own effects).
    Rule: none stated. Games: Runeterra. Files: r3 c15.
    - (no line exists) Vex's Glare -> Vex
        [runeterra] line now: NONE
        Vex's Glare: KW: Slow | WHEN played of self DO give_keyword chosen unit in board <Gloom> for permanent THEN draw mine card in deck_top (amount=1) THEN create in deck <Vex>
        Vex: KW: Fearsome, Attack | WHEN attacks by self DO give_keyword highest enemy unit by power in board <Gloom> for permanent | WHEN always IF event_count given_keyword by mine player of unit [keyword is Gloom] ge 5 this_game DO level_up self
    - (no line exists) Xerath's Rite of the Arcane -> Xerath
        [runeterra] line now: NONE
        Xerath's Rite of the Arcane: KW: Slow | WHEN played of self DO choose_one OR kill chosen mine landmark in board OR kill chosen mine mana THEN damage chosen unit in board (amount=4) THEN create in deck <Xerath>
        Xerath: WHEN killed by mine player of mine landmark DO damage lowest enemy unit by power in board (amount=1) | WHEN always IF event_count killed by mine player of mine landmark ge 4 this_game DO level_up self
    - (no line exists) Jax's Counter Strike -> Jax
        [runeterra] line now: NONE
        Jax's Counter Strike: KW: Burst | WHEN played of self DO give_keyword chosen mine unit in board [card is Jax] <Barrier> for this_round THEN keyword_action chosen mine unit in board [card is Jax] <Forge> for unstated THEN create in deck <Jax>
        Jax: WHEN played of self DO attach self <The Light of Icathia> | WHEN always IF event_count attacks by mine unit [state is equipped] power ge 16 this_game DO level_up self

84. Missing: a transform into a named card is not seen as "puts it into play".
    Rule: none stated. Games: Runeterra. Files: r3 c16.
    - (no line exists) Pyke -> Death From Below
        [runeterra] line now: NONE
        Pyke: KW: Lurk, Quick Attack | WHEN keyword_used of self [keyword is Lurk] DO transform self <Death From Below> | WHEN always IF event_count damaged by mine unit [name_has is Pyke] damage ge 15 this_game DO level_up self
        Death From Below: KW: Fast, Lurk | WHEN played of self DO summon in board <Pyke> THEN strike it to chosen enemy unit in board
    - (no line exists) The Darkin Halberd -> Taarosh
        [runeterra] line now: NONE
        The Darkin Halberd: KW: Equipment | WHEN played of self DO kill chosen mine unit in board | WHEN played of self DO spend_mana mine mana (amount=10) THEN transform self <Taarosh>
        Taarosh: KW: Fearsome | WHEN attacks by self [first_each_round] IF event_count killed by mine player of unit [category is follower] ge 1 this_game DO revive highest enemy unit by power in discard [category is follower] THEN give_keyword it <Ephemeral> for permanent
    - (no line exists) Avenging Vastaya's Ambush -> Avenging Vastaya
        [runeterra] line now: NONE
        Avenging Vastaya's Ambush: KW: Burst | WHEN played of self DO transform chosen mine unit in board [card is Shadow in the Brush] <Avenging Vastaya> | WHEN leaves_play of mine unit in board [card is Shadow in the Brush] DO obliterate self
        Avenging Vastaya: KW: SpellShield | WHEN always DO keyword_action <Ambush> (amount=3) | WHEN transformed of self DO counter all enemy spell [category in fast_spell] [category in slow_spell] [category in skill]

85. Missing: Ephemeral revives (Taarosh) are not seen.
    Rule: L3 (example shape). Games: Runeterra. Files: r3 c17.
    - (no line exists) Taarosh -> Moonlit Glenkeeper
        [runeterra] line now: NONE
        Taarosh: KW: Fearsome | WHEN attacks by self [first_each_round] IF event_count killed by mine player of unit [category is follower] ge 1 this_game DO revive highest enemy unit by power in discard [category is follower] THEN give_keyword it <Ephemeral> for permanent
        Moonlit Glenkeeper: KW: Fearsome, Nightfall | WHEN summoned of mine unit [state is ephemeral] DO stat_change it (power=1) for permanent | WHEN played of self IF keyword_condition Nightfall DO summon in board <Sapling>
    - (no line exists) Taarosh -> Fallen Sands General
        [runeterra] line now: NONE
        Taarosh: KW: Fearsome | WHEN attacks by self [first_each_round] IF event_count killed by mine player of unit [category is follower] ge 1 this_game DO revive highest enemy unit by power in discard [category is follower] THEN give_keyword it <Ephemeral> for permanent
        Fallen Sands General: KW: Overwhelm | WHEN always DO stat_change self (power=event_count of (summoned of mine unit [state is ephemeral]) this_game) for while

86. Missing: World Runes are not a kind the database knows.
    Rule: none stated. Games: Runeterra. Files: r3 c18.
    - (no line exists) Shard of Hope -> Ryze
        [runeterra] line now: NONE
        Shard of Hope: KW: Landmark | WHEN played of self IF count all mine landmark in board [card is Shard of Hope] le 1 DO repeat all mine landmark in board [type is World Rune] [card not Shard of Hope] | WHEN played of self DO heal all mine unit in board [card is Ryze] (amount=2) THEN heal mine player (amount=2) | WHEN activated DO heal all mine unit in board [card is Ryze] (amount=2) THEN heal mine player (amount=2)
        Ryze: WHEN summoned of self DO create in deck <Delve Into The Past> (amount=2) | WHEN round_start DO create in deck <Delve Into The Past> (amount=2) | WHEN always IF amount distinct card of (all mine landmark in board [type is World Rune]) ge 3 DO level_up self
    - (no line exists) Delve Into The Past -> each Shard
        (cards not found by these names)

87. Missing: Overwhelm given to a card that needs to hit the Nexus.
    Rule: L20. Games: Runeterra. Files: r3 c19.
    - (no line exists) Heavy Blade Fragment -> Chempunk Pickpocket
        [runeterra] line now: NONE
        Heavy Blade Fragment: KW: Focus | WHEN played of self DO give_keyword chosen mine unit in board <Overwhelm> for this_round
        Chempunk Pickpocket: WHEN strikes_nexus by self DO copy random enemy card in deck [category is spell] in hand
    - (no line exists) Wildclaw Stance -> Pakaa Cub
        [runeterra] line now: NONE
        Wildclaw Stance: KW: Slow | WHEN played of self DO stat_change chosen mine unit in board (power=2) for permanent THEN give_keyword it mine unit in board <Overwhelm> for permanent
        Pakaa Cub: KW: Fearsome | WHEN always DO keyword_action <Ambush> (amount=1) | WHEN strikes_nexus by self DO summon <Pakaa Protector>

88. Missing: Puffcap planters -> Teemo / Teemo (level 2).
    Rule: none stated. Games: Runeterra. Files: r6 M1.
    - (no line exists) Puffcap Peddler -> Teemo
        [runeterra] line now: NONE
        Puffcap Peddler: KW: Imbue | WHEN played by mine player of spell DO keyword_action 3 random enemy card in deck <Poison Puffcap Plant> (amount=3)
        Teemo: KW: Elusive | WHEN strikes_nexus by self DO keyword_action 5 random enemy card in deck <Poison Puffcap Plant> (amount=5) | WHEN always IF event_count keyword_used by mine player of [keyword is Plant] [card is Poison Puffcap] ge 15 this_game DO level_up self
    - (no line exists) Poison Dart -> Teemo (level 2)
        [runeterra] line now: NONE
        Poison Dart: WHEN played of self DO damage chosen any (amount=1) THEN keyword_action enemy card in deck <Poison Puffcap Plant> (amount=3)
        Teemo (level 2): KW: Elusive | WHEN strikes_nexus by self DO copy all enemy card in deck [card is Poison Puffcap] in deck (min=5)
        case n05: expect line  (Kaptain: Teemo 2 doubles planted Puffcaps)

89. Missing: traps/boons and their planters -> Mister Thrift.
    Rule: none stated. Games: Runeterra. Files: r6 M2.
    - (no line exists) Poison Puffcap -> Mister Thrift
        [runeterra] line now: NONE
        Poison Puffcap: KW: Trap | WHEN played of self DO damage mine player (amount=1)
        Mister Thrift: WHEN keyword_used by mine player of effect [keyword in Trap] [keyword in Boon] DO keyword_action owner player in deck <Plant> (amount=2)
    - (no line exists) Volatile Bloom -> Mister Thrift
        [runeterra] line now: NONE
        Volatile Bloom: KW: Skill | WHEN played of self DO repeat 5 top enemy card in deck [keyword is Trap]
        Mister Thrift: WHEN keyword_used by mine player of effect [keyword in Trap] [keyword in Boon] DO keyword_action owner player in deck <Plant> (amount=2)

90. Missing: other Lurkers' Lurk -> Rek'Sai (it reads its own power).
    Rule: L15 (exception). Games: Runeterra. Files: r6 M3.
    - (no line exists) Xerxa'Reth, The Undertitan -> Rek'Sai (Lurk +1|+0)
        (cards not found by these names)

91. Missing: Bone Skewer -> Lurk cards (Rek'Sai, Pyke, Xerxa'Reth).
    Rule: none stated. Games: Runeterra. Files: r6 M4.
    - (no line exists) Bone Skewer -> Rek'Sai
        [runeterra] line now: NONE
        Bone Skewer: WHEN played of self DO strike chosen mine unit in board to chosen enemy unit in board THEN move it in deck_top
        Rek'Sai: KW: Lurk | WHEN keyword_used by self of keyword [keyword is Lurk] DO stat_change all mine unit in everywhere [type is Lurker] (power=1) for permanent | WHEN attacks by self DO stat_change all mine unit in everywhere [type is Lurker] (power=1) for permanent | WHEN round_end DO shuffle_into_deck self in deck | WHEN always IF event_count attacks by self power ge 10 this_game DO level_up self
    - (no line exists) Bone Skewer -> Pyke
        [runeterra] line now: NONE
        Bone Skewer: WHEN played of self DO strike chosen mine unit in board to chosen enemy unit in board THEN move it in deck_top
        Pyke: KW: Lurk, Quick Attack | WHEN keyword_used of self [keyword is Lurk] DO transform self <Death From Below> | WHEN always IF event_count damaged by mine unit [name_has is Pyke] damage ge 15 this_game DO level_up self

92. Missing: Pen Nib counts Attacks played but gets no count lines (like Nunchaku).
    Rule: none stated. Games: Slay the Spire. Files: s2 c8.
    - (no line exists) Shiv -> Pen Nib
        [sts1] line now: NONE
        Shiv: (no rows)
        Pen Nib: WHEN played of mine spell [type is Attack] IF event_count played of mine spell [type is Attack] every 10 this_game DO increase_effect it (percent=100)
    - (no line exists) Claw -> Pen Nib
        [sts1] line now: NONE
        Claw: WHEN played of self DO damage chosen enemy unit in board (amount=3) THEN increase_effect all mine card [card is Claw] (amount=2) for permanent
        Pen Nib: WHEN played of mine spell [type is Attack] IF event_count played of mine spell [type is Attack] every 10 this_game DO increase_effect it (percent=100)
    - (no line exists) Beam Cell -> Pen Nib
        [sts1] line now: NONE
        Beam Cell: WHEN played of self DO damage chosen enemy unit in board (amount=3) THEN give_keyword it enemy unit <Vulnerable> (amount=1) for permanent
        Pen Nib: WHEN played of mine spell [type is Attack] IF event_count played of mine spell [type is Attack] every 10 this_game DO increase_effect it (percent=100)

93. Missing: Stun cards -> Cryoblade ("double damage to Stunned enemies"); Omniseer -> Verdant Fulmination.
    Rule: none stated. Games: Duelyst. Files: u1 (Missed lines).
    - (no line exists) Icy -> Cryoblade
        [duelyst] line now: NONE
        Icy: KW: Opening Gambit | WHEN played of self DO give_keyword chosen enemy unit in board [position is surrounding] <Stunned> for next_own_turn
        Cryoblade: WHEN damaged by self of enemy unit in board [state is stunned] DO damage it (amount=event_amount)
    - (no line exists) Permafrost -> Cryoblade
        [duelyst] line now: NONE
        Permafrost: WHEN played of self DO give_keyword chosen enemy unit in board <Stunned> for next_own_turn THEN give_keyword chosen enemy unit in board [position is surrounding] <Stunned> for next_own_turn
        Cryoblade: WHEN damaged by self of enemy unit in board [state is stunned] DO damage it (amount=event_amount)
    - (no line exists) Omniseer -> Verdant Fulmination
        [duelyst] line now: NONE
        Omniseer: KW: Opening Gambit | WHEN played of self DO set_terrain chosen position [position is surrounding] to position [terrain is growth_space] <Primal Flourish>
        Verdant Fulmination: WHEN played of self DO grow all mine unit in board [position is same_space] THEN set_terrain position [position is same_space] to position [terrain is growth_space] <Primal Flourish>

94. Missing: Fractal Replication -> Dying Wish cards (Unseven, Grimes, Dagona).
    Rule: L19. Games: Duelyst. Files: u3 c12.
    - (no line exists) Fractal Replication -> Unseven
        [duelyst] line now: NONE
        Fractal Replication: WHEN played of self DO copy chosen mine unit in board to chosen position [position is surrounding] in board (amount=2)
        Unseven: KW: Dying Wish | WHEN dies of self DO summon chosen mine card in hand [category is unit] [keyword is Dying Wish]
    - (no line exists) Fractal Replication -> Dagona
        [duelyst] line now: NONE
        Fractal Replication: WHEN played of self DO copy chosen mine unit in board to chosen position [position is surrounding] in board (amount=2)
        Dagona: KW: Dying Wish, Opening Gambit | WHEN played of self DO capture chosen unit in everywhere | WHEN dies of self DO summon it to position [position is same_space]

95. Missing: return to the action bar of Opening Gambit cards (Hailstone Prison -> Hearth-Sister; Sandswirl Reader -> Azure Herald / Healing Mystic).
    Rule: L14. Games: Duelyst. Files: u3 c12.
    - (no line exists) Hailstone Prison -> Hearth-Sister
        [duelyst] line now: NONE
        Hailstone Prison: WHEN played of self DO return_to_hand chosen unit in board
        Hearth-Sister: KW: Opening Gambit | WHEN played of self DO swap self to chosen unit in board [card not Hearth-Sister]
    - (no line exists) Sandswirl Reader -> Azure Herald
        [duelyst] line now: NONE
        Sandswirl Reader: KW: Opening Gambit | WHEN played of self DO return_to_hand chosen unit in board [position is surrounding] THEN set_terrain position [position is same_space] to position [terrain is summon_space] <Exhuming Sand>
        Azure Herald: KW: Opening Gambit | WHEN played of self DO heal mine player (amount=3)
    - (no line exists) Sandswirl Reader -> Healing Mystic
        [duelyst] line now: NONE
        Sandswirl Reader: KW: Opening Gambit | WHEN played of self DO return_to_hand chosen unit in board [position is surrounding] THEN set_terrain position [position is same_space] to position [terrain is summon_space] <Exhuming Sand>
        Healing Mystic: KW: Opening Gambit | WHEN played of self DO heal chosen any in board (amount=2)

## Unsure items raised by more than one file
- Removal -> Ranged Attack "clears its line of fire": is a ranged attack blocked by units in between? (f1, f3)
- Land colour (L22) lines to all cards of a colour, and Seed/Wild Growth/Baeru -> coloured cards: count huge, colours unchecked. (f2, f3)
- Plain single-target removal/damage on my own Last Words / sacrifice target (Soul Drain -> Deathwish Ghoul, Ravenous Flock -> Ceaseless Sentry, Mystic Shot -> Blade Squire, Sump Fumes -> Last Breath allies): L11 or a real sacrifice? (f3, r4, r6, r7)
- Plain draw cards -> cards that wait for one kind of draw (Sunsilk Faerie, Flight of the Mantas, Ancient Herald, Gabrian Commander, Janna, Cloak Clasp): L1b generic? (f3, f4, r5, s1)
- Cost-match filters ("play a 2 cost card", Insightful Investigator, Tri-beam Improbulator) and "pays for it" with a low EXPENSIVE threshold (energy to 2+ cost): generic by L21? (r3, r5, s1, s2, r1)
- Mecha vs Yordle (Rumble (level 2), Arena Kingpin, Wizened Wizard, Gnar -> Heimerdinger): tribe not shown in the printed text. (r2, r3, r5)
- Random help (Dragon Dedicant / Smokescaled Host reduce a random card; Snecko Oil, Madness, Mummified Hand): is random cost change aimed help? (r3, s1)
- Heal (not more health) to Provoke/Taunt units: does healing count under L18? (u1, u2, u3)
- Whether spells are a minority for L1b (308 of 1036 cards in Duelyst), so "is a spell whose playing..." lines stay. (u1, u3)
- Kills/damage of any friendly or enemy minion feeding Deathwatch/revivers (Death Knell, Corpse Combustion, Bonereaper -> Deathwatch cards): generic by L21? (u1, u2)
- Does Scout / Challenger / Tough count as a second attack, targeting, or a damage reduction (Samira -> Ardent Tracker, King Jarvan III -> Gwen, Braum -> Ezreal, The Scargrounds -> Braum)? (r2, r3, r5, r7)
- "Is played" from Prank and Stance Swap: do they play another card? (r1, r2; r7 Prank -> Curious Shellfolk)
- A tribe/kind narrow enough for aimed help (Arcanyst via Kindling/Owlbeast Sage, Infiltrate via Wind Sister Maia, Golem, 5+ Life creatures)? L14. (f1, u1, u2, u3)
- Movement/keyword given to Combat cards depends on Faeria's Combat trigger. (f2, f3)
- Copies of Flashbomb Trap/trap planting: whose side the trap lands on. (r2, r5)
- Cards that fill hand "Chemtech Drake <- fills your hand" / hand-size readers (Cloak Clasp, Spirit Shield): too generic under L21. (r1, s1)

## Must-stay lines (exact, up to 15)
- Clockwork Yak -> Topaz Yak: type: is a yak it asks for
- Syland Horsemaster -> Lost Explorer: waits: moves it for its effect
- Celestial Tower -> Oradrim Monk: moves: moves it within reach of the enemy player
- Fragmenter -> Hate Seed: cheaper: puts your units into play
- Architect -> Doomgate, Door to Oblivion: stronger: can give it more health
- Illusion of Grandeur -> Gabrian Commander: triggers: is a card whose drawing sets off its effect
- Chemtech Drake -> Jagged Butcher: damages the enemy player
- Fae Guide -> Fizz (level 2): can give it Elusive
- Mischievous Marai -> Kennen: puts your units into play (levels it up)
- Laurent Protege -> Baccai Witherclaw: waits: makes this happen: challenges
- Cithria the Bold -> Bitsy Lizard: type: helps it hit the enemy player
- Corruption -> Feel No Pain: triggers: exhausts cards
- Shuriken -> Heavy Blade: type: gives you Strength
- Unseven -> Dagona: puts it into play: puts it into play from the hand
- Bonereaper -> Deathstrike Seal: waits: damages units or players (for the ability it gives)
