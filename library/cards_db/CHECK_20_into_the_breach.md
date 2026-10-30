# Stored rows of 20 cards (check_table.py)

Each card: its name and text on one line, then its stored rows, one row per effect, then the rows of each keyword it has.
- ability: one numbered "when -> if -> do" unit of the card. Rows with the same ability number are one ability; they happen together, in effect order.
- effect: the step inside the ability. link says how a step joins the step before it: and = also; then = after it, using its result; if_done = only if it happened; or = instead (a choice); instead = replaces it.
- pick=it in a target = the thing the step before acted on (the drawn card, the summoned unit, the chosen enemy).
- A row labelled "keyword X" is what keyword X does; the card has it, so the card does it too.
- Targets, events, conditions and amounts are written in place as their stored fields.

**Centipede Leader**: Health 7, move 3. Weapons/skills: Caustic Vomit: Launch a volatile mass of goo for 3 damage, applying A.C.I.D. on nearby units and all tiles it passes through.. Special: Massive: Massive units can walk in Water (but Water will prevent attacking or repairing).. The Centipede leader fires a projectile goo that damages the tile and the two nearby ones perpendicular to its direction, acidifying both the damaged tiles and all tiles that it passes through. (keywords: Massive)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self |  |  |  | 0 | damage | kind=unit_or_structure pick=nearest with[position is straight_line of (pick=self)] |  |  |  |  |  | amount=3 |  |  |
| 0 | attacks | pick=self |  |  |  | 1 | give_keyword | kind=unit_or_structure pick=all with[position in same_space of (pick=it); position in sides of (pick=it)] |  |  |  | A.C.I.D. |  |  | permanent | and |
| 0 | attacks | pick=self |  |  |  | 2 | give_keyword | kind=position pick=all with[position is straight_line of (pick=self)] |  |  |  | A.C.I.D. |  |  | permanent | and |
| 1 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Massive |  |  | permanent |  |
| keyword Massive: 0 | always |  |  |  |  | 0 | can | pick=self | kind=position with[terrain is ocean] |  |  |  |  | event=moves | while |  |
| keyword Massive: 1 | always |  |  |  | (test=have of=(pick=self with[position is same_space of (kind=position with[terrain is ocean])]) op=is) | 0 | cant | pick=self |  |  |  |  |  | event=attacks | while |  |

**Quick-Fire Mech**: Health 2, move 4. Weapon: Quick-Fire Rockets: Fire two projectiles in different directions. Damage: 1. Power: Free. Upgrades: Add Push (1 Reactor Core): Will now push both targets; +1 Damage (3 Reactor Cores): +1 damage to both targets.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self |  |  |  | 0 | damage | kind=unit_or_structure pick=nearest n=2 with[position is straight_line of (pick=self)] |  |  |  |  |  | amount=1 |  |  |
| 1 | attacks | pick=self |  |  | (test=upgraded n=1) | 0 | move | kind=unit_or_structure pick=nearest n=2 with[position is straight_line of (pick=self)] | kind=position with[position is bordering of (kind=unit_or_structure pick=nearest n=2 with[position is straight_line of (pick=self)])] |  |  |  |  |  |  |  |
| 2 | attacks | pick=self |  |  | (test=upgraded n=2) | 0 | damage | kind=unit_or_structure pick=nearest n=2 with[position is straight_line of (pick=self)] |  |  |  |  |  | amount=1 |  |  |

**Hook Mech**: Keywords: Natural Armor. Health 3, move 3. Weapon: Grappling Hook: Use a grapple to pull Mech towards immovable objects, or units to the Mech. Power: Free. Upgrades: Shield Ally (1 Reactor Core): If used on an ally unit it gives them a Shield. (keywords: Natural Armor)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self |  |  |  | 0 | move | kind=unit_or_structure pick=nearest with[position is straight_line of (pick=self); keyword not Stable] | kind=position with[position is bordering of (pick=self)] |  |  |  |  |  |  |  |
| 0 | attacks | pick=self |  |  |  | 1 | move | pick=self | kind=position with[position is bordering of (kind=unit_or_structure pick=nearest with[position is straight_line of (pick=self); keyword is Stable])] |  |  |  |  |  |  | or |
| 1 | attacks | pick=self |  |  | (test=upgraded n=1) | 0 | give_keyword | kind=unit side=mine pick=nearest with[position is straight_line of (pick=self)] |  |  |  | Energy Shield |  |  | permanent |  |
| keyword Natural Armor: 0 | damaged |  | pick=self |  | (test=it_matches of=( with[origin is weapon])) | 0 | damage_reduction | pick=self |  |  |  |  |  | amount=1 |  |  |

**Emerging**: Vek will emerge here next turn. Any unit blocking this space will take one damage.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | turn_start |  |  | next_time |  | 0 | summon | kind=unit side=enemy | kind=position with[position is same_space of (pick=self)] | board |  |  |  |  |  |  |
| 0 | turn_start |  |  | next_time |  | 1 | damage | kind=unit pick=all with[position is same_space of (pick=self)] |  |  |  |  |  | amount=1 |  | and |

**Alpha Hornet**: Health 4, move 5. Weapons/skills: Launching Stinger: Stab 2 tiles in front of the unit for 2 damage.. Special: Flying: Flying units can move over any terrain tile.. The stronger variant of the regular Hornet with more health, damage and range. Flying mobility lets it move freely through mountains, cities and the players units. It cannot be drowned, so has to be killed through damage and damaging effects instead. (keywords: Flying)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self |  |  |  | 0 | damage | kind=unit_or_structure pick=all with[position is ahead of (pick=self); distance le 2 of (pick=self)] |  |  |  |  |  | amount=2 |  |  |
| 1 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Flying |  |  | permanent |  |
| keyword Flying: 0 | always |  |  |  |  | 0 | can | pick=self | kind=position with[terrain not mountain; state is empty] |  |  |  |  | event=moves | while |  |
| keyword Flying: 0 | always |  |  |  |  | 1 | cant | pick=self |  |  |  | Submerged |  | event=given_keyword | while | and |
| keyword Flying: 0 | always |  |  |  |  | 2 | cant | pick=self |  |  |  | A.C.I.D. |  | event=given_keyword | while | and |

**Spring-Loaded Legs**: Leap and attack a tile (next to your landing point), dealing damage and pushing it. Damage: 2. Power: 1 Reactor Core. Upgrades: +2 Range (1 Reactor Core): Leap up to 4 tiles away; +2 Damage (3 Reactor Cores): Increase damage to the target by 2.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self |  |  |  | 0 | move | pick=self | kind=position pick=chosen with[distance le 2 of (pick=self)] |  |  |  |  |  |  |  |
| 0 | attacks | pick=self |  |  |  | 1 | damage | kind=unit_or_structure pick=chosen with[position is bordering of (pick=self)] |  |  |  |  |  | amount=2 |  | and |
| 0 | attacks | pick=self |  |  |  | 2 | move | pick=it | kind=position with[position is bordering of (pick=it)] |  |  |  |  |  |  | and |
| 1 | attacks | pick=self |  |  | (test=upgraded n=1) | 0 | can | pick=self | kind=position with[distance le 4 of (pick=self)] |  |  |  |  | event=moves | while |  |
| 2 | attacks | pick=self |  |  | (test=upgraded n=2) | 0 | damage | kind=unit_or_structure pick=chosen with[position is bordering of (pick=self)] |  |  |  |  |  | amount=2 |  |  |

**Alpha Bouncer**: Health 4, move 3. Weapons/skills: Powered Horns: Deal 3 damage to the target then bounce backwards.. Bouncers attack one tile in front of them, much like a Hornet without flight. What differentiates the Bouncer is that it will push the target tile and push themselves back by 1 tile, potentially resulting in a chain of collisions.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self |  |  |  | 0 | damage | kind=unit_or_structure pick=chosen with[position is in_front of (pick=self)] |  |  |  |  |  | amount=3 |  |  |
| 0 | attacks | pick=self |  |  |  | 1 | move | pick=it | kind=position with[position is bordering of (pick=it)] |  |  |  |  |  |  | and |
| 0 | attacks | pick=self |  |  |  | 2 | move | pick=self | kind=position with[position is behind of (pick=self)] |  |  |  |  |  |  | and |

**Raining Death**: A dangerous projectile that damages everything it passes. Damage: 2 (1 to self). Power: Free. Upgrades: Buildings Immune (1 Reactor Core): This attack will no longer damage Grid Buildings; +1 Damage Each (2 Reactor Cores): Increases damage to self and targets by 1.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self |  |  |  | 0 | damage | kind=unit_or_structure pick=all with[position is straight_line of (pick=self)] |  |  |  |  |  | amount=2 |  |  |
| 0 | attacks | pick=self |  |  |  | 1 | damage | pick=self |  |  |  |  |  | amount=1 |  | and |
| 1 | attacks | pick=self |  |  | (test=upgraded n=1) | 0 | cant | pick=self | kind=landmark side=mine |  |  |  |  | event=strikes | while |  |
| 2 | attacks | pick=self |  |  | (test=upgraded n=2) | 0 | damage | kind=unit_or_structure pick=all with[position is straight_line of (pick=self)] |  |  |  |  |  | amount=1 |  |  |
| 2 | attacks | pick=self |  |  | (test=upgraded n=2) | 1 | damage | pick=self |  |  |  |  |  | amount=1 |  | and |

**Alpha Beetle**: Health 5, move 2. Weapons/skills: Sharpened Pincers: Charge forward to deal 3 damage and push the target.. The Alpha Beetle charges forward in a line, dealing 3 damage and pushing the first target it hits.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self |  |  |  | 0 | move | pick=self | kind=position with[position is straight_line of (pick=self)] |  |  |  |  |  |  |  |
| 0 | attacks | pick=self |  |  |  | 1 | damage | kind=unit_or_structure pick=nearest with[position is straight_line of (pick=self)] |  |  |  |  |  | amount=3 |  | and |
| 0 | attacks | pick=self |  |  |  | 2 | move | pick=it | kind=position with[position is bordering of (pick=it)] |  |  |  |  |  |  | and |

**Techno-Scarab**: Health 2, move 3. Weapon: Explosive Goo: Artillery attack that damages a tile and pushes adjacent tiles away. Damage: 1. Power: Free. Upgrades: +1 Tile (1 Reactor Core): Increases area hit by 1 tile; +2 Damage (3 Reactor Cores): Increases damage by 2.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self |  |  |  | 0 | damage | kind=unit_or_structure pick=chosen with[position is straight_line of (pick=self)] |  |  |  |  |  | amount=1 |  |  |
| 0 | attacks | pick=self |  |  |  | 1 | move | kind=unit_or_structure pick=all with[position is bordering of (pick=it)] | kind=position with[position is bordering of (kind=unit_or_structure pick=all with[position is bordering of (pick=it)])] |  |  |  |  |  |  | and |
| 1 | attacks | pick=self |  |  | (test=upgraded n=1) | 0 | increase_effect | pick=self |  |  |  |  |  | area=1 |  |  |
| 2 | attacks | pick=self |  |  | (test=upgraded n=2) | 0 | damage | kind=unit_or_structure pick=chosen with[position is straight_line of (pick=self)] |  |  |  |  |  | amount=2 |  |  |

**Tentacles**: The unit here will die and the tile will turn into Lava.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | turn_start | kind=player side=enemy |  | next_time |  | 0 | kill | kind=unit pick=all with[position is same_space of (pick=self)] |  |  |  |  |  |  |  |  |
| 0 | turn_start | kind=player side=enemy |  | next_time |  | 1 | set_terrain | pick=self | kind=position with[terrain is lava] |  |  |  |  |  |  | and |

**Meteor Mech**: Health 3, move 3. Weapon: Vulcan Artillery: Light the target on Fire and push adjacent tiles. Damage: 0. Power: Free. Upgrades: Backburn (1 Reactor Core): Light the tile behind the Mech on Fire; +2 Damage (3 Reactor Cores): Adds 2 damage to targeted tiles.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self |  |  |  | 0 | give_keyword | kind=unit_or_structure pick=chosen with[position is straight_line of (pick=self)] |  |  |  | Fire |  |  | permanent |  |
| 0 | attacks | pick=self |  |  |  | 1 | move | kind=unit_or_structure pick=all with[position is bordering of (pick=it)] | kind=position with[position is bordering of (kind=unit_or_structure pick=all with[position is bordering of (pick=it)])] |  |  |  |  |  |  | and |
| 1 | attacks | pick=self |  |  | (test=upgraded n=1) | 0 | give_keyword | kind=position with[position is behind of (pick=self)] |  |  |  | Fire |  |  | permanent |  |
| 2 | attacks | pick=self |  |  | (test=upgraded n=2) | 0 | damage | kind=unit_or_structure pick=chosen with[position is straight_line of (pick=self)] |  |  |  |  |  | amount=2 |  |  |

**Alpha Scarab**: Health 4, move 3. Weapons/skills: Spitting Glands: Lob a powerful artillery shot at a single tile for 3 damage (5 tile range).. Alpha Scarabs are shaped like soft-shelled beetles. They attack similarly to artillery style Mech weapons. Alpha Scarabs will aim in a straight line at a tile and shoot over any tiles in between them and their target.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self |  |  |  | 0 | damage | kind=unit_or_structure pick=chosen with[position is straight_line of (pick=self); distance le 5 of (pick=self)] |  |  |  |  |  | amount=3 |  |  |

**Mine-Mech**: Health 1, move 0. Weapons/skills: Minelayer: Deploy a single Freeze mine.. Special: Mine Immunity: This unit avoids mines. | Smoke Immunity: This unit is unaffected by Smoke.. (keywords: Mine Immunity, Smoke Immunity)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self |  |  |  | 0 | summon |  | kind=position pick=chosen | board | Freeze Mine |  |  |  |  |  |
| 1 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Mine Immunity |  |  | permanent |  |
| 1 | always |  |  |  |  | 1 | give_keyword | pick=self |  |  |  | Smoke Immunity |  |  | permanent | and |
| keyword Mine Immunity: 0 | always |  |  |  |  | 0 | cant | pick=self |  |  |  |  |  | event=trap_activated | while |  |
| keyword Smoke Immunity: 0 | always |  |  |  |  | 0 | cant | pick=self |  |  |  | Smoke |  | event=given_keyword | while |  |

**Cannon Mech**: Health 3, move 3. Weapon: Taurus Cannon: Fires a powerful projectile that damages and pushes its target. Damage: 1. Power: Free. Upgrades: +1 Damage (2 Reactor Cores): Increases damage by 1; +1 Damage (3 Reactor Cores): Increases damage by 1.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self |  |  |  | 0 | damage | kind=unit_or_structure pick=nearest with[position is straight_line of (pick=self)] |  |  |  |  |  | amount=1 |  |  |
| 0 | attacks | pick=self |  |  |  | 1 | move | pick=it | kind=position with[position is bordering of (pick=it)] |  |  |  |  |  |  | and |
| 1 | attacks | pick=self |  |  | (test=upgraded n=1) | 0 | damage | kind=unit_or_structure pick=nearest with[position is straight_line of (pick=self)] |  |  |  |  |  | amount=1 |  |  |
| 2 | attacks | pick=self |  |  | (test=upgraded n=2) | 0 | damage | kind=unit_or_structure pick=nearest with[position is straight_line of (pick=self)] |  |  |  |  |  | amount=1 |  |  |

**Alpha Mosquito**: Health 4, move 4. Weapons/skills: Storm Tentacles: Smoke the target, preparing to whip it for 3 damage.. Special: Flying: Flying units can move over any terrain tile.. As a flying enemy with 4 health, the Mosquito is similar to the Alpha Hornet, trading 1 point of movement and the ability to attack 2 tiles for the ability to apply Smoke to the target tile and damage for three points. Mosquitoes and their alpha variant cannot spawn on an island with any other flying Vek (Hornet, Moth) other than the island's Psion. (keywords: Flying)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self |  |  |  | 0 | give_keyword | kind=unit_or_structure pick=chosen with[position is bordering of (pick=self)] |  |  |  | Smoke |  |  | permanent |  |
| 0 | attacks | pick=self |  |  |  | 1 | damage | pick=it |  |  |  |  |  | amount=3 |  | and |
| 1 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Flying |  |  | permanent |  |
| keyword Flying: 0 | always |  |  |  |  | 0 | can | pick=self | kind=position with[terrain not mountain; state is empty] |  |  |  |  | event=moves | while |  |
| keyword Flying: 0 | always |  |  |  |  | 1 | cant | pick=self |  |  |  | Submerged |  | event=given_keyword | while | and |
| keyword Flying: 0 | always |  |  |  |  | 2 | cant | pick=self |  |  |  | A.C.I.D. |  | event=given_keyword | while | and |

**Repulse**: Push all adjacent tiles. Power: Free. Upgrades: Shield Self (1 Reactor Core): Creates a personal Shield when used; Shield Friendly (2 Reactor Cores): Shield adjacent ally or Building.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self |  |  |  | 0 | move | kind=unit_or_structure pick=all with[position is bordering of (pick=self)] | kind=position with[position is bordering of (kind=unit_or_structure pick=all with[position is bordering of (pick=self)])] |  |  |  |  |  |  |  |
| 1 | attacks | pick=self |  |  | (test=upgraded n=1) | 0 | give_keyword | pick=self |  |  |  | Energy Shield |  |  | permanent |  |
| 2 | attacks | pick=self |  |  | (test=upgraded n=2) | 0 | give_keyword | kind=unit_or_structure side=mine pick=all with[position is bordering of (pick=self)] |  |  |  | Energy Shield |  |  | permanent |  |

**Burrower**: Health 3, move 4. Weapons/skills: Spiked Carapace: Slam against 3 tiles in a row, hitting each for 1 damage.. Special: Burrower: This Vek will hide underground after taking one or more damage. | Stable : Cannot be moved by any weapon effect (Push, Teleport, etc.).. Burrowers move underground to arrive at their destination and bypass any obstacles, much like a Leaper minus the jumping. When emerging they attack a 3-tile wide area in front of them perpendicular to where they are facing. Upon taking any damage, they will cancel their attack and retreat underground, re-emerging elsewhere (within 4 tiles of where they retreated from) on their next turn. Burrowers can not end their move on top of Ice Tiles. Burrowers are Stable and thus cannot be pushed or moved with physical force, however they can still be relocated by the Control Mech's Control Shot weapon. (keywords: Burrower, Stable)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self |  |  |  | 0 | damage | kind=unit_or_structure pick=all with[position in same_space of (kind=position with[position is in_front of (pick=self)]); position in sides of (kind=position with[position is in_front of (pick=self)])] |  |  |  |  |  | amount=1 |  |  |
| 1 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Burrower |  |  | permanent |  |
| 1 | always |  |  |  |  | 1 | give_keyword | pick=self |  |  |  | Stable |  |  | permanent | and |
| keyword Burrower: 0 | damaged |  | pick=self |  |  | 0 | give_keyword | pick=self |  |  |  | Stealth |  |  | unstated |  |
| keyword Stable: 0 | always |  |  |  |  | 0 | cant | kind=unit pick=all zone=board | pick=self |  |  |  |  | event=moves | while |  |

**Ramming Speed**: Dash across the map, damaging and pushing the target tile. Damage: 1. Power: Free. Upgrades: Smoke Behind (1 Reactor Core): Tile behind you gains Smoke; +2 Damage (3 Reactor Cores): Increases damage by 2.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self |  |  |  | 0 | move | pick=self | kind=position with[position is straight_line of (pick=self)] |  |  |  |  |  |  |  |
| 0 | attacks | pick=self |  |  |  | 1 | damage | kind=unit_or_structure pick=nearest with[position is straight_line of (pick=self)] |  |  |  |  |  | amount=1 |  | and |
| 0 | attacks | pick=self |  |  |  | 2 | move | pick=it | kind=position with[position is bordering of (pick=it)] |  |  |  |  |  |  | and |
| 1 | attacks | pick=self |  |  | (test=upgraded n=1) | 0 | give_keyword | kind=position with[position is behind of (pick=self)] |  |  |  | Smoke |  |  | permanent |  |
| 2 | attacks | pick=self |  |  | (test=upgraded n=2) | 0 | damage | kind=unit_or_structure pick=nearest with[position is straight_line of (pick=self)] |  |  |  |  |  | amount=2 |  |  |

**Lily Reed**: Pilot ability: Impulsive: Gain +3 Move on first turn of every mission.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | turn_start | kind=player side=mine |  | once_per_game |  | 0 | stat_change | pick=self |  |  |  |  |  | movement=3 | this_round |  |

