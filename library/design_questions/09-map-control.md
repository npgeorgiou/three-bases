# How to make a faction that controls spots on the map?

`ask.py all kit zone_control movement`

```
## duelyst
Songhai Empire (117 cards): zone_control 2, movement 16
  Blink: Keywords: Bloodbound Spell. Teleport a friendly minion up to 2 spaces.
  Dusk Rigger: Backstab: (2). Whenever this backstabs, put a MECHAZ0R Progression into your action bar.
  Flicker: Teleport your General to a space behind an enemy.
  Juxtaposition: Switch positions between ANY two minions.
Vetruvian Imperium (114 cards): zone_control 7, movement 10
  Arid Unmaking: Destroy a friendly minion to turn its space into Exhuming Sand.
  Astral Phasing: Give a friendly minion +5 Health and Flying.
  Cataclysmic Fault: Turn the entire center column into Exhuming Sand.
  Circle of Fabrication: Summon one of each Obelysk from your deck on random spaces.
  works with: quests (e.g. Oakenheart -> MECHAZ0R Progression); activated (e.g. Oakenheart -> MECHAZ0R Progression); terrain (e.g. Sunrise Cleric -> Nocturne)
## faeria
Pandora (40 cards): zone_control 7, movement 12
  Jeweled Magpie: Flying, Haste Whenever this attacks a god, add a random Treasure to your hand.
  Magic Carpet: Flying, Dash 5 Gift - Fill your hand with Flash Winds. They become wild land.
  Spear of the Guardians: Divine,Flying,Dash 5 Must be summoned next to a friendly creature.
  Ancient Gargoyle: Charge 3, Flying Gift - Destroy all Treasure Maps in your deck and gain +1/+1 for each...
Yellow (72 cards): zone_control 12, movement 42
  Amai Merchant: Flying Gift - Discover a card that costs 5 faeria or more. Add the 2 cards you didn't...
  Annoying Gnat: Flying Can't harvest faeria. Last Words - Deal 2 damage to yourself. Summon this in a...
  Demonic Salmon: Haste, Flying, Charge 2 Can't harvest faeria. Whenever this attacks a god, it gains +1/+1.
  Flash Salmon: Divine, Flying, Haste, Charge 2 Can't harvest faeria. At the end of your turn, destroy...
  works with: high_cost (e.g. Thyrian Expedition -> Gemshell Tortoise); in_hand_buff (e.g. Thyrian Expedition -> Gemshell Tortoise); cost_reduction (e.g. Thyrian Expedition -> Gemshell Tortoise)
## gwent
Nilfgaard (177 cards): zone_control 20, movement 19
  False Ciri: Disloyal. Deploy: Play a bronze Tactic from your graveyard and give it Doomed. At the...
  Mage Infiltrator: Disloyal. Deploy: Damage adjacent units by 3. Deathblow: Move self to the opposite row...
  Usurper: Emperor: Veil. Deploy: Spawn an Operative on each enemy row and give them Spying. Zeal. Order:...
  Usurper: General: Deploy: Spawn an Operative on each enemy row and give them Spying. Zeal. Order: Seize...
Syndicate / Skellige (3 cards): zone_control 0, movement 1
  Hammond: Deploy: Move an enemy unit to the other row and give it Bleeding (2). Increase the...
  works with: steal (e.g. Rosa and Edna var Attre -> Emhyr var Emreis); forced_movement (e.g. Usurper: Emperor -> Doadrick Leumaerts); movement (e.g. Rot Tosser -> Siege)
## inscryption
Beast (122 cards): zone_control 0, movement 18
  Bloodhound: Keywords: Guardian.
  Burrowing Trap: Keywords: Burrower, Steel Trap.
  Elk: Keywords: Sprinter.
  Elk Fawn: Keywords: Sprinter, Fledgling.
Undead (24 cards): zone_control 0, movement 3
  Bonehound: Keywords: Guardian.
  Ghost Ship: Keywords: Waterborne, Skeleton Crew.
  Headless Horseman: Keywords: Airborne, Sprinter.
## into_the_breach
Brute (31 cards): zone_control 1, movement 19
  AP Cannon: Fire a pushing projectile that pierces the first target and damages the second. Damage:...
  Aerial Bombs: Fly over a target, dropping an explosive smoke bomb. Damage: 1. Power: Free. Upgrades:...
  Astra Bombs: Leap over any distance dropping a bomb on each tile you pass. Single-use. Damage: 1....
  Def. Shrapnel: Fire a non-damaging projectile that pushes tiles around the target. Power: Free.
Prime (30 cards): zone_control 0, movement 15
  Explosive Vents: Blast (and push) all adjacent tiles. Damage: 1. Power: Free. Upgrades: +1 Damage (2...
  Flame Thrower: Push target tile and light tiles on Fire. Damage units already on Fire. (Starts with 1...
  Hydraulic Legs: Leap to a tile, damaging self and adjacent tiles (with push). Damage: 1 (1 to self)....
  Hydraulic Lifter: Throw an adjacent unit and damage it. (Starts with 2-tile range.) Damage: 1. Power:...
  works with: friendly_fire (e.g. Grid Repulse -> Fire); aoe_damage (e.g. Grid Repulse -> Fire); ping (e.g. Grid Repulse -> Fire)
## marvel_snap
(all cards) (867 cards): zone_control 5, movement 63
  Strange Academy: After turn 5, move all cards here to other random locations.
  Aero: On Reveal: The last card your opponent played moves to this location.
  Agamotto: Game Start: Shuffle 4 Ancient Arcana into your deck.
  Angel: When one of your cards is destroyed, this flies out of your hand or deck to replace it.
  works with: positional (e.g. Strange Academy -> Kingpin); lanes (e.g. Strange Academy -> Kingpin); movement (e.g. Strange Academy -> Hercules)
## monster_train
Clanless (28 cards): zone_control 0, movement 3
  Olde Magic: Built by the player at the Arcane Machine event (Concealed Caverns): one primary effect...
  Steel Pulleyclaw: Consume. / Ascend an enemy unit to the Pyre room. Apply Dazed 3.
  Trap Chute: Consume. / Descend a unit to the bottom floor. Apply Dazed 2.
Hellhorned (41 cards): zone_control 0, movement 3
  Hidden Passage: Ascend a unit.
  March of Shields: Move a unit to the front and apply Armor 10.
  Tiresome Climb: Ascend a unit and apply Dazed 2.
## runeterra
Ionia (236 cards): zone_control 0, movement 14
  Ahri: Keywords: Quick Attack. Attack: The first time I attack strike, swap me with the ally to...
  Ahri (level 2): Keywords: Quick Attack, Elusive, . When you Recall an ally, reduce its cost by 1....
  Ahri's Charm: Keywords: Focus. Recall an ally to give an enemy Vulnerable this round. Create an Ahri...
  Bladesurge: Keywords: Burst, Fleeting. Swap Irelia with an ally.
Bilgewater (220 cards): zone_control 0, movement 5
  Bilgewater Tellstones: Create a Fleeting More Powder!, Playful Trickster, or Chum the Waters in hand.
  Fizz: Keywords: Imbue. When you play a spell, stop all enemy spells and Skills targeting me...
  Fizz's Playful Trickster: Keywords: Fast. Remove an attacking ally from combat to Rally. Create a Fizz in your deck.
  Playful Trickster: Remove an attacking ally from combat to Rally.
  works with: permanent_growth (e.g. Soothsayer -> Lux: Illuminated); defence_gain (e.g. Soothsayer -> Lux: Illuminated); attack_gain (e.g. Soothsayer -> Lux: Illuminated)
## stormbound
Ironclad (34 cards): zone_control 0, movement 9
  Absorbing Varmints: Before moving, make friendly Ancients and Rodents pull enemy units from behind. Then...
  Armed Schemers: On play, pull enemy units towards itself. Then deal 3/4/5/6/7 damage to bordering enemy...
  Cheesy Lurers: On play, pull the first enemy in front and deal 2/3/4/5/6 damage to it
  Eloth the Ignited: On play, fly to the first enemy unit in front, push it away and deal 2/3/4/5/6 damage,...
Swarm (34 cards): zone_control 1, movement 5
  Forgotten Souls: On play, command a/a/// random/random///...
  Head Start: Spawn a 5/6/7/8/9 strength Satyr on a random tile in your furthest row
  Herald’s Hymn: Give 2/3/4/5/6 strength to a target friendly unit. Command friendly units in its row...
  Lasting Remains: After attacking, move forward
  works with: attack_now (e.g. Angelic Tikas -> Hair-Raising Cats); activated (e.g. Slyboots -> Temple of the Mind); removal (e.g. Slyboots -> Temple of the Mind)
## sts1
Defect (89 cards): zone_control 0, movement 23
  Ball Lightning: Deal 7 damage. Channel 1 Lightning.
  Chaos: Channel 1 random Orb.
  Chill: Keywords: Innate, Exhaust. Channel 1 Frost for each enemy in combat.
  Chill+: Keywords: Innate, Exhaust. Channel 1 Frost for each enemy in combat.
```
