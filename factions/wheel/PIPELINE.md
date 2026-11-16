# The wheel pipeline, steps 1-9: the commands and what each step makes
Commands run from `library/cards_db/` unless they start with `factions/`. The rules of each step are in
`factions/START_DESIGN-1-wheel.md`; this file says how each result is made.
Before anything: `gunzip -kf links.sqlite.gz` (every number below needs links.sqlite). After a change to `network.py`
or `cards.sqlite`: `PYTHONHASHSEED=0 python3 links.py` (about 7 minutes; tell Kaptain and wait for his OK; it writes
links.sqlite.gz too). A step is redone only when what it uses changes, and then only for the parts that
changed. Each step says what a script does and what is judgment.

## Step 1. The radii
- What: 24 radii (`SPOKES` in axes.py: key, name, the library concepts that count a card for it). A faction's value
  on a radius = its share of such cards / its game's average share (1 = average). 43 real factions of 8 games.
- Script: `python3 axes.py` -> `axes.tsv`, `factions/wheel-axes.html`. How the values are made: `factions/13`.
- Judgment: which concepts belong to each radius (checked by agents reading cards, `axes.py --cards <file>`).

## Step 2. The radii that work together
- Numbers: `python3 mechanics_wheel.py links --radii` -> `wheel/radius_links.tsv` (`axes.radius_links`). Per pair of
  radii: `cards` = how much more often than chance the library links a card of one with a card of the other (same
  game); `decks` = how much more decks heavy in one hold the other. 1 = chance. Both are worked out per game and
  averaged over the games, so each game counts the same (`cards`: games where chance gives 5+ linked pairs, 20+ in all;
  `decks`: games with enough decks holding both). `links` = the linked card pairs made by the two; `level` = that
  count growing slowly (0, 1 link = 1, 10 = 2, 100+ = 3). "Rewards playing spells" is judged by `decks` only.
- Radii joined = `cards` 1.2 or more, or `decks` 1.5 or more. Mechanics joined (steps 5-6) = `level` 1 or more (the library
  links them at all), or `decks` 1.5 or more.
- A link counts for a radius only when the effect that made it, on that card's side, belongs to the radius (the links'
  `a_ab`/`b_ab` columns), for chance too (the share of a radius' cards' links its own effects make). Numbers only:
  nobody reads card pairs. Checked by `cases/wheel.tsv` (run at the end).

## Step 3. The 20 factions as shapes
- Script: `python3 ../../factions/wheel/work/shapes.py --write` (about 2 minutes) -> `factions/wheel/work/shapes.tsv`
  (letter A-T, radius=value list). Without `--write` it only prints the 20, their real factions and the archetypes
  each carries.
- Candidates: every 3-6 of a real faction's radii valued 1.2+ ("cards" values in axes.tsv) whose radii are all joined
  (step 2), with that faction's values. "One chosen" is left out.
- Picking: a search over 20 candidates, at most one per real faction; misses of the rules count 100 each (every
  radius in 2-5 shapes; every archetype of `factions/wheel/archetypes.tsv` carried by 2+ shapes, a shape carrying at
  most 2 through its two highest values), and sameness (shared radii between two shapes, squared) decides the rest.
  Four fixed seeds, so the result is the same each run.
- Checked by: `python3 tools/wheel_table_check.py` (from the repo root; 3-6 radii, each joined, no two shapes the same).

## Step 4. The mechanics list
- File: `factions/wheel/mechanics.tsv`, one line per mechanic, never two merged: key; sentence "I do X -> I gain from
  X"; concepts (the library concepts that count a card as this mechanic; `concept@game,game` counts only in those
  games); NEW RULE mark; "made by" concepts (cards that make it happen, counted with it); size (SMALL = under 30 right
  cards in every real faction).
- Where the list comes from: every library concept with real cards and in no mechanic is sorted in
  `work/concept_sort.tsv` (concept, cards, verdict); a CANDIDATE is read like the others and joins the list or gets its reason.
- Reading: `python3 mechanics_wheel.py cards <file>` writes 8 cards per mechanic from cards.sqlite (game, the card's
  concepts, name, the first 220 letters of its text). Agents read them and say how many of the 8 are really this
  mechanic and which concepts to add, drop or limit to some games (`work/concept_fixes_*.tsv`,
  `work/newmech_verdicts*.tsv`). Only the concepts column changes; cards.sqlite is not changed.
- Rule check against this game's rules (summary/03-07) and the archetype check against `archetypes.tsv`
  (START_DESIGN-1-wheel.md step 4).
- Then: `python3 mechanics_wheel.py measure` -> `wheel/measured.tsv` (per mechanic: cards, games with 10+, the biggest
  real faction's count, the real factions with the highest share, the radii it serves) and
  `python3 mechanics_wheel.py links` -> `wheel/links.tsv` (per pair of mechanics, the same numbers as step 2).
- Stop A: `STOPA.md` shows the list to Kaptain in plain words.

## Step 5. Each faction's mechanics
- Scripts, no reading: `cd factions/wheel/work && python3 signatures.py --write` then `python3 borrow.py --write`
  -> `work/assign.tsv`; checked by `work/check_assign.py`. Both solve all 20 factions at once (an exact solver): the
  score of a choice is its fit to the faction's radii and archetypes plus how strongly the faction's mechanics are linked
  (`wheel/links.tsv`: `cards` and `decks`), under the rules of START_DESIGN-1-wheel.md step 5.

## Step 6. Links between mechanics
- Numbers only: `python3 mechanics_wheel.py links` -> `wheel/links.tsv` (per pair of mechanics, the same numbers as
  step 2, counted by the links' own effects). `python3 apart.py` gives the pairs real factions keep apart.

## Step 7. Theme, then tools
- Claude picks one theme per faction -> `factions/wheel/themes.tsv` (faction, theme).
- Claude writes 2-4 tools per faction -> `factions/wheel/tools.tsv` (faction, tool, mechanic, the tools it feeds, the
  cell-by-cell line, source: a library card or CLAUDE, NEW RULE). Card texts read for it go into
  `factions/read-cards.tsv` (within the faction's 100).

## Step 8. Combos on this board
- Agents (`work/combo_prompt.txt`, Kaptain's OK first) rate all 190 pairs of factions from their tools and mechanics ->
  `combos.tsv` (STRONG/OK/WEAK/NONE/AGAINST, how it plays, source, a test column for playtests). Partners = STRONG or OK.

## Step 9. The seven answers and Stop 1
- An agent (`work/answers_prompt.txt`) -> `answers.tsv`, from the tools. `python3 tools/wheel_table_check.py` (repo
  root) checks steps 2-9, including words that break this game's rules. `python3 factions/wheel/work/make_stop1.py`
  writes `STOP1.md` and `STOP1-1..5.md`.

## Files, in order
| step | input | script | output |
|---|---|---|---|
| 1 | cards.sqlite, links.sqlite | axes.py | axes.tsv, factions/wheel-axes.html |
| 2 | links.sqlite | mechanics_wheel.py links --radii | wheel/radius_links.tsv |
| 3 | steps 1-2, archetypes.tsv | work/shapes.py | work/shapes.tsv |
| 4 | mechanics.tsv | mechanics_wheel.py cards, agents, measure, links | mechanics.tsv, work/concept_fixes_*.tsv, wheel/measured.tsv, wheel/links.tsv |
| 5 | steps 3-4 | work/signatures.py, work/borrow.py | work/assign.tsv |
| 6 | links.sqlite | mechanics_wheel.py links, apart.py | wheel/links.tsv |
| 7 | steps 5-6 | Claude | themes.tsv, tools.tsv |
| 8 | steps 6-7 | agents | combos.tsv |
| 9 | steps 7-8 | agent, wheel_table_check.py, make_stop1.py | answers.tsv, STOP1*.md |
