# Process: describing a game's cards (the framework for every game)

For the chat that imports a game. Runeterra is the finished example: every step below was done on it.
Commands run from `library/cards_db/`. Files and tables: README.md.

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

## Steps
### 0. Before reading
1. Decide with Kaptain what is left out (modes, other products): `exclude.tsv`.
2. Completeness: compare the library's cards with the game's own published card list (by card code and by name). Cards
   the library lacks go to `supplement/<game>.jsonl` through a `supplement_<game>.py` like Runeterra's (ids 900001+).
   Runeterra lacked 185 cards, champions among them. Keywords the cards name that the library lacks come from the game's
   own glossary the same way (Runeterra: Assimilate). Keywords-field entries that are data artefacts go to NOT_KEYWORDS in
   build_input.py, with the proof (Runeterra: "Missing Translation" is Riot's AuraVisualFakeKeyword).
3. `python3 build_input.py <game> 20000` (batches of ~20,000 characters; a reader costs ~110-125k tokens whatever the size).
4. Read the keywords first (`input/<game>/keywords.jsonl`) and check every keyword record by eye: all cards with a keyword
   inherit it. A keyword the library lacks: a record by name in `read/<game>/keywords_stub.jsonl` only when its meaning is
   known (the name says it, or Kaptain's definition in `supplement/<game>_kaptain.jsonl`, ids 990001+).
5. Add the game's trigger labels and verbs to `patterns/patterns.tsv` (step 2.2 says how they are judged).

### 1. Reading
- Readers: background agents, model sonnet, the prompt in READER_PROMPT.md with only the batch name filled in. 6-8 at once.
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
`check_table.py CHECK_20.md --random <game> 20` (save the ids in CHECK_20_ids.txt). Each card: one line with its name and
text, then its rows. Every error he finds is fixed for all cards with the same problem.

### 5. Done when
`run.py <game>` passes every step; word check 0 open flags; no proposal need is shared by cards with different texts; stubs are
only names nothing defines; Kaptain approved CHECK_20; RESULTS.md and HANDOFF.md say the state; everything pushed.

## Asking the database
`ask.py <game> cares|makes <happening> [mine|enemy]`, `concept <concept>`, `combo <A> <B>`, `partners <card>`,
`card <card>`, `list happenings|concepts`. For "which cards care about X" always use flat_ref (ask.py cares): the same
thing is stored as a trigger, a condition, a count or a target filter depending on the wording.

## Surviving session limits
- `python3 status.py <game>` first: it says from the files which batches are done, partial or todo.
- Readers write in parts (`<batch>.partN.jsonl`); a stopped reader is restarted with the same prompt and continues.
- Every finished batch is checked and pushed at once. Chats end with HANDOFF.md updated.

## Mistakes made on Runeterra (do not repeat)
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
