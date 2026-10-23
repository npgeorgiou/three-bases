# The Elder Scrolls: Legends

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*Claude's summary (Oct 2026), from general knowledge of the game and the rules and terms under Mechanics; not from the sources below.*
- Genre: digital collectible card game (Bethesda, The Elder Scrolls: Legends, 2017).
- Board: two lanes; creatures entering the shadow lane get Cover for a turn; creatures fight only in their own lane.
- Health and runes: 30 health with 5 runes; each rune broken draws a card, and a Prophecy card drawn this way can be played for free.
- Magicka: grows by 1 per turn up to 12; the second player gets the Ring of Magicka.
- Decks: 50 or more cards, one or two attributes (three in some decks).
- Keywords: Guard, Ward, Charge, Breakthrough, Drain, Lethal, Regenerate, Pilfer, Last Gasp, Summon, Prophecy, Slay, Rally.
- Win: reduce the opponent to 0 health.

## Sources and notes

Sources:
[1] https://en.uesp.net/wiki/Legends:Attributes
[2] https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes (official beginner's guide)
[3] https://elderscrollslegends.wiki.fextralife.com/Attributes
[4] https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight
[5] https://bethesda.net/en-US/news/top-highlights-of-the-month-november-2018

Neutral is not a faction. Two-attribute classes are listed in [2] without playstyles. No source names what an attribute has
only a little of.

## Factions

### Strength
*Claude:* Red: aggression, weapons and Breakthrough.
Known for: direct, head-on attacks that remove enemies before they use tricks [1]; pure power, considerable force [2][3].
Weak at: lower defences than Endurance [2].

### Intelligence
*Claude:* Blue: actions, spells and control.
Known for: trickery and magic, spells, weapons, conjured Atronachs, destruction and long-term planning [1]; many spells with
random, unpredictable outcomes, creatures with tricks [2][3].

### Willpower
*Claude:* Yellow: wide boards of small creatures and buffs.
Known for: amassing large armies, strong defences, boosting forces with magic, destroying enemy creatures or bending them to
your will [1]; going wide with many small creatures that help each other, the greatest ability to deal with threats [2][3].

### Agility
*Claude:* Green: Lethal, Pilfer and Charge.
Known for: poison and precision against larger foes, cover and movement to slip past enemies [1]; Lethal and Pilfer, moving
creatures between lanes, speed [2][3].

### Endurance
*Claude:* Purple: big creatures, Guard and health.
Known for: large creatures, strong guards, healing actions, more Magicka [1]; Guard, more magicka, heals for player and
creature, many high-cost, high-power creatures [2][3].

## Combos
- Snowy Sabre Cat + Swift Strike / Crusader's Assault / Monk's Strike: power boosts for a huge one-turn attack [4]
- Doomcrag Vampire + Nord Firebrand / Sharpshooter Scout: pings take down big creatures [4]
- Disciple of Namira + Namira's Shrine: draw lots of cards [4]
- Paarthurnax / Blood Magic Lord / Odirniran Necromancer + Soultear: reuse for value [4]
- Odirniran Necromancer + Galyn The Shelterer: more power and targets [4]
- Ulfric's Uprising + Nix-Ox / Therana: re-triggers and extra copies [4][5]
- Ring of Namira + The Night Mother: her life gain becomes damage [5]
- Devour + Territorial Viper: gives Wildfire Dragon Lethal and Charge [5]
- Wildfire Dragon + Brotherhood Sanctuary: repeats its +7/+7 [5]
- Dremora Markynaz + Dagoth Ur: grows Dagoth Ur [5]

## Mechanics
The mechanics the guides name, one per line as `name|concept|regex`, and the rules and terms as `# term:` lines. Read by `coverage.py --mechanics` and `key/key.py`.

```mechanics
# Mechanics the guides name (source in brackets): name|expected concept|wording on the cards. Checked with coverage.py --mechanics.
# https://bethesda.net/en-AU/news/beginners-guide-to-attributes-and-classes
# Rules and terms for the game block (key.py read), only facts the source states: https://en.uesp.net/wiki/Legends:Guard (and its keyword navigation)
# term: Enemy Guard creatures in a lane must be destroyed before other creatures in that lane can damage the opponent's health.
# term: The shadow lane gives Cover; damage to a player breaks Runes; some effects gain max magicka.
# term: Keywords and mechanics: Guard, Prophecy, Regenerate, Last Gasp, Pilfer, Cover, Shackle, Silence, Charge, Drain, Breakthrough, Lethal, Ward, Rally, Exalt, Slay, Summon, Consume, Veteran, Plot, Treasure Hunt, Mobilize, Betray, Assemble, Empower, Ongoing, Wax, Wane, Wounded, Activate, Move.
# Rules and terms assumed from game knowledge (no source found; Kaptain: assume when no source exists)
# term: Ongoing: a support whose effect lasts while it stays in play (assumed)
# term: Beast Form: the creature turns into its stronger beast version once its condition is met (assumed)
atronachs|summon|\batronach
equip items|merge_attach|\bequip|\bitem
random spells|random_effect|\brandom
summon many|summon|\bsummon (a|an|two|three|\d)
take control|steal|\b(take|gain|steal)s? control\b|\bsteal\b
lethal|deathtouch|\blethal\b
move lanes|movement|\bmove\b|\bswitch lanes?\b|\bother lane\b
cover|immunity|\bcover\b|\bshadow lane\b
pilfer|on_attack|\bpilfer\b
guard|taunt|\bguard\b
increase magicka|resource_gain|\bmagicka\b
healing|heal|\bheal|\bgain \d+ health\b|\bdrain\b
big creatures|stat_condition|\bwith \d+ (power|health) or (more|greater)\b
prophecy|free_play|\bprophecy\b
```

## Cases
The real-world cases, one per line, tab-separated: `type  a  b  why  source` (see `realworld/RESEARCH.md`). Read by `realworld.py`, `realworld_report.py`, `realworld_why.py` and `learn_recipes.py`.

```tsv
signature	Strength	removal	removes enemies head-on	https://en.uesp.net/wiki/Legends:Attributes
signature	Intelligence	random_effect	spells with random outcomes	https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes
signature	Intelligence	generate_cards	conjured Atronachs	https://en.uesp.net/wiki/Legends:Attributes
signature	Intelligence	merge_attach	weapons	https://en.uesp.net/wiki/Legends:Attributes
signature	Willpower	board_presence	going wide	https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes
signature	Willpower	buff	boosting forces with magic	https://en.uesp.net/wiki/Legends:Attributes
signature	Willpower	steal	bending enemies to your will	https://en.uesp.net/wiki/Legends:Attributes
signature	Willpower	destroy	destroying enemy creatures	https://en.uesp.net/wiki/Legends:Attributes
signature	Agility	deathtouch	Lethal	https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes
signature	Agility	movement	moving creatures between lanes	https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes
signature	Agility	on_attack	Pilfer	https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes
signature	Endurance	taunt	Guard	https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes
signature	Endurance	resource_gain	more magicka	https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes
signature	Endurance	heal	heals for player and creature	https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes
signature	Endurance	high_cost	high-cost, high-power creatures	https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes
archetype	Strength	aggro_tempo	head-on attacks, pure power	https://en.uesp.net/wiki/Legends:Attributes
archetype	Intelligence	chaos	random, unpredictable spells	https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes
archetype	Intelligence	spellslinger	trickery and magic, spells	https://en.uesp.net/wiki/Legends:Attributes
archetype	Willpower	swarm	going wide	https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes
archetype	Willpower	control	greatest ability to deal with threats	https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes
archetype	Agility	positional	lane movement	https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes
archetype	Endurance	fortress	strong guards	https://en.uesp.net/wiki/Legends:Attributes
archetype	Endurance	ramp	more magicka, high-cost creatures	https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes
archetype	Endurance	sustain	healing actions	https://bethesda.net/de-DE/news/beginners-guide-to-attributes-and-classes
combo	Snowy Sabre Cat	Swift Strike	one-turn attack	https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight
combo	Snowy Sabre Cat	Crusader's Assault	one-turn attack	https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight
combo	Snowy Sabre Cat	Monk's Strike	one-turn attack	https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight
combo	Doomcrag Vampire	Nord Firebrand	pings take down big creatures	https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight
combo	Doomcrag Vampire	Sharpshooter Scout	pings take down big creatures	https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight
combo	Disciple of Namira	Namira's Shrine	draw lots of cards	https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight
combo	Paarthurnax	Soultear	reuse for value	https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight
combo	Blood Magic Lord	Soultear	reuse for value	https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight
combo	Odirniran Necromancer	Soultear	more power	https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight
combo	Odirniran Necromancer	Galyn The Shelterer	more power and targets	https://bethesda.net/en-US/news/houses-of-morrowind-community-deck-spotlight
combo	Ulfric's Uprising	Nix-Ox	re-triggers Nix-Ox for magicka	https://bethesda.net/en-US/news/top-highlights-of-the-month-november-2018
combo	Therana	Ulfric's Uprising	extra copies of Uprising	https://bethesda.net/en-US/news/top-highlights-of-the-month-november-2018
combo	Ring of Namira	The Night Mother	life gain becomes damage	https://bethesda.net/en-US/news/top-highlights-of-the-month-november-2018
combo	Devour	Territorial Viper	Lethal and Charge	https://bethesda.net/en-US/news/top-highlights-of-the-month-november-2018
combo	Wildfire Dragon	Brotherhood Sanctuary	repeats the boost	https://bethesda.net/en-US/news/top-highlights-of-the-month-november-2018
combo	Dremora Markynaz	Dagoth Ur	grows Dagoth Ur	https://bethesda.net/en-US/news/top-highlights-of-the-month-november-2018
```
