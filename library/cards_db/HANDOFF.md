# Handoff: card database (28 Oct 2026)

## Start of a chat
1. Clone with the library (CLAUDE.md "Start of a chat", then `git sparse-checkout disable`). Read only this file.
2. cards.sqlite is committed and current: questions need no build (`ask.py runeterra ...`). Run `run.py runeterra` only after
   changing records, values or scripts; it must then pass every step.
3. Then, as the task needs: PROCESS.md (importing a game), README.md (files, tables, questions), RESULTS.md (Runeterra).

## State
- Runeterra is done and approved (RESULTS.md). Nothing is open on it.
- The next game follows PROCESS.md from step 0. Runeterra's files are the template: supplement_runeterra.py for the
  game's own data, the patterns.tsv lines marked runeterra for the game's own wording, cases/*.tsv rows for its cases.
- Stormbound (started 28 Oct 2026): step 0 done except Kaptain's check of the game words (BRIEF.md "Game words: Stormbound",
  vocab rows marked "pending Kaptain"; questions asked: the mapping, spawned tribe = "Token <Tribe>s", When attacking =
  attacks, words that change by level = test level, card data of Feb 2022). Supplement (42 dropped cards, 15 glossary
  keywords), keyword records (read/stormbound/keywords.jsonl), word-check patterns, 4 batches + second_001 (20 cards),
  cases (62 mechanics, 18 faction, 42 combos). Next: apply his answers, then step 1 (readers on batch_001-004 and second_001).
