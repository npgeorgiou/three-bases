# Into the Breach keywords: the concept each is filed under (for Kaptain's check)

Made from vocab.tsv (the keyword rows) and library/tools/concept_tree_v3.txt, 30 Oct 2026. The concept choice is Claude's,
made from the keyword's definition (read/into_the_breach/keywords.jsonl and the wiki texts) and checked twice against the
concept's definition and its "not this" part.
Second check (30 Oct 2026): every row read again against its concept and the "not this" part; Flying, Regeneration and Stealth
share another game's vocab row, so their Into the Breach meaning is written here. Alpha Unit and Minor describe no effect.

| keyword | what it does | concept | the concept means | not this |
|---|---|---|---|---|
| A.C.I.D. | weapon damage against this unit is doubled and its Natural Armor is off | debuff (Make a unit weaker (debuff)) | A unit loses stats or gets a combat penalty. | Stopping it from acting is suppress. |
| Alpha Unit | a label, the unit is a stronger version; describes no effect, no record | none (no effect) |  |  |
| Boost | the unit's next attack deals 1 more damage | temporary_buff (Temporary bonus (this turn only)) | A unit's bonus lasts only this turn, round or fight. | A bonus that stays is stat_gain or permanent_growth. |
| Burrower | the Vek hides underground after taking damage | stealth (Stealth / hidden until it acts) | The unit can't be seen, targeted or attacked until it acts or a condition ends. | Untargetable for good is immunity. |
| Energy Shield | blocks damage and new negative statuses until direct damage removes it | shield (Absorb one hit (shield, ward)) | The next hit or damage instance is fully absorbed or cancelled. | Damage lowered by an amount is damage_reduction. |
| Explosive Decay | explodes on death, 1 damage to adjacent tiles | death_trigger (When it dies (deathrattle)) | Effects when this unit dies or is destroyed: its own death. (Narrowed 20 Oct 2026, Kaptain's decision.) | Another unit dying is other_death_trigger; leaving play by other means is leave_trigger. |
| Fire | a unit on Fire takes 1 damage at the start of every turn | damage_over_time (Damage over time (poison, burn)) | Damage repeats over turns: poison, burn, bleed. | One-time damage is damage. |
| Fire Immunity | this unit cannot be set on Fire | immunity (Immune / can't be targeted) | A unit can't be targeted, or is immune to a damage type, effect or condition. | Hard to block is evasion; hidden until it acts is stealth. |
| Flying | stands on any tile but mountains; flies over mountains and enemy units; not hurt by lava or A.C.I.D. tiles | movement (Move my units (reposition)) | The owner moves their own unit to another space, row, lane or location. | Moving enemy units is forced_movement. |
| Frozen | the unit cannot move or attack; damage to it is negated and frees it | disable (Can't act at all (stun, freeze)) | The unit can't act at all: stun, freeze, sleep, skip its turn. | Losing only its attack is attack_lock. |
| Hardened Carapace | the Shell Psion gives every Vek Armor, weapon damage reduced by 1 | damage_reduction (Take less damage (armour)) | Damage a unit or player takes is reduced by an amount or a share. | Absorbing one whole hit is shield; points that wear off are block_armor. |
| Hive Leader | the strongest Vek, immune to Water | immunity (Immune / can't be targeted) | A unit can't be targeted, or is immune to a damage type, effect or condition. | Hard to block is evasion; hidden until it acts is stealth. |
| Hive Targeted | the Psion Tyrant deals 1 damage to all the player's units every turn | damage_over_time (Damage over time (poison, burn)) | Damage repeats over turns: poison, burn, bleed. | One-time damage is damage. |
| Invigorating Spores | the Soldier Psion gives every Vek +1 HP | stat_gain (Stat gain (+power, +health)) | A unit's power, attack, health or other stat goes up, or is set or swapped to a higher value. | Gaining only a keyword is that keyword's concept (evasion, first_strike...); a lasting rise each turn is permanent_growth. |
| Massive | the unit can walk in Water, where it cannot shoot | movement (Move my units (reposition)) | The owner moves their own unit to another space, row, lane or location. | Moving enemy units is forced_movement. |
| Mine Immunity | this unit avoids mines | immunity (Immune / can't be targeted) | A unit can't be targeted, or is immune to a damage type, effect or condition. | Hard to block is evasion; hidden until it acts is stealth. |
| Minor | the unit gives no XP to pilots on kill; describes no effect in a battle, no record | none (no effect) |  |  |
| Natural Armor | weapon damage to this unit is reduced by 1 | damage_reduction (Take less damage (armour)) | Damage a unit or player takes is reduced by an amount or a share. | Absorbing one whole hit is shield; points that wear off are block_armor. |
| Overpowered | the Psion Abomination gives every Vek +1 HP, regeneration and explosion on death | stat_gain (Stat gain (+power, +health)) | A unit's power, attack, health or other stat goes up, or is set or swapped to a higher value. | Gaining only a keyword is that keyword's concept (evasion, first_strike...); a lasting rise each turn is permanent_growth. |
| Regeneration | heals 1 every turn (Psion Abomination) | regeneration (Heal every turn (regeneration)) | A unit heals again each turn or returns to full health each turn. | A single heal is heal. |
| Self-Repairing | if damaged, shields itself and prepares to heal | shield (Absorb one hit (shield, ward)) | The next hit or damage instance is fully absorbed or cancelled. | Damage lowered by an amount is damage_reduction. |
| Smoke | units in Smoke cannot attack or repair | attack_lock (Can't attack (lock on an enemy)) | An enemy unit can't attack, often for a turn or round. | My own unit that never attacks is cant_attack. |
| Smoke Immunity | this unit is unaffected by Smoke | immunity (Immune / can't be targeted) | A unit can't be targeted, or is immune to a damage type, effect or condition. | Hard to block is evasion; hidden until it acts is stealth. |
| Spawner | spawns two Medium Goos on death | death_trigger (When it dies (deathrattle)) | Effects when this unit dies or is destroyed: its own death. (Narrowed 20 Oct 2026, Kaptain's decision.) | Another unit dying is other_death_trigger; leaving play by other means is leave_trigger. |
| Stable | cannot be moved by any weapon effect | immunity (Immune / can't be targeted) | A unit can't be targeted, or is immune to a damage type, effect or condition. | Hard to block is evasion; hidden until it acts is stealth. |
| Stealth | hidden underground, cannot be hit (Burrowers after damage) | stealth (Stealth / hidden until it acts) | The unit can't be seen, targeted or attacked until it acts or a condition ends. | Untargetable for good is immunity. |
| Submerged | weapons do not work when submerged in Water | suppress (Stop an enemy unit from acting) | An enemy unit can't attack, deal damage, block, move, use abilities, or act at all. | Lowering its stats is debuff. |
| Webbed | the unit cannot move but can still attack | immobilize (Can't move (root)) | An enemy unit can't move: root, snare, pin. | Moved against its will is forced_movement. |
