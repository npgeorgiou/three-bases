## C1 lr2_tb_3.md 1 (CAUSE, open, 3862 table lines from the same code)
A strength boost is linked to a card whose text reads the strength of enemy units, of cards in the deck or of cards in the discard, which a boost on my board units does not change (L18, L9).
- W gwent: Field Medic -> Caravan Guard: can give it more strength (when next to it) | network.py [1532]
- W gwent: Field Medic -> Yennefer: Divination: can give it more strength (when next to it) | network.py [1532]
- W gwent: Shaping Nature: Vitality -> Yennefer: Divination: can give it more strength | network.py [1532]
- W gwent: Chimera -> Ozzrel: makes your units die: Ozzrel Consumes them; also makes stronger: gives it more strength | network.py [1531]
- R gwent: Squire -> Redanian Knight: more strength: its text reads its strength when it comes | network.py [2472]
- R gwent: Anna Strenger -> Redanian Knight: can give it more strength | network.py [1531, 1532]
  Field Medic:
    when 1928 played self
    do 1928 own stat_change unit all board position is sides of self strength=2.0
  Caravan Guard:
    when 3150 played self
    if 3150 amount_sum
    if 3150 amount_stat strength unit enemy it board
    if 3150 amount_divided
    do 3150 own damage unit enemy chosen board amount=sum
  Yennefer: Divination:
    when 2571 played self
    when 4506 activated
    if 2571 keyword_condition
    if 2571 amount_stat strength unit mine it deck
    if 2571 have is self position is back_row
    do 2571 own keyword_action unit mine random deck
    do 4506 uses_keyword reveal unit mine random deck
    do 2571 own stat_change unit mine chosen board strength=stat
  Shaping Nature: Vitality:
    when 4401 played self
    when 4534 turn_end
    do 4401 own stat_change unit mine chosen board strength=6.0
    do 4401 own give_keyword unit mine it amount=6.0
    do 4534 uses_keyword stat_change unit mine it strength=1.0
  Chimera:
    when 3589 played self
    when 4538 activated
    when 4516 activated
    when 3590 played self
    if 4538 amount_stat strength it
    if 3590 keyword_condition 5.0
    if count le listed card mine hand
    if 3590 count le listed card mine hand
    do 3589 own keyword_action unit mine chosen board
    do 4538 uses_keyword kill unit mine chosen board
    do 4538 uses_keyword stat_change unit mine chosen board strength=stat
    do 4538 uses_keyword keyword_action unit mine chosen board
    do 4516 uses_keyword obliterate unit mine chosen board
    do 3590 own stat_change unit mine all board state is copy_of_it;position is same_row of it strength=1.0
  Ozzrel:
    when 2544 played self
    when 4538 activated
    when 4516 activated
    when 2545 played self
    when 4538 activated
    when 4516 activated
    if 2544 keyword_condition
    if 4538 amount_stat strength it
    if 2545 keyword_condition
    if 4538 amount_stat strength it
    if 2544 have is self position is front_row
    if 2545 have is self position is back_row
    do 2544 own keyword_action unit enemy chosen discard
    do 4538 uses_keyword kill unit enemy chosen discard
    do 4538 uses_keyword stat_change unit enemy chosen discard strength=stat
    do 4538 uses_keyword keyword_action unit enemy chosen discard
    do 4516 uses_keyword obliterate unit enemy chosen discard
    do 2545 own keyword_action unit mine chosen discard
    do 4538 uses_keyword kill unit mine chosen discard
    do 4538 uses_keyword stat_change unit mine chosen discard strength=stat
    do 4538 uses_keyword keyword_action unit mine chosen discard
    do 4516 uses_keyword obliterate unit mine chosen discard

## C2 lr2_lines_3.md 3 (CAUSE, open, 3800 table lines from the same code)
More strength is linked to a card that does not read its own strength, only filters its targets by strength or just acts (L14, L18).
- W gwent: Tactical Advantage -> Toad Prince: can give it more strength | network.py [1532]
- W gwent: Bone Talisman -> Kikimore Stalker: gives it more strength | network.py [1531]
- R gwent: Target Practice -> Knight-Errant: can give it more strength | network.py [1532]
- R gwent: Squire -> Knight-Errant: more strength: its text reads its strength when it comes | network.py [2472]
- R gwent: Imposter -> False Ciri: more strength: its text reads its strength when it comes | network.py [2472] | cases n614 line
  Tactical Advantage:
    when 4327 activated self
    when 4504 played self
    do 4327 own stat_change unit mine chosen board strength=5.0
    do 4504 has_keyword cant self event=activated;turns=1.0
  Toad Prince:
    when 1986 played self
    when 4538 activated
    when 4516 activated
    if 1986 keyword_condition
    if 4538 amount_stat strength it
    if 1986 have is self position is front_row
    do 1986 own keyword_action unit chosen board strength le 1951
    do 4538 uses_keyword kill unit chosen board strength le 1951
    do 4538 uses_keyword stat_change unit chosen board strength le 1951 strength=stat
    do 4538 uses_keyword keyword_action unit chosen board strength le 1951
    do 4516 uses_keyword obliterate unit chosen board strength le 1951
  Bone Talisman:
    when 2456 played self
    do 2456 own stat_change unit mine all board strength=1.0
  Kikimore Stalker:
    when 4169 always
    when 4519 always
    when 4510 played self
    when 4513 always
    when 4170 activated self
    when 4538 activated
    when 4516 activated
    when 4171 summoned unit mine type is 53
    when 4513 always
    when 4519 always
    when 4510 played self
    when 4513 always
    if 4513 amount_listed
    if 4170 keyword_condition
    if 4538 amount_stat strength it
    if 4513 amount_listed
    if 4513 amount_listed
    if 4170 keyword_condition
    do 4169 own give_keyword self
    do 4519 uses_keyword cant self event=given_keyword
    do 4169 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 4169 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4170 own choose_one
    do 4170 own damage unit enemy chosen board amount=1.0
    do 4170 own keyword_action unit mine chosen board card is 813582
    do 4538 uses_keyword kill unit mine chosen board card is 813582
    do 4538 uses_keyword stat_change unit mine chosen board card is 813582 strength=stat
    do 4538 uses_keyword keyword_action unit mine chosen board card is 813582
    do 4516 uses_keyword obliterate unit mine chosen board card is 813582
    do 4171 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4519 has_keyword cant self event=given_keyword
    do 4510 has_keyword can self event=activated
    do 4513 has_keyword can self event=activated;times=listed

## C3 lr2_lines_4.md 1 (CAUSE, open, 1931 table lines from the same code)
a plain damage to one chosen unit is read as "leaves weak units for its kill" for a card that waits for a kill, but a plain hit on one target feeds no kill trigger (L11).
- W runeterra: Noxian Fervor -> Parrrley: leaves weak units for its kill | network.py [2731]
- W gwent: Coup de Grâce -> Impera Enforcers: leaves weak units for its kill; also gives it units to kill | network.py [2731]
- W gwent: Waylay -> Milva: Sharpshooter: leaves weak units for its kill; also gives it units to kill | network.py [2731]
- W into_the_breach: Hydraulic Lifter -> Seismic Capacitor: Hydraulic Lifter moves enemy units, and Seismic Capacitor acts on units next to it; also triggers: leaves weak units for its kill | network.py [2731]
- R runeterra: Swain (level 2) -> Parrrley: leaves weak units for its kill | network.py [2731]
  Noxian Fervor:
    when 7537 played self
    do 7537 own damage unit mine chosen board amount=3.0
    do 7537 own damage unit chosen board amount=3.0
  Parrrley:
    when 7495 played self
    when 7496 killed unit
    do 7495 own damage any chosen amount=1.0
    do 7496 own damage player enemy amount=1.0
  Coup de Grâce:
    when 3425 always
    when 4545 round_start
    when 4517 leaves_play self
    when 3426 played self
    when 3427 killed
    when 3428 played self
    when 4545 round_start
    when 4517 leaves_play self
    if 3428 keyword_condition
    if it_matches keyword is 9000001
    if 3428 it_matches keyword is 9000001
    do 3425 own give_keyword self
    do 4545 uses_keyword put_on_top self
    do 4545 uses_keyword give_keyword self
    do 4517 uses_keyword obliterate self
    do 3426 own damage unit enemy chosen board amount=3.0
    do 3427 own copy it
    do 3427 own play_card it
    do 3428 own copy it
    do 3428 own play_card it
    do 4545 has_keyword put_on_top self discard
    do 4545 has_keyword give_keyword self
    do 4517 uses_keyword obliterate self
  Impera Enforcers:
    when 2218 always
    when 4510 played self
    when 2219 activated self
    when 2220 always
    when 4513 always
    when 2221 killed
    when 4532 damaged self
    when 2222 given_keyword unit enemy keyword is 9000001
    when 4513 always
    when 4510 played self
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 4532 amount_listed
    if 4513 amount_listed
    if 4513 amount_listed
    do 2218 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2219 own damage unit enemy chosen board amount=1.0
    do 2220 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 2221 own give_keyword self amount=1.0
    do 4532 uses_keyword negate_damage self amount=listed
    do 2222 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4510 has_keyword can self event=activated
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Waylay:
    when 2076 played self
    do 2076 own damage unit enemy chosen board amount=3.0
    do 2076 own summon
  Milva: Sharpshooter:
    when 3939 always
    when 4510 played self
    when 3940 activated self
    when 3941 killed
    when 3942 moves unit enemy
    when 4510 played self
    when 4504 played self
    if 3942 my_turn
    do 3939 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 3940 own damage unit enemy chosen board amount=1.0
    do 3941 own shuffle_into_deck self
    do 3942 own summon self
    do 3942 own damage unit mine it card is 757351 amount=1.0
    do 4510 has_keyword can self event=activated
    do 4504 has_keyword cant self event=activated;turns=1.0
  Hydraulic Lifter:
    when 5235 attacks
    when 5236 attacks
    when 5237 attacks
    if 5236 upgraded 1.0
    if 5237 upgraded 2.0
    do 5235 own move unit chosen position is bordering of self
    do 5235 own damage unit it amount=1.0
    do 5236 own can self event=attacks
    do 5237 own damage unit chosen position is bordering of self amount=2.0
  Seismic Capacitor:
    when 5403 attacks
    when 5404 attacks
    when 5405 attacks
    when 5406 killed
    if 5404 upgraded 1.0
    if 5405 upgraded 2.0
    do 5403 own damage unit_or_structure chosen position is bordering of self amount=1.0
    do 5403 own move unit_or_structure it
    do 5404 own damage unit_or_structure chosen position is bordering of self amount=1.0
    do 5405 own damage unit_or_structure chosen position is bordering of self amount=1.0
    do 5406 own set_terrain position all position is bordering of it

## C4 lr2_tb_3.md 2 (CAUSE, open, 1790 table lines from the same code)
"gives it units to kill" and "leaves weak units for its kill" are said for cards that only summon, play or hurt MY OWN units, so no enemy unit is made ready for the kill (L9, L11).
- W runeterra: Shape of Fear -> Parrrley: gives it units to kill | network.py [2731]
- W runeterra: Void Seeker -> Parrrley: leaves weak units for its kill | network.py [2731]
- W gwent: Magic Compass -> Gregoire de Gorgon: gives it units to kill; also plays it: its effect goes off | network.py [2731]
- W into_the_breach: Bomb Dispenser -> Fissure Fist: gives it units to kill | network.py [2731]
- R runeterra: Cataclysm -> Short Fuse: makes enemy units block: Short Fuse damages them | network.py []
- R gwent: Geralt: Professional -> Wolfsbane: its 1 damage kills what it sets to strength 1 | network.py [2737]
  Shape of Fear:
    when 8742 played self
    do 8742 own kill unit mine chosen board
    do 8742 own summon
  Parrrley:
    when 7495 played self
    when 7496 killed unit
    do 7495 own damage any chosen amount=1.0
    do 7496 own damage player enemy amount=1.0
  Void Seeker:
    when 8492 played self
    when 8493 played self
    if 8492 event_count lt 1.0
    if 8493 event_count ge 1.0
    do 8492 own damage unit mine chosen board category is follower amount=1.0
    do 8493 own damage unit mine chosen board amount=3.0
  Magic Compass:
    when 3984 always
    when 4545 round_start
    when 4517 leaves_play self
    when 3985 played self
    when 3986 played self
    when 4545 round_start
    when 4517 leaves_play self
    if 3985 count ge 3.0 card mine all deck
    if 3986 count lt 3.0 card mine all deck
    do 3984 own give_keyword self
    do 4545 uses_keyword put_on_top self
    do 4545 uses_keyword give_keyword self
    do 4517 uses_keyword obliterate self
    do 3985 own look card mine all deck_top
    do 3985 own play_card card mine chosen deck_top
    do 3985 own discard card mine all deck_top
    do 3986 own create card mine chosen hand state is gold;region is own_regions;state not started_in_deck
    do 3986 own play_card card mine chosen hand state is created
    do 4545 has_keyword put_on_top self discard
    do 4545 has_keyword give_keyword self
    do 4517 uses_keyword obliterate self
  Gregoire de Gorgon:
    when 2665 played self
    when 2666 killed
    when 4535 damaged self
    if 2665 keyword_condition
    if 4535 amount_event_amount
    if 2665 have is self position is front_row
    do 2665 own damage unit enemy chosen board amount=1.0
    do 2666 own stat_change self strength=8.0
    do 2666 own give_keyword self
    do 4535 uses_keyword negate_damage self amount=event_amount
    do 4535 uses_keyword remove_keyword self
  Bomb Dispenser:
    when 5345 attacks
    when 5346 attacks
    if 5346 upgraded 1.0
    do 5345 own summon
    do 5346 own summon
  Fissure Fist:
    when 5238 attacks
    when 5239 attacks
    when 5240 attacks
    when 5241 killed
    if 5239 upgraded 1.0
    if 5240 upgraded 2.0
    do 5238 own damage unit_or_structure chosen position is bordering of self amount=3.0
    do 5239 own damage unit_or_structure chosen position is bordering of self amount=1.0
    do 5240 own increase_effect self times=1.0
    do 5241 own set_terrain position all position is behind of it

## C5 lr2_lines_5.md 3 (CAUSE, open, 1478 table lines from the same code)
one reason is said twice with two words ("enables" or "makes stronger" next to "triggers" for the same given keyword), and "makes stronger" is said for a card that reads no stat (L10, L18).
- W gwent: Drakenborg -> Redanian Secret Service: makes your units get a keyword or status; also puts it into play: its summon effect goes off; also makes stronger: does what it waits for or counts (given keywo | network.py [1532]
- W gwent: Emhyr var Emreis -> Impera Enforcers: puts it into play from the hand; also enables: makes enemy units get Spying; also triggers: gives it units to kill; also triggers: plays it: its effect goes off | network.py [2731]
- R gwent: Fercart -> Impera Enforcers: makes enemy units get Spying; also triggers: gives it units to kill | network.py [2731] | cases n571 line
- R gwent: Treason -> Impera Enforcers: makes enemy units get Spying; also triggers: leaves weak units for its kill | network.py [2731]
  Drakenborg:
    when 4155 always
    when 4541 round_end
    when 4156 played self
    when 4523 always
    when 4157 activated self
    when 4534 turn_end
    when 4802 always
    when 4541 round_end
    when 4803 played self
    when 4523 always
    when 4804 activated self
    when 4534 turn_end
    when 4541 round_end
    when 4504 played self
    if 4157 amount_sum
    if 4157 amount_listed
    if 4157 amount_stat boost unit mine board state is summoned_this_round
    if 4804 amount_sum
    if 4804 amount_stat strength unit mine board state is summoned_this_round
    if 4804 amount_stat base_power unit mine board state is summoned_this_round
    if 4804 amount_minus
    do 4155 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 4156 own summon unit mine chosen deck
    do 4156 own give_keyword unit mine it
    do 4523 uses_keyword silence unit mine it
    do 4157 own give_keyword unit mine chosen board amount=sum
    do 4534 uses_keyword stat_change unit mine chosen board strength=1.0
    do 4802 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 4803 own summon unit mine chosen deck
    do 4803 own give_keyword unit mine it
    do 4523 uses_keyword silence unit mine it
    do 4804 own give_keyword unit mine chosen board amount=sum
    do 4534 uses_keyword stat_change unit mine chosen board strength=1.0
    do 4541 has_keyword cant self event=leaves_play
    do 4541 has_keyword remove_keyword self
    do 4504 has_keyword cant self event=activated;turns=1.0
  Redanian Secret Service:
    when 4158 always
    when 4510 played self
    when 4159 activated self
    when 4536 activated
    when 4160 given_keyword unit mine
    when 4510 played self
    when 4504 played self
    if 4160 have not unit mine board card is 757430
    do 4158 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 4159 own keyword_action unit mine chosen board
    do 4536 uses_keyword remove_keywords unit mine chosen board
    do 4160 own summon self
    do 4510 has_keyword can self event=activated
    do 4504 has_keyword cant self event=activated;turns=1.0
  Emhyr var Emreis:
    when 3627 played self
    when 3628 played unit enemy
    when 4569 always
    when 3629 activated self
    when 4539 activated
    when 4569 always
    when 3630 turn_end
    when 4504 played self
    if 3630 keyword_condition
    if have not card mine state is started_in_deck;region is Neutral
    if 3630 have not card mine state is started_in_deck;region is Neutral
    do 3627 own play_card card mine chosen hand state is bronze;type in 46;type in 62
    do 3627 own draw card mine deck_top amount=1.0
    do 3628 own give_keyword unit enemy it
    do 4569 uses_keyword can unit enemy it event=summoned
    do 3629 own keyword_action unit enemy chosen board strength eq 3431;keyword is 9000001
    do 4539 uses_keyword move unit enemy chosen board strength eq 3431;keyword is 9000001
    do 4539 uses_keyword give_keyword unit enemy chosen board strength eq 3431;keyword is 9000001
    do 4569 uses_keyword can unit enemy chosen board strength eq 3431;keyword is 9000001 event=summoned
    do 4539 uses_keyword remove_keyword unit enemy chosen board strength eq 3431;keyword is 9000001
    do 3630 own refresh self
    do 4504 has_keyword cant self event=activated;turns=1.0
  Impera Enforcers:
    when 2218 always
    when 4510 played self
    when 2219 activated self
    when 2220 always
    when 4513 always
    when 2221 killed
    when 4532 damaged self
    when 2222 given_keyword unit enemy keyword is 9000001
    when 4513 always
    when 4510 played self
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 4532 amount_listed
    if 4513 amount_listed
    if 4513 amount_listed
    do 2218 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2219 own damage unit enemy chosen board amount=1.0
    do 2220 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 2221 own give_keyword self amount=1.0
    do 4532 uses_keyword negate_damage self amount=listed
    do 2222 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4510 has_keyword can self event=activated
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0

## C6 lr2_lines_2.md 4 (CAUSE, open, 1397 table lines from the same code)
the same relation (a card gives a keyword, the other card reacts to "a unit is given a keyword") is said with different line words, here "puts" and "enables" instead of the trigger word (L10).
- W gwent: Emhyr var Emreis -> Impera Enforcers: puts it into play from the hand; also enables: makes enemy units get Spying; also triggers: gives it units to kill; also triggers: plays it: its effect goes off | network.py [2731]
- R gwent: Drakenborg -> Redanian Secret Service: makes your units get a keyword or status; also puts it into play: its summon effect goes off; also makes stronger: does what it waits for or counts (given keywo | network.py [1532]
  Emhyr var Emreis:
    when 3627 played self
    when 3628 played unit enemy
    when 4569 always
    when 3629 activated self
    when 4539 activated
    when 4569 always
    when 3630 turn_end
    when 4504 played self
    if 3630 keyword_condition
    if have not card mine state is started_in_deck;region is Neutral
    if 3630 have not card mine state is started_in_deck;region is Neutral
    do 3627 own play_card card mine chosen hand state is bronze;type in 46;type in 62
    do 3627 own draw card mine deck_top amount=1.0
    do 3628 own give_keyword unit enemy it
    do 4569 uses_keyword can unit enemy it event=summoned
    do 3629 own keyword_action unit enemy chosen board strength eq 3431;keyword is 9000001
    do 4539 uses_keyword move unit enemy chosen board strength eq 3431;keyword is 9000001
    do 4539 uses_keyword give_keyword unit enemy chosen board strength eq 3431;keyword is 9000001
    do 4569 uses_keyword can unit enemy chosen board strength eq 3431;keyword is 9000001 event=summoned
    do 4539 uses_keyword remove_keyword unit enemy chosen board strength eq 3431;keyword is 9000001
    do 3630 own refresh self
    do 4504 has_keyword cant self event=activated;turns=1.0
  Impera Enforcers:
    when 2218 always
    when 4510 played self
    when 2219 activated self
    when 2220 always
    when 4513 always
    when 2221 killed
    when 4532 damaged self
    when 2222 given_keyword unit enemy keyword is 9000001
    when 4513 always
    when 4510 played self
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 4532 amount_listed
    if 4513 amount_listed
    if 4513 amount_listed
    do 2218 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2219 own damage unit enemy chosen board amount=1.0
    do 2220 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 2221 own give_keyword self amount=1.0
    do 4532 uses_keyword negate_damage self amount=listed
    do 2222 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4510 has_keyword can self event=activated
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0

## C7 lr2_lines_4.md 2 (CAUSE, open, 1160 table lines from the same code)
a summon or put-into-play from the deck is linked to a card that has no "when I'm summoned" effect (only a Play effect, a turn-end effect or nothing), and a summoned card is not played (L17, L19).
- W gwent: Damsel in Distress -> Cintrian Knight: puts it into play from the deck; also enables: changes its stats for its effect; also triggers: puts it into play: its summon effect goes off | network.py [1531]
- W gwent: Damsel in Distress -> Knight-Errant: puts it into play from the deck; also makes stronger: gives it more strength | network.py [1531]
- W gwent: Damsel in Distress -> Redanian Knight: puts it into play from the deck; also makes stronger: gives it more strength | network.py [1531]
- W gwent: Arachas Behemoth -> Drone: summons | network.py []
- R gwent: Witches' Sabbath -> Kikimore Stalker: puts your units into play; also brings it back: its summon effect goes off | network.py []
- R gwent: Spontaneous Evolution -> Kikimore Stalker: puts your units into play; also makes stronger: can give it more strength | network.py [1532]
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
  Knight-Errant:
    when 3883 turn_end
    when 3884 stat_changed self
    when 4535 damaged self
    when 3885 keyword_removed self keyword is 756181
    when 4775 turn_end
    when 4776 stat_changed self
    when 4535 damaged self
    when 4777 keyword_removed self keyword is 756181
    if 3883 amount_count unit all board position is sides of self;state is buffed
    if 3883 amount_count unit all board position is sides of self;state is damaged
    if 3884 keyword_condition 9.0
    if 4535 amount_event_amount
    if 4775 amount_count unit mine all board position is sides;state is damaged
    if 4775 amount_count unit mine all board position is sides;state is buffed
    if 4776 keyword_condition 9.0
    if 4535 amount_event_amount
    if stat strength ge listed self
    if 3884 stat strength ge listed self
    if 4776 stat strength ge listed self
    do 3883 own stat_change self strength=count
    do 3883 own damage self amount=count
    do 3884 own give_keyword unit all board position is sides of self
    do 4535 uses_keyword negate_damage unit all board position is sides of self amount=event_amount
    do 4535 uses_keyword remove_keyword unit all board position is sides of self
    do 3884 own give_ability unit all board position is sides of self
    do 3885 gives stat_change self strength=2.0
    do 4775 own stat_change self strength=count
    do 4775 own damage self amount=count
    do 4776 own give_keyword unit mine all board position is sides
    do 4535 uses_keyword negate_damage unit mine all board position is sides amount=event_amount
    do 4535 uses_keyword remove_keyword unit mine all board position is sides
    do 4776 own give_ability unit mine all board position is sides
    do 4777 gives stat_change self strength=2.0
  Redanian Knight:
    when 1920 turn_end
    when 1921 keyword_removed self keyword is 756174
    when 1922 stat_changed self
    if 1920 keyword_condition
    if 1920 keyword_condition
    if 1922 keyword_condition 8.0
    if stat strength ge listed self
    if 1920 have is self keyword is 756174
    if 1920 have is self position is back_row
    if 1922 stat strength ge listed self
    do 1920 own stat_change self strength=1.0
    do 1921 own move self
    do 1921 own damage unit enemy highest board amount=2.0
    do 1922 own stat_change unit all board position is sides of self strength=1.0
  Arachas Behemoth:
    when 1960 played self
    do 1960 own summon amount=2.0
    do 1960 own stat_change unit mine all board type is 53;position is same_row of self strength=1.0
  Drone:
    when 4308 always
    when 4517 leaves_play self
    when 4517 leaves_play self
    do 4308 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4517 has_keyword obliterate self

## C8 lr2_lines_2.md 3 (CAUSE, open, 346 table lines from the same code)
moving enemy units is said to help a card that "acts on units next to it", but the receiving card's text has no need that a move fills (L14, L16).
- W into_the_breach: Hydraulic Lifter -> Seismic Capacitor: Hydraulic Lifter moves enemy units, and Seismic Capacitor acts on units next to it; also triggers: leaves weak units for its kill | network.py [696, 2731]
- W into_the_breach: Titan Fist -> Seismic Capacitor: Titan Fist moves enemy units, and Seismic Capacitor acts on units next to it; also triggers: leaves weak units for its kill | network.py [2731]
- R gwent: Maxii van Dekkar -> Albrich: shuffles a card into the deck: its move effect goes off; also moves it for its effect | network.py [] | cases n576 line
  Hydraulic Lifter:
    when 5235 attacks
    when 5236 attacks
    when 5237 attacks
    if 5236 upgraded 1.0
    if 5237 upgraded 2.0
    do 5235 own move unit chosen position is bordering of self
    do 5235 own damage unit it amount=1.0
    do 5236 own can self event=attacks
    do 5237 own damage unit chosen position is bordering of self amount=2.0
  Seismic Capacitor:
    when 5403 attacks
    when 5404 attacks
    when 5405 attacks
    when 5406 killed
    if 5404 upgraded 1.0
    if 5405 upgraded 2.0
    do 5403 own damage unit_or_structure chosen position is bordering of self amount=1.0
    do 5403 own move unit_or_structure it
    do 5404 own damage unit_or_structure chosen position is bordering of self amount=1.0
    do 5405 own damage unit_or_structure chosen position is bordering of self amount=1.0
    do 5406 own set_terrain position all position is bordering of it
  Titan Fist:
    when 5189 attacks
    when 5190 attacks
    when 5191 attacks
    if 5190 upgraded 1.0
    if 5191 upgraded 2.0
    do 5189 own damage unit_or_structure chosen position is bordering of self amount=2.0
    do 5189 own move unit_or_structure it
    do 5190 own move self
    do 5191 own damage unit_or_structure chosen position is bordering of self amount=2.0

## C9 lr2_lines_5.md 1 (CAUSE, open, 147 table lines from the same code)
"its summon effect goes off" is said for a revived, summoned or copied card that has no "when I'm summoned" ability in its rows (L17, L19; a copy put into play sets off only summon or death effects).
- W gwent: Sigrdrifa's Rite -> Rage of the Sea: brings it back: its summon effect goes off | network.py []
- W gwent: Drakenborg -> Redanian Secret Service: makes your units get a keyword or status; also puts it into play: its summon effect goes off; also makes stronger: does what it waits for or counts (given keywo | network.py [1532]
- W gwent: Mobilization -> Lyrian Arbalest: puts it into play: its summon effect goes off; also is a card whose playing sets off its effect | network.py [1856]
- W gwent: Witches' Sabbath -> Arachas Swarm: is an Organic whose playing sets off its effect; also brings it back: its summon effect goes off | network.py [1856]
  Sigrdrifa's Rite:
    when 2127 played self
    when 4517 leaves_play self
    do 2127 own revive unit mine chosen discard region not Neutral
    do 2127 own give_keyword unit mine it
    do 4517 uses_keyword obliterate unit mine it
  Rage of the Sea:
    when 2454 activated self
    when 4522 turn_start
    when 2455 always
    when 4513 always
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 4513 amount_listed
    do 2454 own give_keyword position enemy chosen turns=2.0
    do 4522 uses_keyword damage unit random board position is same_row of self amount=1.0
    do 2454 own summon
    do 2455 own give_keyword self amount=2.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Drakenborg:
    when 4155 always
    when 4541 round_end
    when 4156 played self
    when 4523 always
    when 4157 activated self
    when 4534 turn_end
    when 4802 always
    when 4541 round_end
    when 4803 played self
    when 4523 always
    when 4804 activated self
    when 4534 turn_end
    when 4541 round_end
    when 4504 played self
    if 4157 amount_sum
    if 4157 amount_listed
    if 4157 amount_stat boost unit mine board state is summoned_this_round
    if 4804 amount_sum
    if 4804 amount_stat strength unit mine board state is summoned_this_round
    if 4804 amount_stat base_power unit mine board state is summoned_this_round
    if 4804 amount_minus
    do 4155 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 4156 own summon unit mine chosen deck
    do 4156 own give_keyword unit mine it
    do 4523 uses_keyword silence unit mine it
    do 4157 own give_keyword unit mine chosen board amount=sum
    do 4534 uses_keyword stat_change unit mine chosen board strength=1.0
    do 4802 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 4803 own summon unit mine chosen deck
    do 4803 own give_keyword unit mine it
    do 4523 uses_keyword silence unit mine it
    do 4804 own give_keyword unit mine chosen board amount=sum
    do 4534 uses_keyword stat_change unit mine chosen board strength=1.0
    do 4541 has_keyword cant self event=leaves_play
    do 4541 has_keyword remove_keyword self
    do 4504 has_keyword cant self event=activated;turns=1.0
  Redanian Secret Service:
    when 4158 always
    when 4510 played self
    when 4159 activated self
    when 4536 activated
    when 4160 given_keyword unit mine
    when 4510 played self
    when 4504 played self
    if 4160 have not unit mine board card is 757430
    do 4158 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 4159 own keyword_action unit mine chosen board
    do 4536 uses_keyword remove_keywords unit mine chosen board
    do 4160 own summon self
    do 4510 has_keyword can self event=activated
    do 4504 has_keyword cant self event=activated;turns=1.0
  Mobilization:
    when 2373 activated self
    when 4504 played self
    do 2373 own copy unit mine chosen board state is bronze;type is 46
    do 2373 own stat_change unit mine it type is 46 strength=3.0
    do 2373 own stat_change unit mine it state is created strength=3.0
    do 4504 has_keyword cant self event=activated;turns=1.0
  Lyrian Arbalest:
    when 2632 activated self
    when 2633 always
    when 4513 always
    when 2634 played card mine keyword is 756143
    when 4513 always
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 4513 amount_listed
    if 4513 amount_listed
    do 2632 own damage unit chosen board amount=1.0
    do 2633 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 2634 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Witches' Sabbath:
    when 3815 played self
    when 4517 leaves_play self
    if 3815 amount_count it
    do 3815 own revive unit enemy highest discard
    do 3815 own revive unit mine highest discard region not Neutral
    do 3815 own give_keyword unit mine it
    do 4517 uses_keyword obliterate unit mine it
  Arachas Swarm:
    when 2550 activated self
    when 2551 always
    when 4513 always
    when 2552 played card mine type is 28
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 4513 amount_listed
    do 2550 own summon
    do 2551 own give_keyword self amount=5.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 2552 own summon
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0

## C10 lr2_tb_2.md 2 (CAUSE, open, 36 table lines from the same code)
Giving Stormbound strength to units around it is read as a help for cards that never read their own strength, so it is generic more-damage/more-health help (L18, L14).
- W stormbound: Upgrade Point -> Finite Loopers: NONE | network.py []
- W stormbound: Upgrade Point -> Frontline Engineers: is a landmark or structure it asks for | network.py [1948]
- W stormbound: Greengale Serpents -> Va’vel the Looper: NONE | network.py []
- W stormbound: Greengale Serpents -> Tegor the Vengeful: NONE | network.py []
  Upgrade Point:
    when 10288 turn_start
    if 10288 amount_per_level
    do 10288 own stat_change unit mine all board position is surrounding;type is 153 strength=2.0
  Frontline Engineers:
    when 10310 played self
    if 10310 amount_per_level
    if 10310 amount_count landmark mine board
    do 10310 own stat_change self strength=2.0;times=count

## C11 lr2_lines_2.md 1 (CAUSE, open, 0 table lines from the same code)
"fills your hand" is given as a reason to cards whose text wants a small hand ("if cards in hand at most N"), which is the wrong direction (L21 read wants right), and Damsel in Distress does not draw at all.
- W gwent: Selective Mutation -> Vesemir: Mentor: draws it from the deck | network.py [] | cases n588 none
- W gwent: Selective Mutation -> Geralt: Quen: draws it from the deck | network.py []
- W gwent: Damsel in Distress -> Keldar: is played | network.py []
- R duelyst: Replicant -> Theobule: NONE | network.py []
  Selective Mutation:
    when 3483 played self
    do 3483 own draw card mine chosen deck keyword is 756153
    do 3483 own shuffle_into_deck card mine chosen hand
    do 3483 own summon
  Vesemir: Mentor:
    when 2400 played self
    when 2401 played self
    if 2401 keyword_condition 4.0
    if count le listed card mine hand
    if 2401 count le listed card mine hand
    do 2400 own stat_change unit mine all board type is 34 strength=1.0
    do 2401 own stat_change unit mine all hand type is 34 strength=1.0
    do 2401 own stat_change unit mine all deck type is 34 strength=1.0
  Geralt: Quen:
    when 3480 always
    when 4535 damaged self
    when 3481 played self
    when 3482 played self
    when 4535 damaged self
    when 4535 damaged self
    if 4535 amount_event_amount
    if 3481 keyword_condition not 4.0
    if 3482 keyword_condition 4.0
    if 4535 amount_event_amount
    if 4535 amount_event_amount
    if count le listed card mine hand
    if 3481 count le listed card mine hand
    if 3482 count le listed card mine hand
    do 3480 own give_keyword self
    do 4535 uses_keyword negate_damage self amount=event_amount
    do 4535 uses_keyword remove_keyword self
    do 3481 own play_card card mine chosen deck type is 34
    do 3482 own play_card card mine chosen deck type is 34
    do 3482 own give_keyword card mine it type is 34
    do 4535 uses_keyword negate_damage card mine it type is 34 amount=event_amount
    do 4535 uses_keyword remove_keyword card mine it type is 34
    do 4535 has_keyword negate_damage self amount=event_amount
    do 4535 has_keyword remove_keyword self
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
  Keldar:
    when 3557 played spell mine
    when 3558 turn_end
    if 3558 keyword_condition 4.0
    if count le listed card mine hand
    if 3558 count le listed card mine hand
    do 3557 own summon
    do 3558 own summon

## C12 lr2_lines_2.md 2 (CAUSE, open, 0 table lines from the same code)
a card that only damages or kills itself is said to feed a card that acts on what that card kills or on units that die, but the receiving card's text does not act on that death (L3, L16).
- W gwent: Madoc -> Northern Wind: NONE | network.py []
- W gwent: Little Havfrue -> Freya's Blessing: dies by its own effect | network.py []
- R monster_train: Rector Flicker -> Memories of the Melted: NONE | network.py []
- R gwent: Magic Compass -> Coral: makes you discard cards; also plays it: its effect goes off | network.py []
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
  Freya's Blessing:
    when 2148 played self
    when 4517 leaves_play self
    do 2148 own play_card unit mine chosen discard state is bronze;region not Neutral
    do 2148 own give_keyword unit mine it
    do 4517 uses_keyword obliterate unit mine it

## C13 lr2_lines_3.md 1 (CAUSE, open, 0 table lines from the same code)
A card whose only "played self" rows are the engine's generic "can/cannot activate" rows (4510/4504/4513) is read as having a play or summon effect, but it has none (L1, L19).
- W gwent: Vernon Roche -> Redanian Archer: plays it: its effect goes off | network.py []
- W gwent: Mobilization -> Redanian Archer: puts it into play: its summon effect goes off | network.py []
- W gwent: Lydia van Bredevoort -> Snowdrop: plays it: its effect goes off | network.py []
- W gwent: Bountiful Harvest -> Freixenet: plays it: its effect goes off | network.py []
- R gwent: Ihuarraquax -> Barghest: puts it into play: its summon effect goes off | network.py []
- R gwent: Sove -> Little Havfrue: puts it into play from the deck; also triggers: puts it into play: its summon effect goes off | network.py []
  Vernon Roche:
    when 1866 always
    when 4527 always
    when 4528 played self
    when 4569 always
    when 1867 played self
    when 4527 always
    when 4528 played self
    when 4569 always
    do 1866 own give_keyword self
    do 4527 uses_keyword can self event=summoned
    do 4528 uses_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
    do 1867 own play_card card mine top deck
    do 4527 has_keyword can self event=summoned
    do 4528 has_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
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
  Mobilization:
    when 2373 activated self
    when 4504 played self
    do 2373 own copy unit mine chosen board state is bronze;type is 46
    do 2373 own stat_change unit mine it type is 46 strength=3.0
    do 2373 own stat_change unit mine it state is created strength=3.0
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
  Snowdrop:
    when 3475 always
    when 4510 played self
    when 3476 activated self
    when 3477 drawn
    when 4510 played self
    when 4504 played self
    do 3475 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 3476 own draw card mine chosen deck_top amount=2.0;max=2.0
    do 3476 own shuffle_into_deck card mine chosen hand
    do 3477 own stat_change self strength=2.0
    do 4510 has_keyword can self event=activated
    do 4504 has_keyword cant self event=activated;turns=1.0
  Bountiful Harvest:
    when 3795 played self
    when 3796 played self
    when 3797 played self
    if 3795 it_matches position is first_in_front
    if 3796 it_matches position is middle_lane
    if 3797 it_matches position is behind_all
    do 3795 own create card mine chosen hand state is bronze;region is Scoiatael;type is 40
    do 3795 own play_card card mine chosen hand state is created
    do 3795 own stat_change card mine leftmost hand strength=2.0
    do 3796 own create card mine chosen hand state is bronze;region is Scoiatael;type is 40
    do 3796 own play_card card mine chosen hand state is created
    do 3796 own stat_change card mine random hand strength=2.0
    do 3797 own create card mine chosen hand state is bronze;region is Scoiatael;type is 40
    do 3797 own play_card card mine chosen hand state is created
    do 3797 own stat_change card mine rightmost hand strength=2.0
  Freixenet:
    when 3454 always
    when 4510 played self
    when 3455 activated self
    when 3456 always
    when 4511 activated self
    when 3457 turn_end
    when 4511 activated self
    when 4510 played self
    if 3455 keyword_condition
    if 4511 amount_listed
    if 3457 keyword_condition
    if 3457 amount_stat keyword_amount self keyword is 756177
    if 3457 amount_minus
    if 4511 amount_listed
    if 3455 have is self position is back_row
    if 3457 have not card mine state is started_in_deck;region is Neutral
    do 3454 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 3455 own summon
    do 3456 own keyword_action amount=4.0
    do 4511 uses_keyword cant event=activated;turns=listed
    do 3457 own keyword_action amount=minus
    do 4511 uses_keyword cant event=activated;turns=listed
    do 4510 has_keyword can self event=activated

## C14 lr2_lines_3.md 4 (CAUSE, open, 0 table lines from the same code)
A draw by kind or by name family is given a "draws it" line although no card is named (L1b).
- W gwent: Octavia Hale -> Ignatius Hale: draws it from the deck | network.py []
- W gwent: Selective Mutation -> Vesemir: Mentor: draws it from the deck | network.py [] | cases n588 none
- W gwent: Selective Mutation -> Geralt: Quen: draws it from the deck | network.py []
  Octavia Hale:
    when 3822 played self
    when 3823 activated self
    when 3824 activated self
    if 3822 amount_event_amount
    if 3823 event_count eq 0.0
    if 3824 event_count ge 1.0
    do 3822 own draw card mine chosen deck name_has is 16;card not 757313 amount=2.0
    do 3822 own shuffle_into_deck card mine chosen hand
    do 3823 own spend_mana secondary_resource mine amount=2.0
    do 3823 own stat_change unit mine chosen board type is 65 strength=2.0
    do 3824 own spend_mana secondary_resource mine amount=2.0
    do 3824 own stat_change unit mine chosen board type is 65 strength=3.0
  Ignatius Hale:
    when 3765 game_start
    when 3766 created self
    when 3767 dies unit enemy keyword is 756214
    when 4515 activated
    if 3767 amount_stat base_power it
    if 4515 amount_full
    if 4515 amount_listed
    do 3765 own stat_set self strength=1.0
    do 3766 own stat_set self strength=1.0
    do 3767 own keyword_action self amount=stat
    do 4515 uses_keyword heal self amount=full
    do 4515 uses_keyword heal self amount=listed
  Selective Mutation:
    when 3483 played self
    do 3483 own draw card mine chosen deck keyword is 756153
    do 3483 own shuffle_into_deck card mine chosen hand
    do 3483 own summon
  Vesemir: Mentor:
    when 2400 played self
    when 2401 played self
    if 2401 keyword_condition 4.0
    if count le listed card mine hand
    if 2401 count le listed card mine hand
    do 2400 own stat_change unit mine all board type is 34 strength=1.0
    do 2401 own stat_change unit mine all hand type is 34 strength=1.0
    do 2401 own stat_change unit mine all deck type is 34 strength=1.0
  Geralt: Quen:
    when 3480 always
    when 4535 damaged self
    when 3481 played self
    when 3482 played self
    when 4535 damaged self
    when 4535 damaged self
    if 4535 amount_event_amount
    if 3481 keyword_condition not 4.0
    if 3482 keyword_condition 4.0
    if 4535 amount_event_amount
    if 4535 amount_event_amount
    if count le listed card mine hand
    if 3481 count le listed card mine hand
    if 3482 count le listed card mine hand
    do 3480 own give_keyword self
    do 4535 uses_keyword negate_damage self amount=event_amount
    do 4535 uses_keyword remove_keyword self
    do 3481 own play_card card mine chosen deck type is 34
    do 3482 own play_card card mine chosen deck type is 34
    do 3482 own give_keyword card mine it type is 34
    do 4535 uses_keyword negate_damage card mine it type is 34 amount=event_amount
    do 4535 uses_keyword remove_keyword card mine it type is 34
    do 4535 has_keyword negate_damage self amount=event_amount
    do 4535 has_keyword remove_keyword self

## C15 lr2_lines_5.md 4 (CAUSE, open, 0 table lines from the same code)
random damage at turn start (any unit on the row, either side) is read as "makes your cards leave play"; it does not aim at my cards and the obliterate is only the unit's own leaving (L9, L5, L2).
- W gwent: Fucusya -> Tyr: Master of An Skellig: makes your cards leave play | network.py []
- R gwent: Little Havfrue -> Sigrdrifa's Rite: dies by its own effect: Sigrdrifa's Rite brings them back | network.py []
  Fucusya:
    when 3784 played self
    when 4517 leaves_play self
    when 4522 turn_start
    if 3784 amount_stat unused_provisions player mine
    do 3784 own play_card unit mine chosen discard region not Neutral;cost le 3554
    do 3784 own give_keyword unit mine it
    do 4517 uses_keyword obliterate unit mine it
    do 3784 own give_keyword position enemy chosen position is opposite_row of self turns=stat
    do 4522 uses_keyword damage unit random board position is same_row of self amount=1.0
  Tyr: Master of An Skellig:
    when 4472 always
    when 4517 leaves_play self
    when 4473 played self
    when 4543 activated
    when 4474 leaves_play unit mine state is bronze
    when 4517 leaves_play self
    if 4474 my_turn
    if 4474 amount_stat base_power it
    do 4472 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4473 own return_card unit mine chosen discard state is bronze;region not Neutral
    do 4473 own keyword_action card mine chosen hand
    do 4543 uses_keyword discard card mine chosen hand
    do 4474 own stat_change unit mine it strength=stat
    do 4517 has_keyword obliterate self

## C16 lr2_tb_3.md 3 (CAUSE, open, 0 table lines from the same code)
"plays it: its effect goes off" is said for target cards that have no Play effect of their own (only an activated ability), so playing them sets nothing off (L14, L1).
- W gwent: Necromancy -> Vysogota of Corvo: is played; also plays it: its effect goes off | network.py []
- W gwent: War Council -> Imperial Formation: plays it: its effect goes off | network.py []
- W gwent: Decoy -> Vincent Meis: plays it: its effect goes off | network.py []
- R gwent: Ihuarraquax -> Tuirseach Bearmaster: puts it into play: its summon effect goes off | network.py []
  Necromancy:
    when 2246 played self
    when 4517 leaves_play self
    do 2246 own play_card unit mine chosen discard state is bronze
    do 2246 own give_keyword unit mine it
    do 4517 uses_keyword obliterate unit mine it
  Vysogota of Corvo:
    when 2621 always
    when 4510 played self
    when 2622 activated self
    when 2623 always
    when 4513 always
    when 2624 played card
    when 4513 always
    when 4510 played self
    when 4513 always
    if 2622 keyword_condition
    if 4513 amount_listed
    if 4513 amount_listed
    if 4513 amount_listed
    if 2622 have is self position is back_row
    do 2621 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2622 own stat_change unit chosen board strength=1.0
    do 2623 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 2624 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4510 has_keyword can self event=activated
    do 4513 has_keyword can self event=activated;times=listed
  War Council:
    when 3081 always
    when 4541 round_end
    when 3082 played self
    when 3083 activated self
    when 4541 round_end
    when 4504 played self
    do 3081 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 3082 own look card mine deck_top
    do 3082 own play_card card mine chosen deck_top
    do 3083 own create card mine
    do 3083 own play_card card mine it card is 756987
    do 4541 has_keyword cant self event=leaves_play
    do 4541 has_keyword remove_keyword self
    do 4504 has_keyword cant self event=activated;turns=1.0
  Imperial Formation:
    when 2360 activated self
    when 4532 damaged self
    when 2361 always
    when 4513 always
    when 4513 always
    when 4504 played self
    if 4532 amount_listed
    if 4513 amount_listed
    if 4513 amount_listed
    do 2360 own stat_change unit mine chosen board strength=1.0
    do 2360 own swap unit mine it
    do 2360 own give_keyword unit mine it type is 46 amount=1.0
    do 4532 uses_keyword negate_damage unit mine it type is 46 amount=listed
    do 2361 own give_keyword self amount=4.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Decoy:
    when 1833 played self
    do 1833 own shuffle_into_deck unit mine chosen board
    do 1833 own play_card unit mine top deck
  Vincent Meis:
    when 2317 always
    when 4510 played self
    when 2318 activated self
    when 4510 played self
    if 2318 keyword_condition
    if 2318 have is self position is front_row
    do 2317 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2318 own stat_set unit enemy chosen board state not buffed strength=1.0
    do 4510 has_keyword can self event=activated

## C17 lr2_lines_3.md 2 (CAUSE, CONFLICT n570, 5588 table lines from the same code)
Units put on MY side (played, created or summoned for me) are called "units to kill" for a card that damages or kills ENEMY units (L9).
- W gwent: Imperial Diplomacy -> Impera Enforcers: gives it units to kill | network.py [2731]
- W gwent: False Ciri -> Impera Enforcers: gives it units to kill | network.py [2731]
- W gwent: Battle Stations! -> Impera Enforcers: gives it units to kill; also plays it: its effect goes off | network.py [2731] | cases n570 line
- W gwent: Joachim de Wett -> Impera Enforcers: gives it units to kill; also plays it: its effect goes off | network.py [2731]
- R runeterra: Gangplank -> Parrrley: gives it units to kill | network.py [2731]
- R runeterra: Gangplank (level 2) -> Parrrley: gives it units to kill | network.py [2731]
  Imperial Diplomacy:
    when 2234 played self
    do 2234 own create card mine random state is opponent_faction;state is bronze
    do 2234 own play_card card mine it
  Impera Enforcers:
    when 2218 always
    when 4510 played self
    when 2219 activated self
    when 2220 always
    when 4513 always
    when 2221 killed
    when 4532 damaged self
    when 2222 given_keyword unit enemy keyword is 9000001
    when 4513 always
    when 4510 played self
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 4532 amount_listed
    if 4513 amount_listed
    if 4513 amount_listed
    do 2218 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2219 own damage unit enemy chosen board amount=1.0
    do 2220 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 2221 own give_keyword self amount=1.0
    do 4532 uses_keyword negate_damage self amount=listed
    do 2222 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4510 has_keyword can self event=activated
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  False Ciri:
    when 2200 always
    when 4527 always
    when 4528 played self
    when 4569 always
    when 2201 played self
    when 4517 leaves_play self
    when 2202 turn_end
    when 2203 stat_changed self
    when 4536 activated
    when 4527 always
    when 4528 played self
    when 4569 always
    if 2203 keyword_condition 8.0
    if stat strength ge listed self
    if 2203 stat strength ge listed self
    do 2200 own give_keyword self
    do 4527 uses_keyword can self event=summoned
    do 4528 uses_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
    do 2201 own play_card card mine chosen discard state is bronze;type is 21
    do 2201 own give_keyword card mine it type is 21
    do 4517 uses_keyword obliterate card mine it type is 21
    do 2202 own stat_change self strength=1.0
    do 2203 own move self
    do 2203 own keyword_action self
    do 4536 uses_keyword remove_keywords self
    do 4527 has_keyword can self event=summoned
    do 4528 has_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
  Battle Stations!:
    when 4196 played self
    if 4196 amount_event_amount
    do 4196 own play_card card mine chosen hand state is bronze
    do 4196 own draw card mine deck_top amount=event_amount
  Joachim de Wett:
    when 2198 always
    when 4527 always
    when 4528 played self
    when 4569 always
    when 2199 played self
    when 4527 always
    when 4528 played self
    when 4569 always
    do 2198 own give_keyword self
    do 4527 uses_keyword can self event=summoned
    do 4528 uses_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
    do 2199 own play_card unit mine deck_top keyword not 756170
    do 2199 own stat_change unit mine it strength=8.0
    do 4527 has_keyword can self event=summoned
    do 4528 has_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned

## C18 lr2_lines_5.md 2 (CAUSE, CONFLICT n549, 3208 table lines from the same code)
"leaves weak units for its kill" is said for a plain hit on one target; a plain hit feeds no "when an enemy dies" (L11, L2).
- W into_the_breach: Titan Fist -> Seismic Capacitor: Titan Fist moves enemy units, and Seismic Capacitor acts on units next to it; also triggers: leaves weak units for its kill | network.py [2731]
- W gwent: Samum -> Milva: Sharpshooter: leaves weak units for its kill; also makes enemy units move | network.py [2731]
- W gwent: Forbidden Magic -> Kaedweni Revenant: summons; also triggers: leaves weak units for its kill; also triggers: gives it units to kill | network.py [2731] | cases n549 line
- R gwent: Treason -> Impera Enforcers: makes enemy units get Spying; also triggers: leaves weak units for its kill | network.py [2731]
  Titan Fist:
    when 5189 attacks
    when 5190 attacks
    when 5191 attacks
    if 5190 upgraded 1.0
    if 5191 upgraded 2.0
    do 5189 own damage unit_or_structure chosen position is bordering of self amount=2.0
    do 5189 own move unit_or_structure it
    do 5190 own move self
    do 5191 own damage unit_or_structure chosen position is bordering of self amount=2.0
  Seismic Capacitor:
    when 5403 attacks
    when 5404 attacks
    when 5405 attacks
    when 5406 killed
    if 5404 upgraded 1.0
    if 5405 upgraded 2.0
    do 5403 own damage unit_or_structure chosen position is bordering of self amount=1.0
    do 5403 own move unit_or_structure it
    do 5404 own damage unit_or_structure chosen position is bordering of self amount=1.0
    do 5405 own damage unit_or_structure chosen position is bordering of self amount=1.0
    do 5406 own set_terrain position all position is bordering of it
  Samum:
    when 2683 played self
    when 2684 killed
    do 2683 own damage unit chosen board amount=3.0
    do 2684 own move unit all board position is sides of it
  Milva: Sharpshooter:
    when 3939 always
    when 4510 played self
    when 3940 activated self
    when 3941 killed
    when 3942 moves unit enemy
    when 4510 played self
    when 4504 played self
    if 3942 my_turn
    do 3939 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 3940 own damage unit enemy chosen board amount=1.0
    do 3941 own shuffle_into_deck self
    do 3942 own summon self
    do 3942 own damage unit mine it card is 757351 amount=1.0
    do 4510 has_keyword can self event=activated
    do 4504 has_keyword cant self event=activated;turns=1.0
  Forbidden Magic:
    when 2492 played self
    when 2493 killed
    do 2492 own damage unit enemy chosen board amount=2.0
    do 2493 own summon
  Kaedweni Revenant:
    when 2487 activated self
    when 2488 killed
    when 4504 played self
    do 2487 own damage unit chosen board amount=1.0
    do 2488 own copy self
    do 4504 has_keyword cant self event=activated;turns=1.0

## C19 lr2_lines_1.md 1 (MISSED CAUSE, gone, 0 table lines from the same code)
a card whose text reacts to a minority kind being played or being on my board (a deck choice, not every card) lost its line from the cards of that kind (L1b: a minority kind keeps its line; L24 style needs).
- W gwent: Making a Bomb -> Madoc: is a Bomb whose playing sets off its effect; also moves into place: moves an enemy unit into the row it hits | network.py [1856, 2235]
- W gwent: War Council -> Fire Scorpion: is a Tactic whose playing sets off its effect; also is played; also plays it: its effect goes off | network.py [1856]
- W gwent: Crach an Craite -> Holger Blackhand: is a Pirate whose playing sets off its effect | network.py [1856]
- W stormbound: Spare Dragonling -> Wandering Wyrms: is a Dragon it asks for | network.py [878]

## C20 lr2_lines_1.md 2 (MISSED CAUSE, gone, 0 table lines from the same code)
a card whose text counts or reads the cards of a minority kind in my deck or on my board lost its line from the cards of that kind (L1b: "the number of X in your deck" keeps its line where X is a minority; Annie).
- W gwent: Aen Elle Aristocrat -> Tir ná Lia: is a Wild Hunt it asks for; also moves into place: moves an enemy unit into the row it hits | network.py [2235]
- W gwent: Wild Hunt Bruiser -> Tir ná Lia: is a Wild Hunt it asks for; also moves into place: moves an enemy unit into the row it hits | network.py [2235]
- W gwent: Petri's Philter -> Otkell: is an Alchemy it asks for; also makes stronger: can give it more strength | network.py [1532]
- W stormbound: Spare Dragonling -> Sunbeam Serpents: is a Dragon it asks for | network.py []

## C21 lr2_lines_1.md 3 (MISSED CAUSE, gone, 0 table lines from the same code)
a card that gains the second resource (coins) lost its line to cards whose text spends that resource to act; what pays a card's cost is a line (L22).
- W gwent: Shakedown -> Casino Bouncers: lets you gain the second resource (Bones); also makes stronger: can give it more strength | network.py [1532]
- W gwent: Collusion -> Whoreson Junior: lets you gain the second resource (Bones); also makes stronger: can give it more strength | network.py [1532]
- W gwent: Collusion -> Bloody Good Friends: lets you gain the second resource (Bones); also makes stronger: can give it more strength | network.py [1532]

## C22 lr2_lines_1.md 4 (MISSED CAUSE, gone, 0 table lines from the same code)
a card that gives a keyword to enemy units lost its line to a card that waits for that keyword being given ("when an enemy gets Spying"); anything a card waits for is a line (L14).
- W gwent: Fercart -> Impera Enforcers: makes enemy units get Spying; also triggers: gives it units to kill | network.py [2731] | cases n571 line
- W gwent: Treason -> Impera Enforcers: makes enemy units get Spying; also triggers: leaves weak units for its kill | network.py [2731]

## C23 lr2_lines_3.md 5 (MISSED CAUSE, gone, 0 table lines from the same code)
A card that is a Ship/Pirate type, which the other card's own text asks for (Crach reacts to playing Ships and Pirates beside him), lost its line; and a move of enemy units feeds a card that reacts to enemy moves (L10, L14).
- W gwent: Tidecloak Hideaway -> Crach an Craite: is a Ship it asks for; also makes stronger: can give it more strength | network.py [1532, 1856]
- W gwent: Samum -> Milva: Sharpshooter: leaves weak units for its kill; also makes enemy units move | network.py [2731]

## C24 lr2_lines_4.md 3 (CAUSE, CONFLICT n617, 0 table lines from the same code)
a card that copies an enemy unit is said to "create cards" for a card that copies too; the receiver waits for nothing the giver makes, it copies its own chosen target (L19, L3).
- W gwent: Imposter -> Torres var Emreis: Founder: creates cards: Torres var Emreis: Founder copys them | network.py [] | cases n617 line
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
  Torres var Emreis: Founder:
    when 4080 always
    when 4517 leaves_play self
    when 4081 played self
    when 4569 always
    when 4082 activated self
    when 4516 activated
    when 4083 round_won
    when 4517 leaves_play self
    when 4504 played self
    if 4081 amount_stat provisions_below_limit unit enemy chosen deck
    do 4080 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4081 own give_keyword unit enemy chosen deck cost le 3841
    do 4569 uses_keyword can unit enemy chosen deck cost le 3841 event=summoned
    do 4081 own copy unit enemy it state is created
    do 4081 own stat_change self strength=stat
    do 4082 own keyword_action card mine chosen deck state is started_in_deck
    do 4516 uses_keyword obliterate card mine chosen deck state is started_in_deck
    do 4083 own transform self
    do 4517 has_keyword obliterate self
    do 4504 has_keyword cant self event=activated;turns=1.0

## C25 lr2_tb_1.md 1 (MISSED CAUSE, gone, 0 table lines from the same code)
A card whose own text makes enemy units block (challenge) feeds a card that damages blocking enemy units; the fix removed this line although challenge does the very thing the need asks for (L2, L10, L4).
- W runeterra: Royal Decree -> Short Fuse: makes enemy units block: Short Fuse damages them | network.py []
- W runeterra: The List -> Short Fuse: makes enemy units block: Short Fuse damages them | network.py []
- W runeterra: The Warrior -> Short Fuse: makes enemy units block: Short Fuse damages them | network.py []

## C26 lr2_tb_2.md 1 (CAUSE, gone, 0 table lines from the same code)
Damage to the enemy's row is read as "makes your units die"; Tyr waits for my own bronze units leaving play, and these cards only hit enemy units (L9).
- W gwent: Dragon's Dream -> Tyr: Master of An Skellig: NONE | network.py []
- W gwent: Ragh Nar Roog -> Tyr: Master of An Skellig: NONE | network.py []
- W gwent: Rage of the Sea -> Tyr: Master of An Skellig: NONE | network.py []

## C27 lr2_tb_2.md 3 (CAUSE, gone, 0 table lines from the same code)
More strength is read as "keeps it alive" for cards that do not wait to survive damage (Cave Troll only cannot be targeted; Donimir's damage rows are the shield keyword's own working, L15), so the help is generic (L18).
- W gwent: Blessing of Kindness -> Cave Troll: NONE | network.py []
- W gwent: Reynard Odo -> Donimir of Troy: NONE | network.py []
- W gwent: Vandergrift's Blade -> Donimir of Troy: NONE | network.py []

## C28 lr2_tb_2.md 4 (CAUSE, gone, 0 table lines from the same code)
Consuming a unit from the graveyard is read as "makes units die", but the unit is already dead; no death happens, so cards that wait for deaths or revive from the graveyard get no line (L15, L2).
- W gwent: Ghoul -> Vran Warrior: NONE | network.py []
- W gwent: Ozzrel -> Vran Warrior: NONE | network.py []
- W gwent: Ozzrel -> Incubus: NONE | network.py []
- W gwent: Ozzrel -> Witches' Sabbath: NONE | network.py []

## C29 lr2_tb_2.md 5 (CAUSE, gone, 0 table lines from the same code)
Reinforce adding Armor to units that have Armor is linked to cards whose own text never reads Armor (their Armor rows are the keyword's inner working), so it is generic health help (L15, L18).
- W monster_train: Reinforce -> Railbeater: NONE | network.py []
- W monster_train: Reinforce -> Kinhost Pupa: NONE | network.py []

## C30 lr2_tb_4.md 1 (MISSED CAUSE, gone, 0 table lines from the same code)
Snowdrifts deals damage equal to its own strength after it attacks (its text reads the stat), so every card that gives it more strength helps it and keeps its line (L18: reads its power; L24 spirit).
- W stormbound: Big Sisters of Growth -> Snowdrifts: gives it more strength | network.py [1531]
- W stormbound: Fortification Tonic -> Snowdrifts: gives it more strength | network.py [1531]
- W stormbound: Original Blueprints -> Snowdrifts: can give it more strength (when around it) | network.py [1532]
- W stormbound: Emerald Towers -> Snowdrifts: gives it more strength (when ahead of it) | network.py [1531]

