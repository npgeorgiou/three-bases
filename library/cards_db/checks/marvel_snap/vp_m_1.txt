## lr_misses.md 1 (MISSED CAUSE, open, 0 table lines from the same code)
Morbius grows per discard; Swarm returns after it is discarded (combo case cms02).
- W marvel_snap: Swarm -> Morbius: NONE | network.py []
  Swarm:
    when 3296 discarded self
    do 3296 own copy self amount=2.0
    do 3296 own cost_set it cost=0.0
  Morbius:
    when 3084 always
    if 3084 amount_product
    if 3084 amount_event_count
    do 3084 own stat_change self power=product

## lr_misses.md 2 (MISSED CAUSE, open, 0 table lines from the same code)
Morbius grows per discard; Apocalypse returns after it is discarded (combo case cms03).
- W marvel_snap: Apocalypse -> Morbius: NONE | network.py []
  Apocalypse:
    when 2748 discarded self
    do 2748 own return_card self
    do 2748 own stat_change self power=4.0
  Morbius:
    when 3084 always
    if 3084 amount_product
    if 3084 amount_event_count
    do 3084 own stat_change self power=product

## lr_misses.md 4 (MISSED CAUSE, open, 0 table lines from the same code)
White Tiger still places a card in the flooded location (combo case cms07).
- W marvel_snap: Storm -> White Tiger: NONE | network.py []
  Storm:
    when 3277 played self
    do 3277 own cant card all hand event=played
  White Tiger:
    when 3373 played self
    do 3373 own summon power=10.0

## lr_misses.md 5 (MISSED CAUSE, open, 0 table lines from the same code)
Doctor Doom still places cards in the flooded location (combo case cms08).
- W marvel_snap: Storm -> Doctor Doom: NONE | network.py []
  Storm:
    when 3277 played self
    do 3277 own cant card all hand event=played
  Doctor Doom:
    when 2849 played self
    do 2849 own summon power=5.0

## lr_misses.md 7 (MISSED CAUSE, open, 0 table lines from the same code)
Shuri doubles the next card's power (combo case cms11).
- W marvel_snap: Shuri -> Typhoid Mary: NONE | network.py []
  Shuri:
    when 3217 played unit mine position is same_lane
    if 3217 amount_stat power it
    do 3217 own stat_change unit mine it power=stat
  Typhoid Mary:
    when 3333 always
    do 3333 own stat_change unit mine all board position is same_lane;card not 8000671 power=-2.0

## lr_misses.md 8 (MISSED CAUSE, open, 0 table lines from the same code)
Shuri doubles the next card's power (combo case cms12).
- W marvel_snap: Shuri -> Red Skull: NONE | network.py []
  Shuri:
    when 3217 played unit mine position is same_lane
    if 3217 amount_stat power it
    do 3217 own stat_change unit mine it power=stat
  Red Skull:
    when 3168 always
    do 3168 own stat_change unit enemy all board position is same_lane power=2.0

## lr_misses.md 9 (MISSED CAUSE, open, 0 table lines from the same code)
Zero removes his drawback (combo case cms14).
- W marvel_snap: Zero -> Ebony Maw: NONE | network.py []
  Zero:
    when 3395 played unit mine
    do 3395 own silence unit mine it
  Ebony Maw:
    when 2859 always
    when 2860 always
    if 2859 event_count ge 4.0
    do 2859 own cant self event=played
    do 2860 own cant card mine all hand event=played

## lr_misses.md 11 (MISSED CAUSE, open, 0 table lines from the same code)
Taskmaster copies the last card's power (combo case cms17).
- W marvel_snap: Taskmaster -> Red Skull: NONE | network.py []
  Taskmaster:
    when 3302 played self
    if 3302 amount_stat power unit mine top board state is summoned_this_round
    do 3302 own stat_set self power=stat
  Red Skull:
    when 3168 always
    do 3168 own stat_change unit enemy all board position is same_lane power=2.0

## lr_misses.md 12 (MISSED CAUSE, open, 0 table lines from the same code)
Taskmaster copies the last card's power (combo case cms18).
- W marvel_snap: Taskmaster -> Typhoid Mary: NONE | network.py []
  Taskmaster:
    when 3302 played self
    if 3302 amount_stat power unit mine top board state is summoned_this_round
    do 3302 own stat_set self power=stat
  Typhoid Mary:
    when 3333 always
    do 3333 own stat_change unit mine all board position is same_lane;card not 8000671 power=-2.0

## lr_misses.md 13 (MISSED CAUSE, open, 0 table lines from the same code)
both take cards from the opponent's deck (combo case cms19).
- W marvel_snap: Cable -> Mantis: NONE | network.py []
  Cable:
    when 2793 played self
    do 2793 own draw card enemy deck_top amount=1.0
  Mantis:
    when 3049 played self
    if 3049 event_count ge 1.0
    do 3049 own copy unit enemy chosen board position is same_lane;state is summoned_this_round

## lr_misses.md 14 (MISSED CAUSE, open, 0 table lines from the same code)
the deck is built around the two (combo case cms23).
- W marvel_snap: Wave -> Death: NONE | network.py []
  Wave:
    when 3365 played self
    do 3365 own cost_change card all max=4.0
  Death:
    when 2831 always
    if 2831 amount_event_count
    if 2831 amount_minus
    do 2831 own cost_change self cost=minus

## lr_misses.md 15 (MISSED CAUSE, open, 0 table lines from the same code)
Collector buffs cards, Moon Girl copies them (combo case cms24).
- W marvel_snap: The Collector -> Moon Girl: NONE | network.py []
  The Collector:
    when 3314 created card mine
    do 3314 own stat_change self power=1.0
  Moon Girl:
    when 3080 played self
    do 3080 own copy card mine all hand

## lr_misses.md 17 (MISSED CAUSE, open, 0 table lines from the same code)
a real-world combo of the library (realworld.py).
- W marvel_snap: Professor X -> Devil Dinosaur: NONE | network.py []
  Professor X:
    when 3138 always
    do 3138 own cant card all hand event=played
    do 3138 own cant card all event=summoned
    do 3138 own cant unit all board position is same_lane event=dies
  Devil Dinosaur:
    when 2836 always
    if 2836 amount_product
    if 2836 amount_count card mine all hand
    do 2836 own stat_change self power=product

## lr_misses.md 18 (MISSED CAUSE, open, 0 table lines from the same code)
Absorbing Man repeats the On Reveal of the unit played before him, so On Reveal cards are his partners, but only Wong and Odin (repeaters) have lines to him (L15, L10 enables).
- W marvel_snap: Brood -> Absorbing Man: NONE | network.py []
- W marvel_snap: Silver Surfer -> Absorbing Man: NONE | network.py []
- W marvel_snap: Hazmat -> Absorbing Man: NONE | network.py []
- W marvel_snap: Magik -> Absorbing Man: NONE | network.py []
- R marvel_snap: Wong -> Absorbing Man: plays it again | network.py [2314]
  Brood:
    when 2789 played self
    if 2789 amount_stat power self
    do 2789 own summon amount=2.0;power=stat
  Absorbing Man:
    when 2725 played self
    if 2725 last_card unit mine keyword is 8000750
    do 2725 own repeat unit mine it board
  Silver Surfer:
    when 3221 played self
    do 3221 own stat_change unit mine all board card not 8000536;cost eq 3449 power=2.0
  Hazmat:
    when 2928 played self
    do 2928 own stat_change unit all board card not 8000234 power=-1.0
  Magik:
    when 3039 played self
    if 3039 amount le 5.0
    if 3039 amount_event_count
    do 3039 own set_terrain position position is same_lane

## lr_misses.md 19 (MISSED CAUSE, open, 0 table lines from the same code)
Absorbing Man repeats the On Reveal of the last unit played (his text reads that unit's On Reveal, like Astral Projection and Joaquin Torres Falcon II do for their lines, L10 triggers/makes it go off again), yet he has no line to any On Reveal unit in his deck.
- W marvel_snap: Absorbing Man -> Black Panther: NONE | network.py []
- W marvel_snap: Absorbing Man -> Luna Snow: NONE | network.py []
- W marvel_snap: Absorbing Man -> Arnim Zola: NONE | network.py []
- W marvel_snap: Absorbing Man -> Peni Parker: NONE | network.py []
  Absorbing Man:
    when 2725 played self
    if 2725 last_card unit mine keyword is 8000750
    do 2725 own repeat unit mine it board
  Black Panther:
    when 2779 played self
    if 2779 amount_stat power self
    do 2779 own stat_change self power=stat
  Luna Snow:
    when 3033 played self
    do 3033 own summon
  Arnim Zola:
    when 2757 played self
    do 2757 own kill unit mine chosen board position is same_lane;card not 8000034
    do 2757 own copy unit mine it card not 8000034
  Peni Parker:
    when 3127 played self
    when 3128 merged
    do 3127 own create
    do 3128 own mana_gain mana mine amount=1.0

## lr_misses.md 3 (MISSED CAUSE, gone, 0 table lines from the same code)
Wong doubles Odin's On Reveal (combo case cms04).
- W marvel_snap: Wong -> Odin: plays it again | network.py [2314]

## lr_misses.md 6 (MISSED CAUSE, gone, 0 table lines from the same code)
the doubled hand boosts Devil Dinosaur (combo case cms10).
- W marvel_snap: Moon Girl -> Devil Dinosaur: fills your hand | network.py [2031]

## lr_misses.md 10 (MISSED CAUSE, gone, 0 table lines from the same code)
Sauron removes his drawback (combo case cms16).
- W marvel_snap: Sauron -> Ebony Maw: silence | network.py [1396]

## lr_misses.md 16 (MISSED CAUSE, gone, 0 table lines from the same code)
wong makes these cards' effects happen again (deck case dms03, The Wong Spectrum: Wong doubles Spectrum's On Reveal).
- W marvel_snap: Wong -> Spectrum: plays it again | network.py [2314]

