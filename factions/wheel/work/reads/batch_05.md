# Tag reading, batch 05


## Family: concept `mark_target` ("Mark a target for later hits"), from rows `do mark`
- Counts as mark_target: A target is marked so that later effects or attacks hit it harder.
- Not mark_target: A lasting stat loss is stat_loss.
- Why the script suspects it: hurts me: acts on my own side

### Card 757264 (gwent), tagged from: row | do mark | unit/mine/chosen | board | played(self) | own

**Megascope**
Card text: "Deploy: Choose a bronze allied unit. Timer 2: Spawn a base copy of chosen unit to the right of Megascope."

Keywords (their own rows are on the keyword entries): Timer, Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | mark | chosen mine unit in board [state is bronze] |  |  |  | permanent |
| always |  |  | give_keyword | self |  | Timer | amount=2 | permanent |
| countdown_done of self |  |  | copy | mine unit in board [state is marked] [state is created] to right_of_self mine position | board |  |  |  |


Keyword entry:
**Timer**
Card text: "Before the end of your turn, lower the number by 1. When the number reaches 0, trigger the ability."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_end by mine player |  |  | countdown_advance | self |  |  | amount=1 |  |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)


### Card 8000539 (marvel_snap), tagged from: row | do mark | card/mine/top | deck | game_start | own

**Sinister Six**
Card text: "Game Start: The first 6 characters you draw are EVIL! After you play them all, merge them into this and add this to the last one's location. (0/6)"

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| game_start |  |  | mark | 6 top mine card in deck |  |  |  | permanent |
| played of mine unit in board [state is marked] | event_count played of mine unit in board [state is marked] ge 6 this_game |  | merge | all mine unit in board [state is marked] to self |  |  |  |  |
| played of mine unit in board [state is marked] | event_count played of mine unit in board [state is marked] ge 6 this_game | then | summon | self to position [position is same_lane] |  |  |  |  |


### Card 796933 (runeterra), tagged from: row | do mark | unit/mine/chosen | board | played(self) | own

**Ram Stance**
Card text: "Keywords: Slow. Pick an ally. Deal 1 to EVERYTHING else."

Keywords (their own rows are on the keyword entries): Slow

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | mark | chosen mine unit in board |  |  |  | this_round |
| played of self |  | then | damage | all any [state not marked] |  |  | amount=1 |  |


Keyword entry:
**Slow**
Card text: "Can be played outside of combat when no spells or skills are pending. Happens after your opponent has a chance to react."

(no rows of its own)


### Card 1000083 (stormbound), tagged from: row | do mark | unit_or_structure/mine/all | board | turn_end | own

**Temple of Time**
Card text: "At the end of your turn, remember the state of surrounding friendly units and structures. At the start of your turn, restore 1/2/2/3/3 of them"

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_end by mine player |  |  | mark | all mine unit_or_structure in board [position is surrounding] |  |  |  | permanent |
| turn_start by mine player |  |  | heal | per_level (1 + 2 + 2 + 3 + 3) chosen mine unit_or_structure in board [state is marked] |  |  | amount=full |  |


### Card 8000201 (marvel_snap), tagged from: row | do mark | unit/mine/it | - | played | own

**Galactus First Steps**
Card text: "My Herald is the next character I see you play. End of Turn: +2 Power if you're winning my Herald's location. (if in hand or in play)"

Keywords (their own rows are on the keyword entries): End of Turn

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of mine unit in board [next_time] |  |  | mark | it |  |  |  | permanent |
| round_end | amount stat power of (mine position [position is same_lane]) gt stat power of (enemy position [position is same_lane]) |  | stat_change | self |  |  | power=2 | permanent |


Keyword entry:
**End of Turn**
Card text: "Acts at the end of every turn while the card is on the board."

(no rows of its own)



## Family: concept `movement` ("Move my units (reposition)"), from rows `do can`
- Counts as movement: The owner moves their own unit to another space, row, lane or location.
- Not movement: Moving enemy units is forced_movement.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 5000473 (duelyst), tagged from: row | do can | unit/enemy/it | - | always | uses_keyword Flying

**Unleash the Evil**
Card text: "Summon a copy of the minion your opponent most recently summoned from their action bar. It gains Rush and Flying."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | copy | top enemy unit in board [state is from_hand] | board |  |  |  |
| played of self |  | and | give_keyword | it |  | Rush |  | permanent |
| played of self |  | and | give_keyword | it |  | Flying |  | permanent |


Keyword entry:
**Rush**
Card text: "Can move and attack immediately."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | can | self |  |  | event=moves | this_round |
| played of self |  | and | can | self |  |  | event=attacks | this_round |


Keyword entry:
**Flying**
Card text: "Move anywhere on the battlefield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | self to position |  |  | event=moves | while |



## Family: concept `movement` ("Move my units (reposition)"), from rows `do move`
- Counts as movement: The owner moves their own unit to another space, row, lane or location.
- Not movement: Moving enemy units is forced_movement.
- Why the script suspects it: helps the enemy: puts it on the enemy side

### Card 756544 (gwent), tagged from: rule movement | do move | unit/-/all to enemy | board | played(self) | own

**Nivellen**
Card text: "Deploy: Move all units on an enemy row to the other row."

Keywords (their own rows are on the keyword entries): Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | move | all unit in board [position is same_row] to enemy position [position not same_row] |  |  |  |  |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)


### Card 1000105 (stormbound), tagged from: rule movement | do move | -/-/self to enemy | - | played(self) | own

**Eloth the Ignited**
Card text: "On play, fly to the first enemy unit in front, push it away and deal 2/3/4/5/6 damage, then move forward if it died"

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | move | self to enemy unit in board [position is first_in_front] |  |  |  |  |
| played of self |  | then | move | enemy unit in board [position is in_front] |  | Push |  |  |
| played of self |  | then | damage | enemy unit in board [position is in_front] |  |  | amount=per_level (2 + 3 + 4 + 5 + 6) |  |
| played of self |  | if_done | move | self to position [position is in_front] |  |  |  |  |


Keyword entry:
**Push**
Card text: "Moves a unit along a row or column until it reaches the edge of the board or another unit or structure; a unit cannot be pushed into a base."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | move | it |  |  |  |  |


### Card 757476 (gwent), tagged from: row | do move | unit/mine/it to enemy | - | played(self) | own

**Henry var Attre**
Card text: "Deploy: If your opponent has not passed and their hand is not full, Create a legendary unit from your faction that was not in your starting deck, add it to your opponent's hand, move the rest to the bottom of your opponent's deck, then Create a legendary unit from your opponent's faction that was not in their starting deck, add it to your hand, put the rest on the bottom of your deck."

Keywords (their own rows are on the keyword entries): Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self | have enemy player [state is passed] not; have enemy card in hand [state is full] not |  | create | random mine unit [state not started_in_deck] [region is own_regions] [state is gold] | hand |  |  |  |
| played of self | have enemy player [state is passed] not; have enemy card in hand [state is full] not | then | move | it to enemy card in hand |  |  |  |  |
| played of self | have enemy player [state is passed] not; have enemy card in hand [state is full] not | then | move | all mine card [state is created] | deck_bottom |  |  |  |
| played of self | have enemy player [state is passed] not; have enemy card in hand [state is full] not | then | create | random mine unit [state not started_in_deck] [state is opponent_faction] [state is gold] | hand |  |  |  |
| played of self | have enemy player [state is passed] not; have enemy card in hand [state is full] not | then | move | it to mine card in hand |  |  |  |  |
| played of self | have enemy player [state is passed] not; have enemy card in hand [state is full] not | then | move | all enemy card [state is created] | deck_bottom |  |  |  |
| played of self | have enemy player [state is passed] not; have enemy card in hand [state is full] not |  | create | random mine unit [state not started_in_deck] [region is own_regions] [state is gold] | hand |  |  |  |
| played of self | have enemy player [state is passed] not; have enemy card in hand [state is full] not | then | move | it to enemy card in hand |  |  |  |  |
| played of self | have enemy player [state is passed] not; have enemy card in hand [state is full] not | then | move | all mine card [state is created] | deck_bottom |  |  |  |
| played of self | have enemy player [state is passed] not; have enemy card in hand [state is full] not | then | create | random mine unit [state not started_in_deck] [state is opponent_faction] [state is gold] | hand |  |  |  |
| played of self | have enemy player [state is passed] not; have enemy card in hand [state is full] not | then | move | it to mine card in hand |  |  |  |  |
| played of self | have enemy player [state is passed] not; have enemy card in hand [state is full] not | then | move | all enemy card [state is created] | deck_bottom |  |  |  |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)



## Family: concept `on_ally_play` ("When I play another card"), from rows `when played`
- Counts as on_ally_play: Triggers when the owner plays or summons another card or unit.
- Not on_ally_play: When this card is played is on_play.
- Why the script suspects it: fires on the enemy's action

### Card 5000696 (duelyst), tagged from: row | when played | unit/enemy/- by enemy | - | played | own

**Soulstealer**
Card text: "Whenever the enemy General plays a minion, it becomes their new General. Whenever Soulstealer dies, he inhabits the body of one of his minions."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played by enemy player of enemy unit |  |  | become_leader | it |  |  |  |  |
| dies of self |  |  | transform | self to chosen mine unit in board |  |  |  |  |


### Card 756452 (gwent), tagged from: row | when played | unit/enemy/- by enemy | - | played | own

**An Craite Longship**
Card text: "Melee: Whenever your opponent plays a unit on their side of the battlefield, damage it by 1."

Keywords (their own rows are on the keyword entries): Melee

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played by enemy player of enemy unit | keyword_condition Melee |  | damage | it |  |  | amount=1 |  |


Keyword entry:
**Melee**
Card text: "This ability can only be used while on the melee row."

(no rows of its own)


### Card 796327 (marvel_snap), tagged from: row | when played | unit/enemy/- | - | played | own

**The Abbey**
Card text: "First to put exactly 2 cards here draws a card."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of mine unit [position is same_lane] [once_per_game] | count mine unit in board [position is same_lane] eq 2; count enemy unit in board [position is same_lane] lt 2 |  | draw | mine card in deck_top |  |  | amount=1 |  |
| played of enemy unit [position is same_lane] [once_per_game] | count enemy unit in board [position is same_lane] eq 2; count mine unit in board [position is same_lane] lt 2 |  | draw | enemy card in deck_top |  |  | amount=1 |  |


### Card 752050 (runeterra), tagged from: row | when played | unit/-/- by enemy | - | played | gives

**Capsize**
Card text: "Recall an enemy to increase the cost of the next unit your opponent plays this round by 2."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | keyword_action | chosen enemy unit in board |  | Recall |  | unstated |
| played of self |  | if_done | give_ability | mine player |  |  |  |  |


Keyword entry:
**Recall**
Card text: "Return a unit to hand and remove all effects applied to it."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | return_to_hand | it |  |  |  |  |
| activated |  | then | silence | it |  |  |  |  |


### Card 5000692 (duelyst), tagged from: row | when played | unit/enemy/- by enemy | - | played | own

**Andromeda**
Card text: "Keywords: Flying. Whenever the enemy General plays a minion, transform it into a random minion with the same mana cost."

Keywords (their own rows are on the keyword entries): Flying

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played by enemy player of enemy unit |  |  | transform | it to random unit in board [cost eq stat cost of (it)] |  |  |  |  |


Keyword entry:
**Flying**
Card text: "Move anywhere on the battlefield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | self to position |  |  | event=moves | while |



## Family: concept `on_ally_play` ("When I play another card"), from rows `when summoned`
- Counts as on_ally_play: Triggers when the owner plays or summons another card or unit.
- Not on_ally_play: When this card is played is on_play.
- Why the script suspects it: fires on the enemy's action

### Card 5000333 (duelyst), tagged from: row | when summoned | unit/enemy/- | - | summoned | own

**Crimson Oculus**
Card text: "Whenever opponent summons a minion, this minion gains +1/+1"

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of enemy unit |  |  | stat_change | self |  |  | power=1, health=1 | permanent |


### Card 741259 (faeria), tagged from: row | when summoned | unit/enemy/- | - | summoned | own

**Crumbling Golem**
Card text: "Whenever your opponent summons a creature, deal 1 damage to this."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of enemy unit |  |  | damage | self |  |  | amount=1 |  |


### Card 4000029 (inscryption), tagged from: row | when summoned | unit/enemy/- | - | summoned | has_keyword Guardian

**Bonehound**
Card text: "Keywords: Guardian."

Keywords (their own rows are on the keyword entries): Guardian

(no rows of its own)


Keyword entry:
**Guardian**
Card text: "Rulebook: When an opposing creature is placed opposite to an empty space, a card bearing this sigil will move to that empty space."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of enemy unit | have mine position [position is same_lane] [state is empty] is |  | move | self to position [position is same_lane] |  |  |  |  |


### Card 796835 (runeterra), tagged from: row | when summoned | unit/enemy/- | - | summoned | own

**Roiling Sands**
Card text: "Keywords: Landmark. When an enemy is summoned, destroy me to grant it Vulnerable."

Keywords (their own rows are on the keyword entries): Landmark

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of enemy unit |  |  | kill | self |  |  |  |  |
| summoned of enemy unit |  | then | give_keyword | it |  | Vulnerable |  | permanent |


Keyword entry:
**Landmark**
Card text: "Landmarks take up a space on the board. They can't attack, block, or take damage."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | cant | self |  |  | event=attacks | while |
| always |  | and | cant | self |  |  | event=blocks | while |
| always |  | and | cant | self |  |  | event=damaged | while |


Keyword entry:
**Vulnerable**
Card text: "The enemy can challenge this unit, forcing it to block."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | enemy player to self |  |  | event=challenges | while |


### Card 5000650 (duelyst), tagged from: row | when summoned | unit/enemy/- | - | summoned | own

**Malyk**
Card text: "Keywords: Ranged. Whenever your opponent summons a minion, they draw a card. Whenever your opponent overdraws, summon a 3/3 Ooz"

Keywords (their own rows are on the keyword entries): Ranged

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of enemy unit |  |  | draw | enemy card in deck_top |  |  | amount=1 |  |
| drawn of enemy card |  |  | summon |  |  | Ooz | power=3, health=3 |  |


Keyword entry:
**Ranged**
Card text: "Attack from anywhere on the battlefield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | self to position |  |  | event=attacks | while |


Card it names or makes:
**Ooz**
Card text: "Whenever this minion takes damage, turn a space occupied by an enemy into Shadow Creep."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| damaged of self |  |  | set_terrain | chosen position [position is same_space] to position [terrain is damage_space] |  | Shadow Creep |  |  |


