# The wheel: where we are
Read this, then `factions/START_DESIGN-1-wheel.md` (the steps, their rules and the stops), then only the step you are
on. Clone with the library (`git sparse-checkout disable`); `gunzip -kf links.sqlite.gz` in `library/cards_db`.
One chat does one step; at its end, mark the step done here and say what it left for the next.

## The steps
| step | state | what it made |
|---|---|---|
| 1. Fix the library's concepts | done | concepts split by whom a row acts on; "Skill" removed; Runeterra's spell mana rule written (`read/runeterra/game_rules.jsonl`) but not built yet |
| 2. The usable concepts | done; `concept_catch.py` still writes the share of each concept's cards on each radius: drop those columns in step 4 | `work/concepts.tsv`, `work/concepts.md` |
| 3. The archetypes | done | `archetypes.tsv`: 71 archetypes, 47 can exist, each with its concepts (radii in step 4); Formidable fixed in the library (strikes_with_defence, stat_fixed) |
| 4. The radii and how they work together | **next** | |
| 5. The 20 shapes | to do | |
| 6. The links between concepts | to do | |
| 7. The 20 groups and each faction's list | to do | |
| 8. Theme, then tools | to do | |
| 9. Combos on this board | to do | |
| 10. The seven answers, Stop 1 | to do | |

## What the next steps find in the files
- Step 4: `axes.py` still counts cards, not concept instances, and its `SPOKES` hold measurements that are no
  concepts (`position*` = "an effect on my own units beside it"): step 4 rewrites both as START_DESIGN-1 says. First
  show Kaptain every usable concept with the radius it goes on, in plain words, and wait for his OK. `axes.tsv`, `wheel-axes.html`, `wheel/radius_links.tsv` and
  `work/shapes.tsv` are from the old count and are all made again (steps 4 and 5).
- Step 4, agreed with Kaptain: the radius "brings back" becomes "reuses my cards" (return_to_hand, recycle,
  leave_trigger, discard, on_discard, self_mill, copy of a card or a unit, repeat_trigger: the same card or effect used
  again); revive and other_leave_trigger go on "spends them" (my units die, and
  come back). Picks keeps only choosing a card (tutor, selection, card_quality, information, deck_position,
  deck_condition).
- Step 4: `axes.py` still uses stat_multiply in `DISRUPT_ON_ENEMY` and its "multiply_own" measure; since 17 Nov 2026 a stat
  set on an enemy is stat_loss and a stat set to a number is stat_fixed: the rewrite uses the concepts as they are now.
- Step 5: 47 archetypes can exist, each carried by 2-3 shapes, but 20 shapes carry at most 2 each (40 places): ask
  Kaptain which rule gives before making the shapes.
- Step 6: `mechanics_wheel.py` has the radius mode only; the concept mode is written there, with the same count.
- Step 7: `groups.py` and `concept_list.py` are written; `tools/wheel_table_check.py` (it reads an old file) is
  rewritten.
- Step 10: `make_stop1.py` is rewritten.

## The numbers (library/cards_db)
- `links.sqlite` is rebuilt only after `network.py` or `cards.sqlite` changed: `PYTHONHASHSEED=0 python3 links.py`
  (about 6 minutes; with `check_all.py` 14 more: tell Kaptain and wait for his OK); it ends with `cases/links.tsv` and the sides check.
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
- The wheel is general; step 8 turns each faction's group into these own things, from scratch.
- Every game counts the same in every number. Shapes come from real factions, so a game with no factions (Marvel Snap)
  gives no shape; its cards still count in every number.
- Interactions with the player (heal, Block, strength on the player; the player hurt) stay off the radii: no player
  health here. They stay in the library as player_<concept>.
- Damage over time and my units changing form are possibilities for cards, not concepts a faction builds on.
- An all-Immobile faction is allowed.
- Must stay in: G = grows when hurt + I damage my own units; steal; kill spells; placing units in the enemy camp;
  bringing back without an Egg. Only one Egg in the whole wheel: look-alikes are compared by what the card does.
  "Strike first" is not a plan here. "Ping" is a library word: say "small hits".
- A faction's 100 cards use its list a lot (every concept of the library, by how strongly it links with the group):
  the group is its character (what it is strongest at, what its tools grow from), not all it may use.
- A faction is built from 2-4 tools that feed each other, played out cell by cell. The tools are the backbone, not all
  100 cards: 3-5 ways to play are built around them, as many as the closest real factions show. One idea is never the
  whole faction. The theme is picked after the group, before the tools; a tool that fits the theme but grows from no
  mechanic of the group is dropped.
- Each faction answers seven questions, one line each: how it wins, how it removes the front unit, how it MAINLY
  removes back-row units, how it MAINLY acts between lanes, how it holds a base, its best Place effect, its blind spot.
- Stop 1 pages: juicy and easy to read; one line per answer; one line per partner faction saying HOW the combo plays.
- Combos are judged once, on this board (step 9): STRONG / OK / WEAK / NONE / AGAINST; partners = STRONG or OK, 10+
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
