# Stored rows of 20 cards (check_table.py)

Each card: its name and text on one line, then its stored rows, one row per effect, then the rows of each keyword it has.
- ability: one numbered "when -> if -> do" unit of the card. Rows with the same ability number are one ability; they happen together, in effect order.
- effect: the step inside the ability. link says how a step joins the step before it: and = also; then = after it, using its result; if_done = only if it happened; or = instead (a choice); instead = replaces it.
- pick=it in a target = the thing the step before acted on (the drawn card, the summoned unit, the chosen enemy).
- A row labelled "keyword X" is what keyword X does; the card has it, so the card does it too.
- Targets, events, conditions and amounts are written in place as their stored fields.

**Eredon, Voice of All**: Last Words - Give all creatures in your deck and hand +1/+1.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | dies |  | pick=self |  |  | 0 | stat_change | kind=card side=mine pick=all zone=deck with[category is unit] |  |  |  |  |  | power=1; health=1 | permanent |  |
| 0 | dies |  | pick=self |  |  | 1 | stat_change | kind=card side=mine pick=all zone=hand with[category is unit] |  |  |  |  |  | power=1; health=1 | permanent | and |

**Windborne Champion**: Flying, Charge 5 Gift - Move a creature. (keywords: Flying, Charge)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Flying |  |  | permanent |  |
| 0 | always |  |  |  |  | 1 | give_keyword | pick=self |  |  |  | Charge |  | amount=5 | permanent | and |
| 1 | played |  | pick=self |  |  | 0 | move | kind=unit pick=chosen zone=board |  |  |  |  |  |  |  |  |
| keyword Flying: 0 | always |  |  |  |  | 0 | can | pick=self | kind=position with[terrain in ocean; terrain in land] |  |  |  |  | event=moves | while |  |
| keyword Charge: 0 | always |  |  |  |  | 0 | can | pick=self | kind=position with[position is straight_line of (pick=self)] |  |  |  |  | event=moves | while |  |

**Elderwood Hermit**: Last Words - Give a random friendly creature +2/+4.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | dies |  | pick=self |  |  | 0 | stat_change | kind=unit side=mine pick=random zone=board |  |  |  |  |  | power=2; health=4 | permanent |  |

**Istanu, Eternal Light**: Flying, Charge 3 Last Words - A random friendly creature becomes the new Istanu. (keywords: Flying, Charge)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Flying |  |  | permanent |  |
| 0 | always |  |  |  |  | 1 | give_keyword | pick=self |  |  |  | Charge |  | amount=3 | permanent | and |
| 1 | dies |  | pick=self |  |  | 0 | transform | kind=unit side=mine pick=random zone=board |  |  | Istanu, Eternal Light |  |  |  |  |  |
| keyword Flying: 0 | always |  |  |  |  | 0 | can | pick=self | kind=position with[terrain in ocean; terrain in land] |  |  |  |  | event=moves | while |  |
| keyword Charge: 0 | always |  |  |  |  | 0 | can | pick=self | kind=position with[position is straight_line of (pick=self)] |  |  |  |  | event=moves | while |  |

**Possessed Ursus**: After this creature is dealt damage, double its Attack.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | damaged |  | pick=self |  |  | 0 | stat_set | pick=self |  |  |  |  |  | power={x=double inner={x=stat of=(pick=self) attr=power}} |  |  |

**Hunt Down**: Give a friendly beast +2/+0. Then it fights an enemy creature.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | stat_change | kind=unit side=mine pick=chosen zone=board with[type is beast] |  |  |  |  |  | power=2 | permanent |  |
| 0 | played |  | pick=self |  |  | 1 | start_attack | pick=it | kind=unit side=enemy pick=chosen zone=board |  |  | Fight |  |  |  | then |

**Rakoan Reveller**: Last Words - Gain 1 faeria equal to this creature's attack.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | dies |  | pick=self |  |  | 0 | mana_gain | kind=player side=mine |  |  |  |  |  | amount={x=stat of=(pick=self) attr=power} |  |  |

**Water Elemental**: Jump Gift - Create lake (keywords: Jump)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Jump |  |  | permanent |  |
| 1 | played |  | pick=self |  |  | 0 | set_terrain | kind=position pick=chosen with[terrain is ocean] | kind=position with[terrain is lake] |  |  |  |  |  |  |  |
| keyword Jump: 0 | always |  |  |  |  | 0 | can | pick=self | kind=position with[distance le 2 of (pick=self)] |  |  |  |  | event=moves | while |  |

**Barter**: Discover an event from your opponent's deck. It becomes wild land and costs 2 faeria less.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | keyword_action | kind=card side=enemy zone=deck with[category is spell] |  | hand |  | Discover |  |  | unstated |  |
| 0 | played |  | pick=self |  |  | 1 | give_keyword | pick=it |  |  |  | Wild |  |  | permanent | and |
| 0 | played |  | pick=self |  |  | 2 | cost_change | pick=it |  |  |  |  |  | cost=-2 | permanent | and |

**Spring Mochi**: Gift - The next card you draw with an original cost of 7 faeria or higher costs 3 faeria less.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | give_ability | kind=player side=mine |  |  |  |  |  |  |  |  |
| 0.0.1 (given by effect 0) | drawn |  | kind=card side=mine zone=hand with[cost ge 7] | next_time |  | 0 | cost_change | pick=it |  |  |  |  |  | cost=-3 | permanent |  |

**Seed Sower**: Gift - Create an adjacent forest at random.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | set_terrain | kind=position pick=random with[terrain is ocean; position is bordering] | kind=position with[terrain is forest] |  |  |  |  |  |  |  |

**Bone Collector**: Whenever an adjacent creature dies, this gains +1/+1.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | dies |  | kind=unit pick=all zone=board with[position is bordering] |  |  | 0 | stat_change | pick=self |  |  |  |  |  | power=1; health=1 | permanent |  |

**Seifer's Wrath**: Deal 2 damage to a creature. If it dies, deal 2 damage to its controller.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | damage | kind=unit pick=chosen zone=board |  |  |  |  |  | amount=2 |  |  |
| 0 | played |  | pick=self |  |  | 1 | damage | kind=player pick=owner |  |  |  |  |  | amount=2 |  | if_done |

**Blightborn Specter**: Charge 2 Production - If your opponent has 4 or more cards in hand, this gains +1/+1. (keywords: Charge, Production)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | always |  |  |  |  | 0 | give_keyword | pick=self |  |  |  | Charge |  | amount=2 | permanent |  |
| 1 | turn_start | kind=player side=mine |  |  | (test=count of=(kind=card side=enemy pick=all zone=hand) op=ge n=4) | 0 | stat_change | pick=self |  |  |  |  |  | power=1; health=1 | permanent |  |
| keyword Charge: 0 | always |  |  |  |  | 0 | can | pick=self | kind=position with[position is straight_line of (pick=self)] |  |  |  |  | event=moves | while |  |
| keyword Production |  |  |  |  |  |  | (a trigger label: event turn_start) |  |  |  |  |  |  |  |  |  |

**Rakoan Illusionist**: Gift - You may transform another friendly Rakoan into a 4/4 Flying Charge 2 Dune Drake until the start of your next turn.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | transform | kind=unit side=mine pick=chosen zone=board with[type is rakoan; card not Rakoan Illusionist] |  |  | Dune Drake |  |  | power=4; health=4 | next_own_turn |  |
| 0 | played |  | pick=self |  |  | 1 | give_keyword | pick=it |  |  |  | Flying |  |  | next_own_turn | and |
| 0 | played |  | pick=self |  |  | 2 | give_keyword | pick=it |  |  |  | Charge |  | amount=2 | next_own_turn | and |

**Faeria Tree**: Production - This structure gains +0/+1. When this has 5 or more Life, destroy it and gain 10 faeria. (keywords: Production)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | turn_start | kind=player side=mine |  |  |  | 0 | stat_change | pick=self |  |  |  |  |  | health=1 | permanent |  |
| 1 | always |  |  |  | (test=stat of=(pick=self) attr=health op=ge n=5) | 0 | kill | pick=self |  |  |  |  |  |  |  |  |
| 1 | always |  |  |  | (test=stat of=(pick=self) attr=health op=ge n=5) | 1 | mana_gain | kind=player side=mine |  |  |  |  |  | amount=10 |  | and |
| keyword Production |  |  |  |  |  |  | (a trigger label: event turn_start) |  |  |  |  |  |  |  |  |  |

**Sharra, Dragonslayer**: Sharra ignores all damage equal to 4 or more.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | always |  |  |  |  | 0 | negate_damage | pick=self |  |  |  |  |  | min=4 | while |  |

**Spirit Theft**: Drain 1 life from an enemy creature. If you kill it, add a copy of it to your hand. It becomes wild land.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | damage | kind=unit side=enemy pick=chosen zone=board |  |  |  |  |  | amount=1 |  |  |
| 0 | played |  | pick=self |  |  | 1 | heal | kind=player side=mine |  |  |  |  |  | amount={x=event_amount} |  | then |
| 0 | played |  | pick=self |  |  | 2 | copy | pick=it |  | hand |  |  |  |  |  | if_done |
| 0 | played |  | pick=self |  |  | 3 | give_keyword | pick=it |  |  |  | Wild |  |  | permanent | and |

**Dustbringer Wraith**: Corrupt - Increase the cost of each card in your opponent's hand by 1 faeria. (keywords: Corrupt)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | moves_onto |  | pick=self with[position is same_space of (kind=position side=enemy with[terrain is land])] | once_per_game |  | 0 | cost_change | kind=card side=enemy pick=all zone=hand |  |  |  |  |  | cost=1 | permanent |  |
| keyword Corrupt |  |  |  |  |  |  | (a trigger label: event moves_onto) |  |  |  |  |  |  |  |  |  |

**Triton Chef**: Gift - Add a Triton Banquet to your hand.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | create |  |  | hand | Triton Banquet |  |  |  |  |  |

