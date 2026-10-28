# Process: describing a game's cards (the framework for every game)

For the chat that imports a game. Runeterra and Stormbound went through every step below; their files are the templates.
Commands run from `library/cards_db/`. Files and tables: README.md.

The database is one place for all games: questions run across games (`ask.py all ...`), so everything stored must be
generic. A game's own words live only in the card texts, its keyword entries and its types; what cards DO is said with
vocab.tsv values and concepts that any game can share.

## Rules that are never broken
1. The card text is the truth. A record says only what the text states. No rule from memory: a definition that neither
   the library nor the game's own data has is asked from Kaptain (Runeterra: Deep, Plant).
2. The records in `read/<game>/` are the source. Everything else is rebuilt from them by `run.py <game>`.
3. Every value is a row of `vocab.tsv`. A new value is a vocab row, a BRIEF.md line if readers need it, and a CHANGES.md
   line, in one commit. A new event or state also gets its `causes` entry, or "which cards care about X" misses it.
4. One meaning, one form. When two forms of one meaning appear, pick one, write a normalize.py rule and a BRIEF rule, and
   rebuild: normalize runs on all records, not only the ones you looked at.
5. Fix the cause, for every card. A wrong record is a symptom: find all cards with the same wording (regex on the texts),
   fix them all (normalize rule, or re-read with a note).
6. Judge data against the texts. Never against old library tags, never against agreement between records and patterns.
7. Nothing lives only in a chat. Decisions go into the files at once; commit and push after every change.
8. Nothing is "maybe". A card the values cannot describe is marked unsure (table `unsure`); a word-check flag is decided
   once (`patterns/verdicts.tsv`); a dropped test case is written in `cases/DROPPED.md` with its reason.
9. Generic, never game-specific. A new value names what happens in any game ("start of the owner's turn", "the tile in
   front"), not one game's word; the game's word is mapped to it in BRIEF.md "Game words: <game>". Every keyword gets a
   vocab keyword row with its concept (Stun and Freeze are both disable), so keywords of different games meet. Before a
   game is done, `ask.py all compare <concepts>` shows its cards next to the other games' for the same concepts.

## Steps
### 0. Before reading (in this order)
1. **Research the game** (library/ADDING_GAMES.md section 0.1 says how): rules, the full keyword glossary, factions or
   tribes, board, turn structure. It is the checklist for steps 0.4, 0.5 and the case tests.
2. **Left out** (`exclude.tsv`): only other modes or products, and only what Kaptain names. Cards that other cards create
   (tokens) are never left out: links to them are how combos are found.
3. **Cards.** Compare the library's cards with the game's own published card list, by card code and by name.
   - Game in the library: nothing to do for the cards it has. Only if cards or glossary keywords are missing, write
     `supplement_<game>.py` (like supplement_runeterra.py) for those. When a reliable source has newer card data than the
     library (more cards, changed texts), the supplement holds every card from it: an entry replaces the library's entry
     with the same card code (source.py). Stormbound: Stormbound Kitty's card database replaced the library's 2022 copy.
   - Game not in the library: `supplement_<game>.py` writes all its cards and glossary keywords. The old library pipeline
     (ADDING_GAMES.md converters, tags, patterns) is not used.
   - The supplement is `supplement/<game>.jsonl` in the library's entities columns (source.py lists them; ext_id = the
     game's card code; category keyword for glossary entries, with the glossary text as text).
   - Ids: one block of 1,000,000 per game, listed in source.py; write the game's line there before writing any id. Cards
     and glossary keywords take ids from the block's start, definitions Kaptain gives (`supplement/<game>_kaptain.jsonl`)
     from start + 900,000.
   - Keywords-field entries that are data artefacts go to NOT_KEYWORDS in build_input.py with the proof.
4. **Keyword definitions** come from the game's own glossary (official site, the game's data, its wiki), with the source
   in source_type. Kaptain is asked only for a keyword no source defines. A keyword with no definition stays a name.
5. **The game's words** (before any reading; readers can only use values that exist). For every term of the checklist
   (stats, board positions, turn structure, zones, card kinds, statuses), in this order:
   - same meaning as an existing value: use it, and write the mapping in BRIEF.md under "Game words: <game>" (e.g. a
     player's base or hero with health = kind player, like Runeterra's Nexus);
   - a different meaning: a new vocab.tsv row (rule 3), with an example from one of the game's cards in BRIEF.md. A new
     event or state needs its `causes`. Do not stretch an old value: "at the start of your turn" is not round_start when
     the game has turns per player.
   Kaptain has not played most games: decide the mapping from the game's rules yourself (marked as Claude's) and write it
   in BRIEF.md; ask him only what no source settles. Also give every keyword a vocab keyword row with its concept.
6. **Numbers per card level** ("1/2/3/4/5 strength", one number per level): every level is kept, as
   `{"x": "per_level", "items": [1, 2, 3, 4, 5]}` in level order. A number the same at every level is a plain number.
7. `python3 build_input.py <game> 20000` (batches of ~20,000 characters; a reader costs ~110-125k tokens whatever the size).
8. Read the keywords first (`input/<game>/keywords.jsonl`) and check every keyword record by eye: all cards with a keyword
   inherit it. A keyword named by cards but missing from the library and every source: a record by name in
   `read/<game>/keywords_stub.jsonl` only when the name says what it does (Can't Block).
9. Add the game's trigger labels and verbs to `patterns/patterns.tsv` (step 2.2 says how they are judged).

### 1. Reading
- Readers: background agents, model sonnet, the prompt in READER_PROMPT.md with only the batch name filled in. A reader
  costs about the same for 40 or 240 cards, so use as few as possible: one per ~20,000 characters (most games: one reader for
  the cards, one for the second reading).
- Never merge, normalize or rebuild while a reader runs (`run.py` refuses while part files exist). Wait for its reply.
- Keep a 10% sample for a second, independent reading (`second/<game>/`): the only accuracy measure needing no person.

### 2. After all batches (repeat until nothing changes)
1. `python3 run.py <game>`: normalize, check, load, cases, word check, status, examples. It stops at the first failure.
2. Word check. Patterns name only what a record must contain: trigger labels and phrases (an event), standard verbs (an
   act), duration words (this round, this game), and every keyword named outside the card's own Keywords field (automatic).
   Card names are masked first. Each pattern is judged once by reading its hits in the texts: where the wording means
   something else ("a follower that costs 2 more" is a filter, not a cost change), narrow the regex or widen what it
   accepts, with the reason in the file. Then `pattern_check.py <game> --reread` makes one batch of all flagged cards with
   the flags as notes. After the merge, each flag still open or rejected by the reader is decided by Claude against the
   text (a doubt goes to Kaptain) and written to `patterns/verdicts.tsv`.
3. Values: tally the readers' proposals (`*.proposals.jsonl`). Needs that repeat get values (rule 3), then
   `reread.py make <game> unsure` and read those batches. Repeat once more; what is left is unique to one card.
4. Names: every stub (a name a text uses that is no entry) is a card or keyword from the game's data (supplement), a
   family of cards (name_has), a type, or a misreading: `names.tsv` (normalize N6) turns a name read as a keyword or card
   into what it is. Look each up in the game's data; never guess. What nothing defines stays a name.
5. Second readings: `compare.py`, a judge agent (model opus) classifies each difference against the text; re-read the
   kept readings that are wrong; every "same meaning, different form" becomes a normalize rule.
6. `reread.py merge <game>` after every re-read, then `run.py <game>` again: a re-read can lose what the old reading had.

### 3. Case tests (`cases/`)
- mechanics.tsv: a question, the expected cards from the texts (regex on the text without its Keywords field, or a
  keyword in that field) and the query. Passes at 95% found. At least 60 per game: every trigger word, every keyword,
  every common verb, and "benefits from X, any way" for the main happenings (flat_ref).
- combos.tsv: real enabler/payoff pairs: the library's combos.tsv rows for the game, plus pairs found in the texts. 40+.
- regions.tsv: per faction its known mechanics (marked as Claude's), plus the library's signature, splash and archetype rows.
- A failing case is fixed at its cause: the query (check it against the texts first), the pattern, the value, or the
  records. Old tags are hints only; a case built on wrong old tags is dropped with its reason in DROPPED.md.

### 4. Kaptain's check
`check_table.py CHECK_20_<game>.md --random <game> 20` (cards with rows only; save the ids in CHECK_20_<game>_ids.txt). Each card: one line with its name and
text, then its rows. Every error he finds is fixed for all cards with the same problem.

### 5. Done when
`run.py <game>` passes every step; word check 0 open flags; no proposal need is shared by cards with different texts; stubs are
only names nothing defines; Kaptain approved CHECK_20_<game>; RESULTS.md and HANDOFF.md say the state; everything pushed.

After Kaptain's check: add a few of the game's approved records to BRIEF.md as worked examples under "Game words: <game>",
so the readers of every later game see approved examples from all earlier games.

## Asking the database
`ask.py <games> ...` where <games> is one game, several (runeterra,stormbound) or all: `cares|makes <happening or concept>
[mine|enemy]`, `concept <concept>`, `both <A> <B>`, `compare <concept> ...`, `together|feeds|fed|chains <concept>`,
`<game> deck <card or concept>`, `combo <A> <B>` (one game only),
`partners <card>`, `card <card>`, `list happenings|concepts`. QUERIES.md has example questions with real answers.
For "which cards care about X" always use flat_ref (ask.py cares): the same thing is stored as a trigger, a condition, a
count or a target filter depending on the wording. For "how do games do X" use concepts: a happening can differ between
games (round_start, turn_start) where the concept is the same (turn_start).

## Surviving session limits
- `python3 status.py <game>` first: it says from the files which batches are done, partial or todo.
- Readers write in parts (`<batch>.partN.jsonl`); a stopped reader is restarted with the same prompt and continues.
- Every finished batch is checked and pushed at once. Chats end with HANDOFF.md updated.

## Lessons from earlier games (do not repeat)
Runeterra:
- Judging the data by a narrow question. "Only 6 cards reward an ally dying" was one test's trigger-only question; the
  data held 41 (texts) as triggers, conditions, counts and dead-unit targets. Ask in every form (flat_ref), compare with texts.
- Old library tags taken as truth: they were wrong for whole regions (on_kill).
- A query with a SQL precedence slip blamed on the data. Check the query against the texts first.
- "Missing" or "broken" assumed instead of proven from the game's own data (Missing Translation; 185 missing cards; most
  stubs were misread families, types or keywords).
- One value with several meanings: zone discard held dead, discarded and tossed cards until BRIEF rule 17 split them.
- A keyword recorded as the wrong kind: Drain as a status made all 10 uses the wrong act. Read the keyword's definition
  and how cards use it.
- Re-reads trusted blindly: copies became summons, "summon an attacking champion" became a state filter and broke a combo.
- Rebuilding while a reader wrote part files; readers sharing a scratch folder; merging a batch whose reader still ran.
- Running normalize.py without file arguments (it does nothing); `run.py` now does it.
- Patch scripts that were not safe to run twice: a crash left some files changed. Check the new text is absent first.
- Card names inside texts taken as wording ("Prismatic Barrier", "Fury of the North", "Forge Workers").
- Showing Kaptain many tables or merged prose: he reads one line per card, then its rows (check_table.py).
- Writing a definition from memory instead of asking Kaptain.

Stormbound:
- The library's copy of a game can be old: Stormbound's was a 2022 list of 232 cards, the game's own card database had 284
  and many changed texts. Look for the game's current data before step 0.3 (the site's own data source; the built-in
  browser reaches what the workspace cannot), and verify a transcription against the source (length and checksum).
- A card with no text (plain units, tokens) is still a card: tokens are what other cards link to.
- A game that is not Runeterra-shaped needs its own values before reading (step 0.5): one stat (strength), a grid of tiles,
  turns per player, statuses. Readers still propose what is missing; tally the proposals after the first reading.
- Positions need "what from": "bordering a friendly Dragon" is a position filter with "of" (the Dragon). Readers left it
  out on many cards; the query layer shows it as of: parts and the combo reasons use them.
- Numbers per card level stay in the records (x per_level); the query layer shows the level-1 value so rules and SQL
  compare numbers. An amount worked out in play shows its kind (event_amount, count), never None.
- Generic layer gaps showed only when asking across games: keyword concepts missing for the new game, a stat named
  differently (strength vs power and health), act stun not naming its keyword, one meaning in two forms (Yasuo's trigger,
  now normalize N12 for every game). Every event, state, keyword and duration that two games word differently needs the same
  concept in vocab.tsv (column tree); a stat needs its role (attack_gain, defence_gain).
  Run `ask.py all compare` on the main concepts before calling a game done. Never link cards of different games.
- One reader for all cards, one for the second reading, one re-read: ~400k tokens in all, against 5.5 million on Runeterra
  with 53 readers.
- run.py loads every game, so the database never loses a game when another is rebuilt.
