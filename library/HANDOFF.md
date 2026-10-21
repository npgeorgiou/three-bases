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
  Stormbound all 202; Monster Train all 362). Each game block has sourced rules and terms (`# term:` lines in `tools/mechanics/<game>.txt`),
  except Monster Train (its 66 keyword entries already cover it). Stormbound's is thin: no glossary page could be reached.

## Next steps, in order
1. Read the five requests (one game first, check its answer by hand), then `key.py answer <game> --force` and `key.py credit`.
   Their current `key.json` (40-50 entries, read earlier) is replaced by the new answers.
2. Score the five games on the new keys: `key.py score <db> lorcana stormbound swu tesl monster_train`.
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
