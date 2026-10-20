# Real-world test: every case

Made by `tools/realworld_report.py` from the library build. A case is a fact a wiki or guide states about a game (a faction's signature mechanic, its archetype, a two-card combo, a splash); the test checks whether the library finds it.

## Totals

| Game | Signature | Archetype | Combo | Splash | All |
|---|---|---|---|---|---|
| Darkest Dungeon |  |  | 4/5 |  | 4/5 |
| Duelyst | 5/8 | 4/5 |  |  | 9/13 |
| Faeria | 4/9 | 5/5 |  | 0/1 | 9/15 |
| Gwent (standalone) | 7/10 | 5/7 | 1/2 |  | 13/19 |
| Hearthstone | 9/10 | 7/10 | 4/10 | 3/6 | 23/36 |
| Hearthstone Battlegrounds |  |  | 7/10 |  | 7/10 |
| Inscryption | 0/3 | 1/2 | 0/2 |  | 1/7 |
| Into the Breach | 2/9 | 2/2 | 0/2 | 1/4 | 5/17 |
| Disney Lorcana | 15/19 | 6/7 | 5/7 |  | 26/33 |
| Marvel Snap |  |  | 7/10 |  | 7/10 |
| Monster Train | 4/9 | 3/5 |  |  | 7/14 |
| Magic: The Gathering | 10/10 | 4/6 | 2/4 | 6/8 | 22/28 |
| Legends of Runeterra | 5/10 | 3/5 | 1/1 |  | 9/16 |
| Shadowverse | 8/10 | 4/5 | 2/2 |  | 14/17 |
| Stormbound | 5/8 | 5/8 | 2/2 |  | 12/18 |
| Slay the Spire | 7/10 | 5/9 | 9/10 |  | 21/29 |
| Slay the Spire 2 (Early Access) | 5/11 | 2/6 | 0/2 |  | 7/19 |
| Star Wars: Unlimited | 13/14 | 5/6 |  |  | 18/20 |
| The Elder Scrolls: Legends | 9/12 | 4/8 |  |  | 13/20 |
| Warhammer 40,000 (10th edition) | 4/7 | 1/8 | 3/7 |  | 8/22 |
| Warhammer Age of Sigmar (4th edition) | 5/8 | 1/9 |  |  | 6/17 |
| Blood Bowl (Third Season) | 0/2 |  |  |  | 0/2 |
| Warhammer 40,000: Kill Team | 0/5 | 0/3 |  |  | 0/8 |
| Warhammer Underworlds |  | 1/10 |  |  | 1/10 |
| **All** | 117/184 | 68/126 | 47/76 | 10/19 | **242/405** |

## Why cases miss

| Cases | Type | Reason |
|---|---|---|
| 58 | archetype | recipe not 1.5x the other factions |
| 35 | signature | not 1.5x the rest of the game |
| 19 | signature | could be chance (5%) |
| 15 | combo | a card name is not in the library |
| 14 | combo | both cards there, no connection |
| 11 | signature | no card of the faction has it |
| 9 | splash | missing from the splash list |
| 2 | signature | faction not in library |

## Darkest Dungeon

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | combo | Flashbang | Finish Him | linked by relation, role |  | [stun then bonus damage on stunned](https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide) |
| ✓ | combo | If It Bleeds | Hound's Harry | linked by relation |  | [bleed party](https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide) |
| ✗ | combo | Wyrd Reconstruction | If It Bleeds |  | both cards there, no connection | [bleed party](https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide) |
| ✓ | combo | Point Blank Shot | Daemon's Pull | linked by keyword, relation |  | [pull toughest enemy forward for front-line shot](https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide) |
| ✓ | combo | Blinding Gas | Flashbang | linked by relation |  | [chain stuns](https://www.gameskinny.com/7xyiu/darkest-dungeon-party-building-guide) |

## Duelyst

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Lyonar Kingdoms | taunt | 12/90 cards (13%), 3.1x the rest, chance 0.001, rank 1 of 7 |  | [Provoke builds big board](https://gamewave.fr/duelyst/duelyst-le-jeu-de-carte-aux-six-factions/) |
| ✓ | signature | Lyonar Kingdoms | heal | 11/90 cards (12%), 3.3x the rest, chance 0.002, rank 1 of 7 |  | [strong healing](https://steamcommunity.com/app/291410/discussions/0/1696043263495626833) |
| ✓ | signature | Magmar Aspects | permanent_growth | 9/89 cards (10%), 3.9x the rest, chance 0.002, rank 1 of 7 |  | [Grow minions](https://steamcommunity.com/app/291410/discussions/0/1696043263495626833) |
| ✓ | signature | Abyssian Host | removal | 13/92 cards (14%), 2.7x the rest, chance 0.002, rank 1 of 7 |  | [removal-heavy](https://steamcommunity.com/app/291410/discussions/0/1696043263495626833) |
| ✓ | signature | Abyssian Host | death_trigger | 18/92 cards (20%), 3.2x the rest, chance 0.000, rank 1 of 7 |  | [Deathwatch effects](https://gamewave.fr/duelyst/duelyst-le-jeu-de-carte-aux-six-factions/) |
| ✗ | signature | Vetruvian Imperium | summon | 19/94 cards (20%), 1.4x the rest, chance 0.105, rank 3 of 7 | not 1.5x the rest of the game | [Dervishes, Obelysks](https://gamewave.fr/duelyst/duelyst-le-jeu-de-carte-aux-six-factions/) |
| ✗ | signature | Vanar Kindred | silence | 2/99 cards (2%), 1.2x the rest, chance 0.544, rank 5 of 7 | not 1.5x the rest of the game | [dispels/transforms minions](https://steamcommunity.com/app/291410/discussions/0/1696043263495626833) |
| ✗ | signature | Songhai Empire | stealth | 0/98 cards (0%), 0.0x the rest, chance 1.000, rank 3 of 7 | no card of the faction has it | [subterfuge and assassination](https://gamewave.fr/duelyst/duelyst-le-jeu-de-carte-aux-six-factions/) |
| ✗ | archetype | Abyssian Host | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [Wraithlings swarm](https://gamewave.fr/duelyst/duelyst-le-jeu-de-carte-aux-six-factions/) |
| ✓ | archetype | Songhai Empire | spellslinger | recipe score 1.17, 3.1x the other factions, 14 cards |  | [chained spell combos](https://gamewave.fr/duelyst/duelyst-le-jeu-de-carte-aux-six-factions/) |
| ✓ | archetype | Lyonar Kingdoms | sustain | recipe score 1.49, 3.6x the other factions, 12 cards |  | [attrition with healing](https://gamewave.fr/duelyst/duelyst-le-jeu-de-carte-aux-six-factions/) |
| ✓ | archetype | Magmar Aspects | scaling | recipe score 1.63, 12.8x the other factions, 10 cards |  | [Grow deck](https://steamcommunity.com/app/291410/discussions/0/1696043263495626833) |
| ✓ | archetype | Abyssian Host | sacrifice | recipe score 1.21, 3.0x the other factions, 29 cards |  | [profit from death](https://gamewave.fr/duelyst/duelyst-le-jeu-de-carte-aux-six-factions/) |

## Faeria

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Green | taunt | 13/67 cards (19%), 3.5x the rest, chance 0.000, rank 1 of 6 |  | [big minions and taunts](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✗ | signature | Green | stat_gain | 32/67 cards (48%), 2.1x the rest, chance 0.000, rank 1 of 6 | could be chance (5%) | [buffs and growth theme](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✗ | signature | Blue | transform | 2/71 cards (3%), 2.6x the rest, chance 0.247, rank 2 of 6 | could be chance (5%) | [creature transformation theme](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✗ | signature | Blue | movement | 33/71 cards (46%), 1.5x the rest, chance 0.007, rank 2 of 6 | could be chance (5%) | [mobility and moving lands](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✓ | signature | Red | direct_damage | 21/68 cards (31%), 5.5x the rest, chance 0.000, rank 1 of 6 |  | [burn to the orb](https://www.faeria.com/the-hub/guide/42-deck-archetypes) |
| ✓ | signature | Red | ranged | 6/68 cards (9%), 3.0x the rest, chance 0.032, rank 1 of 6 |  | [ranged effects](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✓ | signature | Yellow | haste | 6/70 cards (9%), 4.0x the rest, chance 0.013, rank 1 of 6 |  | [rush and haste](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✗ | signature | Yellow | resource_gain | 5/70 cards (7%), 1.4x the rest, chance 0.324, rank 1 of 6 | not 1.5x the rest of the game | [cards generate faeria](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |
| ✗ | signature | Yellow | movement | 42/70 cards (60%), 2.2x the rest, chance 0.000, rank 1 of 6 | could be chance (5%) | [movement tricks](https://www.faeria.com/the-hub/guide/42-deck-archetypes) |
| ✓ | archetype | Yellow | aggro_tempo | recipe score 0.62, 5.6x the other factions, 33 cards |  | [Yellow Rush](https://www.faeria.com/the-hub/guide/42-deck-archetypes) |
| ✓ | archetype | Red | burn | recipe score 1.85, 7.2x the other factions, 20 cards |  | [Red Yellow Burn](https://www.faeria.com/the-hub/guide/42-deck-archetypes) |
| ✓ | archetype | Green | sacrifice | recipe score 0.46, 1.8x the other factions, 16 cards |  | [Green Yellow Sacrifice](https://www.faeria.com/the-hub/guide/42-deck-archetypes) |
| ✓ | archetype | Blue | spellslinger | recipe score 0.99, 2.0x the other factions, 4 cards |  | [Blue Yellow events](https://www.faeria.com/the-hub/guide/42-deck-archetypes) |
| ✓ | archetype | Yellow | control | recipe score 0.50, 2.7x the other factions, 8 cards |  | [Yellow Control removal plus movement](https://www.faeria.com/the-hub/guide/42-deck-archetypes) |
| ✗ | splash | Yellow | sacrifice |  | missing from the splash list | [sacrifice theme besides Green](https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292) |

## Gwent (standalone)

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | signature | Northern Realms | block_armor | 6/178 cards (3%), 0.6x the rest, chance 0.923, rank 5 of 7 | not 1.5x the rest of the game | [armour absorbs damage](https://www.redbull.com/gb-en/Witcher-3-gwent-guide-2018) |
| ✗ | signature | Monster | aoe_damage | 14/183 cards (8%), 0.4x the rest, chance 1.000, rank 7 of 7 | not 1.5x the rest of the game | [weather hurts enemy side](https://www.redbull.com/gb-en/Witcher-3-gwent-guide-2018) |
| ✓ | signature | Monster | sacrifice | 19/183 cards (10%), 15.2x the rest, chance 0.000, rank 1 of 7 |  | [consume / kill own units](https://www.redbull.com/gb-en/Witcher-3-gwent-guide-2018) |
| ✗ | signature | Skellige | revive | 0/184 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 7 | no card of the faction has it | [resurrects from graveyard](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | signature | Skellige | condition_life | 4/184 cards (2%), 25.5x the rest, chance 0.001, rank 1 of 7 |  | [self-wounding for bonuses](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | signature | Nilfgaard | donate | 10/180 cards (6%), 8.2x the rest, chance 0.000, rank 1 of 7 |  | [disloyal units on opponent side](https://www.pcgamer.com/au/the-nilfgaard-faction-shows-gwent-has-a-life-after-the-witcher-3) |
| ✓ | signature | Nilfgaard | deck_position | 14/180 cards (8%), 3.7x the rest, chance 0.000, rank 1 of 7 |  | [Xarthisius views opponent deck top](https://www.pcgamer.com/au/the-nilfgaard-faction-shows-gwent-has-a-life-after-the-witcher-3) |
| ✓ | signature | Nilfgaard | tutor | 21/180 cards (12%), 1.4x the rest, chance 0.108, rank 2 of 7 |  | [Emissary/Rainfarn fetch deck cards](https://masters.playgwent.com/en/news/22010/the-evolution-of-gwents-factions) |
| ✓ | signature | Syndicate | coin_economy | 129/190 cards (68%), infx the rest, chance 0.000, rank 1 of 7 |  | [cards generate and spend coins](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | signature | Scoiatael | tribal | 29/188 cards (15%), 2.4x the rest, chance 0.000, rank 1 of 7 |  | [dwarf and elf families](https://www.redbull.com/gb-en/Witcher-3-gwent-guide-2018) |
| ✓ | archetype | Monster | swarm | recipe score 0.17, 4.6x the other factions, 70 cards |  | [swarm and devour](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | archetype | Skellige | graveyard | recipe score 1.45, 3.7x the other factions, 41 cards |  | [resurrection, graveyard interaction](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | archetype | Nilfgaard | control | recipe score 0.41, 1.8x the other factions, 40 cards |  | [locking, spying, counterplay](https://www.bluestacks.com/blog/game-guides/gwent/gwt-decks-guide-en.html) |
| ✓ | archetype | Northern Realms | fortress | recipe score 0.62, 1.8x the other factions, 33 cards |  | [armour, boosted hard-to-remove units](https://www.redbull.com/gb-en/Witcher-3-gwent-guide-2018) |
| ✗ | archetype | Scoiatael | control | under 1.5x the other factions | recipe not 1.5x the other factions | [Old Schirru control](https://masters.playgwent.com/en/news/22010/the-evolution-of-gwents-factions) |
| ✗ | archetype | Scoiatael | spellslinger | under 1.5x the other factions | recipe not 1.5x the other factions | [special-heavy spell deck](https://masters.playgwent.com/en/news/22010/the-evolution-of-gwents-factions) |
| ✓ | archetype | Monster | sacrifice | recipe score 1.95, 10.6x the other factions, 51 cards |  | [kill own units deck](https://www.redbull.com/gb-en/Witcher-3-gwent-guide-2018) |
| ✓ | combo | Vattier de Rideaux | Mangonel | linked by keyword, relation |  | [reveals trigger Mangonel damage](https://www.pcgamer.com/au/the-nilfgaard-faction-shows-gwent-has-a-life-after-the-witcher-3) |
| ✗ | combo | Letho | Fake Ciri |  | a card name is not in the library | [Letho absorbs and destroys Fake Ciri](https://www.pcgamer.com/au/the-nilfgaard-faction-shows-gwent-has-a-life-after-the-witcher-3) |

## Hearthstone

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Druid | resource_gain | 39/634 cards (6%), 11.4x the rest, chance 0.000, rank 1 of 12 |  | [mana acceleration](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Hunter | tribal | 97/507 cards (19%), 6.7x the rest, chance 0.000, rank 1 of 12 |  | [Beast synergy](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | signature | Mage | trap_secret | 50/548 cards (9%), 4.5x the rest, chance 0.000, rank 2 of 12 |  | [Secrets](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Paladin | shield | 112/531 cards (21%), 18.7x the rest, chance 0.000, rank 1 of 12 |  | [Divine Shield](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Priest | heal | 93/506 cards (18%), 4.0x the rest, chance 0.000, rank 1 of 12 |  | [healing](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Rogue | combo_sequence | 78/549 cards (14%), 20.9x the rest, chance 0.000, rank 1 of 12 |  | [Combo cards](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | signature | Shaman | overload_debt | 68/537 cards (13%), 5.1x the rest, chance 0.000, rank 1 of 12 |  | [Overload](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Warlock | life_payment | 8/534 cards (1%), 22.5x the rest, chance 0.000, rank 1 of 12 |  | [life as a resource](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | signature | Warrior | on_damaged | 18/506 cards (4%), 3.8x the rest, chance 0.000, rank 1 of 12 |  | [Enrage and on-damage effects](https://hearthstone.wiki.gg/wiki/Classes) |
| ✗ | signature | Demonhunter | tribal | 4/361 cards (1%), 0.3x the rest, chance 1.000, rank 11 of 12 | not 1.5x the rest of the game | [demons and fel](https://hearthstone.wiki.gg/wiki/Classes) |
| ✓ | archetype | Druid | swarm | recipe score 0.31, 1.9x the other factions, 175 cards |  | [Token Druid](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | archetype | Hunter | aggro_tempo | recipe score 0.35, 2.0x the other factions, 84 cards |  | [Face Hunter](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | archetype | Mage | spellslinger | recipe score 0.61, 3.3x the other factions, 98 cards |  | [spell focused](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | archetype | Paladin | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [Odd Paladin, minion swarms](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | archetype | Priest | sustain | recipe score 1.17, 4.2x the other factions, 104 cards |  | [healing Priest](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | archetype | Rogue | spellslinger | recipe score 0.74, 4.3x the other factions, 131 cards |  | [Miracle combo Rogue](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | archetype | Shaman | tribal | recipe score 0.24, 2.3x the other factions, 32 cards |  | [Murloc Shaman](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | archetype | Warlock | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [Zoo Warlock](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | archetype | Warrior | fortress | recipe score 1.00, 2.5x the other factions, 163 cards |  | [armor and Taunt, Control Warrior](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | archetype | Druid | ramp | under 1.5x the other factions | recipe not 1.5x the other factions | [Big Druid, mana generation](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | combo | Auchenai Soulpriest | Circle of Healing | linked by role |  | [heal turned into damage](https://www.keengamer.com/articles/guides/7-great-hearthstone-card-combos/) |
| ✓ | combo | Equality | Consecration | linked by relation |  | [board clear](https://www.keengamer.com/articles/guides/7-great-hearthstone-card-combos/) |
| ✓ | combo | Leeroy Jenkins | Shadowstep | linked by engine, relation |  | [replay for repeat charge damage](https://www.keengamer.com/articles/guides/7-great-hearthstone-card-combos/) |
| ✗ | combo | Unleash the Hounds | Stormwind Champion |  | both cards there, no connection | [hound buff burst](https://www.keengamer.com/articles/guides/7-great-hearthstone-card-combos/) |
| ✗ | combo | Injured Blademaster | Circle of Healing |  | both cards there, no connection | [heal triggers damage and buff](https://primagames.com/tips/hearthstone-powerful-card-combos) |
| ✓ | combo | Ancestral Spirit | Cairne Bloodhoof | linked by engine, keyword |  | [repeating deathrattle](https://primagames.com/tips/hearthstone-powerful-card-combos) |
| ✗ | combo | Force of Nature | Savage Roar |  | both cards there, no connection | [treant charge burst](https://primagames.com/tips/hearthstone-powerful-card-combos) |
| ✗ | combo | Defias Ringleader | The Coin |  | both cards there, no connection | [enables Combo](https://hearthstone.fandom.com/wiki/Combo) |
| ✗ | combo | Youthful Brewmaster | SI:7 Agent |  | both cards there, no connection | [re-trigger Combo](https://hearthstone.fandom.com/wiki/Combo) |
| ✗ | combo | Divine Spirit | Inner Fire |  | a card name is not in the library | [double then set attack to health](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | splash | Paladin | trap_secret |  | missing from the splash list | [Secret Paladin](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | splash | Priest | death_trigger |  |  | [Deathrattle Priest](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | splash | Rogue | death_trigger |  |  | [Deathrattle Rogue](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | splash | Shaman | direct_damage |  | missing from the splash list | [damage spells](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✓ | splash | Warlock | draw |  |  | [card draw](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |
| ✗ | splash | Druid | draw |  | missing from the splash list | [card draw](https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/) |

## Hearthstone Battlegrounds

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | combo | Mechano-Egg | Baron Rivendare |  | a card name is not in the library | [doubles deathrattle](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✓ | combo | Coldlight Seer | Brann Bronzebeard | linked by role |  | [doubled battlecry buff](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✓ | combo | King Bagurgle | Brann Bronzebeard | linked by role |  | [doubled battlecry buff](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✓ | combo | Gentle Megasaur | Brann Bronzebeard | linked by role |  | [doubled poison and divine shield](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✓ | combo | Rat Pack | Mama Bear | linked by relation, role, type |  | [beast scaling](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✓ | combo | Cave Hydra | Goldrinn, the Great Wolf | linked by type |  | [beast buff](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✓ | combo | Soul Juggler | Voidlord | linked by relation, type |  | [demon damage and taunt](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✗ | combo | Mechano-Egg | Cobalt Guardian |  | a card name is not in the library | [deathrattle retriggers shield](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✗ | combo | Replicating Menace | Cobalt Guardian |  | a card name is not in the library | [deathrattle retriggers shield](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |
| ✓ | combo | Wrath Weaver | Floating Watcher | linked by engine, type |  | [demon synergy](https://gamersdecide.dev.weebpal.com/articles/best-hearthstone-battlegrounds-cards) |

## Inscryption

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | signature | Undead | death_trigger | 4/20 cards (20%), 1.6x the rest, chance 0.260, rank 2 of 4 | could be chance (5%) | [Walkers/Obols give bones on death](https://steamcommunity.com/app/1092790/discussions/0/3553931489687797930) |
| ✗ | signature | Undead | summon | 2/20 cards (10%), 0.9x the rest, chance 0.675, rank 3 of 4 | not 1.5x the rest of the game | [Skeletons and Ghost Ship spawn skeletons](https://steamcommunity.com/app/1092790/discussions/0/3123802224156217321) |
| ✗ | signature | Beast | fodder | 3/77 cards (4%), 0.8x the rest, chance 0.773, rank 3 of 4 | not 1.5x the rest of the game | [squirrels and cat as fodder](https://steamcommunity.com/app/1092790/discussions/0/3553931489687797930) |
| ✓ | archetype | Undead | sacrifice | recipe score 0.81, 3.1x the other factions, 7 cards |  | [bone deck](https://steamcommunity.com/app/1092790/discussions/0/3553931489687797930) |
| ✗ | archetype | Beast | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [squirrel fodder decks](https://steamcommunity.com/app/1092790/discussions/0/3553931489687797930) |
| ✗ | combo | Necromancer | Walker |  | a card name is not in the library | [sacrifice to Walker for bones](https://steamcommunity.com/app/1092790/discussions/0/3553931489687797930) |
| ✗ | combo | Necromancer | Obol |  | a card name is not in the library | [sacrifice to Obol for bones](https://steamcommunity.com/app/1092790/discussions/0/3553931489687797930) |

## Into the Breach

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | signature | Prime | forced_movement | 17/31 cards (55%), 0.9x the rest, chance 0.699, rank 4 of 5 | not 1.5x the rest of the game | [most Prime weapons push (Titan Fist, Vice Fist)](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | signature | Prime | multi_target_attack | 8/31 cards (26%), 1.2x the rest, chance 0.362, rank 2 of 5 | not 1.5x the rest of the game | [Burst Beam hits a whole line](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | signature | Science | forced_movement | 16/25 cards (64%), 1.1x the rest, chance 0.305, rank 2 of 5 | not 1.5x the rest of the game | [Attraction Pulse and Grav Well pull](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✓ | signature | Science | swap | 9/25 cards (36%), 2.5x the rest, chance 0.015, rank 1 of 5 |  | [Swap weapon](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✓ | signature | Science | shield | 6/25 cards (24%), 2.7x the rest, chance 0.040, rank 1 of 5 |  | [Shield Projector and Shield Array](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | signature | Science | disable | 3/25 cards (12%), 1.9x the rest, chance 0.269, rank 2 of 5 | could be chance (5%) | [Frost Beam freezes](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | signature | Ranged | ranged | 16/26 cards (62%), 2.2x the rest, chance 0.002, rank 1 of 5 | could be chance (5%) | [artillery weapons](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | signature | Brute | movement | 7/29 cards (24%), 1.5x the rest, chance 0.240, rank 2 of 5 | not 1.5x the rest of the game | [Grappling Hook and charge engines](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | signature | Brute | friendly_fire | 4/29 cards (14%), 3.3x the rest, chance 0.071, rank 1 of 5 | could be chance (5%) | [Ramming Engines damage the mech itself](https://www.giantbomb.com/profile/majormitch/blog/thoughts-on-into-the-breachs-squads/116986/) |
| ✓ | archetype | Science | positional | recipe score 0.23, 3.2x the other factions, 19 cards |  | [pull, swap and push reposition Vek](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✓ | archetype | Science | fortress | recipe score 0.25, 1.8x the other factions, 10 cards |  | [shield weapons protect buildings](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | splash | Brute | forced_movement |  | missing from the splash list | [Taurus Cannon and Janus Cannon push](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✓ | splash | Brute | shield |  |  | [Phase Cannon shields buildings](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | splash | Science | damage_over_time |  | missing from the splash list | [Fire Beam burns](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | splash | Prime | damage_over_time |  | missing from the splash list | [Flame Thrower burns](https://intothebreach.fandom.com/wiki/Weapons?oldid=3699) |
| ✗ | combo | Electric Whip | Grappling Hook |  | both cards there, no connection | [hook and rocks build chains for lightning](https://www.gameskinny.com/i7374/into-the-breach-squads-guide) |
| ✗ | combo | Vice Fist | Grav Well |  | both cards there, no connection | [Gravity pulls, Judo pushes follow-up](https://www.pocketgamer.com/into-the-breach/best-squads) |

## Disney Lorcana

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Amber | heal | 40/309 cards (13%), 6.8x the rest, chance 0.000, rank 1 of 6 |  | [protection and healing](https://www.wargamer.com/disney-lorcana/colors) |
| ✓ | signature | Amethyst | return_to_hand | 20/315 cards (6%), 4.1x the rest, chance 0.000, rank 2 of 6 |  | [Recursion: cards return to hand](https://www.wargamer.com/disney-lorcana/colors) |
| ✓ | signature | Amethyst | draw | 77/315 cards (24%), 2.0x the rest, chance 0.000, rank 1 of 6 |  | [extra card draw](https://www.wargamer.com/disney-lorcana/colors) |
| ✓ | signature | Emerald | hand_disruption | 41/319 cards (13%), 15.2x the rest, chance 0.000, rank 1 of 6 |  | [Forcing opponents to discard](https://wiki.mushureport.com/wiki/Emerald) |
| ✓ | signature | Emerald | bounce_enemy | 21/319 cards (7%), 3.9x the rest, chance 0.000, rank 1 of 6 |  | [Returning cards in play to hand](https://wiki.mushureport.com/wiki/Emerald) |
| ✓ | signature | Emerald | immunity | 66/319 cards (21%), 2.0x the rest, chance 0.000, rank 1 of 6 |  | [Ward](https://wiki.mushureport.com/wiki/Emerald) |
| ✗ | signature | Emerald | recycle | 9/319 cards (3%), 1.3x the rest, chance 0.307, rank 3 of 6 | not 1.5x the rest of the game | [recovering actions from the discard pile](https://wiki.mushureport.com/wiki/Emerald) |
| ✗ | signature | Emerald | cost_reduction | 17/319 cards (5%), 1.2x the rest, chance 0.272, rank 2 of 6 | not 1.5x the rest of the game | [Reducing action costs](https://wiki.mushureport.com/wiki/Emerald) |
| ✓ | signature | Ruby | haste | 24/306 cards (8%), 4.2x the rest, chance 0.000, rank 2 of 6 |  | [Rush](https://www.wargamer.com/disney-lorcana/colors) |
| ✓ | signature | Ruby | destroy | 37/306 cards (12%), 2.2x the rest, chance 0.000, rank 1 of 6 |  | [Banishing characters](https://wiki.mushureport.com/wiki/Ruby) |
| ✓ | signature | Ruby | drawback | 41/306 cards (13%), 1.2x the rest, chance 0.178, rank 3 of 6 |  | [Reckless, "typically a downside"](https://wiki.mushureport.com/wiki/Ruby) |
| ✓ | signature | Ruby | untap | 36/306 cards (12%), 4.3x the rest, chance 0.000, rank 1 of 6 |  | [Readying exerted characters](https://wiki.mushureport.com/wiki/Ruby) |
| ✓ | signature | Sapphire | resource_gain | 44/303 cards (15%), 104.0x the rest, chance 0.000, rank 1 of 6 |  | [Ink ramp](https://wiki.mushureport.com/wiki/Sapphire) |
| ✗ | signature | Sapphire | points_scoring | 41/303 cards (14%), 0.8x the rest, chance 0.878, rank 5 of 6 | not 1.5x the rest of the game | [Lore increase](https://wiki.mushureport.com/wiki/Sapphire) |
| ✓ | signature | Sapphire | selection | 39/303 cards (13%), 5.4x the rest, chance 0.000, rank 1 of 6 |  | [card filtering (filtering the top of the deck)](https://wiki.mushureport.com/wiki/Sapphire) |
| ✓ | signature | Steel | damage | 65/303 cards (21%), 4.5x the rest, chance 0.000, rank 1 of 6 |  | [Direct damage to characters](https://wiki.mushureport.com/wiki/Steel) |
| ✓ | signature | Steel | taunt | 18/303 cards (6%), 3.9x the rest, chance 0.000, rank 2 of 6 |  | [Bodyguard](https://wiki.mushureport.com/wiki/Steel) |
| ✓ | signature | Steel | attack_lock | 11/303 cards (4%), 8.7x the rest, chance 0.000, rank 1 of 6 |  | [Challenge prevention](https://wiki.mushureport.com/wiki/Steel) |
| ✗ | signature | Steel | stat_gain | 60/303 cards (20%), 1.0x the rest, chance 0.510, rank 2 of 6 | not 1.5x the rest of the game | [Challenger, "Strength increase"](https://wiki.mushureport.com/wiki/Steel) |
| ✓ | archetype | Ruby | aggro_tempo | recipe score 0.58, 4.3x the other factions, 44 cards |  | [Aggressive and direct ... Rush](https://www.wargamer.com/disney-lorcana/colors) |
| ✓ | archetype | Sapphire | ramp | recipe score 0.65, 16.5x the other factions, 74 cards |  | [ramp and big combo cards](https://www.wargamer.com/disney-lorcana/colors) |
| ✗ | archetype | Steel | control | under 1.5x the other factions | recipe not 1.5x the other factions | [Midrange and Control are the most popular archetypes](https://www.wargamer.com/disney-lorcana/colors) |
| ✓ | archetype | Steel | fortress | recipe score 0.93, 3.9x the other factions, 103 cards |  | [Focuses on defense](https://www.wargamer.com/disney-lorcana/colors) |
| ✓ | archetype | Amber | sustain | recipe score 0.48, 7.8x the other factions, 40 cards |  | [protection and healing](https://www.wargamer.com/disney-lorcana/colors) |
| ✓ | archetype | Emerald | disruption | recipe score 0.41, 2.3x the other factions, 45 cards |  | [forcing opponents to discard](https://www.wargamer.com/disney-lorcana/colors) |
| ✓ | archetype | Amethyst | card_advantage | recipe score 0.60, 2.0x the other factions, 103 cards |  | [extra card draw](https://www.wargamer.com/disney-lorcana/colors) |
| ✓ | combo | Merlin - Goat | Madam Mim - Fox | linked by relation, type |  | [bounce Merlin for lore on leaving and entering play](https://www.wargamer.com/best-disney-lorcana-cards) |
| ✓ | combo | Merlin - Goat | Arthur - Wizard's Apprentice | linked by relation, type |  | [returning Merlin to hand repeats his lore](https://www.wargamer.com/best-disney-lorcana-cards) |
| ✓ | combo | Merlin - Rabbit | Madam Mim - Snake | linked by engine, relation, type |  | [bounce Rabbit to draw on leave and on play](https://spellmana.com/amethyst-sapphire-deck-guide-lorcana/) |
| ✓ | combo | Tipo - Growing Son | Madam Mim - Snake | linked by engine, relation, type |  | [quest, bounce, replay or ink](https://spellmana.com/amethyst-sapphire-deck-guide-lorcana/) |
| ✗ | combo | Tinker Bell - Giant Fairy | Grab Your Sword |  | both cards there, no connection | [1 damage to all on play, then sing for 2 more to all](https://geekydomain.com/blogs/guides/competitive-amethyst-steel-bounce-guide) |
| ✗ | combo | Tinker Bell - Giant Fairy | A Whole New World |  | both cards there, no connection | [exert the 6-cost to sing the 5-cost song for free](https://geekydomain.com/blogs/guides/competitive-amethyst-steel-bounce-guide) |
| ✓ | combo | Captain Hook - Forceful Duelist | Mr. Smee - Bumbling Mate | linked by relation, type |  | [a Captain keeps Smee from damaging himself](https://geekydomain.com/blogs/guides/competitive-amethyst-steel-bounce-guide) |

## Marvel Snap

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | combo | MODOK | Hela |  | a card name is not in the library | [discard hand then return cards](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✗ | combo | Wong | Odin |  | a card name is not in the library | [doubled On Reveal triggers](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✗ | combo | Wong | Doctor Doom |  | a card name is not in the library | [DoomBots twice](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Ironheart | Odin | linked by keyword, role |  | [Odin doubles power boosts](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Black Panther | Odin | linked by keyword, role |  | [Panther power doubles repeatedly](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Forge | Silver Surfer | linked by keyword |  | [3-cost cards gain +2](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Brood | Wolfsbane | linked by engine, keyword, relation, role |  | [three cards at one location boosted](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Moon Girl | Devil Dinosaur | linked by relation |  | [doubles hand size](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Shuri | Typhoid Mary | linked by engine, relation, role |  | [doubles next card](https://www.highgroundgaming.com/marvel-snap-best-decks/) |
| ✓ | combo | Shuri | Taskmaster | linked by keyword, role |  | [copies doubled power](https://www.highgroundgaming.com/marvel-snap-best-decks/) |

## Monster Train

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | signature | Hellhorned | multi_attack | 2/39 cards (5%), 1.2x the rest, chance 0.535, rank 2 of 7 | not 1.5x the rest of the game | [Multistrike and Rage](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✗ | signature | Hellhorned | stat_gain | 5/39 cards (13%), 0.7x the rest, chance 0.833, rank 5 of 7 | not 1.5x the rest of the game | [Multistrike and Rage](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✗ | archetype | Hellhorned | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [Offense-focused, "much more firepower"](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✗ | signature | Awoken | multi_target_attack | 2/39 cards (5%), 3.0x the rest, chance 0.207, rank 2 of 7 | could be chance (5%) | [Giant minions that can sweep enemies](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✗ | archetype | Awoken | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [Defensive tanks](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✓ | signature | Stygian Guard | on_spell | 9/41 cards (22%), 50.7x the rest, chance 0.000, rank 1 of 7 |  | [incant abilities](https://indiecator.org/2021/07/12/monster-train-my-favourite-clans/) |
| ✗ | signature | Stygian Guard | damage_over_time | 13/41 cards (32%), 1.6x the rest, chance 0.082, rank 3 of 7 | could be chance (5%) | [Frostbite effects](https://indiecator.org/2021/07/12/monster-train-my-favourite-clans/) |
| ✓ | archetype | Stygian Guard | spellslinger | recipe score 1.05, 7.5x the other factions, 12 cards |  | [their powerful spells](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✗ | signature | Umbra | summon | 2/46 cards (4%), 1.0x the rest, chance 0.633, rank 2 of 7 | not 1.5x the rest of the game | [Morsel units are summoned and eaten](https://indiecator.org/2021/07/12/monster-train-my-favourite-clans/) |
| ✓ | archetype | Umbra | sacrifice | recipe score 1.03, 2.3x the other factions, 7 cards |  | [buffing units by killing other units](https://indiecator.org/2021/07/12/monster-train-my-favourite-clans/) |
| ✓ | signature | Melting Remnant | revive | 7/40 cards (18%), 20.3x the rest, chance 0.000, rank 1 of 7 |  | [dying "return them to the deck with upgraded stats"](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✓ | signature | Melting Remnant | self_destruct | 6/40 cards (15%), infx the rest, chance 0.000, rank 1 of 7 |  | [burnout kills the unit when the stacks run out](https://indiecator.org/2021/07/12/monster-train-my-favourite-clans/) |
| ✓ | archetype | Melting Remnant | sacrifice | recipe score 2.51, 12.3x the other factions, 15 cards |  | [Aggressive and self-sacrificing](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |
| ✓ | signature | Wurmkin | transform | 4/42 cards (10%), infx the rest, chance 0.001, rank 1 of 7 |  | [Hatching Eggs](https://progameguides.com/monster-train/best-clans-in-monster-train-ranked/) |

## Magic: The Gathering

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Red | direct_damage | 1367/4380 cards (31%), 3.5x the rest, chance 0.000, rank 1 of 6 |  | [primary direct damage](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | White | first_strike | 668/4300 cards (16%), 1.9x the rest, chance 0.000, rank 1 of 6 |  | [primary first and double strike](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Blue | counter_spell | 361/4291 cards (8%), 6.2x the rest, chance 0.000, rank 1 of 6 |  | [primary counterspells](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Black | destroy | 831/4375 cards (19%), 3.4x the rest, chance 0.000, rank 1 of 6 |  | [primary destroying creatures](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Green | stat_gain | 1045/4242 cards (25%), 1.7x the rest, chance 0.000, rank 1 of 6 |  | [primary +1/+1 counters](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Red | haste | 803/4380 cards (18%), 8.2x the rest, chance 0.000, rank 1 of 6 |  | [primary haste](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | White | lifesteal | 1016/4300 cards (24%), 1.6x the rest, chance 0.000, rank 1 of 6 |  | [primary lifelink](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Blue | draw | 1165/4291 cards (27%), 2.4x the rest, chance 0.000, rank 1 of 6 |  | [primary card draw](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Black | deathtouch | 1042/4375 cards (24%), 2.0x the rest, chance 0.000, rank 1 of 6 |  | [primary deathtouch](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | signature | Green | excess_damage | 1300/4242 cards (31%), 1.7x the rest, chance 0.000, rank 1 of 6 |  | [primary trample](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | archetype | Red | burn | recipe score 2.32, 84.6x the other factions, 773 cards |  | [direct damage](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | archetype | Blue | control | recipe score 1.05, 9.9x the other factions, 1296 cards |  | [counterspells and bounce](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | archetype | Black | graveyard | recipe score 1.13, 8.2x the other factions, 1705 cards |  | [reanimation](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✗ | archetype | Green | ramp | under 1.5x the other factions | recipe not 1.5x the other factions | [permanent mana and putting lands/creatures into play](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✗ | archetype | White | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [token generation and team pumps](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | archetype | Black | sacrifice | recipe score 0.85, 11.7x the other factions, 1232 cards |  | [forced sacrifice and rewards for death](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✗ | combo | Splinter Twin | Pestermite |  | a card name is not in the library | [infinite hasty copies](https://edhrec.com/combos/ur/2905-4702) |
| ✓ | combo | Kiki-Jiki, Mirror Breaker | Restoration Angel | linked by engine, relation |  | [infinite hasty copies](https://blog.cardkingdom.com/?p=10964) |
| ✓ | combo | Saheeli Rai | Felidar Guardian | linked by engine, relation |  | [infinite copies](https://blog.cardkingdom.com/?p=10964) |
| ✗ | combo | Inverter of Truth | Thassa's Oracle |  | both cards there, no connection | [win with empty library](https://blog.cardkingdom.com/?p=10964) |
| ✓ | splash | White | draw |  |  | [tertiary card draw](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | splash | Red | draw |  |  | [tertiary card draw](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✗ | splash | Blue | summon |  | missing from the splash list | [secondary token generation](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✗ | splash | Black | summon |  | missing from the splash list | [secondary token generation](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | splash | Green | deathtouch |  |  | [secondary deathtouch](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | splash | White | counter_spell |  |  | [tertiary counterspells](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | splash | Red | revive |  |  | [secondary reanimation](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |
| ✓ | splash | Black | heal |  |  | [secondary life gain](https://magic.wizards.com/en/news/making-magic/mechanical-color-pie-2021) |

## Legends of Runeterra

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Noxus | excess_damage | 78/218 cards (36%), 2.0x the rest, chance 0.000, rank 1 of 10 |  | [Overwhelm](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |
| ✓ | signature | Shadow Isles | death_trigger | 31/213 cards (15%), 7.3x the rest, chance 0.000, rank 1 of 10 |  | [Last Breath](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |
| ✗ | signature | Demacia | forced_attack | 0/203 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 10 | no card of the faction has it | [Challenger](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |
| ✗ | signature | Freljord | stat_loss | 10/210 cards (5%), 1.2x the rest, chance 0.328, rank 3 of 10 | not 1.5x the rest of the game | [Frostbite](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |
| ✗ | signature | Piltover & Zaun | evasion | 29/226 cards (13%), 1.0x the rest, chance 0.558, rank 5 of 10 | not 1.5x the rest of the game | [Elusive](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |
| ✓ | signature | Ionia | evasion | 42/235 cards (18%), 1.4x the rest, chance 0.014, rank 3 of 10 |  | [Elusive](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |
| ✗ | signature | Noxus | evasion | 16/218 cards (7%), 0.5x the rest, chance 0.998, rank 8 of 10 | not 1.5x the rest of the game | [Fearsome](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |
| ✓ | signature | Shadow Isles | evasion | 53/213 cards (25%), 2.1x the rest, chance 0.000, rank 1 of 10 |  | [Fearsome](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |
| ✗ | signature | Demacia | attack_now | 3/203 cards (1%), 1.1x the rest, chance 0.532, rank 4 of 10 | not 1.5x the rest of the game | [Rally](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |
| ✓ | signature | Freljord | excess_damage | 60/210 cards (29%), 1.5x the rest, chance 0.001, rank 2 of 10 |  | [Overwhelm](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |
| ✗ | archetype | Noxus | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [offense-first All-Out Assault](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |
| ✓ | archetype | Shadow Isles | sacrifice | recipe score 2.12, 17.4x the other factions, 94 cards |  | [sacrifices units](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |
| ✗ | archetype | Freljord | disruption | under 1.5x the other factions | recipe not 1.5x the other factions | [freezes opponents](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |
| ✓ | archetype | Ionia | aggro_tempo | recipe score 0.43, 2.0x the other factions, 76 cards |  | [evades defenses](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |
| ✓ | archetype | Shadow Isles | swarm | recipe score 0.48, 2.9x the other factions, 72 cards |  | [swarms the board with low-level units](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |
| ✓ | combo | Ashe | Rimetusk Shaman | linked by keyword, relation |  | [Frostbite each round](https://www.oneesports.gg/legends-of-runeterra/legends-of-runeterra-beginners-guide-tips-and-strategies-everyone-should-know/) |

## Shadowverse

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Forestcraft | combo_sequence | 87/492 cards (18%), 172.1x the rest, chance 0.000, rank 1 of 9 |  | [many cards per turn](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✓ | signature | Swordcraft | tribal | 70/519 cards (13%), 1.6x the rest, chance 0.000, rank 4 of 9 |  | [Officers and Commanders](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✓ | signature | Runecraft | in_hand_buff | 118/514 cards (23%), 7.3x the rest, chance 0.000, rank 1 of 9 |  | [Spellboost](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✗ | signature | Dragoncraft | resource_gain | 45/492 cards (9%), 1.4x the rest, chance 0.016, rank 1 of 9 | not 1.5x the rest of the game | [extra PP and Overflow](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✓ | signature | Shadowcraft | death_trigger | 170/502 cards (34%), 2.8x the rest, chance 0.000, rank 1 of 9 |  | [Last Words](https://shadowversecb.com/cards-classes) |
| ✗ | signature | Bloodcraft | life_payment | 33/491 cards (7%), 1.1x the rest, chance 0.295, rank 2 of 9 | not 1.5x the rest of the game | [risks own life](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✓ | signature | Havencraft | delayed | 166/495 cards (34%), 4.9x the rest, chance 0.000, rank 1 of 9 |  | [Countdown amulets](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✓ | signature | Portalcraft | deck_condition | 51/480 cards (11%), 11.2x the rest, chance 0.000, rank 1 of 9 |  | [Resonance even deck](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✓ | signature | Forestcraft | return_to_hand | 38/492 cards (8%), 14.3x the rest, chance 0.000, rank 1 of 9 |  | [returns own cards to hand](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✓ | signature | Swordcraft | haste | 130/519 cards (25%), 1.4x the rest, chance 0.000, rank 1 of 9 |  | [Storm and Rush](https://shadowversecb.com/cards-classes) |
| ✓ | archetype | Forestcraft | swarm | recipe score 0.12, 1.8x the other factions, 94 cards |  | [many small Fairies](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✓ | archetype | Runecraft | spellslinger | recipe score 1.63, 4.6x the other factions, 45 cards |  | [Spellboost decks](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✗ | archetype | Dragoncraft | ramp | under 1.5x the other factions | recipe not 1.5x the other factions | [extra PP for big dragons](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✓ | archetype | Shadowcraft | graveyard | recipe score 1.47, 7.2x the other factions, 197 cards |  | [Burial Rite and Reanimate](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✓ | archetype | Swordcraft | tribal | recipe score 0.23, 1.8x the other factions, 70 cards |  | [Officer and Commander](https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/) |
| ✓ | combo | Witching Moggy | Chrono Witch | linked by relation |  | [Spellboost synergy](https://shadowversecb.com/cards-classes) |
| ✓ | combo | Cursed Maiden | God of Curses | linked by keyword, relation, role |  | [countdown and resurrection](https://shadowversecb.com/cards-classes) |

## Stormbound

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Winter | disable | 10/30 cards (33%), infx the rest, chance 0.000, rank 1 of 5 |  | [Freeze status](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✓ | signature | Winter | resource_gain | 5/30 cards (17%), infx the rest, chance 0.000, rank 1 of 5 |  | [gaining extra mana (Frozen Core, Dawnsparks)](https://stormboundkingdomwars.fandom.com/wiki/Winter_Pact?oldid=7023) |
| ✗ | signature | Winter | aoe_damage | 4/30 cards (13%), 0.6x the rest, chance 0.931, rank 4 of 5 | not 1.5x the rest of the game | [Area damage (Wisp Cloud, Midwinter Chaos)](https://stormboundkingdomwars.fandom.com/wiki/Winter_Pact?oldid=7023) |
| ✓ | archetype | Winter | control | recipe score 1.03, 2.4x the other factions, 12 cards |  | [Defensive board control](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✓ | archetype | Winter | ramp | recipe score 0.66, 5.4x the other factions, 5 cards |  | [gaining extra mana](https://stormboundkingdomwars.fandom.com/wiki/Winter_Pact?oldid=7023) |
| ✓ | signature | Shadowfen | damage_over_time | 11/28 cards (39%), 1.8x the rest, chance 0.042, rank 1 of 5 |  | [poison](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✗ | signature | Shadowfen | summon | 7/28 cards (25%), 1.8x the rest, chance 0.124, rank 1 of 5 | could be chance (5%) | [floods the board with Toads](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✓ | archetype | Shadowfen | swarm | recipe score 0.12, 5.7x the other factions, 7 cards |  | [floods the board with Toads](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✗ | archetype | Shadowfen | tribal | under 1.5x the other factions | recipe not 1.5x the other factions | [Toads, then buffs them](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✗ | signature | Swarm | summon | 6/28 cards (21%), 1.4x the rest, chance 0.263, rank 2 of 5 | not 1.5x the rest of the game | [unit generation](https://stormboundkingdomwars.fandom.com/wiki/Swarm_of_the_East?oldid=4049) |
| ✓ | signature | Swarm | direct_damage | 7/28 cards (25%), 1.3x the rest, chance 0.313, rank 2 of 5 |  | [direct base damage](https://stormboundkingdomwars.fandom.com/wiki/Swarm_of_the_East?oldid=4049) |
| ✓ | signature | Swarm | movement | 6/28 cards (21%), 4.3x the rest, chance 0.008, rank 1 of 5 |  | [high movement](https://stormboundkingdomwars.fandom.com/wiki/Swarm_of_the_East?oldid=4049) |
| ✓ | archetype | Swarm | aggro_tempo | recipe score 0.03, 4.0x the other factions, 4 cards |  | [Almost entirely Aggro](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✓ | archetype | Swarm | swarm | recipe score 0.08, 2.7x the other factions, 6 cards |  | [filling the board with many weak units](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✗ | archetype | Swarm | tribal | under 1.5x the other factions | recipe not 1.5x the other factions | [Satyrs](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✗ | archetype | Ironclad | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [Rush with cheap cards](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✓ | combo | Wisp Cloud | Frosthexers | linked by type |  | [freeze all surrounding, then damage all frozen](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |
| ✓ | combo | Moonlit Aerie | Queen of Herds | linked by type |  | [Queen plays Satyrs, Aerie buffs all Satyrs](https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html) |

## Slay the Spire

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Ironclad | stat_gain | 6/83 cards (7%), 4.1x the rest, chance 0.016, rank 1 of 5 |  | [Strength scaling (Demon Form, Inflame)](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✗ | signature | Ironclad | exhaust | 26/83 cards (31%), 1.2x the rest, chance 0.200, rank 2 of 5 | not 1.5x the rest of the game | [Exhaust builds (Feel No Pain, Dark Embrace)](https://slaythespire.gg/guides/slay-the-spire-best-character) |
| ✗ | signature | Ironclad | life_payment | 0/83 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 5 | no card of the faction has it | [self-damage with Rupture and Hemokinesis](https://www.gamecat.it.com/articles/slay-the-spire-2-best-builds) |
| ✓ | signature | Silent | damage_over_time | 30/83 cards (36%), 1.3x the rest, chance 0.064, rank 1 of 5 |  | [Poison stacking](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | signature | Silent | discard | 10/83 cards (12%), 41.2x the rest, chance 0.000, rank 1 of 5 |  | [discard engine (Calculated Gamble, Acrobatics)](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✗ | signature | Silent | generate_cards | 8/83 cards (10%), 0.9x the rest, chance 0.713, rank 3 of 5 | not 1.5x the rest of the game | [Shivs made by Blade Dance and Infinite Blades](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | signature | Defect | slots_queue | 32/89 cards (36%), infx the rest, chance 0.000, rank 1 of 5 |  | [Orb slots](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | signature | Watcher | stances | 28/89 cards (31%), infx the rest, chance 0.000, rank 1 of 5 |  | [Calm, Wrath, Divinity](https://slaythespire.gg/guides/slay-the-spire-best-character) |
| ✓ | signature | Watcher | retain | 13/89 cards (15%), 7.0x the rest, chance 0.000, rank 1 of 5 |  | [Retain build (Establishment, Sands of Time)](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | signature | Watcher | selection | 9/89 cards (10%), 4.2x the rest, chance 0.003, rank 2 of 5 |  | [Scry build (Cut Through Fate, Third Eye)](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✗ | archetype | Ironclad | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [Bunker build with Barricade and Body Slam](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | archetype | Ironclad | scaling | recipe score 0.92, 3.0x the other factions, 5 cards |  | [Strength scaling](https://slaythespire.gg/guides/slay-the-spire-best-character) |
| ✓ | archetype | Silent | poison_attrition | recipe score 3.25, 99.0x the other factions, 9 cards |  | [Poison with Catalyst](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✗ | archetype | Silent | spellslinger | under 1.5x the other factions | recipe not 1.5x the other factions | [cheap-card chains (After Image, A Thousand Cuts)](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✗ | archetype | Silent | card_advantage | under 1.5x the other factions | recipe not 1.5x the other factions | [Discard and draw cycling](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | archetype | Defect | fortress | recipe score 0.72, 5.9x the other factions, 24 cards |  | [Frost orb tank](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✗ | archetype | Defect | scaling | under 1.5x the other factions | recipe not 1.5x the other factions | [Claw scaling over the fight](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | archetype | Watcher | transformation | recipe score 1.34, 99.0x the other factions, 28 cards |  | [stance dancing](https://slaythespire.gg/guides/slay-the-spire-best-character) |
| ✓ | archetype | Watcher | card_advantage | recipe score 1.03, 3.3x the other factions, 18 cards |  | [Scry and card control](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | combo | Body Slam | Barricade | linked by keyword, role |  | [keep Block, convert it to damage](https://www.thegamer.com/slay-the-spire-best-builds/) |
| ✓ | combo | Corruption | Feel No Pain | linked by engine, role |  | [free exhausting skills give Block](https://www.gamecat.it.com/articles/slay-the-spire-2-best-builds) |
| ✓ | combo | Limit Break | Inflame | linked by keyword, relation |  | [Limit Break doubles stacked Strength](https://www.gamecat.it.com/articles/slay-the-spire-2-best-builds) |
| ✓ | combo | Rupture | Hemokinesis | linked by engine, role |  | [self-damage turns into Strength](https://www.gamecat.it.com/articles/slay-the-spire-2-best-builds) |
| ✓ | combo | Noxious Fumes | Catalyst | linked by keyword, role |  | [Catalyst multiplies stacked Poison](https://www.gamecat.it.com/articles/slay-the-spire-2-best-builds) |
| ✓ | combo | After Image | Blade Dance | linked by relation |  | [free Shivs each give Block](https://www.gamecat.it.com/articles/slay-the-spire-2-best-builds) |
| ✓ | combo | Loop | Defragment | linked by role |  | [Focus plus repeated orb passives](https://slaythespire.gg/guides/slay-the-spire-best-character) |
| ✓ | combo | Flurry of Blows | Mental Fortress | linked by keyword, role |  | [stance changes recur and give Block](https://www.highgroundgaming.com/slay-the-spire-watcher-guide/) |
| ✓ | combo | Worship | Brilliance | linked by keyword |  | [Mantra raises Brilliance damage](https://www.highgroundgaming.com/slay-the-spire-watcher-guide/) |
| ✗ | combo | All for One | Claw |  | both cards there, no connection | [0-cost cards return and Claw grows](https://slaythespire.gg/guides/slay-the-spire-best-character) |

## Slay the Spire 2 (Early Access)

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | signature | Ironclad | stat_gain | 9/103 cards (9%), 1.5x the rest, chance 0.162, rank 3 of 8 | could be chance (5%) | [Strength scaling](https://keengamer.com/articles/guides/slay-the-spire-2-best-character-tier-list) |
| ✗ | signature | Ironclad | life_payment | 0/103 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 8 | no card of the faction has it | [self-damage synergy](https://slaythespire2.gg/characters) |
| ✓ | signature | Ironclad | exhaust | 31/103 cards (30%), 2.1x the rest, chance 0.000, rank 1 of 8 |  | [Exhaust synergy](https://slaythespire2.gg/characters) |
| ✓ | signature | Silent | damage_over_time | 38/106 cards (36%), 1.8x the rest, chance 0.000, rank 2 of 8 |  | [Poison stacking](https://keengamer.com/articles/guides/slay-the-spire-2-best-character-tier-list) |
| ✗ | signature | Silent | generate_cards | 12/106 cards (11%), 1.4x the rest, chance 0.163, rank 3 of 8 | not 1.5x the rest of the game | [Shiv generation](https://keengamer.com/articles/guides/slay-the-spire-2-best-character-tier-list) |
| ✓ | signature | Silent | discard | 19/106 cards (18%), 40.3x the rest, chance 0.000, rank 1 of 8 |  | [Sly discard payoffs](https://slaythespire2.gg/characters) |
| ✓ | signature | Defect | slots_queue | 42/112 cards (38%), 111.6x the rest, chance 0.000, rank 1 of 8 |  | [Orb channelling](https://slaythespire2.gg/characters) |
| ✓ | signature | Necrobinder | summon | 12/107 cards (11%), 33.6x the rest, chance 0.000, rank 1 of 8 |  | [companion Osty and Summon](https://slaythespire2.gg/characters) |
| ✗ | signature | Necrobinder | destroy | 0/107 cards (0%), 0.0x the rest, chance 1.000, rank 1 of 8 | no card of the faction has it | [Doom executes at a health threshold](https://keengamer.com/articles/guides/slay-the-spire-2-best-character-tier-list) |
| ✗ | signature | Regent | resource_gain | 8/106 cards (8%), 1.0x the rest, chance 0.609, rank 4 of 8 | not 1.5x the rest of the game | [Stars resource](https://slaythespire2.gg/characters) |
| ✗ | signature | Regent | permanent_growth | 0/106 cards (0%), 0.0x the rest, chance 1.000, rank 6 of 8 | no card of the faction has it | [Forge grows the Sovereign Blade](https://slaythespire2.gg/characters) |
| ✗ | archetype | Ironclad | scaling | under 1.5x the other factions | recipe not 1.5x the other factions | [Strength scaling](https://brokenbuilds.gg/slay-the-spire-2/guides/slay-the-spire-2-best-builds) |
| ✓ | archetype | Silent | poison_attrition | recipe score 3.55, 99.0x the other factions, 14 cards |  | [Poison attrition](https://slaythespire2.gg/characters) |
| ✗ | archetype | Silent | card_advantage | under 1.5x the other factions | recipe not 1.5x the other factions | [discard cycling](https://keengamer.com/articles/guides/slay-the-spire-2-best-character-tier-list) |
| ✗ | archetype | Defect | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [Frost tank with Focus](https://brokenbuilds.gg/slay-the-spire-2/guides/slay-the-spire-2-best-builds) |
| ✓ | archetype | Necrobinder | control | recipe score 0.53, 2.5x the other factions, 4 cards |  | [Doom execute](https://brokenbuilds.gg/slay-the-spire-2/guides/slay-the-spire-2-best-builds) |
| ✗ | archetype | Regent | scaling | under 1.5x the other factions | recipe not 1.5x the other factions | [patient long-term scaling](https://slaythespire2.gg/characters) |
| ✗ | combo | Star Battery | Sovereign Blade |  | a card name is not in the library | [climbing damage plan for the Act 3 fight](https://brokenbuilds.gg/slay-the-spire-2/guides/slay-the-spire-2-best-builds) |
| ✗ | combo | Parry | Sword Sage |  | both cards there, no connection | [defensive loop](https://brokenbuilds.gg/slay-the-spire-2/guides/slay-the-spire-2-best-builds) |

## Star Wars: Unlimited

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Vigilance | taunt | 64/418 cards (15%), 3.6x the rest, chance 0.000, rank 1 of 7 |  | [Sentinel keyword (primary)](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Vigilance | heal | 83/418 cards (20%), 4.7x the rest, chance 0.000, rank 1 of 7 |  | [healing units and bases, Restore (primary)](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Vigilance | destroy | 60/418 cards (14%), 1.7x the rest, chance 0.000, rank 1 of 7 |  | [defeating enemy units (primary)](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Command | resource_gain | 15/430 cards (3%), 9.6x the rest, chance 0.000, rank 1 of 7 |  | [resource acceleration (primary)](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✗ | signature | Command | condition_count | 74/430 cards (17%), 1.0x the rest, chance 0.401, rank 3 of 7 | not 1.5x the rest of the game | [rewards for having many units (primary)](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Command | stat_gain | 171/430 cards (40%), 1.3x the rest, chance 0.000, rank 2 of 7 |  | [temporary stat buffs (primary)](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Aggression | direct_damage | 171/421 cards (41%), 1.7x the rest, chance 0.000, rank 1 of 7 |  | [direct damage to units and bases (primary)](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Aggression | excess_damage | 162/421 cards (38%), 1.2x the rest, chance 0.009, rank 1 of 7 |  | [Overwhelm (primary)](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Aggression | untap | 35/421 cards (8%), 3.0x the rest, chance 0.000, rank 1 of 7 |  | [readying units (primary)](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Aggression | draw | 38/421 cards (9%), 1.8x the rest, chance 0.003, rank 1 of 7 |  | [card draw (primary)](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Cunning | attack_now | 48/445 cards (11%), 2.3x the rest, chance 0.000, rank 2 of 7 |  | [Ambush keyword (primary)](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Cunning | disable | 69/445 cards (16%), 15.2x the rest, chance 0.000, rank 1 of 7 |  | [exhausting units (primary)](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Cunning | bounce_enemy | 59/445 cards (13%), 4.5x the rest, chance 0.000, rank 1 of 7 |  | [returning units to hand (primary)](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | signature | Cunning | immunity | 18/445 cards (4%), 2.1x the rest, chance 0.011, rank 3 of 7 |  | [Hidden keyword (primary)](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✗ | archetype | Command | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [playing lots of units](https://starwarsunlimited.com/articles/command) |
| ✓ | archetype | Command | ramp | recipe score 0.47, 3.2x the other factions, 68 cards |  | [resource acceleration](https://starwarsunlimited.com/articles/command) |
| ✓ | archetype | Aggression | aggro_tempo | recipe score 0.18, 3.6x the other factions, 170 cards |  | [attack bonuses and offensive keywords](https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie) |
| ✓ | archetype | Aggression | burn | recipe score 2.02, 15.2x the other factions, 146 cards |  | [damage, damage, damage](https://starwarsunlimited.com/articles/aggression) |
| ✓ | archetype | Vigilance | fortress | recipe score 0.68, 1.9x the other factions, 133 cards |  | [Defensive units with strong HP](https://cardgamer.com/games/star-wars/aspects-in-star-wars-unlimited/) |
| ✓ | archetype | Cunning | disruption | recipe score 1.06, 2.3x the other factions, 32 cards |  | [Control and manipulation of opponent's units](https://cardgamer.com/games/star-wars/aspects-in-star-wars-unlimited/) |

## The Elder Scrolls: Legends

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | archetype | Strength | aggro_tempo | recipe score 0.85, 2.7x the other factions, 41 cards |  | [direct attacks that clear enemies out](https://En.UESP.net/wiki/Legends:Attributes) |
| ✗ | signature | Intelligence | generate_cards | 13/165 cards (8%), 1.7x the rest, chance 0.077, rank 1 of 6 | could be chance (5%) | [conjure an Atronach](https://En.UESP.net/wiki/Legends:Attributes) |
| ✓ | signature | Intelligence | merge_attach | 20/165 cards (12%), 1.9x the rest, chance 0.011, rank 2 of 6 |  | [equipping weapons](https://En.UESP.net/wiki/Legends:Attributes) |
| ✓ | signature | Intelligence | random_effect | 29/165 cards (18%), 1.6x the rest, chance 0.014, rank 2 of 6 |  | [spells with unpredictable results](https://bethesda.net/en-AU/news/beginners-guide-to-attributes-and-classes) |
| ✓ | archetype | Intelligence | chaos | recipe score 1.02, 8.2x the other factions, 36 cards |  | [Magic and chaos](https://bethesda.net/en-AU/news/beginners-guide-to-attributes-and-classes) |
| ✗ | archetype | Intelligence | spellslinger | under 1.5x the other factions | recipe not 1.5x the other factions | [Spells](https://En.UESP.net/wiki/Legends:Attributes) |
| ✓ | signature | Willpower | summon | 24/158 cards (15%), 1.5x the rest, chance 0.043, rank 1 of 6 |  | [Amassing large armies](https://En.UESP.net/wiki/Legends:Attributes) |
| ✓ | signature | Willpower | steal | 7/158 cards (4%), 15.3x the rest, chance 0.000, rank 1 of 6 |  | [bending them to your control](https://En.UESP.net/wiki/Legends:Attributes) |
| ✓ | archetype | Willpower | swarm | recipe score 0.57, 7.0x the other factions, 33 cards |  | [going wide](https://bethesda.net/en-AU/news/beginners-guide-to-attributes-and-classes) |
| ✗ | archetype | Willpower | control | under 1.5x the other factions | recipe not 1.5x the other factions | [the greatest ability to deal with opposing threats](https://bethesda.net/en-AU/news/beginners-guide-to-attributes-and-classes) |
| ✓ | signature | Agility | deathtouch | 15/155 cards (10%), 1.5x the rest, chance 0.111, rank 2 of 6 |  | [Lethal, "poison and precision"](https://bethesda.net/en-AU/news/beginners-guide-to-attributes-and-classes) |
| ✓ | signature | Agility | movement | 11/155 cards (7%), 16.4x the rest, chance 0.000, rank 1 of 6 |  | [shift creatures from one lane to another](https://bethesda.net/en-AU/news/beginners-guide-to-attributes-and-classes) |
| ✓ | signature | Agility | immunity | 6/155 cards (4%), 3.0x the rest, chance 0.040, rank 1 of 6 |  | [cover](https://En.UESP.net/wiki/Legends:Attributes) |
| ✗ | signature | Agility | on_attack | 9/155 cards (6%), 1.6x the rest, chance 0.149, rank 2 of 6 | could be chance (5%) | [Pilfer](https://bethesda.net/en-AU/news/beginners-guide-to-attributes-and-classes) |
| ✓ | signature | Endurance | taunt | 23/162 cards (14%), 1.6x the rest, chance 0.032, rank 2 of 6 |  | [Guard](https://bethesda.net/en-AU/news/beginners-guide-to-attributes-and-classes) |
| ✗ | signature | Endurance | resource_gain | 4/162 cards (2%), 2.1x the rest, chance 0.180, rank 2 of 6 | could be chance (5%) | [increasing Magicka](https://En.UESP.net/wiki/Legends:Attributes) |
| ✓ | signature | Endurance | heal | 31/162 cards (19%), 2.4x the rest, chance 0.000, rank 1 of 6 |  | [healing actions](https://En.UESP.net/wiki/Legends:Attributes) |
| ✗ | archetype | Endurance | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [Guard creatures and sturdy defense](https://bethesda.net/en-AU/news/beginners-guide-to-attributes-and-classes) |
| ✗ | archetype | Endurance | ramp | under 1.5x the other factions | recipe not 1.5x the other factions | [cards that increase magicka supply](https://bethesda.net/en-AU/news/beginners-guide-to-attributes-and-classes) |
| ✓ | archetype | Endurance | sustain | recipe score 1.26, 9.5x the other factions, 31 cards |  | [healing for both player and creatures](https://bethesda.net/en-AU/news/beginners-guide-to-attributes-and-classes) |

## Warhammer 40,000 (10th edition)

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Xenos - Necrons | revive | 6/147 cards (4%), 3.4x the rest, chance 0.012, rank 1 of 26 |  | [Reanimation Protocols revive fallen Warriors](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | signature | Xenos - Genestealer Cults | revive | 2/74 cards (3%), 2.1x the rest, chance 0.253, rank 4 of 26 | could be chance (5%) | [units often return to play after dying](https://www.wargamer.com/warhammer-40k/factions) |
| ✓ | signature | Imperium - Adepta Sororitas | resource_banking | 40/121 cards (33%), 23.0x the rest, chance 0.000, rank 1 of 26 |  | [Miracle Dice store results for later use](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | signature | Xenos - Leagues of Votann | mark_target | 0/107 cards (0%), 0.0x the rest, chance 1.000, rank 9 of 26 | no card of the faction has it | [Eye of the Ancestors makes enemies easier to hit and wound](https://www.wargamer.com/warhammer-40k/factions) |
| ✓ | signature | Chaos - Death Guard | debuff | 23/124 cards (19%), 1.3x the rest, chance 0.116, rank 6 of 26 |  | [plague aura weakens enemies](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | signature | Chaos - Chaos Space Marines | friendly_fire | 17/204 cards (8%), 2.3x the rest, chance 0.002, rank 3 of 26 | could be chance (5%) | [Dark Pacts can disastrously backfire](https://www.wargamer.com/warhammer-40k/factions) |
| ✓ | signature | Imperium - Adeptus Mechanicus | modal_choice | 43/107 cards (40%), 6.5x the rest, chance 0.000, rank 1 of 26 |  | [reconfigurable, pick the right tool at the right moment](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | archetype | Xenos - Orks | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [relentless green tide of Boyz and Grots](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | archetype | Xenos - Tyranids | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [swarms of Termagants and Hormagaunts](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | archetype | Xenos - Necrons | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [slow but tough](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | archetype | Chaos - Death Guard | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [slow hardy plague-carriers, very durable](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | archetype | Imperium - Adeptus Custodes | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [extremely tough with top-tier defensive wargear](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | archetype | Xenos - T'au Empire | positional | under 1.5x the other factions | recipe not 1.5x the other factions | [highly mobile battlesuits project force](https://www.wargamer.com/warhammer-40k/factions) |
| ✓ | archetype | Chaos - Emperor's Children | aggro_tempo | recipe score 1.02, 1.8x the other factions, 27 cards |  | [fast aggressive melee specialists](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | archetype | Chaos - Thousand Sons | spellslinger | under 1.5x the other factions | recipe not 1.5x the other factions | [psyker-driven army, strength in psychic abilities](https://www.wargamer.com/warhammer-40k/factions) |
| ✗ | combo | Storm Speeder Thunderstrike | Eradicators |  | a card name is not in the library | [+1 to wound vs vehicles/monsters boosts Eradicators](https://www.tabletopbattles.com/10th-edition-competitive-faction-focus-space-marines) |
| ✗ | combo | Storm Speeder Thunderstrike | Hellblasters |  | a card name is not in the library | [+1 to wound vs vehicles/monsters boosts Hellblasters](https://www.tabletopbattles.com/10th-edition-competitive-faction-focus-space-marines) |
| ✓ | combo | Storm Speeder Thunderstrike | Redemptor Dreadnought | linked by keyword, relation |  | [+1 to wound vs vehicles/monsters](https://www.tabletopbattles.com/10th-edition-competitive-faction-focus-space-marines) |
| ✗ | combo | Impulsor | Hellblasters |  | a card name is not in the library | [Firing Deck lets them shoot from inside](https://www.tabletopbattles.com/10th-edition-competitive-faction-focus-space-marines) |
| ✗ | combo | Impulsor | Sternguard Veteran Squad |  | both cards there, no connection | [Firing Deck lets them shoot from inside](https://www.tabletopbattles.com/10th-edition-competitive-faction-focus-space-marines) |
| ✓ | combo | Judiciar | Bladeguard Veteran Squad | linked by keyword, link, role_tree |  | [closest the melee options come to viable](https://www.tabletopbattles.com/10th-edition-competitive-faction-focus-space-marines) |
| ✓ | combo | Ghazghkull Thraka | Meganobz | linked by link |  | [Ghaz can attach to Meganobz in Bully Boyz lists](https://www.belloflostsouls.net/2024/08/warhammer-40k-top-5-must-have-units-for-10ths-hot-armies.html) |

## Warhammer Age of Sigmar (4th edition)

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✓ | signature | Soulblight Gravelords | summon | 17/125 cards (14%), 1.9x the rest, chance 0.010, rank 2 of 33 |  | [spawning abilities, especially zombies](https://ageofminiatures.com/aos-armies/) |
| ✓ | signature | Flesh-eater Courts | revive | 11/104 cards (11%), 2.6x the rest, chance 0.005, rank 3 of 33 |  | [Carrion Retainers resurrect fallen units](https://ageofminiatures.com/aos-armies/) |
| ✗ | signature | Seraphon | summon | 2/67 cards (3%), 0.4x the rest, chance 0.965, rank 20 of 33 | not 1.5x the rest of the game | [conjuration summons extra units](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✓ | signature | Idoneth Deepkin | first_strike | 7/88 cards (8%), 1.7x the rest, chance 0.114, rank 6 of 33 |  | [tide stage lets units fight first regardless of order](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | signature | Lumineth Realm-lords | counter_spell | 2/86 cards (2%), 0.8x the rest, chance 0.746, rank 18 of 33 | not 1.5x the rest of the game | [units can dispel enemy spells](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✓ | signature | Maggotkin of Nurgle | damage_over_time | 16/97 cards (16%), 1.2x the rest, chance 0.227, rank 8 of 33 |  | [disease points deal splash mortal wounds each turn](https://ageofminiatures.com/aos-armies/) |
| ✓ | signature | Kharadron Overlords | ranged | 38/118 cards (32%), 2.3x the rest, chance 0.000, rank 2 of 33 |  | [shooting-focused airborne gunboats](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | signature | Sylvaneth | movement | 18/103 cards (17%), 1.1x the rest, chance 0.313, rank 11 of 33 | not 1.5x the rest of the game | [up to half the army in reserve, arrives mid-game](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✓ | archetype | Skaven | swarm | recipe score 0.20, 2.4x the other factions, 13 cards |  | [horde-based rat-men](https://ageofminiatures.com/aos-armies/) |
| ✗ | archetype | Disciples of Tzeentch | spellslinger | under 1.5x the other factions | recipe not 1.5x the other factions | [magic-heavy, strong hero phase](https://ageofminiatures.com/aos-armies/) |
| ✗ | archetype | Blades of Khorne | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [violent expendable blood armies, no summoning](https://ageofminiatures.com/aos-armies/) |
| ✗ | archetype | Hedonites of Slaanesh | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [very fast but fragile, hit-first charges](https://ageofminiatures.com/aos-armies/) |
| ✗ | archetype | Daughters of Khaine | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [very fast melee glass cannons](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | archetype | Maggotkin of Nurgle | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [tough, slow, hard to dislodge from objectives](https://ageofminiatures.com/aos-armies/) |
| ✗ | archetype | Nighthaunt | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [durable spectral units, Ethereal ignores save modifiers](https://ageofminiatures.com/aos-armies/) |
| ✗ | archetype | Ogor Mawtribes | sustain | under 1.5x the other factions | recipe not 1.5x the other factions | [tough units that can heal](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |
| ✗ | archetype | Beasts of Chaos | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [fast mobile brutes that charge the front line](https://www.wargamer.com/warhammer-age-of-sigmar/armies-guide) |

## Blood Bowl (Third Season)

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | signature | Chaos Renegade | damage | faction under 20 cards or not in the library | faction not in library | [big guys with lots of bashing strength](https://www.gaming.net/blood-bowl-3-all-teams-ranked/) |
| ✗ | signature | Old World Alliance | variety_payoff | faction under 20 cards or not in the library | faction not in library | [mixed roster of species offsetting each other's weaknesses](https://www.gaming.net/blood-bowl-3-all-teams-ranked/) |

## Warhammer 40,000: Kill Team

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | signature | Novitiate | resource_gain | 2/43 cards (5%), 1.5x the rest, chance 0.383, rank 13 of 45 | could be chance (5%) | [Faith Points earned and spent on Acts of Faith](https://www.warhammer-community.com/2024/09/09/kill-teams-of-the-imperium-enforce-the-emperors-will-in-the-new-edition/) |
| ✗ | signature | Novitiate | life_payment | 0/43 cards (0%), 0.0x the rest, chance 1.000, rank 6 of 45 | no card of the faction has it | [auto-chastisers hurt the wearer for an Act of Faith](https://www.warhammer-community.com/2024/09/09/kill-teams-of-the-imperium-enforce-the-emperors-will-in-the-new-edition/) |
| ✗ | signature | Kasrkin | modal_choice | 0/41 cards (0%), 0.0x the rest, chance 1.000, rank 17 of 45 | no card of the faction has it | [pick one of four Skill at Arms options each turn](https://www.warhammer-community.com/2024/09/09/kill-teams-of-the-imperium-enforce-the-emperors-will-in-the-new-edition/) |
| ✗ | signature | Inquisitorial Agents | play_restriction | 11/87 cards (13%), 1.7x the rest, chance 0.075, rank 10 of 45 | could be chance (5%) | [Absolute Authority prevents enemies using Ploys](https://www.warhammer-community.com/2024/09/09/kill-teams-of-the-imperium-enforce-the-emperors-will-in-the-new-edition/) |
| ✗ | signature | Imperial Navy Breacher | damage_types | 0/44 cards (0%), 0.0x the rest, chance 1.000, rank 13 of 45 | no card of the faction has it | [void-sealed armour resists explosive and flame weapons](https://www.warhammer-community.com/2024/09/09/kill-teams-of-the-imperium-enforce-the-emperors-will-in-the-new-edition/) |
| ✗ | archetype | Death Korps | swarm | under 1.5x the other factions | recipe not 1.5x the other factions | [large expendable force overwhelming with numbers](https://www.warhammer-community.com/2024/09/09/kill-teams-of-the-imperium-enforce-the-emperors-will-in-the-new-edition/) |
| ✗ | archetype | Exaction Squad | control | under 1.5x the other factions | recipe not 1.5x the other factions | [aggressive pursuit and suppression of targets](https://www.warhammer-community.com/2024/09/09/kill-teams-of-the-imperium-enforce-the-emperors-will-in-the-new-edition/) |
| ✗ | archetype | Imperial Navy Breacher | fortress | under 1.5x the other factions | recipe not 1.5x the other factions | [methodical close-quarters grind, shields shove enemies away](https://www.warhammer-community.com/2024/09/09/kill-teams-of-the-imperium-enforce-the-emperors-will-in-the-new-edition/) |

## Warhammer Underworlds

| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |
|---|---|---|---|---|---|---|
| ✗ | archetype | The Crimson Court | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [best for killing all your enemies](https://www.warhammer-community.com/en-gb/articles/ZvLICueF/good-all-rounders-most-killy-or-best-for-pets-a-guide-to-warhammer-underworlds-warbands/) |
| ✗ | archetype | Morgok's Krushas | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [best for killing all your enemies](https://www.warhammer-community.com/en-gb/articles/ZvLICueF/good-all-rounders-most-killy-or-best-for-pets-a-guide-to-warhammer-underworlds-warbands/) |
| ✗ | archetype | Khagra's Ravagers | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [best for killing all your enemies](https://www.warhammer-community.com/en-gb/articles/ZvLICueF/good-all-rounders-most-killy-or-best-for-pets-a-guide-to-warhammer-underworlds-warbands/) |
| ✓ | archetype | Morgwaeth's Blade-coven | aggro_tempo | recipe score 0.83, 1.6x the other factions, 6 cards |  | [best for killing all your enemies](https://www.warhammer-community.com/en-gb/articles/ZvLICueF/good-all-rounders-most-killy-or-best-for-pets-a-guide-to-warhammer-underworlds-warbands/) |
| ✗ | archetype | Ironsoul's Condemners | aggro_tempo | under 1.5x the other factions | recipe not 1.5x the other factions | [best for killing all your enemies](https://www.warhammer-community.com/en-gb/articles/ZvLICueF/good-all-rounders-most-killy-or-best-for-pets-a-guide-to-warhammer-underworlds-warbands/) |
| ✗ | archetype | Hedkrakka's Madmob | spellslinger | under 1.5x the other factions | recipe not 1.5x the other factions | [best for unleashing magic](https://www.warhammer-community.com/en-gb/articles/ZvLICueF/good-all-rounders-most-killy-or-best-for-pets-a-guide-to-warhammer-underworlds-warbands/) |
| ✗ | archetype | The Wurmspat | spellslinger | under 1.5x the other factions | recipe not 1.5x the other factions | [best for unleashing magic](https://www.warhammer-community.com/en-gb/articles/ZvLICueF/good-all-rounders-most-killy-or-best-for-pets-a-guide-to-warhammer-underworlds-warbands/) |
| ✗ | archetype | The Starblood Stalkers | spellslinger | under 1.5x the other factions | recipe not 1.5x the other factions | [best for unleashing magic](https://www.warhammer-community.com/en-gb/articles/ZvLICueF/good-all-rounders-most-killy-or-best-for-pets-a-guide-to-warhammer-underworlds-warbands/) |
| ✗ | archetype | Myari's Purifiers | spellslinger | under 1.5x the other factions | recipe not 1.5x the other factions | [best for unleashing magic](https://www.warhammer-community.com/en-gb/articles/ZvLICueF/good-all-rounders-most-killy-or-best-for-pets-a-guide-to-warhammer-underworlds-warbands/) |
| ✗ | archetype | Lady Harrow's Mournflight | objectives | under 1.5x the other factions | recipe not 1.5x the other factions | [fights well and claims objective tokens](https://www.warhammer-community.com/en-gb/articles/ZvLICueF/good-all-rounders-most-killy-or-best-for-pets-a-guide-to-warhammer-underworlds-warbands/) |
