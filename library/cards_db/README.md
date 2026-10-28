# Card database (what cards do, as linked rows)

Start here: HANDOFF.md (state). Importing a game: PROCESS.md. Results per game: RESULTS.md. Example answers: QUERIES.md.

Games: Runeterra (done), Stormbound (waiting for Kaptain's check). One database holds all games, and every question can run
across them (`ask.py all ...`).

Each card is described as abilities: an event (when), conditions (if) and effects (do). Every field is a value from
`vocab.tsv`, a number, or a link to another card, keyword or type. No free text. Values are generic (no game's own words);
equal mechanics of different games share one concept of the concept tree (Stun and Freeze: disable). The reader records in
`read/<game>/` are the source; `cards.sqlite` is rebuilt from them, for every game, by `run.py <game>`.

## Files
| File | What it is |
|---|---|
| `run.py` | The whole build of a game in one command, in the safe order (PROCESS.md step 2.1); it loads every game |
| `ask.py` | Questions answered with card names, per game or across games (`ask.py all ...`; QUERIES.md shows examples) |
| `PROCESS.md` | The framework: rules, steps, gates, mistakes not to repeat |
| `BRIEF.md`, `READER_PROMPT.md` | What readers follow: record shapes, reading rules, approved examples; the reader prompt |
| `vocab.tsv` | Every allowed value per field: meaning, concept-tree concept, and the events it causes (`causes`) |
| `names.tsv` | Names readers took for a keyword or card that are something else (keyword, card, type, name family, or dropped), per game, with reasons |
| `source.py`, `supplement/`, `supplement_<game>.py` | Cards come from the library plus `supplement/<game>.jsonl` (cards and keywords the library lacks, from the game's own data) and `<game>_kaptain.jsonl` (definitions Kaptain gave); id blocks per game in source.py |
| `build_input.py` | Reader input batches (`--add` for cards new to the source); keyword-only cards get empty records |
| `check.py`, `normalize.py` | Records against shapes and values; one canonical form for equal meanings (rules N1-N9) |
| `load.py`, `flat.py`, `refs.py` | Build `cards.sqlite`; the query layer (keywords expanded, concepts, flat_ref) |
| `mechanics.py` | Questions about mechanics (concepts) and decks, links inside each game added up over games |
| `connections.py` | How one card sets off another, every reason ranked, most direct first |
| `pattern_check.py`, `patterns/` | Word check: `patterns.tsv` (wording rules, each judged once), `verdicts.tsv` (flags decided once), `<game>_flags.tsv` (open flags) |
| `reread.py` | Re-read chosen cards under the current brief; merge replaces the old readings (kept in `replaced/`, re-read output in `fixes/`) |
| `cases/` | Case tests (mechanics, combos, regions), `run.py`, REPORT.md, DROPPED.md |
| `rows.py`, `check_table.py`, `CHECK_20_<game>.md`, `CHECK_20_<game>_ids.txt` | A card's rows with names; Kaptain's check file (one line per card, then its rows) and its card ids |
| `status.py`, `STATUS.md`, `compare.py`, `examples.py`, `QUERIES.md` | Progress from the files; first vs second reading; example questions with answers |
| `exclude.tsv`, `excluded/` | Entries left out on purpose and their old records |
| `input/`, `read/`, `second/` | Reader input; reader output (the source) with proposals; the independent second reading of a 10% sample |
| `CHANGES.md`, `RESULTS.md`, `HANDOFF.md` | Every change to shapes, values and rules; each game's results; where the work stands |

## Tables in cards.sqlite
card, type, card_type, card_keyword, card_link (levels into, generates), ability (given_by_effect for abilities an effect
gives), event, cond, effect, param, target, filter (op in on several rows of one attr = one of them), amount, amount_item,
name_part, keyword_trigger, unsure, vocab, causes; the query layer flat_when, flat_if, flat_do, flat_concept, flat_ref.
Searches use the query layer, never keyword names.

## Which cards care about something
Anything a card can work with is a happening: an `event` value in vocab.tsv (dies, summoned, damaged, given_keyword,
stat_changed, drawn, ...). flat_ref has one row for every way a card works with one: makes it, waits for it (trigger),
tests or counts it (condition), or picks things it happened to (state: a state whose vocab `causes` names it, or a unit in
zone discard = died). So one query finds them all, whatever the wording:
`select distinct card from flat_ref where happening='dies' and role!='makes' and side in ('mine','any','')`
(side '' = either side; add `and coalesce(pick,'')!='self'` for "other units"). Same as `ask.py all cares dies mine`.

## Questions across games
`ask.py all concept <concept>` and `compare <concept> ...` show how each game does a mechanic; `both <A> <B>` the cards
that combine two mechanics; `cares` / `makes` take a concept too (`cares disable`: units stunned or frozen). Mechanic
questions (mechanics.py): `together <concept>` (what a mechanic is built with), `feeds` / `fed <concept>` (mechanics that set
it off or that it sets off), `chains <concept>` (families of three), `<game> deck <card or concept>` (cards of one game, in
its faction, that feed each other). A link between two cards is only made inside one game: each game is its own world; the
answers add up, by concept, what every game shows. Keywords meet through their concept (vocab keyword rows), states
through theirs (stunned, frozen: disable), events through theirs (round_start, turn_start: turn_start), stats through
their role (concepts attack_gain, defence_gain: Power, Health, or a strength that is both).
