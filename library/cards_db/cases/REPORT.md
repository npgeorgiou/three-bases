# Case tests: into_the_breach

Made by `cases/run.py into_the_breach`.
**30 of 30 cases pass.**


## Mechanics (expected cards from the texts)

| case | question | expected | found | recall | extra | pass |
|---|---|---|---|---|---|---|
| mx01 | a trigger on another unit dying is other_death_trigger | 0 | 0 | 100% | 4 | yes |
| mx02 | moving enemy units is forced_movement | 0 | 0 | 100% | 80 | yes |
| mx03 | a plain draw is one form: zone deck_top, no pick top | 0 | 0 | 100% | 0 | yes |
| mx10 | damage to the enemy player is Nexus damage (kinds kept, v30) | 0 | 0 | 100% | 12 | yes |
| mx11 | moving or pushing units makes units move (positions change, v30) | 2 | 2 | 100% | 118 | yes |
| mx12 | a unit that moves (onto a space) is the event's object, never its actor (N16, Sentry, v36, v38) | 0 | 0 | 100% | 22 | yes |
| mx13 | can't be targeted by spells: the cant is on the spells, the protected unit is "to" (N19, v37) | 0 | 0 | 100% | 0 | yes |
| mx14 | a dead unit put into play is revive, never summon from the discard (N20, v37) | 0 | 0 | 100% | 0 | yes |
| mx15 | a trigger that holds only "this turn" is an ability given to the player for this turn (v37, Duelyst) | 0 | 0 | 100% | 0 | yes |
| mx13 | an effect on the creature opposing it is about lanes (concept lanes from same_lane, v38) | 0 | 0 | 100% | 17 | yes |
| mx14 | a strike on the spaces beside the opposing one reaches other lanes (cross_lane, v38) | 0 | 0 | 100% | 0 | yes |
| mx15 | within a circuit is a formation (link_formation, v38) | 0 | 0 | 100% | 0 | yes |
| mx16 | more or faster base resource (base_resource_gain, v38) | 0 | 0 | 100% | 1 | yes |
| mtb1 | Flying units stop on no mountain and no enemy unit (they fly over them) | 9 | 9 | 100% | 19 | yes |
| mtb2 | hits the tile in front and its two sides (Burrowers) | 2 | 2 | 100% | 0 | yes |
| mtb3 | an upgrade that makes the area hit bigger | 1 | 1 | 100% | 0 | yes |

## Combos (the enabler must set off the payoff)

| case | enabler | payoff | why | found as | pass |
|---|---|---|---|---|---|

## Region identity (signature, splash, archetype)

| case | region | kind | mechanic | need | found | pass |
|---|---|---|---|---|---|---|

## Guide decks (the explanation must say what the guide says)

| case | deck | must say | missing | pass |
|---|---|---|---|---|
| dtb01 | Rusting Hulks | Enemy units get Smoke: made by Aerial Bombs | - | yes |

## Deck networks (a line must be there, or must not)

| case | deck | from | to | expect | found | pass |
|---|---|---|---|---|---|---|
| ntb1 | Blitzkrieg | Electric Whip | Rock Accelerator | none  | - | yes |
| ntb2 | Teleporter, Flame Shielding | Teleporter | Flame Shielding | none  | - | yes |
| ntb3 | Hazardous Mechs | Viscera Nanobots | Hydraulic Legs | line heals the mech with Hydraulic Legs when it kills | heals: Viscera Nanobots heals the mech with Hydraulic Legs when it kills | yes |
| ntb4 | Steel Judoka | Vice Fist | Vek Hormones | none damages enemy units | - | yes |
| ntb6 | Spartan Shield, Vek Hormones | Spartan Shield | Vek Hormones | line damages enemy units | waits: damages enemy units or players | yes |
| ntb5 | Mist Eaters | Reverse Thrusters | Nanofilter Mending | line Smoke | type: makes your units get Smoke | yes |
| ntb7 | Rusting Hulks | Repulse | Jet Mech | line gives it Energy Shield | keyword: gives it Energy Shield (when next to it) | yes |
| ntb8 | Run: Rusting Hulks (Sevastromo, Unfair) | Rocket Artillery | Force Amp | line bump damage | waits: Rocket Artillery pushes enemy units into things (bump damage) | yes |
| ntb9 | Run: Rusting Hulks (Sevastromo, Unfair) | Aerial Bombs | Force Amp | none  | - | yes |
| ntb10 | Run: Rift Walkers (Sevastromo, Unfair) | Titan Fist | Artemis Artillery | line acts on units | type: Titan Fist moves units, and Artemis Artillery acts on units in a line from | yes |
| ntb11 | Rift Walkers | Combat Mech | Titan Fist | line carries | carries: Combat Mech carries Titan Fist | yes |
| ntb12 | Claude: Steel Judoka with second weapons | Confuse Shot | Vek Hormones | line damages enemy units | waits: damages enemy units or players | yes |
| ntb13 | Claude: Mist Eaters with second weapons | Smoke Pellets | Smog Mech | line keeps Smoke off it | rules: keeps Smoke off it | yes |
