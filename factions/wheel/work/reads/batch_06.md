# Tag reading, batch 06


## Family: concept `on_draw` ("When a card is drawn"), from rows `when drawn`
- Counts as on_draw: Triggers when the owner or a player draws a card. (Added 19 Oct 2026, Claude's.)
- Not on_draw: Drawing cards as the effect is draw.
- Why the script suspects it: fires on the enemy's action

### Card 5000650 (duelyst), tagged from: row | when drawn | card/enemy/- | - | drawn | own

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


### Card 750837 (runeterra), tagged from: row | when drawn | card/enemy/- by mine | - | drawn | own

**Black Market Merchant**
Card text: "Keywords: Plunder. When you draw an enemy card, reduce its cost by 1. Plunder: Nab 1."

Keywords (their own rows are on the keyword entries): Plunder

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| drawn by mine player of enemy card |  |  | cost_change | it |  |  | cost=-1 | permanent |
| played of self | keyword_condition Plunder |  | keyword_action |  |  | Nab | amount=1 |  |


Keyword entry:
**Plunder**
Card text: "A card activates its plunder ability when played if you damaged the enemy Nexus this round."

(no rows of its own)


Keyword entry:
**Nab**
Card text: "Draw a non-champion card from the bottom of the enemy deck."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | draw | bottom enemy card in deck_bottom [category not champion] |  |  |  |  |


### Card 5000238 (duelyst), tagged from: row | when drawn | -/-/- by enemy | - | drawn | own

**Vindicator**
Card text: "Whenever your opponent draws a card, this minion gains +2/+2."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| drawn by enemy player |  |  | stat_change | self |  |  | power=2, health=2 | permanent |


### Card 751493 (runeterra), tagged from: row | when drawn | -/-/- by enemy | - | drawn | own

**Justice Rider**
Card text: "Whenever your opponent draws, plant 1 Flashbomb Trap in the top 8 cards of the enemy deck."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| drawn by enemy player |  |  | keyword_action | 8 enemy card in deck_top |  | Flashbomb Trap Plant | amount=1 |  |


Keyword entry:
**Plant**
Card text: "Planting adds cards (invisible or trap items such as Poison Puffcaps or Mysterious Portals) into decks."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | create | it | deck |  | amount=event_amount |  |


Card it names or makes:
**Flashbomb Trap**
Card text: "Keywords: Trap. Deal 1 damage to a random ally."

Keywords (their own rows are on the keyword entries): Trap

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | random mine unit in board |  |  | amount=1 |  |


### Card 5000793 (duelyst), tagged from: row | when drawn | -/-/- by enemy | - | drawn | own

**Decimus**
Card text: "Whenever your opponent draws a card, deal 2 damage to the enemy General."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| drawn by enemy player |  |  | damage | enemy player |  |  | amount=2 |  |



## Family: concept `permanent_growth` ("Grows again and again"), from rows `do give_keyword`
- Counts as permanent_growth: A unit gains stats repeatedly (each turn, each trigger) and keeps them.
- Not permanent_growth: A single lasting bonus is stat_gain.
- Why the script suspects it: grows once, when played: a single lasting bonus is stat_gain

### Card 5000482 (duelyst), tagged from: row | do give_keyword | unit/-/chosen | board | played(self) | own

**Gargantuan Growth**
Card text: "Give a minion, \"Grow: +8/+8.\""

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | give_keyword | chosen unit in board |  | Grow | amount=8 | permanent |


Keyword entry:
**Grow**
Card text: "Gets bigger at the start of your turn."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_start by mine player |  |  | stat_change | self |  |  | power=unstated, health=unstated | permanent |


### Card 757337 (gwent), tagged from: row | do give_keyword | unit/mine/chosen | board | played(self) | own

**Orchard Mantrap**
Card text: "Deploy (Melee): Consume an allied unit. This unit triggers Thrive an additional time. Deploy (Ranged): Infuse 2 allied units with "Thrive"."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self | keyword_condition Melee |  | keyword_action | chosen mine unit in board |  | Consume |  | unstated |
| always |  |  | increase_effect | self |  | Thrive | amount=1 |  |
| played of self | keyword_condition Ranged |  | give_keyword | 2 chosen mine unit in board |  | Thrive |  | permanent |


Keyword entry:
**Consume**
Card text: "Destroy a unit and boost self by its power. If target is in the graveyard, Banish it instead."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | kill | it unit in board |  |  |  |  |
| activated |  | then | stat_change | self |  |  | strength=stat strength of (it) | permanent |
| activated |  | instead | keyword_action | it unit in discard |  | Banish |  | unstated |


Keyword entry:
**Thrive**
Card text: "Boost this unit by 1 or the specified amount whenever you play a unit with higher power."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of mine unit [strength gt stat strength of (self)] |  |  | stat_change | self |  |  | strength=listed | permanent |


### Card 751115 (runeterra), tagged from: row | do give_keyword | card/mine/all | - | played(self) | own

**Glorious Evolution**
Card text: "Your cards have -1 cost, Augment, are created by Glorious Evolution, and are now Tech."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | cost_change | all mine card |  |  | cost=-1 | permanent |
| played of self |  | and | give_keyword | all mine card |  | Augment |  | permanent |
| played of self |  | and | give_type | all mine card |  |  |  | permanent |


Keyword entry:
**Augment**
Card text: "When you play a created card, grant me +1|+0."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played by mine player of card [state is created] |  |  | stat_change | self |  |  | power=1, health=0 | permanent |


### Card 1000084 (stormbound), tagged from: row | do give_keyword | unit/-/it | - | played(self) | own

**Soap Cleanse**
Card text: "Give 1/2/3/4/5 strength to poisoned units and vitalize them"

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stat_change | all unit in board [state is poisoned] |  |  | strength=per_level (1 + 2 + 3 + 4 + 5) | permanent |
| played of self |  | and | give_keyword | it |  | Vitalize |  | permanent |


Keyword entry:
**Vitalize**
Card text: "A vitalized unit gains 1 strength at the start of each turn until it is poisoned."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_start by mine player |  |  | stat_change | self |  |  | strength=1 | permanent |
| given_keyword of self [keyword is Poison] |  |  | remove_keyword | self |  | Vitalize |  |  |


### Card 7000589 (sts1), tagged from: row | do give_keyword | player/mine/- | - | played(self) | own

**Cultist Potion**
Card text: "Gain 1 Ritual."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | give_keyword | mine player |  | Ritual | amount=1 | permanent |


Keyword entry:
**Ritual**
Card text: "Gain Strength at the end of your turn."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_end by mine player |  |  | give_keyword | self |  | Strength | amount=count of (self keyword [keyword is Ritual]) | permanent |



## Family: concept `permanent_growth` ("Grows again and again"), from rows `do give_keyword`
- Counts as permanent_growth: A unit gains stats repeatedly (each turn, each trigger) and keeps them.
- Not permanent_growth: A single lasting bonus is stat_gain.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 1000120 (stormbound), tagged from: row | do give_keyword | unit/enemy/it | - | dies(self) | own

**Green Prototypes**
Card text: "On death, give 1/2/3/4/5 strength to a random enemy unit and vitalize it"

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| dies of self |  |  | stat_change | random enemy unit in board |  |  | strength=per_level (1 + 2 + 3 + 4 + 5) | permanent |
| dies of self |  | and | give_keyword | it |  | Vitalize |  | permanent |


Keyword entry:
**Vitalize**
Card text: "A vitalized unit gains 1 strength at the start of each turn until it is poisoned."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_start by mine player |  |  | stat_change | self |  |  | strength=1 | permanent |
| given_keyword of self [keyword is Poison] |  |  | remove_keyword | self |  | Vitalize |  |  |



## Family: concept `permanent_growth` ("Grows again and again"), from rows `do repeat`
- Counts as permanent_growth: A unit gains stats repeatedly (each turn, each trigger) and keeps them.
- Not permanent_growth: A single lasting bonus is stat_gain.
- Why the script suspects it: grows once, when played: a single lasting bonus is stat_gain

### Card 756968 (gwent), tagged from: row | do repeat | -/-/self | - | played | own

**Kikimore Queen**
Card text: "Thrive. Whenever this unit's Thrive is triggered, boost all allied Insectoids on this row by 1. Whenever you play an Organic card, trigger own Thrive."

Keywords (their own rows are on the keyword entries): Thrive

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Thrive |  | permanent |
| keyword_used by self | keyword_condition Thrive |  | stat_change | all mine unit in board [type is Insectoid] [position is same_row] |  |  | strength=1 | permanent |
| played of mine card [type is Organic] |  |  | repeat | self |  | Thrive |  |  |


Keyword entry:
**Thrive**
Card text: "Boost this unit by 1 or the specified amount whenever you play a unit with higher power."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of mine unit [strength gt stat strength of (self)] |  |  | stat_change | self |  |  | strength=listed | permanent |



## Family: concept `permanent_growth` ("Grows again and again"), from rows `do stat_change`
- Counts as permanent_growth: A unit gains stats repeatedly (each turn, each trigger) and keeps them.
- Not permanent_growth: A single lasting bonus is stat_gain.
- Why the script suspects it: grows once, when played: a single lasting bonus is stat_gain

### Card 5000525 (duelyst), tagged from: rule permanent_growth | do stat_change | -/-/self | - | played | own

**Pureblade Enforcer**
Card text: "Whenever your opponent casts a spell, this minion gains +1/+1."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of enemy spell |  |  | stat_change | self |  |  | power=1, health=1 | permanent |


### Card 741230 (faeria), tagged from: rule permanent_growth | do stat_change | -/-/self | - | played(self) | own

**Axe Grinder**
Card text: "Gift - Gains +1/+1 if summoned adjacent to an opponent's well."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self | have enemy position [terrain is resource_well] [position is bordering] is |  | stat_change | self |  |  | power=1, health=1 | permanent |


### Card 756811 (gwent), tagged from: rule permanent_growth | do stat_change | -/-/self | - | played | uses_keyword Harmony

**Weeping Willow**
Card text: "Harmony. Order (Melee): Boost self by the number of unique primary categories among units you control. Deploy (Ranged): Poison an enemy unit."

Keywords (their own rows are on the keyword entries): Harmony

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Harmony |  | permanent |
| activated of self | keyword_condition Melee |  | stat_change | self |  |  | strength=distinct primary_type of (all mine unit in board) | permanent |
| played of self | keyword_condition Ranged |  | give_keyword | chosen enemy unit in board |  | Poison |  | permanent |


Keyword entry:
**Harmony**
Card text: "Boost self by 1 or the specified amount whenever you play a non-Neutral unit, whose primary category is unique among all of your units."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of mine unit [region not Neutral] | have mine unit in board [state is shares_subtype_with_it] not |  | stat_change | self |  |  | strength=listed | permanent |


Keyword entry:
**Poison**
Card text: "Status - if a unit receives two instances of Poison, destroy it."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| given_keyword of self [keyword is Poison] | event_count given_keyword of self [keyword is Poison] ge 2 this_game |  | kill | self |  |  |  |  |


### Card 8000031 (marvel_snap), tagged from: rule permanent_growth | do stat_change | -/-/self | - | played(self) | own

**Ares**
Card text: "On Reveal: Compare the Power of the top 3 cards of both decks. If your total is higher, +6 Power."

Keywords (their own rows are on the keyword entries): On Reveal

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self | amount sum (stat power of (3 mine card in deck_top) + minus (stat power of (3 enemy card in deck_top))) gt 0 |  | stat_change | self |  |  | power=6 | permanent |


Keyword entry:
**On Reveal**
Card text: "Acts once, when the card is turned face up on the board: after it is played, and also when a location or card puts it there, unless something stops On Reveal (Cosmo)."

(no rows of its own)


### Card 2000110 (monster_train), tagged from: rule permanent_growth | do stat_change | -/-/self | - | played | own

**Siren of the Sea**
Card text: "Incant: +2 Attack and +2 Health."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of mine spell [position is same_lane] |  |  | stat_change | self |  |  | power=2, health=2 | permanent |


