# The wheel pipeline: the commands of each step and what each makes
Commands run from `library/cards_db/` unless they start with `factions/` or `tools/`. The rules of each step are in
`factions/START_DESIGN-1-wheel.md`; this file says how each result is made. Before anything: `gunzip -kf links.sqlite.gz`.
After a change to `network.py` or `cards.sqlite`: `PYTHONHASHSEED=0 python3 links.py` (about 7 minutes; tell Kaptain and
wait for his OK; it writes links.sqlite.gz too). A step is redone when what it uses changes. A script marked "to write"
is written in that step's chat, from the rules of the step, and its line here is then filled in.

## Step 1. Fix the library's concepts
- Suspects: `factions/wheel/work/suspects.tsv` (concept, the games it is counted in, the games left out, where it
  was limited). `python3 ../../factions/wheel/work/concept_games.py [--all]` -> `work/concept_games.tsv` (`--all`:
  `concept_games_all.tsv`, every concept with 10+ cards): per concept and game, where its rows act (kind, side, zone),
  the keywords that give it, its link partners and how alike they are to the other games' (too noisy to decide alone;
  the rows decide). Verdicts: `work/suspect_verdicts.tsv`.
- Fixes: split by the card's rows in `flat.py` derive (ON_PLAYER, BODY, SEVERAL_SUPPLIES; the database's rules in
  `START_DATABASE.md`), each with cases (`cases/mechanics.tsv` wc01-wc24); tried on a copy of cards.sqlite with every
  case first; a card read (within the wheel's 500, low-cost model, Kaptain's OK first) only where its rows can't
  tell. Then the game limits went from the radius lists in `axes.py`, and `links.py` was rebuilt.

## Step 2. The radii and how they work together
- What: 23 radii (`SPOKES` in axes.py: key, name, the library concepts that count a card for it). A faction's value
  on a radius = its share of such cards / its game's average share (1 = average). 43 real factions of 8 games.
- `python3 axes.py` -> `axes.tsv`, `factions/wheel-axes.html`. How the values are made: `factions/13`.
- `python3 mechanics_wheel.py links --radii` -> `wheel/radius_links.tsv` (`axes.radius_links`): per pair of radii
  `cards`, `decks`, `games` (in how many games real cards link them), worked out per game and averaged (`cards`: games where chance gives 5+ linked
  pairs, 20+ in all; `decks`: games with 5+ decks holding both). A link counts for a radius only when the effect that
  made it, on that card's side, belongs to the radius (the links' `a_ab`/`b_ab`), for chance too. Checked by
  `cases/wheel.tsv`.

## Step 3. The 20 shapes
- `python3 ../../factions/wheel/work/shapes.py --write` (about 2 minutes) -> `factions/wheel/work/shapes.tsv` (letter
  A-T, radius=value list). Without `--write` it prints the 20, their real factions and the archetypes each carries.
- Candidates: every 3-6 of a real faction's radii valued 1.2+ whose radii are all joined (step 2), with that faction's
  values. Picking: a search over 20 candidates, at most one per real faction; misses of the rules count 100 each, and
  sameness (shared radii between two shapes, squared) decides the rest. Four fixed seeds, so every run gives the same.
  A shape's highest radius must give it an archetype; a radius fewer than 2 real factions are strong at (strength,
  defence) only has to stay under 5 shapes. It then prints the rules missed and the archetype concepts with under a
  quarter of their cards on that archetype's radii.
- The archetypes: `factions/wheel/archetypes.tsv` (key, what it is, its radii, its concepts).

## Step 4. The usable concepts
- `python3 ../../factions/wheel/work/concept_catch.py` (a second) -> `work/concepts.tsv`: every concept with 10+
  real cards, its card count (`card_count`), its games, its kind (usable, helper, out) and reason, the share of its cards on each
  radius (per game, averaged; strength and defence come from unit stats, so no share); a parent in
  `library/concept_tree.txt` keeps only the cards none of its children carry. Kinds and reasons: `work/concept_verdicts.tsv`
  (a concept not in it is usable); player_<concept> and a parent left with under 10 cards are out. `work/concepts.md`:
  the same by kind in plain words, for Kaptain.

## Step 5. The links between concepts
- `python3 mechanics_wheel.py links --concepts` (to write; the same count as `--radii`) -> `wheel/concept_links.tsv`:
  per pair of usable concepts and helpers `cards`, `decks`, `games`, which one makes and which one uses, the top link
  texts.
  `python3 apart.py` gives the pairs real factions keep apart.

## Step 6. The 20 groups
- `python3 factions/wheel/work/groups.py --write` (to write; an exact solver for all 20) -> `factions/wheel/work/groups.tsv`
  (faction, pillars, others, its mechanics with link texts and counts). `python3 tools/wheel_table_check.py` (to
  rewrite) checks the rules of the step from the files.
- `python3 ../../factions/wheel/work/concept_list.py` (to write) -> `factions/wheel/work/lists/<letter>.tsv`: per
  faction every usable concept and helper, by fit (step 6), with its links to the group (times chance, games).

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
