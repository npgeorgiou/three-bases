# Is a family of features viable for a faction? (sacrifice and card draw)

`ask.py all kit sacrifice draw`

```
## duelyst
Vetruvian Imperium (114 cards): sacrifice 12, draw 9
  Reassemble: Return a friendly Obelysk to your action bar and reduce its cost to 0. Draw a card.
  Allomancer: Dying Wish: Summon a random Obelysk on this space.
  Arid Unmaking: Destroy a friendly minion to turn its space into Exhuming Sand.
  Azure Summoning: Whenever you summon a minion with Flying from your action bar this turn, draw a minion...
Abyssian Host (117 cards): sacrifice 13, draw 8
  Vellumscry: Destroy a friendly minion to draw three cards.
  Abhorrent Unbirth: Destroy all friendly minions to summon a 1/1 Abomination that gains their Attack,...
  Aphotic Drain: Destroy a friendly minion to restore 5 Health to your General.
  Blood Echoes: Destroy all friendly minions and resummon them on random spaces at end of turn.
  works with: revive (e.g. Stone to Spears -> The Releaser); death_trigger (e.g. Soulburn Obelysk -> Khanuum-ka); leave_trigger (e.g. Stone to Spears -> The Releaser)
## faeria
Blue (72 cards): sacrifice 1, draw 12
  Aurora's Dream: Draw until you have 9 cards. Reduce the cost of all cards in your hand to 0 faeria.
  Curious Biomancer: Gift - For each enemy creature, draw a non-blue creature from your deck.
  Failed Experiment: The next creature you play this turn costs 4 faeria less. It dies instantly.
  Forbidden Library: Production - Draw a card, gain 1 faeria, and deal 2 damage to yourself.
Yellow (72 cards): sacrifice 6, draw 6
  Doomgate, Door to Oblivion: When Doomgate has 13 Life or more, destroy it and summon Ostregoth in its place....
  Death Walker: Deathtouch You must sacrifice another creature to summon this creature.
  Demon Wrangler: Gift - You may sacrifice another creature, summoning a 5/2 Flying Demon Wing in its place.
  Flash Salmon: Divine, Flying, Haste, Charge 2 Can't harvest faeria. At the end of your turn, destroy...
  works with: death_trigger (e.g. Rakoan Cannoneer -> Rakoan Shield Mates); cheat_death (e.g. Failed Experiment -> Aryana, Soul of Gagana); death_count (e.g. Failed Experiment -> Mother of All Yaks)
## inscryption
Magick (25 cards): sacrifice 1, draw 4
  Master Bleene: Keywords: True Scholar.
  Blue Mage: Keywords: Mental Gemnastics.
  Blue Sporemage: Keywords: Mental Gemnastics, Mental Gemnastics.
  Master Orlu: Keywords: Airborne, Looter.
Undead (24 cards): sacrifice 2, draw 1
  Dead Hand: Keywords: Handy.
  Necromancer: Keywords: Double Death.
  Pharaoh's Pets: Keywords: Worthy Sacrifice, Many Lives.
  works with: on_sacrifice (e.g. Master Bleene -> Child 13); cost_reduction (e.g. Master Bleene -> Pharaoh's Pets); cheat_death (e.g. Master Bleene -> Child 13)
## into_the_breach
Ranged (10 cards): sacrifice 1, draw 0
  Arachnoid Mech: Health 3, move 3. Weapon: Arachnoid Injector: Damage target, creating a friendly robot...
  works with: summon (e.g. Arachnoid Mech -> Marked tile); on_kill (e.g. Arachnoid Mech -> Cascading Resonator); death_trigger (e.g. Arachnoid Mech -> Ice Tile)
## monster_train
Umbra (47 cards): sacrifice 12, draw 2
  Antumbra Morsel: Eaten: Eater gains +6 Health.
  Cannibalize: Sacrifice. / Add 3 random uncommon or rare Morsel units to your hand.
  Ember Cache: Consume. / Add 3 Excavated Ember cards to your discard pile.
  Feast: Trigger feeding on units with Eaten abilities.
Melting Remnant (43 cards): sacrifice 11, draw 1
  Crushing Demise: Kill a random non-boss enemy unit. / Kill a random friendly unit.
  Hallowed Drippings: Consume. / Apply Burnout 5 to friendly Burnout units.
  Hallowed Halls: Kill friendly units. / Reform random units to this floor until it exceeds its Capacity.
  Lady of the Reformed: Burnout 3. / Revenge: Friendly Burnout units gain Burnout 1.
  works with: on_sacrifice (e.g. Primordium -> Alloyed Construct); upkeep (e.g. Primordium -> Alloyed Construct); rule_change (e.g. Primordium -> Alloyed Construct)
## runeterra
Shurima (264 cards): sacrifice 24, draw 52
  Rite of Calling: Kill an ally or destroy one of your mana gems to draw a champion.
  Rite of Calling (created): Keywords: Slow. Kill an ally to draw a Champion.
  Shimmering Mirage: Keywords: Burst. Summon an exact copy of an ally. It's Ephemeral. Draw 1.
  Xerath: When you destroy an allied landmark, deal 1 to the weakest enemy. Level up: You've...
Runeterra (76 cards): sacrifice 4, draw 45
  Aatrox: Origin: The World Ender. Auto-Equip: The Darkin Blade. When I'm summoned or strike: Heal...
  Aatrox (level 2): Keywords: Overwhelm. Auto-Equip: The Darkin Blade. Darkin allies cost 5 less. When I'm...
  Aatrox's Deathbringer Sweep: Keywords: Fast. Aatrox and an enemy strike each other. Create a Deathbringer Slash in...
  Bard: Origin: The Wandering Caretaker. Attack: Plant 3 Chimes in your deck. Level up: You've...
  works with: revive (e.g. Kalista (level 2) -> Bladepierced Revenant); death_trigger (e.g. Kalista (level 2) -> Bladepierced Revenant); other_leave_trigger (e.g. The Darkin Bloodletters (created) -> The Shadow Reaper)
## stormbound
Ironclad (34 cards): sacrifice 1, draw 0
  Temple of Space: When played with a friendly copy on the board, teleport 2/3/4/6/8 surrounding units from...
Shadowfen (34 cards): sacrifice 1, draw 0
  Toxic Sacrifice: Destroy a target friendly unit. Deal 2/3/4/5/6 damage to surrounding units and poison them
  works with: death_trigger (e.g. Toxic Sacrifice -> Green Prototypes); revive (e.g. Pricey Freedom -> Project PH03-NIX); cheat_death (e.g. Pricey Freedom -> Project PH03-NIX)
## sts1
Silent (83 cards): sacrifice 0, draw 18
  Acrobatics: Draw 3 cards. Discard 1 card.
  Adrenaline: Keywords: Exhaust. Gain 1 energy. Draw 2 cards.
  Adrenaline+: Keywords: Exhaust. Gain 2 energy. Draw 2 cards.
  Backflip: Gain 5 Block. Draw 2 cards.
Defect (89 cards): sacrifice 0, draw 13
  Compile Driver: Deal 7 damage. Draw 1 card for each unique Orb you have.
  Coolheaded: Channel 1 Frost. Draw 1 card.
  FTL: Deal 5 damage. If you have played less than 3 cards this turn, draw 1 card.
  Fission: Keywords: Exhaust. Remove all your Orbs. Gain 1 energy and draw 1 card for each Orb...
  works with: stances (e.g. Blasphemy+ -> Prostrate); resource_gain (e.g. Blasphemy -> Bloody Idol); base_resource_gain (e.g. Blasphemy -> Double Energy)
```
