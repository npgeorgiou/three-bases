# Patterns check: one game at a time

Read this whole file before the first game of a chat. It is README "Improving the library", item 1.

## Goal (Kaptain, 24 Oct 2026)
Improve each game's tagging. The game's answer key (`tools/key/<game>/key.json`) and its real-world cases (the ```tsv block of
`tools/games/<game>.md`) are the tests, not the target: never make tags agree artificially. The key and the cases can be wrong
too. Find the reason for every disagreement and fix it where it is: the entry tagging (mechanics regexes, then
`tools/patterns/<game>.txt`, reviews, keyword entries), the key or the case.

## Rules (Kaptain)
- **Never push without Kaptain's "push".** Present the results first; an OK to a change is not an OK to push.
- **Never change the key yourself.** Propose: the entries, what each card says (quote it), the tag to add or remove, one yes/no
  question. Proposing is mandatory, in the same report, whenever something shows a key tag wrong or missing. Apply only what
  Kaptain approves (or settles with "change the key where you are sure"), and list it in the game's line below.
- **Report the game's own numbers**, before and after: key wrong and missed per 100 key entries, and its real-world cases per kind.
- **Shared changes** (`patterns/_all.txt`, code in `tools/`, the concept tree, definitions) reach every game: present every game's
  numbers (`compare_builds.py`).
- **Explain for someone who has not played the game.** Each decision: the situation, the cards, what each option does. Short.
- Never invent rules, stats or mechanics; mark judgements and suggestions as Claude's.
- One game per pass, all 21 games (table below).

## Decisions that apply to every game
- **Cases the cards don't support:** a signature or archetype case whose faction shows no lead of 1.3 times in the cards (the key; Kaptain, 26 Oct 2026, was 1.5)
  is removed, with the reason in the game's "Notes from the patterns check".
- **Shared pools** (Neutral, Colorless, Any) are not factions (`factions.py` SHARED).
- **Faction counts:** a card merged into another with the same text (`dedupe.py`, table `merged_entities`) still counts as a card.
  Cost tags (role `cost`) count. A mechanic on more than 25% of the cards is too common for a signature, unless one faction holds
  at least 60% of it.
- **Combos** can name a card, a merged card, a keyword or a tribe. A tribe connects through its cards.
- **Summon reactions** ("Whenever you summon a minion") have the trigger (`on_ally_play`, or `on_enemy_enter` for the opponent's
  summons), never `summon`.
- **Back to hand vs revive:** `revive` = a dead unit comes back into play; back to hand (when it dies, or from the discard pile or
  graveyard) is `return_to_hand`.
- **Damage types:** `multi_target_attack` = several separately chosen targets; `aoe_damage` = damage reaching several without
  choosing each; `random_target` = a random existing target; `adjacency` = neighbours for any purpose; `area_templates` = a named
  shape. Gwent "damage N units by X" is chosen targets. Smoke is `attack_lock`.
- **Stat gains:** `attack_gain` / `defence_gain` where the text names the stat; `stat_gain` where it does not; Gwent, Stormbound and
  Marvel Snap are single-stat games (no split). Warhammer "+1 to Hit / Wound / save rolls" are gains.
- **Data outside the text** (costs) is tagged from its field (`cost_rules.py`), not by text patterns.
- **Effects on the card itself** carry `scope_self` in every wording ("this gains", "Has +2/+0 while", "She gains", "double its
  Attack"), in the key and in the patterns (Kaptain, 26 Oct 2026; Faeria done, the other games in their passes).
- **Discounts on cards in hand** are `in_hand_buff` and `cost_reduction` both; a discount on the card itself is `cost_reduction`.
  "Give the next X creature you summon +1/+1" is `delayed` + `on_ally_play` + the stat gains, not `in_hand_buff`.
- **Key quotes** must be words of the card; a quote that is a definition marks an unverified tag.

## Games
Order of `tools/key/key.py` GAMES. Numbers: key wrong / missed per 100 entries, then real-world cases met, as of 26 Oct 2026
(after the Inscryption pass). Open: what the game's pass must look at besides the procedure.

| Game | Pass | Key wrong / missed | Cases met | Open |
|---|---|---|---|---|
| into_the_breach | done 26 Oct | 47.0 / 13.3 | signature 2/2, archetype 1/1, combo 6/6, splash 2/2 | |
| inscryption | done 26 Oct | 50.4 / 26.9 | signature 6/7, combo 22/23 | Beast generate_cards (lead 1.8, too few cards); Mantis God + Fecundity |
| faeria | done 26 Oct | 24.8 / 5.9 | signature 9/15, archetype 5/9, combo 8/12, splash 0/2 | Khalim's Prayer + Zealous Crusader, Ruby Yak + Ulani's Medallion and two more combos need new link types; Yellow sacrifice (recipe) |
| duelyst | done 24 Oct, rechecked 26 Oct | 34.5 / 24.3 | signature 16/16, archetype 7/8, splash 1/1 | |
| sts1 | **next** | 40.5 / 27.6 | signature 9/18, archetype 5/9, combo 18/21 | Defect cost_condition, Silent draw (narrow leads) |
| marvel_snap | to do | 101.4 / 31.5 | combo 20/24 | |
| darkest_dungeon | done 24 Oct, rechecked 26 Oct | 48.0 / 26.6 | combo 6/7 | |
| sts2 | to do | 51.1 / 38.2 | signature 8/16, archetype 2/6, combo 0/2 | |
| gwent | to do | 65.2 / 77.9 | signature 15/22, archetype 7/8, combo 3/3 | Northern Realms activated (lost to merged-card counts) |
| hs_battlegrounds | to do | 49.4 / 46.2 | combo 9/13 | |
| runeterra | to do | 79.4 / 72.0 | signature 30/40, archetype 7/16, combo 7/19, splash 1/1 | Freljord resource_gain (lost to merged-card counts) |
| wh_aos_4th | to do | 138.8 / 164.3 | signature 12/47, archetype 4/18 | |
| wh_40k_10e | to do | 229.7 / 120.0 | signature 8/28, archetype 4/12, combo 5/8 | |
| shadowverse | to do | 103.8 / 72.3 | signature 17/22, archetype 8/13 | |
| hearthstone | to do | 56.2 / 62.2 | signature 37/57, archetype 12/34, combo 6/13, splash 7/9 | Deathknight control, Mage tribal, Shaman tribal (narrow leads); Druid swarm and draw (lost to merged-card counts) |
| mtg | to do | 115.7 / 126.2 | signature 46/48, archetype 8/10, combo 9/15, splash 12/15 | |
| lorcana | to do | 96.8 / 64.2 | signature 19/25, archetype 7/8, combo 12/12, splash 7/12 | |
| stormbound | to do | 44.1 / 67.3 | signature 6/17, archetype 6/10, combo 1/1 | |
| swu | to do | 140.0 / 75.4 | signature 17/20, archetype 6/8, combo 4/7, splash 2/3 | |
| tesl | to do | 105.4 / 68.8 | signature 11/15, archetype 6/9, combo 6/16 | |
| monster_train | to do | 58.3 / 66.6 | signature 6/14, archetype 4/7, combo 2/4 | |

## Per game
1. **Baseline:** `sh tools/game_check.sh <scratch> <game>` (about 40 s): mechanics coverage, key score, cases, regression, combos.
2. **Where the errors come from:** `tools/entry_diff.py <db> <game>` lists every wrong and missed tag per key entry with the method
   that made it (text_pattern = a pattern, claude_review = a review, via_keyword = inherited from a keyword entry). Most errors are
   not patterns. `tools/key_diag.py`, `tools/pattern_hits.py` (which pattern gives a tag), `tools/mechanic_gaps.py` (entries
   behind a mechanics GAP line) and the step log `<scratch>/gc_<game>.sqlite.steps.tsv` (which step changed a concept) help.
3. **Keyword entries first.** A keyword's tags reach every card that has it. If its entry is a wiki page (rule, then notes about
   single cards), tag the rule; a note's effect belongs to that card. Fix the keyword, not the holders.
4. **Patterns:** write all candidate lines, test them on the key with `tools/pattern_eval.py <db> <game> <file>` (right, wrong, and
   how many cards the matched keywords pass the tag to), keep the good ones, then build once. Fix generically: every entry with the
   same wording.
5. **Cases:** `tools/case_lead.py <db> <game> <faction:concept>` shows whether the faction leads, in the key and in the library.
   Under 1.3 times in the key: the case, the key or the data source is the problem, not the patterns. Verify combos against the
   game's wiki; add missing cards (below) rather than drop a true combo.
6. **The key:** check that its quotes are words of the card; propose corrections (Rules).
7. **Each try:** `game_check.sh`. Then re-run `tools/step3/key_patterns.py <scratch>/gc_<game>.sqlite <game>` and check once more.
8. **Present** (Rules), then after Kaptain's OK: `sh tools/reload_game.sh <scratch> <game>` (add `<game>=<cards.json>` to add
   cards), `compare_builds.py` against the library when anything shared changed, copy `<scratch>/reloaded.sqlite` over
   `three-bases-library.sqlite`, commit; push when Kaptain says so.
9. **Game file:** what the pass learned about the game ("The game"), and the case and key notes ("Notes from the patterns check").
   Update the table above.

**Things that silently undo a fix:** a review drop without a role also drops the `benefits`/`counters` tags (write `concept:does`);
reviews are applied in the old ids too, where `death_trigger` still means any death (write `other_death_trigger`); `!` lines
remove only text_pattern tags, and `pattern_fix.py` re-adds its decision patterns after them; a review or key change can break a
`regression.tsv` line (fix it in the same change). `benefits` and `counters` tags count as wrong in the score (the key lists what a
card does): do not chase them.

**Adding cards to a game already in the library:** `reload_game.sh <scratch> <game> <game>=<cards.json>`, never `build.sh` with a
load (it makes the game's built tags its base: every game came out worse). A card without tags is dropped; a card without text
needs a review entry keyed by its name. Fields the sources do not give stay empty.

## How a tag gets there (read before guessing)
A game's tags come from the whole build chain (`tools/build.sh`, function `steps`), not only from its pattern file. In order:
- `start_clean.py`: back to the frozen base tags (`make_base.py`; a reload makes the game's base from today's patterns).
- `game_patterns.py`: `patterns/_all.txt` (every game but Marvel Snap) and `patterns/<game>.txt`. The general patterns (table
  `concept_patterns`, game NULL) are in the frozen base already; they are not applied again.
  A line `!concept|regex` removes that concept's text_pattern tags where the regex matches and no other pattern of the concept
  matches; a line removed from a file takes its tags away.
- `kw_sync.py` (keyword tags inherited), `propagate.py`, `keyword_defs.py`, reviews (`reviews/*.json`).
- `outcome_tree.py`, `link_types.py` (concept relations), `cost_rules.py` (tags from the cost field); `trigger_pairs.py` re-applies every trigger pattern and gives
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
- **Times:** `game_check.sh` 40 s (wh_40k_10e about 2 min); `reload_game.sh` about 3 min; a full `build.sh` about 4.5 min and
  `compare_builds.py` about 3 min (run them in the background).

## Tools
- `tools/game_check.sh <scratch> <game>`: the build's steps on a one-game copy, then the game's measures (each try).
- `tools/entry_diff.py`, `tools/pattern_eval.py`, `tools/case_lead.py`: errors per entry with their source; candidate patterns on
  the key; does a faction lead in a mechanic.
- `tools/key_diag.py`, `tools/pattern_hits.py`, `tools/mechanic_gaps.py`, `tools/coverage.py <db> <game> 0 --mechanics
  tools/games/<game>.md`: older diagnosis helpers.
- `tools/reload_game.sh`, `tools/compare_builds.py`: the end of a pass. Times: `game_check.sh` 40 s (wh_40k_10e 2 min),
  `reload_game.sh` 3 min, full `build.sh` 4.5 min, `compare_builds.py` 3 min (run the long ones in the background).

## Change log
- 24 Oct: darkest_dungeon pass (key wrong 78.9 -> 57.6, missed 44.2 -> 26.6; skills on all enemy ranks have `multi_target_attack`).
  Shared: `multi_target_attack` under `damage`; `final_revert.py` restores only tags still shown right; ITB "in a row" ->
  `positional`; shared pools out of the faction comparison. Patterns: ITB explosions and Fire, 40k "selected to fight", Lorcana
  costs without a number.
- 24 Oct: duelyst pass (wrong 44.4 -> 37.7, missed 41.5 -> 27.5; signature 13/21 -> 16/16). Key: artifacts `merge_attach` + `buff`;
  tribal where a card picks or counts by tribe; Gigaloth `permanent_growth`. Cases removed where no faction lead (game file).
  Shared: "action bar" read as the hand; "transform ANY" possibly an enemy; `link_types.py` honours `!` lines.
- 26 Oct: damage types and adjacency (see Decisions; 117 key entries moved), `stat_gain` split into attack/defence gain (about 460
  key entries), keyword mentions the sentence denies are not inherited. into_the_breach pass (wrong 74.0 -> 47.0, missed 67.6 ->
  13.3, combos 6/6). darkest_dungeon and duelyst rechecked (`!random_effect` on plain "chance"; "all friendly/enemy minions" is
  `scope_global`, 18 Duelyst key entries).
- 26 Oct: speed: `query._anc` reads the tree once; `refast.py` pre-filters regexes (build steps 238 s -> about 160 s; identical
  output).
- 26 Oct: inscryption pass (key wrong 72.8 -> 50.4, missed 57.3 -> 26.9; signature 2/12 -> 6/7, combos 1/5 -> 22/23). Sigil entries
  tag their rule, not notes about single cards; costs tagged from the cost field; six missing cards added; 19 verified combos.
  Key (Kaptain): Stimulate, Enlarge, Marrow Sucker `scope_self`; Unkillable `return_to_hand`; Fledgling and Unkillable lose stat
  gains; Waterborne's and Many Lives' transform moved to Great Kraken and the Cat; the Mox sigil `resource_gain`; Fecundity
  `generate_cards`; Boulder and Frozen Opossum lose it. Shared (all games compared, real-world 508 -> 543 of 860, no key score
  worse): cost tags in signatures, the 25%/60% rule, merged cards counted, summon reactions (Duelyst undone), revive vs
  return_to_hand (27 key entries, definitions), 7 bulk stat-gain key tags removed, combos may name keywords and tribes,
  four concept relations (deathtouch + multi_attack / aoe_damage, free_play + on_play / copy), `_all.txt` lines tag every game.
- 26 Oct: faeria pass (key wrong 52.8 -> 24.8, missed 43.0 -> 5.9; combos 0/1 -> 8/12). Key (Kaptain): Flying is not evasion
  (39 entries) and the movement keywords are not terrain; land destruction, moving and taking lands are terrain; `scope_self` on
  50 self-only effects; hand discounts also `cost_reduction`; wild land `cost_type`; Aquatic `placement_rules` and `turn_end`.
  Library: keyword reviews (Taunt, Corrupt, Swallow, Aquatic, Flying), 30 Faeria pattern lines, wording-wide review drops,
  11 new verified combos, the case rule lowered to 1.3 times.

## Open, outside the game passes
- Tagging redesign: tags per effect instead of per card (`TAGGING_RECORDS.md`, proposal for Kaptain). It would settle area
  effects for any effect (not only damage) and the overlap of stat gains, temporary bonuses and growth.
- Cases removed in earlier passes under the old 1.5 rule that reach 1.3: Into the Breach signature Prime damage (1.42), Brute
  damage (1.30), Science damage_over_time (1.33); recheck them in that game's next pass.
- Keyword denial rule: it covers only the 7 games where the position rule is skipped (`kw_links.py` SKIP).
