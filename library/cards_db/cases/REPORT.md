# Case tests: duelyst

Made by `cases/run.py duelyst`.
**65 of 65 cases pass.**


## Mechanics (expected cards from the texts)

| case | question | expected | found | recall | extra | pass |
|---|---|---|---|---|---|---|
| mx01 | a trigger on another unit dying is other_death_trigger | 0 | 0 | 100% | 22 | yes |
| mx02 | moving enemy units is forced_movement | 1 | 1 | 100% | 36 | yes |
| mx03 | a plain draw is one form: zone deck_top, no pick top | 53 | 53 | 100% | 17 | yes |
| mx10 | damage to the enemy player is Nexus damage (kinds kept, v30) | 0 | 0 | 100% | 680 | yes |
| mx11 | moving or pushing units makes units move (positions change, v30) | 1 | 1 | 100% | 94 | yes |
| mx12 | a unit that moves is the event's object, never its actor (N16, Sentry, v36) | 0 | 0 | 100% | 7 | yes |
| du01 | Opening Gambit triggers | 118 | 118 | 100% | 420 | yes |
| du02 | Dying Wish triggers | 48 | 48 | 100% | 14 | yes |
| du03 | Deathwatch triggers | 8 | 8 | 100% | 15 | yes |
| du04 | Blood Surge triggers | 17 | 17 | 100% | 19 | yes |
| du05 | Grow | 10 | 10 | 100% | 49 | yes |
| du06 | start of your turn | 17 | 17 | 100% | 42 | yes |
| du07 | end of your turn | 17 | 17 | 100% | 24 | yes |
| du08 | Zeal | 10 | 10 | 100% | 20 | yes |
| du09 | Infiltrate | 6 | 6 | 100% | 24 | yes |
| du10 | Bond | 8 | 8 | 100% | 22 | yes |
| du11 | Backstab | 18 | 18 | 100% | 0 | yes |
| du12 | Stun | 15 | 15 | 100% | 6 | yes |
| du13 | Dispel | 13 | 13 | 100% | 0 | yes |
| du14 | Shadow Creep made | 8 | 8 | 100% | 15 | yes |
| du15 | summon Wraithlings | 14 | 14 | 100% | 1 | yes |
| du16 | teleport | 22 | 22 | 100% | 19 | yes |
| du17 | equipped artifacts on the General | 29 | 29 | 100% | 12 | yes |
| du18 | Intensify | 13 | 13 | 100% | 525 | yes |
| du19 | Sentinel | 15 | 15 | 100% | 53 | yes |
| du20 | Build | 14 | 14 | 100% | 0 | yes |
| du21 | Provoke | 38 | 38 | 100% | 10 | yes |
| du22 | Rush | 15 | 15 | 100% | 17 | yes |
| du23 | Flying | 31 | 31 | 100% | 12 | yes |
| du24 | Ranged | 29 | 29 | 100% | 4 | yes |
| du25 | Frenzy | 20 | 20 | 100% | 8 | yes |
| du26 | Celerity | 15 | 15 | 100% | 7 | yes |
| du27 | Forcefield | 15 | 15 | 100% | 6 | yes |
| du28 | Airdrop | 10 | 10 | 100% | 1 | yes |
| du29 | Rebirth | 8 | 8 | 100% | 1 | yes |
| du30 | Blast | 5 | 5 | 100% | 2 | yes |
| mx13 | can't be targeted by spells: the cant is on the spells, the protected unit is "to" (N19, v37) | 6 | 6 | 100% | 2 | yes |
| mx14 | a dead unit put into play is revive, never summon from the discard (N20, v37) | 1 | 1 | 100% | 16 | yes |
| mx15 | a trigger that holds only "this turn" is an ability given to the player for this turn (v37, Duelyst) | 3 | 3 | 100% | 9 | yes |
| du31 | attacking from behind, or getting behind an enemy, is flanking (v39) | 17 | 17 | 100% | 0 | yes |
| du32 | being on the enemy side is territory (Infiltrate, v39) | 0 | 0 | 100% | 7 | yes |
| du33 | named areas (2x2, 3x3, corners, starting side) are area shapes (v39) | 12 | 12 | 100% | 12 | yes |
| du34 | a stun makes a unit unable to act (v39) | 15 | 15 | 100% | 4 | yes |

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
| ndu01 | Vaath Dying Wish | Spelljammer | Dagona | none  | - | yes |
| ndu02 | Cassyva Replace Abomination | Healing Mystic | Letigress | none  | - | yes |
| ndu03 | Cassyva Replace Abomination | Cassyva Soulreaper | Letigress | line  | waits: your units attack (by fighting) | yes |
| ndu04 | Argeon Mechaz0r | Lifestream | Argeon Highmayne | none  | - | yes |
| ndu05 | Vaath Dying Wish | Vaath the Immortal | Lavaslasher | none  | - | yes |
| ndu06 | Shidai Artifacts | Mask of Shadows | Shidai Stormblossom | line  | boosts: more power: it hits harder | yes |
| ndu07 | Shidai Artifacts | Flicker | Mask of Shadows | line  | waits: your units move | yes |
| ndu08 | Kaleos Trial of Songhai | EMP | Dagona | none  | - | yes |
| ndu09 | Vaath Dying Wish | Unseven | Dagona | line  | puts: puts it into play from the hand | yes |
| ndu10 | Kaleos Trial of Songhai | Scroll Bandit | Battle Panddo | none  | - | yes |
| ndu11 | Kaleos Trial of Songhai | Heartseeker | Hideatsu the Ebon Ox | line  | waits: is a card it counts when played | yes |
| ndu12 | Kaleos Trial of Songhai | Kaleos Xaan | Scroll Bandit | line  | waits: your units move | yes |
| ndu13 | Cassyva Replace Abomination | Aethermaster | White Widow | line  | waits: cards are replaced (shuffled into the deck) | yes |
| ndu14 | Lilithe Darkfire | Lilithe Blightchaser | Phantasm | none  | - | yes |
| ndu15 | Lilithe Darkfire | Grasp of Agony | Vorpal Reaver | none  | - | yes |
| ndu16 | Argeon Intensify Riftwalker | Lifestream | Sunstrike | none  | - | yes |
| ndu17 | Argeon Intensify Riftwalker | Sunstrike | Lifestream | none  | - | yes |
| ndu18 | Faie Blood Taura | Flameblood Warlock | Blood Taura | line  | waits: your Nexus or base takes damage | yes |
| ndu19 | Argeon Intensify Riftwalker | Windblade Adept | Afterblaze | line  | type: is a unit with Zeal it counts or asks for | yes |
| ndu20 | Argeon Mechaz0r | Helm of MECHAZ0R | MECHAZ0R! | line  | puts: summons | yes |
| ndu21 | Vaath Dying Wish | Kujata | Juggernaut | line  | boosts: makes it cheaper; waits: your units or players take damage | yes |
| ndu22 | Kaleos Trial of Songhai | Juxtaposition | Bonereaper | line  | waits: enemy units move | yes |
