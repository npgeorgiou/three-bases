# Tag-fix plan: final comparison (20 Oct 2026)

Original: the library at commit c7a77a4. New: the build pushed on 20 Oct 2026. Both are scored on the answer key (8,242 entries, with the tags of the keywords each card has, `tools/key/key.py load`). Numbers are per 100 key entries.
Wrong: a library tag that is neither a key concept nor a broader or narrower one. Missed: a key concept the library has nothing of.

| Game | Wrong (original → new) | Missed (original → new) |
|---|---|---|
| into_the_breach | 146.7 → 74.0 | 100.0 → 43.2 |
| wh_bloodbowl3 | 237.2 → 164.3 | 177.8 → 17.6 |
| inscryption | 153.9 → 70.4 | 78.1 → 55.2 |
| faeria | 107.7 → 58.7 | 54.9 → 46.2 |
| duelyst | 82.5 → 45.6 | 45.0 → 34.2 |
| sts1 | 130.7 → 43.1 | 39.9 → 27.9 |
| marvel_snap | 149.4 → 108.5 | 33.8 → 31.2 |
| darkest_dungeon | 155.3 → 78.9 | 147.4 → 44.2 |
| dnd5e | 276.7 → 148.5 | 241.3 → 212.6 |
| sts2 | 146.6 → 53.2 | 46.3 → 38.2 |
| gwent | 158.3 → 65.2 | 129.0 → 78.4 |
| hs_battlegrounds | 111.4 → 52.6 | 60.5 → 47.7 |
| wh_killteam | 281.1 → 159.2 | 250.6 → 163.9 |
| runeterra | 114.9 → 82.0 | 124.2 → 73.2 |
| wh_underworlds | 172.5 → 90.6 | 122.2 → 95.2 |
| wh_aos_4th | 322.0 → 139.9 | 240.1 → 168.7 |
| wh_40k_10e | 347.6 → 232.2 | 253.0 → 120.6 |
| shadowverse | 177.5 → 99.1 | 131.9 → 72.8 |
| hearthstone | 82.3 → 59.4 | 82.1 → 62.6 |
| mtg | 195.6 → 117.6 | 164.8 → 133.7 |

All 20 games: fewer wrong and fewer missed tags. Right tags of the original that the new build no longer has: 461, all
replaced by the key's own concept where a review disagreed with the key (key wins, Kaptain's decision of 19 Oct 2026).
Scoring note: the key reads what a card does, so a payoff tag (role benefits) counts as wrong when the key lacks it; the wrong
figures are slightly pessimistic for payoff cards.

## Real-world cases (tools/realworld, 322 cases with sources)

Original 161 met, new 162 met (13 gained, 12 lost). Per game, original | new:

- darkest_dungeon    combo 4/5  |  darkest_dungeon    combo 4/5
- dnd5e              signature 4/10  archetype 5/7  combo 1/5  |  dnd5e              signature 4/10  archetype 5/7  combo 3/5
- duelyst            signature 6/8  archetype 5/5  |  duelyst            signature 5/8  archetype 5/5
- faeria             signature 5/9  archetype 5/5  splash 0/1  |  faeria             signature 4/9  archetype 4/5  splash 0/1
- gwent              signature 7/10  archetype 4/7  combo 1/2  |  gwent              signature 4/10  archetype 4/7  combo 1/2
- hearthstone        signature 6/10  archetype 7/10  combo 4/10  splash 1/6  |  hearthstone        signature 7/10  archetype 8/10  combo 4/10  splash 1/6
- hs_battlegrounds   combo 7/10  |  hs_battlegrounds   combo 7/10
- inscryption        signature 0/3  archetype 0/2  combo 0/2  |  inscryption        signature 0/3  archetype 0/2  combo 0/2
- into_the_breach    signature 1/9  archetype 0/2  combo 0/2  splash 0/4  |  into_the_breach    signature 1/9  archetype 0/2  combo 0/2  splash 0/4
- marvel_snap        combo 7/10  |  marvel_snap        combo 7/10
- mtg                signature 9/10  archetype 5/6  combo 2/4  splash 8/8  |  mtg                signature 10/10  archetype 3/6  combo 2/4  splash 8/8
- runeterra          signature 4/10  archetype 4/5  combo 1/1  |  runeterra          signature 4/10  archetype 3/5  combo 1/1
- shadowverse        signature 6/10  archetype 3/5  combo 2/2  |  shadowverse        signature 8/10  archetype 3/5  combo 2/2
- sts1               signature 6/10  archetype 3/9  combo 8/10  |  sts1               signature 7/10  archetype 4/9  combo 9/10
- sts2               signature 6/11  archetype 2/6  combo 0/2  |  sts2               signature 5/11  archetype 1/6  combo 0/2
- wh_40k_10e         signature 2/7  archetype 1/8  combo 3/7  |  wh_40k_10e         signature 2/7  archetype 1/8  combo 3/7
- wh_aos_4th         signature 4/8  archetype 1/9  |  wh_aos_4th         signature 4/8  archetype 1/9
- wh_bloodbowl3      signature 0/2  |  wh_bloodbowl3      signature 0/2
- wh_killteam        signature 0/5  archetype 1/3  |  wh_killteam        signature 1/5  archetype 1/3
- wh_underworlds     archetype 0/10  |  wh_underworlds     archetype 1/10

Lost (to trace next): Duelyst Vetruvian summon signature; Faeria Blue transform signature and spellslinger archetype; Gwent
Nilfgaard donate and tutor, Skellige condition_life signatures; Magic Blue control and Green ramp archetypes; Runeterra Freljord
disruption archetype; Slay the Spire 2 Necrobinder control archetype and Regent permanent_growth signature; 40k Death Guard debuff signature.

## Combos (tools/combos.tsv)

Original 80 of 82, new 80 of 82 (the same two known misses).

## What changed

- The key credits the tags of the keywords a card has (`key.py credit`).
- Patterns from the key's quoted words, kept only when 90%+ right on the half of the key they were not built from (`step3/key_patterns.py`).
- Old patterns right less than half the time on the key switched off, or pointed at the concept the key shows them right for (`step3/switch_off.py`).
- Review records in the tree v3 ids (`fixes/f15`); where a review and the key disagree on what a card does, the key wins (`key_wins.py`).
- New trigger concepts (on_draw, on_discard, on_lifegain, on_block, on_targeted, on_sacrifice, on_life_loss) with patterns for every game, own units
  given up by exiling/consuming as sacrifice, amplifiers in every game (`step3/trigger_patterns.py`, `step3/amp_patterns.py`); the scorers skip
  concepts the key never had (`key/added_concepts.txt`).
- Two concept relations (sacrifice with cast_from_zone, life_payment with on_life_loss); the connection search knows what fires the new triggers.
- Trigger pairs are made again after the tree move, for the tags added since; the keyword rule runs again per game (`step_games.json`).
- Revert passes (`final_compare.py revert`, `final_revert.py`) put back right tags of the original.
