# How to make a disruptive faction?

`ask.py all kit disruption suppress`

```
## duelyst
Lyonar Kingdoms (110 cards): disruption 0, suppress 22
  Beam Shock: Stun an enemy.
  Brome Warcrest: Bloodbound Spell: Conscript.
  Conscript: Keywords: Bloodbound Spell. Summon a 1/2 Crestfallen with Zeal: Provoke in front of your...
  Crestfallen: Zeal: Provoke
Vanar Kindred (124 cards): disruption 1, suppress 17
  Ancient Grove: Keywords: Provoke. Opening Gambit: Your minions gain "Dying Wish: Summon a 1/1 Treant...
  Avalanche: Deal 4 damage to everything on your starting side of the battlefield and Stun them.
  Bonechill Barrier: Summon three joined 0/2 Vespyr Walls. Minions that attack these walls are Stunned.
  Bonechill Barrier (token): Keywords: Wall. Minions next to this minion that attack it are Stunned.
  works with: on_lifegain (e.g. Saurian Finality -> Sunriser); heal (e.g. Malicious Wisp -> Saurian Finality); on_play (e.g. Malicious Wisp -> Saurian Finality)
## faeria
Green (72 cards): disruption 0, suppress 12
  Emerald Yak: Gift - Summon a 1/1 Baby Yak with Taunt and Can't harvest faeria on a prairie you control.
  Flowersilk Faerie: Flying The first time you draw an event, this gains +1/+4, Taunt and Charge 2.
  Grove Guardian: Taunt
  Haunted Willow: Taunt
Red (72 cards): disruption 0, suppress 3
  Devouring Plant: Taunt Production - Deal 2 damage to all adjacent enemy creatures.
  Grim Guard: Taunt Combat - Deal 2 damage to your opponent.
  Ogre Battler: Taunt
  works with: on_damaged (e.g. Imperial Drain -> Unlikely Hero); damage_reduction (e.g. Imperial Drain -> Divine Guardian); death_trigger (e.g. Imperial Drain -> Celeste, Crystal Dragon)
## gwent
Nilfgaard (177 cards): disruption 11, suppress 12
  Admiral Rompally: Zeal. Order: Choose 3 enemy units, then give them Lock, Poison and Spying, in that...
  Alba Armored Cavalry: Deploy (Melee): Lock an enemy unit.
  Auckes: Deploy: Lock an enemy unit. If Serrit is in your hand, Lock all copies of that unit on...
  Collar: Order: Lock an enemy unit and damage it by 3.
Skellige (181 cards): disruption 5, suppress 1
  Armor Up: Damage an enemy unit by 2. Spawn 3 Witcher Students on the opposite row, damage them by...
  Djenge Frett: Deploy (Bloodthirst 1): Lock an enemy unit.
  Feral Bond: Spawn Skellige Wolves on an enemy row and damage it by 1, then Create a bronze Skellige...
  Gerd: Deploy: Spawn a Deafening Siren on the opposite row and damage all units on that row by...
## inscryption
Beast (122 cards): disruption 2, suppress 0
  Cuckoo: Keywords: Airborne, Brood Parasite.
  The Limoncello: Keywords: Mighty Leap, Omni Strike, Made Of Stone, Uncuttable. Traits: Giant. Special...
## into_the_breach
Cyborg (6 cards): disruption 0, suppress 1
  Ramming Speed: Dash across the map, damaging and pushing the target tile. Damage: 1. Power: Free....
Ranged (29 cards): disruption 0, suppress 4
  Cryo-Launcher: Freeze yourself and the target. Power: 1 Reactor Core.
  Rocket Artillery: Fires a pushing artillery and creates Smoke behind the shooter. Damage: 2. Power: Free....
  Smoke Mortar: Artillery shot that applies Smoke and pushes two adjacent tiles. Power: Free.
  Smoldering Shells: Damage and apply Fire to a tile while adding Smoke to adjacent tiles (vertical). Damage:...
## marvel_snap
(all cards) (867 cards): disruption 38, suppress 16
  Alioth: On Reveal: Remove the text from all unrevealed enemy characters here.
  Asgard Besieged: After turn 3, add The Destroyer to the winning side.
  Baron Zemo: On Reveal: Recruit a card that costs the least from your opponent's deck to your side of...
  Black Bolt: On Reveal: Discard the card that costs the least from your opponent's hand.
  works with: card_presence_condition (e.g. Entropic Havok -> Red Hulk); turn_end (e.g. Entropic Havok -> Red Hulk); count_payoff (e.g. Entropic Havok -> Jim Hammond Human Torch)
## monster_train
Stygian Guard (41 cards): disruption 0, suppress 3
  Frenzied Swarm: Apply Dazed 1 to enemy units. / Discard your hand.
  Siren's Song: Pyrebound. / Ascend all enemy units on this floor and apply Dazed 3.
  Unnamed Tome: Permafrost. Consume. / Apply Silence to enemy units.
Clanless (28 cards): disruption 0, suppress 2
  Steel Pulleyclaw: Consume. / Ascend an enemy unit to the Pyre room. Apply Dazed 3.
  Trap Chute: Consume. / Descend a unit to the bottom floor. Apply Dazed 2.
## runeterra
Ionia (236 cards): disruption 6, suppress 41
  Empyrean Dance: Stop an enemy Fast spell, Slow spell, or Skill, Recall an enemy, and summon The Empyrean.
  All-Seeing Oracle: Play: Pick 1 of 3 Fast or Slow spells in the enemy's hand or deck. Create a Carvings of...
  Blooming Bud: Sleep a unit.
  Capsize: Recall an enemy to increase the cost of the next unit your opponent plays this round by 2.
Targon (237 cards): disruption 1, suppress 44
  Aphelios: Nightfall: Pick a Moon Weapon to create in hand. Each round, the first time you play 2...
  Aphelios (level 2): Keywords: Quick Attack, . Nightfall: Pick a Moon Weapon to create in hand. Each round,...
  Aphelios' Gifts From Beyond: Keywords: Burst. Pick a Moon Weapon to create in hand. Create an Aphelios in your deck.
  Blinded Mystic: Play: Grant an ally +1|+1 and Silence an enemy follower.
## stormbound
Winter (34 cards): disruption 0, suppress 7
  Blizzard Bombs: On death, freeze surrounding units
  Frosthexers: On play, freeze bordering enemy units
  Glacier Palace: At the start of your turn, freeze the most forward enemy unit
  Icicle Burst: Freeze a target enemy unit. If it is already frozen, deal 6/7/8/10/12 damage to it...
Shadowfen (34 cards): disruption 1, suppress 0
  Dubious Hags: On death, spawn a 1 strength enemy Raven on a random bordering tile
```
