# Case tests: faeria

Made by `cases/run.py faeria`.
**82 of 82 cases pass.**


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
| mx12 | a unit that moves is the event's object, never its actor (N16, Sentry, v36) | 0 | 0 | 100% | 2 | yes |
| mx13 | can't be targeted by spells: the cant is on the spells, the protected unit is "to" (N19, v37) | 0 | 0 | 100% | 0 | yes |
| mx14 | a dead unit put into play is revive, never summon from the discard (N20, v37) | 0 | 0 | 100% | 0 | yes |
| mx15 | a trigger that holds only "this turn" is an ability given to the player for this turn (v37, Duelyst) | 0 | 0 | 100% | 2 | yes |
| fa36 | placement: where a unit may be summoned | 7 | 7 | 100% | 16 | yes |
| fa37 | taking a land | 1 | 1 | 100% | 1 | yes |
| fa38 | reward for harvesting enemy wells | 5 | 5 | 100% | 0 | yes |
| fa39 | area shapes (on or adjacent to a space) | 2 | 2 | 100% | 118 | yes |
| fa40 | counts my lands | 10 | 10 | 100% | 57 | yes |
| fa41 | neighbours in a trigger | 3 | 3 | 100% | 73 | yes |
| fa42 | Corrupt is entering enemy territory | 14 | 14 | 100% | 4 | yes |
| fa43 | a trigger label written "Corrupt -" is the card's keyword | 14 | 14 | 100% | 0 | yes |

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
| cfa10 | Ruunin, the Relentless | Shaytan Monstrosity | each time Ruunin dies, Monstrosity drains her Attack | condition: stat_changed | yes |
| cfa13 | Voice of Hunger | Eredon, Voice of All | the deck wins through the Voice of Hunger and Eredon combo | event: kill -> dies | yes |
| cfa14 | Famine | Plague Bearer | Famine is an extra trigger for Plague Bearer | event: damage -> dies | yes |
| cfa15 | Falcon Dive | Plague Bearer | Falcon Dive is an extra trigger for Plague Bearer | event: damage -> dies | yes |

## Region identity (signature, splash, archetype)

| case | region | kind | mechanic | need | found | pass |
|---|---|---|---|---|---|---|

## Guide decks (the explanation must say what the guide says)

| case | deck | must say | missing | pass |
|---|---|---|---|---|

## Deck networks (a line must be there, or must not)

| case | deck | from | to | expect | found | pass |
|---|---|---|---|---|---|---|
| nfa01 | Beastmaster Green | Oakling | Deepwood Stalker | line  | boosts: more power: it hits harder | yes |
| nfa02 | Red Archers | Gift of Steel | Hilltop Archer | line  | boosts: more power: it hits harder | yes |
| nfa03 | Fast Rakoans | Rakoan Illusionist | Imperial Trooper | none moves | - | yes |
| nfa04 | Fast Rakoans | Airbot | Imperial Trooper | none  | - | yes |
| nfa05 | Beastmaster Green | Time of Legends | Eredon, Voice of All | line  | puts: draws it from the deck | yes |
| nfa06 | Beastmaster Green | The Emperor's Command | Feed the Forest | none healed | waits: any units have their stats changed | yes |
| nfa07 | Blue Jump | Wavecrash Colossus | Gabrian Commander | line  | waits: is a card it counts when drawn | yes |
| nfa08 | Blue Jump | Ninja Toad | Gabrian Commander | none  | - | yes |
| nfa09 | Yellow Flyers | Windborne Champion | Drakkar Skycaptain | none get Flying | waits: is a card it counts when drawn | yes |
| nfa10 | Bargain (Krog) | Krog's Dinner | Krog, the Ogre King | line  | boosts: makes it cheaper; puts: draws it from the deck | yes |
| nfa11 | Bargain (Krog) | Bold Bargainer | Ogre Dance | none  | - | yes |
| nfa12 | Red Combat | Garudan, Heart of the Mountain | Bomb Slinger | none move | - | yes |
| nfa13 | Yellow Flyers | Celestial Tower | Khalim, Sky Prodigy | line  | boosts: moves it within reach of the enemy player | yes |
| nfa14 | Red Blue Mobility Burn | Syland Horsemaster | Grim Guard | line  | boosts: moves it where it must be | yes |
| nfa15 | Voice of Hunger Control | Time of Legends | Voice of Hunger | none enter | - | yes |
| nfa16 | Midrange Sacrifice | Iona's Smile | Soul Eater | line  | puts: draws it from the deck | yes |
| nfa17 | Midrange Sacrifice | Iona's Smile | Demon Wing | none draws it | - | yes |
| nfa18 | Voice of Hunger Control | Voice of Hunger | Eredon, Voice of All | line  | waits: your units die | yes |
