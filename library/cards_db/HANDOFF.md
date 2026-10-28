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
- Stormbound (28 Oct 2026): card data = Stormbound Kitty's current card database (284 cards, supplement_stormbound.py,
  replaces the library's 2022 copy). Read (batch_001, fix_001), second reading done (24 cards, the kept reading right on
  every difference). run.py stormbound passes every step: 120 of 120 cases, word check 0 flags, no stubs, 15 unsure
  rows (needs unique to one card). Waiting for Kaptain's check: CHECK_20_stormbound.md (ids in CHECK_20_stormbound_ids.txt).
  After his approval: fix what he finds for all cards with the same problem, add a few approved records as examples to
  BRIEF.md, write Stormbound's results in RESULTS.md.
