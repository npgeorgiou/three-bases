# Reader brief: describe each card as a record (version 4)

You read card texts and write what each card DOES as JSON records. Every value is a number, a value from
`vocab.tsv` (column `value`, grouped by `field`), or the exact name of another card, keyword or type (the script turns names into
links). Never write free text. Never guess a rule the text does not state.

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
         ("by" only with pick highest / lowest: "the ally with the highest Countdown" = pick highest, by countdown)  n defaults to 1;
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
   = X (target filtered "not Y"), then Z with link instead (target pick it, filtered "Y"). "X, or if <you / the game state> Y,
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
  "do": [{"act": "mark", "on": {"kind": "unit", "side": "enemy", "pick": "weakest", "zone": "board"}, "lasts": "permanent"}]},
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
  "do": [{"act": "stun", "on": {"kind": "unit", "side": "enemy", "pick": "strongest", "zone": "board", "with": [{"attr": "state", "op": "not", "val": "in_combat"}]}, "lasts": "this_round"}]},
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
