# Runeterra: results (28 Oct 2026)

## What exists
- 2,479 cards and 107 keywords described: the library's base-game entries (Path of Champions excluded, exclude.tsv) plus
  186 cards and keywords the library lacked, taken from Riot's own data (supplement/runeterra.jsonl), and Deep and Plant
  defined by Kaptain (supplement/runeterra_kaptain.jsonl).
- cards.sqlite: 3,109 abilities, 4,582 effects, 358 values; flat_ref 13,658 rows over 40 happenings; 109 concept-tree
  concepts on the cards.
- Mark of the Storm is a keyword with Kaptain's definition; Phased Moon Weapon is the type Moon Weapon. Spriteling stays a
  name: no Runeterra source defines it. Can't Block has a record by its name.

## What it answers (ask.py; example answers in QUERIES.md)
- Which cards care about a happening, whatever the wording (trigger, condition, count, picked by it): e.g. 127 cards
  benefit from my units dying. Which cards make it happen (kill -> dies, summon -> summoned...).
- Cards by concept (removal, revive, stat_gain, ...); how card A sets off card B, every reason ranked; a card's partners.

## Quality
- 248 of 248 case tests pass (cases/REPORT.md): 81 mechanics found from the texts at 95%+, 40 combos, 127 region cases.
- Word check: 0 open flags; 9 flags decided one by one (patterns/verdicts.tsv).
- 10% read twice independently: the kept readings were wrong on 9%, all re-read. Kaptain approved CHECK_20 (28 Oct).
- 73 cards marked unsure: mechanics the values cannot say yet, each on one card or on cards with the same text
  (Voidling, Patched Porobot); the record holds the closest description.
- Not measured: mistakes both readers made the same way.

## Limits
- Connections are broad by design: a card that makes a happening connects to every card that cares about it on a
  matching side. The reasons are ranked (most direct first), not filtered.

## Cost
- About 53 reader runs of 95,000-125,000 tokens each, plus 2 judge runs: roughly 5.5 million tokens. A reader costs nearly
  the same for 40 or 190 cards, so batches are ~20,000 characters.

# Monster Train: results (29 Oct 2026, waiting for Kaptain's check of CHECK_20_monster_train.md)

## What exists
- 284 cards (282 from the wiki's Module:Cards/Data in library/tools/convert/monster_train_cards.psv, the two wax tokens
  from the wiki page Legion of Wax), the 12 champions with their upgrade paths, 70 glossary keywords with the wiki's
  definitions (supplement_monster_train.py). Game words in BRIEF.md "Game words: Monster Train"; every keyword has a
  concept (Frostbite and Rally have their own rows, monster_train:Frostbite and monster_train:Rally).

## Quality
- run.py passes every step: mechanics, 7 guide decks (decks.tsv) and the guides' card pairs (combos.tsv) all pass; word
  check 0 open flags; no stub names. Unsure: Hallowed Halls ("until it exceeds its Capacity"), Eternal Kinstone ("cannot
  be removed") and 8 keyword entries whose rule no value says (Piercing, Trample's "next unit", ...).
- Second reading: 28 cards, 17 the same; of the 11 others, 10 the same meaning in another form (one became normalize N14)
  and 1 kept reading fixed.
- Cost: three readers (cards, keywords, second reading); the unsure cards fixed by rule (fixes/monster_train/).

# Inscryption: results (30 Oct 2026, v45; reviewed by Kaptain; families F1-F18 in deck_read_inscryption.md)

## What exists
- 251 cards from the Inscryption wiki's card boxes (supplement_inscryption.py; the library had merged and dropped cards),
  108 sigils and traits; sigils are each card's Keywords field, so 212 cards take their records from their sigils.
  Special card behaviours (Ouroboros, Cat, Pack Mule, Caged Wolf, Strange Frog, Child 13, Daus, Pelts, the giants) are in
  the texts from the wiki page Special Card Behaviours.
- Game rules (read/inscryption/game_rules.jsonl): units fight, Bones from deaths, units can be sacrificed, and Blood,
  Bones and Green / Orange / Blue Mox costs, which are needs of the cards whose cost names them.
- Decks: 17 kept (decks.tsv): 3 Act II starters with links, 4 full 20-card decks from Steam (Archeronline4U, Burntcookies1,
  BEAR, the 666-damage guide), 7 core lists from gamersdecide.com (Acts I-III), 3 Kaycee's Mod decks built as the wiki's
  Kaycee's Mod tips page (rev 13001) says. 20 decks with few or no links are listed with their source in
  decks_dropped_inscryption.tsv (the page does not draw them; cases keep their card lists).
- Why the networks are thin (30 Oct 2026): only 31% of Inscryption's cards act on another card of mine (Runeterra 74%,
  Faeria 62%, Duelyst 58%, Stormbound 45%) and 18% have no effect at all (vanilla 1/1, 2/2 cards). Most sigils act on the
  card itself (Airborne, Sprinter, Mighty Leap, Bifurcated Strike). The game's synergy is its costs (sacrificing cards for
  Blood, Bones from deaths), which every card can do by the rules, so they make no line (Kaptain's rule). What is left:
  Worthy Sacrifice and Morsel, Bone makers to Bones cards and spenders, Mox gems to Mox cards, Ants, conduits and circuits,
  Leader, and cards that make cards (Warren, Tomb Robber, Ant Queen).
- run.py passes; cases 72 of 72 (23 sigil mechanics, 7 combos, 4 guide decks, 8 faction cases, 17 network lines, shared
  cases); word check, text audit and link audit 0.
- Unsure records left (no value for one card's need): Build-a-Card, Campfire, Card Recycle, Pliers, Wiseclock, Pack Mule,
  The Limoncello, Glitched card, Dead Byte, Detonator,
  Energy Conduit, Tidal Lock ("pulls small creatures into its orbit": no place stated), Trinket Bearer, Satisfies Ring Trial, Bell Ringer, Kraken Waterborne, Mox Sigils, Cat and Child 13 (a count
  across battles).
- Energy ramp (Energy Bot, Energy Conduit, Extra Battery, Hrokkall) is concept base_resource_gain, as mana ramp in the other
  games, with no line to Energy-cost cards (Kaptain 29 Oct 2026).
- Positions: lanes (same_lane, the opposing space), sides (adjacent), circuits (two conduit cards); strikes into empty
  spaces hit the opponent; who benefits from a place is said on the line ("gives it +1|+0 (when next to it)").

# Faeria: results (29 Oct 2026, waiting for Kaptain's check of CHECK_20_faeria.md and CONCEPTS_faeria.md)

## What exists
- 462 cards from Abrakam's own card export (github.com/abrakam/Faeria_Cards; the library had 443, 13 of them with export
  markup in their texts) and 23 keywords (the library's 19 from the faeria.com Keyword Rulings guide, plus Wild, Fight,
  Teleport, Transform). 16 tokens named by texts stay names: the export has collectible cards only (Frog, Mecha, Angry Yak,
  Treasure Map, Manta, Hydra Head, Yak Guard, Baby Yak, Guardian, Explore, Ostregoth, Sky Swallower, Angry Prairie Yak, and
  Looking Glass Phantasm's own joke name "msatnahP ssalG gnikooL").
- Game rules (read/faeria/game_rules.jsonl): units fight (an enemy unit or structure, or the enemy god) and harvest the
  wells next to them (mine or the enemy's).
- The board, written the same way as every game with spaces (BRIEF "The board"): ground of spaces (lands, ocean, wells),
  land making and taking, neighbours, straight lines and distances, where a card may enter, moving onto a place.
- 12 full decks in decks.tsv (faeria.com The Hub), all read card by card; 16 deck-read lines are cases nfa01-nfa18.

## Quality
- run.py passes; cases 113 of 113 (43 Faeria mechanics, 12 combos, 40 network lines, 5 guide-deck explanations, shared cases); word check 0 flags;
  text audit 0; every other game still passes.
- Link audit, explained: nothing in a card makes "turn_option_chosen" (Flamestoker, Ignus, Wrath of Ignus wait for the
  player picking +1 faeria on the power wheel, which the player does every turn); the 14 token names above.
- Unsure records left (no value for one card's need): Master Swordsman ("during your turn"), Celeste ("only 1 of each
  card in your deck"), Thyrian Expedition ("total land cost"), and the keyword entries Flying, Taunt (whom the attack goes
  to), Ranged Attack (no retaliation), Wild, Transform.
- Not in the database: each turn a player builds lands, draws or takes faeria (the power wheel). Cards that count my lakes
  or forests are fed only by cards that make lands, not by the player's own land building.

# Duelyst: results (29 Oct 2026, waiting for Kaptain's check of CHECK_20_duelyst.md and CONCEPTS_duelyst.md)

## What exists
- 1,117 cards and 46 keywords from the open-sourced game's own card factories (open-duelyst; supplement_duelyst.py). Cards
  the source names twice keep the collectible card's name; the others are "<name> (<kind>)". Stubs (named, no card): Spriggin Kin, Spirit Wolf; the two game rules are rows too.
- Generals are category `leader`: the card is its player (help to "your General" reaches only it; it fights by the rules).
- Game rules (read/duelyst/game_rules.jsonl, from the game's tutorial and tips): units and Generals attack and are
  counterattacked; summons go next to my units; mana springs, the 9x5 board.
- The board in the shared form (BRIEF "The board"): nearby, behind, in front, rows and columns, center column, 2x2 and 3x3
  areas, corners, starting sides, tiles (Shadow Creep, Hallowed Ground, Exhuming Sand, Primal Flourish, mana springs).
  Backstab, Zeal and Infiltrate are needs for moves; teleports and swaps feed them.
- 10 full decks in decks.tsv (from deck codes, supplement/duelyst_deck_codes.tsv), all read card by card twice
  (deck_read_duelyst.md, 24 families fixed by rule), then Kaptain's check (9 rules); cases ndu01-ndu47.
- Each General's Bloodbound Spell is its own card (its signature card), drawn as a node next to the General.

## Quality
- run.py passes; cases 94 of 94 (34 Duelyst mechanics, 47 network lines, shared cases); text audit 0; every other game still
  passes.
- Link audit, explained: Pandora summons "a 3/3 Spirit Wolf with a random ability"; the source has five wolves under other
  names, so Spirit Wolf stays a name.
- Wording still shared with other games: a player's damage reads "your Nexus or base" (the General in Duelyst).

# Into the Breach: results (30 Oct 2026, v51, done; deck_read_into_the_breach.md)

## What exists
299 cards (42 mechs, 104 weapons, 17 passives, 20 pilots, Vek, tiles, 6 deployed units) and 27 keywords, read once; 30 cards
read twice. 23 decks in decks.tsv: 14 official squads, 6 players' custom squads, 3 builds from players' runs with extra weapons; a
deck is each mech followed by what it carries (its starting weapon and passive, at most one extra weapon).

## Quality
- run.py passes every step; word check 0 flags, text audit 0 unexplained, 27 cases. Families F1-F6 fixed by rule (v48.py),
  F13-F16 from Claude's check of 20 cards (v51.py), F20 weapons as cards in the decks (v52.py), F7-F12, F17-F19 and
  F21-F23 in shared code (network.py, refs.py, deck_analysis.py).
- Link audit, explained: Spore, Alpha Spore, Alpha Blob, Blob Leader, Boulder, Unstable Boulder, Freeze Mine, Strange Pod and
  Strange Object are things Vek and tiles put on the board; the source has no entry for them and the wiki is not reachable
  from here, so they stay names. Emerging and High Tide are each one tile with two library pages (terrain and modifier,
  same text); both are read alike and no deck holds them.
- Deck networks: all 20 read twice; F7 kept by Kaptain, F8-F12 fixed and approved by Kaptain (30 Oct 2026). Every squad
  explained by ask.py analyze with no false weak spot (Rusting Hulks: Smoke for Storm Generator, case dtb01).
- Keywords: CONCEPTS_into_the_breach.md (every keyword and its concept, checked twice). `ask.py all compare forced_movement
  shield damage_over_time` shows its cards next to the other games' (it has the most forced movement of all games).
- Check of 20 cards: CHECK_20_into_the_breach.md (ids in CHECK_20_into_the_breach_ids.txt), checked by Claude at Kaptain's
  word (30 Oct 2026: "its YOUR task"); errors and fixes in deck_read_into_the_breach.md "Check of 20 cards".
