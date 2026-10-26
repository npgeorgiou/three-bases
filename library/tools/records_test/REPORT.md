# Tagging per effect: test report

Built by `tools/records_test/` (words.py, abilities.py, report.py) on a copy of the database.
Script numbers only; the gold reading is not in this report yet.

## How the tags were put into abilities

Keyword: the keyword's own ability. One trigger / no trigger: the card has at most one trigger, so all its other tags go with
it (no text read). Position: cards with two or more triggers; the tag goes to the nearest trigger before its words.
Statistics: words unknown; the trigger this game's one-trigger cards most often show with that tag. Card: whole-card tags.
Agree: on tags placed by position, how often the statistics rule picks the same ability (a check per game, no reading).

| game | cards | cards with 2+ trigger abilities | tags | keyword | one trigger | no trigger | position | statistics | card | agree |
|---|---|---|---|---|---|---|---|---|---|---|
| darkest_dungeon | 944 | 5 | 5622 | 42 | 840 | 4228 | 38 | 15 | 443 | 27.8% |
| duelyst | 785 | 10 | 2722 | 392 | 1045 | 1057 | 58 | 1 | 108 | 83.3% |
| faeria | 443 | 8 | 1825 | 418 | 506 | 775 | 37 | 2 | 59 | 87.5% |
| gwent | 1355 | 259 | 7069 | 1857 | 2164 | 925 | 1065 | 49 | 184 | 61.8% |
| hearthstone | 8039 | 334 | 26970 | 4006 | 12032 | 7587 | 1022 | 62 | 927 | 74.4% |
| hs_battlegrounds | 2208 | 62 | 8506 | 917 | 3702 | 2090 | 243 | 24 | 1186 | 81.2% |
| inscryption | 269 | 10 | 1044 | 293 | 204 | 286 | 72 | 6 | 141 | 43.9% |
| into_the_breach | 287 | 2 | 1202 | 158 | 236 | 787 | 11 | 0 | 0 | 62.5% |
| lorcana | 1788 | 46 | 6559 | 1073 | 2560 | 2033 | 240 | 14 | 468 | 78.7% |
| marvel_snap | 917 | 17 | 5132 | 506 | 892 | 1923 | 75 | 10 | 1660 | 61.8% |
| monster_train | 267 | 0 | 862 | 258 | 187 | 346 | 0 | 0 | 71 | - |
| mtg | 18880 | 2376 | 95108 | 16846 | 35482 | 20735 | 12414 | 126 | 2428 | 53.2% |
| runeterra | 2426 | 124 | 11023 | 3121 | 3500 | 2972 | 650 | 22 | 366 | 63.8% |
| shadowverse | 4381 | 666 | 24164 | 3890 | 10244 | 3639 | 3722 | 81 | 561 | 56.5% |
| stormbound | 190 | 1 | 625 | 0 | 496 | 78 | 2 | 0 | 47 | 0.0% |
| sts1 | 889 | 14 | 3146 | 506 | 794 | 1372 | 44 | 51 | 300 | 87.5% |
| sts2 | 1378 | 27 | 4835 | 265 | 1227 | 2488 | 124 | 97 | 471 | 81.0% |
| swu | 1812 | 120 | 7477 | 1615 | 2915 | 1535 | 593 | 7 | 385 | 56.1% |
| tesl | 849 | 25 | 3366 | 916 | 1316 | 794 | 125 | 2 | 148 | 55.1% |
| wh_40k_10e | 3749 | 224 | 22973 | 7053 | 5292 | 7228 | 2319 | 49 | 3 | 60.8% |
| wh_aos_4th | 3377 | 267 | 13098 | 0 | 4660 | 4447 | 2565 | 100 | 9 | 60.0% |

## Trigger pairs

| game | before | after |
|---|---|---|
| darkest_dungeon | 1092 | 317 |
| duelyst | 660 | 598 |
| faeria | 494 | 333 |
| gwent | 2913 | 1995 |
| hearthstone | 9305 | 6827 |
| hs_battlegrounds | 2175 | 1816 |
| inscryption | 443 | 240 |
| into_the_breach | 120 | 155 |
| lorcana | 2529 | 1377 |
| marvel_snap | 1024 | 439 |
| monster_train | 130 | 112 |
| mtg | 37102 | 31597 |
| runeterra | 4243 | 2713 |
| shadowverse | 10312 | 8737 |
| stormbound | 183 | 179 |
| sts1 | 563 | 487 |
| sts2 | 810 | 776 |
| swu | 3318 | 2473 |
| tesl | 1023 | 929 |
| wh_40k_10e | 8057 | 4482 |
| wh_aos_4th | 3339 | 4077 |

### Known errors

- Wild Avenger (faeria): wrong pairs today 3/4, after 0/4; pairs now: on_play -> movement
- Invincible (hearthstone): wrong pairs today 3/3, after 1/3 (death_trigger -> summon); pairs now: death_trigger -> attack_gain, death_trigger -> defence_gain, death_trigger -> summon, death_trigger -> taunt, on_play -> attack_gain, on_play -> defence_gain, on_play -> summon, on_play -> taunt
- Mortarion (wh_40k_10e): wrong pairs today 3/3, after 0/3; pairs now: on_attack -> damage_reduction, on_attack -> debuff, on_attack -> drawback, on_attack -> movement, other_death_trigger -> attack_now, other_death_trigger -> cheat_death, other_death_trigger -> flexibility, other_death_trigger -> play_restriction, other_death_trigger -> temporary_buff
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

Strongest layer, old: {'engine': 30, 'MISS': 2, 'relation': 17, 'role_tree': 5, 'role': 14, 'type': 4, 'keyword': 9, 'link': 1}; new: {'engine': 28, 'MISS': 2, 'relation': 17, 'role_tree': 6, 'role': 16, 'type': 3, 'keyword': 9, 'link': 1}.

