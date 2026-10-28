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
