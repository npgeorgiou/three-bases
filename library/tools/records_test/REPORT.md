# Tagging per effect: test report

Built by `tools/records_test/` on a copy of the database (TAGGING_RECORDS.md). Script numbers only;
the gold reading (step 2) and the read checks of step 3 are not in this report yet.

## Step 1: does it fly

Tags: all tags except cost and structure tags (data_rule, game_structure). Clean: the words that made the tag were found
and lie inside its row. Card-level: tags with no words in the text (hand-mapped whole-card tags), in the card row.
Excerpt: only an old fixed-length excerpt is stored and the patterns no longer find the words in it; clean when the whole excerpt lies in the row.
Pass: clean + card-level 98%+ in every game.

| game | tags | clean | card-level | of them excerpts | words cross rows | clean + card | rows | rows without effect | trigger rows without effect | pairs before | pairs after | pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| darkest_dungeon | 5251 | 75.6% | 1067 | 62 | 212 | 96.0% | 2230 | 45.5% | 300 of 752 | 1092 | 98 | FAIL |
| duelyst | 2696 | 87.5% | 316 | 199 | 20 | 99.3% | 966 | 12.2% | 67 of 368 | 660 | 575 | pass |
| faeria | 1796 | 90.8% | 129 | 82 | 36 | 98.0% | 722 | 16.5% | 43 of 240 | 494 | 403 | FAIL |
| gwent | 7104 | 94.8% | 347 | 474 | 22 | 99.7% | 2816 | 26.6% | 410 of 1278 | 2913 | 1697 | pass |
| hearthstone | 26164 | 96.1% | 882 | 960 | 145 | 99.4% | 10729 | 13.7% | 1082 of 4870 | 9305 | 6545 | pass |
| hs_battlegrounds | 7374 | 92.7% | 485 | 282 | 52 | 99.3% | 2752 | 22.5% | 275 of 1283 | 2175 | 1941 | pass |
| inscryption | 1186 | 82.7% | 190 | 247 | 15 | 98.7% | 610 | 37.7% | 63 of 131 | 443 | 246 | pass |
| into_the_breach | 1264 | 86.6% | 156 | 4 | 14 | 98.9% | 523 | 12.2% | 20 of 61 | 120 | 90 | pass |
| lorcana | 6119 | 97.5% | 62 | 199 | 93 | 98.5% | 2528 | 13.2% | 202 of 1105 | 2529 | 1129 | pass |
| marvel_snap | 3504 | 79.2% | 583 | 375 | 146 | 95.8% | 975 | 21.4% | 170 of 692 | 1024 | 785 | FAIL |
| monster_train | 847 | 81.6% | 126 | 10 | 30 | 96.5% | 422 | 14.2% | 32 of 81 | 130 | 149 | FAIL |
| mtg | 93226 | 96.4% | 1237 | 4418 | 2104 | 97.7% | 38892 | 16.0% | 2573 of 14029 | 37102 | 25449 | FAIL |
| runeterra | 10871 | 90.4% | 929 | 1090 | 117 | 98.9% | 4591 | 24.6% | 256 of 1143 | 4243 | 2098 | pass |
| shadowverse | 23639 | 96.4% | 405 | 828 | 444 | 98.1% | 9796 | 22.8% | 507 of 4237 | 10312 | 7059 | pass |
| stormbound | 578 | 100.0% | 0 | 2 | 0 | 100.0% | 191 | 10.5% | 18 of 159 | 183 | 179 | pass |
| sts1 | 2938 | 77.8% | 640 | 196 | 11 | 99.6% | 1097 | 14.9% | 43 of 306 | 563 | 502 | pass |
| sts2 | 4378 | 75.0% | 1060 | 30 | 34 | 99.2% | 1636 | 13.9% | 56 of 431 | 810 | 683 | pass |
| swu | 7135 | 93.8% | 146 | 334 | 293 | 95.9% | 2984 | 22.2% | 332 of 1368 | 3318 | 1907 | FAIL |
| tesl | 3271 | 92.0% | 219 | 155 | 43 | 98.7% | 1170 | 10.9% | 76 of 520 | 1023 | 882 | pass |
| wh_40k_10e | 23089 | 96.1% | 320 | 4632 | 580 | 97.5% | 8769 | 20.9% | 589 of 2092 | 8057 | 3852 | FAIL |
| wh_aos_4th | 13098 | 87.6% | 680 | 250 | 946 | 92.8% | 6205 | 35.2% | 1417 of 2437 | 3339 | 1386 | FAIL |

All games: clean 93.8%, clean + card 97.8%; outliers (words or excerpt across rows): 5357.

How the words were found: narrowed 162837, pattern 35332, excerpt 18433, keyword 14476, entry_level 9884, wordless 9682, note_text 3493, pair_clause 978, no_text 297.

## Step 2 (answer-key part): compound tags

Per game and concept on the key entries: old (today's tags) and new (computed from the rows, rows.py). Scope tags are unchanged.
P = right / tagged, R = found / key. Pass: no concept worse in any game (precision and recall both).

| game | concept | old tagged | old P | old R | new tagged | new P | new R | key | worse |
|---|---|---|---|---|---|---|---|---|---|
| darkest_dungeon | aoe_damage | 25 | 100.0% | 100.0% | 25 | 100.0% | 100.0% | 25 |  |
| darkest_dungeon | temporary_buff | 22 | 100.0% | 88.2% | 22 | 100.0% | 88.2% | 17 |  |
| darkest_dungeon | permanent_growth | 0 | - | 0.0% | 0 | - | 0.0% | 1 |  |
| darkest_dungeon | scope_multi | 2 | 100.0% | 100.0% | 2 | 100.0% | 100.0% | 26 |  |
| darkest_dungeon | scope_self | 35 | 11.4% | 100.0% | 35 | 11.4% | 100.0% | 4 |  |
| duelyst | aoe_damage | 25 | 100.0% | 96.2% | 27 | 96.3% | 96.2% | 26 | WORSE |
| duelyst | temporary_buff | 6 | 100.0% | 75.0% | 8 | 100.0% | 87.5% | 8 |  |
| duelyst | permanent_growth | 16 | 100.0% | 94.1% | 14 | 92.9% | 70.6% | 17 | WORSE |
| duelyst | scope_global | 20 | 100.0% | 92.6% | 20 | 100.0% | 92.6% | 27 |  |
| duelyst | scope_multi | 0 | - | 93.4% | 0 | - | 93.4% | 61 |  |
| faeria | aoe_damage | 10 | 100.0% | 90.9% | 15 | 93.3% | 90.9% | 11 | WORSE |
| faeria | temporary_buff | 4 | 100.0% | 80.0% | 5 | 100.0% | 80.0% | 5 |  |
| faeria | permanent_growth | 18 | 100.0% | 100.0% | 15 | 60.0% | 50.0% | 18 | WORSE |
| faeria | scope_global | 3 | 100.0% | 100.0% | 3 | 100.0% | 100.0% | 9 |  |
| faeria | scope_multi | 0 | - | 89.7% | 0 | - | 89.7% | 29 |  |
| faeria | scope_self | 48 | 100.0% | 96.0% | 48 | 100.0% | 96.0% | 50 |  |
| gwent | aoe_damage | 4 | 100.0% | 33.3% | 17 | 82.4% | 88.9% | 9 | WORSE |
| gwent | permanent_growth | 18 | 100.0% | 47.4% | 2 | 100.0% | 5.3% | 38 | WORSE |
| gwent | scope_global | 2 | 0.0% | 87.5% | 2 | 0.0% | 87.5% | 8 |  |
| gwent | scope_multi | 7 | 100.0% | 77.4% | 7 | 100.0% | 83.9% | 31 |  |
| hearthstone | aoe_damage | 26 | 96.2% | 92.6% | 34 | 82.4% | 96.3% | 27 | WORSE |
| hearthstone | temporary_buff | 3 | 100.0% | 33.3% | 8 | 87.5% | 83.3% | 6 | WORSE |
| hearthstone | permanent_growth | 5 | 40.0% | 22.2% | 7 | 85.7% | 66.7% | 9 |  |
| hearthstone | scope_global | 2 | 100.0% | 82.4% | 2 | 100.0% | 82.4% | 17 |  |
| hearthstone | scope_multi | 1 | 0.0% | 72.9% | 1 | 0.0% | 74.3% | 70 |  |
| hearthstone | scope_self | 5 | 0.0% | - | 5 | 0.0% | - | 0 |  |
| hs_battlegrounds | aoe_damage | 10 | 90.0% | 100.0% | 11 | 81.8% | 100.0% | 9 | WORSE |
| hs_battlegrounds | temporary_buff | 17 | 88.2% | 86.7% | 17 | 88.2% | 86.7% | 15 |  |
| hs_battlegrounds | permanent_growth | 17 | 94.1% | 72.7% | 12 | 66.7% | 36.4% | 22 | WORSE |
| hs_battlegrounds | scope_global | 2 | 100.0% | 100.0% | 2 | 100.0% | 100.0% | 5 |  |
| hs_battlegrounds | scope_multi | 0 | - | 72.7% | 0 | - | 72.7% | 22 |  |
| hs_battlegrounds | scope_self | 6 | 0.0% | - | 6 | 0.0% | - | 0 |  |
| inscryption | aoe_damage | 20 | 95.0% | 90.5% | 20 | 95.0% | 90.5% | 21 |  |
| inscryption | temporary_buff | 4 | 75.0% | 100.0% | 5 | 80.0% | 100.0% | 2 |  |
| inscryption | permanent_growth | 5 | 100.0% | 100.0% | 0 | - | 0.0% | 5 | WORSE |
| inscryption | scope_global | 1 | 0.0% | - | 1 | 0.0% | - | 0 |  |
| inscryption | scope_multi | 0 | - | 92.6% | 0 | - | 92.6% | 27 |  |
| inscryption | scope_self | 6 | 100.0% | 100.0% | 6 | 100.0% | 100.0% | 6 |  |
| into_the_breach | aoe_damage | 73 | 100.0% | 97.2% | 94 | 95.7% | 97.2% | 72 | WORSE |
| into_the_breach | temporary_buff | 6 | 83.3% | 50.0% | 6 | 83.3% | 50.0% | 4 |  |
| into_the_breach | scope_global | 1 | 100.0% | 100.0% | 1 | 100.0% | 100.0% | 1 |  |
| into_the_breach | scope_multi | 0 | - | 97.4% | 0 | - | 97.4% | 77 |  |
| lorcana | aoe_damage | 9 | 88.9% | 72.7% | 16 | 87.5% | 81.8% | 11 | WORSE |
| lorcana | temporary_buff | 51 | 74.5% | 92.7% | 55 | 70.9% | 95.1% | 41 | WORSE |
| lorcana | scope_global | 1 | 0.0% | 100.0% | 1 | 0.0% | 100.0% | 8 |  |
| lorcana | scope_multi | 0 | - | 67.7% | 0 | - | 71.0% | 31 |  |
| marvel_snap | permanent_growth | 3 | 66.7% | 28.6% | 5 | 80.0% | 57.1% | 7 |  |
| marvel_snap | scope_global | 12 | 8.3% | 100.0% | 12 | 8.3% | 100.0% | 18 |  |
| marvel_snap | scope_multi | 0 | - | 96.0% | 0 | - | 96.0% | 25 |  |
| marvel_snap | scope_self | 7 | 0.0% | - | 7 | 0.0% | - | 0 |  |
| monster_train | aoe_damage | 13 | 100.0% | 72.2% | 13 | 100.0% | 72.2% | 18 |  |
| monster_train | temporary_buff | 10 | 60.0% | 100.0% | 10 | 60.0% | 100.0% | 6 |  |
| monster_train | permanent_growth | 4 | 75.0% | 37.5% | 0 | - | 0.0% | 8 | WORSE |
| monster_train | scope_multi | 0 | - | 72.2% | 0 | - | 72.2% | 18 |  |
| mtg | aoe_damage | 5 | 100.0% | 50.0% | 31 | 48.4% | 75.0% | 8 | WORSE |
| mtg | temporary_buff | 88 | 89.8% | 100.0% | 102 | 83.3% | 100.0% | 51 | WORSE |
| mtg | permanent_growth | 28 | 78.6% | 88.0% | 2 | 50.0% | 4.0% | 25 | WORSE |
| mtg | scope_global | 4 | 100.0% | 66.7% | 4 | 100.0% | 66.7% | 39 |  |
| mtg | scope_multi | 0 | - | 52.8% | 0 | - | 56.2% | 89 |  |
| runeterra | aoe_damage | 5 | 100.0% | 71.4% | 12 | 100.0% | 85.7% | 7 |  |
| runeterra | temporary_buff | 20 | 95.0% | 82.6% | 25 | 92.0% | 87.0% | 23 | WORSE |
| runeterra | permanent_growth | 9 | 66.7% | 54.5% | 3 | 100.0% | 27.3% | 11 | WORSE |
| runeterra | scope_global | 1 | 100.0% | 100.0% | 1 | 100.0% | 100.0% | 6 |  |
| runeterra | scope_multi | 0 | - | 51.4% | 0 | - | 54.3% | 35 |  |
| shadowverse | aoe_damage | 20 | 100.0% | 90.9% | 29 | 86.2% | 100.0% | 22 | WORSE |
| shadowverse | temporary_buff | 0 | - | 0.0% | 11 | 27.3% | 100.0% | 1 |  |
| shadowverse | permanent_growth | 3 | 100.0% | 60.0% | 5 | 80.0% | 80.0% | 5 | WORSE |
| shadowverse | scope_global | 0 | - | 87.5% | 0 | - | 87.5% | 8 |  |
| shadowverse | scope_multi | 5 | 100.0% | 79.6% | 5 | 100.0% | 83.3% | 54 |  |
| stormbound | aoe_damage | 6 | 100.0% | 30.0% | 22 | 77.3% | 80.0% | 20 | WORSE |
| stormbound | permanent_growth | 6 | 100.0% | 66.7% | 0 | - | 0.0% | 9 | WORSE |
| stormbound | scope_global | 2 | 0.0% | - | 2 | 0.0% | - | 0 |  |
| stormbound | scope_multi | 0 | - | 26.1% | 0 | - | 73.9% | 23 |  |
| sts1 | aoe_damage | 15 | 100.0% | 93.8% | 18 | 94.4% | 100.0% | 16 | WORSE |
| sts1 | temporary_buff | 3 | 66.7% | 100.0% | 4 | 75.0% | 100.0% | 2 |  |
| sts1 | permanent_growth | 3 | 100.0% | 50.0% | 3 | 100.0% | 50.0% | 6 |  |
| sts1 | scope_global | 1 | 0.0% | - | 1 | 0.0% | - | 0 |  |
| sts1 | scope_multi | 5 | 80.0% | 100.0% | 5 | 80.0% | 100.0% | 19 |  |
| sts2 | aoe_damage | 18 | 100.0% | 100.0% | 21 | 95.2% | 100.0% | 18 | WORSE |
| sts2 | temporary_buff | 5 | 100.0% | 83.3% | 9 | 100.0% | 100.0% | 6 |  |
| sts2 | permanent_growth | 9 | 11.1% | 0.0% | 1 | 0.0% | 0.0% | 2 | WORSE |
| sts2 | scope_multi | 0 | - | 94.7% | 0 | - | 100.0% | 19 |  |
| swu | aoe_damage | 11 | 90.9% | 100.0% | 19 | 57.9% | 100.0% | 10 | WORSE |
| swu | temporary_buff | 41 | 97.6% | 88.9% | 50 | 86.0% | 93.3% | 45 | WORSE |
| swu | permanent_growth | 0 | - | 0.0% | 3 | 0.0% | 0.0% | 2 |  |
| swu | scope_global | 1 | 100.0% | 57.1% | 1 | 100.0% | 57.1% | 7 |  |
| swu | scope_multi | 0 | - | 48.1% | 0 | - | 48.1% | 27 |  |
| tesl | aoe_damage | 18 | 100.0% | 92.3% | 22 | 90.9% | 100.0% | 13 | WORSE |
| tesl | temporary_buff | 5 | 100.0% | 62.5% | 10 | 80.0% | 87.5% | 8 | WORSE |
| tesl | permanent_growth | 8 | 0.0% | 0.0% | 7 | 14.3% | 5.6% | 18 |  |
| tesl | scope_global | 2 | 0.0% | 100.0% | 2 | 0.0% | 100.0% | 4 |  |
| tesl | scope_multi | 0 | - | 82.6% | 0 | - | 91.3% | 23 |  |
| wh_40k_10e | aoe_damage | 121 | 92.6% | 97.3% | 143 | 90.2% | 100.0% | 112 | WORSE |
| wh_40k_10e | temporary_buff | 116 | 94.0% | 91.6% | 129 | 87.6% | 91.6% | 83 | WORSE |
| wh_40k_10e | permanent_growth | 3 | 0.0% | 0.0% | 0 | - | 0.0% | 3 |  |
| wh_40k_10e | scope_global | 1 | 0.0% | - | 1 | 0.0% | - | 0 |  |
| wh_40k_10e | scope_multi | 1 | 100.0% | 92.4% | 1 | 100.0% | 95.0% | 119 |  |
| wh_aos_4th | aoe_damage | 29 | 100.0% | 41.4% | 46 | 95.7% | 72.4% | 29 | WORSE |
| wh_aos_4th | temporary_buff | 76 | 85.5% | 62.2% | 134 | 71.6% | 79.3% | 82 | WORSE |
| wh_aos_4th | permanent_growth | 4 | 75.0% | 37.5% | 2 | 100.0% | 25.0% | 8 | WORSE |
| wh_aos_4th | scope_global | 1 | 100.0% | 66.7% | 1 | 100.0% | 66.7% | 3 |  |
| wh_aos_4th | scope_multi | 11 | 100.0% | 44.3% | 11 | 100.0% | 57.1% | 70 |  |

### Known errors

- Wild Avenger (faeria): wrong pairs today 3/4, after 0/4; pairs now: on_play -> movement
- Invincible (hearthstone): wrong pairs today 3/3, after 1/3 (death_trigger -> summon); pairs now: death_trigger -> attack_gain, death_trigger -> defence_gain, death_trigger -> summon, death_trigger -> taunt, on_play -> attack_gain, on_play -> defence_gain, on_play -> summon, on_play -> taunt
- Mortarion (wh_40k_10e): wrong pairs today 3/3, after 0/3; pairs now: death_trigger -> attack_now, death_trigger -> cheat_death, death_trigger -> temporary_buff, on_attack -> debuff, on_attack -> drawback, other_death_trigger -> attack_now, other_death_trigger -> cheat_death, other_death_trigger -> temporary_buff
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

Strongest layer, old: {'engine': 30, 'MISS': 2, 'relation': 17, 'role_tree': 5, 'role': 14, 'type': 4, 'keyword': 9, 'link': 1}; new: {'engine': 30, 'role': 15, 'MISS': 2, 'relation': 17, 'role_tree': 6, 'type': 3, 'keyword': 8, 'link': 1}.

## Verdict per game (script parts only)

| game | step 1 | step 2 key | step 3 combos |
|---|---|---|---|
| darkest_dungeon | FAIL | pass | - |
| duelyst | pass | FAIL | - |
| faeria | FAIL | FAIL | - |
| gwent | pass | FAIL | pass |
| hearthstone | pass | FAIL | pass |
| hs_battlegrounds | pass | FAIL | pass |
| inscryption | pass | FAIL | - |
| into_the_breach | pass | FAIL | - |
| lorcana | pass | FAIL | - |
| marvel_snap | FAIL | pass | pass |
| monster_train | FAIL | FAIL | - |
| mtg | FAIL | FAIL | pass |
| runeterra | pass | FAIL | pass |
| shadowverse | pass | FAIL | - |
| stormbound | pass | FAIL | - |
| sts1 | pass | FAIL | pass |
| sts2 | pass | FAIL | - |
| swu | FAIL | FAIL | - |
| tesl | pass | FAIL | - |
| wh_40k_10e | FAIL | FAIL | - |
| wh_aos_4th | FAIL | FAIL | - |
