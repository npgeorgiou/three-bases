# The wheel pipeline: the commands of each step and what each makes
Commands run from `library/cards_db/` unless they start with `factions/` or `tools/`. The rules of each step are in
`factions/START_DESIGN-1-wheel.md`; this file says how each result is made. Before anything: `gunzip -kf links.sqlite.gz`.
After a change to `network.py` or `cards.sqlite`: `PYTHONHASHSEED=0 python3 links.py` (about 7 minutes; tell Kaptain and
wait for his OK; it writes links.sqlite.gz too). A step is redone when what it uses changes. A script marked "to write"
is written in that step's chat, from the rules of the step, and its line here is then filled in.

## Step 1. Fix the library's concepts
- Suspects: `factions/wheel/work/suspects.tsv` (concept, the games it is counted in, the games left out, where it
  is limited), plus a script (to write) that finds concepts whose cards link to quite different concepts in one
  game than in the others.
- Fixes: split by the card's rows, as the database's fix scripts do (`START_DATABASE.md`), each with test cases; a
  card read (within the wheel's 500, low-cost model, Kaptain's OK first) only where its rows can't tell. Then the game
  limits go from the radius lists in `axes.py`, and `links.py` is rebuilt.

## Step 2. The radii and how they work together
- What: 23 radii (`SPOKES` in axes.py: key, name, the library concepts that count a card for it). A faction's value
  on a radius = its share of such cards / its game's average share (1 = average). 43 real factions of 8 games.
- `python3 axes.py` -> `axes.tsv`, `factions/wheel-axes.html`. How the values are made: `factions/13`.
- `python3 mechanics_wheel.py links --radii` -> `wheel/radius_links.tsv` (`axes.radius_links`): per pair of radii
  `cards`, `decks`, `links`, `level`, each worked out per game and averaged (`cards`: games where chance gives 5+ linked
  pairs, 20+ in all; `decks`: games with 5+ decks holding both). A link counts for a radius only when the effect that
  made it, on that card's side, belongs to the radius (the links' `a_ab`/`b_ab`), for chance too. Checked by
  `cases/wheel.tsv`.

## Step 3. The 20 shapes
- `python3 ../../factions/wheel/work/shapes.py --write` (about 2 minutes) -> `factions/wheel/work/shapes.tsv` (letter
  A-T, radius=value list). Without `--write` it prints the 20, their real factions and the kinds of play each carries.
- Candidates: every 3-6 of a real faction's radii valued 1.2+ whose radii are all joined (step 2), with that faction's
  values. Picking: a search over 20 candidates, at most one per real faction; misses of the rules count 100 each, and
  sameness (shared radii between two shapes, squared) decides the rest. Four fixed seeds, so every run gives the same.
- The kinds of play: `factions/wheel/archetypes.tsv` (key, what it is, its radii, its concepts).

## Step 4. The usable concepts
- `python3 ../../factions/wheel/work/concept_catch.py` (to write) -> `work/concepts.tsv`: every concept with 10+
  real cards, its cards, the share of its cards on each radius; the concepts left out with their reasons from
  `work/concept_verdicts.tsv`.

## Step 5. The links between concepts
- `python3 mechanics_wheel.py links --concepts` (to write; the same count as `--radii`) -> `wheel/concept_links.tsv`:
  per pair of usable concepts `cards`, `decks`, `links`, `level`, which one makes and which one uses, the top link texts.
  `python3 apart.py` gives the pairs real factions keep apart.

## Step 6. The 20 groups
- `python3 factions/wheel/work/groups.py --write` (to write; an exact solver for all 20) -> `factions/wheel/work/groups.tsv`
  (faction, pillars, others, its mechanics with link texts and counts). `python3 tools/wheel_table_check.py` (to
  rewrite) checks the rules of the step from the files.

## Step 7. Theme, then tools
- Claude -> `factions/wheel/themes.tsv` (faction, theme) and `factions/wheel/tools.tsv` (faction, tool, mechanic, the
  tools it feeds, the cell-by-cell line, source: a library card or CLAUDE, NEW RULE).

## Step 8. Combos on this board
- A script (to write) counts the joins between every two groups (step 5 numbers); Claude rates the pairs on the board
  -> `factions/wheel/combos.tsv` (pair, STRONG/OK/WEAK/NONE/AGAINST, how it plays, the numbers, a test column).

## Step 9. The seven answers and Stop 1
- Claude -> `factions/wheel/answers.tsv`, from the tools. `python3 tools/wheel_table_check.py` checks steps 2-9,
  including words that break this game's rules. `python3 factions/wheel/work/make_stop1.py` (to rewrite) writes
  `STOP1.md` and `STOP1-1..5.md`.
