# The wheel chat: 20 factions designed together, with their combos

Read `factions/START_DESIGN.md` and its parts 2-4 whole first, then `factions/12-mechanical-wheel.txt` (why the wheel
and its radii) and `factions/wheel/PIPELINE.md` (the commands of every step). Start with `gunzip -kf links.sqlite.gz` in
`library/cards_db`; rebuild with `PYTHONHASHSEED=0 python3 links.py` only after `network.py` or `cards.sqlite` changed
(about 7 minutes; tell Kaptain and wait for his OK, CLAUDE.md). The chat writes no cards, no stats and no code for the
game; it picks the 20 themes (step 7).

Three Bases is a game of combos: decks mix 2 factions. Every faction combines well with at least 10 others. Every
radius, mechanic and combo comes from the library, measured by script; what has no library source is marked as Claude's.
Faction text uses plain words Kaptain uses (no library names like "ping" or "overkill": say "small hits", "the rest of
the hit goes into the unit behind").

## The whole process and its stops
- Wheel chat (this file): steps 1-9. **Kaptain agrees the 20 shapes (step 3).** **Stop A: Kaptain agrees the mechanics
  list (step 4).** **Stop 1: Kaptain agrees the 20 factions (step 9).**
- One chat per faction (two can run at the same time): steps 1-6 of START_DESIGN.md (theme facts from the wheel's
  theme, then up to the ways to play).
  **Stop 2: Kaptain agrees them.** Then cards, the gate, `wheel_check.js`, the separate agent's review.
  **Stop 3: Kaptain gets the finished faction.**
- Pilot: the first two factions are a pair with a STRONG combo. Their premades play each other (`cardstats.js`), and
  one mixed deck shows whether their combo fires. **Stop 4: Kaptain decides whether the rest is built.**

## Steps 1-9, in this order
A step uses only what the steps before it made. Steps 1-3 are the wheel; the mechanics come after, found inside each
faction's radii.

1. **The radii.** The 23 radii of `factions/13-wheel-measurement.txt`, measured on 43 real factions (`axes.py`).
   A radius is a list of library concepts. Changing a list changes the values, the joins (step 2) and so the shapes
   (step 3): before changing one, tell Kaptain that the agreed shapes will be redone, and change it only on his OK.
2. **The radii that work together.** For every two radii, the library's numbers (`mechanics_wheel.py links --radii`):
   - `cards`: how much more often than chance a card of one is linked with a card of the other (1 = chance). A link
     counts only where the effects that made it belong to the two radii (the links store which effect of each card
     made them). Worked out in each game alone, then averaged, so each game counts the same: a game of 300 cards
     weighs as much as one of 2,600.
   - `decks`: how much more often real decks heavy in one hold the other (1 = as usual), also per game and averaged.
   - `links`: the linked card pairs made by the two; `level` = that count growing slowly (0 links = 0, 1 = 1, 10 = 2,
     100+ = 3).
   Two radii are joined by `cards` 1.2+ or `decks` 1.5+. "Rewards playing spells" is judged by `decks` only, because
   such a card links to every spell. Numbers only: nobody reads card pairs.
3. **The 20 factions as shapes** (`work/shapes.py`, by script). A shape is 3-6 radii a faction is strong at, with
   uneven values. Each shape is taken from one real faction: some of its radii valued 1.2+, with that faction's values,
   so every shape exists in a real game. The rules:
   - every radius is joined (step 2) to another radius of the same shape; strength, defence and "position and combos"
     only give a faction its shape and need no join;
   - at most one shape per real faction, and no two shapes the same;
   - every radius is a strength of 2-5 shapes;
   - `archetypes.tsv` lists this game's 18 kinds of play (swarm, sacrifice, bringing back, control, damage, aggro,
     scaling, grows when hit, fortress, sustain, spells, ramp, position, enemy camp, disruption, steal, cards,
     carrying), each with its radii and its mechanics. A shape carries an archetype when one of the archetype's radii
     is among its two highest values. Each shape carries at most 2 archetypes and each archetype is carried by 2-3
     shapes, so every kind of play has factions and none is crowded;
   - within these rules, the shapes are as different from each other as possible;
   Output: `work/shapes.tsv`. **Kaptain agrees the 20 shapes.**
4. **The mechanics list** (`mechanics.tsv`, 53 mechanics). Each mechanic is written "I do X -> I gain from X" on this game's things (units, rows,
   columns, front cells, dots, supply per lane, carry-over, hand, discard pile), with the library concepts that catch
   its cards. The list starts from all the library's concepts, not from the archetypes, in this order:
   - `work/concept_catch.py` (run from `library/cards_db`) finds every concept with real cards that is in no mechanic
     and where its cards land (`work/concept_sort.tsv`). A concept is caught by a mechanic or radius that holds half its
     cards (each game counts the same). Strength and defence catch nothing; "many cheap units" and "a few big units"
     catch only by what cards do, not by their cost.
   - Claude decides every concept caught nowhere, and every catch by chance (its cards share another effect), in
     `work/concept_verdicts.tsv`, marked as Claude's: trigger or condition; not in this game; one of the game's own
     things; ruled out by Kaptain; a possibility for cards; spread over several mechanics; add to mechanic X; candidate
     mechanic. Kaptain agrees the additions and candidates.
   - An addition or a candidate is read and checked like every mechanic (below), then joins the list or gets its reason.
   For each mechanic, in this order:
   - an agent reads 8 of its real cards, each with the meaning of its keywords (`library/cards_db/vocab.tsv`: Provoke also
     stops nearby enemies moving), and fixes the concept list until it catches the right cards;
   - it is measured: the real factions built on it, the radii its cards sit on;
   - **the rule check**: it must work by this game's rules (`summary/03` to `07`). An attacked unit doesn't hit back
     (only Riposte does), so "strike first" means nothing here and is not a mechanic; who acts first is random in
     round 1 and then alternates; units are placed only in my own camp. A mechanic that needs a rule the game lacks is
     kept and marked NEW RULE.
   - **the archetype check**: every mechanic belongs to an archetype of `archetypes.tsv`, and every archetype has its
     mechanics, including the small ones: steal (take the enemy's unit or card), units that grow when they are hit and
     survive, my units placed in the enemy camp, kill spells, bringing back. Damage over time and my units changing
     form are possibilities for cards, not mechanics. A mechanic small in the library (under 30 right cards in every real
     faction, marked SMALL) can still be a faction's base; SMALL only says there are few real cards to learn from.
   Each mechanic keeps its own line; two are never merged. **Stop A: Kaptain agrees the list.**
5. **Each faction's mechanics.** All 20 factions get their mechanics at once, from one algorithm that finds the best
   whole: the best fit of every faction's mechanics to its radii and archetypes, together with how strongly its
   mechanics work together, by the library's numbers (step 6's `cards`: linked more often than chance; `decks`: real
   decks heavy in one hold the other). No faction is filled first and none is fixed by hand, except G (hurt and selfhurt).
   - 2 signature mechanics: the faction builds on them. Each is a signature of one faction only. Both sit on the
     faction's radii and are joined to each other or through an extra (step 2 numbers or an argument).
   - 2-4 extras: other mechanics on several cards. At least a quarter of an extra's cards sit on one of the faction's
     radii, and the library links it with a signature mechanic. Any mechanic may be an extra, a signature of another
     faction too, but each extra is in at most 3 factions. The mechanic the faction's removal needs is kept.
   - Archetypes: at least one signature is a mechanic of an archetype the faction carries, and every archetype it
     carries has a mechanic among its signatures and extras.
   - One-offs: any card may carry a one-off from any mechanic (a faction far from bringing back may have one unit that
     comes back). One-offs are not planned here; they keep cards from being unimaginative.
   - Every mechanic of the list is a signature or an extra of at least one faction (Kaptain, 16 Nov 2026).
   - Two factions strong on the same radius have different signatures in it ("brings back": one has "my dead units
     come back", another "my unit goes back to hand").
6. **Links between mechanics.** For every two mechanics, the library's numbers (`mechanics_wheel.py links`), by script
   only. Nobody reads card pairs here (Kaptain, 15 Nov 2026): the database already holds what each card does, and
   whether two factions really make a combo on this board is judged once, in step 8 ("links" are between mechanics,
   "combos" between factions). `apart.py` gives the pairs
   real factions keep apart; a faction that holds both ends of such a pair is shown to Kaptain.
7. **Theme, then tools.** First each faction gets a real theme (START_DESIGN.md step 1: World War I artillery, the
   Zulu regiments), picked for its mechanics; the 20 themes all differ. The theme is a source of tools, never a reason
   for one: a tool that fits the story but grows from none of the faction's mechanics is dropped, and the theme never
   lets one mechanic take all the tools. Then each faction gets 2-4 tools: a tool is a new kind of thing or rule that makes the faction's plan happen
   on this game's own things (dots and front cells, the back row, rows, columns, lanes, the 3x3 camp, unit size,
   supply per lane, carry-over, round start and round end, one action per turn, moving, reach, strikes and fixed
   damage, the hand, the discard pile, Immobile), carried by many of its cards. Examples (Claude's): eggs (my dead unit
   leaves an egg in its cell that turns back into it at round end), trophies (the first time each round I kill a marked enemy, I get a card),
   edicts (a lasting rule on a lane), graves, debts, banners, oaths, tunnels, hostages, echoes; examples only, each
   kind of tool once in the wheel. Countdowns very sparingly; a lane never holds more than 12 supply. Each tool:
   - names the mechanic it grows from; each signature has a tool; an extra joins a tool or sits only on cards;
   - feeds at least one other tool (one makes what the other uses): faction A's eggs keep the front cell after a
     death, and its departures make the touching allies strike when a unit leaves; take one away and the other loses
     part of its point;
   - is played out cell by cell before it is written: which cell, what happens there, what the enemy does with its
     one action in between; two tools that need the same cell clash.
   The tools together are the faction idea, and the seven answers (step 9) are built from them, not from how it wins
   alone. A faction holds together because its tools feed each other, never because one idea is on every card (Mark,
   Projectiles, back-in-time are one tool at most). Sources: the library's board games first (Duelyst, Faeria,
   Stormbound, Into the Breach, Inscryption) and real things that act on their own (Slay the Spire's orbs: placed in
   slots, each acts every turn); no source = Claude's; a rule the game lacks = NEW RULE. **No two factions have the
   same tool doing the same job, compared by what the card does and looks like, not by mechanic name**: one Egg in
   the whole wheel. A whole faction may stand on one board thing (all Immobile). Written to `factions/wheel/themes.tsv`
   (faction, theme) and `factions/wheel/tools.tsv` (faction, tool, mechanic, the tools it feeds, the cell-by-cell line,
   source: a library card or CLAUDE, NEW RULE).
   The old candidates (commit d4a3de0^, `factions/3-candidates/`) are read last, only to see that no idea Kaptain
   liked is missing.
8. **Combos on this board.** Agents rate every pair of factions (190) from their tools and mechanics, with
   step 6's numbers as sources: STRONG (both halves on many cards, helps take or hold a base, the enemy's one action
   between can't easily stop it), OK (real but breakable), WEAK, NONE, AGAINST. Partners = STRONG or OK; every faction
   has 10+. A faction under 10 goes back to step 5 (other extras), then step 3, and steps 6-8 are redone for it. `combos.tsv` has a test column that
   playtests fill; what doesn't work in play is dropped.
9. **The seven answers** (START_DESIGN.md step 2) for all 20, made from the tools: how it wins, how it
   removes a front unit, how it mainly removes back-row units, how it mainly acts between lanes, how it holds a base,
   its best Place effect, its blind spot. Every answer differs from every other faction's; each removal uses one of the
   faction's mechanics; a blind spot never touches a mechanic the faction has. Then the check script
   (`tools/wheel_table_check.py`) and the Stop 1 pages.

## The check script
It reads the files of steps 2-9 and checks real numbers, not only columns: every shape's joins (step 3); 2 signatures
per faction, each a signature once; extras 2-4, each in at most 3 factions; each faction's mechanics joined; 10+
partners; a theme per faction, all different; 2-4 tools per faction, each naming its mechanic and feeding another,
every signature with a tool, none the same; all seven answers present and different; removals by the
faction's own mechanics; blind spots outside its mechanics. It fails loudly; a failure is fixed, never argued away. It fails until step 7 writes `themes.tsv` and `tools.tsv`.

## What Kaptain sees at Stop 1
`factions/wheel/STOP1.md` and its parts: per faction, in plain words, its strong radii, its signatures and extras, its
theme, its tools and how they feed each other, the seven answers, and its partners with the combo for each. Files in factions/ stay
under 150 lines (split them); the CLAUDE.md map names them.

## How to read the wheel
23 radii in 8 areas, measured on 43 real factions of 8 games (Duelyst, Faeria, Gwent, Inscryption, Into the Breach,
Runeterra, Stormbound, Slay the Spire; Marvel Snap has no factions, Monster Train is left out). A value compares a faction with the average faction of
its own game (1 = average), so compare factions of different games loosely. Into the Breach, Stormbound, Slay the Spire
and Inscryption have no value on 10 or more radii. Strength, defence and the two width radii give a faction its shape;
they are not mechanics.

## Token budget
Agents use about 9 of every 10 tokens. So:
- At most 4 agents at once, each with about 20 sections; each writes its lines to its file as it goes, so a stop loses
  nothing. Before a big batch, count the sections and tell Kaptain how many agents it needs and their cost (about
  110k tokens each), and wait for his OK.
- No agent reads what the database already holds; judgment happens once per question (step 8 for combos).
- Concept fixes: give the agent the counts per game in its file, so it doesn't run queries itself.
- Write the rules of a step down before doing it, and let a script check each try.

## Wrong ways, and what stops them
1. Mechanics built first from concepts, the radii left out. Stops it: steps 1-3 come before any mechanic.
2. Mechanics given to factions by judgment. Stops it: step 4 (read and measured, agreed at Stop A) and step 5 (by
   script).
3. A combo guessed per pair of factions, no library behind it. Stops it: steps 6 and 8.
4. Every strong radius set to the same value, blind spots picked so the check passes. Stops it: step 3.
5. A check that checks only columns, so it passes by construction. Stops it: the check script reads numbers.
6. A mechanic copied from another game that doesn't work here ("strike first"). Stops it: step 4's rule check.
7. A basic archetype missing because it is small in the library (units that grow when hit). Stops it: step 4's
   archetype check.
8. Two factions with the same thing under different mechanic names (two Eggs). Stops it: step 7, compared by what
   the card does.
9. Answers that look only at the front cells. Stops it: step 9's back-row and between-lanes answers.
10. A faction that is one idea on every card (all marks, all echoes). Stops it: step 7, tools that feed each other.
11. A theme that brings tools no mechanic has. Stops it: step 7, every tool names its mechanic.
