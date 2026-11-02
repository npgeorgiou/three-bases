# Merged causes (Runeterra, new method) - files: a, d1, d2, d3, d4, v3a, v3d1, v3d2, v3d3
Format per cause: wrong thinking | rule broken | games | files | examples.
File reference "d1 cG" = cause G in causes_d_runeterra_1.md; "a c1" = cause 1 in causes_a_runeterra.md; v3a, v3d1, v3d2, v3d3 = v3_causes_a_runeterra.md, v3_causes_d_runeterra_p2_1/2/3.md.

## A. Reaching the Nexus (Overwhelm, Elusive, Fearsome, Plunder)

1. Wrong thinking: a card that only HAS Overwhelm/Elusive/Fearsome itself gets "helps it hit the enemy player" toward a card that just needs Nexus damage dealt (the keyword works only for its own card, and the same pair type is split at random between "damages" and "helps it hit").
   Rule: L20, L10. Games: Runeterra. Files: a c1, d3 cF, v3d1 c7
   - Alpha Wildclaw -> Bitsy Lizard: helps it hit the enemy player [Alpha Wildclaw: KW: Overwhelm]
        [runeterra] line now: type: damages the enemy player; type: helps it hit the enemy player
        Alpha Wildclaw: KW: Overwhelm
        Bitsy Lizard: WHEN round_end IF event_count nexus_damaged of enemy player ge 1 this_round DO transform self <Lava Lizard>
   - Bubble Bear -> Dame the Despoiler: helps it hit the enemy player [Bubble Bear: KW: Attune, Elusive; no give_keyword row]
        [runeterra] line now: type: damages the enemy player; type: helps it hit the enemy player
        Bubble Bear: KW: Attune, Elusive
        Dame the Despoiler: KW: Plunder, Overwhelm | WHEN played of self IF keyword_condition Plunder DO stat_change all mine unit in board (power=1) for permanent
   - Darius -> Jagged Butcher: enables: damages the enemy player; also helps it hit the enemy player
        [runeterra] line now: type: damages the enemy player; type: helps it hit the enemy player
        Darius: KW: Overwhelm | WHEN always IF stat enemy player health le half base_health of (enemy player) DO level_up self
        Jagged Butcher: KW: Plunder | WHEN played of self IF keyword_condition Plunder DO stat_change self (power=1, health=1) for permanent
   - Amateur Aeronaut -> Darius: levels: helps it hit the enemy player [Elusive]
        [runeterra] line now: levels: damages the enemy player (levels it up); levels: helps it hit the enemy player (levels it up)
        Amateur Aeronaut: KW: Elusive
        Darius: KW: Overwhelm | WHEN always IF stat enemy player health le half base_health of (enemy player) DO level_up self
        case n12: expect line  (Kaptain: Nexus damage levels Darius)

2. Wrong thinking: a card whose only reason is a keyword (Overwhelm, Elusive, Fearsome) is described both as "damages the enemy player" and "helps it hit the enemy player" in one line, although it has no damage text.
   Rule: L10, L1, L20. Games: Runeterra. Files: d1 cG, d2 cG, d3 cF, v3d1 c7, v3d2 c1
   - Iron Ballista -> Gnar: helps it level up: damages the enemy player (levels it up); also helps it hit the enemy player (levels it up)
        [runeterra] line now: levels: damages the enemy player (levels it up); levels: helps it hit the enemy player (levels it up)
        Iron Ballista: KW: Overwhelm
        Gnar: KW: Quick Attack | WHEN strikes by self IF have mine card in hand [card is Pokey Stick] not DO create in hand <Pokey Stick> | WHEN strikes by self IF have mine card in hand [card is Pokey Stick] is DO cost_change mine card in hand [card is Pokey Stick] (cost=-2) for permanent | WHEN round_end IF event_count nexus_damaged of enemy player ge 1 this_round DO level_up self
   - Zap Sprayfin -> Black Market Merchant: enables: damages the enemy player; also helps it hit the enemy player
        [runeterra] line now: type: damages the enemy player; type: helps it hit the enemy player
        Zap Sprayfin: KW: Elusive, Attune | WHEN summoned of self DO draw random mine card in deck [category is spell] [cost le 3] (amount=1)
        Black Market Merchant: KW: Plunder | WHEN drawn by mine player of enemy card DO cost_change it (cost=-1) for permanent | WHEN played of self IF keyword_condition Plunder DO keyword_action <Nab> (amount=1)
   - Trundle (level 2) -> Sejuani (level 2): triggers: damages the enemy player; also helps it hit the enemy player
        [runeterra] line now: waits: damages the enemy player; waits: helps it hit the enemy player
        Trundle (level 2): KW: Overwhelm, Regeneration, Attack | WHEN summoned of self DO create in hand <Ice Pillar> | WHEN attacks by self IF keyword_condition Behold mine card in hand [cost ge 8] DO stat_change self (power=count of (mine card in hand [cost ge 8])) for permanent
        Sejuani (level 2): KW: Overwhelm | WHEN played of self DO keyword_action chosen enemy unit in board <Frostbite> for unstated THEN give_keyword it <Vulnerable> for this_round | WHEN nexus_damaged by mine player of enemy player [first_each_round] DO keyword_action all enemy unit in board <Frostbite> for unstated
   - The Dreadway -> Gangplank: puts it into play: draws it from the deck; also helps it level up: damages the enemy player (levels it up); also helps it level up: helps it hit the enemy player (levels it up); also makes stronger: doubles its damage
        [runeterra] line now: puts: draws it from the deck; levels: damages the enemy player (levels it up); levels: helps it hit the enemy player (levels it up); stronger: doubles its damage
        The Dreadway: KW: Fearsome | WHEN summoned of self DO draw mine card in deck [card is Gangplank] (amount=1) | WHEN damaged by mine spell DO damage it (amount=event_amount) | WHEN damaged by mine unit DO damage it (amount=event_amount)
        Gangplank: KW: Overwhelm | WHEN summoned of self DO summon in board <Powder Keg> | WHEN always IF event_count nexus_damaged of enemy player ge 5 different_rounds DO level_up self

3. Wrong thinking: a Plunder cost drop is said as "enables" and also as "makes cheaper" (the same act written twice).
   Rule: L10. Games: Runeterra. Files: d2 cF, d3 cF, v3d1 c7, v3d2 c1
   - Zap Sprayfin -> Monster Harpoon: enables: helps it hit the enemy player; also makes cheaper: damages the enemy player
        [runeterra] line now: type: helps it hit the enemy player; cheaper: damages the enemy player
        Zap Sprayfin: KW: Elusive, Attune | WHEN summoned of self DO draw random mine card in deck [category is spell] [cost le 3] (amount=1)
        Monster Harpoon: KW: Plunder | WHEN always IF keyword_condition Plunder DO cost_change self (cost=-2) for while | WHEN played of self DO damage chosen unit in board (amount=5)
   - Gangplank (level 2) -> Monster Harpoon: enables: helps it hit the enemy player; also makes cheaper: damages the enemy player
        [runeterra] line now: type: helps it hit the enemy player; cheaper: damages the enemy player
        Gangplank (level 2): KW: Overwhelm, Attack | WHEN summoned of self DO summon in board <Powder Keg> | WHEN round_start DO summon in board <Powder Keg> | WHEN attacks by self DO damage all enemy unit in board (amount=1) THEN damage enemy player (amount=1)
        Monster Harpoon: KW: Plunder | WHEN always IF keyword_condition Plunder DO cost_change self (cost=-2) for while | WHEN played of self DO damage chosen unit in board (amount=5)
   - Sejuani -> Monster Harpoon: enables: helps it hit the enemy player; also makes cheaper: damages the enemy player
        [runeterra] line now: type: helps it hit the enemy player; cheaper: damages the enemy player
        Sejuani: KW: Overwhelm | WHEN played of self DO keyword_action chosen enemy unit in board <Frostbite> for unstated THEN give_keyword it enemy unit in board <Vulnerable> for this_round | WHEN always IF event_count nexus_damaged of enemy player ge 5 different_rounds DO level_up self
        Monster Harpoon: KW: Plunder | WHEN always IF keyword_condition Plunder DO cost_change self (cost=-2) for while | WHEN played of self DO damage chosen unit in board (amount=5)
   - Captain Farron -> Monster Harpoon: enables: helps it hit the enemy player; also makes cheaper: damages the enemy player
        [runeterra] line now: type: helps it hit the enemy player; cheaper: damages the enemy player
        Captain Farron: KW: Overwhelm | WHEN summoned of self DO create in hand <Decimate> (amount=2)
        Monster Harpoon: KW: Plunder | WHEN always IF keyword_condition Plunder DO cost_change self (cost=-2) for while | WHEN played of self DO damage chosen unit in board (amount=5)

## B. Attacks and fighting

4. Wrong thinking: two cards with the same keyword Scout are linked by "another attack", although no text uses the extra attack.
   Rule: L15, L1, L2. Games: Runeterra. Files: a c9
   - Greathorn Companion -> Greenfang Warden: another attack [Greathorn Companion: KW: Scout; Greenfang Warden: KW: Barrier, Scout]
        [runeterra] line now: type: another attack
        Greathorn Companion: KW: Scout
        Greenfang Warden: KW: Barrier, Scout

5. Wrong thinking: every unit can fight, so a source whose only row is Scout, Quick Attack, Fearsome, Elusive or a summon is linked by "(by fighting)" reasons (makes units die, makes your units attack, damages the enemy player).
   Rule: L1, L2, L4, L15, L20. Games: Runeterra. Files: a c12, d4 cC7
   - Greathorn Companion -> Angel: damages the enemy player (by fighting)
        [runeterra] line now: type: damages the enemy player (by fighting); type: helps it hit the enemy player
        Greathorn Companion: KW: Scout
        Angel: KW: Brash, Plunder | WHEN played of self IF keyword_condition Plunder DO create in hand <Coin> (amount=3)
   - Academy Prodigy -> Ye Been Warned: makes enemy units die (by fighting) [Academy Prodigy: KW: Quick Attack]
        [runeterra] line now: waits: makes enemy units die (by fighting)
        Academy Prodigy: KW: Quick Attack
        Ye Been Warned: WHEN played of self DO give_keyword chosen enemy unit in board <Vulnerable> for this_round | WHEN dies of enemy unit [keyword is Vulnerable] [state is targeted_this_round] [next_time] DO draw mine card in deck_top (amount=1)
   - Camavoran Soldier -> Viego (level 2): triggers: makes units die (by fighting)
        [runeterra] line now: waits: makes units die (by fighting)
        Camavoran Soldier: WHEN summoned of self DO summon <Encroaching Mist>
        Viego (level 2): KW: Fearsome | WHEN dies of unit [card not Viego] [first_each_round] DO summon mine unit [card not Viego (level 2)] in board <Encroaching Mist> | WHEN round_start DO steal highest enemy unit by power in board [category not champion] for this_round THEN kill it enemy unit [category is champion]
   - Ghastly Band -> Shark Chariot: triggers: makes your units attack (by fighting)
        [runeterra] line now: waits: makes your units attack (by fighting)
        Ghastly Band: KW: Hallowed, Ephemeral
        Shark Chariot: KW: Can't Block, Ephemeral, Last Breath | WHEN dies of self DO give_ability mine player

6. Wrong thinking: one extra attack (Rally, attack token) is said two or three times in one line ("another attack", "makes your units attack", "makes it attack for its effect").
   Rule: L10. Games: Runeterra. Files: d1 cB, d2 cA, d4 cC12
   - Blood in the Water -> Rek'Sai: helps it level up: another attack (levels it up); also makes it attack for its effect (levels it up); also triggers: makes it attack for its effect
        [runeterra] line now: levels: another attack (levels it up); levels: makes it attack for its effect (levels it up); waits: makes it attack for its effect
        Blood in the Water: KW: Lurk | WHEN played of self DO damage chosen any (amount=1) THEN gain_attack_token mine player
        Rek'Sai: KW: Lurk | WHEN keyword_used by self of keyword [keyword is Lurk] DO stat_change all mine unit in everywhere [type is Lurker] (power=1) for permanent | WHEN attacks by self DO stat_change all mine unit in everywhere [type is Lurker] (power=1) for permanent | WHEN round_end DO shuffle_into_deck self in deck | WHEN always IF event_count attacks by self power ge 10 this_game DO level_up self
   - Golden Aegis -> Poppy: helps it level up: another attack (levels it up); also makes it attack for its effect (levels it up); also triggers: makes it attack for its effect
        [runeterra] line now: levels: another attack (levels it up); levels: makes it attack for its effect (levels it up); waits: makes it attack for its effect
        Golden Aegis: WHEN played of self DO give_keyword chosen mine unit in board <Barrier> for this_round THEN gain_attack_token mine player
        Poppy: KW: Attack | WHEN attacks by self DO stat_change all mine unit in board [power le stat power of (self)] (power=1, health=1) for permanent | WHEN always IF event_count attacks by self ge 3 this_game DO level_up self
   - Golden Aegis -> Sivir (level 2): enables: another attack; also makes your units attack; also makes it attack for its effect
        [runeterra] line now: type: another attack; type: makes it attack for its effect; type: makes your units attack
        Golden Aegis: WHEN played of self DO give_keyword chosen mine unit in board <Barrier> for this_round THEN gain_attack_token mine player
        Sivir (level 2): KW: Quick Attack, SpellShield | WHEN always IF have self [state is attacking] is DO copy_keywords all mine unit in board [state is attacking] to self for while
   - Blossoming Blade -> Irelia (level 2): triggers: another attack; also makes your units attack
        [runeterra] line now: waits: another attack; waits: makes your units attack
        Blossoming Blade: WHEN played of self DO keyword_action <Blade Dance> (amount=2)
        Irelia (level 2): KW: Quick Attack, Attune | WHEN summoned of self IF attack_token is DO create in hand <Flawless Duet> | WHEN round_start IF attack_token is DO create in hand <Flawless Duet> | WHEN attacks by all mine unit in board DO create in hand <Bladesurge>

7. Wrong thinking: a level 2 card that only has attack keywords or attack rows is linked by "damages units or players" because attacking is what every card does.
   Rule: L2. Games: Runeterra. Files: d1 cJ
   - Ashe (level 2) -> LeBlanc: helps it level up: damages units or players (levels it up)
        [runeterra] line now: levels: damages units or players (levels it up)
        Ashe (level 2): KW: Attack | WHEN attacks by self DO keyword_action highest enemy unit by power in board <Frostbite> for unstated | WHEN always DO cant all enemy unit in board [power eq 0] (event=blocks) for while
        LeBlanc: KW: Quick Attack | WHEN always IF event_count damaged by mine player damage ge 15 this_game DO level_up self | WHEN levels_up of self DO create in hand <Mirror Image>
        case n13: expect line  (Kaptain: damage you deal levels LeBlanc)

## C. One reason said twice

8. Wrong thinking: one power boost is said as both "enables: changes its stats for its effect" and "makes stronger: more power" (or "changes your units' stats" plus "can give it more power and health").
   Rule: L10. Games: Runeterra. Files: d1 cB, d2 cA
   - Call the Pack -> Xerxa'Reth, The Undertitan: enables: changes its stats for its effect; also makes stronger: more power
        [runeterra] line now: type: changes its stats for its effect; stronger: more power
        Call the Pack: KW: Lurk | WHEN played of self DO put_on_top chosen mine card in hand in deck_top THEN create 2 random unit [type is Lurker] in hand
        Xerxa'Reth, The Undertitan: KW: Lurk, Attack | WHEN attacks by self IF stat self power ge 8 DO give_keyword self <Fearsome> for this_round THEN give_keyword self <Overwhelm> for this_round THEN give_keyword self <SpellShield> for this_round
   - Bloodbait -> Xerxa'Reth, The Undertitan: enables: changes its stats for its effect; also makes stronger: more power
        [runeterra] line now: type: changes its stats for its effect; stronger: more power
        Bloodbait: KW: Lurk | WHEN played of self DO create in deck_top <Snapjaw Swarm>
        Xerxa'Reth, The Undertitan: KW: Lurk, Attack | WHEN attacks by self IF stat self power ge 8 DO give_keyword self <Fearsome> for this_round THEN give_keyword self <Overwhelm> for this_round THEN give_keyword self <SpellShield> for this_round
   - Chime -> Bard: helps it level up: changes your units' stats (levels it up); also makes stronger: can give it more power and health
        [runeterra] line now: levels: changes your units' stats (levels it up); stronger: can give it more power and health
        Chime: KW: Boon | WHEN played of self DO stat_change random mine unit in hand (power=1, health=1) for permanent
        Bard: KW: Attack | WHEN attacks by self DO keyword_action mine player in deck <Chime Plant> (amount=3) | WHEN always IF event_count stat_changed of mine unit total_stats ge 20 this_game DO level_up self
        case n09: expect line  (Kaptain: Chimes add stats, which levels Bard)
   - Snapjaw Swarm -> Xerxa'Reth, The Undertitan: enables: changes its stats for its effect; also makes stronger: more power
        [runeterra] line now: type: changes its stats for its effect; stronger: more power
        Snapjaw Swarm: KW: Lurk | WHEN played of self DO start_attack self
        Xerxa'Reth, The Undertitan: KW: Lurk, Attack | WHEN attacks by self IF stat self power ge 8 DO give_keyword self <Fearsome> for this_round THEN give_keyword self <Overwhelm> for this_round THEN give_keyword self <SpellShield> for this_round

9. Wrong thinking: one fact (the card it names, the spell it needs played, a discard) is said as several needs in one line (names / counts / asks / triggers).
   Rule: L10. Games: Runeterra. Files: d2 cA, v3d1 c7 (Ravenous Flock is not here), v3d2 c1
   - Warlord's Palace -> Akshan: enables: is a landmark it counts; also is a landmark or structure it asks for; also is the Warlord's Palace it names
        [runeterra] line now: type: is a landmark it counts; type: is a landmark or structure it asks for; type: is the Warlord's Palace it names
        Warlord's Palace: KW: Countdown, Landmark | WHEN countdown_done of self DO create in hand <Relic of Power> | WHEN targeted by mine player of mine unit DO countdown_advance self (amount=1)
        Akshan: KW: Quick Attack | WHEN summoned of self IF have mine landmark [card is Warlord's Palace] not DO summon in board <Warlord's Palace> | WHEN summoned of self IF have mine landmark [card is Warlord's Palace] is DO countdown_advance mine landmark [card is Warlord's Palace] (amount=1) | WHEN strikes by self IF have mine landmark [card is Warlord's Palace] not DO summon in board <Warlord's Palace> | WHEN strikes by self IF have mine landmark [card is Warlord's Palace] is DO countdown_advance mine landmark [card is Warlord's Palace] (amount=1) | WHEN always IF event_count countdown_done of mine landmark [card is Warlord's Palace] ge 1 this_game DO level_up self | WHEN levels_up of self DO summon in board <Warlord's Hoard>
   - Ice Pillar -> Trundle: helps it level up: is a card it needs played for its count (levels it up); also enables: is the Ice Pillar it names
        [runeterra] line now: levels: is a card it needs played for its count (levels it up); type: is the Ice Pillar it names
        Ice Pillar: KW: Vulnerable | WHEN played of self DO mana_gain mine mana (amount=8) THEN give_keyword highest enemy unit by power in board <Vulnerable> for this_round | WHEN round_start DO give_keyword highest enemy unit by power in board <Vulnerable> for this_round
        Trundle: KW: Regeneration | WHEN summoned of self DO create in hand <Ice Pillar> | WHEN always IF event_count played by mine player of card [card is Ice Pillar] ge 1 this_game DO level_up self
   - Assembly Line -> Lux: helps it level up: costs 6: pays it alone (levels it up); also is a spell it needs played for its count (levels it up)
        [runeterra] line now: levels: costs 6: pays it alone (levels it up); levels: is a spell it needs played for its count (levels it up)
        Assembly Line: WHEN played of self DO summon <Forge Worker> (amount=2)
        Lux: KW: Barrier | WHEN always IF event_count mana_spent by mine player of spell ge 6 this_game DO level_up self | WHEN levels_up of self DO create in hand <Final Spark>
   - Grave Physician -> Sion: helps it level up: makes you discard cards (levels it up); also enables: makes you discard cards; also triggers: makes you discard cards
        [runeterra] line now: levels: makes you discard cards (levels it up); type: makes you discard cards; waits: makes you discard cards
        Grave Physician: WHEN played of self DO discard chosen mine card in hand (amount=1) THEN draw mine card in deck [category is unit] (amount=1)
        Sion: KW: Overwhelm | WHEN discarded of self DO give_keyword highest mine unit by power in board <Overwhelm> for permanent THEN move self in deck | WHEN always DO stat_change self (power=event_count of (discarded by mine player of card) this_game, max=7) for while | WHEN always IF amount sum (event_count power of (discarded by mine player of card) this_game + event_count power of (summoned by mine player of mine unit) this_game) ge 35 DO level_up self

10. Wrong thinking: speeding up a countdown is said as summons, finishes countdowns and speeds up its countdown at once.
   Rule: L10. Games: Runeterra. Files: d2 cA
   - Akshan -> Warlord's Palace: puts it into play: summons; also triggers: finishes countdowns; also makes stronger: can speed up its countdown
        [runeterra] line now: puts: summons; waits: finishes countdowns; stronger: can speed up its countdown
        Akshan: KW: Quick Attack | WHEN summoned of self IF have mine landmark [card is Warlord's Palace] not DO summon in board <Warlord's Palace> | WHEN summoned of self IF have mine landmark [card is Warlord's Palace] is DO countdown_advance mine landmark [card is Warlord's Palace] (amount=1) | WHEN strikes by self IF have mine landmark [card is Warlord's Palace] not DO summon in board <Warlord's Palace> | WHEN strikes by self IF have mine landmark [card is Warlord's Palace] is DO countdown_advance mine landmark [card is Warlord's Palace] (amount=1) | WHEN always IF event_count countdown_done of mine landmark [card is Warlord's Palace] ge 1 this_game DO level_up self | WHEN levels_up of self DO summon in board <Warlord's Hoard>
        Warlord's Palace: KW: Countdown, Landmark | WHEN countdown_done of self DO create in hand <Relic of Power> | WHEN targeted by mine player of mine unit DO countdown_advance self (amount=1)
   - Akshan -> Warlord's Hoard: puts it into play: summons; also triggers: finishes countdowns; also makes stronger: can speed up its countdown
        [runeterra] line now: puts: summons
        Akshan: KW: Quick Attack | WHEN summoned of self IF have mine landmark [card is Warlord's Palace] not DO summon in board <Warlord's Palace> | WHEN summoned of self IF have mine landmark [card is Warlord's Palace] is DO countdown_advance mine landmark [card is Warlord's Palace] (amount=1) | WHEN strikes by self IF have mine landmark [card is Warlord's Palace] not DO summon in board <Warlord's Palace> | WHEN strikes by self IF have mine landmark [card is Warlord's Palace] is DO countdown_advance mine landmark [card is Warlord's Palace] (amount=1) | WHEN always IF event_count countdown_done of mine landmark [card is Warlord's Palace] ge 1 this_game DO level_up self | WHEN levels_up of self DO summon in board <Warlord's Hoard>
        Warlord's Hoard: KW: Countdown, Landmark | WHEN countdown_done of self DO create in hand <Sentinel's Hoard> | WHEN targeted by mine player of mine unit DO countdown_advance self (amount=1)
   - Akshan (level 2) -> Warlord's Hoard: puts it into play: summons; also triggers: finishes countdowns; also makes stronger: can speed up its countdown
        [runeterra] line now: puts: summons; waits: finishes countdowns; stronger: can speed up its countdown
        Akshan (level 2): KW: Quick Attack | WHEN summoned of self DO choose_one mine player OR summon in board <Warlord's Hoard> OR countdown_advance mine landmark [card is Warlord's Hoard] (amount=1) | WHEN strikes by self DO choose_one mine player OR summon in board <Warlord's Hoard> OR countdown_advance mine landmark [card is Warlord's Hoard] (amount=1)
        Warlord's Hoard: KW: Countdown, Landmark | WHEN countdown_done of self DO create in hand <Sentinel's Hoard> | WHEN targeted by mine player of mine unit DO countdown_advance self (amount=1)

11. Wrong thinking: one act is said under two different reasons (a play said as "plays" and "casts its skill"; giving Elusive said as "helps it hit" and "gives keyword").
   Rule: L10. Games: Runeterra. Files: d1 cB
   - Ruined Rex -> Cannon Barrage: puts it into play: plays; also casts its skill
        [runeterra] line now: puts: plays; puts: casts its skill
        Ruined Rex: WHEN played of self DO play_card random enemy unit in board <Cannon Barrage> (times=event_count of (drawn by mine player) this_round, max=6)
        Cannon Barrage: KW: Skill | WHEN played of self DO damage chosen unit in board (amount=2) THEN damage enemy player (amount=1)
   - Ghost -> Zed: helps it level up: helps it hit the enemy player (levels it up); also gives keyword: can give it Elusive
        [runeterra] line now: levels: helps it hit the enemy player (levels it up); keyword: can give it Elusive
        Ghost: WHEN played of self DO give_keyword chosen mine unit in board <Elusive> for this_round
        Zed: KW: Quick Attack, Attack | WHEN attacks by self DO summon chosen mine unit in board <Living Shadow> (power=stat power of (self), health=stat health of (self)) THEN start_attack it | WHEN always IF event_count strikes_nexus by chosen mine unit [card in Zed] [card in Living Shadow] of enemy player ge 2 this_game DO level_up self
        case n261: expect line (levels it up) (Claude 31 Oct 2026: Elusive gets Zed to the Nexus)

12. Wrong thinking: giving Stun (or another Stun-type act) is said as both "enables" and "triggers" in one line, although the receiver has only reaction rows.
   Rule: L10. Games: Runeterra. Files: d4 cC12
   - Steel Tempest -> Fae Bladetwirler: enables: makes units get Stun; also triggers: makes units get Stun
        [runeterra] line now: type: makes units get Stun; waits: makes units get Stun
        Steel Tempest: WHEN played of self DO stun chosen enemy unit in board [state is attacking] for this_round
        Fae Bladetwirler: KW: Quick Attack | WHEN given_keyword by mine player of unit [keyword is Stun] DO stat_change self (power=2) for permanent | WHEN recalled by mine player of unit DO stat_change self (power=2) for permanent
   - Steel Tempest -> Yasuo (level 2): enables: makes enemy units get Stun; also triggers: makes enemy units get Stun
        [runeterra] line now: type: makes enemy units get Stun; waits: makes enemy units get Stun
        Steel Tempest: WHEN played of self DO stun chosen enemy unit in board [state is attacking] for this_round
        Yasuo (level 2): KW: Quick Attack | WHEN given_keyword by mine player of enemy unit [keyword is Stun] DO strike self to it | WHEN recalled by mine player of enemy unit DO strike self to it
   - Malphite (level 2) -> Yasuo: helps it level up: makes units get Stun (levels it up); also enables: makes enemy units get Stun; also triggers: makes enemy units get Stun
        [runeterra] line now: levels: makes units get Stun (levels it up); type: makes enemy units get Stun; waits: makes enemy units get Stun
        Malphite (level 2): KW: Tough | WHEN played of self DO stun chosen enemy unit in board for this_round | WHEN summoned of self IF attack_token is DO create in hand <Unstoppable Force> | WHEN round_start IF attack_token is DO create in hand <Unstoppable Force>
        Yasuo: KW: Quick Attack | WHEN given_keyword by mine player of enemy unit [keyword is Stun] DO damage it (amount=2) | WHEN recalled by mine player of enemy unit DO damage it (amount=2) | WHEN always IF amount sum (event_count of (given_keyword by mine player of unit [state is stunned]) this_game + event_count of (recalled by mine player of unit) this_game) ge 5 DO level_up self

13. Wrong thinking: a trigger-and-count card gets both "waits: is a spell whose playing sets off its effect" and "type: is a spell it needs played for its count".
   Rule: L10. Games: Runeterra. Files: a c3
   - Absorb Soul -> Claws of the Dragon: WHEN played by mine player of spell IF event_count played by mine player of spell ge 2 this_round DO summon self
        [runeterra] line now: type: is a spell it needs played for its count; waits: is a spell whose playing sets off its effect
        Absorb Soul: WHEN played of self DO keyword_action chosen mine unit in board <Drain> (amount=4) for unstated
        Claws of the Dragon: WHEN played by mine player of spell IF event_count played by mine player of spell ge 2 this_round DO summon self in board
   - Accelerated Purrsuit -> Fleet Admiral Shelly: WHEN played by mine player of spell [once_per_round] IF event_count ... ge 2 this_round
        [runeterra] line now: type: is a spell it needs played for its count; waits: is a spell whose playing sets off its effect
        Accelerated Purrsuit: KW: Slow | WHEN played of self IF event_count played by mine player of card [state is new] ge 15 this_game DO summon <Catastrophe>
        Fleet Admiral Shelly: KW: Elusive, Imbue | WHEN played by mine player of spell [once_per_round] IF event_count played by mine player of spell ge 2 this_round DO stat_change all mine unit in board [card not Fleet Admiral Shelly] (power=1, health=1) for permanent

## D. Stat help and damage help to cards that do not read it

14. Wrong thinking: "stronger: more power (and health)" is given to a card whose rows do not read power or health (no rows, only Fearsome/Overwhelm/Lifesteal/Quick Attack, fixed damage, or a fight start).
   Rule: L14, L18. Games: Runeterra. Files: a c10, a c15, d1 cC, d4 cC6, v3a c5, v3d3 c1
   - Battlesmith -> Blocking Badgerbear: stronger: gives it more power and health when it comes [Blocking Badgerbear: (no rows)]
        [runeterra] line now: stronger: gives it more power and health when it comes
        Battlesmith: WHEN summoned by mine player of it mine unit [type is Elite] DO stat_change it (power=1, health=1) for permanent
        Blocking Badgerbear: (no rows)
   - Arachnoid Host -> Arachnoid Horror [Arachnoid Host: WHEN summoned of self DO stat_change all mine unit in board [card not Arachnoid Host] [type is Spider] (power=2) for permanent; Arachnoid Horror: KW: Fearsome]
        (cards not found by these names)
   - Rek'Sai -> Sharkling: makes stronger: gives it more power
        [runeterra] line now: stronger: gives it more power
        Rek'Sai: KW: Lurk | WHEN keyword_used by self of keyword [keyword is Lurk] DO stat_change all mine unit in everywhere [type is Lurker] (power=1) for permanent | WHEN attacks by self DO stat_change all mine unit in everywhere [type is Lurker] (power=1) for permanent | WHEN round_end DO shuffle_into_deck self in deck | WHEN always IF event_count attacks by self power ge 10 this_game DO level_up self
        Sharkling: KW: Lurk
   - Poppy -> Radiant Guardian: makes stronger: gives it more power and health
        [runeterra] line now: stronger: gives it more power and health
        Poppy: KW: Attack | WHEN attacks by self DO stat_change all mine unit in board [power le stat power of (self)] (power=1, health=1) for permanent | WHEN always IF event_count attacks by self ge 3 this_game DO level_up self
        Radiant Guardian: WHEN summoned of self IF event_count dies of mine unit ge 1 this_round DO give_keyword self <Lifesteal> for permanent THEN give_keyword self <Tough> for permanent

15. Wrong thinking: "stronger: more power" from a card that only has the keyword Hallowed to a card that reads its own power when played.
   Rule: L2, L4, L15, L18. Games: Runeterra. Files: a c2
   - Ghastly Band -> Banana Blaster [Ghastly Band: KW: Hallowed, Ephemeral]
        (cards not found by these names)
   - Ghostly Paramour -> Dashing Dandy [KW: Hallowed, Lifesteal]
        (cards not found by these names)
   - Boisterous Host -> Adnere's Aviarists [KW: Hallowed]
        (cards not found by these names)

16. Wrong thinking: more damage / more power is called "enables: more damage" or "its damage gets 1 more" for a plain damage or kill spell that does not read the damage.
   Rule: L18, L4. Games: Runeterra. Files: a c13, d3 cA
   - Deluge -> Avalanche: stronger: its damage gets 1 more [Deluge: WHEN played of self DO give_ability mine player for permanent; Avalanche: WHEN played of self DO damage all unit in board (amount=2)]
        [runeterra] line now: stronger: its damage gets 1 more
        Deluge: WHEN played of self DO give_ability mine player for permanent
        Avalanche: WHEN played of self DO damage all unit in board (amount=2)
   - Might -> Scorched Earth: enables: more damage
        [runeterra] line now: type: more damage
        Might: WHEN played of self DO stat_change chosen mine unit in board (power=3) for this_round THEN give_keyword it <Overwhelm> for this_round
        Scorched Earth: WHEN played of self DO kill chosen unit in board [state is damaged] OR kill chosen landmark in board

17. Wrong thinking: a unit's own power or Overwhelm (with no damage text) "enables more damage" for Ravenous Flock, which needs a damaged or stunned unit.
   Rule: L2, L18. Games: Runeterra. Files: d2 cQ, v3d3 c3
   - Sion -> Ravenous Flock: enables: more damage
        [runeterra] line now: type: more damage
        Sion: KW: Overwhelm | WHEN discarded of self DO give_keyword highest mine unit by power in board <Overwhelm> for permanent THEN move self in deck | WHEN always DO stat_change self (power=event_count of (discarded by mine player of card) this_game, max=7) for while | WHEN always IF amount sum (event_count power of (discarded by mine player of card) this_game + event_count power of (summoned by mine player of mine unit) this_game) ge 35 DO level_up self
        Ravenous Flock: WHEN played of self DO damage chosen unit in board [state in damaged] [state in stunned] (amount=4)
   - Sion (level 2) -> Ravenous Flock: enables: more damage
        [runeterra] line now: type: more damage
        Sion (level 2): KW: Overwhelm, Last Breath | WHEN dies of self DO summon in board <Sion Returned> | WHEN discarded of self DO give_keyword highest mine unit by power in board <Overwhelm> for permanent THEN shuffle_into_deck self in deck
        Ravenous Flock: WHEN played of self DO damage chosen unit in board [state in damaged] [state in stunned] (amount=4)

18. Wrong thinking: "doubles its damage" is given to a card that has no damage text, or whose damage is not taken by the doubling card.
   Rule: L2, L18. Games: Runeterra. Files: a c19, v3d2 c7
   - The Dreadway -> Darkwater Scourge: stronger: doubles its damage [The Dreadway: KW: Fearsome | WHEN damaged by mine spell DO damage it (amount=event_amount) | WHEN damaged by mine unit DO damage it (amount=event_amount); Darkwater Scourge: KW: Ephemeral, Lifesteal]
        [runeterra] line now: stronger: doubles its damage
        The Dreadway: KW: Fearsome | WHEN summoned of self DO draw mine card in deck [card is Gangplank] (amount=1) | WHEN damaged by mine spell DO damage it (amount=event_amount) | WHEN damaged by mine unit DO damage it (amount=event_amount)
        Darkwater Scourge: KW: Ephemeral, Lifesteal
   - The Dreadway -> Gangplank: also makes stronger: doubles its damage [Gangplank level 1: Overwhelm, summon Powder Keg, level up]
        [runeterra] line now: puts: draws it from the deck; levels: damages the enemy player (levels it up); levels: helps it hit the enemy player (levels it up); stronger: doubles its damage
        The Dreadway: KW: Fearsome | WHEN summoned of self DO draw mine card in deck [card is Gangplank] (amount=1) | WHEN damaged by mine spell DO damage it (amount=event_amount) | WHEN damaged by mine unit DO damage it (amount=event_amount)
        Gangplank: KW: Overwhelm | WHEN summoned of self DO summon in board <Powder Keg> | WHEN always IF event_count nexus_damaged of enemy player ge 5 different_rounds DO level_up self

19. Wrong thinking: "makes its effect bigger" is given to a card that has no number to enlarge.
   Rule: L4, L14, L18. Games: Runeterra. Files: a c14, d3 cD
   - Alatis the Gallant -> Dragonling: stronger: makes its effect bigger [Dragonling: KW: Ephemeral, Lifesteal]
        [runeterra] line now: stronger: makes its effect bigger
        Alatis the Gallant: KW: Fury | WHEN always DO increase_effect all mine unit in board [type is Dragon] for while
        Dragonling: KW: Ephemeral, Lifesteal
   - Powder Keg -> Paralyzing Bite: makes stronger: makes its effect bigger
        [runeterra] line now: stronger: makes its effect bigger
        Powder Keg: KW: Immobile, Vulnerable | WHEN always DO increase_effect all mine spell [category in spell] [category in skill] (amount=1) for while | WHEN damaged by mine spell [category in spell] [category in skill] of enemy any DO kill self
        Paralyzing Bite: KW: Skill | WHEN played of self DO stun chosen enemy unit in board for this_round
   - Powder Keg -> Scorched Earth: makes stronger: makes its effect bigger
        [runeterra] line now: stronger: makes its effect bigger
        Powder Keg: KW: Immobile, Vulnerable | WHEN always DO increase_effect all mine spell [category in spell] [category in skill] (amount=1) for while | WHEN damaged by mine spell [category in spell] [category in skill] of enemy any DO kill self
        Scorched Earth: WHEN played of self DO kill chosen unit in board [state is damaged] OR kill chosen landmark in board

20. Wrong thinking: power lines point to Master Yi (level 2), whose text does not read the damage it deals, while Master Yi (level 1), which does read it, has none of them.
   Rule: L18, L14. Games: Runeterra. Files: d4 cC9
   - Mentor of the Stones -> Master Yi (level 2): makes stronger: more power: its text uses the damage it deals
        [runeterra] line now: stronger: more power: its text uses the damage it deals
        Mentor of the Stones: KW: Last Breath, Support | WHEN supports by self DO stat_change right_of_self (power=2, health=2) for permanent | WHEN dies of self DO create in hand <Gem> (amount=3)
        Master Yi (level 2): KW: Quick Attack, Flow, Attack | WHEN attacks by self DO strike self to lowest enemy unit by power in board | WHEN round_start DO cost_change chosen mine spell in hand (cost=-1) for permanent | WHEN round_start IF keyword_condition Flow DO stat_change all mine unit in everywhere [name_has is Master Yi] (power=2) for permanent
   - Gem -> Master Yi (level 2): makes stronger: more power: its text uses the damage it deals
        [runeterra] line now: stronger: more power: its text uses the damage it deals
        Gem: KW: Focus | WHEN played of self DO heal chosen mine unit in board (amount=1) THEN stat_change it (power=1) for permanent
        Master Yi (level 2): KW: Quick Attack, Flow, Attack | WHEN attacks by self DO strike self to lowest enemy unit by power in board | WHEN round_start DO cost_change chosen mine spell in hand (cost=-1) for permanent | WHEN round_start IF keyword_condition Flow DO stat_change all mine unit in everywhere [name_has is Master Yi] (power=2) for permanent
   - Divine Judgment -> Master Yi (level 2): makes stronger: can give it more power
        [runeterra] line now: stronger: can give it more power
        Divine Judgment: WHEN played of self DO cant chosen mine unit in board (event=damaged) for this_round THEN cant it (event=dies) for this_round THEN stat_change all mine unit in board (power=1) for this_round
        Master Yi (level 2): KW: Quick Attack, Flow, Attack | WHEN attacks by self DO strike self to lowest enemy unit by power in board | WHEN round_start DO cost_change chosen mine spell in hand (cost=-1) for permanent | WHEN round_start IF keyword_condition Flow DO stat_change all mine unit in everywhere [name_has is Master Yi] (power=2) for permanent
   - Pale Cascade -> Master Yi (level 2): makes stronger: can give it more power and health
        [runeterra] line now: stronger: can give it more power and health
        Pale Cascade: KW: Nightfall | WHEN played of self DO stat_change chosen mine unit in board (power=1, health=1) for this_round | WHEN played of self IF keyword_condition Nightfall DO draw mine card in deck_top (amount=1)
        Master Yi (level 2): KW: Quick Attack, Flow, Attack | WHEN attacks by self DO strike self to lowest enemy unit by power in board | WHEN round_start DO cost_change chosen mine spell in hand (cost=-1) for permanent | WHEN round_start IF keyword_condition Flow DO stat_change all mine unit in everywhere [name_has is Master Yi] (power=2) for permanent

21. Wrong thinking: damage that hurts my own units (a drawback paid for a draw) is doubled as a help.
   Rule: L5. Games: Runeterra. Files: v3d1 c5
   - The Dreadway -> Fortune Croaker: makes stronger: doubles its damage
        [runeterra] line now: stronger: doubles its damage
        The Dreadway: KW: Fearsome | WHEN summoned of self DO draw mine card in deck [card is Gangplank] (amount=1) | WHEN damaged by mine spell DO damage it (amount=event_amount) | WHEN damaged by mine unit DO damage it (amount=event_amount)
        Fortune Croaker: WHEN played of self DO damage self (amount=1) THEN damage chosen mine unit in board (amount=1) THEN draw mine card in deck_top (amount=1)

22. Wrong thinking: a card that only starts its own attack is given a stat change it does not make.
   Rule: L3, L6. Games: Runeterra. Files: v3d3 c2
   - Snapjaw Swarm -> Xerxa'Reth, The Undertitan: enables: changes its stats for its effect; also makes stronger: more power
        [runeterra] line now: type: changes its stats for its effect; stronger: more power
        Snapjaw Swarm: KW: Lurk | WHEN played of self DO start_attack self
        Xerxa'Reth, The Undertitan: KW: Lurk, Attack | WHEN attacks by self IF stat self power ge 8 DO give_keyword self <Fearsome> for this_round THEN give_keyword self <Overwhelm> for this_round THEN give_keyword self <SpellShield> for this_round

## E. Draws, creations and summons by kind

23. Wrong thinking: a draw by kind or by a cost filter that half the cards pass is a named "draws it from the deck" line.
   Rule: L1b, L21. Games: Runeterra. Files: a c11, d2 cH, d3 cC, v3d1 c6
   - Zap Sprayfin -> Make it Rain: puts it into play: draws it from the deck
        [runeterra] line now: puts: draws it from the deck
        Zap Sprayfin: KW: Elusive, Attune | WHEN summoned of self DO draw random mine card in deck [category is spell] [cost le 3] (amount=1)
        Make it Rain: WHEN played of self DO damage 3 random enemy unit in board (amount=1) OR damage enemy player (amount=1)
   - Zap Sprayfin -> Warning Shot: puts it into play: draws it from the deck
        [runeterra] line now: puts: draws it from the deck
        Zap Sprayfin: KW: Elusive, Attune | WHEN summoned of self DO draw random mine card in deck [category is spell] [cost le 3] (amount=1)
        Warning Shot: WHEN played of self DO damage enemy player (amount=1)
   - Zap Sprayfin -> Scorched Earth: puts it into play: draws it from the deck
        [runeterra] line now: puts: draws it from the deck
        Zap Sprayfin: KW: Elusive, Attune | WHEN summoned of self DO draw random mine card in deck [category is spell] [cost le 3] (amount=1)
        Scorched Earth: WHEN played of self DO kill chosen unit in board [state is damaged] OR kill chosen landmark in board
   - Dragon Allegiant -> Fused Firebrand [Dragon Allegiant: WHEN summoned of self IF keyword_condition Behold DO draw random mine card in deck [type is Dragon]; Fused Firebrand: KW: Fury, SpellShield]
        (cards not found by these names)

24. Wrong thinking: a draw or a summon from hand or deck is linked to a level 2 form, which no player can own in hand or deck.
   Rule: L9. Games: Runeterra. Files: v3a c2, d4 cC8, a c11
   - Realm Warp -> Elder Dragon (level 2): draws it and keeps it [Elder Dragon (level 2): KW: Fury]
        [runeterra] line now: puts: draws it and keeps it
        Realm Warp: KW: Burst | WHEN played of self DO draw mine card in deck_top (amount=3) THEN discard it mine card in hand [category is follower]
        Elder Dragon (level 2): KW: Fury
   - Thresh (level 2) -> Hecarim (level 2): triggers: makes it attack for its effect
        [runeterra] line now: waits: makes it attack for its effect
        Thresh (level 2): KW: Challenger | WHEN attacks by self [once_per_game] DO summon chosen mine unit in deck [category is champion] in board OR summon chosen mine unit in hand [category is champion] in board THEN start_attack it
        Hecarim (level 2): KW: Overwhelm, Attack | WHEN levels_up of self DO give_ability mine player | WHEN attacks by self DO summon mine unit <Spectral Rider> (amount=2) THEN start_attack it
   - Realm Warp -> Darius (level 2) [Realm Warp: draw mine card in deck_top (amount=3) THEN discard it ... [category is follower]; Darius (level 2): KW: Overwhelm]
        (cards not found by these names)

25. Wrong thinking: a card that creates cards is linked to a need that asks for a kind the created card is not.
   Rule: L20, L3, L17. Games: Runeterra. Files: a c5, a c8, v3a c1
   - Angel -> Cunning Kitten: type: creates cards [Angel: WHEN played of self IF keyword_condition Plunder DO create in hand <Coin> (amount=3); Cunning Kitten: WHEN summoned of self IF it_matches [state is created] DO draw ... THEN stat_change self]
        [runeterra] line now: type: creates cards
        Angel: KW: Brash, Plunder | WHEN played of self IF keyword_condition Plunder DO create in hand <Coin> (amount=3)
        Cunning Kitten: WHEN summoned of self IF it_matches [state is created] DO draw mine card in deck_top (amount=1) THEN stat_change self (power=2, health=1) for permanent
   - Acoustician -> The World Ender [Acoustician: WHEN strikes by self DO create random mine card [category is spell] [cost eq 2] [state is new] in hand; The World Ender: ... distinct card of (played by mine player of any [type is Darkin] [card not Aatrox]) ...]
        (cards not found by these names)
   - Acoustician -> Norra: levels: creates cards (levels it up) [Norra: WHEN always IF event_count summoned of mine unit [state is created] ge 6 this_game DO level_up self]
        [runeterra] line now: levels: creates cards (levels it up)
        Acoustician: WHEN strikes by self DO create random mine card [category is spell] [cost eq 2] [state is new] in hand
        Norra: KW: Elusive | WHEN strikes_nexus by self DO keyword_action 4 top mine card in deck <Mysterious Portal Plant> (amount=1) | WHEN always IF event_count summoned of mine unit [state is created] ge 6 this_game DO level_up self
   - Angel -> The World Ender [The World Ender: ... distinct card of (played by mine player of any [type is Darkin] [card not Aatrox]) ...]
        (cards not found by these names)

26. Wrong thinking: a card that makes cards is linked to a card that goes off on ANY card played.
   Rule: L1, L1b, L19. Games: Runeterra. Files: a c7, d4 cC2
   - Angel -> The Swindler's Den: waits: makes more cards to play [The Swindler's Den: WHEN played by mine player of card DO draw mine card in deck_top (amount=1)]
        [runeterra] line now: waits: makes more cards to play
        Angel: KW: Brash, Plunder | WHEN played of self IF keyword_condition Plunder DO create in hand <Coin> (amount=3)
        The Swindler's Den: KW: Landmark | WHEN always DO give_keyword all mine card in hand <Fleeting> for while | WHEN played by mine player of card DO draw mine card in deck_top (amount=1)
   - Babbling Balladeers -> Valley of Imitation: waits: makes more cards to play [WHEN played by mine player of unit [category is follower] DO transform self to it]
        [runeterra] line now: waits: makes more cards to play
        Babbling Balladeers: WHEN summoned of self DO create in hand <Hungry Owlcat>
        Valley of Imitation: KW: Landmark | WHEN played by mine player of unit [category is follower] DO transform self to it for this_round
   - Avarosan Trapper -> Marai Reef Spire: waits: makes more cards to play [WHEN mana_spent by mine player of unit DO mana_gain mine spell_mana (amount=1)]
        [runeterra] line now: waits: makes more cards to play
        Avarosan Trapper: WHEN summoned of self DO create in deck_top <Enraged Yeti> (amount=3)
        Marai Reef Spire: KW: Landmark | WHEN mana_spent by mine player of unit DO mana_gain mine spell_mana (amount=1)
   - Aphelios -> The Veiled Temple: triggers: makes more cards to play
        [runeterra] line now: waits: makes more cards to play
        Aphelios: KW: Nightfall | WHEN played of self IF keyword_condition Nightfall DO choose_card mine card [name_has is Moon Weapon] (options=1) THEN create it in hand | WHEN played by mine player of [card not Aphelios] [first_each_round] IF event_count played by mine player ge 2 this_round; have mine card in hand [type is Moon Weapon] not DO create in hand | WHEN always IF event_count played by mine player of [name_has is Moon Weapon] ge 4 this_game DO level_up self
        The Veiled Temple: KW: Landmark | WHEN played by mine player of card [first_each_round] IF event_count played by mine player of card ge 2 this_round DO mana_gain mine mana (amount=2) THEN stat_change highest mine unit by power in board (power=1) for permanent

27. Wrong thinking: creating cards of a kind into hand or deck is "makes a Lurker it asks for" (a draw by kind).
   Rule: L1b, L19. Games: Runeterra. Files: d1 cE
   - Call the Pack -> Frenzied Feast: enables: makes a Lurker it asks for
        [runeterra] line now: type: makes a Lurker it asks for
        Call the Pack: KW: Lurk | WHEN played of self DO put_on_top chosen mine card in hand in deck_top THEN create 2 random unit [type is Lurker] in hand
        Frenzied Feast: KW: Skill | WHEN played of self DO strike all mine unit in board [type is Lurker] to random enemy unit in board
   - Bloodbait -> Frenzied Feast: enables: makes a Lurker it asks for
        [runeterra] line now: type: makes a Lurker it asks for
        Bloodbait: KW: Lurk | WHEN played of self DO create in deck_top <Snapjaw Swarm>
        Frenzied Feast: KW: Skill | WHEN played of self DO strike all mine unit in board [type is Lurker] to random enemy unit in board
   - Rek'Sai (level 2) -> Frenzied Feast: enables: is a Lurker it asks for; also makes a Lurker it asks for
        [runeterra] line now: type: is a Lurker it asks for; type: makes a Lurker it asks for
        Rek'Sai (level 2): KW: Lurk, Overwhelm | WHEN levels_up of self DO create random card [type is Lurker] in hand (amount=3) | WHEN keyword_used by self of keyword [keyword is Lurk] DO stat_change all mine card in everywhere [type is Lurker] (power=1) for permanent | WHEN attacks by self DO stat_change all mine card in everywhere [type is Lurker] (power=1) for permanent
        Frenzied Feast: KW: Skill | WHEN played of self DO strike all mine unit in board [type is Lurker] to random enemy unit in board

28. Wrong thinking: "fills your hand" (draw of the top card, creation of cheap cards) is linked to a card that counts only cost 8+ cards in hand.
   Rule: L1, L1b, L19. Games: Runeterra. Files: d2 cL, v3d2 c3
   - Avarosan Sentry -> Trundle (level 2): triggers: fills your hand
        [runeterra] line now: waits: fills your hand
        Avarosan Sentry: KW: Last Breath | WHEN dies of self DO draw mine card in deck_top (amount=1)
        Trundle (level 2): KW: Overwhelm, Regeneration, Attack | WHEN summoned of self DO create in hand <Ice Pillar> | WHEN attacks by self IF keyword_condition Behold mine card in hand [cost ge 8] DO stat_change self (power=count of (mine card in hand [cost ge 8])) for permanent
   - Three Sisters -> Trundle (level 2): triggers: fills your hand
        [runeterra] line now: waits: fills your hand
        Three Sisters: WHEN played of self DO choose_one OR create in hand <Flash Freeze> OR create in hand <Fury of the North> OR create in hand <Entomb> THEN give_keyword it <Fleeting> for permanent
        Trundle (level 2): KW: Overwhelm, Regeneration, Attack | WHEN summoned of self DO create in hand <Ice Pillar> | WHEN attacks by self IF keyword_condition Behold mine card in hand [cost ge 8] DO stat_change self (power=count of (mine card in hand [cost ge 8])) for permanent

29. Wrong thinking: a copy put into the deck is a use for a plain unit.
   Rule: L19. Games: Runeterra. Files: a c17
   - Nautilus -> Alpha Wildclaw: puts: copies it [Nautilus: WHEN levels_up of self DO copy all mine unit in removed [cost ge 4] in deck; Alpha Wildclaw: KW: Overwhelm]
        [runeterra] line now: puts: copies it
        Nautilus: KW: Tough, Fearsome | WHEN always IF keyword_condition Deep DO level_up self | WHEN levels_up of self DO copy all mine unit in removed [cost ge 4] in deck
        Alpha Wildclaw: KW: Overwhelm

## F. Sides, kinds, levels and rows

30. Wrong thinking: an effect on the enemy side (or a need about the enemy) is linked to the opposite side's need.
   Rule: L9, L7. Games: Runeterra. Files: a c18, v3a c3, d4 cC11, d2 cO
   - Avalanche -> Petricite Charger: waits: damages it for its effect [Petricite Charger: WHEN damaged by enemy spell of self DO negate_damage self]
        [runeterra] line now: waits: damages it for its effect
        Avalanche: WHEN played of self DO damage all unit in board (amount=2)
        Petricite Charger: KW: Formidable | WHEN damaged by enemy spell [category in spell] [category in skill] of self DO negate_damage self
   - Early Bird -> Noble Rebel [Early Bird: ... DO discard highest_cost enemy card in hand; Noble Rebel: ... event_count discarded by mine player ge 3 ...]
        (cards not found by these names)
   - Yasuo (level 2) -> Blue Sentinel: triggers: kills it for its death effect
        [runeterra] line now: waits: kills it for its death effect
        Yasuo (level 2): KW: Quick Attack | WHEN given_keyword by mine player of enemy unit [keyword is Stun] DO strike self to it | WHEN recalled by mine player of enemy unit DO strike self to it
        Blue Sentinel: KW: Last Breath | WHEN dies of self DO summon <Crest of Insight>
   - Powder Keg -> Poison Puffcap: makes stronger: makes its effect bigger
        [runeterra] line now: stronger: makes its effect bigger
        Powder Keg: KW: Immobile, Vulnerable | WHEN always DO increase_effect all mine spell [category in spell] [category in skill] (amount=1) for while | WHEN damaged by mine spell [category in spell] [category in skill] of enemy any DO kill self
        Poison Puffcap: KW: Trap | WHEN played of self DO damage mine player (amount=1)

31. Wrong thinking: a landmark put into play is called "puts your units into play".
   Rule: L8, L10. Games: Runeterra. Files: d2 cB, v3d1 c3
   - Akshan -> Shaped Stone: enables: puts your units into play
        [runeterra] line now: type: puts your units into play
        Akshan: KW: Quick Attack | WHEN summoned of self IF have mine landmark [card is Warlord's Palace] not DO summon in board <Warlord's Palace> | WHEN summoned of self IF have mine landmark [card is Warlord's Palace] is DO countdown_advance mine landmark [card is Warlord's Palace] (amount=1) | WHEN strikes by self IF have mine landmark [card is Warlord's Palace] not DO summon in board <Warlord's Palace> | WHEN strikes by self IF have mine landmark [card is Warlord's Palace] is DO countdown_advance mine landmark [card is Warlord's Palace] (amount=1) | WHEN always IF event_count countdown_done of mine landmark [card is Warlord's Palace] ge 1 this_game DO level_up self | WHEN levels_up of self DO summon in board <Warlord's Hoard>
        Shaped Stone: WHEN played of self IF event_count summoned of mine landmark lt 1 this_game DO stat_change chosen mine unit in board (power=1, health=1) for this_round | WHEN played of self IF event_count summoned of mine landmark ge 1 this_game DO stat_change chosen mine unit in board (power=2, health=1) for this_round
   - Akshan (level 2) -> Shaped Stone: enables: puts your units into play
        [runeterra] line now: type: puts your units into play
        Akshan (level 2): KW: Quick Attack | WHEN summoned of self DO choose_one mine player OR summon in board <Warlord's Hoard> OR countdown_advance mine landmark [card is Warlord's Hoard] (amount=1) | WHEN strikes by self DO choose_one mine player OR summon in board <Warlord's Hoard> OR countdown_advance mine landmark [card is Warlord's Hoard] (amount=1)
        Shaped Stone: WHEN played of self IF event_count summoned of mine landmark lt 1 this_game DO stat_change chosen mine unit in board (power=1, health=1) for this_round | WHEN played of self IF event_count summoned of mine landmark ge 1 this_game DO stat_change chosen mine unit in board (power=2, health=1) for this_round

32. Wrong thinking: a hit that only aims at units is credited with killing a landmark.
   Rule: L8, L16. Games: Runeterra. Files: d2 cC, v3d1 c4
   - Noxian Fervor -> Scrappy Bomb: triggers: kills it for its death effect
        [runeterra] line now: waits: kills it for its death effect
        Noxian Fervor: WHEN played of self DO damage chosen mine unit in board (amount=3) THEN damage chosen unit in board (amount=3)
        Scrappy Bomb: KW: Countdown, Landmark | WHEN countdown_done DO damage enemy player (amount=1) | WHEN dies of self DO damage enemy player (amount=1)

33. Wrong thinking: a keyword given to a kind (Spiders) is a use for a card whose text does not use it.
   Rule: L14, L15. Games: Runeterra. Files: d2 cM, v3d2 c4
   - Spider Queen Elise (level 2) -> Spiderling: gives keyword: gives it Challenger; also gives it Fearsome
        [runeterra] line now: keyword: gives it Challenger; keyword: gives it Fearsome
        Spider Queen Elise (level 2): KW: Fearsome, Challenger | WHEN always DO give_keyword all mine unit in board [type is Spider] [card not Spider Queen Elise (level 2)] <Challenger> for while THEN give_keyword all mine unit in board [type is Spider] [card not Spider Queen Elise (level 2)] <Fearsome> for while
        Spiderling: (no rows)

34. Wrong thinking: a level 1 card gets a line from its level 2 text.
   Rule: L1. Games: Runeterra. Files: d2 cI
   - Gangplank -> Powderful Explosion: puts it into play: casts its skill
        [runeterra] line now: puts: casts its skill
        Gangplank: KW: Overwhelm | WHEN summoned of self DO summon in board <Powder Keg> | WHEN always IF event_count nexus_damaged of enemy player ge 5 different_rounds DO level_up self
        Powderful Explosion: KW: Skill | WHEN played of self DO damage all enemy unit in board (amount=1) THEN damage enemy player (amount=1)

35. Wrong thinking: a card that gives Ephemeral only to its own copy is linked as if it killed other cards.
   Rule: L14, L9. Games: Runeterra. Files: d4 cC10
   - Prancing Sea Spirits -> Ceaseless Sentry: triggers: kills it for its death effect
        [runeterra] line now: waits: kills it for its death effect
        Prancing Sea Spirits: KW: Elusive | WHEN played of self DO copy self in board THEN give_keyword it <Ephemeral> for permanent
        Ceaseless Sentry: KW: Last Breath | WHEN dies of self DO draw chosen mine card in deck_top (amount=1)
   - Prancing Sea Spirits -> Hapless Aristocrat: triggers: kills it for its death effect
        [runeterra] line now: waits: kills it for its death effect
        Prancing Sea Spirits: KW: Elusive | WHEN played of self DO copy self in board THEN give_keyword it <Ephemeral> for permanent
        Hapless Aristocrat: KW: Last Breath | WHEN dies of self DO summon in board <Spiderling>

36. Wrong thinking: the Countdown keyword of one landmark finishes another landmark's countdown.
   Rule: L15. Games: Runeterra. Files: v3a c6
   - Buried Armory -> Stormcarved Spire [Buried Armory: KW: Landmark, Countdown | WHEN countdown_done DO create in hand <Treasure of the Sands>; Stormcarved Spire: KW: Landmark, Countdown | WHEN countdown_done DO copy it mine unit in attached in board]
        (cards not found by these names)

37. Wrong thinking: an Equipment card that only attaches "makes cards leave play" (a keyword's inner working read as the card's act).
   Rule: L1, L3, L15. Games: Runeterra. Files: a c16, v3a c4
   - Bone Club -> Papercraft Dragon (created): waits: makes cards leave play [Bone Club: KW: Equipment]
        [runeterra] line now: waits: makes cards leave play
        Bone Club: KW: Equipment
        Papercraft Dragon (created): KW: Attach, Double Attack | WHEN played of self DO attach self to chosen mine unit in board THEN stat_change attached_to (power=stat power of (self), health=stat health of (self)) for while_attached THEN copy_keywords attached_to to self for while_attached | WHEN leaves_play of attached_to DO keyword_action self <Recall> for unstated
   - Bone Club -> Quick Quill (created) [Bone Club: KW: Equipment; Quick Quill (created): ... WHEN leaves_play of attached_to DO keyword_action self <Recall>]
        (cards not found by these names)

38. Wrong thinking: board-position thinking from other games ("moves it within reach of the enemy player") is used for a swap of two allies.
   Rule: L4. Games: Runeterra. Files: v3a c7
   - Syncopation -> Acorn, the Hextechnician [Syncopation: WHEN played of self DO swap 2 chosen mine unit in board; Acorn: KW: Elusive | WHEN strikes_nexus by self ...]
        (cards not found by these names)

39. Wrong thinking: SpellShield (counters a spell) is a "survives damage" help for a card waiting to survive damage.
   Rule: L20, L2, L4, L6. Games: Runeterra. Files: a c4
   - Belvethi Elder -> Bone Scryer: waits: more health or protection: survives damage [Belvethi Elder: KW: Evolve, SpellShield]
        [runeterra] line now: waits: more health or protection: survives damage
        Belvethi Elder: KW: Evolve, SpellShield
        Bone Scryer: WHEN survives_damage of self DO damage enemy player (amount=1)
   - Hungry Owlcat -> Legion Veteran [Hungry Owlcat: KW: SpellShield]
        (cards not found by these names)
   - Fused Firebrand -> Crimson Disciple [KW: Fury, SpellShield]
        (cards not found by these names)
   - Belvethi Elder -> Braum: levels: more health or protection: survives damage (levels it up)
        [runeterra] line now: levels: more health or protection: survives damage (levels it up); waits: more health or protection: survives damage
        Belvethi Elder: KW: Evolve, SpellShield
        Braum: KW: Challenger, Regeneration | WHEN survives_damage of self [once_per_game] DO summon in board <Mighty Poro> | WHEN always IF event_count survives_damage of self damage ge 10 this_game DO level_up self

40. Wrong thinking: a cost RAISE (or fixed price) is read as "cheaper".
   Rule: L10. Games: Runeterra. Files: a c6
   - Mageseeker Junior -> Assembly Line: cheaper: pays for it [Mageseeker Junior: WHEN always DO cost_set card [category is spell] [cost lt 3] (cost=3) for while]
        [runeterra] line now: cheaper: pays for it: more mana or a lower cost
        Mageseeker Junior: WHEN always DO cost_set card [category is spell] [cost lt 3] (cost=3) for while
        Assembly Line: WHEN played of self DO summon <Forge Worker> (amount=2)
   - Mageseeker Junior -> Absorb Soul: cheaper: can cost set it
        [runeterra] line now: cheaper: can cost set it
        Mageseeker Junior: WHEN always DO cost_set card [category is spell] [cost lt 3] (cost=3) for while
        Absorb Soul: WHEN played of self DO keyword_action chosen mine unit in board <Drain> (amount=4) for unstated

41. Wrong thinking: a speed (Fast) given to a kind of spell is a use for a spell whose text does not use speed.
   Rule: L14. Games: Runeterra. Files: a c20
   - Senna (level 2) -> Absorb Soul: rules: gives it Fast [Absorb Soul: WHEN played of self DO keyword_action chosen mine unit in board <Drain> (amount=4)]
        [runeterra] line now: cheaper: makes it cheaper; rules: gives it Fast
        Senna (level 2): KW: Quick Attack | WHEN summoned of self IF have mine card in hand [card is Darkness] not DO create in hand <Darkness> | WHEN attacks by self IF have mine card in hand [card is Darkness] not DO create in hand <Darkness> | WHEN always DO give_keyword all mine spell [category in spell] [does in damage] [does in kill] <Fast> for while THEN cost_change all mine spell [category in spell] [does in damage] [does in kill] (cost=-1) for while
        Absorb Soul: WHEN played of self DO keyword_action chosen mine unit in board <Drain> (amount=4) for unstated

42. Wrong thinking: a discard-and-draw or discard-and-create card "empties your hand" for Jinx.
   Rule: L4. Games: Runeterra. Files: d3 cH
   - Rummage -> Jinx: helps it level up: empties your hand (levels it up)
        [runeterra] line now: levels: empties your hand (levels it up)
        Rummage: WHEN played of self DO discard chosen mine card in hand (amount=2) THEN draw mine card in deck_top (amount=count of (it mine card in discard))
        Jinx: KW: Quick Attack | WHEN always IF count all mine card in hand eq 0 now DO level_up self
   - Rummage -> Jinx (level 2): triggers: empties your hand
        [runeterra] line now: waits: empties your hand
        Rummage: WHEN played of self DO discard chosen mine card in hand (amount=2) THEN draw mine card in deck_top (amount=count of (it mine card in discard))
        Jinx (level 2): KW: Quick Attack | WHEN round_start DO draw mine card in deck_top (amount=1) | WHEN levels_up of self [first_each_round] DO create in hand <Super Mega Death Rocket!> | WHEN always [first_each_round] IF count all mine card in hand eq 0 now DO create in hand <Super Mega Death Rocket!>
   - Poro Cannon -> Jinx: helps it level up: empties your hand (levels it up)
        [runeterra] line now: levels: empties your hand (levels it up)
        Poro Cannon: WHEN played of self DO discard chosen mine card in hand (amount=1) THEN create in hand <Daring Poro> (amount=2)
        Jinx: KW: Quick Attack | WHEN always IF count all mine card in hand eq 0 now DO level_up self
   - Poro Cannon -> Jinx (level 2): triggers: empties your hand
        [runeterra] line now: waits: empties your hand
        Poro Cannon: WHEN played of self DO discard chosen mine card in hand (amount=1) THEN create in hand <Daring Poro> (amount=2)
        Jinx (level 2): KW: Quick Attack | WHEN round_start DO draw mine card in deck_top (amount=1) | WHEN levels_up of self [first_each_round] DO create in hand <Super Mega Death Rocket!> | WHEN always [first_each_round] IF count all mine card in hand eq 0 now DO create in hand <Super Mega Death Rocket!>

43. Wrong thinking: a plain hit on one target is linked to "killed by my spell" cards (kills units).
   Rule: L11. Games: Runeterra. Files: d2 cN, v3d2 c2
   - Piercing Darkness -> Buhru Sentinel: triggers: kills units
        [runeterra] line now: waits: kills units
        Piercing Darkness: KW: Slow | WHEN played of self DO keyword_action chosen unit in board <Drain> (amount=5) for unstated
        Buhru Sentinel: KW: Fearsome | WHEN killed by mine spell of unit [once_per_game] DO stat_change self (power=2, health=1) for permanent
   - Thermogenic Beam -> Buhru Sentinel: triggers: kills units
        [runeterra] line now: waits: kills units
        Thermogenic Beam: WHEN played of self DO spend_mana mine mana (amount=full of (mine mana)) THEN damage chosen unit in board (amount=event_amount)
        Buhru Sentinel: KW: Fearsome | WHEN killed by mine spell of unit [once_per_game] DO stat_change self (power=2, health=1) for permanent
   - Vile Feast -> Burgeoning Sentinel: triggers: kills units
        [runeterra] line now: waits: kills units
        Vile Feast: WHEN played of self DO keyword_action chosen unit in board <Drain> (amount=1) for unstated THEN summon in board <Spiderling>
        Burgeoning Sentinel: KW: Fearsome | WHEN killed by mine spell of unit [once_per_game] DO stat_change self (power=2, health=1) for permanent
   - Vile Feast -> Buhru Sentinel: triggers: kills units
        [runeterra] line now: waits: kills units
        Vile Feast: WHEN played of self DO keyword_action chosen unit in board <Drain> (amount=1) for unstated THEN summon in board <Spiderling>
        Buhru Sentinel: KW: Fearsome | WHEN killed by mine spell of unit [once_per_game] DO stat_change self (power=2, health=1) for permanent

44. Wrong thinking: every spell is a "triggers" line to Lux (level 2), which goes off only when ONE spell costs 6 or more.
   Rule: L17, L1. Games: Runeterra. Files: v3d3 c4
   - Conchologist -> Lux (level 2): triggers: makes a spell whose playing sets off its effect
        [runeterra] line now: waits: makes a spell whose playing sets off its effect
        Conchologist: WHEN played of self DO keyword_action card [category is spell] [region is own_regions] [cost le 3] in hand <Manifest> for unstated
        Lux (level 2): KW: Barrier | WHEN mana_spent by mine player of spell IF amount event_amount ge 6 DO create in hand <Final Spark>
   - Trinket Trade -> Lux (level 2): triggers: is a spell whose playing sets off its effect; also makes a spell whose playing sets off its effect
        [runeterra] line now: waits: is a spell whose playing sets off its effect; waits: makes a spell whose playing sets off its effect
        Trinket Trade: WHEN played of self DO choose_one self OR keyword_action card [card is Otterpus] in hand <Manifest> for unstated OR keyword_action card [category is spell] [region is own_regions] [cost le 3] in hand <Manifest> (options=2) for unstated
        Lux (level 2): KW: Barrier | WHEN mana_spent by mine player of spell IF amount event_amount ge 6 DO create in hand <Final Spark>
   - Pokey Stick -> Lux (level 2): triggers: is a spell whose playing sets off its effect
        [runeterra] line now: waits: is a spell whose playing sets off its effect
        Pokey Stick: WHEN played of self DO damage chosen any (amount=1) THEN draw mine card in deck_top (amount=1)
        Lux (level 2): KW: Barrier | WHEN mana_spent by mine player of spell IF amount event_amount ge 6 DO create in hand <Final Spark>
   - Concerted Strike -> Lux (level 2): triggers: is a spell whose playing sets off its effect
        [runeterra] line now: waits: is a spell whose playing sets off its effect
        Concerted Strike: WHEN played of self DO strike 2 chosen mine unit in board to chosen enemy unit in board
        Lux (level 2): KW: Barrier | WHEN mana_spent by mine player of spell IF amount event_amount ge 6 DO create in hand <Final Spark>

## G. Missed lines (a line that should exist is missing)

45. Wrong thinking: a line that should exist is missing: a kill on a chosen unit of either side feeds The Harrowing only for some cards.
   Rule: L10, L9. Games: Runeterra. Files: d1 cA
   - Soul Harvest -> The Harrowing: missing line [Soul Harvest: WHEN played of self DO choose_one OR kill chosen unit in board [category is follower] [power le 3] OR ...; Soul Harvest has only "Soul Harvest -> Ceaseless Sentry"]
        [runeterra] line now: NONE
        Soul Harvest: WHEN played of self DO choose_one OR kill chosen unit in board [category is follower] [power le 3] OR spend_mana mine mana (amount=3) THEN kill chosen unit in board [category is champion] [power le 3]
        The Harrowing: WHEN played of self DO revive 6 highest mine unit by power in discard THEN give_keyword it <Ephemeral> for permanent
   - (same deck, present) Glimpse Beyond -> The Harrowing: enables: makes your units die: The Harrowing brings them back
        (cards not found by these names)
   - (same deck, present) Disintegrate -> The Harrowing: enables: makes your units die
        (cards not found by these names)

46. Wrong thinking: a line that should exist is missing: strikes now have no line to Pyke's damage level-up.
   Rule: L2, L18. Games: Runeterra. Files: d1 cD
   - Bone Skewer -> Pyke: missing line [Bone Skewer: strike chosen mine unit in board to chosen enemy unit; 0 partners]
        [runeterra] line now: NONE
        Bone Skewer: WHEN played of self DO strike chosen mine unit in board to chosen enemy unit in board THEN move it in deck_top
        Pyke: KW: Lurk, Quick Attack | WHEN keyword_used of self [keyword is Lurk] DO transform self <Death From Below> | WHEN always IF event_count damaged by mine unit [name_has is Pyke] damage ge 15 this_game DO level_up self
   - Frenzied Feast -> Pyke: missing line [strike all mine unit [type is Lurker] to random enemy unit]
        [runeterra] line now: NONE
        Frenzied Feast: KW: Skill | WHEN played of self DO strike all mine unit in board [type is Lurker] to random enemy unit in board
        Pyke: KW: Lurk, Quick Attack | WHEN keyword_used of self [keyword is Lurk] DO transform self <Death From Below> | WHEN always IF event_count damaged by mine unit [name_has is Pyke] damage ge 15 this_game DO level_up self
   - Jaull-fish -> Pyke: missing line [strike all mine unit [type is Lurker] ...]
        [runeterra] line now: NONE
        Jaull-fish: KW: Lurk | WHEN played of self DO strike all mine unit in board [type is Lurker] to random enemy unit in board
        Pyke: KW: Lurk, Quick Attack | WHEN keyword_used of self [keyword is Lurk] DO transform self <Death From Below> | WHEN always IF event_count damaged by mine unit [name_has is Pyke] damage ge 15 this_game DO level_up self
   - Bone Skewer -> Pyke (level 2): missing line [Pyke (level 2): killed by self of enemy unit]
        [runeterra] line now: NONE
        Bone Skewer: WHEN played of self DO strike chosen mine unit in board to chosen enemy unit in board THEN move it in deck_top
        Pyke (level 2): KW: Lurk, Quick Attack | WHEN keyword_used by self of keyword [keyword is Lurk] DO transform self <Death From Below> | WHEN killed by self of enemy unit in board DO strike self to lowest enemy unit by power in board

47. Wrong thinking: a line that should exist is missing: the same planter row gives Byrd, The Bellringer -> Chime but no Esmus line.
   Rule: L3. Games: Runeterra. Files: d1 cF
   - Esmus, Breath of the World -> Chime: missing line "puts it into play: plants" [row: summoned of self DO keyword_action top mine card in deck_top <Chime Plant>]
        [runeterra] line now: puts: plants
        Esmus, Breath of the World: KW: Elusive, Support | WHEN summoned of self DO keyword_action top mine card in deck_top <Chime Plant> (amount=1) | WHEN supports by self DO stat_change it mine unit in board (power=1, health=1) for permanent
        Chime: KW: Boon | WHEN played of self DO stat_change random mine unit in hand (power=1, health=1) for permanent
   - (present, same row) Byrd, The Bellringer -> Chime
        (cards not found by these names)

48. Wrong thinking: a line that should exist is missing: a copy put into play (Mirror Image) sets off "when I'm summoned" cards.
   Rule: L19. Games: Runeterra. Files: d1 cH
   - Mirror Image -> Omen Hawk: missing line [Omen Hawk: summoned of self DO stat_change 2 top mine unit in deck; 0 partners]
        [runeterra] line now: NONE
        Mirror Image: KW: Slow | WHEN played of self DO copy chosen mine unit in board in board THEN give_keyword it mine unit in board <Ephemeral> for permanent
        Omen Hawk: WHEN summoned of self DO stat_change 2 top mine unit in deck (power=1, health=1) for permanent
   - Mirror Image -> Avarosan Hearthguard: missing line [summoned of self DO stat_change all mine unit in deck; 0 partners]
        [runeterra] line now: NONE
        Mirror Image: KW: Slow | WHEN played of self DO copy chosen mine unit in board in board THEN give_keyword it mine unit in board <Ephemeral> for permanent
        Avarosan Hearthguard: WHEN summoned of self DO stat_change all mine unit in deck (power=1, health=1) for permanent
   - Mirror Image -> Trifarian Assessor: missing line [summoned of self DO draw ...; 0 partners]
        [runeterra] line now: NONE
        Mirror Image: KW: Slow | WHEN played of self DO copy chosen mine unit in board in board THEN give_keyword it mine unit in board <Ephemeral> for permanent
        Trifarian Assessor: WHEN summoned of self DO draw mine card in deck_top (amount=count of (all mine unit in board [power ge 5]))
   - Mirror Image -> Incisive Tactician: missing line [summoned of self DO keyword_action <Rally>]
        [runeterra] line now: NONE
        Mirror Image: KW: Slow | WHEN played of self DO copy chosen mine unit in board in board THEN give_keyword it mine unit in board <Ephemeral> for permanent
        Incisive Tactician: KW: Reputation | WHEN always IF keyword_condition Reputation DO cost_change self (cost=-2) for while | WHEN summoned of self DO keyword_action <Rally>

49. Wrong thinking: a line that should exist is missing: power boosts have no line to cards that count or need units with power 5+.
   Rule: L14, L10. Games: Runeterra. Files: d1 cI
   - Avarosan Hearthguard -> Trifarian Assessor: missing line [Hearthguard: stat_change all mine unit in deck (power=1, health=1); Assessor: draw ... count of (all mine unit in board [power ge 5]); 0 partners]
        [runeterra] line now: NONE
        Avarosan Hearthguard: WHEN summoned of self DO stat_change all mine unit in deck (power=1, health=1) for permanent
        Trifarian Assessor: WHEN summoned of self DO draw mine card in deck_top (amount=count of (all mine unit in board [power ge 5]))
   - Omen Hawk -> Trifarian Assessor: missing line
        [runeterra] line now: NONE
        Omen Hawk: WHEN summoned of self DO stat_change 2 top mine unit in deck (power=1, health=1) for permanent
        Trifarian Assessor: WHEN summoned of self DO draw mine card in deck_top (amount=count of (all mine unit in board [power ge 5]))
   - Yadulski Snowdog -> Trifarian Assessor: missing line [Attack: stat_change 2 top mine card in deck (+1|+1)]
        [runeterra] line now: NONE
        Yadulski Snowdog: KW: Attack | WHEN attacks by self DO stat_change 2 top mine card in deck [category is unit] (power=1, health=1) for permanent
        Trifarian Assessor: WHEN summoned of self DO draw mine card in deck_top (amount=count of (all mine unit in board [power ge 5]))

50. Wrong thinking: a line that should exist is missing: power helpers link only to Zed and not to Poppy cards that read their own power.
   Rule: L18. Games: Runeterra. Files: d1 cK
   - Sharpsight -> Poppy: missing line [exists: Sharpsight -> Zed: makes stronger: more health; also more power]
        [runeterra] line now: NONE
        Sharpsight: WHEN always DO can self (event=blocks) for while
        Poppy: KW: Attack | WHEN attacks by self DO stat_change all mine unit in board [power le stat power of (self)] (power=1, health=1) for permanent | WHEN always IF event_count attacks by self ge 3 this_game DO level_up self
   - Twin Disciplines -> Poppy (level 2): missing line
        [runeterra] line now: NONE
        Twin Disciplines: WHEN played of self DO choose_one chosen mine unit in board OR stat_change chosen mine unit in board (power=3) for this_round OR stat_change chosen mine unit in board (health=3) for this_round
        Poppy (level 2): KW: Impact, Attack | WHEN attacks by self DO stat_change all mine unit in board [power le stat power of (self)] (power=2, health=2) for permanent THEN give_keyword it <Impact> for permanent
   - Young Witch -> Poppy: missing line [exists: Young Witch -> Zed: makes stronger: more power]
        [runeterra] line now: NONE
        Young Witch: KW: Elusive, Support | WHEN supports by self DO give_keyword right_of_self <Quick Attack> for this_round THEN stat_change right_of_self (power=1) for this_round
        Poppy: KW: Attack | WHEN attacks by self DO stat_change all mine unit in board [power le stat power of (self)] (power=1, health=1) for permanent | WHEN always IF event_count attacks by self ge 3 this_game DO level_up self
   - For Demacia! -> Poppy: missing line
        [runeterra] line now: NONE
        For Demacia!: WHEN played of self DO stat_change all mine unit in board (power=3, health=3) for this_round
        Poppy: KW: Attack | WHEN attacks by self DO stat_change all mine unit in board [power le stat power of (self)] (power=1, health=1) for permanent | WHEN always IF event_count attacks by self ge 3 this_game DO level_up self

51. Wrong thinking: a line that should exist is missing: a card that puts my champions into play by description sets off "when I'm summoned" champions.
   Rule: L17, L19. Games: Runeterra. Files: d2 cD, v3d1 c8, v3d2 c6
   - Feel The Rush -> Gangplank: missing line "puts it into play: its summon effect goes off" [Gangplank: KW: Overwhelm | WHEN summoned of self DO summon in board <Powder Keg>]
        [runeterra] line now: NONE
        Feel The Rush: WHEN played of self DO summon 2 random mine unit in everywhere [category is champion] in board THEN stat_set it (power=10, health=10)
        Gangplank: KW: Overwhelm | WHEN summoned of self DO summon in board <Powder Keg> | WHEN always IF event_count nexus_damaged of enemy player ge 5 different_rounds DO level_up self
   - Feel The Rush -> Gangplank (level 2): missing line
        [runeterra] line now: NONE
        Feel The Rush: WHEN played of self DO summon 2 random mine unit in everywhere [category is champion] in board THEN stat_set it (power=10, health=10)
        Gangplank (level 2): KW: Overwhelm, Attack | WHEN summoned of self DO summon in board <Powder Keg> | WHEN round_start DO summon in board <Powder Keg> | WHEN attacks by self DO damage all enemy unit in board (amount=1) THEN damage enemy player (amount=1)
   - Feel The Rush -> Trundle: missing line [Trundle: Summoned: create Ice Pillar]
        [runeterra] line now: NONE
        Feel The Rush: WHEN played of self DO summon 2 random mine unit in everywhere [category is champion] in board THEN stat_set it (power=10, health=10)
        Trundle: KW: Regeneration | WHEN summoned of self DO create in hand <Ice Pillar> | WHEN always IF event_count played by mine player of card [card is Ice Pillar] ge 1 this_game DO level_up self
   - Feel The Rush -> Trundle (level 2): missing line
        [runeterra] line now: NONE
        Feel The Rush: WHEN played of self DO summon 2 random mine unit in everywhere [category is champion] in board THEN stat_set it (power=10, health=10)
        Trundle (level 2): KW: Overwhelm, Regeneration, Attack | WHEN summoned of self DO create in hand <Ice Pillar> | WHEN attacks by self IF keyword_condition Behold mine card in hand [cost ge 8] DO stat_change self (power=count of (mine card in hand [cost ge 8])) for permanent

52. Wrong thinking: a line that should exist is missing: cards that create units of other regions feed Buster Shot but not The Bandle Tree.
   Rule: L17. Games: Runeterra. Files: d2 cJ
   - Loping Telescope -> The Bandle Tree: missing line [The Bandle Tree: round_start IF amount distinct region of (mine unit) this_game ge 10 DO win_game; 1 partner, Buster Shot]
        [runeterra] line now: NONE
        Loping Telescope: WHEN played of self DO choose_one OR keyword_action mine card [type is Celestial] [cost le 3] <Manifest> for unstated OR keyword_action mine card [rarity is epic] <Manifest> for unstated OR keyword_action mine card [category is follower] [state is multi_region] <Manifest> for unstated
        The Bandle Tree: KW: Landmark | WHEN round_start DO create random mine card [category is follower] [region not own_regions] in hand | WHEN round_start IF amount distinct region of (mine unit) this_game ge 10 DO win_game mine player
   - Bandle City Mayor -> The Bandle Tree: missing line
        [runeterra] line now: NONE
        Bandle City Mayor: WHEN always [first_each_round] DO cost_change mine card in hand [category is unit] [state is multi_region] (cost=-1) for while | WHEN played of self DO keyword_action mine card in hand [category is follower] [state is multi_region] <Manifest> for unstated
        The Bandle Tree: KW: Landmark | WHEN round_start DO create random mine card [category is follower] [region not own_regions] in hand | WHEN round_start IF amount distinct region of (mine unit) this_game ge 10 DO win_game mine player

53. Wrong thinking: a line that should exist is missing: cost 8+ cards of the deck have no line to the cards that need cost 8+ cards in hand.
   Rule: L10, L22. Games: Runeterra. Files: d2 cK
   - Feel The Rush -> Faces of the Old Ones: missing line [Faces of the Old Ones: round_start IF have mine card [cost ge 8] is DO max_mana_change]
        [runeterra] line now: NONE
        Feel The Rush: WHEN played of self DO summon 2 random mine unit in everywhere [category is champion] in board THEN stat_set it (power=10, health=10)
        Faces of the Old Ones: WHEN round_start IF have mine card [cost ge 8] is DO max_mana_change mine mana (amount=1) for this_round
   - Ice Pillar -> Faces of the Old Ones: missing line
        [runeterra] line now: NONE
        Ice Pillar: KW: Vulnerable | WHEN played of self DO mana_gain mine mana (amount=8) THEN give_keyword highest enemy unit by power in board <Vulnerable> for this_round | WHEN round_start DO give_keyword highest enemy unit by power in board <Vulnerable> for this_round
        Faces of the Old Ones: WHEN round_start IF have mine card [cost ge 8] is DO max_mana_change mine mana (amount=1) for this_round
   - Tryndamere -> Faces of the Old Ones: missing line
        [runeterra] line now: NONE
        Tryndamere: KW: Overwhelm | WHEN dies of self DO level_up self
        Faces of the Old Ones: WHEN round_start IF have mine card [cost ge 8] is DO max_mana_change mine mana (amount=1) for this_round

54. Wrong thinking: a line that should exist is missing: any damage makes a unit "damaged", which Ravenous Flock asks for, but only stun was linked and damaging spells have no line.
   Rule: L2, L18. Games: Runeterra. Files: d2 cQ, v3d3 c5
   - Mystic Shot -> Ravenous Flock: missing line "enables: makes a unit damaged" [Mystic Shot: damage chosen any 2; printed with no partner]
        [runeterra] line now: NONE
        Mystic Shot: WHEN played of self DO damage chosen any (amount=2)
        Ravenous Flock: WHEN played of self DO damage chosen unit in board [state in damaged] [state in stunned] (amount=4)
   - Thermogenic Beam -> Ravenous Flock: missing line [damage chosen unit (X)]
        [runeterra] line now: NONE
        Thermogenic Beam: WHEN played of self DO spend_mana mine mana (amount=full of (mine mana)) THEN damage chosen unit in board (amount=event_amount)
        Ravenous Flock: WHEN played of self DO damage chosen unit in board [state in damaged] [state in stunned] (amount=4)
   - Get Excited! -> Ravenous Flock: missing line [damages chosen any 3]
        [runeterra] line now: NONE
        Get Excited!: WHEN played of self DO discard chosen mine card in hand (amount=1) THEN damage chosen any (amount=3)
        Ravenous Flock: WHEN played of self DO damage chosen unit in board [state in damaged] [state in stunned] (amount=4)

55. Wrong thinking: a line that should exist is missing: power help to cards whose own text reads a power threshold.
   Rule: L18. Games: Runeterra. Files: d3 cG
   - Fury of the North -> Reckoning: missing line [Reckoning: IF mine unit with power 5+ ... kill all units with power 4 or less]
        [runeterra] line now: NONE
        Fury of the North: KW: Burst | WHEN played of self DO stat_change chosen mine unit in board (power=3, health=4) for this_round
        Reckoning: WHEN played of self IF count all mine unit in board [power ge 5] ge 1 now DO kill all unit in board [power le 4]
   - Fury of the North -> Bloody Business: missing line [strikes a mine unit with power 5+]
        [runeterra] line now: NONE
        Fury of the North: KW: Burst | WHEN played of self DO stat_change chosen mine unit in board (power=3, health=4) for this_round
        Bloody Business: KW: Reputation | WHEN always IF keyword_condition Reputation DO cost_change self (cost=-2) for while | WHEN played of self DO strike chosen mine unit in board [power ge 5] to chosen enemy unit in board
        case n16: expect line  (Kaptain: Reputation needs allies striking for 5+)
   - Troll Chant -> Reckoning: missing line
        [runeterra] line now: NONE
        Troll Chant: WHEN played of self DO stat_change chosen mine unit in board (health=2) for this_round THEN stat_change chosen enemy unit in board (power=-2) for this_round
        Reckoning: WHEN played of self IF count all mine unit in board [power ge 5] ge 1 now DO kill all unit in board [power le 4]

56. Wrong thinking: a line that should exist is missing: the same Invoke effect gets the "more different cards to play" line to Zoe for some cards and not for others.
   Rule: L17. Games: Runeterra. Files: d4 cC1
   - Supercool Starchart -> Zoe: missing line [WHEN played of self DO keyword_action mine card in hand [type is Celestial] [cost le 3] <Invoke>; 1 partner]
        [runeterra] line now: levels: creates cards: more different cards to play (levels it up)
        Supercool Starchart: WHEN played of self DO keyword_action mine card in hand [type is Celestial] [cost le 3] <Invoke> for unstated
        Zoe: KW: Elusive | WHEN strikes_nexus by self IF have mine card in hand [card is Supercool Starchart] not DO create in hand <Supercool Starchart> | WHEN strikes_nexus by self IF have mine card in hand [card is Supercool Starchart] is DO cost_change mine card in hand [card is Supercool Starchart] (cost=-1) for permanent | WHEN always IF amount distinct card of (played by mine player of card) this_game ge 10 DO level_up self
   - Behold the Infinite -> Zoe: missing line [WHEN played of self DO keyword_action mine card in hand <Invoke>; 2 partners]
        [runeterra] line now: levels: creates cards: more different cards to play (levels it up)
        Behold the Infinite: WHEN played of self DO keyword_action mine card in hand <Invoke> for unstated
        Zoe: KW: Elusive | WHEN strikes_nexus by self IF have mine card in hand [card is Supercool Starchart] not DO create in hand <Supercool Starchart> | WHEN strikes_nexus by self IF have mine card in hand [card is Supercool Starchart] is DO cost_change mine card in hand [card is Supercool Starchart] (cost=-1) for permanent | WHEN always IF amount distinct card of (played by mine player of card) this_game ge 10 DO level_up self
   - The Fangs -> Zoe: missing line
        [runeterra] line now: levels: creates cards: more different cards to play (levels it up)
        The Fangs: KW: Lifesteal | WHEN played of self DO keyword_action mine card in hand [type is Celestial] [cost le 3] <Invoke> for unstated
        Zoe: KW: Elusive | WHEN strikes_nexus by self IF have mine card in hand [card is Supercool Starchart] not DO create in hand <Supercool Starchart> | WHEN strikes_nexus by self IF have mine card in hand [card is Supercool Starchart] is DO cost_change mine card in hand [card is Supercool Starchart] (cost=-1) for permanent | WHEN always IF amount distinct card of (played by mine player of card) this_game ge 10 DO level_up self
   - (present) Mountain Scryer -> Zoe: helps it level up: creates cards: more different cards to play (levels it up)
        (cards not found by these names)

57. Wrong thinking: a line that should exist is missing: cards with the Nightfall keyword have no line to The Sky Shadows.
   Rule: L10, L21. Games: Runeterra. Files: d4 cC3
   - Aphelios -> The Sky Shadows: missing line [Aphelios: KW: Nightfall; The Sky Shadows: WHEN summoned of self IF have mine card [keyword is Nightfall] is DO mana_gain ...]
        [runeterra] line now: NONE
        Aphelios: KW: Nightfall | WHEN played of self IF keyword_condition Nightfall DO choose_card mine card [name_has is Moon Weapon] (options=1) THEN create it in hand | WHEN played by mine player of [card not Aphelios] [first_each_round] IF event_count played by mine player ge 2 this_round; have mine card in hand [type is Moon Weapon] not DO create in hand | WHEN always IF event_count played by mine player of [name_has is Moon Weapon] ge 4 this_game DO level_up self
        The Sky Shadows: WHEN summoned of self IF have mine card [keyword is Nightfall] is DO mana_gain mine spell_mana (amount=2)
   - Aphelios (level 2) -> The Sky Shadows: missing line
        [runeterra] line now: NONE
        Aphelios (level 2): KW: Quick Attack, Nightfall | WHEN played of self IF keyword_condition Nightfall DO choose_card mine card [name_has is Moon Weapon] (options=1) THEN create it in hand | WHEN played by mine player of [card not Aphelios (level 2)] [first_each_round] IF event_count played by mine player ge 2 this_round; have mine card in hand [type is Moon Weapon] not DO create in hand | WHEN round_start IF have mine card in hand [type is Moon Weapon] not DO create in hand | WHEN always DO cost_change all mine card [name_has is Moon Weapon] (cost=-1) for while
        The Sky Shadows: WHEN summoned of self IF have mine card [keyword is Nightfall] is DO mana_gain mine spell_mana (amount=2)
   - Pale Cascade -> The Sky Shadows: missing line [Pale Cascade: KW: Nightfall]
        [runeterra] line now: NONE
        Pale Cascade: KW: Nightfall | WHEN played of self DO stat_change chosen mine unit in board (power=1, health=1) for this_round | WHEN played of self IF keyword_condition Nightfall DO draw mine card in deck_top (amount=1)
        The Sky Shadows: WHEN summoned of self IF have mine card [keyword is Nightfall] is DO mana_gain mine spell_mana (amount=2)

58. Wrong thinking: a line that should exist is missing: the same "gives Ephemeral to a unit in hand" act has lines to the Ephemeral readers for Oblivious Islander but not for Stalking Shadows.
   Rule: L10, L17. Games: Runeterra. Files: d4 cC4
   - Stalking Shadows -> Hecarim: missing line [exists: Oblivious Islander -> Hecarim: helps it level up: makes your units Ephemeral (levels it up)]
        [runeterra] line now: NONE
        Stalking Shadows: WHEN played of self DO look 4 mine card in deck_top THEN draw chosen mine card in deck_top [category is follower] (amount=1) THEN shuffle_into_deck all mine card in deck_top THEN copy it in hand THEN give_keyword it <Ephemeral> for permanent
        Hecarim: KW: Overwhelm, Attack | WHEN attacks by self DO summon in board <Spectral Rider> (amount=2) THEN start_attack it | WHEN always IF event_count attacks by mine unit [state is ephemeral] ge 7 this_game DO level_up self
   - Stalking Shadows -> Moonlit Glenkeeper: missing line [exists: Oblivious Islander -> Moonlit Glenkeeper: triggers: makes your units Ephemeral]
        [runeterra] line now: NONE
        Stalking Shadows: WHEN played of self DO look 4 mine card in deck_top THEN draw chosen mine card in deck_top [category is follower] (amount=1) THEN shuffle_into_deck all mine card in deck_top THEN copy it in hand THEN give_keyword it <Ephemeral> for permanent
        Moonlit Glenkeeper: KW: Fearsome, Nightfall | WHEN summoned of mine unit [state is ephemeral] DO stat_change it (power=1) for permanent | WHEN played of self IF keyword_condition Nightfall DO summon in board <Sapling>

59. Wrong thinking: a line that should exist is missing: a return to hand of a card with a Play or Summon effect.
   Rule: L14, L17. Games: Runeterra. Files: d4 cC5, v3d2 c5
   - Defiant Dance -> Dunekeeper: missing line [Dunekeeper: WHEN summoned of self DO summon in board <Sand Soldier>]
        [runeterra] line now: NONE
        Defiant Dance: WHEN played of self DO return_to_hand chosen unit in board THEN keyword_action <Blade Dance> (amount=1)
        Dunekeeper: WHEN summoned of self DO summon in board <Sand Soldier>
   - Defiant Dance -> Forsaken Baccai: missing line [WHEN played of self IF it_matches [type is Darkin] ... <Predict>; no partner at all]
        [runeterra] line now: NONE
        Defiant Dance: WHEN played of self DO return_to_hand chosen unit in board THEN keyword_action <Blade Dance> (amount=1)
        Forsaken Baccai: WHEN played of self IF it_matches [type is Darkin] DO keyword_action mine player <Predict> for unstated THEN stat_change self (power=1, health=1) for permanent | WHEN played of self IF it_matches [category is equipment] [type not Darkin] DO keyword_action mine player <Predict> for unstated THEN stat_change self (power=1, health=1) for permanent
   - Will of Ionia -> Icevale Archer: missing line [Play: Frostbite; no partner]
        [runeterra] line now: NONE
        Will of Ionia: WHEN played of self DO keyword_action chosen unit in board <Recall> for unstated
        Icevale Archer: WHEN played of self DO keyword_action chosen enemy unit in board <Frostbite> for unstated
   - Will of Ionia -> Kindly Tavernkeeper: missing line [Play: heal 3; no partner]
        [runeterra] line now: NONE
        Will of Ionia: WHEN played of self DO keyword_action chosen unit in board <Recall> for unstated
        Kindly Tavernkeeper: WHEN played of self DO heal chosen mine any (amount=3)

60. Wrong thinking: a line that should exist is missing: Rally (a free extra attack) is linked to a champion that waits for an attack but not to one that waits for its own strike.
   Rule: L2, L4, L14, L16. Games: Runeterra. Files: d2 cE, v3d1 c1, v3d3 c6
   - Golden Aegis -> Akshan: missing line [exists: Cataclysm -> Akshan: triggers: does what it waits for or counts (strikes)]
        [runeterra] line now: NONE
        Golden Aegis: WHEN played of self DO give_keyword chosen mine unit in board <Barrier> for this_round THEN gain_attack_token mine player
        Akshan: KW: Quick Attack | WHEN summoned of self IF have mine landmark [card is Warlord's Palace] not DO summon in board <Warlord's Palace> | WHEN summoned of self IF have mine landmark [card is Warlord's Palace] is DO countdown_advance mine landmark [card is Warlord's Palace] (amount=1) | WHEN strikes by self IF have mine landmark [card is Warlord's Palace] not DO summon in board <Warlord's Palace> | WHEN strikes by self IF have mine landmark [card is Warlord's Palace] is DO countdown_advance mine landmark [card is Warlord's Palace] (amount=1) | WHEN always IF event_count countdown_done of mine landmark [card is Warlord's Palace] ge 1 this_game DO level_up self | WHEN levels_up of self DO summon in board <Warlord's Hoard>
   - Golden Aegis -> Akshan (level 2): missing line [exists: Cataclysm -> Akshan (level 2): triggers: does what it waits for or counts (strikes)]
        [runeterra] line now: NONE
        Golden Aegis: WHEN played of self DO give_keyword chosen mine unit in board <Barrier> for this_round THEN gain_attack_token mine player
        Akshan (level 2): KW: Quick Attack | WHEN summoned of self DO choose_one mine player OR summon in board <Warlord's Hoard> OR countdown_advance mine landmark [card is Warlord's Hoard] (amount=1) | WHEN strikes by self DO choose_one mine player OR summon in board <Warlord's Hoard> OR countdown_advance mine landmark [card is Warlord's Hoard] (amount=1)
   - Sion Returned -> Draven (level 2): missing line "triggers: another attack" [Draven (level 2): WHEN strikes by self DO create in hand <Spinning Axe> (amount=2); exists: Sion Returned -> Draven: helps it level up: helps my units strike more (levels it up)]
        [runeterra] line now: NONE
        Sion Returned: KW: Overwhelm, Ephemeral | WHEN summoned of self DO gain_attack_token mine player
        Draven (level 2): KW: Quick Attack, Overwhelm | WHEN summoned of self DO create in hand <Spinning Axe> (amount=2) | WHEN strikes by self DO create in hand <Spinning Axe> (amount=2)

61. Wrong thinking: a line that should exist is missing: Sivir (level 2) copies the keywords of attacking allies, but no keyword-giver links to it.
   Rule: L14, L20. Games: Runeterra. Files: v3d1 c2
   - Lucky Find -> Sivir (level 2): missing line [Lucky Find (3 partners): Warlord's Hoard, Warlord's Palace, Vekauran Bruiser]
        [runeterra] line now: NONE
        Lucky Find: KW: Focus, Fleeting | WHEN played of self DO give_keyword chosen mine unit in board <Fearsome> for unstated
        Sivir (level 2): KW: Quick Attack, SpellShield | WHEN always IF have self [state is attacking] is DO copy_keywords all mine unit in board [state is attacking] to self for while
   - Brightsteel Protector -> Sivir (level 2): missing line [2 partners: Warlord's Hoard, Warlord's Palace]
        [runeterra] line now: NONE
        Brightsteel Protector: WHEN played of self DO give_keyword chosen mine unit in board <Barrier> for this_round
        Sivir (level 2): KW: Quick Attack, SpellShield | WHEN always IF have self [state is attacking] is DO copy_keywords all mine unit in board [state is attacking] to self for while
   - Golden Aegis -> Sivir (level 2) (Barrier): keyword-giver line [Sivir (level 2): WHEN always IF have self [state is attacking] is DO copy_keywords all mine unit in board [state is attacking] to self]
        (cards not found by these names)
   - The Absolver's Return -> Sivir (level 2): missing line [Overwhelm]
        [runeterra] line now: NONE
        The Absolver's Return: KW: Burst, Fleeting | WHEN played of self DO give_keyword chosen mine unit in board <Overwhelm> for this_round THEN stat_change it (power=2, health=1) for this_round
        Sivir (level 2): KW: Quick Attack, SpellShield | WHEN always IF have self [state is attacking] is DO copy_keywords all mine unit in board [state is attacking] to self for while
