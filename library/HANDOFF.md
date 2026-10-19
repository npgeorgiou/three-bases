# Library tag-fix: state and next steps (19 Oct 2026)

Rule for the next chat: **no readers, judges or agents.** Scripts and builds only. Commit after each step.

## Done and kept (all pushed)
- **Step 1, concept tree v3**: `tools/concept_tree_v3.txt`, `tools/concept_tree.py`, `CONCEPT_TREE.md`. The database in the repo is the Step 1 build.
- **Step 2, answer key**: `tools/key/<game>/key.json`, 8,242 entries. Two readers each, a third for disagreements, and every tag carries the exact quoted words. Accurate, and the only measuring stick.
- **Step 3, pattern judgments and narrowing**: `tools/step3/` (`questions.json`, `judge/`, `decisions.tsv` with 106 narrowings that passed a check on what they drop). Applied by the build step `tools/pattern_fix.py`.
- **Step 4, keywords**: `tools/key/kw_<game>/key.json` holds all 1,167 keyword entries, read twice and settled. This work is good. The build step `tools/kw_links.py` applies it: keyword tags, the new rule for when a card has a keyword, and inheritance only through has/grants.
  - On the key it made 7 games worse (into_the_breach, wh_bloodbowl3, faeria, marvel_snap, runeterra, wh_40k_10e, hearthstone), so `tools/step_games.json` switches it on only for the other 13 games.
- **Step 6, smaller database**: `tools/compact_text.py`, in the build. Tested; the database drops to 87 MB.
- **Step 7, real-world cases**: `tools/realworld/<game>.tsv` (322 cases with source URLs) and the check `tools/realworld.py`, in the build. The original meets 161.
- **Final comparison tools**: `tools/final_compare.py` and `tools/final_revert.py` (in the build after parent_rule). `tools/final/revert.tsv` is from an experiment: regenerate it at the end (step 4 below).
- **Original database for comparison**: `git show c7a77a4:library/three-bases-library.sqlite > <scratch>/baseline.sqlite`.

## Why the key score is still about 2 wrong and 1.1 missed per entry
Patterns cause about half the wrong tags (hand reviews and keyword inheritance the rest). Narrowing only removes tags, and no step has yet added the many conditions, triggers and effects the key readers found.

## Next steps (scripts only, est. 0.3-0.5M tokens)
1. **Patterns from the key's quotes.** A new script `tools/step3/key_patterns.py`: for each game and concept, build regexes from the key's quoted words (escaped, lower-case, the entry's own name as `name`, Magic without reminder text). Test each on held-out key entries: split each game's key 50/50 with seed 1, build on one half, test on the other, and the reverse. Keep a pattern only if it is 90%+ right on the half it was not built from. Write the kept ones as `new` lines into `tools/step3/decisions.tsv` (format in `tools/pattern_fix.py`). One pattern set per game.
2. **Build:** `sh tools/build.sh three-bases-library.sqlite <scratch>/new.sqlite`. All checks must pass.
3. **Score:** `python3 tools/final_compare.py <scratch>/baseline.sqlite <scratch>/new.sqlite check`.
4. **No game worse than the original:** `... revert` writes `tools/final/revert.tsv`, then rebuild once and check again.
5. Copy the build over `three-bases-library.sqlite`, write `tools/final/report.md` from the numbers, update README, commit, push.
6. **Step 5** (reading what rules cannot decide) is not started and needs Kaptain's choice first. No readers without his OK.
