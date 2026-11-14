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

## Steps 1-6 (in this order)
1. **Pool of mechanics.** Start from the library's concepts (`ask.py all list concepts`), not from a guess. For each
   candidate: `factions` (which real factions are built on it), which radii it serves (its concepts against SPOKES in
   axes.py, measured, not judged), `analyze` on the closest real faction (30+ cards make it or use it), and an agent
   reads 5-10 of its cards and says whether the concept catches the right cards. Each is written "I do X -> I gain from
   X" on this game's things (units, rows, columns, front cells, dots, supply, carry-over, hand, discard pile), with its
   sources (game: card). Drop what can't carry 30 cards here; merge two that are one mechanic (lock and silence, offer
   and Death effects: check with `both`); drop what copies the seven factions in the game (Offering, Harden, Barrage,
   Augur, Marked...: `factions/11-seven-factions.txt`). Every effect the game can't do yet is marked NEW RULE.
2. **Links between mechanics.** A script gives, for every two mechanics, how much more often than chance the library
   links a card of one with a card of the other in the same game (as `radius_links` in axes.py does for radii), in all
   cards and in real decks. Then `fed`, `feeds`, `both`, `chains` and `deckmates` on the strong pairs, and `apart.py`
   for the pairs real factions keep apart. An agent reads the real card pairs behind each high number and keeps only
   true combos (one card changes what the other does; part 4); each is written in this board's rules as a played
   sequence. Result: the combo list, mechanic by mechanic, with its numbers.
3. **The 20 factions.** Each is 4-6 mechanics that feed each other in the combo list, giving 3-6 strong radii joined by
   trigger -> payoff (factions/12, step 3). Each mechanic has one owner (its monopoly; 2-3 per faction); the owner's
   two neighbours may use it on a few cards. Each shape is checked against real factions with uneven values, as real
   factions are: `python3 axes.py --near "heals=1.6,growsdef=1.4,stops=0.3"` (from library/cards_db).
4. **The circle and the hooks.** Neighbours are the two factions whose mechanics link the most (step 2), not two that
   merely share a radius. Then every faction's partners: for every other faction, the combos between their mechanics
   from the combo list, each a played sequence (which card of one sets off which card of the other), with its library
   number. 10+ partners per faction; also the pairs that work against each other. A faction under 10 is regrouped
   (step 3 again).
5. **The five questions** (START_DESIGN.md step 2) for all 20 in one table. Every answer differs from every other
   faction's; each removal is a way no other faction has. Blind spots never touch a mechanic the faction owns or uses.
6. **Check script.** It reads the files of steps 1-5 and checks real things, not only columns: 30+ cards per mechanic,
   the library number of every join and combo (a low number must be argued from this game's rules), 10+ partners per
   faction, one owner per mechanic, the graph of factions/12 method 5 (each faction's mechanics linked to each other).

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
   some were one mechanic counted twice. Stops it: step 1, measured and read.
2. One guessed combo per pair of neighbours, no library query behind it. Stops it: steps 2 and 4.
3. Neighbours chosen because they share one radius. Stops it: step 4, by the links.
4. Every strong radius set to 1.8 and blind spots picked so the check passes. Stops it: uneven shapes from real factions.
5. A check script that checked only columns and counts, so it passed by construction. Stops it: step 6.
6. Factions that copied the seven in the game (a death faction with an Offering, a defence faction with Harden).
