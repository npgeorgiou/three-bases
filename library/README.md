# Three Bases inspiration library

## What it is
A SQLite database of game mechanics from 20 other games, built for Three Bases design questions: faction ideas, alternatives to a mechanic, cards that work with a concept or with other cards, and fixes for design problems. It holds mechanics only: names and wording are never reused in Three Bases.

It lives unzipped in **github.com/npgeorgiou/three-bases**: `three-bases-library.sqlite` at the root, `tools/` (query and build scripts, data files), this README and `SEARCH_GUIDE.md` (how to search and read results). three-bases-library.zip holds the same files and is only a way to download them.

## Contents
55,312 entries (cards, units, locations, abilities, items, rules), 1,187 keywords and 450 card types/tribes. Entries that repeat a mechanic within one faction are merged, so the counts are distinct mechanics, not printed cards.

| Game | Entries |
|---|---|
| Magic: The Gathering | 17,813 |
| Hearthstone | 8,389 |
| Shadowverse | 3,799 |
| Warhammer 40,000 (10th edition) | 3,761 |
| Warhammer Age of Sigmar (4th edition) | 3,213 |
| Warhammer Underworlds | 3,131 |
| Legends of Runeterra | 2,438 |
| Hearthstone Battlegrounds | 2,260 |
| Warhammer 40,000: Kill Team | 1,977 |
| Dungeons & Dragons 5e (SRD) | 1,279 |
| Slay the Spire 2 (Early Access) | 1,271 |
| Gwent (standalone) | 1,250 |
| Darkest Dungeon | 950 |
| Marvel Snap (699 cards, 212 locations, 6 rules) | 917 |
| Slay the Spire | 838 |
| Duelyst | 786 |
| Faeria | 443 |
| Into the Breach | 289 |
| Inscryption | 264 |
| Blood Bowl (Third Season) | 244 |

Created cards are included where a source has them: Runeterra (levelled champions, champion spells, tokens), Hearthstone (tokens, generated cards, rewards) and Battlegrounds. They carry edition `non-collectible`, and a name already used gets " (created)".

## Structure
**entities**: every card, unit, spell, item, location, ability, rule, keyword (its definition as text) and tribe, with game, category, faction, cost, stats and rules text. `variants` lists other names the same mechanic was printed under; **merged_entities** maps each merged name to the entry that kept it, so commands still find it.

**concepts**: Claude's cross-game network of 277 design concepts under ten roots (effect, combat, trigger, condition, economy, scope, structure, win_condition, role, design_problem). Effects are sorted by **outcome first, mechanism second**, and a concept can have several parents. For example, "no damage output" holds can't attack (attack lock), attack set to 0 and damage prevention. It sits under "suppress", next to can't block, immobilize, silence and total disable (stun, freeze). "Stat loss" (debuff) is a separate branch, and "this turn / round only" is a separate marker. The view `concept_tree` gives all descendants.

**entity_concepts**: links each entry to its concepts with a role (does, grants, benefits, counters, cost; exhibits for design problems) and the method that made the link (reliability order in SEARCH_GUIDE).

**concept_relations**: 447 relations (synergizes, enables, counters, mitigates, tension, variant_of), Claude's analysis. Every design problem is linked to the mechanics that ease or worsen it, including five from Three Bases playtests: p_objective_stalemate (dot-holding stalemates), p_resource_hoarding (carry-over hoarding), p_front_pileup (units piling into the front row), p_draw_engine (card-draw engines) and p_holder_snowball (the base holder snowballing).

**entity_links**:
- **Keyword links:** has, grants, mentions. D&D conditions use inflicts, counters, suffers and benefits instead.
- **Type links:** has_type, cares_about_type.
- **Name links:** references, summons, generates (a card that creates another), transforms_into (a champion's level-up).
- **variant_of:** also links the same mechanic in another faction.
- **equivalent_keyword:** the same keyword in another game.

**trigger_effect**: about 68,400 "when X, do Y" pairs, from every clause of every entry and from the entry's keywords. Each pair has a **frequency** limit and its basis:
- **per_card:** a spell, a Place/on-play effect, the card's own death, or once per game.
- **per_round:** a once-per-turn cap, or the card's own turn start/end, attack, kill or tap ability.
- **unbounded:** fires on other units' events or on repeated events.
- **static:** an aura, not a trigger.

**faction_signature**: per source faction (30+ entries):
- **signature mechanics:** concepts the faction uses much more than the rest of its game;
- **keyword signatures** (`kw:<keyword>`): a keyword whose cards are 60%+ that faction's;
- **splash:** every other faction that uses a signature mechanic, sorted by share.

**factions / archetypes / faction_archetypes**: per-faction concept profiles, and 20 cross-game archetypes (swarm, sacrifice, graveyard, control, burn, aggro/tempo, scaling, fortress, sustain, spellslinger, ramp, positional, disruption, trickery, chaos, card advantage, tribal, objectives, damage over time, transformation). Each faction is listed with its share and lift, recomputed from the current tags.

**concept_precision**: per concept and game, how often the automatic tags were right on the entries the hand reviews checked. `concept` warns where they are below 70%.

**entity_fts**: full-text search. **games**, **load_log**: what each game is and how it was loaded.

## How Claude uses it
In a fresh chat, Claude clones the repository and runs `python3 tools/query.py <command>` (the script finds the database next to `tools/`; `TB_LIB` overrides). The commands and the rules for reading results are in SEARCH_GUIDE.md. The database never enters the conversation, only printed results do, so a design question costs a few short queries.

## Maintenance
`tools/build.sh` rebuilds the database from the raw corpus and the data files in `tools/`. Wrong tags are fixed in these places:
- the per-game pattern files (`tools/patterns/<game>.txt`);
- the hand reviews (`tools/reviews/<game>.json`);
- the keyword reviews against the outcome tree (`tools/reviews_outcome/<game>.json`).

The build stops if any check fails:
- **regression set** (`regression.py <db> check`): 12,694 reviewed tags must hold;
- **combo set** (`combo_check.py <db>`): 82 enabler → payoff pairs, 80 found, 2 known misses;
- **trigger coverage** (`trigger_pairs.py <db> check`): at least 50% of entries with a trigger in every game;
- **query tests** (`test_query.py <db>`): all 16 commands.

After a new hand review, run `regression.py <db> make`.

## Known limits
- Automatic tags on long prose (D&D, Warhammer army rules) are the least precise; the precision warnings show where.
- Combo detection finds candidates through concepts, keywords and trigger links; confirming a combo means reading both cards.
- Frequency limits, D&D condition roles and trigger pairs come from wording rules, not play; real counts come from the Three Bases simulator.
- Missing data:
  - Magic: commons, tokens and Commander cards.
  - Shadowverse and Gwent: tokens.
  - Slay the Spire: upgraded card versions.
  - Underworlds: fighter stat lines.
  - All games: entries the first build dropped because no pattern matched them.

## Suggestions for improving the library
Claude's suggestions, none done.
1. **Load the missing data** above once the source files are available. The files needed are:
   - Magic: Scryfall's "Oracle Cards" bulk file or MTGJSON's AtomicCards.json;
   - Shadowverse and Gwent: a full card export including tokens;
   - Slay the Spire 1 and 2: card data with upgraded text;
   - all games: the raw corpus (library-corpus.zip).

   This session cannot reach any of these sources.
2. **Review the weak cells** that concept_precision lists (below 70%), game by game, and fix them in the pattern files.
