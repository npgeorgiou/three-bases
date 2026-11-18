# Tag reading, batch 03


## Family: concept `return_to_hand` ("Return my unit to hand"), from rows `do return_to_hand`
- Counts as return_to_hand: The owner returns their own unit to hand, to replay it or save it: from play, when it dies, or from the discard pile or graveyard. (Widened 26 Oct 2026, Kaptain.)
- Not return_to_hand: Sending an enemy unit back is bounce_enemy.
- Why the script suspects it: return to hand: its rows say neither whose unit nor from where (the rows that say go to return_from_board, return_on_leave)

### Card 751758 (runeterra), tagged from: row | do return_to_hand | card/-/chosen | board | activated | uses_keyword Recall

**Unworthy Soul**
Card text: "Keywords: Flow. Flow: I cost 2 less. Recall a unit or landmark. If it has any attachments, destroy them first."

Keywords (their own rows are on the keyword entries): Flow

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always | event_count played by mine player of spell [category in fast_spell] [category in slow_spell] [category in skill] ge 2 last_round |  | cost_change | self |  |  | cost=-2 | while |
| played of self |  |  | kill | all equipment in attached |  |  |  |  |
| played of self |  | then | keyword_action | chosen card in board [category in unit] [category in landmark] |  | Recall |  | unstated |


Keyword entry:
**Flow**
Card text: "A card activates its Flow on Round Start if you played 2+ spells or skills last round."

(no rows of its own)


Keyword entry:
**Recall**
Card text: "Return a unit to hand and remove all effects applied to it."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | return_to_hand | it |  |  |  |  |
| activated |  | then | silence | it |  |  |  |  |


### Card 751446 (runeterra), tagged from: row | do return_to_hand | -/-/left_of_self | - | strikes | gives

**Ahri**
Card text: "Keywords: Quick Attack. Attack: The first time I attack strike, swap me with the ally to my right, then Recall it. Level up: You've Recalled 5+ units."

Keywords (their own rows are on the keyword entries): Quick Attack, Attack

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| attacks by self |  |  | give_ability | self |  |  |  | this_round |
| always | event_count recalled by mine player of unit ge 5 this_game |  | level_up | self |  |  |  |  |


Keyword entry:
**Quick Attack**
Card text: "While attacking, strikes before its blocker."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| attacks by self |  |  | first_strike | self |  |  |  | this_round |


Keyword entry:
**Attack**
Card text: "Get this effect when this unit attacks."

(no rows of its own)


### Card 751133 (runeterra), tagged from: row | do return_to_hand | unit/-/chosen | board | played(self) | own

**Defiant Dance**
Card text: "Recall a unit. Blade Dance 1."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | return_to_hand | chosen unit in board |  |  |  |  |
| played of self |  | then | keyword_action |  |  | Blade Dance | amount=1 |  |


Keyword entry:
**Blade Dance**
Card text: "Start a free attack with that many summoned Blades."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | start_attack | event_amount chosen mine unit [card is Blade] |  |  |  |  |



## Family: concept `spell_power` ("My spells and abilities get stronger"), from rows `do increase_effect`
- Counts as spell_power: The owner's spells or abilities deal more damage or have bigger effects: spell damage, ability power, amplify.
- Not spell_power: A unit gaining stats is stat_gain.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 7000415 (sts1), tagged from: row | do increase_effect | unit/enemy/it | - | damaged | own

**The Boot**
Card text: "Whenever you would deal 4 or less unblocked attack damage, increase it to 5."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| damaged by mine player of enemy unit [state is unblocked] | amount event_amount le 4 |  | increase_effect | it |  |  | amount=5 |  |


### Card 751497 (runeterra), tagged from: row | do increase_effect | player/enemy/it | - | attacks | own

**Albus Ferros**
Card text: "Keywords: Quick Attack. When I'm summoned, draw Jayce. Attack: Deal 3 to the enemy Nexus. For each 6+ cost spell you've played this game, increase it by 1."

Keywords (their own rows are on the keyword entries): Quick Attack, Attack

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of self |  |  | draw | mine card in deck [card is Jayce] |  |  | amount=1 |  |
| attacks by self |  |  | damage | enemy player |  |  | amount=3 |  |
| attacks by self |  | and | increase_effect | it |  |  | amount=event_count of (played by mine player of spell [cost ge 6]) this_game |  |


Keyword entry:
**Quick Attack**
Card text: "While attacking, strikes before its blocker."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| attacks by self |  |  | first_strike | self |  |  |  | this_round |


Keyword entry:
**Attack**
Card text: "Get this effect when this unit attacks."

(no rows of its own)


### Card 752099 (runeterra), tagged from: row | do increase_effect | unit/enemy/all | - | activated | uses_keyword Boost

**The Family Reunion**
Card text: "Keywords: Landmark. I: Grant a unit Gloom. II: Grant an ally Impact. III: Boost 2 units."

Keywords (their own rows are on the keyword entries): Landmark

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated | stage 1 |  | give_keyword | chosen unit in board |  | Gloom |  | permanent |
| activated | stage 2 |  | give_keyword | chosen mine unit in board |  | Impact |  | permanent |
| activated | stage 3 |  | keyword_action |  |  | Boost |  |  |


Keyword entry:
**Landmark**
Card text: "Landmarks take up a space on the board. They can't attack, block, or take damage."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | cant | self |  |  | event=attacks | while |
| always |  | and | cant | self |  |  | event=blocks | while |
| always |  | and | cant | self |  |  | event=damaged | while |


Keyword entry:
**Gloom**
Card text: "This unit has -1|-1. This keyword can stack."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | stat_change | self |  |  | power=-1, health=-1 | while |


Keyword entry:
**Impact**
Card text: "When this strikes while attacking, it deals 1 to the enemy Nexus. This keyword can stack."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| strikes by self [state is attacking] |  |  | damage | enemy player |  |  | amount=1 |  |


Keyword entry:
**Boost**
Card text: "Increase allies' positive stackable keywords or enemies' negative stackable keywords."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | choose_one |  |  |  |  |  |
| activated |  | or | increase_effect | all mine unit |  |  |  |  |
| activated |  | or | increase_effect | all enemy unit |  |  |  |  |


### Card 751391 (runeterra), tagged from: row | do increase_effect | card/enemy/all | everywhere | always | own

**Ava Achiever**
Card text: "When I'm summoned or Round End: Plant 3 Poison Puffcaps in the enemy deck. Traps on enemy cards are doubled when activated."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of self |  |  | keyword_action | enemy player | deck | Poison Puffcap Plant | amount=3 |  |
| round_end |  |  | keyword_action | enemy player | deck | Poison Puffcap Plant | amount=3 |  |
| always |  |  | increase_effect | all enemy card in everywhere [keyword is Trap] |  |  | amount=double (event_amount) | while |


Keyword entry:
**Plant**
Card text: "Planting adds cards (invisible or trap items such as Poison Puffcaps or Mysterious Portals) into decks."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | create | it | deck |  | amount=event_amount |  |


Card it names or makes:
**Poison Puffcap**
Card text: "Keywords: Trap. Deal 1 to your Nexus."

Keywords (their own rows are on the keyword entries): Trap

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | mine player |  |  | amount=1 |  |



## Family: concept `stat_gain` ("Stat gain (+power, +health)"), from rows `do stat_change`
- Counts as stat_gain: A unit's power, attack, health or other stat goes up, or is set or swapped to a higher value.
- Not stat_gain: Gaining only a keyword is that keyword's concept (evasion, first_strike...); a lasting rise each turn is permanent_growth.
- Why the script suspects it: lowers a stat: that is stat_loss

### Card 8000474 (marvel_snap), tagged from: row | do stat_change | unit/enemy/lowest | board | played(self) | own

**Red Guardian**
Card text: "On Reveal: Afflict the lowest-Power enemy card here with -2 Power and remove its text."

Keywords (their own rows are on the keyword entries): On Reveal

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stat_change | lowest enemy unit by power in board [position is same_lane] |  |  | power=-2 | permanent |
| played of self |  | and | silence | it |  |  |  |  |


Keyword entry:
**On Reveal**
Card text: "Acts once, when the card is turned face up on the board: after it is played, and also when a location or card puts it there, unless something stops On Reveal (Cosmo)."

(no rows of its own)


### Card 8000282 (marvel_snap), tagged from: row | do stat_change | unit/enemy/random | board | played(self) | own

**Jane Foster Fractured Frontier**
Card text: "On Reveal: Judge 4 other random characters. +1 Power (if yours) or -1 Power (enemies). Quickdraw: Judge the worthy again."

Keywords (their own rows are on the keyword entries): On Reveal, Quickdraw

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stat_change | 4 random mine unit in board [card not Jane Foster Fractured Frontier] |  |  | power=1 | permanent |
| played of self |  | and | stat_change | 4 random enemy unit in board |  |  | power=-1 | permanent |
| played of self | keyword_condition Quickdraw |  | stat_change | 4 random mine unit in board [card not Jane Foster Fractured Frontier] |  |  | power=1 | permanent |
| played of self | keyword_condition Quickdraw | and | stat_change | 4 random enemy unit in board |  |  | power=-1 | permanent |


Keyword entry:
**On Reveal**
Card text: "Acts once, when the card is turned face up on the board: after it is played, and also when a location or card puts it there, unless something stops On Reveal (Cosmo)."

(no rows of its own)


Keyword entry:
**Quickdraw**
Card text: "The stronger ability after the word is used instead of the normal one when the card is played on the same turn it was drawn."

(no rows of its own)


### Card 8000689 (marvel_snap), tagged from: row | do stat_change | card/enemy/chosen | hand | played(self) | own

**Vampiric Spear**
Card text: "On Reveal: Vampire Killmonger steals 2 Power from a character in your opponent's hand."

Keywords (their own rows are on the keyword entries): On Reveal

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stat_change | chosen enemy card in hand |  |  | power=-2 | permanent |
| played of self |  | then | stat_change | mine unit in board [card is Vampire Killmonger] |  |  | power=2 | permanent |


Keyword entry:
**On Reveal**
Card text: "Acts once, when the card is turned face up on the board: after it is played, and also when a location or card puts it there, unless something stops On Reveal (Cosmo)."

(no rows of its own)


### Card 8000738 (marvel_snap), tagged from: row | do stat_change | card/enemy/chosen | hand | round_end | own

**Zombie Blade**
Card text: "End of Turn: If you played an On Reveal, your Zombie Horde steals 1 Power from a character in your opponent's hand. (Horde first if necessary)"

Keywords (their own rows are on the keyword entries): End of Turn

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| round_end | event_count played by mine player of mine unit in board [keyword is On Reveal] ge 1 this_round |  | stat_change | chosen enemy card in hand |  |  | power=-1 | permanent |
| round_end | event_count played by mine player of mine unit in board [keyword is On Reveal] ge 1 this_round | then | stat_change | mine card [card is Zombie Horde] |  |  | power=1 | permanent |


Keyword entry:
**End of Turn**
Card text: "Acts at the end of every turn while the card is on the board."

(no rows of its own)


### Card 8000064 (marvel_snap), tagged from: row | do stat_change | unit/enemy/highest_cost | hand | played(self) | own

**Brand of Shou-Lao**
Card text: "On Reveal: One of your other cards here steals 2 Power from the character that costs the most in your opponent's hand."

Keywords (their own rows are on the keyword entries): On Reveal

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stat_change | highest_cost enemy unit in hand |  |  | power=-2 | permanent |
| played of self |  | then | stat_change | chosen mine unit in board [position is same_lane] [card not Brand of Shou-Lao] |  |  | power=2 | permanent |


Keyword entry:
**On Reveal**
Card text: "Acts once, when the card is turned face up on the board: after it is played, and also when a location or card puts it there, unless something stops On Reveal (Cosmo)."

(no rows of its own)


### Card 751637 (runeterra), tagged from: row | do stat_change | unit/enemy/all | board | played(self) | own

**Sands of Time**
Card text: "Give enemies -2|-0 this round. Create a Fleeting Instant Century in hand."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stat_change | all enemy unit in board |  |  | power=-2 | this_round |
| played of self |  | and | create | mine card [state is fleeting] | hand | Instant Century |  |  |


Card it names or makes:
**Instant Century**
Card text: "Keywords: Focus. Summon a random landmark with Countdown, or advance a landmark 4 rounds."

Keywords (their own rows are on the keyword entries): Focus

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | choose_one |  |  |  |  |  |
| played of self |  | or | summon | random landmark [keyword is Countdown] |  |  |  |  |
| played of self |  | or | countdown_advance | chosen landmark in board |  |  | amount=4 |  |


### Card 752061 (runeterra), tagged from: row | do stat_change | unit/enemy/all | board | always | uses_keyword Gloom

**Existential Dread**
Card text: "Grant enemies Gloom."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | give_keyword | all enemy unit in board |  | Gloom |  | permanent |


Keyword entry:
**Gloom**
Card text: "This unit has -1|-1. This keyword can stack."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | stat_change | self |  |  | power=-1, health=-1 | while |


### Card 8000594 (marvel_snap), tagged from: row | do stat_change | unit/enemy/all | board | played(self) | own

**Spider-Woman**
Card text: "On Reveal: Afflict all enemy cards here with -1 Power."

Keywords (their own rows are on the keyword entries): On Reveal

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stat_change | all enemy unit in board [position is same_lane] |  |  | power=-1 | permanent |


Keyword entry:
**On Reveal**
Card text: "Acts once, when the card is turned face up on the board: after it is played, and also when a location or card puts it there, unless something stops On Reveal (Cosmo)."

(no rows of its own)


### Card 750898 (runeterra), tagged from: row | do stat_change | unit/enemy/all | board | attacks | own

**Terror of the Tides**
Card text: "Keywords: Deep. Sea Monster allies have Fearsome. Attack: Give enemies -2|-0 this round."

Keywords (their own rows are on the keyword entries): Deep, Attack

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | all mine unit in board [type is Sea Monster] |  | Fearsome |  | while |
| attacks by self |  |  | stat_change | all enemy unit in board |  |  | power=-2 | this_round |


Keyword entry:
**Deep**
Card text: "Once a player has 15 or fewer cards in their Deck, they become Deep for the rest of the game. Increasing the number of cards in the Deck to more than 15 cards will not remove the Deep state. When a player is Deep, their units with the Deep keyword have +3|+3, including when in deck or hand."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always | keyword_condition Deep |  | stat_change | self in everywhere |  |  | power=3, health=3 | while |


Keyword entry:
**Attack**
Card text: "Get this effect when this unit attacks."

(no rows of its own)


Keyword entry:
**Fearsome**
Card text: "Can only be blocked by enemies with 3 or more Power."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | cant | all enemy unit [power lt 3] to self |  |  | event=blocks | while |



## Family: concept `summon` ("Summon units / tokens"), from rows `do summon`
- Counts as summon: New units are put onto the owner's side of the board.
- Not summon: Units put on the opponent's side are board_clog; units back from death are revive.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 5000588 (duelyst), tagged from: row | do summon | unit/enemy/all | hand | played(self) | own

**Evolutionary Apex**
Card text: "BOTH players put all minions in their action bars onto the battlefield nearby their General."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | summon | all mine unit in hand to position [position is surrounding] |  |  |  |  |
| played of self |  | and | summon | all enemy unit in hand to position [position is surrounding] |  |  |  |  |


### Card 760875 (into_the_breach), tagged from: row | do summon | unit/enemy/- | board | turn_start | own

**Emerging**
Card text: "Vek will emerge here next turn. Any unit blocking this space will take one damage."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_start [next_time] |  |  | summon | enemy unit to position [position is same_space] | board |  |  |  |
| turn_start [next_time] |  | and | damage | all unit [position is same_space] |  |  | amount=1 |  |


### Card 761152 (into_the_breach), tagged from: row | do summon | unit/enemy/- | board | turn_start | own

**Spawn Tile**
Card text: "Vek will emerge here next turn. Any unit blocking this space will take one damage. Vek will emerge here next turn. Any unit blocking this space will take one damage."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_start [next_time] |  |  | summon | enemy unit to position [position is same_space] | board |  |  |  |
| turn_start [next_time] |  | and | damage | all unit [position is same_space] |  |  | amount=1 |  |


