# The wheel: where we are
Read this, then `factions/START_DESIGN-1-wheel.md` (the steps, their rules and the stops), then only the step you are
on. Clone with the library (`git sparse-checkout disable`); `gunzip -kf links.sqlite.gz` in `library/cards_db`.
One chat does one step; at its end, mark the step done here.

## The steps
| step | state | what it made |
|---|---|---|
| 1. Fix the library's concepts | done 16 Nov 2026 | concepts split by whom a row acts on (player, my unit, cards between piles), radii without game limits; `work/suspect_verdicts.tsv` |
| 2. The radii and how they work together | redo (Agreed 17 Nov, items 2-3) | `axes.tsv`, `wheel/radius_links.tsv` |
| 3. The 20 shapes | redo (Agreed 17 Nov, items 1-3) | `work/shapes.tsv` |
| 4. The usable concepts | done 17 Nov 2026 (redone: kinds usable, helper, out; Skill removed from the library; steps 2-3 redone, nothing moved) | `work/concepts.tsv`, `work/concepts.md` |
| 5. The links between concepts | to do (Agreed 17 Nov, item 4); `mechanics_wheel.py` gets a concept mode (usable concepts and helpers; `cards`, `decks`, `games`, never a raw pair count) | |
| 6. The 20 groups | to do; `work/groups.py` and `work/concept_list.py` to write, `tools/wheel_table_check.py` to rewrite (it still reads the old `level`) | |
| 7. Theme, then tools | to do | |
| 8. Combos on this board | to do | |
| 9. The seven answers, Stop 1 | to do; `work/make_stop1.py` to rewrite | |

For step 6: some archetypes (`archetypes.tsv`) name concepts that are no library concept with 10+ cards: the
starred radius groups countboard*, kill*, weaken*, spelldmg*, position*, and polymorph, piercing, cross_lane.

## Agreed 17 Nov 2026 (Kaptain approved; do in this order, each with Kaptain's OK before the next)
1. **Archetypes from Kaptain's list** (`archetypes_kaptain.txt`) replace the 18 in `archetypes.tsv`. For each one: can
   it exist in this game (no lands, poison, player life, planeswalkers, multiplayer...; the reason when not); for the
   others its library concepts and its radius (Claude's, marked). Show Kaptain the table; he approves.
2. **Every usable concept on one radius** (a radius is defined by its concepts, `axes.SPOKES`), starting with "moving my
   units" (movement) on "position and combos"; each archetype's concepts on its radius. Show Kaptain; he approves.
3. **Radii measured by concept instances, not cards:** every instance of a concept in the database (one row that gives
   it) goes to its concept's radius; a faction's value = the share of its instances on that radius; the card itself
   goes nowhere ("deal 2, then draw" = one instance on damage, one on more cards). Strength and defence stay measured
   from the units' numbers. Rewrite `axes.py` and the docs (START_DESIGN-1 steps 2 and 6, 13-wheel-measurement.txt),
   redo step 2 and step 3 (the shapes may change; Kaptain approves them again).
4. **Step 5** with `cards`, `decks`, `games` and the slow `level` (1 pair = 1, 10 = 2, 100+ = 3); rare links are never
   lost. Games with no factions (Marvel Snap, Inscryption, Into the Breach, Slay the Spire, Monster Train...) count in
   every concept-pair number like the others.
5. **Step 6 and each faction's list:** the list holds every concept (on radii, helpers, out: all); each has a score of
   how often its instances link with the faction's group (any of its 4-6 concepts), per game:
   (real links + 1) / (chance links + 1), then averaged over the games where it and the group both appear (every game
   weighs the same; games with no factions count). Shown with it: the slow level and in how many games. Step 7 (tools)
   and START_DESIGN steps 5-8 (cards) use the list a lot.
- Spell mana (Runeterra) is recorded (`read/runeterra/game_rules.jsonl`, `kind_has`), not yet built: rebuild
  `check_all.py runeterra` and `PYTHONHASHSEED=0 links.py` (about 20 minutes, Kaptain's OK first) before step 3's
  measuring.

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
