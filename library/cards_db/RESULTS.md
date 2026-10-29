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
- 284 cards (282 from the wiki's Module:Cards/Data already in the repo, library/tools/convert/monster_train_cards.psv; the
  two wax tokens from the wiki page Legion of Wax), the 12 champions with their upgrade paths, 70 glossary keywords with the
  wiki's definitions (supplement_monster_train.py). 24 tribes from the library.
- Game words in BRIEF.md "Game words: Monster Train"; every keyword has a concept (vocab keyword rows; Frostbite and Rally
  mean something else here than in Runeterra, so they have rows monster_train:Frostbite and monster_train:Rally).

## Quality
- run.py monster_train passes every step: 149 of 149 cases (77 mechanics, 28 clan cases, 44 combos), word check 0 open flags,
  no stub names. 10 entries stay unsure (3 cards: Legion of Wax's twin-making is described, Hallowed Halls "until it exceeds
  its Capacity", Eternal Kinstone "cannot be removed"; 7 keyword entries whose rule no value says, such as Piercing).
- Second reading: 28 cards, 17 the same; of the 11 others, 10 the same meaning in another form and 1 kept reading fixed
  (Hallowed Halls "to this floor"). The draw form became normalize N14 for every game.

## Cost
- Three readers (cards, keywords, second reading). The cards the first reading marked unsure were fixed by rule
  (fixes/monster_train/v24.py, v25.py) instead of a re-read; the two tokens were recorded by Claude.
