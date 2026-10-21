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
- **Patterns of the five new games against their keys** (21 Oct). `step3/key_patterns.py` made 177 `new` lines for them in
  `step3/decisions.tsv` (the other games' lines unchanged) and `step_games.json` now lets `pattern_fix` run on them (it was off
  for them, so no step-3 line ever reached them). Then, by `ADDING_GAMES.md` 4b.6, the 16 lines under 90% right on the whole key
  (3+ matches) were removed, and 55 alternatives that were only a keyword's name got the keyword position rule of `kw_links.py`
  (`valid()`), so a mention ("with Prophecy", "the Consume pile") no longer tags. Missed / 100: Lorcana 89.6 -> 65.4, Stormbound
  81.7 -> 67.3, SWU 96.8 -> 77.8, Legends 73.6 -> 69.0, Monster Train 89.8 -> 69.6; wrong unchanged except Lorcana 125.2 -> 125.4
  and SWU 152.8 -> 153.0 (one tag each, from patterns 13/14 and 40/41 right on the key). Regression, combos unchanged; real
  world 245 -> 250 of 405, no new misses; the 48 lost pairs all have a narrower pair in their place (damage -> ping and the
  like). Re-running `key_patterns.py` would bring the removed lines back and undo the keyword rule: redo both after it.
- Earlier (20-21 Oct night): new death and leave triggers, one build chain from the frozen base, the cleanup, reload of an older
  game, the step log, the real-world case audit (README suggestions 2-4).

## Open work, in order
1. **Mechanics files for the 16 older games without one** (todo.md item 10 and README suggestion 1, the same work): darkest_dungeon,
   duelyst, gwent, hearthstone, hs_battlegrounds, marvel_snap, mtg, runeterra, shadowverse, sts1, sts2, wh_40k_10e, wh_aos_4th,
   wh_bloodbowl3, wh_killteam, wh_underworlds. For each: the mechanics its guides name (`name|concept|regex`) and its rules and
   terms as `# term:` lines with their source (`(assumed)` where no source has it); then `coverage.py --mechanics`, fix the gaps
   in its patterns, reload it (`reload_game.sh`), keep only if the key, regression and real-world are not worse. One game per
   pass. Their keys already exist (read earlier); do not re-read them. Faeria (has a file): first re-measure its reload on the
   corrected key, then the same check.
2. **Retire `final_revert.py`.** It still puts back 915 tags of the c7a77a4 library. Measure first: a build without it, compared
   on key, regression and real-world; retire it only if none is worse.
3. **One vocabulary** (a cleanup, not a size fix): move the pattern files and early build steps to the concept tree's ids, so
   `concept_tree.py` no longer moves tags each build and the `v2_*` tables can go.
4. **README suggestions still open**: 5 (more real-world cases, then learn the archetype recipes again), 6 (tribal from type
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
