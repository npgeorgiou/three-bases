# How to make a faction that pushes and pulls enemies?

`ask.py all kit forced_movement movement`

```
## duelyst
Songhai Empire (117 cards): forced_movement 10, movement 16
  Blink: Keywords: Bloodbound Spell. Teleport a friendly minion up to 2 spaces.
  Flicker: Teleport your General to a space behind an enemy.
  Kaleos Xaan: Bloodbound Spell: Blink.
  Mist Dragon Seal: Give a friendly minion +1/+1 and teleport it anywhere.
Vanar Kindred (124 cards): forced_movement 4, movement 13
  Lightning Blitz: Give all friendly minions +1/+1 and randomly teleport them to your opponent's starting...
  Mesmerize: Teleport an enemy one space.
  The Dredger: Whenever your General damages an enemy, randomly teleport them to your starting side of...
  Wanderlust: Intensify: Teleport 1 random enemy minion to a space on your starting side of the...
  works with: board_wipe (e.g. Mist Dragon Seal -> Necrotic Sphere); polymorph (e.g. Mist Dragon Seal -> Eternity Painter); regeneration (e.g. Mist Dragon Seal -> Lux Ignis)
## faeria
Yellow (72 cards): forced_movement 8, movement 42
  Flash Wind: Move a friendly creature or pay 2 faeria and move an enemy creature.
  Keldran Adventurer: Dash 1 At the end of your turn, shuffle 2 Treasure Maps into your deck if this is on an...
  Mistral Guide: Flying Give friendly creatures summoned adjacent to this creature Dash 2 and Flying.
  Oradrim Fanatic: Jump Gift - You may move a friendly creature.
Blue (72 cards): forced_movement 7, movement 38
  Animated Banquet: Dash 1 At the end of your turn, a random adjacent friendly creature swallows this and...
  Coral Polliwog: This creature can harvest faeria the turn you play it. Gift - You may move this...
  Dream Reaver: Dash 3 Gift - Set a god's Life to 10.
  Prophet of Tides: Gift - Move this creature's land twice.
  works with: territory_trigger (e.g. Rebel Glider -> Nekomata); terrain (e.g. Triton Adventurer -> Gabrian Commander); adjacency (e.g. Triton Adventurer -> Tide Lord)
## gwent
Syndicate / Skellige (3 cards): forced_movement 1, movement 1
  Hammond: Deploy: Move an enemy unit to the other row and give it Bleeding (2). Increase the...
Nilfgaard (177 cards): forced_movement 24, movement 19
  Amnesty: Seize an enemy unit with 3 or less power. Conspiracy: Also boost it by 2. Devotion:...
  Ard Feainn Heavy Cavalry: Flanking. At the end of your turn, gain 1 Armor. Ranged: When this unit reaches 5 Armor,...
  Baccalà: Resilience. Deploy: Spawn Imperial Fleet to the left of self and Imperial Marine to the...
  Emhyr var Emreis: Deploy: Play a bronze Soldier or Aristocrat from your hand, then draw a card. Whenever...
  works with: junk_cards (e.g. Ard Feainn Heavy Cavalry -> Viper Witcher Alchemist); bounce_enemy (e.g. Ard Feainn Heavy Cavalry -> Ardal aep Dahy); steal (e.g. Vattier de Rideaux -> Emhyr var Emreis)
## inscryption
Beast (122 cards): forced_movement 18, movement 18
  Bloodhound: Keywords: Guardian.
  Burrowing Trap: Keywords: Burrower, Steel Trap.
  Elk: Keywords: Sprinter.
  Elk Fawn: Keywords: Sprinter, Fledgling.
Undead (24 cards): forced_movement 3, movement 3
  Bonehound: Keywords: Guardian.
  Ghost Ship: Keywords: Waterborne, Skeleton Crew.
  Headless Horseman: Keywords: Airborne, Sprinter.
  works with: enemy_benefit (e.g. Wild Bull -> Alarm Bot); link_formation (e.g. Pronghorn -> Tough Cell); base_resource_gain (e.g. Pronghorn -> Energy Conduit)
## into_the_breach
Prime (30 cards): forced_movement 15, movement 15
  Explosive Vents: Blast (and push) all adjacent tiles. Damage: 1. Power: Free. Upgrades: +1 Damage (2...
  Flame Thrower: Push target tile and light tiles on Fire. Damage units already on Fire. (Starts with 1...
  Hydraulic Legs: Leap to a tile, damaging self and adjacent tiles (with push). Damage: 1 (1 to self)....
  Hydraulic Lifter: Throw an adjacent unit and damage it. (Starts with 2-tile range.) Damage: 1. Power:...
Brute (31 cards): forced_movement 17, movement 19
  AP Cannon: Fire a pushing projectile that pierces the first target and damages the second. Damage:...
  Aerial Bombs: Fly over a target, dropping an explosive smoke bomb. Damage: 1. Power: Free. Upgrades:...
  Astra Bombs: Leap over any distance dropping a bomb on each tile you pass. Single-use. Damage: 1....
  Def. Shrapnel: Fire a non-damaging projectile that pushes tiles around the target. Power: Free.
  works with: movement (e.g. Thermal Discharger -> Flame Thrower); destroy (e.g. Thermal Discharger -> Water Tile); rule_change (e.g. Thermal Discharger -> Flame Thrower)
## marvel_snap
(all cards) (867 cards): forced_movement 53, movement 63
  Aero: On Reveal: The last card your opponent played moves to this location.
  Agamotto: Game Start: Shuffle 4 Ancient Arcana into your deck.
  Angel: When one of your cards is destroyed, this flies out of your hand or deck to replace it.
  Araña: Activate: After you play your next card, give it +1 Power and move it to the right.
  works with: board_wipe (e.g. Hawkeye Kate Bishop -> Mercworld); play_restriction (e.g. Hawkeye Kate Bishop -> Professor X); friendly_fire (e.g. Hawkeye Kate Bishop -> Murderworld)
## monster_train
Clanless (28 cards): forced_movement 3, movement 3
  Olde Magic: Built by the player at the Arcane Machine event (Concealed Caverns): one primary effect...
  Steel Pulleyclaw: Consume. / Ascend an enemy unit to the Pyre room. Apply Dazed 3.
  Trap Chute: Consume. / Descend a unit to the bottom floor. Apply Dazed 2.
Hellhorned (41 cards): forced_movement 3, movement 3
  Hidden Passage: Ascend a unit.
  March of Shields: Move a unit to the front and apply Armor 10.
  Tiresome Climb: Ascend a unit and apply Dazed 2.
  works with: attack_lock (e.g. Olde Magic -> Siren's Song); placement_rules (e.g. Olde Magic -> Siren's Song); immobilize (e.g. Crypt Builder -> Wyldenten)
## runeterra
Bilgewater (220 cards): forced_movement 9, movement 5
  Bilgewater Tellstones: Create a Fleeting More Powder!, Playful Trickster, or Chum the Waters in hand.
  Fizz: Keywords: Imbue. When you play a spell, stop all enemy spells and Skills targeting me...
  Fizz's Playful Trickster: Keywords: Fast. Remove an attacking ally from combat to Rally. Create a Fizz in your deck.
  Playful Trickster: Remove an attacking ally from combat to Rally.
Ionia (236 cards): forced_movement 0, movement 14
  Ahri: Keywords: Quick Attack. Attack: The first time I attack strike, swap me with the ally to...
  Ahri (level 2): Keywords: Quick Attack, Elusive, . When you Recall an ally, reduce its cost by 1....
  Ahri's Charm: Keywords: Focus. Recall an ally to give an enemy Vulnerable this round. Create an Ahri...
  Bladesurge: Keywords: Burst, Fleeting. Swap Irelia with an ally.
  works with: attack_token (e.g. Sion -> Riven (level 2)); on_discard (e.g. Fizz -> Rumble (level 2)); board_wipe (e.g. An Acquired Taste -> Tahm Kench)
## stormbound
Ironclad (34 cards): forced_movement 9, movement 9
  Absorbing Varmints: Before moving, make friendly Ancients and Rodents pull enemy units from behind. Then...
  Armed Schemers: On play, pull enemy units towards itself. Then deal 3/4/5/6/7 damage to bordering enemy...
  Cheesy Lurers: On play, pull the first enemy in front and deal 2/3/4/5/6 damage to it
  Eloth the Ignited: On play, fly to the first enemy unit in front, push it away and deal 2/3/4/5/6 damage,...
Swarm (34 cards): forced_movement 3, movement 5
  Lasting Remains: After attacking, move forward
  Xuri, Lord of Life: On play, fly to the first empty tile in front. Give 2/3/4/5/6 strength to all friendly...
  Forgotten Souls: On play, command a/a/// random/random///...
  Herald’s Hymn: Give 2/3/4/5/6 strength to a target friendly unit. Command friendly units in its row...
  works with: variety_payoff (e.g. Eloth the Ignited -> Ubass the Hunter); attack_now (e.g. Sweetcap Kittens -> Hair-Raising Cats); generate_cards (e.g. Eloth the Ignited -> Guardi the Lightbringer)
## sts1
Defect (89 cards): forced_movement 29, movement 23
  Ball Lightning: Deal 7 damage. Channel 1 Lightning.
  Chaos: Channel 1 random Orb.
  Chill: Keywords: Innate, Exhaust. Channel 1 Frost for each enemy in combat.
  Chill+: Keywords: Innate, Exhaust. Channel 1 Frost for each enemy in combat.
Silent (83 cards): forced_movement 6, movement 0
  After Image: Keywords: Innate. Whenever you play a card, gain 1 Block.
  After Image+: Keywords: Innate. Whenever you play a card, gain 1 Block.
  Backstab: Keywords: Innate, Exhaust. Deal 11 damage.
  Infinite Blades: Keywords: Innate. At the start of your turn, add a Shiv into your hand.
  works with: slots_queue (e.g. Rainbow+ -> Chaos); movement (e.g. Rainbow+ -> Chaos); repeat_trigger (e.g. Rainbow+ -> Chaos)
```
