# Case tests: stormbound

Made by `cases/run.py stormbound`.
**114 of 122 cases pass.**


## Mechanics (expected cards from the texts)

| case | question | expected | found | recall | extra | pass |
|---|---|---|---|---|---|---|
| sb01 | on play triggers | 91 | 91 | 100% | 38 | yes |
| sb02 | on death triggers | 19 | 19 | 100% | 0 | yes |
| sb03 | before / when attacking triggers | 22 | 22 | 100% | 0 | yes |
| sb04 | after attacking triggers | 6 | 6 | 100% | 0 | yes |
| sb05 | after surviving damage triggers | 17 | 17 | 100% | 0 | yes |
| sb06 | before moving triggers | 23 | 23 | 100% | 7 | yes |
| sb07 | start of your turn triggers | 25 | 25 | 100% | 11 | yes |
| sb08 | end of your turn triggers | 1 | 1 | 100% | 0 | yes |
| sb09 | poisons | 6 | 6 | 100% | 0 | yes |
| sb10 | cares about poisoned units | 5 | 5 | 100% | 0 | yes |
| sb11 | vitalizes | 7 | 7 | 100% | 0 | yes |
| sb12 | freezes | 8 | 8 | 100% | 0 | yes |
| sb13 | cares about frozen units | 4 | 4 | 100% | 0 | yes |
| sb14 | confuses | 8 | 8 | 100% | 0 | yes |
| sb15 | cares about confused units | 3 | 3 | 100% | 0 | yes |
| sb16 | disables abilities | 2 | 2 | 100% | 0 | yes |
| sb17 | spawns or builds | 36 | 35 | 97% | 3 | yes |
| sb18 | destroys | 16 | 16 | 100% | 1 | yes |
| sb19 | converts enemies | 5 | 5 | 100% | 0 | yes |
| sb20 | drains strength | 7 | 7 | 100% | 67 | yes |
| sb21 | pushes | 5 | 5 | 100% | 26 | yes |
| sb22 | pulls | 3 | 3 | 100% | 28 | yes |
| sb23 | commands forward | 3 | 3 | 100% | 28 | yes |
| sb24 | teleports, jumps or flies | 10 | 10 | 100% | 21 | yes |
| sb25 | forces attacks | 4 | 4 | 100% | 0 | yes |
| sb26 | damages the enemy base | 6 | 6 | 100% | 16 | yes |
| sb27 | damages its own base | 4 | 4 | 100% | 0 | yes |
| sb28 | gains mana | 6 | 6 | 100% | 1 | yes |
| sb29 | spends mana | 1 | 1 | 100% | 0 | yes |
| sb30 | draws cards | 4 | 4 | 100% | 3 | yes |
| sb31 | discards | 3 | 3 | 100% | 0 | yes |
| sb32 | replaces a card in hand | 2 | 2 | 100% | 0 | yes |
| sb33 | gives or gains strength | 51 | 51 | 100% | 18 | yes |
| sb34 | gives speed or movement | 7 | 7 | 100% | 30 | yes |
| sb35 | sets strength to a value | 2 | 2 | 100% | 6 | yes |
| sb36 | restores strength | 0 | 0 | 100% | 1 | yes |
| sb37 | deals damage | 59 | 59 | 100% | 15 | yes |
| sb38 | damages all bordering or surrounding | 0 | 0 | 100% | 20 | yes |
| sb39 | cares about structures | 28 | 27 | 96% | 21 | yes |
| sb40 | cares about a unit type | 44 | 44 | 100% | 22 | yes |
| sb41 | cares about ancients | 5 | 4 | 80% | 26 | NO |
| sb42 | bordering positions | 45 | 45 | 100% | 0 | yes |
| sb43 | surrounding positions | 49 | 48 | 98% | 0 | yes |
| sb44 | in front positions | 28 | 27 | 96% | 3 | yes |
| sb45 | behind positions | 8 | 8 | 100% | 0 | yes |
| sb46 | row or column positions | 6 | 5 | 83% | 0 | NO |
| sb47 | next to a base | 9 | 9 | 100% | 1 | yes |
| sb48 | compares strength (stronger / weaker) | 9 | 9 | 100% | 9 | yes |
| sb49 | picks the strongest or weakest | 11 | 11 | 100% | 1 | yes |
| sb50 | X or less strength targets | 13 | 13 | 100% | 3 | yes |
| sb51 | copies cards | 5 | 5 | 100% | 1 | yes |
| sb52 | creates a card in the deck | 3 | 3 | 100% | 3 | yes |
| sb53 | plays cards for free | 2 | 2 | 100% | 1 | yes |
| sb54 | triggers structures again | 2 | 2 | 100% | 1 | yes |
| sb55 | respawns | 3 | 3 | 100% | 0 | yes |
| sb56 | moves forward | 3 | 3 | 100% | 110 | yes |
| sb57 | cards in hand matter | 11 | 10 | 91% | 1 | NO |
| sb58 | random targets | 67 | 66 | 99% | 9 | yes |
| sb59 | spreads an amount among targets | 5 | 5 | 100% | 1 | yes |
| sb60 | benefits from units dying, any way | 21 | 20 | 95% | 1 | yes |
| sb61 | benefits from taking damage, any way | 17 | 17 | 100% | 0 | yes |
| sb62 | benefits from poison, any way | 5 | 5 | 100% | 19 | yes |

Missed cards (first 8 per failing case):

- sb41 cares about ancients: Orgone Leechers
- sb46 row or column positions: Temple of Life
- sb57 cards in hand matter: Clap of Thunder

## Combos (the enabler must set off the payoff)

| case | enabler | payoff | why | found as | pass |
|---|---|---|---|---|---|
| csb01 | Frosthexers | Wisp Cloud | freezing enemies sets up damage to frozen enemies | state: given_keyword | yes |
| csb02 | Glacier Palace | Wisp Cloud | freezes an enemy each turn for Wisp Cloud | state: given_keyword | yes |
| csb03 | Frosthexers | Icicle Burst | an already frozen target takes damage instead | state: given_keyword | yes |
| csb04 | Frosthexers | Midwinter Chaos | already frozen enemies are destroyed | state: given_keyword | yes |
| csb05 | Icicle Burst | Spellbinder Zhevana | frozen units in front are destroyed for mana | condition: damage -> killed | yes |
| csb06 | Moment’s Peace | Midwinter Chaos | frozen enemies are destroyed | state: given_keyword | yes |
| csb07 | Blizzard Bombs | Wisp Cloud | freezes surrounding units for Wisp Cloud | state: given_keyword | yes |
| csb08 | Copperskin Ranger | Marked as Prey | needs a poisoned target | state: given_keyword | yes |
| csb09 | Venomfall Spire | Amberhides | drains a poisoned unit | state: given_keyword | yes |
| csb10 | Copperskin Ranger | Brood Sages | spawns Toads per surrounding poisoned unit | state: given_keyword | yes |
| csb11 | Toxic Sacrifice | Plague Monarchs | ancients drain poisoned enemies | state: given_keyword | yes |
| csb12 | Heliotroopers | Soap Cleanse | restores and vitalizes friendly poisoned units | keyword: Poison | yes |
| csb13 | Crimson Sentry | Amberhides | poisons units that Amberhides drains | state: given_keyword | yes |
| csb14 | Sweetcap Kittens | Hair-Raising Cats | forces a confused enemy to attack | state: given_keyword | yes |
| csb15 | Fluffy Badboxers | Melodious Sisters | damage when attacking a confused unit | state: given_keyword | yes |
| csb16 | Slyboots | Temple of the Mind | destroys the weakest confused unit | state: given_keyword | yes |
| csb17 | Sweetcap Kittens | Melodious Sisters | confused targets | state: given_keyword | yes |
| csb18 | Doppelbocks | Swarmcallers | gains strength per bordering Satyr | type: Satyr | yes |
| csb19 | Dreadfauns | Moonlit Aerie | gives strength to friendly Satyrs | target: type Satyr | yes |
| csb20 | Shady Ghoul | Faun Companions | gives strength to a bordering Satyr | target: type Satyr | yes |
| csb21 | Head Start | Swarmcallers | Satyr on the board | type: Satyr | yes |
| csb22 | Ludic Matriarchs | Dangerous Suitors | gains per Dragon on the board | type: Dragon | yes |
| csb23 | Draconic Roamers | Sunbeam Serpents | gains the strongest friendly Dragon’s strength | type: Dragon | yes |
| csb24 | Ludic Matriarchs | Dreadful Keepers | spawns a Dragon bordering a friendly Dragon | - | NO |
| csb25 | Draconic Roamers | Wandering Wyrms | played bordering a friendly Dragon | type: Dragon | yes |
| csb26 | Broodmother Qordia | Spare Dragonling | gives strength to a friendly Dragon | target: type Dragon | yes |
| csb27 | Mech Workshop | Upgrade Point | strength to surrounding Constructs | target: type Construct | yes |
| csb28 | Finite Loopers | Linked Golems | played bordering a Construct | type: Construct | yes |
| csb29 | Mechanical Workers | Upgrade Point | Constructs from the workshop | target: type Construct | yes |
| csb30 | Rockworkers | Fortification Tonic | units surrounding a friendly structure | - | NO |
| csb31 | Rockworkers | Hearthguards | played bordering a friendly structure | count: landmark | yes |
| csb32 | Mech Workshop | Doctor Mia | triggers bordering friendly structures | target: structure | yes |
| csb33 | Frozen Core | Lady Rime | spends the remaining mana for strength | count: mana | yes |
| csb34 | Rimelings | Visions of the Grove | damage for remaining mana | count: mana | yes |
| csb35 | Gift of the Wise | Lady Rime | remaining mana | count: mana | yes |
| csb36 | Dawnsparks | Visions of the Grove | remaining mana | count: mana | yes |
| csb37 | Martyr Spongers | Orgone Leechers | other friendly ancients lower its mana cost | - | NO |
| csb38 | Absorbing Varmints | Plague Monarchs | friendly ancients act | target: type Ancient | yes |
| csb39 | Summon Militia | Kindred’s Grace | strength to all others of the same unit type | - | NO |
| csb40 | Rain of Frogs | Excited Mousers | confuses as many enemies as friendly units | count: unit | yes |
| csb41 | Brothers in Arms | Kindred’s Grace | same unit type | - | NO |
| csb42 | Frosthexers | Spellbinder Zhevana | frozen units destroyed for mana | state: given_keyword | yes |

## Region identity (signature, splash, archetype)

| case | region | kind | mechanic | need | found | pass |
|---|---|---|---|---|---|---|
| rsb01 | Winter | signature (library) | Freeze | 8 | 10 | yes |
| rsb02 | Winter | signature (library) | extra mana | 5 | 8 | yes |
| rsb03 | Winter | signature (library) | heavy area damage | 4 | 6 | yes |
| rsb04 | Winter | archetype (library) | ramp: extra mana for big units | 5 | 8 | yes |
| rsb05 | Swarm | signature (library) | unit generation | 5 | 9 | yes |
| rsb06 | Swarm | signature (library) | Satyrs (tribal) | 6 | 12 | yes |
| rsb07 | Swarm | signature (library) | direct damage to the enemy base | 3 | 5 | yes |
| rsb08 | Swarm | signature (library) | high movement | 4 | 6 | yes |
| rsb09 | Swarm | signature (library) | strengthening units on the board | 4 | 6 | yes |
| rsb10 | Swarm | signature (library) | self-damage costs | 2 | 3 | yes |
| rsb11 | Shadowfen | signature (library) | poison | 8 | 11 | yes |
| rsb12 | Shadowfen | signature (library) | Toads | 3 | 7 | yes |
| rsb13 | Shadowfen | archetype (library) | flooding the board | 5 | 7 | yes |
| rsb14 | Shadowfen | archetype (Claude) | converting enemies | 3 | 5 | yes |
| rsb15 | Shadowfen | archetype (Claude) | draining strength | 4 | 7 | yes |
| rsb16 | Ironclad | signature (library) | knockback (push, pull) | 5 | 6 | yes |
| rsb17 | Ironclad | signature (library) | buffs (Boosting Elixir) | 4 | 8 | yes |
| rsb18 | Ironclad | archetype (Claude) | Constructs and structures | 4 | 9 | yes |
