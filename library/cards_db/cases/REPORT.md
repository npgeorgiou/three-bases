<<<<<<< Updated upstream
# Case tests: sts1

Made by `cases/run.py sts1`.
**13 of 13 cases pass.**
=======
# Case tests: stormbound

Made by `cases/run.py stormbound`.
**141 of 145 cases pass.**
>>>>>>> Stashed changes


## Mechanics (expected cards from the texts)

| case | question | expected | found | recall | extra | pass |
|---|---|---|---|---|---|---|
<<<<<<< Updated upstream
| mx01 | a trigger on another unit dying is other_death_trigger | 2 | 2 | 100% | 1 | yes |
| mx02 | moving enemy units is forced_movement | 0 | 0 | 100% | 59 | yes |
| mx03 | a plain draw is one form: zone deck_top, no pick top | 65 | 65 | 100% | 5 | yes |
| mx10 | damage to the enemy player is Nexus damage (kinds kept, v30) | 0 | 0 | 100% | 86 | yes |
| mx11 | moving or pushing units makes units move (positions change, v30) | 0 | 0 | 100% | 59 | yes |
| mx12 | a unit that moves (onto a space) is the event's object, never its actor (N16, Sentry, v36, v38) | 0 | 0 | 100% | 0 | yes |
| mx13 | can't be targeted by spells: the cant is on the spells, the protected unit is "to" (N19, v37) | 0 | 0 | 100% | 0 | yes |
| mx14 | a dead unit put into play is revive, never summon from the discard (N20, v37) | 0 | 0 | 100% | 0 | yes |
| mx15 | a trigger that holds only "this turn" is an ability given to the player for this turn (v37, Duelyst) | 4 | 4 | 100% | 8 | yes |
| mx13 | an effect on the creature opposing it is about lanes (concept lanes from same_lane, v38) | 0 | 0 | 100% | 0 | yes |
| mx14 | a strike on the spaces beside the opposing one reaches other lanes (cross_lane, v38) | 0 | 0 | 100% | 0 | yes |
| mx15 | within a circuit is a formation (link_formation, v38) | 0 | 0 | 100% | 0 | yes |
| mx16 | more or faster base resource (base_resource_gain, v38) | 0 | 0 | 100% | 67 | yes |
=======
| sb01 | on play triggers | 91 | 91 | 100% | 38 | yes |
| sb02 | on death triggers | 19 | 19 | 100% | 0 | yes |
| sb03 | before / when attacking triggers | 22 | 22 | 100% | 0 | yes |
| sb04 | after attacking triggers | 6 | 6 | 100% | 0 | yes |
| sb05 | after surviving damage triggers | 17 | 17 | 100% | 0 | yes |
| sb06 | before moving triggers | 23 | 23 | 100% | 7 | yes |
| sb07 | start of your turn triggers | 25 | 25 | 100% | 12 | yes |
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
| sb19 | converts enemies | 4 | 4 | 100% | 0 | yes |
| sb20 | drains strength | 7 | 7 | 100% | 67 | yes |
| sb21 | pushes | 5 | 5 | 100% | 26 | yes |
| sb22 | pulls | 3 | 3 | 100% | 28 | yes |
| sb23 | commands forward | 3 | 3 | 100% | 28 | yes |
| sb24 | teleports, jumps or flies | 10 | 10 | 100% | 21 | yes |
| sb25 | forces attacks | 4 | 4 | 100% | 0 | yes |
| sb26 | damages the enemy base | 6 | 6 | 100% | 17 | yes |
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
| sb40 | cares about a unit type | 44 | 44 | 100% | 23 | yes |
| sb41 | cares about ancients | 5 | 5 | 100% | 28 | yes |
| sb42 | bordering positions | 45 | 45 | 100% | 0 | yes |
| sb43 | surrounding positions | 49 | 49 | 100% | 0 | yes |
| sb44 | in front positions | 28 | 28 | 100% | 3 | yes |
| sb45 | behind positions | 8 | 8 | 100% | 1 | yes |
| sb46 | row or column positions | 6 | 6 | 100% | 0 | yes |
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
| sb57 | cards in hand matter | 11 | 11 | 100% | 1 | yes |
| sb58 | random targets | 67 | 65 | 97% | 9 | yes |
| sb59 | spreads an amount among targets | 5 | 5 | 100% | 1 | yes |
| sb60 | benefits from units dying, any way | 21 | 21 | 100% | 1 | yes |
| sb61 | benefits from taking damage, any way | 17 | 17 | 100% | 0 | yes |
| sb62 | benefits from poison, any way | 5 | 5 | 100% | 19 | yes |
| sb63 | gives its own unit to the opponent | 1 | 1 | 100% | 0 | yes |
| mx01 | a trigger on another unit dying is other_death_trigger | 0 | 0 | 100% | 0 | yes |
| mx02 | moving enemy units is forced_movement | 5 | 5 | 100% | 23 | yes |
| mx03 | a plain draw is one form: zone deck_top, no pick top | 3 | 3 | 100% | 2 | yes |
| mx10 | damage to the enemy player is Nexus damage (kinds kept, v30) | 3 | 3 | 100% | 225 | yes |
| mx11 | moving or pushing units makes units move (positions change, v30) | 6 | 6 | 100% | 25 | yes |
| mx12 | a unit that moves (onto a space) is the event's object, never its actor (N16, Sentry, v36, v38) | 0 | 0 | 100% | 30 | yes |
| mx13 | can't be targeted by spells: the cant is on the spells, the protected unit is "to" (N19, v37) | 0 | 0 | 100% | 0 | yes |
| mx14 | a dead unit put into play is revive, never summon from the discard (N20, v37) | 0 | 0 | 100% | 3 | yes |
| mx15 | a trigger that holds only "this turn" is an ability given to the player for this turn (v37, Duelyst) | 0 | 0 | 100% | 0 | yes |
| mx13 | an effect on the creature opposing it is about lanes (concept lanes from same_lane, v38) | 0 | 0 | 100% | 24 | yes |
| mx14 | a strike on the spaces beside the opposing one reaches other lanes (cross_lane, v38) | 0 | 0 | 100% | 0 | yes |
| mx15 | within a circuit is a formation (link_formation, v38) | 0 | 0 | 100% | 0 | yes |
| mx16 | more or faster base resource (base_resource_gain, v38) | 0 | 0 | 100% | 7 | yes |
>>>>>>> Stashed changes

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
| csb08 | Copperskin Ranger | Marked as Prey | needs a poisoned target | condition: damage -> dies | yes |
| csb09 | Venomfall Spire | Amberhides | drains a poisoned unit | - | NO |
| csb10 | Copperskin Ranger | Brood Sages | spawns Toads per surrounding poisoned unit | - | NO |
| csb11 | Toxic Sacrifice | Plague Monarchs | ancients drain poisoned enemies | - | NO |
| csb12 | Heliotroopers | Soap Cleanse | restores and vitalizes friendly poisoned units | keyword: Poison | yes |
| csb13 | Crimson Sentry | Amberhides | poisons units that Amberhides drains | - | NO |
| csb14 | Sweetcap Kittens | Hair-Raising Cats | forces a confused enemy to attack | state: given_keyword | yes |
| csb15 | Fluffy Badboxers | Melodious Sisters | damage when attacking a confused unit | state: given_keyword | yes |
| csb16 | Slyboots | Temple of the Mind | destroys the weakest confused unit | state: given_keyword | yes |
| csb17 | Sweetcap Kittens | Melodious Sisters | confused targets | state: given_keyword | yes |
| csb18 | Doppelbocks | Swarmcallers | gains strength per bordering Satyr | type: Satyr | yes |
| csb19 | Dreadfauns | Moonlit Aerie | gives strength to friendly Satyrs | target: my units | yes |
| csb20 | Shady Ghoul | Faun Companions | gives strength to a bordering Satyr | target: type Satyr | yes |
| csb21 | Head Start | Swarmcallers | Satyr on the board | type: Satyr | yes |
| csb22 | Ludic Matriarchs | Dangerous Suitors | gains per Dragon on the board | type: Dragon | yes |
| csb23 | Draconic Roamers | Sunbeam Serpents | gains the strongest friendly Dragon’s strength | type: Dragon | yes |
| csb24 | Ludic Matriarchs | Dreadful Keepers | spawns a Dragon bordering a friendly Dragon | target: type Dragon | yes |
| csb25 | Draconic Roamers | Wandering Wyrms | played bordering a friendly Dragon | type: Dragon | yes |
| csb26 | Broodmother Qordia | Spare Dragonling | gives strength to a friendly Dragon | target: type Dragon | yes |
| csb27 | Mech Workshop | Upgrade Point | strength to surrounding Constructs | target: my units | yes |
| csb28 | Finite Loopers | Linked Golems | played bordering a Construct | type: Construct | yes |
| csb29 | Mechanical Workers | Upgrade Point | Constructs from the workshop | target: my units | yes |
| csb30 | Rockworkers | Fortification Tonic | units surrounding a friendly structure | target: my units | yes |
| csb31 | Rockworkers | Hearthguards | played bordering a friendly structure | count: landmark | yes |
| csb32 | Mech Workshop | Doctor Mia | triggers bordering friendly structures | target: structure | yes |
| csb33 | Frozen Core | Lady Rime | spends the remaining mana for strength | condition: mana_refilled | yes |
| csb34 | Rimelings | Visions of the Grove | damage for remaining mana | condition: mana_refilled | yes |
| csb35 | Gift of the Wise | Lady Rime | remaining mana | condition: mana_refilled | yes |
| csb36 | Dawnsparks | Visions of the Grove | remaining mana | condition: mana_refilled | yes |
| csb37 | Martyr Spongers | Orgone Leechers | other friendly ancients lower its mana cost | type: Ancient | yes |
| csb38 | Absorbing Varmints | Plague Monarchs | friendly ancients act | state: moves | yes |
| csb40 | Rain of Frogs | Excited Mousers | confuses as many enemies as friendly units | count: unit | yes |
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
| rsb07 | Swarm | signature (library) | direct damage to the enemy base | 3 | 6 | yes |
| rsb08 | Swarm | signature (library) | high movement | 4 | 6 | yes |
| rsb09 | Swarm | signature (library) | strengthening units on the board | 4 | 6 | yes |
| rsb10 | Swarm | signature (library) | self-damage costs | 2 | 3 | yes |
| rsb11 | Shadowfen | signature (library) | poison | 8 | 11 | yes |
| rsb12 | Shadowfen | signature (library) | Toads | 3 | 7 | yes |
| rsb13 | Shadowfen | archetype (library) | flooding the board | 5 | 7 | yes |
| rsb14 | Shadowfen | archetype (Claude) | converting enemies | 3 | 4 | yes |
| rsb15 | Shadowfen | archetype (Claude) | draining strength | 4 | 7 | yes |
| rsb16 | Ironclad | signature (library) | knockback (push, pull) | 5 | 7 | yes |
| rsb17 | Ironclad | signature (library) | buffs (Boosting Elixir) | 4 | 8 | yes |
| rsb18 | Ironclad | archetype (Claude) | Constructs and structures | 4 | 9 | yes |

## Guide decks (the explanation must say what the guide says)

| case | deck | must say | missing | pass |
|---|---|---|---|---|

## Deck networks (a line must be there, or must not)

| case | deck | from | to | expect | found | pass |
|---|---|---|---|---|---|---|
| n17 | Royal Reactant | Doctor Mia | Emerald Towers | line  | repeats: repeats its effects | yes |
| n18 | Royal Reactant | Emerald Towers | Fortification Tonic | line  | type: is a landmark or structure it asks for | yes |
| n19 | Extreme Speed | Reckless Rushers | Green Prototypes | none  | - | yes |
| n20 | Extreme Speed | Reckless Rushers | Restless Goats | none  | - | yes |
| n21 | Extreme Speed | Restless Goats | Green Prototypes | none  | - | yes |
| n22 | Nu Bad Medicine | Ozone Purifiers | Wild Saberpaws | line  | type: makes units move | yes |
| n23 | Nu Bad Medicine | Windmakers | Booming Professors | line  | type: makes enemy units move | yes |
| n24 | Nu Bad Medicine | * | Unhealthy Hysteria | line  | type: makes enemy units move | yes |
| n25 | Nu Bad Medicine | Ozone Purifiers | Chaotic Pupil | line  | type: makes enemy units move | yes |
| n63 | IC pirate | First Mutineer | Northsea Dogs | line  | waits: empties your hand | yes |
| n64 | Chronobreak | Heliotroopers | Sunbeam Serpents | none  | - | yes |
