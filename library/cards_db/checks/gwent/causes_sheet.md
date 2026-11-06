## C1 vv_1.md 1 (REAL, open, 7286 table lines from the same code)
the draws shuffle a card back (net zero) or draw by kind only, so nothing fills the hand and no text waits for the draw (L1b, L14).
- W gwent: Selective Mutation -> Geralt: Quen: draws it from the deck; also triggers: fills your hand | network.py [764, 2141]
- W gwent: Selective Mutation -> Vesemir: Mentor: draws it from the deck; also triggers: fills your hand | network.py [2141]
- W gwent: Griffin Witcher Mentor -> Geralt: Quen: fills your hand | network.py [2141]
- W gwent: Pincer Maneuver -> Temple of Melitele: Congregation: fills your hand | network.py [2141]
- R gwent: Geralt: Quen -> Geralt of Rivia: puts it into play from the deck; also triggers: plays it: its effect goes off | network.py []
- R gwent: Oneiromancy -> Geralt: Quen: plays it: its effect goes off | network.py []
  Selective Mutation:
    when 3483 played self
    do 3483 own draw card mine chosen deck keyword is 756153
    do 3483 own shuffle_into_deck card mine chosen hand
    do 3483 own summon
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
  Vesemir: Mentor:
    when 2400 played self
    when 2401 played self
    if 2401 keyword_condition 4.0
    if count le listed card mine hand
    if 2401 count le listed card mine hand
    do 2400 own stat_change unit mine all board type is 34 strength=1.0
    do 2401 own stat_change unit mine all hand type is 34 strength=1.0
    do 2401 own stat_change unit mine all deck type is 34 strength=1.0
  Griffin Witcher Mentor:
    when 3562 played self
    when 3563 played self
    if 3562 keyword_condition not 4.0
    if 3563 keyword_condition 4.0
    if count le listed card mine hand
    if 3562 count le listed card mine hand
    if 3563 count le listed card mine hand
    do 3562 own draw unit mine deck_top
    do 3562 own stat_change unit mine it strength=1.0
    do 3562 own shuffle_into_deck card mine chosen hand
    do 3563 own draw unit mine deck_top
    do 3563 own stat_change unit mine it strength=1.0
    do 3563 own shuffle_into_deck card mine chosen hand
  Pincer Maneuver:
    when 2643 activated self
    when 2644 always
    when 4513 always
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 4513 amount_listed
    do 2643 own draw card mine chosen deck region not Neutral amount=1.0
    do 2643 own shuffle_into_deck card mine chosen hand
    do 2643 own summon
    do 2644 own give_keyword self amount=2.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Temple of Melitele: Congregation:
    when 4102 always
    when 4517 leaves_play self
    when 4103 always
    when 4537 always
    when 4104 always
    when 4541 round_end
    when 4105 played self
    when 4106 activated self
    when 4107 round_won
    when 4108 round_won
    when 4517 leaves_play self
    when 4537 always
    when 4541 round_end
    when 4504 played self
    if 4106 amount_count card mine all hand
    if 4107 have is self hand
    if 4108 have is self deck
    do 4102 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4103 own give_keyword self
    do 4537 uses_keyword cant player all event=targeted
    do 4104 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 4105 own create unit mine random state is gold;region is own_regions;state not started_in_deck
    do 4106 own draw unit mine chosen deck amount=1.0
    do 4106 own stat_change unit mine it strength=count
    do 4106 own shuffle_into_deck card mine chosen hand
    do 4107 own transform self
    do 4108 own transform self
    do 4517 has_keyword obliterate self
    do 4537 has_keyword cant player all event=targeted
    do 4541 has_keyword cant self event=leaves_play
    do 4541 has_keyword remove_keyword self
    do 4504 has_keyword cant self event=activated;turns=1.0

## C2 vv_1.md 3 (REAL, open, 5424 table lines from the same code)
a draw is no help to a card that only has a hand-size limit or reads nothing of the hand (L5, L6, L1).
- W gwent: Ardal aep Dahy -> Eskel: fills your hand | network.py [2141]
- W gwent: Battle Stations! -> Geralt: Yrden: fills your hand; also plays it: its effect goes off | network.py [2141]
- W gwent: Birna Bran -> Arnaghad: fills your hand | network.py [2141]
- R gwent: Eventide Plunder -> Carlo Varese: fills your hand | network.py [2141]
  Ardal aep Dahy:
    when 3930 played self
    if 3930 keyword_condition
    if 3930 have not player mine state is passed
    if 3930 have not player enemy state is passed
    if 3930 count lt 10.0 card enemy hand
    if 3930 have is self position is back_row
    do 3930 own return_to_hand unit enemy chosen board keyword not 756159;strength le 3685
    do 3930 own draw card mine deck_top amount=1.0
  Eskel:
    when 1798 played self
    if 1798 keyword_condition 4.0
    if 1798 count le listed card mine hand
    do 1798 own summon card mine deck card is 756243
    do 1798 own summon card mine deck card is 756244
  Battle Stations!:
    when 4196 played self
    if 4196 amount_event_amount
    do 4196 own play_card card mine chosen hand state is bronze
    do 4196 own draw card mine deck_top amount=event_amount
  Geralt: Yrden:
    when 2436 played self
    when 4568 activated
    when 2437 played self
    when 4568 activated
    if 2436 keyword_condition
    if 2436 keyword_condition not
    if 4568 amount_stat base_power it
    if 2437 keyword_condition
    if 2437 keyword_condition 2.0
    if 4568 amount_stat base_power it
    if count le listed card mine hand
    if 2436 have is self position is front_row
    if 2436 count le listed card mine hand
    if 2437 have is self position is front_row
    if 2437 count le listed card mine hand
    do 2436 own keyword_action unit all board position is same_row of position chosen;of:kind is position
    do 4568 uses_keyword stat_set unit all board position is same_row of position chosen;of:kind is position strength=stat
    do 2437 own keyword_action unit mine all board position is same_row of position mine chosen;of:kind is position
    do 4568 uses_keyword stat_set unit mine all board position is same_row of position mine chosen;of:kind is position strength=stat
  Birna Bran:
    when 2099 played self
    when 4543 activated
    if 2099 amount_event_amount
    do 2099 own draw card mine deck_top max=2.0
    do 2099 own keyword_action card mine chosen hand amount=event_amount
    do 4543 uses_keyword discard card mine chosen hand
  Arnaghad:
    when 3527 played self
    when 4532 damaged self
    when 3528 played unit enemy chosen
    when 4567 activated
    if 3527 amount_count unit all board state is damaged
    if 4532 amount_listed
    if 3528 keyword_condition 4.0
    if 4567 amount_stat strength self
    if 4567 amount_stat strength it
    if count le listed card mine hand
    if 3528 count le listed card mine hand
    do 3527 own give_keyword self amount=count
    do 4532 uses_keyword negate_damage self amount=listed
    do 3528 own keyword_action unit enemy it
    do 4567 uses_keyword damage unit enemy it amount=stat
    do 4567 uses_keyword damage unit enemy it amount=stat

## C3 vv_1.md 4 (REAL, open, 4896 table lines from the same code)
the receiving cards read only their own keyword (self Shield, self Doomed) or have no rows, so having a keyword is no "card it asks for" (L7, L15, L9).
- W gwent: Donimir of Troy -> Windhalm of Attre: is a card it asks for | network.py [1915]
- W gwent: Bear Abomination -> Delirium: is a card it asks for | network.py [1915]
- W gwent: Elder Bear -> Eskel: Pathfinder: is a card it asks for | network.py [1915]
- R gwent: Duda: Companion -> Telianyn aep Collen: is a card it asks for | network.py [1915]
  Donimir of Troy:
    when 3029 always
    when 4565 always
    when 3030 always
    when 4535 damaged self
    when 4565 always
    when 4535 damaged self
    if 4535 amount_event_amount
    if 4535 amount_event_amount
    do 3029 own give_keyword self
    do 4565 uses_keyword cant player enemy event=targeted
    do 3030 own give_keyword self
    do 4535 uses_keyword negate_damage self amount=event_amount
    do 4535 uses_keyword remove_keyword self
    do 4565 has_keyword cant player enemy event=targeted
    do 4535 has_keyword negate_damage self amount=event_amount
    do 4535 has_keyword remove_keyword self
  Windhalm of Attre:
    when 2754 always
    when 4535 damaged self
    when 2755 turn_end
    when 2756 activated self
    when 4535 damaged self
    when 4535 damaged self
    if 4535 amount_event_amount
    if 2755 have is self keyword is 756181
    if 2756 keyword_condition 10.0
    if 4535 amount_event_amount
    if 4535 amount_event_amount
    if 2756 stat strength ge listed self
    do 2754 own give_keyword self
    do 4535 uses_keyword negate_damage self amount=event_amount
    do 4535 uses_keyword remove_keyword self
    do 2755 own stat_change self strength=2.0
    do 2756 own give_keyword self
    do 4535 uses_keyword negate_damage self amount=event_amount
    do 4535 uses_keyword remove_keyword self
    do 4535 has_keyword negate_damage self amount=event_amount
    do 4535 has_keyword remove_keyword self
  Bear Abomination:
    when 4334 always
    when 4517 leaves_play self
    when 4517 leaves_play self
    do 4334 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4517 has_keyword obliterate self
  Delirium:
    when 2161 always
    when 4545 round_start
    when 4517 leaves_play self
    when 2162 played self
    when 2163 played self
    when 4545 round_start
    when 4517 leaves_play self
    if 2162 have not self keyword is 756159
    if 2163 have self keyword is 756159
    do 2161 own give_keyword self
    do 4545 uses_keyword put_on_top self
    do 4545 uses_keyword give_keyword self
    do 4517 uses_keyword obliterate self
    do 2162 own choose_one
    do 2162 own create card mine random state is bronze;region is Skellige;type is 43;state not started_in_deck
    do 2162 own create card mine random state is bronze;region is Skellige;type is 36;state not started_in_deck
    do 2162 own play_card card mine it type is 36
    do 2162 own create card mine it state not started_in_deck
    do 2163 own choose_one
    do 2163 own create card mine random state is gold;region is Skellige;type is 43;state not started_in_deck
    do 2163 own create card mine random state is gold;region is Skellige;type is 36;state not started_in_deck
    do 2163 own play_card card mine it type is 36
    do 2163 own create card mine it state not started_in_deck
    do 4545 has_keyword put_on_top self discard
    do 4545 has_keyword give_keyword self
    do 4517 uses_keyword obliterate self
  Elder Bear:
  Eskel: Pathfinder:
    when 2399 played self
    do 2399 own kill unit enemy chosen board primary_type not None of card mine all deck;of:kind is card;of:state is started_in_deck

## C4 vv_1.md 1 (REAL, open, 1776 table lines from the same code)
Kurt, Witch Hunter, The Witchfinder read only base power and Moreelse deals fixed damage, so more strength helps none of them (L18, L14).
- W gwent: Tamara Strenger -> Kurt: gives it more strength | network.py [1499]
- W gwent: Octavia Hale -> Witch Hunter: can give it more strength | network.py [1500]
- W gwent: Tamara Strenger -> The Witchfinder: gives it more strength | network.py [1499]
- W gwent: Octavia Hale -> Moreelse: can give it more strength | network.py [1500]
  Tamara Strenger:
    when 2857 played self
    do 2857 own stat_change unit mine all board type is 65 strength=1.0
    do 2857 own spend_mana secondary_resource mine amount=3.0
    do 2857 own stat_change unit mine all everywhere type is 65 strength=1.0
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
  Witch Hunter:
    when 2873 played self
    when 4561 dies self
    when 4562 obliterated self
    if 4561 amount_stat base_power self
    if 4562 amount_stat base_power self
    do 2873 own give_keyword unit enemy chosen board
    do 4561 uses_keyword mana_gain secondary_resource enemy amount=stat
    do 4562 uses_keyword mana_gain secondary_resource enemy amount=stat
  The Witchfinder:
    when 3705 played self
    when 3706 turn_end
    when 4561 dies self
    when 4562 obliterated self
    when 4762 played self
    when 4763 turn_end
    when 4561 dies self
    when 4562 obliterated self
    if 3706 have not unit enemy board keyword is 756214
    if 4561 amount_stat base_power self
    if 4562 amount_stat base_power self
    if 4763 have not unit enemy board keyword is 756214
    if 4561 amount_stat base_power self
    if 4562 amount_stat base_power self
    do 3705 own summon amount=3.0
    do 3706 own give_keyword unit enemy highest board
    do 4561 uses_keyword mana_gain secondary_resource enemy amount=stat
    do 4562 uses_keyword mana_gain secondary_resource enemy amount=stat
    do 4762 own summon unit mine amount=3.0
    do 4763 own give_keyword unit enemy highest board
    do 4561 uses_keyword mana_gain secondary_resource enemy amount=stat
    do 4562 uses_keyword mana_gain secondary_resource enemy amount=stat
  Moreelse:
    when 2843 played self
    do 2843 own damage unit enemy chosen board amount=4.0
    do 2843 own spend_mana secondary_resource mine amount=6.0
    do 2843 own kill secondary_resource mine it

## C5 vv_1.md 3 (REAL, open, 1477 table lines from the same code)
Cave Troll only gives itself Defender and Elder Bear has no rows, so nothing reads their power (L18, L14).
- W gwent: Adrenaline Rush -> Cave Troll: can give it more strength | network.py [1500]
- W gwent: Bone Talisman -> Cave Troll: gives it more strength | network.py [1499]
- W gwent: Kelpie -> Elder Bear: can give it more strength | network.py [1500]
- R gwent: Adrenaline Rush -> Lyrian Scytheman: changes units' stats | network.py [1500]
- R gwent: Adrenaline Rush -> Falibor: changes its stats for its effect | network.py [1500]
  Adrenaline Rush:
    when 1850 played self
    if 1850 count eq 1.0 unit mine all board position is same_row of unit mine chosen board;of:kind is unit
    do 1850 own stat_change unit mine chosen board card not 756275 strength=8.0
  Cave Troll:
    when 3061 always
    when 4565 always
    when 4565 always
    do 3061 own give_keyword self
    do 4565 uses_keyword cant player enemy event=targeted
    do 4565 has_keyword cant player enemy event=targeted
  Bone Talisman:
    when 2456 played self
    do 2456 own stat_change unit mine all board strength=1.0
  Kelpie:
    when 4140 played self
    when 4522 turn_start
    when 4141 damaged unit enemy
    if 4140 amount_sum
    if 4140 amount_count unit mine all everywhere type is 43;state is started_in_deck
    if 4140 amount_divided
    do 4140 own give_keyword position enemy chosen turns=sum
    do 4522 uses_keyword damage unit random board position is same_row of self amount=1.0
    do 4141 own stat_change unit mine random board type is 43;boost eq 3900 strength=1.0
  Elder Bear:

## C6 vv_1.md 5 (REAL, open, 1178 table lines from the same code)
Weeping Willow and Treant Boar have fixed effects that never read their power, so more strength is generic (L18, L14).
- W gwent: Nature's Rebuke -> Weeping Willow: can give it more strength | network.py [1500]
- W gwent: Nature's Rebuke -> Treant Boar: can give it more strength | network.py [1500]
- R gwent: Shieldwall -> Cintrian Knight: changes its stats for its effect | network.py []
  Nature's Rebuke:
    when 3237 played self
    when 3238 killed
    when 4705 played self
    when 4706 killed
    do 3237 own damage unit enemy chosen board amount=5.0
    do 3238 own stat_change unit mine random board type is 64 strength=2.0
    do 4705 own damage unit enemy chosen board amount=5.0
    do 4706 own stat_change unit mine random board type is 64 strength=2.0
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
  Treant Boar:
    when 2782 played self
    when 4510 played self
    when 2783 activated self
    when 4515 activated
    when 2784 activated self
    when 2785 always
    when 4511 activated self
    if 2782 have unit mine board type is 58
    if 2783 keyword_condition
    if 4515 amount_full
    if 4515 amount_listed
    if 2784 keyword_condition
    if 4511 amount_listed
    if 2783 have is self position is front_row
    if 2784 have is self position is back_row
    do 2782 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2783 own move self
    do 2783 own keyword_action self
    do 4515 uses_keyword heal self amount=full
    do 4515 uses_keyword heal self amount=listed
    do 2784 own move self
    do 2784 own damage unit enemy chosen board amount=2.0
    do 2785 own keyword_action amount=1.0
    do 4511 uses_keyword cant event=activated;turns=listed

## C7 vv_1.md 2 (PARTLY, open, 598 table lines from the same code)
Geralt of Rivia and Berengar never read their own strength (L18, L14; Berengar keeps only its "is a Witcher it asks for" reason), but Arachas Queen and Kikimore Stalker move the strength of an ally they eat or kill, so boosting insectoids in their row raises what they pass on (L18).
- W gwent: Vesemir: Mentor -> Geralt of Rivia: gives it more strength | network.py [1499]
- W gwent: Vesemir: Mentor -> Berengar: is a Witcher it asks for; also makes stronger: gives it more strength | network.py [1499]
- R gwent: Arachas Behemoth -> Arachas Queen: gives it more strength (when in its row) | network.py [1499]
- R gwent: Kikimore Queen -> Kikimore Stalker: is an Insectoid whose summoning sets off its effect; also makes stronger: gives it more strength (when in its row) | network.py [1499, 1823]
- R gwent: Vesemir: Mentor -> Lyrian Scytheman: changes units' stats | network.py []
- R gwent: Crystal Skull -> Prince Anséis: changes its stats for its effect | network.py []
  Vesemir: Mentor:
    when 2400 played self
    when 2401 played self
    if 2401 keyword_condition 4.0
    if count le listed card mine hand
    if 2401 count le listed card mine hand
    do 2400 own stat_change unit mine all board type is 34 strength=1.0
    do 2401 own stat_change unit mine all hand type is 34 strength=1.0
    do 2401 own stat_change unit mine all deck type is 34 strength=1.0
  Geralt of Rivia:
    when 1778 played self
    do 1778 own kill unit enemy chosen board strength ge 1786
  Berengar:
    when 3485 turn_start
    if 3485 have not unit mine all board type is 34;position is same_row of self;card not 757163
    do 3485 own kill self

## C8 vv_1.md 4 (REAL, open, 554 table lines from the same code)
Vrygheff repeats turn_end effects and Alba Armored Cavalry has only a play effect, so nothing is repeated (L21).
- W gwent: Vrygheff -> Alba Armored Cavalry: repeats its effects | network.py [1464]
- R gwent: Syanna -> Alba Spearman: repeats its Deploy effects; also repeats its effects | network.py [1464]
- R gwent: Syanna -> Aglaïs: repeats its Deploy effects; also repeats its effects | network.py [1464]
  Vrygheff:
    when 2535 always
    when 4510 played self
    when 2536 activated self
    when 4510 played self
    when 4504 played self
    do 2535 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2536 own repeat unit mine chosen board state is bronze;type is 46 event=turn_end
    do 4510 has_keyword can self event=activated
    do 4504 has_keyword cant self event=activated;turns=1.0
  Alba Armored Cavalry:
    when 2406 played self
    when 4523 always
    if 2406 keyword_condition
    if 2406 have is self position is front_row
    do 2406 own give_keyword unit enemy chosen board
    do 4523 uses_keyword silence unit enemy chosen board

## C9 vv_1.md 2 (REAL, open, 492 table lines from the same code)
Aen Elle Conqueror, Wild Hunt Rider, Naglfar Taskmaster and Winter Queen never read their own strength, so the played-unit +1 is generic more power (L18, L14).
- W gwent: Auberon: Conqueror -> Aen Elle Conqueror: gives it more strength when it comes | network.py [2429]
- W gwent: Auberon: Conqueror -> Wild Hunt Rider: gives it more strength when it comes | network.py [2429]
- W gwent: White Frost -> Naglfar Taskmaster: gives it more strength when it comes | network.py [2429]
- W gwent: Auberon: Conqueror -> Winter Queen: gives it more strength when it comes | network.py [2429]
- R gwent: Alp -> Orianna: is a Vampire it asks for; also makes enemy units get Bleeding | network.py []
  Auberon: Conqueror:
    when 4351 always
    when 4519 always
    when 4352 played self
    when 4353 played unit mine type is 23
    when 4519 always
    do 4351 own give_keyword self
    do 4519 uses_keyword cant self event=given_keyword
    do 4352 own create unit mine random state is bronze;type is 23;state is started_in_deck
    do 4352 own play_card unit mine it type is 23
    do 4353 own stat_change unit mine it type is 23 strength=1.0
    do 4519 has_keyword cant self event=given_keyword
  Aen Elle Conqueror:
    when 3333 always
    when 4519 always
    when 3334 played self
    when 4718 always
    when 4519 always
    when 4719 played self
    when 4519 always
    if 3334 keyword_condition not
    if 4719 keyword_condition not
    if have not card mine state is started_in_deck;region is Neutral
    if 3334 have not card mine state is started_in_deck;region is Neutral
    if 4719 have not card mine state is started_in_deck;region is Neutral
    do 3333 own give_keyword self
    do 4519 uses_keyword cant self event=given_keyword
    do 3334 own kill self
    do 4718 own give_keyword self
    do 4519 uses_keyword cant self event=given_keyword
    do 4719 own kill self
    do 4519 has_keyword cant self event=given_keyword
  Wild Hunt Rider:
    when 2010 played self
    if 2010 keyword_condition
    if 2010 amount ge stat
    do 2010 own summon card mine all deck
  White Frost:
    when 2293 activated self
    when 4520 turn_start
    when 2294 always
    when 4513 always
    when 2295 played unit mine type is 23
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 2295 have is position keyword is 756162;position is opposite_row of it
    if 4513 amount_listed
    do 2293 own move unit enemy chosen board
    do 2293 own give_keyword position enemy position is same_row of it turns=2.0
    do 4520 uses_keyword damage unit highest board position is same_row of self amount=2.0
    do 2294 own give_keyword self amount=2.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 2295 own stat_change unit mine it type is 23 strength=1.0
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Naglfar Taskmaster:
    when 3331 played self
    when 4536 activated
    when 3332 played self
    when 4536 activated
    if 3331 keyword_condition not
    if 3332 keyword_condition
    if amount ge stat
    if 3331 amount ge stat
    if 3332 amount ge stat
    do 3331 own keyword_action unit enemy chosen board
    do 4536 uses_keyword remove_keywords unit enemy chosen board
    do 3332 own keyword_action unit chosen board
    do 4536 uses_keyword remove_keywords unit chosen board
  Winter Queen:
    when 3321 turn_end
    when 3322 passed
    if 3321 count ge 2.0 position enemy all keyword is 756162
    if 3322 keyword_condition
    if 3322 have is player mine state is passed
    if 3322 have is player enemy state is passed
    if 3322 amount_stat countdown position enemy all keyword is 756162
    if 3322 amount_product
    if have not card mine state is started_in_deck;region is Neutral
    if 3322 have not card mine state is started_in_deck;region is Neutral
    do 3321 own summon self deck
    do 3322 own stat_change self strength=product

## C10 vv_2.md 3 (REAL, open, 369 table lines from the same code)
more strength for a Pirate or Ship is generic and none of these cards reads strength (L18, L14).
- W gwent: Holger Blackhand -> Tidecloak Hideaway: is a Pirate it asks for; also makes stronger: gives it more strength when it comes | network.py [2429]
- W gwent: Holger Blackhand -> An Craite Longship: gives it more strength when it comes | network.py [2429]
- W gwent: Holger Blackhand -> Bjorn's Drakkar: gives it more strength when it comes | network.py [2429]
  Holger Blackhand:
    when 2118 played self
    when 2119 played card mine type is 59
    when 2120 played card mine type is 60
    do 2118 own damage unit chosen board amount=2.0
    do 2119 own stat_change card mine it type is 59 strength=1.0
    do 2120 own damage unit enemy random board amount=1.0
  Tidecloak Hideaway:
    when 2893 played self
    if 2893 keyword_condition
    if 2893 amount_count card mine all hand type is 60
    if 2893 have is self position is back_row
    do 2893 own stat_change unit mine chosen board strength=count
  An Craite Longship:
    when 2154 played unit enemy
    if 2154 keyword_condition
    if have is self position is front_row
    if 2154 have is self position is front_row
    do 2154 own damage unit enemy it amount=1.0
  Bjorn's Drakkar:
    when 4432 always
    when 4517 leaves_play self
    when 4433 activated self
    when 4434 damaged self
    when 4435 always
    when 4513 always
    when 4517 leaves_play self
    when 4513 always
    when 4504 played self
    if 4434 amount_event_amount
    if 4513 amount_listed
    if 4513 amount_listed
    do 4432 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4433 own damage unit enemy chosen board amount=1.0
    do 4433 own give_ability unit enemy it
    do 4434 gives damage self amount=event_amount
    do 4435 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4517 has_keyword obliterate self
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0

## C11 vv_2.md 4 (REAL, open, 302 table lines from the same code)
Armor is health-like help and these cards' text never uses Armor (L14, L18).
- W gwent: Onslaught -> Tidecloak Hideaway: gives it Armor | network.py [1499]
- W gwent: Onslaught -> An Craite Longship: gives it Armor | network.py [1499]
- W gwent: Crach an Craite -> Dimun Pirate: can give it Armor | network.py [1500]
- W gwent: Crach an Craite -> Deranged Corsair: can give it Armor | network.py [1500]
  Onslaught:
    when 2353 activated self
    when 2354 always
    when 4513 always
    when 2355 damaged unit enemy
    when 4532 damaged self
    when 4639 activated self
    when 4640 always
    when 4513 always
    when 4641 damaged unit enemy
    when 4532 damaged self
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 4532 amount_listed
    if 4513 amount_listed
    if 4532 amount_listed
    if 4513 amount_listed
    do 2353 own damage unit enemy chosen board amount=3.0
    do 2354 own give_keyword self amount=2.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 2355 own give_keyword unit mine all hand type in 60;type in 59 amount=1.0
    do 4532 uses_keyword negate_damage unit mine all hand type in 60;type in 59 amount=listed
    do 4639 own damage unit enemy chosen board amount=3.0
    do 4640 own give_keyword self amount=2.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4641 own give_keyword card mine all hand type in 60;type in 59 amount=1.0
    do 4532 uses_keyword negate_damage card mine all hand type in 60;type in 59 amount=listed
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Tidecloak Hideaway:
    when 2893 played self
    if 2893 keyword_condition
    if 2893 amount_count card mine all hand type is 60
    if 2893 have is self position is back_row
    do 2893 own stat_change unit mine chosen board strength=count
  An Craite Longship:
    when 2154 played unit enemy
    if 2154 keyword_condition
    if have is self position is front_row
    if 2154 have is self position is front_row
    do 2154 own damage unit enemy it amount=1.0
  Crach an Craite:
    when 3631 played self
    when 4532 damaged self
    when 3632 activated self
    when 3633 always
    when 4511 activated self
    when 3634 played unit mine type in 60;type in 59;position is sides of self
    when 4567 activated
    when 4504 played self
    if 4532 amount_listed
    if 4511 amount_listed
    if 4567 amount_stat strength self
    if 4567 amount_stat strength it
    do 3631 own give_keyword card mine chosen hand type in 60;type in 59 amount=2.0
    do 4532 uses_keyword negate_damage card mine chosen hand type in 60;type in 59 amount=listed
    do 3632 own damage unit chosen board amount=1.0
    do 3633 own keyword_action amount=2.0
    do 4511 uses_keyword cant event=activated;turns=listed
    do 3634 own keyword_action unit mine it type in 60;type in 59
    do 4567 uses_keyword damage unit mine it type in 60;type in 59 amount=stat
    do 4567 uses_keyword damage unit mine it type in 60;type in 59 amount=stat
    do 4504 has_keyword cant self event=activated;turns=1.0
  Dimun Pirate:
    when 2139 played self
    if 2139 have not unit mine all board type is 59
    do 2139 own move card mine top deck
  Deranged Corsair:
    when 3858 played self
    when 3859 dies self
    when 4514 turn_start
    when 4514 turn_start
    do 3858 own give_ability unit enemy chosen board
    do 3859 gives give_keyword position position is same_row of self turns=2.0
    do 4514 uses_keyword damage unit random board position is same_row of self amount=3.0;spread=1.0
    do 3858 own give_keyword position enemy position is same_row of it turns=1.0
    do 4514 uses_keyword damage unit random board position is same_row of self amount=3.0;spread=1.0

## C12 vv_1.md 3 (PARTLY, open, 246 table lines from the same code)
Roderick of Dun Tynne and Torres var Emreis: Founder never read their own strength (L18; Torres keeps its "creates cards" reason), but False Ciri levels off at "strength ge" a threshold on stat_changed, so power helps her (L18, L24).
- W gwent: Imposter -> Roderick of Dun Tynne: gives it more strength when it comes | network.py [2429]
- W gwent: Imposter -> Torres var Emreis: Founder: creates cards: Torres var Emreis: Founder copys them; also makes stronger: gives it more strength when it comes | network.py [2429]
- R gwent: Imposter -> False Ciri: gives it more strength when it comes | network.py [2429]
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
  Roderick of Dun Tynne:
    when 2729 always
    when 4527 always
    when 4528 played self
    when 4569 always
    when 2730 played self
    when 4527 always
    when 4528 played self
    when 4569 always
    do 2729 own give_keyword self
    do 4527 uses_keyword can self event=summoned
    do 4528 uses_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
    do 2730 own look card mine random deck state is gold
    do 2730 own choose_card card mine chosen deck
    do 2730 own play_card card mine it
    do 4527 has_keyword can self event=summoned
    do 4528 has_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
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

## C13 vv_2.md 3 (REAL, open, 207 table lines from the same code)
removing a Shield helps any damage card, which is generic and not the card's own text (L18, L4).
- W gwent: Tourney Joust -> Impera Enforcers: removes their Block: its damage gets through | network.py [2318]
- W gwent: Tourney Joust -> Ace up the Sleeve: removes their Block: its damage gets through | network.py [2318]
- W gwent: Tourney Joust -> Coup de Grâce: removes their Block: its damage gets through | network.py [2318]
  Tourney Joust:
    when 2733 played self
    when 4535 damaged self
    if 4535 amount_event_amount
    do 2733 own choose_one
    do 2733 own remove_keyword unit enemy chosen board
    do 2733 own damage unit enemy it amount=4.0
    do 2733 own give_keyword unit mine chosen board
    do 4535 uses_keyword negate_damage unit mine chosen board amount=event_amount
    do 4535 uses_keyword remove_keyword unit mine chosen board
    do 2733 own stat_change unit mine it strength=4.0
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
  Ace up the Sleeve:
    when 4465 always
    when 4517 leaves_play self
    when 4466 played self
    when 4517 leaves_play self
    do 4465 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4466 own damage unit enemy chosen board amount=2.0
    do 4517 has_keyword obliterate self
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

## C14 vv_2.md 4 (REAL, open, 138 table lines from the same code)
removing a Shield is generic help for any damage and these cards only deal damage as one part of their text (L18, L2).
- W gwent: Tourney Joust -> Ard Feainn Heavy Cavalry: removes their Block: its damage gets through | network.py [2318]
- W gwent: Tourney Joust -> Ivar Evil-Eye: removes their Block: its damage gets through | network.py [2318]
  Tourney Joust:
    when 2733 played self
    when 4535 damaged self
    if 4535 amount_event_amount
    do 2733 own choose_one
    do 2733 own remove_keyword unit enemy chosen board
    do 2733 own damage unit enemy it amount=4.0
    do 2733 own give_keyword unit mine chosen board
    do 4535 uses_keyword negate_damage unit mine chosen board amount=event_amount
    do 4535 uses_keyword remove_keyword unit mine chosen board
    do 2733 own stat_change unit mine it strength=4.0
  Ard Feainn Heavy Cavalry:
    when 3093 always
    when 4546 turn_end
    when 4547 turn_end
    when 4532 damaged self
    when 3094 turn_end
    when 4532 damaged self
    when 3095 stat_changed self
    when 3096 played unit enemy
    when 4523 always
    when 4546 turn_end
    when 4547 turn_end
    when 4532 damaged self
    if 4546 count eq 1.0 unit mine board position is sides of self
    if 4546 have is self position is front_row
    if 4547 count eq 1.0 unit mine board position is sides of self
    if 4547 have is self position is back_row
    if 4532 amount_listed
    if 4532 amount_listed
    if 3095 keyword_condition
    if 3095 stat armor ge 5.0 self
    if 3096 keyword_condition
    if 3096 keyword_condition
    if 3096 amount_stat armor self
    if 4546 count eq 1.0 unit mine board position is sides of self
    if 4546 have is self position is front_row
    if 4547 count eq 1.0 unit mine board position is sides of self
    if 4547 have is self position is back_row
    if 4532 amount_listed
    if have is self position is back_row
    if 3095 have is self position is back_row
    if 3096 have is self keyword is 756174
    if 3096 have is self position is front_row
    do 3093 own give_keyword self
    do 4546 uses_keyword repeat self
    do 4547 uses_keyword give_keyword self amount=1.0
    do 4532 uses_keyword negate_damage self amount=listed
    do 3094 own give_keyword self amount=1.0
    do 4532 uses_keyword negate_damage self amount=listed
    do 3095 own move self
    do 3096 own damage unit enemy it amount=stat
    do 3096 own remove_keyword self
    do 3096 own give_keyword self
    do 4523 uses_keyword silence self
    do 4546 has_keyword repeat self
    do 4547 has_keyword give_keyword self amount=1.0
    do 4532 uses_keyword negate_damage self amount=listed
  Ivar Evil-Eye:
    when 3488 played self
    when 3489 played self
    if 3488 keyword_condition not
    if 3489 keyword_condition 2.0
    if count le listed card mine hand
    if 3488 count le listed card mine hand
    if 3489 count le listed card mine hand
    do 3488 own swap_stats self
    do 3489 own damage unit enemy chosen board amount=4.0

## C15 vv_2.md 3 (REAL, open, 120 table lines from the same code)
Bernard Loredo's duel summons no Soldier and Northern Wind banishes only its own kills, so neither card's effect goes off (L16, L3).
- W gwent: Bernard Loredo -> Boholt: is a Soldier whose summoning sets off its effect | network.py [1823]
- W gwent: Bernard Loredo -> Northern Wind: dies by its own effect: Northern Wind Banishes them | network.py []
- R gwent: Berengar -> Hjalmar an Craite: dies by its own effect: Hjalmar an Craite Banishes them | network.py []
  Bernard Loredo:
    when 4239 activated self
    when 4552 activated
    when 4504 played self
    if 4552 amount_stat strength self
    if 4552 amount_stat strength it
    do 4239 own keyword_action self
    do 4552 uses_keyword damage self amount=stat
    do 4552 uses_keyword damage self amount=stat
    do 4552 uses_keyword repeat self
    do 4504 has_keyword cant self event=activated;turns=1.0
  Boholt:
    when 4038 always
    when 4524 played self
    when 4510 played self
    when 4525 played self
    when 4039 activated self
    when 4040 summoned unit mine type is 46
    when 4524 played self
    when 4510 played self
    when 4525 played self
    when 4504 played self
    if 4524 have is self position is front_row
    if 4525 have is self position is back_row
    if 4524 have is self position is front_row
    if 4525 have is self position is back_row
    do 4038 own give_keyword self
    do 4524 uses_keyword give_keyword self
    do 4510 uses_keyword can self event=activated
    do 4525 uses_keyword stat_change self strength=1.0
    do 4039 own copy unit mine chosen board state is bronze;type is 46
    do 4040 own stat_change self strength=2.0
    do 4524 has_keyword give_keyword self
    do 4510 uses_keyword can self event=activated
    do 4525 has_keyword stat_change self strength=1.0
    do 4504 has_keyword cant self event=activated;turns=1.0
  Northern Wind:
    when 2680 played self
    when 2681 killed
    when 4516 activated
    do 2680 own damage unit chosen board amount=4.0
    do 2681 own keyword_action unit it discard
    do 4516 uses_keyword obliterate unit it discard

## C16 vv_2.md 2 (REAL, open, 118 table lines from the same code)
Vitality given to Berengar helps nothing because Berengar's text never uses Vitality (L14, L6).
- W gwent: Inspirational Ballad -> Berengar: can give it Vitality | network.py [1500]
- R gwent: Witch Hunter -> Vigilantes: makes enemy units get Bounty | network.py []
  Inspirational Ballad:
    when 2686 played self
    when 4534 turn_end
    when 4534 turn_end
    when 4534 turn_end
    when 4534 turn_end
    do 2686 own give_keyword unit mine random board type is 34 amount=6.0
    do 4534 uses_keyword stat_change unit mine random board type is 34 strength=1.0
    do 2686 own give_keyword unit mine random board type is 39 amount=6.0
    do 4534 uses_keyword stat_change unit mine random board type is 39 strength=1.0
    do 2686 own give_keyword unit mine random board type is 36 amount=6.0
    do 4534 uses_keyword stat_change unit mine random board type is 36 strength=1.0
    do 2686 own give_keyword unit mine random board type is 35 amount=6.0
    do 4534 uses_keyword stat_change unit mine random board type is 35 strength=1.0
  Berengar:
    when 3485 turn_start
    if 3485 have not unit mine all board type is 34;position is same_row of self;card not 757163
    do 3485 own kill self

## C17 vv_2.md 1 (REAL, open, 27 table lines from the same code)
Naiad Fledgling removes Vitality for its own strength, so the Vitality makers feed it and its own gift to its left neighbour is no need of Frog, Cat Witcher Adept or Nature's Gift (L6, L14).
- W gwent: Naiad Fledgling -> Frog: keeps the Vitality it gives itself off it | network.py [1508]
- W gwent: Naiad Fledgling -> Cat Witcher Adept: keeps the Vitality it gives itself off it | network.py [1508]
- W gwent: Naiad Fledgling -> Nature's Gift: keeps the Vitality it gives itself off it | network.py [1508]
- R gwent: Nature's Gift -> Freixenet: gives it Vitality for its effect; also makes stronger: does what it waits for or counts (given keyword) | network.py [1500]
  Naiad Fledgling:
    when 4036 keyword_used keyword is 756204
    when 4534 turn_end
    when 4037 activated self
    when 4504 played self
    if 4037 amount_event_amount
    do 4036 own give_keyword unit left_of_self amount=2.0
    do 4534 uses_keyword stat_change unit left_of_self strength=1.0
    do 4037 own remove_keyword unit mine chosen board
    do 4037 own stat_change self strength=event_amount
    do 4504 has_keyword cant self event=activated;turns=1.0
  Frog:
    when 4437 always
    when 4517 leaves_play self
    when 4438 turn_end
    when 4534 turn_end
    when 4439 activated self
    when 4517 leaves_play self
    when 4504 played self
    do 4437 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4438 own give_keyword unit all board position is sides of self
    do 4534 uses_keyword stat_change unit all board position is sides of self strength=1.0
    do 4439 own move self
    do 4517 has_keyword obliterate self
    do 4504 has_keyword cant self event=activated;turns=1.0
  Cat Witcher Adept:
    when 3524 played self
    when 4526 turn_end
    when 3525 played self
    when 4534 turn_end
    if 3524 keyword_condition
    if 3524 amount_count unit all board position is same_row of it
    if 3525 keyword_condition
    if 3525 amount_count unit all board position is same_row of it
    if 3524 have is self position is front_row
    if 3525 have is self position is back_row
    do 3524 own give_keyword unit enemy chosen board amount=count
    do 4526 uses_keyword damage unit enemy chosen board amount=1.0
    do 3525 own give_keyword unit mine chosen board amount=count
    do 4534 uses_keyword stat_change unit mine chosen board strength=1.0
  Nature's Gift:
    when 2363 always
    when 4551 played card mine type is 26
    when 2364 activated self
    when 4534 turn_end
    when 2365 always
    when 4513 always
    when 4551 played card mine type is 26
    when 4513 always
    when 4504 played self
    if 4551 amount_count unit mine board keyword is 756204
    if 4513 amount_listed
    if 4551 amount_count unit mine board keyword is 756204
    if 4513 amount_listed
    do 2363 own give_keyword self
    do 4551 uses_keyword summon unit mine
    do 4551 uses_keyword stat_set unit mine it card is 813637 strength=count
    do 2364 own give_keyword unit mine chosen board amount=2.0
    do 4534 uses_keyword stat_change unit mine chosen board strength=1.0
    do 2365 own give_keyword self amount=3.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4551 has_keyword summon unit mine
    do 4551 has_keyword stat_set unit mine it card is 813637 strength=count
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0

## C18 vv_2.md 5 (REAL, open, 23 table lines from the same code)
Dwimveandra refreshes only a landmark and Flotsam is a unit, so "lets you use it again" does not fit (L8, L14).
- W gwent: Dwimveandra -> Flotsam: lets you use it again | network.py [1508]
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
  Flotsam:
    when 4240 always
    when 4541 round_end
    when 4241 played self
    when 4242 activated self
    when 4510 played self
    when 4811 always
    when 4541 round_end
    when 4812 played self
    when 4813 activated self
    when 4510 played self
    when 4541 round_end
    when 4504 played self
    do 4240 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 4241 own create unit mine random state is bronze;region is Northern Realms;keyword is 756143
    do 4242 own refresh unit mine chosen board state is bronze
    do 4242 own give_keyword unit mine it
    do 4510 uses_keyword can unit mine it event=activated
    do 4811 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 4812 own create unit mine random state is bronze;region is Northern Realms;keyword is 756143
    do 4813 own refresh unit mine chosen board state is bronze
    do 4813 own give_keyword unit mine it
    do 4510 uses_keyword can unit mine it event=activated
    do 4541 has_keyword cant self event=leaves_play
    do 4541 has_keyword remove_keyword self
    do 4504 has_keyword cant self event=activated;turns=1.0

## C19 vv_2.md 2 (REAL, open, 7 table lines from the same code)
Loc Feainn: Convergence makes a Scoiatael unit but Pavko Gale asks for a Neutral unit, and a made card must be the kind the need asks (L20).
- W gwent: Loc Feainn: Convergence -> Pavko Gale: makes a unit it asks for | network.py [1919]
- R gwent: Pavko Gale -> Mysteries of Loc Feainn: is a unit whose playing sets off its effect | network.py [1823]
  Loc Feainn: Convergence:
    when 4442 always
    when 4517 leaves_play self
    when 4443 played self
    when 4517 leaves_play self
    do 4442 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4443 own create unit mine chosen board state is bronze;region is Scoiatael;state is primary_category_not_controlled
    do 4517 has_keyword obliterate self
  Pavko Gale:
    when 2537 always
    when 4553 played unit mine region not Neutral
    when 2538 activated self
    when 2539 activated self
    when 2540 always
    when 4511 activated self
    when 4553 played unit mine region not Neutral
    if 4553 have not unit mine board state is shares_subtype_with_it
    if 4553 amount_listed
    if 2538 keyword_condition
    if 2538 have is unit mine board region is Neutral
    if 2539 keyword_condition
    if 2539 have not unit mine board region is Neutral
    if 4511 amount_listed
    if 4553 have not unit mine board state is shares_subtype_with_it
    if 4553 amount_listed
    if 2538 have is self position is back_row
    if 2539 have is self position is back_row
    do 2537 own give_keyword self
    do 4553 uses_keyword stat_change self strength=listed
    do 2538 own damage unit chosen board amount=1.0
    do 2539 own damage unit chosen board amount=2.0
    do 2540 own keyword_action amount=1.0
    do 4511 uses_keyword cant event=activated;turns=listed
    do 4553 has_keyword stat_change self strength=listed

## C20 vv_2.md 6 (PARTLY, open, 0 table lines from the same code)
Eventide Plunder makes a unit that is no Firesworn token, so Procession of Penance's count is not fed (L20), but Mahakam Defender's own text reads Armor so Armor givers keep their line (L14).
- W gwent: Eventide Plunder -> Procession of Penance: creates cards | network.py []
- R gwent: Barclay Els -> Mahakam Defender: gives it Armor for its effect; also gives keyword: gives it Armor | network.py [1499]
- R gwent: Wagenburg -> Ard Feainn Tortoise: gives it Armor for its effect; also makes stronger: does what it waits for or counts (given keyword) (when next to it) | network.py [1500]
  Eventide Plunder:
    when 2903 played self
    do 2903 own create unit mine random cost eq 2758;keyword is 756213
  Procession of Penance:
    when 2930 played self
    if 2930 amount_sum
    if 2930 amount_product
    if 2930 amount_count unit mine all board type is 20;state is token
    if 2930 amount_minus
    do 2930 own damage self amount=sum

## C21 vv_3.md 2 (MISSED REAL, open, 0 table lines from the same code)
Naiad Fledgling removes a keyword from a unit and takes its amount, so it waits for a card to have what the givers put on, a thing a card waits for or counts (L14).
- W gwent: Frog -> Naiad Fledgling: NONE | network.py []
- W gwent: Cat Witcher Adept -> Naiad Fledgling: NONE | network.py []
- W gwent: Dryad's Caress -> Naiad Fledgling: NONE | network.py []
- W gwent: Frog Mating Season -> Naiad Fledgling: NONE | network.py []
- R gwent: Nature's Gift -> Naiad Fledgling: has Symbiosis | network.py []
  Frog:
    when 4437 always
    when 4517 leaves_play self
    when 4438 turn_end
    when 4534 turn_end
    when 4439 activated self
    when 4517 leaves_play self
    when 4504 played self
    do 4437 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4438 own give_keyword unit all board position is sides of self
    do 4534 uses_keyword stat_change unit all board position is sides of self strength=1.0
    do 4439 own move self
    do 4517 has_keyword obliterate self
    do 4504 has_keyword cant self event=activated;turns=1.0
  Naiad Fledgling:
    when 4036 keyword_used keyword is 756204
    when 4534 turn_end
    when 4037 activated self
    when 4504 played self
    if 4037 amount_event_amount
    do 4036 own give_keyword unit left_of_self amount=2.0
    do 4534 uses_keyword stat_change unit left_of_self strength=1.0
    do 4037 own remove_keyword unit mine chosen board
    do 4037 own stat_change self strength=event_amount
    do 4504 has_keyword cant self event=activated;turns=1.0
  Cat Witcher Adept:
    when 3524 played self
    when 4526 turn_end
    when 3525 played self
    when 4534 turn_end
    if 3524 keyword_condition
    if 3524 amount_count unit all board position is same_row of it
    if 3525 keyword_condition
    if 3525 amount_count unit all board position is same_row of it
    if 3524 have is self position is front_row
    if 3525 have is self position is back_row
    do 3524 own give_keyword unit enemy chosen board amount=count
    do 4526 uses_keyword damage unit enemy chosen board amount=1.0
    do 3525 own give_keyword unit mine chosen board amount=count
    do 4534 uses_keyword stat_change unit mine chosen board strength=1.0
  Dryad's Caress:
    when 2786 played self
    when 4536 activated
    when 2787 played self
    when 4534 turn_end
    if 2787 have unit mine board type is 58
    do 2786 own keyword_action unit mine chosen board
    do 4536 uses_keyword remove_keywords unit mine chosen board
    do 2786 own stat_change unit mine it strength=3.0
    do 2787 own give_keyword it amount=3.0
    do 4534 uses_keyword stat_change it strength=1.0
  Frog Mating Season:
    when 4033 played self
    when 4534 turn_end
    do 4033 own give_keyword unit mine chosen board amount=4.0
    do 4534 uses_keyword stat_change unit mine chosen board strength=1.0
    do 4033 own summon

## C22 vv_3.md 4 (REAL, open, 0 table lines from the same code)
Simlas Finn aep Dabairr plays a bronze spell from the deck and copies of it, never a unit, and Bountiful Harvest makes a card of the kind its rows name, so neither is linked to units of another kind (L17, L20).
- W gwent: Simlas Finn aep Dabairr -> Fauve: plays it: its effect goes off | network.py []
- W gwent: Simlas Finn aep Dabairr -> Filavandrel aén Fidháil: plays it: its effect goes off | network.py []
- W gwent: Simlas Finn aep Dabairr -> Cat Witcher Adept: plays it: its effect goes off | network.py []
- W gwent: Bountiful Harvest -> Cat Witcher Adept: plays it: its effect goes off | network.py []
- R gwent: Isengrim's Council -> Fauve: puts it into play from the deck; also triggers: plays it: its effect goes off | network.py []
- R gwent: Call of the Forest -> Cat Witcher Adept: plays it: its effect goes off | network.py []
  Simlas Finn aep Dabairr:
    when 3737 played self
    do 3737 own play_card card mine chosen deck state is bronze;category is spell
    do 3737 own play_card card mine all deck state is copy_of_it
  Fauve:
    when 2773 played self
    do 2773 own play_card card mine chosen deck type is 26
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
  Cat Witcher Adept:
    when 3524 played self
    when 4526 turn_end
    when 3525 played self
    when 4534 turn_end
    if 3524 keyword_condition
    if 3524 amount_count unit all board position is same_row of it
    if 3525 keyword_condition
    if 3525 amount_count unit all board position is same_row of it
    if 3524 have is self position is front_row
    if 3525 have is self position is back_row
    do 3524 own give_keyword unit enemy chosen board amount=count
    do 4526 uses_keyword damage unit enemy chosen board amount=1.0
    do 3525 own give_keyword unit mine chosen board amount=count
    do 4534 uses_keyword stat_change unit mine chosen board strength=1.0
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

## C23 vv_3.md 5 (MISSED REAL, open, 0 table lines from the same code)
Simlas Finn aep Dabairr puts a spell from the deck into play by kind, like Fauve does (Fauve -> Tempering), so it feeds the spells that go off when played (L17).
- W gwent: Simlas Finn aep Dabairr -> Circle of Life: NONE | network.py []
- W gwent: Simlas Finn aep Dabairr -> Tempering: NONE | network.py []
- W gwent: Simlas Finn aep Dabairr -> Frog Mating Season: NONE | network.py []
- R gwent: Fauve -> Tempering: puts it into play from the deck | network.py []
  Simlas Finn aep Dabairr:
    when 3737 played self
    do 3737 own play_card card mine chosen deck state is bronze;category is spell
    do 3737 own play_card card mine all deck state is copy_of_it
  Circle of Life:
    when 3462 played self
    when 3463 killed
    do 3462 own damage unit enemy chosen board amount=3.0
    do 3462 own stat_change unit mine random hand region not Neutral strength=2.0
    do 3463 own stat_change unit mine chosen hand region not Neutral strength=2.0
  Tempering:
    when 3133 played self
    when 4532 damaged self
    when 4698 played self
    when 4532 damaged self
    if 4532 amount_listed
    if 4532 amount_listed
    do 3133 own stat_change unit mine chosen board strength=5.0
    do 3133 own give_keyword unit mine it board type is 39 amount=2.0
    do 4532 uses_keyword negate_damage unit mine it board type is 39 amount=listed
    do 4698 own stat_change unit mine chosen board strength=5.0
    do 4698 own give_keyword unit mine it board type is 39 amount=2.0
    do 4532 uses_keyword negate_damage unit mine it board type is 39 amount=listed
  Frog Mating Season:
    when 4033 played self
    when 4534 turn_end
    do 4033 own give_keyword unit mine chosen board amount=4.0
    do 4534 uses_keyword stat_change unit mine chosen board strength=1.0
    do 4033 own summon

## C24 vv_3.md 6 (REAL, open, 0 table lines from the same code)
Mahakam Pass creates cards in hand, not in the deck Isengrim's Council plays from, and Bountiful Harvest boosts any card in hand so creating one is no help (L19, L14).
- W gwent: Mahakam Pass -> Isengrim's Council: makes a Dwarf it asks for | network.py []
- W gwent: Mahakam Pass -> Bountiful Harvest: creates cards | network.py []
- R gwent: Mahakam Pass -> Tempering: creates | network.py []
  Mahakam Pass:
    when 4277 always
    when 4541 round_end
    when 4278 played self
    when 4532 damaged self
    when 4279 activated self
    when 4541 round_end
    when 4504 played self
    if 4532 amount_listed
    do 4277 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 4278 own create card mine random region is Scoiatael;type is 39
    do 4278 own give_keyword card mine it type is 39 amount=4.0
    do 4532 uses_keyword negate_damage card mine it type is 39 amount=listed
    do 4279 own create
    do 4279 own play_card card mine it card is 757004
    do 4541 has_keyword cant self event=leaves_play
    do 4541 has_keyword remove_keyword self
    do 4504 has_keyword cant self event=activated;turns=1.0
  Isengrim's Council:
    when 2472 played self
    do 2472 own look card mine random deck type is 39
    do 2472 own look card mine random deck type is 58
    do 2472 own look card mine random deck type is 40
    do 2472 own play_card card mine chosen deck type in 39;type in 58;type in 40
    do 2472 own stat_change card mine it type in 39;type in 58;type in 40 strength=2.0
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

## C25 vv_3.md 7 (MISSED PARTLY, open, 0 table lines from the same code)
Call of the Forest plays a non-Neutral unit from the deck, so Mahakam Pass with its play effect needs a line (L17), while Naiad Pondkeeper already has one.
- W gwent: Call of the Forest -> Mahakam Pass: NONE | network.py []
- R gwent: Call of the Forest -> Naiad Pondkeeper: plays it: its effect goes off | network.py []
- R gwent: Call of the Forest -> Fauve: plays it: its effect goes off | network.py []
  Call of the Forest:
    when 2570 played self
    do 2570 own play_card unit mine chosen deck region not Neutral
    do 2570 own stat_change unit mine it strength=1.0
  Mahakam Pass:
    when 4277 always
    when 4541 round_end
    when 4278 played self
    when 4532 damaged self
    when 4279 activated self
    when 4541 round_end
    when 4504 played self
    if 4532 amount_listed
    do 4277 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 4278 own create card mine random region is Scoiatael;type is 39
    do 4278 own give_keyword card mine it type is 39 amount=4.0
    do 4532 uses_keyword negate_damage card mine it type is 39 amount=listed
    do 4279 own create
    do 4279 own play_card card mine it card is 757004
    do 4541 has_keyword cant self event=leaves_play
    do 4541 has_keyword remove_keyword self
    do 4504 has_keyword cant self event=activated;turns=1.0

## C26 vv_3.md 8 (REAL, open, 0 table lines from the same code)
Dancing Star, Dimeritium Bomb, Waylay and Guerilla Tactics only hit one chosen target, and a plain hit on one target feeds no "when an enemy dies" (L11).
- W gwent: Dancing Star -> Saesenthessis: Blaze: makes enemy units die | network.py []
- W gwent: Dimeritium Bomb -> Saesenthessis: Blaze: makes enemy units die | network.py []
- W gwent: Waylay -> Saesenthessis: Blaze: makes enemy units die | network.py []
- W gwent: Guerilla Tactics -> Saesenthessis: Blaze: makes enemy units die | network.py []
- R gwent: Ocvist -> Saesenthessis: Blaze: is a Dragon it asks for; also triggers: makes enemy units die | network.py []
- R gwent: Madoc -> Saesenthessis: Blaze: makes enemy units die | network.py []
  Dancing Star:
    when 2676 played self
    when 2677 killed
    do 2676 own damage unit enemy chosen board amount=3.0
    do 2677 own damage unit enemy right_of_self board amount=2.0
  Saesenthessis: Blaze:
    when 2469 always
    when 4507 game_start
    when 2470 dies unit enemy
    when 2471 obliterated unit enemy
    when 4507 game_start
    if 4507 amount_count card mine type is 38;state is started_in_deck
    if 2470 my_turn
    if 2471 my_turn
    if 4507 amount_count card mine type is 38;state is started_in_deck
    do 2469 own give_keyword self
    do 4507 uses_keyword stat_change self strength=count
    do 2470 own stat_change self strength=1.0
    do 2471 own stat_change self strength=1.0
    do 4507 has_keyword stat_change self strength=count
  Dimeritium Bomb:
    when 1837 played self
    when 4519 always
    when 4572 played self
    when 4519 always
    do 1837 own damage unit chosen board amount=4.0
    do 1837 own give_keyword unit it
    do 4519 uses_keyword cant unit it event=given_keyword
    do 4572 own damage unit chosen board amount=4.0
    do 4572 own give_keyword unit it
    do 4519 uses_keyword cant unit it event=given_keyword
  Waylay:
    when 2076 played self
    do 2076 own damage unit enemy chosen board amount=3.0
    do 2076 own summon
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

## C27 vv_3.md 9 (REAL, open, 0 table lines from the same code)
Myrgtabrakke moves a card from hand to the deck bottom, not a unit on the board, so it helps no card that acts on its board position (L23, L7).
- W gwent: Myrgtabrakke -> Filavandrel aén Fidháil: Myrgtabrakke moves Filavandrel aén Fidháil, and Filavandrel aén Fidháil acts on units back row it or front row it | network.py []
- R gwent: Guerilla Tactics -> Filavandrel aén Fidháil: Guerilla Tactics moves Filavandrel aén Fidháil, and Filavandrel aén Fidháil acts on units back row it or front row it | network.py []
- R gwent: Samum -> Filavandrel aén Fidháil: Samum moves Filavandrel aén Fidháil, and Filavandrel aén Fidháil acts on units back row it or front row it | network.py []
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

## C28 vv_3.md 3 (REAL, open, 0 table lines from the same code)
Cursed Scroll moves a card from hand to the deck bottom, not units on the board, so it helps no card that acts on units in a row (L1, L16).
- W gwent: Cursed Scroll -> Arachas Behemoth: Cursed Scroll moves Arachas Behemoth and your units, and Arachas Behemoth acts on units in its row | network.py []
- W gwent: Cursed Scroll -> Kikimore Queen: Cursed Scroll moves Kikimore Queen and your units, and Kikimore Queen acts on units in its row | network.py []
- W gwent: Cursed Scroll -> Orchard Mantrap: Cursed Scroll moves Orchard Mantrap, and Orchard Mantrap acts on units back row it or front row it | network.py []
- W gwent: Cursed Scroll -> Whispess: Tribute: Cursed Scroll moves Whispess: Tribute, and Whispess: Tribute acts on units back row it | network.py []
  Cursed Scroll:
    when 3156 activated self
    when 4504 played self
    do 3156 own draw card mine chosen deck amount=1.0
    do 3156 own move card mine chosen hand
    do 4504 has_keyword cant self event=activated;turns=1.0
  Arachas Behemoth:
    when 1960 played self
    do 1960 own summon amount=2.0
    do 1960 own stat_change unit mine all board type is 53;position is same_row of self strength=1.0
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
  Whispess: Tribute:
    when 2383 played self
    when 4643 played self
    if 2383 keyword_condition
    if 4643 keyword_condition
    if 2383 have is self position is back_row
    if 4643 have is self position is back_row
    do 2383 own play_card card mine chosen deck type is 28
    do 4643 own play_card card mine chosen deck type is 28

## C29 vv_3.md 4 (REAL, open, 0 table lines from the same code)
Siege has no Order, it only has a played effect, so it is not the Order card Lyrian Arbalest waits for (L10, L7).
- W gwent: Siege -> Lyrian Arbalest: is played | network.py []
- R gwent: Pincer Maneuver -> Lyrian Arbalest: is a card whose playing sets off its effect | network.py [1823]
- R gwent: Reinforced Ballista -> Lyrian Arbalest: is a card whose playing sets off its effect | network.py [1823]
  Siege:
    when 3163 always
    when 4517 leaves_play self
    when 3164 played self
    when 3165 played unit mine type is 51
    when 3166 played unit mine type is 51
    when 4517 leaves_play self
    if 3165 stage 1.0
    if 3166 stage 2.0
    do 3163 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 3164 own summon
    do 3165 own summon
    do 3166 own create card mine
    do 3166 own play_card card mine it card is 756310
    do 4517 has_keyword obliterate self
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

## C30 vv_3.md 5 (REAL, open, 0 table lines from the same code)
Arachas Queen uses Consume, and Kikimore Queen waits only for Thrive being used, a keyword's inner working is no need (L15, L10).
- W gwent: Arachas Queen -> Kikimore Queen: uses a keyword or status | network.py []
- R gwent: Orchard Mantrap -> Kikimore Queen: uses a keyword or status; also makes stronger: does what it waits for or counts (keyword used) | network.py [1500]
- R gwent: Sir Scratch-a-Lot -> Kikimore Queen: lets it do more (keyword_used) | network.py [1499]
  Arachas Queen:
    when 3927 played self
    when 4538 activated
    when 4516 activated
    when 3928 activated self
    when 3929 dies self
    when 4504 played self
    if 4538 amount_stat strength it
    do 3927 own keyword_action unit mine chosen board
    do 4538 uses_keyword kill unit mine chosen board
    do 4538 uses_keyword stat_change unit mine chosen board strength=stat
    do 4538 uses_keyword keyword_action unit mine chosen board
    do 4516 uses_keyword obliterate unit mine chosen board
    do 3928 own create
    do 3928 own play_card card mine chosen hand card is 756376
    do 3929 own copy it state is created
    do 4504 has_keyword cant self event=activated;turns=1.0
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

## C31 vv_3.md 6 (MISSED REAL, open, 0 table lines from the same code)
Onager waits for an Order being used and each of these cards has an Order, and a keyword trigger links to every card with it however common (L10, L21).
- W gwent: Pincer Maneuver -> Onager: NONE | network.py []
- W gwent: Kerack City Guard -> Onager: NONE | network.py []
- W gwent: Prince Anséis -> Onager: NONE | network.py []
- W gwent: Reinforced Ballista -> Onager: NONE | network.py []
- R gwent: Onager -> Siege Master: is a Siege Engine whose playing sets off its effect | network.py [1823]
  Pincer Maneuver:
    when 2643 activated self
    when 2644 always
    when 4513 always
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 4513 amount_listed
    do 2643 own draw card mine chosen deck region not Neutral amount=1.0
    do 2643 own shuffle_into_deck card mine chosen hand
    do 2643 own summon
    do 2644 own give_keyword self amount=2.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Onager:
    when 4244 keyword_used keyword is 756143
    do 4244 own damage unit enemy random board amount=1.0
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
  Prince Anséis:
    when 2746 always
    when 4524 played self
    when 4510 played self
    when 4525 played self
    when 2747 activated self
    when 2748 activated self
    when 4552 activated
    when 4524 played self
    when 4510 played self
    when 4525 played self
    when 4504 played self
    if 4524 have is self position is front_row
    if 4525 have is self position is back_row
    if 2747 keyword_condition not
    if 2748 keyword_condition
    if 4552 amount_stat strength self
    if 4552 amount_stat strength it
    if 4524 have is self position is front_row
    if 4525 have is self position is back_row
    if stat strength gt stat self
    if 2747 stat strength gt stat self
    if 2748 stat strength gt stat self
    do 2746 own give_keyword self
    do 4524 uses_keyword give_keyword self
    do 4510 uses_keyword can self event=activated
    do 4525 uses_keyword stat_change self strength=1.0
    do 2747 own damage unit enemy chosen board amount=4.0
    do 2748 own keyword_action unit enemy chosen board
    do 4552 uses_keyword damage unit enemy chosen board amount=stat
    do 4552 uses_keyword damage unit enemy chosen board amount=stat
    do 4552 uses_keyword repeat unit enemy chosen board
    do 4524 has_keyword give_keyword self
    do 4510 uses_keyword can self event=activated
    do 4525 has_keyword stat_change self strength=1.0
    do 4504 has_keyword cant self event=activated;turns=1.0
  Reinforced Ballista:
    when 1911 always
    when 4524 played self
    when 4510 played self
    when 4525 played self
    when 1912 always
    when 4533 played card mine type is 18
    when 1913 activated self
    when 1914 always
    when 4511 activated self
    when 4524 played self
    when 4510 played self
    when 4525 played self
    when 4533 played card mine type is 18
    when 4504 played self
    if 4524 have is self position is front_row
    if 4525 have is self position is back_row
    if 4511 amount_listed
    if 4524 have is self position is front_row
    if 4525 have is self position is back_row
    do 1911 own give_keyword self
    do 4524 uses_keyword give_keyword self
    do 4510 uses_keyword can self event=activated
    do 4525 uses_keyword stat_change self strength=1.0
    do 1912 own give_keyword self
    do 4533 uses_keyword countdown_advance self amount=1.0
    do 1913 own damage unit chosen board amount=1.0
    do 1914 own keyword_action amount=1.0
    do 4511 uses_keyword cant event=activated;turns=listed
    do 4524 has_keyword give_keyword self
    do 4510 uses_keyword can self event=activated
    do 4525 has_keyword stat_change self strength=1.0
    do 4533 has_keyword countdown_advance self amount=1.0
    do 4504 has_keyword cant self event=activated;turns=1.0

## C32 vv_3.md 1 (REAL, open, 0 table lines from the same code)
Maxii van Dekkar only reorders cards inside the deck, so it does not move a unit to the front or back row and a help must do the very thing needed (L4, L23).
- W gwent: Maxii van Dekkar -> Heymaey Skald: Maxii van Dekkar moves Heymaey Skald, and Heymaey Skald acts on units back row it | network.py []
- W gwent: Maxii van Dekkar -> Sove: Maxii van Dekkar moves Sove, and Sove acts on units front row it | network.py []
- R gwent: Magic Compass -> Sove: plays it: its effect goes off | network.py []
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

## C33 vv_4.md 2 (REAL, open, 0 table lines from the same code)
Kaer Trolde only creates and plays bronze units while Ragh Nar Roog waits for a gold unit being played, so the kind does not fit (L14).
- W gwent: Kaer Trolde -> Ragh Nar Roog: is played | network.py []
- R gwent: Birna Bran -> Coral: makes you discard cards | network.py []
  Kaer Trolde:
    when 4206 always
    when 4541 round_end
    when 4207 played self
    when 4208 activated self
    when 4532 damaged self
    when 4567 activated
    when 4541 round_end
    when 4504 played self
    if 4532 amount_listed
    if 4567 amount_stat strength self
    if 4567 amount_stat strength it
    do 4206 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 4207 own create unit mine chosen board state is bronze;name_has is 21
    do 4207 own play_card card mine it name_has is 21
    do 4208 own give_keyword unit mine chosen board amount=6.0
    do 4532 uses_keyword negate_damage unit mine chosen board amount=listed
    do 4208 own keyword_action unit mine it
    do 4567 uses_keyword damage unit mine it amount=stat
    do 4567 uses_keyword damage unit mine it amount=stat
    do 4541 has_keyword cant self event=leaves_play
    do 4541 has_keyword remove_keyword self
    do 4504 has_keyword cant self event=activated;turns=1.0
  Ragh Nar Roog:
    when 1827 always
    when 4517 leaves_play self
    when 1828 played unit mine chosen state is gold
    when 1829 played self
    when 4514 turn_start
    when 1830 played unit mine chosen state is gold
    when 1831 played unit mine chosen state is gold
    when 4517 leaves_play self
    if 1830 stage 1.0
    if 1831 stage 2.0
    do 1827 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 1828 own stage_advance self
    do 1829 own give_keyword position enemy all turns=2.0
    do 4514 uses_keyword damage unit random board position is same_row of self amount=3.0;spread=1.0
    do 1830 own damage unit enemy chosen board amount=5.0
    do 1831 own create
    do 1831 own play_card card mine chosen hand card is 756272
    do 4517 has_keyword obliterate self

## C34 vv_4.md 1 (REAL, open, 0 table lines from the same code)
Northern Wind only Banishes units it killed itself (killed by self), so kills by other cards feed nothing (L7).
- W gwent: Eyck of Denesle -> Northern Wind: makes units die: Northern Wind Banishes them | network.py []
- W gwent: Madoc -> Northern Wind: makes units die: Northern Wind Banishes them; also dies by its own effect: Northern Wind Banishes them | network.py []
- W gwent: Villentretenmerth -> Northern Wind: makes units die: Northern Wind Banishes them | network.py []
- W gwent: Dancing Star -> Northern Wind: makes units die: Northern Wind Banishes them | network.py []
- R gwent: Northern Wind -> Saesenthessis: NONE | network.py []
  Eyck of Denesle:
    when 2578 played self
    when 4510 played self
    when 2579 activated self
    when 4504 played self
    if 2578 have is card mine hand type is 38
    do 2578 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2579 own kill unit enemy chosen board strength ge 2451
    do 4504 has_keyword cant self event=activated;turns=1.0
  Northern Wind:
    when 2680 played self
    when 2681 killed
    when 4516 activated
    do 2680 own damage unit chosen board amount=4.0
    do 2681 own keyword_action unit it discard
    do 4516 uses_keyword obliterate unit it discard
  Madoc:
    when 3624 played spell mine type is 27
    when 3625 activated self
    when 4514 turn_start
    when 4504 played self
    do 3624 own summon self
    do 3625 own give_keyword position enemy chosen position is opposite_row of self turns=1.0
    do 4514 uses_keyword damage unit random board position is same_row of self amount=3.0;spread=1.0
    do 3625 own kill self
    do 4504 has_keyword cant self event=activated;turns=1.0
  Villentretenmerth:
    when 1783 always
    when 4507 game_start
    when 1784 always
    when 4508 turn_end
    when 1785 countdown_done self
    when 4507 game_start
    when 4508 turn_end
    if 4507 amount_count card mine type is 38;state is started_in_deck
    if 4507 amount_count card mine type is 38;state is started_in_deck
    do 1783 own give_keyword self
    do 4507 uses_keyword stat_change self strength=count
    do 1784 own give_keyword self amount=3.0
    do 4508 uses_keyword countdown_advance self amount=1.0
    do 1785 own kill unit highest board type not 38
    do 4507 has_keyword stat_change self strength=count
    do 4508 has_keyword countdown_advance self amount=1.0
  Dancing Star:
    when 2676 played self
    when 2677 killed
    do 2676 own damage unit enemy chosen board amount=3.0
    do 2677 own damage unit enemy right_of_self board amount=2.0

## C35 vv_4.md 3 (REAL, open, 0 table lines from the same code)
Mobilization copies a unit onto the board, not into hand, so Queen Adalia (copies created cards in hand) gets nothing from it (L19).
- W gwent: Mobilization -> Queen Adalia: creates cards: Queen Adalia copys them | network.py []
- R gwent: Queen Adalia -> Mobilization: creates cards: Mobilization copys them | network.py []
  Mobilization:
    when 2373 activated self
    when 4504 played self
    do 2373 own copy unit mine chosen board state is bronze;type is 46
    do 2373 own stat_change unit mine it type is 46 strength=3.0
    do 2373 own stat_change unit mine it state is created strength=3.0
    do 4504 has_keyword cant self event=activated;turns=1.0
  Queen Adalia:
    when 2745 played self
    when 4535 damaged self
    if 4535 amount_event_amount
    do 2745 own copy unit mine hand state is bronze;region not Neutral;state is created
    do 2745 own play_card card mine it
    do 2745 own give_keyword unit mine it
    do 4535 uses_keyword negate_damage unit mine it amount=event_amount
    do 4535 uses_keyword remove_keyword unit mine it

## C36 vv_4.md 6 (MISSED REAL, open, 0 table lines from the same code)
Redanian Knight's own text reads its Strength after a stat change (strength ge 8, triggered by stat_changed self), so stat help to a chosen unit is a line (L24, L14 "anything a card waits for").
- W gwent: Shieldwall -> Redanian Knight: NONE | network.py []
- W gwent: Tactical Advantage -> Redanian Knight: NONE | network.py []
- W gwent: Mahakam Ale -> Redanian Knight: NONE | network.py []
- W gwent: Ale of the Ancestors -> Redanian Knight: NONE | network.py []
  Shieldwall:
    when 2452 activated self
    when 4535 damaged self
    when 2453 always
    when 4513 always
    when 4513 always
    when 4504 played self
    if 4535 amount_event_amount
    if 4513 amount_listed
    if 4513 amount_listed
    do 2452 own stat_change unit mine chosen board strength=2.0
    do 2452 own give_keyword unit mine it
    do 4535 uses_keyword negate_damage unit mine it amount=event_amount
    do 4535 uses_keyword remove_keyword unit mine it
    do 2453 own give_keyword self amount=3.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
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
  Tactical Advantage:
    when 4327 activated self
    when 4504 played self
    do 4327 own stat_change unit mine chosen board strength=5.0
    do 4504 has_keyword cant self event=activated;turns=1.0
  Mahakam Ale:
    when 2412 played self
    do 2412 own stat_change unit chosen board strength=5.0
    do 2412 own remove_keyword unit it
  Ale of the Ancestors:
    when 2423 always
    when 4541 round_end
    when 2424 always
    when 4510 played self
    when 2425 activated self
    when 2426 targeted self
    when 2427 targeted self
    when 2428 always
    when 4511 activated self
    when 4541 round_end
    when 4510 played self
    when 4504 played self
    if 4511 amount_listed
    do 2423 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 2424 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2425 own stat_change unit chosen board strength=3.0
    do 2425 own give_ability unit it
    do 2426 gives stat_change self strength=2.0
    do 2425 own give_ability unit it
    do 2427 gives stat_change self strength=2.0
    do 2428 own keyword_action amount=2.0
    do 4511 uses_keyword cant event=activated;turns=listed
    do 4541 has_keyword cant self event=leaves_play
    do 4541 has_keyword remove_keyword self
    do 4510 has_keyword can self event=activated
    do 4504 has_keyword cant self event=activated;turns=1.0

## C37 vv_4.md 3 (REAL, open, 0 table lines from the same code)
a tutor or play from the deck by kind (any unit, a gold card, a type) is a pick that half the deck passes, and Ge'els -> Nithral sets off no Play or Summon effect at all (L1b, L21, L17).
- W gwent: The Last Wish -> Squirrel: plays it: its effect goes off | network.py []
- W gwent: Royal Decree -> Pellar: plays it: its effect goes off | network.py []
- W gwent: Prince Villem -> Endrega Larva: plays it: its effect goes off | network.py []
- W gwent: Ge'els -> Nithral: puts it into play from the deck | network.py []
- W gwent: The Naglfar -> Toad Prince: plays it: its effect goes off | network.py []
- R gwent: Whispering Hillock -> Nightwraith: puts it into play from the deck; also triggers: plays it: its effect goes off | network.py []
- R gwent: Haunt -> Barghest: creates | network.py []
- R gwent: Tir ná Lia -> Red Riders: creates | network.py []
  The Last Wish:
    when 1832 played self
    when 4516 activated
    do 1832 own look card mine deck_top
    do 1832 own play_card card mine chosen deck_top
    do 1832 own keyword_action card mine it deck_top
    do 4516 uses_keyword obliterate card mine it deck_top
  Squirrel:
    when 3310 played self
    when 4516 activated
    do 3310 own keyword_action card enemy chosen discard
    do 4516 uses_keyword obliterate card enemy chosen discard
  Royal Decree:
    when 2350 played self
    do 2350 own play_card unit mine chosen deck
  Pellar:
    when 2689 played self
    when 4536 activated
    do 2689 own keyword_action unit chosen board
    do 4536 uses_keyword remove_keywords unit chosen board
  Prince Villem:
    when 2581 always
    when 4527 always
    when 4528 played self
    when 4569 always
    when 2582 played self
    when 4527 always
    when 4528 played self
    when 4569 always
    do 2581 own give_keyword self
    do 4527 uses_keyword can self event=summoned
    do 4528 uses_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
    do 2582 own play_card card mine random deck state is gold
    do 4527 has_keyword can self event=summoned
    do 4528 has_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
  Endrega Larva:
    when 4847 always
    when 4540 played unit mine strength gt 4192
    when 4848 played self
    when 4540 played unit mine strength gt 4192
    if 4540 amount_listed
    if 4540 amount_listed
    do 4847 own give_keyword self
    do 4540 uses_keyword stat_change self strength=listed
    do 4848 own copy self
    do 4540 has_keyword stat_change self strength=listed
  Ge'els:
    when 1946 played self
    when 1947 played self
    if 1946 keyword_condition not
    if 1947 keyword_condition
    if have not card mine state is started_in_deck;region is Neutral
    if 1946 have not card mine state is started_in_deck;region is Neutral
    if 1947 have not card mine state is started_in_deck;region is Neutral
    do 1946 own play_card spell mine chosen deck type is 23
    do 1947 own play_card card mine chosen deck type is 23
  Nithral:
    when 1981 activated self
    when 1982 activated self
    when 1983 always
    when 4511 activated self
    if 1981 keyword_condition
    if 1981 keyword_condition not
    if 1982 keyword_condition
    if 1982 keyword_condition
    if 4511 amount_listed
    if amount ge stat
    if 1981 have is self position is front_row
    if 1981 amount ge stat
    if 1982 have is self position is front_row
    if 1982 amount ge stat
    do 1981 own damage unit chosen board amount=1.0
    do 1982 own damage unit chosen board amount=2.0
    do 1983 own keyword_action amount=1.0
    do 4511 uses_keyword cant event=activated;turns=listed
  The Naglfar:
    when 2409 played self
    do 2409 own look card mine random deck state is gold
    do 2409 own play_card card mine chosen deck state is gold
    do 2409 own put_on_top card mine chosen deck state is gold
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

## C38 vv_4.md 4 (MISSED REAL, open, 0 table lines from the same code)
Winter Queen needs 2 enemy rows with Frost and Ancient Foglet is fed when Frost is given, so cards that put Frost on enemy rows make the line (L10 enables / feeds).
- W gwent: Ard Gaeth -> Winter Queen: NONE | network.py []
- W gwent: Eredin Bréacc Glas -> Winter Queen: NONE | network.py []
- W gwent: Ard Gaeth -> Ancient Foglet: NONE | network.py []
- W gwent: White Frost -> Ancient Foglet: NONE | network.py []
  Ard Gaeth:
    when 3319 always
    when 4545 round_start
    when 4517 leaves_play self
    when 3320 played self
    when 4520 turn_start
    when 4545 round_start
    when 4517 leaves_play self
    do 3319 own give_keyword self
    do 4545 uses_keyword put_on_top self
    do 4545 uses_keyword give_keyword self
    do 4517 uses_keyword obliterate self
    do 3320 own give_keyword position enemy all turns=3.0
    do 4520 uses_keyword damage unit highest board position is same_row of self amount=2.0
    do 4545 has_keyword put_on_top self discard
    do 4545 has_keyword give_keyword self
    do 4517 uses_keyword obliterate self
  Winter Queen:
    when 3321 turn_end
    when 3322 passed
    if 3321 count ge 2.0 position enemy all keyword is 756162
    if 3322 keyword_condition
    if 3322 have is player mine state is passed
    if 3322 have is player enemy state is passed
    if 3322 amount_stat countdown position enemy all keyword is 756162
    if 3322 amount_product
    if have not card mine state is started_in_deck;region is Neutral
    if 3322 have not card mine state is started_in_deck;region is Neutral
    do 3321 own summon self deck
    do 3322 own stat_change self strength=product
  Eredin Bréacc Glas:
    when 3317 played self
    when 4520 turn_start
    when 3318 played self
    if 3318 keyword_condition
    if amount ge stat
    if 3318 amount ge stat
    do 3317 own give_keyword position enemy chosen turns=2.0
    do 4520 uses_keyword damage unit highest board position is same_row of self amount=2.0
    do 3318 own increase_effect keyword keyword is 756162 amount=1.0
  Ancient Foglet:
    when 1997 always
    when 4519 always
    when 1998 played self
    when 1999 given_keyword position keyword in 756162;keyword in 756163;keyword in 756164;keyword in 756160;keyword in 756156;keyword in 756208;keyword in 756209
    when 4519 always
    if 1998 amount_sum keyword_amount position enemy all board keyword in 756162;keyword in 756163;keyword in 756164;keyword in 756160;keyword in 756156;keyword in 756208;keyword in 756209
    if 1999 amount_stat keyword_amount position it
    do 1997 own give_keyword self
    do 4519 uses_keyword cant self event=given_keyword
    do 1998 own stat_change self strength=sum
    do 1999 own stat_change self strength=stat
    do 4519 has_keyword cant self event=given_keyword
  White Frost:
    when 2293 activated self
    when 4520 turn_start
    when 2294 always
    when 4513 always
    when 2295 played unit mine type is 23
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 2295 have is position keyword is 756162;position is opposite_row of it
    if 4513 amount_listed
    do 2293 own move unit enemy chosen board
    do 2293 own give_keyword position enemy position is same_row of it turns=2.0
    do 4520 uses_keyword damage unit highest board position is same_row of self amount=2.0
    do 2294 own give_keyword self amount=2.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 2295 own stat_change unit mine it type is 23 strength=1.0
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0

## C39 vv_4.md 5 (MISSED REAL, open, 0 table lines from the same code)
Blood Scent gives Bleeding to an enemy unit just as Alp does, and Orianna counts and Dettlaff damages Bleeding enemies, so the same lines belong to it (L10).
- W gwent: Blood Scent -> Orianna: NONE | network.py []
- W gwent: Blood Scent -> Dettlaff van der Eretein: NONE | network.py []
- R gwent: Alp -> Orianna: is a Vampire it asks for; also makes enemy units get Bleeding | network.py []
- R gwent: Alp -> Dettlaff van der Eretein: is a Vampire it asks for; also makes enemy units get Bleeding | network.py []
  Blood Scent:
    when 2639 activated self
    when 4526 turn_end
    when 2640 always
    when 4513 always
    when 2641 always
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 2641 keyword_condition eq 0.0
    if 4513 amount_listed
    if 2641 keyword_condition
    do 2639 own give_keyword unit enemy chosen board amount=3.0
    do 4526 uses_keyword damage unit enemy chosen board amount=1.0
    do 2640 own give_keyword self amount=3.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 2641 own summon
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Orianna:
    when 2699 played self
    when 4526 turn_end
    when 2700 turn_end
    if 2699 amount_count unit mine all board type is 35
    if 2700 keyword_condition
    if 2700 amount_count unit enemy all board keyword is 756169
    if have is self position is back_row
    if 2700 have is self position is back_row
    do 2699 own give_keyword unit enemy chosen board amount=count
    do 4526 uses_keyword damage unit enemy chosen board amount=1.0
    do 2700 own stat_change self strength=count
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

## C40 vv_4.md 1 (REAL, open, 0 table lines from the same code)
Naglfar Crew and Red Riders: Charge only put Frost on an enemy row (the damage is the keyword's own, on enemies), so they do not kill my Lara Dorren or Nightwraith for a death effect (L1, L9, L16).
- W gwent: Naglfar Crew -> Lara Dorren: kills it for its death effect | network.py []
- W gwent: Naglfar Crew -> Nightwraith: kills it for its death effect | network.py []
- W gwent: Red Riders: Charge -> Lara Dorren: kills it for its death effect | network.py []
- W gwent: Red Riders: Charge -> Nightwraith: kills it for its death effect | network.py []
- R gwent: Ge'els -> Lara Dorren: puts it into play from the deck; also triggers: plays it: its effect goes off | network.py [] | cases n569 line
  Naglfar Crew:
    when 3329 played self
    when 4520 turn_start
    when 3330 turn_end
    if 3330 have position enemy all position is opposite_row of self;keyword is 756162
    do 3329 own give_keyword position enemy chosen turns=2.0
    do 4520 uses_keyword damage unit highest board position is same_row of self amount=2.0
    do 3330 own stat_change self strength=1.0
  Lara Dorren:
    when 4286 always
    when 4527 always
    when 4528 played self
    when 4569 always
    when 4287 played self
    when 4288 dies self
    when 4289 played unit enemy state is gold;type is 23
    when 4517 leaves_play self
    when 4527 always
    when 4528 played self
    when 4569 always
    if 4287 amount_sum keyword_amount position enemy all keyword is 756162
    if 4289 have self discard
    do 4286 own give_keyword self
    do 4527 uses_keyword can self event=summoned
    do 4528 uses_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
    do 4287 own damage self amount=sum
    do 4288 own stat_change unit enemy all board strength=2.0
    do 4289 own play_card self discard
    do 4289 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4527 has_keyword can self event=summoned
    do 4528 has_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
  Nightwraith:
    when 3221 played self
    when 3222 dies self
    do 3221 own summon amount=2.0
    do 3222 own summon amount=2.0
  Red Riders: Charge:
    when 4431 played self
    when 4520 turn_start
    do 4431 own give_keyword position enemy chosen turns=2.0
    do 4520 uses_keyword damage unit highest board position is same_row of self amount=2.0
    do 4431 own play_card unit mine chosen board state is bronze;type is 23

## C41 vv_4.md 2 (REAL, open, 0 table lines from the same code)
Enslave and Amnesty only Seize a unit (move it) and give no Spying, so they do not feed cards that wait for Spying (L10, L20).
- W gwent: Enslave -> Impera Enforcers: makes enemy units get Spying | network.py []
- W gwent: Enslave -> Coup de Grâce: makes units get Spying | network.py []
- W gwent: Enslave -> Emhyr var Emreis: makes enemy units get Spying | network.py []
- W gwent: Amnesty -> Impera Enforcers: makes enemy units get Spying | network.py []
- R gwent: Treason -> Impera Enforcers: makes enemy units get Spying | network.py []
- R gwent: Fercart -> Impera Enforcers: makes enemy units get Spying | network.py [] | cases n571 line
  Enslave:
    when 2609 activated self
    when 4539 activated
    when 4569 always
    when 4504 played self
    do 2609 own keyword_action unit enemy chosen board strength le 2472
    do 4539 uses_keyword move unit enemy chosen board strength le 2472
    do 4539 uses_keyword give_keyword unit enemy chosen board strength le 2472
    do 4569 uses_keyword can unit enemy chosen board strength le 2472 event=summoned
    do 4539 uses_keyword remove_keyword unit enemy chosen board strength le 2472
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
  Amnesty:
    when 3435 played self
    when 4539 activated
    when 4569 always
    when 3436 played self
    when 3437 played self
    if 3436 keyword_condition
    if 3437 keyword_condition
    if have not card mine state is started_in_deck;region is Neutral
    if it_matches keyword is 9000001
    if 3436 it_matches keyword is 9000001
    if 3437 have not card mine state is started_in_deck;region is Neutral
    do 3435 own keyword_action unit enemy chosen board strength le 3227
    do 4539 uses_keyword move unit enemy chosen board strength le 3227
    do 4539 uses_keyword give_keyword unit enemy chosen board strength le 3227
    do 4569 uses_keyword can unit enemy chosen board strength le 3227 event=summoned
    do 4539 uses_keyword remove_keyword unit enemy chosen board strength le 3227
    do 3436 own stat_change it strength=2.0
    do 3437 own stat_change it strength=2.0

## C42 vv_4.md 4 (REAL, open, 0 table lines from the same code)
Slave Driver damages and copies any bronze unit of mine, a filter most cards pass, and only its own copy is "created", so card creators feed nothing it waits for (L14, L21).
- W gwent: Artorius Vigo -> Slave Driver: creates cards: Slave Driver damages them | network.py []
- W gwent: Imperial Diplomacy -> Slave Driver: creates cards: Slave Driver damages them | network.py []
- W gwent: Runemage -> Slave Driver: creates cards: Slave Driver damages them | network.py []
- W gwent: Coup de Grâce -> Slave Driver: creates cards: Slave Driver damages them | network.py []
- R gwent: Artorius Vigo -> Artaud Terranova: creates cards: Artaud Terranova copys them | network.py []
  Artorius Vigo:
    when 2727 always
    when 4557 played card mine state not started_in_deck
    when 2728 played self
    when 4557 played card mine state not started_in_deck
    if 4557 amount_listed
    if 4557 amount_listed
    do 2727 own give_keyword self
    do 4557 uses_keyword stat_change self strength=listed
    do 2728 own create unit mine random state is started_in_deck;state is bronze
    do 2728 own stat_set card mine it strength=1.0
    do 2728 own play_card card mine it
    do 4557 has_keyword stat_change self strength=listed
  Slave Driver:
    when 2468 played self
    do 2468 own damage unit mine chosen board state is bronze amount=1.0
    do 2468 own copy unit mine it
    do 2468 own stat_set unit mine it state is created strength=1.0
    do 2468 own play_card unit mine it state is created;type is 46
  Imperial Diplomacy:
    when 2234 played self
    do 2234 own create card mine random state is opponent_faction;state is bronze
    do 2234 own play_card card mine it
  Runemage:
    when 3979 played self
    do 3979 own increase_effect effect mine keyword is 756201 options=5.0
    do 3979 own create card mine name_has is 19
    do 3979 own play_card card mine it name_has is 19
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

## C43 vv_4.md 5 (REAL, open, 0 table lines from the same code)
Artorius Vigo and Artaud Terranova play only units, Emhyr var Emreis plays only bronze units of other types, and Fercart and Hefty Helge wait for a played spell or a type 21 card, so no match (L7, L17).
- W gwent: Artorius Vigo -> Fercart: is played | network.py []
- W gwent: Artaud Terranova -> Fercart: is played; also plays it: its effect goes off | network.py []
- W gwent: Emhyr var Emreis -> Hefty Helge: is played | network.py []
- R gwent: Assassination -> Fercart: is a spell whose playing sets off its effect | network.py [1823]
  Artorius Vigo:
    when 2727 always
    when 4557 played card mine state not started_in_deck
    when 2728 played self
    when 4557 played card mine state not started_in_deck
    if 4557 amount_listed
    if 4557 amount_listed
    do 2727 own give_keyword self
    do 4557 uses_keyword stat_change self strength=listed
    do 2728 own create unit mine random state is started_in_deck;state is bronze
    do 2728 own stat_set card mine it strength=1.0
    do 2728 own play_card card mine it
    do 4557 has_keyword stat_change self strength=listed
  Fercart:
    when 3720 played self
    when 3721 played spell mine
    when 4569 always
    do 3720 own play_card card mine chosen hand category is spell
    do 3720 own draw card mine deck_top amount=1.0
    do 3721 own give_keyword unit enemy random board keyword not 9000001
    do 4569 uses_keyword can unit enemy random board keyword not 9000001 event=summoned
  Artaud Terranova:
    when 3716 always
    when 4557 played card mine state not started_in_deck
    when 3717 played self
    when 4557 played card mine state not started_in_deck
    if 4557 amount_listed
    if 3717 event_count ge 1.0
    if 4557 amount_listed
    do 3716 own give_keyword self
    do 4557 uses_keyword stat_change self strength=listed
    do 3717 own copy unit chosen board keyword not 756170;card not 757265;state is created
    do 3717 own play_card card mine chosen hand state is created
    do 4557 has_keyword stat_change self strength=listed
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
  Hefty Helge:
    when 2272 always
    when 4535 damaged self
    when 2273 activated self
    when 2274 always
    when 4513 always
    when 2275 played card mine type is 21
    when 4513 always
    when 4535 damaged self
    when 4513 always
    when 4504 played self
    if 4535 amount_event_amount
    if 4513 amount_listed
    if 4513 amount_listed
    if 4535 amount_event_amount
    if 4513 amount_listed
    do 2272 own give_keyword self
    do 4535 uses_keyword negate_damage self amount=event_amount
    do 4535 uses_keyword remove_keyword self
    do 2273 own damage unit chosen board amount=2.0
    do 2274 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 2275 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4535 has_keyword negate_damage self amount=event_amount
    do 4535 has_keyword remove_keyword self
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0

## C44 vv_5.md 7 (MISSED REAL, open, 0 table lines from the same code)
Naglfar Crew grows when the opposite enemy row has Frost, and both Red Riders put Frost on enemy rows (L24, L10).
- W gwent: Red Riders: Spread -> Naglfar Crew: NONE | network.py []
- W gwent: Red Riders: Charge -> Naglfar Crew: NONE | network.py []
  Red Riders: Spread:
    when 4403 played self
    when 4520 turn_start
    when 4840 played self
    when 4520 turn_start
    do 4403 own give_keyword position enemy all turns=2.0
    do 4520 uses_keyword damage unit highest board position is same_row of self amount=2.0
    do 4840 own give_keyword position enemy all turns=2.0
    do 4520 uses_keyword damage unit highest board position is same_row of self amount=2.0
  Naglfar Crew:
    when 3329 played self
    when 4520 turn_start
    when 3330 turn_end
    if 3330 have position enemy all position is opposite_row of self;keyword is 756162
    do 3329 own give_keyword position enemy chosen turns=2.0
    do 4520 uses_keyword damage unit highest board position is same_row of self amount=2.0
    do 3330 own stat_change self strength=1.0
  Red Riders: Charge:
    when 4431 played self
    when 4520 turn_start
    do 4431 own give_keyword position enemy chosen turns=2.0
    do 4520 uses_keyword damage unit highest board position is same_row of self amount=2.0
    do 4431 own play_card unit mine chosen board state is bronze;type is 23

## C45 vv_5.md 1 (REAL, open, 0 table lines from the same code)
Cursed Scroll, Fisher King and Doadrick Leumaerts move cards between hand and deck, not units on the board, so the "moves it" lines to row and neighbour cards are wrong (L1, L23).
- W gwent: Cursed Scroll -> Cow Carcass: Cursed Scroll moves Cow Carcass and your units, and Cow Carcass acts on units next to it | network.py []
- W gwent: Cursed Scroll -> Doadrick Leumaerts: Cursed Scroll moves Doadrick Leumaerts, and Doadrick Leumaerts acts on units back row it | network.py []
- W gwent: Fisher King -> Vilgefortz: Fisher King moves Vilgefortz, and Vilgefortz acts on units back row it or front row it | network.py []
- W gwent: Doadrick Leumaerts -> Mage Assassin: moves it for its effect | network.py []
- R gwent: Blightmaker -> Albrich: moves it for its effect | network.py []
- R gwent: Fisher King -> Albrich: moves it for its effect | network.py []
  Cursed Scroll:
    when 3156 activated self
    when 4504 played self
    do 3156 own draw card mine chosen deck amount=1.0
    do 3156 own move card mine chosen hand
    do 4504 has_keyword cant self event=activated;turns=1.0
  Cow Carcass:
    when 4312 always
    when 4517 leaves_play self
    when 4313 always
    when 4527 always
    when 4528 played self
    when 4569 always
    when 4314 turn_end
    when 4549 given_keyword self keyword is 756202
    when 4517 leaves_play self
    when 4527 always
    when 4528 played self
    when 4569 always
    if 4549 event_count ge 2.0
    do 4312 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4313 own give_keyword self
    do 4527 uses_keyword can self event=summoned
    do 4528 uses_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
    do 4314 own give_keyword unit mine all board position is sides of self
    do 4549 uses_keyword kill unit mine all board position is sides of self
    do 4314 own kill self
    do 4517 has_keyword obliterate self
    do 4527 has_keyword can self event=summoned
    do 4528 has_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
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
  Mage Assassin:
    when 3670 played self
    when 3671 moves self
    if 3671 my_turn
    do 3670 own damage unit enemy chosen board amount=2.0
    do 3671 own summon self
    do 3671 own damage unit enemy random board amount=2.0

## C46 vv_5.md 2 (REAL, open, 0 table lines from the same code)
Lydia van Bredevoort only creates and plays bronze spells, so a line "plays it" to units is wrong (L14, L4).
- W gwent: Lydia van Bredevoort -> Ciri: Nova: plays it: its effect goes off | network.py []
- W gwent: Lydia van Bredevoort -> Imperial Golem: plays it: its effect goes off | network.py []
- W gwent: Lydia van Bredevoort -> Strays of Spalla: plays it: its effect goes off | network.py []
- W gwent: Lydia van Bredevoort -> Xarthisius: plays it: its effect goes off | network.py []
- R gwent: Golden Nekker -> Strays of Spalla: plays it: its effect goes off | network.py []
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
  Ciri: Nova:
    when 2490 played self
    when 4541 round_end
    when 4535 damaged self
    when 4519 always
    if 2490 have not card mine deck state is started_in_deck;cost ge 2384;card not 756651;card not 757376
    if 4535 amount_event_amount
    do 2490 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 2490 own give_keyword self
    do 4535 uses_keyword negate_damage self amount=event_amount
    do 4535 uses_keyword remove_keyword self
    do 2490 own give_keyword self
    do 4519 uses_keyword cant self event=given_keyword
  Imperial Golem:
    when 2021 played self
    when 4506 activated
    if 2021 amount_stat strength unit enemy it deck
    do 2021 own keyword_action unit enemy top deck
    do 4506 uses_keyword reveal unit enemy top deck
    do 2021 own damage self amount=stat
    do 2021 own shuffle_into_deck unit enemy it deck
  Strays of Spalla:
    when 2613 played self
    when 2614 played self
    if 2613 keyword_condition not
    if 2614 keyword_condition
    if have is unit mine board state is copy_of_it
    if 2613 have is unit mine board state is copy_of_it
    if 2614 have is unit mine board state is copy_of_it
    do 2613 own shuffle_into_deck card mine chosen hand state is gold
    do 2613 own draw card mine deck state is bronze amount=1.0
    do 2613 own stat_change self strength=4.0
    do 2614 own shuffle_into_deck card mine chosen hand state is gold
    do 2614 own stat_change self strength=4.0
  Xarthisius:
    when 2183 played self
    when 4506 activated
    if 2183 amount_stat strength unit mine it deck
    do 2183 own keyword_action card mine random deck
    do 4506 uses_keyword reveal card mine random deck
    do 2183 own stat_change self strength=stat
    do 2183 own shuffle_into_deck unit mine it deck
    do 2183 own play_card card mine it deck category in spell;category in landmark

## C47 vv_5.md 5 (REAL, open, 0 table lines from the same code)
Beauclair sets the stats of one of my own units, and an effect on my side feeds no need about enemy units (L9); Milton de Peyrac-Peyran does not wait for a stat change at all.
- W gwent: Beauclair -> Milton de Peyrac-Peyran: changes enemy units' stats | network.py []
- W gwent: Beauclair -> Toussaintois Hospitality: changes enemy units' stats | network.py []
- R gwent: Sangreal -> Toussaintois Hospitality: changes enemy units' stats | network.py []
- R gwent: Ard Feainn Tortoise -> Toussaintois Hospitality: changes enemy units' stats | network.py []
  Beauclair:
    when 4015 always
    when 4541 round_end
    when 4016 played self
    when 4017 activated self
    when 4568 activated
    when 4541 round_end
    when 4504 played self
    if 4016 amount_stat strength unit enemy highest board
    if 4568 amount_stat base_power it
    do 4015 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 4016 own stat_set unit mine chosen board strength=stat
    do 4017 own keyword_action unit chosen board
    do 4568 uses_keyword stat_set unit chosen board strength=stat
    do 4541 has_keyword cant self event=leaves_play
    do 4541 has_keyword remove_keyword self
    do 4504 has_keyword cant self event=activated;turns=1.0
  Milton de Peyrac-Peyran:
    when 2725 played self
    when 2726 activated self
    when 4665 played self
    when 4666 activated self
    when 4504 played self
    if 2726 amount_event_amount
    if 4666 amount_event_amount
    do 2725 own stat_change unit enemy chosen board strength=3.0
    do 2725 own stat_change self strength=3.0
    do 2726 own stat_change self strength=event_amount
    do 4665 own stat_change unit enemy chosen board strength=3.0
    do 4665 own stat_change self strength=3.0
    do 4666 own stat_change self strength=event_amount
    do 4504 has_keyword cant self event=activated;turns=1.0
  Toussaintois Hospitality:
    when 2442 activated self
    when 2443 stat_changed unit enemy
    when 4504 played self
    if 2443 my_turn
    do 2442 own create
    do 2442 own play_card card mine it card is 757379
    do 2443 own stat_change unit mine random board strength=1.0
    do 4504 has_keyword cant self event=activated;turns=1.0

## C48 vv_5.md 6 (MISSED REAL, open, 0 table lines from the same code)
Cahir Dyffryn grows when an enemy unit's stats change on my turn, so the cards that change enemy stats help it level up like they help Toussaintois Hospitality (L24, L10).
- W gwent: Milton de Peyrac-Peyran -> Cahir Dyffryn: NONE | network.py []
- W gwent: Sangreal -> Cahir Dyffryn: NONE | network.py []
- W gwent: Ard Feainn Tortoise -> Cahir Dyffryn: NONE | network.py []
  Milton de Peyrac-Peyran:
    when 2725 played self
    when 2726 activated self
    when 4665 played self
    when 4666 activated self
    when 4504 played self
    if 2726 amount_event_amount
    if 4666 amount_event_amount
    do 2725 own stat_change unit enemy chosen board strength=3.0
    do 2725 own stat_change self strength=3.0
    do 2726 own stat_change self strength=event_amount
    do 4665 own stat_change unit enemy chosen board strength=3.0
    do 4665 own stat_change self strength=3.0
    do 4666 own stat_change self strength=event_amount
    do 4504 has_keyword cant self event=activated;turns=1.0
  Cahir Dyffryn:
    when 2173 stat_changed unit enemy
    if 2173 keyword_condition
    if 2173 my_turn
    if 2173 amount_event_amount
    if have is self position is front_row
    if 2173 have is self position is front_row
    do 2173 own stat_change self strength=event_amount
  Sangreal:
    when 2671 played self
    when 4536 activated
    when 2672 passed
    if 2672 have player mine state is passed
    if 2672 have player enemy state is passed
    do 2671 own keyword_action unit chosen board
    do 4536 uses_keyword remove_keywords unit chosen board
    do 2671 own stat_change unit it strength=12.0
    do 2671 own give_ability unit it
    do 2672 gives damage self amount=12.0
  Ard Feainn Tortoise:
    when 3090 keyword_removed self keyword is 756174
    do 3090 own stat_change unit enemy highest board strength=3.0

## C49 vv_5.md 2 (REAL, open, 0 table lines from the same code)
A plain damage hit on one chosen enemy is no kill effect, so it feeds no "when an enemy Bounty unit dies"; Blood Money gives no Bounty for The Brute either (L11).
- W gwent: Tunnel Drill -> Ignatius Hale: makes enemy units die | network.py []
- W gwent: Blood Money -> Ignatius Hale: makes enemy units die | network.py []
- W gwent: Confession Extractor -> Ignatius Hale: makes enemy units die | network.py []
- W gwent: Blood Money -> The Brute: makes enemy units die | network.py []
- R gwent: Graden -> Ignatius Hale: makes enemy units die | network.py []
- R gwent: Moreelse -> Blood Money: makes enemy units die | network.py []
- R gwent: Moreelse -> The Brute: makes enemy units die | network.py []
  Tunnel Drill:
    when 2982 played self
    when 2983 activated self
    when 2984 always
    when 4511 activated self
    when 2985 played card mine type is 24
    if 4511 amount_listed
    do 2982 own mana_gain secondary_resource mine amount=2.0
    do 2983 own spend_mana secondary_resource mine amount=2.0
    do 2983 own damage unit enemy chosen board amount=3.0
    do 2984 own keyword_action amount=1.0
    do 4511 uses_keyword cant event=activated;turns=listed
    do 2985 own countdown_advance self amount=1.0
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
  Blood Money:
    when 2838 activated self
    when 2839 dies unit enemy keyword is 756214
    when 2840 exhausted self
    when 4504 played self
    if 2838 amount_excess it
    do 2838 own damage unit enemy chosen board amount=6.0
    do 2838 own mana_gain secondary_resource mine amount=excess
    do 2839 own increase_effect self amount=1.0
    do 2840 own refresh self
    do 2840 own stat_set self amount=1.0
    do 4504 has_keyword cant self event=activated;turns=1.0
  Confession Extractor:
    when 3768 played self
    when 3769 given_keyword unit enemy keyword is 756214
    when 3770 always
    if 3769 have self discard
    do 3768 own mana_gain secondary_resource mine amount=4.0
    do 3769 own damage unit enemy it amount=1.0
    do 3770 own give_keyword self amount=3.0
  The Brute:
    when 3819 played self
    when 3820 played self
    when 3821 given_keyword unit enemy keyword is 756214
    if 3820 amount_stat base_power unit enemy highest discard keyword is 756214
    do 3819 own mana_gain secondary_resource mine amount=0.0
    do 3820 own stat_change self strength=stat
    do 3821 own increase_effect self amount=1.0

## C50 vv_5.md 3 (REAL, open, 0 table lines from the same code)
Hysteria picks an enemy without Bounty and gives it Bounty itself, so more Bounty from other cards needs nothing and only removes its targets (L10, L5).
- W gwent: Kurt -> Hysteria: makes enemy units get Bounty | network.py []
- W gwent: Witch Hunter -> Hysteria: makes enemy units get Bounty | network.py []
- W gwent: The Witchfinder -> Hysteria: makes enemy units get Bounty | network.py []
- W gwent: Caleb Menge -> Hysteria: makes enemy units get Bounty | network.py []
- R gwent: Hysteria -> The Brute: makes enemy units get Bounty; also makes enemy units die | network.py []
- R gwent: Hysteria -> Confession Extractor: makes enemy units get Bounty | network.py []
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
  Hysteria:
    when 3710 played self
    when 4561 dies self
    when 4562 obliterated self
    if 4561 amount_stat base_power self
    if 4562 amount_stat base_power self
    do 3710 own give_keyword unit enemy chosen board keyword not 756214
    do 4561 uses_keyword mana_gain secondary_resource enemy amount=stat
    do 4562 uses_keyword mana_gain secondary_resource enemy amount=stat
    do 3710 own damage unit enemy it amount=3.0
    do 3710 own damage unit enemy it board keyword is 756214 amount=6.0
  Witch Hunter:
    when 2873 played self
    when 4561 dies self
    when 4562 obliterated self
    if 4561 amount_stat base_power self
    if 4562 amount_stat base_power self
    do 2873 own give_keyword unit enemy chosen board
    do 4561 uses_keyword mana_gain secondary_resource enemy amount=stat
    do 4562 uses_keyword mana_gain secondary_resource enemy amount=stat
  The Witchfinder:
    when 3705 played self
    when 3706 turn_end
    when 4561 dies self
    when 4562 obliterated self
    when 4762 played self
    when 4763 turn_end
    when 4561 dies self
    when 4562 obliterated self
    if 3706 have not unit enemy board keyword is 756214
    if 4561 amount_stat base_power self
    if 4562 amount_stat base_power self
    if 4763 have not unit enemy board keyword is 756214
    if 4561 amount_stat base_power self
    if 4562 amount_stat base_power self
    do 3705 own summon amount=3.0
    do 3706 own give_keyword unit enemy highest board
    do 4561 uses_keyword mana_gain secondary_resource enemy amount=stat
    do 4562 uses_keyword mana_gain secondary_resource enemy amount=stat
    do 4762 own summon unit mine amount=3.0
    do 4763 own give_keyword unit enemy highest board
    do 4561 uses_keyword mana_gain secondary_resource enemy amount=stat
    do 4562 uses_keyword mana_gain secondary_resource enemy amount=stat
  Caleb Menge:
    when 2827 played self
    when 2828 activated self
    when 4561 dies self
    when 4562 obliterated self
    when 2829 always
    when 4511 activated self
    if 2828 keyword_condition
    if 4561 amount_stat base_power self
    if 4562 amount_stat base_power self
    if 4511 amount_listed
    if 2828 have is self position is front_row
    do 2827 own mana_gain secondary_resource mine amount=3.0
    do 2828 own spend_mana secondary_resource mine amount=3.0
    do 2828 own give_keyword unit enemy chosen board
    do 4561 uses_keyword mana_gain secondary_resource enemy amount=stat
    do 4562 uses_keyword mana_gain secondary_resource enemy amount=stat
    do 2829 own keyword_action amount=1.0
    do 4511 uses_keyword cant event=activated;turns=listed

## C51 vv_5.md 4 (REAL, open, 0 table lines from the same code)
Eventide Plunder creates a random cost-4 Fee unit in hand, which is not a Tidecloaks on the board and may be any kind, so it is not the kind Collusion or Sigi Reuven ask for (L19, L20).
- W gwent: Eventide Plunder -> Collusion: is a Tidecloaks it asks for | network.py []
- W gwent: Eventide Plunder -> Sigi Reuven: Mastermind: is a Tidecloaks it asks for | network.py []
- R gwent: Flaming Rose Footman -> Collusion: is a Firesworn it asks for | network.py []
- R gwent: Fisstech Trafficker -> Collusion: is a Blindeyes it asks for | network.py []
  Eventide Plunder:
    when 2903 played self
    do 2903 own create unit mine random cost eq 2758;keyword is 756213
  Collusion:
    when 3260 played self
    when 3261 played self
    when 3262 played self
    when 3263 played self
    when 3264 played self
    if 3260 have is unit mine all board type is 30
    if 3261 have is unit mine all board type is 33
    if 3262 have is unit mine all board type is 32
    if 3263 have is unit mine all board type is 20
    if 3264 have is unit mine all board type is 31
    do 3260 own increase_effect self amount=1.0
    do 3261 own stat_change unit mine lowest board strength=4.0
    do 3262 own damage unit enemy highest board amount=4.0
    do 3263 own summon amount=2.0
    do 3264 own mana_gain secondary_resource mine amount=4.0
  Sigi Reuven: Mastermind:
    when 4056 played self
    when 4057 played self
    when 4793 played self
    when 4794 played self
    if 4057 amount_sum
    if 4057 amount_product
    if 4057 amount_distinct type unit mine all board type in 30;type in 32;type in 33;type in 31;type in 20
    if 4057 amount_minus
    if 4794 amount_sum
    if 4794 amount_product
    if 4794 amount_distinct type unit mine all board type in 30;type in 32;type in 33;type in 31;type in 20
    if 4794 amount_minus
    do 4056 own look card mine deck card is 757070
    do 4056 own look card mine random deck type in 30;type in 32;type in 33;type in 31;type in 20
    do 4056 own play_card card mine chosen deck
    do 4057 own spend_mana secondary_resource mine amount=sum
    do 4057 own look card mine deck card is 757070
    do 4057 own look card mine random deck type in 30;type in 32;type in 33;type in 31;type in 20
    do 4057 own play_card card mine chosen deck
    do 4793 own look card mine deck card is 757070
    do 4793 own look card mine random deck type in 30;type in 32;type in 33;type in 31;type in 20
    do 4793 own play_card card mine chosen deck
    do 4794 own spend_mana secondary_resource mine amount=sum
    do 4794 own look card mine deck card is 757070
    do 4794 own look card mine random deck type in 30;type in 32;type in 33;type in 31;type in 20
    do 4794 own play_card card mine chosen deck

## C52 vv_5.md 1 (REAL, open, 0 table lines from the same code)
Eavesdrop moves a card from hand to the bottom of the deck, not a unit on the board, so the "moves it" lines are wrong (the Bones line to Oxenfurt Guard and Cleaver stays) (L1, L23).
- W gwent: Eavesdrop -> Kurt: Eavesdrop moves Kurt, and Kurt acts on units back row it or front row it | network.py []
- W gwent: Eavesdrop -> Ferko the Sculptor: Eavesdrop moves Ferko the Sculptor, and Ferko the Sculptor acts on units front row it | network.py []
- W gwent: Eavesdrop -> Oxenfurt Guard: lets you gain the second resource (Bones); also Eavesdrop moves Oxenfurt Guard and your units, and Oxenfurt Guard acts on units next to it | network.py []
- W gwent: Eavesdrop -> Cleaver: lets you gain the second resource (Bones); also Eavesdrop moves Cleaver and units, and Cleaver acts on units next to it | network.py []
- R gwent: Eavesdrop -> Casino Bouncers: lets you gain the second resource (Bones) | network.py []
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
  Ferko the Sculptor:
    when 2991 played self
    if 2991 keyword_condition
    if 2991 have is self position is front_row
    do 2991 own play_card card mine chosen deck type is 24
  Oxenfurt Guard:
    when 4184 activated self
    when 4185 activated self
    if 4184 count ge 3.0 secondary_resource mine
    if 4185 count eq 2.0 secondary_resource mine
    do 4184 own spend_mana secondary_resource mine amount=2.0
    do 4184 own stat_change unit mine all board position is sides of self strength=1.0
    do 4185 own spend_mana secondary_resource mine amount=2.0
    do 4185 own stat_change unit mine all board position is sides of self strength=2.0
  Cleaver:
    when 3658 always
    when 4563 played card mine type is 24
    when 3659 played self
    when 3660 always
    when 4563 played card mine type is 24
    when 3661 activated self
    when 4563 played card mine type is 24
    if 4563 amount_listed
    if 3660 amount_count unit all board position is sides of self;type is 33
    if 4563 amount_listed
    if 4563 amount_listed
    do 3658 own give_keyword self
    do 4563 uses_keyword stat_change self strength=listed
    do 3659 own create
    do 3659 own play_card card mine chosen hand card is 756918
    do 3660 own give_keyword self amount=count
    do 4563 uses_keyword stat_change self strength=listed
    do 3661 own spend_mana secondary_resource mine amount=4.0
    do 3661 own summon
    do 4563 has_keyword stat_change self strength=listed

## C53 vv_5.md 2 (PARTLY, open, 0 table lines from the same code)
Eveline Gallo and Open, Sesame! want NO Bones, so cards that gain Bones are the opposite (L21), but Casimir Bassi spends all Bones, which empties them for Open, Sesame!.
- W gwent: Tiger's Eye -> Eveline Gallo: lets you gain the second resource (Bones) | network.py []
- W gwent: Vivaldi Bank -> Open, Sesame!: lets you gain the second resource (Bones) | network.py []
- W gwent: Lined Pockets -> Open, Sesame!: lets you gain the second resource (Bones) | network.py []
- R gwent: Casimir Bassi -> Open, Sesame!: lets you gain the second resource (Bones) | network.py []
- R gwent: Tiger's Eye -> Casino Bouncers: lets you gain the second resource (Bones) | network.py []
  Tiger's Eye:
    when 3259 activated self
    when 4710 activated self
    when 4504 played self
    do 3259 own mana_gain secondary_resource mine amount=5.0
    do 4710 own mana_gain secondary_resource mine amount=5.0
    do 4504 has_keyword cant self event=activated;turns=1.0
  Eveline Gallo:
    when 4179 turn_end
    if 4179 have not secondary_resource mine
    do 4179 own mana_gain secondary_resource mine amount=3.0
  Vivaldi Bank:
    when 2835 played self
    if 2835 amount_sum
    if 2835 amount_count secondary_resource mine
    if 2835 amount_stat distance_from_top card mine chosen deck_top
    do 2835 own mana_gain secondary_resource mine amount=4.0
    do 2835 own look card mine deck_top
    do 2835 own choose_one
    do 2835 own play_card card mine top deck
    do 2835 own spend_mana secondary_resource mine amount=stat
    do 2835 own play_card card mine chosen deck_top
    do 2835 own shuffle_into_deck card mine all deck_top
  Open, Sesame!:
    when 4180 played self
    when 4181 always
    when 4182 mana_spent
    when 4183 countdown_done self
    if 4182 have is self discard
    if 4182 have not secondary_resource mine
    if 4183 have is self discard
    do 4180 own mana_gain secondary_resource mine amount=5.0
    do 4181 own give_keyword self amount=6.0
    do 4182 own countdown_advance self amount=1.0
    do 4183 own mana_gain secondary_resource mine amount=4.0
  Lined Pockets:
    when 1869 activated self
    when 1870 always
    when 4513 always
    when 1871 played card mine type is 24
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 4513 amount_listed
    do 1869 own mana_gain secondary_resource mine amount=1.0
    do 1870 own give_keyword self amount=6.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 1871 own mana_gain secondary_resource mine amount=1.0
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0

## C54 vv_5.md 1 (REAL, open, 0 table lines from the same code)
Draig Bon-Dhu and Dimun Pirate move cards between deck and discard, not units on the board, so "moves it" lines to position-dependent cards are wrong (L23, L16); the Pirate line to Tidecloak Hideaway stays.
- W gwent: Draig Bon-Dhu -> Tuirseach Axeman: Draig Bon-Dhu moves Tuirseach Axeman, and Tuirseach Axeman acts on units front row it | network.py []
- W gwent: Draig Bon-Dhu -> Vabjorn: Draig Bon-Dhu moves Vabjorn, and Vabjorn acts on units front row it | network.py []
- W gwent: Dimun Pirate -> Vabjorn: Dimun Pirate moves Vabjorn, and Vabjorn acts on units front row it | network.py []
- W gwent: Dimun Pirate -> Tidecloak Hideaway: is a Pirate it asks for; also Dimun Pirate moves Tidecloak Hideaway, and Tidecloak Hideaway acts on units back row it | network.py []
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
  Vabjorn:
    when 2255 played self
    if 2255 keyword_condition
    if 2255 have is self position is front_row
    do 2255 own play_card card mine chosen deck type is 29
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

## C55 vv_6.md 2 (REAL, open, 0 table lines from the same code)
the made card gets a line back to its maker, but the maker only makes it and waits for nothing, so the line is wrong (L3, L6).
- W gwent: Deafening Siren -> Patricidal Fury: is the Deafening Siren it names | network.py []
- W gwent: Skellige Wolves -> Feral Bond: is the Skellige Wolves it names | network.py []
- R gwent: Bjorn's Drakkar -> Endless Voyage: is the Bjorn's Drakkar it names | network.py []
  Deafening Siren:
    when 4328 always
    when 4517 leaves_play self
    when 4517 leaves_play self
    do 4328 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4517 has_keyword obliterate self
  Patricidal Fury:
    when 2610 activated self
    when 2611 always
    when 4513 always
    when 2612 always
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 2612 keyword_condition eq 0.0
    if 4513 amount_listed
    if 2612 keyword_condition
    do 2610 own summon
    do 2610 own damage unit mine it card is 813603 amount=1.0
    do 2611 own give_keyword self amount=3.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 2612 own create
    do 2612 own play_card card mine it card is 813604
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Skellige Wolves:
    when 4462 always
    when 4517 leaves_play self
    when 4463 always
    when 4537 always
    when 4464 dies self
    when 4517 leaves_play self
    when 4537 always
    do 4462 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4463 own give_keyword self
    do 4537 uses_keyword cant player all event=targeted
    do 4464 own copy self state is created
    do 4517 has_keyword obliterate self
    do 4537 has_keyword cant player all event=targeted
  Feral Bond:
    when 4027 played self
    when 4028 played self
    when 4029 played self
    if 4028 keyword_condition not 3.0
    if 4029 keyword_condition 3.0
    if count ge listed unit enemy board state is damaged
    if 4028 count ge listed unit enemy board state is damaged
    if 4029 count ge listed unit enemy board state is damaged
    do 4027 own summon
    do 4027 own damage unit mine it card is 813680 amount=1.0
    do 4028 own create unit mine random state is bronze;region is Skellige;type is 45;state not started_in_deck
    do 4029 own create unit mine random state is bronze;region is Skellige;type is 45;state not started_in_deck
    do 4029 own play_card unit mine it type is 45

## C56 vv_6.md 5 (REAL, open, 0 table lines from the same code)
Doomed and a unit's own keyword do not make cards leave play or die, and a Doomed unit never lies in the discard, so there is no line to cards that wait for that (L1, L15).
- W gwent: Crow -> Tyr: Master of An Skellig: makes your cards leave play | network.py []
- W gwent: Bear Abomination -> Tyr: Master of An Skellig: makes your cards leave play | network.py []
- W gwent: Patricidal Fury -> Freya's Blessing: makes your units die | network.py []
- W gwent: Arnjolf the Patricide -> Freya's Blessing: makes your units die | network.py []
- R gwent: Harald an Craite -> Freya's Blessing: dies by its own effect | network.py []
- R gwent: Fucusya -> Tyr: Master of An Skellig: makes your units die: Tyr: Master of An Skellig brings them back to hand; also triggers: makes your cards leave play | network.py []
  Crow:
    when 4344 always
    when 4517 leaves_play self
    when 4517 leaves_play self
    do 4344 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4517 has_keyword obliterate self
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
  Bear Abomination:
    when 4334 always
    when 4517 leaves_play self
    when 4517 leaves_play self
    do 4334 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4517 has_keyword obliterate self
  Patricidal Fury:
    when 2610 activated self
    when 2611 always
    when 4513 always
    when 2612 always
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 2612 keyword_condition eq 0.0
    if 4513 amount_listed
    if 2612 keyword_condition
    do 2610 own summon
    do 2610 own damage unit mine it card is 813603 amount=1.0
    do 2611 own give_keyword self amount=3.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 2612 own create
    do 2612 own play_card card mine it card is 813604
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Freya's Blessing:
    when 2148 played self
    when 4517 leaves_play self
    do 2148 own play_card unit mine chosen discard state is bronze;region not Neutral
    do 2148 own give_keyword unit mine it
    do 4517 uses_keyword obliterate unit mine it
  Arnjolf the Patricide:
    when 4329 always
    when 4517 leaves_play self
    when 4330 played self
    when 4517 leaves_play self
    do 4329 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4330 own summon
    do 4330 own damage unit mine it card is 813603 amount=1.0
    do 4517 has_keyword obliterate self

## C57 vv_6.md 6 (REAL, open, 0 table lines from the same code)
a plain hit that many Gwent cards deal feeds no "whenever an enemy is damaged" trigger (L21, L11).
- W gwent: Primal Savagery -> King Bran: damages enemy units or players | network.py []
- W gwent: Seagull -> King Bran: damages enemy units or players | network.py []
- W gwent: Stunning Blow -> Onslaught: damages enemy units or players | network.py []
- W gwent: Bjorn's Drakkar -> Onslaught: damages enemy units or players | network.py []
  Primal Savagery:
    when 2819 played self
    when 2820 killed
    do 2819 own damage unit enemy chosen board amount=2.0
    do 2820 own summon
  King Bran:
    when 3931 always
    when 4544 round_start
    when 3932 played self
    when 3933 damaged unit enemy
    when 3934 game_start
    when 4544 round_start
    if 4544 event_count ge 2.0
    if 3933 amount gt 0.0
    if 3933 amount_excess
    if 4544 event_count ge 2.0
    do 3931 own give_keyword self
    do 4544 uses_keyword base_change self strength=1.0
    do 3932 own stat_change self strength=0.0
    do 3933 own increase_effect self amount=1.0
    do 3934 own repeat unit mine all board keyword is 756196
    do 4544 has_keyword base_change self strength=1.0
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
  Stunning Blow:
    when 3118 played self
    do 3118 own damage unit chosen board keyword not 756174 amount=5.0
    do 3118 own damage unit it board keyword is 756174 amount=7.0
  Onslaught:
    when 2353 activated self
    when 2354 always
    when 4513 always
    when 2355 damaged unit enemy
    when 4532 damaged self
    when 4639 activated self
    when 4640 always
    when 4513 always
    when 4641 damaged unit enemy
    when 4532 damaged self
    when 4513 always
    when 4504 played self
    if 4513 amount_listed
    if 4532 amount_listed
    if 4513 amount_listed
    if 4532 amount_listed
    if 4513 amount_listed
    do 2353 own damage unit enemy chosen board amount=3.0
    do 2354 own give_keyword self amount=2.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 2355 own give_keyword unit mine all hand type in 60;type in 59 amount=1.0
    do 4532 uses_keyword negate_damage unit mine all hand type in 60;type in 59 amount=listed
    do 4639 own damage unit enemy chosen board amount=3.0
    do 4640 own give_keyword self amount=2.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4641 own give_keyword card mine all hand type in 60;type in 59 amount=1.0
    do 4532 uses_keyword negate_damage card mine all hand type in 60;type in 59 amount=listed
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Bjorn's Drakkar:
    when 4432 always
    when 4517 leaves_play self
    when 4433 activated self
    when 4434 damaged self
    when 4435 always
    when 4513 always
    when 4517 leaves_play self
    when 4513 always
    when 4504 played self
    if 4434 amount_event_amount
    if 4513 amount_listed
    if 4513 amount_listed
    do 4432 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 4433 own damage unit enemy chosen board amount=1.0
    do 4433 own give_ability unit enemy it
    do 4434 gives damage self amount=event_amount
    do 4435 own give_keyword self amount=1.0
    do 4513 uses_keyword can self event=activated;times=listed
    do 4517 has_keyword obliterate self
    do 4513 has_keyword can self event=activated;times=listed
    do 4504 has_keyword cant self event=activated;turns=1.0

## C58 vv_6.md 7 (MISSED REAL, open, 0 table lines from the same code)
Draig Bon-Dhu puts a bronze Beast from the deck into the discard and Mask of Uroboros discards a chosen card, which is the act that fills the discard for cards that play or revive units from it, as a player builds it (L10, L17).
- W gwent: Draig Bon-Dhu -> War of Clans: NONE | network.py []
- W gwent: Draig Bon-Dhu -> Harald an Craite: NONE | network.py []
- W gwent: Draig Bon-Dhu -> Fucusya: NONE | network.py []
- W gwent: Mask of Uroboros -> Fucusya: NONE | network.py []
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
  War of Clans:
    when 3351 played self
    when 3352 killed
    when 4517 leaves_play self
    when 3353 played self
    when 4517 leaves_play self
    if 3353 keyword_condition
    if have not card mine state is started_in_deck;region is Neutral
    if 3353 have not card mine state is started_in_deck;region is Neutral
    do 3351 own damage unit enemy chosen board amount=2.0
    do 3352 own play_card unit mine chosen discard state is bronze;type is 45;cost eq 3173
    do 3352 own give_keyword unit mine it type is 45
    do 4517 uses_keyword obliterate unit mine it type is 45
    do 3353 own play_card unit mine chosen discard state is bronze;type is 45;cost eq 3174
    do 3353 own give_keyword unit mine it type is 45
    do 4517 uses_keyword obliterate unit mine it type is 45
  Harald an Craite:
    when 3335 played self
    when 4517 leaves_play self
    when 3336 round_start
    when 3337 round_start
    if 3336 have self hand
    if 3337 have self deck
    do 3335 own play_card unit mine chosen discard state is bronze;type is 45
    do 3335 own give_keyword unit mine it type is 45
    do 4517 uses_keyword obliterate unit mine it type is 45
    do 3335 own damage self amount=2.0
    do 3336 own transform self
    do 3337 own transform self
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
  Mask of Uroboros:
    when 3187 activated self
    when 4543 activated
    when 4504 played self
    do 3187 own draw card mine deck_top amount=1.0
    do 3187 own keyword_action card mine chosen hand
    do 4543 uses_keyword discard card mine chosen hand
    do 3187 own summon amount=2.0
    do 4504 has_keyword cant self event=activated;turns=1.0

## C59 vv_6.md 2 (REAL, open, 0 table lines from the same code)
Rain or Storm given to an enemy row hurts only enemy units, never mine, so it feeds nothing that waits for my units to die (L9).
- W gwent: Melusine Cultist -> Freya's Blessing: makes your units die | network.py []
- W gwent: Rage of the Sea -> Sigrdrifa's Rite: makes your units die: Sigrdrifa's Rite brings them back | network.py []
- W gwent: Fulmar -> Freya's Blessing: makes your units die | network.py []
- W gwent: Melusine Cultist -> Sigrdrifa's Rite: makes your units die: Sigrdrifa's Rite brings them back | network.py []
- R gwent: Melusine -> Freya's Blessing: makes your units die; also dies by its own effect | network.py []
- R gwent: Little Havfrue -> Sigrdrifa's Rite: makes your units die: Sigrdrifa's Rite brings them back; also dies by its own effect: Sigrdrifa's Rite brings them back | network.py []
  Melusine Cultist:
    when 3675 activated self
    when 4522 turn_start
    when 3676 turn_end
    when 3677 turn_end
    when 4504 played self
    if 3676 have position enemy all position is opposite_row of self;keyword is 756164
    if 3676 have not position enemy all position is opposite_row of self;keyword is 756160
    if 3677 have position enemy all position is opposite_row of self;keyword is 756160
    do 3675 own give_keyword position enemy chosen turns=2.0
    do 4522 uses_keyword damage unit random board position is same_row of self amount=1.0
    do 3676 own stat_change unit right_of_self board strength=1.0
    do 3677 own stat_change unit all board position is sides of self strength=1.0
    do 4504 has_keyword cant self event=activated;turns=1.0
  Freya's Blessing:
    when 2148 played self
    when 4517 leaves_play self
    do 2148 own play_card unit mine chosen discard state is bronze;region not Neutral
    do 2148 own give_keyword unit mine it
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
  Sigrdrifa's Rite:
    when 2127 played self
    when 4517 leaves_play self
    do 2127 own revive unit mine chosen discard region not Neutral
    do 2127 own give_keyword unit mine it
    do 4517 uses_keyword obliterate unit mine it
  Fulmar:
    when 3672 played self
    when 3673 activated self
    when 4518 turn_start
    when 4504 played self
    if 3673 amount_stat keyword_amount it
    do 3672 own create
    do 3672 own play_card card mine chosen hand card is 757246
    do 3673 own remove_keyword position enemy chosen keyword is 756164
    do 3673 own give_keyword position enemy it turns=stat
    do 4518 uses_keyword damage unit all board position is same_row of self amount=1.0
    do 4504 has_keyword cant self event=activated;turns=1.0

## C60 vv_6.md 3 (MISSED REAL, open, 0 table lines from the same code)
cards that give Rain or Storm to the enemy row feed cards whose own text counts or reads Rain or Storm there, which is what the player builds (L10, L14).
- W gwent: Rage of the Sea -> Anglerfish: NONE | network.py []
- W gwent: Little Havfrue -> Fulmar: NONE | network.py []
- W gwent: Tears of Siren -> Melusine Cultist: NONE | network.py []
- W gwent: Torrential Rain -> Bride of the Sea: NONE | network.py []
- R gwent: Tempest -> Torrential Rain: puts it into play from the deck | network.py []
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
  Anglerfish:
    when 4143 turn_end
    when 4144 turn_end
    if 4143 have is self deck
    if 4143 count ge 2.0 position enemy all keyword in 756164;keyword in 756160
    if 4144 have not position enemy all keyword in 756164;keyword in 756160
    do 4143 own summon self
    do 4144 own move self
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
  Fulmar:
    when 3672 played self
    when 3673 activated self
    when 4518 turn_start
    when 4504 played self
    if 3673 amount_stat keyword_amount it
    do 3672 own create
    do 3672 own play_card card mine chosen hand card is 757246
    do 3673 own remove_keyword position enemy chosen keyword is 756164
    do 3673 own give_keyword position enemy it turns=stat
    do 4518 uses_keyword damage unit all board position is same_row of self amount=1.0
    do 4504 has_keyword cant self event=activated;turns=1.0
  Tears of Siren:
    when 3678 played self
    when 4522 turn_start
    do 3678 own give_keyword position enemy chosen turns=2.0
    do 4522 uses_keyword damage unit random board position is same_row of self amount=1.0
    do 3678 own summon
  Melusine Cultist:
    when 3675 activated self
    when 4522 turn_start
    when 3676 turn_end
    when 3677 turn_end
    when 4504 played self
    if 3676 have position enemy all position is opposite_row of self;keyword is 756164
    if 3676 have not position enemy all position is opposite_row of self;keyword is 756160
    if 3677 have position enemy all position is opposite_row of self;keyword is 756160
    do 3675 own give_keyword position enemy chosen turns=2.0
    do 4522 uses_keyword damage unit random board position is same_row of self amount=1.0
    do 3676 own stat_change unit right_of_self board strength=1.0
    do 3677 own stat_change unit all board position is sides of self strength=1.0
    do 4504 has_keyword cant self event=activated;turns=1.0
  Torrential Rain:
    when 1857 played self
    when 4522 turn_start
    do 1857 own give_keyword position enemy chosen turns=3.0
    do 4522 uses_keyword damage unit random board position is same_row of self amount=1.0
  Bride of the Sea:
    when 3674 played self
    if 3674 amount_sum keyword_amount position enemy all keyword in 756164;keyword in 756160
    do 3674 own play_card card mine chosen discard type is 15;cost le 3472
    do 3674 own cost_change card mine it type is 15 cost=sum

## C61 vv_6.md 4 (REAL, open, 0 table lines from the same code)
Cursed Scroll moves a card from hand to the deck, not a unit on the board, so it gives no line to cards that only read board positions (L1, L23).
- W gwent: Cursed Scroll -> Redanian Archer: Cursed Scroll moves Redanian Archer, and Redanian Archer acts on units back row it | network.py []
- W gwent: Cursed Scroll -> Dwimveandra: Cursed Scroll moves Dwimveandra, and Dwimveandra acts on units back row it or front row it | network.py []
- W gwent: Cursed Scroll -> Avallac'h: Sage: Cursed Scroll moves Avallac'h: Sage, and Avallac'h: Sage acts on units back row it | network.py []
- W gwent: Cursed Scroll -> Lyrian Landsknecht: Cursed Scroll moves Lyrian Landsknecht, and Lyrian Landsknecht acts on units back row it or front row it | network.py []
- R gwent: Cursed Scroll -> Lyrian Arbalest: is a card whose playing sets off its effect | network.py [1823]
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
  Avallac'h: Sage:
    when 1793 played self
    if 1793 keyword_condition
    if 1793 have is self position is back_row
    do 1793 own play_card landmark mine chosen deck
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

## C62 vv_6.md 1 (REAL, open, 0 table lines from the same code)
a card that plays a card by another filter (bronze, highest, lowest, a type) does not set off a card that reacts only to a narrower kind played (gold, spell, Bonded) (L14, L17).
- W gwent: Battle Stations! -> Roach: is played | network.py []
- W gwent: Alzur's Double-Cross -> Ban Ard Tutor: is played | network.py []
- W gwent: Blessing of Charity -> Primordial D'ao: is played; also triggers: plays it: its effect goes off | network.py []
- W gwent: Artis -> Gascon: is played | network.py []
- R gwent: Aen Seidhe Saber -> Ivo of Belhaven: is played | network.py []
  Battle Stations!:
    when 4196 played self
    if 4196 amount_event_amount
    do 4196 own play_card card mine chosen hand state is bronze
    do 4196 own draw card mine deck_top amount=event_amount
  Roach:
    when 1814 played card mine state is gold
    do 1814 own summon self
  Alzur's Double-Cross:
    when 1845 played self
    do 1845 own play_card unit mine highest deck
  Ban Ard Tutor:
    when 2284 played card mine category is spell;state is gold
    do 2284 own stat_change self strength=2.0
  Blessing of Charity:
    when 4456 activated leader_ability mine
    do 4456 own play_card unit mine lowest deck
  Primordial D'ao:
    when 1979 always
    when 4535 damaged self
    when 1980 played self
    when 4535 damaged self
    if 4535 amount_event_amount
    if 1980 amount_event_count
    if 4535 amount_event_amount
    do 1979 own give_keyword self
    do 4535 uses_keyword negate_damage self amount=event_amount
    do 4535 uses_keyword remove_keyword self
    do 1980 own stat_change self strength=event_count
    do 4535 has_keyword negate_damage self amount=event_amount
    do 4535 has_keyword remove_keyword self
  Artis:
    when 2809 played self
    when 2810 played unit
    if 2810 keyword_condition
    if 2810 amount_stat strength it
    if 2810 amount_half
    if have is self position is back_row
    if 2810 have is self position is back_row
    do 2809 own play_card card mine chosen deck type is 61;cost eq 2642
    do 2810 own damage unit it amount=half
  Gascon:
    when 2580 played unit mine keyword is 756190
    if 2580 event_count ge 1.0
    do 2580 own stat_change self strength=3.0

## C63 vv_6.md 2 (REAL, open, 0 table lines from the same code)
a card that only moves, consumes or freezes cards kills no unit, and enemy-side effects feed no need about my unit's death (L11, L9).
- W gwent: Ghoul -> Dettlaff: Higher Vampire: kills it for its death effect | network.py []
- W gwent: Aen Elle Aristocrat -> Endrega Eggs: kills it for its death effect | network.py []
- W gwent: Biting Frost -> Archespore: kills it for its death effect | network.py []
- R gwent: Forktail -> Bridge Troll: kills it for its death effect | network.py []
  Ghoul:
    when 2004 played self
    when 4538 activated
    when 4516 activated
    if 2004 keyword_condition
    if 4538 amount_stat strength it
    if 2004 have is self position is front_row
    do 2004 own keyword_action unit mine chosen discard state is bronze
    do 4538 uses_keyword kill unit mine chosen discard state is bronze
    do 4538 uses_keyword stat_change unit mine chosen discard state is bronze strength=stat
    do 4538 uses_keyword keyword_action unit mine chosen discard state is bronze
    do 4516 uses_keyword obliterate unit mine chosen discard state is bronze
  Dettlaff: Higher Vampire:
    when 2823 dies self
    do 2823 own revive unit mine self discard
  Aen Elle Aristocrat:
    when 4052 activated self
    when 4053 turn_end
    when 4520 turn_start
    if 4052 keyword_condition
    if 4052 amount ge stat
    do 4052 own move unit enemy chosen board
    do 4053 own give_keyword position enemy all keyword is 756162;state is applied_this_turn turns=1.0
    do 4520 uses_keyword damage unit highest board position is same_row of self amount=2.0
  Endrega Eggs:
    when 3076 dies self
    do 3076 own summon amount=3.0
  Biting Frost:
    when 1847 played self
    when 4520 turn_start
    do 1847 own give_keyword position enemy chosen turns=3.0
    do 4520 uses_keyword damage unit highest board position is same_row of self amount=2.0
  Archespore:
    when 2266 dies self
    do 2266 own summon card mine all deck

## C64 vv_6.md 5 (REAL, open, 0 table lines from the same code)
a card that changes only itself or units on the board gives no line to cards that read buffs on hand or deck cards (L14, L18).
- W gwent: Aglaïs -> Hawker Support: changes your units' stats | network.py []
- W gwent: Aretuza Adept -> Sigismund Dijkstra: changes your units' stats | network.py []
- W gwent: Adrenaline Rush -> Farseer: changes your units' stats | network.py [1500]
- R gwent: Alchemist -> Ornate Censer: changes your units' stats | network.py []
  Aglaïs:
    when 2035 played self
    when 2036 turn_end
    if 2036 amount_stat boost self
    do 2035 own give_ability self
    do 2036 gives stat_change self strength=stat
  Hawker Support:
    when 2083 played self
    do 2083 own stat_change unit mine chosen hand state not buffed strength=1.0
    do 2083 own stat_change unit mine it hand state is buffed strength=3.0
  Aretuza Adept:
    when 2262 keyword_used unit mine keyword is 756172
    do 2262 own stat_change self strength=1.0
  Sigismund Dijkstra:
    when 4153 activated self
    when 4154 stat_changed self
    when 4504 played self
    if 4154 have is self deck
    if 4154 amount_event_amount
    do 4153 own play_card unit mine chosen deck state is buffed
    do 4154 own stat_change self strength=event_amount
    do 4504 has_keyword cant self event=activated;turns=1.0
  Adrenaline Rush:
    when 1850 played self
    if 1850 count eq 1.0 unit mine all board position is same_row of unit mine chosen board;of:kind is unit
    do 1850 own stat_change unit mine chosen board card not 756275 strength=8.0
  Farseer:
    when 2333 played self
    if 2333 amount_count unit mine all hand state is buffed
    do 2333 own stat_change unit mine chosen hand state not buffed strength=count

## C65 vv_7.md 6 (PARTLY, open, 0 table lines from the same code)
Dimun Pirate, Fisher King and Lippy Gudmund move or swap cards in the deck or discard, not units on the board, so they set up nothing for row-readers (L2, L23); Nivellen really moves units into other rows, which Tax Collector (back row) and Dol Blathanna Sentry read.
- W gwent: Dimun Pirate -> Aguara: Dimun Pirate moves Aguara, and Aguara acts on units back row it or front row it | network.py []
- W gwent: Fisher King -> Cintrian Artificer: Fisher King moves Cintrian Artificer, and Cintrian Artificer acts on units back row it or front row it | network.py []
- W gwent: Lippy Gudmund -> Cerys an Craite: Lippy Gudmund moves Cerys an Craite, and Cerys an Craite acts on units back row it or front row it | network.py []
- R gwent: Nivellen -> Tax Collector: Nivellen moves Tax Collector, and Tax Collector acts on units back row it | network.py []
  Dimun Pirate:
    when 2139 played self
    if 2139 have not unit mine all board type is 59
    do 2139 own move card mine top deck
  Aguara:
    when 2298 played self
    when 4523 always
    when 2299 played self
    if 2298 keyword_condition
    if 2299 keyword_condition
    if 2298 have is self position is front_row
    if 2299 have is self position is back_row
    do 2298 own give_keyword unit chosen board
    do 4523 uses_keyword silence unit chosen board
    do 2299 own remove_keyword unit chosen board
  Fisher King:
    when 2663 played self
    if 2663 keyword_condition
    if 2663 have is self position is back_row
    do 2663 own move card mine chosen deck
  Cintrian Artificer:
    when 2763 always
    when 4524 played self
    when 4510 played self
    when 4525 played self
    when 2764 activated self
    when 4535 damaged self
    when 4524 played self
    when 4510 played self
    when 4525 played self
    when 4504 played self
    if 4524 have is self position is front_row
    if 4525 have is self position is back_row
    if 4535 amount_event_amount
    if 4524 have is self position is front_row
    if 4525 have is self position is back_row
    do 2763 own give_keyword self
    do 4524 uses_keyword give_keyword self
    do 4510 uses_keyword can self event=activated
    do 4525 uses_keyword stat_change self strength=1.0
    do 2764 own give_keyword unit mine chosen board
    do 4535 uses_keyword negate_damage unit mine chosen board amount=event_amount
    do 4535 uses_keyword remove_keyword unit mine chosen board
    do 4524 has_keyword give_keyword self
    do 4510 uses_keyword can self event=activated
    do 4525 has_keyword stat_change self strength=1.0
    do 4504 has_keyword cant self event=activated;turns=1.0
  Lippy Gudmund:
    when 2595 played self
    if 2595 keyword_condition
    if 2595 have is self position is back_row
    do 2595 own swap card mine discard
  Cerys an Craite:
    when 2375 played self
    when 2376 played self
    if 2375 keyword_condition
    if 2376 keyword_condition
    if 2375 have is self position is front_row
    if 2376 have is self position is back_row
    do 2375 own summon
    do 2376 own summon

## C66 vv_7.md 7 (REAL, open, 0 table lines from the same code)
the putting-into-play line goes to cards with only a death effect or a stat trigger, none of which goes off when a unit is put into play (L17).
- W gwent: Brewess: Ritual -> Archespore: puts it into play from the deck | network.py []
- W gwent: Whispering Hillock -> Bridge Troll: puts it into play from the deck | network.py []
- W gwent: Artis -> Svalblod Fanatic: puts it into play from the deck; also enables: damages it for its effect | network.py []
- R gwent: Ermion -> Gigascorpion Decoction: puts it into play from the deck | network.py []
  Brewess: Ritual:
    when 2384 dies self
    do 2384 own summon unit mine random deck state is bronze;keyword is 756173
  Archespore:
    when 2266 dies self
    do 2266 own summon card mine all deck
  Whispering Hillock:
    when 2449 played self
    do 2449 own play_card unit mine chosen deck keyword is 756173
  Bridge Troll:
    when 2546 dies self
    do 2546 own stat_change unit mine lowest board strength=4.0
  Artis:
    when 2809 played self
    when 2810 played unit
    if 2810 keyword_condition
    if 2810 amount_stat strength it
    if 2810 amount_half
    if have is self position is back_row
    if 2810 have is self position is back_row
    do 2809 own play_card card mine chosen deck type is 61;cost eq 2642
    do 2810 own damage unit it amount=half
  Svalblod Fanatic:
    when 2818 stat_changed self
    if 2818 stat strength le 2.0 self
    if stat strength le listed self
    do 2818 own transform self

## C67 vv_7.md 8 (REAL, open, 0 table lines from the same code)
Anna Henrietta copies a leader ability, Drummond Queensguard copies itself, Aguara: True Form plays its created spell at once and Alissa Henson copies a card elsewhere, so none leaves a created card where the second card copies from (L19).
- W gwent: Anna Henrietta -> Imperial Practitioner: creates cards: Imperial Practitioner copys them | network.py []
- W gwent: Drummond Queensguard -> Operator: creates cards: Operator copys them | network.py []
- W gwent: Aguara: True Form -> Caranthir Ar-Feiniel: creates cards: Caranthir Ar-Feiniel copys them | network.py []
- W gwent: Alissa Henson -> Blue Stripes Scout: creates cards: Blue Stripes Scout copys them | network.py []
- R gwent: Cynthia -> Curse of Lust: creates cards: Curse of Lust copys them | network.py []
  Anna Henrietta:
    when 3626 played self
    if 3626 keyword_condition
    if 3626 have is self position is back_row
    do 3626 own copy leader_ability enemy
  Imperial Practitioner:
    when 3780 always
    when 4557 played card mine state not started_in_deck
    when 3781 activated self
    when 4557 played card mine state not started_in_deck
    when 4504 played self
    if 4557 amount_listed
    if 4557 amount_listed
    do 3780 own give_keyword self
    do 4557 uses_keyword stat_change self strength=listed
    do 3781 own copy card enemy top discard state is created
    do 4557 has_keyword stat_change self strength=listed
    do 4504 has_keyword cant self event=activated;turns=1.0
  Drummond Queensguard:
    when 2143 activated self
    if 2143 keyword_condition 3.0
    if 2143 stat strength le listed self
    do 2143 own copy self
  Operator:
    when 1812 played self
    do 1812 own copy unit mine chosen hand state is bronze;state is created
    do 1812 own copy unit mine chosen hand state is bronze;state is created
  Aguara: True Form:
    when 2296 played self
    if 2296 keyword_condition
    if 2296 have is self position is back_row
    do 2296 own create card mine random category is spell
    do 2296 own play_card card mine it category is spell
  Caranthir Ar-Feiniel:
    when 1952 played self
    do 1952 own copy card mine chosen hand region not Neutral;cost le 1927;state is created
    do 1952 own stat_set card mine it strength=1.0
  Alissa Henson:
    when 3833 played self
    do 3833 own shuffle_into_deck card mine chosen discard category is spell
    do 3833 own copy card mine it state is bronze
  Blue Stripes Scout:
    when 1926 played self
    when 4579 played self
    if 1926 keyword_condition
    if 4579 keyword_condition
    if 1926 have is self position is front_row
    if 4579 have is self position is front_row
    do 1926 own copy unit mine chosen board state is bronze;region not Neutral;state is created
    do 4579 own copy unit mine chosen board state is bronze;region not Neutral

## C68 vv_7.md 9 (REAL, open, 0 table lines from the same code)
Arena Endrega gives Bones, but Eveline Gallo acts only when the player has none, so gaining Bones works against it (L21 read wants right).
- W gwent: Arena Endrega -> Eveline Gallo: lets you gain the second resource (Bones) | network.py []
- R gwent: Pickpocket -> Hvitr and Aelydia: lets you gain the second resource (Bones) | network.py []
  Arena Endrega:
    when 2927 played self
    if 2927 amount_stat damage unit mine chosen board
    do 2927 own mana_gain secondary_resource mine amount=stat
  Eveline Gallo:
    when 4179 turn_end
    if 4179 have not secondary_resource mine
    do 4179 own mana_gain secondary_resource mine amount=3.0

## C69 vv_7.md 10 (REAL, open, 0 table lines from the same code)
Disgraced Brawler locks or kills itself and Skjall kills itself when damaged, so damage feeds only a drawback to itself (L5).
- W gwent: An Craite Marauder -> Disgraced Brawler: damages enemy units or players | network.py []
- W gwent: Dragon's Dream -> Skjall: damages it for its effect | network.py []
- R gwent: Hemdall -> Svalblod Fanatic: damages it for its effect | network.py []
  An Craite Marauder:
    when 2439 played self
    if 2439 keyword_condition
    if 2439 have is self position is front_row
    do 2439 own damage unit enemy all board amount=3.0;spread=1.0
  Disgraced Brawler:
    when 2821 played self
    when 4523 always
    when 2822 stat_changed self
    if 2821 keyword_condition 1.0
    if 2822 stat strength le 3.0 self
    if stat strength le listed self
    if 2821 count ge listed unit enemy board state is damaged
    do 2821 own give_keyword self
    do 4523 uses_keyword silence self
    do 2822 own kill self
  Dragon's Dream:
    when 2507 played self
    when 4554 turn_start
    when 4555 countdown_done self
    do 2507 own give_keyword position enemy chosen turns=3.0
    do 4554 uses_keyword countdown_advance position enemy chosen amount=1.0
    do 4555 uses_keyword damage unit all board position is same_row of self amount=3.0
  Skjall:
    when 2381 stat_changed self
    if 2381 keyword_condition 5.0
    if stat strength le listed self
    if 2381 stat strength le listed self
    do 2381 own kill self

## C70 vv_7.md 11 (PARTLY, open, 0 table lines from the same code)
Biting Frost and Dragon's Dream hit only the enemy row, so they feed no need about my own damaged units (Drummond Queensguard, Skjall) (L9); Bear Witcher Mentor's second mode counts damaged units of all sides, so enemy damage feeds it.
- W gwent: Biting Frost -> Drummond Queensguard: damages it for its effect | network.py []
- W gwent: Dragon's Dream -> Skjall: damages it for its effect | network.py []
- R gwent: Biting Frost -> Bear Witcher Mentor: damages units or players; also damages your units or players | network.py []
- R gwent: Red Riders: Precision -> Caranthir: Golden Child: damages units or players | network.py []
  Biting Frost:
    when 1847 played self
    when 4520 turn_start
    do 1847 own give_keyword position enemy chosen turns=3.0
    do 4520 uses_keyword damage unit highest board position is same_row of self amount=2.0
  Drummond Queensguard:
    when 2143 activated self
    if 2143 keyword_condition 3.0
    if 2143 stat strength le listed self
    do 2143 own copy self
  Dragon's Dream:
    when 2507 played self
    when 4554 turn_start
    when 4555 countdown_done self
    do 2507 own give_keyword position enemy chosen turns=3.0
    do 4554 uses_keyword countdown_advance position enemy chosen amount=1.0
    do 4555 uses_keyword damage unit all board position is same_row of self amount=3.0
  Skjall:
    when 2381 stat_changed self
    if 2381 keyword_condition 5.0
    if stat strength le listed self
    if 2381 stat strength le listed self
    do 2381 own kill self

## C71 vv_7.md 1 (PARTLY, open, 0 table lines from the same code)
Biting Frost and Dragon's Dream act on the enemy row, so they feed no need about MY units dying or being damaged (L9); Bear Witcher Mentor also counts enemy damaged units, so that line is right.
- W gwent: Biting Frost -> Frightener: Dormant: makes your units die | network.py []
- W gwent: Biting Frost -> Hjalmar an Craite: makes your units die: Hjalmar an Craite Banishes them | network.py []
- W gwent: Biting Frost -> Blueboy Lugos: damages it for its effect | network.py []
- R gwent: Dragon's Dream -> Bear Witcher Mentor: damages units or players; also damages your units or players | network.py []
- R gwent: Curse of Corruption -> Svanrige Tuirseach: makes your units die | network.py []
- R gwent: Curse of Corruption -> Mourntart: makes your units die: Mourntart Banishes them | network.py []
- R gwent: Biting Frost -> Wild Boar of the Sea: damages enemy units or players: Wild Boar of the Sea damages them | network.py []
  Biting Frost:
    when 1847 played self
    when 4520 turn_start
    do 1847 own give_keyword position enemy chosen turns=3.0
    do 4520 uses_keyword damage unit highest board position is same_row of self amount=2.0
  Frightener: Dormant:
    when 4307 dies unit mine
    if 4307 event_count ge 3.0
    do 4307 own transform self
  Hjalmar an Craite:
    when 2096 played self
    when 4516 activated
    if 2096 keyword_condition
    if 2096 amount_stat strength unit mine it discard
    if 2096 have is self position is front_row
    do 2096 own keyword_action unit mine chosen discard
    do 4516 uses_keyword obliterate unit mine chosen discard
    do 2096 own damage unit enemy chosen board amount=stat
  Blueboy Lugos:
    when 2105 damaged self
    do 2105 own damage unit enemy random board amount=2.0

## C72 vv_7.md 2 (REAL, open, 0 table lines from the same code)
An Craite Longship deals a plain 1 damage to one unit, which feeds no "when an enemy dies" or "makes units die" line (L11).
- W gwent: An Craite Longship -> Saesenthessis: Blaze: makes enemy units die | network.py []
- W gwent: An Craite Longship -> Regis: makes units die | network.py []
- W gwent: An Craite Longship -> Northern Wind: makes units die: Northern Wind Banishes them | network.py []
- W gwent: An Craite Longship -> Funeral Boat: makes units die | network.py []
- R gwent: Basilisk Venom -> Vran Warrior: makes units die | network.py []
- R gwent: Basilisk Venom -> Hybrid: makes units die | network.py []
  An Craite Longship:
    when 2154 played unit enemy
    if 2154 keyword_condition
    if have is self position is front_row
    if 2154 have is self position is front_row
    do 2154 own damage unit enemy it amount=1.0
  Saesenthessis: Blaze:
    when 2469 always
    when 4507 game_start
    when 2470 dies unit enemy
    when 2471 obliterated unit enemy
    when 4507 game_start
    if 4507 amount_count card mine type is 38;state is started_in_deck
    if 2470 my_turn
    if 2471 my_turn
    if 4507 amount_count card mine type is 38;state is started_in_deck
    do 2469 own give_keyword self
    do 4507 uses_keyword stat_change self strength=count
    do 2470 own stat_change self strength=1.0
    do 2471 own stat_change self strength=1.0
    do 4507 has_keyword stat_change self strength=count
  Regis:
    when 1779 played self
    when 1780 played self
    if 1780 keyword_condition
    if 1780 event_count ge 1.0
    if event_count eq 0.0
    if 1780 event_count eq 0.0
    do 1779 own damage unit all board position is same_row of position enemy chosen;of:kind is position amount=1.0
    do 1780 own repeat effect
  Northern Wind:
    when 2680 played self
    when 2681 killed
    when 4516 activated
    do 2680 own damage unit chosen board amount=4.0
    do 2681 own keyword_action unit it discard
    do 4516 uses_keyword obliterate unit it discard
  Funeral Boat:
    when 4216 dies card
    when 4217 discarded card
    if 4216 my_turn
    if 4217 my_turn
    do 4216 own damage unit enemy random board amount=1.0
    do 4217 own damage unit enemy random board amount=1.0

## C73 vv_7.md 5 (REAL, open, 0 table lines from the same code)
Dimun Pirate and Fisher King move a card in the deck, not a unit on the board, so nothing is set up for cards that act on units next to a moved unit (L14, L2).
- W gwent: Dimun Pirate -> Arachas Venom: Dimun Pirate moves units, and Arachas Venom acts on units next to its target | network.py []
- W gwent: Dimun Pirate -> Berengar: Dimun Pirate moves Berengar and your units, and Berengar acts on units in its row | network.py []
- W gwent: Fisher King -> Heymaey Protector: Fisher King moves Heymaey Protector and units, and Heymaey Protector acts on units next to it | network.py []
- W gwent: Fisher King -> Dennis Cranmer: Fisher King moves Dennis Cranmer and your units, and Dennis Cranmer acts on units next to it | network.py []
  Dimun Pirate:
    when 2139 played self
    if 2139 have not unit mine all board type is 59
    do 2139 own move card mine top deck
  Arachas Venom:
    when 2251 played self
    when 2252 killed
    do 2251 own damage unit chosen board amount=3.0
    do 2252 own damage unit all board position is sides of it amount=3.0
  Berengar:
    when 3485 turn_start
    if 3485 have not unit mine all board type is 34;position is same_row of self;card not 757163
    do 3485 own kill self
  Fisher King:
    when 2663 played self
    if 2663 keyword_condition
    if 2663 have is self position is back_row
    do 2663 own move card mine chosen deck
  Heymaey Protector:
    when 2349 damaged unit position is sides of self
    do 2349 own stat_change self strength=1.0
  Dennis Cranmer:
    when 2040 played self
    if 2040 amount_stat armor it
    do 2040 own stat_change unit mine all board position is sides of self;keyword is 756174 strength=stat

## C74 vv_7.md 7 (PARTLY, open, 0 table lines from the same code)
Allgod buffs cards in the deck and Cyprian Wiley uses a keyword on another card, while Koshchey and Call of the Depths wait for their own keyword use (L7, L15); Alzur's Double-Cross is itself a spell that is played, which Cintrian Spellweaver's play trigger reads (L1b, a minority kind).
- W gwent: Allgod -> Call of the Depths: uses a keyword or status | network.py []
- W gwent: Cyprian Wiley -> Koshchey: uses a keyword or status | network.py []
- R gwent: Alzur's Double-Cross -> Cintrian Spellweaver: is played; also is a card whose playing sets off its effect | network.py [1823]
- R gwent: Magne Division -> Experimental Remedy: puts it into play from the hand | network.py []
  Allgod:
    when 3305 played self
    if 3305 amount_sum
    if 3305 amount_count card mine all deck card is 757094;state is started_in_deck
    do 3305 own stat_change unit mine chosen deck strength=2.0
  Call of the Depths:
    when 4496 always
    when 4516 activated
    if 4496 event_count ge 4.0
    do 4496 own summon
    do 4496 own keyword_action self
    do 4516 uses_keyword obliterate self
  Cyprian Wiley:
    when 1818 played self
    when 4516 activated
    do 1818 own keyword_action unit chosen board strength le 1814
    do 4516 uses_keyword obliterate unit chosen board strength le 1814
  Koshchey:
    when 3572 always
    when 4540 played unit mine strength gt 4192
    when 3573 keyword_used self
    when 3574 keyword_used self
    when 4540 played unit mine strength gt 4192
    if 4540 amount_listed
    if 3573 keyword_condition
    if 3573 keyword_condition not 4.0
    if 3574 keyword_condition
    if 3574 keyword_condition 4.0
    if 4540 amount_listed
    if count le listed card mine hand
    if 3573 keyword_condition
    if 3573 count le listed card mine hand
    if 3574 keyword_condition
    if 3574 count le listed card mine hand
    do 3572 own give_keyword self
    do 4540 uses_keyword stat_change self strength=listed
    do 3573 own summon
    do 3574 own summon
    do 4540 has_keyword stat_change self strength=listed

## C75 vv_7.md 8 (REAL, open, 0 table lines from the same code)
Adrenaline Rush changes a unit on the board, while Mysterious Puzzle Box transforms a card in hand that was targeted, and no stat is read (L16).
- W gwent: Adrenaline Rush -> Mysterious Puzzle Box: targets your cards: Mysterious Puzzle Box transforms them | network.py []
- R gwent: Adrenaline Rush -> Bloody Baron: changes units' stats: Bloody Baron gives them Bleeding | network.py [1500]
  Adrenaline Rush:
    when 1850 played self
    if 1850 count eq 1.0 unit mine all board position is same_row of unit mine chosen board;of:kind is unit
    do 1850 own stat_change unit mine chosen board card not 756275 strength=8.0
  Mysterious Puzzle Box:
    when 3963 always
    when 4527 always
    when 4528 played self
    when 4569 always
    when 3964 played self
    when 3965 played self
    when 3966 played self
    when 3967 activated self
    when 3968 turn_end
    when 4516 activated
    when 4527 always
    when 4528 played self
    when 4569 always
    when 4504 played self
    if 3964 keyword_condition not 2.0
    if 3965 keyword_condition not 2.0
    if 3965 have not player state is passed
    if 3966 keyword_condition 2.0
    if count le listed card mine hand
    if 3964 count le listed card mine hand
    if 3965 count le listed card mine hand
    if 3966 count le listed card mine hand
    do 3963 own give_keyword self
    do 4527 uses_keyword can self event=summoned
    do 4528 uses_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
    do 3964 own summon
    do 3964 own stat_set unit mine it card is 813616 strength=7.0
    do 3965 own choose_card card mine chosen hand
    do 3966 own summon
    do 3966 own stat_set unit mine it card is 813616 strength=7.0
    do 3966 own kill self
    do 3967 own choose_card card mine chosen hand
    do 3968 own transform card mine highest hand state is targeted_this_round
    do 3968 own keyword_action self
    do 4516 uses_keyword obliterate self
    do 4527 has_keyword can self event=summoned
    do 4528 has_keyword give_keyword self
    do 4569 uses_keyword can self event=summoned
    do 4504 has_keyword cant self event=activated;turns=1.0

## C76 vv_7.md 1 (REAL, open, 0 table lines from the same code)
Renfri's Gang and Alzur put units into play, but Procession of Penance counts tokens and Smoke Them Out! reads buffed units, so neither waits for that summoning (L17, L3).
- W gwent: Renfri's Gang -> Procession of Penance: puts your units into play | network.py []
- W gwent: Alzur -> Smoke Them Out!: puts your units into play | network.py []
- R gwent: Blue Stripes Commando -> Kennet and Gar: puts your units into play; also is a Soldier whose summoning sets off its effect | network.py [1823]
  Renfri's Gang:
    when 3918 played self
    if 3918 count ge 25.0 unit mine state is started_in_deck
    do 3918 own summon card mine all deck state is copy_of_it
  Procession of Penance:
    when 2930 played self
    if 2930 amount_sum
    if 2930 amount_product
    if 2930 amount_count unit mine all board type is 20;state is token
    if 2930 amount_minus
    do 2930 own damage self amount=sum
  Alzur:
    when 3473 played spell mine
    when 3474 always
    do 3473 own summon unit mine random deck cost eq 3253
    do 3474 own give_keyword self amount=3.0
  Smoke Them Out!:
    when 3404 played self
    when 3405 played self
    when 4730 played self
    when 4731 played self
    if 3404 have not unit mine all board state is buffed
    if 3405 have unit mine all board state is buffed
    if 4730 have not unit mine board state is buffed
    if 4731 have is unit mine board state is buffed
    do 3404 own summon amount=2.0
    do 3405 own summon amount=2.0
    do 3405 own stat_change unit mine it card is 813629 strength=1.0
    do 4730 own summon unit mine amount=2.0
    do 4731 own summon unit mine amount=2.0
    do 4731 own stat_change unit mine all board card is 813629;state is summoned_this_round strength=1.0

## C77 vv_7.md 1 (MISSED REAL, open, 0 table lines from the same code)
case n545 is the players' truth, and no rule forbids it in its own words; Mahakam Pass gives armor, a keyword Naiad Fledgling's own text reacts to (L14).
- W gwent: Mahakam Pass -> Naiad Fledgling: NONE | network.py [] | cases n545 line
  Mahakam Pass:
    when 4277 always
    when 4541 round_end
    when 4278 played self
    when 4532 damaged self
    when 4279 activated self
    when 4541 round_end
    when 4504 played self
    if 4532 amount_listed
    do 4277 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 4278 own create card mine random region is Scoiatael;type is 39
    do 4278 own give_keyword card mine it type is 39 amount=4.0
    do 4532 uses_keyword negate_damage card mine it type is 39 amount=listed
    do 4279 own create
    do 4279 own play_card card mine it card is 757004
    do 4541 has_keyword cant self event=leaves_play
    do 4541 has_keyword remove_keyword self
    do 4504 has_keyword cant self event=activated;turns=1.0
  Naiad Fledgling:
    when 4036 keyword_used keyword is 756204
    when 4534 turn_end
    when 4037 activated self
    when 4504 played self
    if 4037 amount_event_amount
    do 4036 own give_keyword unit left_of_self amount=2.0
    do 4534 uses_keyword stat_change unit left_of_self strength=1.0
    do 4037 own remove_keyword unit mine chosen board
    do 4037 own stat_change self strength=event_amount
    do 4504 has_keyword cant self event=activated;turns=1.0

## C78 vv_7.md 2 (MISSED REAL, open, 0 table lines from the same code)
case n546 is the players' truth, and no rule forbids it; Mahakam Pass makes and plays the card Naiad Pondkeeper's text acts on (L3).
- W gwent: Mahakam Pass -> Naiad Pondkeeper: NONE | network.py [] | cases n546 line
  Mahakam Pass:
    when 4277 always
    when 4541 round_end
    when 4278 played self
    when 4532 damaged self
    when 4279 activated self
    when 4541 round_end
    when 4504 played self
    if 4532 amount_listed
    do 4277 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 4278 own create card mine random region is Scoiatael;type is 39
    do 4278 own give_keyword card mine it type is 39 amount=4.0
    do 4532 uses_keyword negate_damage card mine it type is 39 amount=listed
    do 4279 own create
    do 4279 own play_card card mine it card is 757004
    do 4541 has_keyword cant self event=leaves_play
    do 4541 has_keyword remove_keyword self
    do 4504 has_keyword cant self event=activated;turns=1.0
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

## C79 vv_7.md 5 (MISSED REAL, open, 0 table lines from the same code)
case n551 is the players' truth, and no rule forbids it in its own words; Redanian Secret Service gives Kaedweni Revenant a cheap unit to kill (L10).
- W gwent: Redanian Secret Service -> Kaedweni Revenant: NONE | network.py [] | cases n551 line
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
  Kaedweni Revenant:
    when 2487 activated self
    when 2488 killed
    when 4504 played self
    do 2487 own damage unit chosen board amount=1.0
    do 2488 own copy self
    do 4504 has_keyword cant self event=activated;turns=1.0

## C80 vv_7.md 6 (MISSED REAL, open, 0 table lines from the same code)
case n553 is the players' truth, and no rule forbids it in its own words (L9 does not forbid it).
- W gwent: Drakenborg -> Vincent Meis: NONE | network.py [] | cases n553 line
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

## C81 vv_8.md 9 (MISSED REAL, open, 0 table lines from the same code)
Vincent Meis sets an unboosted enemy to strength 1 and Kaedweni Revenant's 1 damage then kills it and copies itself, a strike now (L2); no rule forbids it.
- W gwent: Kaedweni Revenant -> Vincent Meis: NONE | network.py [] | cases n557 line
  Kaedweni Revenant:
    when 2487 activated self
    when 2488 killed
    when 4504 played self
    do 2487 own damage unit chosen board amount=1.0
    do 2488 own copy self
    do 4504 has_keyword cant self event=activated;turns=1.0
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

## C82 vv_8.md 10 (MISSED REAL, open, 0 table lines from the same code)
Vincent Meis sets an unboosted enemy to strength 1 and Redanian Archer's 1 damage then kills it, a strike now (L2); no rule forbids it.
- W gwent: Redanian Archer -> Vincent Meis: NONE | network.py [] | cases n558 line
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

## C83 vv_8.md 12 (MISSED REAL, open, 0 table lines from the same code)
Sabrina Glevissig's death damage of 3 to all in her row leaves weak units for Kaedweni Revenant's 1 damage kill, a kill effect on all (L11); no rule forbids it.
- W gwent: Sabrina Glevissig -> Kaedweni Revenant: NONE | network.py [] | cases n561 line
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
  Kaedweni Revenant:
    when 2487 activated self
    when 2488 killed
    when 4504 played self
    do 2487 own damage unit chosen board amount=1.0
    do 2488 own copy self
    do 4504 has_keyword cant self event=activated;turns=1.0

## C84 vv_8.md 13 (MISSED REAL, open, 0 table lines from the same code)
Philippa: Blind Fury's 4, 3, 2, 1 damage leaves weak units for Kaedweni Revenant's 1 damage kill, hits on several targets (L11); no rule forbids it.
- W gwent: Philippa: Blind Fury -> Kaedweni Revenant: NONE | network.py [] | cases n562 line
  Philippa: Blind Fury:
    when 3028 played self
    do 3028 own damage unit enemy chosen board amount=4.0
    do 3028 own damage unit enemy random board amount=3.0
    do 3028 own damage unit enemy random board amount=2.0
    do 3028 own damage unit enemy random board amount=1.0
  Kaedweni Revenant:
    when 2487 activated self
    when 2488 killed
    when 4504 played self
    do 2487 own damage unit chosen board amount=1.0
    do 2488 own copy self
    do 4504 has_keyword cant self event=activated;turns=1.0

## C85 vv_8.md 14 (MISSED REAL, open, 0 table lines from the same code)
a case says Vernon Roche is Revenant food and no rule of LINE_RULES.md forbids that line in its own words.
- W gwent: Vernon Roche -> Kaedweni Revenant: NONE | network.py [] | cases n564 line
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
  Kaedweni Revenant:
    when 2487 activated self
    when 2488 killed
    when 4504 played self
    do 2487 own damage unit chosen board amount=1.0
    do 2488 own copy self
    do 4504 has_keyword cant self event=activated;turns=1.0

## C86 vv_8.md 15 (MISSED REAL, open, 0 table lines from the same code)
Ale of the Ancestors buffs a unit and Knight-Errant's own text counts buffed units at its sides, so it is fed (L14 kept: anything a card counts).
- W gwent: Ale of the Ancestors -> Knight-Errant: NONE | network.py [] | cases n565 line
  Ale of the Ancestors:
    when 2423 always
    when 4541 round_end
    when 2424 always
    when 4510 played self
    when 2425 activated self
    when 2426 targeted self
    when 2427 targeted self
    when 2428 always
    when 4511 activated self
    when 4541 round_end
    when 4510 played self
    when 4504 played self
    if 4511 amount_listed
    do 2423 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 2424 own give_keyword self
    do 4510 uses_keyword can self event=activated
    do 2425 own stat_change unit chosen board strength=3.0
    do 2425 own give_ability unit it
    do 2426 gives stat_change self strength=2.0
    do 2425 own give_ability unit it
    do 2427 gives stat_change self strength=2.0
    do 2428 own keyword_action amount=2.0
    do 4511 uses_keyword cant event=activated;turns=listed
    do 4541 has_keyword cant self event=leaves_play
    do 4541 has_keyword remove_keyword self
    do 4510 has_keyword can self event=activated
    do 4504 has_keyword cant self event=activated;turns=1.0
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

## C87 vv_8.md 18 (MISSED REAL, open, 0 table lines from the same code)
Strays of Spalla shuffles a gold card into the deck, which is the move Albrich's own text waits for (L14 kept: anything a card waits for); no rule forbids it.
- W gwent: Strays of Spalla -> Albrich: NONE | network.py [] | cases n577 line
  Strays of Spalla:
    when 2613 played self
    when 2614 played self
    if 2613 keyword_condition not
    if 2614 keyword_condition
    if have is unit mine board state is copy_of_it
    if 2613 have is unit mine board state is copy_of_it
    if 2614 have is unit mine board state is copy_of_it
    do 2613 own shuffle_into_deck card mine chosen hand state is gold
    do 2613 own draw card mine deck state is bronze amount=1.0
    do 2613 own stat_change self strength=4.0
    do 2614 own shuffle_into_deck card mine chosen hand state is gold
    do 2614 own stat_change self strength=4.0
  Albrich:
    when 2184 moves self
    if 2184 have self deck_top
    do 2184 own stat_change unit mine random board strength=2.0
    do 2184 own stat_change self strength=2.0

## C88 vv_8.md 19 (MISSED REAL, open, 0 table lines from the same code)
Summoning Circle puts a chosen unit from the deck into play, so a player picks Imperial Golem for it (L17); no rule forbids it in words.
- W gwent: Summoning Circle -> Imperial Golem: NONE | network.py [] | cases n578 line
  Summoning Circle:
    when 2247 always
    when 4541 round_end
    when 2248 played self
    when 2249 turn_end
    when 2250 countdown_done self
    when 4541 round_end
    if 2248 amount_stat cost unit mine it deck
    if 2249 amount_count unit mine all board position is sides of self
    if 2249 amount_minus
    do 2247 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 2248 own look unit mine all deck
    do 2248 own choose_card unit mine chosen deck
    do 2248 own give_keyword self amount=stat
    do 2249 own give_keyword self amount=minus
    do 2250 own summon unit mine it deck
    do 2250 own kill self
    do 4541 has_keyword cant self event=leaves_play
    do 4541 has_keyword remove_keyword self
  Imperial Golem:
    when 2021 played self
    when 4506 activated
    if 2021 amount_stat strength unit enemy it deck
    do 2021 own keyword_action unit enemy top deck
    do 4506 uses_keyword reveal unit enemy top deck
    do 2021 own damage self amount=stat
    do 2021 own shuffle_into_deck unit enemy it deck

## C89 vv_8.md 21 (MISSED REAL, open, 0 table lines from the same code)
Hammond moves an enemy unit and Ragh Nar Roog's damage hits units in its row, so moving a target in gives it a hit (L2: a strike now); no rule forbids it.
- W gwent: Hammond -> Ragh Nar Roog: NONE | network.py [] | cases n587 line
  Hammond:
    when 2942 played self
    when 4526 turn_end
    if 2942 amount_sum
    if 2942 amount_count unit all board position is sides of self;type is 60
    do 2942 own move unit enemy chosen board
    do 2942 own give_keyword unit enemy it board amount=sum
    do 4526 uses_keyword damage unit enemy it board amount=1.0
  Ragh Nar Roog:
    when 1827 always
    when 4517 leaves_play self
    when 1828 played unit mine chosen state is gold
    when 1829 played self
    when 4514 turn_start
    when 1830 played unit mine chosen state is gold
    when 1831 played unit mine chosen state is gold
    when 4517 leaves_play self
    if 1830 stage 1.0
    if 1831 stage 2.0
    do 1827 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 1828 own stage_advance self
    do 1829 own give_keyword position enemy all turns=2.0
    do 4514 uses_keyword damage unit random board position is same_row of self amount=3.0;spread=1.0
    do 1830 own damage unit enemy chosen board amount=5.0
    do 1831 own create
    do 1831 own play_card card mine chosen hand card is 756272
    do 4517 has_keyword obliterate self

## C90 vv_9.md 28 (MISSED REAL, open, 0 table lines from the same code)
case n577 and n578 say these lines exist and no rule of L1-L24 forbids them in its words (Strays of Spalla shuffles a card into the deck for Albrich to proc; Summoning Circle picks the unit Imperial Golem from the deck, L17).
- W gwent: Strays of Spalla -> Albrich: NONE | network.py [] | cases n577 line
- W gwent: Summoning Circle -> Imperial Golem: NONE | network.py [] | cases n578 line
  Strays of Spalla:
    when 2613 played self
    when 2614 played self
    if 2613 keyword_condition not
    if 2614 keyword_condition
    if have is unit mine board state is copy_of_it
    if 2613 have is unit mine board state is copy_of_it
    if 2614 have is unit mine board state is copy_of_it
    do 2613 own shuffle_into_deck card mine chosen hand state is gold
    do 2613 own draw card mine deck state is bronze amount=1.0
    do 2613 own stat_change self strength=4.0
    do 2614 own shuffle_into_deck card mine chosen hand state is gold
    do 2614 own stat_change self strength=4.0
  Albrich:
    when 2184 moves self
    if 2184 have self deck_top
    do 2184 own stat_change unit mine random board strength=2.0
    do 2184 own stat_change self strength=2.0
  Summoning Circle:
    when 2247 always
    when 4541 round_end
    when 2248 played self
    when 2249 turn_end
    when 2250 countdown_done self
    when 4541 round_end
    if 2248 amount_stat cost unit mine it deck
    if 2249 amount_count unit mine all board position is sides of self
    if 2249 amount_minus
    do 2247 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 2248 own look unit mine all deck
    do 2248 own choose_card unit mine chosen deck
    do 2248 own give_keyword self amount=stat
    do 2249 own give_keyword self amount=minus
    do 2250 own summon unit mine it deck
    do 2250 own kill self
    do 4541 has_keyword cant self event=leaves_play
    do 4541 has_keyword remove_keyword self
  Imperial Golem:
    when 2021 played self
    when 4506 activated
    if 2021 amount_stat strength unit enemy it deck
    do 2021 own keyword_action unit enemy top deck
    do 4506 uses_keyword reveal unit enemy top deck
    do 2021 own damage self amount=stat
    do 2021 own shuffle_into_deck unit enemy it deck

## C91 vv_9.md 31 (MISSED REAL, open, 0 table lines from the same code)
case n586 and n587 say these lines exist and no rule forbids them in its words (Seagull's swarm and Hammond's move of an enemy unit feed Ragh Nar Roog).
- W gwent: Seagull -> Ragh Nar Roog: NONE | network.py [] | cases n586 line
- W gwent: Hammond -> Ragh Nar Roog: NONE | network.py [] | cases n587 line
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
  Ragh Nar Roog:
    when 1827 always
    when 4517 leaves_play self
    when 1828 played unit mine chosen state is gold
    when 1829 played self
    when 4514 turn_start
    when 1830 played unit mine chosen state is gold
    when 1831 played unit mine chosen state is gold
    when 4517 leaves_play self
    if 1830 stage 1.0
    if 1831 stage 2.0
    do 1827 own give_keyword self
    do 4517 uses_keyword obliterate self
    do 1828 own stage_advance self
    do 1829 own give_keyword position enemy all turns=2.0
    do 4514 uses_keyword damage unit random board position is same_row of self amount=3.0;spread=1.0
    do 1830 own damage unit enemy chosen board amount=5.0
    do 1831 own create
    do 1831 own play_card card mine chosen hand card is 756272
    do 4517 has_keyword obliterate self
  Hammond:
    when 2942 played self
    when 4526 turn_end
    if 2942 amount_sum
    if 2942 amount_count unit all board position is sides of self;type is 60
    do 2942 own move unit enemy chosen board
    do 2942 own give_keyword unit enemy it board amount=sum
    do 4526 uses_keyword damage unit enemy it board amount=1.0

## C92 vv_8.md 22 (MISSED PARTLY, CONFLICT n545, 0 table lines from the same code)
Mahakam Pass makes a Treant-type card that Naiad Pondkeeper's own text uses (L3 making links to a card that waits for it), but armor for Naiad Fledgling is L18: more health links only to Taunt units and cards that wait to survive damage.
- W gwent: Mahakam Pass -> Naiad Pondkeeper: NONE | network.py [] | cases n546 line
- R gwent: Mahakam Pass -> Naiad Fledgling: NONE | network.py [] | cases n545 line
  Mahakam Pass:
    when 4277 always
    when 4541 round_end
    when 4278 played self
    when 4532 damaged self
    when 4279 activated self
    when 4541 round_end
    when 4504 played self
    if 4532 amount_listed
    do 4277 own give_keyword self
    do 4541 uses_keyword cant self event=leaves_play
    do 4541 uses_keyword remove_keyword self
    do 4278 own create card mine random region is Scoiatael;type is 39
    do 4278 own give_keyword card mine it type is 39 amount=4.0
    do 4532 uses_keyword negate_damage card mine it type is 39 amount=listed
    do 4279 own create
    do 4279 own play_card card mine it card is 757004
    do 4541 has_keyword cant self event=leaves_play
    do 4541 has_keyword remove_keyword self
    do 4504 has_keyword cant self event=activated;turns=1.0
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

## C93 vv_8.md 23 (MISSED PARTLY, CONFLICT n547,n553,n554,n555,n559,n560, 0 table lines from the same code)
Pro-line examples are weak units or strikes for Revenant and Vincent Meis (L2, L11), but boost to a unit is L14 and L18: help aimed at any unit links only to a card whose own text uses it, and more health links only to Taunt units and cards that wait to survive damage.
- W gwent: Poor Fucking Infantry -> Kaedweni Revenant: NONE | network.py [] | cases n548 line
- W gwent: Redanian Secret Service -> Kaedweni Revenant: NONE | network.py [] | cases n551 line
- W gwent: Kaedweni Revenant -> Vincent Meis: NONE | network.py [] | cases n557 line
- W gwent: Redanian Archer -> Vincent Meis: NONE | network.py [] | cases n558 line
- W gwent: Vernon Roche -> Kaedweni Revenant: NONE | network.py [] | cases n564 line
- R gwent: Kerack Marine -> Kaedweni Revenant: NONE | network.py [] | cases n547 line
- R gwent: Drakenborg -> Vincent Meis: NONE | network.py [] | cases n553 line
- R gwent: Drakenborg -> Margarita Laux-Antille: NONE | network.py [] | cases n554 line
- R gwent: Drakenborg -> Botchling: NONE | network.py [] | cases n555 line
- R gwent: Voymir -> Kaedweni Revenant: NONE | network.py [] | cases n559 line
- R gwent: Voymir -> Redanian Archer: gives it Armor for its effect | network.py [] | cases n560 line
  Poor Fucking Infantry:
    when 2396 played self
    when 2397 played self
    if 2397 keyword_condition
    if have is unit mine board state is copy_of_it
    if 2397 have is unit mine board state is copy_of_it
    do 2396 own summon
    do 2396 own summon
    do 2397 own stat_change self strength=3.0
  Kaedweni Revenant:
    when 2487 activated self
    when 2488 killed
    when 4504 played self
    do 2487 own damage unit chosen board amount=1.0
    do 2488 own copy self
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

## C94 vv_8.md 27 (MISSED PARTLY, CONFLICT n570, 0 table lines from the same code)
Joachim de Wett -> Coup de Grâce is a case combo no rule forbids, but Battle Stations! plays any bronze and Impera Enforcers have no summon trigger (L17).
- W gwent: Joachim de Wett -> Coup de Grâce: has Spying | network.py [] | cases n574 line
- R gwent: Battle Stations! -> Impera Enforcers: NONE | network.py [] | cases n570 line

