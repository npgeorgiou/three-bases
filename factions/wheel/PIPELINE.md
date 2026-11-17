# The wheel pipeline: the commands of each step and what each makes
Commands run from `library/cards_db/` unless they start with `factions/` or `tools/`. The rules of each step are in
`factions/START_DESIGN-1-wheel.md`; this file says how each result is made. Before anything: `gunzip -kf links.sqlite.gz`.
After a change to `network.py` or `cards.sqlite`: `PYTHONHASHSEED=0 python3 links.py` (about 6 minutes, after `check_all.py` 14; tell Kaptain and
wait for his OK; it writes links.sqlite.gz too). A step is redone when what it uses changes. A script marked "to write"
is written in that step's chat, from the rules of the step, and its line here is then filled in.

## Step 1. Fix the library's concepts
- Suspects: `factions/wheel/work/suspects.tsv` (concept, the games it is counted in, the games left out, where it
  was limited). `python3 ../../factions/wheel/work/concept_games.py [--all]` -> `work/concept_games.tsv` (`--all`:
  `concept_games_all.tsv`, every concept with 10+ cards): per concept and game, where its rows act (kind, side, zone),
  the keywords that give it, its link partners and how alike they are to the other games' (too noisy to decide alone;
  the rows decide). Verdicts: `work/suspect_verdicts.tsv`.
- Fixes: split by the card's rows in `flat.py` derive (ON_PLAYER, BODY, SEVERAL_SUPPLIES; the database's rules in
  `START_DATABASE.md`), each with cases (`cases/mechanics.tsv` wc01-wc26); tried on a copy of cards.sqlite with every
  case first; a card read (within the wheel's 500, low-cost model, Kaptain's OK first) only where its rows can't
  tell. A game rule no card text says goes into `read/<game>/game_rules.jsonl` (`applies_to`; `kind_has` puts it only
  on the cards whose own rows name that kind, as Runeterra's spell mana). Then `check_all.py <game>` and `links.py`.

## Step 2. The usable concepts
- `python3 ../../factions/wheel/work/concept_catch.py` (a second) -> `work/concepts.tsv`: every concept with 10+
  real cards, its card count (`card_count`), its games, its kind (usable, helper, out) and reason; a parent in
  `library/concept_tree.txt` keeps only the cards none of its children carry. Kinds and reasons:
  `work/concept_verdicts.tsv` (a concept not in it is usable); player_<concept> and a parent left with under 10 cards
  are out. `work/concepts.md`: the same by kind in plain words, for Kaptain.

## Step 3. The archetypes
- Claude -> `factions/wheel/archetypes.tsv`: one line per part of each archetype of `archetypes_kaptain.txt` that
  can exist here (archetype key, its name in Kaptain's list, what it is in this game, the part
  in plain words, engine or brick, the usable concepts that can do it).
- `python3 work/archetypes_plain.py` -> `factions/wheel/archetypes.md`: the same in plain words, for Kaptain's OK.

## Step 4. The radii and how they work together
- `work/radii.tsv`: every usable concept, the radius it goes on (key and name), the part of it that counts there, and
  whose decision it is; helpers kept off the radii; the radii measured from the units' numbers. `axes.py` builds
  `SPOKES` from it (a concept on two radii counts as concept@radius, each instance where its rows put it: PART).
  A faction's value on a radius = its share of concept instances on the radius / its game's average share (1 =
  average). 43 real factions of 8 games. About 30 seconds.
- `python3 axes.py` -> `axes.tsv`, `factions/wheel-axes.html`. How the values are made: `factions/13`.
- `python3 mechanics_wheel.py links --radii` (about 30 seconds) -> `wheel/radius_links.tsv` (`axes.radius_links`): per
  pair of radii `cards`, `decks`, `games` (in how many games real cards link them), `level` (the linked pairs: 1 = 1, 10 = 2, 100+ =
  3), worked out per game and averaged (`cards`: games where chance gives 5+ linked pairs, 20+ in all; `decks`: games
  with 5+ decks holding both). A link counts for a radius only when the effect that made it, on that card's side,
  belongs to the radius (the links' `a_ab`/`b_ab`), for chance too. Checked by `cases/wheel.tsv`.

## Step 5. The links between concepts
- `python3 mechanics_wheel.py links --concepts` (about a minute; the same count as `--radii`, every game including
  those with no factions) -> `wheel/concept_links.tsv`: per pair of concepts of `work/concepts.tsv` that real cards or
  decks link: `cards`, `decks`, `games`, `level`, `rare`, `makes`, the top three link texts. `python3 apart.py` gives
  the pairs real factions keep apart.

## Step 6. The archetype map
- `python3 ../../factions/wheel/work/archetype_map.py` (to write) -> `factions/wheel/work/archetype_map.tsv` (archetype,
  concept a, concept b, `cards`, `games`, `level`, top link text, one real card pair, from `wheel/concept_links.tsv`)
  and `factions/wheel-archetypes.html` (the nodes and edges, one archetype or all).

## Step 7. The 20 factions and their lists
- `python3 ../../factions/wheel/work/factions.py` (to write, after Kaptain agrees its rules) ->
  `factions/wheel/work/factions.tsv` (faction letter, its archetypes, their concepts, its mechanics).
- `python3 ../../factions/wheel/work/concept_list.py` (to write) -> `factions/wheel/work/lists/<letter>.tsv`: per
  faction every concept with 10+ cards and its score ((real + 1) / (chance + 1) links with the concepts of its
  archetypes per game, averaged over the games where both appear), its `level` and its games, sorted by score.

## Step 8. Theme, then tools
- Claude -> `factions/wheel/themes.tsv` (faction, theme) and `factions/wheel/tools.tsv` (faction, tool, mechanic, the
  tools it feeds, the cell-by-cell line, source: a library card or CLAUDE, NEW RULE).

## Step 9. Combos on this board
- A script (to write) counts the joins between the concepts of every two factions' archetypes (step 5 numbers); Claude rates the pairs on the board
  -> `factions/wheel/combos.tsv` (pair, STRONG/OK/WEAK/NONE/AGAINST, how it plays, the numbers, a test column).

## Step 10. The seven answers and Stop 1
- Claude -> `factions/wheel/answers.tsv`, from the tools. `python3 tools/wheel_table_check.py` checks steps 4-10,
  including words that break this game's rules. `python3 factions/wheel/work/make_stop1.py` (to rewrite) writes
  `STOP1.md` and `STOP1-1..5.md`.
