# The wheel chat: 20 factions designed together, with their combos (Kaptain, 14 Nov 2026)

Read `factions/START_DESIGN.md` and its parts 2-4 whole first, then `factions/12-mechanical-wheel.txt` and
`factions/13-wheel-measurement.txt` whole. Start with `python3 links.py` in `library/cards_db` (about 4 minutes; the
file is not in git). The chat writes no cards, no stats, no code for the game, and picks no themes.

Three Bases is a game of combos: decks will mix 2 factions. Every faction must combine reasonably well with at least
10 others (Kaptain, 14 Nov 2026), not only its two neighbours. Every mechanic, faction and combo here comes from the
library, measured and read; what has no library source is marked as Claude's.

## The whole process and its stops
- Wheel chat (this file): steps 1-6. **Stop 1: Kaptain agrees the table and the hooks.**
- One chat per faction (two can run at the same time): theme, then steps 1-6 of START_DESIGN.md (ways to play).
  **Stop 2: Kaptain agrees them.** Then cards, the gate, `wheel_check.js`, the separate agent's review.
  **Stop 3: Kaptain gets the finished faction.**
- Pilot: the first two factions are a neighbouring pair. Their premades play each other and some of the seven factions
  (`cardstats.js`), and one mixed deck shows whether their combo fires. **Stop 4: Kaptain decides whether the rest is built.**

## Steps 1-6 (in this order; the base is the wheel and its "Radii that work together")
1. **The 20 shapes and the circle, from the wheel.** Each faction is 3-6 strong radii that work together: every two of
   them with a high number in "Radii that work together" (`factions/wheel-axes.html`, all cards and real decks; a low
   number is argued from this game's rules). Values uneven, as real factions are; each shape is checked against real
   factions with `python3 axes.py --near "heals=1.6,growsdef=1.4,stops=0.3"` (from library/cards_db). Neighbours on the
   circle are the factions whose strong radii work together the most across the pair, so combos run between them.
2. **Pool of mechanics on those radii.** Start from the library's concepts of each strong radius (SPOKES in axes.py),
   not from a guess. For each: `factions` (real factions built on it), `analyze` on the closest real faction (30+ cards
   make it or use it here), and an agent reads 5-10 of its cards. Each is written "I do X -> I gain from X" on this
   game's things (units, rows, columns, front cells, dots, supply, carry-over, hand, discard pile), with its sources
   (game: card). Drop what can't carry 30 cards; merge two that are one mechanic (check with `both`); drop what copies
   the seven factions in the game (`factions/11-seven-factions.txt`). Effects the game can't do yet are marked NEW RULE.
3. **Links between mechanics.** For every two mechanics: how much more often than chance the library links a card of
   one with a card of the other (as `radius_links` in axes.py does for radii), all cards and real decks; then `fed`,
   `feeds`, `both`, `chains`, `deckmates`, and `apart.py` for pairs real factions keep apart. An agent reads the card
   pairs behind each high number and keeps only true combos (part 4), each written in this board's rules as a played
   sequence. Each faction gets 4-6 mechanics of its radii that feed each other; each mechanic one owner (2-3 per
   faction), its two neighbours may use it on a few cards.
4. **Hooks: 10+ partners per faction.** For every other faction, the combos between their mechanics from step 3, each a
   played sequence (which card of one sets off which card of the other) with its library number; also the pairs that
   work against each other. A faction under 10 is changed (steps 1-3 again for it).
5. **The five questions** (START_DESIGN.md step 2) for all 20 in one table. Every answer differs from every other
   faction's; each removal is a way no other faction has. Blind spots never touch a mechanic the faction owns or uses.
6. **Check script.** It checks real things, not only columns: the radius numbers of every shape, 30+ cards per
   mechanic, the library number of every combo, 10+ partners per faction, one owner per mechanic, the graph of
   factions/12 method 5.

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
1. Mechanics placed on radii and given owners by judgment, no card text read: some were too small to carry 30 cards,
   some were one mechanic counted twice. Stops it: step 2, measured and read.
2. One guessed combo per pair of neighbours, no library query behind it. Stops it: steps 3 and 4.
3. Neighbours chosen because they share one radius. Stops it: step 1, by "Radii that work together".
4. Every strong radius set to 1.8 and blind spots picked so the check passes. Stops it: uneven shapes from real factions.
5. A check script that checked only columns and counts, so it passed by construction. Stops it: step 6.
6. Factions that copied the seven in the game (a death faction with an Offering, a defence faction with Harden).
7. The radii and "Radii that work together" left out as the base (the rewrite of 14 Nov 2026 started from concepts).
   Stops it: step 1 builds the shapes and the circle from them, before any mechanic.
