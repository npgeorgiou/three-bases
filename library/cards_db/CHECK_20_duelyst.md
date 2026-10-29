# Stored rows of 20 cards (check_table.py)

Each card: its name and text on one line, then its stored rows, one row per effect, then the rows of each keyword it has.
- ability: one numbered "when -> if -> do" unit of the card. Rows with the same ability number are one ability; they happen together, in effect order.
- effect: the step inside the ability. link says how a step joins the step before it: and = also; then = after it, using its result; if_done = only if it happened; or = instead (a choice); instead = replaces it.
- pick=it in a target = the thing the step before acted on (the drawn card, the summoned unit, the chosen enemy).
- A row labelled "keyword X" is what keyword X does; the card has it, so the card does it too.
- Targets, events, conditions and amounts are written in place as their stored fields.

**Kage Lightning**: Deal 5 damage to an enemy minion.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | damage | kind=unit side=enemy pick=chosen zone=board |  |  |  |  |  | amount=5 |  |  |

**Blood Baronette**: Opening Gambit: Double a nearby Wraithling's Attack and Health. (keywords: Opening Gambit)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | stat_set | kind=unit side=mine pick=chosen zone=board with[position is surrounding; card is Wraithling] |  |  |  |  |  | power={x=double inner={x=stat of=(pick=it) attr=power}}; health={x=double inner={x=stat of=(pick=it) attr=health}} |  |  |
| keyword Opening Gambit |  |  |  |  |  |  | (a trigger label: event played) |  |  |  |  |  |  |  |  |  |

**Frigid Corona**: Stun an enemy minion. Draw a card.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | give_keyword | kind=unit side=enemy pick=chosen zone=board |  |  |  | Stunned |  |  | next_own_turn |  |
| 0 | played |  | pick=self |  |  | 1 | draw | kind=card side=mine zone=deck_top |  |  |  |  |  | amount=1 |  | and |

**Keshrai Fanblade**: Opening Gambit: Next turn, opponent's spells cost 2 more to cast (keywords: Opening Gambit)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | cost_change | kind=card side=enemy pick=all zone=hand with[category is spell] |  |  |  |  |  | cost=2 | next_round |  |
| keyword Opening Gambit |  |  |  |  |  |  | (a trigger label: event played) |  |  |  |  |  |  |  |  |  |

**Cryogenesis**: Deal 4 damage to an enemy minion. Draw a Vespyr minion from your deck.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | damage | kind=unit side=enemy pick=chosen zone=board |  |  |  |  |  | amount=4 |  |  |
| 0 | played |  | pick=self |  |  | 1 | draw | kind=card side=mine zone=deck with[type is Vespyr; category is unit] |  |  |  |  |  | amount=1 |  | and |

**Fifth Canopic**: The enemy General cannot cast their Bloodbound Spell.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | always |  |  |  |  | 0 | cant | kind=player side=enemy | kind=spell with[keyword is Bloodbound Spell] |  |  |  |  | event=played | while |  |

**Z0r**: Dying Wish: Put a random MECH minion into your action bar. (keywords: Dying Wish)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | dies |  | pick=self |  |  | 0 | create | kind=card side=mine pick=random zone=hand with[category is unit; type is Mech] |  | hand |  |  |  |  |  |  |
| keyword Dying Wish |  |  |  |  |  |  | (a trigger label: event dies) |  |  |  |  |  |  |  |  |  |

**Thumping Wave**: Give a minion +5 Attack. At end of turn, transform it into a 3/3 Kin.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | stat_change | kind=unit pick=chosen zone=board |  |  |  |  |  | power=5 | permanent |  |
| 1 | turn_end | kind=player side=mine |  | next_time |  | 0 | transform | pick=it |  |  | Kin |  |  | power=3; health=3 |  |  |

**Cascading Rebirth**: Destroy a friendly minion to summon a random Magmar minion that costs 1 more.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | kill | kind=unit side=mine pick=chosen zone=board |  |  |  |  |  |  |  |  |
| 0 | played |  | pick=self |  |  | 1 | summon | kind=unit pick=random zone=board with[cost eq {x=sum items={x=stat of=(pick=it) attr=cost}, 1}; region is Magmar Aspects] |  |  |  |  |  |  |  | then |

**Riftwalker**: Keywords: Airdrop. Intensify: Deal 1 damage to everything around it. (keywords: Airdrop)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | damage | kind=any pick=all with[position is surrounding] |  |  |  |  |  | amount={x=product items=1, {x=event_count event=(event=played object=(kind=card side=mine with[card is Riftwalker])) span=this_game}} |  |  |
| keyword Airdrop: 0 | always |  |  |  |  | 0 | can | pick=self | kind=position |  |  |  |  | event=played | while |  |

**Crossbones**: Opening Gambit: Destroy an enemy minion with Ranged. (keywords: Opening Gambit)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | kill | kind=unit side=enemy pick=chosen zone=board with[keyword is Ranged] |  |  |  |  |  |  |  |  |
| keyword Opening Gambit |  |  |  |  |  |  | (a trigger label: event played) |  |  |  |  |  |  |  |  |  |

**Bloodtide Priestess**: Deathwatch: Summon a Wraithling on a random nearby space.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | dies |  | kind=unit |  |  | 0 | summon |  | kind=position pick=random with[position is surrounding] |  | Wraithling |  |  |  |  |  |

**Bastion**: At the end of your turn, give all friendly minions +1 health.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | turn_end | kind=player side=mine |  |  |  | 0 | stat_change | kind=unit side=mine pick=all zone=board |  |  |  |  |  | health=1 | permanent |  |

**Flamewreath**: Whenever this minion is moved for any reason, it deals 2 damage to all enemies around it.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | moves |  | pick=self |  |  | 0 | damage | kind=unit side=enemy pick=all zone=board with[position is surrounding] |  |  |  |  |  | amount=2 |  |  |

**Flaming Stampede**: Deal 8 damage to ALL non-Egg minions and Generals.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | damage | kind=any pick=all with[name_has not Egg] |  |  |  |  |  | amount=8 |  |  |

**Zephyr**: Blood Surge: Your General gains Frenzy this turn.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | kind=spell side=mine with[keyword is Bloodbound Spell] |  |  | 0 | give_keyword | kind=player side=mine |  |  |  | Frenzy |  |  | this_round |  |

**Golden Justicar**: Keywords: Provoke. Your other minions with Provoke can move two additional spaces. (keywords: Provoke)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | always |  |  |  |  | 0 | stat_change | kind=unit side=mine pick=all zone=board with[keyword is Provoke; card not Golden Justicar] |  |  |  |  |  | movement=2 | while |  |
| keyword Provoke: 0 | always |  |  |  |  | 0 | cant | kind=any side=enemy pick=all zone=board with[position is surrounding of (pick=self)] |  |  |  |  |  | event=moves | while |  |
| keyword Provoke: 0 | always |  |  |  |  | 1 | cant | kind=any side=enemy pick=all zone=board with[position is surrounding of (pick=self)] | kind=any side=mine pick=all with[keyword not Provoke] |  |  |  |  | event=attacks | while | and |

**First Sword of Akrane**: Your other minions have +1 Attack.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | always |  |  |  |  | 0 | stat_change | kind=unit side=mine pick=all zone=board with[card not First Sword of Akrane] |  |  |  |  |  | power=1 | while |  |

**Omniseer**: Opening Gambit: Turn a nearby space into Primal Flourish. (keywords: Opening Gambit)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | set_terrain | kind=position pick=chosen with[position is surrounding] | kind=position with[terrain is growth_space] |  |  | Primal Flourish |  |  |  |  |
| keyword Opening Gambit |  |  |  |  |  |  | (a trigger label: event played) |  |  |  |  |  |  |  |  |  |

**Whisper of the Sands**: Summon a Wind Dervish nearby each friendly Obelysk.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | summon |  | kind=position pick=chosen with[position is surrounding of (kind=unit side=mine pick=all zone=board with[name_has is Obelysk])] |  | Wind Dervish |  |  | amount={x=count of=(kind=unit side=mine pick=all zone=board with[name_has is Obelysk])} |  |  |

