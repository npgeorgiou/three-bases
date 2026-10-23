# Slay the Spire

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*Claude's summary (Oct 2026), from general knowledge of the game and the rules and terms under Mechanics; not from the sources below.*
- Genre: single-player roguelike deckbuilder (MegaCrit, 2017-2019).
- Turn: 3 energy and 5 cards drawn per turn; unused cards are discarded; Block lasts until the next turn.
- Enemies show their intent (attack, buff, debuff) before the player acts.
- Run: 3 acts (and a hidden fourth) along a branching map of fights, elites, events, shops, rests and treasure; relics and potions change the rules.
- Keywords: Exhaust, Ethereal, Innate, Retain, Strength, Dexterity, Vulnerable, Weak, Frail, Poison, Orbs, Focus, Stances, Scry.
- Win: beat the final boss; Ascension levels add difficulty.

## Sources and notes

Sources:
[1] https://www.thegamer.com/slay-the-spire-best-builds/ (builds per character with their key cards)
[2] https://slaythespire.gg/guides/slay-the-spire-best-character (mechanics, strengths, weaknesses, builds)

Colorless and Curse are not characters. Block is block_armor (it wears off each turn unless kept). Relics in the builds
(Artifact, Shuriken, Kunai, Ornamental Fan, Unceasing Top, The Specimen, Wrist Blade) are not cards here.

## Factions

### Ironclad
*Claude:* Warrior: Strength, Exhaust, self-damage and healing after combat.
Known for: Strength scaling and Exhaust [2]; Block with Barricade and Entrench, multi-attack cards to use Strength [1];
passive healing from Burning Blood (relic) [2].
Builds: Bunker (Block), Strength [1]; Strength scaling, Exhaust [2].

### Silent
*Claude:* Huntress: Shivs, Poison and discard.
Known for: Poison, Shivs, discard loops, infinite decks [2]; drawing and discarding, playing many cards (Momentum) [1].
Builds: Shivs, Discard and Draw, Momentum, Poison [1][2].

### Defect
*Claude:* Automaton: Orbs (Lightning, Frost, Dark, Plasma) and Focus.
Known for: Orbs and powers, Focus stacking, burst with orb synergy [2]; Frost for Block, Lightning, zero-cost cards with Claw [1].
Builds: Frost Tank, Lightning Spam, Claw [1]; Focus stacking, Loop + Defragment, All for One with Claw [2].

### Watcher
*Claude:* Monk: stances (Wrath, Calm, Divinity), Scry and Retain.
Known for: stances (Calm, Wrath, Divinity), stance dancing for burst, Mantra [2]; Retain, creating and upgrading cards, Scry [1].
Builds: Retain, Creation, Stance Master, Scry [1]; stance burst, Mantra [2].

## Combos
- Body Slam + Barricade / Entrench: Block becomes damage [1]
- Demon Form / Limit Break + Sword Boomerang / Whirlwind: Strength with multi-attack [1]
- Feel No Pain + Dark Embrace: Exhaust value [2]
- After Image + A Thousand Cuts: both trigger on every card played [1]
- Catalyst + Noxious Fumes / Bouncing Flask: Catalyst doubles the Poison they apply [1]
- Glacier + Capacitor: Frost for Block, more Orb slots [1]
- Recursion + Loop: more use of Orbs [1]
- Loop + Defragment: Focus scaling [2]
- All for One + Claw: zero-cost engine [2]
- Establishment + Windmill Strike / Sands of Time: retained cards get cheaper [1]
- Master Reality + Conjure Blade / Evaluate: created cards come upgraded [1]
- Talk to the Hand + Flurry of Blows: stance switching [1]
- Nirvana + Cut Through Fate / Just Lucky / Third Eye / Weave: Block whenever you Scry [1]

## Mechanics
The mechanics the guides name, one per line as `name|concept|regex`, and the rules and terms as `# term:` lines. Read by `coverage.py --mechanics` and `key/key.py`.

```mechanics
# Mechanics the guides name: name|expected concept|wording on the cards. Checked with coverage.py --mechanics (not yet run).
# Sources (21 Oct 2026): thegamer.com/slay-the-spire-best-builds, slaythespire.gg/guides/slay-the-spire-best-character.
strength|permanent_growth|\bstrength\b
exhaust|exhaust|\bexhaust\b
block|block_armor|\bblock\b
keep block (Barricade)|block_armor|\bblock is not removed\b
multi-hit attacks|multi_attack|\b\d+ times\b
poison|damage_over_time|\bpoison\b
shiv|generate_cards|\bshivs?\b
discard|discard|\bdiscard\b
draw|draw|\bdraw \d+ cards?\b
whenever you play a card|on_ally_play|\bwhenever you play a card\b
channel and evoke orbs|slots_queue|\b(channel|evoke)\b
focus|spell_power|\bfocus\b
frost orb block|block_armor|\bfrost\b
zero-cost cards (Claw)|cost_condition|\bcosts? 0\b
stances (Calm, Wrath, Divinity)|stances|\b(calm|wrath|divinity)\b
mantra|condition_count|\bmantra\b
retain|retain|\bretain\b
scry|selection|\bscry\b
upgrade created cards|upgrade|\bupgrade\b
create cards|generate_cards|\badd [a-z0-9 ]{0,30} (into|to) your hand\b
# term: Block: absorbs attack damage; Barricade and Entrench keep and grow it (thegamer); it is removed at the start of the next turn otherwise (assumed).
# term: Orbs: channelled into slots; Frost gives Block, Lightning deals damage; Focus strengthens orbs (thegamer; slaythespire.gg).
# term: Stances: Calm, Wrath and Divinity; switching between them (stance dancing) is the Watcher's burst (slaythespire.gg).
# term: Retain: the card stays in hand at the end of the turn (assumed); Establishment makes retained cards cheaper (thegamer).
```

## Cases
The real-world cases, one per line, tab-separated: `type  a  b  why  source` (see `realworld/RESEARCH.md`). Read by `realworld.py`, `realworld_report.py`, `realworld_why.py` and `learn_recipes.py`.

```tsv
signature	Ironclad	permanent_growth	Strength scaling	https://slaythespire.gg/guides/slay-the-spire-best-character
signature	Ironclad	exhaust	Exhaust builds	https://slaythespire.gg/guides/slay-the-spire-best-character
signature	Ironclad	block_armor	Block with Barricade and Entrench	https://www.thegamer.com/slay-the-spire-best-builds/
signature	Ironclad	multi_attack	multi-attack cards	https://www.thegamer.com/slay-the-spire-best-builds/
signature	Silent	damage_over_time	Poison	https://slaythespire.gg/guides/slay-the-spire-best-character
signature	Silent	generate_cards	Shivs	https://slaythespire.gg/guides/slay-the-spire-best-character
signature	Silent	discard	discard loops	https://slaythespire.gg/guides/slay-the-spire-best-character
signature	Silent	draw	drawing and discarding	https://www.thegamer.com/slay-the-spire-best-builds/
signature	Silent	on_ally_play	triggers on every card played	https://www.thegamer.com/slay-the-spire-best-builds/
signature	Defect	slots_queue	Orbs	https://slaythespire.gg/guides/slay-the-spire-best-character
signature	Defect	spell_power	Focus stacking	https://slaythespire.gg/guides/slay-the-spire-best-character
signature	Defect	block_armor	Frost for Block	https://www.thegamer.com/slay-the-spire-best-builds/
signature	Defect	cost_condition	zero-cost cards with Claw	https://www.thegamer.com/slay-the-spire-best-builds/
signature	Watcher	stances	Calm, Wrath, Divinity	https://slaythespire.gg/guides/slay-the-spire-best-character
signature	Watcher	retain	Retain	https://www.thegamer.com/slay-the-spire-best-builds/
signature	Watcher	selection	Scry	https://www.thegamer.com/slay-the-spire-best-builds/
signature	Watcher	generate_cards	creating cards	https://www.thegamer.com/slay-the-spire-best-builds/
signature	Watcher	upgrade	upgrading created cards	https://www.thegamer.com/slay-the-spire-best-builds/
archetype	Ironclad	scaling	Strength scaling	https://slaythespire.gg/guides/slay-the-spire-best-character
archetype	Ironclad	fortress	Bunker	https://www.thegamer.com/slay-the-spire-best-builds/
archetype	Silent	poison_attrition	Poison	https://www.thegamer.com/slay-the-spire-best-builds/
archetype	Silent	card_advantage	Discard and Draw	https://www.thegamer.com/slay-the-spire-best-builds/
archetype	Silent	spellslinger	Momentum, playing many cards	https://www.thegamer.com/slay-the-spire-best-builds/
archetype	Defect	fortress	Frost Tank	https://www.thegamer.com/slay-the-spire-best-builds/
archetype	Defect	scaling	Focus stacking, Claw	https://slaythespire.gg/guides/slay-the-spire-best-character
archetype	Watcher	transformation	stance switching	https://www.thegamer.com/slay-the-spire-best-builds/
archetype	Watcher	card_advantage	Scry and Creation	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Body Slam	Barricade	Block becomes damage	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Body Slam	Entrench	Block becomes damage	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Demon Form	Sword Boomerang	Strength with multi-attack	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Limit Break	Whirlwind	Strength with multi-attack	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Feel No Pain	Dark Embrace	Exhaust value	https://slaythespire.gg/guides/slay-the-spire-best-character
combo	After Image	A Thousand Cuts	both trigger on every card	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Catalyst	Noxious Fumes	Catalyst doubles Poison	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Catalyst	Bouncing Flask	Catalyst doubles Poison	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Glacier	Capacitor	Frost and more Orb slots	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Recursion	Loop	more use of Orbs	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Loop	Defragment	Focus scaling	https://slaythespire.gg/guides/slay-the-spire-best-character
combo	All for One	Claw	zero-cost engine	https://slaythespire.gg/guides/slay-the-spire-best-character
combo	Establishment	Windmill Strike	retained cards get cheaper	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Establishment	Sands of Time	retained cards get cheaper	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Master Reality	Conjure Blade	created cards come upgraded	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Master Reality	Evaluate	created cards come upgraded	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Talk to the Hand	Flurry of Blows	stance switching	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Nirvana	Cut Through Fate	Block whenever you Scry	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Nirvana	Third Eye	Block whenever you Scry	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Nirvana	Just Lucky	Block whenever you Scry	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Nirvana	Weave	Block whenever you Scry	https://www.thegamer.com/slay-the-spire-best-builds/
```
