# causes_d_runeterra_3 (runeterra deck check, file lines 2782-4088, all read)
Lines read: 2782-2931, 2932-3081, 3082-3231, 3232-3381, 3382-3531, 3532-3681, 3682-3831, 3832-3981, 3982-4088.
Six causes (A, C, D, F, G, H).

## Cause A: a power/Overwhelm buff linked to a card that waits for an already damaged unit (L18, L4)
- Wrong thinking: Might (+3 power, Overwhelm) "enables more damage" for Scorched Earth. Scorched Earth only needs a unit that is already damaged; Might damages nothing. More power is the game's generic "hits harder".
- Example: `Might -> Scorched Earth: enables: more damage`
- Lines in part: 1.

## Cause C: a draw by kind with a cost filter counted as "draws it from the deck" for one card (L1b, L21)
- Wrong thinking: Zap Sprayfin draws a random spell with cost 3 or less; any cheap spell passes that filter, so it is a draw by kind, no line to Scorched Earth / Noxian Fervor.
- Examples: `Zap Sprayfin -> Scorched Earth: puts it into play: draws it from the deck` ; `Zap Sprayfin -> Noxian Fervor: puts it into play: draws it from the deck`
- Lines in part: 2.

## Cause D: Powder Keg "makes its effect bigger" for spells that have no number to grow (L4)
- Wrong thinking: Powder Keg raises the numbers of spells and skills by 1 (increase_effect amount=1). Paralyzing Bite only stuns and Scorched Earth only kills: no number, so nothing is made bigger.
- Examples: `Powder Keg -> Paralyzing Bite: makes stronger: makes its effect bigger` ; `Powder Keg -> Scorched Earth: makes stronger: makes its effect bigger`
- Lines in part: 2.

## Cause F: a source's own Overwhelm counted as "also helps it hit the enemy player" for another card (L20, L3)
- Wrong thinking: Overwhelm works for the card that has it (Nasus's Fearsome, not Abyssal Eye). Darius, Darius (level 2) and Miss Fortune (level 2) have Overwhelm; Captain Farron's damage comes from a made card (Decimate: L3). Jagged Butcher (Plunder), Monster Harpoon and Gangplank need the enemy player to be damaged, not a way to reach him. The first half of each line ("damages the enemy player") can stay where the source's own text damages the player; the "helps it hit the enemy player" half is wrong.
- Examples: `Darius -> Jagged Butcher: enables: damages the enemy player; also helps it hit the enemy player` ; `Miss Fortune (level 2) -> Darius: helps it level up: damages the enemy player (levels it up); also helps it hit the enemy player (levels it up)` ; `Captain Farron -> Monster Harpoon: enables: helps it hit the enemy player; also makes cheaper: damages the enemy player` ; `Captain Farron -> Gangplank: helps it level up: damages the enemy player (levels it up); also helps it hit the enemy player (levels it up)`
- Lines in part: 7 (Gangplank/Twisted Fate deck 3 Farron lines, plus Farron -> Swain (level 2); Hand of Pirates: Darius, Darius (level 2), Miss Fortune (level 2) to Butcher/Darius). Farron -> Jagged Butcher is the same.

## Cause G (missing lines): power help to cards whose own text reads a power threshold (L18 keeps a line where the card reads the stat)
- Reckoning (IF mine unit with power 5+ ... kill all units with power 4 or less) and Bloody Business (strikes a mine unit with power 5+) read power. Fury of the North (+3 power) and Troll Chant (-2 power on an enemy) are in the same Frozen Rose deck with no line to them (whole deck file: no Fury/Troll Chant line to Reckoning or Bloody Business). Reckoning shows 1 partner, Troll Chant none.
- Lines that should exist: `Fury of the North -> Reckoning` ; `Fury of the North -> Bloody Business` ; `Troll Chant -> Reckoning`
- Lines in part: 3 missing. Moderate confidence.

## Cause H: a discard-and-draw/create card counted as "empties your hand" for Jinx (L4: a help must do the very thing needed)
- Wrong thinking: Rummage discards 2 and draws as many as it discarded; Poro Cannon discards 1 and creates 2 Daring Poro in hand. Both leave the hand as full or fuller; Jinx needs "no cards in hand". (Get Excited! and Spinning Axe discard 1 with no refill: kept.)
- Examples: `Rummage -> Jinx: helps it level up: empties your hand (levels it up)` ; `Rummage -> Jinx (level 2): triggers: empties your hand` ; `Poro Cannon -> Jinx: helps it level up: empties your hand (levels it up)` ; `Poro Cannon -> Jinx (level 2): triggers: empties your hand`
- Lines in part: 4.

## Must-stay (right lines)
- `Vladimir -> Vladimir (level 2): levels into: levels into`
- `Blighted Ravine -> Scorched Earth: enables: damages enemy units or players: Scorched Earth kills them`
- `Rummage -> Fallen Rider: triggers: makes you discard cards` (Fallen Rider: discarded of self)
- `Reckoning -> Yeti Yearling: triggers: kills it for its death effect` (kills power 4 or less; Yearling has Last Breath)
- `Whirling Death -> Akshan: helps it level up: makes it strike for its effect` (Akshan strike advances Palace countdown)
- Also fine: `Get Excited! -> Twinblade Revenant: triggers: kills it for its death effect` (3 damage vs 4|3; Mystic Shot's 2 gets no line: consistent); `Spirit Fire -> Sivir` (Spirit Fire gives enemies "damage self 2 at round end").

## Unsure
- "puts it into play: casts its skill" from a champion/unit to its own skill (`Vladimir -> Crimson Pact (created)`, `Miss Fortune -> Love Tap`, `Miss Fortune (level 2) -> Bullet Time`, `Solari Sunhawk -> Solar Flare`): the shown rows have no row that casts it, but card_link has a "generates" link for each, so likely right.
- `The Dreadway -> Scorched Earth: enables: damages enemy units or players`: Dreadway only repeats damage already dealt (rows: damaged by mine spell/unit DO damage it event_amount); the target is already damaged.
- `Kindly Tavernkeeper -> Crimson Curator/Braum/Scarmother Vrynna` "more health or protection": the card heals 3, it adds no health.
- `Scorched Earth -> Ziggs: makes your units die`: Ziggs counts landmark deaths; only the landmark half of Scorched Earth fits; `Bomber Twins -> Ziggs: makes a landmark it counts`: Twins create the landmark in hand, Ziggs counts landmark deaths.
- `Viktor -> Hex Core Upgrade` has "is the Viktor it names"; `Viktor (level 2) -> Hex Core Upgrade` does not (level 2 is still Viktor).
- `Eclipse Dragon -> Aurelion Sol: changes your units' stats (levels it up)`: Dragon's rows have only a cost change and a create; stats only through its Fury (L15).
- `Single Combat -> Radiant Guardian: enables: makes your units die`: a strike may or may not kill my unit.
- Mystic Shot -> Blade Squire / Avarosan Sentry "kills it for its death effect": plain damage to my own unit; L16 may say this is only "can aim at it".
- Volunteer Elnuk (makes Elnuks on top of the deck) <-> Troop of Elnuks (summons the top Elnuks): the line is worded from Troop's side only.
- Crowd Favorite (stats = number of my other units) has no partner beside Jury-Rig, Flame Chompers!, Boom Baboon (extra units); probably generic.
- `Katarina (level 2) -> Whispered Words: helps my units strike more` and Whispered Words / Bloody Business "Reputation": Reputation has no rows here.
