# The wheel pipeline: the commands of each step and what each makes
Commands run from `library/cards_db/` unless they start with `factions/` or `tools/`. The rules of each step are in
`factions/START_DESIGN-1-wheel.md`; this file says how each result is made. Before anything: `gunzip -kf links.sqlite.gz`.
After a change to `network.py` or `cards.sqlite`: `PYTHONHASHSEED=0 python3 links.py` (about 6 minutes, after `check_all.py` 14; tell Kaptain and
wait for his OK; it writes links.sqlite.gz too). A step is redone when what it uses changes. A script marked "to write"
is written in that step's chat, from the rules of the step, and its line here is then filled in.

## Step 1. Fix the library's concepts
- Suspects: `factions/wheel/work/suspects.tsv` (concept, the games it is counted in, the games left out, where it
  was limited). `python3 ../../factions/wheel/work/concept_games.py [--all]` -> `work/concept_games.tsv` (`--all`:
  `concept_games_all.tsv`, every concept with 5+ cards): per concept and game, where its rows act (kind, side, zone),
  the keywords that give it, its link partners and how alike they are to the other games' (too noisy to decide alone;
  the rows decide). Verdicts: `work/suspect_verdicts.tsv`.
- Fixes: split by the card's rows in `flat.py` derive (ON_PLAYER, BODY, SEVERAL_SUPPLIES; the database's rules in
  `START_DATABASE.md`), each with cases (`cases/mechanics.tsv` wc01-wc26); tried on a copy of cards.sqlite with every
  case first; a card read (within the wheel's 500, low-cost model, Kaptain's OK first) only where its rows can't
  tell. A game rule no card text says goes into `read/<game>/game_rules.jsonl` (`applies_to`; `kind_has` puts it only
  on the cards whose own rows name that kind, as Runeterra's spell mana).
- Tags: `python3 ../../factions/wheel/work/tag_check.py` (a second) -> `work/tag_cards.tsv` (every card of every
  suspect family, with its group); with `--reads` also `work/tag_groups.tsv` (per usable concept of
  `work/concepts.tsv`, its real cards grouped by what put the tag on: the row's table and action, test or event, whom it
  acts on (kind/side/pick, and to or by whose side), from where, when it fires, and the card or the keyword that gave it;
  or the keyword; or the general rule of `flat.py` and the row that set it off; with cards, games, suspect and why) and
  `work/tag_reads.tsv` (the reading: a family is one concept, one action or test and one reason; 5 of its cards spread
  over the games, with the group each came from; then the reader's verdict and one line why). `python3 ../../factions/wheel/work/tag_read_input.py`
  -> `work/reads/batch_NN.md` (the reader's inputs, about 20 cards each; low-cost model readers, 4 batches each) and
  the readers' `work/reads/batch_NN.verdicts.tsv` (card id, verdict, why). `work/tag_read_sum.py` -> `work/tag_verdicts.tsv` (per family: fix,
  stays or mixed). `work/tag_split.py` -> `work/tag_reads2.tsv`: each mixed family split by the one detail that best
  keeps the cards read right apart from those read wrong, 5 cards per half (the ones read keep their verdict); its new
  cards read the same way (`tag_read_input.py tag_reads2.tsv round2` -> `work/reads/round2_NN.md` and their verdicts). The reasons are in its
  `checks`: a good action on an enemy or a bad one on my side for a concept the concept tree puts under helps_me or
  hurts_enemy, a thing put on the enemy side, a trigger of mine firing on the enemy's action, and the rows that match
  what a concept's definition gives to another concept. Fixes go into `flat.py` derive with cases in
  `cases/mechanics.tsv`. Then `check_all.py` and `links.py`.
- Return my unit to hand: `flat.py` derive gives my unit's return its smaller concept by its rows (return_on_leave when
  the ability fires as it dies or leaves play, return_from_board from the board); cases wc40-wc43.

## Step 2. The usable concepts
- `python3 ../../factions/wheel/work/concept_catch.py` (a second) -> `work/concepts.tsv`: every concept with 5+
  real cards, its card count (`card_count`), its games, its kind (usable, helper, out) and reason; a parent in
  `library/concept_tree.txt` keeps only the cards none of its children carry. Kinds and reasons:
  `work/concept_verdicts.tsv` (a concept not in it is usable); player_<concept> and a parent left with under 5 cards
  are out. `work/concepts.md`: the same by kind in plain words, for Kaptain.

## Step 3. The faction archetypes
- `python3 ../../factions/wheel/work/faction_archetypes.py` (to write; uses `axes.py`'s real factions and concept
  instances) -> `factions/wheel/work/faction_strong.tsv` (real faction, its strong concepts, their value against its
  game's average) and `factions/wheel/archetypes.tsv` (archetype key, name, the real factions of its group, the part in
  plain words, the usable concepts that can do it; engine or brick is filled by step 6).
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
- `python3 ../../factions/wheel/work/archetype_map.py` (about 10 seconds; needs links.sqlite) ->
  `factions/wheel/work/archetype_map.tsv` (archetype, its two engine parts, concept a, concept b, `cards`, `decks`,
  `games`, `level`, top link text, the real card pair of its strongest link, from `wheel/concept_links.tsv`; a pair
  joined only by real decks has no card pair; `note`: "about the player" when more than half of its card links are about
  hitting the player, "decks only" when no card pair; it prints the cards behind the most edges), `work/archetype_gaps.tsv` (two engine parts with no joined edge, shown to
  Kaptain with the numbers) and `factions/wheel-archetypes.html` (page template `work/archetype_map_template.html`; the concepts' places by
  networkx's spring layout over every joined pair of usable concepts, seed 7). It writes engine or brick for each part
  into `archetypes.tsv`.

## Step 7. The 20 factions
- `python3 ../../factions/wheel/work/factions.py` (rules: `START_DESIGN-1-wheel.md` step 7) ->
  `factions/wheel/work/factions.tsv` (faction letter, its 2 archetypes, its concepts per part, its synergies, its
  main radius, its theme, its extras, the way or concept for each of its seven answers, its blind spot radius). It
  prints the 20 groups with their scores and the weakest; the run stops after 7.2 for Kaptain's OK of the archetypes,
  then goes on with the themes written into `factions/wheel/work/themes.tsv` (faction letter, theme).
- `python3 ../../factions/wheel/work/concept_list.py` -> `factions/wheel/work/lists/<letter>.tsv`: per faction every
  concept with 5+ cards except the faction's own concepts, its score ((real + 1) / (chance + 1) links with the
  faction's concepts per game, averaged over the games where both appear), its `level` and its games, sorted by score.
- `factions/wheel/work/answer_concepts.tsv` (agreed with Kaptain): per answer its ways (answer, the way in plain words,
  its concepts: one, two that real cards link with their times chance and games, or removals on a spell; whose).

## Step 8. Combos on this board
- A script counts the joins between every two factions' concepts (own concepts and extras; step 5 numbers); Claude rates
  the pairs on the board -> `factions/wheel/combos.tsv` (pair, STRONG/OK/WEAK/NONE/AGAINST, how it plays, the numbers,
  a test column). Every faction needs 7+ partners. The same script lists per pair the deck archetypes
  (`factions/wheel/deck_archetypes.tsv`: their parts and the concepts that can do each) the two factions can play
  together -> `factions/wheel/deck_pairs.tsv`.
- Once, before the first run of step 8 (then this line goes): the concepts of each deck archetype part are checked
  against the parts' job, each concept by its definition in `library/concept_tree.txt`; Claude's changes are shown to
  Kaptain. Found so far: "Return my unit to hand" in 5 discard-pile parts (Toolbox, Reanimator, Self-Mill, Recursion,
  Turbo-Fog); "Copy" in Blink, Storm and Turbo-Fog; "Put into play for free" in Discover; "Cards cost less" in Blink and
  Recursion; Self-Mill, Reanimator and Recursion, Madness and Wheels, Aristocrats and Eggs, Stompy and Voltron, Control,
  Midrange and Toolbox nearly the same concepts; Combo, Control-Combo and Extra Turns parts go.

## Step 9. Game plan, then keywords
- Claude -> `factions/wheel/plans.tsv` (faction, its game plan turn by turn on the board).
- Claude -> `factions/wheel/keywords.tsv` (keyword, its rule, the synergy it grows from, its source card pairs, the
  factions that carry it and how much, own or shared, NEW RULE). A script checks the keyword rules of step 9.

## Step 10. Stop 1
- Claude -> `factions/wheel/answers.tsv`, from the game plan and keywords. `python3 tools/wheel_table_check.py`
  (against each faction's archetypes, extras and answers). `python3 factions/wheel/work/make_stop1.py` writes `STOP1.md`
  and `STOP1-1..5.md`.
