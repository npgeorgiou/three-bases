# Star Wars: Unlimited

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*Claude's summary (Oct 2026), from general knowledge of the game and the rules and terms under Mechanics; not from the sources below.*
- Genre: physical trading card game (Fantasy Flight Games, Star Wars: Unlimited, 2024).
- Setup: a Leader (it can deploy as a unit) and a Base with health; decks of at least 50 cards.
- Resources: each round a card from hand can be put face down as a resource; resources pay for cards.
- Aspects: cards cost 2 more for each aspect the Leader and Base do not provide.
- Round: players alternate one action at a time; a player can take the initiative (go first next round) instead of acting.
- Arenas: ground and space units fight only units in their own arena or attack the base.
- Win: destroy the enemy base.
- Keywords: Ambush, Bounty, Grit, Overwhelm, Raid, Restore, Saboteur, Sentinel, Shielded, Smuggle, Coordinate, Piloting.

## Sources and notes

Sources:
[1] https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie (designers' colour pie: each aspect's primary
    mechanics, weaknesses, and secondary mechanics it shares a little with the aspect that owns them)
[2] https://cardgamer.com/games/star-wars/aspects-in-star-wars-unlimited/
[3] https://starwarsunlimited.com/articles/heroism-and-villainy
[4] https://tcg-hq.beehiiv.com/p/cad-bane-tarkin-town-master-class (versions picked by their card text)

Heroism and Villainy: "different flavours of colourless" [1], no mechanics described [1][3]; no faction cases. Neutral is
not a faction. Upgrades (attachments) and Capture have no exact concept..

## Factions

### Vigilance
*Claude:* Blue: defence, healing, control and removal.
Known for: survivability and defence, healing units and bases (Restore), Sentinel, removing threats, a few powerful units
grown by upgrades [1]; guard-type units with strong HP [2].
A little: once-per-round card draw (Aggression's), exhausting units and Shield tokens (Cunning's); Grit, which no aspect has as primary [1].
Weak at: early pressure; reactive and slow [1]. Plays: control, the long game [1].

### Command
*Claude:* Green: big units, extra resources and tokens.
Known for: units and resources: the only proactive resource acceleration, the most units, Experience tokens and unit tokens,
the largest units [1]; supports other units through upgrades and events [2].
A little: Raid (Aggression's and Cunning's), Capture [1].
Weak at: direct disruption [1]. Plays: fair unit combat, growth and ramping [1].

### Aggression
*Claude:* Red: damage, Raid and pressure on the base.
Known for: direct damage to units and bases, Overwhelm, Saboteur, Hidden, card draw, readying units, upgrade destruction,
high-power units [1]; damage [2].
A little: Grit, discarding from hand [1].
Weak at: defence: no Sentinel, no healing [1]. Plays: high-risk pressure [1].

### Cunning
*Claude:* Yellow: tricks, exhausting, bouncing and disruption.
Known for: tempo; the most and strongest When Played abilities and the most events; surprise attacks, exhausting resources
and units, hand disruption, temporary board advantage; Hidden, Shield tokens [1]; controlling opposing units [2].
A little: Capture, Shield tokens, exhausting units [1].
Weak at: card draw, long games [1]. Plays: fast tempo, tricks [1].

## Combos
- Tarkintown + Cad Bane - He Who Needs No Introduction: Cad pings, Tarkintown finishes damaged units [4]
- Crafty Smugglers + Ma Klounkee: Ma Klounkee returns them to hand and deals damage [4]
- Now There Are Two of Them + Zuckuss - Bounty Hunter for Hire / Bossk - Deadly Stalker: cheaper deployment [4]
- Jabba the Hutt - Cunning Daimyo + Shoot First / Ma Klounkee: his cost reduction makes them free [4]
- Ma Klounkee + Bossk - Deadly Stalker: Bossk deals 2 when an event is played [4]

## Mechanics
The mechanics the guides name, one per line as `name|concept|regex`, and the rules and terms as `# term:` lines. Read by `coverage.py --mechanics` and `key/key.py`.

```mechanics
# Mechanics the guides name (source in brackets): name|expected concept|wording on the cards. Checked with coverage.py --mechanics.
# https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie , /command , /vigilance , /cunning , /aggression
# Rules and terms for the game block (key.py read), only facts the source states: https://rulespal.com/star-wars-unlimited/rulebook
# term: Zones: each player has a base and a leader in the base zone, a resource zone (face-down resources), deck, hand and discard pile; the ground arena and the space arena are shared, and a unit attacks an enemy unit in its own arena or the opposing base.
# term: Rounds: an action phase in which players alternate one action (play a card, attack with a unit, use an action ability, take the initiative, pass) until both pass in a row; then the regroup phase: each player draws 2, may put one card from hand into resources, and readies all exhausted cards.
# term: Ready and exhaust: non-leader units and resources enter play exhausted; paying costs exhausts resources; a ready unit exhausts to attack.
# term: Attacks: attacker and defender deal damage equal to their power to each other at the same time. A unit with damage equal to or over its HP is defeated (a leader unit returns exhausted to the base zone). A player whose base reaches 0 HP loses.
# term: Upgrades attach to friendly or enemy units and change power and HP; they are defeated when their unit leaves play. Experience tokens are upgrades giving +1 power and +1 HP.
# term: Initiative: its holder acts first each round; taking it is an action, after which that player passes for the rest of the phase.
sentinel|taunt|\bsentinel\b
restore|heal|\brestore \d
heal|heal|\bheal \d
defeat enemy|destroy|\bdefeat (a|an|each|all|that|up to \d+) (enemy |non-leader )*(unit|units|upgrade)
experience tokens|stat_gain|\bexperience token
shield tokens|shield|\bshield token|\bshielded\b
exhaust units|disable|\bexhaust (a|an|each|all|that|up to \d+|the|another|it|enemy)\b
when defeated|death_trigger|\bwhen defeated\b
resource acceleration|resource_gain|\bas a resource\b|\binto (your )?resources\b
many units|condition_count|\bif you control (\d|three|four|five) or more units\b|\bfor each (friendly )?unit\b
capture|removal|\bcaptures?\b
raid|stat_gain|\braid \d
ambush|attack_now|\bambush\b
overwhelm|excess_damage|\boverwhelm\b
saboteur|taunt|\bsaboteur\b
hidden|immunity|\bhidden\b
ready units|untap|\bready (a|an|another|this|that|it|each|up to)\b
return to hand|bounce_enemy|\breturn (a|an|that|each|up to)[^.]{0,40}to (its|their) owner.s hand
when played|on_play|\bwhen played\b
draw cards|draw|\bdraw (a|\d) cards?\b
damage to base|direct_damage|\bdamage to (a|the|each|an enemy|your opponent.s) base\b
discard from hand|discard|\bdiscards? (a|\d|that|those|up to)[^.]{0,30}\bfrom (your|their) hand
initiative|turn_structure|\binitiative\b
grit|stat_gain|\bgrit\b
tokens|summon|\bcreate (a|\d|two|three)\b
```

## Cases
The real-world cases, one per line, tab-separated: `type  a  b  why  source` (see `realworld/RESEARCH.md`). Read by `realworld.py`, `realworld_report.py`, `realworld_why.py` and `learn_recipes.py`.

```tsv
signature	Vigilance	heal	Restore, healing units and bases	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
signature	Vigilance	taunt	Sentinel	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
signature	Vigilance	removal	removing threats	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
signature	Vigilance	tank	guard-type units with strong HP	https://cardgamer.com/games/star-wars/aspects-in-star-wars-unlimited/
signature	Command	resource_gain	proactive resource acceleration	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
signature	Command	board_presence	the most units	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
signature	Command	summon	unit tokens	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
signature	Command	stat_gain	Experience tokens	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
signature	Command	high_cost	the largest, most expensive units	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
signature	Aggression	direct_damage	direct damage to bases	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
signature	Aggression	damage	direct damage to units	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
signature	Aggression	excess_damage	Overwhelm	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
signature	Aggression	evasion	Saboteur gets past Sentinel	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
signature	Aggression	draw	card draw	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
signature	Aggression	untap	readying units	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
signature	Cunning	on_play	the most When Played abilities	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
signature	Cunning	stealth	Hidden	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
signature	Cunning	disable	exhausting units	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
signature	Cunning	hand_disruption	hand disruption	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
signature	Cunning	temporary_effect	temporary board advantage	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
archetype	Vigilance	control	a control aspect, long game	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
archetype	Vigilance	fortress	survivability and defence	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
archetype	Command	ramp	growth and ramping	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
archetype	Aggression	aggro_tempo	assertive pressure	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
archetype	Aggression	burn	direct damage to bases	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
archetype	Cunning	aggro_tempo	tempo	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
archetype	Cunning	trickery	tricks, surprise attacks	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
archetype	Cunning	disruption	hand disruption, exhausting resources	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
splash	Vigilance	draw	once-per-round card draw	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
splash	Vigilance	disable	exhausting units	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
splash	Vigilance	shield	Shield tokens	https://starwarsunlimited.com/articles/behind-unlimited-on-the-color-pie
combo	Tarkintown	Cad Bane - He Who Needs No Introduction	ping, then finish damaged units	https://tcg-hq.beehiiv.com/p/cad-bane-tarkin-town-master-class
combo	Crafty Smugglers	Ma Klounkee	return to hand and deal damage	https://tcg-hq.beehiiv.com/p/cad-bane-tarkin-town-master-class
combo	Now There Are Two of Them	Zuckuss - Bounty Hunter for Hire	cheaper deployment	https://tcg-hq.beehiiv.com/p/cad-bane-tarkin-town-master-class
combo	Now There Are Two of Them	Bossk - Deadly Stalker	cheaper deployment	https://tcg-hq.beehiiv.com/p/cad-bane-tarkin-town-master-class
combo	Jabba the Hutt - Cunning Daimyo	Shoot First	cost reduction makes it free	https://tcg-hq.beehiiv.com/p/cad-bane-tarkin-town-master-class
combo	Jabba the Hutt - Cunning Daimyo	Ma Klounkee	cost reduction makes it free	https://tcg-hq.beehiiv.com/p/cad-bane-tarkin-town-master-class
combo	Ma Klounkee	Bossk - Deadly Stalker	Bossk deals 2 on an event	https://tcg-hq.beehiiv.com/p/cad-bane-tarkin-town-master-class
```
