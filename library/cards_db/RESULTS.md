# Runeterra reading test: results (27-28 Oct 2026)

## What was built
- All 2,431 Runeterra entries described: 2,333 read, 98 keyword-only (no reading needed), plus the 104 keywords described once.
- `cards.sqlite`: 3,092 abilities and 4,497 effects, every field a value from `vocab.tsv` (280 values), a number or a link.
  69 cards and keywords the texts name but the library lacks (Dauntless Vanguard, Plant, Tentacle...) are name-only stubs,
  so the links still work.
- Connections are queries over the links (`queries.py feeds/fed_by/event/same`): an effect causes an event, another card's
  ability waits for that event on a matching target. Created cards and used keywords are followed through their own records.

## Accuracy
- 219 cards (10%) were read twice by independent readers. 131 identical; 44 the same meaning written differently;
  44 with a misreading in at least one reading (judged against the card text by a stronger model).
- The readings kept in the database were wrong on 19 of the 219 (about 9%), mostly partial: a missing "only the next time",
  a dropped filter, "hand or deck" read as deck only. Those 19 were re-read with the judge's notes and replaced.
  Errors where both readers made the same mistake are not measured; Kaptain's own check of `CHECK_20.md` is the outside test.
- 120 cards (5%) stay marked unsure: a long tail of about 100 rare mechanics the values cannot say yet ("in 5+ different
  rounds", "every third time", swapping Power and Health). Their records hold the closest correct description.
- The 44 "same meaning, different form" cases led to the normalization rules N1-N4 (`normalize.py`), so queries match.

## Batch size and cost
- Batches were cut at 8,000 characters of card text (about 100 cards; 59-189 cards depending on text length).
- One reader per batch used about 110,000-125,000 tokens, roughly 1,100 tokens per card including the reader's fixed start
  (brief, values, checking). Many readers wrote their records through a small script instead of the Write tool; quality was
  the same and it used fewer steps.
- Whole test, all readers: about 33 runs, roughly 3.8 million tokens (22 batches, keywords, 2 second readings, 6 re-read
  batches, the judge, the trial corrections).
- The table grew while reading: v1 (13 cards) to v3, 226 to 280 values; every change and the card that caused it is in
  `CHANGES.md`. Values were added in rounds from the readers' proposals, then the unsure cards were re-read.

## What went wrong and was fixed
- Readers were stopped by a session limit; their part files were saved and the batches finished (rules in README.md).
- A merge ran while two readers were still writing, so they rewrote their files; merges now wait for readers to finish.
- Readers shared a scratch folder once; each reader now uses its own.
