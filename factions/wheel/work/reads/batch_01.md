# Tag reading, batch 01


## Family: concept `aoe_damage` ("Damage to many at once"), from rows `do damage`
- Counts as aoe_damage: Damage reaches several units without the player choosing each: around the target, a row, a lane, an area or all. Full or reduced damage both count.
- Not aoe_damage: If the targets are named one by one it is multi_target_attack; random targets are random_target.
- Why the script suspects it: hurts me: acts on my own side

### Card 4000105 (inscryption), tagged from: rule aoe_damage | do damage | unit/mine/all | board | dies | has_keyword Gem Detonator (sigil)

**Gem Detonator**
Card text: "Keywords: Gem Detonator (sigil)."

Keywords (their own rows are on the keyword entries): Gem Detonator (sigil)

(no rows of its own)


Keyword entry:
**Gem Detonator (sigil)**
Card text: "Rulebook: When Gem Vessels on the owner's side of the board die, they Detonate (the creature opposing them, as well as adjacent friendly creatures, are dealt 10 damage)."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| dies of mine unit [name_has is Vessel] |  |  | damage | enemy unit in board [position is same_lane] |  |  | amount=10 |  |
| dies of mine unit [name_has is Vessel] |  | and | damage | all mine unit in board [position is sides] |  |  | amount=10 |  |


### Card 761051 (into_the_breach), tagged from: rule aoe_damage | do damage | unit/mine/all | - | turn_end | own

**Psion Tyrant**
Card text: "Health 2, move 2. Weapons/skills: Hive Targeting: All player units take 1 damage at the end of every turn.. Special: Flying: Flying units can move over any terrain tile.. The Psion Tyrant does not buff Vek and instead damages all player-controlled units every turn, including the Renfield Bomb and deployable tanks. It has a primarily orange body with dark purple bumps adorning its head. Psion Tyrants only spawn on the Volcanic Hive and are capped at one spawn per "phase" of the final mission. Under the Psionic Receiver, the Psion Tyrant also inflicts 1 damage to all Vek, the Tyrant itself included."

Keywords (their own rows are on the keyword entries): Flying

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_end |  |  | damage | all mine unit |  |  | amount=1 |  |
| turn_end | have mine card [card is Psionic Receiver] is |  | damage | all enemy unit |  |  | amount=1 |  |
| always |  |  | give_keyword | self |  | Flying |  | permanent |


Keyword entry:
**Flying**
Card text: "Flying units can be positioned at any terrain tile, except mountains and other units. Mountains and unfriendly units can be overflown. Flying mechs cannot be waterlogged, and all flying units are not affected by lava or A.C.I.D. tiles, because they don't submerge. Flying units are not immune to A.C.I.D. pools, fire, or emerging Vek."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | self to position [terrain not mountain] [state is empty] |  |  | event=moves | while |
| always |  | and | cant | self |  | Submerged | event=given_keyword | while |
| always |  | and | cant | self |  | A.C.I.D. | event=given_keyword | while |


### Card 2000034 (monster_train), tagged from: rule aoe_damage | do damage | unit/mine/all | board | played(self) | own

**Inferno**
Card text: "Piercing. / Deal 100 damage to friendly and enemy units."

Keywords (their own rows are on the keyword entries): Piercing

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Piercing |  | permanent |
| played of self |  |  | damage | all mine unit in board |  |  | amount=100 |  |
| played of self |  | and | damage | all enemy unit in board |  |  | amount=100 |  |


Keyword entry:
**Piercing**
Card text: "Damage dealt by this card ignores armor and shield."

(no rows of its own)


### Card 751967 (runeterra), tagged from: rule aoe_damage | do damage | spell/mine/all | - | activated | uses_keyword Drain

**Chakram Dancer**
Card text: "Keywords: Missing Translation. Play: Deal 1 to anything. Your Skills Drain."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | chosen any |  |  | amount=1 |  |
| always |  |  | keyword_action | all mine spell [category is skill] |  | Drain |  | unstated |


Keyword entry:
**Drain**
Card text: "Heal your Nexus for the amount of damage dealt"

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | damage | it |  |  | amount=event_amount |  |
| activated |  | then | heal | mine player |  |  | amount=event_amount |  |


### Card 4000100 (inscryption), tagged from: rule aoe_damage | do damage | unit/mine/all | board | dies(self) | has_keyword Detonator

**Explode Bot**
Card text: "Keywords: Detonator."

Keywords (their own rows are on the keyword entries): Detonator

(no rows of its own)


Keyword entry:
**Detonator**
Card text: "Detonator is a Sigil that appears in Act II and Act III. When a Card bearing this Sigil dies, all adjacent cards (those to the left, right and front of the card) are dealt 10 damage. This effect doesn't apply for sacrificing a card bearing this Sigil, but destroying it with the hammer does activate the Sigil."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| dies of self |  |  | damage | all mine unit in board [position is sides] |  |  | amount=10 |  |
| dies of self |  | and | damage | enemy unit in board [position is same_lane] |  |  | amount=10 |  |



## Family: concept `attack_gain` ("Attack gain (+attack)"), from rows `do give_keyword`
- Counts as attack_gain: A unit's attack, damage, power or strength goes up: +2 attack, +1/+0, gain strength.
- Not attack_gain: Health, defence or armour going up is defence_gain; a bonus that raises both (+1/+1) carries both; a bonus whose stat the text does not name stays stat_gain; the player's own strength is player_attack_gain.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 7000281 (sts1), tagged from: row | do give_keyword | unit/enemy/all | board | played(self) | own

**Piercing Wail**
Card text: "Keywords: Exhaust. ALL enemies lose 6 Strength this turn."

Keywords (their own rows are on the keyword entries): Exhaust

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | give_keyword | all enemy unit in board |  | Strength | amount=-6 | this_round |


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


### Card 7000419 (sts1), tagged from: row | do give_keyword | unit/enemy/all | board | turn_start | own

**Brimstone**
Card text: "At the start of your turn, gain 2 Strength and ALL enemies gain 1 Strength."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_start by mine player |  |  | give_keyword | mine player |  | Strength | amount=2 | permanent |
| turn_start by mine player |  | and | give_keyword | all enemy unit in board |  | Strength | amount=1 | permanent |


Keyword entry:
**Strength**
Card text: "Strength adds additional damage to attacks."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | increase_effect | all mine spell [type is Attack] |  |  | amount=count of (self keyword [keyword is Strength]) | while |


### Card 7000251 (sts1), tagged from: row | do give_keyword | unit/enemy/chosen | board | played(self) | own

**Malaise**
Card text: "Keywords: Exhaust. Enemy loses X Strength. Apply X Weak."

Keywords (their own rows are on the keyword entries): Exhaust

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | give_keyword | chosen enemy unit in board |  | Strength | amount=minus (x_paid) | permanent |
| played of self |  | and | give_keyword | it enemy unit |  | Weak | amount=x_paid | permanent |


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


Keyword entry:
**Weak**
Card text: "Weakened creatures deal 25% less damage with Attacks."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| damaged by self | it_matches [origin is combat] |  | increase_effect | it |  |  | percent=-25 |  |


### Card 7000152 (sts1), tagged from: row | do give_keyword | unit/enemy/chosen | board | played(self) | own

**Disarm**
Card text: "Keywords: Exhaust. Enemy loses 2 Strength."

Keywords (their own rows are on the keyword entries): Exhaust

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | give_keyword | chosen enemy unit in board |  | Strength | amount=-2 | permanent |


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


### Card 7000518 (sts1), tagged from: row | do give_keyword | unit/enemy/all | board | combat_start | own

**Philosopher's Stone**
Card text: "Gain 1 energy at the start of your turn. ALL enemies start combat with 1 Strength."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_start by mine player |  |  | mana_gain | mine mana |  |  | amount=1 |  |
| combat_start |  |  | give_keyword | all enemy unit in board |  | Strength | amount=1 | permanent |


Keyword entry:
**Strength**
Card text: "Strength adds additional damage to attacks."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | increase_effect | all mine spell [type is Attack] |  |  | amount=count of (self keyword [keyword is Strength]) | while |



## Family: concept `attack_gain` ("Attack gain (+attack)"), from rows `do stat_change`
- Counts as attack_gain: A unit's attack, damage, power or strength goes up: +2 attack, +1/+0, gain strength.
- Not attack_gain: Health, defence or armour going up is defence_gain; a bonus that raises both (+1/+1) carries both; a bonus whose stat the text does not name stays stat_gain; the player's own strength is player_attack_gain.
- Why the script suspects it: lowers a stat: that is stat_loss

### Card 757196 (gwent), tagged from: rule attack_gain | do stat_change | unit/mine/all | deck | activated(self) | own

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


### Card 2000085 (monster_train), tagged from: rule attack_gain | do stat_change | unit/-/chosen | board | always | uses_keyword Sap

**Spike of the Stygian**
Card text: "Consume. / Apply 1 per X Sap and 5 per X Frostbite."

Keywords (their own rows are on the keyword entries): Consume

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Consume |  | permanent |
| played of self |  |  | give_keyword | chosen unit in board |  | Sap | amount=x_paid | permanent |
| played of self |  | and | give_keyword | it |  | Frostbite | amount=x_paid (5) | permanent |


Keyword entry:
**Consume**
Card text: "Can only be played once per battle."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | exhaust | self |  |  |  |  |


Keyword entry:
**Sap**
Card text: "-2 Attack per stack. Decreases every turn."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | stat_change | self |  |  | power=minus (double (count of (self keyword [keyword is Sap]))) | while |
| turn_start by mine player |  |  | remove_keyword | self |  | Sap | amount=1 |  |


Keyword entry:
**Frostbite**
Card text: "Unit takes 1 damage per stack at the end of turn. Decreases every turn."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_end by mine player |  |  | damage | self |  |  | amount=count of (self keyword [keyword is Frostbite]) |  |
| turn_end by mine player |  | then | remove_keyword | self |  | Frostbite | amount=1 |  |


### Card 2000094 (monster_train), tagged from: rule attack_gain | do stat_change | unit/-/chosen | board | always | uses_keyword Sap

**Drain**
Card text: "Apply Sap 3. / Discard a card at random."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | give_keyword | chosen unit in board |  | Sap | amount=3 | permanent |
| played of self |  | and | discard | random mine card in hand |  |  | amount=1 |  |


Keyword entry:
**Sap**
Card text: "-2 Attack per stack. Decreases every turn."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | stat_change | self |  |  | power=minus (double (count of (self keyword [keyword is Sap]))) | while |
| turn_start by mine player |  |  | remove_keyword | self |  | Sap | amount=1 |  |



## Family: concept `buff` ("Make a unit stronger (buff)"), from rows `do copy_keywords`
- Counts as buff: A unit gains stats or a combat ability it did not have: more power or health, first strike, flying, extra attacks, reach, piercing.
- Not buff: Improving a card still in hand is in_hand_buff; a unit printed with high stats is not buffed.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 757067 (gwent), tagged from: row | do copy_keywords | unit/enemy/chosen to enemy | board | played(self) | own

**Van Moorlehem Servant**
Card text: "Deploy: Copy all statuses (excluding Infused) from an enemy unit to another enemy unit. Boost self by the number of status copied that way."

Keywords (their own rows are on the keyword entries): Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | copy_keywords | chosen enemy unit in board to chosen enemy unit in board [state in positive] [state in negative] [keyword not Infused] |  |  |  |  |
| played of self |  | then | stat_change | self |  |  | strength=event_amount | permanent |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)



## Family: concept `buff` ("Make a unit stronger (buff)"), from rows `do give_ability`
- Counts as buff: A unit gains stats or a combat ability it did not have: more power or health, first strike, flying, extra attacks, reach, piercing.
- Not buff: Improving a card still in hand is in_hand_buff; a unit printed with high stats is not buffed.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 5000212 (duelyst), tagged from: row | do give_ability | unit/enemy/chosen | board | played(self) | own

**Grasp of Agony**
Card text: "Choose an enemy minion. When it dies, it deals 3 damage to enemies around it."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | give_ability | chosen enemy unit in board |  |  |  |  |


### Card 751787 (runeterra), tagged from: row | do give_ability | unit/enemy/it | - | played(self) | own

**Test of Spirit**
Card text: "Give an enemy Vulnerable this round. If it dies this round, deal 1 to the enemy Nexus."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | give_keyword | chosen enemy unit in board |  | Vulnerable |  | this_round |
| played of self |  | and | give_ability | it |  |  |  | this_round |


Keyword entry:
**Vulnerable**
Card text: "The enemy can challenge this unit, forcing it to block."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | enemy player to self |  |  | event=challenges | while |


### Card 7000358 (sts1), tagged from: row | do give_ability | unit/enemy/it | - | played(self) | own

**Talk to the Hand**
Card text: "Keywords: Exhaust. Deal 5 damage. Whenever you attack this enemy, gain 2 Block."

Keywords (their own rows are on the keyword entries): Exhaust

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | chosen enemy unit in board |  |  | amount=5 |  |
| played of self |  | and | give_ability | it enemy unit |  |  |  | permanent |


Keyword entry:
**Exhaust**
Card text: "Removed until end of combat."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | exhaust | it |  |  |  |  |


### Card 5000563 (duelyst), tagged from: row | do give_ability | unit/enemy/all | board | played(self) | own

**Superior Mirage**
Card text: "Summon three copies of an enemy minion nearby it. They disappear when attacked."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | copy | chosen enemy unit in board to position [position is surrounding] | board |  | amount=3 |  |
| played of self |  | and | give_ability | all enemy unit in board [state is copy_of_it] |  |  |  |  |


### Card 751235 (runeterra), tagged from: row | do give_ability | unit/enemy/all | board | played(self) | own

**Spirit Fire**
Card text: "Give enemies -2|-0 and "Round End: Deal 2 to me" this round."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stat_change | all enemy unit in board |  |  | power=-2 | this_round |
| played of self |  | and | give_ability | all enemy unit in board |  |  |  | this_round |


