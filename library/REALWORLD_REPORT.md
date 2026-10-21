# Real-world test: every case

Made by `tools/realworld_report.py` from the library build. A case is a fact a wiki or guide states about a game (a faction's signature mechanic, its archetype, a two-card combo, a splash); the test checks whether the library finds it.

## Totals

| Game | Signature | Archetype | Combo | Splash | All |
|---|---|---|---|---|---|
| Darkest Dungeon |  |  | 6/7 |  | 6/7 |
| Duelyst | 13/22 | 6/8 |  |  | 19/30 |
| Faeria | 9/20 | 6/9 | 0/1 | 0/2 | 15/32 |
| Gwent (standalone) | 16/22 | 7/8 | 3/3 |  | 26/33 |
| Hearthstone | 38/57 | 13/34 | 6/13 | 8/9 | 65/113 |
| Hearthstone Battlegrounds |  |  | 9/13 |  | 9/13 |
| Inscryption | 2/12 | 1/1 | 1/5 |  | 4/18 |
| Into the Breach | 2/11 | 1/1 | 0/1 | 2/4 | 5/17 |
| Disney Lorcana | 18/25 | 7/8 | 12/12 | 6/12 | 43/57 |
| Marvel Snap |  |  | 19/24 |  | 19/24 |
| Monster Train | 6/14 | 4/7 | 2/4 |  | 12/25 |
| Magic: The Gathering | 44/48 | 7/10 | 9/15 | 12/15 | 72/88 |
| Legends of Runeterra | 31/40 | 7/16 | 7/19 | 1/1 | 46/76 |
| Shadowverse | 15/22 | 7/13 |  |  | 22/35 |
| Stormbound | 6/17 | 6/10 | 1/1 |  | 13/28 |
| Slay the Spire | 10/18 | 5/9 | 18/21 |  | 33/48 |
| Slay the Spire 2 (Early Access) | 7/16 | 1/6 | 0/2 |  | 8/24 |
| Star Wars: Unlimited | 17/20 | 6/8 | 4/7 | 2/3 | 29/38 |
| The Elder Scrolls: Legends | 10/15 | 5/9 | 6/16 |  | 21/40 |
| Warhammer 40,000 (10th edition) | 8/28 | 4/12 | 5/8 |  | 17/48 |
| Warhammer Age of Sigmar (4th edition) | 11/47 | 4/18 |  |  | 15/65 |
| **All** | 263/454 | 97/187 | 108/172 | 31/46 | **499/859** |

## Why cases miss

| Cases | Type | Reason |
|---|---|---|
| 114 | signature | not 1.5x the rest of the game |
| 90 | archetype | recipe not 1.5x the other factions |
| 43 | combo | both cards there, no connection |
| 39 | signature | no card of the faction has it |
| 38 | signature | could be chance (5%) |
| 21 | combo | a card name is not in the library |
| 15 | splash | missing from the splash list |

## Darkest Dungeon

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | combo | Blinding Gas | Finish Him | linked by relation, role |  | [stun, then extra damage on the stunned](https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide) |
| ✓ | combo | Disorienting Blast | Finish Him | linked by relation, role |  | [stun, then extra damage on the stunned](https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide) |
| ✗ | combo | Barbaric YAWP! | Wicked Hack |  | both cards there, no connection | [stun, then mop up](https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide) |
| ✓ | combo | Barbaric YAWP! | Breakthrough | linked by keyword |  | [stun, then mop up](https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide) |
| ✓ | combo | Cry Havoc | Transform | linked by relation |  | [stress relief offsets the transform](https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide) |
| ✓ | combo | Daemon's Pull | Point Blank Shot | linked by keyword, relation |  | [pull the toughest enemy forward, then shoot](https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide) |
| ✓ | combo | Disorienting Blast | Point Blank Shot | linked by relation |  | [the Blast clears the Shot's corpses](https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide) |

## Duelyst

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Lyonar Kingdoms | taunt | 12/90 cards (13%), 3.1x the rest, chance 0.001, rank 1 of 7 |  | [Provoke](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✓ | signature | Lyonar Kingdoms | adjacency | 34/90 cards (38%), 1.8x the rest, chance 0.001, rank 1 of 7 |  | [Zeal](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✓ | signature | Lyonar Kingdoms | heal | 11/90 cards (12%), 3.3x the rest, chance 0.002, rank 1 of 7 |  | [healing](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✗ | signature | Lyonar Kingdoms | board_presence | 7/90 cards (8%), 0.5x the rest, chance 0.992, rank 6 of 7 | not 1.5x the rest of the game | [strong board presence](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✗ | signature | Songhai Empire | movement | 11/98 cards (11%), 1.8x the rest, chance 0.068, rank 2 of 7 | could be chance (5%) | [displacement, extended movement](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✗ | signature | Songhai Empire | ranged | 6/98 cards (6%), 1.0x the rest, chance 0.589, rank 3 of 7 | not 1.5x the rest of the game | [ranged attacks](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✓ | signature | Songhai Empire | flanking | 14/98 cards (14%), 14.0x the rest, chance 0.000, rank 1 of 7 |  | [Backstab](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✓ | signature | Songhai Empire | on_spell | 9/98 cards (9%), 3.0x the rest, chance 0.008, rank 1 of 7 |  | [spell synergies](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✗ | signature | Songhai Empire | combo_sequence | 0/98 cards (0%), 0.0x the rest, chance 1.000, rank 2 of 7 | no card of the faction has it | [chained combos](https://gamewave.fr/duelyst/duelyst-le-jeu-de-carte-aux-six-factions/) |
| ✗ | signature | Vetruvian Imperium | summon | 19/94 cards (20%), 1.4x the rest, chance 0.105, rank 3 of 7 | not 1.5x the rest of the game | [Dervish summons](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✓ | signature | Vetruvian Imperium | self_destruct | 2/94 cards (2%), infx the rest, chance 0.014, rank 1 of 7 |  | [short-lived Dervishes](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✓ | signature | Vetruvian Imperium | buff | 31/94 cards (33%), 0.9x the rest, chance 0.761, rank 5 of 7 |  | [buffs](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✗ | signature | Vetruvian Imperium | debuff | 3/94 cards (3%), 2.0x the rest, chance 0.229, rank 3 of 7 | could be chance (5%) | [debuffs](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✗ | signature | Vetruvian Imperium | merge_attach | 0/94 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 7 | no card of the faction has it | [artifacts on the General](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✓ | signature | Abyssian Host | other_death_trigger | 6/92 cards (7%), 9.1x the rest, chance 0.001, rank 1 of 7 |  | [Deathwatch](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✓ | signature | Abyssian Host | terrain | 9/92 cards (10%), 4.0x the rest, chance 0.002, rank 1 of 7 |  | [Shadow Creep](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✓ | signature | Abyssian Host | summon | 25/92 cards (27%), 2.0x the rest, chance 0.001, rank 1 of 7 |  | [Wraithlings](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✓ | signature | Abyssian Host | board_presence | 25/92 cards (27%), 2.0x the rest, chance 0.001, rank 1 of 7 |  | [strong in numbers](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✓ | signature | Magmar Aspects | permanent_growth | 9/89 cards (10%), 4.7x the rest, chance 0.001, rank 1 of 7 |  | [Grow](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✗ | signature | Magmar Aspects | cheat_death | 0/89 cards (0%), 0.0x the rest, chance 1.000, rank 3 of 7 | no card of the faction has it | [Rebirth](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✓ | signature | Vanar Kindred | territory_trigger | 14/99 cards (14%), 48.6x the rest, chance 0.000, rank 1 of 7 |  | [Infiltrate](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✗ | signature | Vanar Kindred | removal | 5/99 cards (5%), 0.8x the rest, chance 0.764, rank 4 of 7 | not 1.5x the rest of the game | [swift, precise removal](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✓ | archetype | Lyonar Kingdoms | sustain | recipe score 1.49, 3.6x the other factions, 12 cards |  | [healing, war of attrition](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✓ | archetype | Songhai Empire | spellslinger | recipe score 1.17, 3.1x the other factions, 14 cards |  | [spell synergies and damage combos](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✓ | archetype | Songhai Empire | positional | recipe score 0.64, 2.5x the other factions, 33 cards |  | [displacement and movement](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✗ | archetype | Abyssian Host | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [Wraithlings in numbers](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✓ | archetype | Abyssian Host | sacrifice | recipe score 1.31, 2.8x the other factions, 29 cards |  | [profiting from death](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✓ | archetype | Magmar Aspects | scaling | recipe score 1.63, 12.8x the other factions, 10 cards |  | [Grow](https://store.steampowered.com/app/2004320/Duelyst_II/) |
| ✓ | archetype | Vanar Kindred | control | recipe score 0.70, 2.5x the other factions, 20 cards |  | [tactical control](https://gamewave.fr/duelyst/duelyst-le-jeu-de-carte-aux-six-factions/) |
| ✗ | archetype | Vanar Kindred | positional | under 1.5x the other factions | recipe not 1.5x the other factions | [battlefield manipulation](https://store.steampowered.com/app/2004320/Duelyst_II/) |

## Faeria

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | signature | Blue | movement | 33/71 cards (46%), 1.5x the rest, chance 0.009, rank 2 of 6 | could be chance (5%) | [mobility, jump](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✗ | signature | Blue | transform | 2/71 cards (3%), 2.6x the rest, chance 0.247, rank 2 of 6 | could be chance (5%) | [transforming creatures](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✗ | signature | Blue | stat_loss | 1/71 cards (1%), 1.0x the rest, chance 0.652, rank 4 of 6 | not 1.5x the rest of the game | [shrinking big creatures](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✗ | signature | Blue | terrain | 10/71 cards (14%), 0.7x the rest, chance 0.908, rank 5 of 6 | not 1.5x the rest of the game | [turning lands into lakes, moving lands](https://boards.faeria.com/t/board-and-colour-a-state-of-the-game-analysis/2586) |
| ✓ | signature | Green | taunt | 14/67 cards (21%), 3.6x the rest, chance 0.000, rank 1 of 6 |  | [Taunt](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✗ | signature | Green | high_cost | 0/67 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 6 | no card of the faction has it | [big creatures](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✓ | signature | Green | buff | 35/67 cards (52%), 1.3x the rest, chance 0.072, rank 2 of 6 |  | [many buffs](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✗ | signature | Green | terrain | 15/67 cards (22%), 1.2x the rest, chance 0.267, rank 3 of 6 | not 1.5x the rest of the game | [forests](https://boards.faeria.com/t/board-and-colour-a-state-of-the-game-analysis/2586) |
| ✓ | signature | Red | damage | 30/68 cards (44%), 4.1x the rest, chance 0.000, rank 1 of 6 |  | [damaging events](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✓ | signature | Red | direct_damage | 21/68 cards (31%), 5.5x the rest, chance 0.000, rank 1 of 6 |  | [burn](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✗ | signature | Red | taunt | 3/68 cards (4%), 0.5x the rest, chance 0.938, rank 3 of 6 | not 1.5x the rest of the game | [the biggest Taunts](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✓ | signature | Red | ranged | 6/68 cards (9%), 3.0x the rest, chance 0.032, rank 1 of 6 |  | [ranged creatures](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✗ | signature | Red | terrain | 3/68 cards (4%), 0.2x the rest, chance 1.000, rank 6 of 6 | not 1.5x the rest of the game | [land destruction](https://boards.faeria.com/t/board-and-colour-a-state-of-the-game-analysis/2586) |
| ✓ | signature | Yellow | haste | 6/70 cards (9%), 4.0x the rest, chance 0.013, rank 1 of 6 |  | [rush and haste](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✓ | signature | Yellow | evasion | 27/70 cards (39%), 2.7x the rest, chance 0.000, rank 1 of 6 |  | [flight](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✓ | signature | Yellow | sacrifice | 6/70 cards (9%), 8.0x the rest, chance 0.002, rank 1 of 6 |  | [sacrificing creatures](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✗ | signature | Yellow | life_payment | 2/70 cards (3%), 10.7x the rest, chance 0.066, rank 1 of 6 | could be chance (5%) | [sacrificing health](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✗ | signature | Yellow | on_spell | 1/70 cards (1%), 5.3x the rest, chance 0.291, rank 1 of 6 | could be chance (5%) | [cards buffed by events](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✗ | signature | Yellow | aoe_damage | 3/70 cards (4%), 0.4x the rest, chance 0.989, rank 4 of 6 | not 1.5x the rest of the game | [area damage](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✓ | signature | Yellow | terrain | 23/70 cards (33%), 2.0x the rest, chance 0.002, rank 1 of 6 |  | [land conversion](https://boards.faeria.com/t/board-and-colour-a-state-of-the-game-analysis/2586) |
| ✓ | archetype | Yellow | aggro_tempo | recipe score 0.61, 5.2x the other factions, 34 cards |  | [Yellow Rush](https://www.faeria.com/the-hub/guide/42-deck-archetypes) |
| ✓ | archetype | Yellow | control | recipe score 0.49, 2.4x the other factions, 9 cards |  | [Yellow control](https://www.faeria.com/the-hub/guide/42-deck-archetypes) |
| ✗ | archetype | Yellow | spellslinger | under 1.5x the other factions | recipe not 1.5x the other factions | [Blue Yellow Events](https://www.faeria.com/the-hub/guide/42-deck-archetypes) |
| ✗ | archetype | Yellow | burn | under 1.5x the other factions | recipe not 1.5x the other factions | [Red Yellow Burn](https://www.faeria.com/the-hub/guide/42-deck-archetypes) |
| ✓ | archetype | Yellow | sacrifice | recipe score 0.62, 2.5x the other factions, 15 cards |  | [Green and Yellow sacrifice](https://www.faeria.com/the-hub/guide/42-deck-archetypes) |
| ✓ | archetype | Blue | spellslinger | recipe score 0.99, 2.0x the other factions, 4 cards |  | [Blue Yellow Events](https://www.faeria.com/the-hub/guide/42-deck-archetypes) |
| ✓ | archetype | Red | burn | recipe score 1.85, 7.2x the other factions, 20 cards |  | [Red Yellow Burn](https://www.faeria.com/the-hub/guide/42-deck-archetypes) |
| ✗ | archetype | Red | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [Rush decks](https://boards.faeria.com/t/board-and-colour-a-state-of-the-game-analysis/2586) |
| ✓ | archetype | Green | sacrifice | recipe score 0.50, 1.8x the other factions, 16 cards |  | [Green and Yellow sacrifice](https://www.faeria.com/the-hub/guide/42-deck-archetypes) |
| ✗ | splash | Green | resource_gain |  | missing from the splash list | [a dash of ramp](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✗ | splash | Yellow | resource_gain |  | missing from the splash list | [cards that give mana](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✗ | combo | Khalim's Prayer | Zealous Crusader |  | both cards there, no connection | [orb attacks give faeria and buff the Crusader](https://www.faeria.com/the-hub/guide/42-deck-archetypes) |

## Gwent (standalone)

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | signature | Northern Realms | stat_gain | 84/178 cards (47%), 1.7x the rest, chance 0.000, rank 1 of 7 | could be chance (5%) | [boosting friendly units](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | signature | Northern Realms | haste | 48/178 cards (27%), 4.4x the rest, chance 0.000, rank 1 of 7 |  | [Zeal](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | signature | Northern Realms | activated | 109/178 cards (61%), 2.6x the rest, chance 0.000, rank 1 of 7 |  | [Order abilities](https://www.keengamer.com/articles/guides/what-is-the-best-faction-in-gwent/) |
| ✓ | signature | Nilfgaard | silence | 13/180 cards (7%), 3.0x the rest, chance 0.002, rank 1 of 7 |  | [locking units](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | signature | Nilfgaard | information | 8/180 cards (4%), 2.9x the rest, chance 0.015, rank 2 of 7 |  | [spying on enemy hands](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | signature | Nilfgaard | steal | 7/180 cards (4%), 15.3x the rest, chance 0.000, rank 1 of 7 |  | [stealing enemy units](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | signature | Nilfgaard | donate | 10/180 cards (6%), 8.2x the rest, chance 0.000, rank 1 of 7 |  | [Spies on the opponent's board](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✗ | signature | Nilfgaard | cast_from_zone | 1/180 cards (1%), 6.5x the rest, chance 0.248, rank 1 of 7 | could be chance (5%) | [playing cards from the opponent's deck](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | signature | Monster | sacrifice | 19/183 cards (10%), 15.2x the rest, chance 0.000, rank 1 of 7 |  | [Consume devours weaker units](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | signature | Monster | death_trigger | 33/183 cards (18%), 21.2x the rest, chance 0.000, rank 1 of 7 |  | [Deathwish](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | signature | Monster | stat_condition | 38/183 cards (21%), 2.9x the rest, chance 0.000, rank 1 of 7 |  | [highest value on board](https://www.keengamer.com/articles/guides/what-is-the-best-faction-in-gwent/) |
| ✓ | signature | Monster | row_effects | 19/183 cards (10%), 10.2x the rest, chance 0.000, rank 1 of 7 |  | [weather](https://www.keengamer.com/articles/guides/what-is-the-best-faction-in-gwent/) |
| ✓ | signature | Scoiatael | trap_secret | 13/188 cards (7%), 6.7x the rest, chance 0.000, rank 1 of 7 |  | [traps](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | signature | Scoiatael | ranged | 2/188 cards (1%), infx the rest, chance 0.019, rank 1 of 7 |  | [ranged attacks](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | signature | Scoiatael | movement | 8/188 cards (4%), 4.1x the rest, chance 0.003, rank 1 of 7 |  | [mobility](https://www.keengamer.com/articles/guides/what-is-the-best-faction-in-gwent/) |
| ✗ | signature | Scoiatael | ping | 52/188 cards (28%), 1.1x the rest, chance 0.183, rank 2 of 7 | not 1.5x the rest of the game | [many small damage instances](https://www.keengamer.com/articles/guides/what-is-the-best-faction-in-gwent/) |
| ✗ | signature | Scoiatael | tutor | 10/188 cards (5%), 0.6x the rest, chance 0.983, rank 7 of 7 | not 1.5x the rest of the game | [playing cards straight from the deck](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | signature | Skellige | condition_life | 4/184 cards (2%), 25.5x the rest, chance 0.001, rank 1 of 7 |  | [Berserk](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✗ | signature | Skellige | friendly_fire | 13/184 cards (7%), 4.1x the rest, chance 0.000, rank 1 of 7 | could be chance (5%) | [damaging itself or allies for bonuses](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✗ | signature | Skellige | revive | 0/184 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 7 | no card of the faction has it | [reviving from the graveyard](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | signature | Skellige | damage | 95/184 cards (52%), 1.8x the rest, chance 0.000, rank 1 of 7 |  | [damaging units many ways](https://www.keengamer.com/articles/guides/what-is-the-best-faction-in-gwent/) |
| ✓ | signature | Syndicate | coin_economy | 129/190 cards (68%), infx the rest, chance 0.000, rank 1 of 7 |  | [coins spent on effects](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | archetype | Nilfgaard | control | recipe score 0.41, 1.8x the other factions, 40 cards |  | [control and counterplay](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | archetype | Nilfgaard | disruption | recipe score 1.14, 4.6x the other factions, 24 cards |  | [limiting the opponent's options](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | archetype | Monster | swarm | recipe score 0.17, 4.6x the other factions, 70 cards |  | [swarm and devour](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | archetype | Monster | sacrifice | recipe score 2.08, 10.3x the other factions, 51 cards |  | [consume and Deathwish](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | archetype | Scoiatael | trickery | recipe score 2.36, 24.4x the other factions, 14 cards |  | [traps and ambush](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | archetype | Skellige | graveyard | recipe score 1.45, 3.7x the other factions, 41 cards |  | [resurrection](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✗ | archetype | Skellige | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [aggression](https://www.pockettactics.com/gwent-the-witcher-card-game/decks) |
| ✓ | archetype | Syndicate | ramp | recipe score 5.08, 156.6x the other factions, 134 cards |  | [coin economy](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | combo | Koshchey | Caranthir Ar-Feiniel | linked by engine, keyword, relation |  | [a large amount of points](https://www.bluestacks.com/blog/game-guides/gwent/gwt-top-5-best-decks-en.html) |
| ✓ | combo | Joachim de Wett | Coup de Grâce | linked by engine, relation |  | [strong plays always available](https://www.bluestacks.com/blog/game-guides/gwent/gwt-top-5-best-decks-en.html) |
| ✓ | combo | Iris von Everec | Iris' Companions | linked by relation |  | [thinning for Round 3](https://www.bluestacks.com/blog/game-guides/gwent/gwt-top-5-best-decks-en.html) |

## Hearthstone

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Druid | resource_gain | 39/633 cards (6%), 11.4x the rest, chance 0.000, rank 1 of 12 |  | [speeds up mana gain](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Druid | taunt | 121/633 cards (19%), 2.1x the rest, chance 0.000, rank 1 of 12 |  | [strong Taunt minions](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Druid | modal_choice | 78/633 cards (12%), 18.6x the rest, chance 0.000, rank 1 of 12 |  | [flexible Choose One effects](https://hearthstone.wiki.gg/wiki/Classes) |
| ✗ | signature | Druid | high_cost | 0/633 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 12 | no card of the faction has it | [giant minions](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | signature | Druid | board_presence | 170/633 cards (27%), 1.5x the rest, chance 0.000, rank 2 of 12 | not 1.5x the rest of the game | [minion swarms](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | signature | Druid | draw | 90/633 cards (14%), 1.6x the rest, chance 0.000, rank 1 of 12 |  | [card draw](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | signature | Druid | tribal | 23/633 cards (4%), 0.9x the rest, chance 0.661, rank 4 of 12 | not 1.5x the rest of the game | [Beasts](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | signature | Hunter | tribal | 97/506 cards (19%), 6.7x the rest, chance 0.000, rank 1 of 12 |  | [Beasts](https://hearthstone.wiki.gg/wiki/Classes) |
| ✗ | signature | Hunter | direct_damage | 61/506 cards (12%), 1.3x the rest, chance 0.014, rank 4 of 12 | not 1.5x the rest of the game | [face damage](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | signature | Hunter | trap_secret | 49/506 cards (10%), 4.8x the rest, chance 0.000, rank 1 of 12 |  | [Secrets and traps](https://hearthstone.wiki.gg/wiki/Classes) |
| ✗ | signature | Hunter | death_trigger | 90/506 cards (18%), 1.4x the rest, chance 0.001, rank 2 of 12 | not 1.5x the rest of the game | [Deathrattle](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | signature | Mage | aoe_damage | 114/546 cards (21%), 1.8x the rest, chance 0.000, rank 1 of 12 |  | [area-of-effect damage](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Mage | disable | 37/546 cards (7%), 3.7x the rest, chance 0.000, rank 1 of 12 |  | [Freeze](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Mage | on_spell | 27/546 cards (5%), 3.2x the rest, chance 0.000, rank 1 of 12 |  | [spell synergy](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Mage | trap_secret | 50/546 cards (9%), 4.5x the rest, chance 0.000, rank 2 of 12 |  | [Secrets](https://hearthstone.wiki.gg/wiki/Classes) |
| ✗ | signature | Mage | board_wipe | 4/546 cards (1%), 0.5x the rest, chance 0.936, rank 8 of 12 | not 1.5x the rest of the game | [board clear](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | signature | Paladin | shield | 112/531 cards (21%), 18.6x the rest, chance 0.000, rank 1 of 12 |  | [Divine Shield](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Paladin | heal | 63/531 cards (12%), 2.4x the rest, chance 0.000, rank 2 of 12 |  | [healing](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Paladin | debuff | 30/531 cards (6%), 3.6x the rest, chance 0.000, rank 1 of 12 |  | [weakens enemies](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Paladin | trap_secret | 28/531 cards (5%), 2.3x the rest, chance 0.000, rank 3 of 12 |  | [Secrets](https://hearthstone.wiki.gg/wiki/Classes) |
| ✗ | signature | Paladin | board_presence | 109/531 cards (21%), 1.1x the rest, chance 0.180, rank 6 of 12 | not 1.5x the rest of the game | [minion swarms](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | signature | Paladin | buff | 162/531 cards (31%), 1.6x the rest, chance 0.000, rank 1 of 12 |  | [minion buffs](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | signature | Priest | heal | 93/506 cards (18%), 4.0x the rest, chance 0.000, rank 1 of 12 |  | [restorative healing](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Priest | steal | 15/506 cards (3%), 4.1x the rest, chance 0.000, rank 1 of 12 |  | [seizing control of enemy minds](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Priest | destroy | 33/506 cards (7%), 1.4x the rest, chance 0.035, rank 3 of 12 |  | [destroying enemies](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Priest | copy | 87/506 cards (17%), 3.0x the rest, chance 0.000, rank 1 of 12 |  | [copying](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | signature | Priest | death_trigger | 66/506 cards (13%), 1.0x the rest, chance 0.513, rank 7 of 12 | not 1.5x the rest of the game | [Deathrattle](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | signature | Rogue | combo_sequence | 78/549 cards (14%), 20.9x the rest, chance 0.000, rank 1 of 12 |  | [Combo](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Rogue | destroy | 46/549 cards (8%), 1.9x the rest, chance 0.000, rank 2 of 12 |  | [destroying individual minions](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | signature | Rogue | draw | 72/549 cards (13%), 1.5x the rest, chance 0.001, rank 3 of 12 | not 1.5x the rest of the game | [card draw](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | signature | Rogue | death_trigger | 78/549 cards (14%), 1.1x the rest, chance 0.212, rank 4 of 12 | not 1.5x the rest of the game | [Deathrattle](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | signature | Shaman | tribal | 32/537 cards (6%), 1.6x the rest, chance 0.010, rank 2 of 12 |  | [Totems, Elementals, Murlocs](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Shaman | overload_debt | 68/537 cards (13%), 5.1x the rest, chance 0.000, rank 1 of 12 |  | [Overload](https://hearthstone.wiki.gg/wiki/Classes) |
| ✗ | signature | Shaman | board_presence | 115/537 cards (21%), 1.1x the rest, chance 0.073, rank 5 of 12 | not 1.5x the rest of the game | [minion swarms](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | signature | Shaman | damage | 123/537 cards (23%), 1.4x the rest, chance 0.000, rank 5 of 12 |  | [damage spells](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | signature | Warlock | tribal | 11/533 cards (2%), 0.5x the rest, chance 0.995, rank 7 of 12 | not 1.5x the rest of the game | [Demons](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Warlock | sacrifice | 16/533 cards (3%), 16.1x the rest, chance 0.000, rank 1 of 12 |  | [sacrifices its own minions](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Warlock | life_payment | 8/533 cards (2%), 22.6x the rest, chance 0.000, rank 1 of 12 |  | [trades Health to draw](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Warlock | discard | 48/533 cards (9%), 28.2x the rest, chance 0.000, rank 1 of 12 |  | [sacrifices cards](https://hearthstone.wiki.gg/wiki/Classes) |
| ✗ | signature | Warlock | draw | 48/533 cards (9%), 1.0x the rest, chance 0.583, rank 7 of 12 | not 1.5x the rest of the game | [card draw](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | signature | Warlock | board_presence | 120/533 cards (23%), 1.2x the rest, chance 0.018, rank 4 of 12 | not 1.5x the rest of the game | [minion swarms](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | signature | Warlock | disruption | 32/533 cards (6%), 2.6x the rest, chance 0.000, rank 2 of 12 |  | [disruption](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | signature | Warrior | block_armor | 90/506 cards (18%), 11.9x the rest, chance 0.000, rank 1 of 12 |  | [armor](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Warrior | on_damaged | 18/506 cards (4%), 3.8x the rest, chance 0.000, rank 1 of 12 |  | [Enrage and on-damage effects](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Warrior | haste | 65/506 cards (13%), 1.9x the rest, chance 0.000, rank 3 of 12 |  | [sends minions charging](https://hearthstone.wiki.gg/wiki/Classes) |
| ✗ | signature | Warrior | taunt | 71/506 cards (14%), 1.5x the rest, chance 0.001, rank 3 of 12 | not 1.5x the rest of the game | [Taunt](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | signature | Warrior | destroy | 18/506 cards (4%), 0.7x the rest, chance 0.920, rank 7 of 12 | not 1.5x the rest of the game | [destroying minions](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | signature | Demonhunter | hand_position | 50/360 cards (14%), 25.4x the rest, chance 0.000, rank 1 of 12 |  | [Outcast](https://hearthstone.blizzard.com/en-us/news/23305788) |
| ✓ | signature | Demonhunter | temporary_buff | 30/360 cards (8%), 2.1x the rest, chance 0.000, rank 2 of 12 |  | [hero Attack for one turn](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Demonhunter | lifesteal | 71/360 cards (20%), 1.5x the rest, chance 0.000, rank 3 of 12 |  | [Lifesteal](https://www.hearthstonetopdecks.com/vengeance-revisited-what-is-demon-hunters-new-identity/) |
| ✗ | signature | Demonhunter | tribal | 4/360 cards (1%), 0.3x the rest, chance 1.000, rank 11 of 12 | not 1.5x the rest of the game | [Demons](https://hearthstone.blizzard.com/en-us/news/23305788) |
| ✓ | signature | Demonhunter | draw | 51/360 cards (14%), 1.6x the rest, chance 0.001, rank 2 of 12 |  | [great card draw](https://hearthstone.wiki.gg/wiki/Demon_Hunter) |
| ✓ | signature | Deathknight | coin_economy | 1/270 cards (0%), 28.8x the rest, chance 0.066, rank 1 of 12 |  | [Corpses, a resource spent on cards](https://hearthstone.blizzard.com/en-us/news/23852696) |
| ✗ | signature | Deathknight | deckbuilding_effect | 5/270 cards (2%), 1.0x the rest, chance 0.605, rank 8 of 12 | not 1.5x the rest of the game | [Runes decide the deck](https://hearthstone.blizzard.com/en-us/news/23852696) |
| ✗ | signature | Deathknight | tribal | 4/270 cards (1%), 0.4x the rest, chance 0.994, rank 9 of 12 | not 1.5x the rest of the game | [Undead (Unholy)](https://hearthstone.blizzard.com/en-us/news/23852696) |
| ✓ | signature | Deathknight | board_presence | 77/270 cards (29%), 1.5x the rest, chance 0.000, rank 1 of 12 |  | [going wide (Unholy)](https://hearthstone.wiki.gg/wiki/Death_Knight) |
| ✓ | signature | Deathknight | disable | 12/270 cards (4%), 2.1x the rest, chance 0.014, rank 3 of 12 |  | [Freeze (Frost)](https://hearthstone.blizzard.com/en-us/news/23852696) |
| ✓ | archetype | Druid | swarm | recipe score 0.31, 1.9x the other factions, 175 cards |  | [Token Druid](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | archetype | Druid | tribal | under 1.5x the other factions | recipe not 1.5x the other factions | [Beast Druid](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | archetype | Druid | ramp | under 1.5x the other factions | recipe not 1.5x the other factions | [Big Druid, mana gain](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | archetype | Druid | fortress | recipe score 0.79, 1.9x the other factions, 181 cards |  | [Taunt Druid](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | archetype | Hunter | aggro_tempo | recipe score 0.35, 2.0x the other factions, 84 cards |  | [Face Hunter](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | archetype | Hunter | tribal | recipe score 0.95, 24.0x the other factions, 97 cards |  | [Midrange Beast Hunter](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | archetype | Hunter | trickery | recipe score 0.72, 3.6x the other factions, 54 cards |  | [Secret Hunter](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | archetype | Mage | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [Tempo Mage](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | archetype | Mage | tribal | recipe score 0.20, 1.8x the other factions, 30 cards |  | [Mech and Murloc Mage](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | archetype | Mage | spellslinger | recipe score 0.62, 3.4x the other factions, 99 cards |  | [strong spell synergy](https://hearthstone.wiki.gg/wiki/Classes) |
| ✗ | archetype | Paladin | trickery | under 1.5x the other factions | recipe not 1.5x the other factions | [Secret Paladin](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | archetype | Paladin | tribal | under 1.5x the other factions | recipe not 1.5x the other factions | [Mech Paladin](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | archetype | Paladin | control | under 1.5x the other factions | recipe not 1.5x the other factions | [Control Paladin](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | archetype | Paladin | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [minion swarms](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | archetype | Priest | tribal | under 1.5x the other factions | recipe not 1.5x the other factions | [Dragon Priest](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | archetype | Priest | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [Wall Priest](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | archetype | Priest | sustain | recipe score 1.16, 4.2x the other factions, 104 cards |  | [healing](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | archetype | Rogue | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [Tempo Rogue](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | archetype | Shaman | swarm | recipe score 0.49, 3.3x the other factions, 126 cards |  | [Token Shaman](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | archetype | Shaman | tribal | recipe score 0.24, 2.3x the other factions, 32 cards |  | [Murloc and Elemental Shaman](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | archetype | Shaman | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [Aggro Shaman](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | archetype | Shaman | control | under 1.5x the other factions | recipe not 1.5x the other factions | [Control Shaman](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | archetype | Warlock | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [Zoo, minion swarms](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | archetype | Warlock | control | under 1.5x the other factions | recipe not 1.5x the other factions | [Control Warlock](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | archetype | Warrior | control | under 1.5x the other factions | recipe not 1.5x the other factions | [Control Warrior](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | archetype | Warrior | tribal | under 1.5x the other factions | recipe not 1.5x the other factions | [Pirate Warrior](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | archetype | Warrior | fortress | recipe score 1.00, 2.5x the other factions, 163 cards |  | [armor and Taunt](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | archetype | Demonhunter | aggro_tempo | recipe score 0.59, 3.8x the other factions, 85 cards |  | [aggressive decks](https://hearthstone.wiki.gg/wiki/Demon_Hunter) |
| ✗ | archetype | Demonhunter | tribal | under 1.5x the other factions | recipe not 1.5x the other factions | [Demon tribal](https://www.hearthstonetopdecks.com/vengeance-revisited-what-is-demon-hunters-new-identity/) |
| ✗ | archetype | Demonhunter | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [token decks](https://www.hearthstonetopdecks.com/vengeance-revisited-what-is-demon-hunters-new-identity/) |
| ✗ | archetype | Demonhunter | sustain | under 1.5x the other factions | recipe not 1.5x the other factions | [Lifesteal builds](https://www.hearthstonetopdecks.com/vengeance-revisited-what-is-demon-hunters-new-identity/) |
| ✓ | archetype | Deathknight | control | recipe score 0.54, 1.6x the other factions, 32 cards |  | [Blood control](https://hearthstone.wiki.gg/wiki/Death_Knight) |
| ✗ | archetype | Deathknight | burn | under 1.5x the other factions | recipe not 1.5x the other factions | [Frost burn](https://hearthstone.wiki.gg/wiki/Death_Knight) |
| ✗ | archetype | Deathknight | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [Unholy zoo](https://hearthstone.wiki.gg/wiki/Death_Knight) |
| ✓ | splash | Hunter | draw |  |  | [card draw is a limitation](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | splash | Hunter | generate_cards |  |  | [card generation is a limitation](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | splash | Hunter | board_wipe |  | missing from the splash list | [board clear is a limitation](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | splash | Hunter | taunt |  |  | [Taunt is a limitation](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | splash | Mage | board_presence |  |  | [minion swarms are a limitation](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | splash | Paladin | cost_reduction |  |  | [cost reduction is a limitation](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | splash | Priest | draw |  |  | [card draw is a limitation](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | splash | Warrior | draw |  |  | [card draw is a limitation](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | splash | Warrior | generate_cards |  |  | [card generation is a limitation](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | combo | Auchenai Soulpriest | Circle of Healing | linked by role |  | [healing becomes damage to all minions](https://www.keengamer.com/articles/guides/7-great-hearthstone-card-combos/) |
| ✓ | combo | Equality | Consecration | linked by relation |  | [health set to 1, then 2 damage to each enemy](https://www.keengamer.com/articles/guides/7-great-hearthstone-card-combos/) |
| ✓ | combo | Leeroy Jenkins | Shadowstep | linked by engine, relation |  | [charge, return to hand, again](https://www.keengamer.com/articles/guides/7-great-hearthstone-card-combos/) |
| ✗ | combo | Unleash the Hounds | Raid Leader |  | both cards there, no connection | [buffs the charging Hounds](https://www.keengamer.com/articles/guides/7-great-hearthstone-card-combos/) |
| ✗ | combo | Unleash the Hounds | Stormwind Champion |  | both cards there, no connection | [buffs the charging Hounds](https://www.keengamer.com/articles/guides/7-great-hearthstone-card-combos/) |
| ✗ | combo | Unleash the Hounds | Hunter's Mark |  | a card name is not in the library | [Mark lowers targets for the Hounds](https://www.keengamer.com/articles/guides/7-great-hearthstone-card-combos/) |
| ✗ | combo | Injured Blademaster | Circle of Healing |  | both cards there, no connection | [heals the damaged Blademaster](https://primagames.com/tips/hearthstone-powerful-card-combos) |
| ✓ | combo | Ancestral Spirit | Cairne Bloodhoof | linked by engine, keyword |  | [resummoned Cairne summons again on death](https://primagames.com/tips/hearthstone-powerful-card-combos) |
| ✗ | combo | Force of Nature | Savage Roar |  | both cards there, no connection | [three charging 2/2s get +2 attack](https://primagames.com/tips/hearthstone-powerful-card-combos) |
| ✓ | combo | Deadly Poison | Blade Flurry | linked by relation |  | [weapon damage hits all enemies](https://primagames.com/tips/hearthstone-powerful-card-combos) |
| ✗ | combo | Assassin's Blade | Blade Flurry |  | a card name is not in the library | [weapon damage hits all enemies](https://primagames.com/tips/hearthstone-powerful-card-combos) |
| ✗ | combo | Divine Spirit | Inner Fire |  | a card name is not in the library | [the pair Priest decks need](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | combo | Venomizer | Missile Launcher | linked by keyword, type |  | [Hunter's board clear](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |

## Hearthstone Battlegrounds

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | combo | Wrath Weaver | Floating Watcher | linked by engine, type |  | [Watcher grows faster](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✓ | combo | Soul Juggler | Voidlord | linked by relation, type |  | [Voidlord protects the Jugglers](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✓ | combo | Coldlight Seer | Brann Bronzebeard | linked by role |  | [named as a combo](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✓ | combo | King Bagurgle | Brann Bronzebeard | linked by role |  | [named as a combo](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✓ | combo | Gentle Megasaur | Brann Bronzebeard | linked by role |  | [named as a combo](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✓ | combo | Rat Pack | Mama Bear | linked by relation, role, type |  | [named as a combo](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✓ | combo | Rat Pack | Goldrinn, the Great Wolf | linked by engine, keyword, type |  | [Goldrinn sets up the rats](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✓ | combo | Cave Hydra | Mama Bear | linked by type |  | [named as a combo](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✓ | combo | Cave Hydra | Goldrinn, the Great Wolf | linked by type |  | [Goldrinn sets up the Hydra](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✗ | combo | Replicating Menace | Cobalt Guardian |  | a card name is not in the library | [Deathrattle summons give Divine Shield](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✗ | combo | Mechano-Egg | Cobalt Guardian |  | a card name is not in the library | [Deathrattle summons give Divine Shield](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✗ | combo | Mechano-Egg | Baron Rivendare |  | a card name is not in the library | [doubled Deathrattle](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✗ | combo | Cobalt Guardian | Screwjank Clunker |  | a card name is not in the library | [stacked buffs](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |

## Inscryption

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | signature | Beast | sacrifice | 6/77 cards (8%), 1.5x the rest, chance 0.343, rank 2 of 4 | could be chance (5%) | [Blood costs paid by sacrifice](https://steamcommunity.com/app/1092790/discussions/0/3553931489687797930) |
| ✗ | signature | Beast | generate_cards | 8/77 cards (10%), 2.5x the rest, chance 0.094, rank 1 of 4 | could be chance (5%) | [Warren puts a Rabbit in hand](https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide) |
| ✗ | signature | Beast | deathtouch | 5/77 cards (6%), 1.6x the rest, chance 0.358, rank 1 of 4 | could be chance (5%) | [Adder kills what it damages](https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide) |
| ✗ | signature | Beast | evasion | 9/77 cards (12%), 1.4x the rest, chance 0.306, rank 2 of 4 | not 1.5x the rest of the game | [Hawk hits past blockers](https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide) |
| ✗ | signature | Undead | cost_type | 0/20 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 4 | no card of the faction has it | [Bones](https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide) |
| ✗ | signature | Undead | sacrifice | 3/20 cards (15%), 2.9x the rest, chance 0.118, rank 1 of 4 | could be chance (5%) | [destroying its own cards](https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide) |
| ✗ | signature | Undead | death_trigger | 4/20 cards (20%), 1.6x the rest, chance 0.260, rank 2 of 4 | could be chance (5%) | [Draugr releases a creature when it perishes](https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide) |
| ✗ | signature | Technology | resource_gain | 10/57 cards (18%), 0.9x the rest, chance 0.701, rank 3 of 4 | not 1.5x the rest of the game | [energy-boosting cards](https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide) |
| ✗ | signature | Technology | aura | 1/57 cards (2%), 1.0x the rest, chance 0.699, rank 2 of 4 | not 1.5x the rest of the game | [support circuits buff robots](https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide) |
| ✗ | signature | Technology | autonomous_units | 0/57 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 4 | no card of the faction has it | [49er moves on its own](https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide) |
| ✓ | signature | Magick | multiple_resources | 5/20 cards (25%), 6.4x the rest, chance 0.004, rank 1 of 4 |  | [Mox of three colours](https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide) |
| ✓ | signature | Magick | draw | 4/20 cards (20%), 15.4x the rest, chance 0.002, rank 1 of 4 |  | [Blue Mage draws per Mox](https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide) |
| ✓ | archetype | Undead | sacrifice | recipe score 0.81, 3.1x the other factions, 7 cards |  | [Necromancers and perish effects](https://steamcommunity.com/app/1092790/discussions/0/3553931489687797930) |
| ✗ | combo | Necromancer | Obol |  | a card name is not in the library | [the Obol dies twice](https://steamcommunity.com/app/1092790/discussions/0/3553931489687797930) |
| ✗ | combo | Warren | Rabbit |  | a card name is not in the library | [Warren supplies Rabbits](https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide) |
| ✓ | combo | Blue Mage | Sapphire Mox | linked by role |  | [needs the matching Mox](https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide) |
| ✗ | combo | Mage Knight | Ruby Mox |  | a card name is not in the library | [needs the matching Mox](https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide) |
| ✗ | combo | Junior Sage | Emerald Mox |  | a card name is not in the library | [needs the matching Mox](https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide) |

## Into the Breach

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | signature | Prime | damage | 19/31 cards (61%), 1.4x the rest, chance 0.072, rank 2 of 5 | not 1.5x the rest of the game | [punches and strikes](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | signature | Prime | forced_movement | 17/31 cards (55%), 1.0x the rest, chance 0.669, rank 4 of 5 | not 1.5x the rest of the game | [strikes that push](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | signature | Brute | damage | 20/29 cards (69%), 1.6x the rest, chance 0.010, rank 1 of 5 | could be chance (5%) | [projectiles and charges](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | signature | Brute | forced_movement | 22/29 cards (76%), 1.5x the rest, chance 0.016, rank 1 of 5 | not 1.5x the rest of the game | [shots that push](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | signature | Ranged | ranged | 16/26 cards (62%), 2.2x the rest, chance 0.002, rank 1 of 5 | could be chance (5%) | [artillery](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | signature | Ranged | forced_movement | 16/26 cards (62%), 1.1x the rest, chance 0.372, rank 2 of 5 | not 1.5x the rest of the game | [artillery that pushes](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | signature | Science | forced_movement | 15/25 cards (60%), 1.1x the rest, chance 0.444, rank 3 of 5 | not 1.5x the rest of the game | [pull and push](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✓ | signature | Science | swap | 9/25 cards (36%), 2.4x the rest, chance 0.020, rank 1 of 5 |  | [swap](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✓ | signature | Science | shield | 6/25 cards (24%), 2.7x the rest, chance 0.040, rank 1 of 5 |  | [shields](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | signature | Science | disable | 2/25 cards (8%), 1.2x the rest, chance 0.522, rank 3 of 5 | not 1.5x the rest of the game | [smoke and freeze](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | signature | Science | damage_over_time | 4/25 cards (16%), 0.4x the rest, chance 0.999, rank 5 of 5 | not 1.5x the rest of the game | [acid and fire](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✓ | archetype | Science | positional | recipe score 0.22, 2.9x the other factions, 18 cards |  | [utility: pull, push, swap](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✓ | splash | Prime | shield |  |  | [only Spartan Shield](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | splash | Prime | damage_over_time |  | missing from the splash list | [only Flame Thrower](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✓ | splash | Brute | shield |  |  | [Phase Cannon, Grappling Hook](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | splash | Brute | disable |  | missing from the splash list | [only Aerial Bombs' smoke](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | combo | Electric Whip | Grappling Hook |  | both cards there, no connection | [the Hook extends the chain](https://www.giantbomb.com/profile/majormitch/blog/thoughts-on-into-the-breachs-squads/116986/) |

## Disney Lorcana

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Amber | heal | 40/309 cards (13%), 6.8x the rest, chance 0.000, rank 1 of 6 |  | [healing](https://wiki.mushureport.com/wiki/Amber) |
| ✓ | signature | Amber | protection | 38/309 cards (12%), 0.6x the rest, chance 1.000, rank 6 of 6 |  | [protection](https://www.wargamer.com/disney-lorcana/colors) |
| ✗ | signature | Amber | bodyguard | 0/309 cards (0%), 0.0x the rest, chance 1.000, rank 2 of 6 | no card of the faction has it | [Bodyguard](https://wiki.mushureport.com/wiki/Amber) |
| ✓ | signature | Amber | assists_support | 12/309 cards (4%), 4.0x the rest, chance 0.001, rank 2 of 6 |  | [Support](https://wiki.mushureport.com/wiki/Amber) |
| ✓ | signature | Amber | revive | 27/309 cards (9%), 6.6x the rest, chance 0.000, rank 1 of 6 |  | [recovering characters from the discard pile](https://wiki.mushureport.com/wiki/Amber) |
| ✓ | signature | Amethyst | draw | 77/315 cards (24%), 2.0x the rest, chance 0.000, rank 1 of 6 |  | [more card draw than any other ink](https://wiki.mushureport.com/wiki/Amethyst) |
| ✓ | signature | Amethyst | return_to_hand | 20/315 cards (6%), 4.1x the rest, chance 0.000, rank 2 of 6 |  | [returns its cards to hand](https://www.wargamer.com/disney-lorcana/colors) |
| ✗ | signature | Amethyst | selection | 15/315 cards (5%), 1.2x the rest, chance 0.340, rank 2 of 6 | not 1.5x the rest of the game | [filtering the top card](https://wiki.mushureport.com/wiki/Amethyst) |
| ✓ | signature | Amethyst | disable | 41/315 cards (13%), 26.4x the rest, chance 0.000, rank 1 of 6 |  | [exerting opposing characters](https://wiki.mushureport.com/wiki/Amethyst) |
| ✓ | signature | Emerald | flexibility | 12/319 cards (4%), 4.4x the rest, chance 0.000, rank 1 of 6 |  | [a toolbox ink](https://wiki.mushureport.com/wiki/Emerald) |
| ✓ | signature | Emerald | hand_disruption | 41/319 cards (13%), 15.2x the rest, chance 0.000, rank 1 of 6 |  | [making opponents discard](https://www.wargamer.com/disney-lorcana/colors) |
| ✓ | signature | Emerald | bounce_enemy | 21/319 cards (7%), 3.9x the rest, chance 0.000, rank 1 of 6 |  | [bounce](https://wiki.mushureport.com/wiki/Emerald) |
| ✗ | signature | Emerald | forced_attack | 0/319 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 6 | no card of the faction has it | [granting Reckless](https://wiki.mushureport.com/wiki/Emerald) |
| ✗ | signature | Emerald | stat_gain | 51/319 cards (16%), 0.8x the rest, chance 0.975, rank 6 of 6 | not 1.5x the rest of the game | [strength increase more than Ruby and Steel](https://wiki.mushureport.com/wiki/Emerald) |
| ✓ | signature | Ruby | haste | 24/306 cards (8%), 4.2x the rest, chance 0.000, rank 2 of 6 |  | [Rush](https://www.wargamer.com/disney-lorcana/colors) |
| ✓ | signature | Ruby | destroy | 37/306 cards (12%), 2.1x the rest, chance 0.000, rank 1 of 6 |  | [banishing opposing characters](https://wiki.mushureport.com/wiki/Ruby) |
| ✓ | signature | Ruby | evasion | 41/306 cards (13%), 1.8x the rest, chance 0.001, rank 2 of 6 |  | [Evasive](https://wiki.mushureport.com/wiki/Ruby) |
| ✓ | signature | Ruby | untap | 36/306 cards (12%), 4.3x the rest, chance 0.000, rank 1 of 6 |  | [readying exerted characters](https://wiki.mushureport.com/wiki/Ruby) |
| ✓ | signature | Sapphire | resource_gain | 45/303 cards (15%), 106.3x the rest, chance 0.000, rank 1 of 6 |  | [more than one card into the inkwell](https://wiki.mushureport.com/wiki/Sapphire) |
| ✗ | signature | Sapphire | cost_reduction | 15/303 cards (5%), 1.1x the rest, chance 0.404, rank 3 of 6 | not 1.5x the rest of the game | [items cost less](https://wiki.mushureport.com/wiki/Sapphire) |
| ✓ | signature | Sapphire | stat_loss | 23/303 cards (8%), 3.1x the rest, chance 0.000, rank 2 of 6 |  | [strength reduction more than Amber](https://wiki.mushureport.com/wiki/Sapphire) |
| ✗ | signature | Sapphire | immunity | 42/303 cards (14%), 1.1x the rest, chance 0.222, rank 4 of 6 | not 1.5x the rest of the game | [Ward it can grant](https://wiki.mushureport.com/wiki/Sapphire) |
| ✓ | signature | Steel | damage | 65/303 cards (21%), 4.5x the rest, chance 0.000, rank 1 of 6 |  | [direct damage](https://www.wargamer.com/disney-lorcana/colors) |
| ✗ | signature | Steel | bodyguard | 1/303 cards (0%), infx the rest, chance 0.175, rank 1 of 6 | could be chance (5%) | [Bodyguard](https://wiki.mushureport.com/wiki/Steel) |
| ✓ | signature | Steel | attack_lock | 11/303 cards (4%), 8.7x the rest, chance 0.000, rank 1 of 6 |  | [challenge prevention](https://wiki.mushureport.com/wiki/Steel) |
| ✓ | archetype | Amber | sustain | recipe score 0.48, 7.8x the other factions, 40 cards |  | [protection and healing](https://www.wargamer.com/disney-lorcana/colors) |
| ✓ | archetype | Amethyst | card_advantage | recipe score 0.60, 2.0x the other factions, 103 cards |  | [extra card draw](https://www.wargamer.com/disney-lorcana/colors) |
| ✓ | archetype | Emerald | disruption | recipe score 0.41, 2.3x the other factions, 45 cards |  | [discard and bounce](https://www.wargamer.com/disney-lorcana/colors) |
| ✓ | archetype | Ruby | aggro_tempo | recipe score 0.69, 7.4x the other factions, 101 cards |  | [aggression and Rush](https://www.wargamer.com/disney-lorcana/colors) |
| ✓ | archetype | Ruby | control | recipe score 0.41, 1.6x the other factions, 44 cards |  | [Ruby Control](https://www.wargamer.com/disney-lorcana/colors) |
| ✓ | archetype | Sapphire | ramp | recipe score 0.65, 16.6x the other factions, 75 cards |  | [ramp](https://www.wargamer.com/disney-lorcana/colors) |
| ✗ | archetype | Steel | control | under 1.5x the other factions | recipe not 1.5x the other factions | [control decks](https://www.wargamer.com/disney-lorcana/colors) |
| ✓ | archetype | Steel | fortress | recipe score 0.93, 3.9x the other factions, 103 cards |  | [defence, defensive fortress](https://wiki.mushureport.com/wiki/Steel) |
| ✓ | splash | Amber | draw |  |  | [less card draw than Amethyst or Steel](https://wiki.mushureport.com/wiki/Amber) |
| ✗ | splash | Amber | stat_loss |  | missing from the splash list | [strength reduction weaker than Sapphire's](https://wiki.mushureport.com/wiki/Amber) |
| ✓ | splash | Amber | hand_disruption |  |  | [discard shared with Emerald](https://wiki.mushureport.com/wiki/Amber) |
| ✗ | splash | Amethyst | bounce_enemy |  | missing from the splash list | [bounce less than Emerald](https://wiki.mushureport.com/wiki/Amethyst) |
| ✗ | splash | Amethyst | evasion |  | missing from the splash list | [Evasive less than Emerald and Ruby](https://wiki.mushureport.com/wiki/Amethyst) |
| ✓ | splash | Emerald | haste |  |  | [Rush less than Amethyst and Ruby](https://wiki.mushureport.com/wiki/Emerald) |
| ✓ | splash | Ruby | disable |  |  | [exerting less than Amethyst](https://wiki.mushureport.com/wiki/Ruby) |
| ✗ | splash | Ruby | stat_gain |  | missing from the splash list | [strength increase less than Emerald](https://wiki.mushureport.com/wiki/Ruby) |
| ✗ | splash | Sapphire | heal |  | missing from the splash list | [healing weaker than Amber's](https://wiki.mushureport.com/wiki/Sapphire) |
| ✗ | splash | Sapphire | selection |  | missing from the splash list | [filtering less than Amethyst](https://wiki.mushureport.com/wiki/Sapphire) |
| ✓ | splash | Sapphire | untap |  |  | [readying less than Ruby](https://wiki.mushureport.com/wiki/Sapphire) |
| ✓ | splash | Steel | stat_gain |  |  | [strength increase less than Emerald](https://wiki.mushureport.com/wiki/Steel) |
| ✓ | combo | Madam Mim - Fox | Tinker Bell - Giant Fairy | linked by engine, relation |  | [bounce heals her, replay repeats damage](https://geekydomain.com/blogs/guides/competitive-amethyst-steel-bounce-guide) |
| ✓ | combo | Madam Mim - Snake | Merlin - Rabbit | linked by engine, relation, type |  | [bounce and replay draws two](https://geekydomain.com/blogs/guides/competitive-amethyst-steel-bounce-guide) |
| ✓ | combo | Madam Mim - Fox | Merlin - Rabbit | linked by engine, relation, type |  | [bounce and replay draws two](https://geekydomain.com/blogs/guides/competitive-amethyst-steel-bounce-guide) |
| ✓ | combo | Tinker Bell - Giant Fairy | Grab Your Sword | linked by role |  | [she sings it for free](https://geekydomain.com/blogs/guides/competitive-amethyst-steel-bounce-guide) |
| ✓ | combo | Tinker Bell - Giant Fairy | A Whole New World | linked by role |  | [she sings it for free](https://geekydomain.com/blogs/guides/competitive-amethyst-steel-bounce-guide) |
| ✓ | combo | Captain Hook - Forceful Duelist | Mr. Smee - Bumbling Mate | linked by relation, type |  | [Hook keeps Smee alive](https://geekydomain.com/blogs/guides/competitive-amethyst-steel-bounce-guide) |
| ✓ | combo | Tipo - Growing Son | Madam Mim - Snake | linked by engine, relation, type |  | [quest, bounce, replay or ink](https://spellmana.com/amethyst-sapphire-deck-guide-lorcana/) |
| ✓ | combo | Merlin - Goat | Madam Mim - Snake | linked by relation, type |  | [lore on enter and leave, bounce](https://spellmana.com/amethyst-sapphire-deck-guide-lorcana/) |
| ✓ | combo | Merlin - Goat | Madam Mim - Fox | linked by relation, type |  | [lore on enter and leave, bounce](https://www.wargamer.com/best-disney-lorcana-cards) |
| ✓ | combo | Merlin - Goat | Arthur - Wizard's Apprentice | linked by relation, type |  | [lore on enter and leave, bounce](https://www.wargamer.com/best-disney-lorcana-cards) |
| ✓ | combo | Merlin - Goat | Bibbidi Bobbidi Boo | linked by relation |  | [cheaper replays of Merlin](https://www.wargamer.com/best-disney-lorcana-cards) |
| ✓ | combo | Stitch - Rock Star | Stitch - Carefree Surfer | linked by type |  | [Shift onto Rock Star](https://www.wargamer.com/best-disney-lorcana-cards) |

## Marvel Snap

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | combo | M.O.D.O.K. | Hela | linked by keyword, relation, role, role_tree |  | [discard, then Hela brings them back](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✗ | combo | Morbius | Swarm |  | both cards there, no connection | [Morbius grows per discard](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✗ | combo | Morbius | Apocalypse |  | both cards there, no connection | [Morbius grows per discard](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✗ | combo | Wong | Odin |  | a card name is not in the library | [Wong doubles Odin's On Reveal](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Ironheart | Odin | linked by keyword, role |  | [Odin repeats the power boost](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Black Panther | Odin | linked by keyword, role |  | [Odin repeats the power boost](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Storm | White Tiger | linked by keyword, role_tree |  | [places cards in the flooded location](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Storm | Doctor Doom | linked by keyword, role_tree |  | [places cards in the flooded location](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Brood | Wolfsbane | linked by engine, keyword, relation, role |  | [Wolfsbane gains power as the fourth card](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Moon Girl | Devil Dinosaur | linked by relation |  | [doubled hand boosts Devil Dinosaur](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Professor X | Devil Dinosaur | linked by keyword, role_tree |  | [named together](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Shuri | Typhoid Mary | linked by engine, relation, role |  | [Shuri doubles the next card's power](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Shuri | Red Skull | linked by engine, relation, role |  | [Shuri doubles the next card's power](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Zero | Titania | linked by role |  | [removes the drawback](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Zero | Ebony Maw | linked by role_tree |  | [removes the drawback](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Sauron | Ebony Maw | linked by keyword, role_tree |  | [removes the drawback](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Taskmaster | Typhoid Mary | linked by role |  | [Taskmaster copies the last card's power](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Taskmaster | Red Skull | linked by role |  | [Taskmaster copies the last card's power](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Cable | Mantis | linked by engine, keyword, relation, role |  | [take cards from the opponent's deck](https://www.pocketgamer.com/marvel-snap/best-decks/) |
| ✓ | combo | Carnage | Nova | linked by engine, relation, role |  | [buff all cards on the board](https://www.pocketgamer.com/marvel-snap/best-decks/) |
| ✓ | combo | Ant Man | Angela | linked by engine, role |  | [points in the third location](https://www.pocketgamer.com/marvel-snap/best-decks/) |
| ✓ | combo | Doctor Octopus | Mojo | linked by relation, role |  | [+6 when the spot is empty](https://www.pocketgamer.com/marvel-snap/best-decks/) |
| ✗ | combo | Wave | Death |  | both cards there, no connection | [the deck is built around the two](https://www.pocketgamer.com/marvel-snap/best-decks/) |
| ✗ | combo | The Collector | Moon Girl |  | both cards there, no connection | [Collector buffs, Moon Girl copies](https://www.pocketgamer.com/marvel-snap/best-decks/) |

## Monster Train

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | signature | Hellhorned | multi_attack | 3/39 cards (8%), 1.6x the rest, chance 0.324, rank 2 of 7 | could be chance (5%) | [Multistrike](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✓ | signature | Hellhorned | temporary_buff | 4/39 cards (10%), 4.8x the rest, chance 0.027, rank 1 of 7 |  | [Rage](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✗ | signature | Hellhorned | tribal | 0/39 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 7 | no card of the faction has it | [Imps](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✗ | signature | Hellhorned | summon | 0/39 cards (0%), 0.0x the rest, chance 1.000, rank 5 of 7 | no card of the faction has it | [Imp Parade makes Imps](https://progameguides.com/monster-train/best-builds-in-monster-train/) |
| ✗ | signature | Awoken | multi_target_attack | 2/39 cards (5%), 3.0x the rest, chance 0.207, rank 2 of 7 | could be chance (5%) | [Sweep](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✗ | signature | Awoken | tank | 0/39 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 7 | no card of the faction has it | [giant minions that protect others](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✓ | signature | Stygian Guard | damage_over_time | 17/41 cards (41%), 2.0x the rest, chance 0.005, rank 1 of 7 |  | [Frostbite](https://progameguides.com/monster-train/best-builds-in-monster-train/) |
| ✓ | signature | Umbra | sacrifice | 7/46 cards (15%), 17.2x the rest, chance 0.000, rank 1 of 7 |  | [buffing units by killing other units](https://indiecator.org/2021/07/12/monster-train-my-favourite-clans/) |
| ✗ | signature | Umbra | stat_gain | 10/46 cards (22%), 1.1x the rest, chance 0.403, rank 3 of 7 | not 1.5x the rest of the game | [eating Morsels for their buffs](https://progameguides.com/monster-train/best-builds-in-monster-train/) |
| ✓ | signature | Melting Remnant | death_trigger | 9/40 cards (22%), 6.5x the rest, chance 0.000, rank 1 of 7 |  | [minions with death abilities](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✓ | signature | Melting Remnant | revive | 7/40 cards (18%), 20.3x the rest, chance 0.000, rank 1 of 7 |  | [Reform](https://progameguides.com/monster-train/best-builds-in-monster-train/) |
| ✓ | signature | Melting Remnant | self_destruct | 10/40 cards (25%), infx the rest, chance 0.000, rank 1 of 7 |  | [Burnout](https://progameguides.com/monster-train/best-builds-in-monster-train/) |
| ✗ | signature | Melting Remnant | other_death_trigger | 0/40 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 7 | no card of the faction has it | [Harvest](https://indiecator.org/2021/07/12/monster-train-my-favourite-clans/) |
| ✗ | signature | Wurmkin | buff | 14/42 cards (33%), 1.0x the rest, chance 0.594, rank 5 of 7 | not 1.5x the rest of the game | [Infused cards and Eggs buff monsters](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✗ | archetype | Hellhorned | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [glass-cannon offence](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✗ | archetype | Hellhorned | tribal | under 1.5x the other factions | recipe not 1.5x the other factions | [Imp build](https://progameguides.com/monster-train/best-builds-in-monster-train/) |
| ✗ | archetype | Awoken | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [tanks](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✓ | archetype | Stygian Guard | spellslinger | recipe score 1.23, 5.5x the other factions, 13 cards |  | [powerful spells](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✓ | archetype | Stygian Guard | poison_attrition | recipe score 1.71, 7.0x the other factions, 9 cards |  | [Frostbite](https://progameguides.com/monster-train/best-builds-in-monster-train/) |
| ✓ | archetype | Umbra | sacrifice | recipe score 0.92, 1.9x the other factions, 7 cards |  | [killing units to buff others](https://indiecator.org/2021/07/12/monster-train-my-favourite-clans/) |
| ✓ | archetype | Melting Remnant | sacrifice | recipe score 2.69, 13.5x the other factions, 21 cards |  | [wanting minions to die](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✓ | combo | Molded | Rector Flicker | linked by keyword, relation |  | [returns the fallen Flicker by Reform](https://progameguides.com/monster-train/best-builds-in-monster-train/) |
| ✗ | combo | Crushing Demise | Rector Flicker |  | both cards there, no connection | [Flicker upgrades on each death](https://progameguides.com/monster-train/best-builds-in-monster-train/) |
| ✓ | combo | Cannibalize | Penumbra | linked by engine |  | [Morsels for Penumbra to Gorge on](https://progameguides.com/monster-train/best-builds-in-monster-train/) |
| ✗ | combo | Morselmaker | Penumbra |  | both cards there, no connection | [Morsels for Penumbra](https://progameguides.com/monster-train/best-builds-in-monster-train/) |

## Magic: The Gathering

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | White | buff | 2450/4282 cards (57%), 1.2x the rest, chance 0.000, rank 2 of 6 |  | [+1/+1 counters and team pumps](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✗ | signature | White | summon | 683/4282 cards (16%), 1.5x the rest, chance 0.000, rank 1 of 6 | not 1.5x the rest of the game | [token generation](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | White | heal | 758/4282 cards (18%), 3.3x the rest, chance 0.000, rank 1 of 6 |  | [life gain](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | White | lifesteal | 1016/4282 cards (24%), 1.6x the rest, chance 0.000, rank 1 of 6 |  | [lifelink](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | White | first_strike | 396/4282 cards (9%), 2.6x the rest, chance 0.000, rank 1 of 6 |  | [first strike and double strike](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | White | evasion | 1068/4282 cards (25%), 1.3x the rest, chance 0.000, rank 2 of 6 |  | [flying](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | White | protection | 528/4282 cards (12%), 1.7x the rest, chance 0.000, rank 1 of 6 |  | [protection, indestructible](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | White | board_wipe | 122/4282 cards (3%), 2.7x the rest, chance 0.000, rank 1 of 6 |  | [destroy all creatures](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | White | attack_lock | 26/4282 cards (1%), 5.9x the rest, chance 0.000, rank 1 of 6 |  | [Pacifism-like effects](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | White | cost_increase | 96/4282 cards (2%), 1.4x the rest, chance 0.006, rank 2 of 6 |  | [taxing](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | White | blink | 71/4282 cards (2%), 3.3x the rest, chance 0.000, rank 1 of 6 |  | [flicker](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Blue | draw | 1237/4283 cards (29%), 2.5x the rest, chance 0.000, rank 1 of 6 |  | [card draw](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Blue | selection | 589/4283 cards (14%), 1.6x the rest, chance 0.000, rank 2 of 6 |  | [filtering and scry](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Blue | counter_spell | 361/4283 cards (8%), 6.2x the rest, chance 0.000, rank 1 of 6 |  | [counterspells](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Blue | evasion | 1304/4283 cards (30%), 1.7x the rest, chance 0.000, rank 1 of 6 |  | [can't be blocked, flying](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Blue | disable | 141/4283 cards (3%), 2.7x the rest, chance 0.000, rank 1 of 6 |  | [freeze and lockdown](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Blue | bounce_enemy | 219/4283 cards (5%), 12.9x the rest, chance 0.000, rank 1 of 6 |  | [return to hand](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Blue | mill | 217/4283 cards (5%), 2.1x the rest, chance 0.000, rank 1 of 6 |  | [milling](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Blue | copy | 365/4283 cards (9%), 2.8x the rest, chance 0.000, rank 1 of 6 |  | [copying permanents and spells](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Blue | steal | 137/4283 cards (3%), 3.3x the rest, chance 0.000, rank 1 of 6 |  | [permanently stealing permanents](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Blue | extra_turn | 31/4283 cards (1%), 6.6x the rest, chance 0.000, rank 1 of 6 |  | [Time Walk](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Blue | on_spell | 354/4283 cards (8%), 2.2x the rest, chance 0.000, rank 1 of 6 |  | [instant and sorcery triggers](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Black | destroy | 831/4371 cards (19%), 3.4x the rest, chance 0.000, rank 1 of 6 |  | [destroying creatures](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Black | deathtouch | 872/4371 cards (20%), 2.8x the rest, chance 0.000, rank 1 of 6 |  | [deathtouch](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Black | stat_loss | 403/4371 cards (9%), 2.7x the rest, chance 0.000, rank 1 of 6 |  | [-N/-N](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Black | hand_disruption | 283/4371 cards (6%), 11.9x the rest, chance 0.000, rank 1 of 6 |  | [discard as an effect](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✗ | signature | Black | life_payment | 478/4371 cards (11%), 1.5x the rest, chance 0.000, rank 2 of 6 | not 1.5x the rest of the game | [life loss as a cost](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Black | sacrifice | 848/4371 cards (19%), 2.1x the rest, chance 0.000, rank 1 of 6 |  | [sacrifice its own creatures](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Black | revive | 375/4371 cards (9%), 3.0x the rest, chance 0.000, rank 1 of 6 |  | [reanimation](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Black | other_death_trigger | 197/4371 cards (5%), 3.6x the rest, chance 0.000, rank 1 of 6 |  | [rewards for death](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Black | tutor | 383/4371 cards (9%), 0.9x the rest, chance 0.990, rank 3 of 6 |  | [tutoring for any card](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Black | lifesteal | 987/4371 cards (23%), 1.5x the rest, chance 0.000, rank 2 of 6 |  | [drain life, lifelink](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Red | direct_damage | 1367/4374 cards (31%), 3.5x the rest, chance 0.000, rank 1 of 6 |  | [damage to players](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Red | aoe_damage | 996/4374 cards (23%), 3.1x the rest, chance 0.000, rank 1 of 6 |  | [damage to several targets](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Red | haste | 803/4374 cards (18%), 8.1x the rest, chance 0.000, rank 1 of 6 |  | [haste](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Red | temporary_buff | 1158/4374 cards (26%), 1.5x the rest, chance 0.000, rank 1 of 6 |  | [+N/+0](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Red | multi_attack | 173/4374 cards (4%), 1.7x the rest, chance 0.000, rank 2 of 6 |  | [double strike, extra attack](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Red | forced_attack | 4/4374 cards (0%), 6.6x the rest, chance 0.029, rank 1 of 6 |  | [forced attack, must attack](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Red | random_effect | 250/4374 cards (6%), 2.7x the rest, chance 0.000, rank 1 of 6 |  | [random destruction, chaotic play](https://edhrec.com/articles/foundations-choosing-your-color) |
| ✓ | signature | Red | steal | 109/4374 cards (2%), 2.1x the rest, chance 0.000, rank 2 of 6 |  | [temporary stealing](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Red | cant_block | 89/4374 cards (2%), 1.3x the rest, chance 0.031, rank 2 of 6 |  | [can't block](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Green | stat_gain | 1030/4236 cards (24%), 1.8x the rest, chance 0.000, rank 1 of 6 |  | [+1/+1 counters](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✗ | signature | Green | summon | 635/4236 cards (15%), 1.4x the rest, chance 0.000, rank 2 of 6 | not 1.5x the rest of the game | [token generation](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Green | resource_gain | 314/4236 cards (7%), 1.8x the rest, chance 0.000, rank 2 of 6 |  | [mana production, extra lands](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Green | excess_damage | 967/4236 cards (23%), 1.5x the rest, chance 0.000, rank 2 of 6 |  | [trample](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Green | tutor | 586/4236 cards (14%), 1.6x the rest, chance 0.000, rank 1 of 6 |  | [tutoring for creatures and lands](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✗ | signature | Green | free_play | 127/4236 cards (3%), 1.1x the rest, chance 0.146, rank 3 of 6 | not 1.5x the rest of the game | [creatures from hand onto the battlefield](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Green | heal | 361/4236 cards (9%), 1.1x the rest, chance 0.157, rank 3 of 6 |  | [life gain](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✗ | archetype | White | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [small creatures, tokens, team pumps](https://edhrec.com/articles/foundations-choosing-your-color) |
| ✓ | archetype | Blue | control | recipe score 1.11, 11.1x the other factions, 1369 cards |  | [counterspells, card draw](https://edhrec.com/articles/foundations-choosing-your-color) |
| ✓ | archetype | Blue | card_advantage | recipe score 0.97, 15.1x the other factions, 1645 cards |  | [card draw, library manipulation](https://edhrec.com/articles/foundations-choosing-your-color) |
| ✓ | archetype | Black | graveyard | recipe score 1.13, 8.2x the other factions, 1705 cards |  | [graveyard recursion and reanimation](https://edhrec.com/articles/foundations-choosing-your-color) |
| ✓ | archetype | Black | sacrifice | recipe score 0.83, 10.5x the other factions, 1162 cards |  | [sacrifice, rewards for death](https://edhrec.com/articles/foundations-choosing-your-color) |
| ✗ | archetype | Black | control | under 1.5x the other factions | recipe not 1.5x the other factions | [creature removal](https://edhrec.com/articles/foundations-choosing-your-color) |
| ✓ | archetype | Red | burn | recipe score 2.31, 84.9x the other factions, 773 cards |  | [damage to creatures and players](https://edhrec.com/articles/foundations-choosing-your-color) |
| ✓ | archetype | Red | chaos | recipe score 0.35, 4.5x the other factions, 306 cards |  | [random card play](https://edhrec.com/articles/foundations-choosing-your-color) |
| ✓ | archetype | Red | aggro_tempo | recipe score 0.81, 5.0x the other factions, 2376 cards |  | [haste](https://edhrec.com/articles/foundations-choosing-your-color) |
| ✗ | archetype | Green | ramp | under 1.5x the other factions | recipe not 1.5x the other factions | [mana ramp and mana creatures](https://edhrec.com/articles/foundations-choosing-your-color) |
| ✓ | splash | White | draw |  |  | [card draw is tertiary](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | splash | White | counter_spell |  |  | [counterspell is tertiary](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✗ | splash | White | immunity |  | missing from the splash list | [hexproof is tertiary](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | splash | White | excess_damage |  |  | [trample is tertiary](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✗ | splash | White | cast_from_zone |  | missing from the splash list | [casting from the graveyard is tertiary](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | splash | Blue | stat_gain |  |  | [+1/+1 counters are tertiary](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | splash | Blue | excess_damage |  |  | [trample is tertiary](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | splash | Black | first_strike |  |  | [first strike is tertiary](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | splash | Black | steal |  |  | [permanently stealing is tertiary](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | splash | Black | excess_damage |  |  | [trample is tertiary](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | splash | Red | stat_gain |  |  | [+1/+1 counters are tertiary](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | splash | Red | draw |  |  | [card draw is tertiary](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | splash | Red | extra_turn |  |  | [Time Walk is tertiary](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | splash | Green | evasion |  |  | [flying is tertiary](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✗ | splash | Green | cast_from_zone |  | missing from the splash list | [casting from the graveyard is tertiary](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | combo | Sanguine Bond | Exquisite Blood | linked by engine, role |  | [life gain and life loss loop](https://edhrec.com/combos/early-game-2-card-combos) |
| ✓ | combo | Vito, Thorn of the Dusk Rose | Exquisite Blood | linked by engine, relation, role |  | [life gain and life loss loop](https://edhrec.com/combos/early-game-2-card-combos) |
| ✓ | combo | Sanguine Bond | Bloodthirsty Conqueror | linked by engine, role |  | [life gain and life loss loop](https://edhrec.com/combos/early-game-2-card-combos) |
| ✗ | combo | Demonic Consultation | Thassa's Oracle |  | both cards there, no connection | [exile the library, win](https://edhrec.com/combos/early-game-2-card-combos) |
| ✓ | combo | Tainted Pact | Thassa's Oracle | linked by relation |  | [exile the library, win](https://edhrec.com/combos/early-game-2-card-combos) |
| ✗ | combo | Dramatic Reversal | Isochron Scepter |  | a card name is not in the library | [infinite mana](https://edhrec.com/combos/early-game-2-card-combos) |
| ✓ | combo | Gravecrawler | Phyrexian Altar | linked by relation |  | [infinite death triggers](https://edhrec.com/combos/early-game-2-card-combos) |
| ✓ | combo | Dualcaster Mage | Twinflame | linked by engine, relation |  | [infinite creature tokens](https://edhrec.com/combos/early-game-2-card-combos) |
| ✓ | combo | Curiosity | Niv-Mizzet, Parun | linked by engine, role, role_tree |  | [infinite draw and damage](https://edhrec.com/combos/early-game-2-card-combos) |
| ✗ | combo | Basalt Monolith | Forsaken Monument |  | a card name is not in the library | [infinite colorless mana](https://edhrec.com/combos/early-game-2-card-combos) |
| ✗ | combo | The Gitrog Monster | Dakmor Salvage |  | a card name is not in the library | [infinite self-mill](https://edhrec.com/combos/early-game-2-card-combos) |
| ✗ | combo | Splinter Twin | Pestermite |  | a card name is not in the library | [infinite hasty tokens](https://edhrec.com/combos/ur/2905-4702) |
| ✓ | combo | Kiki-Jiki, Mirror Breaker | Restoration Angel | linked by engine, relation |  | [infinite hasty tokens](https://edhrec.com/combos/boros/618-1090) |
| ✓ | combo | Saheeli Rai | Felidar Guardian | linked by engine, relation |  | [infinite hasty tokens](https://edhrec.com/combos/jeskai/142-2781) |
| ✗ | combo | Inverter of Truth | Thassa's Oracle |  | both cards there, no connection | [win the game](https://commanderspellbook.com/combo/1295-2503-2726) |

## Legends of Runeterra

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Demacia | buff | 97/203 cards (48%), 1.2x the rest, chance 0.029, rank 2 of 10 |  | [buffing allies](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✓ | signature | Demacia | shield | 20/203 cards (10%), 2.8x the rest, chance 0.000, rank 1 of 10 |  | [Barrier](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✗ | signature | Demacia | board_presence | 15/203 cards (7%), 0.5x the rest, chance 0.997, rank 8 of 10 | not 1.5x the rest of the game | [strength in numbers](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✓ | signature | Demacia | target_choice | 27/203 cards (13%), 4.4x the rest, chance 0.000, rank 1 of 10 |  | [Challenger](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✓ | signature | Demacia | damage_reduction | 17/203 cards (8%), 8.7x the rest, chance 0.000, rank 1 of 10 |  | [Tough](https://www.pcgamer.com/uk/legends-of-runeterra-regions-factions) |
| ✗ | signature | Demacia | extra_turn | 0/203 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 10 | no card of the faction has it | [Rally](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✓ | signature | Freljord | attack_zero | 23/210 cards (11%), 11.3x the rest, chance 0.000, rank 1 of 10 |  | [Frostbite](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✓ | signature | Freljord | resource_gain | 10/210 cards (5%), 1.9x the rest, chance 0.049, rank 2 of 10 |  | [mana ramp, extra mana gems](https://www.pcgamer.com/uk/legends-of-runeterra-regions-factions) |
| ✗ | signature | Freljord | high_cost | 0/210 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 10 | no card of the faction has it | [the biggest units](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✗ | signature | Freljord | board_wipe | 1/210 cards (0%), 0.4x the rest, chance 0.903, rank 6 of 10 | not 1.5x the rest of the game | [area board clears](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✓ | signature | Ionia | return_to_hand | 50/235 cards (21%), 7.0x the rest, chance 0.000, rank 1 of 10 |  | [Recall](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✓ | signature | Ionia | bounce_enemy | 37/235 cards (16%), 16.1x the rest, chance 0.000, rank 1 of 10 |  | [Recall](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✓ | signature | Ionia | evasion | 43/235 cards (18%), 1.4x the rest, chance 0.023, rank 3 of 10 |  | [Elusive](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✓ | signature | Ionia | disable | 29/235 cards (12%), 2.9x the rest, chance 0.000, rank 2 of 10 |  | [Stun](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✓ | signature | Ionia | counter_spell | 4/235 cards (2%), 5.0x the rest, chance 0.020, rank 2 of 10 |  | [Deny](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✓ | signature | Noxus | damage | 112/217 cards (52%), 1.9x the rest, chance 0.000, rank 1 of 10 |  | [many ways to deal damage](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✓ | signature | Noxus | excess_damage | 78/217 cards (36%), 1.9x the rest, chance 0.000, rank 1 of 10 |  | [Overwhelm](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✗ | signature | Noxus | friendly_fire | 16/217 cards (7%), 4.0x the rest, chance 0.000, rank 1 of 10 | could be chance (5%) | [damaging its own units for benefit](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✓ | signature | Noxus | direct_damage | 110/217 cards (51%), 2.2x the rest, chance 0.000, rank 1 of 10 |  | [burn finishers](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✓ | signature | Piltover & Zaun | on_spell | 8/226 cards (4%), 3.2x the rest, chance 0.009, rank 1 of 10 |  | [units that gain from spells](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✗ | signature | Piltover & Zaun | generate_cards | 40/226 cards (18%), 1.3x the rest, chance 0.068, rank 3 of 10 | not 1.5x the rest of the game | [card generation](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✓ | signature | Piltover & Zaun | copy | 20/226 cards (9%), 2.4x the rest, chance 0.001, rank 1 of 10 |  | [copying](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✓ | signature | Piltover & Zaun | draw | 44/226 cards (19%), 2.9x the rest, chance 0.000, rank 1 of 10 |  | [card draw](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✓ | signature | Piltover & Zaun | cost_reduction | 23/226 cards (10%), 3.0x the rest, chance 0.000, rank 1 of 10 |  | [discounts](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✓ | signature | Shadow Isles | death_trigger | 29/213 cards (14%), 6.8x the rest, chance 0.000, rank 1 of 10 |  | [Last Breath](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✓ | signature | Shadow Isles | sacrifice | 27/213 cards (13%), 21.8x the rest, chance 0.000, rank 1 of 10 |  | [sacrifice](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✓ | signature | Shadow Isles | revive | 20/213 cards (9%), 21.5x the rest, chance 0.000, rank 1 of 10 |  | [resurrection](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✓ | signature | Shadow Isles | self_destruct | 40/213 cards (19%), 2.2x the rest, chance 0.000, rank 1 of 10 |  | [Ephemeral](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✓ | signature | Shadow Isles | lifesteal | 45/213 cards (21%), 1.6x the rest, chance 0.002, rank 1 of 10 |  | [Drain and Lifesteal](https://www.pcgamer.com/uk/legends-of-runeterra-regions-factions) |
| ✓ | signature | Shadow Isles | evasion | 56/213 cards (26%), 2.1x the rest, chance 0.000, rank 1 of 10 |  | [Fearsome](https://www.pcgamer.com/uk/legends-of-runeterra-regions-factions) |
| ✓ | signature | Bilgewater | self_mill | 4/225 cards (2%), 7.3x the rest, chance 0.008, rank 2 of 10 |  | [Toss and Deep](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |
| ✓ | signature | Bilgewater | draw | 32/225 cards (14%), 2.0x the rest, chance 0.001, rank 2 of 10 |  | [card draw](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✗ | signature | Targon | generate_cards | 42/234 cards (18%), 1.3x the rest, chance 0.052, rank 2 of 10 | not 1.5x the rest of the game | [Invoke and card generation](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✓ | signature | Targon | silence | 5/234 cards (2%), 7.3x the rest, chance 0.003, rank 1 of 10 |  | [Hush](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✓ | signature | Shurima | selection | 14/263 cards (5%), 1.8x the rest, chance 0.040, rank 2 of 10 |  | [Predict](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✓ | signature | Shurima | shield | 17/263 cards (6%), 1.7x the rest, chance 0.031, rank 4 of 10 |  | [Spellshield](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✓ | signature | Shurima | counter_spell | 5/263 cards (2%), 6.4x the rest, chance 0.005, rank 1 of 10 |  | [counterspell](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✗ | signature | Bandle City | summon | 15/249 cards (6%), 0.4x the rest, chance 1.000, rank 9 of 10 | not 1.5x the rest of the game | [token generation](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✗ | signature | Bandle City | board_presence | 15/249 cards (6%), 0.4x the rest, chance 1.000, rank 9 of 10 | not 1.5x the rest of the game | [swarm](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✓ | signature | Bandle City | merge_attach | 19/249 cards (8%), 2.2x the rest, chance 0.002, rank 1 of 10 |  | [Attach](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✓ | archetype | Demacia | aggro_tempo | recipe score 0.41, 1.9x the other factions, 48 cards |  | [board tempo](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✗ | archetype | Freljord | control | under 1.5x the other factions | recipe not 1.5x the other factions | [control](https://www.pcgamer.com/uk/legends-of-runeterra-regions-factions) |
| ✗ | archetype | Freljord | ramp | under 1.5x the other factions | recipe not 1.5x the other factions | [mana ramp, biggest units](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✓ | archetype | Ionia | aggro_tempo | recipe score 0.43, 2.0x the other factions, 76 cards |  | [tempo](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✗ | archetype | Noxus | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [aggro and tempo](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✗ | archetype | Noxus | burn | under 1.5x the other factions | recipe not 1.5x the other factions | [burn finishers](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✓ | archetype | Piltover & Zaun | spellslinger | recipe score 0.78, 2.2x the other factions, 28 cards |  | [spellslinger](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✗ | archetype | Piltover & Zaun | card_advantage | under 1.5x the other factions | recipe not 1.5x the other factions | [fast-draw decks](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✓ | archetype | Shadow Isles | sacrifice | recipe score 2.11, 17.2x the other factions, 94 cards |  | [sacrificing units for benefit](https://mobalytics.gg/blog/lor/legends-of-runeterra-regions-overview/) |
| ✓ | archetype | Shadow Isles | control | recipe score 0.57, 1.7x the other factions, 61 cards |  | [control](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✓ | archetype | Shadow Isles | swarm | recipe score 0.48, 2.9x the other factions, 72 cards |  | [swarming the board](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |
| ✗ | archetype | Bilgewater | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [Pirate Aggro](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✓ | archetype | Targon | card_advantage | recipe score 1.00, 2.1x the other factions, 30 cards |  | [never run out of cards](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✗ | archetype | Shurima | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [explosive tempo](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✗ | archetype | Bandle City | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [go-wide swarm](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✗ | archetype | Bandle City | tribal | under 1.5x the other factions | recipe not 1.5x the other factions | [Yordle and Fae](https://gamersdecide.com/articles/legends-of-runeterra-best-regions) |
| ✓ | splash | Demacia | direct_damage |  |  | [direct damage is limited](https://www.pcgamer.com/uk/legends-of-runeterra-regions-factions) |
| ✓ | combo | Ashe | Rimetusk Shaman | linked by keyword, relation |  | [Frostbite the strongest enemy](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |
| ✗ | combo | Lulu | Flame Chompers! |  | both cards there, no connection | [early tempo swing](https://mobalytics.gg/?p=15986) |
| ✗ | combo | Towering Pairofant | Curious Changelings |  | both cards there, no connection | [surprise lethal](https://mobalytics.gg/?p=15986) |
| ✓ | combo | The Grand Plaza | Aurelion Sol | linked by engine, relation |  | [board, then finisher](https://mobalytics.gg/blog/lor/lor-5-top-decks-ranked/) |
| ✓ | combo | Solari Sunforger | Starshaping | linked by relation |  | [heal back](https://mobalytics.gg/blog/lor/lor-5-top-decks-ranked/) |
| ✗ | combo | Hush | Single Combat |  | both cards there, no connection | [answer threats](https://mobalytics.gg/blog/lor/lor-5-top-decks-ranked/) |
| ✗ | combo | Karma | Lux |  | both cards there, no connection | [Lux stacks twice as fast](https://mobalytics.gg/blog/lor-how-to-play-control-ezreal-lux-karma/) |
| ✓ | combo | Ezreal | Trueshot Barrage | linked by role |  | [stabilises and levels Ezreal](https://mobalytics.gg/blog/lor-how-to-play-control-ezreal-lux-karma/) |
| ✗ | combo | Entreat | Mystic Shot |  | both cards there, no connection | [Entreat fetches Mystic Shot](https://mobalytics.gg/blog/lor-how-to-play-control-ezreal-lux-karma/) |
| ✗ | combo | Chump Whump | Rummage |  | both cards there, no connection | [fuel for the discard](https://mobalytics.gg/blog/lor-how-to-play-control-ezreal-lux-karma/) |
| ✗ | combo | Chump Whump | Get Excited! |  | both cards there, no connection | [fuel for the discard](https://mobalytics.gg/blog/lor-how-to-play-control-ezreal-lux-karma/) |
| ✓ | combo | Judgment | Deny | linked by keyword |  | [Deny protects Judgment](https://mobalytics.gg/blog/lor-how-to-play-control-ezreal-lux-karma/) |
| ✗ | combo | Judgment | Purify |  | both cards there, no connection | [Purify punishes Elusives](https://mobalytics.gg/blog/lor-how-to-play-control-ezreal-lux-karma/) |
| ✓ | combo | Stand Alone | Emerald Awakener | linked by relation |  | [good against aggro](https://mobalytics.gg/blog/lor-how-to-play-control-ezreal-lux-karma/) |
| ✗ | combo | Curious Shellfolk | Ezreal |  | both cards there, no connection | [engine, then Ezreal closes](https://mobalytics.gg/blog/lor/lor-deck-guide-ezreal-vi-pranks/) |
| ✓ | combo | Ezreal | Timewinder | linked by role |  | [two Ezreal triggers](https://mobalytics.gg/blog/lor/lor-deck-guide-ezreal-vi-pranks/) |
| ✗ | combo | Ezreal | Bouncing Bomb |  | both cards there, no connection | [two Ezreal triggers](https://mobalytics.gg/blog/lor/lor-deck-guide-ezreal-vi-pranks/) |
| ✗ | combo | Vi | Ambush |  | both cards there, no connection | [sneaky nexus strike](https://mobalytics.gg/blog/lor/lor-deck-guide-ezreal-vi-pranks/) |
| ✗ | combo | Vi | Sumpworks Map |  | both cards there, no connection | [sneaky nexus strike](https://mobalytics.gg/blog/lor/lor-deck-guide-ezreal-vi-pranks/) |

## Shadowverse

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Forestcraft | combo_sequence | 87/491 cards (18%), 172.4x the rest, chance 0.000, rank 1 of 9 |  | [several cards a turn power other cards](https://shadowverse.fandom.com/wiki/Forestcraft) |
| ✓ | signature | Forestcraft | return_to_hand | 38/491 cards (8%), 14.3x the rest, chance 0.000, rank 1 of 9 |  | [returning its own cards to hand](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✗ | signature | Forestcraft | generate_cards | 113/491 cards (23%), 1.3x the rest, chance 0.002, rank 3 of 9 | not 1.5x the rest of the game | [filling the hand with Fairies](https://shadowverse.fandom.com/wiki/Forestcraft) |
| ✗ | signature | Forestcraft | board_presence | 79/491 cards (16%), 0.7x the rest, chance 1.000, rank 7 of 9 | not 1.5x the rest of the game | [many small followers](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✓ | signature | Swordcraft | tribal | 70/519 cards (13%), 1.6x the rest, chance 0.000, rank 4 of 9 |  | [Officer and Commander traits](https://shadowverse.fandom.com/wiki/Swordcraft) |
| ✓ | signature | Swordcraft | buff | 217/519 cards (42%), 1.4x the rest, chance 0.000, rank 1 of 9 |  | [Commanders boost Officers](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✓ | signature | Runecraft | in_hand_buff | 118/514 cards (23%), 7.3x the rest, chance 0.000, rank 1 of 9 |  | [Spellboost](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✓ | signature | Runecraft | on_spell | 22/514 cards (4%), 23.7x the rest, chance 0.000, rank 1 of 9 |  | [spells boost cards](https://shadowverse.fandom.com/wiki/Runecraft) |
| ✓ | signature | Runecraft | cost_reduction | 51/514 cards (10%), 4.6x the rest, chance 0.000, rank 1 of 9 |  | [Spellboost cost reduction](https://shadowverse.fandom.com/wiki/Runecraft) |
| ✗ | signature | Runecraft | damage | 179/514 cards (35%), 1.1x the rest, chance 0.169, rank 3 of 9 | not 1.5x the rest of the game | [damage through effects](https://shadowverse.fandom.com/wiki/Runecraft) |
| ✗ | signature | Dragoncraft | resource_gain | 45/491 cards (9%), 1.4x the rest, chance 0.016, rank 1 of 9 | not 1.5x the rest of the game | [cards that grant play points](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✗ | signature | Dragoncraft | high_cost | 0/491 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 9 | no card of the faction has it | [large dragons](https://shadowverse.fandom.com/wiki/Dragoncraft) |
| ✓ | signature | Shadowcraft | death_trigger | 170/502 cards (34%), 2.8x the rest, chance 0.000, rank 1 of 9 |  | [Last Words](https://shadowverse.fandom.com/wiki/Shadowcraft) |
| ✓ | signature | Shadowcraft | revive | 51/502 cards (10%), 78.8x the rest, chance 0.000, rank 1 of 9 |  | [Reanimate](https://shadowverse.fandom.com/wiki/Shadowcraft) |
| ✓ | signature | Shadowcraft | sacrifice | 27/502 cards (5%), 6.0x the rest, chance 0.000, rank 1 of 9 |  | [Burial Rite destroys its own follower](https://shadowverse.fandom.com/wiki/Shadowcraft) |
| ✗ | signature | Shadowcraft | coin_economy | 0/502 cards (0%), 0.0x the rest, chance 1.000, rank 6 of 9 | no card of the faction has it | [shadows spent by Necromancy](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✗ | signature | Bloodcraft | life_payment | 33/491 cards (7%), 1.1x the rest, chance 0.297, rank 2 of 9 | not 1.5x the rest of the game | [damaging itself for benefits](https://shadowverse.fandom.com/wiki/Bloodcraft) |
| ✓ | signature | Bloodcraft | low_life | 119/491 cards (24%), infx the rest, chance 0.000, rank 1 of 9 |  | [Vengeance at 10 life or less](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✓ | signature | Havencraft | delayed | 166/494 cards (34%), 4.9x the rest, chance 0.000, rank 1 of 9 |  | [Countdown amulets](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✓ | signature | Portalcraft | deck_condition | 51/480 cards (11%), 11.2x the rest, chance 0.000, rank 1 of 9 |  | [Resonance](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✓ | signature | Portalcraft | generate_cards | 153/480 cards (32%), 1.9x the rest, chance 0.000, rank 1 of 9 |  | [Puppets](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✓ | signature | Portalcraft | tribal | 73/480 cards (15%), 1.8x the rest, chance 0.000, rank 3 of 9 |  | [Machina and Artifacts](https://shadowverse.fandom.com/wiki/Portalcraft) |
| ✓ | archetype | Forestcraft | swarm | recipe score 0.12, 1.8x the other factions, 94 cards |  | [bands of Fairies](https://shadowverse.fandom.com/wiki/Forestcraft) |
| ✓ | archetype | Forestcraft | spellslinger | recipe score 1.10, 2.6x the other factions, 92 cards |  | [chains of cheap cards](https://shadowverse.fandom.com/wiki/Forestcraft) |
| ✓ | archetype | Swordcraft | aggro_tempo | recipe score 0.34, 9.0x the other factions, 160 cards |  | [aggressive tempo](https://shadowverse.fandom.com/wiki/Swordcraft) |
| ✓ | archetype | Swordcraft | tribal | recipe score 0.23, 1.8x the other factions, 70 cards |  | [trait synergy](https://shadowverse.fandom.com/wiki/Swordcraft) |
| ✓ | archetype | Runecraft | spellslinger | recipe score 1.63, 4.6x the other factions, 45 cards |  | [spell-focused](https://shadowverse.fandom.com/wiki/Runecraft) |
| ✗ | archetype | Dragoncraft | ramp | under 1.5x the other factions | recipe not 1.5x the other factions | [play points, then big dragons](https://shadowverse.fandom.com/wiki/Dragoncraft) |
| ✓ | archetype | Shadowcraft | graveyard | recipe score 1.46, 7.2x the other factions, 197 cards |  | [its own destroyed followers](https://shadowverse.fandom.com/wiki/Shadowcraft) |
| ✗ | archetype | Shadowcraft | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [aggressive decks](https://shadowverse.fandom.com/wiki/Shadowcraft) |
| ✓ | archetype | Shadowcraft | control | recipe score 0.32, 1.6x the other factions, 130 cards |  | [control decks](https://shadowverse.fandom.com/wiki/Shadowcraft) |
| ✗ | archetype | Bloodcraft | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [aggressive decks](https://shadowverse.fandom.com/wiki/Bloodcraft) |
| ✗ | archetype | Bloodcraft | control | under 1.5x the other factions | recipe not 1.5x the other factions | [control decks](https://shadowverse.fandom.com/wiki/Bloodcraft) |
| ✗ | archetype | Portalcraft | control | under 1.5x the other factions | recipe not 1.5x the other factions | [control decks](https://shadowverse.fandom.com/wiki/Portalcraft) |
| ✗ | archetype | Portalcraft | spellslinger | under 1.5x the other factions | recipe not 1.5x the other factions | [combo decks](https://shadowverse.fandom.com/wiki/Portalcraft) |

## Stormbound

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Winter | disable | 10/30 cards (33%), infx the rest, chance 0.000, rank 1 of 5 |  | [Freeze](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✓ | signature | Winter | resource_gain | 5/30 cards (17%), infx the rest, chance 0.000, rank 1 of 5 |  | [extra mana](https://stormboundkingdomwars.fandom.com/wiki/Winter_Pact?oldid=7023) |
| ✗ | signature | Winter | aoe_damage | 4/30 cards (13%), 0.6x the rest, chance 0.931, rank 4 of 5 | not 1.5x the rest of the game | [heavy area damage](https://stormboundkingdomwars.fandom.com/wiki/Winter_Pact?oldid=7023) |
| ✗ | signature | Winter | high_cost | 0/30 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 5 | no card of the faction has it | [big units that finish the game](https://stormboundkingdomwars.fandom.com/wiki/Winter_Pact?oldid=7023) |
| ✗ | signature | Swarm | summon | 6/28 cards (21%), 1.4x the rest, chance 0.263, rank 2 of 5 | not 1.5x the rest of the game | [unit generation](https://stormboundkingdomwars.fandom.com/wiki/Swarm_of_the_East?oldid=4049) |
| ✗ | signature | Swarm | board_presence | 6/28 cards (21%), 1.4x the rest, chance 0.263, rank 2 of 5 | not 1.5x the rest of the game | [many weak units](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✗ | signature | Swarm | buff | 7/28 cards (25%), 1.2x the rest, chance 0.427, rank 2 of 5 | not 1.5x the rest of the game | [strengthening units on the board](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✓ | signature | Swarm | direct_damage | 7/28 cards (25%), 1.3x the rest, chance 0.313, rank 2 of 5 |  | [direct damage to the enemy base](https://stormboundkingdomwars.fandom.com/wiki/Swarm_of_the_East?oldid=4049) |
| ✓ | signature | Swarm | movement | 6/28 cards (21%), 4.3x the rest, chance 0.008, rank 1 of 5 |  | [high movement](https://stormboundkingdomwars.fandom.com/wiki/Swarm_of_the_East?oldid=4049) |
| ✗ | signature | Swarm | tribal | 0/28 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 5 | no card of the faction has it | [Satyrs](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✗ | signature | Swarm | life_payment | 0/28 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 5 | no card of the faction has it | [self-damage costs](https://stormboundkingdomwars.fandom.com/wiki/Swarm_of_the_East?oldid=4049) |
| ✓ | signature | Shadowfen | damage_over_time | 11/28 cards (39%), 1.8x the rest, chance 0.042, rank 1 of 5 |  | [poison](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✗ | signature | Shadowfen | summon | 7/28 cards (25%), 1.8x the rest, chance 0.124, rank 1 of 5 | could be chance (5%) | [Toads](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✗ | signature | Shadowfen | tribal | 0/28 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 5 | no card of the faction has it | [Toads](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✗ | signature | Shadowfen | sacrifice | 0/28 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 5 | no card of the faction has it | [sacrifice-based poison](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✗ | signature | Ironclad | buff | 7/28 cards (25%), 1.2x the rest, chance 0.427, rank 2 of 5 | not 1.5x the rest of the game | [Boosting Elixir](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✓ | signature | Ironclad | forced_movement | 6/28 cards (21%), 4.3x the rest, chance 0.008, rank 1 of 5 |  | [knockback](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✓ | archetype | Winter | control | recipe score 1.03, 2.4x the other factions, 12 cards |  | [control and attrition](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✓ | archetype | Winter | ramp | recipe score 0.66, 5.4x the other factions, 5 cards |  | [extra mana for big units](https://stormboundkingdomwars.fandom.com/wiki/Winter_Pact?oldid=7023) |
| ✓ | archetype | Swarm | aggro_tempo | recipe score 0.03, 4.0x the other factions, 4 cards |  | [aggro](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✓ | archetype | Swarm | swarm | recipe score 0.08, 2.7x the other factions, 6 cards |  | [many weak units](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✗ | archetype | Swarm | tribal | under 1.5x the other factions | recipe not 1.5x the other factions | [Satyrs](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✓ | archetype | Shadowfen | swarm | recipe score 0.12, 5.7x the other factions, 7 cards |  | [flooding the board](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✗ | archetype | Shadowfen | tribal | under 1.5x the other factions | recipe not 1.5x the other factions | [Toads](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✓ | archetype | Shadowfen | poison_attrition | recipe score 3.67, 99.0x the other factions, 10 cards |  | [poison wears down health](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✗ | archetype | Ironclad | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [aggro variant](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✗ | archetype | Ironclad | control | under 1.5x the other factions | recipe not 1.5x the other factions | [control variant](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✓ | combo | Wisp Cloud | Frosthexers | linked by type |  | [freeze, then clear frozen targets](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |

## Slay the Spire

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | signature | Ironclad | permanent_growth | 1/83 cards (1%), 0.7x the rest, chance 0.784, rank 3 of 5 | not 1.5x the rest of the game | [Strength scaling](https://slaythespire.gg/guides/slay-the-spire-best-character) |
| ✗ | signature | Ironclad | exhaust | 26/83 cards (31%), 1.2x the rest, chance 0.200, rank 2 of 5 | not 1.5x the rest of the game | [Exhaust builds](https://slaythespire.gg/guides/slay-the-spire-best-character) |
| ✗ | signature | Ironclad | block_armor | 20/83 cards (24%), 1.2x the rest, chance 0.203, rank 2 of 5 | not 1.5x the rest of the game | [Block with Barricade and Entrench](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✗ | signature | Ironclad | multi_attack | 4/83 cards (5%), 1.6x the rest, chance 0.284, rank 2 of 5 | could be chance (5%) | [multi-attack cards](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | signature | Silent | damage_over_time | 31/83 cards (37%), 1.4x the rest, chance 0.042, rank 1 of 5 |  | [Poison](https://slaythespire.gg/guides/slay-the-spire-best-character) |
| ✗ | signature | Silent | generate_cards | 8/83 cards (10%), 0.9x the rest, chance 0.713, rank 3 of 5 | not 1.5x the rest of the game | [Shivs](https://slaythespire.gg/guides/slay-the-spire-best-character) |
| ✓ | signature | Silent | discard | 10/83 cards (12%), 41.2x the rest, chance 0.000, rank 1 of 5 |  | [discard loops](https://slaythespire.gg/guides/slay-the-spire-best-character) |
| ✓ | signature | Silent | draw | 17/83 cards (20%), 1.7x the rest, chance 0.043, rank 1 of 5 |  | [drawing and discarding](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✗ | signature | Silent | on_ally_play | 4/83 cards (5%), 2.4x the rest, chance 0.148, rank 1 of 5 | could be chance (5%) | [triggers on every card played](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | signature | Defect | slots_queue | 32/89 cards (36%), infx the rest, chance 0.000, rank 1 of 5 |  | [Orbs](https://slaythespire.gg/guides/slay-the-spire-best-character) |
| ✓ | signature | Defect | spell_power | 6/89 cards (7%), 7.6x the rest, chance 0.004, rank 1 of 5 |  | [Focus stacking](https://slaythespire.gg/guides/slay-the-spire-best-character) |
| ✗ | signature | Defect | block_armor | 21/89 cards (24%), 1.2x the rest, chance 0.228, rank 3 of 5 | not 1.5x the rest of the game | [Frost for Block](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | signature | Defect | cost_condition | 2/89 cards (2%), infx the rest, chance 0.043, rank 1 of 5 |  | [zero-cost cards with Claw](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | signature | Watcher | stances | 28/89 cards (31%), infx the rest, chance 0.000, rank 1 of 5 |  | [Calm, Wrath, Divinity](https://slaythespire.gg/guides/slay-the-spire-best-character) |
| ✓ | signature | Watcher | retain | 13/89 cards (15%), 7.0x the rest, chance 0.000, rank 1 of 5 |  | [Retain](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | signature | Watcher | selection | 9/89 cards (10%), 4.2x the rest, chance 0.003, rank 2 of 5 |  | [Scry](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | signature | Watcher | generate_cards | 17/89 cards (19%), 2.2x the rest, chance 0.006, rank 1 of 5 |  | [creating cards](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✗ | signature | Watcher | upgrade | 2/89 cards (2%), 1.5x the rest, chance 0.450, rank 3 of 5 | could be chance (5%) | [upgrading created cards](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | archetype | Ironclad | scaling | recipe score 0.92, 3.0x the other factions, 5 cards |  | [Strength scaling](https://slaythespire.gg/guides/slay-the-spire-best-character) |
| ✗ | archetype | Ironclad | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [Bunker](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | archetype | Silent | poison_attrition | recipe score 3.25, 99.0x the other factions, 9 cards |  | [Poison](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✗ | archetype | Silent | card_advantage | under 1.5x the other factions | recipe not 1.5x the other factions | [Discard and Draw](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✗ | archetype | Silent | spellslinger | under 1.5x the other factions | recipe not 1.5x the other factions | [Momentum, playing many cards](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | archetype | Defect | fortress | recipe score 0.72, 5.9x the other factions, 24 cards |  | [Frost Tank](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✗ | archetype | Defect | scaling | under 1.5x the other factions | recipe not 1.5x the other factions | [Focus stacking, Claw](https://slaythespire.gg/guides/slay-the-spire-best-character) |
| ✓ | archetype | Watcher | transformation | recipe score 1.34, 99.0x the other factions, 28 cards |  | [stance switching](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | archetype | Watcher | card_advantage | recipe score 1.03, 3.3x the other factions, 18 cards |  | [Scry and Creation](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | combo | Body Slam | Barricade | linked by keyword, role |  | [Block becomes damage](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | combo | Body Slam | Entrench | linked by keyword, role |  | [Block becomes damage](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | combo | Demon Form | Sword Boomerang | linked by role |  | [Strength with multi-attack](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | combo | Limit Break | Whirlwind | linked by relation, role_tree |  | [Strength with multi-attack](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | combo | Feel No Pain | Dark Embrace | linked by role |  | [Exhaust value](https://slaythespire.gg/guides/slay-the-spire-best-character) |
| ✓ | combo | After Image | A Thousand Cuts | linked by relation |  | [both trigger on every card](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | combo | Catalyst | Noxious Fumes | linked by keyword, role |  | [Catalyst doubles Poison](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | combo | Catalyst | Bouncing Flask | linked by keyword, role |  | [Catalyst doubles Poison](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✗ | combo | Glacier | Capacitor |  | both cards there, no connection | [Frost and more Orb slots](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✗ | combo | Recursion | Loop |  | both cards there, no connection | [more use of Orbs](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | combo | Loop | Defragment | linked by role |  | [Focus scaling](https://slaythespire.gg/guides/slay-the-spire-best-character) |
| ✗ | combo | All for One | Claw |  | both cards there, no connection | [zero-cost engine](https://slaythespire.gg/guides/slay-the-spire-best-character) |
| ✓ | combo | Establishment | Windmill Strike | linked by relation, role |  | [retained cards get cheaper](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | combo | Establishment | Sands of Time | linked by relation, role |  | [retained cards get cheaper](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | combo | Master Reality | Conjure Blade | linked by role |  | [created cards come upgraded](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | combo | Master Reality | Evaluate | linked by role |  | [created cards come upgraded](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | combo | Talk to the Hand | Flurry of Blows | linked by relation |  | [stance switching](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | combo | Nirvana | Cut Through Fate | linked by keyword, role |  | [Block whenever you Scry](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | combo | Nirvana | Third Eye | linked by keyword, role |  | [Block whenever you Scry](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | combo | Nirvana | Just Lucky | linked by keyword, role |  | [Block whenever you Scry](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | combo | Nirvana | Weave | linked by keyword, role |  | [Block whenever you Scry](https://www.thegamer.com/slay-the-spire-best-builds/) |

## Slay the Spire 2 (Early Access)

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | signature | Ironclad | permanent_growth | 1/103 cards (1%), 0.7x the rest, chance 0.757, rank 3 of 8 | not 1.5x the rest of the game | [Strength scaling](https://slaythespire2.gg/characters) |
| ✗ | signature | Ironclad | life_payment | 0/103 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 8 | no card of the faction has it | [self-damage for power](https://slaythespire2.gg/characters) |
| ✓ | signature | Ironclad | exhaust | 31/103 cards (30%), 2.1x the rest, chance 0.000, rank 1 of 8 |  | [Exhaust payoffs](https://slaythespire2.gg/characters) |
| ✓ | signature | Silent | damage_over_time | 38/106 cards (36%), 1.8x the rest, chance 0.000, rank 2 of 8 |  | [Poison](https://slaythespire2.gg/characters) |
| ✗ | signature | Silent | generate_cards | 12/106 cards (11%), 1.4x the rest, chance 0.163, rank 3 of 8 | not 1.5x the rest of the game | [Shivs](https://slaythespire2.gg/characters) |
| ✓ | signature | Silent | discard | 20/106 cards (19%), 42.4x the rest, chance 0.000, rank 1 of 8 |  | [discard combos](https://slaythespire2.gg/characters) |
| ✗ | signature | Silent | on_discard | 0/106 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 8 | no card of the faction has it | [Sly](https://slaythespire2.gg/characters) |
| ✓ | signature | Defect | slots_queue | 42/112 cards (38%), 111.6x the rest, chance 0.000, rank 1 of 8 |  | [Orbs](https://slaythespire2.gg/characters) |
| ✓ | signature | Defect | spell_power | 8/112 cards (7%), 63.8x the rest, chance 0.000, rank 1 of 8 |  | [Focus](https://keengamer.com/articles/guides/slay-the-spire-2-best-character-tier-list) |
| ✓ | signature | Necrobinder | summon | 12/107 cards (11%), 33.6x the rest, chance 0.000, rank 1 of 8 |  | [Osty scales by Summon](https://slaythespire2.gg/characters) |
| ✗ | signature | Necrobinder | destroy | 0/107 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 8 | no card of the faction has it | [Doom executes at a threshold](https://slaythespire2.gg/characters) |
| ✗ | signature | Necrobinder | draw | 6/107 cards (6%), 0.5x the rest, chance 0.987, rank 8 of 8 | not 1.5x the rest of the game | [Souls, burst card draw](https://slaythespire2.gg/characters) |
| ✗ | signature | Necrobinder | transform | 1/107 cards (1%), 0.6x the rest, chance 0.837, rank 5 of 8 | not 1.5x the rest of the game | [card transform](https://slaythespire2.gg/characters) |
| ✓ | signature | Regent | coin_economy | 19/106 cards (18%), 80.6x the rest, chance 0.000, rank 1 of 8 |  | [Stars, a second resource](https://slaythespire2.gg/characters) |
| ✗ | signature | Regent | permanent_growth | 0/106 cards (0%), 0.0x the rest, chance 1.000, rank 6 of 8 | no card of the faction has it | [Forge scales the Sovereign Blade](https://slaythespire2.gg/characters) |
| ✗ | signature | Regent | summon | 0/106 cards (0%), 0.0x the rest, chance 1.000, rank 4 of 8 | no card of the faction has it | [Minions](https://slaythespire2.gg/characters) |
| ✗ | archetype | Ironclad | scaling | under 1.5x the other factions | recipe not 1.5x the other factions | [Strength stacking](https://brokenbuilds.gg/slay-the-spire-2/guides/slay-the-spire-2-best-builds) |
| ✓ | archetype | Silent | poison_attrition | recipe score 3.55, 99.0x the other factions, 14 cards |  | [Poison attrition](https://slaythespire2.gg/characters) |
| ✗ | archetype | Silent | card_advantage | under 1.5x the other factions | recipe not 1.5x the other factions | [discard cycling](https://keengamer.com/articles/guides/slay-the-spire-2-best-character-tier-list) |
| ✗ | archetype | Defect | scaling | under 1.5x the other factions | recipe not 1.5x the other factions | [Orb scaling engines](https://slaythespire2.gg/characters) |
| ✗ | archetype | Defect | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [Frost Tank](https://brokenbuilds.gg/slay-the-spire-2/guides/slay-the-spire-2-best-builds) |
| ✗ | archetype | Regent | scaling | under 1.5x the other factions | recipe not 1.5x the other factions | [long-term scaling](https://slaythespire2.gg/characters) |
| ✗ | combo | Star Battery | Sovereign Blade |  | a card name is not in the library | [climbing damage](https://brokenbuilds.gg/slay-the-spire-2/guides/slay-the-spire-2-best-builds) |
| ✗ | combo | Parry | Sword Sage |  | both cards there, no connection | [early Block loop](https://brokenbuilds.gg/slay-the-spire-2/guides/slay-the-spire-2-best-builds) |

## Star Wars: Unlimited

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Vigilance | heal | 83/418 cards (20%), 4.7x the rest, chance 0.000, rank 1 of 7 |  | [Restore, healing units and bases](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Vigilance | taunt | 64/418 cards (15%), 3.5x the rest, chance 0.000, rank 1 of 7 |  | [Sentinel](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Vigilance | removal | 70/418 cards (17%), 1.3x the rest, chance 0.032, rank 2 of 7 |  | [removing threats](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✗ | signature | Vigilance | tank | 0/418 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 7 | no card of the faction has it | [guard-type units with strong HP](https://cardgamer.com/games/star-wars/aspects-in-star-wars-unlimited/) |
| ✓ | signature | Command | resource_gain | 15/430 cards (3%), 9.6x the rest, chance 0.000, rank 1 of 7 |  | [proactive resource acceleration](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Command | board_presence | 53/430 cards (12%), 2.2x the rest, chance 0.000, rank 1 of 7 |  | [the most units](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Command | summon | 53/430 cards (12%), 2.2x the rest, chance 0.000, rank 1 of 7 |  | [unit tokens](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Command | stat_gain | 171/430 cards (40%), 1.3x the rest, chance 0.000, rank 2 of 7 |  | [Experience tokens](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✗ | signature | Command | high_cost | 0/430 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 7 | no card of the faction has it | [the largest, most expensive units](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Aggression | direct_damage | 151/421 cards (36%), 1.6x the rest, chance 0.000, rank 1 of 7 |  | [direct damage to bases](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Aggression | damage | 235/421 cards (56%), 2.1x the rest, chance 0.000, rank 1 of 7 |  | [direct damage to units](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Aggression | excess_damage | 141/421 cards (33%), 1.1x the rest, chance 0.235, rank 5 of 7 |  | [Overwhelm](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Aggression | evasion | 61/421 cards (14%), 1.2x the rest, chance 0.077, rank 2 of 7 |  | [Saboteur gets past Sentinel](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Aggression | draw | 38/421 cards (9%), 1.8x the rest, chance 0.003, rank 1 of 7 |  | [card draw](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Aggression | untap | 35/421 cards (8%), 3.0x the rest, chance 0.000, rank 1 of 7 |  | [readying units](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✗ | signature | Cunning | on_play | 173/445 cards (39%), 1.3x the rest, chance 0.002, rank 1 of 7 | not 1.5x the rest of the game | [the most When Played abilities](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Cunning | stealth | 59/445 cards (13%), 1.8x the rest, chance 0.000, rank 2 of 7 |  | [Hidden](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Cunning | disable | 69/445 cards (16%), 15.2x the rest, chance 0.000, rank 1 of 7 |  | [exhausting units](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Cunning | hand_disruption | 16/445 cards (4%), 3.1x the rest, chance 0.001, rank 1 of 7 |  | [hand disruption](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Cunning | temporary_effect | 60/445 cards (13%), 1.2x the rest, chance 0.082, rank 3 of 7 |  | [temporary board advantage](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✗ | archetype | Vigilance | control | under 1.5x the other factions | recipe not 1.5x the other factions | [a control aspect, long game](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | archetype | Vigilance | fortress | recipe score 0.68, 1.9x the other factions, 133 cards |  | [survivability and defence](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | archetype | Command | ramp | recipe score 0.47, 3.2x the other factions, 68 cards |  | [growth and ramping](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | archetype | Aggression | aggro_tempo | recipe score 0.42, 4.3x the other factions, 199 cards |  | [assertive pressure](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | archetype | Aggression | burn | recipe score 2.05, 17.6x the other factions, 166 cards |  | [direct damage to bases](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✗ | archetype | Cunning | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [tempo](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | archetype | Cunning | trickery | recipe score 0.33, 2.5x the other factions, 59 cards |  | [tricks, surprise attacks](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | archetype | Cunning | disruption | recipe score 0.70, 1.8x the other factions, 36 cards |  | [hand disruption, exhausting resources](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | splash | Vigilance | draw |  |  | [once-per-round card draw](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | splash | Vigilance | disable |  |  | [exhausting units](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✗ | splash | Vigilance | shield |  | missing from the splash list | [Shield tokens](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✗ | combo | Tarkintown | Cad Bane - He Who Needs No Introduction |  | both cards there, no connection | [ping, then finish damaged units](https://tcg-hq.beehiiv.com/p/cad-bane-tarkin-town-master-class) |
| ✗ | combo | Crafty Smugglers | Ma Klounkee |  | a card name is not in the library | [return to hand and deal damage](https://tcg-hq.beehiiv.com/p/cad-bane-tarkin-town-master-class) |
| ✗ | combo | Now There Are Two of Them | Zuckuss - Bounty Hunter for Hire |  | both cards there, no connection | [cheaper deployment](https://tcg-hq.beehiiv.com/p/cad-bane-tarkin-town-master-class) |
| ✓ | combo | Now There Are Two of Them | Bossk - Deadly Stalker | linked by relation |  | [cheaper deployment](https://tcg-hq.beehiiv.com/p/cad-bane-tarkin-town-master-class) |
| ✓ | combo | Jabba the Hutt - Cunning Daimyo | Shoot First | linked by type |  | [cost reduction makes it free](https://tcg-hq.beehiiv.com/p/cad-bane-tarkin-town-master-class) |
| ✓ | combo | Jabba the Hutt - Cunning Daimyo | Ma Klounkee | linked by engine, relation, type |  | [cost reduction makes it free](https://tcg-hq.beehiiv.com/p/cad-bane-tarkin-town-master-class) |
| ✓ | combo | Ma Klounkee | Bossk - Deadly Stalker | linked by engine, relation, type |  | [Bossk deals 2 on an event](https://tcg-hq.beehiiv.com/p/cad-bane-tarkin-town-master-class) |

## The Elder Scrolls: Legends

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | signature | Strength | removal | 18/153 cards (12%), 0.8x the rest, chance 0.809, rank 5 of 6 | not 1.5x the rest of the game | [removes enemies head-on](https://en.uesp.net/wiki/Legends:Attributes) |
| ✓ | signature | Intelligence | random_effect | 29/165 cards (18%), 1.6x the rest, chance 0.014, rank 2 of 6 |  | [spells with random outcomes](https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes) |
| ✗ | signature | Intelligence | generate_cards | 13/165 cards (8%), 1.7x the rest, chance 0.077, rank 1 of 6 | could be chance (5%) | [conjured Atronachs](https://en.uesp.net/wiki/Legends:Attributes) |
| ✓ | signature | Intelligence | merge_attach | 20/165 cards (12%), 1.9x the rest, chance 0.011, rank 2 of 6 |  | [weapons](https://en.uesp.net/wiki/Legends:Attributes) |
| ✓ | signature | Willpower | board_presence | 24/158 cards (15%), 1.5x the rest, chance 0.043, rank 1 of 6 |  | [going wide](https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes) |
| ✓ | signature | Willpower | buff | 61/158 cards (39%), 1.0x the rest, chance 0.478, rank 3 of 6 |  | [boosting forces with magic](https://en.uesp.net/wiki/Legends:Attributes) |
| ✓ | signature | Willpower | steal | 7/158 cards (4%), 15.3x the rest, chance 0.000, rank 1 of 6 |  | [bending enemies to your will](https://en.uesp.net/wiki/Legends:Attributes) |
| ✓ | signature | Willpower | destroy | 15/158 cards (9%), 1.9x the rest, chance 0.025, rank 2 of 6 |  | [destroying enemy creatures](https://en.uesp.net/wiki/Legends:Attributes) |
| ✓ | signature | Agility | deathtouch | 16/155 cards (10%), 1.6x the rest, chance 0.070, rank 1 of 6 |  | [Lethal](https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes) |
| ✓ | signature | Agility | movement | 11/155 cards (7%), 16.4x the rest, chance 0.000, rank 1 of 6 |  | [moving creatures between lanes](https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes) |
| ✗ | signature | Agility | on_attack | 9/155 cards (6%), 1.6x the rest, chance 0.149, rank 2 of 6 | could be chance (5%) | [Pilfer](https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes) |
| ✓ | signature | Endurance | taunt | 23/162 cards (14%), 1.6x the rest, chance 0.042, rank 2 of 6 |  | [Guard](https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes) |
| ✗ | signature | Endurance | resource_gain | 4/162 cards (2%), 2.1x the rest, chance 0.180, rank 2 of 6 | could be chance (5%) | [more magicka](https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes) |
| ✓ | signature | Endurance | heal | 31/162 cards (19%), 2.4x the rest, chance 0.000, rank 1 of 6 |  | [heals for player and creature](https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes) |
| ✗ | signature | Endurance | high_cost | 0/162 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 6 | no card of the faction has it | [high-cost, high-power creatures](https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes) |
| ✓ | archetype | Strength | aggro_tempo | recipe score 0.76, 2.4x the other factions, 41 cards |  | [head-on attacks, pure power](https://en.uesp.net/wiki/Legends:Attributes) |
| ✓ | archetype | Intelligence | chaos | recipe score 1.02, 8.2x the other factions, 36 cards |  | [random, unpredictable spells](https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes) |
| ✗ | archetype | Intelligence | spellslinger | under 1.5x the other factions | recipe not 1.5x the other factions | [trickery and magic, spells](https://en.uesp.net/wiki/Legends:Attributes) |
| ✓ | archetype | Willpower | swarm | recipe score 0.37, 6.8x the other factions, 36 cards |  | [going wide](https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes) |
| ✗ | archetype | Willpower | control | under 1.5x the other factions | recipe not 1.5x the other factions | [greatest ability to deal with threats](https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes) |
| ✓ | archetype | Agility | positional | recipe score 0.57, 41.5x the other factions, 43 cards |  | [lane movement](https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes) |
| ✗ | archetype | Endurance | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [strong guards](https://en.uesp.net/wiki/Legends:Attributes) |
| ✗ | archetype | Endurance | ramp | under 1.5x the other factions | recipe not 1.5x the other factions | [more magicka, high-cost creatures](https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes) |
| ✓ | archetype | Endurance | sustain | recipe score 1.26, 9.5x the other factions, 31 cards |  | [healing actions](https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes) |
| ✗ | combo | Snowy Sabre Cat | Swift Strike |  | both cards there, no connection | [one-turn attack](https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight) |
| ✗ | combo | Snowy Sabre Cat | Crusader's Assault |  | both cards there, no connection | [one-turn attack](https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight) |
| ✗ | combo | Snowy Sabre Cat | Monk's Strike |  | both cards there, no connection | [one-turn attack](https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight) |
| ✗ | combo | Doomcrag Vampire | Nord Firebrand |  | both cards there, no connection | [pings take down big creatures](https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight) |
| ✗ | combo | Doomcrag Vampire | Sharpshooter Scout |  | both cards there, no connection | [pings take down big creatures](https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight) |
| ✗ | combo | Disciple of Namira | Namira's Shrine |  | both cards there, no connection | [draw lots of cards](https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight) |
| ✓ | combo | Paarthurnax | Soultear | linked by engine, keyword, relation |  | [reuse for value](https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight) |
| ✓ | combo | Blood Magic Lord | Soultear | linked by relation |  | [reuse for value](https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight) |
| ✓ | combo | Odirniran Necromancer | Soultear | linked by engine, relation |  | [more power](https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight) |
| ✓ | combo | Odirniran Necromancer | Galyn The Shelterer | linked by engine, keyword, relation, type |  | [more power and targets](https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight) |
| ✗ | combo | Ulfric's Uprising | Nix-Ox |  | a card name is not in the library | [re-triggers Nix-Ox for magicka](https://bethesda.net/en-US/news/top-highlights-of-the-month-november-2018) |
| ✗ | combo | Therana | Ulfric's Uprising |  | a card name is not in the library | [extra copies of Uprising](https://bethesda.net/en-US/news/top-highlights-of-the-month-november-2018) |
| ✓ | combo | Ring of Namira | The Night Mother | linked by relation |  | [life gain becomes damage](https://bethesda.net/en-US/news/top-highlights-of-the-month-november-2018) |
| ✗ | combo | Devour | Territorial Viper |  | both cards there, no connection | [Lethal and Charge](https://bethesda.net/en-US/news/top-highlights-of-the-month-november-2018) |
| ✗ | combo | Wildfire Dragon | Brotherhood Sanctuary |  | a card name is not in the library | [repeats the boost](https://bethesda.net/en-US/news/top-highlights-of-the-month-november-2018) |
| ✓ | combo | Dremora Markynaz | Dagoth Ur | linked by keyword, relation |  | [grows Dagoth Ur](https://bethesda.net/en-US/news/top-highlights-of-the-month-november-2018) |

## Warhammer 40,000 (10th edition)

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | signature | Imperium - Adeptus Astartes - Space Marines | mark_target | 3/471 cards (1%), 3.0x the rest, chance 0.119, rank 6 of 26 | could be chance (5%) | [Oath of Moment](https://wahapedia.ru/wh40k10ed/factions/space-marines/) |
| ✗ | signature | Imperium - Adeptus Astartes - Space Marines | flexibility | 22/471 cards (5%), 0.5x the rest, chance 1.000, rank 17 of 26 | not 1.5x the rest of the game | [flexible, many units](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | signature | Imperium - Adeptus Astartes - Black Templars | modal_choice | 2/20 cards (10%), 1.4x the rest, chance 0.426, rank 8 of 26 | not 1.5x the rest of the game | [four Templar Vows](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | signature | Imperium - Adeptus Astartes - Space Wolves | quests | 3/47 cards (6%), 0.8x the rest, chance 0.753, rank 15 of 26 | not 1.5x the rest of the game | [Sagas completed for power](https://www.wargamer.com/warhammer-40k/factions) |
| ✓ | signature | Imperium - Grey Knights | reserve_bench | 38/115 cards (33%), 2.3x the rest, chance 0.000, rank 3 of 26 |  | [Gate of Infinity to Strategic Reserves](https://wahapedia.ru/wh40k10ed/factions/grey-knights/) |
| ✓ | signature | Imperium - Adepta Sororitas | resource_banking | 40/121 cards (33%), 22.8x the rest, chance 0.000, rank 1 of 26 |  | [Miracle dice stored for later](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | signature | Imperium - Adepta Sororitas | other_death_trigger | 1/121 cards (1%), 3.0x the rest, chance 0.302, rank 2 of 26 | could be chance (5%) | [Miracle die when a friendly unit dies](https://wahapedia.ru/wh40k10ed/factions/adepta-sororitas/) |
| ✓ | signature | Imperium - Adeptus Custodes | stances | 29/109 cards (27%), 4.4x the rest, chance 0.000, rank 1 of 26 |  | [Martial Ka'tah stances](https://wahapedia.ru/wh40k10ed/factions/adeptus-custodes/) |
| ✗ | signature | Imperium - Adeptus Custodes | tank | 0/109 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 26 | no card of the faction has it | [tough, top defensive wargear](https://www.wargamer.com/warhammer-40k/factions) |
| ✓ | signature | Imperium - Adeptus Mechanicus | modal_choice | 43/107 cards (40%), 6.5x the rest, chance 0.000, rank 1 of 26 |  | [Doctrina Imperatives each round](https://wahapedia.ru/wh40k10ed/factions/adeptus-mechanicus/) |
| ✓ | signature | Imperium - Adeptus Mechanicus | buff | 79/107 cards (74%), 1.1x the rest, chance 0.058, rank 6 of 26 |  | [stackable buffs](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | signature | Chaos - Chaos Space Marines | life_payment | 1/202 cards (0%), infx the rest, chance 0.054, rank 1 of 26 | could be chance (5%) | [Dark Pacts cost mortal wounds on a fail](https://wahapedia.ru/wh40k10ed/factions/chaos-space-marines/) |
| ✗ | signature | Chaos - Death Guard | debuff | 23/123 cards (19%), 1.3x the rest, chance 0.117, rank 7 of 26 | not 1.5x the rest of the game | [plague aura weakens enemies](https://www.wargamer.com/warhammer-40k/factions) |
| ✓ | signature | Chaos - Death Guard | aura | 49/123 cards (40%), 4.3x the rest, chance 0.000, rank 1 of 26 |  | [Nurgle's Gift aura](https://wahapedia.ru/wh40k10ed/factions/death-guard/) |
| ✗ | signature | Chaos - Emperor's Children | attack_now | 0/92 cards (0%), 0.0x the rest, chance 1.000, rank 12 of 26 | no card of the faction has it | [shoot and charge after Advancing](https://wahapedia.ru/wh40k10ed/factions/emperor-s-children/) |
| ✗ | signature | Aeldari | movement | 84/329 cards (26%), 1.3x the rest, chance 0.010, rank 5 of 26 | not 1.5x the rest of the game | [Battle Focus extra movement](https://wahapedia.ru/wh40k10ed/factions/aeldari/) |
| ✓ | signature | Aeldari | resource_banking | 51/329 cards (16%), 12.7x the rest, chance 0.000, rank 2 of 26 |  | [Strands of Fate dice replace rolls](https://wahapedia.ru/wh40k10ed/factions/aeldari/) |
| ✗ | signature | Xenos - Necrons | regeneration | 3/144 cards (2%), 0.6x the rest, chance 0.857, rank 21 of 26 | not 1.5x the rest of the game | [reanimate wounds each Command phase](https://wahapedia.ru/wh40k10ed/factions/necrons/) |
| ✓ | signature | Xenos - Necrons | revive | 6/144 cards (4%), 3.4x the rest, chance 0.011, rank 1 of 26 |  | [returning destroyed models](https://wahapedia.ru/wh40k10ed/factions/necrons/) |
| ✗ | signature | Xenos - Orks | temporary_buff | 69/191 cards (36%), 1.1x the rest, chance 0.169, rank 5 of 26 | not 1.5x the rest of the game | [Waaagh! for one round](https://wahapedia.ru/wh40k10ed/factions/orks/) |
| ✗ | signature | Xenos - Orks | once_per_game | 25/191 cards (13%), 1.3x the rest, chance 0.107, rank 4 of 26 | not 1.5x the rest of the game | [Waaagh! once per battle](https://wahapedia.ru/wh40k10ed/factions/orks/) |
| ✗ | signature | Xenos - Orks | board_presence | 3/191 cards (2%), 1.1x the rest, chance 0.520, rank 10 of 26 | not 1.5x the rest of the game | [green tide, strong in numbers](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | signature | Xenos - T'au Empire | mark_target | 0/164 cards (0%), 0.0x the rest, chance 1.000, rank 9 of 26 | no card of the faction has it | [Spotted targets](https://wahapedia.ru/wh40k10ed/factions/t-au-empire/) |
| ✗ | signature | Xenos - T'au Empire | ranged | 53/164 cards (32%), 1.0x the rest, chance 0.618, rank 13 of 26 | not 1.5x the rest of the game | [superior weapons](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | signature | Xenos - Tyranids | aura | 19/175 cards (11%), 1.1x the rest, chance 0.422, rank 10 of 26 | not 1.5x the rest of the game | [Synapse range bonuses](https://wahapedia.ru/wh40k10ed/factions/tyranids/) |
| ✗ | signature | Xenos - Tyranids | stress_morale | 24/175 cards (14%), 1.0x the rest, chance 0.503, rank 11 of 26 | not 1.5x the rest of the game | [Shadow in the Warp Battle-shock](https://wahapedia.ru/wh40k10ed/factions/tyranids/) |
| ✗ | signature | Xenos - Genestealer Cults | revive | 2/73 cards (3%), 2.1x the rest, chance 0.252, rank 3 of 26 | could be chance (5%) | [destroyed units come back](https://wahapedia.ru/wh40k10ed/factions/genestealer-cults/) |
| ✗ | signature | Xenos - Leagues of Votann | zone_control | 9/105 cards (9%), 1.0x the rest, chance 0.554, rank 9 of 26 | not 1.5x the rest of the game | [bonuses near and on objectives](https://wahapedia.ru/wh40k10ed/factions/leagues-of-votann/) |
| ✓ | archetype | Imperium - Adeptus Astartes - Black Templars | aggro_tempo | recipe score 1.53, 2.7x the other factions, 10 cards |  | [ultra-aggressive melee](https://www.wargamer.com/warhammer-40k/factions) |
| ✓ | archetype | Imperium - Adeptus Astartes - Blood Angels | aggro_tempo | recipe score 1.14, 1.9x the other factions, 6 cards |  | [jump pack assaults](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | archetype | Imperium - Adeptus Custodes | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [tough, defensive wargear](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | archetype | Chaos - Death Guard | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [slow and hardy](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | archetype | Chaos - Thousand Sons | spellslinger | under 1.5x the other factions | recipe not 1.5x the other factions | [psychic and sorcerous](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | archetype | Chaos - World Eaters | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [fast, ultra-violent melee](https://www.wargamer.com/warhammer-40k/factions) |
| ✓ | archetype | Chaos - Emperor's Children | aggro_tempo | recipe score 1.02, 1.7x the other factions, 27 cards |  | [fast aggressive melee](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | archetype | Xenos - Necrons | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [slow but resilient](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | archetype | Xenos - Orks | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [green tide](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | archetype | Xenos - T'au Empire | positional | under 1.5x the other factions | recipe not 1.5x the other factions | [dynamic and manoeuvrable](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | archetype | Xenos - Tyranids | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [huge swarms](https://www.wargamer.com/warhammer-40k/factions) |
| ✓ | archetype | Xenos - Genestealer Cults | swarm | recipe score 0.17, 1.5x the other factions, 2 cards |  | [relentless horde](https://www.wargamer.com/warhammer-40k/factions) |
| ✓ | combo | Judiciar | Bladeguard Veteran Squad | linked by keyword, link, role_tree |  | [decent in melee with a Judiciar](https://www.tabletopbattles.com/10th-edition-competitive-faction-focus-space-marines) |
| ✗ | combo | Impulsor | Sternguard Veteran Squad |  | both cards there, no connection | [Firing Deck](https://www.tabletopbattles.com/10th-edition-competitive-faction-focus-space-marines) |
| ✓ | combo | Impulsor | Hellblaster Squad | linked by engine, keyword, relation |  | [Firing Deck](https://www.tabletopbattles.com/10th-edition-competitive-faction-focus-space-marines) |
| ✗ | combo | Storm Speeder Thunderstrike | Eradicator Squad |  | both cards there, no connection | [+1 to wound on vehicles and monsters](https://www.tabletopbattles.com/10th-edition-competitive-faction-focus-space-marines) |
| ✓ | combo | Incursor Squad | Whirlwind | linked by relation |  | [+1 to hit helps indirect fire](https://www.tabletopbattles.com/10th-edition-competitive-faction-focus-space-marines) |
| ✗ | combo | Drop Pod | Devastator Squad |  | both cards there, no connection | [delivers them into shooting position](https://www.tabletopbattles.com/10th-edition-competitive-faction-focus-space-marines) |
| ✓ | combo | Captain | Company Heroes | linked by keyword, link, role, role_tree |  | [they need a Captain](https://www.tabletopbattles.com/10th-edition-competitive-faction-focus-space-marines) |
| ✓ | combo | Ghazghkull Thraka | Meganobz | linked by link |  | [Ghaz leads Meganobz](https://www.belloflostsouls.net/2024/08/warhammer-40k-top-5-must-have-units-for-10ths-hot-armies.html) |

## Warhammer Age of Sigmar (4th edition)

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | signature | Stormcast Eternals | reserve_bench | 2/160 cards (1%), 0.5x the rest, chance 0.924, rank 20 of 33 | not 1.5x the rest of the game | [Celestial Realm reserve](https://wahapedia.ru/aos4/factions/stormcast-eternals/) |
| ✗ | signature | Stormcast Eternals | revive | 5/160 cards (3%), 0.7x the rest, chance 0.831, rank 17 of 33 | not 1.5x the rest of the game | [Heavens-Sent replaces a destroyed unit](https://wahapedia.ru/aos4/factions/stormcast-eternals/) |
| ✗ | signature | Cities of Sigmar | assists_support | 1/183 cards (1%), 1.4x the rest, chance 0.525, rank 10 of 33 | not 1.5x the rest of the game | [orders boost nearby units](https://wahapedia.ru/aos4/factions/cities-of-sigmar/) |
| ✓ | signature | Kharadron Overlords | ranged | 39/118 cards (33%), 2.6x the rest, chance 0.000, rank 1 of 33 |  | [shooting from gunboats](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | signature | Kharadron Overlords | reserve_bench | 4/118 cards (3%), 1.3x the rest, chance 0.360, rank 10 of 33 | not 1.5x the rest of the game | [units wait in the clouds](https://wahapedia.ru/aos4/factions/kharadron-overlords/) |
| ✓ | signature | Sylvaneth | terrain | 25/103 cards (24%), 4.2x the rest, chance 0.000, rank 1 of 33 |  | [overgrowth and Wyldwoods](https://wahapedia.ru/aos4/factions/sylvaneth/) |
| ✗ | signature | Sylvaneth | revive | 5/103 cards (5%), 1.1x the rest, chance 0.462, rank 11 of 33 | not 1.5x the rest of the game | [slain Dryads return](https://wahapedia.ru/aos4/factions/sylvaneth/) |
| ✓ | signature | Sylvaneth | regeneration | 9/103 cards (9%), 1.7x the rest, chance 0.097, rank 4 of 33 |  | [units in the overgrowth heal](https://wahapedia.ru/aos4/factions/sylvaneth/) |
| ✗ | signature | Sylvaneth | reserve_bench | 3/103 cards (3%), 1.1x the rest, chance 0.498, rank 11 of 33 | not 1.5x the rest of the game | [half the army in reserve](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | signature | Sylvaneth | cost_increase | 0/103 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 33 | no card of the faction has it | [enemies pay an extra command point](https://wahapedia.ru/aos4/factions/sylvaneth/) |
| ✗ | signature | Daughters of Khaine | buff | 47/95 cards (49%), 1.1x the rest, chance 0.350, rank 17 of 33 | not 1.5x the rest of the game | [blessings buff units](https://wahapedia.ru/aos4/factions/daughters-of-khaine/) |
| ✗ | signature | Fyreslayers | first_strike | 3/56 cards (5%), 1.6x the rest, chance 0.291, rank 8 of 33 | could be chance (5%) | [Rune of Fury](https://wahapedia.ru/aos4/factions/fyreslayers/) |
| ✓ | signature | Idoneth Deepkin | first_strike | 7/88 cards (8%), 2.5x the rest, chance 0.027, rank 2 of 33 |  | [Sea's Embrace Strike-First](https://wahapedia.ru/aos4/factions/idoneth-deepkin/) |
| ✗ | signature | Idoneth Deepkin | turn_number | 1/88 cards (1%), 2.5x the rest, chance 0.349, rank 7 of 33 | could be chance (5%) | [the tide changes by round](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | signature | Seraphon | summon | 2/67 cards (3%), 0.4x the rest, chance 0.966, rank 20 of 33 | not 1.5x the rest of the game | [conjuration](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | signature | Seraphon | modal_choice | 1/67 cards (1%), 0.4x the rest, chance 0.925, rank 26 of 33 | not 1.5x the rest of the game | [the Great Plan Asterisms](https://wahapedia.ru/aos4/factions/seraphon/) |
| ✗ | signature | Slaves to Darkness | modal_choice | 7/151 cards (5%), 1.2x the rest, chance 0.339, rank 14 of 33 | not 1.5x the rest of the game | [pledge a unit to a god](https://wahapedia.ru/aos4/factions/slaves-to-darkness/) |
| ✗ | signature | Slaves to Darkness | transform | 0/151 cards (0%), 0.0x the rest, chance 1.000, rank 4 of 33 | no card of the faction has it | [become a Daemon Prince](https://wahapedia.ru/aos4/factions/slaves-to-darkness/) |
| ✓ | signature | Slaves to Darkness | quests | 14/151 cards (9%), 2.8x the rest, chance 0.001, rank 3 of 33 |  | [Dark Apotheosis points](https://wahapedia.ru/aos4/factions/slaves-to-darkness/) |
| ✗ | signature | Blades of Khorne | death_count | 6/111 cards (5%), 1.6x the rest, chance 0.197, rank 7 of 33 | could be chance (5%) | [a tithe point whenever a unit dies](https://wahapedia.ru/aos4/factions/blades-of-khorne/) |
| ✗ | signature | Blades of Khorne | coin_economy | 0/111 cards (0%), 0.0x the rest, chance 1.000, rank 21 of 33 | no card of the faction has it | [tithe points spent on abilities](https://wahapedia.ru/aos4/factions/blades-of-khorne/) |
| ✓ | signature | Disciples of Tzeentch | reserve_bench | 9/105 cards (9%), 3.6x the rest, chance 0.001, rank 2 of 33 |  | [illusions send units to reserve](https://wahapedia.ru/aos4/factions/disciples-of-tzeentch/) |
| ✗ | signature | Disciples of Tzeentch | swap | 18/105 cards (17%), 1.1x the rest, chance 0.344, rank 12 of 33 | not 1.5x the rest of the game | [Smoke and Mirrors swaps units](https://wahapedia.ru/aos4/factions/disciples-of-tzeentch/) |
| ✗ | signature | Disciples of Tzeentch | coin_economy | 3/105 cards (3%), 3.3x the rest, chance 0.073, rank 2 of 33 | could be chance (5%) | [fate points spent](https://wahapedia.ru/aos4/factions/disciples-of-tzeentch/) |
| ✗ | signature | Disciples of Tzeentch | comeback | 1/105 cards (1%), 8.2x the rest, chance 0.140, rank 3 of 33 | could be chance (5%) | [fate points from setbacks](https://wahapedia.ru/aos4/factions/disciples-of-tzeentch/) |
| ✗ | signature | Skaven | reserve_bench | 3/125 cards (2%), 0.9x the rest, chance 0.631, rank 14 of 33 | not 1.5x the rest of the game | [tunnels and Gnawholes](https://wahapedia.ru/aos4/factions/skaven/) |
| ✗ | signature | Skaven | board_presence | 8/125 cards (6%), 0.9x the rest, chance 0.727, rank 12 of 33 | not 1.5x the rest of the game | [horde](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✓ | signature | Skaven | damage_over_time | 29/125 cards (23%), 1.8x the rest, chance 0.002, rank 2 of 33 |  | [poison and plague attacks](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | signature | Beasts of Chaos | reserve_bench | 3/40 cards (8%), 3.0x the rest, chance 0.082, rank 4 of 33 | could be chance (5%) | [ambush reserve](https://wahapedia.ru/aos4/factions/beasts-of-chaos/) |
| ✓ | signature | Maggotkin of Nurgle | damage_over_time | 16/97 cards (16%), 1.2x the rest, chance 0.227, rank 8 of 33 |  | [disease deals mortal damage each turn](https://wahapedia.ru/aos4/factions/maggotkin-of-nurgle/) |
| ✗ | signature | Helsmiths of Hashut | coin_economy | 1/78 cards (1%), 1.4x the rest, chance 0.522, rank 12 of 33 | not 1.5x the rest of the game | [daemonic power points](https://wahapedia.ru/aos4/factions/helsmiths-of-hashut/) |
| ✗ | signature | Nighthaunt | evasion | 1/91 cards (1%), 0.9x the rest, chance 0.676, rank 15 of 33 | not 1.5x the rest of the game | [spectral, flying](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | signature | Nighthaunt | movement | 19/91 cards (21%), 1.4x the rest, chance 0.095, rank 6 of 33 | not 1.5x the rest of the game | [redeploy a unit once a turn](https://wahapedia.ru/aos4/factions/nighthaunt/) |
| ✗ | signature | Flesh-eater Courts | summon | 11/104 cards (11%), 1.4x the rest, chance 0.149, rank 5 of 33 | not 1.5x the rest of the game | [summon units](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✓ | signature | Flesh-eater Courts | revive | 11/104 cards (11%), 2.6x the rest, chance 0.005, rank 3 of 33 |  | [replace destroyed units, return slain models](https://wahapedia.ru/aos4/factions/flesh-eater-courts/) |
| ✗ | signature | Flesh-eater Courts | heal | 6/104 cards (6%), 0.9x the rest, chance 0.627, rank 17 of 33 | not 1.5x the rest of the game | [heroes heal](https://wahapedia.ru/aos4/factions/flesh-eater-courts/) |
| ✗ | signature | Soulblight Gravelords | reserve_bench | 5/125 cards (4%), 1.6x the rest, chance 0.217, rank 7 of 33 | could be chance (5%) | [rising from the grave](https://wahapedia.ru/aos4/factions/soulblight-gravelords/) |
| ✓ | signature | Soulblight Gravelords | revive | 14/125 cards (11%), 2.8x the rest, chance 0.001, rank 2 of 33 |  | [destroyed units replaced at half size](https://wahapedia.ru/aos4/factions/soulblight-gravelords/) |
| ✗ | signature | Soulblight Gravelords | lifesteal | 26/125 cards (21%), 1.2x the rest, chance 0.204, rank 9 of 33 | not 1.5x the rest of the game | [vampires heal after fighting](https://wahapedia.ru/aos4/factions/soulblight-gravelords/) |
| ✗ | signature | Ossiarch Bonereapers | coin_economy | 0/95 cards (0%), 0.0x the rest, chance 1.000, rank 21 of 33 | no card of the faction has it | [discipline points replace command points](https://wahapedia.ru/aos4/factions/ossiarch-bonereapers/) |
| ✗ | signature | Ironjawz | temporary_buff | 26/83 cards (31%), 0.9x the rest, chance 0.781, rank 17 of 33 | not 1.5x the rest of the game | [Waaagh! for the turn](https://wahapedia.ru/aos4/factions/ironjawz/) |
| ✗ | signature | Kruleboyz | counterattack | 1/75 cards (1%), 0.6x the rest, chance 0.823, rank 20 of 33 | not 1.5x the rest of the game | [mortal damage on units that charged them](https://wahapedia.ru/aos4/factions/kruleboyz/) |
| ✗ | signature | Bonesplitterz | once_per_game | 4/26 cards (15%), 1.2x the rest, chance 0.455, rank 13 of 33 | not 1.5x the rest of the game | [Waaagh! once per battle](https://wahapedia.ru/aos4/factions/bonesplitterz/) |
| ✗ | signature | Gloomspite Gitz | turn_number | 0/111 cards (0%), 0.0x the rest, chance 1.000, rank 10 of 33 | no card of the faction has it | [the Bad Moon changes each round](https://wahapedia.ru/aos4/factions/gloomspite-gitz/) |
| ✓ | signature | Ogor Mawtribes | forced_movement | 4/104 cards (4%), 8.3x the rest, chance 0.002, rank 1 of 33 |  | [Bull Charge pushes an enemy](https://wahapedia.ru/aos4/factions/ogor-mawtribes/) |
| ✗ | signature | Ogor Mawtribes | heal | 8/104 cards (8%), 1.3x the rest, chance 0.309, rank 10 of 33 | not 1.5x the rest of the game | [healing](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | signature | Sons of Behemat | reserve_bench | 3/80 cards (4%), 1.5x the rest, chance 0.339, rank 9 of 33 | not 1.5x the rest of the game | [leave for reserve and return](https://wahapedia.ru/aos4/factions/sons-of-behemat/) |
| ✗ | archetype | Sylvaneth | positional | under 1.5x the other factions | recipe not 1.5x the other factions | [mobile hit-and-run](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | archetype | Daughters of Khaine | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [fast melee](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | archetype | Idoneth Deepkin | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [fast elite](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | archetype | Lumineth Realm-lords | spellslinger | under 1.5x the other factions | recipe not 1.5x the other factions | [strong magic](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | archetype | Seraphon | spellslinger | under 1.5x the other factions | recipe not 1.5x the other factions | [strong wizards](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | archetype | Blades of Khorne | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [aggressive fast melee](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | archetype | Blades of Khorne | sacrifice | under 1.5x the other factions | recipe not 1.5x the other factions | [Blood Tithe rewards deaths](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | archetype | Disciples of Tzeentch | spellslinger | under 1.5x the other factions | recipe not 1.5x the other factions | [magic-heavy](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✓ | archetype | Skaven | swarm | recipe score 0.20, 2.4x the other factions, 13 cards |  | [horde](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | archetype | Hedonites of Slaanesh | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [quick high-damage strikes](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | archetype | Beasts of Chaos | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [fast, mobile](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | archetype | Maggotkin of Nurgle | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [very tough, slow](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✓ | archetype | Maggotkin of Nurgle | poison_attrition | recipe score 2.22, 2.8x the other factions, 2 cards |  | [disease](https://wahapedia.ru/aos4/factions/maggotkin-of-nurgle/) |
| ✓ | archetype | Soulblight Gravelords | swarm | recipe score 0.30, 3.6x the other factions, 21 cards |  | [skeleton and zombie horde](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | archetype | Ossiarch Bonereapers | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [tanky](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✓ | archetype | Kruleboyz | trickery | recipe score 0.82, 2.1x the other factions, 3 cards |  | [cunning, Dirty Tricks](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | archetype | Gloomspite Gitz | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [horde](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | archetype | Ogor Mawtribes | sustain | under 1.5x the other factions | recipe not 1.5x the other factions | [healing access](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
