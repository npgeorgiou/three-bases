# Start here: chats that import a game or change the card database

Read this file whole, then only what your task needs (map below). Commands run from `library/cards_db/`.
Clone with the library: CLAUDE.md "Start of a chat", then `git sparse-checkout disable` (the library is ~120 MB).

## What the database is
Every card of 8 games (Runeterra, Stormbound, Monster Train, Duelyst, Faeria, Inscryption, Into the Breach, Slay the Spire)
described as rows: when it acts (event), if what (conditions), what it does (effects). Every value is from `vocab.tsv`; equal
mechanics of different games share one concept (`library/concept_tree.txt`). From the rows, network.py draws **lines** between
two cards of one game ("A makes B cheaper", "A sets off B"). Kaptain designs factions for Three Bases from the lines and the
concepts. Wrong lines give wrong design answers, so lines must be right.

## How to talk to Kaptain
Short plain sentences, his words, a card example for every point, one question at a time (last, marked). Answer his questions
first and wait. Never invent rules or mechanics; mark suggestions as yours.

## The six rules most often broken (each cost Kaptain hours)
1. **Fix the cause, never the example.** Every error Kaptain finds is one sample of a family: name the wrong thinking in one
   sentence, find every place it lives (all games, all rules, the readings, the questions), fix it once (PROCESS.md "Fixing
   errors").
2. **Every fix gets test cases** (31 Oct 2026): one `cases/network.tsv` row per point Kaptain made and per similar error found,
   `line` or `none`, only for lines checked against both cards. A fix without cases comes back broken.
3. **Dump all lines before and after** (`dump_lines.py`) and read EVERY gone and new reason group in every game.
4. **One rebuild per round**: `check_all.py <game>` loads all games once (about 25 minutes); after a change to network.py only,
   `check_all.py --no-load` (about 3 minutes). Never `run.py` once per game, never a rebuild between single edits.
5. **Read cards like a player**: what does it need, who gives it that, what does it make, what does that card do.
6. **A check is done only when all its output was read.** Never sample less, skip a game or hand over because the output is
   long: cut it into pieces (PROCESS.md "Token economy"). Say plainly what was not checked; a passing count is not a check.

The rules for lines (L1-L24) are in LINE_RULES.md: read it before judging a line or changing network.py.

## Map: where things are
| What | File |
|---|---|
| Import steps, data rules, token economy, fixing errors | PROCESS.md |
| Rules for lines | LINE_RULES.md |
| How network.py makes lines; the line check after an import; the planned line table | LINKS_PLAN.md |
| What card readers follow | READER_PROMPT.md (the job), BRIEF.md (shapes, reading rules, game words), SYNTAX.md (rows as printed) |
| Line check agents (imports only) | checks/LINE_READER_JOB.md, checks/LINE_VERIFIER_JOB.md, causes.py |
| Values and concepts | vocab.tsv, library/concept_tree.txt |
| Build: rows -> cards.sqlite | run.py (one game), check_all.py (all games), load.py, flat.py, refs.py |
| Lines between cards | network.py; why one line exists: pair.py; all lines: links.py -> links.sqlite (not in git) |
| Decks | decks.tsv, cases/decks.tsv; pages network.html (network_page.py) |
| Questions | ask.py, mechanics.py, connections.py, deck_analysis.py; START_QUESTIONS.md, QUESTION_BANK.md |
| Each game's rules, terms, sources, real-world cases | library/games/<game>.md |
| Files and tables in detail | README.md |

## Every check and test, and when it runs
Scripts cost no tokens; reading their output and card texts does, and readers (agents) cost most.

**A. Rebuild** (`run.py <game>`, or `check_all.py <game>` for all games) after any change to records, vocab or shared code.
It stops at the first failure:
1. normalize.py: one form for equal meanings, on every record.
2. check.py: every record uses allowed shapes and values (0 problems).
3. load.py: cards.sqlite for all 8 games (with flat.py, refs.py: the tables questions use).
4. cases/run.py: every case must pass. mechanics.tsv (a mechanic's cards, found by regex in the texts, found by the query, 95%),
   combos.tsv (a guide's combo: the first card sets off the second), regions.tsv (a faction shows its known mechanic),
   decks.tsv (a guide deck's explanation says the guide's phrases), network.tsv (a deck line that must exist, or must not).
5. pattern_check.py: words in a text that its record must show (open flags listed).
6. audit_text.py: words in a text that its rows miss ("or the enemy Nexus"); each fixed or explained.
7. audit_links.py: links that cannot exist (a need nothing makes, a keyword without concept); each fixed or explained.
8. status.py (reading progress), examples.py (QUERIES.md), review_check.py (families in deck_read_<game>.md, during an import).
Read: any FAILED line and the audit lists. `check_all.py --no-load` runs only steps 4 and 7.

**B. Importing a game:** PROCESS.md steps 0-5, then the line check (LINKS_PLAN.md step 3). The line check is two scripts,
both required, all output read: `links_audit.py <game>` (every reason of the whole game: is its rule right?) and
`deck_audit.py <game>` (the lines inside every deck). `audit_links.py` (A7) is a different check and does not replace them.

**C. After any change to lines, and whenever Kaptain says check:** PROCESS.md "Fixing errors" (dump before and after, read
every gone and new reason group); `deck_audit.py <game>` for each game whose lines changed, read whole, with every level-up line
of every deck against both cards; `realworld.py` for all games (no case that held may break). After a change to the deck pages:
`network_page.py`, load network.html in the browser (Playwright, every deck, no script errors, one hover and click on a line),
push, give network.html to Kaptain.

**The game itself** has its own: tools/build.py, tools/simtest.js, tools/smoke.js (CLAUDE.md).

## State (3 Nov 2026)
- All 8 games imported. Kaptain approved Runeterra and Into the Breach; Slay the Spire done; Inscryption reviewed; Stormbound,
  Monster Train, Faeria, Duelyst wait for his check of their deck networks.
- Cases: all pass. Must-not cases whose old reason no line says any more were made strict (no line at all); n56, n352,
  ntb15-16 and nst36 keep theirs because the pair still has a line for another reason. The next case id is n396.
- Real-world cases: 237 of 261 hold (Zealous Crusader -> Khalim's Prayer is gone by a rule of Kaptain's of 3 Nov 2026, before L24; the other 23 are faction-label checks).
- Lines (pairs in links.sqlite, 3 Nov 2026): Runeterra 201,006; Duelyst 12,427; Faeria 10,014; Slay the Spire 8,797; Into the
  Breach 6,137; Monster Train 3,092; Stormbound 2,686; Inscryption 1,080.
- Known open (also LINKS_PLAN.md "Open"): a card placed by its text near the leader (Conscript) draws
  no line to a card acting near the leader (Fealty); Adaptive Mutation's stat swap has no line; Monster Train has no full decks
  as text (ask Kaptain). Monster Train's Olde Magic is built by the player at an event: its record
  (read/monster_train/event_cards.jsonl) lists the wiki's choices, with no numbers. Stormbound's Fort of Ebonrock has no ability.

## Choosing the next game (Kaptain, 3 Nov 2026)
Judge only data quality, never how much the game looks like Three Bases (ideas come from any game). For each game: cards
complete, with codes, tokens and every form; keyword definitions from the game's own source (not "Claude's summary" or
"inference"); rules from the game's own pages; real decks from players; combos named by players. Check the library entries
and the repo's sources first, then the online sources, and say which parts were only searched, not opened.
Data quality means what helps the rows and the lines: fields that already say what a card does (its triggers, keywords with
values, the cards it creates or names), card wording written to a fixed template, every keyword's exact rule from the
game's own rulebook, and players' combos and decks that test the lines. Completeness alone is not enough.

## Open work, in Kaptain's order
1. A newly imported game gets the line check of LINKS_PLAN.md step 3; its fixes are made in the main chat, never by an agent.

## When you finish
Commit and push every finished step. Update "State" and "Open work" above (short, no history: git log has it).
