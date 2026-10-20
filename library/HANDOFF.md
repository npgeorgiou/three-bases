# Library tag-fix: state and next steps (20 Oct 2026)

Rule: **no readers, judges or agents** without Kaptain's OK. Scripts and builds only. Commit after each step.

## Done (all pushed)
Steps 1-7 and the final comparison are done; the library file is the build of 20 Oct 2026. Results and the full list of changes:
`tools/final/report.md`. In short: fewer wrong and fewer missed tags in all 20 games on the answer key (with the keyword credit,
KEY_BUG.md), real-world cases 161 -> 162, combos 80/82 as before, all build checks pass.

## Open
1. **12 real-world cases the new build lost** (listed in the report): trace each to the tags that dropped and their cause
   (`tools/lost_pairs.py` style), fix generically, rebuild, re-score.
2. **Scoring of payoff tags**: the key reads what a card does, so `benefits` tags count as wrong in `final_compare.py`; decide
   whether the scorers should skip them.
3. **Trigger pairs no longer derived**: `tools/lost_pairs.py <old> <new>` splits lost pairs into replaced-by-narrower and truly lost;
   look at the truly lost ones.
4. **Step 5** (reading what rules cannot decide) is not started and needs Kaptain's choice first.

## How to rebuild
`sh tools/build.sh three-bases-library.sqlite <scratch>/new.sqlite`, then `python3 tools/final_compare.py <scratch>/baseline.sqlite
<scratch>/new.sqlite check` (baseline: `git show c7a77a4:library/three-bases-library.sqlite`). Before a new final run, delete
`tools/final/revert.tsv` and `revert_base.tsv`, then alternate `final_compare.py ... revert` and a rebuild until no game is worse.
Never start a build while another one (or one of its python steps) still runs: two writers corrupt the scratch database.
