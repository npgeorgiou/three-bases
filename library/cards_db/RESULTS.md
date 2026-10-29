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

# Inscryption: results (29 Oct 2026, waiting for Kaptain's check of CHECK_20_inscryption.md and CONCEPTS_inscryption.md)

## What exists
- 251 cards from the Inscryption wiki's card boxes (supplement_inscryption.py; the library had merged and dropped cards),
  108 sigils and traits; sigils are each card's Keywords field, so 212 cards take their records from their sigils.
  Special card behaviours (Ouroboros, Cat, Pack Mule, Caged Wolf, Strange Frog, Child 13, Daus, Pelts, the giants) are in
  the texts from the wiki page Special Card Behaviours.
- Game rules (read/inscryption/game_rules.jsonl): units fight, Bones from deaths, units can be sacrificed, and Blood,
  Bones and Green / Orange / Blue Mox costs, which are needs of the cards whose cost names them.
- 19 decks in decks.tsv, all read card by card: the four Act II starters, five players' Act II decks, the Act I and Act III
  starters and the eight Kaycee's Mod starters.

## Quality
- run.py passes; cases 56 of 56 (20 sigil mechanics, 7 combos, 4 guide decks, 7 faction cases, 12 network lines, shared
  cases); word check, text audit and link audit 0.
- Unsure records left (no value for one card's need): Build-a-Card, Campfire, Card Recycle, Pliers, Wiseclock, Pack Mule,
  The Moon, The Limoncello, Glitched card, Clinger, Dead Byte, Detonator, Energy Conduit, Finical Hatchling, Loose Tail,
  Tidal Lock, Trinket Bearer, Satisfies Ring Trial, Bell Ringer, Kraken Waterborne, Mox Sigils, Cat and Child 13 (a count
  across battles).
- Open for Kaptain: Energy ramp (Battery Bearer, Energy Bot) has no line to Energy-cost cards, as mana in the other games.

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
- run.py passes; cases 99 of 99 (43 Faeria mechanics, 12 combos, 30 network lines, 5 guide-deck explanations, shared cases); word check 0 flags;
  text audit 0; every other game still passes.
- Link audit, explained: nothing in a card makes "turn_option_chosen" (Flamestoker, Ignus, Wrath of Ignus wait for the
  player picking +1 faeria on the power wheel, which the player does every turn); the 14 token names above.
- Unsure records left (no value for one card's need): Master Swordsman ("during your turn"), Celeste ("only 1 of each
  card in your deck"), Thyrian Expedition ("total land cost"), and the keyword entries Flying, Taunt (whom the attack goes
  to), Ranged Attack (no retaliation), Wild, Transform.
- Not in the database: each turn a player builds lands, draws or takes faeria (the power wheel). Cards that count my lakes
  or forests are fed only by cards that make lands, not by the player's own land building.
