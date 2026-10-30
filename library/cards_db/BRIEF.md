# Reader brief: describe each card as a record (version 4)

You read card texts and write what each card DOES as JSON records. Every value is a number, a value from
`vocab.tsv` (column `value`, grouped by `field`), or the exact name of another card, keyword or type (the script turns names into
links). Never write free text. Never guess a rule the text does not state.

## Same values in every game
Every game is written with the same values, so one question finds cards of all games. Use the existing value that means the
same thing (the game's words are mapped in "Game words: <game>" below); propose a new value only when none fits, worded so
any game could use it. Say what a position is measured from ("of"). Give statuses with give_keyword and the keyword.
Mind the direction: steal takes the enemy's unit, donate gives away my own ("convert itself"). Mind who chooses: choose_one
= the player picks, random_one = chance picks, "X, otherwise Y" = two abilities with opposite conditions (rule 8).

## Output
One JSON object per line, one line per card, in the card order of the input, written to the output file you are given:
`{"id": <card id>, "abilities": [ABILITY, ...]}`
`"unsure"` (optional) is a list of field names that did not fit, see below.
A card that only has keywords from its Keywords field gets `"abilities": []`. Do NOT describe the card's own Keywords field:
the script attaches those from the keyword descriptions. DO describe keywords that the card gives, applies or uses on something
("Give an ally Barrier", "Stun an enemy", "Recall an ally", "Invoke").

If a card needs something the values cannot say, still write the closest correct record and add
`"unsure": [<the field names that did not fit>]` to that card's object, and write one line to the proposals file:
`{"id": <card id>, "field": <field>, "need": <short value name you would add>}`. Proposals are the only place for new words.

## Shapes
ABILITY  `{"when": EVENT, "limit": limit, "if": [COND, ...], "do": [EFFECT, ...]}`  (limit and if only when the text says so)
EVENT    `{"event": event, "actor": TARGET, "object": TARGET}`  actor = who does it, object = to whom it happens (omit what the text
         leaves open). A spell's effect and a unit's "Play:" use `{"event": "played", "object": {"pick": "self"}}`.
         Static abilities ("Allies have +1|+0", "I can't be blocked") use `{"event": "always"}`.
TARGET   `{"kind": kind, "side": side, "pick": pick, "n": AMOUNT, "zone": zone, "with": [FILTER, ...], "by": attr}`
         ("by" only with pick highest / lowest: "the ally with the highest Countdown" = pick highest, by countdown; "the
         strongest / weakest enemy" = pick highest / lowest, by power, in every game)  n defaults to 1;
         "all" targets use pick all and omit n. `{"pick": "self"}` alone means the card itself.
FILTER   `{"attr": "power|health|cost|base_power|base_health|damage|countdown", "op": op, "n": AMOUNT}` (n can compare to
         another value: "with less Power than me" = op lt, n `{"x": "stat", "attr": "power", "of": {"pick": "self"}}`)
         `{"attr": "keyword|type|card", "op": "is|not", "ref": "<exact name>"}`
         `{"attr": "state|category|region|origin|rarity", "op": "is|not", "val": <value of that field>}`
         one of several: `"op": "in"` with `"vals": [...]` or `"refs": [...]` ("a Fast spell, Slow spell, or Skill")
         card families by name: `{"attr": "name_has", "op": "is", "ref": "Crimson"}` ("Crimson allies", "Storm Conduits")
COND     `{"test": test, "of": TARGET, "attr": attr, "op": op, "n": AMOUNT, "span": span, "event": EVENT, "ref": "<name>",
          "value": AMOUNT}`
         (only the keys the test needs)
EFFECT   `{"act": act, "on": TARGET, "to": TARGET, "zone": zone, "card": "<exact name>", "keyword": "<exact name>",
          "type": "<exact type name>", "ability": ABILITY, "params": {param: AMOUNT}, "lasts": lasts, "link": link}`
         "ability" (with act give_ability): the whole ability given ("Grant allies 'Round End: Recall me'"); "type" (with
         act give_type). Numbers can be negative ("-1|-0", "costs 2 less" = cost -2).
         on = what the effect acts on; to = second target (strike X to Y, move to); zone = where a created or moved card goes;
         card = the card created, summoned or transformed into; keyword = the keyword given, removed or used.
         lasts is required for stat_change, give_keyword, cant, can, cost_change; link is required from the 2nd effect on.
AMOUNT   a number, or `{"x": x, "of": TARGET, "attr": attr, "event": EVENT, "span": span, "inner": AMOUNT, "items": [AMOUNT]}`
         (only the keys needed; "items" for x sum: "the number of allies stunned or recalled")
         Numbers per card level ("1/2/3/4/5"): `{"x": "per_level", "items": [1, 2, 3, 4, 5]}`.

## Reading rules
1. "I", "me", "my" = the card itself (pick self). "You", "your" = the player (kind player, side mine). "Allies" = side mine,
   "enemies" = side enemy. "Slay" / "when you kill" = event killed with actor the player, any way of killing.
2. "Play:" on a unit = event played, object self. "When I'm summoned" = event summoned, object self.
   "Last Breath:" = event dies, object self. "Attack:" = attacks, actor self. "Strike:" = strikes, actor self.
   "Nexus Strike:" = strikes_nexus, actor self. "Round Start:/Round End:" = round_start/round_end.
3. Condition keywords at the start of an ability (Daybreak, Nightfall, Plunder, Flow, Allegiance, Reputation, Enlightened,
   Empowered N, Behold) are a COND `{"test": "keyword_condition", "ref": "<keyword>"}` (Empowered also "n").
4. "Level up: X" = `{"when": {"event": "always"}, "if": [X as conds], "do": [{"act": "level_up", "on": {"pick": "self"}}]}`;
   if X starts with an event ("Round End: you've ..."), use that event in when.
5. Stats: "+2|+1" = stat_change with params power 2, health 1; "-1|-0" = power -1, health 0. "Grant" is permanent unless the
   text says "this round"; "give" with "this round" is this_round.
6. Numbers written as words become numbers. "that much" / "that amount" = `{"x": "event_amount"}` or the previous effect's
   amount; "for each X" = `{"x": "count", "of": X}`; "equal to its Power" = `{"x": "stat", "attr": "power", "of": TARGET}`.
7. "Create a <card> in hand" = create, zone hand, card <name>. A created card that the text describes but does not name
   ("a random 1 cost Poro") = create/summon with `"on"` describing it: `{"kind": "unit", "pick": "random", "with": [filters]}`.
8. "Choose one: A or B" = a choose_one effect, then A and B as effects with link or. "X, or if <the target> is Y, Z instead"
   = X (target filtered "not Y"), then Z with link instead (target pick it, filtered "Y"). "A random effect: A, B or C" =
   a random_one effect, then A, B, C with link or (nobody chooses). "X, or if <you / the game state> Y,
   Z" = two abilities with the same when: one with the cond "not Y" doing X, one with the cond "Y" doing Z (see Gnar).
9. Stages "I-II:" / "III:" = COND test stage, n 1 and 2 (two conds are OR inside one stage: write one ability per stage).
10. "When X or Y" (two different events) = one ability per event, same effects. "I or a Living Shadow strike" = two abilities.
11. A card, keyword or token the text names but names_in_text does not list: still write its exact name as the text spells
   it (singular: "2 Dauntless Vanguards" = card "Dauntless Vanguard", params amount 2). The script keeps it as a named stub.
12. Combat abilities have their own acts: first_strike (Quick Attack), double_strike, excess_damage (Overwhelm, on the enemy
   player), damage_reduction (Tough), strike_with (Formidable, params attr health). "can't" / "can only be blocked by X":
   act cant on the units that cannot act, params event, and `"to": {"pick": "self"}` (they cannot block ME).
13. "1 less for each X" = `{"x": "minus", "inner": {"x": "count", "of": X}}`. A condition that adds up a stat over events
   ("summon 12+ Power of Tech allies") is test event_count with "attr": "power" (the sum of that stat, not the number of
   events). One total over two events ("5+ units Stunned or Recalled") = `{"test": "amount", "value": {"x": "sum", "items":
   [{"x": "event_count", "event": EVENT1, "span": "this_game"}, {"x": "event_count", "event": EVENT2, "span": "this_game"}]},
   "op": "ge", "n": 5}`.
14. Delayed effects ("At the next Round Start, ...", "the next time an ally attacks this round") = an ability with that
   event and limit next_time. "A new card" (not played before) = state new. Damage totals = attr damage.
15. Keywords passed between units ("grant its keywords to all allies", "we share keywords", "gains the positive keywords of")
   = act copy_keywords: "on" receives, "to" is the unit whose keywords are copied; which keywords as a filter on "to"
   (`{"attr": "state", "op": "is", "val": "positive"}`). "Remove all negative keywords" = remove_keywords with that filter.
   "Another ally" / "other allies" always carries `{"attr": "card", "op": "not", "ref": "<this card's name>"}`.
16. Read every sentence. Remarks, reminders and flavour have no effect: skip them. Deck-building permissions ("You may put any Cultist cards into your deck during deckbuilding", Origin) have no
   effect in play: skip them. Never add an effect the text does not state.
17. Where cards are: a unit that died ("dead ally", "allies that died", revive) is kind unit, zone discard. A discarded card
   is kind card, zone discard (category unit if the text says unit). An obliterated or Tossed card is zone removed. A Captured
   card is zone removed ("my Captured enemies": side enemy, zone removed).
18. A copy ("a copy of me", "exact copies of the units stored inside", "an exact copy of an ally's equipment", "an Ephemeral
   copy") = act copy: on = the card or unit copied, zone = where the copy goes. Never summon, create or attach of the original.

19. Names in the text: a card listed in names_in_text = card; a keyword = keyword; a subtype = type; a family of cards by
   name that is no single card ("a random Husk", "Spritelings", "Mecha Yordles", "Turrets") = filter name_has. A word that
   is none of these ("it", "that keyword", "the Emperor's Deck") is never a card or keyword reference.

20. "Support:" = event supports, actor self; the supported ally is the unit to my right (pick right_of_self). "Attack:" is
   event attacks. Never write one for the other.

21. A unit put into play attacking ("summon an attacking Sand Soldier", "revive an attacking Ephemeral copy", "summon it
   attacking") = the summon / revive / copy, then `{"act": "start_attack", "on": {"pick": "it"}, "link": "and"}`. Never a
   state attacking filter on what is summoned.

22. A card that puts a named card into play ("summon a Stormcarved Spire that ... summons an exact copy of the unit")
   describes only its own part (what it obliterates, which card, the numbers it sets). What the named card then does is
   that card's own record; never copy it into this card.
23. A class of cards is its filter, never one card or a name family: "your traps", "traps or boons" = keyword Trap / Boon;
   "your spells" = category spell; "Imp units" = type Imp. Write one card only when the text names that card ("a Flashbomb
   Trap"). (Caitlyn's "5+ of your traps" was read as Flashbomb Trap, so Poison Puffcaps did not count.)
24. Whose event: "I've struck", "I've survived damage", "when I level up" = the event's object (or actor) pick self; "you
   dealt damage" = actor the player, side mine. Never leave out the "self": without it the card waits for any unit.
25. Write the kind of what is hit: a base, Nexus or Pyre is kind player; a unit is kind unit. Damage "to your base" is not
   damage to a unit.
26. Every target the text names gets a row; "or" makes two effects linked "or". "Deal 1 to three enemies or the enemy
   Nexus" = damage on enemy units AND, link "or", damage on the enemy player (Make it Rain lost the Nexus).
27. A class the text names is the whole class: "spells and Skills" / "Fast spells, Slow spells, and Skills" = category in
   spell, skill on every target the phrase names (28 Runeterra cards lost Skills).
28. Every word that narrows what is counted or picked is a filter: "8 cost reduced cards" = state cost_reduced; "damaged
   enemy" = state damaged; "allies with 5+ Power" = power ge 5. A count without its filter counts everything (Janna).
29. Amounts are what the text says: "double the damage" = amount event_amount (as much again), never 1 (The Dreadway);
   "everywhere" = zone everywhere on that target (Rek'Sai (level 2) lost it).
30. "A strikes B": act strike, on = the striker, to = what it hits; the damage is on "to", never on the striker.
31. One happening is written one way in every card: "strike the enemy Nexus" is strikes_nexus by the striking unit (actor),
   never with the player as its object. Before writing a happening, look at how the worked examples and vocab.tsv write it.
32. Do not write what the game's rules do for every card (a unit attacks, an unblocked attacker hits the enemy Nexus): that is
   in read/<game>/game_rules.jsonl, written once by the import chat. Write only what this card's text says.

## The board (every game with spaces, tiles, hexes, lanes or rows; one form for all)
- A space is `{"kind": "position"}`. Where a thing is = filter `{"attr": "position", "op": "is", "val": <position>, "of":
  TARGET}`; "of" omitted = the card itself. Never write a space as a unit target ("summon adjacent to friendly creatures" is a
  space bordering of `{"kind": "unit", "side": "mine"}`, keeping the units' own filters there: "next to friendly Yaks").
- Neighbours: touching along an edge = bordering (a square's 4, a hex's 6); with diagonals = surrounding; left/right =
  sides; only diagonals = diagonal. "On X" / "X's space" / "its land" = same_space of X. "On or adjacent to X" = one target,
  `{"attr": "position", "op": "in", "vals": ["same_space", "bordering"], "of": X}`, never two effects.
- Lines and areas: "in a straight line" = straight_line of the unit; "in its row / column" = same_row / same_column; named
  areas = area_2x2, area_3x3, corner, center_column, starting_side; "within N spaces", "up to N spaces" = `{"attr":
  "distance", "op": "le", "n": N, "of": X}` (distance counts steps on the grid).
- Ground: what a space is = filter `{"attr": "terrain", "op": "is", "val": ...}` (vocab field terrain: land, ocean, the land
  colours, special_land, resource_well, damage_space ...). A space's owner is its side ("a land you control" = side mine).
  "Empty", "unoccupied" = state empty. Making or changing ground ("create a forest", "turn a space into Shadow Creep",
  "destroy a land" = ocean) = set_terrain, "on" the spaces changed, "to" a position with the new terrain. Taking a space =
  steal on it; moving a land = move on it.
- Movement: moving a unit = move, "on" the unit, "to" the space (with what the text says of it). The event of having moved
  onto a space = moves_onto with the MOVER as object and the space as its filter `same_space of {the space}` (the same way
  as moves, N16): "Corrupt: the first time this moves onto enemy land" = object self with same_space of `{"kind":
  "position", "side": "enemy", "with": [terrain land]}`. A keyword that lets a unit move further or over things (Flying,
  Jump, Charge, Dash) is a `can moves` with "to" the reachable spaces (straight_line, distance, terrain).
- Placement: where a card may enter = `{"act": "can", "params": {"event": "summoned"}, "to": <the spaces>}`, "on" the card
  itself or the cards it lets in ("You can summon creatures next to this" = on my units, pick all). A condition on where it
  entered ("if summoned adjacent to an enemy well") = a COND on the played / summoned ability.
- Resources on the board (wells, springs): collecting one = event harvests, actor the unit, object the space (like strikes);
  emptying / refilling = empty_resource / refill_resource on the spaces.
- "In its place", "where this died" = the summon's "to" `{"kind": "position", "with": [same_space of {"pick": "it"}]}`.
- Room: how many spaces a unit takes = stat size (Monster Train's unit capacity); "takes up every space on its side" =
  stat_set size `{"x": "count", "of": {"kind": "position", "side": "mine", "zone": "board"}}` (it frees them when it leaves).
  Full: "if your board is full" / "no empty space" = COND have of `{"kind": "position", "side": "mine", "with": [state
  empty]}` op not; a board with a set number of units counts them (Runeterra: count of my units ge 6).

## Keyword entries (category keyword)
A keyword's record says what the keyword means, so that every card with it inherits that meaning. Four kinds:
- Status keywords (a unit has it: Elusive, Barrier, Stun, Quick Attack, Ephemeral, ...): abilities of the holder, "I" / "this
  unit" = pick self. Stun: `{"when": {"event": "always"}, "do": [{"act": "cant", "on": {"pick": "self"}, "params": {"event":
  "attacks"}, "lasts": "this_round"}, ...]}`. Quick Attack: `{"when": {"event": "attacks", "actor": {"pick": "self"}}, "do":
  [{"act": "first_strike", "on": {"pick": "self"}, "lasts": "this_round"}]}`.
- Action keywords (a card does it to something: Recall, Obliterate, Invoke, Predict, Toss, Nab, Rally, Forge, ...): one ability
  with `{"event": "activated"}`; what it acts on is `{"pick": "it"}` (the target the card names); numbers the card gives (Toss 2)
  are `{"x": "event_amount"}`.
- Trigger keywords (Play, Attack, Strike, Last Breath, Round Start, Round End, Nexus Strike, Support, Countdown...):
  `"trigger": EVENT` (the event value the keyword stands for) and `"abilities": []`.
- Condition keywords (Daybreak, Nightfall, Plunder, Flow, Allegiance, Enlightened, Empowered, Reputation, Behold):
  `"condition": [COND, ...]` and `"abilities": []`.
Play-speed keywords (Burst, Fast, Slow, Focus, Skill) and reminders with no effect: `"abilities": []`.
A condition that, once met, holds for the rest of the game ("once you have 15 or fewer cards in deck, you are Deep for the
rest of the game") = the test with `"span": "this_game"` (met at some moment this game).

## Worked examples (approved shapes)
Kindred - Keywords: Quick Attack. Each round, the first time you slay a unit, I mark the weakest enemy. Round End: Kill
units with my mark. Level up: I've seen you slay 2+ units with my mark.
{"id": 751268, "abilities": [
 {"when": {"event": "killed", "actor": {"kind": "player", "side": "mine"}, "object": {"kind": "unit"}}, "limit": "first_each_round",
  "do": [{"act": "mark", "on": {"kind": "unit", "side": "enemy", "pick": "lowest", "by": "power", "zone": "board"}, "lasts": "permanent"}]},
 {"when": {"event": "round_end"},
  "do": [{"act": "kill", "on": {"kind": "unit", "pick": "all", "zone": "board", "with": [{"attr": "state", "op": "is", "val": "marked"}]}}]},
 {"when": {"event": "always"},
  "if": [{"test": "event_count", "event": {"event": "killed", "actor": {"kind": "player", "side": "mine"}, "object": {"kind": "unit", "with": [{"attr": "state", "op": "is", "val": "marked"}]}}, "op": "ge", "n": 2, "span": "this_game"}],
  "do": [{"act": "level_up", "on": {"pick": "self"}}]}]}

Gnar - Keywords: Quick Attack. Strike: Create a Pokey Stick in hand or, if you have one, reduce its cost by 2. Level up:
Round End: You've damaged the enemy Nexus this round.
{"id": 751330, "abilities": [
 {"when": {"event": "strikes", "actor": {"pick": "self"}},
  "if": [{"test": "have", "op": "not", "of": {"kind": "card", "side": "mine", "zone": "hand", "with": [{"attr": "card", "op": "is", "ref": "Pokey Stick"}]}}],
  "do": [{"act": "create", "zone": "hand", "card": "Pokey Stick", "on": {"kind": "player", "side": "mine"}}]},
 {"when": {"event": "strikes", "actor": {"pick": "self"}},
  "if": [{"test": "have", "op": "is", "of": {"kind": "card", "side": "mine", "zone": "hand", "with": [{"attr": "card", "op": "is", "ref": "Pokey Stick"}]}}],
  "do": [{"act": "cost_change", "on": {"kind": "card", "side": "mine", "zone": "hand", "with": [{"attr": "card", "op": "is", "ref": "Pokey Stick"}]}, "params": {"cost": -2}, "lasts": "permanent"}]},
 {"when": {"event": "round_end"},
  "if": [{"test": "event_count", "event": {"event": "nexus_damaged", "object": {"kind": "player", "side": "enemy"}}, "op": "ge", "n": 1, "span": "this_round"}],
  "do": [{"act": "level_up", "on": {"pick": "self"}}]}]}

Barknuckles - Keywords: Equipment, Brash. Strike: Create a Coin in hand.   (Equipment's bonuses go to the equipped unit, so
"Strike" here is the equipped unit striking.)
{"id": 751867, "abilities": [
 {"when": {"event": "strikes", "actor": {"pick": "attached_to"}},
  "do": [{"act": "create", "zone": "hand", "card": "Coin", "on": {"kind": "player", "side": "mine"}}]}]}

Swain (level 2) - Keywords: Fearsome, Overwhelm. When you deal non-combat damage to the enemy Nexus, Stun the strongest
backrow enemy. Nexus Strike: Deal 3 to all enemies and the enemy Nexus.
{"id": 796499, "abilities": [
 {"when": {"event": "nexus_damaged", "actor": {"kind": "player", "side": "mine"}, "object": {"kind": "player", "side": "enemy"}},
  "if": [{"test": "it_matches", "of": {"with": [{"attr": "origin", "op": "not", "val": "combat"}]}}],
  "do": [{"act": "stun", "on": {"kind": "unit", "side": "enemy", "pick": "highest", "by": "power", "zone": "board", "with": [{"attr": "state", "op": "not", "val": "in_combat"}]}, "lasts": "this_round"}]},
 {"when": {"event": "strikes_nexus", "actor": {"pick": "self"}},
  "do": [{"act": "damage", "on": {"kind": "unit", "side": "enemy", "pick": "all", "zone": "board"}, "params": {"amount": 3}},
         {"act": "damage", "on": {"kind": "player", "side": "enemy"}, "params": {"amount": 3}, "link": "and"}]}]}
  ("backrow" = units not in combat; the stun target is described by that state.)

Jack - Keywords: Brash. Strike: Create a Coin in hand. When you refill mana, heal me 1 for each mana refilled. Level up:
You've spent 12+ mana in one round.
{"id": 751857, "abilities": [
 {"when": {"event": "strikes", "actor": {"pick": "self"}}, "do": [{"act": "create", "zone": "hand", "card": "Coin", "on": {"kind": "player", "side": "mine"}}]},
 {"when": {"event": "mana_refilled", "actor": {"kind": "player", "side": "mine"}},
  "do": [{"act": "heal", "on": {"pick": "self"}, "params": {"amount": {"x": "event_amount"}}}]},
 {"when": {"event": "always"}, "if": [{"test": "count", "of": {"kind": "mana", "side": "mine", "with": [{"attr": "state", "op": "is", "val": "spent"}]}, "op": "ge", "n": 12, "span": "this_round"}],
  "do": [{"act": "level_up", "on": {"pick": "self"}}]}]}


Coin - Keywords: Focus. Coins stack. Refill 1 mana.
{"id": 797090, "abilities": [{"when": {"event": "played", "object": {"pick": "self"}}, "do": [{"act": "mana_gain", "on": {"kind": "mana", "side": "mine"}, "params": {"amount": 1}}]}]}
  ("Coins stack" is a remark about the hand display: skipped.)

Pokey Stick - Deal 1 to anything. Draw 1.
{"id": 751403, "abilities": [{"when": {"event": "played", "object": {"pick": "self"}}, "do": [
 {"act": "damage", "on": {"kind": "any", "side": "any", "pick": "chosen"}, "params": {"amount": 1}},
 {"act": "draw", "on": {"kind": "card", "side": "mine", "zone": "deck_top"}, "params": {"amount": 1}, "link": "and"}]}]}

Stiffened Sinews - Keywords: Skill. Stun an enemy or if it's already Stunned deal 2 to it instead.
{"id": 796985, "abilities": [
 {"when": {"event": "played", "object": {"pick": "self"}}, "do": [
  {"act": "stun", "on": {"kind": "unit", "side": "enemy", "pick": "chosen", "zone": "board", "with": [{"attr": "state", "op": "not", "val": "stunned"}]}, "lasts": "this_round"},
  {"act": "damage", "on": {"kind": "unit", "side": "enemy", "pick": "it", "with": [{"attr": "state", "op": "is", "val": "stunned"}]}, "params": {"amount": 2}, "link": "instead"}]}]}

Vladimir - Keywords: Fearsome. Play: Deal 1 to any number of allies to deal that much to an enemy. Level up: You've had 5+
allies survive damage.
{"id": 750533, "abilities": [
 {"when": {"event": "played", "object": {"pick": "self"}}, "do": [
  {"act": "damage", "on": {"kind": "unit", "side": "mine", "pick": "chosen", "n": {"x": "count", "of": {"kind": "unit", "side": "mine", "pick": "chosen"}}, "zone": "board"}, "params": {"amount": 1}},
  {"act": "damage", "on": {"kind": "unit", "side": "enemy", "pick": "chosen", "zone": "board"}, "params": {"amount": {"x": "event_amount"}}, "link": "then"}]},
 {"when": {"event": "always"}, "if": [{"test": "event_count", "event": {"event": "survives_damage", "object": {"kind": "unit", "side": "mine"}}, "op": "ge", "n": 5, "span": "this_game"}],
  "do": [{"act": "level_up", "on": {"pick": "self"}}]}]}

The Smokescaled Host - Keywords: Landmark. I-II: To activate, discard 1. Invoke a Celestial card that costs 7 or more.
III: Reduce the cost of a random card in hand by 5.
{"id": 752112, "abilities": [
 {"when": {"event": "activated"}, "if": [{"test": "stage", "n": 1}], "do": [
  {"act": "discard", "on": {"kind": "card", "side": "mine", "pick": "chosen", "zone": "hand"}, "params": {"amount": 1}},
  {"act": "keyword_action", "keyword": "Invoke", "on": {"kind": "card", "with": [{"attr": "type", "op": "is", "ref": "Celestial"}, {"attr": "cost", "op": "ge", "n": 7}]}, "zone": "hand", "link": "if_done"}]},
 {"when": {"event": "activated"}, "if": [{"test": "stage", "n": 2}], "do": [
  {"act": "discard", "on": {"kind": "card", "side": "mine", "pick": "chosen", "zone": "hand"}, "params": {"amount": 1}},
  {"act": "keyword_action", "keyword": "Invoke", "on": {"kind": "card", "with": [{"attr": "type", "op": "is", "ref": "Celestial"}, {"attr": "cost", "op": "ge", "n": 7}]}, "zone": "hand", "link": "if_done"}]},
 {"when": {"event": "activated"}, "if": [{"test": "stage", "n": 3}], "do": [
  {"act": "cost_change", "on": {"kind": "card", "side": "mine", "pick": "random", "zone": "hand"}, "params": {"cost": -5}, "lasts": "permanent"}]}]}

## Game words: Runeterra
- Frostbite sets a unit's Power to 0 this round: a frostbitten unit can still block (attack_zero, never cant_block).
- Overwhelm adds no damage: damage past the blocker's health goes to the enemy Nexus (excess_damage; in a deck network it
  "helps it hit the enemy player").
- "spells and Skills" / "Fast spells, Slow spells, and Skills": category in spell, skill on every target the phrase names.
- "cost reduced cards": state cost_reduced on the counted cards.

## Game words: Stormbound
Stormbound has no Keywords field: describe everything the text says. Its glossary keywords (Poison, Vitalize, Freeze, Confuse,
Disable, Push, Pull, Command, Drain, ...) define the words; cards use the values below.
- Board. A tile is kind position. Where something is: filter `{"attr": "position", "op": "is", "val": <position>, "of": TARGET}`
  ("of" omitted = the card itself). "in front" (one tile) = in_front, "all units in front" = ahead, "the first enemy in front" =
  first_in_front, "the tile behind" = behind, "all tiles behind" = behind_all, "the closest enemy behind" = closest_behind,
  "on the side(s)" = sides, bordering, surrounding, "in its row" = same_row, "column" = same_column, "the most forward" =
  most_forward, "your furthest row" = furthest_row. "Bordering your base" = bordering of `{"kind": "player", "side": "mine"}`.
  "A random tile" = `{"kind": "position", "pick": "random"}`.
- Base = kind player (like Runeterra's Nexus). "Damage to the enemy base" = damage on the enemy player. "Give strength to your
  base" / "remove strength from a base" = stat_change params strength on the player.
- Strength = attr / param strength (attack and health in one; damage lowers it). Movement, "speed", "additional move" = attr /
  param movement. Strongest / weakest / lowest strength = pick highest / lowest, by strength. Stronger / weaker unit = filter
  strength gt / lt `{"x": "stat", "attr": "strength", "of": {"pick": "self"}}`.
- Structure = kind landmark (it stays on its tile). "Unit or structure" = kind unit_or_structure. A plain "enemy" / "enemies"
  (the rulebook: units, structures and the base) = kind anything; "enemy unit" = kind unit.
- Unit types (Dragon, Satyr, Toad, ...) and the extra types Ancient, Elder, Hero = filter type. "Temple structure" = name_has
  Temple. "Non-legendary" = rarity not legendary.
- Triggers. "On play" / "When played" = played, object self ("When played bordering X", "with a full hand", "as the last card"
  = played plus conds). "On death" / "When dying" = dies, object self (also leaving the board through the base). "Before
  attacking" / "When attacking" = attacks, actor self. "After attacking" = attack_done, actor self. "After surviving damage" =
  survives_damage. "Before moving" = moves, object self. "At the start / end of your turn" = turn_start / turn_end, actor
  `{"kind": "player", "side": "mine"}`.
- Statuses. poison, vitalize, freeze, confuse, disable = give_keyword with that keyword, lasts as the glossary says (permanent,
  or next_own_turn for Freeze and Confuse); "deconfuse" = remove_keyword Confuse; "poisoned / frozen / confused / vitalized /
  disabled unit" = state filter; "a random status effect" = give_random_keyword.
- Acts. spawn a unit = summon, card = the token of that type ("a 1 strength Toad" = card "Token Toads", "Nests" = "Qordia’s
  Nest", "an Elder" = "Token Elders"), params strength, "to" = the tile; build / spawn a structure = summon the same way;
  respawn = revive. destroy = kill. convert = steal. drain X from Y = damage Y (amount X), then stat_change strength on the
  drainer by `{"x": "event_amount"}` (link then). push / pull / command / jump / fly / teleport / move forward / move fixedly
  forward = move ("keyword" Push / Pull / Command / Move fixedly forward when the text names it; "to" = where). force to attack
  = start_attack, "to" = what it attacks. give / gain / lose strength = stat_change strength (lasts permanent); set / reduce
  strength to N = stat_set strength; restore initial strength = heal; raise to equal = grow. "deal X additional damage"
  before attacking = damage on the attacked unit. "spread randomly among" = the act on pick all with params spread 1.
  gain mana = mana_gain; spend remaining mana = spend_mana; mana cost -1 = cost_change. replace a card = shuffle_into_deck
  then draw (link then). add a created card to the deck = create, zone deck. trigger the ability of structures = repeat.
- "Single-use" card = state single_use. A card's level ("a random level 1/2/3/4/5 unit") = filter attr level. "The first
  empty tile in front / behind" = position first_empty_in_front / first_empty_behind.
- Numbers per level: `{"x": "per_level", "items": [...]}`; a range at one level ("4-5") is the item `{"x": "range", "items":
  [4, 5]}`. Words that change by level ("bordering/bordering/surrounding", "a/a/all/all/all"): one ability per group of levels,
  each with a level cond: levels 1-2 = `{"test": "level", "op": "le", "n": 2}`, levels 3-5 = `{"test": "level", "op": "ge",
  "n": 3}` (one level: op eq). An empty level value ("bordering/surrounding/surrounding//") is a gap in the card data: describe
  the levels that have words.

## Game words: Monster Train
Monster Train has no Keywords field: describe everything the text says. Its glossary keywords (Armor, Rage, Burnout, Consume,
Extract, ...) define the words; cards use the values below. Mapping decided by Claude from the game's wiki (28 Oct 2026).
- Board. The train has floors (lanes) with the Pyre Room on top; on each floor both sides stand in a line and the front units
  fight first. "On this floor" = position same_lane (of omitted = the card itself, or the floor a spell is cast on); "the
  front (enemy) unit" = position front_of_lane; "to the back" = back_of_lane; "the Pyre Room" = top_lane; "the bottom floor"
  = bottom_lane. Ascend / Descend = keyword_action with that keyword (it moves to lane_above / lane_below). "Move a unit to
  the front" = move, "to" `{"kind": "position", "with": [{"attr": "position", "op": "is", "val": "front_of_lane"}]}`.
- The Pyre = kind player (like Runeterra's Nexus): "Your Pyre takes 3 damage" = damage on `{"kind": "player", "side":
  "mine"}`; "restore Pyre health" = heal it; "+5 Attack to your Pyre" = stat_change power on it.
- Stats: Attack = attr / param power, Health = health ("max health" too). A unit's Capacity = attr / param size; "+1 Capacity
  on this floor" = capacity_change on `{"kind": "position", "with": [same_lane]}`. "15x2" Attack is the stats, not text.
- Ember = mana: "Gain 2 Ember" = mana_gain; "+1 Ember per turn" = max_mana_change; "costs -1 Ember" = cost_change; "apply 0
  Ember" to a card = cost_set 0. Gold = gold_gain. Echo = kind lane_resource: "Gain 1 Echo" = mana_gain on it; "per Echo" =
  `{"x": "count", "of": {"kind": "lane_resource"}}`; Echo slots are proposals.
- X cost: "Deal 2 per X damage" = amount `{"x": "x_paid", "inner": 2}`; "Draw X" = `{"x": "x_paid"}`.
- Triggers. "Summon:" and "When played" = played, object self. "Strike:" = strikes, actor self. "Revenge:" = damaged,
  object self. "Slay:" = killed, actor self. "Extinguish:" = dies, object self. "Hatch:" = dies, object self (the Egg).
  "Harvest:" = dies, object `{"kind": "unit", "with": [same_lane]}`. "Incant:" = played, object `{"kind": "spell", "side":
  "mine", "with": [same_lane]}`. "Rally:" = played, object a mine unit, not type Morsel, same_lane. "Rejuvenate:" = healed,
  object self. "Resolve:" = combat_end. "Action:" = combat_start, actor self. "End of Turn:" = turn_end, actor
  `{"kind": "player", "side": "mine"}`. "Gorge:" = eats, actor self, object a unit of type Morsel (the wiki: it eats a Morsel). "Eaten:" = eats, object self ("the eater" = pick actor).
  "Hunger:" = summoned, object a unit with keyword Eaten. "Etch:" = exhausted, object a card, same_lane. "Inspire:" =
  resource_gained, object `{"kind": "lane_resource", "with": [same_lane]}`. "Reserve:" = kept_in_hand, object self.
  "Armored:" = given_keyword Armor, object self. "Draw +1 next turn" = an ability turn_start (actor me) with limit next_time;
  "each turn" = turn_start.
- A keyword the card has itself, written alone ("Consume.", "Rage 4.", "Extract 2.", "Burnout 1. Multistrike 1.") = one
  ability `{"when": {"event": "always"}, "do": [{"act": "give_keyword", "keyword": "<K>", "on": {"pick": "self"}, "params":
  {"amount": N}, "lasts": "permanent"}]}` (amount only when a number is written). "Apply Rage 3" = give_keyword Rage, amount 3,
  lasts permanent (the keyword's own record says how its stacks fall). "Sacrifice Imp." = keyword_action Sacrifice with "on" a mine
  unit of type Imp ("Sacrifice." alone: "on" a mine unit). "Reform a unit" = keyword_action Reform. "Cultivate 2" = keyword_action Cultivate, amount 2.
- Zones: draw pile = deck ("top of your draw pile" = deck_top); discard pile = discard; consumed cards ("the Consume pile", "a
  consumed spell") = zone exhausted; a defeated or dead unit = kind unit, zone discard (rule 17). "Return ... to your hand"
  from those zones = return_card, zone hand. "Add N cards to your hand / discard pile" = create in that zone.
- "Permanently", "a permanent copy" = lasts this_run (the change stays in the deck for later battles); other changes last the
  battle = permanent.
- "15x the number of Imp units", "4x the amount of Armor" = `{"x": "product", "items": [15, <the count>]}`. "Double the
  amount of Rage on friendly units" / "Double Armor on a unit" = give_keyword that keyword with amount = the count of its
  stacks on the unit (it doubles). "Non-boss" = state not boss. Echo slots = kind lane_resource_slot.
- Types (Imp, Demon, Morsel, Hollow, Egg, Blight, Scourge, ...) = filter type. "Morsel units" = type Morsel.
- Champions: text before the first path holds always. "<Path> path (upgrades I/II/III): ..." = that path's abilities, each with
  the cond `{"test": "upgrade_path", "n": <1, 2 or 3: the path's place in the text>}`; numbers "10/15/20" = per_level items.
  "<Path> path: Upgrade I: ... Upgrade II: ... Upgrade III: ..." = one ability set per upgrade with the path cond plus
  `{"test": "level", "op": "eq", "n": <1, 2, 3>}`. "Next version:" in a card = its next version: write each version's
  abilities with the cond level eq 1, 2, 3.

## Game words: Faeria
Faeria has no Keywords field: describe everything the text says. Its glossary keywords (Gift, Last Words, Production, Combat,
Corrupt, Activate, Flying, Charge, Jump, Dash, Aquatic, Taunt, Haste, Protection, Discover, Ranged Attack, Divine, Deathtouch,
Swallow, Wild, Fight, Teleport, Transform) define the words; cards use the values below. Mapping decided by Claude from the
game's own glossary (Abrakam's card export README, faeria.com Keyword Rulings guide; 29 Oct 2026).
- Players. Each player has a god (an orb) with Life = kind player. "Your opponent", "the enemy god", "a god" = kind player
  (side enemy / any). "Deal 2 damage to yourself" = damage on `{"kind": "player", "side": "mine"}`. "Gain 3 Life" = heal on
  the player. A plain "enemy" / "enemies" (the rulings: all enemies, gods included) = kind anything; "enemy creature" = kind
  unit; "creatures and structures" = unit_or_structure.
- Cards. Creature = unit, structure = landmark (category landmark), event = spell (category spell). Attack = power, Life =
  health ("+2/+1" = power 2, health 1). Legend / legendary = rarity legendary. Types (Yak, Triton, Beast, Mecha, Rakoan) =
  filter type. A colour of card ("a random blue card", "a green creature") = filter `{"attr": "region", "op": "is", "val":
  "Blue"}` (Green, Red, Yellow; the card's faction); "neutral" = region "Neutral (Human)".
- Faeria = mana. "Gain 2 faeria" = mana_gain amount 2 on the player. "Costs 1 faeria less" = cost_change cost -1; "It costs 0
  faeria", "a free X" = cost_set cost 0. "It becomes wild land" / "They are wild land" = give_keyword Wild, lasts permanent.
- The board is hexes ("spaces"). A space is kind position; its ground is filter `{"attr": "terrain", "op": "is", "val": ...}`:
  ocean, land (any land), prairie, lake, forest, mountain, desert, special_land, resource_well (a faeria well). Lands have
  an owner: "a land you control", "your lands", "friendly forest" = side mine; "enemy land", "an opponent's well" = side enemy.
  "Unoccupied" = state empty. "Adjacent" = position bordering ("adjacent enemies" = kind anything, side enemy, position
  bordering of the card; "adjacent to the target" = of `{"pick": "it"}`). "On or adjacent to that space" = one target, position in
  [same_space, bordering] of the space (The board). "This creature's land", "the land it is on" = kind position with position same_space of the card; "if this is on an
  enemy land" = COND `{"test": "count", "of": {"kind": "position", "side": "enemy", "with": [terrain land, position
  same_space]}, "op": "ge", "n": 1}`. "Choose a space" = kind position, pick chosen; "a random space" = pick random.
- Land acts. "Create forest", "Create 3 forests at random" = set_terrain on `{"kind": "position", "with": [terrain ocean]}`
  (n, pick as written), "to" `{"kind": "position", "with": [terrain forest]}`. "Transform a land into lake" = set_terrain on
  the land, "to" terrain lake. "Destroy a land" = set_terrain to terrain ocean. "Move a land" = move on the land (kind position).
  "Gain control of a land" = steal on it. "Fill the world with forests" = set_terrain on all ocean spaces, to forest.
  "Empty / refill / destroy a faeria well" have no value: propose. "Whenever you create forest" = event terrain_changed,
  actor the player, object a position with terrain forest.
- Lands as conditions. "While you control 2 lakes" = COND `{"test": "count", "of": {"kind": "position", "side": "mine",
  "with": [terrain lake]}, "op": "ge", "n": 2}`; "for each forest you control" = `{"x": "count", "of": <that target>}`.
- Triggers. "Gift -" = played, object self. "Last Words -" = dies, object self. "Production -" = turn_start, actor
  `{"kind": "player", "side": "mine"}`. "Combat -" = fights, actor self. "Corrupt -" = moves_onto, object self `with` [position same_space
  of `{"kind": "position", "side": "enemy", "with": [terrain land]}`], limit once_per_game (the mover is the object, as for
  moves; the space is where it now stands). "Activate -" = activated. "At the end
  of your turn" = turn_end, actor me. "On your opponent's next turn" = turn_start, actor the enemy player, limit next_time.
  "Whenever this attacks a god" = strikes_nexus, actor self (rule 31). "Whenever this attacks" = attacks, actor self.
  "Whenever this harvests faeria (from an opponent's well)" = harvests, actor self, object a position with terrain
  resource_well (side enemy). "Whenever you harvest faeria" = harvests, actor `{"kind": "unit", "side": "mine"}`. "Whenever
  this moves into a forest" = moves_onto, object self with position same_space of a position with terrain forest. "Whenever you select +1 faeria from the
  power wheel" = turn_option_chosen, actor me, object `{"kind": "mana"}`. "Whenever you play an event" = played, object kind
  spell side mine.
- Durations. "This turn" = lasts this_round (one turn is the span); "Has +1/+1 while ..." = stat_change lasts while.
- Acts. "X fights Y" = start_attack on X, "to" Y, keyword Fight. "Teleport X to Y" = move, keyword Teleport, "to" Y. "Swallow
  a creature" = capture on it, keyword Swallow. "Drain 2 life from X" = damage X amount 2, then heal the player amount
  event_amount (link then). "Transform X into Y" = transform, card Y. "Discover a Beast" = keyword_action Discover, on
  `{"kind": "card", "with": [type Beast]}`, zone hand (what the Discover offers as filters on "on"). "Sacrifice a creature" = sacrifice
  on a mine unit, pick chosen. "Can't harvest faeria" = cant, params event harvests, on self. "Can only attack gods" = cant
  params event attacks, on self, "to" kind unit_or_structure. "Launch / Summon a 4/2 Mecha" = summon card "Mecha" (the named
  token), with stats in params power, health only when the text gives them.
- A keyword the card has itself, written alone ("Flying, Charge 3", "Taunt", "Dash 2") = one ability `{"when": {"event":
  "always"}, "do": [{"act": "give_keyword", "keyword": "<K>", "on": {"pick": "self"}, "params": {"amount": N}, "lasts":
  "permanent"}]}` (amount only for a number: Charge 3, Dash 2). "Give a creature Charge 3 this turn" = give_keyword Charge,
  amount 3, lasts this_round.
- "Choose one: A / B." then "- A" lines: the "- A" lines repeat the options; describe each option once (rule 8).

## Game words: Inscryption
Cards list their sigils in the Keywords field ("Keywords: Airborne, Fledgling."); do not describe them, the sigil (keyword)
entries do. Read the rest of a card's text ("Traits: Goat.", "Sigils: Repulsive. 5th Starvation onward: Airborne.") and the
keyword entries (category keyword: a sigil, a trait or a variable Power stat). Mapping decided by Claude from the game's wiki
(sigil pages and the rulebook lines; 29 Oct 2026).
- Board. Each side has a row of spaces (4 in most of the game, 5 in Act III); a lane is a space and the space across from it.
  "The opposing space", "the creature opposing it", "across from it" = position same_lane, side enemy (of omitted = the card
  itself). "Adjacent" / "to the left and right" = position sides (on its own side unless the text says opposing: "each opposing
  space to the left and right of the space across" = side enemy, position sides of the opposing space). "An empty space" =
  `{"kind": "position", "with": [{"attr": "state", "op": "is", "val": "empty"}]}`; "in its place" = position same_space of it.
  Follow "The board" above for every other board word: "moves into the space opposing" = moves_onto (the mover as object,
  same_space of the opposing space); "moves towards" a unit = to the sides of it. A strike aimed at opposing spaces
  ("strike each opposing space to the left and right", "choose which opposing space") also strikes the enemy player, link
  or: an empty struck space hits the opponent (wiki Card Battle). "Within a circuit" = position in_circuit of the conduit
  card, and a COND of two Conduit Cards of mine (a circuit is two conduit cards, wiki Circuits).
- The opponent (the scale) = kind player, side enemy. "Strike an opponent directly", "deals damage directly" = strikes_nexus,
  actor self. Damage to the scale = damage on the player.
- Perish / die = dies. "When a card bearing this sigil is struck" = damaged, object self (state combat). "Is played" = played,
  object self. "Is drawn" = drawn, object self. "At the end / beginning of the owner's turn" = turn_end / turn_start, actor
  `{"kind": "player", "side": "mine"}`. "Activate: Pay 2 Bones to ..." = activated; the payment is a first effect: spend on
  `{"kind": "secondary_resource", "side": "mine"}` = act spend_mana with params amount (Energy payment: spend_mana on kind mana).
- Costs. Blood is paid by sacrificing your creatures: "is sacrificed", "when sacrificed" = event sacrificed, object self; "the
  card it was sacrificed for" = pick actor; "sacrifice a card bearing this sigil" = act sacrifice on self (every game: giving
  up my own unit is act sacrifice). "Counts as 3 Blood" = proposal (no value yet). Bones = kind secondary_resource:
  "gain 3 Bones", "1 bone is generated", "4 Bones are awarded" = mana_gain on `{"kind": "secondary_resource", "side": "mine"}`.
  Energy = mana: "an Energy Cell" = max_mana_change amount 1; "your Energy never depletes" = proposal. A Gem (Mox): "a Green Gem
  is provided" = proposal (no value yet); "controls no Mox cards" = COND count of `{"kind": "unit", "side": "mine", "with":
  [{"attr": "type", "op": "is", "ref": "Mox Card"}]}` op eq n 0.
- Created cards. "An Ant is created in your hand" = create, zone hand, card "Worker Ant"; "a Bee", "a Rabbit", "a Skeleton",
  "a Squirrel", "a Chime", "a Dam", "an Egg" (Brood Parasite: "Broken Egg"), "a Tail", "L33pB0ts", "Explode Bots", "a Ruby Mox",
  "Gem Vessels" (the Emerald, Ruby and Sapphire Vessel cards) = those cards; "created on each empty adjacent space" = summon,
  "to" the spaces. "Grow into a more powerful form" (Fledgling) = transform on self at turn_start (the next form is a link of
  the card, not written). "Transform to, or from, Beast mode" = transform on self (the other form is a link).
- "Moves in the direction inscribed" / "moves to that space" = move on self, "to" the space. "Strike" as an act = strike, on
  self, to the struck target. A circuit (Conduits): "within a circuit completed by a card bearing this sigil" = position
  proposal (no value yet: propose "in_circuit").
- Traits that are the game's internal flags with no effect in a battle (Goat, Lice, Fused, KillsSurvivors, DeathCardNonOption,
  DeathcardCreationNonOption, JeresyDevil, Cat, Child 13, Limited Lives, Chime Keeper, Giant without words): no record. A trait
  with words ("Giant (Increases its Power by 1 every turn ...)", the Obol halves' "gives the player one Ancient Obol") is read.
- Items (category item), events, modifiers (Boons) are read like cards: a Boon's "at the start of every battle" = game_start.

## Game words: Duelyst
Cards list their plain keywords in the Keywords field ("Keywords: Provoke, Celerity."): do not describe them. Describe the
rest of the text, labels and numbered keywords included ("Backstab: (2).", "Build: (1)."). Its keyword entries (Provoke, Rush, Ranged, Flying, Frenzy,
Celerity, Blast, Backstab, Zeal, Infiltrate, Grow, Rebirth, Forcefield, Airdrop, Opening Gambit, Dying Wish, Deathwatch, Blood
Surge, Bond, Intensify, Sentinel, Build, Trial, Destiny, the tiles ...) define the words; cards use the values below. Mapping
decided by Claude from the game's own texts (open-duelyst: keyword definitions, tutorial, tips; 29 Oct 2026).
- Players. Each player's General is a unit on the board whose Health is the player's life: the General = kind player. "Your
  General" = `{"kind": "player", "side": "mine"}`, "the enemy General" = side enemy, "a General", "Generals" = kind player.
  A minion = kind unit. An "enemy", "a friendly unit", "anything" (a minion or a General) = kind any; "everything" = kind
  any, pick all (no side). "Your General gains +1 Attack" = stat_change power on the player. "Teleport your General" = move
  on the player. Events of the General: "whenever your General attacks" = attacks, actor `{"kind": "player", "side": "mine"}`;
  "whenever your General takes damage" = damaged, object that player; "whenever your General destroys an enemy" = killed,
  actor that player.
- Cards. Minion = unit, spell = spell, artifact = item. Attack = power, Health = health ("+2/+1" = power 2, health 1).
  The action bar = the hand ("put X into your action bar" = create, zone hand). Tribes (Golem, Mech, Arcanyst, Vespyr,
  Dervish, Structure, Battle Pet) = filter type. "Your Bloodbound Spell" = a spell with keyword Bloodbound Spell, side mine.
- Mana. "Gain 1 mana" = mana_gain; "gain a mana crystal" (more mana every turn) = max_mana_change; "costs 1 less" =
  cost_change cost -1; "costs 0" = cost_set.
- The board is a grid of spaces. A space = kind position. "Nearby X" / "around X" = position surrounding of X ("nearby" alone =
  of this card); "in front of" = in_front, "behind" = behind (of the unit named); "in its row" / "column" = same_row /
  same_column; "anywhere" = kind position with no filter; "a random space" = pick random; "in each corner" = position corner;
  "a 2x2 area" = area_2x2; "a 3x3 area" = area_3x3; "your starting side of the battlefield" = starting_side of the player;
  "diagonal from" = diagonal; "the center column" = center_column. "Empty", "unoccupied" = state empty.
- Tiles. "Turn a space into Shadow Creep" = set_terrain on that position, keyword Shadow Creep, "to" `{"kind": "position",
  "with": [{"attr": "terrain", "op": "is", "val": "damage_space"}]}`; Hallowed Ground = heal_space, Exhuming Sand =
  summon_space, Primal Flourish = growth_space, a mana spring = bonus_mana_space (keyword Mana Spring). "Friendly Shadow
  Creep", "your Shadow Creep" = kind position, side mine, with that terrain; "for each friendly Shadow Creep" = count of it.
- Triggers. "Opening Gambit:" = played, object self. "Dying Wish:" = dies, object self. "Deathwatch:" = dies, object
  `{"kind": "unit"}` (any minion). "Blood Surge:" and a General's "Bloodbound Spell: X" = played, object `{"kind": "spell",
  "side": "mine", "with": [{"attr": "keyword", "op": "is", "ref": "Bloodbound Spell"}]}`. "Grow: +1/+1" = turn_start, actor
  `{"kind": "player", "side": "mine"}`, stat_change power 1, health 1 on self, lasts permanent. "Bond:", "Zeal:" and
  "Infiltrate:" are conditions: COND `{"test": "keyword_condition", "ref": "Bond"}` (Zeal, Infiltrate) on the ability the
  text gives (Bond with event played, object self; "Zeal: Gains +1 Attack" = always, stat_change lasts while). "Sentinel: X"
  = the event X, then transform on self (the true form is a link of the card). "Intensify: X" = played, object self; each
  amount that grows = `{"x": "product", "items": [<N>, {"x": "event_count", "event": {"event": "played", "object": {"kind":
  "card", "side": "mine", "with": [{"attr": "card", "op": "is", "ref": "<this card>"}]}}, "span": "this_game"}]}`.
  "Trial: X" = `{"when": {"event": "always"}, "if": [X as conds, span this_game], "do": [{"act": "can", "on": {"pick":
  "self"}, "params": {"event": "played"}, "lasts": "permanent"}]}`. "Destiny: X" = X as its own ability (its event as
  written), lasts permanent. "When this minion is built" (Build) = transformed, object self. "At the start / end of your
  turn" = turn_start / turn_end, actor `{"kind": "player", "side": "mine"}`. "Whenever you replace a card" = shuffled,
  actor that player, object a card of yours from zone hand.
- Acts. "Stun X" = give_keyword Stunned, lasts next_own_turn. "Dispel X" = silence (a dispelled space: silence on the
  position). "Teleport X to Y" = move, "to" Y; "switch positions" = swap; "push" / "pull" an enemy = move on it. "Return to
  its action bar" = return_to_hand. "Equip an artifact" = attach (on the player, card the artifact). "Progresses MECHAZ0R
  build by +20%" = keyword_action MECHAZ0R, params amount 20. "Destroy" = kill. "Transform into X" = transform, card X.
  "Shuffle into your deck" = shuffle_into_deck; "replace" a card = shuffle_into_deck, then draw (link then).
- "Reactivate" = ready; "becomes your General" = become_leader; "non-token" = filter state not token; "the nearest / closest
  enemy" = pick nearest. A faction named ("a random Songhai spell", "Vetruvian artifacts", "a neutral minion") = filter
  `{"attr": "region", "op": "is", "val": "Songhai Empire"}` (Lyonar Kingdoms, Vetruvian Imperium, Abyssian Host, Magmar
  Aspects, Vanar Kindred, Neutral). A trigger that only holds "this turn" ("Whenever a friendly minion dies this turn") = the
  card gives its player that ability: give_ability on `{"kind": "player", "side": "mine"}`, lasts this_round.
- A keyword the card has itself in its text ("Backstab: (2).", "Build: (1).", "Forcefield, Frenzy, Grow: +7/+7.") = one
  ability `{"when": {"event": "always"}, "do": [{"act": "give_keyword", "keyword": "<K>", "on": {"pick": "self"}, "params":
  {"amount": N}, "lasts": "permanent"}]}` (amount only for a number: Backstab 2, Build 1). "Give a minion Celerity this turn"
  = give_keyword, lasts this_round ("this turn" = this_round).

## Game words: Slay the Spire
Cards list Exhaust, Ethereal, Innate, Retain and Unplayable in the Keywords field ("Keywords: Exhaust. Deal 11 damage."): do not
describe them. Card kinds are types (Attack, Skill, Power, Status, Curse): "an Attack" = filter type Attack, never category
skill. Keyword entries (category keyword: glossary words such as Block, Strength, Vulnerable, Channel, Scry, Wrath, and the
powers Plated Armor, Mark, Hex, Stasis, Surrounded) define the words; cards use the values below. Mapping decided by Claude
from the game's wiki and Wikipedia (tools/games/sts1.md "The game's rules"; 30 Oct 2026).
- No board, no units of mine. The player = kind player, side mine ("you", "your"); enemies = kind unit, side enemy ("an
  enemy" = pick chosen, "a random enemy" = random, "ALL enemies" = all). An enemy's own text (monster, boss) is written from
  its side: the player it attacks is side enemy.
- Damage: "Deal 8 damage" = damage on the enemy; "Deal 7 damage 3 times" = damage, params amount 7 and times 3. "Lose 3 HP",
  "take 2 damage" = damage on the player (side mine). HP = health: "raise your Max HP by 3" = stat_change health on the
  player; "heal 4 HP" = heal.
- Statuses with numbers are keywords with amount, lasts permanent (the keyword's record says how they wear off): "Gain 5
  Block" = give_keyword Block, params amount 5, on the player; "Apply 2 Vulnerable" = give_keyword Vulnerable on the enemy;
  "gain 2 Strength", "4 Plated Armor", "3 Mantra", "8 Mark", "1 Artifact", "Intangible", "Weak", "Frail", "Poison", "Thorns",
  "Focus", "Dexterity" alike. "Lose 2 Strength", "Enemy loses 9 Strength" = give_keyword Strength with a negative amount;
  "this turn" = lasts this_round. "Double the enemy's Poison" = give_keyword Poison, amount the count of its Poison.
- Energy = mana: "Gain 2 energy" = mana_gain amount 2; "costs 1 less (energy)" = cost_change; "costs 0 this turn" = cost_set
  0, lasts this_round; X cost = `{"x": "x_paid"}`. "Next turn, gain 1 energy" / "next turn, draw 2" = an ability turn_start,
  actor the player, limit next_time.
- Piles: draw pile = deck ("top of your draw pile" = deck_top), discard pile = discard, exhaust pile = exhausted, hand = hand.
  "Draw 2 cards" = draw; "Discard 1 card" = discard; "Exhaust a card" = exhaust on a card in hand; "put a card from your
  discard pile into your hand" = return_card zone hand. New cards: "Add 2 Shivs into your hand" = create, zone hand, card Shiv
  (params amount 2); "Shuffle a Wound into your draw pile" / "add a Void into your discard pile" = create in zone deck /
  discard; "a random Skill" = create with "on" `{"kind": "spell", "pick": "random", "with": [type Skill]}` (rule 7).
  "Upgrade a card" = keyword_action Upgrade on the card. "Transform" = keyword_action Transform. "Scry 3" = keyword_action
  Scry, amount 3. "Play twice" / "played twice" = repeat on the card (params times 2).
- Cards played: "Whenever you play a card / an Attack" = played, object `{"kind": "spell", "side": "mine"}` (with type
  Attack). "When this card is drawn / discarded / Exhausted / Retained" = drawn / discarded / exhausted / kept_in_hand, object
  self. "Whenever a card is Exhausted" = exhausted, object a card of mine. "If Fatal" = COND keyword_condition, ref Fatal.
- Turns: "At the start / end of your turn" = turn_start / turn_end, actor the player (mine). "Each turn" = turn_start.
  "Start of combat", "at the start of each combat" = combat_start; "this combat" = lasts permanent; "permanently" (the card
  changes for the run) and Max HP gains = lasts this_run. "Whenever you lose HP" = damaged, object the player.
- Orbs (Lightning, Frost, Dark, Plasma are keywords): "Channel 1 Lightning" = keyword_action Channel, params amount 1, "on"
  `{"kind": "keyword", "with": [{"attr": "keyword", "op": "is", "ref": "Lightning"}]}`; "Evoke your next Orb" =
  keyword_action Evoke on `{"kind": "keyword", "pick": "top"}`; Orb slots are proposals.
- Stances (Wrath, Calm, Divinity are keywords; Stance is their family): "Enter Wrath" = give_keyword Wrath on the player,
  lasts permanent; "exit your Stance" = remove_keyword Stance on the player; "whenever you enter Wrath" = given_keyword,
  object the player, keyword filter Wrath; "whenever you change Stances" = given_keyword with keyword filter Stance.
- Relics (category relic) hold for the run: their text is an ability like a card's ("Whenever you play 10 Attacks, gain 1
  energy" = played, Attack, with the count as COND). "Upon pickup" = played, object self. Potions (category item) = played,
  object self, like a card. Events: "Choices: A | B | C" = choose_one, then each choice linked or. Monsters and bosses:
  "Actions: Slash (attack, 20 damage); ..." = one ability turn_start, actor self, doing random_one of the actions linked or
  (the intent is the enemy's choice). Ascension levels (category modifier) are read like relics.

## Game words: Into the Breach
A squad of 3 mechs fights the Vek on an 8x8 grid of tiles. Mechs (category unit, the player's) carry their starting weapons
and passive in their text ("Weapon: Titan Fist: ...", "Passive: Flame Shielding: ..."); weapons (category ability), passives
(item) and pilots (hero) are also cards of their own. A weapon's or passive's "you", "the Mech", "the user", "self" = the unit
that carries it (pick self); a pilot's "Mech" = the mech it pilots (pick self). Mapping decided by Claude from the game's wiki
(Weapons, Mechs, Passives, Pilots, Status Effects, Abilities and status effects, Tiles pages; 30 Oct 2026).
- Sides. Mechs, allied units and deployed tanks are side mine; Vek (category monster, boss) are side enemy. "Enemies", "Vek"
  = kind unit, side enemy; "allies", "friendly units", "player units" = kind unit, side mine; "units", "a unit", "target"
  (anything on a tile) = kind unit, no side. "Mechs" = units side mine with filter type Mech ("All Mechs"). "Grid Buildings",
  "buildings" = kind landmark, side mine. The Power Grid / Grid Power is the player's life: kind player, side mine; "charge
  the Power Grid 1 point" = heal on that player, amount 1.
- Tiles. A tile = kind position. "Adjacent" = bordering (4 tiles); "nearby" = bordering unless a size is given; "in a line",
  "a beam", "every tile it passes" = straight_line of self; "behind you" / "the tile behind" = behind of self; "in front" =
  in_front of self; "to the left and right of X" = sides of X; "a row or column" = same_row / same_column; "anywhere on the
  map" = kind position, no filter; "within N tiles", "N-tile range" = distance le N. A projectile or beam hits the first unit
  in its straight line; artillery arcs to any tile in a straight line (this is how the weapon aims: write the target, never
  the path).
- Damage. "Damage: 2" = damage params amount 2 on what the weapon hits. "(1 to self)", "damaging self" = a second effect,
  damage on self. "3-1", "1-3", "0 - 2" (damage that changes with distance or hits) = damage with amount `{"x": "range", "items":
  [lowest, highest]}`. "Damage: kills" = kill. "Building Immune" / "Ally Immune" = the target filter excludes landmarks / side mine.
- Moves. "Push" a tile or unit = move on the unit there, "to" the bordering position away from the attacker; "pull" = move
  towards; "toss", "throw", "grab and toss behind you" = move "to" behind of self; "swap places" = swap; "teleport", "leap",
  "dash", "charge", "fly over" by the mech itself = move on self. "Flip its attack direction" = act
  redirect_attack on the unit. "Temporarily control a unit" = steal, lasts this_round. "Force a unit
  to attack" = start_attack on it.
- Statuses (keywords): Fire, Smoke, A.C.I.D., Frozen, Webbed, Shield (keyword Energy Shield), Boost. On a unit = give_keyword
  with that keyword, lasts permanent unless the text says how long (Boost wears off by its own keyword record: lasts permanent). On tiles ("light tiles on Fire", "Smoke on 5 tiles", "Smoke behind the shooter", "A.C.I.D. pool")
  = give_keyword on the positions. "Freeze" = give_keyword Frozen. "Repair" = heal (also of disabled Mechs); "repairs all
  damage", "heal completely" = heal with amount `{"x": "stat", "attr": "health", "of": TARGET}`.
- Damage by origin. "Weapon damage to this unit", "Bumps", "blocking emerging Vek" = event damaged with COND it_matches
  origin weapon / bump / blocking_emerging. "+N Range" with no reach written = increase_effect params range N.
- Ground. "Crack tiles" = set_terrain "to" a position with terrain cracked_space; "convert a liquid Tile to a Hole" = set_terrain
  to chasm. Water = terrain ocean; Chasm = chasm; Lava = lava.
- Events. "On kill", "when they deal a killing blow", "if target is killed" = killed, actor self (the mech) and object the
  target. "When repairing" = healed, actor self. "After attacking" = attack_done, actor self; "after Move" = moves_onto, object
  self. "Every turn" (Vek or environment) = turn_start of the player whose turn it says ("the player turn" = actor kind player
  side mine; "the enemy turn" = side enemy); "start every mission" = game_start (a mission is a game). "On Reset Turn" =
  activated, object kind player side mine (proposal "reset_turn" if it does not fit).
- Limits. "Single-use" = limit once_per_game on the weapon's ability (a battle is a game); "2 uses per battle" = limit n_times
  with params times 2; "+1 Use" upgrades raise times.
- Upgrades. A weapon's upgrades ("Upgrades: Dash (2 Reactor Cores): Charge any distance before punching the target; +2 Damage
  (3 Reactor Cores): Increases damage by 2.") are optional: the base weapon is one ability with no COND; each upgrade is its
  own ability with the base weapon's event and COND `{"test": "upgraded", "n": <its place, 1 or 2>}`, holding only what the
  upgrade adds ("+2 Damage" = damage amount 2 more on the same target, "Gain Shield" = give_keyword Energy Shield on self).
- From the check of 20 cards (30 Oct 2026): "Increases area hit by 1 tile" = increase_effect on self, params area 1. "Shield
  adjacent ally or Building" = every adjacent one (pick all; no choice word, nothing is chosen). Flying over mountains or
  units is no place to stand: write only the tiles it may stop on. "3 tiles in a row" means what the card's own prose says
  (Burrowers: the tile in front and its two sides; Hornet Leader: three tiles ahead).
  Worked example, Repulse "Push all adjacent tiles ... Shield Friendly: Shield adjacent ally or Building":
  `{"when": {"event": "attacks", "actor": {"pick": "self"}}, "if": [{"test": "upgraded", "n": 2}], "do": [{"act":
  "give_keyword", "on": {"kind": "unit_or_structure", "side": "mine", "pick": "all", "with": [{"attr": "position", "op":
  "is", "val": "bordering", "of": {"pick": "self"}}]}, "keyword": "Energy Shield", "lasts": "permanent"}]}`.
- Decks (v52, Kaptain 30 Oct 2026: mechs are equipped with weapons): a squad or build lists each mech, then its weapons and
  passive as cards of their own. A mech's record holds only its own keywords (Flying, Massive, Natural Armor); its weapon's
  and passive's rows are on the weapon and passive cards, read from their own texts.
- A mech has 2 slots: it carries 2 weapons at most (a passive such as Storm Generator takes a slot too). Its starting
  weapon fills one; the other is its starting passive or one extra weapon, never two extra (Kaptain, 30 Oct 2026). A
  starting weapon may be swapped for another. In a deck, each mech comes first and what it carries
  right after it ("Jet Mech, Aerial Bombs, Force Amp, Rocket Mech, ..."); the network draws "Jet Mech carries Aerial Bombs".
  A build whose source does not say which mech carries an item, and no free slot decides it, is not used.
  "Power: ..." (Reactor Cores needed to power the weapon) is no effect: skip it.
- Passives act on all Mechs: "All Mechs are immune to Fire" = always, give_keyword Fire Immunity on units side mine with type
  Mech, lasts while. Pilots: "Mech gains Armored" = give_keyword Natural Armor on self; "+3 Move" = stat_change params movement.
- Vek text ("Health 3, move 3. Weapons/skills: Pincers: Charge forward to deal 1 damage and push the target.") is read the same
  way: the Vek is self, its targets are units or landmarks of either side unless it says.
