# Tag reading, batch 03


## Family: concept `count_payoff` ("Grows with what happened this game"), from rows `if amount_count`
- Counts as count_payoff: The effect grows with how many times something happened this game: cards played, units died, spells cast.
- Not count_payoff: A count of what is on the board now is condition_count.
- Why the script suspects it: counts what is on the board now: that is condition_count

### Card 5000651 (duelyst), tagged from: rule count_payoff | if amount_count | mana/enemy/- | - | turn_end | own

**Archonis**
Card text: "At the end of each turn, deal damage to the player equal to their remaining mana."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_end |  |  | damage | enemy player |  |  | amount=count of (enemy mana) |  |


### Card 741425 (faeria), tagged from: rule count_payoff | if amount_count | unit/mine/all | board | played(self) | own

**Rakoan Champion**
Card text: "Dash 2 Gift - Gains +1/+1 for each other friendly Rakoan in play."

Keywords (their own rows are on the keyword entries): Dash

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Dash | amount=2 | permanent |
| played of self |  |  | stat_change | self |  |  | power=count of (all mine unit in board [type is rakoan] [card not Rakoan Champion]), health=count of (all mine unit in board [type is rakoan] [card not Rakoan Champion]) | permanent |


Keyword entry:
**Dash**
Card text: "When summoned, moves X spaces in a straight line."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | move | self to position [position is straight_line] |  |  | amount=event_amount |  |


### Card 757444 (gwent), tagged from: rule count_payoff | if amount_count | unit/-/all | board | turn_end | gives

**Imperial Fleet**
Card text: "Zeal. Order: Infuse an enemy unit with "At the end of your turn, damage self for each active Flanking unit on the opposite row". Charge: 1"

Keywords (their own rows are on the keyword entries): Zeal, Charge, Order

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Zeal |  | permanent |
| always |  | and | give_keyword | self |  | Charge | amount=1 | permanent |
| activated of self |  |  | give_ability | chosen enemy unit in board |  | Infused |  |  |


Keyword entry:
**Zeal**
Card text: "An Order ability can be used on the same turn the card is placed on the battlefield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | can | self |  |  | event=activated | this_round |


Keyword entry:
**Charge**
Card text: "The number of times an Order ability can be used. Only cards with Charge: X can gain additional Charges."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | self |  |  | event=activated, times=listed | while |


Keyword entry:
**Order**
Card text: "An ability triggered manually by the player. Cards with Order cannot be used for 1 turn after being placed on the battlefield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | cant | self |  |  | event=activated, turns=1 | n_turns |


Keyword entry:
**Infused**
Card text: "Status that adds effects or categories to a card. Removing the status also removes all added effects and categories. Lock disables Infused abilities."

(no rows of its own)


### Card 4000225 (inscryption), tagged from: rule count_payoff | if amount_count | position/mine/- | board | played(self) | own

**The Limoncello**
Card text: "Keywords: Mighty Leap, Omni Strike, Made Of Stone, Uncuttable. Traits: Giant. Special behaviour: When a card is spawned on the board, it replaces all spaces on opponent's side of the board with itself. When a card perishes, it clears all spaces on opponent's side of the board. Once a card has less than 70 Health, each turn one Skeleton Crew per 5 damage taken since last turn will drop onto player's side of the board (if there are free slots)."

Keywords (their own rows are on the keyword entries): Mighty Leap, Omni Strike, Made Of Stone, Uncuttable

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_start by enemy player | stat self health lt 70 |  | summon |  to enemy position [state is empty] |  | Skeleton Crew | amount=event_amount |  |
| played of self |  |  | stat_set | self |  |  | size=count of (mine position in board) | while |


Keyword entry:
**Mighty Leap**
Card text: "Rulebook: A card bearing this sigil will block an opposing creature bearing the Airborne sigil. | speaker = Rule Book"

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | self to enemy unit [keyword is Airborne] |  |  | event=blocks | while |


Keyword entry:
**Omni Strike**
Card text: "Rulebook: A card bearing this sigil will strike each opposing space that is occupied by a creature. It will strike directly if no creatures oppose it."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| attacks by self |  |  | strike | self to all enemy unit in board |  |  |  |  |
| attacks by self |  | or | strike | self to enemy player |  |  |  |  |


Keyword entry:
**Made Of Stone**
Card text: "Rulebook: A card bearing this sigil is immune to the effects of Touch of Death and Stinky."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | cant | self |  | Touch of Death | event=keyword_used | while |
| always |  | and | cant | self |  | Stinky | event=keyword_used | while |


Keyword entry:
**Uncuttable**
Card text: "Uncuttable is a trait. Cards posessing the Uncuttable trait cannot be cut with Scissors, skinned by the Skinning Knife (in Kaycee's Mod) or stolen with the Fish Hook. Even though the Forced Death events in Act I summon many Grizzlys which are intended to be impassable, they are still cuttable."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| targeted by equipment [card in Scissors] [card in Skinning Knife] [card in Fish Hook] of self |  |  | counter | it effect |  |  |  |  |


Card it names or makes:
**Skeleton Crew**
Card text: "Keywords: Brittle."

Keywords (their own rows are on the keyword entries): Brittle

(no rows of its own)


### Card 8000678 (marvel_snap), tagged from: rule count_payoff | if amount_count | position/-/all | - | played(self) | own

**Ultron Soul Stone**
Card text: "On Reveal: For each of your full locations, give one of your cards there +3 Power."

Keywords (their own rows are on the keyword entries): On Reveal

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stat_change | count of (all position [count ge 4]) chosen mine unit in board |  |  | power=3 | permanent |


Keyword entry:
**On Reveal**
Card text: "Acts once, when the card is turned face up on the board: after it is played, and also when a location or card puts it there, unless something stops On Reveal (Cosmo)."

(no rows of its own)



## Family: concept `defence_gain` ("Defence gain (+health)"), from rows `do stat_change`
- Counts as defence_gain: A unit's health, toughness, defence or armour stat goes up: +2 health, +0/+2, gain plated armor.
- Not defence_gain: Attack going up is attack_gain; block points that wear off are block_armor; healing lost health is heal; on the player it is player_defence_gain.
- Why the script suspects it: lowers a stat: that is stat_loss

### Card 757196 (gwent), tagged from: rule defence_gain | do stat_change | unit/mine/all | deck | activated(self) | own

**Erland of Larvik**
Card text: "Deploy: Boost all units in your deck by 1. Adrenaline 3: Also gain Immunity. Order: Remove boosts from all units in your deck, then boost this unit by the same amount."

Keywords (their own rows are on the keyword entries): Order, Deploy, Adrenaline

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stat_change | all mine unit in deck |  |  | strength=1 | permanent |
| played of self | keyword_condition Adrenaline 3 |  | give_keyword | self |  | Immunity |  | permanent |
| activated of self |  |  | stat_change | all mine unit in deck |  |  | strength=minus (stat boost of (all mine unit in deck)) | permanent |
| activated of self |  | then | stat_change | self |  |  | strength=event_amount | permanent |


Keyword entry:
**Order**
Card text: "An ability triggered manually by the player. Cards with Order cannot be used for 1 turn after being placed on the battlefield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | cant | self |  |  | event=activated, turns=1 | n_turns |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)


Keyword entry:
**Adrenaline**
Card text: "Trigger this ability if you have specified number or fewer cards in your hand. Cards with Adrenaline are highlighted when their effect is stronger."

(no rows of its own)


Keyword entry:
**Immunity**
Card text: "Status whereby this card cannot be manually targeted."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | cant | all player to self |  |  | event=targeted | while |



## Family: concept `draw` ("Draw cards"), from rows `do draw`
- Counts as draw: Cards are drawn from the owner's deck into hand.
- Not draw: Searching the deck for a chosen kind of card is tutor; making a new card is generate_cards.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 5001059 (duelyst), tagged from: row | do draw | card/enemy/- | deck_top | played | own

**Seismoid**
Card text: "Whenever you summon a Mech minion from your action bar, both players draw a card."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of mine unit in board [type is Mech] |  |  | draw | mine card in deck_top |  |  | amount=1 |  |
| played of mine unit in board [type is Mech] |  | and | draw | enemy card in deck_top |  |  | amount=1 |  |


### Card 741116 (faeria), tagged from: row | do draw | card/enemy/- | deck_top | dies(self) | own

**Hunted Outlaw**
Card text: "Last Words - Your opponent draws a card and gains 2 faeria."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| dies of self |  |  | draw | enemy card in deck_top |  |  | amount=1 |  |
| dies of self |  | and | mana_gain | enemy player |  |  | amount=2 |  |


### Card 756545 (gwent), tagged from: row | do draw | unit/enemy/- | deck | countdown_done(self) | own

**Stregobor**
Card text: "Timer 2 (Ranged): Each player draws a unit and sets its power to 1."

Keywords (their own rows are on the keyword entries): Timer

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Timer | amount=2 | permanent |
| countdown_done of self | keyword_condition Ranged |  | draw | mine unit in deck |  |  | amount=1 |  |
| countdown_done of self | keyword_condition Ranged | then | stat_set | it |  |  | strength=1 |  |
| countdown_done of self | keyword_condition Ranged | and | draw | enemy unit in deck |  |  | amount=1 |  |
| countdown_done of self | keyword_condition Ranged | then | stat_set | it |  |  | strength=1 |  |


Keyword entry:
**Timer**
Card text: "Before the end of your turn, lower the number by 1. When the number reaches 0, trigger the ability."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_end by mine player |  |  | countdown_advance | self |  |  | amount=1 |  |


### Card 796327 (marvel_snap), tagged from: row | do draw | card/enemy/- | deck_top | played | own

**The Abbey**
Card text: "First to put exactly 2 cards here draws a card."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of mine unit [position is same_lane] [once_per_game] | count mine unit in board [position is same_lane] eq 2; count enemy unit in board [position is same_lane] lt 2 |  | draw | mine card in deck_top |  |  | amount=1 |  |
| played of enemy unit [position is same_lane] [once_per_game] | count enemy unit in board [position is same_lane] eq 2; count mine unit in board [position is same_lane] lt 2 |  | draw | enemy card in deck_top |  |  | amount=1 |  |


### Card 751124 (runeterra), tagged from: row | do draw | card/enemy/bottom | deck_bottom | activated | uses_keyword Nab

**Loaded Dice**
Card text: "Next round, when you damage the enemy Nexus, Nab 1."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | give_ability | mine player |  |  |  | next_round |



## Family: concept `free_play` ("Put into play for free"), from rows `do play_card`
- Counts as free_play: A card enters play without its cost being paid, by an effect or automatically.
- Not free_play: A dead unit coming back is revive.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 756538 (gwent), tagged from: row | do play_card | unit/enemy/chosen | discard | played(self) | own

**Hanmarvyn's Blue Dream**
Card text: "Play a unit from your opponent's graveyard with a provision cost of 9 or less and give it Doomed."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | play_card | chosen enemy unit in discard [cost le 9] |  |  |  |  |
| played of self |  | and | give_keyword | it |  | Doomed |  | permanent |


Keyword entry:
**Doomed**
Card text: "Status that removes the card from the game after it leaves the battlefield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| leaves_play of self |  |  | obliterate | self |  |  |  |  |


### Card 900033 (runeterra), tagged from: row | do play_card | card/enemy/chosen | - | played(self) | own

**Prank**
Card text: "Keywords: Focus. Pick 1 of 2 non-champion cards from the enemy hand or deck and Prank it."

Keywords (their own rows are on the keyword entries): Focus

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | play_card | 1 chosen enemy card [category not champion] |  | Prank |  |  |


Keyword entry:
**Focus**
Card text: "Can be played outside combat or when no other spells or skills are pending. Happens instantly and allows you to continue to play other cards."

(no rows of its own)


### Card 756480 (gwent), tagged from: row | do play_card | card/enemy/- | deck_top | played(self) | own

**Cantarella**
Card text: "Disloyal. Deploy: Play the top card from your opponent's deck."

Keywords (their own rows are on the keyword entries): Disloyal, Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Disloyal |  | permanent |
| played of self |  |  | play_card | enemy card in deck_top |  |  |  |  |


Keyword entry:
**Disloyal**
Card text: "This card is played on the opposite side of the battlefield, then gains Spying."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | self to enemy position |  |  | event=summoned | while |
| played of self |  |  | give_keyword | self |  | Spying |  | permanent |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)


### Card 751131 (runeterra), tagged from: row | do play_card | unit/enemy/random | board | played(self) | own

**Ruined Rex**
Card text: "Play: Play Cannon Barrage on randomly targeted enemies for each card you've drawn this round, up to 6 times."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | play_card | random enemy unit in board |  | Cannon Barrage | times=event_count of (drawn by mine player) this_round, max=6 |  |


Card it names or makes:
**Cannon Barrage**
Card text: "Keywords: Skill. Deal 2 to a unit. If it's dead or gone, deal 1 to the enemy Nexus instead."

Keywords (their own rows are on the keyword entries): Skill

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | chosen unit in board |  |  | amount=2 |  |
| played of self |  | otherwise | damage | enemy player |  |  | amount=1 |  |


### Card 756794 (gwent), tagged from: row | do play_card | card/enemy/it | - | played(self) | own

**Duchess' Informant**
Card text: "Disloyal. Deploy: Spawn and play a base copy of a non-Disloyal bronze enemy unit."

Keywords (their own rows are on the keyword entries): Disloyal, Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Disloyal |  | permanent |
| played of self |  |  | copy | enemy unit [state is bronze] [keyword not Disloyal] [state is created] | hand |  |  |  |
| played of self |  | then | play_card | it card |  |  |  |  |


Keyword entry:
**Disloyal**
Card text: "This card is played on the opposite side of the battlefield, then gains Spying."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | self to enemy position |  |  | event=summoned | while |
| played of self |  |  | give_keyword | self |  | Spying |  | permanent |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)


