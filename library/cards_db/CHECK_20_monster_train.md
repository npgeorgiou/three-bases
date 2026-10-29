# Stored rows of 20 cards (check_table.py)

Each card: its name and text on one line, then its stored rows, one row per effect, then the rows of each keyword it has.
- ability: one numbered "when -> if -> do" unit of the card. Rows with the same ability number are one ability; they happen together, in effect order.
- effect: the step inside the ability. link says how a step joins the step before it: and = also; then = after it, using its result; if_done = only if it happened; or = instead (a choice); instead = replaces it.
- pick=it in a target = the thing the step before acted on (the drawn card, the summoned unit, the chosen enemy).
- A row labelled "keyword X" is what keyword X does; the card has it, so the card does it too.
- Targets, events, conditions and amounts are written in place as their stored fields.

**Railbeater**: Armor 30. / Strike: Apply Melee Weakness 1 to the attacked unit. (keywords: Armor)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Armor |  | amount=30 | permanent |  |
| 1 | strikes | pick=self | kind=unit side=enemy |  |  | 0 | give_keyword | pick=it |  |  |  | Melee Weakness |  | amount=1 | permanent |  |
| keyword Armor: 0 | damaged |  | pick=self |  |  | 0 | negate_damage | pick=self |  |  |  |  |  | amount={x=count of=(kind=keyword pick=self with[keyword is Armor])} |  |  |
| keyword Armor: 0 | damaged |  | pick=self |  |  | 1 | remove_keyword | pick=self |  |  |  | Armor |  | amount=1 |  | then |

**Guardian's Amulet**: Offering. / Apply Sap 2 to enemy units. (keywords: Offering)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Offering |  |  | permanent |  |
| 1 | played |  | pick=self |  |  | 0 | give_keyword | kind=unit side=enemy pick=all zone=board |  |  |  | Sap |  | amount=2 | permanent |  |
| keyword Offering: 0 | discarded |  | pick=self |  |  | 0 | play_card | pick=self |  |  |  |  |  |  |  |  |

**Plink**: Deal 1 damage to a random enemy unit, twice. / Slay: Add a common or uncommon Morsel unit to your hand.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | damage | kind=unit side=enemy pick=random zone=board |  |  |  |  |  | amount=1; times=2 |  |  |
| 1 | killed | pick=self |  |  |  | 0 | create | kind=unit side=any pick=random with[type is Morsel; rarity in common; rarity in uncommon] |  | hand |  |  |  | amount=1 |  |  |

**Fracture**: Apply Reap 2.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | give_keyword | kind=unit side=any pick=chosen zone=board |  |  |  | Reap |  | amount=2 | permanent |  |

**Crucible Collector**: Gorge: Gain Lifesteal 1.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | eats | pick=self | kind=unit with[type is Morsel] |  |  | 0 | give_keyword | pick=self |  |  |  | Lifesteal |  | amount=1 | permanent |  |

**Bog Fly**: +5 Attack per Echo.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | always |  |  |  |  | 0 | stat_change | pick=self |  |  |  |  |  | power={x=product items=5, {x=count of=(kind=lane_resource)}} | while |  |

**Bone Dog's Favor**: Unplayable. / Reserve: Restore 5 Pyre health. (keywords: Unplayable)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Unplayable |  |  | permanent |  |
| 1 | kept_in_hand |  | pick=self |  |  | 0 | heal | kind=player side=mine |  |  |  |  |  | amount=5 |  |  |
| keyword Unplayable: 0 | always |  |  |  |  | 0 | cant | pick=self |  |  |  |  |  | event=played | while |  |

**Dripfall**: Descend a unit and apply Dazed 1.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | keyword_action | kind=unit side=any pick=chosen zone=board |  |  |  | Descend |  |  | unstated |  |
| 0 | played |  | pick=self |  |  | 1 | give_keyword | pick=it |  |  |  | Dazed |  | amount=1 | permanent | and |

**Wickless Baron**: Harvest: +3 Attack and +3 Health.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | dies |  | kind=unit with[position is same_lane] |  |  | 0 | stat_change | pick=self |  |  |  |  |  | power=3; health=3 | permanent |  |

**Echo Break**: Deal 1 damage per Echo

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | damage | kind=unit side=any pick=chosen zone=board |  |  |  |  |  | amount={x=count of=(kind=lane_resource)} |  |  |

**Animus of Speed**: Quick. (keywords: Quick)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Quick |  |  | permanent |  |
| keyword Quick: 0 | attacks | pick=self |  |  |  | 0 | first_strike | pick=self |  |  |  |  |  |  | this_round |  |

**Kindle**: Consume. / Gain 2 Ember per X. (keywords: Consume)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Consume |  |  | permanent |  |
| 1 | played |  | pick=self |  |  | 0 | mana_gain | kind=mana side=mine |  |  |  |  |  | amount={x=x_paid inner=2} |  |  |
| keyword Consume: 0 | played |  | pick=self |  |  | 0 | exhaust | pick=self |  |  |  |  |  |  |  |  |

**Ancient Resonance**: Deal 5 damage to enemy units per Echo.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | damage | kind=unit side=enemy pick=all zone=board |  |  |  |  |  | amount={x=product items=5, {x=count of=(kind=lane_resource)}} |  |  |

**Alloyed Construct**: Inert. Multistrike 1. / Gorge: Gain Fuel 1. (keywords: Inert, Multistrike)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Inert |  |  | permanent |  |
| 1 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Multistrike |  | amount=1 | permanent |  |
| 2 | eats | pick=self | kind=unit with[type is Morsel] |  |  | 0 | give_keyword | pick=self |  |  |  | Fuel |  | amount=1 | permanent |  |
| keyword Inert: 0 | always |  |  |  | (test=have of=(pick=self with[keyword is Fuel]) op=not) | 0 | cant | pick=self |  |  |  |  |  | event=attacks | while |  |
| keyword Multistrike: 0 | attack_done | pick=self |  | once_per_round |  | 0 | start_attack | pick=self |  |  |  |  |  |  |  |  |

**Horn Break**: Piercing. / Deal 5 damage, twice. (keywords: Piercing)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Piercing |  |  | permanent |  |
| 1 | played |  | pick=self |  |  | 0 | damage | kind=unit side=any pick=chosen zone=board |  |  |  |  |  | amount=5; times=2 |  |  |
| keyword Piercing |  |  |  |  |  |  | (no rows: speed, type or reminder keyword) |  |  |  |  |  |  |  |  |  |

**Cannibalize**: Sacrifice. / Add 3 random uncommon or rare Morsel units to your hand.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | keyword_action | kind=unit side=mine pick=chosen zone=board |  |  |  | Sacrifice |  |  | unstated |  |
| 0 | played |  | pick=self |  |  | 1 | create | kind=unit side=any pick=random with[type is Morsel; rarity in uncommon; rarity in rare] |  | hand |  |  |  | amount=3 |  | and |

**Fortify**: Apply Armor 5.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | give_keyword | kind=unit side=any pick=chosen zone=board |  |  |  | Armor |  | amount=5 | permanent |  |

**Kinhost Pupa**: Armor 20. Multistrike 1. / Strike: Apply Reap 1 to enemy units. (keywords: Armor, Multistrike)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Armor |  | amount=20 | permanent |  |
| 1 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Multistrike |  | amount=1 | permanent |  |
| 2 | strikes | pick=self | kind=unit side=enemy |  |  | 0 | give_keyword | kind=unit side=enemy pick=all zone=board |  |  |  | Reap |  | amount=1 | permanent |  |
| keyword Armor: 0 | damaged |  | pick=self |  |  | 0 | negate_damage | pick=self |  |  |  |  |  | amount={x=count of=(kind=keyword pick=self with[keyword is Armor])} |  |  |
| keyword Armor: 0 | damaged |  | pick=self |  |  | 1 | remove_keyword | pick=self |  |  |  | Armor |  | amount=1 |  | then |
| keyword Multistrike: 0 | attack_done | pick=self |  | once_per_round |  | 0 | start_attack | pick=self |  |  |  |  |  |  |  |  |

**Titan Sentry**: Revenge: Apply Frostbite 3 to enemy units.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | damaged |  | pick=self |  |  | 0 | give_keyword | kind=unit side=enemy pick=all zone=board |  |  |  | Frostbite |  | amount=3 | permanent |  |

**Rootseeds**: Apply +2 Attack. / Draw +1 next turn.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | stat_change | kind=unit side=any pick=chosen zone=board |  |  |  |  |  | power=2 | permanent |  |
| 1 | turn_start | kind=player side=mine |  | next_time |  | 0 | draw | kind=card side=mine zone=deck_top |  |  |  |  |  | amount=1 |  |  |

