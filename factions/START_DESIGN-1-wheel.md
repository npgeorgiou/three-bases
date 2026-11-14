# The wheel chat: 20 factions designed together, with their combos (Kaptain, 14 Nov 2026)

Read `factions/START_DESIGN.md` and its parts 2-4 whole first, then `factions/12-mechanical-wheel.txt` and
`factions/13-wheel-measurement.txt` whole. Start with `python3 links.py` in `library/cards_db` (about 4 minutes; the
file is not in git). The chat writes no cards, no stats, no code for the game, and picks no themes.

Three Bases is a game of combos: decks will mix 2 factions. Every faction must combine reasonably well with at least
10 others (Kaptain, 14 Nov 2026), not only its two neighbours. Every mechanic, faction and combo here comes from the
library, measured and read; what has no library source is marked as Claude's.

## The whole process and its stops
- Wheel chat (this file): steps 1-8. **Stop 1: Kaptain agrees the table and the hooks.**
- One chat per faction (two can run at the same time): theme, then steps 1-6 of START_DESIGN.md (ways to play).
  **Stop 2: Kaptain agrees them.** Then cards, the gate, `wheel_check.js`, the separate agent's review.
  **Stop 3: Kaptain gets the finished faction.**
- Pilot: the first two factions are a neighbouring pair. Their premades play each other (`cardstats.js`), and one mixed deck shows whether their combo fires. **Stop 4: Kaptain decides whether the rest is built.**

## Steps 1-8 (in this order: the wheel first, then the mechanics inside it)
Why this order and every number behind it: `factions/wheel/HANDOFF.md`.
1. **The radii.** The 24 radii of `factions/13-wheel-measurement.txt`, measured on the real factions (axes.tsv, the page
   factions/wheel-axes.html).
2. **The radii that work together.** For every two radii, the library's number in all cards and in real decks
   (`radius_links` in axes.py, the page's fourth view). Trust "rewards playing spells" only by its deck number: such a
   card links to every spell. Read the real card pairs behind the strong numbers (an agent) before using them.
3. **The 20 factions as shapes.** Each is 3-6 strong radii; each radius joined to at least one other of the faction by
   trigger -> payoff with a strong number in step 2 (one radius makes what another needs). The shapes are uneven, as
   real factions are, and checked against them: `python3 axes.py --near "heals=1.6,growsdef=1.4,stops=0.3"` (from
   library/cards_db). No two shapes the same.
4. **The circle.** Neighbours are the two factions whose radii work together most (step 2), not two that merely share a
   radius.
5. **The mechanics inside each faction's radii.** From the library's concepts (`ask.py all list concepts`); the pool of
   `factions/wheel/` is a start. For each: an agent reads 8 of its cards first and fixes the concept list until it
   catches the right cards; only then it is measured: `factions` (the real factions built on it), the radii it serves,
   its count in the closest real faction. Each is written "I do X -> I gain from X" on this game's things (units, rows,
   columns, front cells, dots, supply, carry-over, hand, discard pile), with its sources (game: card). Small mechanics
   are kept and marked small; each mechanic keeps its own line. Every effect the game can't do yet is marked NEW
   RULE. Each faction owns 2 mechanics (its monopolies); two factions strong on the same radius own different mechanics
   in it; the owner's two neighbours may use a mechanic on a few cards.
6. **Links between mechanics and the hooks.** `python3 mechanics_wheel.py links` gives, for every two mechanics, the
   library's number in all cards and in real decks; run it only after step 5's concepts are fixed. Then `fed`,
   `feeds`, `both`, `chains`, `deckmates` on the strong pairs and `apart.py` for the pairs real factions keep apart. An
   agent reads the real card pairs behind each high number (`mechanics_wheel.py pairs`) and keeps only true combos
   (one card changes what the other does; part 4), each written in this board's rules as a played sequence. Then every
   faction's partners: for every other faction, the combos between their mechanics, with the library number. 10+
   partners per faction; also the pairs that work against each other. A faction under 10 is regrouped (step 3 again).
7. **The five questions** (START_DESIGN.md step 2) for all 20 in one table. Every answer differs from every other
   faction's; each removal is a way no other faction has. Blind spots never touch a mechanic the faction owns or uses.
8. **Check script.** It reads the files of steps 1-7 and checks real things, not only columns: the library number of
   every join and combo (a low number must be argued from this game's rules), 10+ partners per faction, one owner per
   mechanic, 2 per faction, the graph of factions/12 method 5 (each faction's mechanics linked to each other).

## What Kaptain sees at Stop 1
The table of the 20 factions (place, archetype, strong radii, monopolies, shared with each neighbour, blind spots, the
five answers), per faction its partners with the combo for each, and the pairs that work against each other. Files in
factions/ (each under 150 lines; split them) and the check script in tools/; the CLAUDE.md map names them.

## How to read the wheel
24 radii in 8 areas, measured on 43 real factions of 8 games (no Monster Train, no Marvel Snap). A value compares a
faction with the average faction of its own game, so compare factions of different games loosely. Into the Breach,
Stormbound, Slay the Spire and Inscryption have no value on 10 or more radii. Strength, defence and the two width radii
give a faction its shape; they are not mechanics two factions can share.

## NEVER DO (the first wheel table of 14 Nov 2026, rejected)
1. Mechanics placed on radii and given owners by judgment, no card text read. Stops it: step 5, read and measured.
2. One guessed combo per pair of neighbours, no library query behind it. Stops it: step 6.
3. Neighbours chosen because they share one radius. Stops it: step 4, by the links.
4. Every strong radius set to 1.8 and blind spots picked so the check passes. Stops it: uneven shapes from real factions.
5. A check script that checked only columns and counts, so it passed by construction. Stops it: step 8.
6. The radii and "Radii that work together" left out as the base (the rewrite of 14 Nov 2026 started from concepts).
   Stops it: steps 1-4 build the shapes and the circle from them, before any mechanic.
