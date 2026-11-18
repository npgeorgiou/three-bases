# Tag reading, batch 01


## Family: concept `attack_gain` ("Attack gain (+attack)"), from rows `do give_keyword`
- Counts as attack_gain: A unit's attack, damage, power or strength goes up: +2 attack, +1/+0, gain strength.
- Not attack_gain: Health, defence or armour going up is defence_gain; a bonus that raises both (+1/+1) carries both; a bonus whose stat the text does not name stays stat_gain; the player's own strength is player_attack_gain.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 7000134 (sts1), tagged from: row | do give_keyword | unit/enemy/chosen | board | played(self) | own

**Dark Shackles**
Card text: "Keywords: Exhaust. Enemy loses 9 Strength this turn."

Keywords (their own rows are on the keyword entries): Exhaust

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | give_keyword | chosen enemy unit in board |  | Strength | amount=-9 | this_round |


Keyword entry:
**Exhaust**
Card text: "Removed until end of combat."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | exhaust | it |  |  |  |  |


Keyword entry:
**Strength**
Card text: "Strength adds additional damage to attacks."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | increase_effect | all mine spell [type is Attack] |  |  | amount=count of (self keyword [keyword is Strength]) | while |



## Family: concept `buff` ("Make a unit stronger (buff)"), from rows `do give_ability`
- Counts as buff: A unit gains stats or a combat ability it did not have: more power or health, first strike, flying, extra attacks, reach, piercing.
- Not buff: Improving a card still in hand is in_hand_buff; a unit printed with high stats is not buffed.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 5000461 (duelyst), tagged from: row | do give_ability | player/enemy/- | - | dies(self) | own

**Hexclaw**
Card text: "Dying Wish: The enemy General gains, \"At the start of your turn, take 1 damage.\""

Keywords (their own rows are on the keyword entries): Dying Wish

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| dies of self |  |  | give_ability | enemy player |  |  |  |  |


Keyword entry:
**Dying Wish**
Card text: "Triggers an effect when this minion dies."

(no rows of its own)


### Card 751586 (runeterra), tagged from: row | do give_ability | unit/enemy/chosen | board | played(self) | own

**Cracking Ice**
Card text: "Grant an enemy "Frostbite me at the next Round Start.""

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | give_ability | chosen enemy unit in board |  |  |  |  |


### Card 796730 (runeterra), tagged from: row | do give_ability | unit/enemy/it | board | played(self) | own

**Gravitum**
Card text: "Keywords: Slow. Stun an enemy. If it's a follower, Stun it again at the next Round Start. Phase Infernum or Crescendum."

Keywords (their own rows are on the keyword entries): Slow

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stun | chosen enemy unit in board |  |  |  | this_round |
| played of self |  | and | give_ability | it enemy unit in board [category is follower] |  |  |  | permanent |
| played of self |  | and | keyword_action |  |  | Phase |  |  |


Keyword entry:
**Slow**
Card text: "Can be played outside of combat when no spells or skills are pending. Happens after your opponent has a chance to react."

(no rows of its own)


Keyword entry:
**Phase**
Card text: "Pick the next Moon Weapon for Aphelios."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | choose_card | mine card [type is Moon Weapon] |  |  |  |  |



## Family: concept `draw` ("Draw cards"), from rows `do draw`
- Counts as draw: Cards are drawn from the owner's deck into hand.
- Not draw: Searching the deck for a chosen kind of card is tutor; making a new card is generate_cards.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 8000362 (marvel_snap), tagged from: row | do draw | card/enemy/- | deck_top | played(self) | own

**Maximus**
Card text: "On Reveal: Your opponent draws 2 cards."

Keywords (their own rows are on the keyword entries): On Reveal

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | draw | enemy card in deck_top |  |  | amount=2 |  |


Keyword entry:
**On Reveal**
Card text: "Acts once, when the card is turned face up on the board: after it is played, and also when a location or card puts it there, unless something stops On Reveal (Cosmo)."

(no rows of its own)


### Card 8000103 (marvel_snap), tagged from: row | do draw | card/enemy/- | deck_top | played(self) | own

**Crystal**
Card text: "On Reveal: Each player draws a card."

Keywords (their own rows are on the keyword entries): On Reveal

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | draw | mine card in deck_top |  |  | amount=1 |  |
| played of self |  | and | draw | enemy card in deck_top |  |  | amount=1 |  |


Keyword entry:
**On Reveal**
Card text: "Acts once, when the card is turned face up on the board: after it is played, and also when a location or card puts it there, unless something stops On Reveal (Cosmo)."

(no rows of its own)



## Family: concept `free_play` ("Put into play for free"), from rows `do play_card`
- Counts as free_play: A card enters play without its cost being paid, by an effect or automatically.
- Not free_play: A dead unit coming back is revive.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 796502 (runeterra), tagged from: row | do play_card | unit/enemy/it | board | challenges | own

**Lee Sin (level 2)**
Card text: "Keywords: Imbue. When you play a spell, give me Challenger this round. If you play another, give me Barrier this round. I Dragon's Rage enemies that I Challenge."

Keywords (their own rows are on the keyword entries): Imbue

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played by mine player of spell |  |  | give_keyword | self |  | Challenger |  | this_round |
| played by mine player of spell | event_count played by mine player of spell ge 2 this_round |  | give_keyword | self |  | Barrier |  | this_round |
| challenges by self |  |  | play_card | it enemy unit in board |  | Dragon's Rage |  |  |


Keyword entry:
**Imbue**
Card text: "These abilities trigger when you resolve a spell."

(no rows of its own)


Keyword entry:
**Challenger**
Card text: "Can choose which enemy unit blocks."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| attacks by self |  |  | challenge | chosen enemy unit in board |  |  |  |  |


Keyword entry:
**Barrier**
Card text: "Negates the next damage the unit would take. Lasts one round."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| damaged of self |  |  | negate_damage | self |  |  |  | this_round |


Card it names or makes:
**Dragon's Rage**
Card text: "Keywords: Slow. An ally kicks an enemy into the enemy Nexus, striking the enemy then the enemy Nexus. If the enemy survives, Recall it."

Keywords (their own rows are on the keyword entries): Slow

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | strike | chosen mine unit in board to chosen enemy unit in board |  |  |  |  |
| played of self |  | then | strike | it mine unit to enemy player |  |  |  |  |
| played of self |  | if_done | keyword_action | it enemy unit |  | Recall |  | unstated |


### Card 751997 (runeterra), tagged from: row | do play_card | unit/enemy/random | board | played(self) | own

**Volibear**
Card text: "Play: Play Relentless Storm 3 times. Each one targets a different random enemy or the enemy Nexus if none. Level up: Round End: You've dealt 50+ damage."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | play_card | random enemy unit in board |  | Relentless Storm | times=3 |  |
| played of self |  | otherwise | play_card | enemy player |  | Relentless Storm |  |  |
| round_end | event_count damaged by mine player damage ge 50 this_game |  | level_up | self |  |  |  |  |


Card it names or makes:
**Relentless Storm**
Card text: "Keywords: Elemental Skill. Deal 4 to a unit. If it's dead or gone, deal 2 to the enemy Nexus instead."

Keywords (their own rows are on the keyword entries): Elemental Skill

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | chosen unit in board [state not dead_this_round] |  |  | amount=4 |  |
| played of self |  | instead | damage | enemy player |  |  | amount=2 |  |


### Card 796582 (runeterra), tagged from: row | do play_card | unit/enemy/random | board | played(self) | own

**Volibear (level 2)**
Card text: "Keywords: Overwhelm, Missing Translation. Play or Attack: Play Relentless Storm 3 times. Each one targets a different random enemy or the enemy Nexus if none. Other allies have Overwhelm."

Keywords (their own rows are on the keyword entries): Overwhelm

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | play_card | 3 random enemy unit in board |  | Relentless Storm |  |  |
| played of self |  | otherwise | play_card | enemy player |  | Relentless Storm |  |  |
| attacks by self |  |  | play_card | 3 random enemy unit in board |  | Relentless Storm |  |  |
| attacks by self |  | otherwise | play_card | enemy player |  | Relentless Storm |  |  |
| always |  |  | give_keyword | all mine unit in board [card not Volibear (level 2)] |  | Overwhelm |  | while |


Keyword entry:
**Overwhelm**
Card text: "Inflicts damage beyond what would kill the target(s) to the enemy Nexus."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| strikes by self |  |  | excess_damage | enemy player |  |  |  |  |


Card it names or makes:
**Relentless Storm**
Card text: "Keywords: Elemental Skill. Deal 4 to a unit. If it's dead or gone, deal 2 to the enemy Nexus instead."

Keywords (their own rows are on the keyword entries): Elemental Skill

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | chosen unit in board [state not dead_this_round] |  |  | amount=4 |  |
| played of self |  | instead | damage | enemy player |  |  | amount=2 |  |


### Card 750821 (runeterra), tagged from: row | do play_card | unit/enemy/random | board | played(self) | own

**Riptide Rex**
Card text: "Keywords: Plunder. Plunder: Play Cannon Barrage 7 times on randomly targeted enemies."

Keywords (their own rows are on the keyword entries): Plunder

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self | keyword_condition Plunder |  | play_card | random enemy unit in board |  | Cannon Barrage | times=7 |  |


Keyword entry:
**Plunder**
Card text: "A card activates its plunder ability when played if you damaged the enemy Nexus this round."

(no rows of its own)


Card it names or makes:
**Cannon Barrage**
Card text: "Keywords: Skill. Deal 2 to a unit. If it's dead or gone, deal 1 to the enemy Nexus instead."

Keywords (their own rows are on the keyword entries): Skill

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | chosen unit in board |  |  | amount=2 |  |
| played of self |  | otherwise | damage | enemy player |  |  | amount=1 |  |


### Card 757416 (gwent), tagged from: row | do play_card | unit/enemy/chosen | deck | played(self) | own

**Abduction**
Card text: "Echo. Play a unit that isn't from your opponent's starting deck from their deck with a provision cost of 10 or less. Boost it by 1 for each provision below the limit."

Keywords (their own rows are on the keyword entries): Echo

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Echo |  | permanent |
| always |  |  | give_keyword | self |  | Echo |  | permanent |
| played of self |  |  | play_card | chosen enemy unit in deck [cost le 10] [state not started_in_deck] |  |  |  |  |
| played of self |  | and | stat_change | it |  |  | strength=sum (10 + minus (stat cost of (it))) | permanent |
| played of self |  |  | play_card | chosen enemy unit in deck [cost le 10] [state not started_in_deck] |  |  |  |  |
| played of self |  | and | stat_change | it |  |  | strength=sum (10 + minus (stat cost of (it))) | permanent |


Keyword entry:
**Echo**
Card text: "At the beginning of the round, move this card from the graveyard to the top of its owner's deck. Give it Doomed."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| round_start |  |  | put_on_top | self in discard | deck_top |  |  |  |
| round_start |  | then | give_keyword | self |  | Doomed |  | permanent |


### Card 756487 (gwent), tagged from: row | do play_card | unit/enemy/chosen | discard | played(self) | own

**Experimental Remedy**
Card text: "Play a Bronze unit from your opponent's graveyard."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | play_card | chosen enemy unit in discard [state is bronze] |  |  |  |  |


### Card 757293 (gwent), tagged from: row | do play_card | card/enemy/chosen | discard | played(self) | own

**Lydia van Bredevoort**
Card text: "Deploy (Melee): Create and play a bronze special card from your opponent's faction. Deploy (Ranged): Play a bronze special card from your opponent's graveyard."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self | keyword_condition Melee |  | create | chosen mine card in hand [state is bronze] [category is spell] [state is opponent_faction] | hand |  |  |  |
| played of self | keyword_condition Melee | then | play_card | chosen mine card in hand [state is created] | hand |  |  |  |
| played of self | keyword_condition Ranged |  | play_card | chosen enemy card in discard [state is bronze] [category is spell] | discard |  |  |  |



## Family: concept `mark_target` ("Mark a target for later hits"), from rows `do mark`
- Counts as mark_target: A target is marked so that later effects or attacks hit it harder.
- Not mark_target: A lasting stat loss is stat_loss.
- Why the script suspects it: hurts me: acts on my own side

### Card 8000740 (marvel_snap), tagged from: row | do mark | card/mine/chosen | deck | game_start | own

**Zombie Galacti**
Card text: "Game Start: Choose 6 other characters in your deck. On Reveal: Transform those cards into copies of this."

Keywords (their own rows are on the keyword entries): On Reveal

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| game_start |  |  | mark | 6 chosen mine card in deck |  |  |  | permanent |
| played of self |  |  | transform | mine card [state is marked] to self |  |  |  |  |


Keyword entry:
**On Reveal**
Card text: "Acts once, when the card is turned face up on the board: after it is played, and also when a location or card puts it there, unless something stops On Reveal (Cosmo)."

(no rows of its own)


### Card 8000462 (marvel_snap), tagged from: row | do mark | position/mine/chosen | - | drawn(self) | own

**Punisher War Machine**
Card text: "When drawn, mark one of your empty locations. Objective: Win that location +1 Max Energy."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| drawn of self |  |  | mark | chosen mine position [state is empty] |  |  |  | permanent |
| round_end | amount stat power of (mine position [state is marked]) gt stat power of (enemy position [state is marked]) |  | max_mana_change | mine mana |  |  | amount=1 |  |


