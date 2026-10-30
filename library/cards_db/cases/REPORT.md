# Case tests: faeria

Made by `cases/run.py faeria`.
**123 of 123 cases pass.**

**Cases whose reason no line says any more (rewrite them): nfa03, nfa04, nfa06, nfa12**


## Mechanics (expected cards from the texts)

| case | question | expected | found | recall | extra | pass |
|---|---|---|---|---|---|---|
| mx01 | a trigger on another unit dying is other_death_trigger | 0 | 0 | 100% | 11 | yes |
| mx02 | moving enemy units is forced_movement | 0 | 0 | 100% | 38 | yes |
| mx03 | a plain draw is one form: zone deck_top, no pick top | 26 | 26 | 100% | 16 | yes |
| mx10 | damage to the enemy player is Nexus damage (kinds kept, v30) | 0 | 0 | 100% | 356 | yes |
| mx11 | moving or pushing units makes units move (positions change, v30) | 0 | 0 | 100% | 150 | yes |
| fa01 | Gift triggers | 122 | 122 | 100% | 133 | yes |
| fa02 | Last Words triggers | 32 | 32 | 100% | 0 | yes |
| fa03 | Production triggers | 18 | 18 | 100% | 0 | yes |
| fa04 | Combat triggers | 17 | 17 | 100% | 0 | yes |
| fa05 | Corrupt triggers | 14 | 14 | 100% | 0 | yes |
| fa06 | Activate abilities | 11 | 11 | 100% | 8 | yes |
| fa07 | end of your turn | 11 | 11 | 100% | 10 | yes |
| fa08 | rewards attacking a god | 10 | 10 | 100% | 2 | yes |
| fa09 | harvest triggers | 8 | 8 | 100% | 2 | yes |
| fa10 | Flying | 63 | 63 | 100% | 12 | yes |
| fa11 | Charge | 33 | 33 | 100% | 15 | yes |
| fa12 | Jump | 23 | 23 | 100% | 9 | yes |
| fa13 | Dash | 25 | 25 | 100% | 3 | yes |
| fa14 | Taunt | 22 | 22 | 100% | 9 | yes |
| fa15 | Haste | 9 | 9 | 100% | 5 | yes |
| fa16 | Protection | 7 | 7 | 100% | 5 | yes |
| fa17 | Ranged Attack | 8 | 8 | 100% | 2 | yes |
| fa18 | Divine | 6 | 6 | 100% | 3 | yes |
| fa19 | Deathtouch | 5 | 5 | 100% | 1 | yes |
| fa20 | Aquatic | 6 | 6 | 100% | 0 | yes |
| fa21 | swallows a creature | 6 | 6 | 100% | 4 | yes |
| fa22 | discovers a card | 9 | 9 | 100% | 0 | yes |
| fa23 | makes cards wild | 15 | 15 | 100% | 0 | yes |
| fa24 | gains faeria | 22 | 22 | 100% | 4 | yes |
| fa25 | cheaper cards | 37 | 37 | 100% | 8 | yes |
| fa26 | stat buffs | 126 | 126 | 100% | 24 | yes |
| fa27 | creates or changes lands | 12 | 12 | 100% | 6 | yes |
| fa28 | counts my lands of a colour | 9 | 9 | 100% | 9 | yes |
| fa29 | adjacent things | 45 | 45 | 100% | 31 | yes |
| fa30 | damage to the enemy god | 11 | 11 | 100% | 35 | yes |
| fa31 | transforms a creature | 6 | 6 | 100% | 3 | yes |
| fa32 | fights | 3 | 3 | 100% | 1 | yes |
| fa33 | teleports | 4 | 4 | 100% | 38 | yes |
| fa34 | summons units | 20 | 20 | 100% | 20 | yes |
| fa35 | draws cards | 26 | 26 | 100% | 16 | yes |
| mx12 | a unit that moves (onto a space) is the event's object, never its actor (N16, Sentry, v36, v38) | 0 | 0 | 100% | 18 | yes |
| mx13 | can't be targeted by spells: the cant is on the spells, the protected unit is "to" (N19, v37) | 0 | 0 | 100% | 0 | yes |
| mx14 | a dead unit put into play is revive, never summon from the discard (N20, v37) | 0 | 0 | 100% | 0 | yes |
| mx15 | a trigger that holds only "this turn" is an ability given to the player for this turn (v37, Duelyst) | 0 | 0 | 100% | 2 | yes |
| fa36 | placement: where a unit may be summoned | 7 | 7 | 100% | 1 | yes |
| fa37 | taking a land | 1 | 1 | 100% | 1 | yes |
| fa38 | reward for harvesting enemy wells | 5 | 5 | 100% | 0 | yes |
| fa39 | area shapes (on or adjacent to a space) | 2 | 2 | 100% | 0 | yes |
| fa40 | counts my lands | 10 | 10 | 100% | 57 | yes |
| fa41 | neighbours in a trigger | 3 | 3 | 100% | 73 | yes |
| fa42 | Corrupt is entering enemy territory | 14 | 14 | 100% | 4 | yes |
| fa43 | a trigger label written "Corrupt -" is the card's keyword | 14 | 14 | 100% | 0 | yes |
| mx13 | an effect on the creature opposing it is about lanes (concept lanes from same_lane, v38) | 0 | 0 | 100% | 0 | yes |
| mx14 | a strike on the spaces beside the opposing one reaches other lanes (cross_lane, v38) | 0 | 0 | 100% | 0 | yes |
| mx15 | within a circuit is a formation (link_formation, v38) | 0 | 0 | 100% | 0 | yes |
| mx16 | more or faster base resource (base_resource_gain, v38) | 0 | 0 | 100% | 25 | yes |

## Combos (the enabler must set off the payoff)

| case | enabler | payoff | why | found as | pass |
|---|---|---|---|---|---|
| cfa01 | Feed the Forest | Oakling | destroying Oakling triggers its Last Words and gains faeria | event: kill -> dies | yes |
| cfa02 | Feed the Forest | Ruunin, the Relentless | each death returns Ruunin bigger; Feed the Forest turns her Life into faeria | state: dies | yes |
| cfa03 | Feed the Forest | Tarum, the Forest World | destroying Tarum gains faeria and its Last Words fills the world with forests | event: kill -> dies | yes |
| cfa05 | Doomsday | Soul Eater | Doomsday destroys every creature; each friendly death grows Soul Eater in hand | condition: kill -> dies | yes |
| cfa06 | Doomgate, Door to Oblivion | Annoying Gnat | sacrificing the Gnat draws a card; its Last Words summons it again | event: kill -> dies | yes |
| cfa07 | Famine | Ruby Yak | Famine damages every Yak; Ruby Yak hits the opponent once for each damaged Yak | event: damage -> damaged | yes |
| cfa08 | Ulani's Medallion | Ruby Yak | the Medallion turns your other creatures into copies of Ruby Yak | copies: turns my units into copies of it | yes |
| cfa09 | Rain of Fish | Ulani's Medallion | Rain of Fish fills the board with creatures for the Medallion to copy | target: my units | yes |
| cfa10 | Ruunin, the Relentless | Shaytan Monstrosity | each time Ruunin dies, Monstrosity drains her Attack | trigger: dies | yes |
| cfa13 | Voice of Hunger | Eredon, Voice of All | the deck wins through the Voice of Hunger and Eredon combo | event: kill -> dies | yes |
| cfa14 | Famine | Plague Bearer | Famine is an extra trigger for Plague Bearer | event: damage -> dies | yes |
| cfa15 | Falcon Dive | Plague Bearer | Falcon Dive is an extra trigger for Plague Bearer | event: damage -> dies | yes |

## Region identity (signature, splash, archetype)

| case | region | kind | mechanic | need | found | pass |
|---|---|---|---|---|---|---|

## Guide decks (the explanation must say what the guide says)

| case | deck | must say | missing | pass |
|---|---|---|---|---|
| dfa01 | Midrange Sacrifice | your units die: made by demon wrangler, lord of the wastes;use it: soul eater | - | yes |
| dfa02 | Voice of Hunger Control | get value when they die: eredon, voice of all | - | yes |
| dfa03 | Bargain (Krog) | pays for big cards (more mana, cheaper cards): bold bargainer;krog, the ogre king | - | yes |
| dfa04 | Fast Rakoans | rakoan cards: are or make them | - | yes |
| dfa05 | Blue Yellow Events | spells you play:;set off: windstorm archer | - | yes |

## Deck networks (a line must be there, or must not)

| case | deck | from | to | expect | found | pass |
|---|---|---|---|---|---|---|
| nfa01 | Beastmaster Green | Oakling | Deepwood Stalker | line  | stronger: can give it +5|+5; stronger: more power: it hits harder | yes |
| nfa02 | Red Archers | Gift of Steel | Hilltop Archer | line  | stronger: can give it +3|+0; stronger: more power: it hits harder | yes |
| nfa03 | Fast Rakoans | Rakoan Illusionist | Imperial Trooper | none onto | - | yes |
| nfa04 | Fast Rakoans | Airbot | Imperial Trooper | none onto | moves: moves my units or land forward: they reach enemy ground | yes |
| nfa05 | Beastmaster Green | Time of Legends | Eredon, Voice of All | line puts: | puts: draws it from the deck | yes |
| nfa06 | Beastmaster Green | The Emperor's Command | Feed the Forest | none heals | - | yes |
| nfa07 | Blue Jump | Wavecrash Colossus | Gabrian Commander | line  | waits: is a card it counts when drawn | yes |
| nfa08 | Blue Jump | Ninja Toad | Gabrian Commander | none  | - | yes |
| nfa09 | Yellow Flyers | Windborne Champion | Drakkar Skycaptain | none get Flying | - | yes |
| nfa10 | Bargain (Krog) | Krog's Dinner | Krog, the Ogre King | line cheaper: | cheaper: makes it cheaper; cheaper: pays for it: more mana or a lower cost; puts | yes |
| nfa11 | Bargain (Krog) | Bold Bargainer | Ogre Dance | none  | - | yes |
| nfa12 | Red Combat | Garudan, Heart of the Mountain | Bomb Slinger | none enemy units move | moves: moves my units or land forward: it can enter where it needs to be | yes |
| nfa13 | Yellow Flyers | Celestial Tower | Khalim, Sky Prodigy | line  | keyword: can give it Charge; moves: moves it within reach of the enemy player | yes |
| nfa14 | Red Blue Mobility Burn | Syland Horsemaster | Grim Guard | line  | keyword: can give it Charge; moves: moves it where it must be | yes |
| nfa15 | Voice of Hunger Control | Time of Legends | Voice of Hunger | none enter | - | yes |
| nfa16 | Midrange Sacrifice | Iona's Smile | Soul Eater | line  | puts: draws it from the deck | yes |
| nfa17 | Midrange Sacrifice | Iona's Smile | Demon Wing | none draws it | - | yes |
| nfa18 | Voice of Hunger Control | Voice of Hunger | Eredon, Voice of All | line  | waits: kills it for its death effect | yes |
| nfa19 | Beastmaster Green | Oakling | Grove Guardian | line stronger: | stronger: can give it +5|+5 | yes |
| nfa20 | Yellow Monstrosity | Khalim's Training | Manta Rider | line stronger: | stronger: can give it +1|+0 | yes |
| nfa21 | Red Combat | Syland Horsemaster | Bomb Slinger | line moves: | keyword: can give it Charge; moves: moves my units or land forward: it can enter | yes |
| nfa22 | Red Archers | Flame Burst | Hilltop Archer | line clears: | clears: clears its line of fire | yes |
| nfa23 | Bargain (Krog) | Red Devil | Krog, the Ogre King | line cheaper: | cheaper: pays for it: more mana or a lower cost | yes |
| nfa24 | Bargain (Krog) | Krog, the Ogre King | Krog's Dinner | none  | - | yes |
| nfa25 | Yellow Monstrosity | Soul Drain | Shaytan Monstrosity | none your units die | - | yes |
| nfa26 | Yellow Monstrosity | Flash Wind | Mistral Guide | line moves: | moves: moves it where the units summoned next to it are needed | yes |
| nfa27 | Blue Jump | Battle Toads | Wavecrash Colossus | line moves: | moves: moves my units or land forward: they reach enemy ground | yes |
| nfa28 | Blue Jump | Sunken Tower | Wavecrash Colossus | line moves: | moves: moves my units or land forward: they reach enemy ground | yes |
| nfa29 | Blue Jump | Gabrian Archon | Wavecrash Colossus | none stronger: | moves: moves my units or land forward: they reach enemy ground | yes |
| nfa30 | Bargain (Krog) | Bold Bargainer | Krog, the Ogre King | line cheaper: | cheaper: can make it cheaper; cheaper: pays for it: more mana or a lower cost | yes |
| nfa31 | Blue Yellow Events | Shifting Tide | Windstorm Colossus | none type: | waits: is a card it counts when played; waits: is a spell it counts | yes |
| nfa32 | Yellow Monstrosity | Manta Rider | Windborne Emissary | none waits: | type: has Flying; type: is a unit with Flying it counts or asks for; type: makes | yes |
| nfa33 | Red Combat | Underground Boss | Bomb Slinger | none  | - | yes |
| nfa34 | Red Blue Mobility Burn | Seifer, Blood Tyrant | Gabrian Enchantment | none  | - | yes |
| nfa35 | Red Blue Mobility Burn | Gift of Steel | Gabrian Enchantment | line stronger: | stronger: more health | yes |
| nfa36 | Midrange Sacrifice | Demon Wing | Soul Eater | none  | - | yes |
| nfa37 | Midrange Sacrifice | Lord of the Wastes | Soul Eater | line waits: makes your units die | waits: makes your units die | yes |
| nfa38 | Midrange Sacrifice | Lord of the Wastes | Village Elder | line waits: kills it for its death effect | waits: kills it for its death effect | yes |
| nfa39 | Bargain (Krog) | Krog's Dinner | Meteor | none  | - | yes |
| nfa40 | Voice of Hunger Control | Falcon Dive | Plague Bearer | line waits: kills it for its death effect | waits: kills it for its death effect | yes |
| nfa41 | Yellow Monstrosity | Manta Rider | Windborne Emissary | line type: | type: has Flying; type: is a unit with Flying it counts or asks for; type: makes | yes |
| nfa42 | Blue Yellow Events | Shifting Tide | Windstorm Colossus | line waits: | waits: is a card it counts when played; waits: is a spell it counts | yes |
| nfa43 | Bargain (Krog) | Bold Bargainer | Krog, the Ogre King | none stronger: | cheaper: can make it cheaper; cheaper: pays for it: more mana or a lower cost | yes |
| nfa44 | Red Combat | Underground Brigand | Bomb Slinger | none  | - | yes |
| nfa45 | Red Blue Mobility Burn | Gift of Steel | Gabrian Enchantment | none waits: | stronger: more health | yes |
| nfa46 | Midrange Sacrifice | Village Elder | Soul Eater | none  | - | yes |
| nfa47 | Midrange Sacrifice | Wind Soldier | Soul Eater | line waits: | waits: dies by its own effect | yes |
| nfa48 | Bargain (Krog) | Krog's Dinner | Ogre Battler | none  | - | yes |
| nfa49 | Yellow Monstrosity | Khalim's Training | Windborne Emissary | line type: | stronger: can give it +1|+0; type: makes your units get Flying | yes |
| nfa50 | Voice of Hunger Control | Falcon Dive | Eredon, Voice of All | none death effect | - | yes |
