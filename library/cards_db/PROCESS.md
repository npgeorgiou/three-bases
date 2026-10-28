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

## Writing data the same way in every game (read before step 0.6)
The database answers one question over all games at once (`ask.py all ...`). That only works when every game is written
with the same values, shapes and habits. A game's own words stay in its card texts, keyword entries and types; the rows say
what cards do in shared values.
1. Reuse before adding. For each of the game's terms, search vocab.tsv for a value that means the same and use it (a base
   or hero with life = kind player; a structure = kind landmark). Add a value only when no value means it, and word it so
   any game could use it ("start of the owner's turn", "the tile in front"), with the game as an example in brackets.
2. Every keyword gets a vocab keyword row whose concept (column tree) says what it does by the game's own rules, checked
   against the concept tree's definition. Stun in Runeterra: the unit can't act, so disable; Frostbite sets Power to 0, so
   attack_zero (Kaptain, 28 Oct 2026). Freeze in Stormbound: no move and no ability for a turn, so disable.
   These mappings decide how every card is sorted, so they are checked keyword by keyword before a game is done, and
   checked again: (a) the keyword's meaning from the game's own rules (glossary, wiki), not from memory or the old library;
   (b) the concept's definition, including its "not this" part; (c) whose side it hits (an enemy that can't block is
   cant_block, my own unit that can't block is a drawback); (d) whether the keyword belongs to the game at all (a mode left
   out: Terrify is Path of Champions, so it is deleted). Runeterra's old library mappings were wrong for Stun, Frostbite,
   Rally, Vulnerable, Fleeting, Landmark and Can't Block until Kaptain checked them (28 Oct 2026). Show Kaptain the full
   keyword -> concept list (with each concept's definition) before calling a game done.
3. Every event, state and duration that two games word differently gets the same concept: round_start and turn_start are
   turn_start; this_round and next_own_turn are temporary_effect; a state takes its keyword's concept (stunned like Stun).
4. Stats by role: Power is attack, Health is health, Stormbound's strength is both. Never add a stat for one game when an
   existing one fits; the concepts attack_gain and defence_gain find stat gains in every game.
5. Statuses: giving one is give_keyword with the keyword; "a poisoned unit" is a state whose causes is
   given_keyword:<Keyword>; an act that gives a keyword names it in its causes (stun: given_keyword:Stun).
6. Board positions are filters `{"attr": "position", ..., "of": TARGET}`: always say what the position is measured from.
7. One meaning, one form, in every game: the normalize rules (N1-N12) run on every game. A new form found in one game gets a
   rule for all games, and every game is rebuilt (`run.py <each game>`, all cases must still pass).
8. Card names are stored without trailing spaces (load.py); look names up the same way.
9. Links between cards (combos, decks, "feeds") are made only inside one game: each game is its own world. Questions over
   several games add up, by concept, what each game shows.
10. Before a game is done: `ask.py all compare <its main mechanics>` must show its cards next to the other games' (a mechanic
   its cards clearly have but the answer lacks = a missing mapping), and `ask.py <game> analyze "<a known deck>"` must explain
   a deck from a guide the way the guide does.

## Two chats on two games at the same time
It works: each chat writes its own game's files (read/<game>/, input/<game>/, second/<game>/, supplement/<game>*.jsonl,
supplement_<game>.py, CHECK_20_<game>*). The shared files need care:
- Id block: the first thing each chat does is write its game's line in source.py (the next free block) and push it. If the
  push is refused, pull: the other chat took that block, so take the next one.
- Shared files (vocab.tsv, BRIEF.md, patterns/patterns.tsv, normalize.py, flat.py, refs.py, connections.py, cases/*.tsv,
  CHANGES.md, PROCESS.md): pull before editing, keep each change small, commit and push it at once. Before adding a vocab
  value, pull and search vocab.tsv again: the other chat may have added the same meaning under another name (one meaning,
  one value). Never edit another game's records.
- cards.sqlite and QUERIES.md are rebuilt from the files: after every pull, run `run.py <your game>` (it loads every game);
  on a merge conflict in them, take either side and rebuild. A change to shared code or values must leave every game's
  `run.py` passing (run each game) before it is pushed.
- Never force-push. Readers of different chats never share a scratch folder (/tmp/reader_<game>_<batch>/).

## Steps
### 0. Before reading (in this order)
1. **Research the game** (library/ADDING_GAMES.md section 0.1 says how): rules, the full keyword glossary, factions or
   tribes, board, turn structure. It is the checklist for steps 0.5, 0.6 and the case tests.
2. **Left out** (`exclude.tsv`): only other modes or products, and only what Kaptain names. Cards that other cards create
   (tokens) are never left out: links to them are how combos are found.
3. **The game's data is already in the repo. Look there before fetching anything** (two chats fetched a game's data again
   from the web because they did not look; Kaptain does not know where each file is, so it is written here):
   - `library/tools/convert/conv_<game>.py`: its first lines name the source, date and format of the game's card data. Raw
     files kept next to them: `monster_train_cards.psv` (all 282 Monster Train cards, wiki Module:Cards/Data, 20 Oct 2026),
     `inscryption_missing_cards.json`. Named sources: Lorcana (npm lorcana-oracle), Star Wars: Unlimited (swucardex-data
     a86faed), Elder Scrolls: Legends (TESLegendsTracker c541e82), Slay the Spire (wiki Module:Cards/data), Slay the Spire 2
     (Kaptain's lists, 12 Oct 2026), Gwent (gwent.one v14.8), Magic (MTGJSON AtomicCards, Scryfall tokens), Shadowverse
     (Portal API), 40k and Age of Sigmar (BSData).
   - `library/tools/games/<game>.md`: the research (sources, factions) and, in its mechanics block, the rules and keyword
     terms with the page each comes from. Check each term's source is this game (Monster Train's file mixes in Monster Train
     2 terms from railtools.net) and drop terms marked "assumed": rule 1.
   - `library/tools/key/<game>/`: files of the old library reading. `library/cards_db/supplement/<game>.jsonl`: games
     imported here.
   Fetch from the web only what none of these has, and add the new source to this list.
4. **Cards.** Compare the library's cards with the game's own published card list, by card code and by name.
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
5. **Keyword definitions** come from the game's own glossary (official site, the game's data, its wiki), with the source
   in source_type. Kaptain is asked only for a keyword no source defines. A keyword with no definition stays a name.
6. **The game's words** (before any reading; readers can only use values that exist). For every term of the checklist
   (stats, board positions, turn structure, zones, card kinds, statuses), in this order:
   - same meaning as an existing value: use it, and write the mapping in BRIEF.md under "Game words: <game>" (e.g. a
     player's base or hero with health = kind player, like Runeterra's Nexus);
   - a different meaning: a new vocab.tsv row (rule 3), with an example from one of the game's cards in BRIEF.md. A new
     event or state needs its `causes`. Do not stretch an old value: "at the start of your turn" is not round_start when
     the game has turns per player.
   Kaptain has not played most games: decide the mapping from the game's rules yourself (marked as Claude's) and write it
   in BRIEF.md; ask him only what no source settles. Also give every keyword a vocab keyword row with its concept.
7. **Numbers per card level** ("1/2/3/4/5 strength", one number per level): every level is kept, as
   `{"x": "per_level", "items": [1, 2, 3, 4, 5]}` in level order. A number the same at every level is a plain number.
8. `python3 build_input.py <game> 20000` (batches of ~20,000 characters; a reader costs ~110-125k tokens whatever the size).
9. Read the keywords first (`input/<game>/keywords.jsonl`) and check every keyword record by eye: all cards with a keyword
   inherit it. A keyword named by cards but missing from the library and every source: a record by name in
   `read/<game>/keywords_stub.jsonl` only when the name says what it does (Can't Block).
10. Add the game's trigger labels and verbs to `patterns/patterns.tsv` (step 2.2 says how they are judged).

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
`run.py <game>` passes every step; the keyword -> concept list checked twice and shown to Kaptain; word check 0 open flags; no proposal need is shared by cards with different texts; stubs are
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
  and many changed texts. Look for the game's current data before step 0.4 (the site's own data source; the built-in
  browser reaches what the workspace cannot), and verify a transcription against the source (length and checksum).
- A card with no text (plain units, tokens) is still a card: tokens are what other cards link to.
- A game that is not Runeterra-shaped needs its own values before reading (step 0.6): one stat (strength), a grid of tiles,
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
