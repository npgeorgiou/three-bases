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
  **Proposing is mandatory, not optional.** Whenever you learn something that makes a key tag wrong or missing (the card text shows it,
  a concept definition changed, a pattern now finds more cards, a later step gives better information), write the proposal in your
  report to Kaptain in the same step: the entries, what each card says (quote it), the tag to add or remove, and one yes/no
  question. Do not silently leave the key as it was and do not leave it for a later pass. If Kaptain has said "change the key
  where you are sure" for a task, apply the changes the card text settles and list every one under Status.
- **Report the game's own numbers**, before and after: key wrong and missed per 100 key entries, and its real-world cases per kind
  (signature, archetype, splash, combo). Library totals are not the result of a game's pass.
- **Shared changes** (`tools/patterns/_all.txt`, code in `tools/`, the concept tree) reach every game: present every game's numbers
  (`compare_builds.py`), not only the current game's.
- Never invent rules or mechanics; mark judgements and suggestions as Claude's.
- One game per pass, all 21 games. Faeria: first re-measure its reload on the corrected key, then the same check.
- **Summon reactions** (26 Oct 2026, Kaptain): a card that reacts to summons ("Whenever you summon a minion…") has the trigger
  (`on_ally_play`, or `on_enemy_enter` for the opponent's summons), never `summon`: it does not summon. The earlier rule that gave it
  `summon` was wrong and is undone in Duelyst and Inscryption.
- **Shared pools** (24 Oct 2026): Neutral, Colorless and Any are not factions; `factions.py` SHARED leaves them out of the
  signature and archetype comparison.
- **Cases the cards don't support** (24 Oct 2026): when the faction shows no lead in the cards (the mechanic is as common in other
  factions), remove the case and give the reason in the game's "Notes from the patterns check". Fix the key where it is wrong.
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

## Working fast (lessons of the Inscryption pass, 26 Oct 2026)
The Inscryption pass took many builds because patterns were tried before the errors were understood. Do it in this order:
1. **Find where each error comes from before changing anything.** `tools/entry_diff.py <db> <game>` lists every wrong and missed
   tag per key entry with the method that made it. In Inscryption most errors were not patterns: they were review files
   (claude_review) and tags inherited from keyword entries (via_keyword). A pattern cannot fix those.
2. **Keyword entries reach every card that has the keyword.** One wrong tag on a keyword is wrong on all its holders. Keyword
   entries can be wiki pages (rule line, then notes about single cards): tag the rule, not the notes; a note about one card belongs
   to that card. Fix the keyword, never the holders one by one.
3. **Test a pattern on the key before building.** `tools/pattern_eval.py <db> <game> <file>` gives right/wrong per line and how
   many cards the matched keywords pass the tag to. Write all candidate lines, keep the good ones, then build once.
4. **Check whether a case can be met before tagging for it.** `tools/case_lead.py <db> <game> <faction:concept>` shows the lead in
   the key and in the library. Under 1.5 times in the key: the case or the key is wrong, or the mechanic is not in the text
   (Inscryption costs are in the cost field: `cost_rules.py`). Patterns cannot fix that.
5. **Check the key's quotes.** A quote that is not words of the card (a definition, a keyword name for an unrelated tag) marks a
   bulk addition: verify it against the card text (Unkillable's "health goes up" was one).
6. **Build rarely.** `game_check.sh` once per batch of changes; the full build and `compare_builds.py` once at the end for shared
   changes. Diff two builds per entry instead of rebuilding to guess.
7. **Things that silently undo a fix:** a review drop without a role also drops the `benefits`/`counters` tags (write
   `concept:does`); reviews are applied in the old ids too, where `death_trigger` still means any death (write
   `other_death_trigger`); `!` lines remove only text_pattern tags, and `pattern_fix.py` re-adds its decision patterns after them;
   a review or key change can break a `regression.tsv` line: fix the line in the same change.
8. **Scores:** `benefits` and `counters` tags count as wrong (the key lists what a card does); do not chase them.
9. **Reporting:** one short message: what changed, then the decisions needed, each with the situation explained for someone who
   has not played the game. Push only when Kaptain says "push".

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
- **Times:** `game_check.sh` 40 s (wh_40k_10e about 2 min); `reload_game.sh` about 3 min; a full `build.sh` about 4.5 min and
  `compare_builds.py` about 3 min (run them in the background).

## Tools
- `tools/game_check.sh <scratch> <game>`: the build's steps on a one-game copy (`build.sh --steps`), then the game's mechanics
  coverage, key score, real-world cases, regression lines and combo misses. The one-game base is cached until the library changes.
- `tools/coverage.py <db> <game> 0 --mechanics tools/games/<game>.md`: the mechanics check alone.
- `tools/mechanic_gaps.py`, `tools/key_diag.py`, `tools/pattern_hits.py`: the diagnosis helpers above.
- `tools/entry_diff.py`, `tools/pattern_eval.py`, `tools/case_lead.py`: per-entry errors with their source, candidate patterns
  tested on the key, and whether a faction leads in a mechanic (see "Working fast").

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
- Cases missed since shared pools left the comparison (24 Oct 2026; each a narrow lead now under 1.5 times): check them in
  their game's pass, tagging first: hearthstone Deathknight control and board_presence, Mage tribal and board_presence (splash),
  Demonhunter draw, Shaman tribal; shadowverse Swordcraft tribal; sts1 Defect cost_condition, Silent draw; tesl Willpower
  board_presence.
- Damage types, shared (26 Oct 2026, Kaptain's rules): `multi_target_attack` = several separately named targets (all chosen, or one chosen plus a fixed one: "4 to a minion and your general"); `aoe_damage` = damage reaching several units without choosing each (around the target, a row, all; full or reduced); new `random_target` under `random_effect` = a random existing target; `adjacency` = neighbours for any purpose; `area_templates` = a named shape (plain "adjacent" is `adjacency`). Cleave/sweep/"attacks each" moved to `aoe_damage`; 112 key entries and 66 old hand reviews moved with them; `chain_damage` was not added (almost no wording). Gwent "damage N units by X" is read as chosen targets (Kaptain). Smoke is `attack_lock`.
- into_the_breach: **done** 26 Oct 2026 (key wrong 74.0 → 47.0, missed 67.6 → 13.3 per 100; combos 1/6 → 6/6: the 5 new combo cases are in the game file with their sources; 10 cases that showed no lead of 1.5 times were removed, reasons in the game file).
- Shared fixes 26 Oct 2026 (damage types, adjacency, attack/defence gain): `multi_target_attack` = player-chosen targets, `aoe_damage` = damage reaching several without choosing each, new `random_target`; `adjacency` vocabulary widened per game (adjacent, nearby, surrounding, bordering, next to, left/right) with the key corrected where the library was right; `stat_gain` split into `attack_gain` and `defence_gain` (a card whose text does not name the stat keeps `stat_gain`; single-stat games Gwent, Stormbound, Marvel Snap are not split); relations `forced_movement`, `movement`, `summon` synergize with `adjacency`, `forced_movement` with `area_templates`, `swap` with `terrain`, `attack_gain` with `on_kill`; keyword mentions that the sentence denies ("cannot", "unaffected", "immune") no longer inherit the keyword's tags. Into the Breach done (wrong 74.0 → 48.6, missed 67.6 → 13.3, all 6 combos met).
- Key changes of 26 Oct 2026 (Kaptain: "change the key if you are sure"; every one is settled by the card text): `multi_target_attack` → `aoe_damage` (or dropped) on 117 entries in 8 games; Into the Breach: smoke entries `suppress` → `attack_lock`, `silence` removed from 3 A.C.I.D. entries, `adjacency` +52, `terrain` +12, `ranged` +8, `attack_lock` +18; `adjacency` added where the library tag is right (Stormbound 65 "surrounding/bordering" cards, Inscryption 13, Duelyst 9, others a few); `attack_gain`/`defence_gain` added where the text says "+N attack", "+N/+M", "gain N Strength", Rage/Armor (about 460 entries in 18 games); `random_target` on 2; `summon` on Gwent Tuirseach Skirmisher, Eist Tuirseach and Runeterra Priestess of Desert Light; `forced_movement` on Inscryption Fish Hook.
- Speed (26 Oct 2026): `realworld.py` took 79 s and `combo_check.py` 40 s because `query._anc` asked the database for a concept's ancestors about 29,500 times per run; it now reads the tree once (1.3 s each, same results). `trigger_effect` got an index on `entity` (`indexes.py`). The rest of a full build (now about 4.5 minutes) is the 38 steps over all games: in a one-game timing `trigger_pairs.py` is 35% (6.7 million regex searches, two runs), `pattern_fix.py` 10%, `step_log.py` 15%, `regression.py` 11%. These are Python regex loops, not database queries, so moving them into SQL would not help; the fixes are fewer regex passes (cache each clause's matches, build the per-game pattern lists once) and a cheaper `step_log.py`. `compare_builds.py` runs `realworld.py` twice, so it is faster too.
- Darkest Dungeon and Duelyst rechecked 26 Oct 2026 under the damage rules: darkest_dungeon wrong 50.6 → 46.8 (`!random_effect` on plain "chance"); duelyst wrong 33.9 → 32.7, missed 26.6 → 23.4 (rows are zones, not `area_templates`; "in this row" and "in front" are `aoe_damage`/`adjacency`; "all friendly/enemy minions" is `scope_global`, Kaptain 26 Oct 2026, 18 key entries changed from `scope_multi` or extended; Lux Ignis and Dauntless Advance stay `scope_multi`; lines like "in one straight line" are excluded).
- Speed, second part (26 Oct 2026): `tools/refast.py` rejects a pattern with a plain substring test of a literal it must contain before running the regex; `trigger_pairs.py` and `pattern_fix.py` use it. The tag, link, trigger-pair and faction tables of a full build are identical to the build before (0 differences), and the steps of a build take 154-161 s instead of 238 s (`trigger_pairs.py` 139 s → 75 s, `pattern_fix.py` 41 s → 21 s). `build.sh` now prints the seconds each step takes (`time:` lines), so the next slow step is easy to see; `step_log.py` takes 26 s in all and is left as it is.
- Into the Breach signature case Ranged removed (26 Oct 2026): `ranged` is on 46% of the cards, above the 25% bound.
- inscryption: **done** 26 Oct 2026 (key wrong 72.8 -> 49.6, missed 57.3 -> 26.9 per 100; signature 1/12 -> 5/7, combos 1/5).
  Sigil entries are wiki pages: tags from notes about single cards no longer reach every card with the sigil. Cases (reasons in the
  game file): removed Beast deathtouch, Undead death_trigger, Technology resource_gain, aura, autonomous_units, Undead sacrifice
  (the hammer is an item) and the Undead archetype; Magick multiple_resources -> cost_type; added Undead resource_gain.
  Key (Kaptain): Stimulate, Enlarge, Marrow Sucker `scope_self`; Unkillable `return_to_hand`, no `defence_gain`; Fledgling no
  `attack_gain`/`defence_gain`; Waterborne's `transform`/`random_effect` moved to Great Kraken, Many Lives' `transform` to the Cat;
  the Mox sigil gives `resource_gain`, not `multiple_resources`.
- Shared, 26 Oct 2026 (Kaptain; all games compared, none worse, real-world 508 -> 518 of 842):
  - `cost_rules.py` (new build step): tags from the cost field where cards print it apart from the text (Inscryption: Blood ->
    `sacrifice` as the cost, Bones and Mox -> `cost_type`). Faction signatures count cost tags (`signature.py`).
  - A mechanic on more than 25% of the cards is still a signature when one faction holds at least 60% of it.
  - Summon reactions have the trigger, never `summon` (see Rules); undone in Duelyst (7 cards) and Inscryption.
  - `revive` is back into play; back to hand (when it dies, or from the discard pile or graveyard) is `return_to_hand`. Definitions
    changed; 27 key entries moved (MTG, Lorcana, Hearthstone, Faeria, Marvel Snap, Monster Train, Shadowverse, Inscryption);
    `patterns/_all.txt` lines now tag every game (`game_patterns.py`); a card from your own discard pile counts as yours.
  - 26 Oct bulk `attack_gain`/`defence_gain` key tags quoted the definition, not the card: 458 checked, 7 wrong removed
    (Darkest Dungeon resistances and healing received, Space Prism capacity, Shadowverse Forte, 40k Masters of the Maelstrom).
    Warhammer "+1 to Hit/Wound/save rolls" count as gains (Kaptain).
  - `trigger_pairs.py`: "the start/end of the battle, phase, run, fight, game" is not a turn trigger. `key_wins.py`: a keyword's
    drop also reaches the copies its cards inherited. `load_cards.py`: a reload keeps entries without an external id.
- Inscryption combos (26 Oct 2026, Kaptain's list, verified against the wiki; doubtful ones left out): 19 added, combos 21/23.
  Six missing cards added from readable pages (`tools/convert/inscryption_missing_cards.json`: Squirrel, Rabbit, Geck, Urayuli,
  Child 13, Junior Sage). Shared: combo cases may name a keyword or a tribe and follow merges (`query._ent`, `realworld.py`); a tribe
  and a keyword connect when a card of the tribe bears the keyword; concept relations deathtouch + multi_attack / aoe_damage,
  free_play + on_play / copy; faction counts weigh merged cards (`signature.py`); `drop_untagged.py` keeps entries a review names;
  `reload_game.sh` takes new cards. All games: real-world 529 -> 542 of 860, key scores unchanged outside Inscryption; newly
  missed: gwent Northern Realms activated, hearthstone Druid swarm and draw, runeterra Freljord resource_gain (shares changed by
  the merged-card weights).
- Next: (1) the other games in the order of `tools/key/key.py` GAMES, faeria next: follow this file's procedure; check the
  narrow-lead cases listed above in each, and key tags whose quote is not in the card text. (2) Nothing open on speed (see the
  Speed note). (3) Keyword denial rule: it covers only the 7 games where the position rule is skipped (`kw_links.py` SKIP); other
  games are covered by the position rule.
