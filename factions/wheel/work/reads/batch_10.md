# Tag reading, batch 10


## Family: concept `stat_gain` ("Stat gain (+power, +health)"), from rows `do stat_change`
- Counts as stat_gain: A unit's power, attack, health or other stat goes up, or is set or swapped to a higher value.
- Not stat_gain: Gaining only a keyword is that keyword's concept (evasion, first_strike...); a lasting rise each turn is permanent_growth.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 5000889 (duelyst), tagged from: row | do stat_change | unit/enemy/chosen | board | played(self) | own

**Void Steal**
Card text: "Give an enemy minion -3 Attack. Nearby friendly minions gain +3 Attack."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stat_change | chosen enemy unit in board |  |  | power=-3 | permanent |
| played of self |  | and | stat_change | all mine unit in board [position is surrounding] |  |  | power=3 | permanent |


### Card 757379 (gwent), tagged from: row | do stat_change | unit/enemy/chosen | board | played(self) | own

**Buhurt**
Card text: "Boost an enemy unit by 3, then an allied unit by 9."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stat_change | chosen enemy unit in board |  |  | strength=3 | permanent |
| played of self |  | then | stat_change | chosen mine unit in board |  |  | strength=9 | permanent |


### Card 4000027 (inscryption), tagged from: row | do stat_change | unit/enemy/- | board | always | has_keyword Annoying

**Alarm Bot**
Card text: "Keywords: Annoying."

Keywords (their own rows are on the keyword entries): Annoying

(no rows of its own)


Keyword entry:
**Annoying**
Card text: "Rulebook: The creature opposing a card bearing this sigil gains 1 Power."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | stat_change | enemy unit in board [position is same_lane] |  |  | power=1 | while |


### Card 761013 (into_the_breach), tagged from: row | do stat_change | unit/enemy/all | board | always | own

**Soldier Psion**
Card text: "Health 2, move 2. Weapons/skills: Invigorating Spores: All other Vek receive +1 HP as long as the Psion is living.. Special: Flying: Flying units can move over any terrain tile.. The jellyfish-like Psions act as support units, providing passive bonuses to the Vek. The Soldier Psion is distinguished by its pale blue coloration and bright green cranial nodes. This Psion provides a health bonus to all other Vek units on the field. Under Psionic Receiver, all of the players Mechs will gain an additional +1 HP while the Solider Psion is alive."

Keywords (their own rows are on the keyword entries): Flying

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | stat_change | all enemy unit in board [card not Soldier Psion] |  |  | health=1 | while |
| always | have mine card [card is Psionic Receiver] is |  | stat_change | all mine unit [type is Mech] [card not Soldier Psion] |  |  | health=1 | while |
| always |  |  | give_keyword | self |  | Flying |  | permanent |


Keyword entry:
**Flying**
Card text: "Flying units can be positioned at any terrain tile, except mountains and other units. Mountains and unfriendly units can be overflown. Flying mechs cannot be waterlogged, and all flying units are not affected by lava or A.C.I.D. tiles, because they don't submerge. Flying units are not immune to A.C.I.D. pools, fire, or emerging Vek."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | self to position [terrain not mountain] [state is empty] |  |  | event=moves | while |
| always |  | and | cant | self |  | Submerged | event=given_keyword | while |
| always |  | and | cant | self |  | A.C.I.D. | event=given_keyword | while |


### Card 8000687 (marvel_snap), tagged from: row | do stat_change | unit/enemy/chosen | board | played(self) | own

**Vampire Enchantress**
Card text: "On Reveal: For each different Cost among your cards in play, steal 1 Power from an enemy card here."

Keywords (their own rows are on the keyword entries): On Reveal

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stat_change | chosen enemy unit in board [position is same_lane] |  |  | power=minus (distinct cost of (all mine unit in board)) | permanent |
| played of self |  | then | stat_change | self |  |  | power=distinct cost of (all mine unit in board) | permanent |


Keyword entry:
**On Reveal**
Card text: "Acts once, when the card is turned face up on the board: after it is played, and also when a location or card puts it there, unless something stops On Reveal (Cosmo)."

(no rows of its own)



## Family: concept `stat_gain` ("Stat gain (+power, +health)"), from rows `do stat_change`
- Counts as stat_gain: A unit's power, attack, health or other stat goes up, or is set or swapped to a higher value.
- Not stat_gain: Gaining only a keyword is that keyword's concept (evasion, first_strike...); a lasting rise each turn is permanent_growth.
- Why the script suspects it: lowers a stat: that is stat_loss

### Card 5000186 (duelyst), tagged from: row | do stat_change | any/enemy/chosen | board | played(self) | own

**Blood Siren**
Card text: "Opening Gambit: Give a nearby enemy -2 attack this turn."

Keywords (their own rows are on the keyword entries): Opening Gambit

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stat_change | chosen enemy any in board [position is surrounding] |  |  | power=-2 | this_round |


Keyword entry:
**Opening Gambit**
Card text: "Triggers an effect when summoned from your action bar."

(no rows of its own)


### Card 741288 (faeria), tagged from: row | do stat_change | unit/enemy/all | board | played(self) | own

**Azarai, Wrath of the Desert**
Card text: "Flying, Charge 2 Gift - Azarai drains 2 Attack from each enemy creature."

Keywords (their own rows are on the keyword entries): Flying, Charge

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Flying |  | permanent |
| always |  | and | give_keyword | self |  | Charge | amount=2 | permanent |
| played of self |  |  | stat_change | all enemy unit in board |  |  | power=-2 | permanent |
| played of self |  | then | stat_change | self |  |  | power=product (2 + count of (all enemy unit in board)) | permanent |


Keyword entry:
**Flying**
Card text: "Can move over ocean and land, but not through creatures or structures."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | self to position [terrain in ocean] [terrain in land] |  |  | event=moves | while |


Keyword entry:
**Charge**
Card text: "Can move several spaces in a straight line."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | self to position [position is straight_line] |  |  | event=moves | while |


### Card 756718 (gwent), tagged from: row | do stat_change | leader_ability/mine/it | - | stat_changed(self) | own

**Royal Inspiration**
Card text: "Order: Boost an allied unit by 5. If it triggered an allied unit's Grace ability, refresh the Order and reduce the boost by 1. This ability adds 17 provisions to your deck's provisions limit."

Keywords (their own rows are on the keyword entries): Order

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated of self |  |  | stat_change | chosen mine unit in board |  |  | strength=5 | permanent |
| stat_changed of self | it_matches [keyword is Grace] |  | refresh | mine leader_ability |  |  |  |  |
| stat_changed of self | it_matches [keyword is Grace] | then | stat_change | it |  |  | strength=-1 | permanent |


Keyword entry:
**Order**
Card text: "An ability triggered manually by the player. Cards with Order cannot be used for 1 turn after being placed on the battlefield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | cant | self |  |  | event=activated, turns=1 | n_turns |


### Card 4000181 (inscryption), tagged from: row | do stat_change | unit/enemy/- | board | always | has_keyword Stinky

**Stinkbug**
Card text: "Keywords: Stinky."

Keywords (their own rows are on the keyword entries): Stinky

(no rows of its own)


Keyword entry:
**Stinky**
Card text: "Rulebook: The creature opposing a card bearing this sigil loses 1 Power."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | stat_change | enemy unit in board [position is same_lane] |  |  | power=-1 | while |


### Card 8000482 (marvel_snap), tagged from: row | do stat_change | unit/enemy/highest | board | played(self) | own

**Remote Mines**
Card text: "On Reveal: Afflict the 2 highest-Power enemy cards here with -2 Power."

Keywords (their own rows are on the keyword entries): On Reveal

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stat_change | 2 highest enemy unit by power in board [position is same_lane] |  |  | power=-2 | permanent |


Keyword entry:
**On Reveal**
Card text: "Acts once, when the card is turned face up on the board: after it is played, and also when a location or card puts it there, unless something stops On Reveal (Cosmo)."

(no rows of its own)



## Family: concept `summon` ("Summon units / tokens"), from rows `do summon`
- Counts as summon: New units are put onto the owner's side of the board.
- Not summon: Units put on the opponent's side are board_clog; units back from death are revive.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 5000257 (duelyst), tagged from: row | do summon | unit/enemy/it | - | played(self) | own

**Mind Steal**
Card text: "Steal a random minion from your opponent's deck and summon it."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | steal | random enemy unit in deck |  |  |  |  |
| played of self |  | then | summon | it |  |  |  |  |


### Card 756998 (gwent), tagged from: row | do summon | unit/enemy/it to mine | board | played(self) | own

**Zoltan: Warrior**
Card text: "Deploy: Damage 2 enemy units by 3. For each unit that survived, Spawn a Rowdy Dwarf on this row. Barricade: At the end of your turn, damage a random enemy unit by 1."

Keywords (their own rows are on the keyword entries): Deploy, Barricade

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | 2 chosen enemy unit in board |  |  | amount=3 |  |
| played of self |  | for_each | summon | it enemy unit in board [state is damaged] to mine position [position is same_row] |  | Rowdy Dwarf |  |  |
| turn_end by mine player | keyword_condition Barricade |  | damage | random enemy unit in board |  |  | amount=1 |  |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)


Keyword entry:
**Barricade**
Card text: "Trigger this ability if the unit has armor."

(no rows of its own)


Card it names or makes:
**Rowdy Dwarf**
Card text: "Doomed."

Keywords (their own rows are on the keyword entries): Doomed

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Doomed |  | permanent |


### Card 761154 (into_the_breach), tagged from: row | do summon | unit/enemy/- | board | turn_start | own

**Emerging**
Card text: "Vek will emerge here next turn. Any unit blocking this space will take one damage."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_start [next_time] |  |  | summon | enemy unit to position [position is same_space] | board |  |  |  |
| turn_start [next_time] |  | and | damage | all unit [position is same_space] |  |  | amount=1 |  |


### Card 1000060 (stormbound), tagged from: row | do summon | unit/enemy/- | - | dies(self) | own

**Dubious Hags**
Card text: "On death, spawn a 1 strength enemy Raven on a random bordering tile"

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| dies of self |  |  | summon | enemy unit to random position [position is bordering] |  | Token Ravens | strength=1 |  |


Card it names or makes:
**Token Ravens**
Card text: ""

(no rows of its own)


### Card 5000191 (duelyst), tagged from: row | do summon | unit/enemy/random | deck | dies(self) | own

**Reaper of the Nine Moons**
Card text: "Keywords: Flying. Dying Wish: Summon a random minion from the opponent's deck on this space."

Keywords (their own rows are on the keyword entries): Flying, Dying Wish

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| dies of self |  |  | summon | random enemy unit in deck to position [position is same_space] |  |  |  |  |


Keyword entry:
**Flying**
Card text: "Move anywhere on the battlefield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | self to position |  |  | event=moves | while |


Keyword entry:
**Dying Wish**
Card text: "Triggers an effect when this minion dies."

(no rows of its own)



## Family: concept `summon` ("Summon units / tokens"), from rows `do summon`
- Counts as summon: New units are put onto the owner's side of the board.
- Not summon: Units put on the opponent's side are board_clog; units back from death are revive.
- Why the script suspects it: helps the enemy: acts on an enemy; helps the enemy: puts it on the enemy side

### Card 756467 (gwent), tagged from: row | do summon | unit/enemy/top to enemy | deck | played(self) | own

**Vilgefortz**
Card text: "Deploy (Melee): Destroy an enemy unit, then your opponent Summons the top bronze unit from their deck to their random row. Deploy (Ranged): Destroy an allied unit, then Summon the top unit from your deck to a random allied row."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self | keyword_condition Melee |  | kill | chosen enemy unit in board |  |  |  |  |
| played of self | keyword_condition Melee | then | summon | top enemy unit in deck [state is bronze] to random enemy position |  |  |  |  |
| played of self | keyword_condition Ranged |  | kill | chosen mine unit in board |  |  |  |  |
| played of self | keyword_condition Ranged | then | summon | top mine unit in deck to random mine position |  |  |  |  |


### Card 796300 (marvel_snap), tagged from: row | do summon | card/enemy/random to enemy | hand | round_end | own

**Sakaar**
Card text: "After this turn, put a card from each player's hand here."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| round_end [next_time] |  |  | summon | random mine card in hand to mine position [position is same_lane] |  |  |  |  |
| round_end [next_time] |  | and | summon | random enemy card in hand to enemy position [position is same_lane] |  |  |  |  |


### Card 813631 (gwent), tagged from: row | do summon | unit/enemy/- to enemy | - | played(self) | own

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


### Card 8000219 (marvel_snap), tagged from: row | do summon | card/enemy/random to enemy | deck | played(self) | own

**Gladiator**
Card text: "On Reveal: Add a card from your opponent's deck to their side of this location. If it has less Power, destroy it."

Keywords (their own rows are on the keyword entries): On Reveal

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | summon | random enemy card in deck to enemy position [position is same_lane] |  |  |  |  |
| played of self |  | if_done | kill | it enemy unit in board [power lt stat power of (self)] |  |  |  |  |


Keyword entry:
**On Reveal**
Card text: "Acts once, when the card is turned face up on the board: after it is played, and also when a location or card puts it there, unless something stops On Reveal (Cosmo)."

(no rows of its own)


### Card 757286 (gwent), tagged from: row | do summon | unit/enemy/top to enemy | deck | played(self) | own

**The Scoundrel**
Card text: "Deploy: Summon the top bronze unit from your opponent's deck to the opposite row, then place a Bounty on it. Tribute 2: Choose a bronze unit to Summon instead, then place a Bounty on it. Fee 1: Damage the enemy unit with a Bounty by 1."

Keywords (their own rows are on the keyword entries): Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | summon | top enemy unit in deck [state is bronze] to enemy position [position is opposite_row] |  |  |  |  |
| played of self |  | then | give_keyword | it |  | Bounty |  | permanent |
| played of self |  |  | spend_mana | mine secondary_resource |  |  | amount=2 |  |
| played of self |  | then | summon | chosen enemy unit in deck [state is bronze] to enemy position [position is opposite_row] |  |  |  |  |
| played of self |  | then | give_keyword | it |  | Bounty |  | permanent |
| activated of self |  |  | spend_mana | mine secondary_resource |  |  | amount=1 |  |
| activated of self |  | then | damage | chosen enemy unit in board [keyword is Bounty] |  |  | amount=1 |  |


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


