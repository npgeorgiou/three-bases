# How to make a faction whose units die and come back?

`ask.py all kit sacrifice revive`

```
## duelyst
Abyssian Host (117 cards): sacrifice 13, revive 6
  Blood Echoes: Destroy all friendly minions and resummon them on random spaces at end of turn.
  Consuming Rebirth: Destroy a friendly minion. At the end of your turn, re-summon it on the same space and...
  Abhorrent Unbirth: Destroy all friendly minions to summon a 1/1 Abomination that gains their Attack,...
  Aphotic Drain: Destroy a friendly minion to restore 5 Health to your General.
Magmar Aspects (115 cards): sacrifice 3, revive 11
  Cascading Rebirth: Destroy a friendly minion to summon a random Magmar minion that costs 1 more.
  Cascading Rebirth (follow-up): Destroy a friendly minion to summon a random Magmar minion that costs 1 more.
  Dreadnought: Keywords: Rebirth. Egg minions you summon gain +2/+2.
  Erratic Raptyr: Keywords: Rebirth. After this minion attacks or counterattacks, turn it into an Egg.
  works with: revive (e.g. Deepfire Devourer -> The Releaser); death_trigger (e.g. Windstorm Obelysk -> Khanuum-ka); leave_trigger (e.g. Deepfire Devourer -> The Releaser)
## faeria
Yellow (72 cards): sacrifice 6, revive 0
  Death Walker: Deathtouch You must sacrifice another creature to summon this creature.
  Demon Wrangler: Gift - You may sacrifice another creature, summoning a 5/2 Flying Demon Wing in its place.
  Doomgate, Door to Oblivion: When Doomgate has 13 Life or more, destroy it and summon Ostregoth in its place....
  Lord of the Wastes: Gift - You may sacrifice another creature to gain 3 faeria.
Pandora (40 cards): sacrifice 2, revive 0
  Ancient Gargoyle: Charge 3, Flying Gift - Destroy all Treasure Maps in your deck and gain +1/+1 for each...
  Void Guardian: Gift - Destroy your deck.
  works with: death_trigger (e.g. Rakoan Cannoneer -> Rakoan Shield Mates); cheat_death (e.g. Death Walker -> Annoying Gnat); death_count (e.g. Death Walker -> Spirit Spice)
## inscryption
Undead (24 cards): sacrifice 2, revive 1
  Necromancer: Keywords: Double Death.
  Pharaoh's Pets: Keywords: Worthy Sacrifice, Many Lives.
Magick (25 cards): sacrifice 1, revive 0
  Master Bleene: Keywords: True Scholar.
  works with: on_sacrifice (e.g. Master Bleene -> Pharaoh's Pets); cost_reduction (e.g. Master Bleene -> Pharaoh's Pets); cheat_death (e.g. Master Bleene -> Pharaoh's Pets)
## into_the_breach
Ranged (10 cards): sacrifice 1, revive 0
  Arachnoid Mech: Health 3, move 3. Weapon: Arachnoid Injector: Damage target, creating a friendly robot...
  works with: summon (e.g. Arachnoid Injector -> Marked tile); on_kill (e.g. Arachnoid Injector -> Cascading Resonator); death_trigger (e.g. Arachnoid Injector -> Ice Tile)
## monster_train
Umbra (47 cards): sacrifice 12, revive 0
  Antumbra Morsel: Eaten: Eater gains +6 Health.
  Cannibalize: Sacrifice. / Add 3 random uncommon or rare Morsel units to your hand.
  Feast: Trigger feeding on units with Eaten abilities.
  Magma Morsel: Eaten: Eater gains +6 Attack.
Melting Remnant (43 cards): sacrifice 11, revive 0
  Crushing Demise: Kill a random non-boss enemy unit. / Kill a random friendly unit.
  Hallowed Drippings: Consume. / Apply Burnout 5 to friendly Burnout units.
  Hallowed Halls: Kill friendly units. / Reform random units to this floor until it exceeds its Capacity.
  Lady of the Reformed: Burnout 3. / Revenge: Friendly Burnout units gain Burnout 1.
  works with: on_sacrifice (e.g. Primordium -> Alloyed Construct); upkeep (e.g. Primordium -> Alloyed Construct); rule_change (e.g. Primordium -> Alloyed Construct)
## runeterra
Shadow Isles (220 cards): sacrifice 52, revive 28
  Amalgamation Of Vile Rites: Keywords: Last Breath, Deathless. To play me, kill an ally. Last Breath: Heal your Nexus...
  Chronicler of Ruin: Play: Kill an ally, then revive it.
  Eternal Dancers: Keywords: Hallowed. Attack: Revive an attacking Ephemeral copy of the strongest dead...
  Harrowing Return: Revive the strongest dead allied follower and grant it Ephemeral and Fearsome. Give...
Shurima (264 cards): sacrifice 24, revive 2
  Acolyte's Reliquary: Keywords: Landmark. When I'm summoned, create a Ruinous Acolyte in hand. When you...
  Construct of Desolation: Create a Ruinous Acolyte or an Obelisk of Power in hand.
  Dune Swallower: Keywords: SpellShield, Fearsome. To play me, kill an ally or one of your mana gems 3...
  Empire Reconstructor: Play: Grant an allied landmark, "When I'm destroyed, revive me."
  works with: revive (e.g. Mordekaiser -> Bladepierced Revenant); death_trigger (e.g. Mordekaiser -> Bladepierced Revenant); other_leave_trigger (e.g. The Darkin Bloodletters (created) -> The Shadow Reaper)
## stormbound
Ironclad (34 cards): sacrifice 1, revive 1
  Project PH03-NIX: When dying not bordering any base, randomly respawn at your base with 5/6/7/8/10 strength
  Temple of Space: When played with a friendly copy on the board, teleport 2/3/4/6/8 surrounding units from...
Shadowfen (34 cards): sacrifice 1, revive 0
  Toxic Sacrifice: Destroy a target friendly unit. Deal 2/3/4/5/6 damage to surrounding units and poison them
  works with: death_trigger (e.g. Toxic Sacrifice -> Green Prototypes); revive (e.g. Pricey Freedom -> Siro the Resurrector); cheat_death (e.g. Pricey Freedom -> Project PH03-NIX)
## sts1
Watcher (90 cards): sacrifice 2, revive 0
  Blasphemy: Keywords: Exhaust. Enter Divinity. Die next turn.
  Blasphemy+: Keywords: Retain, Exhaust. Enter Divinity. Die next turn.
  works with: stances (e.g. Blasphemy -> Pray); resource_gain (e.g. Blasphemy -> Bloody Idol); base_resource_gain (e.g. Blasphemy -> Double Energy)
```
