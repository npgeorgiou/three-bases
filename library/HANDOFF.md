# Library: state and next steps (21 Oct 2026, morning)

## For Kaptain (morning)
1. **Database size.** The stored database is 92 MB; GitHub refuses files over 100 MB. The frozen base adds about 19 MB. Options
   (Claude's): store the base in compact form only (done), drop the `v2_*` tables by making the build work in one vocabulary
   (next steps 1), or move the database to Git LFS.
2. **`final_revert.py`** still runs and puts back 915 tags that the c7a77a4 library had and the key shows right. Retiring it
   (planned) changes results; it needs a measured build first.
3. **Scores of the five new games** are against small keys (40-50 entries each, one reader: Claude). `final_compare.py` flags them
   WORSE only because the c7a77a4 library has no such games; read their numbers on their own.

## Done in the night (20-21 Oct)
- **New triggers** `other_death_trigger`, `leave_trigger`, `other_leave_trigger`; `death_trigger` = the entry's own death.
  Rule: `tools/death_side.py` (wording tests run in every build). Keys corrected in all games (`tools/key/death_split.py`,
  run once from the keys of commit c0d1667; it is not idempotent), the readers' missing leave and other-death tags filled in,
  Leader (40k) and Doomed (Gwent) rule-only, keyword credit refreshed, regression lines for every per-card decision.
- **One chain.** Every build now starts from a frozen base inside the database (`base_tags`, `base_pairs`, `base_patterns`, made
  once by `tools/make_base.py` from the stored tagging, because the first build's corpus and code are gone and its curated tags
  cannot be re-derived: a build from the card data alone was reproducible but far worse on the key). `start_clean.py` replaces
  all tags, pairs and game pattern rows with the base at the start; loads add their cards' first tags to the base
  (`start_clean.py keep`) and then run every step over all games. Building twice gives identical tags and pairs (checked). The
  stored database is the output of this chain.
- **Fixes found on the way:** `key_wins.py apply` no longer drops a concept the corrected key now has; MTG `disable` patterns no
  longer read a card not untapping itself or tapping lands. Review of the rebuild differences: `tools/audit/rebuild_groups.md`.
- **Cleanup:** one-time fixes (f01-f16 except the build steps f03, f05, f07), insert-only loading, retag and new-concepts scripts,
  and the key readers' batch inputs are removed (git keeps them). The step3 files stay: the build reads its judged samples
  there (`patterns3.py answers`). A rebuild from the stored library after the cleanup gives identical tags and pairs. `key.py final` refuses to
  overwrite a corrected key.
- **Keys for the five newest games** (Lorcana 50, Stormbound, Star Wars Unlimited, Legends, Monster Train 40 each; random,
  seed 1; quotes checked). Scores: Lorcana wrong 164.0 / missed 78.0 per 100, Stormbound 105.0 / 70.0, SWU 177.5 / 70.0,
  Legends 110.0 / 40.0, Monster Train 102.5 / 42.5.
- **Results of the stored build** against the previous build: missed lower in 15 of 19 games, wrong equal or lower in all;
  regression 21316/21316, combos 80/82, real-world 245/405.

## Next steps, in order
1. One vocabulary: move the pattern files and early steps to the tree's ids, so `concept_tree.py` no longer moves tags each build
   and the `v2_*` tables can go.
2. Retire `final_revert.py` (measure first).
3. Faeria: re-measure the reload on the corrected key; then the mechanics check of the remaining 16 older games (README
   suggestion 1), one game per pass, keep only when the key, regression and real-world are not worse.
4. README suggestions 5-7 and 9 as listed there.

## Commands
- Build: `sh library/tools/build.sh library/three-bases-library.sqlite <scratch>/new.sqlite` (about 10 minutes; one at a time).
- Reproducibility: build the output again and compare `entity_concepts` and `trigger_effect`: they must be identical.
- Original for comparison: `git show c7a77a4:library/three-bases-library.sqlite > <scratch>/baseline.sqlite`
- Key score: `python3 library/tools/final_compare.py <scratch>/baseline.sqlite <scratch>/new.sqlite check`; new games:
  `python3 library/tools/key/key.py score <db> lorcana stormbound swu tesl monster_train`
- Real world: `python3 library/tools/realworld.py <db> -v` and `realworld_why.py <db>`; combos: `combo_check.py <db> -v`
- New wrong key tags of a game, base vs other build: `python3 library/tools/keydiff.py <game> <base.sqlite> <new.sqlite>`
