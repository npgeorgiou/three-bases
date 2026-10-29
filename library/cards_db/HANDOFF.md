# Handoff: card database (29 Oct 2026)

## Start of a chat
1. Clone with the library (CLAUDE.md "Start of a chat", then `git sparse-checkout disable`). Read only this file.
   A game's card data and keyword sources are already in the repo: PROCESS.md step 0.3 says where. Never fetch them again.
2. cards.sqlite is committed and current: questions need no build (`ask.py runeterra ...`). Run `run.py runeterra` only after
   changing records, values or scripts; it must then pass every step.
3. Then, as the task needs: PROCESS.md (importing a game; its "How to work" first), README.md (files, tables, questions),
   RESULTS.md (results per game).

## State
- Runeterra is done and approved (RESULTS.md).
- Stormbound: every build step passes; waiting for Kaptain's check of CHECK_20_stormbound.md (ids in
  CHECK_20_stormbound_ids.txt). After his approval: fix what he finds for all cards with the same problem, add a few
  approved records to BRIEF.md as examples, write Stormbound's results in RESULTS.md.
- Monster Train: every build step passes; waiting for Kaptain's check of CHECK_20_monster_train.md (ids in
  CHECK_20_monster_train_ids.txt) and of the keyword -> concept list. Results in RESULTS.md.
- Questions over all games work (`ask.py all ...`, mechanics.py, QUERIES.md). The next game follows PROCESS.md.
- A deck, faction or game as a network of cards is built (network.py, `ask.py <game> network`; NETWORK_DRAFT.md has the
  plan and Claude's own choices). Waiting for Kaptain's judgement; only the Lucian/Senna guide deck is stored (QUERIES.md),
  the Nilah/Janna, Marauder/Fiora and Telsi/Volibear lists are not in the repo.
