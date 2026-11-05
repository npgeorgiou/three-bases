# Start here: every chat that changes the card database (importing a game, fixing lines). Part 1: the database

The one start file for changing the database. Part 1: what it is, the rules, every check, the state. Part 2: how an import
runs (two chats, agents, nothing lost) and chat 1, the import, step by step. Part 3: chat 2, every check after the import,
and the fixes. Read all three parts whole, then only what
your task needs (map below). Using the database (questions, designs) starts at factions/START_DESIGN.md instead. Commands run from `library/cards_db/`.
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
   sentence, find every place it lives (all games, all rules, the readings, the questions), fix it once ("Fixing
   errors", Part 2).
2. **Every fix gets test cases** (31 Oct 2026): one `cases/network.tsv` row per point Kaptain made and per similar error found,
   `line` or `none`, only for lines checked against both cards. A fix without cases comes back broken.
3. **Dump all lines before and after** (`dump_lines.py`) and read EVERY gone and new reason group in every game.
4. **One rebuild per round**: `check_all.py <game>` loads all games once (about 7 minutes); after a change to network.py only,
   `check_all.py --no-load` (about 2 minutes). Never `run.py` once per game, never a rebuild between single edits.
   Start it only with the Bash tool's background mode (run_in_background), never with `&` or nohup (the shell stops those a
   few minutes after a reply ends); never stop a running build; wait for its notice and work on findings meanwhile, never
   idle (Marvel Snap, 5 Nov 2026: a stopped build left cards.sqlite.new and its journal, and the next build failed).
5. **Read cards like a player**: what does it need, who gives it that, what does it make, what does that card do.
6. **A check is done only when all its output was read.** Never sample less, skip a game or hand over because the output is
   long: cut it into pieces and give them to agents (Part 2 "How an import runs"). Say plainly what was not checked; a passing count is not a check.

The rules for lines (L1-L24) are in LINE_RULES.md: read it before judging a line or changing network.py.

## Map: where things are
| What | File |
|---|---|
| Import steps, data rules, token economy, fixing errors | Part 2 below |
| The line check after an import | Part 3 below |
| Rules for lines | LINE_RULES.md |
| How network.py makes lines; the planned line table | LINKS_PLAN.md |
| What card readers follow | READER_PROMPT.md (the job), BRIEF.md (shapes, reading rules, game words), SYNTAX.md (rows as printed) |
| Chat 2 agents and their files | checks/LINE_READER_JOB.md, LINE_VERIFIER_JOB.md, LINE_FIXER_JOB.md, causes.py; work files and PROGRESS.md in checks/<game>/ |
| Values and concepts | vocab.tsv, library/concept_tree.txt |
| Build: rows -> cards.sqlite | run.py (one game), check_all.py (all games), load.py, flat.py, refs.py |
| Lines between cards | network.py; why one line exists: pair.py; all lines: links.py -> links.sqlite (not in git) |
| Decks | decks.tsv, cases/decks.tsv; pages network.html (network_page.py) |
| Questions | ask.py, mechanics.py, connections.py, deck_analysis.py; factions/START_DESIGN-4-asking.md, QUESTION_BANK.md |
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

**B. Importing a game:** chat 1 = Part 2 steps 0-2.4; chat 2 = Part 3 (steps 2.5-5 and the line check). The line check is two scripts,
both required, all output read: `links_audit.py <game>` (every reason of the whole game: is its rule right?) and
`deck_audit.py <game>` (the lines inside every deck). `audit_links.py` (A7) is a different check and does not replace them.

**C. After any change to lines, and whenever Kaptain says check:** "Fixing errors" (Part 2) (dump before and after, read
every gone and new reason group); `deck_audit.py <game>` for each game whose lines changed, read whole, with every level-up line
of every deck against both cards; `realworld.py` for all games (no case that held may break). After a change to the deck pages:
`network_page.py`, load network.html in the browser (Playwright, every deck, no script errors, one hover and click on a line),
push, give network.html to Kaptain.

**The game itself** has its own: tools/build.py, tools/simtest.js, tools/smoke.js (CLAUDE.md).

## State (3 Nov 2026)
- All 8 games imported. Kaptain approved Runeterra and Into the Breach; Slay the Spire done; Inscryption reviewed; Stormbound,
  Monster Train, Faeria, Duelyst wait for his check of their deck networks.
- Cases: all pass. Must-not cases whose old reason no line says any more were made strict (no line at all); n56, n352,
  n378, ntb15-16 and nst36 keep theirs because the pair still has a line for another reason. The next case id is n413.
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
1. A newly imported game gets chat 2 (Part 3): every check, the fixes made by fixer agents.
2. **Marvel Snap import, in progress (handover, 5 Nov 2026).** Done: Part 2 step 0 (supplement_marvel_snap.py: 749 cards
   from snap-dossier a23b31f, 91 mode variants left out by exclude.tsv for Kaptain's check, 9 texts filled from snap.fan;
   16 keywords from the game's sources; BRIEF "Game words: Marvel Snap"; sourced rules and deck rule in
   library/games/marvel_snap.md; read/marvel_snap/game_rules.jsonl; 18 vocab rows of 5 Nov 2026; patterns T99-T110;
   DECK_RULES marvel_snap); 27 full guide decks in decks.tsv; step 1 (all batches, keywords, second_001; 103 unsure cards
   re-read, 39 still unsure with needs only one card has); decisions: Overdrive left out as a mode (Kaptain); When Discarded is a trigger label like
   End of Turn (Kaptain); "not revealed until the game ends" is cant played, as Dark Dimension; a set of cards ("2 Arrows")
   is a card list (fixes/marvel_snap/v65.py); Muramasa Shard added.
   Chat 1 (the rows) is done: second reading, word check, names, text audit (0 left) and link audit (explained below) fixed,
   cases n403-n412, ms04. Link audit explained: game_end, snapped, mana_spent and keyword_used Moveable are made by the game
   and the player (every game ends; Snap and spending Energy are the player's choices); On Reveal, Ongoing, Quickdraw and When
   Discarded are trigger labels like End of Turn (their events are in the rows). Check 10 leads read: play_restriction,
   generate_cards; not read: symmetric_effect, lane_rule, turn_number, cost_condition, cross_lane, tribal, control_reward,
   stat_condition, lane_closure.
   Chat 2 (the lines), in progress. Done: cases/combos.tsv cms01-24 (the Combos of library/games/marvel_snap.md; 16 fail, the
   misses to trace) and cases/decks.tsv dms01-12 (pockettactics' own explanations; snapcomplete gave no explanations it could
   reach); the line check's readers and verifiers: findings in checks/marvel_snap/ (lr_* readers, vv_* verdicts,
   causes_sheet.md: 21 verified causes, biggest first); v68: discarded and destroyed cards lie apart (zones discarded,
   discarded_or_dead; refs.py: a discarded card of any kind was discarded), cases n413-n416.
   Next: Part 3 from its step 4 (checks/marvel_snap/PROGRESS.md says where): the failing combos and the Wong Spectrum deck
     case become MISSED causes; then fixers work through causes_sheet.md from the top (one `none` and one `line` case each; after about 5 fixes `check_all.py --no-load`).
     Kaptain's answer needed first: On Reveal is on 306 of 660 cards; are repeats of On Reveal (Odin, Wong, Absorbing Man)
     a deck choice or generic (L21)? Odin and Wong have lines now; the verdict said Absorbing Man's are not.
   - The 16 failing combos and the deck cases that fail (cases/REPORT.md); realworld.py marvel_snap (10 misses at the start).
     Deck explanations also say "waits for your units get Ongoing ... nothing else in the deck does it" where Ongoing cards
     are in the deck (Mystique, Onslaught): the cause of verdict 4 (Mystique) and of that wording.
   - The handover's doubtful lines: Power Shot -> Vampire Deacon Frost, Grapple Arrow -> Galactus (verified wrong),
     Mind Shot -> Dragon of the Moon, Hawkeye Kate Bishop -> Basic Arrow.
   - Part 3 step 9, step 4 (`design_questions.py`), step 5, then Kaptain checks the deck page.
   Not written: supplement/marvel_snap_links.jsonl (cards a card creates are linked by the names in its rows).

## When you finish
Commit and push every finished step. Update "State" and "Open work" above (short, no history: git log has it).

# Part 2: importing a game's cards (the framework for every game)

For the chat that imports a game. Commands run from `library/cards_db/`. Runeterra, Stormbound
and Monster Train went through every step; their files are the templates. Files and tables: README.md.

The database is one place for all games: questions run across games (`ask.py all ...`), so everything stored is generic. A
game's own words live only in its card texts, keyword entries and types; what cards DO is said with vocab.tsv values and
concepts any game can share.

## What the rows are for: lines between cards (Kaptain, 2 Nov 2026; read before reading a single card)
From the rows network.py draws the LINES between cards ("A kills it for its death effect", "A makes it cheaper"), and Kaptain
designs factions from them. So the rows hold every part of a card that another card can feed or use: what sets it off, what it
counts, needs, makes and aims at, and the game's own rules (how units fight, move, pay, reach the enemy player). A part left
out draws no line; a part read wrong draws wrong lines in every deck.
So **understand the game fully before reading a card**: how it is played, which combos its players use, what its keywords
really do, which cards are deck choices and which do what every card does. Take it from the game's own sources and its
players' guides (step 0, `library/games/<game>.md`), never from memory. A reader who does not know the game reads the words and
misses the play.

## How an import runs (Kaptain, 5 Nov 2026; read before doing anything)
**Two chats, never more.** Chat 1 is the whole import: Part 2 steps 0-2.4 (research, data, the game's words and rules, the
readers, one fix round for the rows, one rebuild). Chat 2 is every check after it and every fix: Part 3. A chat stopped by
the token limit is not a new chat: the next one continues from the progress file where it stopped.

**The main chat leads; agents do the reading and the fixing.** Every tool call of the main chat sends the whole chat again,
so what the main chat reads is the cost; what an agent reads stays inside the agent, and only its short reply comes back.
- The main chat runs scripts, starts agents, and reads only: their one-line replies, the progress file, counts, and diffs
  short enough to read (longer ones go to an agent). It never reads card texts, check output, deck explanations (ask.py
  analyze) or network.py, and never traces a line by hand (Marvel Snap, 5 Nov 2026: a chat spent that way fixed one cause
  of 21).
- Agents are Sonnet, started with the Agent tool in the background, each from its job file: card readers READER_PROMPT.md,
  line readers checks/LINE_READER_JOB.md, verifiers checks/LINE_VERIFIER_JOB.md, fixers checks/LINE_FIXER_JOB.md. Readers
  and verifiers only read; fixers change only what their one cause needs. Their findings are often wrong ("The Dreadway ->
  Decimate is a combo that works"), so a finding is verified before a fixer gets it, and every fix is checked by a rebuild
  and its diff.
- One game at a time. At most three agents run at once; fixers run one at a time (they change shared files).

**Agents must not run wild** (agents that looked things up, re-read, retried failing checks or rebuilt used up Kaptain's
tokens). Every job file says, and the main chat never asks otherwise:
- a fixed number of tool calls (line reader and verifier 4; fixer at most 25; card reader one part of about 25 cards at a
  time), and one file that holds everything the agent needs, so it looks nothing up;
- never a rebuild (run.py, check_all.py, links.py), never git, never a file outside its job;
- two tries at most: an agent whose change does not do what it wants writes "STUCK:" and what it saw, and stops;
- its result file is written before it replies.
An agent that writes nothing for 30 minutes is stopped (TaskStop) and started again on the same files.

**Nothing is lost at a token reset.**
- Every work file lives in the repo under `checks/<game>/` (pieces, findings, verdicts, causes_sheet.md, fixer reports, the
  line tables before and after), never in /tmp: /tmp is gone in the next chat.
- `checks/<game>/PROGRESS.md` holds one line per step of the chat: done, running (which agent on which file) or next. The
  main chat writes it when a step starts and when it ends, and commits and pushes it with that step's files at once. Card
  readers commit each finished batch (step 1).
- A chat after a reset reads PROGRESS.md, `git log -5` and `status.py <game>`, and continues at the first step not done. An
  agent marked running whose result file is missing or partial is started again on the same file; parts already written
  are kept.
- Every finished step is pushed; a chat ends with Part 1 "State" and "Open work" updated.

**Rules of work.**
1. Look before you make: the game's data (step 0.3), an existing value (vocab.tsv, by meaning), an existing rule (normalize.py
   N-rules, BRIEF.md), an earlier decision (vocab.tsv added column, `patterns/verdicts.tsv`, `git log -S <word>`).
2. A decision is written once and kept. If it was decided (by Kaptain or an earlier chat), do not turn it back; if it truly
   looks wrong, ask Kaptain with the card that shows it (Runeterra's Stun went disable -> attack_lock -> disable in two chats).
3. Batch: collect all problems of one kind before fixing any, fix them with one rule or script, one rebuild per round
   (Faeria, 29 Oct 2026: a rebuild of six games after each deck fix cost over an hour).
4. Fix by rule, for every card: a regex over the texts or a script over the records (`fixes/<game>/vNN.py`, safe to run twice).
   A re-read is the last resort, for cards no rule can fix.
5. Shared code (connections.py, refs.py, flat.py, deck_analysis.py, normalize.py, load.py, network.py) serves every game: a
   change there gets a case, and every game's cases must pass before it is pushed (`check_all.py <your game>`).
6. Scripts are free; reading costs. Every check script prints the size of its output (stderr); long output is cut with
   `audit_pieces.py split <file>` (pieces of about 15,000 tokens, each card's rows once per piece) and goes to agents.
   Judge each rule once with a few varied examples; judge lines by the rows, not by card texts; at most 100 cards per list.
7. Card readers cost about 110-125k tokens each, whatever the batch size. A handful of cards (tokens, fixes) a fixer or the
   import chat writes directly.

## Rules that are never broken
1. **A card is everything it makes** (summons, creates, shuffles in, transforms into, levels into).
2. The card text is the truth. A record says only what the text states. No rule from memory: a definition that neither the
   library nor the game's data has is asked from Kaptain (Runeterra: Deep, Plant).
3. The records in `read/<game>/` are the source; everything else is rebuilt from them by `run.py <game>`.
4. Every value is a row of `vocab.tsv`. A new value is a vocab row (date and reason in its added column) and a BRIEF.md line
   if readers need it, in one commit; a new event or state also gets its `causes` entry, or "which cards care about X" misses
   it. Never change a concept without Kaptain's OK.
5. One meaning, one form: when two forms of one meaning appear, pick one, write a normalize.py rule and a BRIEF rule, rebuild
   (normalize runs on all games).
6. Judge data against the texts, never against old library tags or agreement between records and patterns.
7. Nothing lives only in a chat: decisions go into the files at once; commit and push after every finished step.
8. Nothing is "maybe": a card the values cannot describe is marked unsure (table `unsure`); a word-check flag is decided once
   (`patterns/verdicts.tsv`); a dropped case is written in `cases/DROPPED.md` with its reason.
9. Tests come from the game, never from Claude: card texts (mechanics.tsv), players' guides (decks.tsv, combos.tsv), the
   library's real-world rows (regions.tsv).
10. A game's own rules (how units fight, move, pay) are records in `read/<game>/game_rules.jsonl`, from the game's own sources
   (cited in `library/games/<game>.md`), never from memory.

## Writing data the same way in every game
1. Reuse before adding: for each game term, search vocab.tsv for a value that means the same (a base or hero with life = kind
   player; a structure = kind landmark). Add a value only when none means it, worded so any game could use it ("start of the
   owner's turn", "the tile in front"), with the game as an example in brackets.
2. Every keyword gets a vocab keyword row whose concept (column tree) says what it does by the game's own rules. Check each,
   twice, before the game is done: (a) its meaning from the game's glossary or wiki; (b) the concept's definition including its
   "not this" part (library/concept_tree.txt); (c) whose side it hits (an enemy that can't block is cant_block, my own unit that
   can't block is a drawback); (d) whether it belongs to the game at all (Terrify is Path of Champions: deleted). A shared name
   that means something else here is `<game>:<Name>` (monster_train:Frostbite is damage over time, Runeterra's Frostbite is
   attack_zero); the game's own entry wins (network.kw_tree; a lookup with fetchone() and no order picks either). Show Kaptain the full keyword -> concept list with definitions.
   A loose fit is wrong (Enlightened is a max-mana condition, not high_cost; Deep a deck-size condition, not self_mill; Plunder
   "the enemy Nexus was damaged this round", not on_life_loss). When none fits, add a precise concept to concept_tree.txt with
   its definition and "not this", give it a shape rule in flat.py RULES, run it on every game and read what it found in each.
   Line keywords join through their concept, never by name: a reaction keyword ("Strike:", "Last Words") needs a reaction
   concept (network.TRIGGER_KW), an evasion keyword evasion or excess_damage, or its lines are missed (LINKS_PLAN.md).
3. Events, states and durations worded differently get one concept: round_start and turn_start are turn_start; this_round and
   next_own_turn are temporary_effect; a state takes its keyword's concept (stunned like Stun).
4. Stats by role: Power / Attack is attack (attr power), Health is health, Stormbound's strength is both; never a stat for one
   game when one fits. "Strongest" / "weakest" are pick highest / lowest with "by" (normalize N10).
5. Statuses: giving one is give_keyword with the keyword; "a poisoned unit" is a state whose causes is given_keyword:<Keyword>;
   an act that gives a keyword names it in its causes (stun: given_keyword:Stun). A keyword in a card's own text ("Rage 4.") is
   give_keyword on itself, permanent: load.py counts it as the card's keyword.
6. Board positions are filters `{"attr": "position", ..., "of": TARGET}`: always say what the position is measured from.
7. An effect on the enemy side takes the enemy concept (moving an enemy = forced_movement; flat.py ON_ENEMY).
8. Card names are stored without trailing spaces (load.py); look names up the same way.
9. Links between cards are made only inside one game; questions over several games add up, by concept, what each game shows.

## Two games at the same time (two chats, one per game)
Each chat writes only its own game's files (read/, input/, second/, fixes/<game>/, supplement/<game>*, supplement_<game>.py).
- Id block: first write your game's line in source.py (the next free block) and push it. Refused: pull, take the next block.
- Shared files (vocab.tsv, BRIEF.md, patterns/patterns.tsv, normalize.py, flat.py, refs.py, connections.py, deck_analysis.py,
  network.py, load.py, cases/*.tsv, the docs): pull before editing, small changes, commit and push at once. Pull and search
  vocab.tsv again before adding a value. Never edit another game's records or cases; never `run.py` another chat's game (it
  rewrites that chat's records and reports). A shared fix's effect on another chat's game: show it by the dump and diff, tell
  Kaptain and that chat.
- cards.sqlite, network.html, QUERIES.md and cases/REPORT.md are rebuilt: after a pull or rebase, take the upstream copies,
  keep both sides of code, `run.py <your game>`, `cases/run.py` for every game, compare your lines with your last dump.
- Never force-push. Readers never share a scratch folder (/tmp/reader_<game>_<batch>/).

## Chat 1, the import: the steps
### 0. Before reading (in this order)
1. **Research the game**: its wiki rules and full glossary, every faction page, two or more strategy guides; note each
   mechanic with its page. Search now for players' guides with real decks (Steam guides, build guides, tier lists with card
   lists): they become the deck tests. Check each source is about this game (Monster Train 1 and 2 guides look alike; a page
   with card names the game lacks is no source).
2. **Left out** (`exclude.tsv`): only other modes or products, and only what Kaptain names. Tokens are never left out.
3. **The game's data is already in the repo; look there before fetching** (Kaptain does not know where each file is):
   - `library/sources/conv_<game>.py`: its first lines name the source, date and format. Raw files next to them:
     `monster_train_cards.psv` (282 cards, wiki Module:Cards/Data); Inscryption `inscryption_wiki_cards.jsonl` +
     `inscryption_wiki_cards_more.jsonl` (the whole set, wiki pages with revisions, 29 Oct 2026; `inscryption_missing_cards.json`
     is only the cards the library missed); `faeria_merlin_shortened.csv` + `faeria_cards_english.csv` (462 cards,
     github.com/abrakam/Faeria_Cards 12b7207, its README defines the keywords); `duelyst_cards.psv` (1116 cards, conv_duelyst.py
     over github.com/open-duelyst/duelyst 2843f24; its tutorial and tips are the rules source). Named sources: Lorcana (npm
     lorcana-oracle), Star Wars: Unlimited (swucardex-data a86faed), Elder Scrolls: Legends (TESLegendsTracker c541e82), Slay
     the Spire (wiki Module:Cards/data), Gwent (gwent.one v14.8), Magic
     (MTGJSON AtomicCards, Scryfall tokens), Shadowverse (Portal API), 40k and Age of Sigmar (BSData).
   - `library/games/<game>.md`: research, sources, keyword terms with their pages. Drop terms marked "assumed".
   - `library/cards_db/supplement/<game>*`: games already imported.
   Fetch only what none has (the built-in browser reaches pages the workspace cannot; a fandom wiki's api.php gives its card
   modules), check the copy against the source (length and checksum), and add the source to this list.
4. **Cards.** Compare the library's cards with the game's data by code, name and text (render the source's markup and diff
   every text: Faeria's library kept markup in 13 cards). Pitfalls seen: library entries that were not the game's cards; one
   wiki page holding several cards; keywords hidden in prose; full decks only as deck codes. Missing cards, glossary keywords
   and tokens go into `supplement_<game>.py` -> `supplement/<game>.jsonl` (library entities columns; ext_id = the game's card
   code; category keyword for glossary entries). A source newer than the library: the supplement holds every card and replaces
   the library's entry with the same code (source.py). A card with no text is still a card. Ids: the game's block in source.py;
   definitions Kaptain gives (`supplement/<game>_kaptain.jsonl`) from start + 900,000. Keywords-field entries that are data
   artefacts go to NOT_KEYWORDS in build_input.py with the proof.
   **Take every form of a card by its code, not its name**: a level-up form, a transformed side or a token often shares the
   base card's name (Bard 06RU001 and 06RU001T4; taking by name lost 11 Runeterra level-up forms). Write the links between new
   cards too (`supplement/<game>_links.jsonl`: transforms_into, generates).
5. **Keyword definitions** from the game's own glossary, with the source in source_type; Kaptain is asked only for a keyword
   no source defines. Glossary terms no card uses are left out.
6. **The game's words** (readers can only use values that exist). A board game maps its words to BRIEF "The board" first,
   adding a value only for what it lacks. For every term (stats, board, turn structure, zones, card kinds, statuses): an
   existing value with the same meaning, mapped in BRIEF.md "Game words: <game>", or a new vocab row. Do not stretch an old
   value (readers without a mapping used another game's words). Decide from the game's rules (marked as Claude's); ask Kaptain
   only what no source settles. Give every keyword its
   vocab row now.
7. **Numbers per card level** ("1/2/3/4/5"): `{"x": "per_level", "items": [...]}` in level order.
8. `python3 build_input.py <game> 20000`; a 10% sample for the second reading in `input/<game>/second_001.jsonl`.
9. Add the game's trigger labels and verbs to `patterns/patterns.tsv` (judged as the word check in step 2.2 says).
10. **The game's rules** (`read/<game>/game_rules.jsonl`), before readers run, because they decide most lines: how units
   fight, move and reach the enemy player; on a board, where cards may enter and how the board grows (who may build or claim
   spaces, next to what: Faeria's were missing and caused most of its errors). From the game's tutorial, rulebook, help pages or
   wiki, written with sources into `library/games/<game>.md` ("The game's rules (from sources)"; never the "Claude's summary"
   lines, which came from memory: audit_links check 8). Write what every unit (or card of a category) does that no text says,
   as one record: name "Game rule: ...", `applies_to` (categories), `source`, abilities on event with pick self (Runeterra
   `start_attack` self, `strike` self to an enemy unit or the enemy player; Stormbound strike to an enemy unit, structure or
   base; Monster Train strike to an enemy unit). Not written: what every unit does all the time and that says nothing about
   which cards belong together (Stormbound units moving forward). refs.py copies the rows to every card of the category,
   except units that never attack (Immobile); the network weighs them less; card queries leave them out.
11. **What a deck is in this game** (Into the Breach, 30 Oct 2026: a squad first written as 3 mechs, "no weapons in your
   networks"). Write into `library/games/<game>.md` what the player brings to a battle and its limits (a mech carries its
   starting weapon and its passive or one extra weapon, never two extra; slot and class rules; copies allowed). Each deck lists
   every card brought, in an order that says what rides on what; check every deck against the limits with a script.
12. **Every rule of the game becomes a record or a line rule.** For each rules line ask which cards it links. Into the
   Breach's "a ground unit pushed into a Chasm is destroyed", "Frozen ends when hit", "bumps deal 1 damage" drew no line until
   Kaptain pointed at Flood Drill. A rule linking two kinds of card (makers of holes -> pushers) is a sourced rule in network.py
   (DEADLY_GROUND) with a case.

### 1. Reading
- What reading is: a card reader is a helper agent (another Claude) that takes one batch file of cards made by step 0.8
  (`input/<game>/<batch>.jsonl`) and writes each card's rows (event, conditions, effects) into `read/<game>/<batch>.jsonl`.
- How the import chat starts one: the Agent tool, type general-purpose, model sonnet, in the background, with the text of
  READER_PROMPT.md as its task, GAME and BATCH filled in. Up to three run in parallel (Kaptain, 5 Nov 2026): the cards, the
  keywords, the second reading (`input/<game>/second_001.jsonl`), each on its own batch.
- Safety (Kaptain, 5 Nov 2026: they must not run forever, loop or destroy data, and a token limit must not lose their
  work): a reader writes its records in parts of about 25 cards as it goes, so a stopped reader loses at most one part; a
  reader started again on the same batch continues from its parts. It checks its records at most 3 rounds, then marks the
  rest unsure and stops. It writes only its own batch's files and never runs git or a rebuild. The import chat commits each
  finished batch at once (`git add read/<game>/<batch>.jsonl`), so finished work is never lost; a reader that has written no
  new part for 30 minutes is stopped (TaskStop) and started again on the same batch.
- Never merge, normalize or rebuild while a reader runs (`run.py` refuses while part files exist).
- Check every keyword record by eye: all cards with a keyword inherit it. A trigger keyword that acts by itself (Monster
  Train Eaten: the unit is eaten after combat) has that act in its record.

### 2. After the readings: one fix round for the rows
1. `python3 run.py <game>` (check A in Part 1). It prints the word check, the text audit and the link audit.
2. Collect every finding before fixing any (they are all "rows against text"):
   - proposals: tally `*.proposals.jsonl`; a need that repeats gets a value (Monster Train: "15x the number of" -> x product);
   - word check (`pattern_check.py <game>`): judge each pattern once by its hits; narrow a regex that catches other meanings
     ("damage shield" is no damage), with the reason in the file; each flag left is decided in verdicts.tsv;
   - names: every stub is a card, keyword or token from the game's data (add it to the supplement), a family (name_has), a
     type, or a misreading (`names.tsv`); never guess;
   - second reading: `compare.py <first> <second> <input>` on both readings normalized; judge each difference against the
     text; a wrong kept reading is fixed; each "same meaning, different form" becomes a normalize rule for all games;
   - text audit (`audit_text.py <game> [--list <rule>]`): read each listed card; a wrong row is a family; a right one goes to
     audit_text_explained.tsv with why; a flag the rule should not raise in any game (a lane's neighbours are lane_left and
     lane_right) widens the rule;
   - link audit (`audit_links.py <game>`): each line is a link that cannot exist; fix its cause (a missing `causes`, a keyword
     with no concept or record, a level-up form the source lacks, a misread name, a wrong concept) or explain it in "State".
     Check 10 (old library tags) are leads: read the ones whose tag names a mechanic the game's texts show.
3. Group the findings into families by cause (Part 2 "Fixing errors" 4), across all the lists above. Fix each once: a rule
   script (`fixes/<game>/vNN.py`, or a script for every game when the cause is shared), a normalize rule, or shared code.
4. One rebuild: `check_all.py <game>` (about 7 minutes). Before it `dump_lines.py`, after it `--diff`: read every gone and new
   reason group. Then all cases of every game pass, and the three audits print nothing unexplained. A new family found here
   is fixed in the same way and rebuilt once more; never a rebuild per family.
5. **Decks.** Find at least 20 decks (Kaptain, 30 Oct 2026), spread over its factions and mechanics (Duelyst: every
   General's faction; Runeterra: every region); a list Kaptain gives is used whole, and a name cut short by a page is matched
   to the real card. Full decks first (guides, deck sites, deck codes; not a guide's core cards; a roguelike's guide builds are
   core cards and the source column says so; a later edition's deck codes, Duelyst II, decode to ids the game lacks: left
   out). The source column starts with the URL. A full deck has every copy: counts add up to the game's deck size
   (Inscryption Act II: 20), the source column says counts and size, decks.tsv lists each card once. A roguelike's starter
   deck (Inscryption Act I) is kept, marked as a starter, and does not count toward 10 full decks; fewer than 10 full decks:
   say so in "State". The decks feed cases/decks.tsv and network.tsv (step 3), and the guide's combos cases/combos.tsv.
   Their lines are checked by the line check (Part 3), which reads every deck.
   **Deck cases are written by script, never by reading** (Marvel Snap, 5 Nov 2026): in step 0, when a guide's deck is saved,
   its explanation's card pairs go into `library/games/<game>.md` "Deck pairs" as `deck | A | B | the guide's words`
   (A does it for B). A script turns each into a `line` row of cases/network.tsv; the main chat does not read `ask.py
   analyze` output to write `must` phrases. A guide the workspace cannot fetch is said in "State", not worked around.
6. **The line check** (Part 3, chat 2), never skipped. Not the same as the link audit (links that cannot exist).

### 3. Case tests (`cases/`)
- mechanics.tsv: a question, the expected cards from the texts (regex, or a Keywords-field keyword) and the query; passes at
  95%. Every trigger word, keyword, common verb. Shared changes: rows with game `*`.
- decks.tsv: real guide decks are the benchmark: the guide's cards and the phrases `ask.py <game> analyze` must say. Run them
  early (in Monster Train they showed missing keyword stacks, types, spell triggers and Morsels, fixed in shared code). A guide
  deck the explainer cannot explain is a gap to fix, not a case to drop. Decks never go to readers: they test the result.
- combos.tsv: pairs a guide names, plus the library's combos rows; the source column says which guide.
- network.tsv: lines that must be there (`line`) or must not (`none`; why_not when only one reason is wrong). A `line` row with
  text in that column needs a line whose "kind: reason" holds it ("cheaper:", "kills it for its death effect"): every point
  Kaptain confirms checks the kind too.
- regions.tsv: the library's signature, splash and archetype rows per faction.
- A failing case is fixed at its cause (the query, checked against the texts first; the pattern; the value; shared code; the
  records). A case built on wrong old tags is dropped with its reason in DROPPED.md.

### 4. The last checks
1. Real-world cases: `realworld.py <game>`; read every miss and decide whether the data, the question or the case is wrong
   (cases are mostly right; a wrong case is shown to Kaptain with the texts, never changed quietly).
2. Design questions: `design_questions.py`; read the new game's answers that find no card or look thin or odd, and trace each
   to its cause, fixed for all games.
3. Kaptain checks the deck networks page (network_page.py) in plain words: does a line make sense to a player. No check files
   are written for him. Every point he raises goes into `deck_read_<game>.md` as a family ("## F<n> <name>" with "Root
   cause:", "Same error elsewhere:" (counts per game) and "Fix:" lines; `run.py` fails without them: review_check.py) and is
   fixed as "Fixing errors" says. Once he approves the game, its open items move to LINKS_PLAN.md "Open" or "State" and the
   file is deleted.

### 5. Done when
`run.py <game>` passes and every other game still passes; game_rules.jsonl written; audit_text.py and audit_links.py print
nothing unexplained; the keyword -> concept list checked twice and shown to Kaptain; 0 open word flags; no proposal need shared
by cards with different texts; stubs only names nothing defines; `ask.py all compare <its main concepts>` shows its cards next to
the other games'; every guide deck explained; 20 decks found; the line check done (`links_audit.py` and `deck_audit.py`, all
output read) and its causes fixed; realworld misses and odd design answers traced; "State" says it; everything pushed. After
Kaptain's approval, add a few approved records to BRIEF.md "Game words: <game>" as worked examples.

## Fixing errors: by cause, never by example (read before touching any point Kaptain raises)
Kaptain reviews a few decks, a sliver of the cards; each point is a sample of a rule wrong everywhere it fires. Twice Claude fixed
the named lines only, and added rules of its own without looking at what they did elsewhere; he found the same errors again. How
it happens: a point read as a task ("this line is wrong"), the code changed until the line goes, the counted tests pass, stop.
Do all points in one pass, in this order:
1. **Read like a player.** For each line of a deck, both cards' rows side by side: would a player who knows the game say "A does
   this for B"? Then the other way: what does a player know helps B (its level-up, triggers, conditions, stats, keywords), and is
   each there? "Helps" is wider than "makes what it waits for": more stats, protection, extra attacks, more cards, cheaper cards
   help the card that needs them; a line is right when the help is real, not when the words match. Game facts: a champion and
   its level-up form are one card in play (copies level together); "I / me / my / itself" is the card; damage to a player is not
   damage to a unit; keywords do what the glossary says and nothing more (Overwhelm sends leftover damage to the Nexus and adds
   none; Frostbite sets Power to 0, a frostbitten unit still blocks); skills are no spells unless the text says "spells or Skills".
2. `dump_lines.py checks/<game>/before.tsv` (every line of every deck of every game).
3. For each point find the rule that drew the line (file, function, condition; `pair.py <game> "A" "B"`) and the reading behind
   it (`flat_ref` needs and makes, `flat_do` acts and filters, of both cards). Most wrong lines were one rule firing for every
   card (game rules, a dropped filter, either side). Data or script: rows that disagree with the text are fixed by a text rule
   (fixes/<game>/vNN.py); rows right but the line wrong is a script rule, fixed for every game. Check who does it (Zed's own
   strikes, Ephemeral attackers), what the effect lands on ("it" after "revive me" is the card), what a card makes (Living Shadow,
   The Iron Conquest's skill) and abilities a card gives itself (Shark Chariot's Last Breath).
4. Name the cause in one sentence, not the card ("Start a free attack with 2 Dragonlings" read as using Dragonlings in play).
   Search by meaning, not wording: the same thinking in other words ("Nagakabouros starts a free attack with 4 Tentacles"), other
   games, other scripts (lines, deck plans, combos, questions); the rows' shape of the error (`audit_links.py` 9: a card acting on
   N cards it names but never makes); `dump_lines.py --find checks/<game>/before.tsv <reason>` counts the reason in every game: read 10
   per game. Ask which nearby rules share the cause, and what it breaks outside the decks (they show a tiny part of each game).
5. Fix each cause once, in the shared rule, keeping the exceptions for level-ups and Kaptain's cases. Wording causes ("one fact
   said twice") are fixed once in one_link(). A rule of your own beyond the point is a new cause: dump and read what it does
   everywhere first. A rule with a number (top tenth of costs, a third of the cost) is said with the cases it was checked on; a
   threshold tuned to pass one case is a new error. Never add a line every card of a kind gets from one helper (L14). A rule
   that holds for every game goes into LINE_RULES.md.
6. One rebuild. `dump_lines.py checks/<game>/after.tsv` and `--diff checks/<game>/before.tsv checks/<game>/after.tsv`: read EVERY gone and new reason
   group, in every game, as a player (a too wide rule broke Surgeforger's "give them both"). A wrong one is another family: back
   to 3. Then read every line of the game's decks once more: three more errors of one family were found that way.
7. Cases (Part 1, rule 2 of "The six rules"). A changed reason wording can make must-not cases pass whatever the network says:
   `cases/run.py` lists them; rewrite each as strict (a card-list deck with no other line, "Swap Mech, Flame Shielding", expect
   none) or keep the reason said by a positive case (ntb6 keeps ntb4).
8. Also run `audit_links.py` (10: what the old library's tags say a card does that its rows lack: leads, not truth),
   `realworld.py`, `design_questions.py`: a thin or odd answer is an error to trace.
9. Report per family: the cause, data or script, what it did in every game (counts), the fix, what is still open and which lines
   you are not sure of (with the texts). Say honestly what was fixed only for the named cards; never "done" when only counts pass.
Line labels: a reason says why both cards belong together, with both names where "it" is unclear: "Combat Mech moves units, and
Artillery Mech acts on units in a line from it", not "makes units move". Use {A} and {B} in a reason (network() fills in names);
check help_kind() when a reason's first words change. Kaptain asks about a line he cannot see: check the page data and a
screenshot first, then answer in plain words about what is drawn, not about weights.

## Asking the database
The ask.py commands are in factions/START_DESIGN-4-asking.md, example questions with real answers in QUERIES.md. "Which cards care about X"
uses flat_ref (`ask.py <games> cares`): the same thing is stored as a trigger, a condition, a count or a target filter.

# Part 3: chat 2, every check after the import, and the fixes
Steps 2.5-5 of Part 2 and the line check, in this order and nothing else. Cards are shown by their rows (SYNTAX.md), never by
their text. D = `checks/<game>/`. After each step: write PROGRESS.md, commit and push the step's files.
1. **Start.** Write PROGRESS.md with these ten steps. `links.py <game>`; `dump_lines.py --table D/tb0.tsv` and
   `dump_lines.py D/before.tsv` (every line of every deck of every game).
2. **The two checks, printed and cut.** `links_audit.py <game> > D/la.txt` (each reason of the game: is its rule right?) and
   `deck_audit.py <game> > D/da.txt` (every deck: cards with no or few partners, the special cards);
   `audit_pieces.py split` on each (pieces D/la_<n>.txt, D/da_<n>.txt).
3. **Line readers.** One agent per piece, all started at once in the background: checks/LINE_READER_JOB.md + the piece path
   + the findings path D/lr_<n>.md.
4. **Meanwhile, by script only.** Deck cases from "Deck pairs" (step 2.5: `line` rows of cases/network.tsv); the "Combos" of
   library/games/<game>.md into cases/combos.tsv; `realworld.py <game>`; `cases/run.py <game>`. Every miss (a failing combo,
   deck or real-world case) is written by script into D/lr_misses.md as "N. MISSED CAUSE: <the case's why>. Wrong examples:
   A -> B. Right examples: none." No one traces them now.
5. **Verifiers.** `causes.py D/lr_*.md --out D/vp.md`; `audit_pieces.py split D/vp.md` (cut at causes); one verifier per piece,
   all at once: checks/LINE_VERIFIER_JOB.md + the piece path + the verdict path D/vv_<n>.md.
6. **The sheet.** `causes.py D/vv_*.md --out D/causes_sheet.md`: every REAL, PARTLY and MISSED REAL cause, biggest first, with
   all a fixer needs. CONFLICT causes (a case says the opposite; Kaptain's case wins) and gone ones are skipped.
7. **Fixers, one at a time, from the top.** checks/LINE_FIXER_JOB.md + the sheet path + the cause's heading + the report path
   D/fix_<n>.md. The main chat reads only the report's first line (FIXED, STUCK or CONFLICT), notes it in PROGRESS.md,
   commits and starts the next fixer. A STUCK cause goes to "Open work" with the fixer's words.
8. **One rebuild** when all causes are done: `check_all.py <game>` if records changed, `check_all.py --no-load` if only code,
   in the Bash tool's background mode. Then `links.py`, `dump_lines.py D/after.tsv`, `--diff D/before.tsv D/after.tsv` and
   `--diff` of the tables (tb0 -> tb1). A diff of up to about 60 lines the main chat reads; a longer one is split and read by
   line readers (step 3's job, the diff as the piece). Every wrong gone or new group is a new cause: steps 5-8 once more, at
   most twice in all; what is still wrong then goes to "Open work". Must-not cases that `cases/run.py` lists as stale are
   rewritten as strict.
9. **The last checks** (Part 2 step 4): `realworld.py <game>` again; `design_questions.py` read by one agent (thin or odd
   answers of the new game, as causes in the reader format, then steps 5-8 for them).
10. **Done** (Part 2 step 5): "State" and "Open work" updated, pushed; Kaptain checks the deck page (network_page.py).
The game is not done while a verified cause is open and not in "Open work".
