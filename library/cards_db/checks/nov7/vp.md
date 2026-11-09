## C1 lr_6.md 4 (CAUSE, open, 3475 table lines from the same code)
A card that gives all my units more power and health is said as "changes your units' stats" when the receiver levels or transforms on a power threshold; it must be said "helps it level up: more power and health" (L18 families, L24, L10).
- W runeterra: Kayle (level 2) -> Xolaani the Bloodweaver: changes its stats for its effect | network.py [736, 1600]
  Kayle (level 2):
    when 9312 always
    when 9313 summoned self
    when 9314 levels_up self
    when 9315 always
    when 10178 attacks
    when 10191 attacks
    when 10158 strikes
    if 9312 amount_event_count
    if 9315 keyword_condition 16.0
    if stat power ge listed self
    if 9315 stat power ge listed self
    do 9312 own stat_change self power=event_count
    do 9313 own stat_change unit mine all board power=1.0;health=1.0
    do 9314 own stat_change unit mine all board power=1.0;health=1.0
    do 9315 own give_keyword self
    do 10178 uses_keyword double_strike self
    do 10191 has_keyword first_strike self
    do 10158 has_keyword excess_damage player enemy
  Xolaani the Bloodweaver:
    when 8530 always
    when 8531 always
    when 10158 strikes
    if 8530 amount_event_count
    if 8530 amount_double
    if 8530 amount_event_count
    if 8530 amount_double
    if 8531 keyword_condition 16.0
    if stat power ge listed self
    if 8531 stat power ge listed self
    do 8530 own stat_change self power=double;health=double
    do 8531 own transform self
    do 10158 has_keyword excess_damage player enemy

## C2 lr_14.md 3 (CAUSE, open, 174 table lines from the same code)
A unit that moves or swaps itself, or is only let move or ready again, was read as moving units; a unit moving itself gives no line to place needs (L23, L29).
- W duelyst: Hearth-Sister -> Crystallize: Hearth-Sister moves enemy units, and Crystallize acts on units around it | network.py []
- W duelyst: Hearth-Sister -> Lightbender: Hearth-Sister moves units, and Lightbender acts on units around it | network.py []
- W duelyst: Assassination Protocol -> Frostbone Naga: Assassination Protocol moves your units, and Frostbone Naga acts on units around it | network.py []
- W faeria: Celestial Tower -> Rakoakopter: Celestial Tower moves enemy units, and Rakoakopter acts on units next to it; also moves into place: moves my units or land forward: it can enter where it needs  | network.py [2407]
- R duelyst: Juxtaposition -> Ephemeral Shroud: Juxtaposition moves enemy units, and Ephemeral Shroud acts on units around it | network.py []
- R into_the_breach: Artemis Artillery -> Fire Beam: Artemis Artillery moves units, and Fire Beam acts on units in a line from it | network.py []
  Hearth-Sister:
    when 249 played self
    do 249 own swap self
  Crystallize:
    when 259 played self
    when 1086 always
    do 259 own give_keyword unit enemy chosen board position is surrounding
    do 1086 uses_keyword cant unit enemy chosen board position is surrounding event=moves
    do 1086 uses_keyword cant unit enemy chosen board position is surrounding event=attacks
  Lightbender:
    when 288 played self
    do 288 own silence position all position is surrounding
  Assassination Protocol:
    when 974 played self
    do 974 own ready unit mine chosen board
    do 974 own cant unit mine it event=attacks
  Frostbone Naga:
    when 307 played self
    do 307 own damage any all board position is surrounding amount=2.0
  Celestial Tower:
    when 1367 activated
    when 1756 always
    do 1367 own give_keyword unit chosen board amount=3.0
    do 1756 uses_keyword can unit chosen board event=moves
    do 1367 own damage self amount=1.0
  Rakoakopter:
    when 1580 always
    when 1755 always
    when 1759 played self
    when 1581 played self
    when 1755 always
    when 1759 played self
    if 1759 amount_event_amount
    if 1759 amount_event_amount
    do 1580 own give_keyword self
    do 1755 uses_keyword can self event=moves
    do 1580 own give_keyword self amount=1.0
    do 1759 uses_keyword move self amount=event_amount
    do 1581 own damage unit enemy all board position is bordering amount=2.0
    do 1755 has_keyword can self event=moves
    do 1759 has_keyword move self amount=event_amount

## C3 lr_14.md 1 (CAUSE, open, 66 table lines from the same code)
A summon, revive or copy whose rows name no place was read as "puts your units there"; only a card whose rows put units at a named place (here, same lane, near) is a placer (L29, L2).
- W duelyst: Conscript -> Dauntless Advance: Conscript puts your units there, and Dauntless Advance acts on units around your leader or base | network.py []
- W duelyst: Pandora -> Sandswirl Reader: Pandora puts your units there, and Sandswirl Reader acts on units around it | network.py []
- W gwent: Arachas Nest -> Kikimore Queen: Arachas Nest puts your units there, and Kikimore Queen acts on units in its row; also triggers: is an Organic whose playing sets off its effect | network.py [1933]
- W marvel_snap: Shanna -> Ant Man: Shanna puts your units there, and Ant Man acts on units in its lane | network.py []
- R marvel_snap: Adamantium Infusion -> Fastball Special: Adamantium Infusion puts your units there, and Fastball Special acts on units in its lane | network.py []
- R marvel_snap: Adamantium Infusion -> Symbiote Spider-Man: Adamantium Infusion puts your units there, and Symbiote Spider-Man acts on units in its lane | network.py []
  Conscript:
    when 58 played self
    do 58 own summon power=1.0;health=2.0
  Dauntless Advance:
    when 959 played self
    when 960 always
    when 961 always
    do 959 own give_ability player mine
    do 960 gives negate_damage self
    do 959 own give_ability unit mine all board position is surrounding of player mine;of:kind is player
    do 961 gives negate_damage self
  Pandora:
    when 326 turn_end
    do 326 own summon power=3.0;health=3.0
    do 326 own give_random_keyword unit mine it card is -1001
  Sandswirl Reader:
    when 518 played self
    do 518 own return_to_hand unit chosen board position is surrounding
    do 518 own set_terrain position position is same_space of it
  Arachas Nest:
    when 2025 played self
    do 2025 own summon amount=4.0
  Kikimore Queen:
    when 3058 always
    when 4540 played unit mine strength gt 4192
    when 3059 keyword_used
    when 3060 played card mine type is 28
    when 4540 played unit mine strength gt 4192
    if 4540 amount_listed
    if 3059 keyword_condition
    if 4540 amount_listed
    if 3059 keyword_condition
    do 3058 own give_keyword self
    do 4540 uses_keyword stat_change self strength=listed
    do 3059 own stat_change unit mine all board type is 53;position is same_row of self strength=1.0
    do 3060 own repeat self
    do 4540 has_keyword stat_change self strength=listed
  Shanna:
    when 6286 played self
    do 6286 own summon unit random cost eq 6127
  Ant Man:
    when 5817 always
    if 5817 count ge 4.0 unit mine board position is same_lane
    do 5817 own stat_change self power=4.0

## C4 lr_1.md 1 (CAUSE, open, 0 table lines from the same code)
A Gwent Summon is not a play, so it sets off no "Deploy" of the summoned unit (L27, n698), and the line "puts it into play: its summon effect goes off" is wrong where the target has only a Deploy.
- W gwent: Vilgefortz -> Xarthisius: NONE | network.py []
- W gwent: Ihuarraquax -> Troll Porter: NONE | network.py []
- W gwent: Sove -> Seagull: puts it into play from the deck | network.py []
- W gwent: Sove -> Little Havfrue: puts it into play from the deck | network.py []
- R gwent: Arachas Nest -> Kikimore Queen: Arachas Nest puts your units there, and Kikimore Queen acts on units in its row; also triggers: is an Organic whose playing sets off its effect | network.py [1933]
  Sove:
    when 4023 played self
    when 4024 dies self
    when 4537 always
    if 4023 keyword_condition
    if 4023 amount_count unit enemy all board state is damaged
    if 4024 amount_product
    if 4024 amount_stat base_power self
    if 4023 have is self position is front_row
    do 4023 own summon card mine chosen deck type is 43
    do 4023 own give_ability card mine it type is 43
    do 4024 gives stat_change unit enemy board card is 757381 strength=product
    do 4023 own damage card mine it type is 43 amount=count
    do 4023 own give_keyword self
    do 4537 uses_keyword cant player all event=targeted
  Seagull:
    when 3860 played self
    when 3861 dies unit enemy
    when 4517 leaves_play self
    if 3861 have self discard
    do 3860 own damage unit chosen board amount=1.0
    do 3860 own create card mine
    do 3861 own summon self
    do 3861 own give_keyword self
    do 4517 uses_keyword obliterate self
  Little Havfrue:
    when 3789 played self
    when 3790 activated self
    when 4522 turn_start
    when 4504 played self
    if 3789 keyword_condition
    if 3789 have is unit mine board state is copy_of_it
    do 3789 own base_change self strength=2.0
    do 3790 own damage self amount=4.0
    do 3790 own give_keyword position enemy chosen turns=2.0
    do 4522 uses_keyword damage unit random board position is same_row of self amount=1.0
    do 4504 has_keyword cant self event=activated;turns=1.0

## C5 lr_1.md 3 (CAUSE, open, 0 table lines from the same code)
"Gives it units to kill" is said for cards that only play, copy or hit once and supply no kills (L11, L4).
- W gwent: Madoc -> Milva: Sharpshooter: NONE | network.py []
- W gwent: Queen Adalia -> Kaedweni Revenant: NONE | network.py []
- W gwent: The Naglfar -> Dettlaff van der Eretein: plays it: its effect goes off | network.py []
  The Naglfar:
    when 2409 played self
    do 2409 own look card mine random deck state is gold
    do 2409 own play_card card mine chosen deck state is gold
    do 2409 own put_on_top card mine chosen deck state is gold
  Dettlaff van der Eretein:
    when 3651 played self
    when 4556 turn_start
    when 4526 turn_end
    when 3652 activated self
    when 3653 killed
    when 3654 always
    when 4511 activated self
    when 4504 played self
    if 3651 amount_sum
    if 3651 amount_count unit all board position is sides of self;type is 35
    if 4511 amount_listed
    do 3651 own give_keyword position enemy chosen amount=sum
    do 4556 uses_keyword give_keyword unit random board position is same_row of self;keyword not 756169 amount=2.0
    do 4526 uses_keyword damage unit random board position is same_row of self;keyword not 756169 amount=1.0
    do 4556 uses_keyword damage unit random board position is same_row of self;keyword is 756169 amount=2.0
    do 3652 own damage unit enemy chosen board keyword is 756169 amount=1.0
    do 3653 own summon
    do 3654 own keyword_action amount=1.0
    do 4511 uses_keyword cant event=activated;turns=listed
    do 4504 has_keyword cant self event=activated;turns=1.0

## C6 lr_1.md 5 (CAUSE, open, 0 table lines from the same code)
Berengar dies unless a Witcher is in his row: that is a drawback, not a need (L5); and Keldar's summon has no Witcher kind in its rows, so "is a Witcher it asks for" is not shown.
- W gwent: Keldar -> Berengar: is a Witcher it asks for; also Keldar puts your units there, and Berengar acts on units in its row | network.py []
- W gwent: Keldar -> Target Practice: is a Witcher it asks for; also Keldar puts your units there, and Target Practice acts on units in a card it picks's row | network.py []
  Keldar:
    when 3557 played spell mine
    when 3558 turn_end
    if 3558 keyword_condition 4.0
    if count le listed card mine hand
    if 3558 count le listed card mine hand
    do 3557 own summon
    do 3558 own summon
  Berengar:
    when 3485 turn_start
    if 3485 have not unit mine all board type is 34;position is same_row of self;card not 757163
    do 3485 own kill self
  Target Practice:
    when 3569 played self
    when 3570 played self
    if 3569 have not unit mine all board type is 34;position is same_row of unit mine chosen board;of:kind is unit
    if 3570 have unit mine all board type is 34;position is same_row of unit mine chosen board;of:kind is unit
    do 3569 own stat_change unit mine chosen board strength=4.0
    do 3570 own stat_change unit mine chosen board strength=4.0
    do 3570 own summon

## C7 lr_10.md 1 (CAUSE, open, 0 table lines from the same code)
A move of a card between zones (a tutor, or moving a card in hand or deck) was read as moving a unit on the board, so the card got a "moves it" line to a card that cares about its place (L29, L1b).
- W gwent: Blightmaker -> Fisher King: Blightmaker moves Fisher King, and Fisher King acts on units in the back row | network.py []
- W gwent: Doadrick Leumaerts -> Fisher King: Doadrick Leumaerts moves Fisher King, and Fisher King acts on units in the back row | network.py []
- W gwent: Cursed Scroll -> Lyrian Landsknecht: Cursed Scroll moves Lyrian Landsknecht, and Lyrian Landsknecht acts on units in the back row or in the front row | network.py []
- W gwent: Myrgtabrakke -> Samum: Myrgtabrakke moves your units, and Samum acts on units next to its target | network.py []
- R gwent: Wild Hunt Bruiser -> Imlerith's Wrath: Wild Hunt Bruiser moves enemy units, and Imlerith's Wrath acts on units in a space it picks's row or not in a space it picks's row | network.py []
- R into_the_breach: Attraction Pulse -> Titan Fist: Attraction Pulse moves enemy units, and Titan Fist acts on units next to it | network.py [736]
  Blightmaker:
    when 3669 played self
    do 3669 own move card mine chosen deck
    do 3669 own summon card mine it type is 37
    do 3669 own create
    do 3669 own play_card card mine chosen hand card is 813588
  Fisher King:
    when 2663 played self
    if 2663 keyword_condition
    if 2663 have is self position is back_row
    do 2663 own move card mine chosen deck
  Doadrick Leumaerts:
    when 2883 played self
    when 4510 played self
    when 2884 activated self
    when 2885 always
    when 4511 activated self
    if 2883 have is unit mine all board type is 47
    if 2884 keyword_condition
    if 4511 amount_listed
    if 2884 have is self position is back_row
    do 2883 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2884 own draw card mine deck_top amount=1.0
    do 2884 own move card mine chosen hand
    do 2885 own keyword_action amount=1.0
    do 4511 uses_keyword cant event=activated;turns=listed
  Cursed Scroll:
    when 3156 activated self
    when 4504 played self
    do 3156 own draw card mine chosen deck amount=1.0
    do 3156 own move card mine chosen hand
    do 4504 has_keyword cant self event=activated;turns=1.0
  Lyrian Landsknecht:
    when 2635 always
    when 4524 played self
    when 4510 played self
    when 4525 played self
    when 2636 activated self
    when 2637 activated self
    when 4524 played self
    when 4510 played self
    when 4525 played self
    when 4504 played self
    if 4524 have is self position is front_row
    if 4525 have is self position is back_row
    if 2636 keyword_condition not
    if 2637 keyword_condition
    if 4524 have is self position is front_row
    if 4525 have is self position is back_row
    if stat strength gt stat self
    if 2636 stat strength gt stat self
    if 2637 stat strength gt stat self
    do 2635 own give_keyword self
    do 4524 uses_keyword give_keyword self
    do 4510 uses_keyword can self event=activated
    do 4525 uses_keyword stat_change self strength=1.0
    do 2636 own damage unit chosen board amount=1.0
    do 2637 own damage unit chosen board amount=3.0
    do 4524 has_keyword give_keyword self
    do 4510 uses_keyword can self event=activated
    do 4525 has_keyword stat_change self strength=1.0
    do 4504 has_keyword cant self event=activated;turns=1.0
  Myrgtabrakke:
    when 1801 always
    when 4507 game_start
    when 1802 played self
    when 1803 activated self
    when 1804 always
    when 4513 always
    when 1805 game_start
    when 4513 always
    when 4507 game_start
    when 4513 always
    when 4504 played self
    if 4507 amount_count card mine type is 38;state is started_in_deck
    if 4513 amount_listed
    if 1805 amount_count card mine all deck type is 38;state is started_in_deck
    if 4513 amount_listed
    if 4507 amount_count card mine type is 38;state is started_in_deck
    if 4513 amount_listed
    do 1801 own give_keyword self
    do 4507 uses_keyword stat_change self strength=count
    do 1802 own draw card mine deck type is 38 amount=1.0
    do 1802 own move card mine chosen hand
    do 1803 own damage unit enemy chosen board amount=1.0
    do 1804 own give_keyword self amount=0.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 1805 own give_keyword self amount=count
    do 4513 uses_keyword can self event=activated;times=listed
    do 4507 has_keyword stat_change self strength=count
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Samum:
    when 2683 played self
    when 2684 killed
    do 2683 own damage unit chosen board amount=3.0
    do 2684 own move unit all board position is sides of it

## C8 lr_10.md 2 (CAUSE, open, 0 table lines from the same code)
A line to a card whose rows hold no place need (no "surrounding", "bordering", "row", "lane": it only attacks itself or has no position test) cannot be a line "acts on units around it" (L29, L2).
- W duelyst: Inquisitor Kron -> Lavaslasher: Inquisitor Kron puts your units there, and Lavaslasher acts on units around it | network.py [736]
- W duelyst: Progenitor -> Lavaslasher: Progenitor puts your units there, and Lavaslasher acts on units around it | network.py []
- W faeria: Battle Toads -> Animated Banquet: Battle Toads moves your units, and Animated Banquet acts on units next to it | network.py [736]
- R duelyst: Jax Truesight -> Arclyte Sentinel: Jax Truesight puts your units there, and Arclyte Sentinel acts on units around it | network.py []
- R duelyst: Conscript -> Empyreal Congregation: Conscript puts your units there, and Empyreal Congregation acts on units in a 2x2 area | network.py []
  Inquisitor Kron:
    when 896 shuffled card mine
    when 1098 always
    do 896 own summon power=2.0;health=2.0
    do 896 own give_random_keyword unit mine it card is 5000940
    do 1098 has_keyword cant any enemy all board position is surrounding of self event=moves
    do 1098 has_keyword cant any enemy all board position is surrounding of self event=attacks
  Lavaslasher:
    when 919 played self
    do 919 own start_attack self
  Progenitor:
    when 1014 played self
    do 1014 own summon unit mine all board name_has not 3;card not 5001054
  Battle Toads:
    when 1215 played self
    when 1757 always
    do 1215 own summon amount=2.0;power=2.0;health=2.0
    do 1215 own give_keyword unit mine it card is -2003
    do 1757 uses_keyword can unit mine it card is -2003 event=moves
  Animated Banquet:
    when 1638 always
    when 1759 played self
    when 1639 turn_end
    when 1759 played self
    if 1759 amount_event_amount
    if 1759 amount_event_amount
    do 1638 own give_keyword self amount=1.0
    do 1759 uses_keyword move self amount=event_amount
    do 1639 own capture self
    do 1639 own stat_change it power=1.0;health=1.0
    do 1759 has_keyword move self amount=event_amount

## C9 lr_10.md 3 (CAUSE, open, 0 table lines from the same code)
A card that only destroys, copies (no place shown) or takes control of a unit was read as "puts or moves your units there"; no position changes (L29; L9 for enemy units).
- W marvel_snap: Arnim Zola -> Symbiote Spider-Man: Arnim Zola puts your units there, and Symbiote Spider-Man acts on units in its lane | network.py []
- W marvel_snap: Arnim Zola -> Iron Man: Arnim Zola puts your units there, and Iron Man acts on units in its lane | network.py []
- W duelyst: Mindlathe -> Primus Fist: Mindlathe moves your units, and Primus Fist acts on units around it | network.py []
- R marvel_snap: Grapple Arrow -> Symbiote Spider-Man: Grapple Arrow moves your units, and Symbiote Spider-Man acts on units in its lane | network.py []
- R stormbound: Petrified Fossils -> Wild Saberpaws: Petrified Fossils moves Wild Saberpaws and your units, and Wild Saberpaws acts on units around it or next to it | network.py [736, 1610]
  Arnim Zola:
    when 5829 played self
    do 5829 own kill unit mine chosen board position is same_lane;card not 8000034
    do 5829 own copy unit mine it card not 8000034
  Symbiote Spider-Man:
    when 6371 activated self
    do 6371 own merge unit mine lowest board position is same_lane
    do 6371 own repeat unit mine it
  Iron Man:
    when 6037 always
    if 6037 amount_stat power position mine position is same_lane
    do 6037 own stat_change position mine position is same_lane power=stat
  Mindlathe:
    when 531 damaged unit
    do 531 own ready unit it
    do 531 own steal unit it
  Primus Fist:
    when 304 played self
    do 304 own stat_change unit mine chosen board position is surrounding power=2.0

## C10 lr_10.md 4 (CAUSE, open, 0 table lines from the same code)
Putting more of my units into the area of a card that hurts every unit there (or kills itself when the lane fills) is a drawback, no line (L29 drawback, L5).
- W marvel_snap: Arnim Zola -> Ice Cube: Arnim Zola puts your units there, and Ice Cube acts on units in its lane | network.py []
- W gwent: Poor Fucking Infantry -> Sabrina Glevissig: Poor Fucking Infantry puts your units there, and Sabrina Glevissig acts on units in its row | network.py []
- W duelyst: Grimes -> Riftwalker: Grimes puts your units there, and Riftwalker acts on units around it | network.py []
  Arnim Zola:
    when 5829 played self
    do 5829 own kill unit mine chosen board position is same_lane;card not 8000034
    do 5829 own copy unit mine it card not 8000034
  Ice Cube:
    when 6024 round_start
    when 6025 round_start
    if 6025 count ge 4.0 unit mine board position is same_lane
    do 6024 own mana_gain mana mine amount=1.0
    do 6025 own kill self
  Poor Fucking Infantry:
    when 2396 played self
    when 2397 played self
    if 2397 keyword_condition
    if have is unit mine board state is copy_of_it
    if 2397 have is unit mine board state is copy_of_it
    do 2396 own summon
    do 2396 own summon
    do 2397 own stat_change self strength=3.0
  Sabrina Glevissig:
    when 1891 always
    when 4527 always
    when 4528 played self
    when 4569 always
    when 1892 dies self
    when 4577 always
    when 4527 always
    when 4528 played self
    when 4569 always
    when 4578 dies self
    when 4527 always
    when 4528 played self
    when 4569 always
    do 1891 own give_keyword self
    do 4527 uses_keyword can self event=summoned
    do 4528 uses_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
    do 1892 own damage unit all board position is same_row of self amount=3.0
    do 4577 own give_keyword self
    do 4527 uses_keyword can self event=summoned
    do 4528 uses_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
    do 4578 own damage unit all board position is same_row amount=3.0
    do 4527 has_keyword can self event=summoned
    do 4528 has_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
  Grimes:
    when 936 played self
    when 937 dies self
    do 936 own summon unit random board state is has_subtype
    do 937 own summon unit random board state is has_subtype
  Riftwalker:
    when 467 played self
    when 1097 always
    if 467 amount_product
    if 467 amount_event_count
    do 467 own damage any all position is surrounding amount=product
    do 1097 has_keyword can self event=played

## C11 lr_10.md 5 (CAUSE, open, 0 table lines from the same code)
Moving enemy cards into a lane with Professor X is a card put where the need forbids it (L29).
- W marvel_snap: Magneto -> Professor X: Magneto moves enemy units, and Professor X acts on units in its lane | network.py []
- R marvel_snap: Debrii -> Viper: Debrii puts your units there, and Viper acts on units in its lane | network.py []
  Magneto:
    when 6112 played self
    do 6112 own move unit enemy all board cost in 3;cost in 4
  Professor X:
    when 6210 always
    do 6210 own cant card all hand event=played
    do 6210 own cant card all event=summoned
    do 6210 own cant unit all board position is same_lane event=dies

## C12 lr_10.md 6 (CAUSE, open, 0 table lines from the same code)
A put unit must have the keyword or state the need asks; Amberhides needs a poisoned unit and Lich Summoners' summoned units are not poisoned (L29, L14).
- W stormbound: Lich Summoners -> Amberhides: Lich Summoners puts your units there, and Amberhides acts on units around it | network.py []
- R duelyst: Sky Phalanx -> Arclyte Sentinel: Sky Phalanx puts your units there, and Arclyte Sentinel acts on units around it | network.py []
  Lich Summoners:
    when 10345 attack_done
    if 10345 amount_per_level
    do 10345 own summon strength=3.0
  Amberhides:
    when 10259 played self
    if 10259 amount_event_amount
    if 10259 amount_per_level
    do 10259 own damage unit highest board position is surrounding;state is poisoned amount=4.0
    do 10259 own stat_change self strength=event_amount

## C13 lr_11.md 1 (CAUSE, open, 0 table lines from the same code)
A card that moves a card in hand or deck (draw, put on top, shuffle, "move card ... hand/deck") is read as moving units, but L29 counts only changes of where units stand on the board, so it gets no line to cards that act by row.
- W gwent: Cursed Scroll -> Doadrick Leumaerts: Cursed Scroll moves Doadrick Leumaerts, and Doadrick Leumaerts acts on units in the back row | network.py []
- W gwent: Cursed Scroll -> Vilgefortz: Cursed Scroll moves Vilgefortz, and Vilgefortz acts on units in the back row or in the front row | network.py []
- W gwent: Cursed Scroll -> Avallac'h: Sage: Cursed Scroll moves Avallac'h: Sage, and Avallac'h: Sage acts on units in the back row | network.py []
- W gwent: Maxii van Dekkar -> Doadrick Leumaerts: Maxii van Dekkar moves Doadrick Leumaerts, and Doadrick Leumaerts acts on units in the back row | network.py []
- R gwent: Malena -> Pavko Gale: Malena moves Pavko Gale, and Pavko Gale acts on units in the back row | network.py []
- R gwent: Malena -> Dryad Ranger: Malena moves Dryad Ranger, and Dryad Ranger acts on units in the back row or in the front row | network.py []
- R gwent: Wild Hunt Bruiser -> White Frost: Wild Hunt Bruiser moves enemy units, and White Frost acts on units in its target's row; also moves into place: moves an enemy unit into the row it hits | network.py [2313]
  Cursed Scroll:
    when 3156 activated self
    when 4504 played self
    do 3156 own draw card mine chosen deck amount=1.0
    do 3156 own move card mine chosen hand
    do 4504 has_keyword cant self event=activated;turns=1.0
  Doadrick Leumaerts:
    when 2883 played self
    when 4510 played self
    when 2884 activated self
    when 2885 always
    when 4511 activated self
    if 2883 have is unit mine all board type is 47
    if 2884 keyword_condition
    if 4511 amount_listed
    if 2884 have is self position is back_row
    do 2883 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2884 own draw card mine deck_top amount=1.0
    do 2884 own move card mine chosen hand
    do 2885 own keyword_action amount=1.0
    do 4511 uses_keyword cant event=activated;turns=listed
  Vilgefortz:
    when 2174 played self
    when 2175 played self
    if 2174 keyword_condition
    if 2175 keyword_condition
    if 2174 have is self position is front_row
    if 2175 have is self position is back_row
    do 2174 own kill unit enemy chosen board
    do 2174 own summon unit enemy top deck state is bronze
    do 2175 own kill unit mine chosen board
    do 2175 own summon unit mine top deck
  Avallac'h: Sage:
    when 1793 played self
    if 1793 keyword_condition
    if 1793 have is self position is back_row
    do 1793 own play_card landmark mine chosen deck
  Maxii van Dekkar:
    when 3487 played self
    do 3487 own look card mine all deck
    do 3487 own shuffle_into_deck card mine all deck
    do 3487 own move card mine chosen deck

## C14 lr_11.md 2 (CAUSE, open, 0 table lines from the same code)
A card whose rows only say "start_attack self" (no place, no "nearby") is read as acting on units around it, but L29 needs a row that acts by place, so units put there give it no line.
- W duelyst: Dagona -> Lavaslasher: Dagona puts your units there, and Lavaslasher acts on units around it | network.py []
- W duelyst: Jax Truesight -> Lavaslasher: Jax Truesight puts your units there, and Lavaslasher acts on units around it | network.py []
- W duelyst: Rage Reactor -> Lavaslasher: Rage Reactor puts your units there, and Lavaslasher acts on units around it | network.py []
- R duelyst: Dagona -> Sandswirl Reader: Dagona puts your units there, and Sandswirl Reader acts on units around it | network.py []
- R duelyst: Sky Phalanx -> Primus Fist: Sky Phalanx puts your units there, and Primus Fist acts on units around it | network.py []
- R duelyst: Chirpuka -> Primus Fist: Chirpuka puts your units there, and Primus Fist acts on units around it | network.py []
  Dagona:
    when 595 played self
    when 596 dies self
    do 595 own capture unit chosen everywhere
    do 596 own summon it
  Lavaslasher:
    when 919 played self
    do 919 own start_attack self
  Jax Truesight:
    when 300 played self
    when 1081 always
    do 300 own summon power=1.0;health=1.0
    do 1081 has_keyword can self event=attacks
  Rage Reactor:
    when 1026 always
    when 1027 killed unit enemy
    do 1026 own stat_change player mine power=1.0
    do 1027 own summon

## C15 lr_12.md 1 (CAUSE, open, 0 table lines from the same code)
A move or copy of a card in hand or deck (Gwent "move a card", a copy in hand) was read as moving a unit on the board, but L29 counts only changes of where units stand (and L19: a copy into hand is one more card).
- W gwent: Draig Bon-Dhu -> Tuirseach Axeman: Draig Bon-Dhu moves Tuirseach Axeman, and Tuirseach Axeman acts on units in the front row | network.py []
- W gwent: Maxii van Dekkar -> Heymaey Skald: Maxii van Dekkar moves Heymaey Skald, and Heymaey Skald acts on units in the back row | network.py []
- W gwent: Cursed Scroll -> Redanian Archer: Cursed Scroll moves Redanian Archer, and Redanian Archer acts on units in the back row | network.py []
- W gwent: Operator -> Imposter: Operator puts enemy units there, and Imposter acts on units in a card it picks's row or in its target's row | network.py []
- R gwent: Malena -> Treant Boar: Malena moves Treant Boar, and Treant Boar acts on units in the back row or in the front row | network.py []
  Draig Bon-Dhu:
    when 2111 played self
    when 2112 always
    when 4510 played self
    when 2113 activated self
    when 4544 round_start
    when 2114 always
    when 4511 activated self
    when 4510 played self
    when 4504 played self
    if 4544 event_count ge 2.0
    if 4511 amount_listed
    do 2111 own move unit mine chosen deck state is bronze;type is 45
    do 2112 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2113 own give_keyword unit mine chosen discard
    do 4544 uses_keyword base_change unit mine chosen discard strength=1.0
    do 2114 own keyword_action amount=1.0
    do 4511 uses_keyword cant event=activated;turns=listed
    do 4510 has_keyword can self event=activated
    do 4504 has_keyword cant self event=activated;turns=1.0
  Tuirseach Axeman:
    when 2152 played self
    if 2152 keyword_condition
    if 2152 amount_stat damage chosen
    if 2152 have is self position is front_row
    do 2152 own damage unit chosen board amount=stat
  Maxii van Dekkar:
    when 3487 played self
    do 3487 own look card mine all deck
    do 3487 own shuffle_into_deck card mine all deck
    do 3487 own move card mine chosen deck
  Heymaey Skald:
    when 2144 played self
    when 4543 activated
    if 2144 keyword_condition
    if 2144 have is self position is back_row
    do 2144 own draw card mine deck_top amount=1.0
    do 2144 own keyword_action card mine chosen hand
    do 4543 uses_keyword discard card mine chosen hand
  Cursed Scroll:
    when 3156 activated self
    when 4504 played self
    do 3156 own draw card mine chosen deck amount=1.0
    do 3156 own move card mine chosen hand
    do 4504 has_keyword cant self event=activated;turns=1.0
  Redanian Archer:
    when 3036 always
    when 4510 played self
    when 3037 activated self
    when 3038 always
    when 4513 always
    when 3039 turn_end
    when 4513 always
    when 4510 played self
    when 4513 always
    if 3037 keyword_condition
    if 4513 amount_listed
    if 3039 keyword_condition
    if 4513 amount_listed
    if 4513 amount_listed
    if 3037 have is self position is back_row
    if 3039 have is self keyword is 756174
    do 3036 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 3037 own damage unit enemy chosen board amount=1.0
    do 3038 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 3039 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4510 has_keyword can self event=activated
    do 4513 has_keyword can self event=activated;times=listed
  Operator:
    when 1812 played self
    do 1812 own copy unit mine chosen hand state is bronze;state is created
    do 1812 own copy unit mine chosen hand state is bronze;state is created
  Imposter:
    when 3286 activated self
    when 4523 always
    when 3287 played unit mine type is 62
    when 4714 activated self
    when 4523 always
    when 4715 played unit mine type is 62
    when 4504 played self
    if 3286 amount_count unit enemy all board state in positive;state in negative;position is same_row of unit it;of:kind is unit
    if 3287 amount ge 4.0
    if 3287 amount_distinct keyword unit enemy all board state in positive;state in negative
    if 4714 amount_count unit enemy all board position is same_row of it
    if 4715 amount ge 4.0
    if 4715 amount_distinct keyword unit enemy all board
    do 3286 own give_keyword unit enemy chosen board
    do 4523 uses_keyword silence unit enemy chosen board
    do 3286 own copy unit enemy it board state is created
    do 3286 own stat_change unit enemy it strength=count
    do 3287 own stat_change unit mine it type is 62 strength=1.0
    do 4714 own give_keyword unit enemy chosen board
    do 4523 uses_keyword silence unit enemy chosen board
    do 4714 own copy unit enemy it
    do 4714 own stat_change unit enemy it strength=count
    do 4715 own stat_change unit mine it type is 62 strength=1.0
    do 4504 has_keyword cant self event=activated;turns=1.0

## C16 lr_12.md 2 (CAUSE, open, 0 table lines from the same code)
"Ready" (reactivate) and "steal" were read as moving units, but neither changes a position, so L29 gives no line to a card that acts by place.
- W duelyst: Spirit of the Wild -> Lightbender: Spirit of the Wild moves your units, and Lightbender acts on units around it | network.py []
- W duelyst: Mindlathe -> Blood Siren: Mindlathe moves enemy units, and Blood Siren acts on units around it | network.py []
- R duelyst: Repulsor Beast -> Blood Siren: Repulsor Beast moves enemy units, and Blood Siren acts on units around it | network.py []
  Spirit of the Wild:
    when 276 played self
    do 276 own ready unit mine all board position is starting_side of player enemy;of:kind is player
  Lightbender:
    when 288 played self
    do 288 own silence position all position is surrounding
  Mindlathe:
    when 531 damaged unit
    do 531 own ready unit it
    do 531 own steal unit it
  Blood Siren:
    when 168 played self
    do 168 own stat_change any enemy chosen board position is surrounding power=-2.0

## C17 lr_12.md 3 (CAUSE, open, 0 table lines from the same code)
A placer was linked to a card whose by-place text is a drawback (it kills itself when 4 of my units are in the lane), which L29 and L5 say is no line.
- W marvel_snap: White Tiger -> Widow's Kiss: White Tiger puts your units there, and Widow's Kiss acts on units in its lane | network.py []
- W marvel_snap: Adamantium Infusion -> Ice Cube: Adamantium Infusion puts your units there, and Ice Cube acts on units in its lane | network.py []
- R marvel_snap: Adamantium Infusion -> Arnim Zola: Adamantium Infusion puts your units there, and Arnim Zola acts on units in its lane | network.py []
  White Tiger:
    when 6445 played self
    do 6445 own summon power=10.0
  Widow's Kiss:
    when 6449 always
    if 6449 count ge 4.0 unit mine all board position is same_lane
    do 6449 own kill self
  Adamantium Infusion:
    when 5801 played self
    if 5801 amount_stat power it
    do 5801 own obliterate self
    do 5801 own revive unit mine highest discard position is same_lane
    do 5801 own stat_change unit mine it power=stat
  Ice Cube:
    when 6024 round_start
    when 6025 round_start
    if 6025 count ge 4.0 unit mine board position is same_lane
    do 6024 own mana_gain mana mine amount=1.0
    do 6025 own kill self

## C18 lr_12.md 4 (CAUSE, open, 0 table lines from the same code)
Putting my own units next to a card whose area effect hits every unit around it (damage to all, both sides) was read as help, but the placed units only become its victims, so the line is no help (L9, L29 sides).
- W duelyst: Grimes -> Sunset Paragon: Grimes puts your units there, and Sunset Paragon acts on units around it | network.py []
- W duelyst: Gust -> Frostbone Naga: Gust puts your units there, and Frostbone Naga acts on units around it | network.py []
- W stormbound: Edrik the Fierce -> Witches of the Wild: Edrik the Fierce puts your units there, and Witches of the Wild acts on units next to it | network.py []
- R duelyst: Prominence -> Roar: Prominence puts your units there, and Roar acts on units around your leader or base | network.py []
  Grimes:
    when 936 played self
    when 937 dies self
    do 936 own summon unit random board state is has_subtype
    do 937 own summon unit random board state is has_subtype
  Sunset Paragon:
    when 777 played self
    if 777 amount_stat power it
    do 777 own damage unit all board position is surrounding amount=stat
  Gust:
    when 982 played spell mine keyword is 5001113
    do 982 own summon amount=2.0
  Frostbone Naga:
    when 307 played self
    do 307 own damage any all board position is surrounding amount=2.0
  Edrik the Fierce:
    when 10362 played self
    if 10362 amount_per_level
    do 10362 own summon strength=2.0
  Witches of the Wild:
    when 10258 played self
    if 10258 amount_per_level
    if 10258 amount_event_amount
    do 10258 own damage unit all board position is bordering amount=1.0
    do 10258 own stat_change self strength=event_amount

## C19 lr_13.md 1 (CAUSE, open, 0 table lines from the same code)
An act that does not change where a unit stands on the board (Gwent moving a card inside the deck or hand, readying a unit to act again) was read as "moves units" (L29: changes are moving, pushing, pulling, swapping and putting units at a place).
- W gwent: Fisher King -> Vilgefortz: Fisher King moves Vilgefortz, and Vilgefortz acts on units in the back row or in the front row | network.py []
- W gwent: Blightmaker -> Yennefer: Divination: Blightmaker moves Yennefer: Divination, and Yennefer: Divination acts on units in the back row | network.py []
- W gwent: Dimun Pirate -> Vabjorn: Dimun Pirate moves Vabjorn, and Vabjorn acts on units in the front row | network.py []
- W duelyst: Spirit of the Wild -> Avalanche: Spirit of the Wild moves your units, and Avalanche acts on units base's starting side or on your leader | network.py []
- R gwent: Aen Elle Aristocrat -> Wild Hunt Warrior: Aen Elle Aristocrat moves enemy units, and Wild Hunt Warrior acts on units in a card it picks's row; also moves into place: moves an enemy unit into the row it  | network.py [2313]
- R gwent: Aen Elle Aristocrat -> Imlerith's Wrath: Aen Elle Aristocrat moves enemy units, and Imlerith's Wrath acts on units in a space it picks's row or not in a space it picks's row | network.py []
  Fisher King:
    when 2663 played self
    if 2663 keyword_condition
    if 2663 have is self position is back_row
    do 2663 own move card mine chosen deck
  Vilgefortz:
    when 2174 played self
    when 2175 played self
    if 2174 keyword_condition
    if 2175 keyword_condition
    if 2174 have is self position is front_row
    if 2175 have is self position is back_row
    do 2174 own kill unit enemy chosen board
    do 2174 own summon unit enemy top deck state is bronze
    do 2175 own kill unit mine chosen board
    do 2175 own summon unit mine top deck
  Blightmaker:
    when 3669 played self
    do 3669 own move card mine chosen deck
    do 3669 own summon card mine it type is 37
    do 3669 own create
    do 3669 own play_card card mine chosen hand card is 813588
  Yennefer: Divination:
    when 2571 played self
    when 4506 activated
    if 2571 keyword_condition
    if 2571 amount_stat strength unit mine it deck
    if 2571 have is self position is back_row
    do 2571 own keyword_action unit mine random deck
    do 4506 uses_keyword reveal unit mine random deck
    do 2571 own stat_change unit mine chosen board strength=stat
  Dimun Pirate:
    when 2139 played self
    if 2139 have not unit mine all board type is 59
    do 2139 own move card mine top deck
  Vabjorn:
    when 2255 played self
    if 2255 keyword_condition
    if 2255 have is self position is front_row
    do 2255 own play_card card mine chosen deck type is 29
  Spirit of the Wild:
    when 276 played self
    do 276 own ready unit mine all board position is starting_side of player enemy;of:kind is player
  Avalanche:
    when 267 played self
    when 1086 always
    do 267 own damage any all board position is starting_side of player mine;of:kind is player amount=4.0
    do 267 own give_keyword any it
    do 1086 uses_keyword cant any it event=moves
    do 1086 uses_keyword cant any it event=attacks

## C20 lr_13.md 2 (CAUSE, open, 0 table lines from the same code)
A summon whose rows name no place, or puts the unit at random, on the enemy side, or is the card's own made unit, was read as "puts your units there" (L29: a random put and a card the placer makes itself give no line; L9 sides; the damage or kill of the other card is on the enemy or a drawback).
- W duelyst: Pandora -> Primus Fist: Pandora puts your units there, and Primus Fist acts on units around it | network.py []
- W duelyst: Allomancer -> Orbrider: Allomancer puts your units there, and Orbrider acts on units around it | network.py []
- W duelyst: Dioltas -> Holy Immolation: Dioltas puts your units there, and Holy Immolation acts on units around its target | network.py []
- W duelyst: Conscript -> Decimate: Conscript puts your units there, and Decimate acts on units base or not around a leader | network.py []
- R marvel_snap: Squirrel Girl -> Ant Man: Squirrel Girl puts your units there, and Ant Man acts on units in its lane | network.py []
  Pandora:
    when 326 turn_end
    do 326 own summon power=3.0;health=3.0
    do 326 own give_random_keyword unit mine it card is -1001
  Primus Fist:
    when 304 played self
    do 304 own stat_change unit mine chosen board position is surrounding power=2.0
  Allomancer:
    when 829 dies self
    do 829 own summon unit random board name_has is 1
  Orbrider:
    when 394 played self
    do 394 own return_to_hand unit mine chosen board position is surrounding
  Dioltas:
    when 331 dies self
    when 1098 always
    do 331 own summon power=0.0;health=8.0
    do 1098 uses_keyword cant any enemy all board position is surrounding of self event=moves
    do 1098 uses_keyword cant any enemy all board position is surrounding of self event=attacks
  Holy Immolation:
    when 73 played self
    do 73 own heal unit mine chosen board amount=4.0
    do 73 own damage any enemy all board position is surrounding of it amount=4.0
  Conscript:
    when 58 played self
    do 58 own summon power=1.0;health=2.0
  Decimate:
    when 62 played self
    do 62 own kill unit all board position not surrounding of player all;of:kind is player

## C21 lr_13.md 3 (CAUSE, open, 0 table lines from the same code)
A card that only needs ITS OWN row when it is played (Gwent "if I am in the front/back row") does not act on units by place, and a mover cannot set that row, since the check is at the moment it is played from hand (L29: one card must change a position, the other must care about the places of units).
- W gwent: Ciaran aep Easnillen -> Naiad Pondkeeper: Ciaran aep Easnillen moves Naiad Pondkeeper, and Naiad Pondkeeper acts on units in the back row or in the front row | network.py []
- W gwent: Malena -> Weeping Willow: Malena moves Weeping Willow, and Weeping Willow acts on units in the back row or in the front row | network.py []
- W gwent: Guerilla Tactics -> Filavandrel aén Fidháil: Guerilla Tactics moves Filavandrel aén Fidháil, and Filavandrel aén Fidháil acts on units in the back row or in the front row | network.py []
- R into_the_breach: Titan Fist -> Hydraulic Lifter: Titan Fist moves enemy units, and Hydraulic Lifter acts on units next to it | network.py []
- R stormbound: Cheesy Lurers -> Minion Launchers: Cheesy Lurers moves enemy units, and Minion Launchers acts on units first in front of it | network.py []
  Ciaran aep Easnillen:
    when 2048 played self
    when 4523 always
    do 2048 own give_keyword unit chosen board
    do 4523 uses_keyword silence unit chosen board
    do 2048 own move unit it
  Naiad Pondkeeper:
    when 4034 played self
    when 4568 activated
    when 4035 played self
    when 4551 played card mine type is 26
    if 4034 keyword_condition
    if 4034 amount_stat strength unit mine chosen board card is 813637
    if 4568 amount_stat base_power it
    if 4035 keyword_condition
    if 4551 amount_count unit mine board keyword is 756204
    if 4034 have is self position is front_row
    if 4035 have is self position is back_row
    do 4034 own damage unit enemy chosen board amount=stat
    do 4034 own keyword_action unit mine chosen board card is 813637
    do 4568 uses_keyword stat_set unit mine chosen board card is 813637 strength=stat
    do 4035 own give_keyword unit mine chosen board keyword not 756204
    do 4551 uses_keyword summon unit mine
    do 4551 uses_keyword stat_set unit mine it card is 813637 strength=count
  Malena:
    when 2055 always
    when 4510 played self
    when 2056 activated self
    when 2057 always
    when 4511 activated self
    when 4510 played self
    when 4504 played self
    if 4511 amount_listed
    do 2055 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2056 own move unit chosen board
    do 2057 own keyword_action amount=1.0
    do 4511 uses_keyword cant event=activated;turns=listed
    do 4510 has_keyword can self event=activated
    do 4504 has_keyword cant self event=activated;turns=1.0
  Weeping Willow:
    when 2775 always
    when 4553 played unit mine region not Neutral
    when 2776 activated self
    when 2777 played self
    when 4549 given_keyword self keyword is 756202
    when 4553 played unit mine region not Neutral
    if 4553 have not unit mine board state is shares_subtype_with_it
    if 4553 amount_listed
    if 2776 keyword_condition
    if 2776 amount_distinct primary_type unit mine all board
    if 2777 keyword_condition
    if 4549 event_count ge 2.0
    if 4553 have not unit mine board state is shares_subtype_with_it
    if 4553 amount_listed
    if 2776 have is self position is front_row
    if 2777 have is self position is back_row
    do 2775 own give_keyword self
    do 4553 uses_keyword stat_change self strength=listed
    do 2776 own stat_change self strength=distinct
    do 2777 own give_keyword unit enemy chosen board
    do 4549 uses_keyword kill unit enemy chosen board
    do 4553 has_keyword stat_change self strength=listed
  Guerilla Tactics:
    when 2369 activated self
    when 2370 always
    when 4513 always
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 4513 amount_listed
    do 2369 own move unit chosen board
    do 2369 own damage unit enemy it amount=1.0
    do 2369 own stat_change unit mine it strength=3.0
    do 2370 own give_keyword self amount=3.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Filavandrel aén Fidháil:
    when 3791 played self
    when 3792 played self
    if 3791 keyword_condition
    if 3792 keyword_condition
    if 3791 have is self position is front_row
    if 3792 have is self position is back_row
    do 3791 own create card mine random region is Scoiatael;cost eq 3560;category is spell
    do 3791 own play_card card mine it category is spell
    do 3792 own create card mine random region is Scoiatael;cost le 3561;category is spell
    do 3792 own play_card card mine it category is spell

## C22 lr_14.md 2 (CAUSE, open, 0 table lines from the same code)
A card that moves or draws a card in hand or deck was read as moving units on the board; only a change of board position links to place needs (L29, L1).
- W gwent: Fisher King -> Sove: Fisher King moves Sove, and Sove acts on units in the front row | network.py []
- W gwent: Cursed Scroll -> Vicovaro Novice: Cursed Scroll moves Vicovaro Novice, and Vicovaro Novice acts on units in the back row | network.py []
- W gwent: Doadrick Leumaerts -> Lydia van Bredevoort: Doadrick Leumaerts moves Lydia van Bredevoort, and Lydia van Bredevoort acts on units in the back row or in the front row | network.py []
- W gwent: Blightmaker -> Doadrick Leumaerts: is an Agent it asks for; also Blightmaker moves Doadrick Leumaerts, and Doadrick Leumaerts acts on units in the back row | network.py []
- R gwent: Malena -> Dwarven Skirmisher: Malena moves Dwarven Skirmisher, and Dwarven Skirmisher acts on units in the front row | network.py []
- R gwent: Ciaran aep Easnillen -> Ocvist: Ciaran aep Easnillen moves enemy units, and Ocvist acts on units in the row facing it | network.py []
  Fisher King:
    when 2663 played self
    if 2663 keyword_condition
    if 2663 have is self position is back_row
    do 2663 own move card mine chosen deck
  Sove:
    when 4023 played self
    when 4024 dies self
    when 4537 always
    if 4023 keyword_condition
    if 4023 amount_count unit enemy all board state is damaged
    if 4024 amount_product
    if 4024 amount_stat base_power self
    if 4023 have is self position is front_row
    do 4023 own summon card mine chosen deck type is 43
    do 4023 own give_ability card mine it type is 43
    do 4024 gives stat_change unit enemy board card is 757381 strength=product
    do 4023 own damage card mine it type is 43 amount=count
    do 4023 own give_keyword self
    do 4537 uses_keyword cant player all event=targeted
  Cursed Scroll:
    when 3156 activated self
    when 4504 played self
    do 3156 own draw card mine chosen deck amount=1.0
    do 3156 own move card mine chosen hand
    do 4504 has_keyword cant self event=activated;turns=1.0
  Vicovaro Novice:
    when 1942 played self
    when 4584 played self
    if 1942 keyword_condition
    if 4584 keyword_condition
    if 1942 have is self position is back_row
    if 4584 have is self position is back_row
    do 1942 own draw card mine deck_top amount=1.0
    do 1942 own put_on_top card mine chosen hand
    do 4584 own draw card mine deck_top amount=1.0
    do 4584 own put_on_top card mine chosen hand
  Doadrick Leumaerts:
    when 2883 played self
    when 4510 played self
    when 2884 activated self
    when 2885 always
    when 4511 activated self
    if 2883 have is unit mine all board type is 47
    if 2884 keyword_condition
    if 4511 amount_listed
    if 2884 have is self position is back_row
    do 2883 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2884 own draw card mine deck_top amount=1.0
    do 2884 own move card mine chosen hand
    do 2885 own keyword_action amount=1.0
    do 4511 uses_keyword cant event=activated;turns=listed
  Lydia van Bredevoort:
    when 3778 played self
    when 3779 played self
    if 3778 keyword_condition
    if 3779 keyword_condition
    if 3778 have is self position is front_row
    if 3779 have is self position is back_row
    do 3778 own create card mine chosen hand state is bronze;category is spell;state is opponent_faction
    do 3778 own play_card card mine chosen hand state is created
    do 3779 own play_card card enemy chosen discard state is bronze;category is spell
  Blightmaker:
    when 3669 played self
    do 3669 own move card mine chosen deck
    do 3669 own summon card mine it type is 37
    do 3669 own create
    do 3669 own play_card card mine chosen hand card is 813588

## C23 lr_14.md 4 (CAUSE, open, 0 table lines from the same code)
A placer that puts a random card, or only the unit it makes itself, was linked to a lane need; random or self-made units are no help (L29: Jaxi's corner, the card a placer makes itself, White Tiger's Tiger).
- W marvel_snap: Gladiator -> Shadow King: Gladiator puts enemy units there, and Shadow King acts on units in its lane | network.py []
- W faeria: Frog-Tosser -> Bone Collector: Frog-Tosser moves your units, and Bone Collector acts on units next to it; also triggers: makes units die (by fighting) | network.py []
- W marvel_snap: White Tiger -> Wolfsbane: White Tiger puts your units there, and Wolfsbane acts on units in its lane | network.py []
- R marvel_snap: Grapple Arrow -> Galactus: Grapple Arrow moves your units, and Galactus acts on units in its lane | network.py []
- R marvel_snap: Heimdall -> Carnage: Heimdall moves your units, and Carnage acts on units in its lane | network.py []
  Gladiator:
    when 5987 played self
    do 5987 own summon card enemy random deck
    do 5987 own kill unit enemy it board power lt 5802
  Shadow King:
    when 6280 played self
    if 6280 amount_stat base_power it
    do 6280 own stat_set unit all board position is same_lane power=stat
  Frog-Tosser:
    when 1517 played self
    when 1757 always
    do 1517 own start_attack self
    do 1517 own summon power=2.0;health=2.0
    do 1517 own give_keyword unit mine it card is -2003
    do 1757 uses_keyword can unit mine it card is -2003 event=moves
  Bone Collector:
    when 1218 dies unit all position is bordering
    do 1218 own stat_change self power=1.0;health=1.0
  White Tiger:
    when 6445 played self
    do 6445 own summon power=10.0
  Wolfsbane:
    when 6454 played self
    if 6454 amount_count unit mine all board position is same_lane;card not 8000723
    if 6454 amount_product
    do 6454 own stat_change self power=product

## C24 lr_14.md 5 (CAUSE, open, 0 table lines from the same code)
A card that kills or copies my units in a lane was linked to a card that stops those units dying; Armor works against Arnim Zola's destroy, so it is no help (L4, L5).
- W marvel_snap: Arnim Zola -> Armor: Arnim Zola puts your units there, and Armor acts on units in its lane | network.py []
- W marvel_snap: Arnim Zola -> Fastball Special: Arnim Zola puts your units there, and Fastball Special acts on units in its lane | network.py []
- R marvel_snap: Ghost-Spider -> Arnim Zola: Ghost-Spider moves your units, and Arnim Zola acts on units in its lane | network.py []
  Arnim Zola:
    when 5829 played self
    do 5829 own kill unit mine chosen board position is same_lane;card not 8000034
    do 5829 own copy unit mine it card not 8000034
  Armor:
    when 5828 always
    do 5828 own cant unit all board position is same_lane event=dies
  Fastball Special:
    when 5959 played self
    if 5959 amount_event_amount
    if 5959 amount_minus
    do 5959 own kill unit mine highest board position is same_lane
    do 5959 own stat_change unit enemy chosen board position is same_lane power=minus

## C25 lr_14.md 6 (CAUSE, open, 0 table lines from the same code)
A line says the second card "acts on units in its lane", but its rows show no act by place (Hulkbuster only merges itself); the need must be in the rows (L29).
- W marvel_snap: Doctor Strange -> Hulkbuster: Doctor Strange moves your units, and Hulkbuster acts on units in its lane | network.py [1610]
- R marvel_snap: Heimdall -> Carnage: Heimdall moves your units, and Carnage acts on units in its lane | network.py []
  Doctor Strange:
    when 5913 played self
    do 5913 own move unit mine highest board
  Hulkbuster:
    when 6016 played self
    do 6016 own merge self

## C26 lr_15.md 1 (CAUSE, open, 0 table lines from the same code)
A move of a card in hand or deck (draw, look, shuffle, put on top) is taken as a change of where units stand; L29 counts only moving, pushing, pulling, swapping and putting units at a place on the board.
- W gwent: Myrgtabrakke -> Dwarven Skirmisher: Myrgtabrakke moves Dwarven Skirmisher, and Dwarven Skirmisher acts on units in the front row | network.py []
- W gwent: Maxii van Dekkar -> Hammond: Maxii van Dekkar moves Hammond and your units, and Hammond acts on units next to it | network.py []
- R gwent: Guerilla Tactics -> Madoc: Guerilla Tactics moves enemy units, and Madoc acts on units in the row facing it | network.py []
- R gwent: Ciaran aep Easnillen -> Madoc: Ciaran aep Easnillen moves enemy units, and Madoc acts on units in the row facing it | network.py []
  Myrgtabrakke:
    when 1801 always
    when 4507 game_start
    when 1802 played self
    when 1803 activated self
    when 1804 always
    when 4513 always
    when 1805 game_start
    when 4513 always
    when 4507 game_start
    when 4513 always
    when 4504 played self
    if 4507 amount_count card mine type is 38;state is started_in_deck
    if 4513 amount_listed
    if 1805 amount_count card mine all deck type is 38;state is started_in_deck
    if 4513 amount_listed
    if 4507 amount_count card mine type is 38;state is started_in_deck
    if 4513 amount_listed
    do 1801 own give_keyword self
    do 4507 uses_keyword stat_change self strength=count
    do 1802 own draw card mine deck type is 38 amount=1.0
    do 1802 own move card mine chosen hand
    do 1803 own damage unit enemy chosen board amount=1.0
    do 1804 own give_keyword self amount=0.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 1805 own give_keyword self amount=count
    do 4513 uses_keyword can self event=activated;times=listed
    do 4507 has_keyword stat_change self strength=count
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Dwarven Skirmisher:
    when 2071 played self
    when 4532 damaged self
    when 2072 activated self
    if 2071 keyword_condition
    if 4532 amount_listed
    if 2072 keyword_condition
    if 2071 have is self position is front_row
    if 2072 have is self keyword is 756174
    do 2071 own damage unit enemy chosen board amount=3.0
    do 2071 own give_keyword self amount=1.0
    do 4532 uses_keyword negate_damage self amount=listed
    do 2072 own damage unit enemy chosen board amount=3.0
  Maxii van Dekkar:
    when 3487 played self
    do 3487 own look card mine all deck
    do 3487 own shuffle_into_deck card mine all deck
    do 3487 own move card mine chosen deck
  Hammond:
    when 2942 played self
    when 4526 turn_end
    if 2942 amount_sum
    if 2942 amount_count unit all board position is sides of self;type is 60
    do 2942 own move unit enemy chosen board
    do 2942 own give_keyword unit enemy it board amount=sum
    do 4526 uses_keyword damage unit enemy it board amount=1.0

## C27 lr_15.md 2 (CAUSE, open, 0 table lines from the same code)
The second card is said to act by place, but its rows have no act by place (no lane, row, around or next-to filter); L29 needs one card to change a position and the other to care, and two cards only in the same deck are no line (L2).
- W duelyst: Chirpuka -> Lavaslasher: Chirpuka puts your units there, and Lavaslasher acts on units around it | network.py []
- W faeria: Bloated Toad -> Animated Banquet: Bloated Toad moves your units, and Animated Banquet acts on units next to it | network.py []
- R duelyst: Arcane Heart -> Frostbone Naga: Arcane Heart puts your units there, and Frostbone Naga acts on units around it | network.py []
- R duelyst: Repulsor Beast -> Nightsorrow Assassin: Repulsor Beast moves enemy units, and Nightsorrow Assassin acts on units around it | network.py []
  Chirpuka:
    when 472 summoned unit enemy
    when 1098 always
    do 472 own summon power=2.0;health=1.0
    do 1098 uses_keyword cant any enemy all board position is surrounding of self event=moves
    do 1098 uses_keyword cant any enemy all board position is surrounding of self event=attacks
  Lavaslasher:
    when 919 played self
    do 919 own start_attack self
  Bloated Toad:
    when 1630 always
    when 1757 always
    when 1631 played self
    when 1757 always
    when 1757 always
    do 1630 own give_keyword self
    do 1757 uses_keyword can self event=moves
    do 1631 own summon power=2.0;health=2.0
    do 1631 own give_keyword unit mine it card is -2003
    do 1757 uses_keyword can unit mine it card is -2003 event=moves
    do 1631 own capture unit mine it card is -2003
    do 1757 has_keyword can self event=moves
  Animated Banquet:
    when 1638 always
    when 1759 played self
    when 1639 turn_end
    when 1759 played self
    if 1759 amount_event_amount
    if 1759 amount_event_amount
    do 1638 own give_keyword self amount=1.0
    do 1759 uses_keyword move self amount=event_amount
    do 1639 own capture self
    do 1639 own stat_change it power=1.0;health=1.0
    do 1759 has_keyword move self amount=event_amount

## C28 lr_15.md 3 (CAUSE, open, 0 table lines from the same code)
A card whose only place effect is a drawback on my own units in its lane is taken as a need for units put there; L29 says no line for a drawback (L5).
- W marvel_snap: Mysterio -> Typhoid Mary: Mysterio puts your units there, and Typhoid Mary acts on units in its lane | network.py []
- R marvel_snap: Bucky Barnes -> Shadow King: Bucky Barnes puts your units there, and Shadow King acts on units in its lane | network.py []
- R marvel_snap: Ultron -> Venom: Ultron puts your units there, and Venom acts on units in its lane | network.py []
  Mysterio:
    when 6170 played self
    when 6171 activated self
    do 6170 own summon
    do 6171 own swap_stats self attr=power
  Typhoid Mary:
    when 6405 always
    do 6405 own stat_change unit mine all board position is same_lane;card not 8000671 power=-2.0

## C29 lr_15.md 4 (CAUSE, open, 0 table lines from the same code)
Moving enemy units is linked to a lane effect that protects every unit in the lane; moving enemies there only helps the enemy, so the sides are wrong (L29, L9).
- W marvel_snap: Magneto -> Armor: Magneto moves enemy units, and Armor acts on units in its lane | network.py []
- R duelyst: Repulsor Beast -> Nightsorrow Assassin: Repulsor Beast moves enemy units, and Nightsorrow Assassin acts on units around it | network.py []
- R into_the_breach: Titan Fist -> Quick-Fire Rockets: Titan Fist moves enemy units, and Quick-Fire Rockets acts on units in a line from it | network.py []
  Magneto:
    when 6112 played self
    do 6112 own move unit enemy all board cost in 3;cost in 4
  Armor:
    when 5828 always
    do 5828 own cant unit all board position is same_lane event=dies

## C30 lr_15.md 5 (CAUSE, open, 0 table lines from the same code)
Ready (another move and attack for my units) is taken as a move that changes where units stand, and the target Glacial Fissure hits everything in the middle column; L29 lists moving, pushing, pulling, swapping and putting, not ready (L2).
- W duelyst: Spirit of the Wild -> Glacial Fissure: Spirit of the Wild moves your units, and Glacial Fissure acts on units in the middle column | network.py []
- R marvel_snap: Blink -> Destroyer: Blink moves your units, and Destroyer acts on units not in its lane | network.py []
- R marvel_snap: Ghost-Spider -> Deathlok: Ghost-Spider moves your units, and Deathlok acts on units in its lane | network.py []
  Spirit of the Wild:
    when 276 played self
    do 276 own ready unit mine all board position is starting_side of player enemy;of:kind is player
  Glacial Fissure:
    when 565 played self
    do 565 own damage any all position is center_column amount=8.0

## C31 lr_16.md 1 (CAUSE, open, 0 table lines from the same code)
A card that moves or draws a card inside the deck or hand was read as moving a unit by place, but only units standing on the board change where they stand (L29, L1b).
- W gwent: Draig Bon-Dhu -> Vabjorn: Draig Bon-Dhu moves Vabjorn, and Vabjorn acts on units in the front row | network.py []
- W gwent: Cursed Scroll -> Lydia van Bredevoort: Cursed Scroll moves Lydia van Bredevoort, and Lydia van Bredevoort acts on units in the back row or in the front row | network.py []
- W gwent: Maxii van Dekkar -> Fisher King: Maxii van Dekkar moves Fisher King, and Fisher King acts on units in the back row | network.py []
- W gwent: Dimun Pirate -> Dimun Smuggler: Dimun Pirate moves Dimun Smuggler and your units, and Dimun Smuggler acts on units next to it | network.py []
- R gwent: Ciaran aep Easnillen -> Freixenet: Ciaran aep Easnillen moves Freixenet, and Freixenet acts on units in the back row | network.py []
- R into_the_breach: Hydraulic Lifter -> Titan Fist: Hydraulic Lifter moves enemy units, and Titan Fist acts on units next to it | network.py []
- R gwent: Guerilla Tactics -> Ocvist: Guerilla Tactics moves enemy units, and Ocvist acts on units in the row facing it | network.py []
  Draig Bon-Dhu:
    when 2111 played self
    when 2112 always
    when 4510 played self
    when 2113 activated self
    when 4544 round_start
    when 2114 always
    when 4511 activated self
    when 4510 played self
    when 4504 played self
    if 4544 event_count ge 2.0
    if 4511 amount_listed
    do 2111 own move unit mine chosen deck state is bronze;type is 45
    do 2112 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2113 own give_keyword unit mine chosen discard
    do 4544 uses_keyword base_change unit mine chosen discard strength=1.0
    do 2114 own keyword_action amount=1.0
    do 4511 uses_keyword cant event=activated;turns=listed
    do 4510 has_keyword can self event=activated
    do 4504 has_keyword cant self event=activated;turns=1.0
  Vabjorn:
    when 2255 played self
    if 2255 keyword_condition
    if 2255 have is self position is front_row
    do 2255 own play_card card mine chosen deck type is 29
  Cursed Scroll:
    when 3156 activated self
    when 4504 played self
    do 3156 own draw card mine chosen deck amount=1.0
    do 3156 own move card mine chosen hand
    do 4504 has_keyword cant self event=activated;turns=1.0
  Lydia van Bredevoort:
    when 3778 played self
    when 3779 played self
    if 3778 keyword_condition
    if 3779 keyword_condition
    if 3778 have is self position is front_row
    if 3779 have is self position is back_row
    do 3778 own create card mine chosen hand state is bronze;category is spell;state is opponent_faction
    do 3778 own play_card card mine chosen hand state is created
    do 3779 own play_card card enemy chosen discard state is bronze;category is spell
  Maxii van Dekkar:
    when 3487 played self
    do 3487 own look card mine all deck
    do 3487 own shuffle_into_deck card mine all deck
    do 3487 own move card mine chosen deck
  Fisher King:
    when 2663 played self
    if 2663 keyword_condition
    if 2663 have is self position is back_row
    do 2663 own move card mine chosen deck
  Dimun Pirate:
    when 2139 played self
    if 2139 have not unit mine all board type is 59
    do 2139 own move card mine top deck
  Dimun Smuggler:
    when 2345 played self
    when 2346 always
    when 4510 played self
    when 2347 activated self
    when 4510 played self
    when 4504 played self
    if 2345 have is unit board position is sides of self;type is 59
    do 2345 own copy self
    do 2346 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2347 own damage unit chosen board amount=1.0
    do 4510 has_keyword can self event=activated
    do 4504 has_keyword cant self event=activated;turns=1.0

## C32 lr_16.md 2 (CAUSE, open, 0 table lines from the same code)
My own units put or moved next to a card that damages or hits ALL units around it (mine too) were called help; the placed unit is only hurt, and a need that damages or silences by place is fed by enemy units there (L29 sides as L9).
- W duelyst: Sky Phalanx -> Sunset Paragon: Sky Phalanx puts your units there, and Sunset Paragon acts on units around it | network.py []
- W duelyst: Mist Dragon Seal -> Frostbone Naga: Mist Dragon Seal moves your units, and Frostbone Naga acts on units around it | network.py []
- W duelyst: Inner Focus -> Frostbone Naga: Inner Focus moves your units, and Frostbone Naga acts on units around it | network.py []
- R gwent: Pincer Maneuver -> Carroballista: Pincer Maneuver puts your units there, and Carroballista acts on units next to it | network.py []
- R into_the_breach: Seismic Capacitor -> Air Strike: Seismic Capacitor moves enemy units, and Air Strike acts on units on its space | network.py []
- R duelyst: Juxtaposition -> Hollow Grovekeeper: Juxtaposition moves enemy units, and Hollow Grovekeeper acts on units around it | network.py []
  Sky Phalanx:
    when 808 played self
    do 808 own summon amount=3.0
  Sunset Paragon:
    when 777 played self
    if 777 amount_stat power it
    do 777 own damage unit all board position is surrounding amount=stat
  Mist Dragon Seal:
    when 104 played self
    do 104 own stat_change unit mine chosen board power=1.0;health=1.0
    do 104 own move unit mine it
  Frostbone Naga:
    when 307 played self
    do 307 own damage any all board position is surrounding amount=2.0
  Inner Focus:
    when 112 played self
    do 112 own ready unit mine chosen board power le 111

## C33 lr_16.md 3 (CAUSE, open, 0 table lines from the same code)
A line was written as "acts on units next to it" where the receiving card's rows show no use of place for what the other card does (it captures itself, or only reacts to deaths, which a move or put does not cause) (L29, L16).
- W faeria: Mistral Guide -> Bone Collector: Mistral Guide moves Bone Collector and your units, and Bone Collector acts on units next to it | network.py []
- R faeria: Mistral Guide -> Emerald Salamander: Mistral Guide moves your units, and Emerald Salamander acts on units next to it | network.py []
- R gwent: Spontaneous Evolution -> Wolf Pack: Spontaneous Evolution puts your units there, and Wolf Pack acts on units in its row | network.py []
  Mistral Guide:
    when 1438 always
    when 1755 always
    when 1439 summoned unit mine position is bordering
    when 1759 played self
    when 1755 always
    when 1755 always
    if 1759 amount_event_amount
    do 1438 own give_keyword self
    do 1755 uses_keyword can self event=moves
    do 1439 own give_keyword unit mine it amount=2.0
    do 1759 uses_keyword move unit mine it amount=event_amount
    do 1439 own give_keyword unit mine it
    do 1755 uses_keyword can unit mine it event=moves
    do 1755 has_keyword can self event=moves
  Bone Collector:
    when 1218 dies unit all position is bordering
    do 1218 own stat_change self power=1.0;health=1.0

## C34 lr_2.md 1 (CAUSE, open, 0 table lines from the same code)
A "move" of a card between deck, hand or top of deck (draw and move to hand, shuffle and move to top, put on top) was read as a unit changing its place on the board, but L29 needs units moved or put at a place.
- W gwent: Maxii van Dekkar -> Alba Armored Cavalry: Maxii van Dekkar moves Alba Armored Cavalry, and Alba Armored Cavalry acts on units in the front row | network.py []
- W gwent: Cursed Scroll -> Dwimveandra: Cursed Scroll moves Dwimveandra, and Dwimveandra acts on units in the back row or in the front row | network.py []
- W gwent: Blightmaker -> Courier: Blightmaker moves Courier, and Courier acts on units in the back row or in the front row | network.py []
- W gwent: Myrgtabrakke -> Filavandrel aén Fidháil: Myrgtabrakke moves Filavandrel aén Fidháil, and Filavandrel aén Fidháil acts on units in the back row or in the front row | network.py []
- R gwent: Malena -> Dwarven Skirmisher: Malena moves Dwarven Skirmisher, and Dwarven Skirmisher acts on units in the front row | network.py []
- R gwent: Wild Hunt Bruiser -> Imlerith's Wrath: Wild Hunt Bruiser moves enemy units, and Imlerith's Wrath acts on units in a space it picks's row or not in a space it picks's row | network.py []
- R into_the_breach: Unstable Cannon -> Hydraulic Legs: Unstable Cannon moves enemy units, and Hydraulic Legs acts on units next to it | network.py []
  Maxii van Dekkar:
    when 3487 played self
    do 3487 own look card mine all deck
    do 3487 own shuffle_into_deck card mine all deck
    do 3487 own move card mine chosen deck
  Alba Armored Cavalry:
    when 2406 played self
    when 4523 always
    if 2406 keyword_condition
    if 2406 have is self position is front_row
    do 2406 own give_keyword unit enemy chosen board
    do 4523 uses_keyword silence unit enemy chosen board
  Cursed Scroll:
    when 3156 activated self
    when 4504 played self
    do 3156 own draw card mine chosen deck amount=1.0
    do 3156 own move card mine chosen hand
    do 4504 has_keyword cant self event=activated;turns=1.0
  Dwimveandra:
    when 3775 played self
    when 3776 played self
    if 3775 keyword_condition
    if 3775 amount_full
    if 3776 keyword_condition
    if 3775 have is self position is front_row
    if 3776 have is self position is back_row
    do 3775 own stage_advance landmark mine chosen board type is 14 amount=full
    do 3776 own refresh landmark mine chosen board type is 17
  Blightmaker:
    when 3669 played self
    do 3669 own move card mine chosen deck
    do 3669 own summon card mine it type is 37
    do 3669 own create
    do 3669 own play_card card mine chosen hand card is 813588
  Courier:
    when 2824 played self
    when 2825 played self
    when 4672 played self
    when 4673 played self
    if 2824 keyword_condition
    if 2825 keyword_condition
    if 4672 keyword_condition
    if 4673 keyword_condition
    if 2824 have is self position is front_row
    if 2825 have is self position is back_row
    if 4672 have is self position is front_row
    if 4673 have is self position is back_row
    do 2824 own look card enemy deck_top
    do 2824 own choose_card card enemy chosen deck_top
    do 2824 own put_on_top card enemy it
    do 2825 own look card mine deck_top
    do 2825 own choose_card card mine chosen deck_top
    do 2825 own put_on_top card mine it
    do 4672 own look card enemy top deck
    do 4672 own put_on_top card enemy chosen deck
    do 4673 own look card mine top deck
    do 4673 own put_on_top card mine chosen deck
  Myrgtabrakke:
    when 1801 always
    when 4507 game_start
    when 1802 played self
    when 1803 activated self
    when 1804 always
    when 4513 always
    when 1805 game_start
    when 4513 always
    when 4507 game_start
    when 4513 always
    when 4504 played self
    if 4507 amount_count card mine type is 38;state is started_in_deck
    if 4513 amount_listed
    if 1805 amount_count card mine all deck type is 38;state is started_in_deck
    if 4513 amount_listed
    if 4507 amount_count card mine type is 38;state is started_in_deck
    if 4513 amount_listed
    do 1801 own give_keyword self
    do 4507 uses_keyword stat_change self strength=count
    do 1802 own draw card mine deck type is 38 amount=1.0
    do 1802 own move card mine chosen hand
    do 1803 own damage unit enemy chosen board amount=1.0
    do 1804 own give_keyword self amount=0.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 1805 own give_keyword self amount=count
    do 4513 uses_keyword can self event=activated;times=listed
    do 4507 has_keyword stat_change self strength=count
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Filavandrel aén Fidháil:
    when 3791 played self
    when 3792 played self
    if 3791 keyword_condition
    if 3792 keyword_condition
    if 3791 have is self position is front_row
    if 3792 have is self position is back_row
    do 3791 own create card mine random region is Scoiatael;cost eq 3560;category is spell
    do 3791 own play_card card mine it category is spell
    do 3792 own create card mine random region is Scoiatael;cost le 3561;category is spell
    do 3792 own play_card card mine it category is spell

## C35 lr_2.md 2 (CAUSE, open, 0 table lines from the same code)
"Ready" (the unit may move and attack again) was read as a card that changes positions, but it moves nothing and a unit moving itself gives no line (L23, L29).
- W duelyst: Spirit of the Wild -> Avalanche: Spirit of the Wild moves your units, and Avalanche acts on units base's starting side or on your leader | network.py []
- R gwent: White Frost -> Imlerith's Wrath: White Frost moves enemy units, and Imlerith's Wrath acts on units in a space it picks's row or not in a space it picks's row | network.py []
  Spirit of the Wild:
    when 276 played self
    do 276 own ready unit mine all board position is starting_side of player enemy;of:kind is player
  Avalanche:
    when 267 played self
    when 1086 always
    do 267 own damage any all board position is starting_side of player mine;of:kind is player amount=4.0
    do 267 own give_keyword any it
    do 1086 uses_keyword cant any it event=moves
    do 1086 uses_keyword cant any it event=attacks

## C36 lr_2.md 3 (CAUSE, open, 0 table lines from the same code)
The unit a placer makes or summons itself (Frog, Toad, given the right to move) was counted as a position change for a card that cares where units stand; L29 gives no line for the card the placer makes itself, and these cards show no place-based need on the receiving card.
- W faeria: Battle Toads -> Animated Banquet: Battle Toads moves your units, and Animated Banquet acts on units next to it | network.py []
- W faeria: Frog-Tosser -> Bone Collector: Frog-Tosser moves your units, and Bone Collector acts on units next to it; also triggers: makes units die (by fighting) | network.py []
- R into_the_breach: Rocket Artillery -> Aerial Bombs: Rocket Artillery moves enemy units, and Aerial Bombs acts on units ahead of it or next to it | network.py []
  Battle Toads:
    when 1215 played self
    when 1757 always
    do 1215 own summon amount=2.0;power=2.0;health=2.0
    do 1215 own give_keyword unit mine it card is -2003
    do 1757 uses_keyword can unit mine it card is -2003 event=moves
  Animated Banquet:
    when 1638 always
    when 1759 played self
    when 1639 turn_end
    when 1759 played self
    if 1759 amount_event_amount
    if 1759 amount_event_amount
    do 1638 own give_keyword self amount=1.0
    do 1759 uses_keyword move self amount=event_amount
    do 1639 own capture self
    do 1639 own stat_change it power=1.0;health=1.0
    do 1759 has_keyword move self amount=event_amount
  Frog-Tosser:
    when 1517 played self
    when 1757 always
    do 1517 own start_attack self
    do 1517 own summon power=2.0;health=2.0
    do 1517 own give_keyword unit mine it card is -2003
    do 1757 uses_keyword can unit mine it card is -2003 event=moves
  Bone Collector:
    when 1218 dies unit all position is bordering
    do 1218 own stat_change self power=1.0;health=1.0

## C37 lr_3.md 1 (CAUSE, open, 0 table lines from the same code)
A Gwent "move" that takes a card from the deck to the hand (or to the top of the deck) is read as changing where units stand, so it links to cards that act by row; it is a tutor and moves no unit (L29, L1b, L1).
- W gwent: Eavesdrop -> Ferko the Sculptor: Eavesdrop moves Ferko the Sculptor, and Ferko the Sculptor acts on units in the front row | network.py []
- W gwent: Dimun Pirate -> Vabjorn: Dimun Pirate moves Vabjorn, and Vabjorn acts on units in the front row | network.py []
- W gwent: Blightmaker -> Yennefer: Divination: Blightmaker moves Yennefer: Divination, and Yennefer: Divination acts on units in the back row | network.py []
- W gwent: Cursed Scroll -> Doadrick Leumaerts: Cursed Scroll moves Doadrick Leumaerts, and Doadrick Leumaerts acts on units in the back row | network.py []
- R into_the_breach: Arachnoid -> Rail Cannon: Arachnoid carries Rail Cannon; also enables: Arachnoid moves enemy units, and Rail Cannon acts on units in a line from it | network.py []
- R into_the_breach: Attraction Pulse -> Aerial Bombs: Attraction Pulse moves enemy units, and Aerial Bombs acts on units ahead of it or next to it | network.py []
  Eavesdrop:
    when 2836 played self
    when 4676 played self
    do 2836 own mana_gain secondary_resource mine amount=5.0
    do 2836 own draw card mine deck_top amount=1.0
    do 2836 own move card mine chosen hand
    do 4676 own mana_gain secondary_resource mine amount=5.0
    do 4676 own draw card mine deck_top amount=1.0
    do 4676 own move card mine chosen hand
  Ferko the Sculptor:
    when 2991 played self
    if 2991 keyword_condition
    if 2991 have is self position is front_row
    do 2991 own play_card card mine chosen deck type is 24
  Dimun Pirate:
    when 2139 played self
    if 2139 have not unit mine all board type is 59
    do 2139 own move card mine top deck
  Vabjorn:
    when 2255 played self
    if 2255 keyword_condition
    if 2255 have is self position is front_row
    do 2255 own play_card card mine chosen deck type is 29
  Blightmaker:
    when 3669 played self
    do 3669 own move card mine chosen deck
    do 3669 own summon card mine it type is 37
    do 3669 own create
    do 3669 own play_card card mine chosen hand card is 813588
  Yennefer: Divination:
    when 2571 played self
    when 4506 activated
    if 2571 keyword_condition
    if 2571 amount_stat strength unit mine it deck
    if 2571 have is self position is back_row
    do 2571 own keyword_action unit mine random deck
    do 4506 uses_keyword reveal unit mine random deck
    do 2571 own stat_change unit mine chosen board strength=stat
  Cursed Scroll:
    when 3156 activated self
    when 4504 played self
    do 3156 own draw card mine chosen deck amount=1.0
    do 3156 own move card mine chosen hand
    do 4504 has_keyword cant self event=activated;turns=1.0
  Doadrick Leumaerts:
    when 2883 played self
    when 4510 played self
    when 2884 activated self
    when 2885 always
    when 4511 activated self
    if 2883 have is unit mine all board type is 47
    if 2884 keyword_condition
    if 4511 amount_listed
    if 2884 have is self position is back_row
    do 2883 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2884 own draw card mine deck_top amount=1.0
    do 2884 own move card mine chosen hand
    do 2885 own keyword_action amount=1.0
    do 4511 uses_keyword cant event=activated;turns=listed

## C38 lr_3.md 2 (CAUSE, open, 0 table lines from the same code)
A move that happens after a card is played is linked to a card whose row effects are checked only at the moment it is played, so moving it later changes nothing (L29: one must change a position and the other must care about it).
- W gwent: Malena -> Dryad Ranger: Malena moves Dryad Ranger, and Dryad Ranger acts on units in the back row or in the front row | network.py []
- W gwent: Ciaran aep Easnillen -> Naiad Pondkeeper: Ciaran aep Easnillen moves Naiad Pondkeeper, and Naiad Pondkeeper acts on units in the back row or in the front row | network.py []
- W gwent: Samum -> Dwarven Skirmisher: Samum moves Dwarven Skirmisher, and Dwarven Skirmisher acts on units in the front row | network.py []
- R gwent: Malena -> Weeping Willow: Malena moves Weeping Willow, and Weeping Willow acts on units in the back row or in the front row | network.py []
  Malena:
    when 2055 always
    when 4510 played self
    when 2056 activated self
    when 2057 always
    when 4511 activated self
    when 4510 played self
    when 4504 played self
    if 4511 amount_listed
    do 2055 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2056 own move unit chosen board
    do 2057 own keyword_action amount=1.0
    do 4511 uses_keyword cant event=activated;turns=listed
    do 4510 has_keyword can self event=activated
    do 4504 has_keyword cant self event=activated;turns=1.0
  Dryad Ranger:
    when 2797 always
    when 4553 played unit mine region not Neutral
    when 2798 played self
    when 2799 played self
    when 4549 given_keyword self keyword is 756202
    when 4669 always
    when 4553 played unit mine region not Neutral
    when 4670 played self
    when 4671 played self
    when 4549 given_keyword self keyword is 756202
    when 4553 played unit mine region not Neutral
    if 4553 have not unit mine board state is shares_subtype_with_it
    if 4553 amount_listed
    if 2798 keyword_condition
    if 2799 keyword_condition
    if 4549 event_count ge 2.0
    if 4553 have not unit mine board state is shares_subtype_with_it
    if 4553 amount_listed
    if 4670 keyword_condition
    if 4671 keyword_condition
    if 4549 event_count ge 2.0
    if 4553 have not unit mine board state is shares_subtype_with_it
    if 4553 amount_listed
    if 2798 have is self position is front_row
    if 2799 have is self position is back_row
    if 4670 have is self position is front_row
    if 4671 have is self position is back_row
    do 2797 own give_keyword self
    do 4553 uses_keyword stat_change self strength=listed
    do 2798 own damage unit enemy chosen board amount=2.0
    do 2799 own give_keyword unit enemy chosen board
    do 4549 uses_keyword kill unit enemy chosen board
    do 4669 own give_keyword self
    do 4553 uses_keyword stat_change self strength=listed
    do 4670 own damage unit enemy chosen board amount=2.0
    do 4671 own give_keyword unit enemy chosen board
    do 4549 uses_keyword kill unit enemy chosen board
    do 4553 has_keyword stat_change self strength=listed
  Ciaran aep Easnillen:
    when 2048 played self
    when 4523 always
    do 2048 own give_keyword unit chosen board
    do 4523 uses_keyword silence unit chosen board
    do 2048 own move unit it
  Naiad Pondkeeper:
    when 4034 played self
    when 4568 activated
    when 4035 played self
    when 4551 played card mine type is 26
    if 4034 keyword_condition
    if 4034 amount_stat strength unit mine chosen board card is 813637
    if 4568 amount_stat base_power it
    if 4035 keyword_condition
    if 4551 amount_count unit mine board keyword is 756204
    if 4034 have is self position is front_row
    if 4035 have is self position is back_row
    do 4034 own damage unit enemy chosen board amount=stat
    do 4034 own keyword_action unit mine chosen board card is 813637
    do 4568 uses_keyword stat_set unit mine chosen board card is 813637 strength=stat
    do 4035 own give_keyword unit mine chosen board keyword not 756204
    do 4551 uses_keyword summon unit mine
    do 4551 uses_keyword stat_set unit mine it card is 813637 strength=count
  Samum:
    when 2683 played self
    when 2684 killed
    do 2683 own damage unit chosen board amount=3.0
    do 2684 own move unit all board position is sides of it
  Dwarven Skirmisher:
    when 2071 played self
    when 4532 damaged self
    when 2072 activated self
    if 2071 keyword_condition
    if 4532 amount_listed
    if 2072 keyword_condition
    if 2071 have is self position is front_row
    if 2072 have is self keyword is 756174
    do 2071 own damage unit enemy chosen board amount=3.0
    do 2071 own give_keyword self amount=1.0
    do 4532 uses_keyword negate_damage self amount=listed
    do 2072 own damage unit enemy chosen board amount=3.0

## C39 lr_3.md 3 (CAUSE, open, 0 table lines from the same code)
Moving enemy units is linked to a card whose position need is about my own units' rows or neighbours; sides count as L9 says (L29).
- W gwent: Kerack City Guard -> Reinforced Trebuchet: is a Soldier it asks for; also Kerack City Guard moves enemy units, and Reinforced Trebuchet acts on units in the back row | network.py []
- R gwent: Amnesty -> Treason: Amnesty moves enemy units, and Treason acts on units next to its target | network.py []
- R gwent: Emhyr var Emreis -> Treason: Emhyr var Emreis moves enemy units, and Treason acts on units next to its target | network.py []
  Kerack City Guard:
    when 3410 always
    when 4519 always
    when 3411 activated self
    when 3412 turn_end
    when 4519 always
    when 4504 played self
    if 3412 event_count eq 0.0
    do 3410 own give_keyword self
    do 4519 uses_keyword cant self event=given_keyword
    do 3411 own move unit enemy chosen board
    do 3412 own stat_change self strength=1.0
    do 4519 has_keyword cant self event=given_keyword
    do 4504 has_keyword cant self event=activated;turns=1.0
  Reinforced Trebuchet:
    when 1932 turn_end
    when 1933 turn_end
    if 1932 keyword_condition
    if 1932 keyword_condition not
    if 1933 keyword_condition
    if 1933 keyword_condition
    if have is self position is back_row
    if count ge 2.0 unit mine board position is sides of self;type is 46
    if 1932 have is self position is back_row
    if 1932 count ge 2.0 unit mine board position is sides of self;type is 46
    if 1933 have is self position is back_row
    if 1933 count ge 2.0 unit mine board position is sides of self;type is 46
    do 1932 own damage unit enemy random board position is back_row amount=1.0
    do 1933 own damage unit enemy random board amount=1.0

## C40 lr_3.md 4 (CAUSE, open, 0 table lines from the same code)
Gwent's Summon is not considered played, so putting a unit into play from the deck does not set off a Deploy ("when I'm played") effect (L27).
- W gwent: Damsel in Distress -> Cintrian Knight: puts it into play from the deck; also enables: changes its stats for its effect | network.py [1600]
- R gwent: Ermion -> Ale of the Ancestors: NONE | network.py []
  Damsel in Distress:
    when 3874 always
    when 4517 leaves_play self
    when 3875 played unit mine type is 48
    when 3876 played self
    when 3877 keyword_used unit mine keyword is 756180
    when 3878 played unit mine type is 48
    when 4517 leaves_play self
    if 3877 stage 1.0
    if 3878 stage 2.0
    do 3874 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 3875 own stage_advance self
    do 3876 own summon card mine chosen deck state is bronze;type is 48
    do 3877 own stat_change unit mine all board position is sides of it strength=2.0
    do 3878 own create
    do 3878 own play_card card mine chosen hand card is 756956
    do 4517 has_keyword obliterate self
  Cintrian Knight:
    when 2765 played self
    when 2766 killed
    when 4534 turn_end
    when 2767 always
    if 2767 keyword_condition 6.0
    if stat strength ge listed self
    if 2767 stat strength ge listed self
    do 2765 own damage unit enemy chosen board amount=2.0
    do 2766 own give_keyword self amount=2.0
    do 4534 uses_keyword stat_change self strength=1.0
    do 2767 own stat_change self strength=2.0

## C41 lr_4.md 1 (CAUSE, open, 0 table lines from the same code)
A "move card ... hand/deck" (draw then put a card back, put on top of the deck) is a change of zone, not of a place on the board, so it is no mover for cards that act by row (L29: moves, pushes, pulls, swaps and units put at a place).
- W gwent: Cursed Scroll -> Redanian Archer: Cursed Scroll moves Redanian Archer, and Redanian Archer acts on units in the back row | network.py []
- W gwent: Dimun Pirate -> An Craite Longship: Dimun Pirate moves An Craite Longship, and An Craite Longship acts on units in the front row | network.py []
- W gwent: Maxii van Dekkar -> Courier: Maxii van Dekkar moves Courier, and Courier acts on units in the back row or in the front row | network.py []
- W gwent: Eavesdrop -> Whoreson's Freak Show: lets you gain the second resource (Bones); also Eavesdrop moves Whoreson's Freak Show, and Whoreson's Freak Show acts on units in the front row | network.py []
- R gwent: Malena -> Pavko Gale: Malena moves Pavko Gale, and Pavko Gale acts on units in the back row | network.py []
- R gwent: Ciaran aep Easnillen -> Freixenet: Ciaran aep Easnillen moves Freixenet, and Freixenet acts on units in the back row | network.py []
  Cursed Scroll:
    when 3156 activated self
    when 4504 played self
    do 3156 own draw card mine chosen deck amount=1.0
    do 3156 own move card mine chosen hand
    do 4504 has_keyword cant self event=activated;turns=1.0
  Redanian Archer:
    when 3036 always
    when 4510 played self
    when 3037 activated self
    when 3038 always
    when 4513 always
    when 3039 turn_end
    when 4513 always
    when 4510 played self
    when 4513 always
    if 3037 keyword_condition
    if 4513 amount_listed
    if 3039 keyword_condition
    if 4513 amount_listed
    if 4513 amount_listed
    if 3037 have is self position is back_row
    if 3039 have is self keyword is 756174
    do 3036 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 3037 own damage unit enemy chosen board amount=1.0
    do 3038 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 3039 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4510 has_keyword can self event=activated
    do 4513 has_keyword can self event=activated;times=listed
  Dimun Pirate:
    when 2139 played self
    if 2139 have not unit mine all board type is 59
    do 2139 own move card mine top deck
  An Craite Longship:
    when 2154 played unit enemy
    if 2154 keyword_condition
    if have is self position is front_row
    if 2154 have is self position is front_row
    do 2154 own damage unit enemy it amount=1.0
  Maxii van Dekkar:
    when 3487 played self
    do 3487 own look card mine all deck
    do 3487 own shuffle_into_deck card mine all deck
    do 3487 own move card mine chosen deck
  Courier:
    when 2824 played self
    when 2825 played self
    when 4672 played self
    when 4673 played self
    if 2824 keyword_condition
    if 2825 keyword_condition
    if 4672 keyword_condition
    if 4673 keyword_condition
    if 2824 have is self position is front_row
    if 2825 have is self position is back_row
    if 4672 have is self position is front_row
    if 4673 have is self position is back_row
    do 2824 own look card enemy deck_top
    do 2824 own choose_card card enemy chosen deck_top
    do 2824 own put_on_top card enemy it
    do 2825 own look card mine deck_top
    do 2825 own choose_card card mine chosen deck_top
    do 2825 own put_on_top card mine it
    do 4672 own look card enemy top deck
    do 4672 own put_on_top card enemy chosen deck
    do 4673 own look card mine top deck
    do 4673 own put_on_top card mine chosen deck
  Eavesdrop:
    when 2836 played self
    when 4676 played self
    do 2836 own mana_gain secondary_resource mine amount=5.0
    do 2836 own draw card mine deck_top amount=1.0
    do 2836 own move card mine chosen hand
    do 4676 own mana_gain secondary_resource mine amount=5.0
    do 4676 own draw card mine deck_top amount=1.0
    do 4676 own move card mine chosen hand
  Whoreson's Freak Show:
    when 2904 played self
    when 2905 activated self
    if 2905 keyword_condition
    if 2905 have is self position is front_row
    do 2904 own mana_gain secondary_resource mine amount=2.0
    do 2905 own spend_mana secondary_resource mine amount=2.0
    do 2905 own damage unit enemy chosen board amount=2.0

## C42 lr_4.md 2 (CAUSE, open, 0 table lines from the same code)
A card whose row condition is checked only when it is played gets nothing from a later move, so a mover is no help for it (L29: one must change a position, the other care; L2).
- W gwent: Guerilla Tactics -> Dwarven Skirmisher: Guerilla Tactics moves Dwarven Skirmisher, and Dwarven Skirmisher acts on units in the front row | network.py []
- W gwent: Guerilla Tactics -> Filavandrel aén Fidháil: Guerilla Tactics moves Filavandrel aén Fidháil, and Filavandrel aén Fidháil acts on units in the back row or in the front row | network.py []
- W gwent: Doadrick Leumaerts -> Alba Armored Cavalry: Doadrick Leumaerts moves Alba Armored Cavalry, and Alba Armored Cavalry acts on units in the front row | network.py []
- R gwent: Malena -> Treant Boar: Malena moves Treant Boar, and Treant Boar acts on units in the back row or in the front row | network.py []
- R gwent: Malena -> Pavko Gale: Malena moves Pavko Gale, and Pavko Gale acts on units in the back row | network.py []
  Guerilla Tactics:
    when 2369 activated self
    when 2370 always
    when 4513 always
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 4513 amount_listed
    do 2369 own move unit chosen board
    do 2369 own damage unit enemy it amount=1.0
    do 2369 own stat_change unit mine it strength=3.0
    do 2370 own give_keyword self amount=3.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Dwarven Skirmisher:
    when 2071 played self
    when 4532 damaged self
    when 2072 activated self
    if 2071 keyword_condition
    if 4532 amount_listed
    if 2072 keyword_condition
    if 2071 have is self position is front_row
    if 2072 have is self keyword is 756174
    do 2071 own damage unit enemy chosen board amount=3.0
    do 2071 own give_keyword self amount=1.0
    do 4532 uses_keyword negate_damage self amount=listed
    do 2072 own damage unit enemy chosen board amount=3.0
  Filavandrel aén Fidháil:
    when 3791 played self
    when 3792 played self
    if 3791 keyword_condition
    if 3792 keyword_condition
    if 3791 have is self position is front_row
    if 3792 have is self position is back_row
    do 3791 own create card mine random region is Scoiatael;cost eq 3560;category is spell
    do 3791 own play_card card mine it category is spell
    do 3792 own create card mine random region is Scoiatael;cost le 3561;category is spell
    do 3792 own play_card card mine it category is spell
  Doadrick Leumaerts:
    when 2883 played self
    when 4510 played self
    when 2884 activated self
    when 2885 always
    when 4511 activated self
    if 2883 have is unit mine all board type is 47
    if 2884 keyword_condition
    if 4511 amount_listed
    if 2884 have is self position is back_row
    do 2883 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2884 own draw card mine deck_top amount=1.0
    do 2884 own move card mine chosen hand
    do 2885 own keyword_action amount=1.0
    do 4511 uses_keyword cant event=activated;turns=listed
  Alba Armored Cavalry:
    when 2406 played self
    when 4523 always
    if 2406 keyword_condition
    if 2406 have is self position is front_row
    do 2406 own give_keyword unit enemy chosen board
    do 4523 uses_keyword silence unit enemy chosen board

## C43 lr_4.md 3 (CAUSE, open, 0 table lines from the same code)
A card that only lets units move (a unit moving itself, L23) is no mover, and a target card with no place act in its rows is no card that acts by place (L29).
- W faeria: Bloated Toad -> Animated Banquet: Bloated Toad moves your units, and Animated Banquet acts on units next to it | network.py []
- R into_the_breach: Titan Fist -> Air Strike: Titan Fist moves enemy units, and Air Strike acts on units on its space | network.py []
  Bloated Toad:
    when 1630 always
    when 1757 always
    when 1631 played self
    when 1757 always
    when 1757 always
    do 1630 own give_keyword self
    do 1757 uses_keyword can self event=moves
    do 1631 own summon power=2.0;health=2.0
    do 1631 own give_keyword unit mine it card is -2003
    do 1757 uses_keyword can unit mine it card is -2003 event=moves
    do 1631 own capture unit mine it card is -2003
    do 1757 has_keyword can self event=moves
  Animated Banquet:
    when 1638 always
    when 1759 played self
    when 1639 turn_end
    when 1759 played self
    if 1759 amount_event_amount
    if 1759 amount_event_amount
    do 1638 own give_keyword self amount=1.0
    do 1759 uses_keyword move self amount=event_amount
    do 1639 own capture self
    do 1639 own stat_change it power=1.0;health=1.0
    do 1759 has_keyword move self amount=event_amount

## C44 lr_5.md 1 (CAUSE, open, 0 table lines from the same code)
A move of a card in the deck or hand (to the top of the deck, from deck to hand) is read as a change of where units stand, and linked to cards that act by their row (L29: only moves, pushes, swaps and puts of units on the board change positions).
- W gwent: Maxii van Dekkar -> Sove: Maxii van Dekkar moves Sove, and Sove acts on units in the front row | network.py []
- W gwent: Fisher King -> Yennefer: Divination: Fisher King moves Yennefer: Divination, and Yennefer: Divination acts on units in the back row | network.py []
- W gwent: Cursed Scroll -> Lydia van Bredevoort: Cursed Scroll moves Lydia van Bredevoort, and Lydia van Bredevoort acts on units in the back row or in the front row | network.py []
- W gwent: Draig Bon-Dhu -> Tuirseach Axeman: Draig Bon-Dhu moves Tuirseach Axeman, and Tuirseach Axeman acts on units in the front row | network.py []
- R gwent: Ciaran aep Easnillen -> Cat Witcher Adept: Ciaran aep Easnillen moves Cat Witcher Adept and units, and Cat Witcher Adept acts on units in its target's row or in the back row or in the front row | network.py []
- R into_the_breach: Ramming Engines -> Refractor Laser: Ramming Engines moves enemy units, and Refractor Laser acts on units in a line from it | network.py []
  Maxii van Dekkar:
    when 3487 played self
    do 3487 own look card mine all deck
    do 3487 own shuffle_into_deck card mine all deck
    do 3487 own move card mine chosen deck
  Sove:
    when 4023 played self
    when 4024 dies self
    when 4537 always
    if 4023 keyword_condition
    if 4023 amount_count unit enemy all board state is damaged
    if 4024 amount_product
    if 4024 amount_stat base_power self
    if 4023 have is self position is front_row
    do 4023 own summon card mine chosen deck type is 43
    do 4023 own give_ability card mine it type is 43
    do 4024 gives stat_change unit enemy board card is 757381 strength=product
    do 4023 own damage card mine it type is 43 amount=count
    do 4023 own give_keyword self
    do 4537 uses_keyword cant player all event=targeted
  Fisher King:
    when 2663 played self
    if 2663 keyword_condition
    if 2663 have is self position is back_row
    do 2663 own move card mine chosen deck
  Yennefer: Divination:
    when 2571 played self
    when 4506 activated
    if 2571 keyword_condition
    if 2571 amount_stat strength unit mine it deck
    if 2571 have is self position is back_row
    do 2571 own keyword_action unit mine random deck
    do 4506 uses_keyword reveal unit mine random deck
    do 2571 own stat_change unit mine chosen board strength=stat
  Cursed Scroll:
    when 3156 activated self
    when 4504 played self
    do 3156 own draw card mine chosen deck amount=1.0
    do 3156 own move card mine chosen hand
    do 4504 has_keyword cant self event=activated;turns=1.0
  Lydia van Bredevoort:
    when 3778 played self
    when 3779 played self
    if 3778 keyword_condition
    if 3779 keyword_condition
    if 3778 have is self position is front_row
    if 3779 have is self position is back_row
    do 3778 own create card mine chosen hand state is bronze;category is spell;state is opponent_faction
    do 3778 own play_card card mine chosen hand state is created
    do 3779 own play_card card enemy chosen discard state is bronze;category is spell
  Draig Bon-Dhu:
    when 2111 played self
    when 2112 always
    when 4510 played self
    when 2113 activated self
    when 4544 round_start
    when 2114 always
    when 4511 activated self
    when 4510 played self
    when 4504 played self
    if 4544 event_count ge 2.0
    if 4511 amount_listed
    do 2111 own move unit mine chosen deck state is bronze;type is 45
    do 2112 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2113 own give_keyword unit mine chosen discard
    do 4544 uses_keyword base_change unit mine chosen discard strength=1.0
    do 2114 own keyword_action amount=1.0
    do 4511 uses_keyword cant event=activated;turns=listed
    do 4510 has_keyword can self event=activated
    do 4504 has_keyword cant self event=activated;turns=1.0
  Tuirseach Axeman:
    when 2152 played self
    if 2152 keyword_condition
    if 2152 amount_stat damage chosen
    if 2152 have is self position is front_row
    do 2152 own damage unit chosen board amount=stat

## C45 lr_5.md 2 (CAUSE, open, 0 table lines from the same code)
Own units moved or put next to a card that damages, silences or returns ALL units around it (mine too) is called a help; for the putting card this is a drawback, not a need (L29 "a card put where the need forbids it", L5, L9).
- W duelyst: Mist Dragon Seal -> Lightbender: Mist Dragon Seal moves your units, and Lightbender acts on units around it | network.py []
- W duelyst: Inquisitor Kron -> Lightbender: Inquisitor Kron puts your units there, and Lightbender acts on units around it | network.py []
- W duelyst: Star's Fury -> Lightbender: Star's Fury puts your units there, and Lightbender acts on units around it | network.py []
- W duelyst: Inquisitor Kron -> Sunset Paragon: Inquisitor Kron puts your units there, and Sunset Paragon acts on units around it | network.py []
- R duelyst: Inquisitor Kron -> Primus Fist: Inquisitor Kron puts your units there, and Primus Fist acts on units around it | network.py []
- R duelyst: Repulsor Beast -> Maw: Repulsor Beast moves enemy units, and Maw acts on units around it | network.py []
- R duelyst: Juxtaposition -> Lightbender: Juxtaposition moves units, and Lightbender acts on units around it | network.py []
  Mist Dragon Seal:
    when 104 played self
    do 104 own stat_change unit mine chosen board power=1.0;health=1.0
    do 104 own move unit mine it
  Lightbender:
    when 288 played self
    do 288 own silence position all position is surrounding
  Inquisitor Kron:
    when 896 shuffled card mine
    when 1098 always
    do 896 own summon power=2.0;health=2.0
    do 896 own give_random_keyword unit mine it card is 5000940
    do 1098 has_keyword cant any enemy all board position is surrounding of self event=moves
    do 1098 has_keyword cant any enemy all board position is surrounding of self event=attacks
  Star's Fury:
    when 155 played self
    when 1096 played self
    do 155 own summon
    do 1096 uses_keyword can unit mine it card is 5000146 event=moves
    do 1096 uses_keyword can unit mine it card is 5000146 event=attacks
  Sunset Paragon:
    when 777 played self
    if 777 amount_stat power it
    do 777 own damage unit all board position is surrounding amount=stat

## C46 lr_5.md 3 (CAUSE, open, 0 table lines from the same code)
"Ready" (move and attack again) is read as a card that changes positions; it moves nothing itself, the unit moves itself (L29, L23).
- W duelyst: Inner Focus -> Primus Fist: Inner Focus moves your units, and Primus Fist acts on units around it | network.py []
- W duelyst: Inner Focus -> Lightbender: Inner Focus moves your units, and Lightbender acts on units around it | network.py []
- R duelyst: Mist Dragon Seal -> Primus Fist: Mist Dragon Seal moves your units, and Primus Fist acts on units around it | network.py []
  Inner Focus:
    when 112 played self
    do 112 own ready unit mine chosen board power le 111
  Primus Fist:
    when 304 played self
    do 304 own stat_change unit mine chosen board position is surrounding power=2.0
  Lightbender:
    when 288 played self
    do 288 own silence position all position is surrounding

## C47 lr_5.md 4 (CAUSE, open, 0 table lines from the same code)
A Gwent card that puts a unit into play from the deck is linked to units whose effect is Deploy (played); a summoned unit is not played, so the Deploy does not go off (L27, L17).
- W gwent: Sove -> Little Havfrue: puts it into play from the deck | network.py []
- W gwent: Sove -> Raging Bear: puts it into play from the deck | network.py []
- R gwent: Forbidden Magic -> Kaedweni Revenant: summons | network.py [] | cases n549 line
  Sove:
    when 4023 played self
    when 4024 dies self
    when 4537 always
    if 4023 keyword_condition
    if 4023 amount_count unit enemy all board state is damaged
    if 4024 amount_product
    if 4024 amount_stat base_power self
    if 4023 have is self position is front_row
    do 4023 own summon card mine chosen deck type is 43
    do 4023 own give_ability card mine it type is 43
    do 4024 gives stat_change unit enemy board card is 757381 strength=product
    do 4023 own damage card mine it type is 43 amount=count
    do 4023 own give_keyword self
    do 4537 uses_keyword cant player all event=targeted
  Little Havfrue:
    when 3789 played self
    when 3790 activated self
    when 4522 turn_start
    when 4504 played self
    if 3789 keyword_condition
    if 3789 have is unit mine board state is copy_of_it
    do 3789 own base_change self strength=2.0
    do 3790 own damage self amount=4.0
    do 3790 own give_keyword position enemy chosen turns=2.0
    do 4522 uses_keyword damage unit random board position is same_row of self amount=1.0
    do 4504 has_keyword cant self event=activated;turns=1.0
  Raging Bear:
    when 2164 played self
    when 4614 played self
    do 2164 own damage unit mine chosen board amount=2.0
    do 4614 own damage unit mine chosen board amount=2.0

## C48 lr_6.md 1 (CAUSE, open, 0 table lines from the same code)
An area card that hurts or silences every unit around it (both sides) is counted as an "acts on units there" help for cards that put MY units there; a player would not place his own units into it (drawback L5, sides L9, L29).
- W duelyst: Conscript -> Aperion's Claim: Conscript puts your units there, and Aperion's Claim acts on units in a 3x3 area around it | network.py []
- W duelyst: Arcane Heart -> Sunset Paragon: Arcane Heart puts your units there, and Sunset Paragon acts on units around it | network.py []
- W duelyst: Prominence -> Lightbender: Prominence puts your units there, and Lightbender acts on units around it | network.py []
- W duelyst: Inquisitor Kron -> Necrotic Sphere: Inquisitor Kron puts your units there, and Necrotic Sphere acts on units around your leader or base | network.py []
- R duelyst: Daemonic Lure -> Sunset Paragon: Daemonic Lure moves enemy units, and Sunset Paragon acts on units around it | network.py []
- R duelyst: Repulsor Beast -> Sunset Paragon: Repulsor Beast moves enemy units, and Sunset Paragon acts on units around it | network.py []
  Conscript:
    when 58 played self
    do 58 own summon power=1.0;health=2.0
  Aperion's Claim:
    when 488 played self
    do 488 own kill unit all board position is area_3x3
    do 488 own set_terrain position all position is area_3x3
  Arcane Heart:
    when 97 played self
    do 97 own summon
  Sunset Paragon:
    when 777 played self
    if 777 amount_stat power it
    do 777 own damage unit all board position is surrounding amount=stat
  Prominence:
    when 946 played spell mine keyword is 5001113
    do 946 own summon
  Lightbender:
    when 288 played self
    do 288 own silence position all position is surrounding
  Inquisitor Kron:
    when 896 shuffled card mine
    when 1098 always
    do 896 own summon power=2.0;health=2.0
    do 896 own give_random_keyword unit mine it card is 5000940
    do 1098 has_keyword cant any enemy all board position is surrounding of self event=moves
    do 1098 has_keyword cant any enemy all board position is surrounding of self event=attacks
  Necrotic Sphere:
    when 27 played self
    do 27 own kill unit all board position is surrounding of player mine;of:kind is player
    do 27 own summon

## C49 lr_6.md 2 (CAUSE, open, 0 table lines from the same code)
A lane card whose own text destroys my other units in the lane (Deathlok: "kill mine all same_lane") is treated as a card that wants units put into its lane; the kill is a drawback, not a need (L29, L5).
- W marvel_snap: Bucky Barnes -> Deathlok: Bucky Barnes puts your units there, and Deathlok acts on units in its lane | network.py []
- W marvel_snap: Arnim Zola -> Deathlok: Arnim Zola puts your units there, and Deathlok acts on units in its lane | network.py []
- R marvel_snap: Bucky Barnes -> Venom: Bucky Barnes puts your units there, and Venom acts on units in its lane | network.py []
- R marvel_snap: Arnim Zola -> Carnage: Arnim Zola puts your units there, and Carnage acts on units in its lane | network.py []
  Bucky Barnes:
    when 5863 dies self
    do 5863 own summon
  Deathlok:
    when 5905 played self
    do 5905 own kill unit mine all board position is same_lane;card not 8000118
  Arnim Zola:
    when 5829 played self
    do 5829 own kill unit mine chosen board position is same_lane;card not 8000034
    do 5829 own copy unit mine it card not 8000034

## C50 lr_6.md 3 (CAUSE, open, 0 table lines from the same code)
"ready" a unit (Assassination Protocol, Inner Focus) is said as "moves your units", but ready only lets a unit move and attack again; it changes no position, so it is no placer (L29: moving, pushing, pulling, swapping, putting).
- W duelyst: Assassination Protocol -> Lightbender: Assassination Protocol moves your units, and Lightbender acts on units around it | network.py []
- W duelyst: Assassination Protocol -> Primus Fist: Assassination Protocol moves your units, and Primus Fist acts on units around it | network.py []
- W duelyst: Inner Focus -> Sunset Paragon: Inner Focus moves your units, and Sunset Paragon acts on units around it | network.py []
- R duelyst: Blink -> Sunset Paragon: Blink moves your units, and Sunset Paragon acts on units around it | network.py []
- R duelyst: Juxtaposition -> Maw: Juxtaposition moves enemy units, and Maw acts on units around it | network.py []
  Assassination Protocol:
    when 974 played self
    do 974 own ready unit mine chosen board
    do 974 own cant unit mine it event=attacks
  Lightbender:
    when 288 played self
    do 288 own silence position all position is surrounding
  Primus Fist:
    when 304 played self
    do 304 own stat_change unit mine chosen board position is surrounding power=2.0
  Inner Focus:
    when 112 played self
    do 112 own ready unit mine chosen board power le 111
  Sunset Paragon:
    when 777 played self
    if 777 amount_stat power it
    do 777 own damage unit all board position is surrounding amount=stat

## C51 lr_7.md 1 (CAUSE, open, 0 table lines from the same code)
A card that swaps or moves only itself is read as a mover of units, and gets lines to cards that act by place (L23, L29: a unit moving itself is no line).
- W duelyst: Hearth-Sister -> Icy: Hearth-Sister moves enemy units, and Icy acts on units around it | network.py []
- W duelyst: Hearth-Sister -> Sunset Paragon: Hearth-Sister moves units, and Sunset Paragon acts on units around it | network.py []
- R marvel_snap: Magneto -> Shang-Chi: Magneto moves enemy units, and Shang-Chi acts on units in its lane | network.py []
- R duelyst: Daemonic Lure -> Blood Siren: Daemonic Lure moves enemy units, and Blood Siren acts on units around it | network.py []
  Hearth-Sister:
    when 249 played self
    do 249 own swap self
  Icy:
    when 871 played self
    when 1086 always
    do 871 own give_keyword unit enemy chosen board position is surrounding
    do 1086 uses_keyword cant unit enemy chosen board position is surrounding event=moves
    do 1086 uses_keyword cant unit enemy chosen board position is surrounding event=attacks
  Sunset Paragon:
    when 777 played self
    if 777 amount_stat power it
    do 777 own damage unit all board position is surrounding amount=stat

## C52 lr_7.md 2 (CAUSE, open, 0 table lines from the same code)
Putting my own units next to a card whose effect hits every side (damage or kill on all units around it) is read as help, but it only harms my own units (L9, L5 drawback; L29 sides).
- W duelyst: Allomancer -> Sunset Paragon: Allomancer puts your units there, and Sunset Paragon acts on units around it | network.py []
- W duelyst: Pax -> Sunset Paragon: Pax puts your units there, and Sunset Paragon acts on units around it | network.py []
- W duelyst: Prominence -> Aperion's Claim: Prominence puts your units there, and Aperion's Claim acts on units in a 3x3 area around it | network.py []
- W duelyst: Inquisitor Kron -> Frostbone Naga: Inquisitor Kron puts your units there, and Frostbone Naga acts on units around it | network.py []
- R marvel_snap: Jubilee -> Iron Man: Jubilee puts your units there, and Iron Man acts on units in its lane | network.py []
  Allomancer:
    when 829 dies self
    do 829 own summon unit random board name_has is 1
  Sunset Paragon:
    when 777 played self
    if 777 amount_stat power it
    do 777 own damage unit all board position is surrounding amount=stat
  Pax:
    when 826 dies self
    do 826 own summon power=2.0;health=2.0;amount=2.0
  Prominence:
    when 946 played spell mine keyword is 5001113
    do 946 own summon
  Aperion's Claim:
    when 488 played self
    do 488 own kill unit all board position is area_3x3
    do 488 own set_terrain position all position is area_3x3
  Inquisitor Kron:
    when 896 shuffled card mine
    when 1098 always
    do 896 own summon power=2.0;health=2.0
    do 896 own give_random_keyword unit mine it card is 5000940
    do 1098 has_keyword cant any enemy all board position is surrounding of self event=moves
    do 1098 has_keyword cant any enemy all board position is surrounding of self event=attacks
  Frostbone Naga:
    when 307 played self
    do 307 own damage any all board position is surrounding amount=2.0

## C53 lr_7.md 3 (CAUSE, open, 0 table lines from the same code)
A card that only lets my unit move (a "can move" keyword) or moves my own unit next to a card that silences or returns everything around it is read as a placer, but it gives no help (L23: a unit moving itself; L9; own unit is silenced).
- W duelyst: Scion's Third Wish -> Sandswirl Reader: Scion's Third Wish moves your units, and Sandswirl Reader acts on units around it | network.py []
- W duelyst: Blink -> Lightbender: Blink moves your units, and Lightbender acts on units around it | network.py []
- R stormbound: Ozone Purifiers -> Wild Saberpaws: Ozone Purifiers moves enemy units, and Wild Saberpaws acts on units around it or next to it | network.py [] | cases n22 line
  Scion's Third Wish:
    when 152 played self
    when 1067 always
    do 152 own stat_change unit mine chosen board type is 3 power=3.0;health=3.0
    do 152 own give_keyword unit mine it type is 3
    do 1067 uses_keyword can unit mine it type is 3 event=moves
  Sandswirl Reader:
    when 518 played self
    do 518 own return_to_hand unit chosen board position is surrounding
    do 518 own set_terrain position position is same_space of it
  Blink:
    when 96 played self
    do 96 own move unit mine chosen board max=2.0
  Lightbender:
    when 288 played self
    do 288 own silence position all position is surrounding

## C54 lr_7.md 4 (CAUSE, open, 0 table lines from the same code)
An enemy card summoned from a random deck (no place chosen, and the doer kills it itself), or an enemy moved into the lane of a card that forbids deaths there, is read as a position line (L29: a unit put on a random space, a card put where the need forbids it, Professor X).
- W marvel_snap: Gladiator -> Shang-Chi: Gladiator puts enemy units there, and Shang-Chi acts on units in its lane | network.py []
- W marvel_snap: Spider-Man -> Professor X: Spider-Man moves enemy units, and Professor X acts on units in its lane | network.py []
- R marvel_snap: Spider-Man -> Shang-Chi: Spider-Man moves enemy units, and Shang-Chi acts on units in its lane | network.py []
- R marvel_snap: Polaris -> Enchantress: Polaris moves enemy units, and Enchantress acts on units in its lane | network.py []
  Gladiator:
    when 5987 played self
    do 5987 own summon card enemy random deck
    do 5987 own kill unit enemy it board power lt 5802
  Shang-Chi:
    when 6283 played self
    do 6283 own kill unit enemy chosen board position is same_lane;power ge 6126
  Spider-Man:
    when 6325 played self
    do 6325 own move self
    do 6325 own move unit enemy chosen board position is same_lane
  Professor X:
    when 6210 always
    do 6210 own cant card all hand event=played
    do 6210 own cant card all event=summoned
    do 6210 own cant unit all board position is same_lane event=dies

## C55 lr_8.md 1 (CAUSE, open, 0 table lines from the same code)
A card that moves a card in hand or deck is read as "moves units", but no unit changes its place, so it cannot feed a card that acts by row or position (L29, L1).
- W gwent: Dimun Pirate -> Tidecloak Hideaway: is a Pirate it asks for; also Dimun Pirate moves Tidecloak Hideaway, and Tidecloak Hideaway acts on units in the back row | network.py []
- W gwent: Cursed Scroll -> Dwimveandra: Cursed Scroll moves Dwimveandra, and Dwimveandra acts on units in the back row or in the front row | network.py []
- W gwent: Eavesdrop -> Kurt: Eavesdrop moves Kurt, and Kurt acts on units in the back row or in the front row | network.py []
- W gwent: Maxii van Dekkar -> Alba Armored Cavalry: Maxii van Dekkar moves Alba Armored Cavalry, and Alba Armored Cavalry acts on units in the front row | network.py []
- R gwent: Making a Bomb -> Madoc: Making a Bomb moves enemy units, and Madoc acts on units in the row facing it; also triggers: is a Bomb whose playing sets off its effect; also moves into place | network.py [1933, 2313]
- R duelyst: Repulsor Beast -> Necrotic Sphere: Repulsor Beast moves enemy units, and Necrotic Sphere acts on units around your leader or base | network.py []
  Dimun Pirate:
    when 2139 played self
    if 2139 have not unit mine all board type is 59
    do 2139 own move card mine top deck
  Tidecloak Hideaway:
    when 2893 played self
    if 2893 keyword_condition
    if 2893 amount_count card mine all hand type is 60
    if 2893 have is self position is back_row
    do 2893 own stat_change unit mine chosen board strength=count
  Cursed Scroll:
    when 3156 activated self
    when 4504 played self
    do 3156 own draw card mine chosen deck amount=1.0
    do 3156 own move card mine chosen hand
    do 4504 has_keyword cant self event=activated;turns=1.0
  Dwimveandra:
    when 3775 played self
    when 3776 played self
    if 3775 keyword_condition
    if 3775 amount_full
    if 3776 keyword_condition
    if 3775 have is self position is front_row
    if 3776 have is self position is back_row
    do 3775 own stage_advance landmark mine chosen board type is 14 amount=full
    do 3776 own refresh landmark mine chosen board type is 17
  Eavesdrop:
    when 2836 played self
    when 4676 played self
    do 2836 own mana_gain secondary_resource mine amount=5.0
    do 2836 own draw card mine deck_top amount=1.0
    do 2836 own move card mine chosen hand
    do 4676 own mana_gain secondary_resource mine amount=5.0
    do 4676 own draw card mine deck_top amount=1.0
    do 4676 own move card mine chosen hand
  Kurt:
    when 2841 played self
    when 4561 dies self
    when 4562 obliterated self
    when 2842 played self
    when 4536 activated
    if 2841 keyword_condition
    if 4561 amount_stat base_power self
    if 4562 amount_stat base_power self
    if 2842 keyword_condition
    if 2841 have is self position is front_row
    if 2842 have is self position is back_row
    do 2841 own give_keyword unit enemy chosen board
    do 4561 uses_keyword mana_gain secondary_resource enemy amount=stat
    do 4562 uses_keyword mana_gain secondary_resource enemy amount=stat
    do 2842 own keyword_action unit chosen board
    do 4536 uses_keyword remove_keywords unit chosen board
  Maxii van Dekkar:
    when 3487 played self
    do 3487 own look card mine all deck
    do 3487 own shuffle_into_deck card mine all deck
    do 3487 own move card mine chosen deck
  Alba Armored Cavalry:
    when 2406 played self
    when 4523 always
    if 2406 keyword_condition
    if 2406 have is self position is front_row
    do 2406 own give_keyword unit enemy chosen board
    do 4523 uses_keyword silence unit enemy chosen board

## C56 lr_8.md 2 (CAUSE, open, 0 table lines from the same code)
A unit that moves or swaps only itself, or a ready that only lets a unit act again, is read as a card that changes positions (L23, L29).
- W duelyst: Hearth-Sister -> Zen'Rui, the Blightspawned: Hearth-Sister moves enemy units, and Zen'Rui, the Blightspawned acts on units around it | network.py []
- W duelyst: Assassination Protocol -> Sunset Paragon: Assassination Protocol moves your units, and Sunset Paragon acts on units around it | network.py []
- R duelyst: Blink -> Primus Fist: Blink moves your units, and Primus Fist acts on units around it | network.py []
- R stormbound: Windmakers -> Minion Launchers: Windmakers moves enemy units, and Minion Launchers acts on units first in front of it | network.py []
  Hearth-Sister:
    when 249 played self
    do 249 own swap self
  Zen'Rui, the Blightspawned:
    when 348 played self
    do 348 own steal unit enemy chosen board position is surrounding;power le 361
  Assassination Protocol:
    when 974 played self
    do 974 own ready unit mine chosen board
    do 974 own cant unit mine it event=attacks
  Sunset Paragon:
    when 777 played self
    if 777 amount_stat power it
    do 777 own damage unit all board position is surrounding amount=stat

## C57 lr_8.md 3 (CAUSE, open, 0 table lines from the same code)
My units put next to an effect that hits or silences or kills every unit around it are read as a help, but the effect hurts the put units, a drawback and no need (L29, L5, L9).
- W duelyst: Dark Transformation -> Lightbender: Dark Transformation puts your units there, and Lightbender acts on units around it | network.py []
- W duelyst: Dark Transformation -> Sunset Paragon: Dark Transformation puts your units there, and Sunset Paragon acts on units around it | network.py []
- W duelyst: Pax -> Frostbone Naga: Pax puts your units there, and Frostbone Naga acts on units around it | network.py []
- W duelyst: Inquisitor Kron -> Aperion's Claim: Inquisitor Kron puts your units there, and Aperion's Claim acts on units in a 3x3 area around it | network.py []
- R duelyst: Necrotic Sphere -> Shiro Puppydragon: Necrotic Sphere puts your units there, and Shiro Puppydragon acts on units around it | network.py []
- R duelyst: Repulsor Beast -> Necrotic Sphere: Repulsor Beast moves enemy units, and Necrotic Sphere acts on units around your leader or base | network.py []
  Dark Transformation:
    when 192 played self
    do 192 own kill unit enemy chosen board
    do 192 own summon power=1.0;health=1.0
  Lightbender:
    when 288 played self
    do 288 own silence position all position is surrounding
  Sunset Paragon:
    when 777 played self
    if 777 amount_stat power it
    do 777 own damage unit all board position is surrounding amount=stat
  Pax:
    when 826 dies self
    do 826 own summon power=2.0;health=2.0;amount=2.0
  Frostbone Naga:
    when 307 played self
    do 307 own damage any all board position is surrounding amount=2.0
  Inquisitor Kron:
    when 896 shuffled card mine
    when 1098 always
    do 896 own summon power=2.0;health=2.0
    do 896 own give_random_keyword unit mine it card is 5000940
    do 1098 has_keyword cant any enemy all board position is surrounding of self event=moves
    do 1098 has_keyword cant any enemy all board position is surrounding of self event=attacks
  Aperion's Claim:
    when 488 played self
    do 488 own kill unit all board position is area_3x3
    do 488 own set_terrain position all position is area_3x3

## C58 lr_8.md 4 (CAUSE, open, 0 table lines from the same code)
My units put near an effect that only hits enemies around its target are read as a help, but my units are no part of what that effect needs (L29, L9).
- W duelyst: Prominence -> Holy Immolation: Prominence puts your units there, and Holy Immolation acts on units around its target | network.py []
- W duelyst: Sky Phalanx -> Holy Immolation: Sky Phalanx puts your units there, and Holy Immolation acts on units around its target | network.py []
- W into_the_breach: Targeted Strike -> Tri-Rocket: Targeted Strike puts your units there, and Tri-Rocket acts on units in a line from it | network.py []
- R into_the_breach: Control Shot -> Rail Cannon: Control Shot moves enemy units, and Rail Cannon acts on units in a line from it | network.py []
- R into_the_breach: Titan Fist -> Electric Whip: Titan Fist moves enemy units, and Electric Whip acts on units next to it or next to its target | network.py []
  Prominence:
    when 946 played spell mine keyword is 5001113
    do 946 own summon
  Holy Immolation:
    when 73 played self
    do 73 own heal unit mine chosen board amount=4.0
    do 73 own damage any enemy all board position is surrounding of it amount=4.0
  Sky Phalanx:
    when 808 played self
    do 808 own summon amount=3.0
  Targeted Strike:
    when 5430 attacks
    do 5430 own summon
    do 5430 own damage unit_or_structure all position is same_space of it amount=1.0
  Tri-Rocket:
    when 5354 attacks
    when 5355 attacks
    when 5356 attacks
    if 5355 upgraded 1.0
    if 5356 upgraded 2.0
    do 5354 own damage unit_or_structure nearest position is straight_line of self amount=1.0
    do 5354 own move unit_or_structure nearest position is straight_line of self
    do 5355 own damage unit_or_structure nearest position is straight_line of self amount=1.0
    do 5356 own cant self event=strikes

## C59 lr_8.md 5 (CAUSE, open, 0 table lines from the same code)
A card is said to "act on units around it" when its rows show no act by place at all (only merge self or a self attack), so there is nothing for a placer to feed (L29).
- W marvel_snap: Bucky Barnes -> Hulkbuster: Bucky Barnes puts your units there, and Hulkbuster acts on units in its lane | network.py []
- W duelyst: Grimes -> Lavaslasher: Grimes puts your units there, and Lavaslasher acts on units around it | network.py []
- R marvel_snap: Bucky Barnes -> Arnim Zola: Bucky Barnes puts your units there, and Arnim Zola acts on units in its lane | network.py []
- R marvel_snap: Mysterio -> Carnage: Mysterio puts your units there, and Carnage acts on units in its lane | network.py []
  Bucky Barnes:
    when 5863 dies self
    do 5863 own summon
  Hulkbuster:
    when 6016 played self
    do 6016 own merge self
  Grimes:
    when 936 played self
    when 937 dies self
    do 936 own summon unit random board state is has_subtype
    do 937 own summon unit random board state is has_subtype
  Lavaslasher:
    when 919 played self
    do 919 own start_attack self

## C60 lr_9.md 1 (CAUSE, open, 0 table lines from the same code)
a card drawn, tutored or moved from deck to hand is a zone change, not a change of where units stand, so "moves" gives no line to a card that cares about its row (L29, L1b).
- W gwent: Cursed Scroll -> Orchard Mantrap: Cursed Scroll moves Orchard Mantrap, and Orchard Mantrap acts on units in the back row or in the front row | network.py []
- W gwent: Fisher King -> Alba Armored Cavalry: Fisher King moves Alba Armored Cavalry, and Alba Armored Cavalry acts on units in the front row | network.py []
- W gwent: Myrgtabrakke -> Filavandrel aén Fidháil: Myrgtabrakke moves Filavandrel aén Fidháil, and Filavandrel aén Fidháil acts on units in the back row or in the front row | network.py []
- W gwent: Doadrick Leumaerts -> Yennefer: Divination: Doadrick Leumaerts moves Yennefer: Divination, and Yennefer: Divination acts on units in the back row | network.py []
- R gwent: Ciaran aep Easnillen -> Cat Witcher Adept: Ciaran aep Easnillen moves Cat Witcher Adept and units, and Cat Witcher Adept acts on units in its target's row or in the back row or in the front row | network.py []
  Cursed Scroll:
    when 3156 activated self
    when 4504 played self
    do 3156 own draw card mine chosen deck amount=1.0
    do 3156 own move card mine chosen hand
    do 4504 has_keyword cant self event=activated;turns=1.0
  Orchard Mantrap:
    when 3899 played self
    when 4538 activated
    when 4516 activated
    when 3900 always
    when 3901 played self
    when 4540 played unit mine strength gt 4192
    if 3899 keyword_condition
    if 4538 amount_stat strength it
    if 3901 keyword_condition
    if 4540 amount_listed
    if 3899 have is self position is front_row
    if 3901 have is self position is back_row
    do 3899 own keyword_action unit mine chosen board
    do 4538 uses_keyword kill unit mine chosen board
    do 4538 uses_keyword stat_change unit mine chosen board strength=stat
    do 4538 uses_keyword keyword_action unit mine chosen board
    do 4516 uses_keyword obliterate unit mine chosen board
    do 3900 own increase_effect self amount=1.0
    do 3901 own give_keyword unit mine chosen board
    do 4540 uses_keyword stat_change unit mine chosen board strength=listed
  Fisher King:
    when 2663 played self
    if 2663 keyword_condition
    if 2663 have is self position is back_row
    do 2663 own move card mine chosen deck
  Alba Armored Cavalry:
    when 2406 played self
    when 4523 always
    if 2406 keyword_condition
    if 2406 have is self position is front_row
    do 2406 own give_keyword unit enemy chosen board
    do 4523 uses_keyword silence unit enemy chosen board
  Myrgtabrakke:
    when 1801 always
    when 4507 game_start
    when 1802 played self
    when 1803 activated self
    when 1804 always
    when 4513 always
    when 1805 game_start
    when 4513 always
    when 4507 game_start
    when 4513 always
    when 4504 played self
    if 4507 amount_count card mine type is 38;state is started_in_deck
    if 4513 amount_listed
    if 1805 amount_count card mine all deck type is 38;state is started_in_deck
    if 4513 amount_listed
    if 4507 amount_count card mine type is 38;state is started_in_deck
    if 4513 amount_listed
    do 1801 own give_keyword self
    do 4507 uses_keyword stat_change self strength=count
    do 1802 own draw card mine deck type is 38 amount=1.0
    do 1802 own move card mine chosen hand
    do 1803 own damage unit enemy chosen board amount=1.0
    do 1804 own give_keyword self amount=0.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 1805 own give_keyword self amount=count
    do 4513 uses_keyword can self event=activated;times=listed
    do 4507 has_keyword stat_change self strength=count
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Filavandrel aén Fidháil:
    when 3791 played self
    when 3792 played self
    if 3791 keyword_condition
    if 3792 keyword_condition
    if 3791 have is self position is front_row
    if 3792 have is self position is back_row
    do 3791 own create card mine random region is Scoiatael;cost eq 3560;category is spell
    do 3791 own play_card card mine it category is spell
    do 3792 own create card mine random region is Scoiatael;cost le 3561;category is spell
    do 3792 own play_card card mine it category is spell
  Doadrick Leumaerts:
    when 2883 played self
    when 4510 played self
    when 2884 activated self
    when 2885 always
    when 4511 activated self
    if 2883 have is unit mine all board type is 47
    if 2884 keyword_condition
    if 4511 amount_listed
    if 2884 have is self position is back_row
    do 2883 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2884 own draw card mine deck_top amount=1.0
    do 2884 own move card mine chosen hand
    do 2885 own keyword_action amount=1.0
    do 4511 uses_keyword cant event=activated;turns=listed
  Yennefer: Divination:
    when 2571 played self
    when 4506 activated
    if 2571 keyword_condition
    if 2571 amount_stat strength unit mine it deck
    if 2571 have is self position is back_row
    do 2571 own keyword_action unit mine random deck
    do 4506 uses_keyword reveal unit mine random deck
    do 2571 own stat_change unit mine chosen board strength=stat

## C61 lr_9.md 2 (CAUSE, open, 0 table lines from the same code)
units put or copied where B's area effect hits all units (mine too), or where B's need forbids more units, is a drawback, no help (L29, L5).
- W duelyst: Sky Phalanx -> Aperion's Claim: Sky Phalanx puts your units there, and Aperion's Claim acts on units in a 3x3 area around it | network.py []
- W duelyst: Star's Fury -> Frostbone Naga: Star's Fury puts your units there, and Frostbone Naga acts on units around it | network.py []
- W gwent: Mobilization -> Sabrina Glevissig: Mobilization puts your units there, and Sabrina Glevissig acts on units in its row | network.py []
- W marvel_snap: Ultron -> Galactus: Ultron puts your units there, and Galactus acts on units in its lane | network.py []
- R duelyst: Whisper of the Sands -> Orbrider: Whisper of the Sands puts your units there, and Orbrider acts on units around it | network.py []
- R marvel_snap: Dragon Lord -> En Sabah Nur: Dragon Lord puts your units there, and En Sabah Nur acts on units in the front row | network.py []
  Sky Phalanx:
    when 808 played self
    do 808 own summon amount=3.0
  Aperion's Claim:
    when 488 played self
    do 488 own kill unit all board position is area_3x3
    do 488 own set_terrain position all position is area_3x3
  Star's Fury:
    when 155 played self
    when 1096 played self
    do 155 own summon
    do 1096 uses_keyword can unit mine it card is 5000146 event=moves
    do 1096 uses_keyword can unit mine it card is 5000146 event=attacks
  Frostbone Naga:
    when 307 played self
    do 307 own damage any all board position is surrounding amount=2.0
  Mobilization:
    when 2373 activated self
    when 4504 played self
    do 2373 own copy unit mine chosen board state is bronze;type is 46
    do 2373 own stat_change unit mine it type is 46 strength=3.0
    do 2373 own stat_change unit mine it state is created strength=3.0
    do 4504 has_keyword cant self event=activated;turns=1.0
  Sabrina Glevissig:
    when 1891 always
    when 4527 always
    when 4528 played self
    when 4569 always
    when 1892 dies self
    when 4577 always
    when 4527 always
    when 4528 played self
    when 4569 always
    when 4578 dies self
    when 4527 always
    when 4528 played self
    when 4569 always
    do 1891 own give_keyword self
    do 4527 uses_keyword can self event=summoned
    do 4528 uses_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
    do 1892 own damage unit all board position is same_row of self amount=3.0
    do 4577 own give_keyword self
    do 4527 uses_keyword can self event=summoned
    do 4528 uses_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
    do 4578 own damage unit all board position is same_row amount=3.0
    do 4527 has_keyword can self event=summoned
    do 4528 has_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
  Ultron:
    when 6408 played self
    do 6408 own summon power=2.0;amount=4.0
  Galactus:
    when 5973 played self
    if 5973 amount gt stat
    if 5973 count eq 1.0 unit mine board position is same_lane
    if 5973 amount_stat power position enemy position is same_lane
    if 5973 amount_stat power position mine position is same_lane
    do 5973 own kill position all position not same_lane
    do 5973 own kill unit all board position not same_lane

## C62 lr_9.md 3 (CAUSE, open, 0 table lines from the same code)
a place line was given to a card whose rows show no place at all (only "start_attack self" or "merge self"), and a unit put on a random space gives none (L29, L23).
- W duelyst: Juggernaut -> Lavaslasher: Juggernaut puts your units there, and Lavaslasher acts on units around it | network.py []
- W duelyst: Fractal Replication -> Lavaslasher: Fractal Replication puts your units there, and Lavaslasher acts on units around it | network.py []
- W marvel_snap: Heimdall -> Hulkbuster: Heimdall moves your units, and Hulkbuster acts on units in its lane | network.py [1610]
- W marvel_snap: Arnim Zola -> Hulkbuster: Arnim Zola puts your units there, and Hulkbuster acts on units in its lane | network.py []
- R marvel_snap: Dragon Lord -> En Sabah Nur: Dragon Lord puts your units there, and En Sabah Nur acts on units in the front row | network.py []
  Juggernaut:
    when 922 turn_start
    when 923 damaged self
    if 923 amount_event_amount
    do 922 own stat_change self power=5.0;health=5.0
    do 923 own summon unit random board type is 6;name_has is 3 amount=event_amount
  Lavaslasher:
    when 919 played self
    do 919 own start_attack self
  Fractal Replication:
    when 220 played self
    do 220 own copy unit mine chosen board amount=2.0
  Heimdall:
    when 6002 played self
    do 6002 own move unit mine all board card not 8000236
  Hulkbuster:
    when 6016 played self
    do 6016 own merge self
  Arnim Zola:
    when 5829 played self
    do 5829 own kill unit mine chosen board position is same_lane;card not 8000034
    do 5829 own copy unit mine it card not 8000034

## C63 lr_9.md 4 (CAUSE, open, 0 table lines from the same code)
enemy units put on the enemy side, a copy put into hand, or a unit put away from my leader do not help a need about the area around my own leader or my own board (L9, L19, L29).
- W duelyst: Reaper of the Nine Moons -> Necrotic Sphere: Reaper of the Nine Moons puts enemy units there, and Necrotic Sphere acts on units around your leader or base | network.py []
- W duelyst: Dark Transformation -> Necrotic Sphere: Dark Transformation puts your units there, and Necrotic Sphere acts on units around your leader or base | network.py []
- W gwent: Operator -> Assassination: Operator puts enemy units there, and Assassination acts on units next to its target | network.py []
- W duelyst: White Asp -> Spirit of the Wild: White Asp puts your units there, and Spirit of the Wild acts on units base's starting side or on the enemy leader | network.py []
- R gwent: Nightwraith -> Slyzard: Nightwraith puts your units there, and Slyzard acts on units in its row | network.py []
  Reaper of the Nine Moons:
    when 172 dies self
    when 1067 always
    do 172 own summon unit enemy random deck
    do 1067 has_keyword can self event=moves
  Necrotic Sphere:
    when 27 played self
    do 27 own kill unit all board position is surrounding of player mine;of:kind is player
    do 27 own summon
  Dark Transformation:
    when 192 played self
    do 192 own kill unit enemy chosen board
    do 192 own summon power=1.0;health=1.0
  Operator:
    when 1812 played self
    do 1812 own copy unit mine chosen hand state is bronze;state is created
    do 1812 own copy unit mine chosen hand state is bronze;state is created
  Assassination:
    when 2329 played self
    when 4637 played self
    if 2329 amount_count unit all board position is sides of it;keyword not 9000001
    if 2329 amount_minus
    if 2329 amount_sum
    if 4637 amount_minus
    if 4637 amount_sum
    if 4637 amount_count unit all board position is sides of it;keyword not 9000001
    do 2329 own damage unit chosen board amount=sum
    do 4637 own damage unit chosen board amount=sum
  White Asp:
    when 882 always
    when 883 killed unit
    do 882 own stat_change player mine power=3.0
    do 883 own summon power=3.0;health=3.0
  Spirit of the Wild:
    when 276 played self
    do 276 own ready unit mine all board position is starting_side of player enemy;of:kind is player

## C64 lr_1.md 2 (CAUSE, gone, 0 table lines from the same code)
Gwent Zeal only lets an Order be used the turn the unit is placed, so playing the unit sets off nothing (L27); the line "plays it: its effect goes off" is wrong where the card's only "played" row is Zeal.
- W gwent: Call of the Forest -> Freixenet: NONE | network.py []
- W gwent: Oneiromancy -> Crow Clan Druid: NONE | network.py []
- W gwent: Amphibious Assault -> Margarita Laux-Antille: NONE | network.py []
- W gwent: Joachim de Wett -> Impera Enforcers: NONE | network.py []

## C65 lr_1.md 4 (CAUSE, gone, 0 table lines from the same code)
Marvel Snap's Lizard "-4 Power if your opponent has 4 cards here" is a drawback, no need, and a mover feeds it no line (L29, L5).
- W marvel_snap: Polaris -> Lizard: NONE | network.py []
- W marvel_snap: Spider-Man -> Lizard: NONE | network.py []

## C66 lr_2.md 4 (MISSED CAUSE, gone, 0 table lines from the same code)
Cards that push or pull units on the board were not linked to cards in the same deck that act on units by place (next to it, in a line from it) (L29).
- W into_the_breach: A.C.I.D. Projector -> Hydraulic Legs: A.C.I.D. Projector moves enemy units, and Hydraulic Legs acts on units next to it | network.py []
- W into_the_breach: Hydraulic Legs -> Unstable Cannon: Hydraulic Legs moves units, and Unstable Cannon acts on units in a line from it | network.py []
- W into_the_breach: Titan Fist -> Rock Accelerator: Titan Fist moves enemy units, and Rock Accelerator acts on units in a line from it or next to its target | network.py []
- W into_the_breach: Rock Accelerator -> Titan Fist: Rock Accelerator moves enemy units, and Titan Fist acts on units next to it | network.py []
- R into_the_breach: Titan Fist -> Electric Whip: Titan Fist moves enemy units, and Electric Whip acts on units next to it or next to its target | network.py []
- R into_the_breach: Rock Accelerator -> Electric Whip: Rock Accelerator moves enemy units, and Electric Whip acts on units next to it or next to its target | network.py []

## C67 lr_9.md 5 (MISSED CAUSE, gone, 0 table lines from the same code)
pushing or pulling units links to every card in the same deck that acts on units next to it or in a line, but only some pairs were drawn (L29).
- W into_the_breach: Titan Fist -> Spartan Shield: Titan Fist moves enemy units, and Spartan Shield acts on units next to it | network.py []
- W into_the_breach: Cluster Artillery -> Cryo-Launcher: Cluster Artillery moves units, and Cryo-Launcher acts on units in a line from it; also heals: Cluster Artillery can hit the mech with Cryo-Launcher while it is  | network.py []
- W into_the_breach: Tri-Rocket -> Seismic Capacitor: Tri-Rocket moves enemy units, and Seismic Capacitor acts on units next to it | network.py []
- W into_the_breach: Titan Fist -> Hydraulic Lifter: Titan Fist moves enemy units, and Hydraulic Lifter acts on units next to it | network.py []

