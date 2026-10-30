# Shadowverse (original game)

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*Claude's summary (Oct 2026), from general knowledge of the game and the rules and terms under Mechanics; not from the sources below.*
- Genre: digital collectible card game (Cygames, 2016); leaders with 20 health, 40-card decks, 8 classes.
- Play points: grow by 1 per turn up to 10 and refill each turn.
- Evolve: each player has evolution points (the second player has more and can start earlier); evolving gives +2/+2 and can attack followers at once.
- Board: up to 5 cards (followers and amulets).
- Keywords: Fanfare (on play), Last Words, Ward, Storm, Rush, Bane, Drain, Clash, Spellboost, Necromancy, Overflow, Vengeance, Resonance, Countdown.
- Win: reduce the enemy leader to 0.

## Sources and notes

Sources:
[1] https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/ (March 2020, original game)
[2] https://shadowverse.fandom.com/wiki/Forestcraft
[3] https://shadowverse.fandom.com/wiki/Swordcraft
[4] https://shadowverse.fandom.com/wiki/Runecraft
[5] https://shadowverse.fandom.com/wiki/Dragoncraft
[6] https://shadowverse.fandom.com/wiki/Shadowcraft
[7] https://shadowverse.fandom.com/wiki/Bloodcraft
[8] https://shadowverse.fandom.com/wiki/Havencraft
[9] https://shadowverse.fandom.com/wiki/Portalcraft

Worlds Beyond and Champions Battle pages are not used. Neutral is not a faction. Overflow (7+ play points), Avarice and
Wrath are counts and thresholds (condition_count). No source with named combos was found.

## Factions

### Forestcraft
*Claude:* Elves: fairies and playing many cards in one turn.
Known for: many cheap cards per turn, many small followers (Fairies), returning its own cards to hand [1]; filling the hand
with Fairies, playing several cards a turn to power other cards [2].

### Swordcraft
*Claude:* Royals: officers and commanders.
Known for: efficient followers, Commanders that boost Officers [1]; aggressive tempo, board dominance, Officer/Commander trait
synergy, Rally, evolving many followers [3].

### Runecraft
*Claude:* Witches: Spellboost and Earth Rite sigils.
Known for: Spellboost (spells boost cards in hand), Earth Rite [1]; spells, damage through effects, Spellboost giving stats,
damage, cost reduction [4].
Archetypes: Spellboost [1]; Earth Rite [4].

### Dragoncraft
*Claude:* Dragons: ramp and Overflow at 7 play points.
Known for: large dragons, cards that grant play points, Overflow [1]; build play points early, then big dragons [5].

### Shadowcraft
*Claude:* Necromancers: shadows in the graveyard, Necromancy and Last Words.
Known for: shadows from played cards and destroyed followers, spent by Necromancy; Reanimate, Burial Rite [1]; its own
destroyed followers, Last Words, Burial Rite (put into play and destroy at once), Reanimate [6].
Archetypes: aggressive, midrange, control [6].

### Bloodcraft
*Claude:* Vampires: self-damage and Vengeance at 10 health or less.
Known for: Vengeance at 10 life or less, cards that cost life [1]; risk and reward, damaging itself for benefits, Vengeance,
Wrath, Avarice [7].
Archetypes: aggressive and control [7].

### Havencraft
*Claude:* Bishops: amulets with Countdown, Ward and healing.
Known for: the most amulets, Countdown that summons followers when it ends [1][8].

### Portalcraft
*Claude:* Artifacts and Resonance (an even number of cards in the deck).
Known for: Resonance (even number of cards in deck), changing deck size, Artifacts and Puppets [1]; Machina synergy [9].
Archetypes: midrange, control, combo [9].

## Mechanics
The mechanics the guides name, one per line as `name|concept|regex`, and the rules and terms as `# term:` lines. Read by `coverage.py --mechanics` and `key/key.py`.

```mechanics
# Mechanics the guides name: name|expected concept|wording on the cards. Checked with coverage.py --mechanics (not yet run).
# Sources (21 Oct 2026): upcomer.com Shadowverse starter guide (March 2020), shadowverse.fandom.com/wiki/<Class> pages.
fanfare|on_play|\bfanfare\b
last words|death_trigger|\blast words\b
spellboost|in_hand_buff|\bspellboost\b
earth rite|cost_type|\bearth rite\b
overflow|condition_count|\boverflow\b
necromancy|coin_economy|\bnecromancy\b
burial rite|sacrifice|\bburial rite\b
reanimate|revive|\breanimate\b
vengeance|low_life|\bvengeance\b
wrath|condition_count|\bwrath\b
avarice|condition_count|\bavarice\b
countdown|delayed|\bcountdown\b
resonance|deck_condition|\bresonance\b
rally|condition_count|\brally\b
storm|haste|\bstorm\b
rush|haste|\brush\b
ward|taunt|\bward\b
bane|deathtouch|\bbane\b
drain|lifesteal|\bdrain\b
evolve|upgrade|\bevolve\b
banish|banish|\bbanish\b
return to hand|return_to_hand|\breturn [a-z ]{0,30} to your hand\b
fairies and puppets|generate_cards|\bput (a|an|\d+|two) (fair(y|ies)|puppets?) into your hand\b
traits (Officer, Commander, Machina, Artifact)|tribal|\b(officer|commander|machina|artifact)s?\b
# term: Vengeance: active while the player's life is 10 or less (upcomer).
# term: Overflow: active with 7 or more play point orbs (upcomer).
# term: Resonance: active while the deck holds an even number of cards (upcomer; fandom Portalcraft).
# term: Necromancy: effects that spend Shadows; Shadows come from played cards and destroyed followers (upcomer; fandom Shadowcraft).
# term: Burial Rite: put a follower from hand onto the field and destroy it at once (fandom Shadowcraft).
# term: Wrath: active after the player has damaged themselves 7 or more times; Avarice: drawing several cards in a turn (fandom Bloodcraft).
# term: Countdown: an amulet's counter drops each turn; at zero its effect fires, often summoning followers (upcomer; fandom Havencraft).
# term: Spellboost: playing a spell boosts the Spellboost cards in hand: stats, damage, cost reduction (fandom Runecraft).
```

## Cases
The real-world cases, one per line, tab-separated: `type  a  b  why  source` (see `realworld/RESEARCH.md`). Read by `realworld.py`, `realworld_report.py`, `realworld_why.py` and `learn_recipes.py`.

```tsv
signature	Forestcraft	combo_sequence	several cards a turn power other cards	https://shadowverse.fandom.com/wiki/Forestcraft
signature	Forestcraft	return_to_hand	returning its own cards to hand	https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/
signature	Forestcraft	generate_cards	filling the hand with Fairies	https://shadowverse.fandom.com/wiki/Forestcraft
signature	Forestcraft	board_presence	many small followers	https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/
signature	Swordcraft	tribal	Officer and Commander traits	https://shadowverse.fandom.com/wiki/Swordcraft
signature	Swordcraft	buff	Commanders boost Officers	https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/
signature	Runecraft	in_hand_buff	Spellboost	https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/
signature	Runecraft	on_spell	spells boost cards	https://shadowverse.fandom.com/wiki/Runecraft
signature	Runecraft	cost_reduction	Spellboost cost reduction	https://shadowverse.fandom.com/wiki/Runecraft
signature	Runecraft	damage	damage through effects	https://shadowverse.fandom.com/wiki/Runecraft
signature	Dragoncraft	resource_gain	cards that grant play points	https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/
signature	Dragoncraft	high_cost	large dragons	https://shadowverse.fandom.com/wiki/Dragoncraft
signature	Shadowcraft	death_trigger	Last Words	https://shadowverse.fandom.com/wiki/Shadowcraft
signature	Shadowcraft	revive	Reanimate	https://shadowverse.fandom.com/wiki/Shadowcraft
signature	Shadowcraft	sacrifice	Burial Rite destroys its own follower	https://shadowverse.fandom.com/wiki/Shadowcraft
signature	Shadowcraft	coin_economy	shadows spent by Necromancy	https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/
signature	Bloodcraft	life_payment	damaging itself for benefits	https://shadowverse.fandom.com/wiki/Bloodcraft
signature	Bloodcraft	low_life	Vengeance at 10 life or less	https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/
signature	Havencraft	delayed	Countdown amulets	https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/
signature	Portalcraft	deck_condition	Resonance	https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/
signature	Portalcraft	generate_cards	Puppets	https://upcomer.com/shadowverse-starter-guide-card-basics-classes-how-to-build-a-deck/
signature	Portalcraft	tribal	Machina and Artifacts	https://shadowverse.fandom.com/wiki/Portalcraft
archetype	Forestcraft	swarm	bands of Fairies	https://shadowverse.fandom.com/wiki/Forestcraft
archetype	Forestcraft	spellslinger	chains of cheap cards	https://shadowverse.fandom.com/wiki/Forestcraft
archetype	Swordcraft	aggro_tempo	aggressive tempo	https://shadowverse.fandom.com/wiki/Swordcraft
archetype	Swordcraft	tribal	trait synergy	https://shadowverse.fandom.com/wiki/Swordcraft
archetype	Runecraft	spellslinger	spell-focused	https://shadowverse.fandom.com/wiki/Runecraft
archetype	Dragoncraft	ramp	play points, then big dragons	https://shadowverse.fandom.com/wiki/Dragoncraft
archetype	Shadowcraft	graveyard	its own destroyed followers	https://shadowverse.fandom.com/wiki/Shadowcraft
archetype	Shadowcraft	aggro_tempo	aggressive decks	https://shadowverse.fandom.com/wiki/Shadowcraft
archetype	Shadowcraft	control	control decks	https://shadowverse.fandom.com/wiki/Shadowcraft
archetype	Bloodcraft	aggro_tempo	aggressive decks	https://shadowverse.fandom.com/wiki/Bloodcraft
archetype	Bloodcraft	control	control decks	https://shadowverse.fandom.com/wiki/Bloodcraft
archetype	Portalcraft	control	control decks	https://shadowverse.fandom.com/wiki/Portalcraft
archetype	Portalcraft	spellslinger	combo decks	https://shadowverse.fandom.com/wiki/Portalcraft
```
