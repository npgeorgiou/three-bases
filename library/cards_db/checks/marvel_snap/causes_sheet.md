## vv_marvel_snap_1.md 2 (REAL, open, 11013 table lines from the same code)
Jane Foster only lowers enemy power and the Grand Design and Venus buff units on the board, none of which feeds Fin Fang Foom's or Zombie Giant-Man's own power read, so more power is generic here (L18, L14).
- W marvel_snap: Jane Foster Fractured Frontier -> Fin Fang Foom: more power | network.py [2041]
- W marvel_snap: The Grand Design -> Zombie Giant-Man: more power | network.py [2041]
- W marvel_snap: Venus -> Zombie Giant-Man: more power | network.py [2041]
- R marvel_snap: Zombie Mister Fantastic -> Zombie Giant-Man: more power | network.py [2041]
- R marvel_snap: Excalibur -> Iron Man: more power | network.py [2041]
  Jane Foster Fractured Frontier:
    when 2972 played self
    when 2973 played self
    if 2973 keyword_condition
    if event_count ge 1.0
    if 2973 event_count ge 1.0
    do 2972 own stat_change unit mine random board card not 8000282 power=1.0
    do 2972 own stat_change unit enemy random board power=-1.0
    do 2973 own stat_change unit mine random board card not 8000282 power=1.0
    do 2973 own stat_change unit enemy random board power=-1.0
  Fin Fang Foom:
    when 2889 played self
    if 2889 amount_stat power unit enemy chosen board position is same_lane;position is front_of_lane
    do 2889 own stat_change self power=stat
  The Grand Design:
    when 3315 always
    when 3316 played self
    if 3315 amount_event_count
    if 3315 amount_minus
    do 3315 own cost_change self cost=minus
    do 3316 own stat_change unit mine chosen board position not same_lane power=5.0
  Zombie Giant-Man:
    when 3401 played self
    if 3401 amount_stat power card mine card is 8000742
    do 3401 own stat_change card mine card is 8000742 power=2.0
    do 3401 own stat_change self power=stat
  Venus:
    when 3352 stat_changed unit mine
    if 3352 it_matches state is buffed
    do 3352 own stat_change unit mine it power=1.0

## vv_marvel_snap_1.md 2 (REAL, open, 2602 table lines from the same code)
Acid Arrow's On Reveal only donates itself to the enemy, so repeating or replaying it is a drawback, not help (L5).
- W marvel_snap: Astral Projection -> Acid Arrow: repeats its effects; also repeats its On Reveal effects | network.py [1361]
- W marvel_snap: Toxin -> Acid Arrow: returns it to hand: its Play or summon effect goes off again (when in its lane) | network.py [1405]
- R marvel_snap: Beast -> Absorbing Man: returns it to hand: its Play or summon effect goes off again (when in its lane) | network.py [1405]
- R marvel_snap: Ultron Mind Stone -> Absorbing Man: plays it again | network.py [2314]
  Astral Projection:
    when 2761 played self
    do 2761 own repeat card mine chosen hand keyword is 8000750
  Acid Arrow:
    when 2726 played self
    do 2726 own donate self
  Toxin:
    when 3331 played self
    if 3331 amount_count it
    if 3331 amount_product
    do 3331 own return_to_hand unit mine all board position is same_lane;card not 8000669
    do 3331 own stat_change self power=product

## vv_marvel_snap_1.md 3 (REAL, open, 2246 table lines from the same code)
Repeating Ongoing or protecting cost 1 units is help aimed at a kind, and J. Jonah Jameson and Broodling have no rows that use it (L14).
- W marvel_snap: Onslaught -> J. Jonah Jameson: repeats its effects | network.py [1361]
- W marvel_snap: Caiera -> Broodling: keeps it from dying | network.py [1396]
- R marvel_snap: Joaquin Torres Falcon II -> Electro: repeats its On Reveal effects | network.py []
  Onslaught:
    when 3122 always
    do 3122 own repeat unit mine all board position is same_lane;keyword is 8000751;card not 8000433
  J. Jonah Jameson:
  Caiera:
    when 2794 always
    do 2794 own cant unit mine all board cost in 1;cost in 6 event=dies
  Broodling:

## vv_marvel_snap_1.md 8 (REAL, open, 440 table lines from the same code)
Making random or any-kind cards is one more card of any kind, so it is no line to Angela or Agony (which need units played in a lane), and Agent 13 does not put cards into the deck that King Eitri draws (L19, L1b).
- W marvel_snap: Arishem -> Angela: makes more cards to play | network.py [1703]
- W marvel_snap: Agamotto -> Agony: makes more cards to play | network.py [1703]
- W marvel_snap: Agent 13 -> King Eitri: creates cards | network.py []
- R marvel_snap: Agent 13 -> Devil Dinosaur: fills your hand | network.py [2031]
  Arishem:
    when 2754 game_start
    when 2755 round_start
    if 2755 event_count eq 3.0
    do 2754 own create card mine random state is new amount=12.0
    do 2755 own max_mana_change mana mine amount=1.0
  Angela:
    when 2743 played unit mine position is same_lane
    do 2743 own stat_change self power=1.0
  Agamotto:
    when 2731 game_start
    do 2731 own create card card in 8000575;card in 8000577;card in 8000579;card in 8000581 amount=4.0
  Agony:
    when 2737 played unit mine position is same_lane
    do 2737 own merge self
  Agent 13:
    when 2734 played self
    do 2734 own create card mine random
  King Eitri:
    when 3003 activated self
    do 3003 own draw card mine chosen deck state is created

## vv_marvel_snap_1.md 1 (PARTLY, open, 0 table lines from the same code)
Arana buffs and moves units I play and Kid Omega kills them, so those links to Lancelot, Bucky Barnes and Elixir are real, but Arana does not activate other cards, so the Magus link is wrong (L14, L1).
- W marvel_snap: Araña -> Magus: makes this happen: activated | network.py []
- R marvel_snap: Araña -> Lancelot: changes your units' stats; also makes stronger: does what it waits for or counts (stat changed) when it comes | network.py [2314]
- R marvel_snap: Kid Omega -> Bucky Barnes: kills it for its death effect | network.py []
- R marvel_snap: Kid Omega -> Elixir: makes your units die: Elixir brings them back | network.py []
- R marvel_snap: Jocasta -> Awesome Andy: makes this happen: activated | network.py []
- R marvel_snap: Attuma -> Death Fractured Frontier: makes your units die: Death Fractured Frontier brings them back | network.py []
  Araña:
    when 2750 activated self
    when 2751 played unit mine
    do 2750 own give_ability self
    do 2751 gives stat_change unit mine it power=1.0
    do 2751 gives move unit mine it
  Magus:
    when 3041 activated
    do 3041 own copy_text self

## vv_marvel_snap_1.md 5 (REAL, open, 0 table lines from the same code)
Moving a unit into a lane is not what Danger, Drax, Moonstone or Pizza Slice need, a unit that moves gives no line to cards that act in their lane (L14, L23, L9).
- W marvel_snap: Doctor Strange -> Danger: Doctor Strange moves Danger, and Danger acts on units in its lane | network.py [1405]
- W marvel_snap: Ghost-Spider -> Drax: Ghost-Spider moves Drax, and Drax acts on units in its lane | network.py []
- W marvel_snap: Blink -> Moonstone: Blink moves units, and Moonstone acts on units in its lane | network.py []
- W marvel_snap: Doctor Octopus -> Pizza Slice: Doctor Octopus moves units, and Pizza Slice acts on units in its lane | network.py []
- R marvel_snap: Angel -> Hydra Stomper: makes your units move | network.py []
  Doctor Strange:
    when 2841 played self
    do 2841 own move unit mine highest board
  Danger:
    when 2825 activated self
    do 2825 own kill unit enemy chosen board position is same_lane;power lt 3004
  Ghost-Spider:
    when 2911 played self
    if 2911 last_card unit mine board
    do 2911 own move unit mine it board
  Drax:
    when 2855 played self
    if 2855 event_count ge 1.0
    do 2855 own stat_change self power=4.0
  Blink:
    when 2783 played self
    if 2783 last_card unit mine
    do 2783 own swap unit mine it board
  Moonstone:
    when 3083 always
    do 3083 own copy_text self
  Doctor Octopus:
    when 2839 played self
    do 2839 own move card enemy lowest hand
  Pizza Slice:
    when 3131 played self
    do 3131 own merge self

## vv_marvel_snap_1.md 6 (REAL, open, 0 table lines from the same code)
Wiccan wants no unspent mana and Galactus wants to be alone in the lane, so gaining mana and moving units give the opposite of what they want (L21, L5).
- W marvel_snap: Herbie Program 01 -> Wiccan: lets you gain mana | network.py []
- W marvel_snap: Ghost-Spider -> Galactus: Ghost-Spider moves your units, and Galactus acts on units in its lane | network.py []
- R marvel_snap: Djinn -> Jim Hammond Human Torch: lets you gain mana | network.py []
  Herbie Program 01:
    when 3139 activated self
    do 3139 own mana_gain mana mine amount=2.0
  Wiccan:
    when 3375 played self
    if 3375 count eq 0.0 mana mine state not spent
    do 3375 own max_mana_change mana mine amount=2.0
  Ghost-Spider:
    when 2911 played self
    if 2911 last_card unit mine board
    do 2911 own move unit mine it board
  Galactus:
    when 2901 played self
    if 2901 amount gt stat
    if 2901 count eq 1.0 unit mine board position is same_lane
    if 2901 amount_stat power position enemy position is same_lane
    if 2901 amount_stat power position mine position is same_lane
    do 2901 own kill position all position not same_lane

## vv_marvel_snap_1.md 7 (REAL, open, 0 table lines from the same code)
Effects on the enemy side (their created cards cost more, their cards or units moved) are credited to my need, and my created cards are not the enemy cards Gorgon changes (L9, L5).
- W marvel_snap: Beta Ray Bill -> Gorgon: creates cards | network.py []
- W marvel_snap: Doctor Octopus -> Dagger: Doctor Octopus moves enemy units, and Dagger acts on units in its lane | network.py []
- W marvel_snap: Aero -> Armor: Aero moves units, and Armor acts on units in its lane | network.py []
- R marvel_snap: Moira X -> Quinjet: creates cards | network.py []
  Beta Ray Bill:
    when 2774 played self
    do 2774 own create
  Gorgon:
    when 2919 always
    do 2919 own cost_change card enemy all everywhere state is created cost=1.0;max=6.0
  Doctor Octopus:
    when 2839 played self
    do 2839 own move card enemy lowest hand
  Dagger:
    when 2823 moves self
    if 2823 amount_product
    if 2823 amount_count unit enemy all board position is same_lane
    do 2823 own stat_change self power=product
  Aero:
    when 2730 played self
    if 2730 last_card unit enemy
    do 2730 own move unit enemy it board
  Armor:
    when 2756 always
    do 2756 own cant unit all board position is same_lane event=dies

## vv_marvel_snap_1.md 9 (REAL, open, 0 table lines from the same code)
Agent Venom sets deck cards to power 3, which is not buffed and cannot reach the 6 power Wolverine Horseman of War needs (L4, L18).
- W marvel_snap: Agent Venom -> Wolverine Horseman of War: changes its stats for its effect | network.py []
- W marvel_snap: Agent Venom -> Elder Dragon of the Moon: changes your units' stats | network.py []
- W marvel_snap: Agent Venom -> Gilgamesh: changes your units' stats | network.py []
- R marvel_snap: America Chavez -> Ares: more power | network.py [2041]
  Agent Venom:
    when 2736 played self
    do 2736 own stat_set card mine all deck power=3.0
  Wolverine Horseman of War:
    when 3385 round_end
    if 3385 stat power ge 6.0 self
    do 3385 own stat_change unit mine chosen board power=4.0
  Elder Dragon of the Moon:
    when 2862 always
    if 2862 amount_count unit mine all board state is buffed
    if 2862 amount_minus
    do 2862 own cost_change self cost=minus
  Gilgamesh:
    when 2914 played self
    if 2914 amount_count unit mine all board state is buffed;card not 8000218
    do 2914 own stat_change self power=count

## vv_marvel_snap_1.md 1 (MISSED REAL, open, 0 table lines from the same code)
Mystique needs the last card played to be an Ongoing unit, and Ongoing is a minority kind, so a deck choice that keeps its line like Onslaught -> Blue Marvel (L1b, L10).
- W marvel_snap: Sera -> Mystique: NONE | network.py []
- W marvel_snap: Mojo -> Mystique: NONE | network.py []
- W marvel_snap: Ant Man -> Mystique: NONE | network.py []
- W marvel_snap: Patriot -> Mystique: NONE | network.py []
- R marvel_snap: Wong -> Mystique: plays it again | network.py [2314]
- R marvel_snap: Onslaught -> Blue Marvel: repeats its effects | network.py [1361]
  Sera:
    when 3206 always
    do 3206 own cost_change card mine all hand cost=-1.0;min=1.0
  Mystique:
    when 3100 played self
    if 3100 last_card unit mine keyword is 8000751
    do 3100 own copy_text self
  Mojo:
    when 3077 always
    if 3077 count ge 4.0 unit mine board position is same_lane
    if 3077 count ge 4.0 unit enemy board position is same_lane
    do 3077 own stat_change self power=6.0
  Ant Man:
    when 2745 always
    if 2745 count ge 4.0 unit mine board position is same_lane
    do 2745 own stat_change self power=4.0
  Patriot:
    when 3126 always
    do 3126 own stat_change unit mine all board state is no_abilities power=2.0

## vv_marvel_snap_1.md 2 (MISSED REAL, open, 0 table lines from the same code)
Black Panther doubles his own power, so power added to cards in hand or deck is a setup, the same as "The Dreadway -> Decimate is a combo that works" (L18, L24).
- W marvel_snap: Okoye -> Black Panther: NONE | network.py []
- W marvel_snap: Nakia -> Black Panther: NONE | network.py []
- R marvel_snap: Wong -> Black Panther: plays it again | network.py [2314]
- R marvel_snap: Odin -> Black Panther: repeats its effects; also repeats its On Reveal effects | network.py [1361]
  Okoye:
    when 3118 played self
    do 3118 own stat_change card mine all deck power=1.0
  Black Panther:
    when 2779 played self
    if 2779 amount_stat power self
    do 2779 own stat_change self power=stat
  Nakia:
    when 3101 played self
    do 3101 own stat_change card mine all hand power=1.0

## vv_marvel_snap_1.md 2 (MISSED REAL, open, 0 table lines from the same code)
Galactus kills units in the other lanes, which makes units die for Knull's power and Death's cost, the same as Destroyer (L10).
- W marvel_snap: Galactus -> Knull: NONE | network.py []
- W marvel_snap: Galactus -> Death: NONE | network.py []
- R marvel_snap: Destroyer -> Knull: makes units die | network.py []
- R marvel_snap: Destroyer -> Death: makes units die | network.py []
  Galactus:
    when 2901 played self
    if 2901 amount gt stat
    if 2901 count eq 1.0 unit mine board position is same_lane
    if 2901 amount_stat power position enemy position is same_lane
    if 2901 amount_stat power position mine position is same_lane
    do 2901 own kill position all position not same_lane
  Knull:
    when 3010 always
    if 3010 amount_event_count power
    do 3010 own stat_change self power=event_count
  Death:
    when 2831 always
    if 2831 amount_event_count
    if 2831 amount_minus
    do 2831 own cost_change self cost=minus

## vv_marvel_snap_2.md 3 (MISSED REAL, open, 0 table lines from the same code)
Hela's text counts the distinct costs in her discard pile and revives from it, so cards that discard fill what she reads (L17, L10 enables).
- W marvel_snap: Lady Sif -> Hela: NONE | network.py []
- W marvel_snap: M.O.D.O.K. -> Hela: NONE | network.py []
- W marvel_snap: Black Cat -> Hela: NONE | network.py []
  Lady Sif:
    when 3018 played self
    do 3018 own discard card mine highest_cost hand
  Hela:
    when 2931 played self
    if 2931 amount_distinct cost card mine all discard
    do 2931 own revive unit mine chosen discard
  M.O.D.O.K.:
    when 3075 played self
    do 3075 own discard card mine all hand
  Black Cat:
    when 2777 round_end
    do 2777 own discard self

## vv_marvel_snap_2.md 4 (MISSED REAL, open, 0 table lines from the same code)
Mystique's own text needs the last card played to be an Ongoing unit, and Ongoing is a minority kind, so an Ongoing card is a real deck choice for her (L15, L21, L10 enables).
- W marvel_snap: Victoria Hand -> Mystique: NONE | network.py []
- W marvel_snap: Devil Dinosaur -> Mystique: NONE | network.py []
- W marvel_snap: PymParticle Arrow -> Mystique: NONE | network.py []
- W marvel_snap: Sera -> Mystique: NONE | network.py []
- R marvel_snap: Basic Arrow -> Mystique: makes your units get Ongoing | network.py []
  Victoria Hand:
    when 3355 always
    do 3355 own stat_change unit mine all board state is created power=2.0
  Mystique:
    when 3100 played self
    if 3100 last_card unit mine keyword is 8000751
    do 3100 own copy_text self
  Devil Dinosaur:
    when 2836 always
    if 2836 amount_product
    if 2836 amount_count card mine all hand
    do 2836 own stat_change self power=product
  PymParticle Arrow:
    when 3152 always
    if 3152 count ge 4.0 unit mine board position is same_lane
    do 3152 own stat_change self power=3.0
  Sera:
    when 3206 always
    do 3206 own cost_change card mine all hand cost=-1.0;min=1.0

## vv_marvel_snap_2.md 7 (REAL, open, 0 table lines from the same code)
Fantomex does not make anything activate, a shared Activate keyword is no line, but Zombie Captain Marvel's kills feed Fantomex's count (L15, L1).
- W marvel_snap: Fantomex -> Zombie Captain Marvel: makes this happen: activated | network.py []
- R marvel_snap: Zombie Captain Marvel -> Fantomex: makes your units die | network.py []
  Fantomex:
    when 2886 activated self
    if 2886 event_count ge 1.0
    if 2886 event_count ge 1.0
    do 2886 own stat_change unit enemy all board position is front_of_lane power=-2.0
  Zombie Captain Marvel:
    when 3398 activated
    if 3398 amount_product
    if 3398 amount_count unit mine all board position is same_lane;card not 8000739
    do 3398 own kill unit mine all board position is same_lane;card not 8000739
    do 3398 own stat_change self power=product
    do 3398 own move self

## vv_marvel_snap_2.md 8 (REAL, open, 0 table lines from the same code)
Galactus needs exactly one of my units in his lane and his rows read no move, so moving units into the lane is help for any card of a kind, not the very thing needed (L4, L14).
- W marvel_snap: Grapple Arrow -> Galactus: Grapple Arrow moves your units, and Galactus acts on units in its lane | network.py []
- R marvel_snap: Grapple Arrow -> PymParticle Arrow: Grapple Arrow moves your units, and PymParticle Arrow acts on units in its lane | network.py []
  Grapple Arrow:
    when 2922 played unit mine
    do 2922 own move unit mine it
  Galactus:
    when 2901 played self
    if 2901 amount gt stat
    if 2901 count eq 1.0 unit mine board position is same_lane
    if 2901 amount_stat power position enemy position is same_lane
    if 2901 amount_stat power position mine position is same_lane
    do 2901 own kill position all position not same_lane

## vv_marvel_snap_2.md 1 (REAL, open, 0 table lines from the same code)
King Eitri draws created cards only from the deck, and these cards create into the hand, so nothing is there for him to draw (L10 enables, L19).
- W marvel_snap: Iron Patriot -> King Eitri: creates cards | network.py []
- W marvel_snap: Scarlet Witch Queen of Chaos -> King Eitri: creates cards | network.py []
- W marvel_snap: Valentina -> King Eitri: creates cards | network.py []
- R marvel_snap: Shadowlands Daredevil -> King Eitri: creates cards | network.py []
  Iron Patriot:
    when 2966 played self
    when 2967 round_end
    if 2967 amount gt stat
    if 2967 amount_stat power position enemy position is same_lane
    if 2967 amount_stat power position mine position is same_lane
    do 2966 own create card mine random cost ge 3162
    do 2967 own cost_change card mine it hand cost=-3.0
  King Eitri:
    when 3003 activated self
    do 3003 own draw card mine chosen deck state is created
  Scarlet Witch Queen of Chaos:
    when 3195 round_start
    do 3195 own create spell mine random
    do 3195 own cost_set spell mine it cost=0.0
  Valentina:
    when 3344 played self
    do 3344 own create card random cost eq 3581
    do 3344 own cost_change card it cost=-2.0
    do 3344 own stat_change card it power=-2.0

## vv_marvel_snap_2.md 4 (MISSED REAL, open, 0 table lines from the same code)
Zombie Giant-Man's text reads the power of the Zombie Horde card, so more power for that card feeds him, as Zombie Mister Fantastic already does (L18).
- W marvel_snap: The Hunger -> Zombie Giant-Man: NONE | network.py []
- W marvel_snap: Zombie Scarlet Witch -> Zombie Giant-Man: NONE | network.py []
  The Hunger:
    when 3317 played self
    do 3317 own stat_change card mine card is 8000742 power=3.0
  Zombie Giant-Man:
    when 3401 played self
    if 3401 amount_stat power card mine card is 8000742
    do 3401 own stat_change card mine card is 8000742 power=2.0
    do 3401 own stat_change self power=stat
  Zombie Scarlet Witch:
    when 3407 played unit mine position is same_lane
    do 3407 own stat_change card mine card is 8000742 power=2.0

## vv_marvel_snap_2.md 5 (MISSED REAL, open, 0 table lines from the same code)
SP//dr merges itself onto a unit and Peni Parker and Man-Spider wait for a merge, the same trigger Symbiote Spider-Man already has lines for (L10 triggers).
- W marvel_snap: SP//dr -> Peni Parker: NONE | network.py []
- W marvel_snap: SP//dr -> Man-Spider: NONE | network.py []
  SP//dr:
    when 3182 played self
    do 3182 own merge self
    do 3182 own can it event=moves
  Peni Parker:
    when 3127 played self
    when 3128 merged
    do 3127 own create
    do 3128 own mana_gain mana mine amount=1.0
  Man-Spider:
    when 3046 played self
    when 3047 merged
    if 3046 last_card unit mine
    if 3047 amount_stat power self
    do 3046 own merge unit mine it
    do 3047 own stat_change self power=stat

## vv_marvel_snap_2.md 6 (REAL, open, 0 table lines from the same code)
Super-Skrull gives Ongoing, not On Reveal, so Astral Projection gets nothing, and Cosmo silences On Reveal units so units given On Reveal work against him (L20, L9, L10).
- W marvel_snap: Super-Skrull -> Astral Projection: makes your units get On Reveal | network.py []
- W marvel_snap: High Evolutionary -> Cosmo: makes units get On Reveal | network.py []
  Super-Skrull:
    when 3289 always
    do 3289 own copy_keywords self
  Astral Projection:
    when 2761 played self
    do 2761 own repeat card mine chosen hand keyword is 8000750
  High Evolutionary:
    when 2938 game_start
    do 2938 own give_ability card mine all everywhere state is no_abilities
  Cosmo:
    when 2818 always
    do 2818 own silence unit all board position is same_lane;keyword is 8000750

## vv_marvel_snap_2.md 1 (REAL, open, 0 table lines from the same code)
Invisible Woman's rows read no move, so Grand Master moving my units is help for any card of a kind (L14, L16).
- W marvel_snap: Grand Master -> Invisible Woman: Grand Master moves your units, and Invisible Woman acts on units in its lane | network.py []
- R marvel_snap: Wong -> Shuri: plays it again | network.py [2314]
  Grand Master:
    when 2921 played self
    do 2921 own move unit mine chosen board position is same_lane;keyword is 8000750;card not 8000225
    do 2921 own repeat unit mine it card not 8000225
  Invisible Woman:
    when 2959 always
    do 2959 own cant unit mine all board position is same_lane event=played

