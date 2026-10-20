# Three Bases inspiration library

## What it is
A SQLite database of game mechanics from 21 other games, built for Three Bases design questions: faction ideas, alternatives to a mechanic, cards that work with a concept or with other cards, and fixes for design problems. It holds mechanics only: names and wording are never reused in Three Bases.

It lives in the `library/` folder of **github.com/npgeorgiou/three-bases**: `three-bases-library.sqlite`, `tools/` (query and build scripts, data files), this README and `SEARCH_GUIDE.md` (how to search and read results).

## Contents
58,330 entries (cards, units, locations, abilities, items, rules), 1,151 keywords and 506 card types/tribes. Entries that repeat a mechanic within one faction are merged, so the counts are distinct mechanics, not printed cards.

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
| Disney Lorcana | 1,787 |
| Slay the Spire 2 (Early Access) | 1,386 |
| Gwent (standalone) | 1,357 |
| Darkest Dungeon | 949 |
| Marvel Snap (699 cards, 212 locations, 6 rules) | 917 |
| Slay the Spire | 895 |
| Duelyst | 786 |
| Faeria | 443 |
| Into the Breach | 287 |
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
**entities**: every card, unit, spell, item, location, ability, rule, keyword (its definition as text) and tribe, with game, category, faction, cost, stats and rules text. `variants` lists other names the same mechanic was printed under; **merged_entities** maps each merged name to the entry that kept it, so commands still find it. Keywords no card text uses were dropped on 12 Oct 2026 (`tools/fixes/f13`); one that later loses its last card is marked with `extra.note` "used by no card text in this library".

**concepts**: Claude's cross-game network of 293 design concepts (tree v3, 13 Oct 2026, plus seven triggers added on 19-20 Oct 2026: on_draw, on_discard, on_lifegain, on_block, on_targeted, on_sacrifice, on_life_loss; the readable tree, every move and its reason are in `CONCEPT_TREE.md`). Effects answer first **who it helps or hurts**: helps my side, hurts the enemy, hurts my side (drawback), neutral game rules. A concept has a second parent only when it is always a kind of both (lifesteal: heal and damage). For example, "no damage output" holds can't attack (attack lock), attack set to 0 and damage prevention. It sits under "suppress" (hurts the enemy), next to can't block, immobilize, silence and total disable (stun, freeze). "Make a unit stronger" (buff) holds stat gain and the combat bonuses; "make a unit weaker" (debuff) holds stat loss and penalties. "This turn / round only" is a separate marker. Every definition says what counts, what doesn't and where it goes instead, with two cards that fit and one look-alike that doesn't (`tools/concept_tree_v3.txt`, `tools/concept_examples.tsv`; the build step `tools/concept_tree.py` moves the older steps' tags to the tree). The view `concept_tree` gives all descendants. **Parent and child rule** (every game): an entry keeps only the narrowest concepts of a branch (ping, not also damage), in its tags and its trigger pairs (`tools/parent_rule.py`); every query command finds the parent through `concept_tree`. Definitions and parents fixed on 12 Oct 2026, with the wording patterns that feed them, are in `tools/concept_defs.py`.

**entity_concepts**: links each entry to its concepts with a role (does, grants, benefits, counters, cost; exhibits for design problems) and the method that made the link (reliability order in SEARCH_GUIDE). A card that gives a keyword to others has that keyword's concepts as `grants`, not `does`.

**concept_relations**: 478 relations (synergizes, enables, counters, mitigates, tension, variant_of), Claude's analysis. Every design problem is linked to the mechanics that ease or worsen it, including five from Three Bases playtests: p_objective_stalemate (dot-holding stalemates), p_resource_hoarding (carry-over hoarding), p_front_pileup (units piling into the front row), p_draw_engine (card-draw engines) and p_holder_snowball (the base holder snowballing). `anti_stalemate` (stalemates and board locks, and what breaks them) is a design problem too.

**entity_links**:
- **Keyword links:** has (the card's own keyword), grants (given to others: "creatures you control have flying"), mentions (only named: "creatures with flying"), describes (the text describes a keyword's mechanic in other words, Claude's reading).
- **Type links:** has_type, cares_about_type.
- **Name links:** references (names another card; for Magic also Scryfall's related cards), summons, generates (creates another card), transforms_into (a champion's level-up).
- **variant_of:** the same mechanic in another faction, and a Slay the Spire upgrade to its base card.
- **equivalent_keyword:** the same keyword in another game.

**Text positions (Step 6, 19 Oct 2026)**: tag evidence and pair clauses are stored as positions in the entry's own text (`ev_form/ev_pos/ev_len`, `cl_form/cl_pos/cl_len`; form 0 the stored text, 1 the text as patterns read it, 2 a note in `text_notes`). `tools/compact_text.py` explains the forms and cuts the text back out (`evidence_text`, `clause_text`); the build expands them first and compacts them last.

**trigger_effect**: about 82,500 "when X, do Y" pairs, from every clause of every entry and from the entry's keywords. Each pair has a **frequency** limit and its basis:
- **per_card:** a spell, a Place/on-play effect, the card's own death, or once per game.
- **per_round:** a once-per-turn cap, or the card's own turn start/end, attack, kill or tap ability.
- **unbounded:** fires on other units' events or on repeated events.
- **static:** an aura, not a trigger.

**faction_signature**: per source faction (30+ entries):
- **signature mechanics:** concepts the faction uses much more than the rest of its game. Share = the part of the faction's entries that have the concept; lift = that share divided by the game's average share. The rule: 5+ entries, share 6%+, lift 1.8+, and one of the two factions of its game that use the concept most. A broad faction left with fewer than 3 signatures (a Magic colour, a big class) also gets its concepts with lift 1.3+ (same entry and share minimums).
- **keyword signatures** (`kw:<keyword>`): a keyword whose cards are 60%+ that faction's;
- **splash:** every other faction that uses a signature mechanic, sorted by share.

**factions / archetypes / faction_archetypes**: every faction with its size and concept profile (concepts on 3+ of its entries and 5%+ of them, top 12 by lift), and 20 cross-game archetypes (swarm, sacrifice, graveyard, control, burn, aggro/tempo, scaling, fortress, sustain, spellslinger, ramp, positional, disruption, trickery, chaos, card advantage, tribal, objectives, damage over time, transformation) with each faction's share and lift. All rebuilt from the current tags on every build.

**mechanic_repeat**: an entry whose category, concepts and trigger pairs are exactly those of an earlier entry of the same game (usually the same mechanic in other numbers). Nothing is removed; `concept` and `search` take `distinct=1` to skip these.

**concept_precision**: per concept and game, how often the current wording patterns are right on the entries the hand reviews checked (a reviewed wrong tag counts only while a pattern would still make it). `concept` warns where this is below 70%.

**entity_fts**: full-text search. It and the search indexes are not stored in the file (about 21 MB): `tools/indexes.py` says how the build and `query.py` rebuild them. **games**, **load_log**: what each game is and how it was loaded.

## How Claude uses it
In a fresh chat, Claude clones the repository and runs `python3 library/tools/query.py <command>` (the script finds the database next to `tools/`; `TB_LIB` overrides). The commands and the rules for reading results are in SEARCH_GUIDE.md. The database never enters the conversation, only printed results do, so a design question costs a few short queries.

## Maintenance
- **Tag-fix plan, final (20 Oct 2026)**: the library is the build of that day; `tools/final/report.md` compares it with the original (c7a77a4) on the answer key, the 322 real-world cases and the combos (fewer wrong and fewer missed tags in all 20 games; real-world 161 -> 162; combos 80/82 both). The key credits the tags of the keywords a card has (`tools/key/key.py credit`); patterns built from the key's quotes (`tools/step3/key_patterns.py`), old patterns right less than half the time switched off or redirected (`tools/step3/switch_off.py`), new triggers and amplifiers (`tools/step3/trigger_patterns.py`, `tools/step3/amp_patterns.py`), all as lines of `tools/step3/decisions.tsv`; review records in the tree v3 ids (`tools/fixes/f15`), and where a review and the key disagree on what a card does the key wins (`tools/key_wins.py`). Lost trigger pairs by cause: `tools/lost_pairs.py`.
**Lorcana and Stormbound added (20 Oct 2026)**: patterns in `tools/patterns/lorcana.txt` and `stormbound.txt` (every pattern checked on sampled matches), 33 and 18 real-world cases. Build fixes found on the way: `build.sh` expands the database before loading and reads load paths from the caller's folder; `load_cards.py` honours a `!` line in an old concept id for its new ids and takes a new game's `_game` row; `keep_old.py` puts back old entries the chain itself drops (176 on every rebuild, by drop_untagged). `signature.py` minimum faction size 30 -> 20 (Stormbound factions have 28-30 cards): real-world 176 -> 189 of 351, no game worse.
**D&D 5e removed (20 Oct 2026)**: Kaptain's decision; `tools/fixes/f16_drop_dnd.py` deleted its entries and every row pointing at them, and its scripts, patterns, reviews, key and cases are gone. Real-world test since: 150 of 300 (D&D had 12 of 22); the other games are unchanged.
The build is incremental: `three-bases-library.sqlite` is the base for all work. The raw corpus of the first build is deleted and not needed.

- **Fix wrong tags** in these places, then run `tools/build.sh <in.sqlite> <out.sqlite>`:
  - the per-game pattern files (`tools/patterns/<game>.txt`: `concept|role|regex` adds a pattern, `!concept|pattern` switches a general pattern off for that game);
  - the hand reviews (`tools/reviews/<game>.json`; a decision also reaches entries of the same category with the very same text), then `regression.py <db> make` and `regression.py <db> enforce`;
  - the keyword reviews against the outcome tree (`tools/reviews_outcome/<game>.json`).
- **Tag audit** (12 Oct 2026): `tools/audit/audit.py` (sample, show, trial, confirm, blind, score); per game the errors found in the 150 work entries and the blind checker's judgments of the 50 held-out entries (the samples, snapshots and blind files were removed after scoring). A newer review decision replaces an older opposite one; a reviewed keyword passes added concepts only to entries that have the keyword, not to those that only mention it.
- **Add cards:** a converter in `tools/convert/` turns a source file into the load format (described in `tools/load_cards.py`). Then run `tools/build.sh <in.sqlite> <out.sqlite> <game>=<cards.json> ...`. New cards get the same tagging as the rest of their game; older entries stay as they were, apart from merges and links to the new cards.
- **How entries are tagged:** an entry gets the general wording patterns (all games) once, when it is loaded; the game's own patterns, keyword inheritance, outcome concepts, link rules and trigger pairs are re-derived on every build. Text is read lower-cased with the entry's own name as "name"; Magic without reminder text. Entries that no pattern or keyword reaches are dropped.
- **One-time fixes** of 12 Oct 2026 are in `tools/fixes/` (f01 Magic cut, f02 Scryfall data, f04 text clean-up, f06 leftovers, f08 weak patterns, f09 whole-entry patterns, f10 Magic non-token cards, f11 icon words in Slay the Spire text and stat lines for units without them, f12 review tags that older builds copied across categories, f13 the 19 keywords no card used, f14 the one untagged entry with no mechanic, f16 the removal of D&D 5e; the other 51 untagged entries were read and tagged in the reviews); f03 (granted keywords are not "does"), f05 (faction names and table) and f07 (keyword links, concept tree) are also build steps.

The build stops if any check fails:
- **regression set** (`regression.py <db> check`): 21,282 reviewed tags must hold (a reviewed parent also holds through a narrower concept);
- **combo set** (`combo_check.py <db>`): 82 enabler → payoff pairs, 80 found, 2 known misses;
- **trigger coverage** (`trigger_pairs.py <db> check`): at least 50% of entries with a trigger in every game;
- **query tests** (`test_query.py <db>`): all 16 commands.

Sources of the later loads (converter in brackets):
- Disney Lorcana (20 Oct 2026): LorcanaJSON as bundled in the npm package lorcana-oracle 0.1.2, sets 1-12 (12 incomplete) and Illumineer's Quest [conv_lorcana.py]; keywords from the source's keyword field, definitions from the reminder text, keyword concepts in `reviews/lorcana.json`; 264 vanilla characters (no text) dropped, 248 repeats merged.
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

## Suggestions for improving the library
Claude's suggestions, none done.
1. **Hand-review more entries** of the noisiest games (Age of Sigmar, 40k, Kill Team) and the 12 Oct loads, and add the decisions to `tools/reviews/` (then `regression.py <db> make` and `enforce`). A first sample was reviewed on 12 Oct 2026 (Age of Sigmar 30, 40k 30, D&D 25 entries: 46 needed corrections); it is still too small for precision estimates there (Age of Sigmar has one precision cell, 40k none).
