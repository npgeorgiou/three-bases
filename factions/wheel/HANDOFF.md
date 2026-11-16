# The wheel: where we are
Read this, then `factions/START_DESIGN-1-wheel.md` (the steps, their rules and the stops), then only the step you are
on. Clone with the library (`git sparse-checkout disable`); `gunzip -kf links.sqlite.gz` in `library/cards_db`.
One chat does one step; at its end, mark the step done here.

## The steps
| step | state | what it made |
|---|---|---|
| 1. Fix the library's concepts | done 16 Nov 2026 | concepts split by whom a row acts on (player, my unit, cards between piles), radii without game limits; `work/suspect_verdicts.tsv` |
| 2. The radii and how they work together | done 16 Nov 2026 | `axes.tsv`, `wheel/radius_links.tsv` |
| 3. The 20 shapes | done 17 Nov 2026, Kaptain agreed them | `work/shapes.tsv` |
| 4. The usable concepts | REDO, see "Agreed 17 Nov 2026" below | `work/concepts.tsv` |
| 5. The links between concepts | to do, after the redo; `mechanics_wheel.py` gets a concept mode | |
| 6. The 20 groups | to do; `work/groups.py` to write, `tools/wheel_table_check.py` to rewrite | |
| 7. Theme, then tools | to do | |
| 8. Combos on this board | to do | |
| 9. The seven answers, Stop 1 | to do; `work/make_stop1.py` to rewrite | |

Inputs ready: for step 5 `work/concepts.tsv`. Kinds of play whose concepts are no library concept with 10+ cards
(step 6 must handle them): the starred radius groups countboard*, kill*, weaken*, spelldmg*, position*, and polymorph,
piercing, cross_lane (under 10 cards). Step 3's check: 26 kind-of-play concepts have under a quarter of their cards on
that kind's radii (`shapes.py` prints them); Kaptain decides on them before step 6.

## Agreed 17 Nov 2026: do this next, in this order (one chat; read START_DATABASE.md whole first: it changes the library)
1. Library: the concept "Skill" (spell_or_skill) goes. It only says a card record's kind is "ability" (`flat.py`, the
   line giving it to every category='ability' card; Into the Breach weapons, Runeterra skills); its cards keep what
   their rows say. Remove it from `library/concept_tree.txt` too; cases. Rebuild links (`links.py`, about 7 minutes).
2. Redo step 2 (`axes.py`, `mechanics_wheel.py links --radii`) and step 3 (`shapes.py --write`). If a shape moved,
   show Kaptain the old and the new line to agree again.
3. No raw pair counts anywhere (a big game would drown the others): `links` and `level` in steps 2 and 5, the
   "count of pairs only breaks ties" rule and the link texts get "in how many games" (of 10) beside "times chance"
   (per game, averaged); ties broken by games. Link text: "... (in 7 of 10 games, 3.1 times chance)". Docs too.
4. Redo step 4 with the new rule (rewrite step 4 in START_DESIGN-1-wheel.md to it): a concept is USABLE when a
   faction can build on it: it says what a card does, or reacts to something the player makes happen or builds up. A
   concept that only says when or how a card acts is a HELPER, as are the game's own things and things for single
   cards: never in a group; after step 6 each faction gets them in its list (6). OUT for good: not in this game,
   Kaptain's rulings. A concept that only says what kind of record a card is, is a library error (removed, as Skill).
   - Usable now: on_draw, on_targeted, on_enemy_enter (Kaptain: keep), on_lifegain, hand_size, variety_payoff,
     condition_life, count_payoff, deck_position, card_presence_condition, cost_condition, condition_count.
   - Out: max_mana_condition (supply does not grow by itself). Find the library's concept for supply gained
     (Runeterra: leftover mana saved as spell mana); if there is none, tell Kaptain.
   - Helpers: on_play, turn_end, start_of_game, combat_start, once_per_game, passive, activated, cooldowns, delayed,
     play_timing_condition, modal_choice, symmetric_effect, aura; the game's own things (lanes, zone_control,
     resource_banking, round_carryover, positional, board_limit, high_cost, on_harvest); single cards (exhaust,
     drawback, cant_attack, slots_queue, target_choice).
   - `concept_catch.py` writes the three kinds (`concept_verdicts.tsv` gets a kind column); the card-count column
     gets its own name (it clashes with the radius "cards").
5. Step 5 counts the helpers' links too.
6. After step 6, a script writes per faction ONE list of every usable concept and helper, sorted by fit (step 6's
   fit), with beside each how strongly it links to the faction's group (times chance, in how many games). Step 7 and
   the faction's card chat must read it: write that into START_DESIGN-1-wheel.md step 7 and START_DESIGN.md steps 5-8.
7. Report to Kaptain: what removing Skill changed and any shape that moved; the concepts by kind in plain words
   with card count and games; the new step 4 rule. Push; handoff.

## The numbers (library/cards_db)
- `links.sqlite` is rebuilt only after `network.py` or `cards.sqlite` changed: `PYTHONHASHSEED=0 python3 links.py`
  (about 7 minutes: tell Kaptain and wait for his OK); it ends with `cases/links.tsv` and the sides check.
- Radius keys are not plain words: look up each one's name before talking about it
  (`python3 -c "import axes; [print(s[0], s[3]) for s in axes.SPOKES]"`). `many` is "many at once", `wide` is "many
  cheap units", `back` is "brings back".
- A link counts for two concepts or radii only through what of each card made it. Example: Ghost Rider brings a card
  back and Vibro-Shock Gauntlets give +2 Power to it: revive with +2 Power, never revive with supply, though the
  Gauntlets also give Energy. Cases: `cases/wheel.tsv`.
- Two concepts you expect to work together show 0 links: check that one pair by script (what made each link between
  their cards) before trusting it; a wrong source is fixed for every card, with cases. Never read cards for it.

## Kaptain's standing decisions
- The game's own things: dots and front cells, rows (front/middle/back), columns, 3 lanes, the 3x3 camp, shapes and
  size, supply per lane, carry-over, round start and round end, one action per turn, moving and turning, reach (melee,
  Pike, Ranged), strikes and fixed damage, the hand and the discard pile, Immobile.
- Not in the game: player health, answers on the enemy's turn, supply that grows by itself, unit types, who acts first
  (random in round 1, then alternating), attacked units hitting back (only Riposte), placing at round end.
- The wheel is general; step 7 turns each faction's group into these own things, from scratch.
- Every game counts the same in every number. Shapes come from real factions, so a game with no factions (Marvel Snap)
  gives no shape; its cards still count in every number.
- Interactions with the player (heal, Block, strength on the player; the player hurt) stay off the radii: no player
  health here. They stay in the library as player_<concept>.
- Damage over time and my units changing form are possibilities for cards, not concepts a faction builds on.
- An all-Immobile faction is allowed.
- Must stay in: G = grows when hurt + I damage my own units; steal; kill spells; placing units in the enemy camp;
  bringing back without an Egg. Only one Egg in the whole wheel: look-alikes are compared by what the card does.
  "Strike first" is not a plan here. "Ping" is a library word: say "small hits".
- A faction's 100 cards draw on every usable concept and trigger of the library, never only its group: the group is
  its character (what it is strongest at, what its tools grow from), not all it may use.
- A faction is built from 2-4 tools that feed each other, played out cell by cell. The tools are the backbone, not all
  100 cards: 3-5 ways to play are built around them, as many as the closest real factions show. One idea is never the
  whole faction. The theme is picked after the group, before the tools; a tool that fits the theme but grows from no
  mechanic of the group is dropped.
- Each faction answers seven questions, one line each: how it wins, how it removes the front unit, how it MAINLY
  removes back-row units, how it MAINLY acts between lanes, how it holds a base, its best Place effect, its blind spot.
- Stop 1 pages: juicy and easy to read; one line per answer; one line per partner faction saying HOW the combo plays.
- Combos are judged once, on this board (step 8): STRONG / OK / WEAK / NONE / AGAINST; partners = STRONG or OK, 10+
  each; `combos.tsv` has a test column, and what doesn't work in play is dropped.
- Leaders: 5 per faction, the only cards with a golden border, spread over the costs and the ways to play; their
  special part works by whether I hold the lane's base, helps take and keep a lane, never wins harder in a won lane;
  nine kinds, mixed in each faction (START_DESIGN-2, "What a faction has").
- Countdowns very sparingly. A lane never holds more than 12 supply (summary/05).
- Draw on a kill is allowed: killing an enemy is something the player makes happen.
- "This round" effects that set up another effect of the same round are chains and wanted.
- Reading cards for one faction's chat: at most 100 (its steps 6 and 7), logged in `factions/read-cards.tsv`, never
  read twice. The wheel reads at most 500 cards in all, by a low-cost model, only where a card's rows can't answer.
- The check script fails on words that break the game's rules ("move first", "strikes first", "placed at round end").
- Keep chats short, scripts first.
