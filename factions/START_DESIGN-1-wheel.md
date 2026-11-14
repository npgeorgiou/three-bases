# The wheel chat: the first step, a high-level design of 20 factions based on the wheel (Kaptain, 10 Nov 2026)

Read `factions/START_DESIGN.md` and its parts 2-4 whole first, then `factions/12-mechanical-wheel.txt` and
`factions/13-wheel-measurement.txt` whole.
The chat writes no cards, no stats, no code and picks no themes. It does steps 2-5 of "The design process from the
wheel" in factions/12, in this order:
1. The pool of mechanics. Each is written "I do X -> I gain from X" on this game's own things (units, rows, lanes, dots,
   supply, carry-over, cards), comes from the library with its sources (game: card), can carry 30+ cards on this board,
   and is placed on the radii it serves. `python3 library/cards_db/apart.py` lists mechanics real factions keep apart
   and together; read the card texts before trusting a pair.
2. The 20 factions placed: OPEN, see factions/12 step 3 (real factions are not strong on radii side by side; their
   strong radii are joined by trigger -> payoff). Check each planned shape against real factions:
   `python3 axes.py --near "heals=1.6,growsdef=1.4,stops=0.3"` (from library/cards_db/) lists the 10 closest.
3. Per faction: its archetype (one sentence saying how it wins: Kaptain's first question), 2-3 monopolies, the 1-2
   mechanics it shares with each neighbour on a few cards, its blind spots from the far side, and the other four of
   Kaptain's five questions (step 2 of the thinking process in START_DESIGN.md).
4. The overlaps: per pair of neighbours, the combo the two make, as a played sequence (which card of one sets off which
   card of the other). Choose what neighbours share from radii that work together: the page's view "Radii that work
   together" (`factions/wheel-axes.html`) shows which radii real games join. A low number there is no ban (factions/12:
   real games only show what they happened to do); it means the combo must be argued from this game's rules.
How to read the wheel: 24 radii in 8 areas, measured on 43 real factions of 8 games (no Monster Train, no Marvel Snap).
A value compares a faction with the average faction of its own game, so compare factions of different games loosely.
Into the Breach, Stormbound, Slay the Spire and Inscryption have no value on 10 or more radii. Strength, defence and
the two width radii give a faction its shape; they are not mechanics two factions can share.
What Kaptain sees: one table of the 20 factions (place on the circle, archetype, strong radii, monopolies, shared with
the left and the right neighbour, blind spots) and the list of overlaps. The table is saved as one file in factions/
with a check script (factions/12, method 6). He agrees it before any faction chat starts.
