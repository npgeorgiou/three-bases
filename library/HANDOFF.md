# Library: state and open work (21 Oct 2026)

This file is the one list of open library work, in order. README.md "Suggestions for improving the library" keeps the ideas
and their history; todo.md item 10 points here.

## Done (do not redo)
- **Database size 92 MB -> 59 MB** (21 Oct). `tools/indexes.py` stores the frozen base (`base_tags`, `base_pairs`) only as its
  differences from the output and the big tables without their key indexes; `indexes.py create` (first step of build.sh and
  reload_game.sh) restores both. Round trip and rebuild checked: identical tags, pairs, links and patterns.
- **One reading method** (Kaptain's decision, 21 Oct): `ADDING_GAMES.md`, "Reading cards" (why the key exists, no undefined
  keywords, one request per game read once by one fresh process, `key.py answer`, `key.py credit`). Reader agents, batches and
  second or third readers are removed from tools and docs; never bring them back.
- **Keys of the five newest games** (21 Oct), read with that method: Lorcana 500, Stormbound 202, Star Wars Unlimited 500,
  Legends 497 (3 cards skipped by the reading), Monster Train 362. Their game blocks have sourced `# term:` lines in
  `tools/mechanics/<game>.txt`; Monster Train's 66 keyword entries were re-read with definitions (21 from the fandom wiki or
  assumed, tagged in the chat), its card tags that only quoted a keyword name were dropped, and `key.py credit` gives every card
  of the five games its keywords' tags. Legends: Ongoing and Beast Form assumed. About 715k subagent tokens in all.
  Scores of the stored library, wrong / missed per 100: Lorcana 125.2 / 89.6, Stormbound 75.7 / 81.7, SWU 152.8 / 96.8,
  Legends 111.1 / 73.6, Monster Train 62.7 / 89.8.
- Earlier (20-21 Oct night): new death and leave triggers, one build chain from the frozen base, the cleanup, reload of an older
  game, the step log, the real-world case audit (README suggestions 2-4).

## Open work, in order
1. **Fix the five new games' patterns against their new keys** (`tools/patterns/<game>.txt`). Missed is 74-97 per 100, wrong
   63-153. `tools/step3/key_patterns.py` builds patterns on one half of the key and keeps one only if it is 90%+ right on the
   other half; narrow wrong patterns only after a judged sample (`ADDING_GAMES.md` sections 3, 4, 4b). After each game: build,
   then regression, `combo_check.py`, `realworld.py -v`, `realworld_why.py`, `lost_pairs.py`, and keep it only if the key,
   regression and real-world are not worse. The keys are final: do not re-read them.
2. **Mechanics files for the 16 older games without one** (todo.md item 10 and README suggestion 1, the same work): darkest_dungeon,
   duelyst, gwent, hearthstone, hs_battlegrounds, marvel_snap, mtg, runeterra, shadowverse, sts1, sts2, wh_40k_10e, wh_aos_4th,
   wh_bloodbowl3, wh_killteam, wh_underworlds. For each: the mechanics its guides name (`name|concept|regex`) and its rules and
   terms as `# term:` lines with their source (`(assumed)` where no source has it); then `coverage.py --mechanics`, fix the gaps
   in its patterns, reload it (`reload_game.sh`), keep only if the key, regression and real-world are not worse. One game per
   pass. Their keys already exist (read earlier); do not re-read them. Faeria (has a file): first re-measure its reload on the
   corrected key, then the same check.
3. **Retire `final_revert.py`.** It still puts back 915 tags of the c7a77a4 library. Measure first: a build without it, compared
   on key, regression and real-world; retire it only if none is worse.
4. **One vocabulary** (a cleanup, not a size fix): move the pattern files and early build steps to the concept tree's ids, so
   `concept_tree.py` no longer moves tags each build and the `v2_*` tables can go.
5. **README suggestions still open**: 5 (more real-world cases, then learn the archetype recipes again), 6 (tribal from type
   links), 7 (combos with no connection), 9 (missing data: Legends sets after Houses of Morrowind, Stormbound cards after
   February 2022, keyword entry texts of Monster Train and two Legends keywords; their definitions are now in the mechanics
   files), 10 (Warhammer, not asked).

## Commands
- Build: `sh library/tools/build.sh library/three-bases-library.sqlite <scratch>/new.sqlite` (about 10 minutes; one at a time).
- Compare two builds: unpack both (`indexes.py <db> create`), then compare `entity_concepts` and `trigger_effect` with note texts
  resolved (`text_notes`), since note ids can differ.
- Original for comparison: `git show c7a77a4:library/three-bases-library.sqlite > <scratch>/baseline.sqlite`
- Key score: `python3 library/tools/final_compare.py <scratch>/baseline.sqlite <scratch>/new.sqlite check`; the five new games:
  `python3 library/tools/key/key.py score <db> lorcana stormbound swu tesl monster_train`
- Real world: `python3 library/tools/realworld.py <db> -v` and `realworld_why.py <db>`; combos: `combo_check.py <db> -v`
- New wrong key tags of a game, base vs other build: `python3 library/tools/keydiff.py <game> <base.sqlite> <new.sqlite>`
