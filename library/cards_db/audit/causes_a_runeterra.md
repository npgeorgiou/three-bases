# Causes: runeterra whole-game check (a_runeterra.txt)

## Piece 1: lines 1-150 read
C1. "type: helps it hit the enemy player" is given to a card that only HAS Overwhelm/Elusive/Fearsome itself, not to one that gives it.
 - Rule broken: L20 (a fight keyword works for the card that has it; only GIVING Overwhelm/Elusive to a card that needs the Nexus is "helps it hit"), L10 (one reason said once). The same kind of pair (own-keyword card -> Plunder/nexus-damage card) is split at random between "damages the enemy player" and "helps it hit": Alpha Wildclaw -> Angel is the first, Alpha Wildclaw -> Bitsy Lizard is the second; Amateur Aeronaut -> Bitsy Lizard first, Amateur Aeronaut -> Angel second.
 - Examples (reason "helps it hit", 15306 lines; all 5 shown): 
   Alpha Wildclaw -> Bitsy Lizard  [Alpha Wildclaw: KW: Overwhelm]
   Bubble Bear -> Dame the Despoiler  [Bubble Bear: KW: Attune, Elusive; no give_keyword row]
   Catastrophe -> Elegant Edge  [Catastrophe: KW: Overwhelm]
 - Lines of my part showing it: 5 of 5 shown in this reason (15306 lines).
C2. "stronger: more power" from a card that only has the keyword Hallowed to a card that reads its own power when PLAYED. (Hallowed rows: WHEN attacks by mine unit [first_each_round] IF event_count dies of self ge 1 this_game DO stat_change it (power=1) for this_round: only an attacker gets it, and only after a Hallowed card died.)
 - Rule: L2/L4/L18: the source must give power to the target; Hallowed on the source's own card helps the source only (L15). Banana Blaster reads ITS OWN power, Ghastly Band gives it nothing.
 - Examples: Ghastly Band -> Banana Blaster [Ghastly Band: KW: Hallowed, Ephemeral]; Ghostly Paramour -> Dashing Dandy [KW: Hallowed, Lifesteal]; Boisterous Host -> Adnere's Aviarists [KW: Hallowed] (Aviarists copies the stats of the unit it supports; Host gives nothing).
 - Count: 2 clear of 5 shown (Ghastly Band -> Banana Blaster, Ghostly Paramour -> Dashing Dandy; Banana Blaster/Dandy read their power on play, not attacking). Reason has 15696 lines.
C3. A trigger-and-count card gets both "waits: is a spell whose playing sets off its effect" and "type: is a spell it needs played for its count".
 - Rule: L10 (one reason said once, by its strongest kind: a trigger beats an enabling count).
 - Examples: Absorb Soul -> Claws of the Dragon [WHEN played by mine player of spell IF event_count played by mine player of spell ge 2 this_round DO summon self]; Accelerated Purrsuit -> Fleet Admiral Shelly [WHEN played by mine player of spell [once_per_round] IF event_count ... ge 2 this_round]
 - 2 of 5 lines shown in the count reason (8521 lines). Whether the same pair also sits in "waits" is not visible in the 5 shown: marked half sure.

Unsure (piece 1):
 - "waits: puts your units into play": Accelerated Purrsuit -> Dragon Prince Grinzo (Grinzo needs summoned unit [cost eq 1]; Purrsuit summons <Catastrophe>, whose cost the rows do not show).
 - "waits: puts your units into play": Bladepierced Revenant -> Fleetfeather Tracker (Revenant only reacts to a revive and has Deathless; does it summon "by mine player"?).
 - "waits: kills it for its death effect": Black Spear -> Bladepierced Revenant, Blade's Edge -> Caustic Cask (1 damage, may not kill).
 - "type: damages the enemy player": Bouncer & Bolt, Bass of Burden (KW Impact: unknown if Impact damages the Nexus).
 - "stronger: more power": Phantom Butler -> Divine Clerk (Empowered 3: unknown what Empowered counts); Aberrant Mageseeker -> Honest Croupier (card cost eq my power: exact match, more power may not help).
Must-stay (piece 1): Ancient Crocolith -> Lord Mallat; Airis -> Durand Sculptor; Assembly Line -> Ember Monk; Absorb Soul -> Lux; Ancient Malediction -> Mind Meld

## Piece 2: lines 151-300 read
C4. "waits: more health or protection: survives damage" is given to cards whose only row is the keyword SpellShield (rows: WHEN targeted by enemy spell ... DO counter it effect).
 - Wrong thinking: SpellShield counters the spell, so no damage is taken and "survives_damage" never goes off; and it protects only the card that has it, not the waiter (L20 keyword works for the card that has it, L2, L4 "survive damage" needs health/protection that reaches the waiter, L6).
 - Examples (all 5 shown, reason 3365 lines):
   Belvethi Elder -> Bone Scryer [Belvethi Elder: KW: Evolve, SpellShield; Bone Scryer: WHEN survives_damage of self DO damage enemy player (amount=1)]
   Hungry Owlcat -> Legion Veteran [Hungry Owlcat: KW: SpellShield; Legion Veteran: WHEN survives_damage of mine unit [card not Legion Veteran] DO stat_change it (power=1)]
   Fused Firebrand -> Crimson Disciple [KW: Fury, SpellShield]
 - Lines: 5 of 5 shown.
C5. "type: creates cards": a card that creates a named other-kind card is linked to a card that needs ITSELF to be created.
 - Rule: L20 (a card made by name must be the kind the need asks), L3.
 - Example: Angel -> Cunning Kitten [Angel: WHEN played of self IF keyword_condition Plunder DO create in hand <Coin> (amount=3); Cunning Kitten: WHEN summoned of self IF it_matches [state is created] DO draw ... THEN stat_change self]. Angel makes Coins (spells), never Kitten.
 - Lines: 1 of 5 shown (reason 3196 lines); the other four (Acoustician -> Ambush, Attentive Accountant -> Mirror Mage, Avarosan Trapper -> Portal Scholar, Babbling Balladeers -> Sneezy Biggledust!) look right.
C6. "cheaper: pays for it": a cost RAISE read as "cheaper".
 - Rule: L10 (cheaper = a lowering). Mageseeker Junior sets spells with cost lt 3 to cost 3 (a raise or a fixed price), it cannot make Assembly Line cheaper.
 - Example: Mageseeker Junior -> Assembly Line [Mageseeker Junior: WHEN always DO cost_set card [category is spell] [cost lt 3] (cost=3) for while; Assembly Line: WHEN played of self DO summon <Forge Worker> (amount=2)]
 - Lines: 1 of 5 shown (reason 3574 lines).

Unsure (piece 2):
 - "cheaper: pays for it": Primordial Roar -> Darius (level 2) [Darius (level 2): KW: Overwhelm]: a level-2 form is not paid for a second time; same pattern may repeat for other "(level 2)" cards as the TARGET of a cost reason.
 - "waits: makes it attack": Buhru Leader -> Arena Battlecaster (start_attack only a unit [cost eq 1]; Battlecaster cost is not in the rows). Field Promotion -> Balen the Benevolent (Field Promotion: give_ability mine player for this_round; the ability is not in the rows).
 - "waits: returns it to hand": Shadows of the Past -> Allay (created), Tag Out! (created) -> Allay (created): created tokens as lines (L9 "cards a player can own").
 - "cheaper: pays for it": Heisho -> Alpha Wildclaw, Eager Apprentice -> Ascended's Rise (is the target expensive per network.EXPENSIVE? not in rows).
Must-stay (piece 2): Dragonguard Lookout -> Aurok Glinthorn; Bull -> Arena Mechacaster; Mist's Call -> Adroit Artificer; Avarosan Trapper -> Portal Scholar; Alpha Wildclaw -> Jagged Cutlass
(lines 151-300 read)

## Piece 3: lines 301-450 read
C1 (more lines): the "helps it hit" kind appears again in other reasons for the same own-keyword sources, always next to the "damages" version of the same pair type:
   "waits: helps it hit the enemy player": Alpha Wildclaw -> Fix-Em-Uppers [Alpha Wildclaw: KW: Overwhelm; Overwhelm rows: WHEN strikes by self DO excess_damage enemy player] while "waits: damages the enemy player" has Amateur Aeronaut -> Fix-Em-Uppers (same need: WHEN nexus_damaged by mine player ...).
   "levels: helps it hit the enemy player": Amateur Aeronaut -> Darius [Elusive: WHEN always DO cant all enemy unit [keyword not Elusive] to self (event=blocks)] while "levels: damages the enemy player" has Alpha Wildclaw -> Darius.
   The keyword only works for its own card (L20); Elusive/Overwhelm on a card that is not the target helps nothing. Two reasons for one pair-type (L10). 2 more of the 4 single-line reasons in this piece.
C7. "waits: makes more cards to play": a card that makes cards is linked to a card that goes off on ANY card/unit/follower played.
 - Rule: L1 ("Whenever you play a card": no line from every card), L1b (a unit/follower is most of the game's cards), L19 (one more card of any kind is generic). The created card is not named by the need; the receiver would trigger anyway.
 - Examples (reason 2552 lines; 4 of 5 shown):
   Angel -> The Swindler's Den [The Swindler's Den: WHEN played by mine player of card DO draw mine card in deck_top (amount=1)]
   Babbling Balladeers -> Valley of Imitation [WHEN played by mine player of unit [category is follower] DO transform self to it]
   Avarosan Trapper -> Marai Reef Spire [WHEN mana_spent by mine player of unit DO mana_gain mine spell_mana (amount=1)]
   Attentive Accountant -> The Veiled Temple [WHEN played by mine player of card [first_each_round] IF event_count played ... ge 2 this_round]
 - Honest Croupier (card cost eq my power) is the one in 5 that has a real filter.
C8. "type: creates cards: more different cards to play" feeds a count that asks for a KIND the created card is not.
 - Rule: L20 (a card made must be the kind the need asks), L1.
 - Example: Acoustician -> The World Ender [Acoustician: WHEN strikes by self DO create random mine card [category is spell] [cost eq 2] [state is new] in hand; The World Ender: WHEN always IF amount distinct card of (played by mine player of any [type is Darkin] [card not Aatrox]) this_game ge 3 DO draw ... Aatrox]. A random cost-2 spell is no Darkin.
 - Lines: 1 of 1 shown (reason 1664 lines).
C9. "type: another attack" between two cards with the SAME keyword Scout, with no text that uses an attack.
 - Rule: L15 (what a keyword does to cards with the same keyword is the keyword's rule), L1/L2 (a card must have a text that wants the extra attack). Scout rows: WHEN attacks by mine player [first_each_round] IF count mine unit [state is attacking] [keyword not Scout] eq 0 DO gain_attack_token.
 - Example: Greathorn Companion -> Greenfang Warden [Greathorn Companion: KW: Scout; Greenfang Warden: KW: Barrier, Scout]
 - Lines: 1 of 1 shown (reason 2214 lines).

Unsure (piece 3):
 - Ability given to the player is not in the rows, so cannot judge: Alpha Wildclaw -> Loaded Dice, Alpha Wildclaw -> Stylish Shot, Absorb Soul -> Blades of the Fallen, Armed Gearhead -> Sacred Shears (give_ability self), Absorb Soul -> Twisted Catalyzer (Catalyzer reacts to its own strike; Absorb Soul damages my unit).
 - Lord Mallat -> Chemtech Catermobile (counts mine unit [cost eq 1] summoned "by mine player"; a Deathless revive is not the player's act? cost of Mallat not in rows).
 - Lines to "(level 2)" forms for waits-on-event reasons (Rumble, Sejuani, Swain): fine only because they are on board.
Must-stay (piece 3): Armed Gearhead -> Bard; Alpha Wildclaw -> Darius (levels: damages); Bass of Burden -> Sivir; Absorb Soul -> Plaza Guardian; Absorb Soul -> Haunted Tomb
(lines 301-450 read)

## Piece 4: lines 451-600 read
C10. Stat help ("stronger: gives it more power and health when it comes") to a card with NO rows at all.
 - Rule: L14 (help aimed at a kind makes a line only to a card whose own text uses it), L18 (stat help only where the text reads the stat).
 - Example: Battlesmith -> Blocking Badgerbear [Battlesmith: WHEN summoned by mine player of it mine unit [type is Elite] DO stat_change it (power=1, health=1) for permanent; Blocking Badgerbear: (no rows)]
 - Lines: 1 of 1 shown (reason 1432 lines).
C11. "puts: draws it from the deck" / "puts: draws it and keeps it": a draw or tutor by kind (or any 3 cards) linked to a card with no text about being drawn.
 - Rule: L1b (a draw/tutor by kind only makes no line: any card of that kind can be drawn), L1.
 - Examples: Dragon Allegiant -> Fused Firebrand [Dragon Allegiant: WHEN summoned of self IF keyword_condition Behold DO draw random mine card in deck [type is Dragon]; Fused Firebrand: KW: Fury, SpellShield]; Realm Warp -> Darius (level 2) [Realm Warp: draw mine card in deck_top (amount=3) THEN discard it ... [category is follower]; Darius (level 2): KW: Overwhelm]
 - Lines: 2 of 2 shown (1304 + 973 lines). Also Darius (level 2) cannot be drawn.
C12. The three "(by fighting)" reasons are given to sources whose only row is Scout or Quick Attack.
 - Rule: L1/L2 (every card can fight; only a text that adds an attack, strikes now or a keyword that does the need counts), L4 (a help must do the very thing needed: an extra attack does not reach the Nexus past blockers, does not kill). Quick Attack row: WHEN attacks by self DO first_strike self (fight order only, not deathtouch).
 - Examples: Greathorn Companion -> Angel ("damages the enemy player (by fighting)", Angel needs Plunder); Greathorn Companion -> Siphoning Strike ("makes units die (by fighting)"); Academy Prodigy -> Ye Been Warned [Academy Prodigy: KW: Quick Attack] ("makes enemy units die (by fighting)")
 - Lines: 3 of 3 shown in the three reasons (1260 + 1134 + 1077 lines). Greathorn Companion -> Crackshot Corsair ("makes your units attack") is right: Scout is a Rally.
C13. More damage for a plain damage spell ("stronger: its damage gets 1 more").
 - Rule: L18 (more damage is generic: a plain hit does not read the damage).
 - Example: Deluge -> Avalanche [Deluge: WHEN played of self DO give_ability mine player for permanent; Avalanche: WHEN played of self DO damage all unit in board (amount=2)]
 - Lines: 1 of 1 shown (reason 1050 lines). (The ability itself is not in the rows; only the reason's name says it adds damage.)
C14. "stronger: makes its effect bigger" to a card that has no number to enlarge.
 - Rule: L14 / L18 (a bigger effect only where the card's own text has an effect to grow).
 - Example: Alatis the Gallant -> Dragonling [Alatis the Gallant: WHEN always DO increase_effect all mine unit in board [type is Dragon] for while; Dragonling: KW: Ephemeral, Lifesteal]
 - Lines: 1 of 1 shown (reason 920 lines).
C15. More power to a card whose only rows are Fearsome (or other fight keywords).
 - Rule: L18 states it: more power makes NO line because a card has Fearsome; Fearsome reads the ENEMY's power (WHEN always DO cant all enemy unit [power lt 3] to self (event=blocks)).
 - Example: Arachnoid Host -> Arachnoid Horror [Arachnoid Host: WHEN summoned of self DO stat_change all mine unit in board [card not Arachnoid Host] [type is Spider] (power=2) for permanent; Arachnoid Horror: KW: Fearsome]
 - Lines: 1 of 1 shown (reason 825 lines). Compare the right lines with Lifesteal targets (Ancient Warmonger -> Darkwater Scourge).
C16. "waits: makes cards leave play" from an Equipment card that only attaches.
 - Rule: L1/L3. Equipment rows: WHEN activated DO attach self to chosen mine unit THEN WHEN leaves_play of attached_to DO return_to_hand self. The equipment goes back to hand AFTER the unit left; it makes no card leave play.
 - Example: Bone Club -> Papercraft Dragon (created) [Bone Club: KW: Equipment; Papercraft Dragon: ... WHEN leaves_play of attached_to DO keyword_action self <Recall>]
 - Lines: 1 of 1 shown (reason 1011 lines). Also a "(created)" token (L9).

Unsure (piece 4):
 - Kinkou Wayfinder -> Byrd, The Bellringer (summons a random unit [cost eq 1]; Byrd's cost not in the rows).
 - Dragon Dedicant -> Alpha Wildclaw ("can make it cheaper", random card in hand; L16 "can aim at it" is no reason if that is all).
 - Mechapulverizer -> Darkbulb Acolyte (a discard of ONE chosen card "empties your hand").
 - Papercraft Dragon (created): created token as target.
Must-stay (piece 4): Abyssal Eye -> Patrol Wardens; Abyssal Eye -> Astute Academic; Concerted Strike -> Acoustician; Absorb Soul -> Kalista; Acoustician -> Curious Shellfolk
(lines 451-600 read)

## Piece 5: lines 601-750 read
C8 (more): "levels: creates cards (levels it up)": Acoustician -> Norra. Acoustician creates a random SPELL in hand; Norra: WHEN always IF event_count summoned of mine unit [state is created] ge 6 this_game DO level_up self. A spell is never a created summoned unit (L20 kind). 1 of 1 shown (696 lines). (Same cause as Acoustician -> The World Ender in piece 3: Acoustician creates only cost-2 spells, never units, never Darkin.)
C4 (more): "levels: more health or protection: survives damage (levels it up)": Belvethi Elder -> Braum [Belvethi Elder: KW: Evolve, SpellShield; SpellShield rows: WHEN targeted by enemy spell ... DO counter it effect]. SpellShield counters the spell, no damage taken, protects only its own card. 1 of 1 shown (702 lines). Rule: L20, L4, L6.
C17. "puts: copies it": a copy put into the DECK by Nautilus linked to a plain unit.
 - Rule: L19 (a copy put into hand or deck is one more card of any kind: generic, no line).
 - Example: Nautilus -> Alpha Wildclaw [Nautilus: WHEN levels_up of self DO copy all mine unit in removed [cost ge 4] in deck; Alpha Wildclaw: KW: Overwhelm]
 - Lines: 1 of 1 shown (606 lines).
C18. A needs-about-the-ENEMY card fed by my own effect (the need is the opponent's act).
 - Rule: L9 (my effects feed my needs; Charger's need is damage by an ENEMY spell, which my own Avalanche can never be).
 - Example: Avalanche -> Petricite Charger [Avalanche: WHEN played of self DO damage all unit in board (amount=2); Petricite Charger: KW: Formidable | WHEN damaged by enemy spell [category in spell] [category in skill] of self DO negate_damage self]
 - Lines: 1 of 1 shown ("waits: damages it for its effect", 560 lines).

Unsure (piece 5):
 - Challenger counted as "targets": Affectionate Poro -> Ye Been Warned ("type: targets enemy cards") and Affectionate Poro -> Morgana ("levels: targets cards"). Challenger rows: WHEN attacks by self DO challenge chosen enemy unit (the vocabulary event "targeted" is "by a spell, skill or ability").
 - "waits: finishes countdowns": Buried Armory -> Dragon Roost (Armory's countdown_done has no "of self" in either card; if it means "its own", the Armory finishing its own countdown does not help the Roost).
 - "moves: moves it within reach of the enemy player": Syncopation -> Abyssal Eye (Eye already has Elusive).
 - "stronger: turns the Power it grows into Power": Bayou Brunch -> Abyssal Guard (reason name unclear from the rows).
 - Aberrant Mageseeker -> Sacred Shears ("changes units' stats for the ability it gives": given Spirit rows: WHEN always DO stat_change self (power=1, health=1) for while; the ability Sacred Shears gets is not in rows).
Must-stay (piece 5): Absorb Soul -> Buhru Sentinel; Inspiring Marshal -> Darkwater Scourge; Darkwater Scourge -> Black Spear (Ephemeral kills itself on strike); Arachnoid Sentry -> Falling Star; Absorb Soul -> Malefic Spear
(lines 601-750 read)

## Piece 6: lines 751-906 read
C6 (more): "cheaper: can cost set it": Mageseeker Junior -> Absorb Soul (Mageseeker Junior sets spells of cost lt 3 to cost 3: a raise; same wrong thinking as Assembly Line in piece 2). 1 of 1 shown (320 lines).
C19. "stronger: doubles its damage": a doubling that works only on damage taken BY the card itself, linked to a plain damage dealer.
 - Rule: L2 (a unit hits a friendly unit only if its own text adds a strike), L18 (more damage is generic; only a text that reads the damage counts).
 - Example: The Dreadway -> Darkwater Scourge [The Dreadway: KW: Fearsome | WHEN damaged by mine spell DO damage it (amount=event_amount) | WHEN damaged by mine unit DO damage it (amount=event_amount); Darkwater Scourge: KW: Ephemeral, Lifesteal]. The doubling is on damage The Dreadway takes; Scourge has no text that makes it hit The Dreadway.
 - Lines: 1 of 1 shown (395 lines).
C20. "rules: gives it Fast" (a speed given to a KIND of spell).
 - Rule: L14 (help aimed at any card of a kind links only to a card whose own text uses that help). Absorb Soul has no text that uses speed.
 - Example: Senna (level 2) -> Absorb Soul [Senna (level 2): WHEN always DO give_keyword all mine spell [category in spell] [does in damage] [does in kill] <Fast> for while THEN cost_change all mine spell [...] (cost=-1)]; Absorb Soul: WHEN played of self DO keyword_action chosen mine unit in board <Drain> (amount=4)
 - Lines: 1 of 1 shown (360 lines).

Unsure (piece 6):
 - "levels: helps my units kill": Boisterous Host -> Kindred (Hallowed gives +1 power: more power, L18; Kindred levels from killing marked units).
 - "waits: damages it: its own effect goes off": Crimson Awakener -> Lord Mallat (Mallat only has Deathless; 1 damage kills only if his health is 1, not in rows).
 - "type: puts units into play": Lord Mallat -> Passage Unearned (Passage Unearned obliterates ALL units summoned this round not from hand, mine too: the revived Mallat is collateral, not a use).
 - "cheaper: makes it cheaper": Gleaming Lantern -> Carved Bladetwirler (cost help aimed at [type is Fae]; Bladetwirler's type/cost not in rows).
 - "stronger: plays it again": Seraphine (level 2) -> Absorb Soul (repeat only for spells [state is new] [cost le 2]; Absorb Soul's cost not in rows).
 - "levels: targets enemy cards": Affectionate Poro -> Ezreal (Challenger as targeting, third line of that pattern; see piece 5).
Must-stay (piece 6): Affectionate Poro -> Obeyed Order; Acoustician -> Zoe; Buried Armory -> Taliyah; Coin -> Frostcoat Cub; Bone Club -> Arbiter of the Peak
(lines 751-906 read)

## Summary
Lines read: 1-906 (all). 20 causes (C1-C20). Best confidence: C1, C4, C9, C11, C15, C17, C18; medium: C2, C5, C7, C10, C12, C13, C14, C16, C19, C20; half-sure: C3, C6, C8.
