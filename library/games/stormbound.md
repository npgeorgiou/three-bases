# Stormbound

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*Claude's summary (Oct 2026), from general knowledge of the game and the rules and terms under Mechanics; not from the sources below.*
- Genre: digital card game (Paladin Studios, 2017) on a grid with a base at each end; the rules and terms are listed in full under Mechanics.
- Board: units move forward along their column at the start of each turn; cards can only be played up to the front line.
- Mana: the first player starts with 3, the second with 4, and mana grows by 1 per turn.
- Hand: 4 cards, one cycled per turn; decks are 12 cards of Neutral plus one faction.
- Win: bring the enemy base to 0.

## Sources and notes

Sources:
[1] https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html (all four factions)
[2] https://stormboundkingdomwars.fandom.com/wiki/Winter_Pact?oldid=7023
[3] https://stormboundkingdomwars.fandom.com/wiki/Swarm_of_the_East?oldid=4049

Neutral is a filler class [1], not a faction. The wiki pages for Ironclad Union and Shadowfen could not be read.

## Factions

### Winter
*Claude:* Winter Pact: freezing and Frostlings.
Known for: control and attrition, Freeze, long games [1]; slow and controlling, extra mana, freezing enemies, big units that
finish the game; heavy area damage (Wisp Cloud, Midwinter Chaos) [2].
Weak at: no unit spawning, no early game [2].

### Swarm
*Claude:* Swarm of the East: satyrs and undead.
Known for: aggro, many weak units, summoning and strengthening units, Satyrs [1]; unit generation, high movement, direct
damage to the enemy base; undead that spawn, respawn or hit structures; satyrs that spawn and boost satyrs; self-damage
costs [3].
Weak at: the late game [1].

### Shadowfen
*Claude:* Shadowfen: poison, toads and ravens.
Known for: flooding the board with Toads, poison, diagonal damage, sacrifice-based poison skills, overwhelming numbers [1].

### Ironclad
*Claude:* Ironclad Union: constructs and dwarves, pushing and confusing units.
Known for: an aggro variant (Boosting Elixir buffs two units) and a control variant; area hits (Armed Schemers), knockback
(Windmakers) [1].

## Combos
- Wisp Cloud + Frosthexers: Frosthexers freeze all surrounding enemies, Wisp Cloud clears the board when hitting frozen
  targets [1]

## Mechanics
The mechanics the guides name, one per line as `name|concept|regex`, and the rules and terms as `# term:` lines. Read by `coverage.py --mechanics` and `key/key.py`.

```mechanics
# Mechanics the guides name: name|expected concept|wording on the cards. Checked with coverage.py --mechanics.
# https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html , fandom Winter Pact and Swarm pages
# Rules and terms for the game block (key.py read), only facts the source states: https://stormbound-kitty.com/rulebook
# term: Board: a grid of tiles in rows and columns with a base at each end; units move toward the enemy base along their column.
# term: Front line: the furthest row where a player can play cards, set by that player's units or structures on that row; it shifts during the battle.
# term: Movement: units move forward one tile at the start of each turn; a unit with initial movement moves right after being placed. If an enemy is in front, the unit attacks it instead of moving; units move sideways only when confused. A unit that reaches the enemy base damages it.
# term: Bases: a base has 10 to 20 health; the game ends when a base reaches 0.
# term: Mana: the first player starts with 3, the second with 4; mana grows by 1 each turn. Turn order: structures act, units move, the player plays cards.
# term: Hand: 4 cards; one card per turn can be cycled for a random card from the deck. Decks are 12 cards: Neutral plus one faction.
# term: Card types: units (move and attack), structures (immobile, act at turn start), spells (one-time effects). Token cards are created during a battle and cost 0. Cards level 1 to 5.
# term: Poisoned: takes 1 damage at the start of each turn until it dies or is vitalized.
# term: Vitalized: gains 1 strength at the start of each turn until it is poisoned.
# term: Frozen: can't move at the start of the next turn, and its ability is disabled for that turn.
# term: Confused: moves sideways randomly during its movement for one turn.
# term: Disabled: loses its ability until it dies.
# term: On play: triggers once when the card is placed. Before moving: Ancient units, before movement. Before attacking / after attacking: around the unit's attack, also when forced to attack. After surviving damage: Elder units, when they take damage and survive (strength reduction does not count). On death: when the unit is removed from the board, also by walking into the base.
# term: Positions: in front = the tile north; behind = south; sides = west and east; bordering = the four tiles north, south, east, west; surrounding = bordering plus the four diagonals; baseline = the row next to a player's base.
# term: Commanding: forces a unit to move forward, ignoring the attack pattern and enemies on its sides. Converting: switches a unit to the other side. Destroying: removes a target regardless of strength.
# term: Draining: damages one unit and gives the same amount of health to another. Forcing attack: makes a unit attack a bordering tile, usually randomly, triggering its attack abilities.
# term: Pulling: moves a unit toward another unit in the same row or column when nothing is between them. Pushing: moves a unit away along a row or column until it hits something; units can't be pushed into a base.
# term: Reducing strength: sets a unit's strength to a value; not damage. Spawning: creates a unit or structure at a location.
# term: Unit types (Raven, Construct ...) are mostly cosmetic, but some cards check them; Elder, Ancient and Hero are extra unit types.
freeze|disable|\bfreez|\bfrozen
mana gain|resource_gain|\bgain \d+ mana|\bmana\b
area damage|aoe_damage|\b(all|each) (enemy|enemies|units|surrounding)
poison|damage_over_time|\bpoison
toads|summon|\btoads?\b
spawn units|summon|\bspawn
base damage|direct_damage|\benemy base\b
movement|movement|\b(move|command|forward)\b
satyrs|tribal|\bsatyrs?\b
buffs|stat_gain|\b(give|gain)\b[^.]{0,40}\d+ strength
```

## Cases
The real-world cases, one per line, tab-separated: `type  a  b  why  source` (see `realworld/RESEARCH.md`). Read by `realworld.py`, `realworld_report.py`, `realworld_why.py` and `learn_recipes.py`.

```tsv
signature	Winter	disable	Freeze	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
signature	Winter	resource_gain	extra mana	https://stormboundkingdomwars.fandom.com/wiki/Winter_Pact?oldid=7023
signature	Winter	aoe_damage	heavy area damage	https://stormboundkingdomwars.fandom.com/wiki/Winter_Pact?oldid=7023
signature	Winter	high_cost	big units that finish the game	https://stormboundkingdomwars.fandom.com/wiki/Winter_Pact?oldid=7023
signature	Swarm	summon	unit generation	https://stormboundkingdomwars.fandom.com/wiki/Swarm_of_the_East?oldid=4049
signature	Swarm	board_presence	many weak units	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
signature	Swarm	buff	strengthening units on the board	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
signature	Swarm	direct_damage	direct damage to the enemy base	https://stormboundkingdomwars.fandom.com/wiki/Swarm_of_the_East?oldid=4049
signature	Swarm	movement	high movement	https://stormboundkingdomwars.fandom.com/wiki/Swarm_of_the_East?oldid=4049
signature	Swarm	tribal	Satyrs	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
signature	Swarm	life_payment	self-damage costs	https://stormboundkingdomwars.fandom.com/wiki/Swarm_of_the_East?oldid=4049
signature	Shadowfen	damage_over_time	poison	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
signature	Shadowfen	summon	Toads	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
signature	Shadowfen	tribal	Toads	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
signature	Shadowfen	sacrifice	sacrifice-based poison	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
signature	Ironclad	buff	Boosting Elixir	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
signature	Ironclad	forced_movement	knockback	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
archetype	Winter	control	control and attrition	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
archetype	Winter	ramp	extra mana for big units	https://stormboundkingdomwars.fandom.com/wiki/Winter_Pact?oldid=7023
archetype	Swarm	aggro_tempo	aggro	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
archetype	Swarm	swarm	many weak units	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
archetype	Swarm	tribal	Satyrs	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
archetype	Shadowfen	swarm	flooding the board	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
archetype	Shadowfen	tribal	Toads	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
archetype	Shadowfen	poison_attrition	poison wears down health	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
archetype	Ironclad	aggro_tempo	aggro variant	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
archetype	Ironclad	control	control variant	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
combo	Wisp Cloud	Frosthexers	freeze, then clear frozen targets	https://www.bluestacks.com/blog/game-guides/stormbound-kingdom-wars/sbkw-class-guide-en.html
```
