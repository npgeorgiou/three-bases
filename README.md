# Three Bases inspiration library

## What it is
A SQLite database of game mechanics from 20 other games, built to support Three Bases design questions: faction ideas, alternatives to a mechanic, cards that work with a concept or with other cards, and solutions to design problems. It contains mechanics only: names and wording are never reused in Three Bases, and the library holds no "this could become X in Three Bases" notes.

The library ships as **three-bases-library.zip** (about 20 MB): `three-bases-library.sqlite` (the database), `lib/` (build and query scripts) and `SEARCH_GUIDE.md` (detailed search rules). The raw source data (library-corpus.zip) is not needed to use it, only to rebuild it from scratch.

## Contents
52,181 cards, units, locations, abilities, items, rules and other entries, plus 1,187 keywords and 450 card types/tribes.

| Game | Entries |
|---|---|
| Magic: The Gathering | 17,834 |
| Hearthstone | 5,534 |
| Warhammer 40,000 (10th edition) | 3,833 |
| Shadowverse | 3,799 |
| Warhammer Age of Sigmar (4th edition) | 3,232 |
| Warhammer Underworlds | 3,084 |
| Hearthstone Battlegrounds | 2,251 |
| Warhammer 40,000: Kill Team | 2,041 |
| Legends of Runeterra | 1,793 |
| Dungeons & Dragons 5e (SRD) | 1,332 |
| Slay the Spire 2 (Early Access) | 1,291 |
| Gwent (standalone) | 1,254 |
| Darkest Dungeon | 1,018 |
| Marvel Snap (738 cards, 222 locations, 6 rules) | 966 |
| Slay the Spire | 850 |
| Duelyst | 792 |
| Faeria | 446 |
| Inscryption | 298 |
| Into the Breach | 289 |
| Blood Bowl (Third Season) | 244 |

Dropped by agreement: Kingdom Death: Monster, Darkest Dungeon 2 and DD1 DLC, Hearthstone Mercenaries, Path of Champions (except items), older or variant Warhammer systems (40k 9th/7th/2nd, Horus Heresy, Legions Imperialis, Apocalypse, Epic Armageddon, Titanicus, Aeronautica, Battlefleet Gothic, old Age of Sigmar, old Blood Bowl, Necromunda, Mordheim, Warcry, Warhammer Fantasy, Middle-earth SBG, The Old World). Removed as noise: tokens, cosmetics, joke and Commander-only Magic cards, commons, duplicates, campaign bookkeeping, lore, and every entry that matched no concept. Each game's `load_log` lists exactly what was dropped and why.

## Structure
**entities**: every card, unit, spell, item, relic, building, terrain, hero, monster, boss, event, modifier, ability, status, game rule, keyword (with its definition as text) and tribe. Fields: game, normalized category, the source's own type, faction, subtypes, rarity, cost, stats, original rules text.

**concepts**: Claude's own cross-game network of 256 design concepts, with ten roots: effect, combat, trigger, condition, economy, scope, structure, win_condition, role, design_problem. A concept can have several parents (`concept_parents`); the view `concept_tree` returns all descendants of any concept.

**entity_concepts**: links every entry to its concepts with a role: does, grants, benefits, counters, cost (or exhibits, for design problems). Each link records how it was made, from most to least reliable: claude_review (hand-mapped by reading the entry or its definition), via_keyword (inherited from a reviewed keyword), via_link (inherited from a card the entry names, e.g. a token it summons), claude_inference (keyword without a source definition), data_rule/game_structure (rule applied to a whole category), and text_pattern (automatic, from general and per-game wording patterns).

**concept_relations**: 346 relations between concepts (synergizes, enables, counters, mitigates, tension, variant_of). These are Claude's analysis, not source data. Every design problem (snowballing, stalemate, first-player advantage, board flooding, dead draws and others) is linked to the mechanics that mitigate it or make it worse.

**entity_links**: connections between entries.
- Keyword links: has_keyword, grants_keyword, mentions_keyword.
- Type links: has_type, cares_about_type.
- Name links, where one card names another: references, summons, generates, transforms_into.
- variant_of.
- equivalent_keyword: the same mechanic across games, e.g. Hearthstone Taunt, Shadowverse Ward and Gwent Defender. These links are only for jumping between games; a correction to one game's keyword never travels through them.

**trigger_effect**: about 27,900 trigger → effect pairs taken clause by clause from rules text (e.g. on death → heal). It shows the design space of "when X, do Y", including the combinations no game uses.

**factions / archetypes / faction_archetypes**: per-faction concept profiles, and 20 cross-game archetypes. Archetypes: swarm, sacrifice, graveyard, control, burn, aggro/tempo, scaling, fortress, sustain, spellslinger, ramp, positional, disruption, trickery, chaos, card advantage, tribal, objectives, damage over time and transformation. A faction can belong to several archetypes, each with its share and lift.

**entity_fts**: full-text search over names and rules text. **load_log** and **games**: what each game is, its structure, its source and every cut.

## How Claude uses it
In a chat in this project, Claude unpacks the zip into its sandbox and runs `python3 lib/query.py <command>`. Commands:
- `concept <id>`: everything linked to a concept, per game.
- `concepts <term>`: find concept ids.
- `cooccur <id>`: concepts printed together on cards.
- `problem <p_id>`: mechanics that mitigate a design problem, with examples.
- `faction <game>`: concept profiles of a game's factions.
- `archetypes [id] [game=]`: archetypes and the factions that embody them.
- `grid [trigger] [effect]`: the trigger × effect design space.
- `unused_pairs <trigger>`: effects no game pairs with that trigger.
- `interactions "<card>"`: a card's partners through links, types, keywords and concepts.
- `combo "<A>" "<B>"`: every known connection between two cards.
- `search "<text>"`: full-text search.
- `entity "<name>"`: a full record.

Claude always reads results per game (Magic alone is about a third of the entries), checks each game's own wording for a concept, and reads the actual card text before relying on automatic tags.

## Token cost
The database never enters the conversation. Claude queries it with code and reads only the printed results, so a typical design question costs a few queries of a few hundred lines in total. Unpacking the zip at the start of a chat costs almost nothing. The large costs come from long conversations, not from the library, so it is best to ask library questions in a fresh chat.

## How the tags were built and reviewed
Every game was reviewed in full in the second catalogue pass (October 2026). Marvel Snap came first, then the closest games. Each review was applied at three levels, and every finding was retrofitted to all games where it applied:
1. **General patterns** (all games). Wording rules for each concept. Ones found to misread a common word were corrected in place (the FIX list in `lib/new_concepts.py`). Examples: "discard pile" is not discard, "Remove a card from your deck" is not tutor, "start of combat" is not turn start, "subtract 1 from hit rolls for attacks that target this unit" is damage reduction, not debuff.
2. **Per-game pattern files** (`lib/patterns/<game>.txt`). Lines `concept|role|regex` add the game's own wording. Lines `!concept|pattern` switch off a general pattern that misreads that game. For example, in Kill Team "activated" means the operative's turn, and re-rolls are advantage, not randomness. A switched-off pattern removes its tag only when no other pattern with the same role still matches.
3. **Hand review** (`lib/reviews/<game>.json`). Entries were read and concepts added or dropped. An explicit drop removes the concept whatever made it. A correction to a keyword reaches every entry of the same game that has that keyword.

Two clean-up steps run after these: `fix_grants.py` turns "with Taunt"-style keyword links into benefits or counters when the card does not grant the keyword, and `kw_sync.py` makes inherited keyword concepts match the keyword's reviewed concepts. CHANGES.md lists every change per game.

## Known limits
- Automatic tags on long prose (D&D, Warhammer army rules) are still the least precise, although each now has its own pattern file. Short card text is good.
- Some keyword definitions are Claude's inference where the source had none; the keyword's source_type says so.
- Combo detection works at the level of concepts and keywords. It finds candidates; confirming a combo means reading both cards.
- Gaps: Warhammer Fantasy 6th and the newer Underworlds seasons have no rules text; Underworlds has deck cards but no fighter cards; Darkest Dungeon is base game only, and its text was rendered by Claude from raw data fields. Marvel Snap keyword definitions are Claude's inference from how cards use them.

## Suggestions for improving the library
Claude's suggestions, roughly in order of value for Three Bases design work. None of them are done.
1. **Line-by-line review of the long-prose games.** Warhammer 40k, Age of Sigmar, D&D and Magic were reviewed through patterns, keyword fixes and sampled audits, not card by card like Snap or Hearthstone. A full pass over their remaining text_pattern tags would raise precision the most.
2. **Precision check per concept.** For each concept, draw 20 random tagged entries per game and mark them right or wrong; store the score in a table. Searches could then warn when a concept is unreliable in a game.
3. **Regression set.** Keep a list of known-correct and known-wrong tags (from the reviews) and check it after every build, so a new pattern can't silently undo earlier fixes.
4. **Combo validation set.** Collect 50–100 real, well-known combos across games and test that `combo` and `interactions` find them; use the misses to add link types.
5. **Unmapped keywords.** A few keywords still have no concepts or definition (e.g. Snap's newer ones, some Magic set mechanics such as Prepare, Fabled-style mechanics, Skybound Art). Map them, ideally from official glossaries.
6. **Condition-aware D&D keywords.** D&D conditions (Frightened, Grappled…) are inherited through mentions only; adding has/inflicts roles, like the `h:` sync for other games, would separate "causes it" from "suffers it".
7. **Missing data.** Underworlds fighter cards and the newer Underworlds seasons' rules text; Darkest Dungeon DLC; official Snap location list with exact texts.
8. **Near-duplicates.** Many 40k and Age of Sigmar datasheets repeat the same ability under different names; a variant_of grouping would shorten results.
9. **Design-problem coverage.** Add more design problems seen in Three Bases playtests (e.g. dot-holding stalemates, carry-over hoarding) and link them to mitigating mechanics.
10. **Tests for query.py.** A small test file that runs every command on a fixed query and checks the output shape, so tool changes don't break searches.
