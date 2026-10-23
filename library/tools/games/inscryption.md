# Inscryption

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*Claude's summary (Oct 2026), from general knowledge of the game and the rules and terms under Mechanics; not from the sources below.*
- Genre: single-player roguelike deckbuilder and escape room (Daniel Mullins, 2021).
- Board: lanes (4 per side in most of the game); cards attack the opposing lane, damage goes to the opponent when the lane is empty.
- Win: tip the damage scale 5 points to your side.
- Costs: four cost systems: Blood (sacrifice your creatures), Bones (gained when your creatures die), Energy (refills each turn and grows), Mox gems (gem cards on the board).
- Sigils: card abilities such as Airborne, Touch of Death, Bifurcated Strike, Unkillable, Fledgling, Worthy Sacrifice.
- Specific: each act has its own rules and boss; the four Scrybes stand for the four cost systems.

## Sources and notes

Sources:
[1] https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide (the four Scrybe decks of Act 2)
[2] https://progameguides.com/inscryption/which-deck-should-i-choose-in-act-2-of-inscryption/
[3] https://steamcommunity.com/app/1092790/discussions/0/3553931489687797930 (forum thread; replies named)

The wiki (fandom, wiki.gg) could not be read. Bones (paid by Undead cards, gained when cards die) is an alternative cost
(cost_type); Mox in three colours is multiple_resources.

## Factions

### Beast (Leshy)
*Claude:* Blood costs: sacrifice Squirrels and creatures to play beasts.
Known for: Blood costs, free Squirrels, Warren puts a Rabbit in hand, Adder kills what it damages, Hawk hits the foe directly
past blockers [1]; plays like Act 1, blood and bones [2]; skeletons and bots can be sacrificed for blood [3, RedLizard].

### Undead (Grimora)
*Claude:* Bones costs: cards that die feed the next, Brittle units.
Known for: Bones from Gravedigger and from cards destroyed, killed or sacrificed; destroying its own cards with the hammer;
Draugr releases a creature when it perishes [1].
Archetype: Necromancers make a card die twice to set off perish effects [3, SpongeKnob SquareNuts].

### Technology (P03)
*Claude:* Energy costs: robots, conduits and the energy that refills each turn.
Known for: Energy that rises each turn, energy-boosting cards, support circuits that buff robots, 49er moving on its own at the
end of the turn [1].

### Magick (Magnificus)
*Claude:* Mox gems: gem cards on the board pay for and power the spells.
Known for: Mox crystals of three colours; creatures that need a matching Mox; Blue Mage draws per Mox [1].

## Combos
- Necromancer + Obol: the Obol dies twice, giving bones twice [3, SpongeKnob SquareNuts]
- Warren + Rabbit: Warren supplies free Rabbits [1]
- Blue Mage + Sapphire Mox; Mage Knight + Ruby Mox; Junior Sage + Emerald Mox: they need the matching Mox [1]

## Mechanics
The mechanics the guides name, one per line as `name|concept|regex`, and the rules and terms as `# term:` lines. Read by `coverage.py --mechanics` and `key/key.py`.

```mechanics
# Mechanics of Inscryption: name|expected concept|wording in the sigil (keyword) definitions. Cards list only their sigils, so the
# check reads the keyword entries (coverage.py --keywords). Research (20 Oct 2026, built-in browser): inscryption.fandom.com/wiki/Sigils
# (all sigils of Acts 1-3 and the rulebook), and the real-world sources in tools/realworld/inscryption.tsv.
card into hand when played or struck|generate_cards|\bis created in your hand\b|\bcreated in your hand\b
strikes directly over blockers|evasion|\bstrike an opponent directly\b|\bstrike directly\b
kills what it damages|deathtouch|\bthat creature perishes\b
grows into a stronger form|transform|\bgrow into a more powerful form\b|\btransform to, or from\b
moves each turn|movement|\bwill move in the direction\b|\bwill move to that (empty )?space\b|\bmove towards them\b
tutor a card|tutor|\bsearch your deck for any card\b
returns to hand on death|cheat_death|\bwhen a card bearing this sigil perishes, a copy of it\b|\bwhen a card bearing this sigil is sacrificed, it does not perish\b
thorns and sentry|counterattack|\battacker of said card\b|\bthey are dealt 1 damage\b
cannot be attacked|immunity|\bwould attack a card bearing this sigil, it does not\b|\bimmune to the effects\b
worth more when sacrificed|sacrifice|\bwhen sacrificed\b|\bis sacrificed\b
bones as a resource|resource_gain|\b\d+ bones are awarded\b|\bgenerate 1 bone\b|\bgain 3 bones\b|\balso grant bones\b
hits several spaces|multi_target_attack|\bstrike each opposing space\b|\ban extra time\b
adjacent or circuit creatures gain power|aura|\bcreatures adjacent to a card bearing this sigil gain\b|\bwithin a circuit completed by a card bearing this sigil gain\b|\bmox cards on the owner's side of the board gain\b
opposing creature loses power|stat_loss|\bopposing a card bearing this sigil loses\b
dies after attacking|self_destruct|\bafter attacking, a card bearing this sigil perishes\b
effect when it dies|death_trigger|\bwhen a card bearing this sigil (perishes|dies)\b
draw cards|draw|\bdraw (\d+|a|a new hand of \d+) cards?\b|\bdraw a card\b
gems (mox) as a resource|resource_gain|\bgem is provided\b
energy as a resource|resource_gain|\benergy cell\b|\benergy never depletes\b
activated abilities|activated|\bactivate:
pay to grow|stat_gain|\bincrease the power and health\b|\bgains? \d+ power\b
prevent the first damage|shield|\bwould take damage, prevent that damage\b
random effects|random_effect|\bat random\b|\brandom (card|item)\b|\brandomly\b
creates units on spaces|summon|\bis created on (each|the)\b|\bfill all empty spaces\b|\bspawn (l33pb0ts|gem vessels)\b|\bdrop a (skeleton|squirrel)\b
blocks flyers|blocking|\bwill block an opposing creature bearing the airborne\b
pushes or throws creatures|forced_movement|\bthrown back\b|\bpushing any cards\b
heals|heal|\bare healed\b|\bto heal a card\b
```

## Cases
The real-world cases, one per line, tab-separated: `type  a  b  why  source` (see `realworld/RESEARCH.md`). Read by `realworld.py`, `realworld_report.py`, `realworld_why.py` and `learn_recipes.py`.

```tsv
signature	Beast	sacrifice	Blood costs paid by sacrifice	https://steamcommunity.com/app/1092790/discussions/0/3553931489687797930
signature	Beast	generate_cards	Warren puts a Rabbit in hand	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
signature	Beast	deathtouch	Adder kills what it damages	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
signature	Beast	evasion	Hawk hits past blockers	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
signature	Undead	cost_type	Bones	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
signature	Undead	sacrifice	destroying its own cards	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
signature	Undead	death_trigger	Draugr releases a creature when it perishes	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
signature	Technology	resource_gain	energy-boosting cards	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
signature	Technology	aura	support circuits buff robots	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
signature	Technology	autonomous_units	49er moves on its own	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
signature	Magick	multiple_resources	Mox of three colours	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
signature	Magick	draw	Blue Mage draws per Mox	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
archetype	Undead	sacrifice	Necromancers and perish effects	https://steamcommunity.com/app/1092790/discussions/0/3553931489687797930
combo	Necromancer	Obol	the Obol dies twice	https://steamcommunity.com/app/1092790/discussions/0/3553931489687797930
combo	Warren	Rabbit	Warren supplies Rabbits	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
combo	Blue Mage	Sapphire Mox	needs the matching Mox	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
combo	Mage Knight	Ruby Mox	needs the matching Mox	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
combo	Junior Sage	Emerald Mox	needs the matching Mox	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
```
