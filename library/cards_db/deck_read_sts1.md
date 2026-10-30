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

## Open (for Kaptain)
- Every card -> After Image, A Thousand Cuts ("whenever you play a card"): drawn with a tiny weight; drop them?
- Strike and other damage -> Corpse Explosion, The Specimen ("makes enemy units die"): any damage can kill.
- Energy gains -> 2-3 cost cards ("pays for it", the Faeria rule of a third of the top tenth of costs).
- Dexterity also reaches Block given later by Powers (After Image, Mental Fortress); the records cannot tell it apart.
- Known gaps: Blizzard and Thunder Strike count every Channel; Through Violence is not in the library.
