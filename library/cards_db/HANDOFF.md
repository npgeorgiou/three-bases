# Handoff: card database (29 Oct 2026)

## Start of a chat
0. **Deck-network work in progress: read NEXT_CHAT.md first** (state, open work, how to think).
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
- Deck networks: network.py (`ask.py <game> network`), the page `network_page.py` -> network.html (decks from the web in
  decks.tsv and cases/decks.tsv, a game picker). Kaptain's check of 9 decks found links missing or wrong; fixed for every
  game (CHANGES v30) and turned into cases/network.tsv and audit_links.py. **Importing a game: read PROCESS.md "Why the first
  three games went wrong" and "Links the deck networks showed missing" first, and write the game's rules (step 0.10).**
  Open for Kaptain: his judgement of the v34 networks (NEXT_CHAT.md).
