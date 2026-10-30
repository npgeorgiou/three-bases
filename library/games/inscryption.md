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
- Sigils move between cards (patterns check, 26 Oct 2026, from the wiki pages and the library's sigil entries): in Act I a card
  sacrificed at the Mysterious Stones gives its sigil to another card, so most combos are a card plus a sigil it was given, not two
  cards. A totem (head = tribe, body = sigil) gives that sigil to every card of the tribe; the Squirrel head is found in Leshy's
  cabin and is not in Kaycee's Mod.
- Created cards copy sigils: Dams from Dam Builder "adopt any other sigils from the card that spawned them" (so Worthy Sacrifice or
  Unkillable on a Beaver reaches its Dams). A card played by Corpse Eater triggers "when played" sigils (Fecundity, Rabbit Hole).
- Bones: 1 per card of yours that dies (4 with Bone King); the Bone Lord's altar gives 8 Bones at the start of every battle when
  the Black Goat is sacrificed to him, 1 for any other card. Act II: Tomb Robber's Skeletons broken with the Hammer give a Bone per
  Necromancer in play.
- Library entries: cards list only their sigils and traits ("Sigils: Unkillable."); costs are in the cost field; sigil entries
  are wiki pages (rulebook line first, then notes on single cards). Several cards were merged into a card with the same text
  (Dam into Bait Bucket, Bee into Bat, Skeleton into Revenant, Red Hart into Elk); Squirrel, Rabbit, Pelts, Geck, Urayuli and
  Child 13 are not in the library.

## The game's rules (from sources)
*Read 29 Oct 2026: https://en.wikipedia.org/wiki/Inscryption, and the Inscryption fandom wiki pages Card Battle (rev 12984),
Blood (13205), Bones (11499), Energy (11039), Mox (10838), Cost (10841), Health (3914), Power (11760), Circuits (9920),
Side Deck (12407), Starter Deck (11826), Special Card Behaviours (12544).*
- Board: a 3x4 grid, a 3x5 grid in Act III; the player plays cards into the bottom row, the opponent plays cards ahead of
  time into the top row (Wikipedia). The opponent plays into its back lanes; cards in its front lanes attack (Card Battle).
  Act III has a fifth lane (Circuits). Cards are placed on the player's side of the board (Card Battle).
- Turns: draw one card from the main deck or the side deck, place cards, ring the bell; at the end of the turn all cards on
  the player's side attack, the leftmost first; then the opponent's turn (Card Battle). Side decks: Squirrels in Act I,
  Empty Vessels in Act III, Skeletons and Mox cards in the Finale; Act II has none (Side Deck, Card Battle).
- Attacks: each card attacks the opponent's card in the same column, dealing its attack to that card's health; an
  unopposed card attacks the opponent directly (Wikipedia). Health drops by the attacker's Power; at 0 the creature dies
  (Health).
- Winning: tip the scale 5 points (teeth) to one side; damage is done by cards striking empty board spaces (Wikipedia,
  Card Battle).
- Costs: four types, Bones, Blood, Energy and Mox (Cost). Blood: almost any card can be sacrificed for 1 Blood (Worthy
  Sacrifice: 3); sacrificing kills the card and gives 1 Bone (Blood). Bones: whenever a card on the player's side perishes
  for any reason the player gets 1 Bone (Bone King: 4); a Bones card takes its cost from the player's total (Bones).
  Energy: replenished at the start of the turn and the maximum grows by 1 up to 6 (Energy). Mox: a Mox card of the right
  colour must be on the player's side to play a Mox creature (Mox).
- Traits (wiki Traits, rev 13178, read 30 Oct 2026): markers for other code, not sigils. In battle: Ant (counted by Ants),
  Gem (counted by Gem Dependant and other gem sigils), Giant (+1 Power each turn once out of cards), Terrain (cannot be
  sacrificed unless it has Worthy Sacrifice), Uncuttable (immune to Scissors, Fish Hook, Skinning Knife). Outside battle:
  KillsSurvivors, Goat, Pelt, SatisfiesRingTrial, DeathCardNonOption, Fused; the cut traits have no code.
- Circuits (Acts II and III): two conduit cards on the same side make a circuit; the cards between them are powered; if
  either conduit is destroyed the circuit is broken (Circuits).
Not written as game rules (they say nothing about which cards belong together): Energy refilling each turn, drawing from the
side deck, placing on any empty space of one's own row.

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
# (all sigils of Acts 1-3 and the rulebook).
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
hits several spaces|aoe_damage|\bstrike each opposing space\b|\ban extra time\b
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
signature	Beast	evasion	Hawk hits past blockers	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
signature	Undead	cost_type	Bones	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
signature	Undead	resource_gain	Bones from Gravedigger and from cards that die	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
signature	Magick	cost_type	Magick cards are paid with Mox gems	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
signature	Magick	draw	Blue Mage draws per Mox	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
combo	Necromancer	Right	the Obol dies twice	https://steamcommunity.com/app/1092790/discussions/0/3553931489687797930
combo	Warren	Rabbit	Warren supplies Rabbits	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
combo	Blue Mage	Sapphire Mox	needs the matching Mox	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
combo	Mage Knight	Ruby Mox	needs the matching Mox	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
combo	Junior Sage	Emerald Mox	needs the matching Mox	https://primagames.com/gaming/inscryption-scrybe-starting-deck-act-2-guide
combo	Ouroboros	Fecundity	Ouroboros grows each time it dies; Unkillable returns it and Fecundity copies it	Kaptain's combo list, 26 Oct 2026; source named: Inscryption Wiki
combo	Warren	Unkillable	Warren returns to hand on death and gives a Rabbit each time it is played	Kaptain's combo list, 26 Oct 2026; source named: r/inscryption
combo	Cuckoo	Fecundity	copies of Cuckoo put an egg opposite each time one is played	Kaptain's combo list, 26 Oct 2026; source named: YouTube
combo	Beaver	Worthy Sacrifice	Dams adopt the Beaver's sigils, so each Dam counts as 3 Blood	https://inscryption.fandom.com/wiki/Dam_Builder
combo	Urayuli	Corpse Eater	Corpse Eater plays Urayuli without its 4 Blood cost	https://inscryption.fandom.com/wiki/Urayuli
combo	Fecundity	Corpse Eater	a card played by Corpse Eater triggers Fecundity	Kaptain's combo list, 26 Oct 2026; source named: r/inscryption
combo	Black Goat	Boon of the Bone Lord	sacrificing the Black Goat to the Bone Lord gives 8 Bones each battle	https://inscryption.fandom.com/wiki/The_Bone_Lord
combo	Pronghorn	Touch of Death	Bifurcated Strike with Touch of Death kills both creatures it strikes	Kaptain's combo list, 26 Oct 2026; source named: YouTube
combo	Mantis God	Fecundity	copies of a three-way striker in hand	Kaptain's combo list, 26 Oct 2026; source named: Steam
combo	Geck	Fecundity	a free card that copies itself when played	Kaptain's combo list, 26 Oct 2026; source named: r/inscryption
combo	Tomb Robber	Necromancer	Skeletons from Tomb Robber die twice with Necromancer: more Bones	https://inscryption.fandom.com/wiki/Bones
combo	Necromancer	Bone Heap	the Bones loop pays for Bone Heap's Enlarge	Kaptain's combo list, 26 Oct 2026; source named: Inscryption Wiki
combo	Squirrel	Worthy Sacrifice	Squirrel totem with Worthy Sacrifice: every Squirrel counts as 3 Blood	https://inscryption.fandom.com/wiki/Totem
combo	Squirrel	Fecundity	Squirrel totem with Fecundity: every Squirrel played copies itself	https://inscryption.fandom.com/wiki/Totem
combo	Squirrel	Unkillable	Squirrel totem with Unkillable: sacrificed Squirrels return to hand	Kaptain's combo list, 26 Oct 2026; source named: TheGamer
combo	Squirrel	Ant Spawner	Squirrel totem with Ant Spawner: every Squirrel played gives an Ant	Kaptain's combo list, 26 Oct 2026; source named: ResetEra
combo	Insect	Bees Within	Insect totem with Bees Within: struck insects give a Bee	https://inscryption.fandom.com/wiki/Totem
combo	Reptile	Corpse Eater	Reptile totem with Corpse Eater: a reptile in hand is played free into the space of a creature that died; Unkillable Ouroboros (a reptile) returns to hand and comes back	https://inscryption.fandom.com/wiki/Totem
```

## Notes from the patterns check
Patterns check, 26 Oct 2026 (Claude). Counts are from the answer key (what the card text shows), cards of the four factions only.
- Cases removed, no lead of 1.5 times in the cards: Beast deathtouch (2 of 77 cards, rest 2 of 97: 1.3 times); Undead
  death_trigger (3 of 20, rest 18 of 154: 1.3 times); Technology resource_gain (10 of 57, rest 19 of 117: 1.1 times; the Mox
  vessels give gems too); Technology aura (1 of 57, rest 2 of 117: Buff Conduit only); Technology autonomous_units (no card;
  moving on its own is movement: 3 of 57 against 18 of 117 elsewhere).
- Costs are not in the card text. Cards list only sigils and traits; the cost is in the cost field: Beast 56 of 77 Blood,
  Undead 18 of 20 Bones, Technology 50 of 57 Energy, Magick Mox gems. `cost_rules.py` tags them (Blood: sacrifice as the cost;
  Bones and Mox: cost_type), and faction signatures count cost tags (Kaptain, 26 Oct 2026). "Several resource types" is a fact of
  the whole game, so the Magick case is cost_type (paid with gems).
- Undead (Kaptain, 26 Oct 2026): the "destroying its own cards" of source [1] is the hammer, an item every player gets, not an
  Undead card (1 of 20 Undead cards destroys its own units): case removed. Bones gained when cards die is Undead's (case added).
  The archetype "Necromancers and perish effects" is one card (Necromancer), not the faction: 6 of 20 Undead cards have a death
  mechanic, and Beast's Blood costs make Beast the faction whose units die on purpose: case removed.
- Unkillable and the like ("when it dies, a copy goes to your hand") are return_to_hand, not revive (Kaptain, 26 Oct 2026).
- Sigil entries are wiki pages: the rulebook line, then notes on single cards (Many Lives: "on certain cards ... transform";
  Waterborne: the Kraken's "random Tentacle card"). Tags from the notes reach every card bearing the sigil, so patterns read the
  rulebook wording, and sigil names in another entry's prose are not that entry's ability.
- "At the start of the battle / phase / run" is not a turn trigger. "Activate: Pay" is an activated ability, "activated" in
  passing is not.
