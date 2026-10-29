# Faeria keywords: the concept each is filed under (for Kaptain's check)

Made from vocab.tsv (the keyword rows) and library/tools/concept_tree_v3.txt, 29 Oct 2026. The concept choice is Claude's,
made from the keyword's definition (Abrakam's card export README and the faeria.com Keyword Rulings guide) and checked
against the concept's definition and its "not this" part. Flying, Jump and Aquatic as movement are Kaptain's (26 Oct 2026).

| keyword | what it does (the game's glossary) | concept | the concept means | not this |
|---|---|---|---|---|
| Gift | Triggers when the card is summoned. | on_play (When played (battlecry, on reveal)) | Triggers when the card is played or revealed: battlecry, on reveal, enters. | When another card is played is on_ally_play. |
| Last Words | Triggers when the creature or structure is destroyed. | death_trigger (When it dies (deathrattle)) | Effects when this unit dies or is destroyed: its own death. (Narrowed 20 Oct 2026, Kaptain's decision.) | Another unit dying is other_death_trigger; leaving play by other means is leave_trigger. |
| Production | Triggers at the start of each of its owner's turns. | turn_start (Start of turn / round) | Effects at the start of a turn or round. | End of turn is turn_end. |
| Combat | Triggers whenever it exchanges attacks with creatures, structures or the enemy orb (not when shot by a ranged creature). | on_fight (When it fights) | Triggers when the unit exchanges attacks with another unit, a structure or a player: when it attacks and when it is attacked, both hitting (Faeria Combat). (Added 29 Oct 2026, Claude's.) | Only when it attacks is on_attack; damage from anything is on_damaged. |
| Corrupt | Triggers the first time this creature moves onto enemy land, on a turn after it was played. | territory_trigger (In or entering enemy territory) | The effect fires or turns on when a unit enters or stands in enemy territory or a set zone: infiltrate. | When an enemy arrives on my side is on_enemy_enter. |
| Activate | Structures only: use the ability once per turn. | activated (Activated ability (pay to use)) | The player chooses when to use an ability: activate, tap, pay to use. | Abilities that fire on their own are triggers. |
| Flying | Can move over ocean and land, but not through creatures or structures. | movement (Move my units (reposition)) | The owner moves their own unit to another space, row, lane or location. | Moving enemy units is forced_movement. |
| Charge | Can move several spaces in a straight line. | movement (Move my units (reposition)) | The owner moves their own unit to another space, row, lane or location. | Moving enemy units is forced_movement. |
| Jump | Moves up to two tiles and can leap over obstacles, creatures and ocean. | movement (Move my units (reposition)) | The owner moves their own unit to another space, row, lane or location. | Moving enemy units is forced_movement. |
| Dash | When summoned, moves X spaces in a straight line. | movement (Move my units (reposition)) | The owner moves their own unit to another space, row, lane or location. | Moving enemy units is forced_movement. |
| Aquatic | Can only travel over lakes and ocean; drowns at end of turn on other land. | movement (Move my units (reposition)) | The owner moves their own unit to another space, row, lane or location. | Moving enemy units is forced_movement. |
| Taunt | Adjacent enemy creatures cannot move and can only attack the taunt. | taunt (Taunt (enemies must attack it)) | Enemies must attack or target this unit before other units. | Shielding one chosen ally is bodyguard. |
| Haste | Can move, attack and harvest the turn it is played. | haste (Act the turn it arrives (haste, rush)) | A unit can attack or act on the turn it is played. | An effect that makes it attack at once is attack_now. |
| Protection | Prevents all damage from the next damage source, then is removed. | shield (Absorb one hit (shield, ward)) | The next hit or damage instance is fully absorbed or cancelled. | Damage lowered by an amount is damage_reduction. |
| Discover | Creates a copy of a card. | selection (Look at cards and pick (scry)) | The owner looks at several cards and chooses which to keep, take or put back. | Searching the deck for a stated kind of card is tutor. |
| Ranged Attack | Shoots in a straight line with line of sight; takes no retaliation unless adjacent or shot by another ranged unit; cannot attack after moving normally. | ranged (Ranged attack / long reach) | The unit attacks from a distance, from the back row or over other units. | Damage from a spell is damage. |
| Divine | Cannot be targeted by spells or abilities from either player (still attackable and hit by area effects). | immunity (Immune / can't be targeted) | A unit can't be targeted, or is immune to a damage type, effect or condition. | Hard to block is evasion; hidden until it acts is stealth. |
| Deathtouch | Any creature it damages dies. | deathtouch (Any damage kills (deathtouch, poisonous)) | Any damage this unit deals destroys the unit it hits. | Destroying by an effect without combat damage is destroy. |
| Swallow | Removes a creature from the game until the swallower dies, then releases it. | banish (Banish / exile (gone for good)) | A unit or card is removed from the game for good, beyond the discard pile. | Leaving and coming back is blink. |
| Wild | A card is wild when all the lands it requires are wild: any land colours pay them, and a wild creature can be summoned on any of your lands, including prairies. | cost_type (Alternative costs) | A card can be paid with something other than the usual resource. | An optional extra payment for a bonus is kicker. |
| Fight | Your creature exchanges attacks with an enemy creature anywhere on the board; this does not count as the creature's attack for the turn. | attack_now (Attack right away) | An effect makes a unit attack at once, outside the normal attack step. | Being allowed to attack the turn it arrives is haste. |
| Teleport | Moves a creature to another tile; this does not count as the creature's movement for the turn. | movement (Move my units (reposition)) | The owner moves their own unit to another space, row, lane or location. | Moving enemy units is forced_movement. |
| Transform | Turns a creature into another; its stats return to the new card's printed values (buffs and damage are removed); it is not a summon. | transform (Transform my card into another) | The owner's own card or unit turns into a different one: evolve, flip, become. | Turning an enemy into something weaker is polymorph. |

New concepts this import added to the tree (Claude's): on_fight (Combat), on_harvest (harvesting a well).

Board values Faeria needed, now shared by every game with a board (BRIEF "The board"): terrain (land, ocean, prairie, lake,
forest, mountain, desert, special_land, resource_well), set_terrain, same_space, straight_line, distance, harvest /
harvests, moves_onto, empty_resource, refill_resource, state empty.
