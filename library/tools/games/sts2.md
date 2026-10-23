# Slay the Spire 2 (Early Access)

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*Claude's summary (Oct 2026), from general knowledge of the game and the rules and terms under Mechanics; not from the sources below.*
- Genre: single-player and co-op roguelike deckbuilder (MegaCrit, Early Access 2026), the sequel to Slay the Spire.
- Turn: energy and draws per turn, Block, enemy intents and a branching map, as in the first game.
- New: two new characters with their own resources (Osty for the Necrobinder, Stars for the Regent), and multiplayer runs.
- Keywords: as in the first game, plus new ones such as Sly, Doom and Forge (see Mechanics).

## Sources and notes

Sources:
[1] https://slaythespire2.gg/characters
[2] https://brokenbuilds.gg/slay-the-spire-2/guides/slay-the-spire-2-best-builds
[3] https://keengamer.com/articles/guides/slay-the-spire-2-best-character-tier-list

Not used: gamecat.it.com's build list, which gives the Regent the first game's Watcher stances; keengamer's Regent line about shivs, poison and Sly (Silent's). Event, Shared, Colorless, Curse, Token, Status are not
characters. Sly (a discarded card plays itself) is on_discard. Stars, the Regent's second resource spent on cards, is
coin_economy.

## Factions

### Ironclad
*Claude:* Warrior: Strength, Exhaust and self-damage.
Known for: Strength scaling, self-damage (HP for power), Exhaust payoffs, Vulnerable [1]; Strength stacking with Demon Form,
Exhaust [2]; healing from Burning Blood (relic) [3].

### Silent
*Claude:* Huntress: Shivs, Poison and discard (Sly).
Known for: Poison, small attacks, Sly, Shivs, discard combos [1][3].
Builds: discard combos, Poison, Shivs [1].

### Defect
*Claude:* Automaton: Orbs and Focus.
Known for: Orbs (Lightning, Frost, Dark, Plasma, Glass) for damage, Block and Energy, Evoke turns [1]; Focus on Frost [2][3].
Builds: Orb scaling engines [1]; Frost Tank with Focus [2].

### Necrobinder
*Claude:* Necromancer: the companion Osty grows through Summon; Doom kills.
Known for: Osty, a companion that attacks and tanks and scales by Summon; Doom (execute at a threshold); Souls (burst card
draw); card transform [1][3].
Builds: fighting through Osty, Doom or Soul cycling [1].

### Regent
*Claude:* Royal: Stars as a second resource; Forge strengthens the Sovereign Blade.
Known for: Stars (uncapped second resource), Forge (scales the Sovereign Blade), Minions from card transformation [1][3].
Builds: Forge Sovereign Blade, Minions; patient long-term scaling [1].

## Combos
- Star Battery + Sovereign Blade: the climbing damage line [2]
- Parry + Sword Sage: the early Block loop [2]

## Mechanics
The mechanics the guides name, one per line as `name|concept|regex`, and the rules and terms as `# term:` lines. Read by `coverage.py --mechanics` and `key/key.py`.

```mechanics
# Mechanics the guides name: name|expected concept|wording on the cards. Checked with coverage.py --mechanics (not yet run).
# Sources (21 Oct 2026): slaythespire2.gg/characters, brokenbuilds.gg STS2 best builds, keengamer.com STS2 character tier list.
strength|permanent_growth|\bstrength\b
self-damage|life_payment|\blose \d+ hp\b
exhaust|exhaust|\bexhaust\b
vulnerable|debuff|\bvulnerable\b
poison|damage_over_time|\bpoison\b
sly (plays when discarded)|on_discard|\bsly\b
shiv|generate_cards|\bshivs?\b
discard|discard|\bdiscard\b
orbs (channel, evoke)|slots_queue|\b(channel|evoke)\b
focus|spell_power|\bfocus\b
osty and summon|summon|\b(osty|summon)\b
doom (execute at a threshold)|destroy|\bdoom\b
souls (burst card draw)|draw|\bsouls?\b
transform cards|transform|\btransform\b
stars (second resource)|coin_economy|\bstars?\b
forge (scales the Sovereign Blade)|permanent_growth|\bforge\b
block|block_armor|\bblock\b
# term: Sly: a card with Sly plays itself for free when discarded (slaythespire2.gg).
# term: Doom: enemies whose Doom reaches their health are killed (keengamer: when Doom equals their health).
# term: Osty: the Necrobinder's companion; it attacks, absorbs hits and grows through Summon (slaythespire2.gg; keengamer).
# term: Stars: the Regent's uncapped second resource, granted at combat start by Divine Right (slaythespire2.gg; keengamer).
# term: Forge: strengthens the Sovereign Blade (slaythespire2.gg).
# term: Burning Blood: Ironclad's starter relic heals 6 HP after combat (keengamer).
```

## Cases
The real-world cases, one per line, tab-separated: `type  a  b  why  source` (see `realworld/RESEARCH.md`). Read by `realworld.py`, `realworld_report.py`, `realworld_why.py` and `learn_recipes.py`.

```tsv
signature	Ironclad	permanent_growth	Strength scaling	https://slaythespire2.gg/characters
signature	Ironclad	life_payment	self-damage for power	https://slaythespire2.gg/characters
signature	Ironclad	exhaust	Exhaust payoffs	https://slaythespire2.gg/characters
signature	Silent	damage_over_time	Poison	https://slaythespire2.gg/characters
signature	Silent	generate_cards	Shivs	https://slaythespire2.gg/characters
signature	Silent	discard	discard combos	https://slaythespire2.gg/characters
signature	Silent	on_discard	Sly	https://slaythespire2.gg/characters
signature	Defect	slots_queue	Orbs	https://slaythespire2.gg/characters
signature	Defect	spell_power	Focus	https://keengamer.com/articles/guides/slay-the-spire-2-best-character-tier-list
signature	Necrobinder	summon	Osty scales by Summon	https://slaythespire2.gg/characters
signature	Necrobinder	destroy	Doom executes at a threshold	https://slaythespire2.gg/characters
signature	Necrobinder	draw	Souls, burst card draw	https://slaythespire2.gg/characters
signature	Necrobinder	transform	card transform	https://slaythespire2.gg/characters
signature	Regent	coin_economy	Stars, a second resource	https://slaythespire2.gg/characters
signature	Regent	permanent_growth	Forge scales the Sovereign Blade	https://slaythespire2.gg/characters
signature	Regent	summon	Minions	https://slaythespire2.gg/characters
archetype	Ironclad	scaling	Strength stacking	https://brokenbuilds.gg/slay-the-spire-2/guides/slay-the-spire-2-best-builds
archetype	Silent	poison_attrition	Poison attrition	https://slaythespire2.gg/characters
archetype	Silent	card_advantage	discard cycling	https://keengamer.com/articles/guides/slay-the-spire-2-best-character-tier-list
archetype	Defect	scaling	Orb scaling engines	https://slaythespire2.gg/characters
archetype	Defect	fortress	Frost Tank	https://brokenbuilds.gg/slay-the-spire-2/guides/slay-the-spire-2-best-builds
archetype	Regent	scaling	long-term scaling	https://slaythespire2.gg/characters
combo	Star Battery	Sovereign Blade	climbing damage	https://brokenbuilds.gg/slay-the-spire-2/guides/slay-the-spire-2-best-builds
combo	Parry	Sword Sage	early Block loop	https://brokenbuilds.gg/slay-the-spire-2/guides/slay-the-spire-2-best-builds
```
