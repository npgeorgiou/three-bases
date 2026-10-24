# Patterns check: one game at a time

README "Improving the library", item 1. Read this whole file before the first game of a chat.

## Goal (Kaptain, 24 Oct 2026)
Test each game against 1) its answer key (`tools/key/<game>/key.json`) and 2) its real-world cases (the ```tsv block of
`tools/games/<game>.md`) and make them match as much as possible. Not by making the tags agree artificially: find entry tagging
errors and fix them, so the whole game's tagging gets better. The key and the cases can be wrong too. Find the reason for each
disagreement, then improve the entry tagging: the mechanics regexes (the ```mechanics block of `tools/games/<game>.md`) first,
then the gaps in `tools/patterns/<game>.txt`.

## Rules (Kaptain)
- **Present before pushing.** Never push a pattern change, a key change or a shared change without first presenting the results and
  the findings to Kaptain. Push only after his OK.
- **Never change the key yourself.** Propose a key change; Kaptain decides. Key changes made so far are listed under Status.
- **Report the game's own numbers**, before and after: key wrong and missed per 100 key entries, and its real-world cases per kind
  (signature, archetype, splash, combo). Library totals are not the result of a game's pass.
- **Shared changes** (`tools/patterns/_all.txt`, code in `tools/`, the concept tree) reach every game: present every game's numbers
  (`compare_builds.py`), not only the current game's.
- Never invent rules or mechanics; mark judgements and suggestions as Claude's.
- One game per pass, all 21 games. Faeria: first re-measure its reload on the corrected key, then the same check.
- The keys exist: do not re-read the cards for them. A plain reload is not better by itself (Into the Breach once went from 74 to
  130 wrong per 100).

## Per game
1. **Baseline:** `sh tools/game_check.sh <scratch> <game>` (about 40 s). Unchanged, it gives the library's numbers.
2. **Mechanics regexes:** in its output, a `GAP` line or a low "carry the concept" count. `tools/mechanic_gaps.py <db> <game>` lists
   the entries behind it. A regex that matches other wording (e.g. "stun resistance" for stun) is fixed in the mechanics block;
   a wording the patterns miss is a pattern gap.
3. **Key disagreements:** `tools/key_diag.py <db> <game>` (per concept: wrong tags and missed key concepts, with examples), then
   `tools/pattern_hits.py <db> <game> <concept>` (which stored pattern gives the wrong tags). Decide per concept, by the concept's
   definition (`tools/key/defs.txt`, with its "Not:" line): a tagging error → fix the pattern file, generically for every entry
   with that wording; the key or a case looks wrong → list it for Kaptain.
4. **Every try:** `sh tools/game_check.sh <scratch> <game>`. Never a full reload or `compare_builds.py` per try.
5. **Re-run `tools/step3/key_patterns.py <db> <game>`** on the last check's database (`<scratch>/gc_<game>.sqlite`); it rewrites the
   game's 'new' lines of `tools/step3/decisions.tsv`, which `pattern_fix.py` applies in the build. Check once more.
6. **Present** to Kaptain: the numbers before and after, what was changed and why, the suspected key and case errors.
7. **After his OK:** `sh tools/reload_game.sh <scratch> <game>` once (about 3 min: it writes the game into a full copy and runs the
   library-wide checks once). `compare_builds.py` only when a shared change is in the pass. Copy `<scratch>/reloaded.sqlite` over
   `three-bases-library.sqlite`, commit and push.
8. **Game file:** add what the pass found that fits `tools/games/<game>.md` (rules and terms, faction facts, notes on the key or
   the cases) to its "Notes from the patterns check" section.

## How a tag gets there (read before guessing)
A game's tags come from the whole build chain (`tools/build.sh`, function `steps`), not only from its pattern file. In order:
- `start_clean.py`: back to the frozen base tags (`make_base.py`; a reload makes the game's base from today's patterns).
- `game_patterns.py`: the general patterns (table `concept_patterns`, game NULL), `patterns/_all.txt` and `patterns/<game>.txt`.
  A line `!concept|regex` removes that concept's text_pattern tags where the regex matches and no other pattern of the concept
  matches; a line removed from a file takes its tags away.
- `kw_sync.py` (keyword tags inherited), `propagate.py`, `keyword_defs.py`, reviews (`reviews/*.json`).
- `outcome_tree.py` and `link_types.py` rewrite some general patterns; `trigger_pairs.py` re-applies every trigger pattern and gives
  the trigger tag again (it honours the `!` lines since 24 Oct 2026).
- `regression.py enforce` re-applies the reviewed drops; `concept_tree.py apply` moves the tags to the tree's ids.
- `pattern_fix.py` (`step3/decisions.tsv`), `kw_links.py`, `parent_rule.py`, `final_revert.py` (puts back tags from
  `final/revert.tsv`), `key_wins.py apply`, `dedupe.py`, `distinct.py`.

Things that confused earlier chats:
- **Old ids in the pattern files.** They use the ids from before the tree move (e.g. `stat_loss` is written `debuff`; see
  `concept_tree.to_old`). `game_patterns.py` stops on an unknown id.
- **A tag no pattern matches** came from another step: `tools/pattern_hits.py` shows "(none)". The method column of
  `entity_concepts` says which kind (text_pattern, claude_review, via_keyword, restored, data_rule, game_structure).
- **Which step added or removed it:** the step log `<scratch>/gc_<game>.sqlite.steps.tsv` from `game_check.sh` holds, per step,
  game and concept, the count before and after (a gain has after > before).
- **Scoring** (`key.py score`): a library tag is right when it is a key concept, an ancestor or a descendant of one; game_structure
  and data_rule tags are left out. Two siblings in the tree do not cover each other.
- **The score depends on the tree file on disk** (`tools/concept_tree_v3.txt`, read by `key.py`): before and after must be scored
  with the same tree file. With a tree change stashed, the numbers of `game_check.sh` are not comparable with an earlier run.
- **A tag can be right for the wrong reason.** A pattern that matched other words ("When resolving those attacks" giving
  `on_attack`) or a tree link (a concept under `buff` making every `buff` case met) can hide a real gap. When a fix removes it, the
  score drops: find the real wording and add a pattern for it, instead of keeping the false match.
- **`parent_rule.py` drops a parent tag where a narrower tag is present** (e.g. `damage` where `multi_target_attack` is under it).
  An entry then loses the parent's coverage of the parent's other children (a key `aoe_damage` was met by `damage`): the fix is the
  child that is really there (a pattern for `aoe_damage`), not the parent.
- **Stale decisions after a tree change.** `step3/decisions.tsv` 'redirect' lines (`switch_off.py`) and `final/revert.tsv` restore
  lines were judged with the tree of their day; a tree change can make them wrong (ITB "in a row" pointed at `buff`). Re-running
  `switch_off.py` rewrites every game's lines (and data drift changes many), so fix the one line; `final_revert.py` restores a tag
  only while the key, a judged sample or a hand review still shows it right (24 Oct 2026).
- **Library-wide steps** (`signature.py`, `precision.py`, `finalize.py`, the checks) run only in `reload_game.sh` and `build.sh`;
  `game_check.sh` runs `signature.py` itself for the real-world cases. Tags are the same either way.
- **Times:** `game_check.sh` 40 s (wh_40k_10e about 2 min); `reload_game.sh` about 3 min; a full `build.sh` about 11 min and
  `compare_builds.py` about 4 min (run them in the background).

## Tools
- `tools/game_check.sh <scratch> <game>`: the build's steps on a one-game copy (`build.sh --steps`), then the game's mechanics
  coverage, key score, real-world cases, regression lines and combo misses. The one-game base is cached until the library changes.
- `tools/coverage.py <db> <game> 0 --mechanics tools/games/<game>.md`: the mechanics check alone.
- `tools/mechanic_gaps.py`, `tools/key_diag.py`, `tools/pattern_hits.py`: the diagnosis helpers above.

## Status
- darkest_dungeon: **done** 24 Oct 2026 (key wrong 78.9 → 57.6, missed 44.2 → 26.6 per 100; combos 6/7 → 6/7; it has no other cases).
  Key change (Kaptain): skills that target all enemy ranks also have `multi_target_attack` (wrong then 53.5). Its key_patterns
  run came after the reload, so the next build adds its decisions.
- Shared fixes 24 Oct 2026 (Kaptain's OK; all games, nothing worse): `multi_target_attack` moved under `damage`; `final_revert.py`
  restores only tags still shown right; ITB "in a row" redirect to `positional`. Key and case fixes: ITB Psion "explode on death"
  has `aoe_damage`; 40k "selected to fight" has `on_attack` (3 entries); Duelyst "Vetruvian buff" is a splash, not a signature.
  Patterns: ITB explosions (`aoe_damage`) and Fire (`damage_over_time`); 40k "selected to fight" (`on_attack`); Lorcana costs printed
  without their number ("ink —") are activated abilities.
- duelyst: **done** 24 Oct 2026 (key wrong 44.4 → 37.7, missed 41.5 → 27.5 per 100; signature 13/21 → 16/16, archetype 6/8 → 7/8,
  splash 1/1). Key changes (Kaptain): artifacts have `merge_attach` and `buff`; tribal where a card picks, counts or targets by
  tribe (Cryogenesis, Inkling Surge, Inkhorn Gaze, Snow Rippler, Fog, Sol); Gigaloth `permanent_growth`; Orb Weaver `summon`.
  Cases: Magmar Rebirth is `revive`; removed: Lyonar `board_presence`, Songhai `combo_sequence`, Vetruvian `summon`,
  `merge_attach` and `debuff` (the cards show no faction lead; reasons in the game file). Review: artifacts
  `merge_attach` instead of `items_consumables`. Shared (all games, nothing worse): "action bar" read as the hand in the
  own/enemy split of return_to_hand; "transform ANY" counts as possibly an enemy; `link_types.py` honours the `!` lines; the
  summon narrowing skips "player summons". The key_patterns rewrite was not kept (it lost more than it found).
- Shared 24 Oct 2026 (Kaptain's decision): shared card pools (Neutral, Colorless, Any) are left out of the faction comparison
  (`factions.py` SHARED); signatures and archetypes are measured between real factions only.
- Key rule (Kaptain's decision): a card that reacts to summons ("Whenever you summon a minion…") also has `summon` (it benefits
  from summons). Done for duelyst; add it in each other game's pass.
- Cases missed since shared pools left the comparison (24 Oct 2026; each a narrow lead now under 1.5 times): check them in
  their game's pass, tagging first: hearthstone Deathknight control and board_presence, Mage tribal and board_presence (splash),
  Demonhunter draw, Shaman tribal; shadowverse Swordcraft tribal; sts1 Defect cost_condition, Silent draw; tesl Willpower
  board_presence.
- Next: the other games in the order of `tools/key/key.py` GAMES.
