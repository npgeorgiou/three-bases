# Case tests: sts1

Made by `cases/run.py sts1`.
**38 of 38 cases pass.**


## Mechanics (expected cards from the texts)

| case | question | expected | found | recall | extra | pass |
|---|---|---|---|---|---|---|
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

## Combos (the enabler must set off the payoff)

| case | enabler | payoff | why | found as | pass |
|---|---|---|---|---|---|

## Region identity (signature, splash, archetype)

| case | region | kind | mechanic | need | found | pass |
|---|---|---|---|---|---|---|

## Guide decks (the explanation must say what the guide says)

| case | deck | must say | missing | pass |
|---|---|---|---|---|

## Deck networks (a line must be there, or must not)

| case | deck | from | to | expect | found | pass |
|---|---|---|---|---|---|---|
| nst01 | Ironclad Pain (gamersdecide) | Reaper | Flex | none  | - | yes |
| nst02 | Ironclad Pain (gamersdecide) | Flex | Reaper | line bigger | stronger: makes its effect bigger | yes |
| nst03 | Silent Shiv (gamersdecide) | Shiv | Accuracy | none  | - | yes |
| nst04 | Silent Poison (gamersdecide) | Burst | Catalyst | line plays it again | stronger: plays it again | yes |
| nst05 | Silent Poison (gamersdecide) | Catalyst | Burst | none  | - | yes |
| nst06 | Ironclad Body Slam (highgroundgaming) | Shrug It Off | Ghostly Armor | none  | - | yes |
| nst07 | Silent Discard (gamersdecide) | Reflex | Gambling Chip | none  | - | yes |
| nst08 | Defect Claw (fantasywarden) | Machine Learning | Void | none  | - | yes |
| nst09 | Defect Claw (fantasywarden) | Hologram | FTL | none  | - | yes |
| nst10 | Ironclad Pain (gamersdecide) | Flame Barrier | Rupture | none  | - | yes |
| nst11 | Watcher Stance Change (highgroundgaming) | Bottled Flame | Kunai | none  | - | yes |
| nst12 | Watcher Conjure Blade (slaythespire.info) | Chemical X | Miracle | none  | - | yes |
| nst13 | Watcher Conjure Blade (slaythespire.info) | Chemical X | Conjure Blade | line bigger | stronger: makes its effect bigger | yes |
| nst14 | Defect Claw (fantasywarden) | All for One | Reinforced Body | none  | - | yes |
| nst15 | Ironclad Strength (gamersdecide) | Heavy Blade | Flex | none  | - | yes |
| nst16 | Ironclad Exhaust (gamersdecide) | Barricade | Body Slam | line keeps your Block | stronger: keeps your Block: it counts more of it | yes |
| nst17 | Defect Orb (gamersdecide) | Electrodynamics | Tempest | line Lightning | stronger: makes the Lightning it gives stronger | yes |
| nst18 | Watcher Stance Change (highgroundgaming) | Crescendo | Mental Fortress | line Wrath | waits: gives you Wrath | yes |
| nst19 | Silent Shiv (highgroundgaming) | Blade Dance | After Image | none  | - | yes |
| nst20 | Silent Poison (highgroundgaming) | Strike (Silent) | Corpse Explosion | none  | - | yes |
| nst21 | Ironclad Barricade (Steam, Jeff) | Shrug It Off | Barricade | none  | - | yes |
| nst22 | Ironclad Barricade (Steam, Jeff) | Barricade | Shrug It Off | line keeps the Block | stronger: keeps the Block it gives | yes |
| nst23 | Ironclad Strength (gamersdecide) | Bag of Marbles | Reaper | line Vulnerable | stronger: gives Vulnerable: its damage is bigger | yes |
| nst24 | Silent Discard (gamersdecide) | Gambling Chip | Eviscerate | line cheaper: | cheaper: makes you discard cards | yes |
| nst25 | Ironclad Strength (gamersdecide) | Flex | Heavy Blade | line gives you Strength | type: gives you Strength; also makes stronger: makes its effect bigger | yes |
