# Stored rows of 20 cards (check_table.py)

Each card: its name and text on one line, then its stored rows, one row per effect, then the rows of each keyword it has.
- ability: one numbered "when -> if -> do" unit of the card. Rows with the same ability number are one ability; they happen together, in effect order.
- effect: the step inside the ability. link says how a step joins the step before it: and = also; then = after it, using its result; if_done = only if it happened; or = instead (a choice); instead = replaces it.
- pick=it in a target = the thing the step before acted on (the drawn card, the summoned unit, the chosen enemy).
- A row labelled "keyword X" is what keyword X does; the card has it, so the card does it too.
- Targets, events, conditions and amounts are written in place as their stored fields.

**Dubious Hags**: On death, spawn a 1 strength enemy Raven on a random bordering tile

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | dies |  | pick=self |  |  | 0 | summon | kind=unit side=enemy | kind=position pick=random with[position is bordering] |  | Token Ravens |  |  | strength=1 |  |  |

**Marked as Prey**: Deal 6/7/8/9/11 damage to a target poisoned unit. If that kills it, spawn a 6/7/8/9/11 strength Raven there

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  | (test=event_count op=ge n=1 span=this_turn event=(event=dies object=(pick=it))) | 0 | damage | kind=unit pick=chosen zone=board with[state is poisoned] |  |  |  |  |  | amount={x=per_level items=6, 7, 8, 9, 11} |  |  |
| 0 | played |  | pick=self |  | (test=event_count op=ge n=1 span=this_turn event=(event=dies object=(pick=it))) | 1 | summon |  | kind=position pick=it |  | Token Ravens |  |  | strength={x=per_level items=6, 7, 8, 9, 11} |  | if_done |

**Faithless Prophets**: After surviving damage, convert itself

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | survives_damage |  | pick=self |  |  | 0 | steal | pick=self |  |  |  |  |  |  | permanent |  |

**Ozone Purifiers**: On play, push a random bordering enemy unit away

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | move | kind=unit side=enemy pick=random zone=board with[position is bordering] |  |  |  | Push |  |  |  |  |

**Armed Schemers**: On play, pull enemy units towards itself. Then deal 3/4/5/6/7 damage to bordering enemy units

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | move | kind=unit side=enemy pick=all zone=board | pick=self |  |  | Pull |  |  |  |  |
| 0 | played |  | pick=self |  |  | 1 | damage | kind=unit side=enemy pick=all zone=board with[position is bordering] |  |  |  |  |  | amount={x=per_level items=3, 4, 5, 6, 7} |  | then |

**Temple of Space**: When played with a friendly copy on the board, teleport 2/3/4/6/8 surrounding units from it then destroy the older copy. Otherwise, return a 2 cost copy to hand

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  | (test=count of=(kind=landmark side=mine zone=board with[card is Temple of Space]) op=ge n=2) | 0 | move | kind=unit pick=all n={x=per_level items=2, 3, 4, 6, 8} zone=board with[position is surrounding] | pick=self |  |  |  |  |  |  |  |
| 0 | played |  | pick=self |  | (test=count of=(kind=landmark side=mine zone=board with[card is Temple of Space]) op=ge n=2) | 1 | kill | kind=landmark side=mine zone=board with[card is Temple of Space] |  |  |  |  |  |  |  | then |
| 1 | played |  | pick=self |  | (test=count of=(kind=landmark side=mine zone=board with[card is Temple of Space]) op=lt n=2) | 0 | copy | pick=self |  | hand |  |  |  |  |  |  |
| 1 | played |  | pick=self |  | (test=count of=(kind=landmark side=mine zone=board with[card is Temple of Space]) op=lt n=2) | 1 | cost_set | pick=it |  |  |  |  |  | cost=2 | permanent | then |

**Freebooters**: On play, draw 1/1/1/2/2 card/card/card/cards/cards

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | draw | kind=card side=mine zone=deck_top |  |  |  |  |  | amount={x=per_level items=1, 1, 1, 2, 2} |  |  |

**Snake Eyes**: When played with a full hand, discard all cards and draw 4 new cards

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | discard | kind=card side=mine pick=all zone=hand |  |  |  |  |  |  |  |  |
| 0 | played |  | pick=self |  |  | 1 | draw | kind=card side=mine zone=deck_top |  |  |  |  |  | amount=4 |  | then |

**Trueshot Post**: At the start of your turn, deal 4/5/7/8/9 damage to the most forward enemy unit or structure

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | turn_start | kind=player side=mine |  |  |  | 0 | damage | kind=unit_or_structure side=enemy zone=board with[position is most_forward] |  |  |  |  |  | amount={x=per_level items=4, 5, 7, 8, 9} |  |  |

**Melodious Sisters**: Before attacking a confused unit, deal 4/5/6/7/8 damage to all enemies surrounding it

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attacks | pick=self | kind=unit zone=board with[state is confused] |  |  | 0 | damage | kind=anything side=enemy pick=all zone=board with[position is surrounding of (pick=it)] |  |  |  |  |  | amount={x=per_level items=4, 5, 6, 7, 8} |  |  |

**Bigthrust Tigers**: On play, gain speed equal to the amount of enemy units in front

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | stat_change | pick=self |  |  |  |  |  | movement={x=count of=(kind=unit side=enemy pick=all zone=board with[position is ahead])} | permanent |  |

**Trekking Aldermen**: After surviving damage, deal as much damage as taken spread randomly among enemy units

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | survives_damage |  | pick=self |  |  | 0 | damage | kind=unit side=enemy pick=all zone=board |  |  |  |  |  | amount={x=event_amount}; spread=1 |  |  |

**Rogue Sheep**: On play, draw 1/1/2/2/3 single-use non-pirate card copy/copy/copies/copies/copies from the enemy’s hand. Decrease its/its/their/their/their mana cost by 1 if you have a pirate card in your hand

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | copy | kind=card side=enemy pick=random n={x=per_level items=1, 1, 2, 2, 3} zone=hand with[type not Pirate; state is single_use] |  | hand |  |  |  |  |  |  |
| 1 | played |  | pick=self |  | (test=have of=(kind=card side=mine zone=hand with[type is Pirate]) op=is) | 0 | cost_change | pick=it |  |  |  |  |  | cost=-1 | permanent |  |

**Quakefall of the Skies**: Deal 2/3/4/5/6 damage to non-temple structures, then deal 2/3/4/5/6 damage to surrounding enemy units and structures

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | damage | kind=landmark pick=all zone=board with[name_has not Temple] |  |  |  |  |  | amount={x=per_level items=2, 3, 4, 5, 6} |  |  |
| 0 | played |  | pick=self |  |  | 1 | damage | kind=unit_or_structure side=enemy pick=all zone=board with[position is surrounding of (pick=it)] |  |  |  |  |  | amount={x=per_level items=2, 3, 4, 5, 6} |  | then |

**Awakening of the Will**: Give strength to 1/1/2/2/3 random friendly unit/unit/units/units/units with no ability equal to its mana cost, then repeat this effect for up to 1/2/2/4/5 of its mana cost

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | stat_change | kind=unit side=mine pick=random n={x=per_level items=1, 1, 2, 2, 3} zone=board |  |  |  |  |  | strength={x=stat of=(pick=it) attr=cost} | permanent |  |
| 0 | played |  | pick=self |  |  | 1 | repeat | kind=effect pick=it |  |  |  |  |  | max={x=per_level items=1, 2, 2, 4, 5} |  | then |

**Forgotten Souls**: On play, command a/a/// random/random/// bordering/bordering/bordering/bordering/surrounding friendly unit/unit/units/units/units forward

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  | (test=level op=le n=2) | 0 | move | kind=unit side=mine pick=random zone=board with[position is bordering] |  |  |  | Command |  |  |  |  |
| 1 | played |  | pick=self |  | (test=level op=ge n=3) and (test=level op=le n=4) | 0 | move | kind=unit side=mine pick=all zone=board with[position is bordering] |  |  |  | Command |  |  |  |  |
| 2 | played |  | pick=self |  | (test=level op=eq n=5) | 0 | move | kind=unit side=mine pick=all zone=board with[position is surrounding] |  |  |  | Command |  |  |  |  |

**Lasting Remains**: After attacking, move forward

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | attack_done | pick=self |  |  |  | 0 | move | pick=self | kind=position with[position is in_front] |  |  |  |  |  |  |  |

**Snowman**: At the start of your turn, make surrounding friendly units deal 1 damage to the first enemy in front

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | turn_start | kind=player side=mine |  |  |  | 0 | damage | kind=anything side=enemy zone=board with[position is first_in_front] |  |  |  |  |  | amount=1; times={x=count of=(kind=unit side=mine pick=all zone=board with[position is surrounding])} |  |  |

**Underground Spring**: At the start of your turn, remove 1/1-2/2/2/2 strength from itself and give it to your base

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | turn_start | kind=player side=mine |  |  |  | 0 | stat_change | pick=self |  |  |  |  |  | strength={x=minus inner={x=per_level items=1, {x=range items=1, 2}, 2, 2, 2}} | permanent |  |
| 0 | turn_start | kind=player side=mine |  |  |  | 1 | stat_change | kind=player side=mine |  |  |  |  |  | strength={x=per_level items=1, {x=range items=1, 2}, 2, 2, 2} | permanent | then |

**Orgone Leechers**: Before moving, lose 3 mana and freeze an enemy in the tile in front. Decrease the loss by 2 for each other friendly Ancient and Frostling

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | moves |  | pick=self |  |  | 0 | mana_gain | kind=mana side=mine |  |  |  |  |  | amount={x=sum items=-3, {x=double inner={x=count of=(kind=unit side=mine pick=all zone=board with[type in Ancient; type in Frostling; card not Orgone Leechers])}}} |  |  |
| 0 | moves |  | pick=self |  |  | 1 | give_keyword | kind=unit side=enemy zone=board with[position is in_front of (pick=self)] |  |  |  | Freeze |  |  | next_own_turn | and |

