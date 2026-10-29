# Stored rows of 20 cards (check_table.py)

Each card: its name and text on one line, then its stored rows, one row per effect, then the rows of each keyword it has.
- ability: one numbered "when -> if -> do" unit of the card. Rows with the same ability number are one ability; they happen together, in effect order.
- effect: the step inside the ability. link says how a step joins the step before it: and = also; then = after it, using its result; if_done = only if it happened; or = instead (a choice); instead = replaces it.
- pick=it in a target = the thing the step before acted on (the drawn card, the summoned unit, the chosen enemy).
- A row labelled "keyword X" is what keyword X does; the card has it, so the card does it too.
- Targets, events, conditions and amounts are written in place as their stored fields.

**Red Hart**: Keywords: Spilled Blood, Sprinter. (keywords: Spilled Blood, Sprinter)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| keyword Spilled Blood: 0 | always |  |  |  |  | 0 | stat_set | pick=self |  |  |  |  |  | power={x=event_count event=(event=sacrificed) span=this_turn} |  |  |
| keyword Sprinter: 0 | turn_end | kind=player side=mine |  |  |  | 0 | move | pick=self | kind=position with[position is sides] |  |  |  |  |  |  |  |

**Sapphire Vessel**: Keywords: Blue Mox. (keywords: Blue Mox)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| keyword Blue Mox: 0 | played |  | pick=self |  |  | 0 | mana_gain | kind=gem side=mine with[region is Blue] |  |  |  |  |  | amount=1 |  |  |
| keyword Blue Mox: 1 | always |  |  |  |  | 0 | cost_change | kind=card side=mine pick=all with[keyword is Gemified] |  |  |  |  |  | cost=-1 | while |  |

**Gem Guardian**: Keywords: Gem Guardian (sigil). (keywords: Gem Guardian (sigil))

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| keyword Gem Guardian (sigil): 0 | played |  | pick=self |  |  | 0 | give_keyword | kind=unit side=mine pick=all zone=board with[name_has is Vessel] |  |  |  | Armored |  |  | permanent |  |

**ExeSkeleton**: Keywords: Brittle. (keywords: Brittle)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| keyword Brittle: 0 | attack_done | pick=self |  |  |  | 0 | kill | pick=self |  |  |  |  |  |  |  |  |

**Mothman**: Keywords: Airborne. (keywords: Airborne)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| keyword Airborne: 0 | attacks | pick=self |  |  |  | 0 | strike | pick=self | kind=player side=enemy |  |  |  |  |  |  |  |

**Mirror Tentacle**: Keywords: M!rror r0rriM. (keywords: M!rror r0rriM)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| keyword M!rror r0rriM: 0 | always |  |  |  | (test=have of=(kind=unit side=enemy zone=board with[position is same_lane]) op=is) | 0 | stat_set | pick=self |  |  |  |  |  | power={x=stat of=(kind=unit side=enemy zone=board with[position is same_lane]) attr=power} |  |  |
| keyword M!rror r0rriM: 1 | always |  |  |  | (test=have of=(kind=unit side=enemy zone=board with[position is same_lane]) op=not) | 0 | stat_set | pick=self |  |  |  |  |  | power=0 |  |  |

**Hydra**: Keywords: Bifurcated Strike, Trifurcated Strike. (keywords: Bifurcated Strike, Trifurcated Strike)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| keyword Bifurcated Strike: 0 | attacks | pick=self |  |  |  | 0 | strike | pick=self | kind=unit side=enemy pick=all zone=board with[position is sides of (kind=position side=enemy with[position is same_lane])] |  |  |  |  |  |  |  |
| keyword Trifurcated Strike: 0 | attacks | pick=self |  |  |  | 0 | strike | pick=self | kind=unit side=enemy pick=all zone=board with[position is sides of (kind=position side=enemy with[position is same_lane])] |  |  |  |  |  |  |  |
| keyword Trifurcated Strike: 0 | attacks | pick=self |  |  |  | 1 | strike | pick=self | kind=unit side=enemy zone=board with[position is same_lane] |  |  |  |  |  |  | and |

**Mole (Act III)**: Keywords: Burrower. (keywords: Burrower)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| keyword Burrower: 0 | strikes | kind=unit side=enemy | kind=position with[state is empty] |  |  | 0 | move | pick=self | pick=it |  |  |  |  |  |  |  |

**Spore Mice**: Keywords: Fecundity, Fecundity. Traits: Fused. (keywords: Fecundity, Fecundity)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| keyword Fecundity: 0 | played |  | pick=self |  |  | 0 | copy | pick=self |  | hand |  |  |  |  |  |  |
| keyword Fecundity: 0 | played |  | pick=self |  |  | 0 | copy | pick=self |  | hand |  |  |  |  |  |  |

**Sentry Drone**: Keywords: Sentry. (keywords: Sentry)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| keyword Sentry: 0 | moves |  | kind=unit side=enemy with[position is same_lane] |  |  | 0 | damage | pick=it |  |  |  |  |  | amount=1 |  |  |

**Emerald Vessel**: Keywords: Green Mox. (keywords: Green Mox)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| keyword Green Mox: 0 | played |  | pick=self |  |  | 0 | mana_gain | kind=gem side=mine with[region is Green] |  |  |  |  |  | amount=1 |  |  |
| keyword Green Mox: 1 | always |  |  |  |  | 0 | stat_change | kind=unit side=mine pick=all zone=board with[keyword is Gemified] |  |  |  |  |  | health=2 | while |  |

**Bonehound**: Keywords: Guardian. (keywords: Guardian)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| keyword Guardian: 0 | summoned |  | kind=unit side=enemy |  | (test=have of=(kind=position side=mine with[position is same_lane of (pick=it); state is empty]) op=is) | 0 | move | pick=self | kind=position with[position is same_lane of (pick=it)] |  |  |  |  |  |  |  |

**Hoggy Bank**: Rulebook: To the user: You will immediately gain 4 Bones.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | mana_gain | kind=secondary_resource side=mine |  |  |  |  |  | amount=4 |  |  |

**Fish Hook**: Rulebook: To the user: Hook one of my cards and take it as your own. You must have an empty space on your side to receive it. The Fish Hook is a consumable item in Act I. It allows you to pull one of your opponent's cards to your side of the board, placing it under your control. You must have an empty space on your side of the board in the same lane as the targeted card; if you do not, you cannot use the Fish Hook on that card.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  | (test=count of=(kind=position side=mine with[state is empty; position is same_lane of (pick=it)]) op=ge n=1) | 0 | steal | kind=unit side=enemy pick=chosen zone=board |  |  |  |  |  |  |  |  |

**Hammer**: The Hammer is a tool in Act II and Act III of Inscryption. It can be used on any card on the player's side, including terrain cards, dealing 100 damage to said card. If used on a card with Nano Armor, it will break the Nano Armor first. It will also activate any on death abilities, such as Latchers, Unkillable, and Detonator, assuming the card actually dies from the hit.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | damage | kind=unit side=mine pick=chosen zone=board |  |  |  |  |  | amount=100 |  |  |

**The Moon**: Keywords: Mighty Leap, Omni Strike, Tidal Lock, Uncuttable. Traits: Giant (Increases its Power by 1 every turn after all cards are drawn). Special behaviour: When a card is spawned on the board, it replaces all spaces on opponent's side of the board with itself. When a card perishes, it clears all spaces on opponent's side of the board. (keywords: Mighty Leap, Omni Strike, Tidal Lock, Uncuttable)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | turn_start | kind=player side=mine |  |  | (test=count of=(kind=card side=mine zone=deck) op=eq n=0) | 0 | stat_change | pick=self |  |  |  |  |  | power=1 | permanent |  |
| keyword Mighty Leap: 0 | always |  |  |  |  | 0 | can | pick=self | kind=unit side=enemy with[keyword is Airborne] |  |  |  |  | event=blocks | while |  |
| keyword Omni Strike: 0 | attacks | pick=self |  |  |  | 0 | strike | pick=self | kind=unit side=enemy pick=all zone=board |  |  |  |  |  |  |  |
| keyword Omni Strike: 0 | attacks | pick=self |  |  |  | 1 | strike | pick=self | kind=player side=enemy |  |  |  |  |  |  | or |
| keyword Tidal Lock: 0 | turn_start | kind=player side=mine |  |  |  | 0 | move | kind=unit pick=all zone=board with[card is Squirrel] | kind=position with[position is bordering] |  |  |  |  |  |  |  |
| keyword Uncuttable: 0 | targeted | kind=equipment with[card in Scissors; card in Skinning Knife; card in Fish Hook] | pick=self |  |  | 0 | counter | kind=effect pick=it |  |  |  |  |  |  |  |  |

**Special Dagger**: The Special Dagger is an item in Act I of Inscryption. When used, it adds a weight worth 4 points to the scale in your favor, at the cost of your right eye. Your vision will be impaired for the rest of the battle, but Leshy will let you choose a new eye when it ends. It is semi-unique, as while you can obtain it several times in a run, you can never have more than one copy of the Dagger at any given time.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | damage | kind=player side=enemy |  |  |  |  |  | amount=4 |  |  |

**Wiseclock**: Rulebook: To the user: All creatures on the board will rotate one space clockwise.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | move | kind=unit side=any pick=all zone=board |  |  |  |  |  |  |  |  |

**Magickal Bleach**: Rulebook: To the user: My cards on the board will lose all of their Sigils.

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | played |  | pick=self |  |  | 0 | remove_keywords | kind=unit side=enemy pick=all zone=board |  |  |  |  |  |  |  |  |

**Ourobot**: Keywords: Unkillable. Special behaviour: A card's base Power and Health are permanently incremented by 1 each time card perishes. (keywords: Unkillable)

| ability | when_event | when_actor | when_object | when_limit | if | effect | act | on | to | zone | card | keyword | type | params | lasts | link |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | dies |  | pick=self |  |  | 0 | stat_change | pick=self |  |  |  |  |  | power=1; health=1 | this_run |  |
| keyword Unkillable: 0 | dies |  | pick=self |  |  | 0 | return_card | pick=self |  | hand |  |  |  |  |  |  |

