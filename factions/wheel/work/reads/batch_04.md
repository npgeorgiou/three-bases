# Tag reading, batch 04


## Family: concept `generate_cards` ("Create new cards"), from rows `do create`
- Counts as generate_cards: New cards that were not in the deck are put into hand or deck.
- Not generate_cards: Units made on the board are summon.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 741427 (faeria), tagged from: row | do create | card/enemy/- | hand | played(self) | own

**Rapala, the Dopefish**
Card text: "Aquatic Gift - Fill your opponent's hand with Ruby Fish. What an idiot."

Keywords (their own rows are on the keyword entries): Aquatic

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Aquatic |  | permanent |
| played of self |  |  | create | enemy card | hand | Ruby Fish | amount=full |  |


Keyword entry:
**Aquatic**
Card text: "Can only travel over lakes and ocean; drowns at end of turn on other land."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | cant | self to position [terrain not lake] [terrain not ocean] |  |  | event=moves | while |
| turn_end | count position [terrain is land] [terrain not lake] [position is same_space] ge 1 |  | kill | self |  |  |  |  |


Card it names or makes:
**Ruby Fish**
Card text: "Aquatic"

Keywords (their own rows are on the keyword entries): Aquatic

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Aquatic |  | permanent |


### Card 756503 (gwent), tagged from: row | do create | unit/enemy/random | hand | played(self) | own

**Bribery**
Card text: "Create and play a unit from your opponent's starting deck."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | create | random enemy unit [state is started_in_deck] | hand |  |  |  |
| played of self |  | then | play_card | it card |  |  |  |  |


### Card 8000316 (marvel_snap), tagged from: row | do create | card/enemy/- | deck | played(self) | own

**Korg**
Card text: "On Reveal: Shuffle a Rock into your opponent's deck."

Keywords (their own rows are on the keyword entries): On Reveal

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | create | enemy card in deck | deck | Rock |  |  |


Keyword entry:
**On Reveal**
Card text: "Acts once, when the card is turned face up on the board: after it is played, and also when a location or card puts it there, unless something stops On Reveal (Cosmo)."

(no rows of its own)


Card it names or makes:
**Rock**
Card text: ""

(no rows of its own)


### Card 751738 (runeterra), tagged from: row | do create | card/enemy/random | deck | activated | uses_keyword Plant

**Eclectic Collection**
Card text: "For each ally, plant a Mysterious Portal and 3 Chimes in the top 10 cards of your deck and plant a Flashbomb Trap and 3 Poison Puffcaps in the enemy deck."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | keyword_action | 10 top mine card in deck |  | Mysterious Portal Plant | amount=1, times=count of (mine unit in board) |  |
| played of self |  | and | keyword_action | 10 top mine card in deck |  | Chime Plant | amount=3, times=count of (mine unit in board) |  |
| played of self |  | and | keyword_action | random enemy card in deck |  | Flashbomb Trap Plant | amount=1, times=count of (mine unit in board) |  |
| played of self |  | and | keyword_action | random enemy card in deck |  | Poison Puffcap Plant | amount=3, times=count of (mine unit in board) |  |


Keyword entry:
**Plant**
Card text: "Planting adds cards (invisible or trap items such as Poison Puffcaps or Mysterious Portals) into decks."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | create | it | deck |  | amount=event_amount |  |


Card it names or makes:
**Mysterious Portal**
Card text: "Keywords: Boon. Summon a random 2 or 3 cost follower. If your board is full, create a 0 cost Fleeting copy in hand instead."

Keywords (their own rows are on the keyword entries): Boon

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self | count mine unit in board lt 6 |  | summon | random mine unit [category is follower] [cost in 2] [cost in 3] | board |  |  |  |
| played of self | count mine unit in board ge 6 |  | copy | self | hand |  |  |  |
| played of self | count mine unit in board ge 6 | and | give_keyword | it mine unit in board |  | Fleeting |  | permanent |
| played of self | count mine unit in board ge 6 | and | cost_change | it |  |  | cost=minus (stat cost of (self)) | permanent |


Card it names or makes:
**Chime**
Card text: "Keywords: Boon. Grant a random ally in hand +1|+1."

Keywords (their own rows are on the keyword entries): Boon

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stat_change | random mine unit in hand |  |  | power=1, health=1 | permanent |


Card it names or makes:
**Flashbomb Trap**
Card text: "Keywords: Trap. Deal 1 damage to a random ally."

Keywords (their own rows are on the keyword entries): Trap

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | random mine unit in board |  |  | amount=1 |  |


### Card 1000210 (stormbound), tagged from: row | do create | card/enemy/random | deck | played(self) | own

**Malicious Finch**
Card text: "On play, create a random single-use Malicious Card and put it in the enemy’s deck"

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | create | random enemy card [name_has is Malicious] [state is single_use] | deck |  |  |  |



## Family: concept `generate_cards` ("Create new cards"), from rows `do create`
- Counts as generate_cards: New cards that were not in the deck are put into hand or deck.
- Not generate_cards: Units made on the board are summon.
- Why the script suspects it: helps the enemy: puts it on the enemy side

### Card 757417 (gwent), tagged from: row | do create | -/-/- to enemy | deck_bottom | activated(self) | own

**Sandor de Baccalà**
Card text: "Deploy: Shuffle a card from your deck into your opponent's deck. Order: Spawn a Drone at the bottom of your opponent's deck and set its power to the difference between the number of cards in the players' decks. Whenever a card enters or leaves your opponent's deck, boost self by 1."

Keywords (their own rows are on the keyword entries): Order, Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | shuffle_into_deck | chosen mine card in deck to enemy player |  |  |  |  |
| activated of self |  |  | create |  to enemy player | deck_bottom | Drone |  |  |
| activated of self |  | then | stat_set | it |  |  | strength=sum (count of (all mine card in deck) + minus (count of (all enemy card in deck))) |  |
| shuffled of enemy card in deck |  |  | stat_change | self |  |  | strength=1 | permanent |
| removed_from_deck of enemy card in deck |  |  | stat_change | self |  |  | strength=1 | permanent |


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
**Drone**
Card text: "Doomed."

Keywords (their own rows are on the keyword entries): Doomed

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Doomed |  | permanent |



## Family: concept `haste` ("Act the turn it arrives (haste, rush)"), from rows `do can`
- Counts as haste: A unit can attack or act on the turn it is played.
- Not haste: An effect that makes it attack at once is attack_now.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 5000473 (duelyst), tagged from: row | do can | unit/enemy/it | - | played(self) | uses_keyword Rush

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



## Family: concept `haste` ("Act the turn it arrives (haste, rush)"), from rows `do give_keyword`
- Counts as haste: A unit can attack or act on the turn it is played.
- Not haste: An effect that makes it attack at once is attack_now.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 5000473 (duelyst), tagged from: row | do give_keyword | unit/enemy/it | - | played(self) | own

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



## Family: concept `heal` ("Restore health (heal)"), from rows `do heal`
- Counts as heal: Lost health of a unit is restored.
- Not heal: Preventing damage before it happens is protection; the player's life is player_heal.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 761017 (into_the_breach), tagged from: row | do heal | unit/enemy/all | board | turn_start | own

**Blood Psion**
Card text: "Health 2, move 2. Weapons/skills: Regeneration: All other Vek heal 1 at the start of their turn.. Special: Flying: Flying units can move over any terrain tile.. The jellyfish-like Psions act as support units, providing passive bonuses to the Vek. The Blood Psion is distinguished by its pale pink coloration and bright red cranial nodes. This Psion provides a regeneration bonus to all other Vek units on the field. If the Psionic Receiver is active, it will also heal the player units."

Keywords (their own rows are on the keyword entries): Flying

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_start by enemy player |  |  | heal | all enemy unit in board [card not Blood Psion] |  |  | amount=1 |  |
| turn_start by enemy player | have mine card [card is Psionic Receiver] is |  | heal | all mine unit [card not Blood Psion] |  |  | amount=1 |  |
| always |  |  | give_keyword | self |  | Flying |  | permanent |


Keyword entry:
**Flying**
Card text: "Flying units can be positioned at any terrain tile, except mountains and other units. Mountains and unfriendly units can be overflown. Flying mechs cannot be waterlogged, and all flying units are not affected by lava or A.C.I.D. tiles, because they don't submerge. Flying units are not immune to A.C.I.D. pools, fire, or emerging Vek."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | self to position [terrain not mountain] [state is empty] |  |  | event=moves | while |
| always |  | and | cant | self |  | Submerged | event=given_keyword | while |
| always |  | and | cant | self |  | A.C.I.D. | event=given_keyword | while |


### Card 761097 (into_the_breach), tagged from: row | do heal | unit/enemy/all | board | healed | uses_keyword Boost

**Raging Psion**
Card text: "Health 2, move 2. Weapons/skills: Raging Hormones: All other Vek are Boosted, providing +1 damage to attacks.. Special: Flying: Flying units can move over any terrain tile.. Raging Psions are identifiable by their squid-like black body and beige bumps. While alive, they grant all other Vek the boosted effect, increasing their damage by 1. Psions can only spawn once per mission. The Psionic Receiver boosts all mechs when a Raging Psion is present."

Keywords (their own rows are on the keyword entries): Flying

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | all enemy unit in board [card not Raging Psion] |  | Boost |  | while |
| always | have mine card [card is Psionic Receiver] is |  | give_keyword | all mine unit [type is Mech] |  | Boost |  | while |
| always |  |  | give_keyword | self |  | Flying |  | permanent |


Keyword entry:
**Flying**
Card text: "Flying units can be positioned at any terrain tile, except mountains and other units. Mountains and unfriendly units can be overflown. Flying mechs cannot be waterlogged, and all flying units are not affected by lava or A.C.I.D. tiles, because they don't submerge. Flying units are not immune to A.C.I.D. pools, fire, or emerging Vek."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | self to position [terrain not mountain] [state is empty] |  |  | event=moves | while |
| always |  | and | cant | self |  | Submerged | event=given_keyword | while |
| always |  | and | cant | self |  | A.C.I.D. | event=given_keyword | while |


Keyword entry:
**Boost**
Card text: "This unit's damage is increased by 1 on its next attack. Affects all targets of the attack, including self damage. Removed upon any ability use, including non-damaging abilities and repairing; repairing while Boosted will heal 2 points."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| attacks by self [next_time] |  |  | increase_effect | self |  |  | amount=1 |  |
| healed by self |  |  | heal | self |  |  | amount=2 |  |
| attack_done by self |  |  | remove_keyword | self |  | Boost |  |  |
| healed by self |  |  | remove_keyword | self |  | Boost |  |  |


### Card 761052 (into_the_breach), tagged from: row | do heal | unit/enemy/all | board | turn_start | uses_keyword Regeneration

**Psion Abomination**
Card text: "Health 5, move 3. Weapons/skills: Overpowered: All other Vek gain +1 HP, Regeneration, and explode on death.. Special: Flying: Flying units can move over any terrain tile.. The Psion Abomination does not attack but instead grants all other Vek "overpowered", combining the effects of the Soldier Psion, Blood Psion and Blast Psion. No other Psions can spawn if the mission contains a Psion Abomination. It will never replace the 4th island's Psion enemy during Unfair difficulty (unless it is the leader of the island for the HQ mission), nor replace the Psion Tyrant during the Volcanic Hive."

Keywords (their own rows are on the keyword entries): Flying

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | stat_change | all enemy unit in board [card not Psion Abomination] |  |  | health=1 | while |
| always |  | and | give_keyword | all enemy unit in board [card not Psion Abomination] |  | Regeneration |  | while |
| always |  | and | give_keyword | all enemy unit in board [card not Psion Abomination] |  | Explosive Decay |  | while |
| always |  |  | give_keyword | self |  | Flying |  | permanent |


Keyword entry:
**Flying**
Card text: "Flying units can be positioned at any terrain tile, except mountains and other units. Mountains and unfriendly units can be overflown. Flying mechs cannot be waterlogged, and all flying units are not affected by lava or A.C.I.D. tiles, because they don't submerge. Flying units are not immune to A.C.I.D. pools, fire, or emerging Vek."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | self to position [terrain not mountain] [state is empty] |  |  | event=moves | while |
| always |  | and | cant | self |  | Submerged | event=given_keyword | while |
| always |  | and | cant | self |  | A.C.I.D. | event=given_keyword | while |


Keyword entry:
**Regeneration**
Card text: "The Blood Psion is healing all Vek 1 point every turn."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_start |  |  | heal | all enemy unit in board |  |  | amount=1 |  |


Keyword entry:
**Explosive Decay**
Card text: "Explodes on death, dealing 1 damage to adjacent tiles. This damage ignores Armor!"

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| dies of self |  |  | damage | all position [position is bordering] |  |  | amount=1 |  |



## Family: concept `immunity` ("Immune / can't be targeted"), from rows `do cant`
- Counts as immunity: A unit can't be targeted, or is immune to a damage type, effect or condition.
- Not immunity: Hard to block is evasion; hidden until it acts is stealth; the player immune is player_immunity.
- Why the script suspects it: a "can't" row: check it guards my unit

### Card 757095 (gwent), tagged from: row | do cant | unit/-/chosen | board | always | uses_keyword Veil

**Fortune Teller**
Card text: "Deploy (Melee): Give Doomed to a unit. Deploy (Ranged): Give Veil to a unit."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self | keyword_condition Melee |  | give_keyword | chosen unit in board |  | Doomed |  | permanent |
| played of self | keyword_condition Melee |  | give_keyword | chosen unit in board |  | Doomed |  | permanent |
| played of self | keyword_condition Ranged |  | give_keyword | chosen unit in board |  | Veil |  | permanent |
| played of self | keyword_condition Ranged |  | give_keyword | chosen unit in board |  | Veil |  | permanent |


Keyword entry:
**Doomed**
Card text: "Status that removes the card from the game after it leaves the battlefield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| leaves_play of self |  |  | obliterate | self |  |  |  |  |


Keyword entry:
**Veil**
Card text: "Status that prevents unit from gaining other statuses."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | cant | self |  |  | event=given_keyword | while |


### Card 6000104 (into_the_breach), tagged from: row | do cant | -/-/self | - | always | uses_keyword Energy Shield

**Repulse**
Card text: "Push all adjacent tiles. Power: Free. Upgrades: Shield Self (1 Reactor Core): Creates a personal Shield when used; Shield Friendly (2 Reactor Cores): Shield adjacent ally or Building."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| attacks by self |  |  | move | all unit_or_structure [position is bordering] to position [position is bordering] |  |  |  |  |
| attacks by self | upgraded 1 |  | give_keyword | self |  | Energy Shield |  | permanent |
| attacks by self | upgraded 2 |  | give_keyword | all mine unit_or_structure [position is bordering] |  | Energy Shield |  | permanent |


Keyword entry:
**Energy Shield**
Card text: "Shields block damage and prevent new negative status effects (Fire, Freezing, A.C.I.D, etc.). Only direct damage will remove the Shield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| damaged of self |  |  | negate_damage | self |  |  | amount=event_amount |  |
| always |  |  | cant | self to keyword [state is negative] |  |  | event=given_keyword | while |
| damaged of self |  |  | remove_keyword | self |  | Energy Shield |  |  |


### Card 757224 (gwent), tagged from: row | do cant | unit/mine/it | - | always | uses_keyword Veil

**Stolen Mutagens**
Card text: "Choose a mutagen: Red - Damage an enemy unit by 4. Blue - Poison an allied unit and gain 5 Coins. Green - Boost an allied unit by 4 and give it Veil. If you control at least 2 Salamandra units, also choose an additional mutagen."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | choose_one |  |  |  |  |  |
| played of self |  | or | damage | chosen enemy unit in board |  |  | amount=4 |  |
| played of self |  | or | give_keyword | chosen mine unit in board |  | Poison |  | permanent |
| played of self |  | and | mana_gain | mine secondary_resource |  |  | amount=5 |  |
| played of self |  | or | stat_change | chosen mine unit in board |  |  | strength=4 | permanent |
| played of self |  | and | give_keyword | it |  | Veil |  | permanent |
| played of self | count all mine unit in board [type is Salamandra] ge 2 |  | choose_one |  |  |  |  |  |
| played of self | count all mine unit in board [type is Salamandra] ge 2 | or | damage | chosen enemy unit in board |  |  | amount=4 |  |
| played of self | count all mine unit in board [type is Salamandra] ge 2 | or | give_keyword | chosen mine unit in board |  | Poison |  | permanent |
| played of self | count all mine unit in board [type is Salamandra] ge 2 | and | mana_gain | mine secondary_resource |  |  | amount=5 |  |
| played of self | count all mine unit in board [type is Salamandra] ge 2 | or | stat_change | chosen mine unit in board |  |  | strength=4 | permanent |
| played of self | count all mine unit in board [type is Salamandra] ge 2 | and | give_keyword | it |  | Veil |  | permanent |


Keyword entry:
**Poison**
Card text: "Status - if a unit receives two instances of Poison, destroy it."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| given_keyword of self [keyword is Poison] | event_count given_keyword of self [keyword is Poison] ge 2 this_game |  | kill | self |  |  |  |  |


Keyword entry:
**Veil**
Card text: "Status that prevents unit from gaining other statuses."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | cant | self |  |  | event=given_keyword | while |


### Card 6000070 (into_the_breach), tagged from: row | do cant | landmark/mine/all | - | always | uses_keyword Energy Shield

**Phase Cannon**
Card text: "Shoot a projectile that phases through objects (rocks, explosive boulders, Grid Buildings, Mechs and Allied Units excluding Old Earth Dam and mountains). Damage: 1. Power: Free. Upgrades: Phase Shield (1 Reactor Core): Applies a Shield to buildings it passes through; +1 Damage (2 Reactor Cores): Increases damage by 1."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| attacks by self |  |  | damage | nearest enemy unit [position is straight_line] |  |  | amount=1 |  |
| attacks by self | upgraded 1 |  | give_keyword | all mine landmark [position is straight_line] |  | Energy Shield |  | permanent |
| attacks by self | upgraded 2 |  | damage | nearest enemy unit [position is straight_line] |  |  | amount=1 |  |


Keyword entry:
**Energy Shield**
Card text: "Shields block damage and prevent new negative status effects (Fire, Freezing, A.C.I.D, etc.). Only direct damage will remove the Shield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| damaged of self |  |  | negate_damage | self |  |  | amount=event_amount |  |
| always |  |  | cant | self to keyword [state is negative] |  |  | event=given_keyword | while |
| damaged of self |  |  | remove_keyword | self |  | Energy Shield |  |  |


### Card 757130 (gwent), tagged from: row | do cant | -/-/self | - | always | uses_keyword Veil

**Egmund**
Card text: "Veil. Zeal. Order (Melee): Damage an enemy unit by 3. At the end of your turn, if the Order is not used, boost the unit to the right by 1."

Keywords (their own rows are on the keyword entries): Veil, Zeal

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Veil |  | permanent |
| always |  |  | give_keyword | self |  | Zeal |  | permanent |
| activated of self | keyword_condition Melee |  | damage | chosen enemy unit in board |  |  | amount=3 |  |
| turn_end by mine player | event_count activated of self eq 0 this_turn |  | stat_change | right_of_self unit in board |  |  | strength=1 | permanent |


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



## Family: concept `immunity` ("Immune / can't be targeted"), from rows `do give_keyword`
- Counts as immunity: A unit can't be targeted, or is immune to a damage type, effect or condition.
- Not immunity: Hard to block is evasion; hidden until it acts is stealth; the player immune is player_immunity.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 761098 (into_the_breach), tagged from: row | do give_keyword | unit/enemy/all | board | always | own

**Smoldering Psion**
Card text: "Health 2, move 2. Weapons/skills: Burning Carapace: All other Vek are protected from Fire and leave Fire on death.. Special: Flying: Flying units can move over any terrain tile.. Smoldering Psions are identifiable by their squid-like pink body and blue bumps. While alive, it grant all other Vek fire immunity and make them leave a fire tile on death. Psions can only spawn once per mission. The Psionic Receiver grants fire resistance to all mechs under its presence."

Keywords (their own rows are on the keyword entries): Flying

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | all enemy unit in board [card not Smoldering Psion] |  | Fire Immunity |  | while |
| dies of enemy unit [card not Smoldering Psion] |  |  | give_keyword | position [position is same_space] |  | Fire |  | permanent |
| always | have mine card [card is Psionic Receiver] is |  | give_keyword | all mine unit [type is Mech] |  | Fire Immunity |  | while |
| always |  |  | give_keyword | self |  | Flying |  | permanent |


Keyword entry:
**Flying**
Card text: "Flying units can be positioned at any terrain tile, except mountains and other units. Mountains and unfriendly units can be overflown. Flying mechs cannot be waterlogged, and all flying units are not affected by lava or A.C.I.D. tiles, because they don't submerge. Flying units are not immune to A.C.I.D. pools, fire, or emerging Vek."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | self to position [terrain not mountain] [state is empty] |  |  | event=moves | while |
| always |  | and | cant | self |  | Submerged | event=given_keyword | while |
| always |  | and | cant | self |  | A.C.I.D. | event=given_keyword | while |


Keyword entry:
**Fire Immunity**
Card text: "This unit cannot be set on Fire."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | cant | self |  | Fire | event=given_keyword | while |


Keyword entry:
**Fire**
Card text: "Units on Fire take 1 damage at the start of every turn. Repairing removes the effect, so does ending a movement Submerged in Water or in Smoke. Flying units cannot submerge in Water."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_start |  |  | damage | self |  |  | amount=1 |  |
| healed by self |  |  | remove_keyword | self |  | Fire |  |  |
| moves_onto of self [position is same_space] [keyword not Flying] |  |  | remove_keyword | self |  | Fire |  |  |
| moves_onto of self [position is same_space] |  |  | remove_keyword | self |  | Fire |  |  |



## Family: concept `lifesteal` ("Lifesteal / drain"), from rows `do stat_change`
- Counts as lifesteal: Damage dealt also heals or grows the unit that dealt it (Gwent's Drain, Monster Train's Lifesteal).
- Not lifesteal: Healing not tied to damage dealt is heal; life that goes to the player is player_lifesteal.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 757353 (gwent), tagged from: rule lifesteal | do stat_change | unit/enemy/chosen | board | activated | uses_keyword Drain

**Regis: Reborn**
Card text: "Deploy: Drain an enemy unit by 3. At the end of your turn, while in hand or deck, if there is an enemy unit with Bleeding, increase own base power by 1."

Keywords (their own rows are on the keyword entries): Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | keyword_action | chosen enemy unit in board |  | Drain | amount=3 | unstated |
| turn_end by mine player | have enemy unit in board [keyword is Bleeding] |  | base_change | self |  |  | strength=1 |  |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)


Keyword entry:
**Drain**
Card text: "Damage ignoring the target's armor, then boost self by the damage dealt."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | damage | it |  |  | amount=event_amount |  |
| activated |  | then | stat_change | self |  |  | strength=event_amount | permanent |


### Card 756232 (gwent), tagged from: rule lifesteal | do stat_change | unit/enemy/chosen | board | activated | uses_keyword Drain

**Regis: Higher Vampire**
Card text: "Order (Melee): Drain an enemy unit by the amount of boost it has."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated of self | keyword_condition Melee |  | keyword_action | chosen enemy unit in board |  | Drain | amount=stat boost of (it) | unstated |


Keyword entry:
**Drain**
Card text: "Damage ignoring the target's armor, then boost self by the damage dealt."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | damage | it |  |  | amount=event_amount |  |
| activated |  | then | stat_change | self |  |  | strength=event_amount | permanent |


