# How to make a go-wide faction around one unit type?

`ask.py all kit tribal summon`

```
## duelyst
Magmar Aspects (115 cards): tribal 17, summon 23
  Chrysalis Burst: Summon a random Egg in 4 random spaces.
  Dreadnought: Keywords: Rebirth. Egg minions you summon gain +2/+2.
  Juggernaut: Grow: +5/+5 Whenever this minion takes damage, summon that many random Golem Eggs nearby.
  Nature's Confluence: Summon four copies of a random Battle Pet in a 2x2 area.
Vetruvian Imperium (114 cards): tribal 16, summon 30
  Allomancer: Dying Wish: Summon a random Obelysk on this space.
  Circle of Fabrication: Summon one of each Obelysk from your deck on random spaces.
  Fireblaze Obelysk: Keywords: Summon Dervish. Your dervishes have +1 Attack.
  Khanuum-ka: Keywords: Flying, Rush. Dying Wish: A random friendly Dervish disappears, summoning a...
  works with: on_ally_play (e.g. Stone to Spears -> Night Watcher); high_cost (e.g. Echo Deliverant -> Oak in the Nemeton); rule_change (e.g. Echo Deliverant -> Oak in the Nemeton)
## faeria
Pandora (40 cards): tribal 3, summon 3
  Doom Scythe: Destroy a creature. Summon a 6/1 Slaughtering Shadow in its place.
  Iona's Mirror: Add two copies of the last Treasure your opponent played to your hand.
  Jeweled Magpie: Flying, Haste Whenever this attacks a god, add a random Treasure to your hand.
  Key of the Guardians: Summon two 5/5 Guardians with Taunt and Divine.
Blue (72 cards): tribal 4, summon 5
  Battle Toads: Summon two 2/2 Frogs with Jump.
  Bloated Toad: Jump This enters play with an enemy 2/2 Frog with Jump swallowed.
  Fugoro, Captain of the Gagana: Jump Whenever you discover a Treasure, Fugoro gains +3/+3.
  Gabrian Noble: Gift - Summon a 1/1 Ruby Fish (you may summon it on an ocean tile).
  works with: board_presence (e.g. Fugoro, Captain of the Gagana -> Triton Tactician); temporary_buff (e.g. Mother of All Yaks -> Yak Shepherd); placement_rules (e.g. Fugoro, Captain of the Gagana -> Tide Lord)
## inscryption
Magick (25 cards): tribal 7, summon 1
  Blue Mage: Keywords: Mental Gemnastics.
  Blue Sporemage: Keywords: Mental Gemnastics, Mental Gemnastics.
  Gem Fiend: Keywords: Gem Dependant.
  Mage Knight: Keywords: Gem Dependant.
Technology (76 cards): tribal 9, summon 5
  Factory Conduit: Keywords: Spawn Conduit.
  Gems Conduit: Keywords: Gem Spawn Conduit.
  Buff Conduit: Keywords: Attack Conduit.
  Daus (Act III): Keywords: Bellist. Special behaviour: If a card with "bell" in its internal ID (Chime,...
  works with: death_trigger (e.g. Energy Conduit -> Kind Cell); link_formation (e.g. Energy Conduit -> Splinter Cell); summon (e.g. Worker Ant -> The Limoncello)
## monster_train
Umbra (47 cards): tribal 18, summon 1
  Alloyed Construct: Inert. Multistrike 1. / Gorge: Gain Fuel 1.
  Antumbra Assault: Deal 3 damage. / Slay: Add 2 uncommon or rare Morsel units to your hand.
  Cannibalize: Sacrifice. / Add 3 random uncommon or rare Morsel units to your hand.
  Crucible Collector: Gorge: Gain Lifesteal 1.
Hellhorned (41 cards): tribal 6, summon 0
  Consumer of Crowns: Costs -3 Ember per Imp unit in play.
  Imp-in-a-Box: Consume. / Add 2 random Imp units to your hand.
  Imp-olate: Deal damage to the front enemy unit equal to 15x the number of Imp units in your deck.
  Imp-portant Work: Sacrifice Imp. / Gain 1 Ember. Draw 1.
  works with: death_trigger (e.g. Echowright -> Bog Chrysalis); death_count (e.g. Imp-portant Work -> Memento Mori); activated (e.g. Penumbra -> The Sentient)
## runeterra
Bilgewater (218 cards): tribal 31, summon 54
  Death From Below: Keywords: Fast, Lurk. Summon Pyke striking an enemy.
  Illaoi: Keywords: Overwhelm. Attack: Spawn 1, then I gain Power equal to your strongest...
  Illaoi (level 2): Keywords: Overwhelm. When you Spawn, increase its value by 1. Attack: Spawn 1, then...
  Illaoi's Tentacle Smash: Keywords: Slow. Spawn 2, then your strongest Tentacle and an enemy strike each other....
Shurima (264 cards): tribal 36, summon 73
  Ascended's Call: Keywords: Slow. Rally. Summon Renekton and Nasus. Immediately level them up to level 3.
  Azir: When allies attack, summon an attacking Sand Soldier. Level up: You've summoned 12+...
  Azir (level 2): When I level up, replace your deck with the Emperor's Deck, then draw 1. When allies...
  Azir (other form): When allies attack, summon an attacking Sand Soldier. When you summon another ally, give...
  works with: stances (e.g. Crescendum -> Severum); tutor (e.g. Ripper's Bay -> Pyke); recycle (e.g. Udyr (level 2) -> Janna)
## stormbound
Swarm (34 cards): tribal 6, summon 8
  Dreadful Keepers: On death, randomly spawn a 3/4/6/7/8 strength Dragon on a tile bordering a friendly Dragon
  Cursed Cemetery: At the start of your turn, spawn 1/2/2/3/3 strength Undead on both sides
  Doppelbocks: On play, spawn a 1/1/1-2/2/2 strength Satyr on the tile in front
  Draconic Roamers: Before attacking a unit, spawn a 2/2/2/2/2 strength Dragon on a random tile bordering...
Shadowfen (34 cards): tribal 3, summon 7
  Azure Hatcher: On death, spawn 1 strength Toads on 2/3/4/5/6 random surrounding tiles
  Brood Sages: On play, spawn a 1 strength Toad on 2/2/3/4/4 tiles...
  Broodmother Qordia: On play, spawn 3 Nests on random surrounding tiles which will hatch 2/3/4/5/6 strength...
  Dubious Hags: On death, spawn a 1 strength enemy Raven on a random bordering tile
  works with: random_effect (e.g. Catnip’s Charm -> Hair-Raising Cats); on_attack (e.g. Catnip’s Charm -> Melodious Sisters); summon (e.g. Terrific Slayers -> Retired Commanders)
## sts1
Ironclad (83 cards): tribal 17, summon 0
  Corruption: Skills cost 0. Whenever you play a Skill, Exhaust it.
  Demon Form: At the start of your turn, gain 2 Strength.
  Disarm: Keywords: Exhaust. Enemy loses 2 Strength.
  Double Tap: This turn, your next Attack is played twice.
Colorless (68 cards): tribal 11, summon 0
  Become Almighty: Gain 3 Strength.
  Chrysalis: Keywords: Exhaust. Shuffle 3 random Skills into your draw pile. They cost 0 this combat.
  Dark Shackles: Keywords: Exhaust. Enemy loses 9 Strength this turn.
  Impatience: If you have no Attacks in your hand, draw 2 cards.
  works with: attack_gain (e.g. J.A.X. -> Red Skull); spell_power (e.g. J.A.X. -> Red Skull); passive (e.g. J.A.X. -> Red Skull)
```
