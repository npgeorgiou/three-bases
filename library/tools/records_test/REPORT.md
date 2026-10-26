# Tagging per effect: test report

Built by `tools/records_test/` on a copy of the database (TAGGING_RECORDS.md). Script numbers only;
the gold reading (step 2) and the read checks of step 3 are not in this report yet.

## Step 1: does it fly

Tags: all tags except cost and structure tags (data_rule, game_structure), which describe the whole entry. Placed: in one
ability and one piece, the matched words inside both. Pass: 98%+ placed in every game.

| game | tags | placed (one ability+piece) | words cross pieces | words cross abilities | excerpt crosses (words unknown) | nowhere | no text | abilities without effect | pieces with two effects | pairs before | pairs after | pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| darkest_dungeon | 5251 | 77.6% | 0 | 140 | 74 | 964 | 0 | 70.4% of 4756 | 183 of 4762 | 1092 | 36 | FAIL |
| duelyst | 2696 | 95.8% | 15 | 4 | 19 | 76 | 0 | 12.0% of 1058 | 360 of 1104 | 660 | 650 | FAIL |
| faeria | 1796 | 93.7% | 8 | 16 | 8 | 81 | 0 | 20.7% of 828 | 229 of 893 | 494 | 460 | FAIL |
| gwent | 7104 | 96.4% | 52 | 10 | 23 | 170 | 0 | 32.1% of 3042 | 557 of 3445 | 2913 | 2202 | FAIL |
| hearthstone | 26164 | 97.3% | 79 | 115 | 152 | 360 | 0 | 19.9% of 12560 | 3290 of 13212 | 9305 | 6694 | FAIL |
| hs_battlegrounds | 7374 | 94.1% | 57 | 34 | 80 | 246 | 15 | 32.6% of 3329 | 728 of 3515 | 2175 | 2041 | FAIL |
| inscryption | 1186 | 83.6% | 4 | 2 | 20 | 155 | 13 | 93.9% of 6239 | 78 of 6352 | 443 | 251 | FAIL |
| into_the_breach | 1264 | 88.6% | 12 | 5 | 4 | 123 | 0 | 64.4% of 1613 | 150 of 1756 | 120 | 84 | FAIL |
| lorcana | 6119 | 98.4% | 41 | 9 | 15 | 32 | 0 | 29.8% of 3233 | 554 of 3429 | 2529 | 1163 | pass |
| marvel_snap | 3504 | 89.7% | 42 | 35 | 130 | 135 | 20 | 18.2% of 1091 | 331 of 1138 | 1024 | 977 | FAIL |
| monster_train | 847 | 84.2% | 4 | 14 | 4 | 6 | 106 | 26.7% of 498 | 107 of 549 | 130 | 158 | FAIL |
| mtg | 93226 | 96.1% | 450 | 553 | 1620 | 910 | 99 | 37.5% of 56736 | 12118 of 60647 | 37102 | 22392 | FAIL |
| runeterra | 10871 | 93.2% | 197 | 32 | 62 | 452 | 0 | 27.7% of 5028 | 1221 of 5444 | 4243 | 2484 | FAIL |
| shadowverse | 23639 | 96.1% | 77 | 126 | 361 | 330 | 23 | 35.7% of 13856 | 2383 of 14971 | 10312 | 5748 | FAIL |
| stormbound | 578 | 100.0% | 0 | 0 | 0 | 0 | 0 | 16.9% of 219 | 24 of 242 | 183 | 173 | pass |
| sts1 | 2938 | 90.8% | 15 | 5 | 5 | 244 | 0 | 25.7% of 1589 | 249 of 1630 | 563 | 475 | FAIL |
| sts2 | 4378 | 90.5% | 58 | 4 | 16 | 339 | 0 | 31.4% of 2640 | 350 of 2704 | 810 | 607 | FAIL |
| swu | 7135 | 95.7% | 11 | 71 | 113 | 113 | 0 | 43.1% of 4395 | 986 of 4545 | 3318 | 1695 | FAIL |
| tesl | 3271 | 95.7% | 8 | 41 | 6 | 65 | 21 | 19.8% of 1354 | 477 of 1417 | 1023 | 924 | FAIL |
| wh_40k_10e | 23089 | 96.4% | 75 | 69 | 408 | 279 | 0 | 50.1% of 14659 | 2303 of 15705 | 8057 | 2663 | FAIL |
| wh_aos_4th | 13098 | 88.5% | 70 | 53 | 792 | 586 | 0 | 68.2% of 15016 | 874 of 16117 | 3339 | 680 | FAIL |

All games: 94.9% placed; outliers (nowhere 5666, words across pieces 1275, across abilities 1338, excerpts across 3912): 12191.

How tags were placed: narrowed 162837, pattern 35333, span 18433, keyword 14469, entry_level 9884, nowhere 5666, only_ability 3854, note_text 3493, pair_clause 978, no_text 297, only_trigger 168.

## Step 2 (answer-key part): compound tags

Per game and concept on the key entries: old (today) and new (compound kept only when its piece holds its base effect).
P = right / tagged, R = found / key. Pass: no concept worse in any game (precision and recall both).

| game | concept | old tagged | old P | old R | new tagged | new P | new R | key | worse |
|---|---|---|---|---|---|---|---|---|---|
| darkest_dungeon | aoe_damage | 25 | 100.0% | 100.0% | 25 | 100.0% | 100.0% | 25 |  |
| darkest_dungeon | temporary_buff | 22 | 100.0% | 88.2% | 7 | 100.0% | 0.0% | 17 | WORSE |
| darkest_dungeon | permanent_growth | 0 | - | 0.0% | 0 | - | 0.0% | 1 |  |
| darkest_dungeon | scope_multi | 2 | 100.0% | 100.0% | 2 | 100.0% | 100.0% | 26 |  |
| darkest_dungeon | scope_self | 35 | 11.4% | 100.0% | 35 | 11.4% | 100.0% | 4 |  |
| duelyst | aoe_damage | 25 | 100.0% | 96.2% | 25 | 100.0% | 96.2% | 26 |  |
| duelyst | temporary_buff | 6 | 100.0% | 75.0% | 6 | 100.0% | 75.0% | 8 |  |
| duelyst | permanent_growth | 16 | 100.0% | 94.1% | 15 | 100.0% | 88.2% | 17 | WORSE |
| duelyst | scope_global | 20 | 100.0% | 92.6% | 20 | 100.0% | 92.6% | 27 |  |
| duelyst | scope_multi | 0 | - | 93.4% | 0 | - | 93.4% | 61 |  |
| faeria | aoe_damage | 10 | 100.0% | 90.9% | 10 | 100.0% | 90.9% | 11 |  |
| faeria | temporary_buff | 4 | 100.0% | 80.0% | 4 | 100.0% | 80.0% | 5 |  |
| faeria | permanent_growth | 18 | 100.0% | 100.0% | 17 | 100.0% | 94.4% | 18 | WORSE |
| faeria | scope_global | 3 | 100.0% | 100.0% | 3 | 100.0% | 100.0% | 9 |  |
| faeria | scope_multi | 0 | - | 89.7% | 0 | - | 89.7% | 29 |  |
| faeria | scope_self | 48 | 100.0% | 96.0% | 48 | 100.0% | 96.0% | 50 |  |
| gwent | aoe_damage | 4 | 100.0% | 33.3% | 4 | 100.0% | 33.3% | 9 |  |
| gwent | permanent_growth | 18 | 100.0% | 47.4% | 18 | 100.0% | 47.4% | 38 |  |
| gwent | scope_global | 2 | 0.0% | 87.5% | 2 | 0.0% | 87.5% | 8 |  |
| gwent | scope_multi | 7 | 100.0% | 77.4% | 7 | 100.0% | 77.4% | 31 |  |
| hearthstone | aoe_damage | 26 | 96.2% | 92.6% | 26 | 96.2% | 92.6% | 27 |  |
| hearthstone | temporary_buff | 3 | 100.0% | 33.3% | 3 | 100.0% | 33.3% | 6 |  |
| hearthstone | permanent_growth | 5 | 40.0% | 22.2% | 5 | 40.0% | 22.2% | 9 |  |
| hearthstone | scope_global | 2 | 100.0% | 82.4% | 2 | 100.0% | 82.4% | 17 |  |
| hearthstone | scope_multi | 1 | 0.0% | 72.9% | 1 | 0.0% | 72.9% | 70 |  |
| hearthstone | scope_self | 5 | 0.0% | - | 5 | 0.0% | - | 0 |  |
| hs_battlegrounds | aoe_damage | 10 | 90.0% | 100.0% | 10 | 90.0% | 100.0% | 9 |  |
| hs_battlegrounds | temporary_buff | 17 | 88.2% | 86.7% | 15 | 86.7% | 73.3% | 15 | WORSE |
| hs_battlegrounds | permanent_growth | 17 | 94.1% | 72.7% | 17 | 94.1% | 72.7% | 22 |  |
| hs_battlegrounds | scope_global | 2 | 100.0% | 100.0% | 2 | 100.0% | 100.0% | 5 |  |
| hs_battlegrounds | scope_multi | 0 | - | 72.7% | 0 | - | 72.7% | 22 |  |
| hs_battlegrounds | scope_self | 6 | 0.0% | - | 6 | 0.0% | - | 0 |  |
| inscryption | aoe_damage | 20 | 95.0% | 90.5% | 20 | 95.0% | 90.5% | 21 |  |
| inscryption | temporary_buff | 4 | 75.0% | 100.0% | 4 | 75.0% | 100.0% | 2 |  |
| inscryption | permanent_growth | 5 | 100.0% | 100.0% | 5 | 100.0% | 100.0% | 5 |  |
| inscryption | scope_global | 1 | 0.0% | - | 1 | 0.0% | - | 0 |  |
| inscryption | scope_multi | 0 | - | 92.6% | 0 | - | 92.6% | 27 |  |
| inscryption | scope_self | 6 | 100.0% | 100.0% | 4 | 100.0% | 66.7% | 6 | WORSE |
| into_the_breach | aoe_damage | 73 | 100.0% | 97.2% | 63 | 100.0% | 87.5% | 72 | WORSE |
| into_the_breach | temporary_buff | 6 | 83.3% | 50.0% | 6 | 83.3% | 50.0% | 4 |  |
| into_the_breach | scope_global | 1 | 100.0% | 100.0% | 1 | 100.0% | 100.0% | 1 |  |
| into_the_breach | scope_multi | 0 | - | 97.4% | 0 | - | 88.3% | 77 | WORSE |
| lorcana | aoe_damage | 9 | 88.9% | 72.7% | 9 | 88.9% | 72.7% | 11 |  |
| lorcana | temporary_buff | 51 | 74.5% | 92.7% | 51 | 74.5% | 92.7% | 41 |  |
| lorcana | scope_global | 1 | 0.0% | 100.0% | 1 | 0.0% | 100.0% | 8 |  |
| lorcana | scope_multi | 0 | - | 67.7% | 0 | - | 67.7% | 31 |  |
| marvel_snap | permanent_growth | 3 | 66.7% | 28.6% | 3 | 66.7% | 28.6% | 7 |  |
| marvel_snap | scope_global | 12 | 8.3% | 100.0% | 12 | 8.3% | 100.0% | 18 |  |
| marvel_snap | scope_multi | 0 | - | 96.0% | 0 | - | 96.0% | 25 |  |
| marvel_snap | scope_self | 7 | 0.0% | - | 7 | 0.0% | - | 0 |  |
| monster_train | aoe_damage | 13 | 100.0% | 72.2% | 13 | 100.0% | 72.2% | 18 |  |
| monster_train | temporary_buff | 10 | 60.0% | 100.0% | 10 | 60.0% | 100.0% | 6 |  |
| monster_train | permanent_growth | 4 | 75.0% | 37.5% | 4 | 75.0% | 37.5% | 8 |  |
| monster_train | scope_multi | 0 | - | 72.2% | 0 | - | 72.2% | 18 |  |
| mtg | aoe_damage | 5 | 100.0% | 50.0% | 5 | 100.0% | 50.0% | 8 |  |
| mtg | temporary_buff | 88 | 89.8% | 100.0% | 88 | 89.8% | 100.0% | 51 |  |
| mtg | permanent_growth | 28 | 78.6% | 88.0% | 28 | 78.6% | 88.0% | 25 |  |
| mtg | scope_global | 4 | 100.0% | 66.7% | 4 | 100.0% | 66.7% | 39 |  |
| mtg | scope_multi | 0 | - | 52.8% | 0 | - | 52.8% | 89 |  |
| runeterra | aoe_damage | 5 | 100.0% | 71.4% | 5 | 100.0% | 71.4% | 7 |  |
| runeterra | temporary_buff | 20 | 95.0% | 82.6% | 17 | 94.1% | 69.6% | 23 | WORSE |
| runeterra | permanent_growth | 9 | 66.7% | 54.5% | 9 | 66.7% | 54.5% | 11 |  |
| runeterra | scope_global | 1 | 100.0% | 100.0% | 1 | 100.0% | 100.0% | 6 |  |
| runeterra | scope_multi | 0 | - | 51.4% | 0 | - | 48.6% | 35 | WORSE |
| shadowverse | aoe_damage | 20 | 100.0% | 90.9% | 20 | 100.0% | 90.9% | 22 |  |
| shadowverse | temporary_buff | 0 | - | 0.0% | 0 | - | 0.0% | 1 |  |
| shadowverse | permanent_growth | 3 | 100.0% | 60.0% | 3 | 100.0% | 60.0% | 5 |  |
| shadowverse | scope_global | 0 | - | 87.5% | 0 | - | 87.5% | 8 |  |
| shadowverse | scope_multi | 5 | 100.0% | 79.6% | 5 | 100.0% | 79.6% | 54 |  |
| stormbound | aoe_damage | 6 | 100.0% | 30.0% | 6 | 100.0% | 30.0% | 20 |  |
| stormbound | permanent_growth | 6 | 100.0% | 66.7% | 6 | 100.0% | 66.7% | 9 |  |
| stormbound | scope_global | 2 | 0.0% | - | 2 | 0.0% | - | 0 |  |
| stormbound | scope_multi | 0 | - | 26.1% | 0 | - | 26.1% | 23 |  |
| sts1 | aoe_damage | 15 | 100.0% | 93.8% | 15 | 100.0% | 93.8% | 16 |  |
| sts1 | temporary_buff | 3 | 66.7% | 100.0% | 3 | 66.7% | 100.0% | 2 |  |
| sts1 | permanent_growth | 3 | 100.0% | 50.0% | 3 | 100.0% | 50.0% | 6 |  |
| sts1 | scope_global | 1 | 0.0% | - | 1 | 0.0% | - | 0 |  |
| sts1 | scope_multi | 5 | 80.0% | 100.0% | 5 | 80.0% | 100.0% | 19 |  |
| sts2 | aoe_damage | 18 | 100.0% | 100.0% | 18 | 100.0% | 100.0% | 18 |  |
| sts2 | temporary_buff | 5 | 100.0% | 83.3% | 5 | 100.0% | 83.3% | 6 |  |
| sts2 | permanent_growth | 9 | 11.1% | 0.0% | 9 | 11.1% | 0.0% | 2 |  |
| sts2 | scope_multi | 0 | - | 94.7% | 0 | - | 94.7% | 19 |  |
| swu | aoe_damage | 11 | 90.9% | 100.0% | 11 | 90.9% | 100.0% | 10 |  |
| swu | temporary_buff | 41 | 97.6% | 88.9% | 41 | 97.6% | 88.9% | 45 |  |
| swu | permanent_growth | 0 | - | 0.0% | 0 | - | 0.0% | 2 |  |
| swu | scope_global | 1 | 100.0% | 57.1% | 1 | 100.0% | 57.1% | 7 |  |
| swu | scope_multi | 0 | - | 48.1% | 0 | - | 48.1% | 27 |  |
| tesl | aoe_damage | 18 | 100.0% | 92.3% | 18 | 100.0% | 92.3% | 13 |  |
| tesl | temporary_buff | 5 | 100.0% | 62.5% | 5 | 100.0% | 62.5% | 8 |  |
| tesl | permanent_growth | 8 | 0.0% | 0.0% | 8 | 0.0% | 0.0% | 18 |  |
| tesl | scope_global | 2 | 0.0% | 100.0% | 2 | 0.0% | 100.0% | 4 |  |
| tesl | scope_multi | 0 | - | 82.6% | 0 | - | 82.6% | 23 |  |
| wh_40k_10e | aoe_damage | 121 | 92.6% | 97.3% | 121 | 92.6% | 97.3% | 112 |  |
| wh_40k_10e | temporary_buff | 116 | 94.0% | 91.6% | 116 | 94.0% | 91.6% | 83 |  |
| wh_40k_10e | permanent_growth | 3 | 0.0% | 0.0% | 3 | 0.0% | 0.0% | 3 |  |
| wh_40k_10e | scope_global | 1 | 0.0% | - | 1 | 0.0% | - | 0 |  |
| wh_40k_10e | scope_multi | 1 | 100.0% | 92.4% | 1 | 100.0% | 92.4% | 119 |  |
| wh_aos_4th | aoe_damage | 29 | 100.0% | 41.4% | 29 | 100.0% | 41.4% | 29 |  |
| wh_aos_4th | temporary_buff | 76 | 85.5% | 62.2% | 76 | 85.5% | 62.2% | 82 |  |
| wh_aos_4th | permanent_growth | 4 | 75.0% | 37.5% | 4 | 75.0% | 37.5% | 8 |  |
| wh_aos_4th | scope_global | 1 | 100.0% | 66.7% | 1 | 100.0% | 66.7% | 3 |  |
| wh_aos_4th | scope_multi | 11 | 100.0% | 44.3% | 11 | 100.0% | 44.3% | 70 |  |

### Known errors

- Wild Avenger (faeria): wrong pairs today 3/4, after 0/4; pairs now: on_play -> movement
- Invincible (hearthstone): wrong pairs today 3/3, after 0/3; pairs now: death_trigger -> attack_gain, death_trigger -> defence_gain, death_trigger -> taunt, on_play -> attack_gain, on_play -> defence_gain, on_play -> taunt
- Mortarion (wh_40k_10e): wrong pairs today 3/3, after 0/3; pairs now: on_attack -> debuff, on_attack -> drawback, other_death_trigger -> temporary_buff
- Buzz Lightyear - Jungle Ranger (lorcana): wrong pairs today 2/2, after 0/2; pairs now: on_ally_play -> stat_gain, on_ally_play -> summon, on_ally_play -> temporary_buff, on_play -> recycle, on_spell -> stat_gain, on_spell -> summon, on_spell -> temporary_buff

## Step 3 (combos part): `combo_check.py` on old and new

| game | known combos | found old | found new |
|---|---|---|---|
| gwent | 1 | 1 | 1 |
| hearthstone | 18 | 17 | 17 |
| hs_battlegrounds | 5 | 5 | 5 |
| marvel_snap | 10 | 10 | 10 |
| mtg | 27 | 26 | 26 |
| runeterra | 6 | 6 | 6 |
| sts1 | 15 | 15 | 15 |

Strongest layer, old: {'engine': 30, 'MISS': 2, 'relation': 17, 'role_tree': 5, 'role': 14, 'type': 4, 'keyword': 9, 'link': 1}; new: {'engine': 31, 'role': 15, 'MISS': 2, 'relation': 17, 'role_tree': 5, 'type': 3, 'keyword': 8, 'link': 1}.

## Verdict per game (script parts only)

| game | step 1 | step 2 key | step 3 combos |
|---|---|---|---|
| darkest_dungeon | FAIL | FAIL | - |
| duelyst | FAIL | FAIL | - |
| faeria | FAIL | FAIL | - |
| gwent | FAIL | pass | pass |
| hearthstone | FAIL | pass | pass |
| hs_battlegrounds | FAIL | FAIL | pass |
| inscryption | FAIL | FAIL | - |
| into_the_breach | FAIL | FAIL | - |
| lorcana | pass | pass | - |
| marvel_snap | FAIL | pass | pass |
| monster_train | FAIL | pass | - |
| mtg | FAIL | pass | pass |
| runeterra | FAIL | FAIL | pass |
| shadowverse | FAIL | pass | - |
| stormbound | pass | pass | - |
| sts1 | FAIL | pass | pass |
| sts2 | FAIL | pass | - |
| swu | FAIL | pass | - |
| tesl | FAIL | pass | - |
| wh_40k_10e | FAIL | pass | - |
| wh_aos_4th | FAIL | pass | - |
