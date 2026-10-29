# Case tests: inscryption

Made by `cases/run.py inscryption`.
**14 of 14 cases pass.**


## Mechanics (expected cards from the texts)

| case | question | expected | found | recall | extra | pass |
|---|---|---|---|---|---|---|
| mx01 | a trigger on another unit dying is other_death_trigger | 0 | 0 | 100% | 4 | yes |
| mx02 | moving enemy units is forced_movement | 0 | 0 | 100% | 26 | yes |
| mx03 | a plain draw is one form: zone deck_top, no pick top | 0 | 0 | 100% | 9 | yes |
| mx10 | damage to the enemy player is Nexus damage (kinds kept, v30) | 0 | 0 | 100% | 223 | yes |
| mx11 | moving or pushing units makes units move (positions change, v30) | 0 | 0 | 100% | 26 | yes |
| mx12 | a unit that moves is the event's object, never its actor (N16, Sentry, v36) | 4 | 4 | 100% | 0 | yes |

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
| ni01 | Act II Undead starter | Gravedigger | Zombie | line  | waits: you gain the second resource (Bones) (pays its cost); waits: you gain the | yes |
| ni02 | Act II Undead starter | Skeleton | Frank & Stein | line  | waits: you gain the second resource (Bones) (pays its cost) (by the game's rules | yes |
| ni03 | Act II Beast starter | Squirrel | Hawk | line  | waits: sacrificed (pays its cost) (by the game's rules) | yes |
| ni04 | Act II Magick starter | Emerald Mox | Junior Sage | line  | waits: you gain a gem (Mox) (pays its cost) | yes |
| ni05 | Act II Magick starter | Sapphire Mox | Junior Sage | none you gain a gem | - | yes |
| ni06 | Act II bones and sacrifice (Archeronline4U) | M3atB0t | Urayuli | line  | boosts: makes it cheaper (when it is sacrificed for it); waits: sacrificed (pays | yes |
| ni07 | Act II bones and sacrifice (Archeronline4U) | Bone Lord's Horn | Tomb Robber | line  | waits: you gain the second resource (Bones); waits: you gain the second resource | yes |
| ni08 | Kaycee's Mod Bones | Coyote | Pelts (Rabbit) | none sacrificed | - | yes |
