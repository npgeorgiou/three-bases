# Tag reading, batch 02


## Family: concept `buff` ("Make a unit stronger (buff)"), from rows `do give_keyword`
- Counts as buff: A unit gains stats or a combat ability it did not have: more power or health, first strike, flying, extra attacks, reach, piercing.
- Not buff: Improving a card still in hand is in_hand_buff; a unit printed with high stats is not buffed.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 7000758 (sts1), tagged from: row | do give_keyword | player/enemy/- | - | turn_start | own

**Orb**
Card text: "Actions: Beam (attack, 8 damage); Support Beam (defend, 12 block); Stasis (strong debuff)"

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_start by self |  |  | random_one |  |  |  |  |  |
| turn_start by self |  | or | damage | enemy player |  |  | amount=8 |  |
| turn_start by self |  | or | give_keyword | self |  | Block | amount=12 | permanent |
| turn_start by self |  | or | give_keyword | enemy player |  |  | amount=unstated | unstated |


Keyword entry:
**Block**
Card text: "Until next turn, prevents damage."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| damaged of self |  |  | negate_damage | self |  |  | amount=count of (self keyword [keyword is Block]) |  |
| damaged of self |  | then | remove_keyword | self |  | Block | amount=event_amount |  |
| turn_start by mine player |  |  | remove_keyword | self |  | Block |  |  |


### Card 7000792 (sts1), tagged from: row | do give_keyword | player/enemy/- | - | turn_start | own

**Spire Growth**
Card text: "Actions: Quick Tackle (attack, 16 damage); Constrict (strong debuff); Smash (attack, 22 damage)"

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_start by self |  |  | random_one |  |  |  |  |  |
| turn_start by self |  | or | damage | enemy player |  |  | amount=16 |  |
| turn_start by self |  | or | give_keyword | enemy player |  |  | amount=unstated | unstated |
| turn_start by self |  | or | damage | enemy player |  |  | amount=22 |  |


### Card 7000803 (sts1), tagged from: row | do give_keyword | player/enemy/- | - | turn_start | own

**Spike Slime (M)**
Card text: "Actions: Flame Tackle (attack debuff, 8 damage); Lick (debuff)"

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_start by self |  |  | random_one |  |  |  |  |  |
| turn_start by self |  | or | damage | enemy player |  |  | amount=8 |  |
| turn_start by self |  | and | give_keyword | enemy player |  |  | amount=unstated | unstated |
| turn_start by self |  | or | give_keyword | enemy player |  |  | amount=unstated | unstated |


### Card 7000811 (sts1), tagged from: row | do give_keyword | player/enemy/- | - | turn_start | own

**Writhing Mass**
Card text: "Actions: Big Hit (attack, 32 damage); Multi Hit (attack, 7 damage x3); Attack Block (attack defend, 15 damage); Attack Debuff (attack debuff, 10 damage); Mega Debuff (strong debuff)"

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_start by self |  |  | random_one |  |  |  |  |  |
| turn_start by self |  | or | damage | enemy player |  |  | amount=32 |  |
| turn_start by self |  | or | damage | enemy player |  |  | amount=7, times=3 |  |
| turn_start by self |  | or | damage | enemy player |  |  | amount=15 |  |
| turn_start by self |  | and | give_keyword | self |  | Block | amount=unstated | permanent |
| turn_start by self |  | or | damage | enemy player |  |  | amount=10 |  |
| turn_start by self |  | and | give_keyword | enemy player |  |  | amount=unstated | unstated |
| turn_start by self |  | or | give_keyword | enemy player |  |  | amount=unstated | unstated |


Keyword entry:
**Block**
Card text: "Until next turn, prevents damage."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| damaged of self |  |  | negate_damage | self |  |  | amount=count of (self keyword [keyword is Block]) |  |
| damaged of self |  | then | remove_keyword | self |  | Block | amount=event_amount |  |
| turn_start by mine player |  |  | remove_keyword | self |  | Block |  |  |


### Card 7000763 (sts1), tagged from: row | do give_keyword | player/enemy/- | - | turn_start | own

**Corrupt Heart**
Card text: "Actions: Blood Shots (attack, 2 damage x12); Echo Attack (attack, 40 damage); Debilitate (strong debuff); Gain One Strength (buff)"

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_start by self |  |  | random_one |  |  |  |  |  |
| turn_start by self |  | or | damage | enemy player |  |  | amount=2, times=12 |  |
| turn_start by self |  | or | damage | enemy player |  |  | amount=40 |  |
| turn_start by self |  | or | give_keyword | enemy player |  |  | amount=unstated | unstated |
| turn_start by self |  | or | give_keyword | self |  |  | amount=unstated | unstated |



## Family: concept `cheat_death` ("Cheat death (survive lethal)"), from rows `do copy`
- Counts as cheat_death: A unit that would die survives, or comes back in the same moment it dies.
- Not cheat_death: Bringing back a unit that died earlier is revive.
- Why the script suspects it: helps the enemy: puts it on the enemy side

### Card 751516 (runeterra), tagged from: rule cheat_death | do copy | -/-/self to enemy | deck | dies(self) | own

**Stinky Whump**
Card text: "Keywords: Last Breath. Last Breath: Create a copy of me in the enemy deck with 2 Poison Puffcaps attached."

Keywords (their own rows are on the keyword entries): Last Breath

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| dies of self |  |  | copy | self to enemy player | deck |  |  |  |
| dies of self |  | then | attach | it |  | Poison Puffcap | amount=2 |  |


Keyword entry:
**Last Breath**
Card text: "These abilities take effect when the unit dies."

(no rows of its own)


Card it names or makes:
**Poison Puffcap**
Card text: "Keywords: Trap. Deal 1 to your Nexus."

Keywords (their own rows are on the keyword entries): Trap

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | mine player |  |  | amount=1 |  |


### Card 751057 (runeterra), tagged from: rule cheat_death | do copy | -/-/self to enemy | deck | dies(self) | own

**Pesky Specter**
Card text: "Keywords: Ephemeral, Last Breath. Last Breath: Create 2 copies of me in the enemy deck."

Keywords (their own rows are on the keyword entries): Ephemeral, Last Breath

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| dies of self |  |  | copy | self to enemy player | deck |  | amount=2 |  |


Keyword entry:
**Ephemeral**
Card text: "This unit dies when it strikes or when the round ends."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| strikes by self |  |  | kill | self |  |  |  |  |
| round_end |  |  | kill | self |  |  |  |  |


Keyword entry:
**Last Breath**
Card text: "These abilities take effect when the unit dies."

(no rows of its own)



## Family: concept `copy` ("Copy cards or units"), from rows `do copy`
- Counts as copy: A copy of a card, unit or effect is made for the owner.
- Not copy: Doing a trigger again is repeat_trigger; a copy given to the opponent is enemy_benefit.
- Why the script suspects it: helps the enemy: puts it on the enemy side

### Card 757418 (gwent), tagged from: row | do copy | unit/enemy/it to enemy | deck_bottom | played(self) | own

**Contaminator**
Card text: "Deploy: Banish an enemy unit with 3 or less power, then, if it wasn't a Token, Spawn its base copy at the bottom of your opponent's deck."

Keywords (their own rows are on the keyword entries): Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | keyword_action | chosen enemy unit in board [strength le 3] |  | Banish |  | unstated |
| played of self |  | then | copy | it [state is created] [state not token] to enemy player | deck_bottom |  |  |  |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)


Keyword entry:
**Banish**
Card text: "Remove from the game. Note: Does not count as being destroyed."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | obliterate | it |  |  |  |  |


### Card 796247 (marvel_snap), tagged from: row | do copy | unit/mine/it to enemy | hand | played | own

**Machineworld**
Card text: "After you play a card here, add a copy to the opponent's hand."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of mine unit [position is same_lane] |  |  | copy | it to enemy player | hand |  |  |  |


### Card 751524 (runeterra), tagged from: row | do copy | spell/-/it to enemy | - | played | gives

**Ixtali Sentinel**
Card text: "Keywords: Lifesteal. When I'm summoned, create a Darkness in hand if you don't have one. When you play your next Darkness this round, copy it targeting the enemy Nexus."

Keywords (their own rows are on the keyword entries): Lifesteal

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of self | have mine card in hand [card is Darkness] not |  | create |  | hand | Darkness |  |  |
| summoned of self |  |  | give_ability | mine player |  |  |  | this_round |


Keyword entry:
**Lifesteal**
Card text: "Damage this unit deals heals its Nexus that amount."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| damaged by self |  |  | heal | mine player |  |  | amount=event_amount |  |


Card it names or makes:
**Darkness**
Card text: "Keywords: Slow. Deal 2 to an enemy."

Keywords (their own rows are on the keyword entries): Slow

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | chosen enemy unit in board |  |  | amount=2 |  |


### Card 757175 (gwent), tagged from: row | do copy | -/-/it to enemy | deck_top | killed | own

**Coated Weapons**
Card text: "Damage an enemy unit by 5. Deathblow: If it wasn't a Token, Banish it and Spawn a base copy of it on top of opponent's deck."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | chosen enemy unit in board |  |  | amount=5 |  |
| killed by self | it_matches [state not token] |  | keyword_action | it |  | Banish |  | unstated |
| killed by self | it_matches [state not token] | and | copy | it [state is created] to enemy player | deck_top |  |  |  |


Keyword entry:
**Banish**
Card text: "Remove from the game. Note: Does not count as being destroyed."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | obliterate | it |  |  |  |  |


### Card 751516 (runeterra), tagged from: row | do copy | -/-/self to enemy | deck | dies(self) | own

**Stinky Whump**
Card text: "Keywords: Last Breath. Last Breath: Create a copy of me in the enemy deck with 2 Poison Puffcaps attached."

Keywords (their own rows are on the keyword entries): Last Breath

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| dies of self |  |  | copy | self to enemy player | deck |  |  |  |
| dies of self |  | then | attach | it |  | Poison Puffcap | amount=2 |  |


Keyword entry:
**Last Breath**
Card text: "These abilities take effect when the unit dies."

(no rows of its own)


Card it names or makes:
**Poison Puffcap**
Card text: "Keywords: Trap. Deal 1 to your Nexus."

Keywords (their own rows are on the keyword entries): Trap

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | mine player |  |  | amount=1 |  |



## Family: concept `cost_reduction` ("Cards cost less"), from rows `do cost_change`
- Counts as cost_reduction: The owner's cards cost less by an amount.
- Not cost_reduction: A play that costs nothing at all is free_play; a cost set to a number is cost_set.
- Why the script suspects it: raises a cost

### Card 5000677 (duelyst), tagged from: row | do cost_change | equipment/enemy/all | hand | always | own

**Material Haunt**
Card text: "The enemy General's artifacts cost 1 more to play. Dying Wish: Draw 2 cards"

Keywords (their own rows are on the keyword entries): Dying Wish

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | cost_change | all enemy equipment in hand |  |  | cost=1 | while |
| dies of self |  |  | draw | mine card in deck_top |  |  | amount=2 |  |


Keyword entry:
**Dying Wish**
Card text: "Triggers an effect when this minion dies."

(no rows of its own)


### Card 741459 (faeria), tagged from: row | do cost_change | card/enemy/all | hand | moves_onto(self) | own

**Dustbringer Wraith**
Card text: "Corrupt - Increase the cost of each card in your opponent's hand by 1 faeria."

Keywords (their own rows are on the keyword entries): Corrupt

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| moves_onto of self [position is same_space] [once_per_game] |  |  | cost_change | all enemy card in hand |  |  | cost=1 | permanent |


Keyword entry:
**Corrupt**
Card text: "Triggers the first time this creature moves onto enemy land, on a turn after it was played."

(no rows of its own)


### Card 757244 (gwent), tagged from: row | do cost_change | card/mine/it | - | played(self) | own

**Bride of the Sea**
Card text: "Deploy: Play an Alchemy card from your graveyard with a provision cost 4 or less. Increase the cost by the total duration of Rain and Storm on your opponent's side."

Keywords (their own rows are on the keyword entries): Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | play_card | chosen mine card in discard [type is Alchemy] [cost le 4] | discard |  |  |  |
| played of self |  | then | cost_change | it |  |  | cost=sum keyword_amount of (all enemy position [keyword in Rain] [keyword in Storm]) | permanent |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)


### Card 8000722 (marvel_snap), tagged from: row | do cost_change | card/enemy/it | - | played(self) | own

**Witchfire**
Card text: "On Reveal: Your opponent draws a card, increase its cost by 1."

Keywords (their own rows are on the keyword entries): On Reveal

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | draw | enemy card in deck_top |  |  | amount=1 |  |
| played of self |  | then | cost_change | it |  |  | cost=1 | permanent |


Keyword entry:
**On Reveal**
Card text: "Acts once, when the card is turned face up on the board: after it is played, and also when a location or card puts it there, unless something stops On Reveal (Cosmo)."

(no rows of its own)


### Card 752087 (runeterra), tagged from: row | do cost_change | card/mine/- | hand | summoned(self) | own

**Lillia**
Card text: "Keywords: Quick Attack, Spirit. When I'm summoned or Strike: Create a Dream-Laden Bough in hand or, if you have one, reduce its cost by 1. Level up: You've summoned 15+ allies or landmarks."

Keywords (their own rows are on the keyword entries): Quick Attack, Spirit

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of self | have mine card in hand [card is Dream-Laden Bough] not |  | create |  | hand | Dream-Laden Bough |  |  |
| summoned of self | have mine card in hand [card is Dream-Laden Bough] is |  | cost_change | mine card in hand [card is Dream-Laden Bough] |  |  | cost=-1 | permanent |
| strikes by self | have mine card in hand [card is Dream-Laden Bough] not |  | create |  | hand | Dream-Laden Bough |  |  |
| strikes by self | have mine card in hand [card is Dream-Laden Bough] is |  | cost_change | mine card in hand [card is Dream-Laden Bough] |  |  | cost=-1 | permanent |
| always | amount sum (event_count of (summoned by mine player of mine unit) this_game + event_count of (summoned by mine player of mine landmark) this_game) ge 15 |  | level_up | self |  |  |  |  |


Keyword entry:
**Quick Attack**
Card text: "While attacking, strikes before its blocker."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| attacks by self |  |  | first_strike | self |  |  |  | this_round |


Keyword entry:
**Spirit**
Card text: "This unit has +1|+1. This keyword can stack."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | stat_change | self |  |  | power=1, health=1 | while |


Card it names or makes:
**Dream-Laden Bough**
Card text: "Keywords: Slow. Sleep an ally."

Keywords (their own rows are on the keyword entries): Slow

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | keyword_action | chosen mine unit in board |  | Sleep |  | unstated |



## Family: concept `cost_set` ("Set a cost to a fixed number"), from rows `do cost_set`
- Counts as cost_set: A card's cost becomes a fixed number (costs 0, costs 3).
- Not cost_set: A reduction by an amount is cost_reduction.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 8000042 (marvel_snap), tagged from: row | do cost_set | card/enemy/- | deck_top | played(self) | own

**Baron Mordo**
Card text: "On Reveal: The top card of your opponent's deck costs 6 until turn 6."

Keywords (their own rows are on the keyword entries): On Reveal

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | cost_set | enemy card in deck_top |  |  | cost=6 | while |


Keyword entry:
**On Reveal**
Card text: "Acts once, when the card is turned face up on the board: after it is played, and also when a location or card puts it there, unless something stops On Reveal (Cosmo)."

(no rows of its own)


### Card 750952 (runeterra), tagged from: row | do cost_set | card/enemy/random | hand | round_start | own

**Targon's Peak**
Card text: "Keywords: Landmark. Round Start: Reduce the cost of a random card in ALL players' hands to 0 this round."

Keywords (their own rows are on the keyword entries): Landmark

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| round_start |  |  | cost_set | random mine card in hand |  |  | cost=0 | this_round |
| round_start |  | and | cost_set | random enemy card in hand |  |  | cost=0 | this_round |


Keyword entry:
**Landmark**
Card text: "Landmarks take up a space on the board. They can't attack, block, or take damage."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | cant | self |  |  | event=attacks | while |
| always |  | and | cant | self |  |  | event=blocks | while |
| always |  | and | cant | self |  |  | event=damaged | while |


