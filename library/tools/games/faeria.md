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
- Keyword rules (patterns check, 26 Oct 2026, from faeria.com/the-hub/guide/443-keywords-and-their-expanded-descriptions):
  Flying moves over ocean and land but not through creatures; nothing blocks in Faeria, so Flying is movement. Aquatic creatures are
  summoned only on lakes (Kaptain) and drown if they end their turn on a non-lake land. A swallowed creature is removed until the swallower releases it. Corrupt
  triggers the first time the creature moves onto an enemy land.

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
swallow a creature (any or an enemy; a friendly one is merge_attach)|removal|\bswallow (a creature|and gain control)\b
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
land alteration (create, transform, move, destroy or take lands)|terrain|\b(create|transform|destroy|move|fill|gain control of)\b[^.]{0,40}\b(lands?|forests?|lakes?|mountains?|deserts?|prairies?)\b
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
signature	Green	buff	many buffs	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Green	terrain	forests	https://boards.faeria.com/t/board-and-colour-a-state-of-the-game-analysis/2586
signature	Red	damage	damaging events	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Red	direct_damage	burn	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Red	ranged	ranged creatures	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Yellow	haste	rush and haste	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Yellow	movement	flight (Flying moves over ocean; Faeria has no blocking)	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Yellow	sacrifice	sacrificing creatures	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Yellow	life_payment	sacrificing health	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
signature	Yellow	on_spell	cards buffed by events	https://boards.faeria.com/t/color-identity-color-matchups-fighting-unfavorable-matchups/5292
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
combo	Feed the Forest	Oakling	destroying Oakling triggers its Last Words (+5/+5 to a green creature in hand) and gains faeria	https://www.faeria.com/the-hub/guide/13-how-to-build-a-green-deck
combo	Feed the Forest	Ruunin, the Relentless	each death returns Ruunin bigger; Feed the Forest turns her Life into faeria	https://www.faeria.com/the-hub/deck/1720-illusion-of-failed-ruunin
combo	Feed the Forest	Tarum, the Forest World	destroying Tarum gains 15 faeria and its Last Words fills the world with forests	https://www.faeria.com/the-hub/article/23-aquablad-s-card-review-time-of-legends
combo	Gabrian Enchantment	Oak Father	Oak Father's Life, grown by forests, becomes its Attack	https://www.faeria.com/the-hub/article/23-aquablad-s-card-review-time-of-legends
combo	Doomsday	Soul Eater	Doomsday destroys every creature; each friendly death grows Soul Eater in hand	https://www.faeria.com/the-hub/guide/337-how-to-play-a-393-393-soul-eater
combo	Doomgate, Door to Oblivion	Annoying Gnat	sacrificing the Gnat draws a card; its Last Words summons it again	https://www.faeria.com/the-hub/deck/2486-so-annoying
combo	Ruby Yak	Famine	Famine damages every Yak; Ruby Yak hits the opponent once for each damaged Yak	https://www.faeria.com/the-hub/deck/4206-ruby-yak-otk-combo
combo	Ulani's Medallion	Ruby Yak	the Medallion turns your other creatures into copies of Ruby Yak	https://www.faeria.com/the-hub/guide/344-exodia-yak
combo	Rain of Fish	Ulani's Medallion	Rain of Fish fills the board with creatures for the Medallion to copy into Ruby Yaks	https://www.faeria.com/the-hub/guide/344-exodia-yak
combo	Ruunin, the Relentless	Shaytan Monstrosity	each time Ruunin dies, Monstrosity drains her Attack; she returns bigger	https://www.faeria.com/the-hub/deck/1852-monstrosity-feeds-on-ruunin
combo	Earthcraft	Three Wishes	Earthcraft turns your lands into the colours Three Wishes needs (2 of each)	https://www.faeria.com/the-hub/guide/140-deck-pilot-three-wishes
```

## Notes from the patterns check
Patterns check, 26 Oct 2026 (Claude, decisions by Kaptain). Counts are from the answer key (what the card text shows).
- Flying, Jump and Aquatic are movement, not evasion and not terrain: Faeria has no blocking, and terrain here is land alteration
  (create, transform, move, destroy or take lands). Counting or entering lands is not terrain. Aquatic creatures are summoned
  only on lakes (Kaptain) and drown at the end of the turn on any other land: placement_rules, self_destruct, turn_end.
- Taunt locks the adjacent enemies (immobilize); zone_of_control is not in it. How to tag "every unit in an area" for any effect
  is left to the tagging redesign (library/TAGGING_RECORDS.md).
- Swallow removes a creature until the swallower dies: removal for any or an enemy creature, merge_attach for a friendly one.
- Attacking the enemy god is direct damage: cards rewarded for it carry direct_damage as benefits.
- Discounts on cards in hand are both in_hand_buff and cost_reduction. "Becomes wild land" is cost_type.
- "Give the next X creature you summon +1/+1" is delayed plus on_ally_play plus the stat gains, not in_hand_buff.
- Cases removed, lead under 1.3 times in the cards: Green high_cost (6 of 67 expensive cards against 50 of 376 elsewhere;
  "big creatures" are big in Life, not in cost); Red taunt (1 of 68, rest 6 of 248); Red terrain (1 of 68, rest 10 of 248:
  Meteor only); Yellow aoe_damage (0 of 70); Yellow terrain (0 of 70: no Yellow card converts lands).
- Cases kept but not met: Blue and Yellow movement (movement is on more than a quarter of the cards, too common for a
  signature); Blue transform (2 of 71) and stat_loss (1 of 71), too few cards; Blue terrain (4 of 71, 2.0 times, p 0.22);
  Yellow on_spell (2 of 70; Blue has the other event payoffs). Splash resource_gain (Green, Yellow): no faction owns faeria
  gain. Yellow sacrifice archetype: Yellow leads sacrifice, but the recipe also counts self_destruct, where Blue's drowning and
  self-damaging towers now count.
- Combos from Kaptain's list (another AI's, 26 Oct 2026), kept where the card texts and a guide or deck agree: Feed the Forest
  with Oakling, Ruunin and Tarum; Gabrian Enchantment with Oak Father; Doomsday with Soul Eater; Doomgate with Annoying Gnat;
  Ruby Yak with Famine and Ulani's Medallion; Rain of Fish with Ulani's Medallion; Ruunin with Shaytan Monstrosity ("Shaytan
  Scourge" in the list); Earthcraft with Three Wishes. Left out: Tarum with Doomgate (no source, Kaptain); names no card has
  (Ouroboros, Swallowed Whole, Unbound Evolution, Shaytan Vampire, Khalim Sky Guardian, Seifer Eldritch King, Ignus the Mad,
  Iona Beloved Emissary); effects the cards do not have (Wavecrash Colossus is cheaper per enemy-well harvest; Blood Obelisk
  counts combat deaths; Ruby Fish are not Yaks; Prophet of Tides has no Jump; Voice of Truth and Mirror Phantasm undo the
  other card's gains; Seifer gains Attack and Life alike); pairs with no named partner card. Thyrian Golem (5/10, named in the
  green deck guide) is not in the library.
- Combos the library does not find: Khalim's Prayer + Zealous Crusader (two payoffs of the same thing, attacking the god; no
  link joins two cards that benefit from the same effect); Ulani's Medallion + Ruby Yak, Rain of Fish + Ulani's Medallion,
  Earthcraft + Three Wishes (no link for copying a board into one tribe, or for land colours a cost needs).
