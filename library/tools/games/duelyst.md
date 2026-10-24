# Duelyst

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*Claude's summary (Oct 2026), from general knowledge of the game and the rules and terms under Mechanics; not from the sources below.*
- Genre: digital tactics card game (Counterplay, 2016); 1 vs 1 on a 9x5 grid.
- Generals: each player's General is a unit on the board with 25 HP; killing the enemy General wins.
- Turn: play cards from hand, then each unit may move up to 2 tiles and attack once; attacked units counterattack if they can reach.
- Mana: mana crystals grow by 1 per turn up to 9; mana springs on the board give 1 extra mana to the unit that steps on them.
- Deploy: minions are summoned next to a friendly unit; once per turn a card can be replaced with a random one from the deck.
- Keywords: Opening Gambit (on play), Dying Wish (on death), Provoke, Rush, Ranged, Flying, Frenzy, Celerity, Blast, Backstab, Zeal, Rebirth, Grow, Infiltrate, Deathwatch.
- Specific: each General has a Bloodborn Spell that charges over turns; positioning on the grid is the core of the game.

## Sources and notes

Sources:
[1] https://store.steampowered.com/app/2004320/Duelyst_II/ (official faction descriptions, Duelyst II)
[2] https://gamewave.fr/duelyst/duelyst-le-jeu-de-carte-aux-six-factions/ (French; six factions)

Neutral is not a faction. Zeal (bonus next to the General) is adjacency; Infiltrate (bonus on the enemy side) is
territory_trigger; Rebirth (comes back from an egg) is cheat_death. No source with named combos was found.

## Factions

### Lyonar Kingdoms
*Claude:* Holy knights: Zeal (bonus next to the General), Divine Bond, healing and Provoke.
Known for: close fighters with Provoke and Zeal, strong board presence, healing, war of attrition [1][2].

### Songhai Empire
*Claude:* Ninja empire: Backstab, cheap spells, teleporting and burst damage.
Known for: displacement, ranged attacks, Backstab, the initiative, spell synergies and damage combos [1]; extended movement,
spell synergy, chained combos, assassins [2].

### Vetruvian Imperium
*Claude:* Desert empire: Obelysks that summon Wind Dervishes, artifacts and Blast.
Known for: short-lived Dervish summons, buffs and debuffs, artifacts that make the General lethal [1][2].

### Abyssian Host
*Claude:* Demons: Shadow Creep tiles, Deathwatch, Wraithling swarms and sacrifice.
Known for: profiting from death (Deathwatch), Shadow Creep, Wraithlings weak alone, strong in numbers [1][2].

### Magmar Aspects
*Claude:* Primal beasts: Rebirth eggs, Grow and big minions.
Known for: resilient units with Grow and Rebirth that are hard to remove [1][2].

### Vanar Kindred
*Claude:* Ice tribes: Infiltrate, walls, Stun and freezing.
Known for: battlefield manipulation with Infiltrate minions and Walls, swift precise removal, the cold [1]; tactical control,
fast movement [2].

## Mechanics
The mechanics the guides name, one per line as `name|concept|regex`, and the rules and terms as `# term:` lines. Read by `coverage.py --mechanics` and `key/key.py`.

```mechanics
# Mechanics the guides name: name|expected concept|wording on the cards. Checked with coverage.py --mechanics (not yet run).
# Sources (21 Oct 2026): store.steampowered.com/app/2004320 (Duelyst II faction descriptions), gamewave.fr six factions.
provoke|taunt|\bprovoke\b
zeal|adjacency|\bzeal\b
backstab|flanking|\bbackstab\b
ranged|ranged|\branged\b
rebirth|revive|\brebirth\b
grow|permanent_growth|\bgrow\b
infiltrate|territory_trigger|\binfiltrate\b
deathwatch|other_death_trigger|\bdeathwatch\b
shadow creep|terrain|\bshadow creep\b
dying wish|death_trigger|\bdying wish\b
opening gambit|on_play|\bopening gambit\b
wraithlings|summon|\b(summon|make)s?\b[^.]{0,40}\bwraithlings?\b
dervish (short-lived)|self_destruct|\bephemeral\b|\bdisappears at the end\b
artifacts on the General|merge_attach|\bequip
displacement and teleport (own units)|movement|\bteleport (a friendly|your general|it)\b|\bswitch positions\b|\bmay move an additional space\b
displacement and teleport (enemies)|forced_movement|\bteleport (an? |that |the )?(random )?enemy\b|\bteleport them\b
heal|heal|\brestore \d+ health\b
dispel|silence|\bdispel\b
stun|disable|\bstun\b
walls|summon|\bsummon[^.]{0,40}\bwalls?\b
# term: Zeal: a bonus while the minion is next to its General (Duelyst II store page: close-quarters fighters with Provoke and Zeal).
# term: Infiltrate: a bonus while the minion is on the enemy's side of the board (assumed: the store page names Infiltrate without defining it).
# term: Deathwatch: triggers when any minion dies (assumed: the store page says Abyssians profit from death through Deathwatch).
```

## Cases
The real-world cases, one per line, tab-separated: `type  a  b  why  source` (see `realworld/RESEARCH.md`). Read by `realworld.py`, `realworld_report.py`, `realworld_why.py` and `learn_recipes.py`.

```tsv
signature	Lyonar Kingdoms	taunt	Provoke	https://store.steampowered.com/app/2004320/Duelyst_II/
signature	Lyonar Kingdoms	adjacency	Zeal	https://store.steampowered.com/app/2004320/Duelyst_II/
signature	Lyonar Kingdoms	heal	healing	https://store.steampowered.com/app/2004320/Duelyst_II/
signature	Songhai Empire	movement	displacement, extended movement	https://store.steampowered.com/app/2004320/Duelyst_II/
signature	Songhai Empire	ranged	ranged attacks	https://store.steampowered.com/app/2004320/Duelyst_II/
signature	Songhai Empire	flanking	Backstab	https://store.steampowered.com/app/2004320/Duelyst_II/
signature	Songhai Empire	on_spell	spell synergies	https://store.steampowered.com/app/2004320/Duelyst_II/
signature	Vetruvian Imperium	self_destruct	short-lived Dervishes	https://store.steampowered.com/app/2004320/Duelyst_II/
splash	Vetruvian Imperium	buff	buffs (Lyonar's specialty; Vetruvian's own buffs are the artifacts on the General)	https://store.steampowered.com/app/2004320/Duelyst_II/
signature	Abyssian Host	other_death_trigger	Deathwatch	https://store.steampowered.com/app/2004320/Duelyst_II/
signature	Abyssian Host	terrain	Shadow Creep	https://store.steampowered.com/app/2004320/Duelyst_II/
signature	Abyssian Host	summon	Wraithlings	https://store.steampowered.com/app/2004320/Duelyst_II/
signature	Abyssian Host	board_presence	strong in numbers	https://store.steampowered.com/app/2004320/Duelyst_II/
signature	Magmar Aspects	permanent_growth	Grow	https://store.steampowered.com/app/2004320/Duelyst_II/
signature	Magmar Aspects	revive	Rebirth	https://store.steampowered.com/app/2004320/Duelyst_II/
signature	Vanar Kindred	territory_trigger	Infiltrate	https://store.steampowered.com/app/2004320/Duelyst_II/
signature	Vanar Kindred	removal	swift, precise removal	https://store.steampowered.com/app/2004320/Duelyst_II/
archetype	Lyonar Kingdoms	sustain	healing, war of attrition	https://store.steampowered.com/app/2004320/Duelyst_II/
archetype	Songhai Empire	spellslinger	spell synergies and damage combos	https://store.steampowered.com/app/2004320/Duelyst_II/
archetype	Songhai Empire	positional	displacement and movement	https://store.steampowered.com/app/2004320/Duelyst_II/
archetype	Abyssian Host	swarm	Wraithlings in numbers	https://store.steampowered.com/app/2004320/Duelyst_II/
archetype	Abyssian Host	sacrifice	profiting from death	https://store.steampowered.com/app/2004320/Duelyst_II/
archetype	Magmar Aspects	scaling	Grow	https://store.steampowered.com/app/2004320/Duelyst_II/
archetype	Vanar Kindred	control	tactical control	https://gamewave.fr/duelyst/duelyst-le-jeu-de-carte-aux-six-factions/
archetype	Vanar Kindred	positional	battlefield manipulation	https://store.steampowered.com/app/2004320/Duelyst_II/
```

## Notes from the patterns check
- Artifacts (category item) are deck cards equipped on the General: `merge_attach`, not `items_consumables`. What an artifact
  gives the General is `buff` (and stat_gain or the keyword where it says so).
- Rebirth (a Dying Wish that leaves an Egg, which hatches into the minion) is `revive`, not `cheat_death`.
- Replace (put a card from the action bar back for a new one) is a redraw, not `recycle`; replacing the whole action bar is
  `hand_deck_swap`. "Action bar" is the hand.
- Celerity is `multi_attack`; Rush is `haste`; "in front of" is a grid space, not a lane; a space that turns into Shadow Creep or
  Exhuming Sand is `terrain`, not `transform`. Transforming ANY minion is `polymorph` (and `transform`).
- Tribal: a card that picks, counts or targets cards by tribe (a random Battle Pet, a Vespyr minion from your deck, another
  Wraithling); summoning a named token of a tribe is not tribal.
- Teleporting enemies is `forced_movement`; teleporting your own minions or General, swapping and extra move are `movement`.
- Cases removed: Lyonar "strong board presence" (the store page says Provoke and Zeal give the presence; both are cases) and
  Songhai `combo_sequence` (no card cares about play order; the store page's "damage combos" are the spell synergies).
- Cases removed (the cards show no Vetruvian lead; the store page's words fit the whole game): Dervish summons (Vetruvian
  summons on 24% of its cards, Abyssian 28%, Magmar 24%; its own part, the short-lived Dervishes, is the `self_destruct` case);
  artifacts on the General (every faction has 7 artifacts); debuffs (4 of 94 cards).
