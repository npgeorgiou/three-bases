## C1 lr_dq.md 7 (MISSED CAUSE, open, 0 table lines from the same code)
Gwent is missing or thin where it belongs: 16 (what sets off revive) lists Gwent only for hand_disruption (Kambi -> Call of the Depths) and not for destroy, removal, death_trigger or cheat_death, though 03 says Gwent has revive -> removal -> other_death_trigger; and Skellige (Deathwish, Resurrect, graveyard) is absent from 12 though Monster is shown.
- W gwent: Kambi -> Call of the Depths: uses a keyword or status | network.py [698]
- W gwent: Morkvarg -> Dettlaff: Higher Vampire: NONE | network.py []
- W gwent: Dagon: Risen -> Dettlaff: Higher Vampire: NONE | network.py []
- R gwent: Morkvarg -> Dettlaff: Higher Vampire: NONE | network.py []
  Morkvarg:
    when 2122 dies self
    when 4517 leaves_play self
    when 4612 dies self
    when 4517 leaves_play self
    do 2122 own summon self
    do 2122 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4612 own summon self
    do 4612 own give_keyword self
    do 4517 uses_keyword obliterate self
  Dettlaff: Higher Vampire:
    when 2823 dies self
    do 2823 own revive unit mine self discard
  Dagon: Risen:
    when 4483 always
    when 4517 leaves_play self
    when 4484 always
    when 4485 turn_end
    when 4486 dies self
    when 4487 dies self
    when 4488 dies self
    when 4518 turn_start
    when 4489 dies self
    when 4490 dies self
    when 4517 leaves_play self
    if 4486 keyword_condition ge 1.0
    if 4487 keyword_condition ge 2.0
    if 4488 keyword_condition ge 3.0
    if 4489 keyword_condition ge 4.0
    if 4490 keyword_condition ge 5.0
    if 4486 keyword_condition
    if 4487 keyword_condition
    if 4488 keyword_condition
    if 4489 keyword_condition
    if 4490 keyword_condition
    do 4483 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4484 own give_keyword self amount=1.0
    do 4485 own give_keyword self amount=1.0
    do 4486 own revive unit mine lowest discard state is bronze;keyword is 756173
    do 4487 own stat_change unit mine all board position is same_row of self strength=1.0
    do 4488 own give_keyword position enemy position is opposite_row of self turns=2.0
    do 4518 uses_keyword damage unit all board position is same_row of self amount=1.0
    do 4489 own damage unit enemy lowest board amount=2.0
    do 4490 own copy self state is created
    do 4517 has_keyword obliterate self

## C2 lr_dq.md 1 (CAUSE, gone, 0 table lines from the same code)
Gwent's Syndicate cards are split into 3-card pseudo-factions by second faction ("Syndicate / Nilfgaard", "Syndicate / Monster", "Syndicate / Skellige", "Syndicate / Scoiatael"), so faction answers (kit, factions) show 3-card groups instead of one Syndicate, and 3 cards stand for a whole faction in 04, 11, 12, 13, 14.

## C3 lr_dq.md 2 (CAUSE, gone, 0 table lines from the same code)
forced_movement is tagged on any card that says move, seize, spawn beside, or put a card in the deck, not only on moving a unit against its owner's will; Gwent gets 92 cards and its answer in 13 is mostly not positional.

## C4 lr_dq.md 3 (CAUSE, gone, 0 table lines from the same code)
spell_power is tagged on every "boost/damage/increase by N" with a number, so Gwent's student orders, plain damage cards and Crone counters read as spell help; Northern Realms looks spell-centric in 10 though Gwent has no spells_played_condition card at all.

## C5 lr_dq.md 4 (CAUSE, gone, 0 table lines from the same code)
Gwent texts keep unfilled number slots, so answers show "[0]", "[1]", "[4]-provision" or "by 0" instead of the real value, and a designer cannot read the card.

## C6 lr_dq.md 5 (CAUSE, gone, 0 table lines from the same code)
cheat_death and revive are tagged on Gwent cards that spawn or create new cards, or only damage, not on a card that comes back after dying; so Gwent's death-and-return answers (12, 07) mix them in.

## C7 lr_dq.md 6 (CAUSE, gone, 0 table lines from the same code)
protection, disruption and heal are tagged on damage-dealing Skellige and Scoiatael cards, so staying power (07) and disruptive (08) lists show attackers.

