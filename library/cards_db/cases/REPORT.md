# Case tests: duelyst

Made by `cases/run.py duelyst`.
**109 of 109 cases pass.**

**Cases whose reason no line says any more (rewrite them): ndu23, ndu47, n306, n307, n317**


## Mechanics (expected cards from the texts)

| case | question | expected | found | recall | extra | pass |
|---|---|---|---|---|---|---|
| mx01 | a trigger on another unit dying is other_death_trigger | 0 | 0 | 100% | 21 | yes |
| mx02 | moving enemy units is forced_movement | 1 | 1 | 100% | 35 | yes |
| mx03 | a plain draw is one form: zone deck_top, no pick top | 52 | 52 | 100% | 17 | yes |
| mx10 | damage to the enemy player is Nexus damage (kinds kept, v30) | 0 | 0 | 100% | 680 | yes |
| mx11 | moving or pushing units makes units move (positions change, v30) | 1 | 1 | 100% | 109 | yes |
| mx12 | a unit that moves (onto a space) is the event's object, never its actor (N16, Sentry, v36, v38) | 0 | 0 | 100% | 7 | yes |
| du01 | Opening Gambit triggers | 118 | 118 | 100% | 420 | yes |
| du02 | Dying Wish triggers | 48 | 48 | 100% | 14 | yes |
| du03 | Deathwatch triggers | 8 | 8 | 100% | 14 | yes |
| du04 | Blood Surge triggers | 17 | 17 | 100% | 0 | yes |
| du05 | Grow | 10 | 10 | 100% | 49 | yes |
| du06 | start of your turn | 17 | 17 | 100% | 42 | yes |
| du07 | end of your turn | 17 | 17 | 100% | 24 | yes |
| du08 | Zeal | 10 | 10 | 100% | 20 | yes |
| du09 | Infiltrate | 6 | 6 | 100% | 24 | yes |
| du10 | Bond | 8 | 8 | 100% | 22 | yes |
| du11 | Backstab | 18 | 18 | 100% | 0 | yes |
| du12 | Stun | 14 | 14 | 100% | 6 | yes |
| du13 | Dispel | 13 | 13 | 100% | 0 | yes |
| du14 | Shadow Creep made | 7 | 7 | 100% | 15 | yes |
| du15 | summon Wraithlings | 13 | 13 | 100% | 1 | yes |
| du16 | teleport | 21 | 21 | 100% | 19 | yes |
| du17 | equipped artifacts on the General | 29 | 29 | 100% | 11 | yes |
| du18 | Intensify | 13 | 13 | 100% | 525 | yes |
| du19 | Sentinel | 15 | 15 | 100% | 53 | yes |
| du20 | Build | 14 | 14 | 100% | 0 | yes |
| du21 | Provoke | 38 | 38 | 100% | 6 | yes |
| du22 | Rush | 15 | 15 | 100% | 5 | yes |
| du23 | Flying | 31 | 31 | 100% | 10 | yes |
| du24 | Ranged | 29 | 29 | 100% | 3 | yes |
| du25 | Frenzy | 20 | 20 | 100% | 8 | yes |
| du26 | Celerity | 15 | 15 | 100% | 7 | yes |
| du27 | Forcefield | 15 | 15 | 100% | 6 | yes |
| du28 | Airdrop | 10 | 10 | 100% | 1 | yes |
| du29 | Rebirth | 8 | 8 | 100% | 1 | yes |
| du30 | Blast | 5 | 5 | 100% | 2 | yes |
| mx13 | can't be targeted by spells: the cant is on the spells, the protected unit is "to" (N19, v37) | 6 | 6 | 100% | 2 | yes |
| mx14 | a dead unit put into play is revive, never summon from the discard (N20, v37) | 1 | 1 | 100% | 16 | yes |
| mx15 | a trigger that holds only "this turn" is an ability given to the player for this turn (v37, Duelyst) | 3 | 3 | 100% | 8 | yes |
| mx13 | an effect on the creature opposing it is about lanes (concept lanes from same_lane, v38) | 0 | 0 | 100% | 20 | yes |
| mx14 | a strike on the spaces beside the opposing one reaches other lanes (cross_lane, v38) | 0 | 0 | 100% | 0 | yes |
| mx15 | within a circuit is a formation (link_formation, v38) | 0 | 0 | 100% | 0 | yes |
| mx16 | more or faster base resource (base_resource_gain, v38) | 0 | 0 | 100% | 6 | yes |
| du31 | attacking from behind, or getting behind an enemy, is flanking (v40) | 17 | 17 | 100% | 0 | yes |
| du32 | being on the enemy side is territory (Infiltrate, v39) | 0 | 0 | 100% | 7 | yes |
| du33 | named areas (2x2, 3x3, corners, starting side) are area shapes (v40) | 12 | 12 | 100% | 12 | yes |
| du34 | a stun makes a unit unable to act (v40; not a minion stunning itself, Meltwater Moose) | 13 | 13 | 100% | 4 | yes |

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
| ndu02 | Cassyva Replace Abomination | Healing Mystic | Letigress | none waits | - | yes |
| ndu03 | Cassyva Replace Abomination | Cassyva Soulreaper | Letigress | none  | - | yes |
| ndu04 | Argeon Mechaz0r | Lifestream | Argeon Highmayne | none  | - | yes |
| ndu05 | Vaath Dying Wish | Overload | Lavaslasher | none  | - | yes |
| ndu06 | Shidai Artifacts | Mask of Shadows | Shidai Stormblossom | line  | keyword: can give it Backstab | yes |
| ndu07 | Shidai Artifacts | Flicker | Mask of Shadows | line  | type: Flicker moves your units, and Mask of Shadows acts on units behind its tar | yes |
| ndu08 | Kaleos Trial of Songhai | EMP | Dagona | none  | - | yes |
| ndu09 | Vaath Dying Wish | Unseven | Dagona | line  | puts: puts it into play from the hand | yes |
| ndu10 | Kaleos Trial of Songhai | Scroll Bandit | Battle Panddo | none  | - | yes |
| ndu11 | Kaleos Trial of Songhai | Heartseeker | Hideatsu the Ebon Ox | none  | - | yes |
| ndu12 | Kaleos Trial of Songhai | Blink | Scroll Bandit | line  | type: Blink moves Scroll Bandit, and Scroll Bandit acts on units behind its targ | yes |
| ndu13 | Cassyva Replace Abomination | Aethermaster | White Widow | line  | waits: shuffles cards into the deck | yes |
| ndu14 | Lilithe Darkfire | Lilithe Blightchaser | Phantasm | none  | - | yes |
| ndu15 | Lilithe Darkfire | Grasp of Agony | Vorpal Reaver | none  | - | yes |
| ndu16 | Argeon Intensify Riftwalker | Lifestream | Sunstrike | none  | - | yes |
| ndu17 | Argeon Intensify Riftwalker | Sunstrike | Lifestream | none  | - | yes |
| ndu18 | Faie Blood Taura | Flameblood Warlock | Blood Taura | line  | type: damages your leader | yes |
| ndu19 | Argeon Intensify Riftwalker | Windblade Adept | Afterblaze | line  | type: is a unit with Zeal it counts or asks for | yes |
| ndu20 | Argeon Mechaz0r | Helm of MECHAZ0R | MECHAZ0R! | line  | puts: summons | yes |
| ndu21 | Vaath Dying Wish | Kujata | Juggernaut | line  | waits: damages it for its effect | yes |
| ndu22 | Kaleos Trial of Songhai | Juxtaposition | Bonereaper | line  | type: Juxtaposition moves Bonereaper and enemy units, and Bonereaper acts on uni | yes |
| ndu23 | Vaath Dying Wish | Juggernaut | Lavaslasher | none more power: | - | yes |
| ndu24 | Cassyva Replace Abomination | Aethermaster | Cassyva Soulreaper | none  | - | yes |
| ndu25 | Cassyva Replace Abomination | Healing Mystic | Abhorrent Unbirth | none  | - | yes |
| ndu26 | Lilithe Darkfire | Phantasm | Wraithling | none  | - | yes |
| ndu27 | Lilithe Darkfire | Darkfire Sacrifice | Wraithling | none cheaper | - | yes |
| ndu28 | Cassyva Replace Abomination | Healing Mystic | Cassyva Soulreaper | none  | - | yes |
| ndu29 | Lilithe Darkfire | Wraithling | Inkling Surge | line  | type: is the Wraithling it names | yes |
| ndu31 | Lilithe Darkfire | Vorpal Reaver | Inkling Surge | none makes | - | yes |
| ndu30 | Faie Blood Taura | White Asp | Blazing Spines | none names | - | yes |
| ndu32 | Argeon Mechaz0r | Lifestream | Martyrdom | none  | - | yes |
| ndu33 | Argeon Mechaz0r | Helm of MECHAZ0R | Oakenheart | none  | - | yes |
| ndu34 | Argeon Mechaz0r | Oakenheart | Helm of MECHAZ0R | line  | stronger: gives it more power and health | yes |
| ndu35 | Vaath Dying Wish | Ragebinder | Golem Metallurgist | none  | - | yes |
| ndu36 | Vaath Dying Wish | Golem Metallurgist | Ragebinder | line  | cheaper: makes it cheaper when it comes | yes |
| ndu37 | Cassyva Replace Abomination | Aethermaster | Punish | none  | - | yes |
| ndu38 | Cassyva Replace Abomination | Letigress | Punish | none  | - | yes |
| ndu39 | Shidai Artifacts | Cyclone Mask | Shidai Stormblossom | line  | keyword: can give it Ranged | yes |
| ndu40 | Argeon Dawn's Eye aggro | Argeon Highmayne | Roar | line  | puts: casts its own spell | yes |
| ndu41 | Argeon Dawn's Eye aggro | Roar | Windblade Adept | line  | stronger: can give it more power | yes |
| ndu42 | Argeon Dawn's Eye aggro | Azurite Lion | Holy Immolation | none moves | - | yes |
| ndu43 | Argeon Dawn's Eye aggro | Azurite Lion | Windblade Adept | none  | - | yes |
| ndu44 | Ciphyron Build | Rescue-RX | Timekeeper | none  | - | yes |
| ndu45 | Ciphyron Build | Timekeeper | Rescue-RX | line  | stronger: can speed up its countdown | yes |
| ndu46 | Argeon Dawn's Eye aggro | Tempest | Arclyte Regalia | none  | - | yes |
| ndu47 | Kaleos Trial of Songhai | Dispirited Prisoner | Hideatsu the Ebon Ox | none needs played | - | yes |
| n240 | Brome Swarm | Warblade | Fealty | none  | - | yes |
| n288 | Lilithe Swarm | Bloodtear Alchemist | Horn of the Forsaken | none damages | - | yes |
| n305 | Dragonlark, Vigilator | Dragonlark | Vigilator | none moves your units | - | yes |
| n306 | Mist Walking, Gore Horn | Mist Walking | Gore Horn | none moves Gore Horn | - | yes |
| n307 | Bombard, Penumbraxx | Bombard | Penumbraxx | none moves Penumbraxx | - | yes |
| n312 | Eternity Painter, Manakite Drifter | Eternity Painter | Manakite Drifter | none transforms cards | - | yes |
| n313 | Disciple of Yggdra, Architect-T2K5 | Disciple of Yggdra | Architect-T2K5 | line transforms cards | waits: transforms cards | yes |
| n317 | Faie Bloodwing, Resonance Scythe | Faie Bloodwing | Resonance Scythe | none kills enemy units | - | yes |
| n318 | Piercing Mantis, Gate to the Undervault | Piercing Mantis | Gate to the Undervault | none makes units die | - | yes |
| n364 | Crystallize, Cryoblade | Crystallize | Cryoblade | line  | type: makes enemy units get a keyword or status | yes |
| n365 | Aer Pridebeak, Argeon Highmayne | Aer Pridebeak | Argeon Highmayne | none heal | - | yes |
| n366 | Dawn's Eye, Argeon Highmayne | Dawn's Eye | Argeon Highmayne | none power | - | yes |
| n367 | Lux Ignis, Fireblazer | Lux Ignis | Fireblazer | none heal | - | yes |
| n369 | Mirkblood Devourer, Drogon | Mirkblood Devourer | Drogon | none power | - | yes |
| n376 | Crescent Spear, Phoenix Fire | Crescent Spear | Phoenix Fire | none  | - | yes |
