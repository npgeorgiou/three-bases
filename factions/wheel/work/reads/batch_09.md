# Tag reading, batch 09


## Family: concept `revive` ("Bring back dead units (revive)"), from rows `do revive`
- Counts as revive: A unit that died or was destroyed earlier comes back into play. (Kaptain, 26 Oct 2026: back to hand is return_to_hand.)
- Not revive: Surviving at the moment of death is cheat_death.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 757310 (gwent), tagged from: row | do revive | unit/enemy/chosen to enemy | discard | played(self) | own

**Incubus**
Card text: "Deploy: Summon a bronze unit from your opponent's graveyard to the opposite row, then Summon a bronze unit of equal or less provisions from your graveyard to this row."

Keywords (their own rows are on the keyword entries): Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | revive | chosen enemy unit in discard [state is bronze] to enemy position [position is opposite_row] |  |  |  |  |
| played of self |  | then | revive | chosen mine unit in discard [state is bronze] [cost le stat cost of (it)] to mine position [position is same_row] |  |  |  |  |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)


### Card 8000186 (marvel_snap), tagged from: row | do revive | unit/enemy/highest to mine | discarded_or_dead | activated(self) | own

**Fenris Wolf**
Card text: "Activate: Resurrect your opponent's highest-Power discarded or destroyed card on your side of this location."

Keywords (their own rows are on the keyword entries): Activate

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated of self |  |  | revive | highest enemy unit by power in discarded_or_dead to mine position [position is same_lane] |  |  |  |  |


Keyword entry:
**Activate**
Card text: "The card does nothing when played; from the turn after it was played its player can choose a turn to use the ability, which then happens as that turn plays out."

(no rows of its own)


### Card 797078 (runeterra), tagged from: row | do revive | unit/enemy/highest | discard | attacks | own

**Taarosh**
Card text: "Keywords: Fearsome. Each round, the first time I attack, fill your attackers with revived Ephemeral copies of the strongest followers you've slain this game."

Keywords (their own rows are on the keyword entries): Fearsome

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| attacks by self [first_each_round] | event_count killed by mine player of unit [category is follower] ge 1 this_game |  | revive | highest enemy unit by power in discard [category is follower] |  |  |  |  |
| attacks by self [first_each_round] | event_count killed by mine player of unit [category is follower] ge 1 this_game | then | give_keyword | it |  | Ephemeral |  | permanent |


Keyword entry:
**Fearsome**
Card text: "Can only be blocked by enemies with 3 or more Power."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | cant | all enemy unit [power lt 3] to self |  |  | event=blocks | while |


Keyword entry:
**Ephemeral**
Card text: "This unit dies when it strikes or when the round ends."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| strikes by self |  |  | kill | self |  |  |  |  |
| round_end |  |  | kill | self |  |  |  |  |


### Card 757309 (gwent), tagged from: row | do revive | unit/enemy/highest to enemy | discard | played(self) | own

**Witches' Sabbath**
Card text: "Summon up to 3 highest-power units from your opponent's graveyard to an enemy row, then Summon as many highest-power non-Neutral units from your graveyard to the opposite row and give them Doomed."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | revive | 3 highest enemy unit by strength in discard to chosen enemy position |  |  |  |  |
| played of self |  | then | revive | count of (it) highest mine unit by strength in discard [region not Neutral] to mine position [position is opposite_row] |  |  |  |  |
| played of self |  | then | give_keyword | it |  | Doomed |  | permanent |


Keyword entry:
**Doomed**
Card text: "Status that removes the card from the game after it leaves the battlefield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| leaves_play of self |  |  | obliterate | self |  |  |  |  |



## Family: concept `shield` ("Absorb one hit (shield, ward)"), from rows `do counter`
- Counts as shield: The next hit or damage instance on a unit is fully absorbed or cancelled.
- Not shield: Damage lowered by an amount is damage_reduction; on the player it is player_shield.
- Why the script suspects it: counter: cancelling a spell or removing a keyword is not absorbing a hit

### Card 4000119 (inscryption), tagged from: row | do counter | effect/-/it | - | targeted(self) | has_keyword Uncuttable

**Pack Mule**
Card text: "Keywords: Sprinter, Uncuttable. Special behaviour: When a card perishes, player receives a Squirrel, a Card that Costs 1 Blood, a Card that Costs 2 Blood, and a Card that Costs Bones (or another Card that Costs 1 Blood, if Bones haven't been unlocked yet)."

Keywords (their own rows are on the keyword entries): Sprinter, Uncuttable

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| dies of self |  |  | create |  |  | Squirrel |  |  |
| dies of self |  | and | create | random card [cost eq 1] |  |  |  |  |
| dies of self |  | and | create | random card [cost eq 2] |  |  |  |  |
| dies of self |  | and | create | random card |  |  |  |  |


Keyword entry:
**Sprinter**
Card text: "Rulebook: At the end of the owner's turn, a card bearing this sigil will move in the direction inscribed in the sigil."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| turn_end by mine player |  |  | move | self to position [position is sides] |  |  |  |  |


Keyword entry:
**Uncuttable**
Card text: "Uncuttable is a trait. Cards posessing the Uncuttable trait cannot be cut with Scissors, skinned by the Skinning Knife (in Kaycee's Mod) or stolen with the Fish Hook. Even though the Forced Death events in Act I summon many Grizzlys which are intended to be impassable, they are still cuttable."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| targeted by equipment [card in Scissors] [card in Skinning Knife] [card in Fish Hook] of self |  |  | counter | it effect |  |  |  |  |


Card it names or makes:
**Squirrel**
Card text: ""

(no rows of its own)


### Card 751014 (runeterra), tagged from: row | do counter | effect/-/it | - | targeted(self) | has_keyword SpellShield

**Fledgling Stellacorn**
Card text: "Keywords: Lifesteal, SpellShield."

Keywords (their own rows are on the keyword entries): Lifesteal, SpellShield

(no rows of its own)


Keyword entry:
**Lifesteal**
Card text: "Damage this unit deals heals its Nexus that amount."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| damaged by self |  |  | heal | mine player |  |  | amount=event_amount |  |


Keyword entry:
**SpellShield**
Card text: "Negates the next enemy spell or skill that would affect me."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| targeted by enemy spell [category in spell] [category in skill] of self |  |  | counter | it effect |  |  |  |  |


### Card 7000435 (sts1), tagged from: row | do counter | effect/-/it | - | given_keyword(self) | uses_keyword Artifact

**Clockwork Souvenir**
Card text: "Start each combat with 1 Artifact."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| combat_start |  |  | give_keyword | mine player |  | Artifact | amount=1 | permanent |


Keyword entry:
**Artifact**
Card text: "Negates the next debuff."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| given_keyword of self [state is negative] [next_time] |  |  | counter | it effect |  |  |  |  |
| given_keyword of self [state is negative] [next_time] |  | then | remove_keyword | self |  | Artifact | amount=1 |  |


### Card 4000225 (inscryption), tagged from: row | do counter | effect/-/it | - | targeted(self) | has_keyword Uncuttable

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


### Card 752035 (runeterra), tagged from: row | do counter | effect/-/it | - | targeted(self) | uses_keyword SpellShield

**Herald of Celestial Convergence**
Card text: "Play: Activate other allies' Daybreak and Nightfall effects. Daybreak: Grant me Overwhelm. Nightfall: Grant me SpellShield."

Keywords (their own rows are on the keyword entries): Nightfall, Daybreak

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | keyword_action | all mine unit in board [card not Herald of Celestial Convergence] |  | Daybreak |  |  |
| played of self |  | and | keyword_action | all mine unit in board [card not Herald of Celestial Convergence] |  | Nightfall |  |  |
| always | keyword_condition Daybreak |  | give_keyword | self |  | Overwhelm |  | permanent |
| always | keyword_condition Nightfall |  | give_keyword | self |  | SpellShield |  | permanent |


Keyword entry:
**Nightfall**
Card text: "Bonus if this is NOT the first card you play in a round."

(no rows of its own)


Keyword entry:
**Daybreak**
Card text: "Bonus if this is the FIRST card you play in a round."

(no rows of its own)


Keyword entry:
**Overwhelm**
Card text: "Inflicts damage beyond what would kill the target(s) to the enemy Nexus."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| strikes by self |  |  | excess_damage | enemy player |  |  |  |  |


Keyword entry:
**SpellShield**
Card text: "Negates the next enemy spell or skill that would affect me."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| targeted by enemy spell [category in spell] [category in skill] of self |  |  | counter | it effect |  |  |  |  |



## Family: concept `shield` ("Absorb one hit (shield, ward)"), from rows `do remove_keyword`
- Counts as shield: The next hit or damage instance on a unit is fully absorbed or cancelled.
- Not shield: Damage lowered by an amount is damage_reduction; on the player it is player_shield.
- Why the script suspects it: remove_keyword: cancelling a spell or removing a keyword is not absorbing a hit

### Card 741108 (faeria), tagged from: row | do remove_keyword | -/-/self | - | damaged(self) | uses_keyword Protection

**King's Faithful**
Card text: "Protection"

Keywords (their own rows are on the keyword entries): Protection

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Protection |  | permanent |


Keyword entry:
**Protection**
Card text: "Prevents all damage from the next damage source, then is removed."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| damaged of self |  |  | negate_damage | self |  |  | amount=event_amount |  |
| damaged of self |  | then | remove_keyword | self |  | Protection |  |  |


### Card 756348 (gwent), tagged from: row | do remove_keyword | -/-/self | - | damaged(self) | uses_keyword Shield

**Primordial D'ao**
Card text: "Shield. Deploy: Boost self by [0]. Increase this value by 1 for each Construct you played this game."

Keywords (their own rows are on the keyword entries): Shield, Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Shield |  | permanent |
| played of self |  |  | stat_change | self |  |  | strength=event_count of (played of mine unit [type is Construct]) this_game | permanent |


Keyword entry:
**Shield**
Card text: "Status that blocks the next instance of damage dealt to a unit."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| damaged of self [next_time] |  |  | negate_damage | self |  |  | amount=event_amount |  |
| damaged of self [next_time] |  | then | remove_keyword | self |  | Shield |  |  |


Keyword entry:
**Deploy**
Card text: "Trigger this ability when played."

(no rows of its own)


### Card 6000187 (into_the_breach), tagged from: row | do remove_keyword | unit/mine/chosen | - | damaged(self) | uses_keyword Energy Shield

**Shield-Tank (unit)**
Card text: "Health 1, move 3. It can give Shields to allies."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| attacks by self |  |  | give_keyword | chosen mine unit [position is bordering] |  | Energy Shield |  | permanent |


Keyword entry:
**Energy Shield**
Card text: "Shields block damage and prevent new negative status effects (Fire, Freezing, A.C.I.D, etc.). Only direct damage will remove the Shield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| damaged of self |  |  | negate_damage | self |  |  | amount=event_amount |  |
| always |  |  | cant | self to keyword [state is negative] |  |  | event=given_keyword | while |
| damaged of self |  |  | remove_keyword | self |  | Energy Shield |  |  |


### Card 2000260 (monster_train), tagged from: row | do remove_keyword | unit/-/chosen | board | damaged(self) | uses_keyword Damage Shield

**Thy Holiest Shield**
Card text: "Purge. / Apply 2 per X Damage Shield."

Keywords (their own rows are on the keyword entries): Purge

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | give_keyword | self |  | Purge |  | permanent |
| played of self |  |  | give_keyword | chosen unit in board |  | Damage Shield | amount=x_paid (2) | permanent |


Keyword entry:
**Purge**
Card text: "Once played, this card is removed from your deck for the rest of the run."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | obliterate | self |  |  |  | this_run |


Keyword entry:
**Damage Shield**
Card text: "Nullify the next source of damage."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| damaged of self |  |  | negate_damage | self |  |  |  |  |
| damaged of self |  | then | remove_keyword | self |  | Damage Shield | amount=1 |  |


### Card 741083 (faeria), tagged from: row | do remove_keyword | unit/-/chosen | board | damaged(self) | uses_keyword Protection

**Safeguard**
Card text: "Give a creature Protection."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | give_keyword | chosen unit in board |  | Protection |  | permanent |


Keyword entry:
**Protection**
Card text: "Prevents all damage from the next damage source, then is removed."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| damaged of self |  |  | negate_damage | self |  |  | amount=event_amount |  |
| damaged of self |  | then | remove_keyword | self |  | Protection |  |  |



## Family: concept `spell_power` ("My spells and abilities get stronger"), from rows `do increase_effect`
- Counts as spell_power: The owner's spells or abilities deal more damage or have bigger effects: spell damage, ability power, amplify.
- Not spell_power: A unit gaining stats is stat_gain.
- Why the script suspects it: helps the enemy: acts on an enemy

### Card 5000019 (duelyst), tagged from: row | do increase_effect | player/enemy/- | - | always | own

**Grandmaster Nosh-Rak**
Card text: "Keywords: Blast, Flying. The enemy General takes double damage."

Keywords (their own rows are on the keyword entries): Blast, Flying

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | increase_effect | enemy player |  |  | times=2 | while |


Keyword entry:
**Blast**
Card text: "Attack all enemy minions and Generals in one straight line."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| attacks by self |  |  | strike | self to all enemy any in board [position in same_row] [position in same_column] |  |  |  |  |


Keyword entry:
**Flying**
Card text: "Move anywhere on the battlefield."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | can | self to position |  |  | event=moves | while |


### Card 756768 (gwent), tagged from: row | do increase_effect | position/enemy/chosen | - | activated(self) | own

**Scepter of Storms**
Card text: "Deploy: Spawn and play Biting Frost, Impenetrable Fog, or Torrential Rain. Order: Increase the row effect duration on an enemy row by 1 turn."

Keywords (their own rows are on the keyword entries): Order, Deploy

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | choose_one |  |  |  |  |  |
| played of self |  | or | create |  | hand | Biting Frost |  |  |
| played of self |  | or | create |  | hand | Impenetrable Fog |  |  |
| played of self |  | or | create |  | hand | Torrential Rain |  |  |
| played of self |  | then | play_card | it card |  |  |  |  |
| activated of self |  |  | increase_effect | chosen enemy position |  |  | amount=1 |  |


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
**Biting Frost**
Card text: "Spawn Frost on an enemy row for 3 turns."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | give_keyword | chosen enemy position |  | Frost | turns=3 | n_turns |


Card it names or makes:
**Impenetrable Fog**
Card text: "Spawn Fog on an enemy row for 3 turns."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | give_keyword | chosen enemy position |  | Fog | turns=3 | n_turns |


Card it names or makes:
**Torrential Rain**
Card text: "Spawn Rain on an enemy row for 3 turns."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | give_keyword | chosen enemy position |  | Rain | turns=3 | n_turns |


### Card 761097 (into_the_breach), tagged from: row | do increase_effect | unit/enemy/all | board | attacks | uses_keyword Boost

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


### Card 8000512 (marvel_snap), tagged from: row | do increase_effect | unit/enemy/all | board | always | own

**Scorpion Brand New Day**
Card text: "Ongoing: Double the Power reductions on all enemy cards."

Keywords (their own rows are on the keyword entries): Ongoing

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| always |  |  | increase_effect | all enemy unit in board [state is negative] |  |  | percent=100 | while |


Keyword entry:
**Ongoing**
Card text: "A lasting effect that holds for as long as the card is on the board."

(no rows of its own)


### Card 752072 (runeterra), tagged from: row | do increase_effect | unit/enemy/all | - | activated | uses_keyword Boost

**Smoldering Smirk**
Card text: "Boost 2 allies, then they Strike an enemy one after another."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| played of self |  |  | keyword_action |  |  | Boost |  |  |
| played of self |  | then | strike | it to chosen enemy unit in board |  |  |  |  |


Keyword entry:
**Boost**
Card text: "Increase allies' positive stackable keywords or enemies' negative stackable keywords."

| when | if | link | what | who | where | card/keyword | numbers | lasts |
|---|---|---|---|---|---|---|---|---|
| activated |  |  | choose_one |  |  |  |  |  |
| activated |  | or | increase_effect | all mine unit |  |  |  |  |
| activated |  | or | increase_effect | all enemy unit |  |  |  |  |


