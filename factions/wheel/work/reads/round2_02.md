# Tag reading, batch 02


## Family: concept `permanent_growth` ("Grows again and again"), from rows `do stat_change`
- Counts as permanent_growth: A unit gains stats repeatedly (each turn, each trigger) and keeps them.
- Not permanent_growth: A single lasting bonus is stat_gain.
- Why the script suspects it: grows once, when played: a single lasting bonus is stat_gain

### Card 750576 (runeterra), tagged from: rule permanent_growth | do stat_change | -/-/self | - | summoned(self) | own

**Basilisk Rider**
Card text: "Allegiance: Grant me +1|+1 and Overwhelm."

Keywords (their own rows are on the keyword entries): Allegiance

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of self | keyword_condition Allegiance |  | stat_change | self |  |  | power=1, health=1 | permanent |
| summoned of self | keyword_condition Allegiance | and | give_keyword | self |  | Overwhelm |  | permanent |


Keyword entry:
**Allegiance**
Card text: "When you summon this unit, it gets its allegiance bonus if the top card of your deck matches its region."

(no rows of its own)


Keyword entry:
**Overwhelm**
Card text: "Inflicts damage beyond what would kill the target(s) to the enemy Nexus."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| strikes by self |  |  | excess_damage | enemy player |  |  |  |  |


### Card 796881 (runeterra), tagged from: rule permanent_growth | do stat_change | -/-/self | - | summoned(self) | own

**Salty Spinner**
Card text: "Keywords: Impact. When I'm summoned or Round Start: Grant me +0|+2 for each card you discarded last round, then shuffle my stats."

Keywords (their own rows are on the keyword entries): Impact

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of self |  |  | stat_change | self |  |  | health=double (event_count of (discarded by mine player) last_round) | permanent |
| summoned of self |  | then | shuffle_stats | self |  |  |  |  |
| round_start |  |  | stat_change | self |  |  | health=double (event_count of (discarded by mine player) last_round) | permanent |
| round_start |  | then | shuffle_stats | self |  |  |  |  |


Keyword entry:
**Impact**
Card text: "When this strikes while attacking, it deals 1 to the enemy Nexus. This keyword can stack."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| strikes by self [state is attacking] |  |  | damage | enemy player |  |  | amount=1 |  |


### Card 751167 (runeterra), tagged from: rule permanent_growth | do stat_change | -/-/self | - | summoned(self) | own

**Khahiri the Student**
Card text: "When I'm summoned, if you've Predicted this game, grant me +1|+1."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of self | event_count predicts by mine player ge 1 this_game |  | stat_change | self |  |  | power=1, health=1 | permanent |


### Card 796733 (runeterra), tagged from: rule permanent_growth | do stat_change | -/-/self | - | summoned(self) | own

**The Immortal Fire**
Card text: "Keywords: Elusive. When I'm summoned, grant me +1|+0 for each Celestial card you played this game. The first time I would die, fully heal me instead."

Keywords (their own rows are on the keyword entries): Elusive

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of self |  |  | stat_change | self |  |  | power=event_count of (played by mine player of card [type is Celestial]) this_game | permanent |
| dies of self [once_per_game] |  |  | heal | self |  |  | amount=full |  |


Keyword entry:
**Elusive**
Card text: "Can only be blocked by an Elusive unit."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | cant | all enemy unit [keyword not Elusive] to self |  |  | event=blocks | while |


### Card 750737 (runeterra), tagged from: rule permanent_growth | do stat_change | -/-/self | - | summoned(self) | own

**They Who Endure**
Card text: "Keywords: Overwhelm. When I'm summoned, grant me +1|+1 for each ally that has died."

Keywords (their own rows are on the keyword entries): Overwhelm

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of self |  |  | stat_change | self |  |  | power=event_count of (dies of mine unit) this_game, health=event_count of (dies of mine unit) this_game | permanent |


Keyword entry:
**Overwhelm**
Card text: "Inflicts damage beyond what would kill the target(s) to the enemy Nexus."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| strikes by self |  |  | excess_damage | enemy player |  |  |  |  |


### Card 751812 (runeterra), tagged from: rule permanent_growth | do stat_change | -/-/self | - | summoned | own

**Trusty Ramhound**
Card text: "The first time you summon an Elite, grant me +2|+2."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of mine unit [type is Elite] [once_per_game] |  |  | stat_change | self |  |  | power=2, health=2 | permanent |


### Card 741336 (faeria), tagged from: rule permanent_growth | do stat_change | -/-/self | - | summoned | own

**Illusion of Grandeur**
Card text: "Charge 2 Whenever you summon a creature that costs 1 faeria or less, this gains Attack and Life equal to that creature's (while in your hand or deck)."

Keywords (their own rows are on the keyword entries): Charge

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Charge | amount=2 | permanent |
| summoned of mine unit [cost le 1] |  |  | stat_change | self |  |  | power=stat power of (it), health=stat health of (it) | permanent |


Keyword entry:
**Charge**
Card text: "Can move several spaces in a straight line."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | self to position [position is straight_line] |  |  | event=moves | while |


### Card 5000195 (duelyst), tagged from: rule permanent_growth | do stat_change | -/-/self | - | summoned | own

**Black Solus**
Card text: "When you summon a Wraithling, this minion gains +2 Attack."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of mine unit [card is Wraithling] |  |  | stat_change | self |  |  | power=2 | permanent |


### Card 5000528 (duelyst), tagged from: rule permanent_growth | do stat_change | -/-/self | - | summoned | own

**Auroara**
Card text: "Whenever you summon a minion with 2 or less Attack, this minion gains +2 Attack."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| summoned of mine unit [power le 2] |  |  | stat_change | self |  |  | power=2 | permanent |



## Family: concept `ping` ("Small repeatable damage"), from rows `do damage`
- Counts as ping: A small amount of damage (1 or 2) that can be dealt again and again.
- Not ping: One big hit is damage.
- Why the script suspects it: hurts me: acts on my own side

### Card 7000886 (sts1), tagged from: rule ping | do damage | player/mine/- | - | turn_start | own

**Brutality+**
Card text: "Keywords: Innate. At the start of your turn, lose 1 HP and draw 1 card."

Keywords (their own rows are on the keyword entries): Innate

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_start by mine player |  |  | damage | mine player |  |  | amount=1 |  |
| turn_start by mine player |  | and | draw | mine card in deck_top |  |  | amount=1 |  |


Keyword entry:
**Innate**
Card text: "Start each combat with this card in your hand."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| combat_start |  |  | move | self | hand |  |  |  |


### Card 7000414 (sts1), tagged from: rule ping | do damage | player/mine/- | - | played | own

**Blue Candle**
Card text: "Unplayable Curse cards can now be played. Whenever you play a Curse, lose 1 HP and Exhaust it."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | all mine card [type is Curse] [keyword is Unplayable] |  |  | event=played | while |
| played of mine spell [type is Curse] |  |  | damage | mine player |  |  | amount=1 |  |
| played of mine spell [type is Curse] |  | and | exhaust | it |  |  |  |  |


### Card 5000230 (duelyst), tagged from: rule ping | do damage | unit/mine/it | - | played | own

**Kujata**
Card text: "Your minions cost 1 less to summon and take 1 damage when summoned from your action bar."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | cost_change | all mine unit in hand |  |  | cost=-1 | while |
| played of mine unit |  |  | damage | it |  |  | amount=1 |  |


### Card 757193 (gwent), tagged from: rule ping | do damage | unit/mine/chosen | board | activated(self) | own

**Bear Witcher Quartermaster**
Card text: "Zeal. Order: Damage an allied unit by 1, then Spawn a Witcher Student on this row. Charges: 2"

Keywords (their own rows are on the keyword entries): Zeal, Charge, Order

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Zeal |  | permanent |
| activated of self |  |  | damage | chosen mine unit in board |  |  | amount=1 |  |
| activated of self |  | then | summon |  to chosen mine position [position is same_row] |  | Witcher Student |  |  |
| always |  |  | give_keyword | self |  | Charge | amount=2 | permanent |


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


Card it names or makes:
**Witcher Student**
Card text: "Doomed."

Keywords (their own rows are on the keyword entries): Doomed

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Doomed |  | permanent |


### Card 761091 (into_the_breach), tagged from: rule ping | do damage | unit_or_structure/mine/it | - | attacks | own

**Tumblebug**
Card text: "Health 3, move 3. Weapons/skills: Explosive Prize: Create an explosive boulder, preparing to destroy it next turn by attacking it for 1 damage.. Tumblebugs attack by summoning an Unstable Boulder that will explode when damaged, then threatening to damage it and inflict 1 damage on all of its adjancent tiles, including the Tumblebug. These boulders do not explode if they are not damaged. If a Tumblebug is forced to attack a mech directly it will not summon an unstable boulder. As a rare Vek, Tumblebugs cannot appear on the first island and are restricted to two spawns per mission, including its alpha. They cannot spawn on missions with explosive mines."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| attacks by self |  |  | summon |  to position [position is in_front] | board | Unstable Boulder |  |  |
| attacks by self |  | and | damage | it unit_or_structure |  |  | amount=1 |  |


Card it names or makes:
(card -5007 has no text in the library)

### Card 756831 (gwent), tagged from: rule ping | do damage | unit/mine/right_of_self | board | turn_end | own

**Svalblod Cultist**
Card text: "At the end of your turn, Heal the unit to the left by 1 and damage the unit to the right by 1."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_end by mine player |  |  | keyword_action | left_of_self mine unit in board |  | Heal | amount=1 | unstated |
| turn_end by mine player |  | and | damage | right_of_self mine unit in board |  |  | amount=1 |  |


Keyword entry:
**Heal**
Card text: "If a unit's current power is lower than its base power, restore it either to base power or by the amount specified."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | heal | it unit [state is damaged] |  |  | amount=full |  |
| activated |  | or | heal | it unit [state is damaged] |  |  | amount=listed |  |


### Card 7000112 (sts1), tagged from: rule ping | do damage | player/mine/- | - | turn_end | own

**Combust**
Card text: "At the end of your turn, lose 1 HP and deal 5 damage to ALL enemies."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_end by mine player |  |  | damage | mine player |  |  | amount=1 |  |
| turn_end by mine player |  | and | damage | all enemy unit in board |  |  | amount=5 |  |


### Card 796599 (runeterra), tagged from: rule ping | do damage | unit/mine/chosen | board | played(self) | own

**Crimson Pact (created)**
Card text: "Keywords: Skill. Deal 1 to any number of allies to deal that much to an enemy."

Keywords (their own rows are on the keyword entries): Skill

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | count of (chosen mine unit) chosen mine unit in board |  |  | amount=1 |  |
| played of self |  | then | damage | chosen enemy unit in board |  |  | amount=event_amount |  |


Keyword entry:
**Skill**
Card text: "A unit's spell-like effect that allows enemy reactions."

(no rows of its own)


### Card 757383 (gwent), tagged from: rule ping | do damage | unit/mine/it | - | played(self) | own

**Feral Bond**
Card text: "Spawn Skellige Wolves on an enemy row and damage it by 1, then Create a bronze Skellige Warrior that was not in your starting deck. Bloodthirst 3: You may Spawn and play any bronze Skellige Warrior that was not in your starting deck instead."

Keywords (their own rows are on the keyword entries): Bloodthirst

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | summon |  to chosen enemy position |  | Skellige Wolves |  |  |
| played of self |  | and | damage | it |  |  | amount=1 |  |
| played of self | keyword_condition Bloodthirst not 3 |  | create | random mine unit [state is bronze] [region is Skellige] [type is Warrior] [state not started_in_deck] | hand |  |  |  |
| played of self | keyword_condition Bloodthirst 3 |  | create | random mine unit [state is bronze] [region is Skellige] [type is Warrior] [state not started_in_deck] | hand |  |  |  |
| played of self | keyword_condition Bloodthirst 3 | then | play_card | it |  |  |  |  |


Keyword entry:
**Bloodthirst**
Card text: "Number of damaged enemy units required to trigger this ability."

(no rows of its own)


Card it names or makes:
**Skellige Wolves**
Card text: "Doomed. Immunity. Deathwish: Spawn a base copy of self on the opposite row."

Keywords (their own rows are on the keyword entries): Doomed, Immunity, Deathwish

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Doomed |  | permanent |
| always |  |  | give_keyword | self |  | Immunity |  | permanent |
| dies of self |  |  | copy | self [state is created] to mine position [position is opposite_row] | board |  |  |  |



## Family: concept `recycle` ("Reuse my cards (shuffle back)"), from rows `do shuffle_into_deck`
- Counts as recycle: The owner's used or discarded cards go back into deck or hand to be used again.
- Not recycle: An enemy unit sent to its deck is bounce_enemy.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 796677 (runeterra), tagged from: row | do shuffle_into_deck | unit/enemy/it | deck | played(self) | own

**Nautilus' Riptide**
Card text: "Keywords: Fast. Stun an enemy. Place that unit into the enemy deck if you have a Nautilus. Create a Nautilus into your deck."

Keywords (their own rows are on the keyword entries): Fast

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stun | chosen enemy unit in board |  |  |  | this_round |
| played of self |  | and | create |  | deck | Nautilus |  |  |
| played of self | have mine card [card is Nautilus] is |  | shuffle_into_deck | it enemy unit | deck |  |  |  |


Keyword entry:
**Fast**
Card text: "Can be played whenever you may act. Happens after your opponent has a chance to react."

(no rows of its own)


Card it names or makes:
**Nautilus**
Card text: "Keywords: Tough, Fearsome. Level up: When you are Deep. When I level up, copy Tossed allies that cost 4+ into your deck."

Keywords (their own rows are on the keyword entries): Tough, Fearsome

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always | keyword_condition Deep |  | level_up | self |  |  |  |  |
| levels_up of self |  |  | copy | all mine unit in removed [cost ge 4] | deck |  |  |  |



## Family: concept `repeat_trigger` ("Repeat or double triggers"), from rows `do repeat`
- Counts as repeat_trigger: A trigger or effect happens again, or twice.
- Not repeat_trigger: Copying a whole card is copy.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 756990 (gwent), tagged from: row | do repeat | unit/enemy/it | board | played(self) | own

**Morkvarg: Heart of Terror**
Card text: "Deploy: Damage an enemy unit by 1. Repeat until the target is damaged."

Keywords (their own rows are on the keyword entries): Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | chosen enemy unit in board |  |  | amount=1 |  |
| played of self |  | then | repeat | it enemy unit in board |  |  |  |  |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)


