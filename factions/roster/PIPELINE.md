# The roster pipeline: the commands of each step and what each makes
Commands run from `library/cards_db/` unless they start with `factions/` or `tools/`. The rules of each step are in
`factions/START_DESIGN-1-roster.md`; this file says how each result is made. Before anything: `gunzip -kf links.sqlite.gz`.
After a change to records, `vocab.tsv` or `flat.py`: `python3 check_all.py <any game>` (about 14 minutes; with no game it
reloads nothing), then `PYTHONHASHSEED=0 python3 links.py` (about 6; after `network.py` alone, links.py only); tell Kaptain and
wait for his OK; it writes links.sqlite.gz too). A step is redone when what it uses changes. A script marked "to write"
is written in that step's chat, from the rules of the step, and its line here is then filled in.

## Step 1. Fix the library's concepts
- Suspects: `factions/roster/work/suspects.tsv` (concept, the games it is counted in, the games left out). `python3 ../../factions/roster/work/concept_games.py [--all]` -> `work/concept_games.tsv` (`--all`:
  `concept_games_all.tsv`, every concept with 5+ cards): per concept and game, where its rows act (kind, side, zone),
  the keywords that give it, its link partners and how alike they are to the other games' (too noisy to decide alone;
  the rows decide).
- Fixes: split by the card's rows in `flat.py` derive (ON_PLAYER, BODY, SEVERAL_SUPPLIES; the database's rules in
  `START_DATABASE.md`), each with cases (`cases/mechanics.tsv` wc01-wc26); tried on a copy of cards.sqlite with every
  case first; a card read (within the roster's 500, low-cost model, Kaptain's OK first) only where its rows can't
  tell. A game rule no card text says goes into `read/<game>/game_rules.jsonl` (`applies_to`; `kind_has` puts it only
  on the cards whose own rows name that kind, as Runeterra's spell mana).
- Tags: `python3 ../../factions/roster/work/tag_check.py` (a second) -> `work/tag_cards.tsv` (every card of every
  suspect family, with its group); with `--reads` also `work/tag_groups.tsv` (per usable concept of
  `work/concepts.tsv`, its real cards grouped by what put the tag on: the row's table and action, test or event, whom it
  acts on (kind/side/pick, and to or by whose side), from where, when it fires, and the card or the keyword that gave it;
  or the keyword; or the general rule of `flat.py` and the row that set it off; with cards, games, suspect and why) and
  `work/tag_reads.tsv` (the reading: a family is one concept, one action or test and one reason; 5 of its cards spread
  over the games, with the group each came from; then the reader's verdict and one line why). `python3 ../../factions/roster/work/tag_read_input.py`
  -> `work/reads/batch_NN.md` (the reader's inputs, about 20 cards each; low-cost model readers, 4 batches each) and
  the readers' `work/reads/batch_NN.verdicts.tsv` (card id, verdict, why). `work/tag_read_sum.py` -> `work/tag_verdicts.tsv` (per family: fix,
  stays or mixed). `work/tag_split.py` -> `work/tag_reads2.tsv`: each mixed family split by the one detail that best
  keeps the cards read right apart from those read wrong, 5 cards per half (the ones read keep their verdict); its new
  cards read the same way (`tag_read_input.py tag_reads2.tsv round2` -> `work/reads/round2_NN.md` and their verdicts). The reasons are in its
  `checks`: a good action on an enemy or a bad one on my side for a concept the concept tree puts under helps_me or
  hurts_enemy, a thing put on the enemy side, a trigger of mine firing on the enemy's action, and the rows that match
  what a concept's definition gives to another concept. Fixes go into `flat.py` derive with cases in
  `cases/mechanics.tsv`. Then `check_all.py <any game>` and `links.py`.
- Return my unit to hand: `flat.py` derive gives my unit's return its smaller concept by its rows (return_on_leave when
  the ability fires as it dies or leaves play, return_from_board from the board); cases wc40-wc43.

## Step 2. The usable concepts
- `python3 ../../factions/roster/work/concept_catch.py` (a second) -> `work/concepts.tsv`: every concept with 5+
  real cards, its card count (`card_count`), its games, its kind (usable, helper, out) and reason; a parent in
  `library/concept_tree.txt` keeps only the cards none of its children carry. Kinds and reasons:
  `work/concept_verdicts.tsv` (a concept not in it is usable); player_<concept> and a parent left with under 5 cards
  are out. `work/concepts.md`: the same by kind in plain words, for Kaptain.

## Step 3. The real decks' scores
- `python3 ../../factions/roster/work/deck_scores.py` (from `library/cards_db`, a few seconds) -> `work/deck_scores.json`:
  every real deck's cards per concept, the concepts it is built on (score 1.96+) and its design markers; every real
  faction's cards per concept; every game's cards per concept. Read by step 6, `make_faction.py` and the map.
- `python3 factions/roster/work/make_faction.py ...` (from the repo): one faction from concepts Kaptain gives, the way
  step 6 makes them (its header and `--help` say how).

## Step 4. The links between concepts
- `python3 roster_links.py links --concepts` (about a minute; every game, those with no factions too) ->
  `roster/concept_links.tsv` (`concept_tags.pair_links`): per pair of concepts of `work/concepts.tsv` that real cards or
  decks link: `cards`, `decks`, `games` (in how many games real cards link them), `level` (the linked pairs: 1 = 1,
  10 = 2, 100+ = 3), worked out per game and averaged (`cards`: games where chance gives 5+ linked pairs, 20+ in all;
  `decks`: games with 5+ decks holding both); `rare`, `makes`, the top three link texts. A link counts for a concept
  only when the effect that made it, on that card's side, gives the concept (the links' `a_ab`/`b_ab`), for chance
  too. Checked by `cases/roster.tsv`. `python3 apart.py` gives
  the pairs real factions keep apart.

## Step 5. The map
- `python3 ../../factions/roster/work/roster_map.py` (from `library/cards_db`, about 20 seconds; after step 6) ->
  `factions/roster-map.html` (page template `work/roster_map_template.html`). `roster_map.card_pairs(pairs)` gives the
  real card pair behind any concept pair.

## Step 6. The factions, from what they do
- `python3 factions/roster/work/kernel_factions.py` (from the repo, about a minute; needs links.sqlite) ->
  `factions/roster/work/kernel_factions.md` (for Kaptain: one sheet per faction, plain names, no numbers),
  `kernel_factions_check.md` (every number and where each concept came from), `kernel_factions_summary.json` (the numbers that compare
  ways of making them), `kernel_factions.tsv`
  (`ROSTER_VARIANT=B` or `C` makes the factions another way, into files ending in `_B` or `_C`: B keeps the kernel to
  the identity's core and reads the answers off what the fill brings; C ranks the fill by fit to the core only) (one row per faction: letter, name,
  what it does, theme, kernel, engines, bricks, concepts, extras, design markers, how it wins, the five board answers,
  partners; read by steps 7-9) and `lists/<letter>.tsv` (rules: `START_DESIGN-1-roster.md` step 6). The identities are
  `IDENTITIES` in its head (name, what it does, concept-tree families) and the themes `THEMES` (theme, the families it
  favours in a tie); both Claude's. Per faction: its kernel with the decks leaning on each concept, its engines with
  their kernel links and the real card pair behind the strongest, its bricks with how many times as often its decks
  hold each, what its decks hold that real cards also link to its concepts (a faction still short of 12), its design
  markers, its extras with their list scores, its answers, its partners with their strength and how each plays; then
  every pair. It reads `work/deck_scores.json` (decks and their design markers),
  `library/cards_db/roster/concept_links.tsv` (strong links, their games), `library/concept_tree.txt` (families),
  `work/concepts.tsv` (usable) and `work/answer_concepts.tsv` (the ways of each answer).
- `python3 ../../factions/roster/work/concept_list.py` (from `library/cards_db`) -> `factions/roster/work/lists/<letter>.tsv`
  for every faction of `kernel_factions.tsv`: every concept with 5+ cards except the faction's own concepts, its score
  ((real + 1) / (chance + 1) links with the faction's concepts per game, averaged over the games where both appear), its
  `level` and its games, sorted by score. Its `Library` scores any set of concepts in about a second.
- `factions/roster/work/answer_concepts.tsv` (agreed with Kaptain): per answer its ways (answer, the way in plain words,
  its concepts: one, two that real cards link with their times chance and games, or removals on a spell; whose).

## Step 7. Combos on this board
- Claude rates every two partners on the board -> `factions/roster/combos.tsv` (pair, STRONG/OK/WEAK/NONE/AGAINST, how
  it plays, the numbers from step 6, a test column). Every faction needs 7+ partners rated STRONG or OK (5 among the
  10 of the trial).

## Step 8. Game plan, then keywords
- Claude -> `factions/roster/plans.tsv` (faction, its game plan turn by turn on the board).
- Claude -> `factions/roster/keywords.tsv` (keyword, its rule, the synergy it grows from, its source card pairs, the
  factions that carry it and how much, own or shared, NEW RULE). A script checks the keyword rules of step 8.

## Step 9. Stop 1
- Claude -> `factions/roster/answers.tsv`, from the game plan and keywords. `python3 tools/roster_table_check.py`
  (against each faction's concepts, extras and answers). `python3 factions/roster/work/make_stop1.py` writes `STOP1.md`
  and `STOP1-1..5.md`.
