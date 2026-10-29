# Handoff: card database (29 Oct 2026, v38)

## Start of a chat
1. Clone with the library (CLAUDE.md "Start of a chat", then `git sparse-checkout disable`). Read only this file first.
2. cards.sqlite is committed and current: questions need no build (`ask.py runeterra ...`). After changing records, values
   or scripts, run `run.py <game>` for every game; each must pass every step.
3. Then, as the task needs: PROCESS.md (importing a game), README.md (files, tables, questions), RESULTS.md (results per
   game), NEXT_CHAT.md (open deck-network work on the three games).

## Importing a new game: start here
**Do and don't (Kaptain, 29 Oct 2026, after the Faeria import took over an hour of loops). Keep this list in view:**
- Do research the game's rules first, before readers: how units fight, move and reach things, and, on a board, where cards
  may enter and how the board grows (Faeria: land only next to your god, lands or creatures; summon only on your own empty
  land of the right colour). Write them as game rules (step 0.10). Missing them made most of Faeria's network errors.
- Do read ALL guide decks before fixing anything: write every wrong or missing line in one list, group them into families,
  fix each family once by a rule for all games, rebuild once. Never fix after each deck, never rebuild after each fix.
- Do rebuild only your own game (`run.py <your game>`, it loads every game). After a shared-code change, check the others
  read-only with `cases/run.py <game>`; if one fails, tell Kaptain. Never run `run.py` for another chat's game: it
  normalizes and rewrites that chat's records and files.
- Don't touch other games' records, fixes or flags; don't do work nobody asked for (new explainer roles, wordings).
- Don't trust a passing count or a few lines: look at what a line SAYS in network.html, both directions, as a player.
- If a step here or in PROCESS seems to force a loop, stop and ask Kaptain instead of working around it.

1. Read PROCESS.md in this order: "Why the first three games went wrong", "How to work", "Rules that are never broken",
   "Writing data the same way in every game", then "Steps" and follow them in order, once. Read "Links the deck networks
   showed missing" and "Think like a player" before step 2.9.
2. Before any reader runs: the game's data is already in the repo (step 0.3); its rules and terms are in
   `library/tools/games/<game>.md`. Write `read/<game>/game_rules.jsonl` from that file (step 0.10), map the game's words
   in BRIEF.md "Game words: <game>" (step 0.6), and find full decks for the tests (step 0.1).
3. Readers get READER_PROMPT.md unchanged; BRIEF.md reading rules 1-32 are what they must follow (26-32 are the mistakes
   found in the first three games). Fix what they get wrong by rule scripts (`fixes/<game>/vNN.py`), never by re-reading.
4. After the readings: run.py, then audit_text.py, audit_links.py and the deck networks (steps 2.7-2.9). Every error found
   is fixed for all cards of all games, written as a lesson in PROCESS.md, and turned into a case or an audit rule, so the
   next game is checked for it automatically.
5. Done only by PROCESS "Done when", never by passing counts.

## State
- Runeterra is done and approved (RESULTS.md). Stormbound and Monster Train: every build step passes; waiting for
  Kaptain's check of CHECK_20_<game>.md (ids in CHECK_20_<game>_ids.txt); Monster Train also its keyword -> concept list.
- Questions over all games work (`ask.py all ...`, mechanics.py, QUERIES.md).
- Deck networks: network.py (`ask.py <game> network`), the page `network_page.py` -> network.html (decks in decks.tsv and
  cases/decks.tsv). 36 Runeterra and 28 Stormbound full decks; Monster Train has only guides' core cards (no full lists
  found as text). Kaptain's judgement of the v34 networks is open (NEXT_CHAT.md).
- Cases: Runeterra 304, Stormbound 141, Monster Train 150, Inscryption 59, Duelyst 39, Faeria 87, all passing; audit_links.py findings are explained in RESULTS.md.
- Faeria (v35-v38): imported; every step of PROCESS passes, all 12 decks read card by card (RESULTS.md). Its board words are
  now the shared form for every positional game (BRIEF "The board", PROCESS "Importing Faeria: the board"). Waiting for
  Kaptain's check of CHECK_20_faeria.md (ids in CHECK_20_faeria_ids.txt) and of CONCEPTS_faeria.md.
- Inscryption (v36): imported; every step of PROCESS passes, all 19 decks read card by card (RESULTS.md). Waiting for
  Kaptain's check of CHECK_20_inscryption.md (ids in CHECK_20_inscryption_ids.txt) and of the sigil -> concept list
  CONCEPTS_inscryption.md, and his answer on Energy ramp lines (Battery Bearer -> Energy-cost cards).
