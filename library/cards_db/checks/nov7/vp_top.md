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

