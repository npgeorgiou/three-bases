# Tag reading, batch 11


## Family: concept `summon` ("Summon units / tokens"), from rows `do summon`
- Counts as summon: New units are put onto the owner's side of the board.
- Not summon: Units put on the opponent's side are board_clog; units back from death are revive.
- Why the script suspects it: helps the enemy: puts it on the enemy side

### Card 813630 (gwent), tagged from: row | do summon | -/-/- to enemy | - | played(self) | own

**Usurper: General**
Card text: "Deploy: Spawn an Operative on each enemy row and give them Spying. Zeal. Order: Seize all Spying Operatives. Devotion: At the start of the round, while in hand or deck, evolve."

Keywords (their own rows are on the keyword entries): Zeal, Order, Deploy, Devotion

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | summon |  to all enemy position |  | Operative |  |  |
| played of self |  | and | give_keyword | it |  | Spying |  | permanent |
| always |  |  | give_keyword | self |  | Zeal |  | permanent |
| activated of self |  |  | keyword_action | all unit in board [keyword is Spying] [card is Operative] |  | Seize |  | unstated |
| round_start | keyword_condition Devotion; have self in hand |  | transform | self |  |  |  |  |
| round_start | keyword_condition Devotion; have self in deck |  | transform | self |  |  |  |  |


Keyword entry:
**Zeal**
Card text: "An Order ability can be used on the same turn the card is placed on the battlefield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | can | self |  |  | event=activated | this_round |


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
**Devotion**
Card text: "Trigger this ability if your starting deck has no neutral cards."

(no rows of its own)


Card it names or makes:
**Operative**
Card text: "Doomed."

Keywords (their own rows are on the keyword entries): Doomed

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Doomed |  | permanent |


### Card 4000225 (inscryption), tagged from: row | do summon | -/-/- to enemy | - | turn_start | own

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


### Card 796307 (marvel_snap), tagged from: row | do summon | -/-/- to enemy | - | played(self) | own

**Savage Land**
Card text: "Add two Raptors on each side of this location."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | summon |  to mine position [position is same_lane] |  | Raptor | amount=2 |  |
| played of self |  | and | summon |  to enemy position [position is same_lane] |  | Raptor | amount=2 |  |


Card it names or makes:
**Raptor**
Card text: ""

(no rows of its own)


### Card 813631 (gwent), tagged from: row | do summon | -/-/- to enemy | - | played(self) | own

**Usurper: Emperor**
Card text: "Veil. Deploy: Spawn an Operative on each enemy row and give them Spying. Zeal. Order: Seize all Spying Operatives. Whenever an enemy unit gains Spying, boost self by 1."

Keywords (their own rows are on the keyword entries): Veil, Zeal, Order, Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Veil |  | permanent |
| always |  | and | give_keyword | self |  | Zeal |  | permanent |
| always |  |  | give_keyword | self |  | Veil |  | permanent |
| played of self |  |  | summon |  to all enemy position |  | Operative |  |  |
| played of self |  | and | give_keyword | it |  | Spying |  | permanent |
| played of self |  |  | summon | enemy unit to all enemy position |  | Operative |  |  |
| played of self |  | and | give_keyword | it |  | Spying |  | permanent |
| activated of self |  |  | keyword_action | all unit in board [keyword is Spying] [card is Operative] |  | Seize |  | unstated |
| always |  |  | give_keyword | self |  | Zeal |  | permanent |
| given_keyword of enemy unit [keyword is Spying] |  |  | stat_change | self |  |  | strength=1 | permanent |
| activated of self |  |  | keyword_action | all unit in board [card is Operative] [keyword is Spying] |  | Seize |  | unstated |
| given_keyword of enemy unit [keyword is Spying] |  |  | stat_change | self |  |  | strength=1 | permanent |


Keyword entry:
**Veil**
Card text: "Status that prevents unit from gaining other statuses."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | cant | self |  |  | event=given_keyword | while |


Keyword entry:
**Zeal**
Card text: "An Order ability can be used on the same turn the card is placed on the battlefield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | can | self |  |  | event=activated | this_round |


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


Card it names or makes:
**Operative**
Card text: "Doomed."

Keywords (their own rows are on the keyword entries): Doomed

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Doomed |  | permanent |


### Card 4000077 (inscryption), tagged from: row | do summon | -/-/self to enemy | - | played(self) | has_keyword Brood Parasite

**Cuckoo**
Card text: "Keywords: Airborne, Brood Parasite."

Keywords (their own rows are on the keyword entries): Airborne, Brood Parasite

(no rows of its own)


Keyword entry:
**Airborne**
Card text: "Rulebook: A card bearing this sigil will strike an opponent directly, even if there is a creature opposing it."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| attacks by self |  |  | strike | self to enemy player |  |  |  |  |


Keyword entry:
**Brood Parasite**
Card text: "Rulebook: When a card bearing this Sigil is played, an Egg is created on the opposing space.|speaker=Rule Book}}"

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | summon | self to enemy position [position is same_lane] |  | Broken Egg |  |  |



## Family: concept `swap` ("Swap positions"), from rows `do swap`
- Counts as swap: Two units trade places, or trade lanes or locations.
- Not swap: Trading stats is stat_gain or stat_loss; trading hands or decks is hand_deck_swap.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 757017 (gwent), tagged from: row | do swap | card/enemy/- to mine | deck_top | played(self) | own

**Ofiri Merchant**
Card text: "Deploy: Swap the top card of your opponent's deck with yours."

Keywords (their own rows are on the keyword entries): Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | swap | enemy card in deck_top to mine card in deck_top |  |  |  |  |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)


### Card 757292 (gwent), tagged from: row | do swap | card/enemy/chosen to mine | discard | played(self) | own

**Vilgefortz: Renegade**
Card text: "Deploy: Swap a card from your opponent's graveyard with a card in your hand."

Keywords (their own rows are on the keyword entries): Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | swap | chosen enemy card in discard to chosen mine card in hand |  |  |  |  |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)



## Family: concept `tutor` ("Search the deck for a card (tutor)"), from rows `do put_on_top`
- Counts as tutor: The owner searches the deck for a card of a stated kind and takes it.
- Not tutor: Drawing the top card is draw.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 756836 (gwent), tagged from: row | do put_on_top | card/enemy/it | - | played(self) | own

**Courier**
Card text: "Deploy (Melee): Look at the top 3 cards from your opponent's deck and move one to the top. Deploy (Ranged): Look at the top 3 cards from your deck and move one to the top."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self | keyword_condition Melee |  | look | 3 enemy card in deck_top |  |  |  |  |
| played of self | keyword_condition Melee | then | choose_card | chosen enemy card in deck_top |  |  |  |  |
| played of self | keyword_condition Melee | then | put_on_top | it card |  |  |  |  |
| played of self | keyword_condition Melee |  | look | 3 top enemy card in deck |  |  |  |  |
| played of self | keyword_condition Melee | then | put_on_top | chosen enemy card in deck |  |  |  |  |
| played of self | keyword_condition Ranged |  | look | 3 mine card in deck_top |  |  |  |  |
| played of self | keyword_condition Ranged | then | choose_card | chosen mine card in deck_top |  |  |  |  |
| played of self | keyword_condition Ranged | then | put_on_top | it card |  |  |  |  |
| played of self | keyword_condition Ranged |  | look | 3 top mine card in deck |  |  |  |  |
| played of self | keyword_condition Ranged | then | put_on_top | chosen mine card in deck |  |  |  |  |


### Card 751421 (runeterra), tagged from: row | do put_on_top | unit/enemy/chosen | board | played(self) | own

**Keeper's Verdict**
Card text: "Place an enemy unit on top of the enemy deck."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | put_on_top | chosen enemy unit in board | deck_top |  |  |  |


### Card 756632 (gwent), tagged from: row | do put_on_top | unit/enemy/chosen to mine | board | played(self) | own

**Yennefer's Invocation**
Card text: "Move an enemy unit to the top of your deck."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | put_on_top | chosen enemy unit in board to mine player |  |  |  |  |


### Card 796907 (runeterra), tagged from: row | do put_on_top | unit/enemy/chosen | board | played(self) | own

**Poppy's Keeper's Verdict**
Card text: "Keywords: Slow. Place an enemy unit on top of the enemy deck. Create a Poppy in your deck."

Keywords (their own rows are on the keyword entries): Slow

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | put_on_top | chosen enemy unit in board | deck_top |  |  |  |
| played of self |  | and | create |  | deck | Poppy |  |  |


Keyword entry:
**Slow**
Card text: "Can be played outside of combat when no spells or skills are pending. Happens after your opponent has a chance to react."

(no rows of its own)


Card it names or makes:
**Poppy**
Card text: "Attack: Grant allies with equal or less power than me +1|+1. Level up: I've attacked with allies 3 times."

Keywords (their own rows are on the keyword entries): Attack

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| attacks by self |  |  | stat_change | all mine unit in board [power le stat power of (self)] |  |  | power=1, health=1 | permanent |
| always | event_count attacks by self ge 3 this_game |  | level_up | self |  |  |  |  |



## Family: concept `untap` ("Ready a used unit again (untap)"), from rows `do ready`
- Counts as untap: A used or tapped unit or card is readied so it can act again.
- Not untap: A whole extra turn is extra_turn.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 5000875 (duelyst), tagged from: row | do ready | unit/enemy/it | - | played(self) | own

**Psychic Conduit**
Card text: "Reactivate and take control of an enemy minion with 2 or less Attack until end of turn."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | steal | chosen enemy unit in board [power le 2] |  |  |  | this_round |
| played of self |  | and | ready | it |  |  |  |  |


