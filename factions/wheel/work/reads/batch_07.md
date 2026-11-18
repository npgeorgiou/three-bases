# Tag reading, batch 07


## Family: concept `ping` ("Small repeatable damage"), from rows `do damage`
- Counts as ping: A small amount of damage (1 or 2) that can be dealt again and again.
- Not ping: One big hit is damage.
- Why the script suspects it: hurts me: acts on my own side

### Card 5000872 (duelyst), tagged from: rule ping | do damage | player/mine/- | - | turn_end | own

**Bloodfire Totem**
Card text: "At end of turn, deal 1 damage to your General."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_end by mine player |  |  | damage | mine player |  |  | amount=1 |  |


### Card 756638 (gwent), tagged from: rule ping | do damage | unit/mine/chosen | board | played(self) | own

**Slave Driver**
Card text: "Deploy: Damage a bronze allied unit by 1, then Spawn a 1-power copy of it on this row. If it was a Soldier, Spawn and play the copy instead."

Keywords (their own rows are on the keyword entries): Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | chosen mine unit in board [state is bronze] |  |  | amount=1 |  |
| played of self |  | then | copy | it to mine position [position is same_row] | board |  |  |  |
| played of self |  | and | stat_set | it mine unit [state is created] |  |  | strength=1 |  |
| played of self |  | instead | play_card | it mine unit [state is created] [type is Soldier] |  |  |  |  |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)


### Card 761051 (into_the_breach), tagged from: rule ping | do damage | unit/mine/all | - | turn_end | own

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


### Card 2000273 (monster_train), tagged from: rule ping | do damage | player/mine/- | - | kept_in_hand(self) | own

**Vengeful Shard**
Card text: "Reserve: Your Pyre takes 1 damage."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| kept_in_hand of self |  |  | damage | mine player |  |  | amount=1 |  |


### Card 750880 (runeterra), tagged from: rule ping | do damage | unit/mine/chosen | board | played(self) | own

**Imperial Demolitionist**
Card text: "Play: Deal 1 to an ally to deal 2 to the enemy Nexus."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | damage | chosen mine unit in board |  |  | amount=1 |  |
| played of self |  | if_done | damage | enemy player |  |  | amount=2 |  |



## Family: concept `recycle` ("Reuse my cards (shuffle back)"), from rows `do shuffle_into_deck`
- Counts as recycle: The owner's used or discarded cards go back into deck or hand to be used again.
- Not recycle: An enemy unit sent to its deck is bounce_enemy.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 756472 (gwent), tagged from: row | do shuffle_into_deck | card/enemy/chosen | discard | played(self) | own

**Assire var Anahid**
Card text: "Deploy (Melee): Shuffle a card from your opponent's graveyard into their deck. Deploy (Ranged): Shuffle a card from your graveyard into your deck."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self | keyword_condition Melee |  | shuffle_into_deck | chosen enemy card in discard | deck |  |  |  |
| played of self | keyword_condition Ranged |  | shuffle_into_deck | chosen mine card in discard | deck |  |  |  |


### Card 751512 (runeterra), tagged from: row | do shuffle_into_deck | unit/enemy/chosen | board | played(self) | own

**Coup de Grace**
Card text: "Place an enemy follower into the enemy deck, then your opponent draws 1."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | shuffle_into_deck | chosen enemy unit in board [category is follower] |  |  |  |  |
| played of self |  | then | draw | enemy card in deck_top |  |  | amount=1 |  |


### Card 756372 (gwent), tagged from: row | do shuffle_into_deck | unit/enemy/it | deck | played(self) | own

**Imperial Golem**
Card text: "Deploy: Reveal the top unit from your opponent's deck and damage self by its power, then shuffle it back."

Keywords (their own rows are on the keyword entries): Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | keyword_action | top enemy unit in deck |  | Reveal |  | unstated |
| played of self |  | then | damage | self |  |  | amount=stat strength of (it enemy unit in deck) |  |
| played of self |  | then | shuffle_into_deck | it enemy unit in deck |  |  |  |  |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)


Keyword entry:
**Reveal**
Card text: "Show a card to both players, then hide it back in the hand or deck."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | reveal | it |  |  |  |  |


### Card 750852 (runeterra), tagged from: row | do shuffle_into_deck | unit/enemy/it | board | played(self) | own

**Riptide**
Card text: "Stun an enemy. Place that unit into the enemy deck if you have a Nautilus."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | stun | chosen enemy unit in board |  |  |  | this_round |
| played of self | have mine unit in board [card is Nautilus] is |  | shuffle_into_deck | it enemy unit in board | deck |  |  |  |


### Card 813686 (gwent), tagged from: row | do shuffle_into_deck | unit/enemy/chosen | board | played(self) | own

**Temple of Melitele: Pilgrimage**
Card text: "Doomed. Immunity. Resilience. Deploy: Shuffle an allied unit back into your deck, then shuffle an enemy unit of the same power or less back into your opponent's deck. Order: Play the shuffled unit from your deck."

Keywords (their own rows are on the keyword entries): Doomed, Immunity, Resilience, Order, Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Doomed |  | permanent |
| always |  |  | give_keyword | self |  | Immunity |  | permanent |
| always |  |  | give_keyword | self |  | Resilience |  | permanent |
| played of self |  |  | shuffle_into_deck | chosen mine unit in board |  |  |  |  |
| played of self |  | then | shuffle_into_deck | chosen enemy unit in board [strength le stat strength of (it)] |  |  |  |  |
| activated of self |  |  | play_card | it mine unit in deck |  |  |  |  |


Keyword entry:
**Doomed**
Card text: "Status that removes the card from the game after it leaves the battlefield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| leaves_play of self |  |  | obliterate | self |  |  |  |  |


Keyword entry:
**Immunity**
Card text: "Status whereby this card cannot be manually targeted."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | cant | all player to self |  |  | event=targeted | while |


Keyword entry:
**Resilience**
Card text: "Status that allows a unit to remain on the battlefield at the end of the round, then disappears.\nNote: Boost and Armor are not carried over to the next round."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| round_end |  |  | cant | self |  |  | event=leaves_play | this_round |
| round_end |  | then | remove_keyword | self |  | Resilience |  |  |


Keyword entry:
**Order**
Card text: "An ability triggered manually by the player. Cards with Order cannot be used for 1 turn after being placed on the battlefield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | cant | self |  |  | event=activated, turns=1 | n_turns |



## Family: concept `regeneration` ("Heal every turn (regeneration)"), from rows `do give_keyword`
- Counts as regeneration: A unit heals again each turn or returns to full health each turn.
- Not regeneration: A single heal is heal.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 761052 (into_the_breach), tagged from: row | do give_keyword | unit/enemy/all | board | always | own

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



## Family: concept `repeat_trigger` ("Repeat or double triggers"), from rows `do repeat`
- Counts as repeat_trigger: A trigger or effect happens again, or twice.
- Not repeat_trigger: Copying a whole card is copy.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 756643 (gwent), tagged from: row | do repeat | unit/enemy/chosen | board | activated | uses_keyword Duel

**Seltkirk of Gulet**
Card text: "Order (Melee): Duel an enemy unit."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated of self | keyword_condition Melee |  | keyword_action | chosen enemy unit in board to self |  | Duel |  | unstated |


Keyword entry:
**Duel**
Card text: "Units take turns dealing damage equal to their power until one of them is destroyed."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | damage | it |  |  | amount=stat strength of (self) |  |
| activated |  | then | damage | self |  |  | amount=stat strength of (it) |  |
| activated |  | then | repeat | self |  |  |  |  |


### Card 8000097 (marvel_snap), tagged from: row | do repeat | card/enemy/- | deck_bottom | drawn(self) | own

**Copycat**
Card text: "When you draw this, copy the text from the bottom card of your opponent's deck."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| drawn of self |  |  | repeat | enemy card in deck_bottom |  |  |  |  |


### Card 796966 (runeterra), tagged from: row | do repeat | card/enemy/top | deck | played(self) | own

**Volatile Bloom**
Card text: "Keywords: Skill. Play: Activate the effects of all traps in the top 5 cards of the enemy deck."

Keywords (their own rows are on the keyword entries): Skill

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | repeat | 5 top enemy card in deck [keyword is Trap] |  |  |  |  |


Keyword entry:
**Skill**
Card text: "A unit's spell-like effect that allows enemy reactions."

(no rows of its own)


### Card 756797 (gwent), tagged from: row | do repeat | unit/enemy/chosen | board | activated | uses_keyword Duel

**Prince Anséis**
Card text: "Formation. Order: Damage an enemy unit by 4. Inspired: Duel an enemy unit instead."

Keywords (their own rows are on the keyword entries): Formation, Order, Inspired

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Formation |  | permanent |
| activated of self | keyword_condition Inspired not |  | damage | chosen enemy unit in board |  |  | amount=4 |  |
| activated of self | keyword_condition Inspired |  | keyword_action | chosen enemy unit in board to self |  | Duel |  | unstated |


Keyword entry:
**Formation**
Card text: "If played on the melee row, gain Zeal. If played on the ranged row, boost self by 1."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self | have self [position is front_row] is |  | give_keyword | self |  | Zeal |  | permanent |
| played of self | have self [position is back_row] is |  | stat_change | self |  |  | strength=1 | permanent |


Keyword entry:
**Order**
Card text: "An ability triggered manually by the player. Cards with Order cannot be used for 1 turn after being placed on the battlefield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | cant | self |  |  | event=activated, turns=1 | n_turns |


Keyword entry:
**Inspired**
Card text: "Trigger this ability if this unit's current power is higher than its base power."

(no rows of its own)


Keyword entry:
**Duel**
Card text: "Units take turns dealing damage equal to their power until one of them is destroyed."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | damage | it |  |  | amount=stat strength of (self) |  |
| activated |  | then | damage | self |  |  | amount=stat strength of (it) |  |
| activated |  | then | repeat | self |  |  |  |  |


### Card 756899 (gwent), tagged from: row | do repeat | unit/enemy/chosen | board | activated | uses_keyword Duel

**Tavern Brawl**
Card text: "Force an enemy unit to Duel an adjacent unit."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | keyword_action | chosen enemy unit in board to chosen unit in board [position is sides] |  | Duel |  | unstated |


Keyword entry:
**Duel**
Card text: "Units take turns dealing damage equal to their power until one of them is destroyed."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | damage | it |  |  | amount=stat strength of (self) |  |
| activated |  | then | damage | self |  |  | amount=stat strength of (it) |  |
| activated |  | then | repeat | self |  |  |  |  |


