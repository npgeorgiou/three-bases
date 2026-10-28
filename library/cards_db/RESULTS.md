# Runeterra: results (28 Oct 2026)

## What exists
- 2,479 cards and 107 keywords described: the library's base-game entries (Path of Champions excluded, exclude.tsv) plus
  186 cards and keywords the library lacked, taken from Riot's own data (supplement/runeterra.jsonl), and Deep and Plant
  defined by Kaptain (supplement/runeterra_kaptain.jsonl).
- cards.sqlite: 3,109 abilities, 4,582 effects, 358 values; flat_ref 13,658 rows over 40 happenings; 109 concept-tree
  concepts on the cards.
- Names that nothing defines stay names: Mark of the Storm (a mark granted to enemies), Spriteling, Phased Moon Weapon.
  Can't Block has a record by its name.

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
