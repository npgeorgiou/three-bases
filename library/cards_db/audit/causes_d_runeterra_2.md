# Causes, runeterra deck check, lines 1412-2781 (work file, appended per piece)

## Piece 1-2 (read 1412-1711; decks Sivir Akshan, Poppy Ziggs, start of Gangplank Sejuani)

### Cause A: one reason is said two or three times in one line (L10: one reason is said once, by its strongest kind)
Same act listed as "triggers" and "makes stronger", or the same fact as three different "it asks for/counts/names".
- `Akshan -> Warlord's Palace: puts it into play: summons; also triggers: finishes countdowns; also makes stronger: can speed up its countdown` (finishes a countdown and speeds up the countdown are the same act: countdown_advance)
- `Warlord's Palace -> Akshan: enables: is a landmark it counts; also is a landmark or structure it asks for; also is the Warlord's Palace it names` (one fact: Akshan names the Palace)
- `Golden Aegis -> Sivir (level 2): enables: another attack; also makes your units attack; also makes it attack for its effect` (one fact: Aegis gives the attack token)
- Lines showing it in my part: 5 (the three above, plus `Akshan -> Warlord's Hoard` and `Akshan (level 2) -> Warlord's Hoard`, same "summons; also triggers: finishes countdowns; also makes stronger: can speed up its countdown")

### Cause B: wrong word for what is put into play (L8/L10: say what the card really is)
Shaped Stone counts `summoned of mine landmark`; Akshan puts a landmark (Palace/Hoard) into play, but the line says "puts your units into play".
- `Akshan -> Shaped Stone: enables: puts your units into play`
- `Akshan (level 2) -> Shaped Stone: enables: puts your units into play`
- Lines: 2

### Cause C: the help is aimed at a unit, the partner is a landmark (kind mismatch; L8 kinds)
Noxian Fervor damages `chosen mine unit` and `chosen unit`; Scrappy Bomb has `KW: Countdown, Landmark`. Other damage cards in the deck (Pokey Stick `chosen any`, Black Powder Grenade, Imperial Demolitionist) have no line to the Bomb, so this one stands alone.
- `Noxian Fervor -> Scrappy Bomb: triggers: kills it for its death effect`
- Lines: 1

### Cause D: a card puts my champions into play from my own cards, but no line to the champion whose "when I'm summoned" goes off (L17)
Feel The Rush: `summon 2 random mine unit in everywhere [category is champion] in board`. Gangplank and Gangplank (level 2) both have `WHEN summoned of self DO summon in board <Powder Keg>`. Feel The Rush shows only 1 partner (Powder Keg), so both lines are missing.
- missing `Feel The Rush -> Gangplank` and `Feel The Rush -> Gangplank (level 2)` (puts it into play: its summon effect goes off)
- Lines: 2 missing (Sejuani has no summon row: no line to her)

### Cause E: Rally is not linked to a champion that waits for its own strike (L4 "another attack is only Rally or a free attack"; L14 kept: an attack to a card with Strike/Attack)
Golden Aegis: `give_keyword Barrier ... THEN gain_attack_token mine player`. It has a line to Sivir (level 2) (which only needs "attacking"), and Cataclysm (a free attack) has lines to Akshan and Akshan (level 2) `triggers: does what it waits for (strikes)`. Both Akshan cards have `WHEN strikes by self`. Golden Aegis (3 partners: Sivir L2, Palace, Hoard) has no line to them.
- missing `Golden Aegis -> Akshan`, `Golden Aegis -> Akshan (level 2)`
- Lines: 2 missing

## Unsure (piece 1-2)
- `Sandstone Charger -> Vanguard Redeemer: enables: dies by its own effect`: Ephemeral dies at round end; Redeemer needs a death earlier this round before it is summoned. Rows alone (Charger: `KW: Ephemeral`) do not say when Ephemeral kills. Also L15: a keyword's inner working is no need.
- `For Demacia! -> Radiant Guardian: makes stronger: can give it more power and health`: Guardian gives itself Lifesteal and Tough; more power can stay (Lifesteal reads damage, L18), but "health" fits no Taunt/survive wait (L18/L14).
- `The Absolver's Return -> Sivir: helps it level up: more damage` but no `The Absolver -> Sivir` although The Absolver also gives +2 power: only difference is Overwhelm. Sivir reads damage dealt (30), so L18 may keep both or neither.
- `Ziggs -> Short Fuse: casts its skill`, `Legion Saboteur -> Sabotage: casts its skill`: the Ziggs/Saboteur rows show the skill's damage inline, no `play_card` row. Cannot judge from rows.
- `Scrappy Bomb -> Ziggs (level 2)` not present: Ziggs (level 2) has `killed by mine player of mine landmark` (differs from level 1 `dies of mine landmark`); unclear if the Bomb's death feeds it.
- `The Dreadway -> Fortune Croaker` but no `The Dreadway -> Monkey Idol` (Idol also damages by its own unit effect: `damage self`).
- `Warlord's Palace`/`Warlord's Hoard` -> `Shaped Stone` (they are landmarks put into play, Shaped Stone counts `summoned of mine landmark`): Shaped Stone's partner lines were not in my part.
- `Marai Warden` (random cost-1 follower, no zone given) has no partner: right unless the follower comes from my deck.
- `Powder Keg -> Feel The Rush: makes stronger: makes its effect bigger`: Keg `increase_effect all mine spell`; is aimed at the kind "spell" (L14). Keep an eye on whether Keg has the same line to every spell in the deck (see later pieces).

## Must-stay (piece 1-2)
- `Concerted Strike -> Akshan: helps it level up: makes it strike for its effect`
- `Cataclysm -> Akshan: triggers: does what it waits for or counts (strikes)`
- `Crackshot -> Gangplank: helps it level up: damages the enemy player (levels it up)`
- `Inventive Chemist` has no line to `Ziggs` (L3: Chemist makes the Bomb, the Bomb is the one that dies)
- `Zap Sprayfin` / `Sejuani` etc.: no line from a draw of spells by cost (L1b/L21)

(lines read: 1412-1711)

## Piece 3 (read 1712-1861; deck Gangplank Sejuani, lines of Crackshot..Sejuani)

### Cause F: a cost drop is said as "enables" (L10: a cost that drops for X is "makes it cheaper", never "enables"; one reason once)
Monster Harpoon: `WHEN always IF keyword_condition Plunder DO cost_change self (cost=-2)`. The same act (hit the Nexus) is written twice: "enables: helps it hit the enemy player; also makes cheaper: damages the enemy player".
- `Zap Sprayfin -> Monster Harpoon: enables: helps it hit the enemy player; also makes cheaper: damages the enemy player`
- `Gangplank (level 2) -> Monster Harpoon: enables: helps it hit the enemy player; also makes cheaper: damages the enemy player`
- `Sejuani -> Monster Harpoon: enables: ...; also makes cheaper: ...` (same text)
- Lines: 4 (plus Gangplank -> Monster Harpoon, same text)  [5 total]
Right form (as in Crackshot -> Monster Harpoon): a single "makes cheaper".

### Cause G: a keyword that reaches the Nexus (Overwhelm, Elusive, Fearsome) is written twice, once as "damages the enemy player" although the card has no damage row (L1: a line comes from the text; L10: one reason once)
Sprayfin (`KW: Elusive, Attune`, draws a spell), Sejuani and Gangplank level 1 (`KW: Overwhelm`, no damage row), The Dreadway (`KW: Fearsome`) only have the keyword. The line says both "damages the enemy player" and "helps it hit the enemy player" (also "helps it level up" twice).
- `Zap Sprayfin -> Black Market Merchant: enables: damages the enemy player; also helps it hit the enemy player`
- `Sejuani -> Gangplank: helps it level up: damages the enemy player (levels it up); also helps it hit the enemy player (levels it up)`
- `The Dreadway -> Gangplank: puts it into play: draws it from the deck; also helps it level up: damages the enemy player (levels it up); also helps it level up: helps it hit the enemy player (levels it up); also makes stronger: doubles its damage`
- Lines in 1712-1861: 20 (Sprayfin 6, Gangplank (level 2) 5, Gangplank 3, Sejuani 3, The Dreadway 3). Gangplank (level 2) has real damage text (attacks: Nexus 1) AND Overwhelm: the Nexus damage is still one reason.
Right form: keyword-only cards say only "helps it hit the enemy player"; text-damage cards say only "damages the enemy player".

### Cause H: a draw by kind with a filter half the cards pass (L1b, L21)
Zap Sprayfin `draw random mine card in deck [category is spell] [cost le 3]`: any cheap spell can be drawn.
- `Zap Sprayfin -> Make it Rain: puts it into play: draws it from the deck`
- `Zap Sprayfin -> Warning Shot: puts it into play: draws it from the deck`
- Lines: 2
(The Dreadway draws a named card, Gangplank: that line is right.)

### Cause I: the level 1 card gets a line from its level 2 text (rows of level 1 have no such act)
Gangplank (level 1): `KW: Overwhelm | summoned: summon Powder Keg | level_up`. The skill Powderful Explosion is the inline damage of Gangplank (level 2) `attacks by self`.
- `Gangplank -> Powderful Explosion: puts it into play: casts its skill`
- Lines: 1 (Gangplank (level 2) -> Powderful Explosion is right)

## Unsure (piece 3)
- `Sejuani -> Sejuani (level 2)`, `Gangplank -> Gangplank (level 2)` "levels into": fine as is.
- Dreadway doubling shown for Crackshot Corsair, Gangplank (level 2), Fortune Croaker but not for the skills Crackshot/Powderful Explosion (Dreadway row says `mine spell`, Keg row says spell AND skill): looks right.

## Must-stay (piece 3)
- `Crackshot -> Monster Harpoon: makes cheaper: damages the enemy player` (single clean reason)
- `Crackshot -> Gangplank: helps it level up: damages the enemy player (levels it up)`
- `Powder Keg -> Crackshot: makes stronger: makes its effect bigger`
- `Gangplank (level 2) -> Powder Keg: puts it into play: summons`
- `Crackshot Corsair -> Sejuani (level 2): triggers: damages the enemy player`

(lines read: 1712-1861)

## Piece 4 (read 1862-2011; end of Gangplank Sejuani, deck Bandle Tree, start of deck Trundle Sejuani Tryndamere)

(Cause F and G repeat: `Sejuani (level 2) -> Monster Harpoon`, `-> Gangplank`, `-> Black Market Merchant` carry the same double reason. Counted: F +1 line, G +3 lines. Totals so far F 6, G 23.)

### Cause J: Bandle Tree: cards that create units of other regions feed Buster Shot (count of regions played) but not The Bandle Tree, which counts the regions of my units (L17: a card that makes a card by description links to the card that counts them)
The Bandle Tree: `round_start IF amount distinct region of (mine unit) this_game ge 10 DO win_game`. Loping Telescope and Bandle City Mayor manifest `[category is follower] [state is multi_region]`; both have a line to Buster Shot (`creates cards: more different cards to play`), but The Bandle Tree shows only 1 partner (Buster Shot).
- missing `Loping Telescope -> The Bandle Tree`, `Bandle City Mayor -> The Bandle Tree`
- Lines: 2 missing

### Cause K: a cost 8+ card in hand is read by two cards, but no line comes from the cost 8+ cards of the deck (L10 enables: a thing that must be there; EXPENSIVE for runeterra is 6)
Faces of the Old Ones: `round_start IF have mine card [cost ge 8] is DO max_mana_change`. It is a card with NO partner (a-list) although the deck holds Ice Pillar (cost 8), Feel The Rush (cost 12), Tryndamere (cost 8). Trundle (level 2) counts `mine card in hand [cost ge 8]` (Behold) with the same gap (see later pieces for its lines).
- missing `Feel The Rush -> Faces of the Old Ones`, `Ice Pillar -> Faces of the Old Ones`, `Tryndamere -> Faces of the Old Ones`
- Lines: 3 missing (+ the same toward Trundle (level 2) if it also lacks them)

## Unsure (piece 4)
- `Bandle Commando -> Buster Shot` / `Fizz (level 2) -> Buster Shot` (named creations Hungry Owlcat = Bandle City, Chum the Waters = Bilgewater): "more different cards to play" holds only if the made card has a region the deck lacks; the cards made by name are a region the deck already has. Possibly L19/L1 (one more card is generic).
- `Ravenous Flock -> Fizz: helps it level up: is a spell it needs played for its count (levels it up); also triggers: is a spell whose playing sets off its effect`: two abilities of Fizz, one fact (a spell played): L10 says once. Same family as Cause A.
- `Ice Pillar -> Feel The Rush: makes cheaper: pays for it: more mana or a lower cost`: fine under L22 and EXPENSIVE.

## Must-stay (piece 4)
- `Bandle City Mayor`'s lack of any line to Poppy / Hungry Owlcat (L14: help aimed at a kind: multi-region units)
- `Proto Poro` (KW Impact) with no line to Poppy (level 2) which gives Impact (L15)
- `Aloof Travelers` has no partner (draw from the deck top, discard highest enemy card: nothing needs it)
- `Fizz (level 2) -> Chum the Waters: puts it into play: creates`

(lines read: 1862-2011)

## Piece 5 (read 2012-2161; rest of deck Trundle Sejuani Tryndamere, start of deck Jayce Sentinels)

### Cause L: "fills your hand" for a card that counts only cost 8+ cards in hand (L1: not what every card does; L19: a made/drawn card is one more card of any kind)
Trundle (level 2): `attacks by self IF Behold mine card in hand [cost ge 8] DO stat_change self (power=count of (mine card in hand [cost ge 8]))`. Only cost 8+ cards count (Ice Pillar 8, Feel The Rush 12, Tryndamere 8).
- `Avarosan Sentry -> Trundle (level 2): triggers: fills your hand` (Sentry: Last Breath draws the top card, any card)
- `Three Sisters -> Trundle (level 2): triggers: fills your hand` (Three Sisters creates Flash Freeze / Fury of the North / Entomb, all cost 5 or less)
- Lines: 2
(The cost 8+ cards of the deck: Ice Pillar, Feel The Rush, Tryndamere show no line to Trundle (level 2) either, same gap as Cause K.)

### Cause M: a keyword given to a card that has no text using it (L14: help aimed at a card kind or type, "a Spider", is no narrower than a deck; L15)
Spider Queen Elise (level 2) gives every Spider Challenger and Fearsome. Spiderling has NO rows (vanilla); nothing in its text uses either keyword.
- `Spider Queen Elise (level 2) -> Spiderling: gives keyword: gives it Challenger; also gives it Fearsome`
- Lines: 1

### Cause G (more lines): `Tryndamere -> Sejuani`, `Tryndamere -> Sejuani (level 2)`, `Tryndamere (level 2) -> Sejuani`, `Tryndamere (level 2) -> Sejuani (level 2)`, `Trundle (level 2) -> Sejuani`, `Trundle (level 2) -> Sejuani (level 2)` all say "damages the enemy player; also helps it hit the enemy player" for Overwhelm-only cards. Compare the clean `Scattered Pod -> Sejuani: helps it level up: damages the enemy player (levels it up)` where the Pod gives itself Elusive by its own text: one reason only. +6 lines (G total so far 29: 1712-2161).

### Cause A (more): `Ice Pillar -> Trundle: helps it level up: is a card it needs played for its count (levels it up); also enables: is the Ice Pillar it names` (one fact, Trundle names Ice Pillar). +1 line.

## Unsure (piece 5)
- `Forge Chief -> Thermogenic Beam: makes stronger: more energy: a bigger X`: Forge Chief gains `spell_mana`; Thermogenic Beam spends `mine mana` (full of (mine mana)). Different kinds in the rows; right only if spell mana counts as mana for the Beam.
- `Fury of the North -> Sejuani: makes stronger: can give it more power and health`: power kept by L18 (champion levelling from Nexus damage with Overwhelm); health has no L18 support. Left as is (family label "power and health").
- `Blighted Ravine -> Avarosan Sentry: triggers: kills it for its death effect`: damage 2 to all units kills only if Sentry has 2 or less health; not visible from rows.

## Must-stay (piece 5)
- `Ice Pillar -> Feel The Rush: makes cheaper: pays for it: more mana or a lower cost` (also Ice Pillar -> Sejuani, Tryndamere: cost 6+)
- `Despair -> Buhru Sentinel: triggers: kills units` (kill effect; Mystic Shot / Shock Blast get none, L11)
- `Will of Ionia -> Tail of the Dragon: triggers: returns it to hand for its effect` (card has "recalled of self")
- `Catalyst of Aeons` has no partner (1 mana pays no cost-6+ card)

(lines read: 2012-2161)

## Piece 6 (read 2162-2311; Jayce Sentinels (rest), Ping City, start of Lux Jayce)

### Cause N: a plain hit on one target is linked to "killed by my spell" cards (L11: a plain hit on one target feeds no "when an enemy dies"; only poison, hits on all and kill effects do)
Buhru Sentinel (and Burgeoning Sentinel): `WHEN killed by mine spell of unit [once_per_game]`. These spells only deal damage to ONE chosen unit: Vile Feast `Drain 1 chosen unit THEN summon Spiderling`, Piercing Darkness `Drain 5 chosen unit`, Thermogenic Beam `damage chosen unit (X)`. In the same decks Mystic Shot (`damage chosen any 2`) and Shock Blast get no such line. Despair (`strike ... THEN kill it`) is right.
- `Piercing Darkness -> Buhru Sentinel: triggers: kills units`
- `Thermogenic Beam -> Buhru Sentinel: triggers: kills units`
- `Vile Feast -> Burgeoning Sentinel: triggers: kills units` and `Vile Feast -> Buhru Sentinel: triggers: kills units`
- Lines: 4 printed (the Burgeoning Sentinel twins of Piercing Darkness / Thermogenic Beam are probably the same)

### Cause O: a card put into the ENEMY's deck gets lines from effects on "my spells" (L9: lines link only cards the player can own; my effects feed my needs)
Poison Dart plants Poison Puffcap in the enemy deck (`keyword_action enemy card in deck <Poison Puffcap Plant>`); the enemy plays it and it hurts the enemy (`damage mine player`). Powder Keg (`increase_effect all mine spell`) and The Dreadway (`damaged by mine spell`) work on spells I play.
- `Powder Keg -> Poison Puffcap: makes stronger: makes its effect bigger`
- `The Dreadway -> Poison Puffcap: makes stronger: doubles its damage`
- Lines: 2

### Cause G (more): `Gangplank -> Jagged Butcher: enables: damages the enemy player; also helps it hit the enemy player` (Ping City). +1 line (G total 30). Clean contrast in the same deck: `Stone Stackers -> Gangplank: helps it level up: damages the enemy player (levels it up)` (Impact: one reason).

## Unsure (piece 6)
- `Albus Ferros -> Undermine: casts its skill`: Albus attack row says damage 3 then raise it; Undermine does 2. Cannot tell from rows whether this is the skill.
- `Marai Warden` (Ping City) again no partner: random cost-1 follower has no named zone.
- `Powder Keg -> Hidden Pathways / Blue Card / Gold Card: makes stronger`: fine if Keg raises any number of a spell or skill (draw 2, spell mana 1, stun), consistent with L21 (spells are a minority).

## Must-stay (piece 6)
- `Vile Feast` has no line to Elise (L3: Vile Feast makes the Spiderling, the Spiderling is what Elise counts)
- `Albus Ferros -> Jayce: puts it into play: draws it from the deck` (a named draw)
- `Final Spark -> Lux: helps it level up: is a spell it needs played for its count` (L17 mana spent on spells)
- `Single Combat -> Forge Chief: triggers: makes it strike for its effect`
- `Lecturing Yordle -> Hidden Pathways: makes cheaper: creates cards`

(lines read: 2162-2311)

## Piece 7 (read 2312-2461; rest of Lux Jayce, deck Lurkers, start of Draven Sion)

### Cause A (more, L10 one reason once): same fact said twice in one line
- `Assembly Line -> Lux: helps it level up: costs 6: pays it alone (levels it up); also is a spell it needs played for its count (levels it up)` (Lux counts mana spent on spells: a 6-cost spell is one spell played, one reason)
- `Thermogenic Beam -> Lux: helps it level up: has a variable cost: pays it alone (levels it up); also is a spell it needs played for its count (levels it up)` (same)
- `Snapjaw Swarm -> Xerxa'Reth, The Undertitan: enables: changes its stats for its effect; also makes stronger: more power` (Xerxa'Reth reads `stat self power ge 8`; "more power" is the same fact)
- +3 lines (Cause A total in my part: 5 + 1 (Ice Pillar -> Trundle) + 3 = 9)

## Unsure (piece 7)
- `Single Combat -> Remembrance: makes cheaper: makes your units die`: Single Combat has no kill effect; it strikes my unit with an enemy unit's strike back (a plain hit, L11 for "dies"?). Remembrance counts my dead units. Could be right because the card's own text hurts my unit on purpose.
- `Forge Chief -> Thermogenic Beam` / `The Forge Of Tomorrow -> Thermogenic Beam`: spell mana vs mana (see piece 5).
- `Thermogenic Beam` has no line to Mageseeker Inciter / Persuader / Jayce (cost 6+ spells): right by L8 (variable cost).

## Must-stay (piece 7)
- `Assembly Line -> Forge Worker: puts it into play: summons`
- `Back to Back -> Mageseeker Inciter: enables: is a spell it needs played for its count` (cost 6 spells; the same set of 6 lines for Persuader)
- `Rek'Sai -> Snapjaw Swarm: makes stronger: gives it more power` (Swarm's own text starts a fight with itself)
- `Snapjaw Swarm -> Frenzied Feast: enables: is a Lurker it asks for`
- `Aspiring Chronomancer` and `Rite of Negation` with no partners (Predict; kill/counter)

(lines read: 2312-2461)

## Piece 8 (read 2462-2611; deck Draven Sion, start of deck Poppy Lux)

### Cause E (more): Rally is not linked to a champion that waits for its own strike (L4, L14)
Sion Returned: `summoned of self DO gain_attack_token mine player`. Draven (level 2): `strikes by self DO create in hand <Spinning Axe> (amount=2)`. Sion Returned has a line to Draven (`helps it level up: helps my units strike more`) but Draven (level 2) shows 2 partners (Spinning Axe, Draven) and no Sion Returned.
- missing `Sion Returned -> Draven (level 2)` (and the line to Draven should also say it makes him strike for his Axe effect)
- Lines: 1 more (Cause E total 3 missing)

### Cause A (more, L10): `Grave Physician -> Sion: helps it level up: makes you discard cards (levels it up); also enables: makes you discard cards; also triggers: makes you discard cards` (one fact said three times; Sion has three abilities that read discards but it is one reason). +1 line (Cause A total 10)

### Cause Q: Ravenous Flock needs a damaged or stunned unit (`damage chosen unit in board [state in damaged] [state in stunned]`); the line comes from a card that deals no damage by its text, while cards whose text damages a chosen unit have none (L2, L18; one rule for all)
- `Sion -> Ravenous Flock: enables: more damage` and `Sion (level 2) -> Ravenous Flock: enables: more damage` (Sion: Overwhelm + power by discards, no damage text)
- Missing (same deck, listed as having no partner): `Mystic Shot -> Ravenous Flock` (damage chosen any 2), `Thermogenic Beam -> Ravenous Flock` (damage chosen unit X); `Get Excited!` damages chosen any 3.
- Either the two Sion lines go (L2/L18) or the damaging spells get the line; today it is inconsistent. Lines: 2 wrong + 2 missing

## Unsure (piece 8)
- `Poppy -> Radiant Guardian`, `Poppy (level 2) -> Radiant Guardian` (Poppy Lux), `For Demacia! -> Radiant Guardian`, `Fury of the North -> Sejuani`: all say "gives it more power and health"; the receiving card only uses power (Lifesteal it gives itself / Overwhelm). By L18 health links only to Taunt or survive-damage waits, so "more power" alone would be right. 4 lines.
- `Otterpus -> Curious Shellfolk` is not among the printed lines (Otterpus creates Prank into the hand); it may be printed in another part.
- `Lost Soul` (cost 8): no "pays for it" line seen in my part.

## Must-stay (piece 8)
- `Flame Chompers! -> Sion: helps it level up: puts your units into play (levels it up)` (summoned power counts in Sion's sum)
- `Arachnoid Sentry -> Ravenous Flock: enables: makes enemy units get Stun`
- `Loping Telescope -> Curious Shellfolk: triggers: creates cards` (Shellfolk waits for `created`)
- `Concerted Strike -> Lux (level 2): triggers: is a spell whose playing sets off its effect`
- `Brightsteel Protector` has no partner in Poppy Lux (Barrier given; no card waits for Barrier)

(lines read: 2462-2611)
