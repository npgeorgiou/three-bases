# The wheel chat: 20 factions designed together, with their combos (Kaptain, 14 Nov 2026)

Read `factions/START_DESIGN.md` and its parts 2-4 whole first, then `factions/12-mechanical-wheel.txt`,
`factions/13-wheel-measurement.txt` and `factions/wheel/HANDOFF.md` whole (the handoff holds the numbers behind every
step here and the reasons). Start with `python3 links.py` in `library/cards_db` (about 4 minutes; the file is not in
git). The chat writes no cards, no stats, no code for the game, and picks no themes.

Three Bases is a game of combos: decks will mix 2 factions. Every faction must combine reasonably well with at least
10 others (Kaptain, 14 Nov 2026), not only its two neighbours. Every radius, mechanic, faction and combo here comes
from the library, measured and read; what has no library source is marked as Claude's.

## The whole process and its stops
- Wheel chat (this file): steps 1-8. **Stop 1: Kaptain agrees the table and the hooks.**
- One chat per faction (two can run at the same time): theme, then steps 1-6 of START_DESIGN.md (ways to play).
  **Stop 2: Kaptain agrees them.** Then cards, the gate, `wheel_check.js`, the separate agent's review.
  **Stop 3: Kaptain gets the finished faction.**
- Pilot: the first two factions are a neighbouring pair. Their premades play each other (`cardstats.js`), and one
  mixed deck shows whether their combo fires. **Stop 4: Kaptain decides whether the rest is built.**

## Steps 1-8, in this order
The wheel comes first (steps 1-4): it gives every faction its shape and its place on the circle. The mechanics come
after (steps 5-6), found inside each faction's radii, and the combos between factions come from them. A step uses
only what the steps before it made.

**A. The wheel**
1. **The radii.** The 24 radii of `factions/13-wheel-measurement.txt`, measured on the real factions (axes.tsv; the
   page factions/wheel-axes.html).
2. **The radii that work together.** For every two radii, the library's number in all cards and in real decks
   (`radius_links` in axes.py; the page's fourth view): how much more often than chance a card of one is linked with a
   card of the other. An agent reads the real card pairs behind the strong numbers before they are used. "Rewards
   playing spells" is trusted only by its deck number, because such a card links to every spell.
3. **The 20 factions as shapes.** Each faction is 3-6 strong radii. Each of its radii is joined to at least one other
   of them by trigger -> payoff: one radius makes what the other needs ("spends them" makes deaths, "brings back"
   uses them), with a strong number in step 2. A join with a low number stays only when this game's rules argue for
   it. The values are uneven, as real factions are, and each shape is checked against them:
   `python3 axes.py --near "heals=1.6,growsdef=1.4,stops=0.3"` (from library/cards_db). No two shapes are the same.
4. **The circle.** Neighbours are the two factions whose strong radii work together the most across the pair (step
   2), so combos run between them; never two that merely share a radius.

**B. The mechanics and the combos**
5. **The mechanics inside each faction's radii.** For each strong radius, start from its library concepts (SPOKES in
   axes.py); `factions/wheel/mechanics.tsv` is a start, not a result. For each mechanic, in this order:
   - an agent reads 8 of its cards and fixes the concept list until it catches the right cards
     (`mechanics_wheel.py cards`);
   - then it is measured (`mechanics_wheel.py measure`): the real factions built on it, the radii it serves, its count
     in the closest real faction;
   - it is written "I do X -> I gain from X" on this game's things (units, rows, columns, front cells, dots, supply,
     carry-over, hand, discard pile), with its sources (game: card). Each mechanic keeps its own line; a small one is
     kept and marked small. An effect the game can't do yet is marked NEW RULE.
   Each faction gets 4-6 mechanics of its radii that feed each other. It owns 2 of them (its monopolies); the others
   it shares with its two neighbours, on a few cards. Two factions strong on the same radius own different mechanics
   in it ("brings back": one owns "my dead units come back", another "my unit goes back to hand").
6. **Links between mechanics, and the hooks.** Only after step 5's concepts are fixed: `mechanics_wheel.py links`
   gives, for every two mechanics, the library's number in all cards and in real decks. Then `fed`, `feeds`, `both`,
   `chains` and `deckmates` on the strong pairs, and `apart.py` for the pairs real factions keep apart. An agent reads
   the real card pairs behind each high number (`mechanics_wheel.py pairs`) and keeps only true combos (one card
   changes what the other does; part 4), each written in this board's rules as a played sequence. Then each faction's
   partners: for every other faction, the combos between their mechanics (which card of one sets off which card of
   the other), with the library number. 10+ partners per faction; also the pairs that work against each other. A
   faction under 10 partners is changed: steps 3-6 again for it.
7. **The five questions** (START_DESIGN.md step 2) for all 20 in one table. Every answer differs from every other
   faction's; each removal is a way no other faction has and uses a mechanic the faction owns or shares (B's "my unit dies and takes the enemy facing it" is the sacrifice: B needs it). Blind spots never touch a mechanic the faction owns or uses.
8. **Check script.** It reads the files of steps 1-7 and checks real things, not only columns: the radius numbers of
   every shape's joins (step 3), the library number of every combo (step 6); a low number must carry its argument from
   this game's rules. Also: 10+ partners per faction, 2 owned mechanics per faction and one owner per mechanic, and
   the graph of factions/12 method 5 (each faction's mechanics linked to each other).

## What Kaptain sees at Stop 1
The table of the 20 factions (place, archetype, strong radii, monopolies, shared with each neighbour, blind spots, the
five answers), per faction its partners with the combo for each, and the pairs that work against each other. Files in
factions/ (each under 150 lines; split them) and the check script in tools/; the CLAUDE.md map names them.

## How to read the wheel
24 radii in 8 areas, measured on 43 real factions of 8 games (no Monster Train, no Marvel Snap). A value compares a
faction with the average faction of its own game, so compare factions of different games loosely. Into the Breach,
Stormbound, Slay the Spire and Inscryption have no value on 10 or more radii. Strength, defence and the two width radii
give a faction its shape; they are not mechanics two factions can share.

## Token budget (second try, 14 Nov 2026: it ran out in step 6)
Agents used about 9 of every 10 tokens: 23 agents at 100-160k each. What to do instead:
- Combo reads: first 4 card pairs per mechanic pair, and 8 only for pairs that come back KEEP or WEAK (106 of 167
  read pairs were DROP after 8 pairs each). Read only pairs that can still add a partner the faction lacks.
- Batches: at most 4 agents at once, each with about 20 sections; write each agent's lines to its file as it goes,
  so a stop loses nothing. Before a big batch, count the sections and say how many agents it needs.
- Concept fixes: give the agent the counts per game in its file (`ask.py all compare` output for each concept), so it
  does not run 30 queries itself.
- Owners and shares: write the rules down before the first try (2 owned on the faction's radii, shares only from the
  two neighbours or SMALL unowned ones, every mechanic that is not SMALL owned), then check each try with
  `work/check_assign.py`. Three tries by hand and two runs of an unchecked search were wasted.
- Skip numbers that can't decide anything: partner counts from link numbers alone came out 15-19 for every faction.

## NEVER DO (the rejected tries of 14 Nov 2026)
1. The radii and "the radii that work together" left out as the base: a pool of mechanics built first, from concepts.
   Stops it: steps 1-4 come before any mechanic.
2. Mechanics placed on radii and given owners by judgment, no card text read. Stops it: step 5, read and then measured.
3. One guessed combo per pair of neighbours, no library query behind it. Stops it: step 6.
4. Neighbours chosen because they share one radius. Stops it: step 4, by the radii that work together.
5. Every strong radius set to 1.8 and blind spots picked so the check passes. Stops it: uneven shapes from real
   factions (step 3).
6. A check script that checked only columns and counts, so it passed by construction. Stops it: step 8.
