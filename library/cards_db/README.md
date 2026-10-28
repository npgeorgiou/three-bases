# Card database (what cards do, as a network)

Start here: HANDOFF.md. For a new game: GUIDE.md. What Runeterra showed: RESULTS.md. Example questions: QUERIES.md.

Each card is described as abilities: an event (when), conditions (if) and effects (do). Every field is a value from
`vocab.tsv`, a number, or a link (id) to another card, keyword or type. No free text. The reader records in `read/<game>/`
are the source; `cards.sqlite` is rebuilt from them.

| File | What it is |
|---|---|
| `source.py`, `supplement/`, `supplement_<game>.py` | Every script reads cards through source.lib(): the library's entities plus supplement/<game>.jsonl (cards the library lacks, from the game's own data) |
| `BRIEF.md` | The record shapes, reading rules and approved examples (what readers follow) |
| `vocab.tsv` | Every allowed value per field, its meaning, its concept-tree concept, and (for effects) the events it causes |
| `build_input.py` | Cards to read, cut into batches by amount of text; keyword-only cards get an empty record directly |
| `check.py` | Checks records against the shapes and values and resolves names to ids |
| `load.py` | Builds `cards.sqlite` from the records, then the query layer |
| `flat.py` | Query layer: flat_when / flat_if / flat_do rows with keywords expanded, flat_concept with concept-tree concepts (RULES) |
| `refs.py` | Query layer: flat_ref, every way a card works with a happening (makes it, waits for it, tests or counts it, picks things it happened to), one row each |
| `connections.py` | How one card sets off another (event, made card, zone, keyword or type asked for) |
| `cases/` | Case tests: mechanics.tsv, combos.tsv, regions.tsv, run.py, REPORT.md, DROPPED.md (cases dropped and why) |
| `GUIDE.md`, `RESULTS.md`, `QUERIES.md`, `examples.py` | How to do the next game; the Runeterra findings; example queries with real answers |
| `HANDOFF.md` | Where the work stands and what is open (read first in a new chat) |
| `input/<game>/` | Reader input batches |
| `read/<game>/` | Reader output: one JSON record per card (the source of truth), plus proposals for new values |
| `CHANGES.md` | Every change to the shapes or values, with the card that caused it |
| `CHECK_20.md`, `check_table.py` | Kaptain's check file: chosen cards' stored rows, one table per database table, columns as stored, card/keyword/type/name ids shown as names (always made this way, as one file) |
| `STATUS.md` | Which batches are done, partial or still to read (made by `status.py <game>` from the files) |
| `status.py`, `show.py`, `compare.py` | Progress from the files; cards with their records for checking by eye; first vs second reading |
| `raw.py` | A card's stored rows exactly as in the database (ids, values, numbers) |
| `pattern_check.py` | Plain wording (Round Start:, Stun, a named keyword...) must show up somewhere in the card's record |
| `exclude.tsv`, `excluded/` | Entries left out on purpose (Runeterra: Path of Champions items) and their old records |
| `rows.py` | A card's rows from `cards.sqlite` as a table with names (what Kaptain checks) |
| `reread.py`, `normalize.py` | Re-reading chosen records under the current brief (old readings kept in `replaced/`); one canonical form for equal meanings |
| `fixes/`, `replaced/` | Re-read batches after merging; the old readings they replaced |
| `second/<game>/` | Independent second reading of a 10% sample, to measure how often readers disagree |

Tables in `cards.sqlite`: card, type, card_type, card_keyword, card_link (levels into, generates), ability (given_by_effect
for abilities an effect gives), event, cond, effect, param, target, filter (op in on several rows of one attr = one of them),
amount, amount_item, name_part, keyword_trigger, unsure, vocab, causes (which effect causes which event), and the query layer
flat_when, flat_if, flat_do, flat_concept, flat_ref. Searches use the flat tables and concepts, never keyword names.

**Asking which cards care about something (decided 28 Oct 2026).** Anything a card can work with is a happening: an `event`
value in vocab.tsv (dies, summoned, damaged, given_keyword, stat_changed, drawn, ...). Ask flat_ref, never flat_when alone,
because the same thing is stored as a trigger, a condition, a count or a target filter depending on the wording:
`select distinct card from flat_ref where happening='<event>' and role!='makes' and side in ('mine','any','')`
(role makes = the card causes it; side '' = either side; add `and coalesce(pick,'')!='self'` for "other units"). A state is
tied to its happening by the `causes` column of its vocab row (dead_this_round -> dies; stunned -> given_keyword:Stun); a
unit in zone discard is a unit that died (BRIEF rule 17). A state with no happening (champion, ephemeral, fleeting...) is a
property, not a happening. A new event or state gets its `causes` entry in the same change, or flat_ref misses it.

## Surviving session limits (rules for every chat doing this work)
Nothing about the run lives only in a chat. Everything needed to continue is in these files:
1. Before anything else, run `python3 status.py <game>`: it says from the files which batches are done, partial or todo.
2. Every finished batch is checked (`check.py ... --input ...`) and committed and pushed at once, one commit per batch or
   group of batches. Readers write in parts (`<batch>.partN.jsonl`); part files are committed too when a session ends, so a
   stopped reader loses at most the part it was writing.
3. A partial batch is finished by a new reader told to read only the cards missing from the output (`build_input.py`
   `--only` with those ids, or the reader skips ids already in the parts), then the parts are joined and checked.
4. Values and rules change only through `vocab.tsv`, `BRIEF.md` and a line in `CHANGES.md`, committed in the same step.
5. The reader prompt is in `READER_PROMPT.md`; a new chat uses it unchanged, filling in the batch name.
6. `reread.py merge` and `normalize.py` run only on batches whose reader has finished (a running reader rewrites a file
   that disappears under it).
7. Order of work for a game: all batches -> `normalize.py` on all records -> `pattern_check.py` and re-read what it flags -> `reread.py make <game> unsure` and read the
   fix batches -> `reread.py merge` -> `normalize.py` again -> `compare.py` on the second-reading sample -> `load.py`.
8. After every rebuild: `cases/run.py <game>` must pass; `examples.py` refreshes QUERIES.md.
