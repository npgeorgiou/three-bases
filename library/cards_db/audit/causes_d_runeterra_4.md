# causes_d_runeterra_4 (runeterra deck check, lines 4089-5089)

## Piece 1: lines 4089-4238 (deck Aphelios Zoe, start of Hecarim Zed)

### C1. Same Invoke effect, line to Zoe given to some cards and not others (missed line)
- Zoe counts distinct cards played; the line "creates cards: more different cards to play (levels it up)" is given to Mountain Scryer (Invoke from hand), Solari Priestess, Starshaping, Spacey Sketcher, Aphelios, Lunari Duskbringer. The cards with the same Invoke act get none: Supercool Starchart (1 partner), Behold the Infinite (2 partners), The Fangs.
- Rule: L17 (a card that makes a card links to a card that counts distinct cards played) applied the same to every Invoke / create. Spacey Sketcher (same Invoke, Celestial cost le 3 as Starchart) has the line; Supercool Starchart does not.
- Examples as printed:
  - `Mountain Scryer -> Zoe: helps it level up: creates cards: more different cards to play (levels it up)` (present)
  - `Supercool Starchart (1 partners): (rows above)` (no Zoe line; rows: `WHEN played of self DO keyword_action mine card in hand [type is Celestial] [cost le 3] <Invoke>`)
  - `Behold the Infinite` (rows: `WHEN played of self DO keyword_action mine card in hand <Invoke>`) no Zoe line
- Lines showing it in my part so far: 3 (Starchart, Behold, The Fangs).

### C2. Veiled Temple "triggers: makes more cards to play" from cards that only create cards (probably too many lines)
- Thinking: a card that creates a card into hand "makes more cards to play" for the Temple, which counts cards played this round (any card).
- Rule: L19 (a card put into hand is one more card of any kind, generic), L1 / L1b (any card can be played; Temple's trigger is "a card" of any kind).
- Examples as printed:
  - `Lunari Duskbringer -> The Veiled Temple: triggers: makes more cards to play`
  - `Aphelios -> The Veiled Temple: triggers: makes more cards to play`
  - `Aphelios (level 2) -> The Veiled Temple: triggers: makes more cards to play`
  - `Zoe -> The Veiled Temple: triggers: makes more cards to play`
- Lines showing it: 6 in this piece (also Zoe (level 2)).

### C3. Cards with the Nightfall keyword get no line to The Sky Shadows (missed line)
- The Sky Shadows rows: `WHEN summoned of self IF have mine card [keyword is Nightfall] is DO mana_gain ...`. It needs a Nightfall card in hand: a minority keyword, so a deck choice. Only Zoe (level 2) ("makes your units get Nightfall") is a partner. Aphelios (KW: Nightfall), Aphelios (level 2), Pale Cascade (KW: Nightfall), which are the cards that provide the Nightfall card, have no line.
- Rule: L10 (enables: a thing that must be there), L21 (minority kind stays).
- Examples: `The Sky Shadows (1 partners)`; `Aphelios: KW: Nightfall ...`; `Pale Cascade: KW: Nightfall ...`.
- Lines: 1 card (3 missing lines).

### Unsure (piece 1)
- `Spacey Sketcher -> Aphelios / Zoe: triggers: empties your hand`: Spacey discards one chosen card, not the hand.
- The Sky Shadows gives spell mana: a line to spells (Pale Cascade, Starshaping...) may be missing (L22) or generic.
- `Eye of the Dragon -> Zoe (level 2): triggers: puts your units into play`: Zoe (level 2) rows show only `give_ability mine player`; cannot tell.

### Must stay (piece 1)
- `The Veiled Temple -> Dragonling: makes stronger: can give it more power` and `Pale Cascade -> Dragonling: ...more power and health` (Dragonling has Lifesteal: L18 keeps it).
- `Eye of the Dragon -> Dragonling: puts it into play: summons`
- `Haunted Relic -> Unleashed Spirit: puts it into play: summons`
- `Aphelios -> Aphelios (level 2): levels into`

Read so far: 4089-4238

## Piece 2: lines 4239-4388 (deck Hecarim Zed, start of Azir Irelia)

### C4. Same "gives Ephemeral to a unit in hand" act, lines to the Ephemeral-readers given to Oblivious Islander but not to Stalking Shadows (missed lines)
- Hecarim levels up from attacks by Ephemeral units; Moonlit Glenkeeper triggers on a summoned Ephemeral unit. Oblivious Islander (gives Ephemeral to a unit in hand) has both: `Oblivious Islander -> Hecarim: helps it level up: makes your units Ephemeral (levels it up)` and `Oblivious Islander -> Moonlit Glenkeeper: triggers: makes your units Ephemeral`. Stalking Shadows gives Ephemeral to the copy of a follower in hand (`give_keyword it <Ephemeral> for permanent`) and has the Shadow Apprentice line ("makes your units get Ephemeral"), but its 3 lines (Shadow Apprentice, Shark Chariot, Undying Revenge) lack Hecarim and Moonlit Glenkeeper.
- Rule: L10 / L17 (same reason, said by its strongest kind, for every card that does it).
- Lines showing it: 1 card (Stalking Shadows), 2 missing lines.

### Unsure (piece 2)
- `Sapling -> Shark Chariot: triggers: makes your units attack (by fighting)`: Sapling has only KW Challenger and no text that makes a unit attack (L2 / L15: Challenger works when the card attacks). Shark Chariot's rows do not show what its granted ability needs.
- `Oblivious Islander -> Shark Chariot` and `Stalking Shadows -> Shark Chariot` ("kills it for its death effect"): the Chariot already has Ephemeral, so giving it Ephemeral adds nothing (L15, keyword to a card with the same keyword). Glimpse Beyond -> Shark Chariot (a real kill) is right.
- `Hecarim (level 2)` and `Zed (level 2)` rows hold abilities given to the player; cannot judge their lines.

### Must stay (piece 2)
- `Moonlit Glenkeeper -> Zed: makes stronger: more power` (Zed's Living Shadow takes `stat power of (self)`: L18 reads its power).
- `Dragon Ambush -> Hecarim: helps it level up: another attack ... also makes units attack` (start_attack on Ephemeral Dragonlings).
- `Glimpse Beyond -> Undying Revenge: enables: makes your units die: Undying Revenge brings them back`
- `Hecarim (level 2) -> Spectral Rider: puts it into play: summons`

Read so far: 4089-4388

## Piece 3: lines 4389-4538 (deck Azir Irelia)

### C5. Return to hand of a unit with a Play or Summon effect: line missing for Defiant Dance (missed lines)
- Defiant Dance (`return_to_hand chosen unit in board`, 5 partners, all its lines printed) links only to Irelia / Azir / Dais (attack reasons). The deck has units whose own text has a Summon or Play effect that a return lets you use again: Dunekeeper (`WHEN summoned of self DO summon in board <Sand Soldier>`) and Forsaken Baccai (`WHEN played of self IF it_matches ... DO keyword_action ... <Predict> THEN stat_change self`; it has NO partner at all). Neither gets a line from Defiant Dance.
- Rule: L14 ("a return to hand of a card with Play or Summon" is kept), L17.
- Examples: `Defiant Dance (5 partners)`; `Forsaken Baccai: WHEN played of self IF it_matches [type is Darkin] ...`; `? Dunekeeper: WHEN summoned of self DO summon in board <Sand Soldier>`.
- Lines showing it: 2 missing lines (1 card in (b), 1 in (a)).

### C6. "More power" given to a card that does not read power (wrong part of a line)
- `Desert's Wrath -> Sand Soldier: puts it into play: summons; also makes stronger: gives it more power`. Sand Soldier rows: `KW: Ephemeral | WHEN strikes_nexus by self DO damage enemy player (amount=1)`: the damage is fixed 1, it does not read its power, and more power does not help it reach the Nexus.
- Rule: L18 (more power is generic unless the card's text reads the stat), L14.
- Lines showing it: 1 in this piece (the "summons" part stays).

### Unsure (piece 3)
- `The Emperor's Army -> Sand Strategy / Sunsoaked Fervor: puts it into play: casts its skill`: Emperor's Army rows show only `summon <Sand Soldier>` and `keyword_action <Predict>` (Predict = choose 3 cards in deck, put on top); no cast of a skill is visible. Same for `The Stagehand -> Stunning Performance: puts it into play: casts its skill` (deck 2): the Stagehand row is a plain `stun`, not a cast.
- `Blossoming Blade / Defiant Dance / Flawless Duet / Ribbon Dancer -> Azir: makes your units attack (it levels up from what it then does)`: second-order (the attack sets off Azir's own summon); accepted as written.

### Must stay (piece 3)
- `Emperor's Dais -> Shaped Stone: enables: is a landmark it needs summoned for its count`
- `Desert's Wrath -> Sparring Student: triggers: puts your units into play`
- `Soldiers' Summons -> Azir: helps it level up: puts your units into play (levels it up)`
- `Irelia -> Irelia (level 2): levels into`

Read so far: 4089-4538

## Piece 4: lines 4539-4688 (deck Elu Thresh)

### C7. "Makes units die / attack (by fighting)": every unit can fight, so these lines come from nothing in the text
- Thinking: a unit that can be blocked / blocks / has a fight keyword "makes units die (by fighting)" for Viego (level 2) (dies of any unit) and "makes your units attack (by fighting)" for Shark Chariot. A unit fighting and dying is what every card can do.
- Rule: L2 (the game's rules are no combo; only an added attack, a strike now, or a keyword that does the need, such as deathtouch), L1, L15 (Challenger picks when attacking, a keyword's inner working), L20 (Elusive works for the card that has it).
- Examples as printed (rows have no kill, strike or attack text; Camavoran Soldier is only `WHEN summoned of self DO summon <Encroaching Mist>`; Fae Guide only gives Elusive):
  - `Camavoran Soldier -> Viego (level 2): triggers: makes units die (by fighting)`
  - `Fae Guide -> Viego (level 2): triggers: makes units die (by fighting)`
  - `Invasive Hydravine -> Viego (level 2): triggers: makes units die (by fighting)` (only Fearsome)
  - `Ghastly Band -> Shark Chariot: triggers: makes your units attack (by fighting)`
- Lines showing it: 8 (also Hecarim, Hecarim (level 2), Thresh, Thresh (level 2) -> Viego (level 2)). Death Mark / Glimpse Beyond -> Viego (level 2) ("makes units die", a real kill or Ephemeral) are right.

### C8. A summon from hand or deck linked to a card that only exists after a level-up
- `Thresh (level 2) -> Hecarim (level 2): triggers: makes it attack for its effect`. Thresh (level 2) rows: `summon chosen mine unit in deck/hand [category is champion] in board THEN start_attack it`. A level 2 form is never in the hand or deck, so only Hecarim (level 1) can be summoned and attacked (that line exists: `Thresh (level 2) -> Hecarim`).
- Rule: L9 (lines link only cards a player can own in that place).
- Lines showing it: 1.

### Unsure (piece 4)
- `Shark Chariot -> Hecarim: helps it level up: makes units attack`, `Shark Chariot -> Viego/Thresh`: Shark Chariot rows show only a Last Breath that gives the player an ability; whether its own attack counts for Hecarim is not visible (L2 if it is just an ordinary attack by an Ephemeral unit).
- Ghost (gives Elusive) has no partner; consistent with L20 since no card here needs the Nexus.

### Must stay (piece 4)
- `Death Mark -> Thresh: helps it level up: makes units die (levels it up)`
- `Glimpse Beyond -> Viego: helps it level up: makes your units die (levels it up); also triggers: makes your units die`
- `Ghastly Band -> Viego: ... dies by its own effect (Ephemeral)`
- `Thresh (level 2) -> Hecarim: ... also makes it attack for its effect`
- `Opulent Foyer -> Ghastly Band: puts it into play: summons`

Read so far: 4089-4688

## Piece 5: lines 4689-4838 (deck Gemstone Yi, start of Ephemeral Shadow Isles Ionia)

### C9. Power lines go to Master Yi (level 2), which has no damage text, and not to Master Yi (level 1), which reads the damage (wrong target)
- Master Yi (level 1) rows: `WHEN always IF event_count damaged by mine unit [card is Master Yi] damage ge 12 this_game DO level_up self` (reads the damage it deals). Master Yi (level 2) rows: `WHEN attacks by self DO strike self to lowest enemy unit by power in board` plus cost and Flow power; no count of damage. Yet every power line points to level 2 and Master Yi (level 1) has only 2 partners (Out Of The Way, level 2):
  - `Mentor of the Stones -> Master Yi (level 2): makes stronger: more power: its text uses the damage it deals`
  - `Gem -> Master Yi (level 2): makes stronger: more power: its text uses the damage it deals`
  - `Divine Judgment -> Master Yi (level 2): makes stronger: can give it more power`
  - `Pale Cascade -> Master Yi (level 2): makes stronger: can give it more power and health`
  (also Twin Disciplines)
- Rule: L18 (a line stays where the card's own text reads the damage or the stat). The reason text "its text uses the damage it deals" fits level 1; level 2 only starts a strike, so keep or drop its lines by the Deepwood Stalker case, but level 1 is missing the same lines.
- Lines showing it: 5 (all power lines to Master Yi in this deck); missed on level 1: Divine Judgment, Pale Cascade, Mentor, Gem, Twin Disciplines.

### Unsure (piece 5)
- Taric (level 2) has 1 partner: its text copies the top spell in discard to the unit on its right, a need that a spell in discard is the deck's majority kind (L21), so no line is probably right.
- Deep Meditation and Rivershaper (draw 2 / draw a spell by kind) have no partner: right by L1b.
- We Stand Together and Wuju Style buff units and should have the Out Of The Way and Taric lines the other buffers have; their lines are not printed in my part, cannot check.

### Must stay (piece 5)
- `Divine Judgment -> Taric: helps it level up: targets your cards (levels it up)` (Taric counts `targeted of mine unit`; same for Meditate, Pale Cascade).
- `Master Yi -> Out Of The Way: enables: changes your units' stats` (Out Of The Way needs `[state is buffed]` units).
- `Wuju Style -> Meditate: puts it into play: creates`
- `Dragoncaller -> The Empyrean: puts it into play: summons`
- `Taric -> Taric (level 2): levels into`

Read so far: 4089-4838

## Piece 6: lines 4839-5089 (rest of deck Ephemeral Shadow Isles Ionia, deck Unstoppable Yasuo)

### C10. Ephemeral given only to the card's own copy, linked as if it killed other cards (wrong target)
- Prancing Sea Spirits rows: `copy self in board THEN give_keyword it <Ephemeral>`; `it` is its own copy, no other unit gets Ephemeral or dies. Its lines to Ceaseless Sentry and Hapless Aristocrat ("kills it for its death effect") need a kill of those cards. Encroaching Shadows (gives Ephemeral to all units in hand and deck) is the card that does that, and its same lines are right.
- Rule: L14 / L9 (help to "it" reaches only the target; a made card acts on its own).
- Examples:
  - `Prancing Sea Spirits -> Ceaseless Sentry: triggers: kills it for its death effect`
  - `Prancing Sea Spirits -> Hapless Aristocrat: triggers: kills it for its death effect`
- Lines showing it: 2 (the Shadow Apprentice and Undying Revenge lines stay: the copy is summoned Ephemeral and dies).

### C11. A strike on enemy units linked as if it killed my own unit with a Last Breath
- `Yasuo (level 2) -> Blue Sentinel: triggers: kills it for its death effect`. Yasuo (level 2) rows: `given_keyword ... of enemy unit [keyword is Stun] DO strike self to it` and `recalled ... of enemy unit DO strike self to it`: it strikes ENEMY units; Blue Sentinel (`WHEN dies of self DO summon <Crest of Insight>`) is my unit and does not die by that.
- Rule: L9 (my effects feed my needs; an effect on enemies feeds needs about enemies), L7 (read who does it).
- Lines showing it: 1.

### C12. One reason said twice with different words (enables + triggers, or another attack + makes units attack)
- Thinking: the same Stun-giving act is told as "enables", "helps it level up" and "triggers" in one line. Fae Bladetwirler and Yasuo (level 2) rows only have reactions (`WHEN given_keyword ... [keyword is Stun]`), no count or state that must be there, so "enables" is not a reason beside "triggers".
- Rule: L10 (one reason is said once, by its strongest kind).
- Examples as printed:
  - `Steel Tempest -> Fae Bladetwirler: enables: makes units get Stun; also triggers: makes units get Stun`
  - `Steel Tempest -> Yasuo (level 2): enables: makes enemy units get Stun; also triggers: makes enemy units get Stun`
  - `Malphite (level 2) -> Yasuo: helps it level up: makes units get Stun (levels it up); also enables: makes enemy units get Stun; also triggers: makes enemy units get Stun`
- Lines showing it: 20+ in deck Unstoppable Yasuo (every Stun-giver to Fae Bladetwirler, Yasuo, Yasuo (level 2)). The same doubled wording appears with attacks in deck Azir Irelia: `Blossoming Blade -> Irelia (level 2): triggers: another attack; also makes your units attack` (about 20 lines) and `Dragon Ambush -> Hecarim: ...another attack (levels it up); also makes units attack (levels it up)` (Hecarim Zed). Paddle Star lines (only "enables": it needs a stunned enemy) are right.

### Unsure (piece 6)
- "puts it into play: casts its skill" lines (`The Rootbound Path -> Root Canopy / Sentient Seedling`, `Malphite -> Rockslide`, `Malphite (level 2) -> Rockslide`, earlier Emperor's Army, The Stagehand): the rows of the source card show the skill's plain effect (draw, stun, cost -1), not a cast. If the text really says "cast X" the lines are right; the rows do not show it.
- `Blue Sentinel -> Malphite: helps it level up: puts units into play`: its Last Breath summons a landmark (Crest of Insight), so the word "units" is wrong; the line itself fits L3 (Malphite waits for landmarks summoned).
- Malphite (level 2) rows have `WHEN played of self` and `WHEN summoned of self`: a level 2 form is not played from hand (same doubt as C8).
- Deny (counter a spell) has no partner: right.

### Must stay (piece 6)
- `Encroaching Shadows -> Ceaseless Sentry: triggers: kills it for its death effect` (gives Ephemeral to all units in hand and deck).
- `Sanctuary -> Yasuo: helps it level up: returns units to hand (levels it up)` with no "triggers" part (Sanctuary recalls only my unit; the damage trigger needs an enemy).
- `Peerless Artistry -> Yasuo: helps it level up: returns units to hand (levels it up); also triggers: returns enemy units to hand` (a Recall that can aim at enemies).
- `Steel Tempest -> Paddle Star: enables: makes enemy units get Stun`
- `The Iron Conquest -> Navori Bladescout: triggers: brings it back: its summon effect goes off`

Read so far: 4089-5089 (all)
