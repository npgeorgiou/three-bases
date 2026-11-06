# Verify 3 (after fix_8)

## 1. Wanted changes
- Frost spawners -> Caranthir: Golden Child: as wanted. 11 lines back (decklines_after3): Aen Elle Aristocrat, Ard Gaeth, Eredin Bréacc Glas, Naglfar Crew, Red Riders, Red Riders: Charge/Precision/Spread, Tir na Lia, Wild Hunt Warrior (10 new) + White Frost (reason now "damages units or players; also makes stronger"). All spawn Frost (texts checked).
- Kaer Seren -> Keldar "is played" and Uprising -> Keldar "is played": gone as wanted (they play named units; Keldar wants a special card). Their "fills your hand" lines stay.
- Nithral, Imlerith's Wrath, Wild Hunt Bruiser -> Caranthir: not back, as wanted.

## 2. Other gone/new lines
- gwent Mysteries of Loc Feainn -> Dana Meadbh: Caretaker (waits, is played): right. Mysteries plays Loc Feainn: Convergence, a spell that creates the unit; Dana waits for a played unit.
- gwent Cintrian Knight / Redanian Knight -> Knight-Errant: same two lines, only reason words changed ("changes your units' stats"): right.
- runeterra The Virtuoso -> Annie / Jhin (levels), Kayle (level 2) / Tristana (level 2) -> Xolaani, Virtuoso -> Manasoul Student (waits): same pairs, reason words only: right.
- runeterra The Virtuoso -> The Witness (cheaper, is played): LOSS. Virtuoso plays Lotus Trap (a Skill); Witness's Flow counts "2+ spells or skills played last round" (keyword text 750384), so a Skill played does feed it.
  Cause: fix_8 change 2 (network.py, played rule "named cards in the game and none has a category of the need's kind"): Lotus Trap has category `ability` in runeterra, not `spell`, so the rule cut the line. The rule is applied to all games; it must treat `ability` (Skill) as spell-like in runeterra, or apply only to gwent (where categories are unit/spell/artifact/leader).

## 3. Failing cases not network.tsv deck pairs (n545-n587)
None. All 21 failing cases in REPORT.md are n545-n587.
