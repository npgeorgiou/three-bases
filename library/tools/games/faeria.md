# Faeria

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*Claude's summary (Oct 2026), from general knowledge of the game and the rules and terms under Mechanics; not from the sources below.*
- Genre: digital card game with a hex board (Abrakam, 2016); each player has a God (an orb) with 20 health. Reducing the enemy God to 0 wins.
- Board: the board starts as ocean; players build land tiles: Prairie (neutral), Lake (blue), Forest (green), Mountain (red), Desert (yellow).
- Turn power: each turn a player chooses one: build lands, draw a card, or gain extra faeria.
- Resource: faeria, gained each turn and harvested from the four faeria wells by units next to them.
- Costs: cards cost faeria and need a number of lands of their colour; units are summoned on or next to the player's lands.
- Units: move 1 tile and attack once per turn; keywords include Haste, Dash, Jump, Flying, Aquatic, Ranged, Taunt, Protection, Charge, Gift, Last Words.
- Specific: the board shape is built during the game, so land placement is a resource and a weapon.

## Sources and notes

Sources:
[1] https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292 (forum thread; posters
    named where they differ)
[2] https://www.faeria.com/the-hub/guide/42-deck-archetypes (official deck archetype guide)
[3] https://boards.faeria.com/t/board-and-colour-a-state-of-the-game-analysis/2586 (forum: each colour's land mechanic)

No source covers Human/Neutral or Pandora; no faction cases for them. Land alteration (lakes, forests, land destruction,
land conversion) is terrain.

## Factions

### Blue
*Claude:* Lakes: aquatic units, spells, card draw and control.
Known for: mobility, outmanoeuvring and shrinking big creatures [1]; small creatures, jump, land-moving, many spells,
transforming creatures, ramp [1, Galileus]; turning lands into lakes [3].

### Green
*Claude:* Forests: growing units, Protection and large bodies.
Known for: big creatures and Taunt [1]; many buffs, growth, land ramp [1, Galileus]; forests [3].
A little: "a dash of ramp, but not too much" [1, Galileus].
Weak at: mobility [1].

### Red
*Claude:* Mountains: aggression, direct damage and fast units.
Known for: damaging events and burn [1]; Taunt ("the biggest"), ranged creatures, direct damage spells, buildings
[1, Galileus]; land destruction, Rush decks [3].

### Yellow
*Claude:* Deserts: mobility (Dash, Jump) and tempo.
Known for: rush, haste, flight, sacrificing health or creatures, cards buffed by events [1, Galileus]; area damage, minions
that deal one damage when placed [1, Decabytes]; land conversion, Rush decks [3].
A little: cards that give mana [1, Galileus].

## Archetypes [2]
- Rush (aggro): Yellow Rush, attacks the orb.
- Control: Yellow example, removal and movement tricks.
- Combo: Blue Yellow Events, cards buffed by playing events.
- Burn: Red Yellow Burn.
- Sacrifice: almost always Green and Yellow, Soul Eater with Last Words and sacrifice.

## Combos [2]
- Lord of Terror Burn: play Lord of Terror, then damage it to deal damage to the opponent (one card, no pair).
- Khalim's Prayer + Zealous Crusader: orb attacks give faeria and buff the Crusader.

## Mechanics
The mechanics the guides name, one per line as `name|concept|regex`, and the rules and terms as `# term:` lines. Read by `coverage.py --mechanics` and `key/key.py`.

```mechanics
# Mechanics of Faeria: name|expected concept|wording on the cards. Checked with coverage.py --mechanics.
# Research (20 Oct 2026): faeria.com/the-hub/guide/443-keywords-and-their-expanded-descriptions (every keyword and rule),
# faeria.com/the-hub/guide/59-faeria-academy-chapter-1-cards-and-keywords (lands, colours, faeria), faeria.com/the-hub/guide/42-deck-archetypes,
# boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292 (colour identities), a 40-card sample.
summon trigger (Gift)|on_play|\bgift\b
death trigger (Last Words)|death_trigger|\blast words\b
start of turn (Production)|turn_start|\bproduction\b
combat trigger|on_attack|\bcombat\b
moves onto enemy land (Corrupt)|territory_trigger|\bcorrupt\b
structure ability (Activate)|activated|\bactivate\b
flying (moves over ocean)|movement|\bflying\b
charge (straight-line move past taunts)|movement|\bcharge \d
jump over obstacles|movement|\bjump\b
dash (moves when summoned)|movement|\bdash \d
taunt|taunt|\btaunt\b
haste|haste|\bhaste\b
protection (prevents the next damage)|shield|\bprotection\b
discover|selection|\bdiscover\b
ranged attack|ranged|\branged attack\b
divine (cannot be targeted)|immunity|\bdivine\b
deathtouch|deathtouch|\bdeathtouch\b
aquatic|movement|\baquatic\b
swallow a creature|banish|\bswallows?\b
drain (damage and heal you)|lifesteal|\bdrain\b
teleport|movement|\bteleport
transform a creature|polymorph|\btransform (a|an|another|an enemy|all) [a-z ]{0,10}creatures?\b
fight (attack anywhere, not its attack)|attack_now|\bfights?\b
draw cards|draw|\bdraw (\d+|a|an|two|three) [a-z ]{0,20}cards?\b
gain faeria|resource_gain|\bgain \d+ faeria\b
cost reduction|cost_reduction|\bcosts? \d+ faeria less\b|\bcosts? less\b
random split damage|random_effect|\brandomly split\b|\brandom (adjacent|friendly|enemy)\b
damage a creature or god|damage|\bdeal \d+ damage\b
destroy|destroy|\bdestroy (a|an|all|target)\b
stat gain|stat_gain|\bgains? \+\d+/\+\d+\b|\bgive [a-z ]{0,20}\+\d+/\+\d+\b
stat loss|stat_loss|\b-\d+/-\d+\b
summon units|summon|\bsummon (a|an|two|three|\d+) \b
sacrifice your creature|sacrifice|\bsacrifice a creature\b
heal|heal|\bheal\b
add cards to hand|generate_cards|\badd [a-z0-9 ]{0,25}(card|copy|copies)[a-z ]{0,10} (to|into) your hand\b
land creation|terrain|\b(wild land|forest|lake|mountain|desert)s?\b
# Not checked: harvesting (a creature on a well collects faeria; "whenever this harvests" has no trigger concept).
```

## Cases
The real-world cases, one per line, tab-separated: `type  a  b  why  source` (see `realworld/RESEARCH.md`). Read by `realworld.py`, `realworld_report.py`, `realworld_why.py` and `learn_recipes.py`.

```tsv
signature	Blue	movement	mobility, jump	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Blue	transform	transforming creatures	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Blue	stat_loss	shrinking big creatures	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Blue	terrain	turning lands into lakes, moving lands	https://boards.faeria.com/t/board-and-colour-a-state-of-the-game-analysis/2586
signature	Green	taunt	Taunt	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Green	high_cost	big creatures	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Green	buff	many buffs	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Green	terrain	forests	https://boards.faeria.com/t/board-and-colour-a-state-of-the-game-analysis/2586
signature	Red	damage	damaging events	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Red	direct_damage	burn	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Red	taunt	the biggest Taunts	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Red	ranged	ranged creatures	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Red	terrain	land destruction	https://boards.faeria.com/t/board-and-colour-a-state-of-the-game-analysis/2586
signature	Yellow	haste	rush and haste	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Yellow	evasion	flight	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Yellow	sacrifice	sacrificing creatures	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Yellow	life_payment	sacrificing health	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Yellow	on_spell	cards buffed by events	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Yellow	aoe_damage	area damage	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Yellow	terrain	land conversion	https://boards.faeria.com/t/board-and-colour-a-state-of-the-game-analysis/2586
archetype	Yellow	aggro_tempo	Yellow Rush	https://www.faeria.com/the-hub/guide/42-deck-archetypes
archetype	Yellow	control	Yellow control	https://www.faeria.com/the-hub/guide/42-deck-archetypes
archetype	Yellow	spellslinger	Blue Yellow Events	https://www.faeria.com/the-hub/guide/42-deck-archetypes
archetype	Yellow	burn	Red Yellow Burn	https://www.faeria.com/the-hub/guide/42-deck-archetypes
archetype	Yellow	sacrifice	Green and Yellow sacrifice	https://www.faeria.com/the-hub/guide/42-deck-archetypes
archetype	Blue	spellslinger	Blue Yellow Events	https://www.faeria.com/the-hub/guide/42-deck-archetypes
archetype	Red	burn	Red Yellow Burn	https://www.faeria.com/the-hub/guide/42-deck-archetypes
archetype	Red	aggro_tempo	Rush decks	https://boards.faeria.com/t/board-and-colour-a-state-of-the-game-analysis/2586
archetype	Green	sacrifice	Green and Yellow sacrifice	https://www.faeria.com/the-hub/guide/42-deck-archetypes
splash	Green	resource_gain	a dash of ramp	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
splash	Yellow	resource_gain	cards that give mana	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
combo	Khalim's Prayer	Zealous Crusader	orb attacks give faeria and buff the Crusader	https://www.faeria.com/the-hub/guide/42-deck-archetypes
```
