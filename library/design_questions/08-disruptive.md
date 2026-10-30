# How to make a disruptive faction?

`ask.py all kit disruption suppress`

```
## duelyst
Lyonar Kingdoms (110 cards): disruption 0, suppress 22
  Beam Shock: Stun an enemy.
  Brome Warcrest: Bloodbound Spell: Conscript.
  Conscript: Keywords: Bloodbound Spell. Summon a 1/2 Crestfallen with Zeal: Provoke in front of your...
  Crestfallen: Zeal: Provoke
Vanar Kindred (124 cards): disruption 0, suppress 20
  Ancient Grove: Keywords: Provoke. Opening Gambit: Your minions gain "Dying Wish: Summon a 1/1 Treant...
  Aspect of the Bear: Transform ANY minion into a 4/5 Ursaplomb that will not counterattack.
  Avalanche: Deal 4 damage to everything on your starting side of the battlefield and Stun them.
  Bonechill Barrier: Summon three joined 0/2 Vespyr Walls. Minions that attack these walls are Stunned.
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
  works with: on_damaged (e.g. Imperial Drain -> Unlikely Hero); damage_reduction (e.g. Imperial Drain -> Shadowsilk Faerie); death_trigger (e.g. Imperial Drain -> Celeste, Crystal Dragon)
## inscryption
Beast (122 cards): disruption 4, suppress 1
  Cuckoo: Keywords: Airborne, Brood Parasite.
  Great Kraken: Keywords: Kraken Waterborne.
  Pack Mule: Keywords: Sprinter, Uncuttable. Special behaviour: When a card perishes, player receives...
  The Limoncello: Keywords: Mighty Leap, Omni Strike, Made Of Stone, Uncuttable. Traits: Giant. Special...
## into_the_breach
Brute (10 cards): disruption 0, suppress 2
  Jet Mech: Keywords: Flying. Health 2, move 4. Weapon: Aerial Bombs: Fly over a target, dropping an...
  Thruster Mech: Keywords: Flying. Health 3, move 4. Weapon: Reverse Thrusters: Smoke and deal damage to...
Science (10 cards): disruption 0, suppress 5
  Control Mech: Keywords: Flying. Health 2, move 4. Weapon: Control Shot: Temporarily control a unit,...
  Defense Mech: Keywords: Flying. Health 2, move 4. Weapon: Attraction Pulse: Fires a projectile,...
  Drill Mech: Keywords: Flying. Health 3, move 4. Weapon: Seismic Capacitor: Damage and flip target....
  Nano Mech: Keywords: Flying. Health 2, move 4. Weapon: A.C.I.D. Projector: Fire a projectile that...
## monster_train
Stygian Guard (41 cards): disruption 0, suppress 3
  Frenzied Swarm: Apply Dazed 1 to enemy units. / Discard your hand.
  Siren's Song: Pyrebound. / Ascend all enemy units on this floor and apply Dazed 3.
  Unnamed Tome: Permafrost. Consume. / Apply Silence to enemy units.
Clanless (28 cards): disruption 0, suppress 2
  Steel Pulleyclaw: Consume. / Ascend an enemy unit to the Pyre room. Apply Dazed 3.
  Trap Chute: Consume. / Descend a unit to the bottom floor. Apply Dazed 2.
## runeterra
Shurima (264 cards): disruption 39, suppress 67
  Akshan: Keywords: Quick Attack. When I'm summoned or strike: Summon a Warlord's Palace or...
  Akshan (level 2): Keywords: Quick Attack. When I'm summoned or strike: Summon a Warlord's Hoard or advance...
  Akshan's Grappling Hook: Keywords: Slow. An ally you've targeted this round strikes an enemy. Create an Akshan in...
  Ascended's Call: Keywords: Slow. Rally. Summon Renekton and Nasus. Immediately level them up to level 3.
Runeterra (76 cards): disruption 10, suppress 33
  Delve Into The Past: Keywords: Burst. Choose one of two World Runes you don't have in play or in hand and...
  Ryze: Origin: The Rune Mage. When I'm summoned or Round Start: Create 2 Delve Into The Pasts...
  Ryze (level 2): Keywords: SpellShield. When I'm summoned or Round Start: Create 2 Delve Into The Pasts...
  Ryze's Realm Warp: Keywords: Burst. Draw 3. Discard any followers drawn. Create a Ryze in your deck.
## stormbound
Winter (34 cards): disruption 0, suppress 8
  Blizzard Bombs: On death, freeze surrounding units
  Frosthexers: On play, freeze bordering enemy units
  Glacier Palace: At the start of your turn, freeze the most forward enemy unit
  Iceflakes: On play, freeze itself
## sts1
Colorless (68 cards): disruption 1, suppress 0
  Panacea: Keywords: Exhaust. Gain 1 Artifact.
Defect (89 cards): disruption 1, suppress 0
  Core Surge: Keywords: Exhaust. Deal 11 damage. Gain 1 Artifact.
```
