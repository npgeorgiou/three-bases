## C1 lr_d2.md 2 (CAUSE, open, 7896 table lines from the same code)
more power from the board is said to help a card that doubles its power only when it is played, but a buff on a unit already in play comes after the doubling and does not do the very thing needed (L4, L18); only a buff reaching the card before it is played or at the same moment (hand, deck, a card played with it) helps.
- W runeterra: Eye Of The Storm -> Dashing Dandy: can give it more power | network.py [1465]
- W runeterra: Arena Mechacaster -> Dashing Dandy: can give it more power | network.py [1465]
- W runeterra: Yordles in Arms -> Dashing Dandy: can give it more power and health | network.py [1465]
- R runeterra: Avarosan Hearthguard -> Earthshaker: gives it more power and health | network.py [1464]
- R runeterra: Arena Mechacaster -> Earthshaker: can give it more power | network.py [1465]
  Eye Of The Storm:
    when 5861 played self
    do 5861 own stat_change unit mine chosen board power=2.0
    do 5861 own draw card mine deck_top amount=2.0
  Dashing Dandy:
    when 5687 played self
    when 7086 strikes
    if 5687 keyword_condition
    if 5687 amount_stat power self
    if event_count ge 1.0
    if 5687 event_count ge 1.0
    do 5687 own stat_change self power=stat
    do 7086 has_keyword excess_damage player enemy
  Arena Mechacaster:
    when 5043 attacks
    do 5043 own stat_change unit mine all board state is attacking;card not 751343 power=2.0
  Yordles in Arms:
    when 5130 played self
    when 5131 played self
    if 5130 amount lt 4.0
    if 5130 amount_distinct region
    if 5131 amount ge 4.0
    if 5131 amount_distinct region
    do 5130 own stat_change unit mine all board power=2.0;health=2.0
    do 5131 own stat_change unit mine all board power=3.0;health=3.0

## C2 lr_d3.md 3 (CAUSE, open, 702 table lines from the same code)
a card whose limit stops cards being played (Goose, Jean Grey) is linked to a card that summons, as if the limit were a need; a drawback is no need and the summoner does not use it (L5, L19).
- W marvel_snap: Goose -> Anti-Polar Magneto: stops cards being played, but a summon is not played: it still fills the place | network.py [2539]
- W marvel_snap: Jean Grey -> Ultron: stops cards being played, but a summon is not played: it still fills the place | network.py [2539]
- W marvel_snap: Invisible Woman & Namor Doomsday -> Uncle Ben: stops cards being played, but a summon is not played: it still fills the place | network.py [2539]
  Goose:
    when 2918 always
    do 2918 own cant card all hand cost ge 3117 event=played
  Anti-Polar Magneto:
    when 2746 played self
    do 2746 own summon card mine chosen hand cost in 3;cost in 4
  Jean Grey:
    when 2974 always
    if 2974 event_count eq 0.0
    do 2974 own cant card all hand event=played
  Ultron:
    when 3336 played self
    do 3336 own summon power=2.0;amount=4.0
  Invisible Woman & Namor Doomsday:
    when 2960 always
    when 2961 always
    if 2960 have is self position is front_row
    if 2960 event_count ge 2.0
    if 2961 have is self position is back_row
    if 2961 amount_count position mine position is same_lane of unit mine highest_cost board;of:kind is unit
    if 2961 amount_product
    do 2960 own cant card enemy all hand event=played
    do 2961 own stat_change self power=product
  Uncle Ben:
    when 3343 dies self
    do 3343 own summon

## C3 lr_d3.md 5 (CAUSE, open, 310 table lines from the same code)
an effect that stops the ENEMY's hand playing cards is said as "fills your hand" for a card that counts my hand (L9).
- W marvel_snap: Invisible Woman & Namor Doomsday -> Red Wolf Fractured Frontier: fills your hand | network.py [2102]
  Invisible Woman & Namor Doomsday:
    when 2960 always
    when 2961 always
    if 2960 have is self position is front_row
    if 2960 event_count ge 2.0
    if 2961 have is self position is back_row
    if 2961 amount_count position mine position is same_lane of unit mine highest_cost board;of:kind is unit
    if 2961 amount_product
    do 2960 own cant card enemy all hand event=played
    do 2961 own stat_change self power=product
  Red Wolf Fractured Frontier:
    when 3169 played self
    when 3170 played self
    if 3169 amount_count card mine all hand
    if 3170 keyword_condition
    if event_count ge 1.0
    if 3170 event_count ge 1.0
    do 3169 own stat_change self power=count
    do 3170 own stat_change card mine all hand power=1.0

## C4 lr_d3.md 4 (CAUSE, open, 279 table lines from the same code)
a power boost aimed at chosen "created" units (or one named card) is linked to a card that is not that kind (Deadpool is not a created unit), so its help does not reach it (L14).
- W marvel_snap: Zombie Mister Fantastic -> Deadpool: can give it more power | network.py [1465]
- R marvel_snap: Sam Wilson & Nightcrawler Doomsday -> Deadpool: can give it more power (when in front of it) | network.py [1465]
  Zombie Mister Fantastic:
    when 3402 played self
    when 3403 activated self
    do 3402 own stat_change card mine card is 8000742 power=2.0
    do 3403 own stat_change unit mine chosen state is created power=1.0
  Deadpool:
    when 2829 dies self
    if 2829 amount_stat power self
    do 2829 own return_to_hand self
    do 2829 own stat_change self power=stat

## C5 lr_d3.md 2 (CAUSE, open, 16 table lines from the same code)
a card that creates or summons a random unit (no Ongoing or On Reveal named) is linked to a card that needs a unit with Ongoing or On Reveal; a random unit is not made by that description, and a summon is not played (L17, L19, L20).
- W marvel_snap: Sub-Mariner -> Mystique: makes a unit with Ongoing it counts or asks for | network.py [1882]
- W marvel_snap: Shanna -> Mystique: makes a unit with Ongoing it counts or asks for | network.py [1882]
- W marvel_snap: Mister Fantastic & Beast Doomsday -> Absorbing Man: makes a unit with On Reveal it counts or asks for | network.py [1882]
- W marvel_snap: Sub-Mariner -> Absorbing Man: makes a unit with On Reveal it counts or asks for | network.py [1882]
- R marvel_snap: Viper -> Absorbing Man: is a unit with On Reveal it counts or asks for | network.py [1880]
  Sub-Mariner:
    when 3283 stat_changed self
    if 3283 it_matches state is buffed
    if 3283 amount_event_amount
    do 3283 own create unit random cost eq 3521
    do 3283 own stat_change unit it power=event_amount
  Mystique:
    when 3100 played self
    if 3100 last_card unit mine keyword is 8000751
    do 3100 own copy_text self
  Shanna:
    when 3214 played self
    do 3214 own summon unit random cost eq 3440
  Mister Fantastic & Beast Doomsday:
    when 3090 played self
    when 3091 always
    if 3090 it_matches self position is front_of_lane
    if 3091 it_matches self position is back_of_lane
    if 3091 amount_count unit mine all board state is created
    do 3090 own create unit mine random
    do 3090 own stat_change unit mine it power=3.0
    do 3091 own stat_change self power=count
  Absorbing Man:
    when 2725 played self
    if 2725 last_card unit mine keyword is 8000750
    do 2725 own repeat unit mine it board

## C6 lr_d1.md 2 (MISSED CAUSE, open, 0 table lines from the same code)
a card that sets or raises a unit's stats makes it "buffed", which Out Of The Way waits for, so the stat change helps it (L14: anything a card waits for counts).
- W runeterra: Snowy Razorclaw -> Out Of The Way: NONE | network.py []
- W runeterra: Zed (level 2) -> Out Of The Way: NONE | network.py []
  Snowy Razorclaw:
    when 5793 played self
    when 7086 strikes
    if 5793 keyword_condition
    if 5793 amount_stat power self
    if 5793 amount_stat health self
    if event_count ge 1.0
    if 5793 event_count ge 1.0
    do 5793 own stat_set unit mine chosen board power=stat;health=stat
    do 7086 has_keyword excess_damage player enemy
  Out Of The Way:
    when 4630 played self
    do 4630 own can unit mine all state is buffed;keyword not 750410
    do 4630 own draw card mine deck_top amount=1.0
  Zed (level 2):
    when 6056 attacks
    when 7119 attacks
    if 6056 amount_stat power self
    if 6056 amount_stat health self
    do 6056 own summon
    do 6056 own start_attack unit mine it card is 900023
    do 6056 own stat_set unit mine it card is 900023 power=stat;health=stat
    do 6056 own copy_keywords unit mine it card is 900023
    do 7119 has_keyword first_strike self

## C7 lr_d2.md 1 (MISSED CAUSE, open, 0 table lines from the same code)
a spell that gives a unit an ability whose own effect is a keyword the other card reacts to (Grow, +8|+8 each turn) was dropped together with the wrong lines of its group; the other card's text waits for that keyword on my units (L10, L14).
- W duelyst: Gargantuan Growth -> Oropsisaur: NONE | network.py []
  Gargantuan Growth:
    when 435 played self
    when 436 turn_start
    do 435 own give_ability unit chosen board
    do 436 gives stat_change self power=8.0;health=8.0
  Oropsisaur:
    when 431 turn_start
    when 432 survives_damage unit mine keyword is 741534;card not 5000479
    do 431 own stat_change self power=1.0;health=1.0
    do 432 own grow unit mine it card not 5000479

## C8 lr_d1.md 1 (MISSED CAUSE, gone, 0 table lines from the same code)
a card that forces enemy units to block (challenge) feeds a card that damages blocking enemy units; the fix removed these lines, but the force makes the blockers the damage needs (L10 "enables", L24-style need that the text waits for).
- W runeterra: Silverwing Vanguard -> Molten Shield: makes enemy units block: Molten Shield damages them | network.py [675]
- W runeterra: Mageseeker Inquisitor -> Short Fuse: makes enemy units block: Short Fuse damages them | network.py []
- W runeterra: Savage Reckoner -> Molten Shield: makes enemy units block: Molten Shield damages them | network.py []

## C9 lr_d3.md 1 (MISSED CAUSE, gone, 0 table lines from the same code)
a return to hand of a card with a good On Reveal (it is played again) lost its line when the fix cut the lines for returns of drawback On Reveals (donate self); the good one was cut too (L14: a return to hand of a card with Play is kept).
- W marvel_snap: Beast -> Absorbing Man: is a unit with On Reveal it counts or asks for | network.py [1473, 1880] | cases n424 line

