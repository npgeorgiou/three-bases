# Case tests: marvel_snap

Made by `cases/run.py marvel_snap`.
**157 of 165 cases pass.**

**Cases whose reason no line says any more (rewrite them): n465, n489, n490, n492**


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
| cms02 | Swarm | Morbius | Morbius grows per discard; Swarm returns after it is discarded | line: comes back after it is discarded, to be discarded again | yes |
| cms03 | Apocalypse | Morbius | Morbius grows per discard; Apocalypse returns after it is discarded | line: comes back after it is discarded, to be discarded again | yes |
| cms04 | Wong | Odin | Wong doubles Odin's On Reveal | line: plays it again | yes |
| cms05 | Odin | Ironheart | Odin repeats her power boost | trigger keyword: On Reveal | yes |
| cms06 | Odin | Black Panther | Odin repeats his power boost | trigger keyword: On Reveal | yes |
| cms07 | Storm | White Tiger | White Tiger still places a card in the flooded location | line: stops cards being played, but a summon is not played: it sti | yes |
| cms08 | Storm | Doctor Doom | Doctor Doom still places cards in the flooded location | line: stops cards being played, but a summon is not played: it sti | yes |
| cms09 | Brood | Wolfsbane | Brood fills a location, Wolfsbane gains power as the fourth card | count: unit | yes |
| cms10 | Moon Girl | Devil Dinosaur | the doubled hand boosts Devil Dinosaur | line: fills your hand | yes |
| cms11 | Shuri | Typhoid Mary | Shuri doubles the next card's power | - | NO |
| cms12 | Shuri | Red Skull | Shuri doubles the next card's power | - | NO |
| cms13 | Zero | Titania | Zero removes her drawback | is: playing Zero is a played the payoff waits for | yes |
| cms14 | Zero | Ebony Maw | Zero removes his drawback | line: silences it: its drawback is gone | yes |
| cms15 | Sauron | Titania | Sauron removes her drawback | is: playing Sauron is a played the payoff waits for | yes |
| cms16 | Sauron | Ebony Maw | Sauron removes his drawback | line: silence | yes |
| cms17 | Taskmaster | Red Skull | Taskmaster copies the last card's power | - | NO |
| cms18 | Taskmaster | Typhoid Mary | Taskmaster copies the last card's power | - | NO |
| cms19 | Cable | Mantis | both take cards from the opponent's deck | - | NO |
| cms20 | Carnage | Nova | Carnage destroys Nova, whose death buffs your cards | event: kill -> dies | yes |
| cms21 | Ant Man | Angela | points in the third location | is: playing Ant Man is a played the payoff waits for | yes |
| cms22 | Doctor Octopus | Mojo | +6 when the spot is empty | state: moves | yes |
| cms23 | Wave | Death | the deck is built around the two | line: makes it cheaper | yes |
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
| n417 | Jane Foster Fractured Frontier, Fin Fang Foom | Jane Foster Fractured Frontier | Fin Fang Foom | none  | - | yes |
| n418 | The Grand Design, Zombie Giant-Man | The Grand Design | Zombie Giant-Man | none  | - | yes |
| n419 | Venus, Zombie Giant-Man | Venus | Zombie Giant-Man | none  | - | yes |
| n420 | Zombie Mister Fantastic, Zombie Giant-Man | Zombie Mister Fantastic | Zombie Giant-Man | line  | stronger: more power | yes |
| n421 | Excalibur, Iron Man | Excalibur | Iron Man | line  | stronger: more power | yes |
| n422 | Astral Projection, Acid Arrow | Astral Projection | Acid Arrow | none  | - | yes |
| n423 | Toxin, Acid Arrow | Toxin | Acid Arrow | none  | - | yes |
| n424 | Beast, Absorbing Man | Beast | Absorbing Man | line  | type: is a unit with On Reveal it counts or asks for | yes |
| n425 | Ultron Mind Stone, Absorbing Man | Ultron Mind Stone | Absorbing Man | line  | stronger: plays it again | yes |
| n426 | Onslaught, J. Jonah Jameson | Onslaught | J. Jonah Jameson | none  | - | yes |
| n427 | Caiera, Broodling | Caiera | Broodling | none  | - | yes |
| n428 | Joaquin Torres Falcon II, Electro | Joaquin Torres Falcon II | Electro | line  | repeats: repeats its On Reveal effects | yes |
| n431 | Agent 13, King Eitri | Agent 13 | King Eitri | none  | - | yes |
| n432 | Agent 13, Devil Dinosaur | Agent 13 | Devil Dinosaur | line  | waits: fills your hand | yes |
| n433 | Araña, Magus | Araña | Magus | none  | - | yes |
| n434 | Araña, Lancelot | Araña | Lancelot | line  | type: changes your units' stats; also makes stronger: does what it waits for or  | yes |
| n435 | Kid Omega, Bucky Barnes | Kid Omega | Bucky Barnes | line  | waits: kills it for its death effect | yes |
| n436 | Kid Omega, Elixir | Kid Omega | Elixir | line  | type: makes your units die: Elixir brings them back | yes |
| n437 | Jocasta, Awesome Andy | Jocasta | Awesome Andy | line  | waits: makes this happen: activated | yes |
| n438 | Attuma, Death Fractured Frontier | Attuma | Death Fractured Frontier | line  | type: makes your units die: Death Fractured Frontier brings them back | yes |
| n439 | Doctor Strange, Danger | Doctor Strange | Danger | none  | - | yes |
| n440 | Ghost-Spider, Drax | Ghost-Spider | Drax | none  | - | yes |
| n441 | Blink, Moonstone | Blink | Moonstone | none  | - | yes |
| n442 | Doctor Octopus, Pizza Slice | Doctor Octopus | Pizza Slice | none  | - | yes |
| n443 | Angel, Hydra Stomper | Angel | Hydra Stomper | line  | type: makes your units move | yes |
| n444 | Herbie Program 01, Wiccan | Herbie Program 01 | Wiccan | none  | - | yes |
| n445 | Ghost-Spider, Galactus | Ghost-Spider | Galactus | none  | - | yes |
| n446 | Djinn, Jim Hammond Human Torch | Djinn | Jim Hammond Human Torch | line  | type: lets you gain mana | yes |
| n447 | Beta Ray Bill, Gorgon | Beta Ray Bill | Gorgon | none  | - | yes |
| n448 | Doctor Octopus, Dagger | Doctor Octopus | Dagger | none  | - | yes |
| n449 | Aero, Armor | Aero | Armor | none  | - | yes |
| n450 | Moira X, Quinjet | Moira X | Quinjet | line  | type: creates cards | yes |
| n451 | Agent Venom, Wolverine Horseman of War | Agent Venom | Wolverine Horseman of War | none  | - | yes |
| n452 | Agent Venom, Elder Dragon of the Moon | Agent Venom | Elder Dragon of the Moon | none  | - | yes |
| n453 | Agent Venom, Gilgamesh | Agent Venom | Gilgamesh | none  | - | yes |
| n454 | America Chavez, Ares | America Chavez | Ares | line more power | stronger: more power | yes |
| n455 | Sera, Mystique | Sera | Mystique | line a unit with Ongoing | type: is a unit with Ongoing it counts or asks for | yes |
| n456 | Mojo, Mystique | Mojo | Mystique | line a unit with Ongoing | type: is a unit with Ongoing it counts or asks for | yes |
| n457 | Ant Man, Mystique | Ant Man | Mystique | line a unit with Ongoing | type: is a unit with Ongoing it counts or asks for | yes |
| n458 | Patriot, Mystique | Patriot | Mystique | line a unit with Ongoing | type: is a unit with Ongoing it counts or asks for | yes |
| n459 | Wong, Mystique | Wong | Mystique | line a unit with Ongoing | type: is a unit with Ongoing it counts or asks for; also makes stronger: plays i | yes |
| n460 | Onslaught, Blue Marvel | Onslaught | Blue Marvel | line repeats its effects | repeats: repeats its effects | yes |
| n461 | Okoye, Black Panther | Okoye | Black Panther | line gives it more power | stronger: gives it more power | yes |
| n462 | Nakia, Black Panther | Nakia | Black Panther | line gives it more power | stronger: gives it more power | yes |
| n463 | Wong, Black Panther | Wong | Black Panther | line plays it again | stronger: plays it again | yes |
| n464 | Odin, Black Panther | Odin | Black Panther | line repeats its effects | repeats: repeats its effects; also repeats its On Reveal effects | yes |
| n465 | Okoye, Zabu | Okoye | Zabu | none more power to any card | - | yes |
| n466 | Galactus, Knull | Galactus | Knull | line makes units die | type: makes units die | yes |
| n467 | Galactus, Death | Galactus | Death | line makes units die | cheaper: makes units die | yes |
| n468 | Destroyer, Knull | Destroyer | Knull | line makes units die | type: makes units die | yes |
| n469 | Destroyer, Death | Destroyer | Death | line makes units die | cheaper: makes units die | yes |
| n470 | Victoria Hand, Mystique | Victoria Hand | Mystique | line is a unit with Ongoing it counts or asks for | type: is a unit with Ongoing it counts or asks for | yes |
| n471 | Devil Dinosaur, Mystique | Devil Dinosaur | Mystique | line is a unit with Ongoing it counts or asks for | type: is a unit with Ongoing it counts or asks for | yes |
| n472 | PymParticle Arrow, Mystique | PymParticle Arrow | Mystique | line is a unit with Ongoing it counts or asks for | type: is a unit with Ongoing it counts or asks for | yes |
| n473 | Sera, Mystique | Sera | Mystique | line is a unit with Ongoing it counts or asks for | type: is a unit with Ongoing it counts or asks for | yes |
| n474 | Basic Arrow, Mystique | Basic Arrow | Mystique | line makes your units get Ongoing | type: makes your units get Ongoing | yes |
| n475 | Fantomex, Zombie Captain Marvel | Fantomex | Zombie Captain Marvel | none  | - | yes |
| n476 | Fantomex, Zombie Captain Marvel | Zombie Captain Marvel | Fantomex | line makes your units die | type: makes your units die | yes |
| n477 | Grapple Arrow, Galactus | Grapple Arrow | Galactus | none  | - | yes |
| n478 | Grapple Arrow, PymParticle Arrow | Grapple Arrow | PymParticle Arrow | line moves your units | type: Grapple Arrow moves your units, and PymParticle Arrow acts on units in its | yes |
| n479 | Iron Patriot, King Eitri | Iron Patriot | King Eitri | none  | - | yes |
| n480 | Scarlet Witch Queen of Chaos, King Eitri | Scarlet Witch Queen of Chaos | King Eitri | none  | - | yes |
| n481 | Valentina, King Eitri | Valentina | King Eitri | none  | - | yes |
| n482 | Shadowlands Daredevil, King Eitri | Shadowlands Daredevil | King Eitri | line creates cards | type: creates cards | yes |
| n483 | The Hunger, Zombie Giant-Man | The Hunger | Zombie Giant-Man | line more power | stronger: more power | yes |
| n484 | Zombie Scarlet Witch, Zombie Giant-Man | Zombie Scarlet Witch | Zombie Giant-Man | line more power | stronger: more power | yes |
| n485 | The Hunger, Zombie Mister Fantastic | The Hunger | Zombie Mister Fantastic | none  | - | yes |
| n486 | SP//dr, Peni Parker | SP//dr | Peni Parker | line merges onto it | waits: merges onto it for its effect | yes |
| n487 | SP//dr, Man-Spider | SP//dr | Man-Spider | line merges onto it | waits: merges onto it for its effect | yes |
| n488 | Peni Parker, Man-Spider | Peni Parker | Man-Spider | none  | - | yes |
| n489 | Super-Skrull, Astral Projection | Super-Skrull | Astral Projection | none copies keywords, gives no On Reveal | - | yes |
| n490 | High Evolutionary, Cosmo | High Evolutionary | Cosmo | none gives unnamed abilities, no On Reveal | - | yes |
| n491 | Basic Arrow, Mystique | Basic Arrow | Mystique | line makes your units get Ongoing | type: makes your units get Ongoing | yes |
| n492 | Grand Master, Invisible Woman | Grand Master | Invisible Woman | none moves your units; her rows read no move | - | yes |
| n493 | Wong, Shuri | Wong | Shuri | line plays it again | stronger: plays it again | yes |
| n494 | Zero, Ebony Maw | Zero | Ebony Maw | line silences it: its drawback is gone | waits: silences it: its drawback is gone | yes |
| n495 | Sauron, Ebony Maw | Sauron | Ebony Maw | line silence | rules: silence | yes |
| n496 | Zero, Hazmat | Zero | Hazmat | none  | - | yes |
| n497 | Brood, Absorbing Man | Brood | Absorbing Man | line On Reveal | type: is a unit with On Reveal it counts or asks for | yes |
| n498 | Silver Surfer, Absorbing Man | Silver Surfer | Absorbing Man | line On Reveal | type: is a unit with On Reveal it counts or asks for | yes |
| n499 | Hazmat, Absorbing Man | Hazmat | Absorbing Man | line On Reveal | type: is a unit with On Reveal it counts or asks for | yes |
| n500 | Magik, Absorbing Man | Magik | Absorbing Man | line On Reveal | type: is a unit with On Reveal it counts or asks for | yes |
| n501 | Wong, Absorbing Man | Wong | Absorbing Man | line On Reveal | stronger: plays it again | NO |
| n502 | Absorbing Man, Black Panther | Absorbing Man | Black Panther | line On Reveal | repeats: repeats its On Reveal effects | yes |
| n503 | Absorbing Man, Luna Snow | Absorbing Man | Luna Snow | line On Reveal | repeats: repeats its On Reveal effects | yes |
| n504 | Absorbing Man, Arnim Zola | Absorbing Man | Arnim Zola | line On Reveal | repeats: repeats its On Reveal effects | yes |
| n505 | Absorbing Man, Peni Parker | Absorbing Man | Peni Parker | line On Reveal | repeats: repeats its On Reveal effects | yes |
| n506 | Swarm, Morbius | Swarm | Morbius | line discard | type: comes back after it is discarded, to be discarded again | yes |
| n507 | Apocalypse, Morbius | Apocalypse | Morbius | line discard | type: comes back after it is discarded, to be discarded again | yes |
| n508 | Blade, Morbius | Blade | Morbius | line discard | type: makes you discard cards | yes |
| n509 | Swarm, Dracula | Swarm | Dracula | none  | - | yes |
| n510 | Storm, White Tiger | Storm | White Tiger | line  | type: stops cards being played, but a summon is not played: it still fills the p | yes |
| n511 | Storm, Doctor Doom | Storm | Doctor Doom | line  | type: stops cards being played, but a summon is not played: it still fills the p | yes |
| n512 | Storm, Odin | Storm | Odin | none  | - | yes |
| n513 | Ebony Maw, Doctor Doom | Ebony Maw | Doctor Doom | none  | - | yes |
| n514 | Wave, Death | Wave | Death | line makes it cheaper | cheaper: makes it cheaper | yes |
| n515 | Wave, Hulk | Wave | Hulk | line makes it cheaper | cheaper: makes it cheaper | yes |
| n516 | Wave, Ant Man | Wave | Ant Man | none  | - | yes |
| n517 | Moon Girl, The Collector | Moon Girl | The Collector | line creates cards | waits: creates cards | yes |
| n518 | Professor X, Devil Dinosaur | Professor X | Devil Dinosaur | line fills your hand | waits: fills your hand | yes |
| n519 | Agent 13, Devil Dinosaur | Agent 13 | Devil Dinosaur | line  | waits: fills your hand | yes |
