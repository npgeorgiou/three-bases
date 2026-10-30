# Case tests: into_the_breach

Made by `cases/run.py into_the_breach`.
**19 of 19 cases pass.**


## Mechanics (expected cards from the texts)

| case | question | expected | found | recall | extra | pass |
|---|---|---|---|---|---|---|
| mx01 | a trigger on another unit dying is other_death_trigger | 0 | 0 | 100% | 4 | yes |
| mx02 | moving enemy units is forced_movement | 0 | 0 | 100% | 113 | yes |
| mx03 | a plain draw is one form: zone deck_top, no pick top | 0 | 0 | 100% | 0 | yes |
| mx10 | damage to the enemy player is Nexus damage (kinds kept, v30) | 0 | 0 | 100% | 16 | yes |
| mx11 | moving or pushing units makes units move (positions change, v30) | 2 | 2 | 100% | 145 | yes |
| mx12 | a unit that moves (onto a space) is the event's object, never its actor (N16, Sentry, v36, v38) | 0 | 0 | 100% | 27 | yes |
| mx13 | can't be targeted by spells: the cant is on the spells, the protected unit is "to" (N19, v37) | 0 | 0 | 100% | 0 | yes |
| mx14 | a dead unit put into play is revive, never summon from the discard (N20, v37) | 0 | 0 | 100% | 0 | yes |
| mx15 | a trigger that holds only "this turn" is an ability given to the player for this turn (v37, Duelyst) | 0 | 0 | 100% | 0 | yes |
| mx13 | an effect on the creature opposing it is about lanes (concept lanes from same_lane, v38) | 0 | 0 | 100% | 22 | yes |
| mx14 | a strike on the spaces beside the opposing one reaches other lanes (cross_lane, v38) | 0 | 0 | 100% | 0 | yes |
| mx15 | within a circuit is a formation (link_formation, v38) | 0 | 0 | 100% | 0 | yes |
| mx16 | more or faster base resource (base_resource_gain, v38) | 0 | 0 | 100% | 1 | yes |

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
| ntb1 | Blitzkrieg | Lightning Mech | Boulder Mech | none  | - | yes |
| ntb2 | Swap Mech, Flame Shielding | Swap Mech | Flame Shielding | none  | - | yes |
| ntb3 | Hazardous Mechs | Nano Mech | Leap Mech | line heals Leap Mech when Leap Mech kills | type: Nano Mech moves units, and Leap Mech acts on units next to it; also heals: | yes |
| ntb4 | Steel Judoka | Judo Mech | Gravity Mech | none damages enemy units | type: Judo Mech moves Gravity Mech and units, and Gravity Mech acts on units in  | yes |
| ntb6 | Aegis Mech, Gravity Mech, Judo Mech | Aegis Mech | Gravity Mech | line damages enemy units | waits: damages enemy units or players | yes |
| ntb5 | Mist Eaters | Thruster Mech | Smog Mech | line Smoke | type: makes your units get Smoke | yes |
