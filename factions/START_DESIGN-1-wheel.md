# The wheel chat: 20 factions designed together, with their combos

Read `factions/START_DESIGN.md` and its parts 2-4 whole first, then `factions/wheel/HANDOFF.md` (which step is next,
Kaptain's standing decisions) and this file. Commands of every step: `factions/wheel/PIPELINE.md`. Library commands run
from `library/cards_db/`; first `gunzip -kf links.sqlite.gz` there. The wheel writes no cards, no stats and no game code.

Three Bases is a game of combos: decks mix 2 factions, and every faction combines well with at least 10 others. Every
number comes from the library by script; anything with no library source is marked as Claude's. Faction text uses plain
words Kaptain uses ("small hits", "the rest of the hit goes into the unit behind"), never library names.

## The words
- **Concept**: a tag the library gives an effect ("revive": a unit comes back; "attack_gain": gains strength).
- **Concept instance**: one effect of one card that gives a concept (one row in the database). "Deal 2 to an enemy,
  then draw a card" is two instances: one of damage, one of drawing.
- **Card link**: two real cards of one game where an effect of one sets off or feeds an effect of the other
  (`links.sqlite`). Each link keeps which effect of each card made it, so it counts only for those effects' concepts.
- **Archetype**: a general way to play from Kaptain's list (`wheel/archetypes_kaptain.txt`: aggro, control,
  aristocrats, reanimator, theft...); none is tied to one game's card types, resources, keywords or multiplayer. One
  archetype can be played with different tools, so it is made of parts, each a set of alternative concepts that can do
  it. A part is an **engine** (it works through links with another part: "my units die" -> "my units gain when an ally
  dies") or a **brick** (it works alone and links to nothing: disruption, removal).
- **Radius**: one direction of the wheel, such as "more supply" (23 radii; their names and concepts are in
  `wheel/work/radii.tsv`, from which `axes.py` builds `SPOKES`). Every usable concept belongs to one radius; a few
  count on two, each instance by what its rows say (deal damage: on a spell for "damage from spells", on any other card
  for "damage from units' text"). A faction's value on a radius is the share of its concept instances that belong to
  that radius; the card itself goes nowhere.
- **The faction's archetypes**: the one or, better, more archetypes a faction plays (step 7). Their concepts are its
  character (what it is strongest at, what its tools grow from).
- **The faction's list**: every concept of the library (usable, helpers and out), each with its score for how strongly
  it links with the concepts of the faction's archetypes. The faction's cards use it a lot, to make those concepts
  possible, start them or make them stronger.
- **Helper**: a concept that only says when or how a card acts, one of the game's own things, or a thing for single
  cards (step 2). Never a part of an archetype; always on the faction's list.
- **Mechanic**: a link between two concepts of the faction's archetypes, shown by real card pairs, never written by hand: "makes your
  units die: the other card brings them back (in 7 of 10 games, 3.1 times chance)".

## Rules for every step (Kaptain)
- Every game counts the same in every number: worked out in each game alone, then averaged. Games with no factions
  (Marvel Snap, Inscryption, Into the Breach, Slay the Spire, Monster Train) count in every number about concepts and
  their links.
- How well two things link is judged by how much more often than chance real cards link them, worked out per game;
  ties are broken by how many games show it. The linked pairs themselves count only as a level that grows slowly
  (`level`: 1 pair = 1, 10 = 2, 100 or more = 3), so a big game cannot drown the others and a pairing rare in the ten
  games is never lost.
- A concept needs 10+ real cards in the library (all games together).
- Scripts, no reading agents. Card texts are read only where a card's rows can't answer: at most 500 cards for the
  whole wheel, by a low-cost model; count them and get Kaptain's OK first.
- A concept that means two things in different games is a library error: it is split in the library, with test cases,
  never limited to some games in a list.

## The stops
- **Kaptain agrees the archetypes and their parts** (step 3), **the concepts on each radius** (step 4) and
  **the 20 factions' archetypes** (step 7). **Stop 1: Kaptain agrees the 20 factions** (step 10).
- Then one chat per faction (two can run at once): steps 1-6 of `START_DESIGN.md`. **Stop 2: Kaptain agrees them.**
  Then cards, the gate, `wheel_check.js`, a separate agent's review. **Stop 3: Kaptain gets the finished faction.**
- Pilot: the first two factions are a pair with a STRONG combo; their premades play each other (`cardstats.js`) and
  one mixed deck shows whether the combo fires. **Stop 4: Kaptain decides whether the rest is built.**

## Steps 1-10, in this order (each uses only what the steps before made)
1. **Fix the library's concepts.** The suspects: every concept counted only in some games (`wheel/work/suspects.tsv`),
   and every concept whose cards link to quite different concepts in one game than in the others (by script). For
   each: if its cards in the other games do something else, split the concept by what the rows already say (on a unit
   on the board or on a card in hand; on an enemy or on my own unit; on the player or on a unit; the main supply or a
   side resource), by a fix script with test cases (`library/cards_db/START_DATABASE.md`); if it is the same, no game
   limit. A game whose player is a unit on the board (Duelyst's General; a rule in its `game_rules.jsonl`) gives its
   player rows both concepts. Rows that can't tell: read, within the 500. A concept that only says what kind of record
   a card is (an "ability" record) is a library error and is removed. A rule of a game that no card text says
   (Runeterra: up to 3 unspent mana is kept as spell mana) is a record in its `game_rules.jsonl`, with its source, on
   the cards it concerns. Then `check_all.py` (about 14 minutes) and `links.py` (about 6) are rebuilt, Kaptain's OK first.
2. **The usable concepts** (`work/concept_catch.py` -> `work/concepts.tsv`, `work/concepts.md`). Every concept with
   10+ real cards, with its card count (`card_count`) and its games, sorted into three kinds
   (`work/concept_verdicts.tsv`: kind and reason, each marked Kaptain's or Claude's; a concept not in it is usable):
   - Usable: a faction can build on it. It says what a card does ("brings back a dead unit"), or reacts to something
     the player makes happen or builds up ("when a card is drawn", "when it becomes a target", "if your hand holds 5
     cards").
   - Helper: it only says when or how a card acts ("when played", "at end of round", "once per game", "choose one of
     two effects"); or it is one of the game's own things (lanes, bases, carry-over, cells and rows, the 3x3 camp,
     unit cost); or it is a thing for single cards (used once, a drawback, a wall that can't attack, choosing the
     target).
   - Out: it is not in this game (player health, blocking, answers on the enemy's turn, unit types, shops, supply that
     grows by itself) or Kaptain ruled it out (randomness, my units changing form, countdowns).
   A parent in the concept tree keeps only the cards none of its children carry, so no effect counts twice.
   `work/concepts.md` shows the kinds in plain words for Kaptain.
3. **The archetypes** (`wheel/archetypes_kaptain.txt` -> `wheel/archetypes.tsv`). Only the archetypes of Kaptain's
   list that can exist in this game go in (Three Bases has no lands, no player life, no poison, no planeswalkers, no
   multiplayer, no unit types, no randomness, no answers on the enemy's turn); for each, what it is in this game and its
   parts, read from the words of its line and from how real games play it: each part in plain words, engine or brick,
   with every usable concept (step 2) that can do it. A part is never left to "the units' own numbers": cheap, big or
   strong units are made by concepts too (cards cost less, cost matters, stats equal to a count). For each engine part,
   `wheel/concept_links.tsv` shows which concepts real cards link with the other part's; those that fit the part by
   meaning go in. Claude's, marked. Each concept is checked against its definition in
   `library/concept_tree.txt`; before saying no concept fits, search `vocab.tsv` keywords by meaning (Runeterra's
   Formidable is "strikes with its defence"): a keyword on a loose concept is a library error, fixed as
   `START_DATABASE.md` says. A part with no concept is shown to Kaptain, never filled by guessing.
   **Kaptain agrees the archetypes and their parts.**
4. **The radii and how they work together** (`wheel/work/radii.tsv`). Every usable concept is put on one radius whose
   name says what the concept does (copying a unit is no draw); how often real cards link two concepts decides only
   between radii that fit. A trigger or a condition goes on the radius of the thing it reacts to ("when a unit dies" on
   "spends them"); a count goes with what it counts, read from its rows ("if 3 allies died" on "spends them"). A
   concept whose rows say two different things counts each instance where its rows put it (`axes.py` PART: damage by
   the card, a stat change by the number it changes, "when I play another card" by what is played, "a rule changed" by
   the rule). The wheel describes the examined games: nothing is left off because Three Bases lacks it; later steps
   decide what this game uses. **Kaptain agrees the concepts on each radius**,
   and every later move. Then `axes.py` measures the 43 real factions: a faction's value on a radius = the share of its
   concept instances on that radius, divided by its game's average share (1 = the average faction of its game).
   Strength, defence and "a few big units" come from the units' numbers; "many units on my side" adds its cheap units
   to its concepts, and "position and combos" its card links. For every two radii (`mechanics_wheel.py links
   --radii`): `cards` = how much more often than chance their concepts' instances are linked; `decks` = how much more
   often real decks heavy in one hold the other; `games` = in how many games real cards link them; `level` = the
   linked pairs as the slow level. Joined: `cards` 1.2+ or `decks` 1.5+; "rewards playing spells" by `decks` only
   (such a card links to every spell).
5. **The links between concepts** (`mechanics_wheel.py links --concepts` -> `wheel/concept_links.tsv`). For every two
   concepts of `work/concepts.tsv` (usable, helpers and out), by the same count as step 4: `cards`, `decks`, `games`,
   `level`; `rare` for a pair chance gives under 5 linked pairs in every game (all linked pairs over all chance);
   `makes` (the share of the pair's links where a's card sets off or feeds b's card); the three most common link
   texts. Joined: `cards` 1.2+, or `decks` 1.5+, or `rare` 3+ with a `level` of 1+. `apart.py` lists the concept pairs
   real factions keep apart.
6. **The archetype map** (`work/archetype_map.py` -> `work/archetype_map.tsv` and `factions/wheel-archetypes.html`).
   Each concept of an archetype's parts is a node; a concept used by several archetypes is one node. Between the
   concepts of two engine parts of an archetype, an edge with the step 5 numbers: `cards` (how much more often than
   chance real cards link them), `games`, `level`, the top link text and one real card pair. Bricks are nodes with no
   edges. Two engine parts whose concepts real cards never link are shown to Kaptain with the numbers. On the page
   Kaptain picks one archetype to see its nodes and edges, or all of them to see where archetypes touch.
7. **The 20 factions and their lists** (by script, from the archetype map; `work/factions.py` ->
   `work/factions.tsv`). Each faction plays one or, better, more archetypes that work together as one, judged by the
   strengths of the map. The rules the script follows are agreed with Kaptain before it is written. Kaptain sees per
   faction: its archetypes in plain words, their concepts, and its mechanics (each edge: the real link text with its
   times chance and games); one sentence per faction, written from those texts. **Kaptain agrees the 20 factions'
   archetypes.** Then each faction's list (`work/concept_list.py` -> `work/lists/<letter>.tsv`): every concept with
   10+ cards (usable, helpers and out), each with its score. In each game alone: real links between the concept's
   instances and the instances of the concepts of the faction's archetypes, against the links chance alone gives there;
   the game's score = (real + 1) / (chance + 1), so a single rare link doesn't look huge and a big count is almost
   untouched; the score = the average over the games where the concept and those concepts both appear (every game
   weighs the same). Beside it: the `level` and in how many games. Sorted by score.
8. **Theme, then tools.** First each faction gets a real theme (World War I artillery, the Zulu regiments) picked for
   its archetypes; the 20 themes all differ; the theme is a source of tools, never a reason for one. Then 2-4 tools per
   faction: a tool is a new kind of thing or rule that makes its mechanics happen on this game's own things
   (dots and front cells, rows, columns, lanes, the 3x3 camp, unit size, supply per lane, carry-over, round start and
   end, one action per turn, moving, reach, strikes and fixed damage, the hand, the discard pile, Immobile), used
   on many of its cards, built with the concepts of its list, highest scores first. Each tool names the mechanic it
   grows from; each tool feeds another (one makes what the other uses); each is played out
   cell by cell (which cell, what happens, what the enemy does with his one action between; two tools needing the same
   cell clash). The linked card pairs of the mechanic are its source cards. No two factions have the same tool doing
   the same job, compared by what the card does: one Egg in the whole wheel. Countdowns very sparingly; a lane never
   holds more than 12 supply. A rule the game lacks is marked NEW RULE. Written to `wheel/themes.tsv` and
   `wheel/tools.tsv`. The old candidates (commit d4a3de0^, `factions/3-candidates/`) are read last, only to see that
   no idea Kaptain liked is missing.
9. **Combos on this board.** For every pair of factions (190), the joins between the concepts of one faction's archetypes
   and the other's (step 5 numbers), by script. Claude rates each pair with numbers on the board, from the two factions'
   tools: STRONG (both halves on many cards, helps take or hold a base, the enemy's one action between can't easily
   stop it), OK (real but breakable), WEAK, NONE, AGAINST. Partners = STRONG or OK; every faction has 10+; one under
   10 goes back to step 7. `wheel/combos.tsv` has a test column that playtests fill.
10. **The seven answers** for all 20, made from the tools: how it wins, how it removes a front unit, how it mainly
   removes back-row units, how it mainly acts between lanes, how it holds a base, its best Place effect, its blind spot.
   Every answer differs from every other faction's; each removal uses one of its mechanics; a blind spot never touches
   its archetypes. Then `tools/wheel_table_check.py` and the Stop 1 pages (`work/make_stop1.py` -> `wheel/STOP1*.md`:
   per faction its archetypes and mechanics, theme, tools and how they feed each other, the seven answers, and one
   line per partner saying how the combo plays). Files under 150 lines.
