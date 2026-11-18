# Tag reading, batch 08


## Family: concept `resource_gain` ("Gain resources (ramp)"), from rows `do mana_gain`
- Counts as resource_gain: The owner gains extra mana, energy, supply or another resource, now or for good.
- Not resource_gain: Cards costing less is cost_reduction.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 741116 (faeria), tagged from: row | do mana_gain | player/enemy/- | - | dies(self) | own

**Hunted Outlaw**
Card text: "Last Words - Your opponent draws a card and gains 2 faeria."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| dies of self |  |  | draw | enemy card in deck_top |  |  | amount=1 |  |
| dies of self |  | and | mana_gain | enemy player |  |  | amount=2 |  |


### Card 757259 (gwent), tagged from: row | do mana_gain | secondary_resource/enemy/- | - | dies(self) | uses_keyword Bounty

**The Witchfinder**
Card text: "Deploy: Spawn 3 Syndicate Crowns on this row. At the end of your turn, if no enemy unit has a Bounty, place a Bounty on the highest-power enemy unit."

Keywords (their own rows are on the keyword entries): Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | summon |  to mine position [position is same_row] |  | Syndicate Crown | amount=3 |  |
| played of self |  |  | summon | mine unit to mine position [position is same_row] |  | Syndicate Crown | amount=3 |  |
| turn_end by mine player | have enemy unit in board [keyword is Bounty] not |  | give_keyword | highest enemy unit by strength in board |  | Bounty |  | permanent |
| turn_end by mine player | have enemy unit in board [keyword is Bounty] not |  | give_keyword | highest enemy unit by strength in board |  | Bounty |  | permanent |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)


Keyword entry:
**Bounty**
Card text: "When a unit with this status is destroyed or banished, opponent gains coins equal to its base power. There can be only one unit with Bounty status on each side of the board at given time."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| dies of self |  |  | mana_gain | enemy secondary_resource |  |  | amount=stat base_power of (self) |  |
| obliterated of self |  |  | mana_gain | enemy secondary_resource |  |  | amount=stat base_power of (self) |  |


Card it names or makes:
**Syndicate Crown**
Card text: "Doomed. Zeal. Order: Gain 1 Coin and Banish self."

Keywords (their own rows are on the keyword entries): Doomed, Zeal, Order

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Doomed |  | permanent |
| always |  | and | give_keyword | self |  | Zeal |  | permanent |
| activated of self |  |  | mana_gain | mine secondary_resource |  |  | amount=1 |  |
| activated of self |  | and | keyword_action | self |  | Banish |  | unstated |


### Card 796178 (marvel_snap), tagged from: row | do mana_gain | mana/enemy/- | - | round_start | own

**Castle Blackstone**
Card text: "The player winning here gets +1 Energy each turn."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| round_start | amount sum (stat power of (all mine unit in board [position is same_lane]) + minus (stat power of (all enemy unit in board [position is same_lane]))) gt 0 |  | mana_gain | mine mana |  |  | amount=1 |  |
| round_start | amount sum (stat power of (all enemy unit in board [position is same_lane]) + minus (stat power of (all mine unit in board [position is same_lane]))) gt 0 |  | mana_gain | enemy mana |  |  | amount=1 |  |


### Card 741191 (faeria), tagged from: row | do mana_gain | player/enemy/- | - | dies(self) | own

**Ruunin's Shrine**
Card text: "Gift - Gain 2 faeria. Last Words - Your opponent gains 2 faeria."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | mana_gain | mine player |  |  | amount=2 |  |
| dies of self |  |  | mana_gain | enemy player |  |  | amount=2 |  |


### Card 756846 (gwent), tagged from: row | do mana_gain | secondary_resource/enemy/- | - | dies(self) | uses_keyword Bounty

**Kurt**
Card text: "Deploy (Melee): Place a Bounty on an enemy unit. Deploy (Ranged): Purify a unit."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self | keyword_condition Melee |  | give_keyword | chosen enemy unit in board |  | Bounty |  | permanent |
| played of self | keyword_condition Ranged |  | keyword_action | chosen unit in board |  | Purify |  | unstated |


Keyword entry:
**Bounty**
Card text: "When a unit with this status is destroyed or banished, opponent gains coins equal to its base power. There can be only one unit with Bounty status on each side of the board at given time."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| dies of self |  |  | mana_gain | enemy secondary_resource |  |  | amount=stat base_power of (self) |  |
| obliterated of self |  |  | mana_gain | enemy secondary_resource |  |  | amount=stat base_power of (self) |  |


Keyword entry:
**Purify**
Card text: "Remove all statuses."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | remove_keywords | it |  |  |  |  |



## Family: concept `resource_gain` ("Gain resources (ramp)"), from rows `do max_mana_change`
- Counts as resource_gain: The owner gains extra mana, energy, supply or another resource, now or for good.
- Not resource_gain: Cards costing less is cost_reduction.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 5000492 (duelyst), tagged from: row | do max_mana_change | mana/enemy/- | - | played(self) | own

**Malicious Wisp**
Card text: "Opening Gambit: Take a mana crystal from your opponent. Dying Wish: Give back the mana crystal."

Keywords (their own rows are on the keyword entries): Dying Wish, Opening Gambit

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | max_mana_change | enemy mana |  |  | amount=-1 |  |
| played of self |  | and | max_mana_change | mine mana |  |  | amount=1 |  |
| dies of self |  |  | max_mana_change | mine mana |  |  | amount=-1 |  |
| dies of self |  | and | max_mana_change | enemy mana |  |  | amount=1 |  |


Keyword entry:
**Dying Wish**
Card text: "Triggers an effect when this minion dies."

(no rows of its own)


Keyword entry:
**Opening Gambit**
Card text: "Triggers an effect when summoned from your action bar."

(no rows of its own)


### Card 796301 (marvel_snap), tagged from: row | do max_mana_change | mana/enemy/- | - | round_end | own

**Sakaar Grand Prix**
Card text: "After turn 4, the winner here gets +1 Max Energy."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| round_end | event_count round_start eq 4 this_game; amount sum (stat power of (all mine unit in board [position is same_lane]) + minus (stat power of (all enemy unit in board [position is same_lane]))) gt 0 |  | max_mana_change | mine mana |  |  | amount=1 |  |
| round_end | event_count round_start eq 4 this_game; amount sum (stat power of (all enemy unit in board [position is same_lane]) + minus (stat power of (all mine unit in board [position is same_lane]))) gt 0 |  | max_mana_change | enemy mana |  |  | amount=1 |  |


### Card 796370 (marvel_snap), tagged from: row | do max_mana_change | mana/enemy/- | - | always | own

**White Hot Room**
Card text: "First to fill this gets +3 Max Energy."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always [once_per_game] | count mine unit in board [position is same_lane] ge 4; count enemy unit in board [position is same_lane] lt 4 |  | max_mana_change | mine mana |  |  | amount=3 |  |
| always [once_per_game] | count enemy unit in board [position is same_lane] ge 4; count mine unit in board [position is same_lane] lt 4 |  | max_mana_change | enemy mana |  |  | amount=3 |  |



## Family: concept `return_to_hand` ("Return my unit to hand"), from rows `do keyword_action`
- Counts as return_to_hand: The owner returns their own unit to hand, to replay it or save it: from play, when it dies, or from the discard pile or graveyard. (Widened 26 Oct 2026, Kaptain.)
- Not return_to_hand: Sending an enemy unit back is bounce_enemy.
- Why the script suspects it: return to hand: its rows say neither whose unit nor from where (the rows that say go to return_from_board, return_on_leave)

### Card 750845 (runeterra), tagged from: row | do keyword_action | unit/-/chosen | board | played(self) | own

**Strong-arm**
Card text: "Keywords: Plunder. Plunder: Recall ANY follower into your hand."

Keywords (their own rows are on the keyword entries): Plunder

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self | keyword_condition Plunder |  | keyword_action | chosen unit in board [category is follower] |  | Recall |  | unstated |


Keyword entry:
**Plunder**
Card text: "A card activates its plunder ability when played if you damaged the enemy Nexus this round."

(no rows of its own)


Keyword entry:
**Recall**
Card text: "Return a unit to hand and remove all effects applied to it."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | return_to_hand | it |  |  |  |  |
| activated |  | then | silence | it |  |  |  |  |


### Card 797002 (runeterra), tagged from: row | do keyword_action | unit/-/chosen | board | played(self) | own

**Peerless Artistry**
Card text: "Keywords: Skill. Recall a unit with less Power than me."

Keywords (their own rows are on the keyword entries): Skill

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | keyword_action | chosen unit in board [power lt stat power of (self)] |  | Recall |  | unstated |


Keyword entry:
**Skill**
Card text: "A unit's spell-like effect that allows enemy reactions."

(no rows of its own)


Keyword entry:
**Recall**
Card text: "Return a unit to hand and remove all effects applied to it."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | return_to_hand | it |  |  |  |  |
| activated |  | then | silence | it |  |  |  |  |


### Card 750513 (runeterra), tagged from: row | do keyword_action | unit/-/chosen | board | played(self) | own

**Will of Ionia**
Card text: "Recall a unit."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | keyword_action | chosen unit in board |  | Recall |  | unstated |


Keyword entry:
**Recall**
Card text: "Return a unit to hand and remove all effects applied to it."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | return_to_hand | it |  |  |  |  |
| activated |  | then | silence | it |  |  |  |  |


### Card 796939 (runeterra), tagged from: row | do keyword_action | unit/-/chosen | board | played(self) | own

**Gust**
Card text: "Keywords: Elemental Skill. Recall a unit."

Keywords (their own rows are on the keyword entries): Elemental Skill

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | keyword_action | chosen unit in board |  | Recall |  | unstated |


Keyword entry:
**Elemental Skill**
Card text: "A unit's spell-like effect that allows enemy reactions. It's elemental!"

(no rows of its own)


Keyword entry:
**Recall**
Card text: "Return a unit to hand and remove all effects applied to it."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | return_to_hand | it |  |  |  |  |
| activated |  | then | silence | it |  |  |  |  |


### Card 751066 (runeterra), tagged from: row | do keyword_action | unit/-/all | board | played(self) | own

**Singular Will**
Card text: "Pick an ally. Recall ALL other units and landmarks."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | choose_card | chosen mine unit in board [card not Singular Will] |  |  |  |  |
| played of self |  | then | keyword_action | all unit in board [state not targeted_this_round] |  | Recall |  | unstated |
| played of self |  | and | keyword_action | all landmark in board |  | Recall |  | unstated |


Keyword entry:
**Recall**
Card text: "Return a unit to hand and remove all effects applied to it."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | return_to_hand | it |  |  |  |  |
| activated |  | then | silence | it |  |  |  |  |



## Family: concept `return_to_hand` ("Return my unit to hand"), from rows `do return_to_hand`
- Counts as return_to_hand: The owner returns their own unit to hand, to replay it or save it: from play, when it dies, or from the discard pile or graveyard. (Widened 26 Oct 2026, Kaptain.)
- Not return_to_hand: Sending an enemy unit back is bounce_enemy.
- Why the script suspects it: return to hand: its rows say neither whose unit nor from where (the rows that say go to return_from_board, return_on_leave)

### Card 5000745 (duelyst), tagged from: row | do return_to_hand | unit/-/chosen | board | played(self) | own

**Bounce Minion Spawn Entity**
Card text: "Return a minion its action bar. Summon an entity on that space."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | return_to_hand | chosen unit in board |  |  |  |  |
| played of self |  | and | summon | chosen unit in board to it |  |  |  |  |


### Card 796249 (marvel_snap), tagged from: row | do return_to_hand | unit/-/all | board | round_end | own

**Mercworld**
Card text: "After turn 3, return cards here to hand. Double their Power."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| round_end | event_count round_start eq 3 this_game |  | return_to_hand | all unit in board [position is same_lane] |  |  |  |  |
| round_end | event_count round_start eq 3 this_game | then | stat_change | it |  |  | power=stat power of (it) | permanent |


### Card 796550 (runeterra), tagged from: row | do return_to_hand | -/-/left_of_self | - | strikes | gives

**Ahri (level 2)**
Card text: "Keywords: Quick Attack, Elusive, Missing Translation. When you Recall an ally, reduce its cost by 1. Attack: Each time I attack strike, swap me with the ally to my right, then Recall it."

Keywords (their own rows are on the keyword entries): Quick Attack, Elusive, Attack

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| recalled by mine player of mine unit |  |  | cost_change | it |  |  | cost=-1 | permanent |
| attacks by self |  |  | give_ability | self |  |  |  | this_round |


Keyword entry:
**Quick Attack**
Card text: "While attacking, strikes before its blocker."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| attacks by self |  |  | first_strike | self |  |  |  | this_round |


Keyword entry:
**Elusive**
Card text: "Can only be blocked by an Elusive unit."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | cant | all enemy unit [keyword not Elusive] to self |  |  | event=blocks | while |


Keyword entry:
**Attack**
Card text: "Get this effect when this unit attacks."

(no rows of its own)


### Card 5000307 (duelyst), tagged from: row | do return_to_hand | unit/-/chosen | board | played(self) | own

**Hailstone Prison**
Card text: "Return ANY minion to its action bar."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | return_to_hand | chosen unit in board |  |  |  |  |


### Card 751735 (runeterra), tagged from: row | do return_to_hand | spell/mine/chosen | - | played(self) | own

**Puzzling Signposts**
Card text: "Return a Fast or Slow spell to hand or destroy a unit's Equipment. Draw 1."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | choose_one | self |  |  |  |  |
| played of self |  | or | return_to_hand | chosen mine spell [category in fast_spell] [category in slow_spell] |  |  |  |  |
| played of self |  | or | kill | chosen equipment |  |  |  |  |
| played of self |  | and | draw | mine card in deck_top |  |  | amount=1 |  |


