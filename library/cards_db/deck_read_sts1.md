# Slay the Spire deck networks: every wrong or missing line, by cause (30 Oct 2026, v50)

Claude's reading of all 22 decks (`deck_lines.py sts1`), before Kaptain's check. Each family names the rule that made the
wrong line, what the same rule did elsewhere (all eight games, counted on `dump_lines.py` dumps of every deck network
before and after the fix), and the rule that replaced it. Counts "before" are lines whose reason holds the phrase. Cases
nst01-nst18 in cases/network.tsv hold one point each. `review_check.py` fails a family that lacks one of the three lines.

## F1 What a status or a repeat makes bigger read as what it asks for
Every Attack -> Flex, Inflame, Spot Weakness, Limit Break, Vajra, Red Skull, Reprogram, Wish, Wrist Blade ("is an Attack it
asks for"); Skills -> Burst, Powers -> Amplify, every card -> Echo Form, Poison cards -> Snecko Skull; Shiv -> Accuracy beside
Accuracy -> Shiv; Heavy Blade -> Flex beside Flex -> Heavy Blade. No Strength, Dexterity or Focus giver had a line to the cards
it makes stronger.
- Root cause: network.py lines_of read every type or card filter of an effect as an ask, also the filters of repeat and
  increase_effect (Strength: "Attacks deal more", read through uses_keyword on every Strength giver); aimed_rows took only a
  card's own rows, so a status the card gives (Strength, Focus) and an ability it gives (Burst) drew no help line;
  "whenever you apply Poison, apply 1 more" and Dexterity (an add to a keyword my cards give) were triggers, not help.
  Heavy Blade's record made Strength stronger for every card (text: "affects this card").
- Same error elsewhere: "is an Attack/Skill/Power it asks for" sts1 115/7/15, no other game; "it names" from a boost
  (Accuracy) sts1 2 of 22 (Runeterra 19 and Duelyst 1 are names of cards they make or wait for: unchanged); "it gives
  stronger" Monster Train 4 and Runeterra 2 unchanged (Deranged Brute, Ava Achiever really make the keyword stronger for all).
  Into the Breach: the new status rule first drew Napalm Mech -> Dispersal Mech "makes the Fire it gives stronger" (Fire is a
  filter on the boosted Mechs, not a keyword made stronger); the keyword rule now needs the effect's own keyword: gone. Final
  dumps: every other game keeps all its lines and pairs; only the order of reason parts changed.
- Fix: repeat and increase_effect filters are never asks; a status the card gives my side with a positive amount brings the
  status's boost to the card (Flex -> every Attack "makes its effect bigger", Defragment -> the Orb channelers); a trigger whose
  effects only repeat or enlarge what set it off is help, also when given (Burst -> Skills "plays it again"); keyword_adders:
  an ability that adds to a keyword my cards give -> those givers ("makes the Poison it gives bigger"; Dexterity only for
  Block from cards); givers_of counts "Channel 1 Lightning" as putting Lightning; fixes/sts1/v50.py: "affects this card" is
  pick self.

## F2 The card itself in hand, or what it picks there, read as a hand to fill
Draws -> Ghostly Armor, Echo Form, Deva Form ("fills your hand"); Reflex, Tools of the Trade -> Gambling Chip.
- Root cause: boost_lines' hand rule took every count or test of my hand, also Ethereal's "if this is still in your hand"
  (of_pick self) and Gambling Chip's count of the cards it discards (of_pick chosen).
- Same error elsewhere: "fills your hand" sts1 14 before; Runeterra 35, Stormbound 2, Duelyst 1 are real hand counts: unchanged.
- Fix: the hand rule skips tests of the card itself and of what it picks.

## F3 Cards with no number matched cost filters; "cost X" lost
All for One ("cost 0 cards") -> Burn, Void, Girya, Snecko Eye, Reinforced Body; Chemical X ("cost X cards") -> Deus Ex Machina,
Miracle, Expunger, Deva Form, Ragnarok.
- Root cause: matches() let a card with no cost pass any cost filter; the source writes X costs as "-1 energy"; Chemical X's
  record had no filter at all.
- Same error elsewhere: "can bring it back to hand" sts1 11 before, Monster Train 1 (unchanged); no other game lost lines.
- Fix: a cost filter never matches a card without a number; "cost eq X paid" matches X costs (cards_of x_cost);
  supplement_sts1.py writes "-1 energy" as "X energy"; fixes/sts1/v50.py gives Chemical X its filter.

## F4 A drawback read as a need
Draws -> Void ("fills your hand", "makes you draw cards"); TURBO, Nunchaku -> Void ("lets you gain mana").
- Root cause: harm_abilities knew damage, kills and discards on the card, not a forced energy loss; lines_of skipped harm only
  for triggers, so the energy cost's condition ("needs mana") stayed.
- Same error elsewhere: forced spend_mana triggers exist only in sts1 (Void); paid costs (played, activated: Inscryption Bones,
  Runeterra) stay needs. "lets you gain mana" Stormbound 5, Inscryption 4 unchanged.
- Fix: a forced trigger whose effects only spend my energy is harm; harm abilities make no lines of any role.

## F5 An upper limit read as a need; Unplayable cards counted as played
Every card -> FTL ("if you have played less than 3 cards"); Void -> FTL.
- Root cause: played_lines and lines_of read every count of plays as wanting more of them.
- Same error elsewhere: "is a card it counts when played" sts1 143 before (Runeterra 113, Faeria 16, Duelyst 13, Monster
  Train 13 unchanged: none is an upper limit on another card's plays; Twisted Fate's "first 3 times" waits for plays).
- Fix: capped(): a count with lt/le of a happening that is not the ability's own trigger on other cards wants nothing;
  unplayable() cards are never a card played.

## F6 The attacker of my side had no side
Flame Barrier -> Rupture, Self-Forming Clay, Red Skull ("damages your units or players").
- Root cause: refs.py took the side of "the attacker" from the trigger's actor; "whenever you are attacked" names none.
- Same error elsewhere: "damages your units or players" sts1 8 before, Runeterra 26 (unchanged: their damage is to my side).
- Fix: who attacks, strikes, fights or damages what is mine (or the card itself), with no side named, is an enemy.

## F7 Choosing a card for the run read as making one
Bottled Flame -> Kunai, Shuriken, Vajra ("makes an Attack it asks for").
- Root cause: lines_of counted choose_card with a type filter as making that type, also a pick from my own deck.
- Same error elsewhere: sts1 3 (Bottled Flame, Lightning, Tornado); Runeterra's Invoke and Aphelios picks are from outside: kept.
- Fix: a choose_card from my deck, hand or discard makes nothing.

## F8 Missing lines: kept keywords, Orb rule changes, Stances
Barricade -> Body Slam; Electrodynamics -> Lightning channelers; Crescendo, Tranquility, Teardrop Locket -> Mental Fortress,
Flurry of Blows.
- Root cause: no rule for "keyword is not removed"; a rule change on my Orbs ("can" on kind keyword) was dropped by
  aimed_rows; "whenever you change Stances" waited for the keyword Stance, which no card gives.
- Same error elsewhere: none in other games (no keyword_removed "cant", no "can" on a keyword kind, no keyword text calls
  another keyword "this X").
- Fix: boost_lines: a kept keyword helps the cards that count it ("keeps your Block"); aimed_rows: "can" on my keyword
  helps its givers; fixes/sts1/v50.py: a Stance filter is the keywords whose text says "this Stance" (Wrath, Calm, Divinity).

## F9 Links from what every card does (Kaptain 30 Oct 2026, 1)
Every card -> After Image, A Thousand Cuts ("whenever you play a card"); Echo Form -> every card ("plays it again").
- Root cause: played_lines and object_help_lines skipped "any card" but not a kind that every playable card of the game
  is (Slay the Spire: every card is a spell).
- Same error elsewhere: "is a card it counts when played" sts1 103 before, 0 now with no type; Runeterra 113 -> 109 (Wizened
  Helmsman now says "an Elemental"), Faeria 16, Duelyst 13, Monster Train 13 unchanged (their kinds are narrowed).
- Fix: every_card_kinds(): a kind every playable card of the game is counts as not narrowed; the reason names the type
  ("is an Attack it counts when played").

## F10 The game's normal attack fed death reactions (Kaptain 30 Oct 2026, 2)
Strike (Silent) -> Corpse Explosion, The Specimen ("makes enemy units die").
- Root cause: every damage effect makes a death, so a plain hit on one enemy fed every "when an enemy dies".
- Same error elsewhere: Runeterra "kills units" 12 -> 8 (Mystic Shot, Shock Blast -> the Sentinels: plain hits, as the
  earlier call that removal helps no card in particular); sts1 30 -> 28.
- Fix: special_abilities(): an ability whose every effect is damage to one chosen or random target makes no enemy death
  for these lines; poison, hits on all, kill effects and boosts still do.

## F11 Helpers drawn as needing what they help (Kaptain 30 Oct 2026, 5d, 5e, 5g)
Block cards -> Barricade ("enables: makes your units get Block"); Bag of Marbles and Bash (Vulnerable) had no line to the
damage cards.
- Root cause: "Block is not removed" was read as a need for Block; a status that makes damage bigger (Vulnerable on the
  enemy, Wrath and Divinity on me) had no rule.
- Same error elsewhere: no other game has a keeper of a keyword or such a status in its decks (0 lines either way).
- Fix: keepers need nothing and point at the Block cards ("keeps the Block it gives", 10 lines); status_damage_givers():
  the givers point at every card of mine that deals damage ("gives Vulnerable: its damage is bigger", 28 lines; not
  Lock-On, which only the Orbs use, nor Mantra, which only leads to Divinity).

## F12 A cost that drops for each X drawn as "enables" (Kaptain 30 Oct 2026, 5h)
Gambling Chip -> Eviscerate ("enables: makes you discard cards").
- Root cause: the line kind came from the need (a count: enables), not from what the count does (lowers the cost).
- Same error elsewhere: Runeterra 23 lines (Windborne Mariner, Monster Harpoon, Bloody Business, Remembrance, Hidden
  Pathways), Faeria Windstorm Colossus; "cheaper" Runeterra 85 -> 108.
- Fix: an ability whose every effect lowers this card's cost (also "cost=minus") makes its need lines "makes cheaper";
  a reason said as cheaper is not said again as enables. Case nfa42 rewritten.

## F13 Wording and repeated reasons (Kaptain 30 Oct 2026, 5b, 5c)
"Flex -> Heavy Blade: makes your units get Strength" (it is the player); "Whirlwind -> Pen Nib: enables: is an Attack it
asks for; also is a card it counts when played; also triggers: is a card it counts when played".
- Root cause: the "given keyword" sentence always said "your units"; one count was drawn by two rules (type asks and
  played cards) and by two rows (trigger and condition) of one ability.
- Same error elsewhere: "makes your units get" sts1 44 -> 0 (other games keep it: their keywords go on units);
  Kunai, Shuriken, Finisher, Force Field, Wizened Helmsman lines now said once.
- Fix: a keyword on the player is "gives you X" in a game where the player is no card; counted plays come from
  played_lines only, once per reason, by the strongest kind (cheaper, triggers, enables).

## F14 Abilities given to the player were never set off by plays (Kaptain 30 Oct 2026, h; deck audit)
A Thousand Cuts, After Image, Rage ("whenever you play an Attack this turn"), Choke had no line from the cards that set them off.
- Root cause: played_lines read only a card's own triggers, not those it gives the player; "whenever you play a card" (no
  type) had no feeder once every-card links were dropped.
- Same error elsewhere: Duelyst's given "your next minion costs 2 less and takes 2 damage" (Flash Reincarnation) would have
  drawn 9 wrong lines; it acts on the card that sets it off, so it is skipped (help or harm to that card, not a wait).
  Other games: no change.
- Fix: played_lines reads given triggers too; "whenever you play a card" is fed by the cards that make more cards to play
  (Blade Dance's Shivs: 17 lines).

## F15 Energy and costs not counted (Kaptain 30 Oct 2026, d, f; deck audit)
Snecko Eye (Confused: random costs), Meteor Strike (3 Plasma: energy), energy -> X cards (Conjure Blade, Reinforced Body)
had no lines; Defect Snecko had 6 lines.
- Root cause: the paying rule read only a card's own energy and cost cuts: not a status it gives (Confused), not an Orb it
  puts in (Plasma), and X costs have no number.
- Same error elsewhere: other games have none of the three in decks (no change).
- Fix: a status the card gives me that sets costs pays; an Orb's energy pays (at least 1 per Orb put in); every energy gain
  helps X cards ("more energy: a bigger X").

## F16 Starting relics missing from decks (Kaptain 30 Oct 2026, i)
Black Blood replaces Burning Blood, yet Burning Blood was in no deck; Pure Water had no character.
- Root cause: decks are guides' card lists; what the game gives every deck of a character was never added.
- Same error elsewhere: only Slay the Spire has starter items (rarity starter).
- Fix: deck_analysis.starters adds the deck's character's starter (the region most of its cards have) unless a card says
  "Replaces" it; supplement_sts1.py: a relic with no character takes that of the relic that replaces it.

## F17 Orb cards: rule changes, slots, Lock-On, "next Orb" (Kaptain 30 Oct 2026, e; deck audit)
Loop ("your next Orb") and Capacitor (2 Orb slots) had no line; Lock-On had no rule.
- Root cause: Loop's record had no Orb filter; no rule for more slots; Lock-On's damage boost is by Orbs only.
- Same error elsewhere: none in other games' decks.
- Fix: fixes/sts1/v51.py (an Orb effect with no filter acts on the four Orbs); slot gains help the cards that put things in
  slots; Lock-On helps the cards that put damaging Orbs in.

## F18 Picks, kept draws, adders, Mantra, Melter (Kaptain 30 Oct 2026, b, c; deck audit)
Bottled Flame read as asking for Attacks; Scrape (keeps 0-cost draws) had no line to 0-cost cards; Snecko Skull drawn as
applying Poison itself; Mantra givers (Devotion, Worship) had no line though 10 Mantra is Divinity; Melter (removes Block)
had no rule.
- Root cause: what a card does to the card it picked was read as asks; a discard after a draw was not read as a filter of
  what stays; an adder's own rows fed needs; a keyword that leads to another was not followed.
- Same error elsewhere: none in other games (no change in their lines).
- Fix: a card that picks from my deck is a tutor ("picks it from the deck"); draw + discard of those not matching keeps the
  rest ("draws it and keeps it"); adders feed no needs; a keyword that gives a boosting keyword counts as it; removing an
  enemy keyword that stops damage helps cards that want unblocked damage (no deck has both yet).
- Claw (c): every copy is one card in the network, so Claw cannot link to itself; the cards that bring Claws back (All for
  One, Scrape) are linked to it.

## F19 Wording: "makes you lose HP", "exhausts cards" (deck audit)
- Root cause: the sentences assumed units or a Nexus; Exhaust had no sentence.
- Same error elsewhere: only games with no units of mine (Slay the Spire); Exhaust only in Slay the Spire.
- Fix: damage to me in a game without units of mine is "makes you lose HP"; ACT "exhausts cards".

## Open (for Kaptain)
- Known gaps: Blizzard and Thunder Strike count every Channel; Through Violence is not in the library.
