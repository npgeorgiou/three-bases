# Runeterra reading test: results (27-28 Oct 2026)

## What was built
- All base-game Runeterra entries described (Path of Champions items excluded, `exclude.tsv`): 2,177 cards with text read,
  98 keyword-only, 104 keywords described once, plus one keyword the library lacks (Can't Block, by its name).
- `cards.sqlite`: 2,955 abilities, 4,334 effects; every field a value from `vocab.tsv` (302 values), a number or an id.
  69 cards and keywords the texts name but the library lacks are name-only stubs, so links still work.
- Query layer (`flat.py`): 4,826 trigger rows, 1,474 condition rows, 6,631 effect rows, with each card's keywords copied
  onto it in general terms (Tough on Malphite is damage_reduction) and 109 concept-tree concepts on 12,995 card-concept rows.
- Connections (`connections.py`): an effect causes an event another card waits for; created cards, used keywords, zones
  (discarding empties the hand) and asked-for types or keywords are followed. Example questions and answers: QUERIES.md.

## Tests (cases/REPORT.md): 247 of 247 pass
- 80 mechanics: the expected cards come from the card texts themselves; each query must find 95% of them.
- 40 combos: 5 from the library's combos.tsv (one dropped: the texts do not support it, cases/DROPPED.md) and 35 pairs
  taken from the texts (enabler wording and payoff wording).
- 127 region cases: Claude's list of each region's known mechanics, plus the library's signature, splash and archetype rows
  (three on_kill rows dropped: the old tags are wrong there, DROPPED.md).
- Failing cases were fixed at their cause: text patterns that caught card names, queries that asked too narrowly, missing
  values (copy_keywords), acts that caused no event (gain the attack token), and 87 records re-read with notes.

## Accuracy
- 219 cards (10%) read twice independently; differences judged against the text by a stronger model: the kept readings
  were wrong on 19 (9%), mostly partial (a dropped filter, a missing "only the next time"); all 19 were re-read.
- Word checks (`pattern_check.py`): 12 cards still flagged, all looked at: correct records ("summoned this round" is a
  state, not a summon) or broken source text ("Level up: Missing Translation").
- 122 cards (5%) stay marked unsure: rare mechanics the values cannot say yet; their records hold the closest description.
- Not measured: mistakes both readers made the same way. CHECK_20.md / CHECK_20_RAW.txt are for Kaptain's own check.

## Cost and batch size
- About 33 reader runs for the main reading, 110,000-125,000 tokens each, plus 9 smaller fix runs and 2 judge runs:
  roughly 4.5 million tokens in all.
- Cost per reader was nearly fixed whatever the batch size (39 to 189 cards): the next game uses ~20,000-character batches.

## What the next game needs: GUIDE.md
