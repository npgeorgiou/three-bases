# Case tests: marvel_snap

Made by `cases/run.py marvel_snap`.
**48 of 64 cases pass.**


## Mechanics (expected cards from the texts)

| case | question | expected | found | recall | extra | pass |
|---|---|---|---|---|---|---|
| mx01 | a trigger on another unit dying is other_death_trigger | 0 | 0 | 100% | 10 | yes |
| mx02 | moving enemy units is forced_movement | 1 | 1 | 100% | 49 | yes |
| mx03 | a plain draw is one form: zone deck_top, no pick top | 16 | 16 | 100% | 15 | yes |
| mx10 | damage to the enemy player is Nexus damage (kinds kept, v30) | 0 | 0 | 100% | 0 | yes |
| mx11 | moving or pushing units makes units move (positions change, v30) | 1 | 1 | 100% | 57 | yes |
| mx12 | a unit that moves (onto a space) is the event's object, never its actor (N16, Sentry, v36, v38) | 0 | 0 | 100% | 19 | yes |
| mx13 | can't be targeted by spells: the cant is on the spells, the protected unit is "to" (N19, v37) | 0 | 0 | 100% | 0 | yes |
| mx14 | a dead unit put into play is revive, never summon from the discard (N20, v37) | 0 | 0 | 100% | 16 | yes |
| mx15 | a trigger that holds only "this turn" is an ability given to the player for this turn (v37, Duelyst) | 0 | 0 | 100% | 4 | yes |
| mx13 | an effect on the creature opposing it is about lanes (concept lanes from same_lane, v38) | 0 | 0 | 100% | 398 | yes |
| mx14 | a strike on the spaces beside the opposing one reaches other lanes (cross_lane, v38) | 0 | 0 | 100% | 0 | yes |
| mx15 | within a circuit is a formation (link_formation, v38) | 0 | 0 | 100% | 0 | yes |
| mx16 | more or faster base resource (base_resource_gain, v38) | 0 | 0 | 100% | 35 | yes |
| ms04 | limits what can be played at a location (play_restriction) | 15 | 15 | 100% | 23 | yes |

## Combos (the enabler must set off the payoff)

| case | enabler | payoff | why | found as | pass |
|---|---|---|---|---|---|
| cms01 | M.O.D.O.K. | Hela | M.O.D.O.K. discards the hand, Hela brings the discarded cards back | state: discarded | yes |
| cms02 | Swarm | Morbius | Morbius grows per discard; Swarm returns after it is discarded | - | NO |
| cms03 | Apocalypse | Morbius | Morbius grows per discard; Apocalypse returns after it is discarded | - | NO |
| cms04 | Wong | Odin | Wong doubles Odin's On Reveal | - | NO |
| cms05 | Odin | Ironheart | Odin repeats her power boost | trigger keyword: On Reveal | yes |
| cms06 | Odin | Black Panther | Odin repeats his power boost | trigger keyword: On Reveal | yes |
| cms07 | Storm | White Tiger | White Tiger still places a card in the flooded location | - | NO |
| cms08 | Storm | Doctor Doom | Doctor Doom still places cards in the flooded location | - | NO |
| cms09 | Brood | Wolfsbane | Brood fills a location, Wolfsbane gains power as the fourth card | count: unit | yes |
| cms10 | Moon Girl | Devil Dinosaur | the doubled hand boosts Devil Dinosaur | - | NO |
| cms11 | Shuri | Typhoid Mary | Shuri doubles the next card's power | - | NO |
| cms12 | Shuri | Red Skull | Shuri doubles the next card's power | - | NO |
| cms13 | Zero | Titania | Zero removes her drawback | is: playing Zero is a played the payoff waits for | yes |
| cms14 | Zero | Ebony Maw | Zero removes his drawback | - | NO |
| cms15 | Sauron | Titania | Sauron removes her drawback | is: playing Sauron is a played the payoff waits for | yes |
| cms16 | Sauron | Ebony Maw | Sauron removes his drawback | - | NO |
| cms17 | Taskmaster | Red Skull | Taskmaster copies the last card's power | - | NO |
| cms18 | Taskmaster | Typhoid Mary | Taskmaster copies the last card's power | - | NO |
| cms19 | Cable | Mantis | both take cards from the opponent's deck | - | NO |
| cms20 | Carnage | Nova | Carnage destroys Nova, whose death buffs your cards | event: kill -> dies | yes |
| cms21 | Ant Man | Angela | points in the third location | is: playing Ant Man is a played the payoff waits for | yes |
| cms22 | Doctor Octopus | Mojo | +6 when the spot is empty | state: moves | yes |
| cms23 | Wave | Death | the deck is built around the two | - | NO |
| cms24 | The Collector | Moon Girl | Collector buffs cards, Moon Girl copies them | - | NO |

## Region identity (signature, splash, archetype)

| case | region | kind | mechanic | need | found | pass |
|---|---|---|---|---|---|---|

## Guide decks (the explanation must say what the guide says)

| case | deck | must say | missing | pass |
|---|---|---|---|---|
| dms01 | Self-destruction Deadpool | your units die: made by carnage, deathlok, killmonger, venom;get value when they die: bucky barnes, deadpool | - | yes |
| dms02 | Sera Mystique summons | pays for big cards (more mana, cheaper cards): sera | - | yes |
| dms03 | The Wong Spectrum | wong makes these cards' effects happen again | wong makes these cards' effects happen again | NO |
| dms04 | Deathpool self-destruction | your units die: made by carnage, deadpool, deathlok, killmonger, venom;use it: death, knull | - | yes |
| dms05 | Sera Zero summons | pays for big cards (more mana, cheaper cards): sera;use it: taskmaster | - | yes |
| dms06 | Patriots, drones and clones | onslaught makes these cards' effects happen again: blue marvel, ka-zar, patriot;puts extra units into play: debrii, mister sinister, squirrel girl, ultron | - | yes |
| dms07 | Wakanda Forever | odin makes these cards' effects happen again: black panther | - | yes |
| dms08 | Knull Galactus | your units die: made by destroyer, galactus;use it: death, knull | - | yes |
| dms09 | High Evo Lockjaw | your units get on reveal: made by high evolutionary, lockjaw | - | yes |
| dms10 | Surfin' Sebastian | use it: sebastian shaw | - | yes |
| dms11 | Hidden Hela discard | use it: hela | - | yes |
| dms12 | Hand Size Heroes | cards are created: made by agent coulson, hawkeye kate bishop, iron patriot, maria hill, snowguard | - | yes |

## Deck networks (a line must be there, or must not)

| case | deck | from | to | expect | found | pass |
|---|---|---|---|---|---|---|
| n396 | Hawkeye Kate Bishop, Acid Arrow | Hawkeye Kate Bishop | Acid Arrow | line creates | puts: creates | yes |
| n397 | Hawkeye Kate Bishop, Marrow | Hawkeye Kate Bishop | Marrow | none  | - | yes |
| n399 | Daken, Muramasa Shard | Daken | Muramasa Shard | line creates | puts: creates; also enables: is the Daken it names | yes |
| n400 | Agamotto, Bolts of Balthakk | Agamotto | Bolts of Balthakk | line creates | puts: creates | yes |
| n401 | Zombie Black Cat, Wolverine | Zombie Black Cat | Wolverine | line discard | waits: makes you discard cards | yes |
| n402 | Korg, Rock | Korg | Rock | none  | - | yes |
| n403 | Vampire Thanos | Thanos Fractured Frontier | Power Shot | line creates | puts: creates | yes |
| n404 | Symbiote Galactus | Hawkeye Kate Bishop | Grapple Arrow | line creates | puts: creates | yes |
| n409 | Majestic Wingbeat, Zombie Galacti | Majestic Wingbeat | Zombie Galacti | none  | - | yes |
| n411 | Black Widow, Widow's Bite | Black Widow | Widow's Bite | none  | - | yes |
| n413 | M.O.D.O.K., Hela | M.O.D.O.K. | Hela | line  | type: makes you discard cards | yes |
| n414 | Killmonger, Hela | Killmonger | Hela | none  | - | yes |
| n415 | Lady Sif, Ghost Rider | Lady Sif | Ghost Rider | line  | type: makes you discard cards | yes |
| n416 | Carnage, Phoenix Force | Carnage | Phoenix Force | line  | type: makes your units die: Phoenix Force brings them back | yes |
