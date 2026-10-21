# Library: state and next steps (21 Oct 2026, late morning)

## Done today
- **Database size: 92 MB -> 59 MB.** The stored form (`tools/indexes.py`) keeps the frozen base (`base_tags`, `base_pairs`) only as
  its differences from the output, and the big tables without their primary-key and unique indexes; `indexes.py create` (first
  step of build.sh and reload_game.sh) restores both. A round trip gives identical tables; a build from the new stored form gives
  identical tags, pairs, links and patterns (note ids in `text_notes` are renumbered, the texts are the same). The `v2_*` tables
  are only about 0.1 MB: the one-vocabulary step is a cleanup, not a size fix.
- **One reading method** (Kaptain's decision): `ADDING_GAMES.md`, "Reading cards". One request per game (game block + up to 500
  cards), read once by one fresh process, answer checked by `key.py answer`. Reader agents, batches and second or third readers
  are gone from tools and docs.
- **Reading requests ready** for the five newest games: `tools/key/<game>/read.txt` (Lorcana, SWU, Legends 500 cards each;
  Stormbound all 202; Monster Train all 362). Each game block has sourced rules and terms (`# term:` lines in `tools/mechanics/<game>.txt`);
  Stormbound's comes from the stormbound-kitty rulebook.

- **New keys for the five newest games** (one-request reading, 21 Oct): Lorcana 500, Stormbound 202, SWU 500, Legends 497 (3
  cards skipped), Monster Train 362. Monster Train's cards were read before its keyword definitions were in the block: its 66
  keywords were re-read with definitions (21 found on the fandom wiki or assumed, then tagged by Claude in the chat), the 187
  card tags that only quoted a keyword name were dropped, and `key.py credit` gives every card its keywords' tags. Legends:
  Ongoing and Beast Form definitions assumed. About 715k subagent tokens in all, 106k-144k per game, most of it each subagent's start-up and the
  game block. Scores of the stored library with the keyword credit, wrong / missed per 100: Lorcana 125.2 / 89.6, Stormbound 75.7 / 81.7,
  SWU 152.8 / 96.8, Legends 111.1 / 73.6, Monster Train 62.7 / 89.8 (the old 40-50 entry keys gave 164 / 78, 105 / 70, 177.5 / 70, 110 / 40,
  102.5 / 42.5: the new keys tag more, so missed rose).

## Next steps, in order
1. Use the new keys to fix the five games' patterns (missed is high everywhere).
2. Mechanics files for the 16 games without one (todo.md item 10).
3. Retire `final_revert.py` (measure first: a build without it, compared on key, regression and real-world).
4. One vocabulary: move the pattern files and early steps to the tree's ids, so `concept_tree.py` no longer moves tags each build.
5. Faeria re-measure, then the mechanics check of the remaining 16 older games (README suggestion 1), one game per pass.

## Commands
- Build: `sh library/tools/build.sh library/three-bases-library.sqlite <scratch>/new.sqlite` (about 10 minutes; one at a time).
- Compare two builds: unpack both (`indexes.py <db> create`), then compare `entity_concepts` and `trigger_effect` with note texts
  resolved (`text_notes`), since note ids can differ.
- Original for comparison: `git show c7a77a4:library/three-bases-library.sqlite > <scratch>/baseline.sqlite`
- Key score: `python3 library/tools/final_compare.py <scratch>/baseline.sqlite <scratch>/new.sqlite check`
- Real world: `python3 library/tools/realworld.py <db> -v` and `realworld_why.py <db>`; combos: `combo_check.py <db> -v`
