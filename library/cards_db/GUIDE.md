# Guide: describing another game's cards (from the Runeterra test, 27-28 Oct 2026)

Read this, README.md (files and the rules for surviving session limits) and RESULTS.md before starting a game. Everything
runs from the files in this folder; nothing depends on an earlier chat.

## 0. Before reading
- Decide with Kaptain what is left out (modes, campaigns, other products) and write it to `exclude.tsv`
  (Runeterra: Path of Champions items, found by their source "Path of Champions item").
- `python3 build_input.py <game> 20000`: batches of about 20,000 characters of card text. Reader cost per batch was nearly
  fixed (110,000-125,000 tokens whether 39 or 189 cards), so bigger batches are cheaper; check the first batch's quality
  (show.py on 20 random cards) before reading the rest at that size.
- Read the game's keywords first (input/<game>/keywords.jsonl) and check every keyword record by eye: every card with a
  keyword inherits its meaning in the query layer, so a wrong keyword record is wrong on hundreds of cards.
- Keywords a game's cards name but the library lacks get a record in `read/<game>/keywords_stub.jsonl` by name, only when the
  name says what it does (Can't Block). Never write a rule the library has no text for (Runeterra's Deep stays empty).

## 1. Reading
- Readers: background agents, model sonnet, the prompt in READER_PROMPT.md unchanged. 6-8 at a time.
- After each batch: `check.py` (0 problems), `normalize.py`, commit and push (README rules).
- Keep a 10% sample for a second, independent reading (`second/`): it is the only accuracy measure that needs no person.

## 2. After all batches
1. `pattern_check.py <game>`: plain wording that must show up in the record (Round Start:, Stun, Deal N, a named keyword).
   Add the game's own trigger words to TRIGGERS and its keyword stand-ins to KW_EQUIV first. Re-read what it flags with
   the flags as notes (`reread.py make <game> ids ...`, notes file in second/<game>/).
2. Values: tally the readers' proposals; add the recurring ones to vocab.tsv and BRIEF.md (a line in CHANGES.md each), then
   `reread.py make <game> unsure` and read those batches.
3. `compare.py` first vs second readings, a judge agent (model opus) classifies each difference against the text
   (same / first_wrong / second_wrong / both_wrong). Re-read the kept readings that are wrong, with the judge's notes.
   Turn every "same meaning, different form" into a normalize.py rule.
4. `load.py <game>` builds cards.sqlite and the query layer (flat.py): keywords expanded onto the cards, concept-tree
   concepts on every row, shape rules (RULES in flat.py) for concepts like aoe_damage or permanent_growth.
5. Case tests (`cases/`): write the game's cases, run `cases/run.py <game>`, fix until all pass (below).

## 3. Case tests (cases/)
- mechanics.tsv: a question, the expected cards from the texts themselves (a regex on the card text without its Keywords
  field, or a keyword in the Keywords field), and the query on the records. Passes at 95% of the expected cards found.
  Per game: at least 60 mechanics, covering every trigger word, every keyword (through the Keywords field), every common verb.
- combos.tsv: real enabler/payoff pairs. Take the library's combos.tsv rows for the game, then add pairs found in the texts:
  for each payoff wording ("When you draw", "When an ally dies") pick enablers whose text plainly does it. 40+ per game.
- regions.tsv: per faction, its known mechanics (marked as Claude's), plus the library's faction_signature (signature and
  splash) and faction_archetypes rows. Old library tags are hints: when a case fails, read the old-only cards; if the old tags
  are wrong, drop the case and write why in cases/DROPPED.md (Runeterra: on_kill tags on Rally and Summon cards).
- When a case fails, find out which of three it is, and fix that, never the threshold:
  (a) the text pattern catches other words (a card name like "Behold the Infinite"): fix the pattern;
  (b) the query asks too narrowly (a trigger "When you Recall" is an event, not an act): ask for act, event and condition;
  (c) the record is wrong: re-read the card with a note (reread.py), or add the missing value or rule for every card.
- Look at the "extra" column too: cards the query finds that the text pattern does not. In Runeterra they were mostly right
  (keyword meanings: Deathless revives, Sleep obliterates), which shows the query layer works; a wrong extra is a wrong record.

## 4. What went wrong in Runeterra (do not repeat)
- Checking against old tags as truth: they were wrong for whole regions (on_kill).
- Writing a query with a SQL precedence slip and calling the data wrong ("only 16 cards reward an ally dying"): when a query
  returns too little, check the query first, against the texts.
- Merging a fix batch while its reader was still writing; readers sharing one scratch folder.
- Card names inside texts ("Prismatic Barrier", "Flow (created)") taken as wording.
- Batches too small for the fixed cost per reader.
