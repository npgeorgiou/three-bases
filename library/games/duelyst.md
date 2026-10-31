# Duelyst

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*From the game's own texts: the open-sourced client (github.com/open-duelyst/duelyst, commit 2843f24): tutorial and tips
(app/localization/locales/en/tutorial.json, game_tips.json) and rule constants (app/common/config.js, app/sdk/board.coffee);
each line names its source. Checked 29 Oct 2026.*
- Board: 5 rows by 9 columns (config BOARDROW, BOARDCOL).
- Generals: each player's General is a unit on the board; "If you run out of Health, you lose"; deal enough damage to the
  enemy General to win (tutorial lesson 1). Generals have 25 Health (card factories: General maxHP 25).
- Moving: units can move up to 2 spaces (tutorial; tip novice_tip_22); allies can move through each other, but not through
  enemies (novice_tip_9); actions are movements followed by attacks, a unit cannot attack and then move (novice_tip_38).
- Attacking: a unit attacks an enemy by moving onto it; the General attacks too, also diagonally (tutorial lessons 1, 4);
  melee units reach the spaces next to them, Ranged units the whole board (config REACH_MELEE 1, REACH_RANGED).
- Counterattack: "Your minions will always counterattack, even if they get destroyed" (novice_tip_2); Blast minions are
  counterattacked by Ranged minions (medium_tip_17); Frenzy minions only by their attack target (medium_tip_20).
- Summoning: minions are summoned on a space around any friendly unit (board.coffee getValidSpawnPositions); Airdrop
  anywhere (medium_tip_1); minions must wait a turn to attack (tutorial), Rush acts at once (medium_tip_10).
- Mana: 1 more Mana at the start of your turn, up to 9 (novice_tip_31); Player 2 starts with an extra mana crystal
  (novice_tip_33); occupying a Mana Spring gives +1 bonus Mana for that turn (novice_tip_0).
- Cards: you draw one new card each turn (tutorial); replace one card per turn (novice_tip_23), never getting the same copy
  back (novice_tip_24); cards drawn past the hand limit (6, config MAX_HAND_SIZE) are destroyed (novice_tip_27); decks are
  40 cards with the General, at most 3 copies (config MAX_DECK_SIZE, MAX_DECK_DUPLICATES).
- Artifacts are equipped on your General, up to 3 at a time (novice_tip_1); an artifact is destroyed when the General has
  taken damage three times (medium_tip_16; keyword Destructible).
- Bloodbound Spell: each General's own spell; it counts down each turn until it refreshes (tutorial lesson 4).
- Effects that only target minions do not apply to Generals (medium_tip_19).

## Deck rule (deck_analysis.DECK_RULES, can_share; 31 Oct 2026)
A deck is 40 cards: one General and 39 cards from that General's faction plus Neutral, at most 3 copies of a card
(bandainamcoent.com/news/new-player-guide-getting-started, 3 Nov 2017). So a Lyonar card and a Songhai card never share a
deck, and two Generals never do. Tutorial cards and the Boss battle cards (Living Flame, Holiday Gift) are no deck cards:
boss battles are fights against computer bosses with their own decks (mmobomb.com/news/duelyst-testing-boss-battles-taking-daily-challenges-offline).

## Sources and notes

Sources:
[1] https://store.steampowered.com/app/2004320/Duelyst_II/ (official faction descriptions, Duelyst II)
[2] https://gamewave.fr/duelyst/duelyst-le-jeu-de-carte-aux-six-factions/ (French; six factions)
[3] https://github.com/open-duelyst/duelyst commit 2843f24 (the open-sourced game: cards, texts, tutorial, tips, rules)
[4] https://duelspot.com/ deck pages and the Duelyst forum archive (static.animalcracker.art/duelyst/forum_archive): the decks below

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
# term: Zeal: Gains a bonus effect when nearby your General (modifiers.json); minions lose the Zeal buff when not adjacent to their General (game_tips medium_tip_26).
# term: Infiltrate: Gains a bonus while on the enemy side of the battlefield (modifiers.json, the game's keyword text).
# term: Deathwatch: Triggers effect whenever ANY minion dies (modifiers.json; game_tips medium_tip_4).
```

## Decks
Ten full decks (40 cards with the General) for the deck tests, each from a deck code on the page (decoded with the card ids
of [3]; codes in cards_db/supplement/duelyst_deck_codes.tsv). The authors' plans, in Claude's words:
- Argeon Mechaz0r (duelspot 4k-spirit-lyonar-mirror-mechs): build MECHAZ0R from its pieces, Lifestream and Mirrorrim find
  them, Metaltooth for burst.
- Vaath Dying Wish (duelspot dying-wish-vaath): Dying Wish minions with Cascading Rebirth; Grimes cascades into big
  minions; Unseven pulls Dagona; Dagona + Cascading Rebirth + Homeostatic Rebuke for 15 damage; Fractal Replication copies.
- Cassyva Replace Abomination (duelspot replace-abomination): replace cards (Aethermaster, White Widow, Inquisitor Kron,
  Wings of Paradise) build stats; Abhorrent Unbirth fuses the board and needs a Rush minion (Kron's or Letigress's tokens).
- Faie Blood Taura (duelspot blood-faice): trade face and burn; Blood Taura costs your General's health; Spirit
  of the Wild reactivates Flameblood Warlocks, Blazing Spines, Disciples of Yggdra; Hearth-Sisters switch positions with them.
- Shidai Artifacts (duelspot one-woman-army-shidai): Bangle of Blinding Strike and Cyclone Mask; Mask of Shadows to get
  behind an enemy then Bangle; Flicker with Cyclone Mask; Saberspine Seal with Bangle; Crescent Spear adds damage to damage spells.
- Kaleos Trial of Songhai (duelspot replace-ox): finish the Trial to summon Hideatsu the Ebon Ox, then each summoned minion
  deals damage equal to its cost; minions of many costs.
- Argeon Dawn's Eye aggro (duelspot dawns-eyeggro-patreon): cheap minions take the board early, trade, chip the enemy
  General, burst at the end.
- Lilithe Darkfire (forum: Unearthed Prophecies: Lilithe part two): Darkfire Sacrifice makes the next minion cost 2 less for big minions (Vorpal
  Reaver, Desolator, a good sacrifice); Phantasm wants a hand of strong targets; Daemonic Lure against repositioning.
- Argeon Intensify Riftwalker (forum: DeathsAdvocate's master thread): Mirrorrim and Lifestream on Riftwalker; Replicants
  and Sun Wisps thin the deck so the Riftwalkers come back.
- Ciphyron Build (forum: DeathsAdvocate's master thread): Build cards protected by Ciphyron's defensive tools.

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
