# Case tests: inscryption

Made by `cases/run.py inscryption`.
**72 of 72 cases pass.**


## Mechanics (expected cards from the texts)

| case | question | expected | found | recall | extra | pass |
|---|---|---|---|---|---|---|
| mx01 | a trigger on another unit dying is other_death_trigger | 0 | 0 | 100% | 4 | yes |
| mx02 | moving enemy units is forced_movement | 0 | 0 | 100% | 26 | yes |
| mx03 | a plain draw is one form: zone deck_top, no pick top | 0 | 0 | 100% | 9 | yes |
| mx10 | damage to the enemy player is Nexus damage (kinds kept, v30) | 0 | 0 | 100% | 223 | yes |
| mx11 | moving or pushing units makes units move (positions change, v30) | 0 | 0 | 100% | 26 | yes |
| mx12 | a unit that moves (onto a space) is the event's object, never its actor (N16, Sentry, v36, v38) | 4 | 4 | 100% | 0 | yes |
| mi01 | Airborne: strikes the opponent directly | 20 | 20 | 100% | 14 | yes |
| mi02 | Touch of Death: a creature it damages perishes | 4 | 4 | 100% | 15 | yes |
| mi03 | Bone Digger: gives Bones | 3 | 3 | 100% | 10 | yes |
| mi04 | Bone King: gives Bones when it dies | 5 | 5 | 100% | 8 | yes |
| mi05 | Ant Spawner: creates an Ant in hand | 1 | 1 | 100% | 0 | yes |
| mi06 | Fecundity: a copy in hand | 3 | 3 | 100% | 0 | yes |
| mi07 | Dam Builder: Dams on the spaces beside it | 1 | 1 | 100% | 0 | yes |
| mi08 | Sprinter: moves on its own each turn | 9 | 9 | 100% | 15 | yes |
| mi09 | Fledgling: grows into another form | 8 | 8 | 100% | 13 | yes |
| mi10 | Worthy Sacrifice: something happens when it is sacrificed | 3 | 3 | 100% | 4 | yes |
| mi11 | Many Lives: does not perish when sacrificed | 4 | 4 | 100% | 3 | yes |
| mi12 | Green Mox: gives a Green gem | 6 | 6 | 100% | 8 | yes |
| mi13 | Gem Dependant: perishes without a Mox card | 5 | 5 | 100% | 8 | yes |
| mi14 | Unkillable: back to hand when it dies | 3 | 3 | 100% | 0 | yes |
| mi15 | Bifurcated Strike: strikes two spaces | 4 | 4 | 100% | 32 | yes |
| mi16 | Ants: Power is the number of Ants | 3 | 3 | 100% | 6 | yes |
| mi17 | Sharp Quills: damages its attacker | 4 | 4 | 100% | 11 | yes |
| mi18 | Leader: adjacent creatures gain Power | 1 | 1 | 100% | 0 | yes |
| mi19 | Stinky: the opposing creature loses Power | 2 | 2 | 100% | 3 | yes |
| mi20 | Waterborne: submerged (cannot be attacked) on the enemy turn | 9 | 9 | 100% | 37 | yes |
| mx13 | can't be targeted by spells: the cant is on the spells, the protected unit is "to" (N19, v37) | 0 | 0 | 100% | 0 | yes |
| mx14 | a dead unit put into play is revive, never summon from the discard (N20, v37) | 0 | 0 | 100% | 1 | yes |
| mx15 | a trigger that holds only "this turn" is an ability given to the player for this turn (v37, Duelyst) | 0 | 0 | 100% | 0 | yes |
| mi21 | strikes at opposing spaces also hit the opponent (an empty space is struck: wiki Card Battle) | 4 | 4 | 100% | 30 | yes |
| mx13 | an effect on the creature opposing it is about lanes (concept lanes from same_lane, v38) | 2 | 2 | 100% | 42 | yes |
| mx14 | a strike on the spaces beside the opposing one reaches other lanes (cross_lane, v38) | 2 | 2 | 100% | 4 | yes |
| mx15 | within a circuit is a formation (link_formation, v38) | 1 | 1 | 100% | 9 | yes |
| mx16 | more or faster base resource (base_resource_gain, v38) | 2 | 2 | 100% | 2 | yes |
| mi22 | Burrower: moves to an empty space of its own side when it would be struck | 5 | 5 | 100% | 0 | yes |
| mi23 | rotate one space clockwise: every unit moves to a bordering space | 1 | 1 | 100% | 1 | yes |

## Combos (the enabler must set off the payoff)

| case | enabler | payoff | why | found as | pass |
|---|---|---|---|---|---|
| ci01 | Necromancer | Broken Obol (Right) | the Obol dies twice, giving Bones twice (Bone King) | condition: mana_refilled | yes |
| ci02 | Warren | Rabbit | Warren supplies Rabbits | makes | yes |
| ci03 | Sapphire Mox | Blue Mage | Blue Mage needs the matching Mox | type: Mox Card | yes |
| ci04 | Ruby Mox | Mage Knight | Mage Knight needs the matching Mox | type: Mox Card | yes |
| ci05 | Emerald Mox | Junior Sage | Junior Sage needs the matching Mox | condition: mana_refilled | yes |
| ci07 | Necromancer | Tomb Robber | Skeletons from Tomb Robber die twice with Necromancer: more Bones | condition: mana_refilled | yes |
| ci08 | Necromancer | Bone Heap | the Bones loop pays for Bone Heap's Enlarge | condition: mana_refilled | yes |

## Region identity (signature, splash, archetype)

| case | region | kind | mechanic | need | found | pass |
|---|---|---|---|---|---|---|
| ri01 | Beast | signature (inscryption.md: Blood costs paid by sacrifice) | needs sacrifices to be played (Blood) | 20 | 73 | yes |
| ri02 | Undead | signature (inscryption.md: Bones from Gravedigger and from cards that die) | gives Bones | 3 | 5 | yes |
| ri03 | Undead | signature (inscryption.md: Bones as the cost) | paid with Bones | 10 | 21 | yes |
| ri04 | Magick | signature (inscryption.md: Magick cards are paid with Mox gems) | paid with gems | 8 | 17 | yes |
| ri05 | Beast | signature (inscryption.md: Warren puts a Rabbit in hand) | creates cards in hand | 4 | 8 | yes |
| ri06 | Beast | signature (inscryption.md: Hawk hits past blockers) | strikes the opponent directly | 8 | 23 | yes |
| ri07 | Magick | signature (inscryption.md: Blue Mage draws per Mox) | draws cards | 1 | 4 | yes |
| ri08 | Technology | signature (wiki Energy: Battery Bearer raises Energy) | more or faster base resource | 2 | 2 | yes |

## Guide decks (the explanation must say what the guide says)

| case | deck | must say | missing | pass |
|---|---|---|---|---|
| di01 | Act II Undead starter | second resource (Bones): made by;Gravedigger | - | yes |
| di02 | Act II Beast starter | units are sacrificed;Warren | - | yes |
| di03 | Act II Magick starter | gem (Mox): made by Emerald Mox, Ruby Mox, Sapphire Mox | - | yes |
| di04 | Act II bones and sacrifice (Archeronline4U) | Tomb Robber;second resource (Bones) | - | yes |

## Deck networks (a line must be there, or must not)

| case | deck | from | to | expect | found | pass |
|---|---|---|---|---|---|---|
| ni01 | Act II Undead starter | Gravedigger | Zombie | line  | waits: you gain the second resource (Bones) (pays its cost); waits: you gain the | yes |
| ni02 | Act II Undead starter | Skeleton | Frank & Stein | line  | waits: you gain the second resource (Bones) (pays its cost) (by the game's rule: | yes |
| ni03 | Act II Beast starter | Squirrel | Hawk | line  | waits: your units are sacrificed (pays its cost) (by the game's rule: units can  | yes |
| ni04 | Act II Magick starter | Emerald Mox | Junior Sage | line  | waits: you gain a gem (Mox) (pays its cost) | yes |
| ni05 | Act II Magick starter | Sapphire Mox | Junior Sage | none you gain a gem | - | yes |
| ni06 | Act II bones and sacrifice (Archeronline4U) | M3atB0t | Urayuli | line  | boosts: makes it cheaper (when it is sacrificed for it); waits: your units are s | yes |
| ni07 | Act II bones and sacrifice (Archeronline4U) | Bone Lord's Horn | Tomb Robber | line  | waits: you gain the second resource (Bones) | yes |
| ni08 | Kaycee's Mod Bones | Coyote | Pelts (Rabbit) | none sacrificed | - | yes |
| ni09 | Act II Ouroboros and Mantis God (koi) | Mantis God | Ouroboros | line  | waits: your units are sacrificed (pays its cost) (by the game's rule: units can  | yes |
| ni10 | Act II Ouroboros and Mantis God (koi) | Ouroboros | Mantis God | none Blood costs | waits: your units are sacrificed (pays its cost) (by the game's rule: units can  | yes |
| ni11 | Kaycee's Mod Ants | Ant Queen | Flying Ant | line  | type: is a unit with Ant it counts or asks for; waits: your units are sacrificed | yes |
| ni12 | Kaycee's Mod Moose Blood | Moose Buck | Pelts (Rabbit) | none your units move | - | yes |
| ni13 | Kaycee's Mod Free Reptiles | Rabbit | Bullfrog | none sacrificed | - | yes |
| ni14 | Act III starter | Sniper Bot | Double Gunner | none  | - | yes |
| ni15 | Alpha, Wolf, Moose Buck | Alpha | Wolf | line  | boosts: gives it +1|+0 (when next to it); waits: your units are sacrificed (pays | yes |
| ni16 | Daus, Bell Tentacle | Bell Tentacle | Daus | line  | type: is the Bell Tentacle it names; waits: your units are sacrificed (pays its  | yes |
| ni17 | Daus, Bell Tentacle | Bell Tentacle | Daus | none by fighting | type: is the Bell Tentacle it names; waits: your units are sacrificed (pays its  | yes |
