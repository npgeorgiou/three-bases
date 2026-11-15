# The wheel chat: 20 factions designed together, with their combos

Read `factions/START_DESIGN.md` and its parts 2-4 whole first, then `factions/12-mechanical-wheel.txt` (why the wheel
and its radii) and `factions/wheel/PIPELINE.md` (the commands of every step). Start with `python3 links.py` in
`library/cards_db` (about 4 minutes; the file is not in git). The chat writes no cards, no stats, no code for the game,
and picks no themes.

Three Bases is a game of combos: decks mix 2 factions. Every faction combines well with at least 10 others. Every
radius, mechanic and combo comes from the library, measured and read; what has no library source is marked as Claude's.
Faction text uses plain words Kaptain uses (no library names like "ping" or "overkill": say "small hits", "the rest of
the hit goes into the unit behind").

## The whole process and its stops
- Wheel chat (this file): steps 1-9. **Stop A: Kaptain agrees the mechanics list (step 4).** **Stop 1: Kaptain agrees
  the 20 factions (step 9).**
- One chat per faction (two can run at the same time): theme, then steps 1-6 of START_DESIGN.md (ways to play).
  **Stop 2: Kaptain agrees them.** Then cards, the gate, `wheel_check.js`, the separate agent's review.
  **Stop 3: Kaptain gets the finished faction.**
- Pilot: the first two factions are a pair with a STRONG combo. Their premades play each other (`cardstats.js`), and
  one mixed deck shows whether their combo fires. **Stop 4: Kaptain decides whether the rest is built.**

## Steps 1-9, in this order
A step uses only what the steps before it made. Steps 1-3 are the wheel; the mechanics come after, found inside each
faction's radii.

1. **The radii.** The 24 radii of `factions/13-wheel-measurement.txt`, measured on 43 real factions (`axes.py`).
2. **The radii that work together.** For every two radii, the library's number in all cards and in real decks: how much
   more often than chance a card of one is linked with a card of the other (1 = chance). Agents read the real card
   pairs behind the strong numbers; a pair they drop counts as chance afterwards. "Rewards playing spells" is judged by
   its deck number only, because such a card links to every spell.
3. **The 20 factions as shapes.** Each faction is 3-6 strong radii with uneven values, as real factions have. Each
   radius is joined to another of the same faction by a strong number of step 2 (one makes what the other needs:
   "spends them" makes deaths, "brings back" uses them), or by an argument from this game's rules, written in
   `arguments.tsv`. Each shape is checked against the real factions (`axes.py --near`). No two shapes are the same.
   A radius that only exists by another game's rules is never a faction's base (see step 4's rule check).
4. **The mechanics list.** Each mechanic is written "I do X -> I gain from X" on this game's things (units, rows,
   columns, front cells, dots, supply per lane, carry-over, hand, discard pile), with the library concepts that catch
   its cards. For each mechanic, in this order:
   - an agent reads 8 of its real cards and fixes the concept list until it catches the right cards;
   - it is measured: the real factions built on it, the radii its cards sit on;
   - **the rule check**: it must work by this game's rules (`summary/03` to `07`). An attacked unit doesn't hit back
     (only Riposte does), so "strike first" means nothing here and is not a mechanic; who acts first is random in
     round 1 and then alternates; units are placed only in my own camp. A mechanic that needs a rule the game lacks is
     kept and marked NEW RULE.
   - **the archetype check**: the list covers every kind of play the library's concept list has, including the small
     ones: steal (take the enemy's unit or card), units that grow when they are hit and survive, my units placed in
     the enemy camp, kill spells, bringing back. A mechanic small in the library (under 30 right cards in every real
     faction, marked SMALL) can still be a faction's base; SMALL only says there are few real cards to learn from.
   Each mechanic keeps its own line; two are never merged. **Stop A: Kaptain agrees the list.**
5. **Each faction's mechanics.**
   - 2 signature mechanics: the faction builds on them. Each is a signature of one faction only. Both sit on the
     faction's radii and are joined to each other or through an extra (step 2 numbers or an argument).
   - 2-4 extras: other mechanics on several cards, chosen by fit first and partners second (`work/borrow.py`): at
     least a quarter of its cards sit on one of the faction's radii, and the library links it with a signature
     mechanic; ties go to the one with more partners. Any mechanic may be an extra, a signature of another faction
     too, but each extra is in at most 3 factions. The mechanic the faction's removal needs is kept.
   - One-offs: any card may carry a one-off from any mechanic (a faction far from bringing back may have one unit that
     comes back). One-offs are not planned here; they keep cards from being unimaginative.
   - Two factions strong on the same radius have different signatures in it ("brings back": one has "my dead units
     come back", another "my unit goes back to hand").
6. **Links between mechanics.** For every two mechanics, the library's numbers (`mechanics_wheel.py links`); agents
   read the real card pairs behind the high numbers (4 pairs first, 8 for those that come back KEEP; WEAK never counts) and keep
   only true combos (one card changes what the other does), written as a played sequence. `apart.py` gives the pairs
   real factions keep apart; a faction that holds both ends of such a pair is shown to Kaptain.
7. **Board versions.** Each faction's mechanics turned into this game's own things, from scratch: dots and front
   cells, the back row, rows, columns, lanes, the 3x3 camp, unit size, supply per lane, carry-over, round start and
   round end, one action per turn, moving, reach (melee, Pike, Ranged), strikes and fixed damage, the hand, the
   discard pile, Immobile. Sources: the library's board games first (Duelyst, Faeria, Stormbound, Into the Breach,
   Inscryption); no source = Claude's; a rule the game lacks = NEW RULE. Each faction gets 1-3 board versions and one
   faction idea. **No two factions have the same thing on the board, compared by what the card does and looks like,
   not by mechanic name**: one Egg in the whole wheel. A whole faction may be built on one board thing (all Immobile).
   The old candidates (commit d4a3de0^, `factions/3-candidates/`) are read last, only to see that no idea Kaptain
   liked is missing.
8. **Combos on this board.** Agents rate every pair of factions (190) from their board versions and mechanics, with
   step 6's KEEP combos as sources: STRONG (both halves on many cards, helps take or hold a base, the enemy's one action
   between can't easily stop it), OK (real but breakable), WEAK, NONE, AGAINST. Partners = STRONG or OK; every faction
   has 10+. A faction under 10 goes back to step 5 (other extras), then step 3. `combos.tsv` has a test column that
   playtests fill; what doesn't work in play is dropped.
9. **The seven answers** (START_DESIGN.md step 2) for all 20, made from the board versions: how it wins, how it
   removes a front unit, how it mainly removes back-row units, how it mainly acts between lanes, how it holds a base,
   its best Place effect, its blind spot. Every answer differs from every other faction's; each removal uses one of the
   faction's mechanics; a blind spot never touches a mechanic the faction has. Then the check script
   (`tools/wheel_table_check.py`) and the Stop 1 pages.

## The check script
It reads the files of steps 2-9 and checks real numbers, not only columns: every shape's joins (step 3); 2 signatures
per faction, each a signature once; extras 2-4, each in at most 3 factions; each faction's mechanics joined; 10+
partners; 1-3 board versions per faction, none the same; all seven answers present and different; removals by the
faction's own mechanics; blind spots outside its mechanics. It fails loudly; a failure is fixed, never argued away.

## What Kaptain sees at Stop 1
`factions/wheel/STOP1.md` and its parts: per faction, in plain words, its strong radii, its signatures and extras, its
board versions and faction idea, the seven answers, and its partners with the combo for each. Files in factions/ stay
under 150 lines (split them); the CLAUDE.md map names them.

## How to read the wheel
24 radii in 8 areas, measured on 43 real factions of 8 games. A value compares a faction with the average faction of
its own game (1 = average), so compare factions of different games loosely. Into the Breach, Stormbound, Slay the Spire
and Inscryption have no value on 10 or more radii. Strength, defence and the two width radii give a faction its shape;
they are not mechanics.

## Token budget
Agents use about 9 of every 10 tokens. So:
- At most 4 agents at once, each with about 20 sections; each writes its lines to its file as it goes, so a stop loses
  nothing. Before a big batch, count the sections and say how many agents it needs.
- Card-pair reads: 4 pairs first, 8 only for pairs that come back KEEP.
- Concept fixes: give the agent the counts per game in its file, so it doesn't run queries itself.
- Write the rules of a step down before doing it, and let a script check each try.

## Wrong ways, and what stops them
1. Mechanics built first from concepts, the radii left out. Stops it: steps 1-3 come before any mechanic.
2. Mechanics given to factions by judgment, no card text read. Stops it: steps 4-5, read and measured.
3. A combo guessed per pair of factions, no library behind it. Stops it: steps 6 and 8.
4. Every strong radius set to the same value, blind spots picked so the check passes. Stops it: step 3.
5. A check that checks only columns, so it passes by construction. Stops it: the check script reads numbers.
6. A mechanic copied from another game that doesn't work here ("strike first"). Stops it: step 4's rule check.
7. A basic archetype missing because it is small in the library (units that grow when hit). Stops it: step 4's
   archetype check.
8. Two factions with the same thing under different mechanic names (two Eggs). Stops it: step 7, compared by what
   the card does.
9. Answers that look only at the front cells. Stops it: step 9's back-row and between-lanes answers.
