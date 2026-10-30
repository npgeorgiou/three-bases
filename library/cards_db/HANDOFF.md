# Handoff: card database (30 Oct 2026, v41)

> **CHECKING AFTER A CHANGE: LOAD THE DATABASE ONCE. NEVER RUN `run.py <game>` ONCE PER GAME.**
> Every `run.py` reloads ALL eight games (load.py loads every game, every time). Eight runs = eight reloads = over an hour
> (30 Oct 2026, it happened). Use `python3 check_all.py <your game>` (one reload, then every other game's cases and link
> audit) or, after a change to network.py only, `python3 check_all.py --no-load` (no reload at all: the networks read
> cards.sqlite). Then `dump_lines.py` before/after (PROCESS "Fixing a review").

## Start of a chat
1. Clone with the library (CLAUDE.md "Start of a chat", then `git sparse-checkout disable`). Read only this file first.
2. cards.sqlite is committed and current: questions need no build (`ask.py runeterra ...`). After changing records, values
   or scripts, run `check_all.py <game>` (the box above: one reload for all games); every game must pass.
3. Then, as the task needs: PROCESS.md (importing a game), README.md (files, tables, questions), RESULTS.md (results per
   game), NEXT_CHAT.md (open deck-network work on the three games).

## Importing a new game: start here
**Do and don't (Kaptain, 29 Oct 2026, after the Faeria import took over an hour of loops). Keep this list in view:**
- Do set the game's expensive cost in network.py EXPENSIVE (PROCESS "Rules for links"), and read those rules before any network.
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
- Do fix every review point by its cause (PROCESS.md "Fixing a review"): dump every network line of every game before and
  after (`dump_lines.py`), read every gone and new reason, write root cause / same error elsewhere / fix per family
  (`review_check.py` fails without them). A point fixed for the named cards only comes back.
- If a step here or in PROCESS seems to force a loop, stop and ask Kaptain instead of working around it.
- Do read networks only with `deck_lines.py <game> [deck]`: the same terse text the page copies on a right click (Kaptain
  pastes it). Never write your own export or dump scripts (the Duelyst import lost much time on them).
- Do pull right before you rebuild and again before you commit. Generated files (cards.sqlite, cases/REPORT.md, QUERIES.md,
  STATUS.md, network.html) conflict on every merge: take either side and rebuild your game; keep both sides of code.
- Do read the decks after your last pull, not before it: merged code changes lines (the Duelyst second read found 6 new errors).
- Do write each wrong line as an exact network case (deck, from, to, line/none) when you find it; don't tune text regexes
  for concept cases. After a shared change, compare `dump_lines.py --diff` before and after for every game and read the
  changed lines: passing cases do not show hundreds of lines going away.
- Link kinds (Kaptain, 30 Oct 2026): "triggers" for reactions, "enables" for things needed or counted, help kinds, one link per
  pair (PROCESS "Link kinds and what this chat learned").
- Lines are combos between card abilities (Kaptain, 30 Oct 2026): what every unit does by the rules (attacks, is struck
  back, harvests, gives Bones when it dies) makes no line, except for a level-up count or a need that names the leader; a
  passive that helps cards points from it to them, and those cards do not "enable" it (PROCESS "Kaptain's check of the
  Duelyst networks").

**The order that saves the most time (Inscryption, 29 Oct 2026: done the long way it took three fix rounds, v36, v38, v39,
and about ten rebuilds). Each check below is cheap and found errors that later cost a whole round:**
1. Before readers: every card of every guide deck is a card of the game (`audit_links.py` check 5 on decks.tsv). If not,
   the source is not whole: build the supplement first. Inscryption's merged and missing cards forced a second reading.
2. Before readers: each deck is FULL (PROCESS 2.9): its copies add up to the game's deck size, with the counts and the size
   written in its source. A starter deck or a guide's core cards is not a full deck; mark it so.
3. Before readers: read 20 cards' source boxes field by field (special behaviours, tabs, second boxes on a page) and their
   keyword definitions; a keyword entry that only points elsewhere has no definition yet (audit_links check 6).
4. After readers, before any fix: one pass that lists everything wrong: all decks (deck_read_<game>.md), the 20-card check
   (yourself when Kaptain does not know the game), audit_text, audit_links. Then one fix script, one rebuild, one case per
   family. Fixing as you find costs a rebuild per fix and finds the same family again later.
5. Look at the networks in network.html (network_page.py), not through ad-hoc scripts: it shows both directions at once.

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
- Cases: Runeterra 310, Stormbound 145, Monster Train 154, Inscryption 77, Duelyst 94, Faeria 123, Into the Breach 19, all passing (Stormbound 141, see below); audit_links.py findings are explained in RESULTS.md.
- Faeria (v35-v38): imported; every step of PROCESS passes, all 12 decks read card by card (RESULTS.md). Its board words are
  now the shared form for every positional game (BRIEF "The board", PROCESS "Importing Faeria: the board"). Waiting for
  Kaptain's check of CHECK_20_faeria.md (ids in CHECK_20_faeria_ids.txt) and of CONCEPTS_faeria.md.
- Duelyst (v37-v40): imported; every step of PROCESS passes, all 10 decks read card by card twice (RESULTS.md,
  deck_read_duelyst.md). Generals are leader cards; Backstab, Zeal and Infiltrate are needs for moves. Waiting for Kaptain's
  check of CHECK_20_duelyst.md (ids in CHECK_20_duelyst_ids.txt) and of CONCEPTS_duelyst.md.
- Slay the Spire (v49, sts1): imported to step 2.9; run.py passes; 22 guide decks (no full end-of-run deck found as text);
  first deck read listed in NEXT_CHAT.md "Slay the Spire", not fixed yet. Stormbound has 4 failing combo cases (csb09-csb13,
  poison) that fail without the v49 rows too: not caused by sts1; tell Kaptain.
- Inscryption (v36-v45): imported and reviewed by Kaptain (30 Oct 2026). 17 decks kept (decks.tsv), 20 weak ones listed in
  decks_dropped_inscryption.tsv; families F1-F18 in deck_read_inscryption.md; why its networks are thin: RESULTS.md.
  Energy ramp is marked base_resource_gain, not linked to costs (Kaptain).
- Into the Breach (v48-v51, done 30 Oct 2026): every step of PROCESS passes (RESULTS.md). 20 squads in decks.tsv, rules in
  library/tools/games/into_the_breach.md, BRIEF "Game words: Into the Breach". Families F1-F19 in deck_read_into_the_breach.md
  (F7 kept by Kaptain; F8-F12 approved by him; the check of 20 cards done by Claude at his word). Open, Kaptain's call: does a
  single-target attack next to the unit (Combat Mech) care where units stand like a line or area weapon? Left as is.
  Stormbound shows 141 of 145 cases (csb09-csb13, poisoned-unit lines) since the Slay the Spire chat's v49 shared change.
