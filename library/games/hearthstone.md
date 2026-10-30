# Hearthstone

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*Claude's summary (Oct 2026), from general knowledge of the game and the rules and terms under Mechanics; not from the sources below.*
- Genre: digital collectible card game (Blizzard, 2014); 1 vs 1, heroes with 30 health, 30-card decks.
- Mana: one mana crystal per turn up to 10, refilled every turn. The second player gets The Coin (1 extra mana once).
- Board: up to 7 minions per side. Minions can attack the turn after they are played (unless Charge or Rush).
- Each class has a Hero Power (2 mana, once per turn); weapons let the hero attack.
- Card types: minions, spells, secrets, weapons, hero cards, locations.
- Keywords: Battlecry, Deathrattle, Taunt, Divine Shield, Charge, Rush, Windfury, Stealth, Lifesteal, Poisonous, Discover, Combo, Overload, Outcast, Spell Damage, Freeze, Reborn, Corpses and Runes (Death Knight).
- Win: reduce the enemy hero to 0 health.

## Sources and notes

Sources:
[1] https://hearthstone.wiki.gg/wiki/Classes (class descriptions)
[2] https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/ (2019 class identity
    chart: strengths = what a class excels at; limitations = shows up a few times, limited in power and number of cards;
    weaknesses = lacks; archetypes named per class; no Demon Hunter or Death Knight)
[3] https://hearthstone.blizzard.com/en-us/news/23305788 (Demon Hunter reveal)
[4] https://hearthstone.wiki.gg/wiki/Demon_Hunter
[5] https://www.hearthstonetopdecks.com/vengeance-revisited-what-is-demon-hunters-new-identity/
[6] https://hearthstone.blizzard.com/en-us/news/23852696 (Death Knight deep dive)
[7] https://hearthstone.wiki.gg/wiki/Death_Knight
[8] https://www.keengamer.com/articles/guides/7-great-hearthstone-card-combos/
[9] https://primagames.com/tips/hearthstone-powerful-card-combos

No concept for weapons (Paladin, Rogue, Warrior, Demon Hunter) or hero attack as such; Demon Hunter's one-turn hero Attack is
temporary_buff. Armor (Warrior) absorbs damage until used up: block_armor.

## Factions

### Druid
*Claude:* Nature: mana ramp, Choose One cards, armor and big minions.
Known for: speeding up mana gain [1][2]; Taunt minions [1]; Choose One [1]; giant minions, minion swarms, card draw, Beasts [2].
Archetypes: Token Druid, Beast Druid, Big Druid, Taunt Druid; also Malygos, Jade [2].

### Hunter
*Claude:* Aggression: beasts, secrets and damage to the enemy hero.
Known for: Beasts [1][2]; direct damage to the face [1][2]; Secrets / traps [1][2]; Deathrattle [2].
Limitations: card draw and generation, board clear, Taunt [2].
Archetypes: Face, Midrange (Beasts), Secret, Deathrattle [2].

### Mage
*Claude:* Spells: burn, Freeze, secrets and spell generation.
Known for: single-target and area damage, Freeze, spell synergy, Secrets [1]; spells, damage spells, board clear [2].
Limitations: minion swarms [2].
Archetypes: Freeze, Tempo, Mech, Murloc [2].

### Paladin
*Claude:* Holy warriors: Divine Shield, buffs, Silver Hand Recruits and healing.
Known for: Divine Shield, Blessings, healing, weakening enemies, Secrets [1]; minion swarms, buffs and debuffs, healing,
Divine Shield, Secrets [2].
Limitations: cost reduction [2].
Archetypes: Odd, Even, Midrange, Secret, Control, Mech [2].

### Priest
*Claude:* Control: healing, copying and stealing the opponent's cards.
Known for: healing [1][2]; destroying enemies and taking control of them (mind control) [1]; copying, single-minion buffs,
Deathrattle [2].
Limitations: card draw [2].
Archetypes: Dragon, Wall, Big, Raza, Nomi, Silence [2].

### Rogue
*Claude:* Tricks: Combo, cheap cards, weapons, Stealth and card generation.
Known for: Combo [1][2]; destroying single minions, card draw, Deathrattle [2].
Archetypes: Miracle, Oil, Tempo, Deathrattle [2].

### Shaman
*Claude:* Elements: Overload, totems, elementals and evolve effects.
Known for: Totems, Elementals [1][2]; Overload [1]; minion swarms, damage spells, Murlocs [2].
Archetypes: Token, Murloc, Aggro, Big, Elemental, Control [2].

### Warlock
*Claude:* Demons: health as a resource, discard and self-damage.
Known for: Demons, sacrificing life, cards or its own minions, paying Health to draw [1]; sacrifice, card draw, minion swarms,
disruption [2].
Archetypes: Zoo, Control, Malygos [2].

### Warrior
*Claude:* Armor, weapons and damaged-minion synergies.
Known for: armor, on-damage (Enrage) effects, minions with Charge [1]; armor, Taunt, destroying minions [2].
Limitations: card draw and generation [2].
Archetypes: Control, Pirate [2].

### Demon Hunter
*Claude:* Aggression: hero attacks, Outcast and cheap demons.
Known for: Outcast (bonus from the leftmost or rightmost card in hand) [3][4][5]; hero Attack for one turn [1][3][4];
Lifesteal [5]; Demons [1][3]; great card draw [4]; chip and burst damage [4][5].
Archetypes: aggressive or midrange [3][4]; Demon tribal, tokens, Lifesteal builds [5].

### Death Knight
*Claude:* Undead: runes (Blood, Frost, Unholy) limit the deck; Corpses are a second resource.
Known for: Corpses, a second resource gained when friendly minions die and spent on cards [6][7]; Runes that decide which
cards a deck may hold [6][7]; Undead and going wide (Unholy), Freeze and burst (Frost), tankiness (Blood) [6][7].
Archetypes: Blood control, Frost burn, Unholy zoo [7].

## Combos
- Auchenai Soulpriest + Circle of Healing: healing becomes 4 damage to every minion [8][9]
- Equality + Consecration: health set to 1, then 2 damage to each enemy [8]
- Leeroy Jenkins + Shadowstep: Charge 6 damage, back to hand, again [8][9]
- Unleash the Hounds + Raid Leader / Stormwind Champion / Hunter's Mark: buffs the charging Hounds; Mark lowers targets [8]
- Injured Blademaster + Circle of Healing: heals the damaged 4/7 [9]
- Ancestral Spirit + Cairne Bloodhoof: resummoned Cairne summons again on death [9]
- Force of Nature + Savage Roar: three charging 2/2s get +2 attack [9]
- Deadly Poison or Assassin's Blade + Blade Flurry: weapon damage hits all enemies [9]
- Divine Spirit + Inner Fire: named as the pair Priest decks need [2]
- Venomizer + Missile Launcher: Hunter's board clear [2]

## Mechanics
The mechanics the guides name, one per line as `name|concept|regex`, and the rules and terms as `# term:` lines. Read by `coverage.py --mechanics` and `key/key.py`.

```mechanics
# Mechanics the guides name: name|expected concept|wording on the cards. Checked with coverage.py --mechanics (not yet run).
# Sources (21 Oct 2026): hearthstone.wiki.gg/wiki/Classes, hearthstone.wiki.gg/wiki/Demon_Hunter, hearthstone.wiki.gg/wiki/Death_Knight,
# hearthstonetopdecks.com class identity (2019), hearthstone.blizzard.com/en-us/news/23305788 (Demon Hunter), /23852696 (Death Knight).
taunt|taunt|\btaunt\b
divine shield|shield|\bdivine shield\b
charge|haste|\bcharge\b
rush|haste|\brush\b
choose one|modal_choice|\bchoose one\b
mana gain (ramp)|resource_gain|\bmana crystals?\b
deathrattle|death_trigger|\bdeathrattle\b
battlecry|on_play|\bbattlecry\b
secret|trap_secret|\bsecret\b
freeze|disable|\bfreezes?\b
spell damage and spell synergy|on_spell|\bwhenever you cast a spell\b|\bafter you cast a spell\b
overload|overload_debt|\boverload\b
combo|combo_sequence|\bcombo\b
lifesteal|lifesteal|\blifesteal\b
outcast|hand_position|\boutcast\b
hero attack this turn|temporary_buff|\byour hero \+\d+ attack this turn\b
armor|block_armor|\b(gain|gains) \d+ armor\b|\barmor\b
enrage and on-damage|on_damaged|\bwhenever (this|it) (takes|is dealt) damage\b|\benrage\b
corpses|coin_economy|\bcorpses?\b
take control (mind control)|steal|\btake control\b
destroy a minion|destroy|\bdestroy (a|an|all|target)\b
copy|copy|\bcop(y|ies) of\b
discard|discard|\bdiscard\b
pay health|life_payment|\bdeal \d+ damage to your hero\b|\bcosts? health\b
heal|heal|\brestore \d+ health\b
draw cards|draw|\bdraw (a|\d+|two|three) cards?\b
summon minions|summon|\bsummon (a|an|two|three|\d+)\b
tribes (beast, demon, murloc, elemental, totem, undead, pirate, mech, dragon)|tribal|\b(beast|demon|murloc|elemental|totem|undead|pirate|mech|dragon)s?\b
# term: Outcast: a bonus when the card is played from the leftmost or rightmost position in the hand (hearthstone.blizzard.com Demon Hunter reveal).
# term: Corpses: a Death Knight resource; whenever a friendly minion dies you gain a Corpse, which some cards spend (hearthstone.blizzard.com Death Knight deep dive).
# term: Runes: a Death Knight deck picks three Runes (Blood, Frost, Unholy), which decide which Death Knight cards it may hold (same source).
# term: Demon Claws: the Demon Hunter hero power, 1 mana, +1 Attack to the hero this turn (Demon Hunter reveal).
# term: Ghoul Charge: the Death Knight hero power, 2 mana, a 1/1 Ghoul with Charge that dies at the end of the turn (Death Knight deep dive).
# term: Hero power: each class has its own; most cost 2 mana (hearthstone.wiki.gg/wiki/Demon_Hunter).
```

## Cases
The real-world cases, one per line, tab-separated: `type  a  b  why  source` (see `realworld/RESEARCH.md`). Read by `realworld.py`, `realworld_report.py`, `realworld_why.py` and `learn_recipes.py`.

```tsv
signature	Druid	resource_gain	speeds up mana gain	https://hearthstone.wiki.gg/wiki/Classes
signature	Druid	taunt	strong Taunt minions	https://hearthstone.wiki.gg/wiki/Classes
signature	Druid	modal_choice	flexible Choose One effects	https://hearthstone.wiki.gg/wiki/Classes
signature	Druid	high_cost	giant minions	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Druid	board_presence	minion swarms	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Druid	draw	card draw	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Druid	tribal	Beasts	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Hunter	tribal	Beasts	https://hearthstone.wiki.gg/wiki/Classes
signature	Hunter	direct_damage	face damage	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Hunter	trap_secret	Secrets and traps	https://hearthstone.wiki.gg/wiki/Classes
signature	Hunter	death_trigger	Deathrattle	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Mage	aoe_damage	area-of-effect damage	https://hearthstone.wiki.gg/wiki/Classes
signature	Mage	disable	Freeze	https://hearthstone.wiki.gg/wiki/Classes
signature	Mage	on_spell	spell synergy	https://hearthstone.wiki.gg/wiki/Classes
signature	Mage	trap_secret	Secrets	https://hearthstone.wiki.gg/wiki/Classes
signature	Mage	board_wipe	board clear	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Paladin	shield	Divine Shield	https://hearthstone.wiki.gg/wiki/Classes
signature	Paladin	heal	healing	https://hearthstone.wiki.gg/wiki/Classes
signature	Paladin	debuff	weakens enemies	https://hearthstone.wiki.gg/wiki/Classes
signature	Paladin	trap_secret	Secrets	https://hearthstone.wiki.gg/wiki/Classes
signature	Paladin	board_presence	minion swarms	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Paladin	buff	minion buffs	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Priest	heal	restorative healing	https://hearthstone.wiki.gg/wiki/Classes
signature	Priest	steal	seizing control of enemy minds	https://hearthstone.wiki.gg/wiki/Classes
signature	Priest	destroy	destroying enemies	https://hearthstone.wiki.gg/wiki/Classes
signature	Priest	copy	copying	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Priest	death_trigger	Deathrattle	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Rogue	combo_sequence	Combo	https://hearthstone.wiki.gg/wiki/Classes
signature	Rogue	destroy	destroying individual minions	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Rogue	draw	card draw	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Rogue	death_trigger	Deathrattle	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Shaman	tribal	Totems, Elementals, Murlocs	https://hearthstone.wiki.gg/wiki/Classes
signature	Shaman	overload_debt	Overload	https://hearthstone.wiki.gg/wiki/Classes
signature	Shaman	board_presence	minion swarms	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Shaman	damage	damage spells	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Warlock	tribal	Demons	https://hearthstone.wiki.gg/wiki/Classes
signature	Warlock	sacrifice	sacrifices its own minions	https://hearthstone.wiki.gg/wiki/Classes
signature	Warlock	life_payment	trades Health to draw	https://hearthstone.wiki.gg/wiki/Classes
signature	Warlock	discard	sacrifices cards	https://hearthstone.wiki.gg/wiki/Classes
signature	Warlock	draw	card draw	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Warlock	board_presence	minion swarms	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Warlock	disruption	disruption	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Warrior	block_armor	armor	https://hearthstone.wiki.gg/wiki/Classes
signature	Warrior	on_damaged	Enrage and on-damage effects	https://hearthstone.wiki.gg/wiki/Classes
signature	Warrior	haste	sends minions charging	https://hearthstone.wiki.gg/wiki/Classes
signature	Warrior	taunt	Taunt	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Warrior	destroy	destroying minions	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
signature	Demonhunter	hand_position	Outcast	https://hearthstone.blizzard.com/en-us/news/23305788
signature	Demonhunter	temporary_buff	hero Attack for one turn	https://hearthstone.wiki.gg/wiki/Classes
signature	Demonhunter	lifesteal	Lifesteal	https://www.hearthstonetopdecks.com/vengeance-revisited-what-is-demon-hunters-new-identity/
signature	Demonhunter	tribal	Demons	https://hearthstone.blizzard.com/en-us/news/23305788
signature	Demonhunter	draw	great card draw	https://hearthstone.wiki.gg/wiki/Demon_Hunter
signature	Deathknight	coin_economy	Corpses, a resource spent on cards	https://hearthstone.blizzard.com/en-us/news/23852696
signature	Deathknight	deckbuilding_effect	Runes decide the deck	https://hearthstone.blizzard.com/en-us/news/23852696
signature	Deathknight	tribal	Undead (Unholy)	https://hearthstone.blizzard.com/en-us/news/23852696
signature	Deathknight	board_presence	going wide (Unholy)	https://hearthstone.wiki.gg/wiki/Death_Knight
signature	Deathknight	disable	Freeze (Frost)	https://hearthstone.blizzard.com/en-us/news/23852696
archetype	Druid	swarm	Token Druid	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Druid	tribal	Beast Druid	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Druid	ramp	Big Druid, mana gain	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Druid	fortress	Taunt Druid	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Hunter	aggro_tempo	Face Hunter	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Hunter	tribal	Midrange Beast Hunter	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Hunter	trickery	Secret Hunter	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Mage	aggro_tempo	Tempo Mage	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Mage	tribal	Mech and Murloc Mage	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Mage	spellslinger	strong spell synergy	https://hearthstone.wiki.gg/wiki/Classes
archetype	Paladin	trickery	Secret Paladin	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Paladin	tribal	Mech Paladin	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Paladin	control	Control Paladin	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Paladin	swarm	minion swarms	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Priest	tribal	Dragon Priest	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Priest	fortress	Wall Priest	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Priest	sustain	healing	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Rogue	aggro_tempo	Tempo Rogue	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Shaman	swarm	Token Shaman	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Shaman	tribal	Murloc and Elemental Shaman	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Shaman	aggro_tempo	Aggro Shaman	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Shaman	control	Control Shaman	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Warlock	swarm	Zoo, minion swarms	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Warlock	control	Control Warlock	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Warrior	control	Control Warrior	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Warrior	tribal	Pirate Warrior	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Warrior	fortress	armor and Taunt	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
archetype	Demonhunter	aggro_tempo	aggressive decks	https://hearthstone.wiki.gg/wiki/Demon_Hunter
archetype	Demonhunter	tribal	Demon tribal	https://www.hearthstonetopdecks.com/vengeance-revisited-what-is-demon-hunters-new-identity/
archetype	Demonhunter	swarm	token decks	https://www.hearthstonetopdecks.com/vengeance-revisited-what-is-demon-hunters-new-identity/
archetype	Demonhunter	sustain	Lifesteal builds	https://www.hearthstonetopdecks.com/vengeance-revisited-what-is-demon-hunters-new-identity/
archetype	Deathknight	control	Blood control	https://hearthstone.wiki.gg/wiki/Death_Knight
archetype	Deathknight	burn	Frost burn	https://hearthstone.wiki.gg/wiki/Death_Knight
archetype	Deathknight	swarm	Unholy zoo	https://hearthstone.wiki.gg/wiki/Death_Knight
splash	Hunter	draw	card draw is a limitation	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
splash	Hunter	generate_cards	card generation is a limitation	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
splash	Hunter	board_wipe	board clear is a limitation	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
splash	Hunter	taunt	Taunt is a limitation	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
splash	Mage	board_presence	minion swarms are a limitation	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
splash	Paladin	cost_reduction	cost reduction is a limitation	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
splash	Priest	draw	card draw is a limitation	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
splash	Warrior	draw	card draw is a limitation	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
splash	Warrior	generate_cards	card generation is a limitation	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
combo	Auchenai Soulpriest	Circle of Healing	healing becomes damage to all minions	https://www.keengamer.com/articles/guides/7-great-hearthstone-card-combos/
combo	Equality	Consecration	health set to 1, then 2 damage to each enemy	https://www.keengamer.com/articles/guides/7-great-hearthstone-card-combos/
combo	Leeroy Jenkins	Shadowstep	charge, return to hand, again	https://www.keengamer.com/articles/guides/7-great-hearthstone-card-combos/
combo	Unleash the Hounds	Raid Leader	buffs the charging Hounds	https://www.keengamer.com/articles/guides/7-great-hearthstone-card-combos/
combo	Unleash the Hounds	Stormwind Champion	buffs the charging Hounds	https://www.keengamer.com/articles/guides/7-great-hearthstone-card-combos/
combo	Unleash the Hounds	Hunter's Mark	Mark lowers targets for the Hounds	https://www.keengamer.com/articles/guides/7-great-hearthstone-card-combos/
combo	Injured Blademaster	Circle of Healing	heals the damaged Blademaster	https://primagames.com/tips/hearthstone-powerful-card-combos
combo	Ancestral Spirit	Cairne Bloodhoof	resummoned Cairne summons again on death	https://primagames.com/tips/hearthstone-powerful-card-combos
combo	Force of Nature	Savage Roar	three charging 2/2s get +2 attack	https://primagames.com/tips/hearthstone-powerful-card-combos
combo	Deadly Poison	Blade Flurry	weapon damage hits all enemies	https://primagames.com/tips/hearthstone-powerful-card-combos
combo	Assassin's Blade	Blade Flurry	weapon damage hits all enemies	https://primagames.com/tips/hearthstone-powerful-card-combos
combo	Divine Spirit	Inner Fire	the pair Priest decks need	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
combo	Venomizer	Missile Launcher	Hunter's board clear	https://www.hearthstonetopdecks.com/class-identity-in-hearthstone-the-past-the-present-and-the-future/
```
