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

## The game's rules (from sources)
Read 30 Oct 2026 for the card database (cards_db, PROCESS step 0.10). [W] = Wikipedia "Slay the Spire", Gameplay section;
[M] = slaythespire.wiki.gg/wiki/Mechanics; [K] = slaythespire.wiki.gg/wiki/Keywords.
- The player alone fights: each turn a fresh hand of cards and three energy [W]; energy is set to the base energy (3) and 5
  cards are drawn at the start of the turn [M]. Any cards can be played while there is energy to pay their costs [W].
- Attack cards damage enemies; Skill cards buff the player, debuff enemies or add Block; Power cards keep their effect until
  the combat ends [W]; a played Power leaves the piles [M]. Block reduces damage taken in a turn [K].
- Cards not played go to the discard pile at the end of the turn [W] (shuffled into it [M]); Retained cards stay [K]. Drawing
  from an empty draw pile shuffles the discard pile into it [M]. Exhausted cards go to the exhaust pile until the combat
  ends [M][K]. The hand holds at most 10 cards [M].
- Enemies show their intent (attack and its damage, block, buffs, debuffs) before the player acts [W] and act left to right
  [M]; some enemy attacks add Wounds and other status cards to the deck [W][M]. A fight is won when the enemies die; at 0 HP
  the run ends [W][M].
- Between fights: card rewards (one of three), relics (permanent buffs for the run), potions (single use, free), campfires
  (heal or upgrade a card), shops (buy, remove cards) [W].
No record in read/sts1/game_rules.jsonl: no card category does anything its text does not say (there are no units; every
effect, including every Attack's damage, is on the card), and what the rules do for every card (draw 5, 3 energy, discard the
hand) is no combo between cards (Kaptain, 30 Oct 2026).

## Deck rule (deck_analysis.DECK_RULES, can_share; 31 Oct 2026)
A run is one character: its own cards, plus Colorless cards (any character gets them from the Shop, events or Prismatic
Shard; slaythespire.wiki.gg/wiki/Card), plus Curses, which events add to any deck (slay-the-spire.fandom.com/wiki/Cards).
Most relics are for every character; a few belong to one character (slay-the-spire.fandom.com/wiki/Relics). Potions are for
every character in the data. So an Ironclad card and a Silent card or relic never share a run.

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

## What the database must know (learned importing it, 30 Oct 2026)
- The player is the only one of my side: statuses go on the player (Strength, Dexterity, Focus, Wrath, Calm, Divinity) or
  on enemies (Vulnerable, Weak, Poison, Lock-On). A card that gives a status does what the status does.
- Strength: Attacks deal more. Dexterity: Block a card gives when played is bigger (not a Power's later Block, not
  Entrench; slaythespire.wiki.gg/wiki/Dexterity). Focus: Orbs are stronger. Vulnerable: attack damage taken is bigger.
- Orbs (Lightning: damage; Frost: Block; Dark: damage that grows; Plasma: energy) are put in slots by Channel and act at
  the end of the turn; Evoke uses them up. The card that channels an Orb does what the Orb does. More slots (Capacitor)
  keep more Orbs.
- Stances: Wrath, Calm and Divinity are each "this Stance" in their own texts; "whenever you change Stances" is entering
  any of them. 10 Mantra is Divinity.
- X costs: written "-1 energy" by the source; they are X (energy spent decides the size). Unplayable cards have no cost.
- Every character starts with a relic (Burning Blood, Ring of the Snake, Cracked Core, Pure Water); a boss relic
  "Replaces" it (Black Blood, Ring of the Serpent, Frozen Core, Holy Water).
- Runs: relics, potions, rest sites, shops and events are run rules (act run_rule), not card effects.

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
# term: Block: absorbs attack damage; it is removed at the start of your turn unless kept (Barricade: "Block is not removed at the start of your turn"); Entrench doubles it.
# term: Orbs: channelled into slots; Frost gives Block, Lightning deals damage; Focus strengthens orbs (thegamer; slaythespire.gg).
# term: Stances: Calm, Wrath and Divinity; switching between them (stance dancing) is the Watcher's burst (slaythespire.gg).
# term: Retain: the card stays in hand at the end of the turn (game glossary); Establishment makes retained cards cheaper (thegamer).
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
# dropped 31 Oct (Claude, Kaptain asked to drop wrong cases): both wait for Exhaust; neither Exhausts	# combo	Feel No Pain	Dark Embrace	Exhaust value	https://slaythespire.gg/guides/slay-the-spire-best-character
combo	After Image	A Thousand Cuts	both trigger on every card	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Catalyst	Noxious Fumes	Catalyst doubles Poison	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Catalyst	Bouncing Flask	Catalyst doubles Poison	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Glacier	Capacitor	Frost and more Orb slots	https://www.thegamer.com/slay-the-spire-best-builds/
# dropped 31 Oct (Claude, Kaptain asked to drop wrong cases): both use Orbs; neither feeds the other	# combo	Recursion	Loop	more use of Orbs	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Loop	Defragment	Focus scaling	https://slaythespire.gg/guides/slay-the-spire-best-character
combo	All for One	Claw	zero-cost engine	https://slaythespire.gg/guides/slay-the-spire-best-character
combo	Establishment	Windmill Strike	retained cards get cheaper	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Establishment	Sands of Time	retained cards get cheaper	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Master Reality	Conjure Blade	created cards come upgraded	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Master Reality	Evaluate	created cards come upgraded	https://www.thegamer.com/slay-the-spire-best-builds/
# dropped 31 Oct (Claude, Kaptain asked to drop wrong cases): Talk to the Hand changes no Stance	# combo	Talk to the Hand	Flurry of Blows	stance switching	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Nirvana	Cut Through Fate	Block whenever you Scry	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Nirvana	Third Eye	Block whenever you Scry	https://www.thegamer.com/slay-the-spire-best-builds/
combo	Nirvana	Just Lucky	Block whenever you Scry	https://www.thegamer.com/slay-the-spire-best-builds/
# dropped 31 Oct (Claude, Kaptain asked to drop wrong cases): both wait for Scry; neither Scries	# combo	Nirvana	Weave	Block whenever you Scry	https://www.thegamer.com/slay-the-spire-best-builds/
```
