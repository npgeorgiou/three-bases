# Disney Lorcana

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*Claude's summary (Oct 2026), from general knowledge of the game and the rules and terms under Mechanics; not from the sources below.*
- Genre: physical trading card game (Ravensburger, Disney Lorcana, 2023); 60-card decks of up to two inks.
- Ink: once per turn a card with the inkwell symbol can be put face down into the inkwell; each inkwell card pays 1 each turn.
- Characters: drawn in (cannot act the turn they are played); they quest (exert for lore) or challenge exerted enemy characters.
- Other cards: actions (songs can be sung by exerting a character instead of paying), items and locations.
- Win: first to 20 lore; a player who must draw from an empty deck loses.
- Keywords: Bodyguard, Challenger, Evasive, Reckless, Resist, Rush, Shift, Singer, Support, Ward, Vanish.

## Sources and notes

Sources:
[1] https://www.wargamer.com/disney-lorcana/colors (Feb 2024: ink identities and deck types)
[2] https://wiki.mushureport.com/wiki/Amber
[3] https://wiki.mushureport.com/wiki/Amethyst
[4] https://wiki.mushureport.com/wiki/Emerald
[5] https://wiki.mushureport.com/wiki/Ruby
[6] https://wiki.mushureport.com/wiki/Sapphire
[7] https://wiki.mushureport.com/wiki/Steel
[8] https://geekydomain.com/blogs/guides/competitive-amethyst-steel-bounce-guide
[9] https://spellmana.com/amethyst-sapphire-deck-guide-lorcana/
[10] https://www.wargamer.com/best-disney-lorcana-cards

The wiki pages [2]-[7] compare inks ("less often than", "shared with"); an ink that has a mechanic less often than the ink
that leads it is a splash case. Lore gain and lore loss have no concept (points_scoring is a game rule).

## Factions

### Amber
*Claude:* Support: songs, healing, Bodyguard and Singer.
Known for: synergy and support, protection, healing [1]; Bodyguard, healing (more than Sapphire), Support, recovering
characters from the discard pile [2].
Less than others: card draw (less than Amethyst or Steel), strength reduction (less than Sapphire); discard shared with
Emerald [2].

### Amethyst
*Claude:* Magic: card draw, bouncing and moving characters.
Known for: returning its cards to hand or play, disruption, extra card draw [1]; far more card draw than any other ink,
filtering the top card, exerting opposing characters (more than Ruby), stopping them from readying [3].
Less than others: bounce (less than Emerald), Evasive (less than Emerald and Ruby) [3].
Decks: Amethyst/Ruby Bounce [1].

### Emerald
*Claude:* Trickery: discard, Evasive, Ward and bouncing.
Known for: flexibility, a toolbox [1][4]; making opponents discard, drawing [1]; bounce, granting Reckless or preventing
questing, strength increase (more than Ruby and Steel) [4].
Less than others: Rush (less than Amethyst and Ruby), lore loss (less than Ruby) [4].
Decks: midrange [1].

### Ruby
*Claude:* Aggression: banishing, Rush, Reckless and Challenger.
Known for: aggression, removal, Rush, big hard-hitting characters [1]; banishing opposing characters, Evasive (more than
Amethyst), readying exerted characters (more than Amber and Sapphire), causing lore loss [5].
Less than others: exerting opponents (less than Amethyst), strength increase (less than Emerald) [5].
Decks: Ruby Control, Amethyst/Ruby Bounce [1].

### Sapphire
*Claude:* Ramp and items: extra ink, Support and lore.
Known for: ramp, resource advantage, big combo cards [1]; putting more than one card into the inkwell per turn, items and
their cost reduction, strength reduction (more than Amber), Ward and Support it can grant [6].
Less than others: healing (Amber's is stronger), filtering (less than Amethyst), readying (less than Ruby) [6].
Decks: ramp and combo [1].

### Steel
*Claude:* Fighters: strong challenges, Resist, damage and items.
Known for: defence and direct damage, high Strength and Willpower [1]; direct damage, Bodyguard, challenge prevention,
banishing items [7]; brute force, and a "defensive fortress" design idea [7].
Less than others: strength increase (less than Emerald) [7].
Decks: midrange and control [1].

## Combos
- Madam Mim - Fox + Tinker Bell - Giant Fairy: bounce heals Tinker Bell, replay repeats her damage [8]
- Madam Mim - Snake or Fox + Merlin - Rabbit: each bounce and replay draws two cards [8][9]
- Tinker Bell - Giant Fairy + Grab Your Sword / A Whole New World: she sings the song for free [8]
- Captain Hook - Forceful Duelist + Mr. Smee - Bumbling Mate: Hook keeps Smee from damaging himself [8]
- Tipo - Growing Son + Madam Mim - Snake: quest, bounce, replay or ink [9]
- Merlin - Goat + Madam Mim - Snake / Fox, Arthur - Wizard's Apprentice, Bibbidi Bobbidi Boo: lore on each enter and leave,
  so bounce and replay [9][10]
- Stitch - Rock Star + Stitch - Carefree Surfer: Shift onto Rock Star [10]

## Mechanics
The mechanics the guides name, one per line as `name|concept|regex`, and the rules and terms as `# term:` lines. Read by `coverage.py --mechanics` and `key/key.py`.

```mechanics
# Mechanics the guides name: name|expected concept|wording on the cards. Checked with coverage.py --mechanics.
# https://www.wargamer.com/disney-lorcana/colors , https://wiki.mushureport.com/wiki/Sapphire , /Steel , /Emerald , /Ruby , /Amber
# Rules and terms for the game block (key.py read), only facts the source states: https://www.wargamer.com/disney-lorcana/keywords
# term: Exert: a card turned on its side; an exerted character can't use abilities that need exerting until it is readied. Characters ready again at the start of their owner's next turn.
# term: Quest: questing gathers lore, which wins the game. Reckless characters can't quest.
# term: Challenge: characters challenge opposing characters, using their Strength.
# term: Ink pays card costs; a newly played card must wait for its ink to dry before it can exert or quest.
# term: Songs: a character can sing a song for free when the song's ink cost fits its own; Singer N lets it sing songs costing up to N.
healing|heal|\bremove (up to )?(\d+|all) damage
recursion|return_to_hand|\breturn [^.]{0,40}to your hand
card draw|draw|\bdraw (a|\d+) cards?
discard|hand_disruption|\b(opponent|opponents|player)s? (chooses and )?discards?
bounce|bounce_enemy|\bto their player.s hand
ward|immunity|\bward\b
evasive|immunity|\bevasive\b
recover actions|recycle|\baction cards? [^.]{0,30}from your discard
cost reduction|cost_reduction|\bpay \d+ ink less
rush|haste|\brush\b
banish characters|destroy|\bbanish (chosen|all|each)
reckless|drawback|\breckless\b
readying|untap|\bready (this|chosen|all|your|another)
ink ramp|resource_gain|\binto your inkwell
lore increase|points_scoring|\b(gain \d+ lore|\+\d+ lore)
card filtering|selection|\blook at the top
bodyguard|taunt|\bbodyguard\b
challenge prevention|attack_lock|can'?t challenge
challenger|stat_gain|\bchallenger\b
direct damage|damage|\bdeal \d+ damage
singing|cost_type|\bsing\b|\bsong\b
shift|upgrade|\bshift\b
locations|zone_control|\blocation
support|assists_support|\bsupport\b
```

## Cases
The real-world cases, one per line, tab-separated: `type  a  b  why  source` (see `realworld/RESEARCH.md`). Read by `realworld.py`, `realworld_report.py`, `realworld_why.py` and `learn_recipes.py`.

```tsv
signature	Amber	heal	healing	https://wiki.mushureport.com/wiki/Amber
signature	Amber	protection	protection	https://www.wargamer.com/disney-lorcana/colors
signature	Amber	bodyguard	Bodyguard	https://wiki.mushureport.com/wiki/Amber
signature	Amber	assists_support	Support	https://wiki.mushureport.com/wiki/Amber
signature	Amber	revive	recovering characters from the discard pile	https://wiki.mushureport.com/wiki/Amber
signature	Amethyst	draw	more card draw than any other ink	https://wiki.mushureport.com/wiki/Amethyst
signature	Amethyst	return_to_hand	returns its cards to hand	https://www.wargamer.com/disney-lorcana/colors
signature	Amethyst	selection	filtering the top card	https://wiki.mushureport.com/wiki/Amethyst
signature	Amethyst	disable	exerting opposing characters	https://wiki.mushureport.com/wiki/Amethyst
signature	Emerald	flexibility	a toolbox ink	https://wiki.mushureport.com/wiki/Emerald
signature	Emerald	hand_disruption	making opponents discard	https://www.wargamer.com/disney-lorcana/colors
signature	Emerald	bounce_enemy	bounce	https://wiki.mushureport.com/wiki/Emerald
signature	Emerald	forced_attack	granting Reckless	https://wiki.mushureport.com/wiki/Emerald
signature	Emerald	stat_gain	strength increase more than Ruby and Steel	https://wiki.mushureport.com/wiki/Emerald
signature	Ruby	haste	Rush	https://www.wargamer.com/disney-lorcana/colors
signature	Ruby	destroy	banishing opposing characters	https://wiki.mushureport.com/wiki/Ruby
signature	Ruby	evasion	Evasive	https://wiki.mushureport.com/wiki/Ruby
signature	Ruby	untap	readying exerted characters	https://wiki.mushureport.com/wiki/Ruby
signature	Sapphire	resource_gain	more than one card into the inkwell	https://wiki.mushureport.com/wiki/Sapphire
signature	Sapphire	cost_reduction	items cost less	https://wiki.mushureport.com/wiki/Sapphire
signature	Sapphire	stat_loss	strength reduction more than Amber	https://wiki.mushureport.com/wiki/Sapphire
signature	Sapphire	immunity	Ward it can grant	https://wiki.mushureport.com/wiki/Sapphire
signature	Steel	damage	direct damage	https://www.wargamer.com/disney-lorcana/colors
signature	Steel	bodyguard	Bodyguard	https://wiki.mushureport.com/wiki/Steel
signature	Steel	attack_lock	challenge prevention	https://wiki.mushureport.com/wiki/Steel
archetype	Amber	sustain	protection and healing	https://www.wargamer.com/disney-lorcana/colors
archetype	Amethyst	card_advantage	extra card draw	https://www.wargamer.com/disney-lorcana/colors
archetype	Emerald	disruption	discard and bounce	https://www.wargamer.com/disney-lorcana/colors
archetype	Ruby	aggro_tempo	aggression and Rush	https://www.wargamer.com/disney-lorcana/colors
archetype	Ruby	control	Ruby Control	https://www.wargamer.com/disney-lorcana/colors
archetype	Sapphire	ramp	ramp	https://www.wargamer.com/disney-lorcana/colors
archetype	Steel	control	control decks	https://www.wargamer.com/disney-lorcana/colors
archetype	Steel	fortress	defence, defensive fortress	https://wiki.mushureport.com/wiki/Steel
splash	Amber	draw	less card draw than Amethyst or Steel	https://wiki.mushureport.com/wiki/Amber
splash	Amber	stat_loss	strength reduction weaker than Sapphire's	https://wiki.mushureport.com/wiki/Amber
splash	Amber	hand_disruption	discard shared with Emerald	https://wiki.mushureport.com/wiki/Amber
splash	Amethyst	bounce_enemy	bounce less than Emerald	https://wiki.mushureport.com/wiki/Amethyst
splash	Amethyst	evasion	Evasive less than Emerald and Ruby	https://wiki.mushureport.com/wiki/Amethyst
splash	Emerald	haste	Rush less than Amethyst and Ruby	https://wiki.mushureport.com/wiki/Emerald
splash	Ruby	disable	exerting less than Amethyst	https://wiki.mushureport.com/wiki/Ruby
splash	Ruby	stat_gain	strength increase less than Emerald	https://wiki.mushureport.com/wiki/Ruby
splash	Sapphire	heal	healing weaker than Amber's	https://wiki.mushureport.com/wiki/Sapphire
splash	Sapphire	selection	filtering less than Amethyst	https://wiki.mushureport.com/wiki/Sapphire
splash	Sapphire	untap	readying less than Ruby	https://wiki.mushureport.com/wiki/Sapphire
splash	Steel	stat_gain	strength increase less than Emerald	https://wiki.mushureport.com/wiki/Steel
combo	Madam Mim - Fox	Tinker Bell - Giant Fairy	bounce heals her, replay repeats damage	https://geekydomain.com/blogs/guides/competitive-amethyst-steel-bounce-guide
combo	Madam Mim - Snake	Merlin - Rabbit	bounce and replay draws two	https://geekydomain.com/blogs/guides/competitive-amethyst-steel-bounce-guide
combo	Madam Mim - Fox	Merlin - Rabbit	bounce and replay draws two	https://geekydomain.com/blogs/guides/competitive-amethyst-steel-bounce-guide
combo	Tinker Bell - Giant Fairy	Grab Your Sword	she sings it for free	https://geekydomain.com/blogs/guides/competitive-amethyst-steel-bounce-guide
combo	Tinker Bell - Giant Fairy	A Whole New World	she sings it for free	https://geekydomain.com/blogs/guides/competitive-amethyst-steel-bounce-guide
combo	Captain Hook - Forceful Duelist	Mr. Smee - Bumbling Mate	Hook keeps Smee alive	https://geekydomain.com/blogs/guides/competitive-amethyst-steel-bounce-guide
combo	Tipo - Growing Son	Madam Mim - Snake	quest, bounce, replay or ink	https://spellmana.com/amethyst-sapphire-deck-guide-lorcana/
combo	Merlin - Goat	Madam Mim - Snake	lore on enter and leave, bounce	https://spellmana.com/amethyst-sapphire-deck-guide-lorcana/
combo	Merlin - Goat	Madam Mim - Fox	lore on enter and leave, bounce	https://www.wargamer.com/best-disney-lorcana-cards
combo	Merlin - Goat	Arthur - Wizard's Apprentice	lore on enter and leave, bounce	https://www.wargamer.com/best-disney-lorcana-cards
combo	Merlin - Goat	Bibbidi Bobbidi Boo	cheaper replays of Merlin	https://www.wargamer.com/best-disney-lorcana-cards
combo	Stitch - Rock Star	Stitch - Carefree Surfer	Shift onto Rock Star	https://www.wargamer.com/best-disney-lorcana-cards
```
