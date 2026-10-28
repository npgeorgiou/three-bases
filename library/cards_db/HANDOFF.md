# Handoff: card database (28 Oct 2026)

## Start of a chat
1. Clone with the library (CLAUDE.md "Start of a chat", then `git sparse-checkout disable`). Read only this file.
2. cards.sqlite is committed and current: questions need no build (`ask.py runeterra ...`). Run `run.py runeterra` only after
   changing records, values or scripts; it must then pass every step.
3. Then, as the task needs: PROCESS.md (importing a game), README.md (files, tables, questions), RESULTS.md (Runeterra).

## State
- Runeterra is done and approved (RESULTS.md).
- Stormbound: every build step passes; waiting for Kaptain's check of CHECK_20_stormbound.md (ids in
  CHECK_20_stormbound_ids.txt). After his approval: fix what he finds for all cards with the same problem, add a few
  approved records to BRIEF.md as examples, write Stormbound's results in RESULTS.md.
- Questions over all games work (`ask.py all ...`, mechanics.py, QUERIES.md). The next game follows PROCESS.md, first its
  section "Writing data the same way in every game".
- Next idea, not started: a deck as a network of cards (NETWORK_DRAFT.md).
