# Three Bases inspiration library

## What it is
A SQLite database of game mechanics from 24 other games, built for Three Bases design questions: faction ideas, alternatives to a mechanic, cards that work with a concept or with other cards, and fixes for design problems. It holds mechanics only: names and wording are never reused in Three Bases.

It lives in the `library/` folder of **github.com/npgeorgiou/three-bases**: `three-bases-library.sqlite`, `tools/` (query and build scripts, data files), this README and `SEARCH_GUIDE.md` (how to search and read results).

## Contents
61,266 entries (cards, units, locations, abilities, items, rules), 1,261 keywords and 655 card types/tribes. Entries that repeat a mechanic within one faction are merged, so the counts are distinct mechanics, not printed cards.

| Game | Entries |
|---|---|
| Magic: The Gathering | 18,933 |
| Hearthstone | 8,058 |
| Shadowverse | 4,386 |
| Warhammer 40,000 (10th edition) | 3,813 |
| Warhammer Age of Sigmar (4th edition) | 3,540 |
| Warhammer Underworlds | 3,217 |
| Legends of Runeterra | 2,434 |
| Hearthstone Battlegrounds | 2,239 |
| Warhammer 40,000: Kill Team | 2,219 |
| Star Wars: Unlimited | 1,813 |
| Disney Lorcana | 1,788 |
| Slay the Spire 2 (Early Access) | 1,386 |
| Gwent (standalone) | 1,357 |
| Darkest Dungeon | 949 |
| Marvel Snap (699 cards, 212 locations, 6 rules) | 917 |
| Slay the Spire | 895 |
| The Elder Scrolls: Legends | 850 |
| Duelyst | 786 |
| Faeria | 443 |
| Into the Breach | 287 |
| Monster Train | 272 |
| Inscryption | 263 |
| Blood Bowl (Third Season) | 243 |
| Stormbound | 190 |

What is in, beyond the cards each source lists as playable:
- **Created cards** (edition `non-collectible`; a name already used gets " (created)"): Runeterra (levelled champions, champion spells, tokens), Hearthstone (tokens, generated cards, rewards), Battlegrounds, Gwent and Shadowverse tokens, Magic tokens and emblems that have rules text, Slay the Spire's created cards (Shiv, Miracle, Smite, ...). Cards link to what they create (`generates`; for Magic from Scryfall's list of related tokens).
- **Slay the Spire 1 and 2 upgrades:** an upgrade that changes only numbers is kept on its base card (`extra.upgraded_text`, `extra.upgraded_cost`); an upgrade that changes the mechanic (Innate or Retain added, Exhaust dropped, all cards instead of one, ...) is its own entry `<name>+`, linked `variant_of` to the base card, and carries the base card's hand-review decisions. Slay the Spire 2: 69 such entries and 412 number-only upgrades; its upgraded costs are unknown (the source lists no costs).
- **Warhammer unit datasheets:** units and Kill Team operatives from the current BSData repos that the library lacked (40k 4, Kill Team 63, Age of Sigmar 32), with their stat line (`stats`; other models' lines in `extra.model_stats`) and abilities, weapon abilities and special rules as text; and stat lines for 29 older units that had none. As in the first build, a unit without any ability (Kill Team: without an ability of its own) is left out, and so are Kill Team fire teams, which only group operatives.
- **Magic:** the cards of the first build (no commons, no Commander-only cards, no near-duplicates) plus 640 cards from MTGJSON that bring a mechanic the others lack. The other 10,560 MTGJSON cards repeated existing mechanics and were left out, so Magic does not drown the smaller games.
- **Warhammer factions** are armies: a BSData "Library" file's entries belong to the army that uses it, and an Age of Sigmar army of renown or Legends list belongs to its army (`extra.army_of_renown`, `extra.legends`).

## Structure
**entities**: every card, unit, spell, item, location, ability, rule, keyword (its definition as text) and tribe, with game, category, faction, cost, stats and rules text. `variants` lists other names the same mechanic was printed under; **merged_entities** maps each merged name to the entry that kept it, so commands still find it. Keywords no card text uses are dropped; one that later loses its last card is marked with `extra.note` "used by no card text in this library".

**concepts**: Claude's cross-game network of 293 design concepts (tree v3; the readable tree, every move and its reason are in `CONCEPT_TREE.md`). Effects answer first **who it helps or hurts**: helps my side, hurts the enemy, hurts my side (drawback), neutral game rules. A concept has a second parent only when it is always a kind of both (lifesteal: heal and damage). For example, "no damage output" holds can't attack (attack lock), attack set to 0 and damage prevention. It sits under "suppress" (hurts the enemy), next to can't block, immobilize, silence and total disable (stun, freeze). "Make a unit stronger" (buff) holds stat gain and the combat bonuses; "make a unit weaker" (debuff) holds stat loss and penalties. "This turn / round only" is a separate marker. Every definition says what counts, what doesn't and where it goes instead, with two cards that fit and one look-alike that doesn't (`tools/concept_tree_v3.txt`, `tools/concept_examples.tsv`; the build step `tools/concept_tree.py` moves the older steps' tags to the tree). The view `concept_tree` gives all descendants. **Parent and child rule** (every game): an entry keeps only the narrowest concepts of a branch (ping, not also damage), in its tags and its trigger pairs (`tools/parent_rule.py`); every query command finds the parent through `concept_tree`. Definitions and parents, with the wording patterns that feed them, are in `tools/concept_defs.py`.

**entity_concepts**: links each entry to its concepts with a role (does, grants, benefits, counters, cost; exhibits for design problems) and the method that made the link (reliability order in SEARCH_GUIDE). A card that gives a keyword to others has that keyword's concepts as `grants`, not `does`.

**concept_relations**: 478 relations (synergizes, enables, counters, mitigates, tension, variant_of), Claude's analysis. Every design problem is linked to the mechanics that ease or worsen it, including five from Three Bases playtests: p_objective_stalemate (dot-holding stalemates), p_resource_hoarding (carry-over hoarding), p_front_pileup (units piling into the front row), p_draw_engine (card-draw engines) and p_holder_snowball (the base holder snowballing). `anti_stalemate` (stalemates and board locks, and what breaks them) is a design problem too.

**entity_links**:
- **Keyword links:** has (the card's own keyword), grants (given to others: "creatures you control have flying"), mentions (only named: "creatures with flying"), describes (the text describes a keyword's mechanic in other words, Claude's reading).
- **Type links:** has_type, cares_about_type.
- **Name links:** references (names another card; for Magic also Scryfall's related cards), summons, generates (creates another card), transforms_into (a champion's level-up).
- **variant_of:** the same mechanic in another faction, and a Slay the Spire upgrade to its base card.
- **equivalent_keyword:** the same keyword in another game.

**Text positions**: tag evidence and pair clauses are stored as positions in the entry's own text (`ev_form/ev_pos/ev_len`, `cl_form/cl_pos/cl_len`; form 0 the stored text, 1 the text as patterns read it, 2 a note in `text_notes`). `tools/compact_text.py` explains the forms and cuts the text back out (`evidence_text`, `clause_text`); the build expands them first and compacts them last.

**trigger_effect**: about 82,500 "when X, do Y" pairs, from every clause of every entry and from the entry's keywords. Each pair has a **frequency** limit and its basis:
- **per_card:** a spell, a Place/on-play effect, the card's own death, or once per game.
- **per_round:** a once-per-turn cap, or the card's own turn start/end, attack, kill or tap ability.
- **unbounded:** fires on other units' events or on repeated events.
- **static:** an aura, not a trigger.

**faction_signature**: which mechanics are prominent in which faction (`tools/signature.py`). One rule for every game, concept and archetype: a faction's mechanic is prominent when (1) its share of the faction's cards is at least 1.5 times the share among all the game's other cards, and (2) that difference is not chance (a faction of this size drawn at random from the game would have this many with probability under 5%: a one-sided Fisher exact test). A card of a combined faction (Lorcana Amber-Steel, Legends and Star Wars Unlimited pairs, Gwent "Syndicate / X", Magic "Multicolor (BR)") counts for each of its factions; factions under 20 cards are left out.
- **signature mechanics:** prominent, and the faction is one of the two with the highest share. Share and lift (share over the game average) are stored for reading.
- **keyword signatures** (`kw:<keyword>`): a keyword whose cards are 60%+ that faction's (8+ cards);
- **splash:** every other faction that uses a signature mechanic, sorted by share.

**factions / archetypes / faction_archetypes**: every faction with its size and concept profile (concepts on 3+ of its entries and 5%+ of them, top 12 by lift), and 20 cross-game archetypes (swarm, sacrifice, graveyard, control, burn, aggro/tempo, scaling, fortress, sustain, spellslinger, ramp, positional, disruption, trickery, chaos, card advantage, tribal, objectives, damage over time, transformation), each a fixed bundle of concepts; a faction has an archetype when the bundle is prominent in it by the same rule as signatures. All rebuilt from the current tags on every build.

**mechanic_repeat**: an entry whose category, concepts and trigger pairs are exactly those of an earlier entry of the same game (usually the same mechanic in other numbers). Nothing is removed; `concept` and `search` take `distinct=1` to skip these.

**concept_precision**: per concept and game, how often the current wording patterns are right on the entries the hand reviews checked (a reviewed wrong tag counts only while a pattern would still make it). `concept` warns where this is below 70%.

**entity_fts**: full-text search. It and the search indexes are not stored in the file (about 21 MB): `tools/indexes.py` says how the build and `query.py` rebuild them. **games**, **load_log**: what each game is and how it was loaded.

## How Claude uses it
In a fresh chat, Claude clones the repository and runs `python3 library/tools/query.py <command>` (the script finds the database next to `tools/`; `TB_LIB` overrides). The commands and the rules for reading results are in SEARCH_GUIDE.md. The database never enters the conversation, only printed results do, so a design question costs a few short queries.

## Maintenance
**The build** is one chain: `sh tools/build.sh three-bases-library.sqlite <scratch>/new.sqlite` (about 10 minutes; one build at a
time, two writers corrupt the scratch database). It starts from the frozen base tagging (`base_tags`, `base_pairs`,
`base_patterns`, made once by `tools/make_base.py`), the card data and the record files, so its output never depends on an earlier
build. Every build writes `<out>.steps.tsv` (what each step removed, `step_log.py`). The stored file is compact (`compact_text.py`)
and without its indexes (`indexes.py`); copy a checked build over `three-bases-library.sqlite`, then commit and push.

**Where tags come from**, and where to fix them:
- general wording patterns (all games), applied once when an entry is loaded;
- the game's own patterns, `tools/patterns/<game>.txt` (`concept|role|regex` adds one, `!concept|pattern` switches a general
  pattern off for that game);
- `tools/step3/decisions.tsv`: narrowed patterns and new ones, applied by `pattern_fix.py` to the games listed for it in
  `tools/step_games.json`. Its `|key` lines are written by `tools/step3/key_patterns.py`, which turns the answer key's quoted words
  into patterns and keeps one only if it is 90%+ right on the key half it was not made from and on the whole key; a phrase that is
  only a keyword name matches only where the game prints keywords. It rewrites only the games it is given
  (`key_patterns.py <db> <game> ...`); re-run it for a game whose key or patterns change;
- the hand reviews (`tools/reviews/<game>.json`, then `regression.py <db> make`) and the keyword reviews against the outcome tree
  (`tools/reviews_outcome/<game>.json`); where a review and the answer key disagree on what a card does, the key wins (`key_wins.py`);
- keyword inheritance, outcome concepts, link rules and trigger pairs, re-derived on every build. Text is read lower-cased with the
  entry's own name as "name"; Magic without reminder text. Entries that no pattern or keyword reaches are dropped.

**Add or reload a game:** `ADDING_GAMES.md` (converter in `tools/convert/`, load format in `tools/load_cards.py`,
`build.sh <in> <out> <game>=<cards.json>`; `tools/reload_game.sh <scratch> <game>` reloads a game keeping its ids).

**The build stops** if any of these fails: the regression set (`regression.py <db> check`, the reviewed tags), the combo set
(`combo_check.py`, 82 enabler -> payoff pairs, 2 known misses), trigger coverage (`trigger_pairs.py <db> check`, 50%+ of entries with
a trigger in every game) and the query tests (`test_query.py`, all 16 commands).

**After every change**, compare the build with the stored library and keep it only if nothing is worse:
`python3 tools/compare_builds.py three-bases-library.sqlite <scratch>/new.sqlite <scratch>/cmp`. Per game it prints the answer-key
wrong and missed tags per 100 entries and the real-world cases met per kind (signature, archetype, combo, splash; cases in
`tools/realworld/<game>.tsv`, made from the source summaries `<game>.md` as `tools/realworld/RESEARCH.md` says); then the regression set, the combos, the real-world cases newly met or missed, and the trigger ->
effect pairs lost (`lost_pairs.py`). Why a case misses: `realworld_why.py <db>`. A game's new wrong key tags: `keydiff.py`.
Against the original library (`git show c7a77a4:library/three-bases-library.sqlite`): `final_compare.py <orig> <new> check`.

**Sources** of the card data (converter in brackets):
- Disney Lorcana (20 Oct 2026): LorcanaJSON as bundled in the npm package lorcana-oracle 0.1.2, sets 1-12 (12 incomplete) and Illumineer's Quest [conv_lorcana.py]; keywords from the source's keyword field, definitions from the reminder text, keyword concepts in `reviews/lorcana.json`; 264 vanilla characters (no text) dropped, 248 repeats merged.
- Star Wars: Unlimited (20 Oct 2026): sets/*.json of github.com/Yannick101984/swucardex-data (commit a86faed), an export of the official card database: SOR to ASH and Intro Battle: Hoth [conv_swu.py]; English text from its localisations; keyword names (French in the export) matched to the English word on every card that has them; trait names translated by Claude.
- The Elder Scrolls: Legends (20 Oct 2026): database/dbCards.json and dbTokens.json of github.com/edipo2s/TESLegendsTracker (commit c541e82, Apr 2018) [conv_tesl.py]: sets up to Houses of Morrowind, later sets missing; keyword definitions are Claude's summaries.
- Monster Train (20 Oct 2026): the fandom wiki's Module:Cards/Data, read through Kaptain's Chrome and flattened to one line per card (kept as `tools/convert/monster_train_cards.psv`, since the wiki is reachable only through a browser); keywords from the wiki tags, no keyword definitions.
- Stormbound (20 Oct 2026): github.com/Stormbound-Games/stormbound-kitty src/data/cards.json at commit 96a86726 (28 Feb 2022, the last commit that kept the card list) [conv_stormbound.py]; cards added after that date are missing; no keyword list in the source.
- Magic: MTGJSON AtomicCards.json [conv_mtg.py] for the 640 cards with a new mechanic; Scryfall Oracle Cards [conv_scryfall_tokens.py, fixes/f02] for tokens, emblems, set names, related cards and keyword lists.
- Slay the Spire 1: the wiki's Module:Cards/data [conv_sts.py].
- Slay the Spire 2: the wiki's card lists, normal and upgraded, supplied by Kaptain on 12 Oct 2026 [conv_sts2.py]: upgrades, and 46 cards the library lacked.
- Gwent: the gwent.one v14.8 export, NonOwnable set [conv_gwent.py].
- Shadowverse: the Portal card API export, set 90000 [conv_sv.py].
- Underworlds: yawudb's db.js, github.com/PompolutZ/yawudb [conv_wu.py].
- 40k, Kill Team, Age of Sigmar: the BSData repos at their current state [conv_bs.py]: abilities and rules whose text the library lacked; campaign content (Crusade, Path to Glory, hero creation) left out. Unit datasheets and missing stat lines [conv_bs_units.py].

## Known limits
- Automatic tags on long prose (Warhammer army rules, Inscryption and Into the Breach wiki text) are the least precise. Five concept/game cells are below 70% (Hearthstone hand_disruption, adjacency and debuff; Kill Team information; Shadowverse tutor): their right and wrong tags come from the same wording, so `concept` warns there.
- Combo detection finds candidates through concepts, keywords and trigger links; confirming a combo means reading both cards.
- Frequency limits and trigger pairs come from wording rules, not play; real counts come from the Three Bases simulator.
- Warhammer entries loaded on 12 Oct 2026 come from the current BSData data, which can differ from the older snapshot of the first build. Units still without a stat line: 40k 46, Kill Team 83 (no single matching stat profile in BSData).
- Missing data: Underworlds fighter stat lines. The three stat files Kaptain supplied on 12 Oct 2026 were not loaded: most rows are a repeated template ("Leader", "Minion A", "Melee Weapon" with the same numbers for every warband), and on the fighters they share the files disagree (32 fighter states conflict, 11 agree). Also missing: about 25 dropped entries of Duelyst, Darkest Dungeon, Inscryption and Into the Breach (not reloaded).
- About 280 Magic token links are left out: Scryfall lists a related token whose name and type several tokens share, and the card's text does not say which one.
- Some faction-signature mechanics are generic for factions whose own keyword maps to a concept every faction uses (Magic Black's Fear = evasion); the keyword signature shows them.

## Improving the library: the open work, in order
Kaptain's requests in his own words are in `todo.md` (items 11 and 12); the rest are Claude's suggestions.
1. **Rebuild only the games worked on** (todo.md 11). Find which build steps really cross games and whether a build can run on
   the changed games alone; every later item needs many builds, at about 10 minutes each.
2. **Check the patterns against the mechanics files.** The files are done (21 Oct 2026): `tools/mechanics/<game>.txt` for all
   24 games, the 16 new ones written from the sources read for the real-world cases (named in each file's header), with
   `name|concept|regex` lines and `# term:` lines (`(assumed)` where no source has it); Blood Bowl's is empty (no source read).
   Not done: the regexes are not yet run. For each game: `coverage.py --mechanics`, fix the regexes that miss the cards'
   wording, then the gaps in its patterns, reload it (`reload_game.sh`), keep only if nothing is worse (`compare_builds.py`).
   One game per pass. Their keys exist; do not re-read them. A plain reload is not better by itself (Into the Breach went from
   74 to 130 wrong per 100 key entries). Faeria: first re-measure its reload on the corrected key, then the same check. In each
   pass also re-run `key_patterns.py` for the game: its key lines predate that script's whole-key and keyword checks (all 19
   regenerated at once on 21 Oct 2026: wrong down, Blood Bowl 163 -> 133, Into the Breach 74 -> 65, Runeterra 84 -> 80, but
   missed up in Duelyst, Hearthstone, Shadowverse, Slay the Spire, Kill Team and Blood Bowl, so it is measured per game).
3. **Retire `final_revert.py`.** It still puts back 915 tags of the original library (c7a77a4). Build without it and retire it
   only if nothing is worse.
4. **Tribal from type links.** Hearthstone has 390 cards that name a minion type and 132 tagged tribal; Lorcana 278 and 2. A rule
   "a card that names a type of its game cares about that type" needs only a short stop list per game.
5. **Learn the archetype recipes again** (the real-world cases are done). Learned weights over-fitted on 405 cases; with about 50 cases per game,
   split 50/50 with seed 1, try `learn_recipes.py` again.
6. **Missing data through the browser.** Legends sets after Houses of Morrowind (UESP), Stormbound cards after February 2022
   (fandom wiki), the keyword entry texts of Monster Train and two Legends keywords. The built-in browser reaches both wikis.
7. **One vocabulary** (a cleanup): move the pattern files and early build steps to the concept tree's ids, so `concept_tree.py`
   no longer moves tags on each build and the `v2_*` tables can go.
