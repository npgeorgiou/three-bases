# The wheel chat: 20 factions designed together, with their combos

Read `factions/START_DESIGN.md` and its parts 2-4 whole first, then `factions/wheel/HANDOFF.md` (which step is next,
Kaptain's standing decisions) and this file. Commands of every step: `factions/wheel/PIPELINE.md`. Library commands run
from `library/cards_db/`; first `gunzip -kf links.sqlite.gz` there. The wheel writes no cards, no stats and no game code.

Three Bases is a game of combos: decks mix 2 factions, and every faction combines well with at least 10 others. Every
number comes from the library by script; anything with no library source is marked as Claude's. Faction text uses plain
words Kaptain uses ("small hits", "the rest of the hit goes into the unit behind"), never library names.

## The words
- **Concept**: a tag the library gives a card's effect ("revive": a unit comes back; "attack_gain": gains strength).
- **Card link**: two real cards of one game where an effect of one sets off or feeds an effect of the other
  (`links.sqlite`). Each link keeps which effect of each card made it, so it counts only for those effects' concepts.
- **Radius**: a list of concepts that measures what real factions are strong at (23 radii, `axes.py` `SPOKES`).
- **Shape**: one faction's 3-6 strong radii with their values, taken from one real faction.
- **Kind of play** (`wheel/archetypes.tsv`): swarm, sacrifice, bringing back... each with its radii and concepts.
- **Group**: the concepts a faction builds on: 2 pillars and 2-4 others.
- **Mechanic**: a link between two concepts of a group, shown by real card pairs, with the text of the link: "makes
  your units die: the other card brings them back (2,328 pairs)". A mechanic is never written by hand.

## Rules for every step (Kaptain)
- Every game counts the same in every number: worked out in each game alone, then averaged. A combo is judged by how
  much more often than chance its cards link, never by its raw size; the count of pairs only breaks ties.
- A concept needs 10+ real cards in the library (all games together).
- Scripts, no reading agents. Card texts are read only where a card's rows can't answer: at most 500 cards for the
  whole wheel, by a low-cost model; count them and get Kaptain's OK first.
- A concept that means two things in different games is a library error: it is split in the library, with test
  cases, never limited to some games in a list.
- A radius is a list of concepts; changing one changes the values, the joins and so the shapes. Tell Kaptain first
  that the agreed shapes will be redone, and change it only on his OK.
- One chat does one step and ends by marking that step done in `wheel/HANDOFF.md`. Docs are rewritten when the
  process changes, never added to.

## The stops
- **Kaptain agrees the 20 shapes** (step 3). **Kaptain agrees the 20 groups** (step 6). **Stop 1: Kaptain agrees the 20
  factions** (step 9).
- Then one chat per faction (two can run at once): steps 1-6 of `START_DESIGN.md`. **Stop 2: Kaptain agrees them.**
  Then cards, the gate, `wheel_check.js`, a separate agent's review. **Stop 3: Kaptain gets the finished faction.**
- Pilot: the first two factions are a pair with a STRONG combo; their premades play each other (`cardstats.js`) and
  one mixed deck shows whether the combo fires. **Stop 4: Kaptain decides whether the rest is built.**

## Steps 1-9, in this order (each uses only what the steps before made)
1. **Fix the library's concepts.** The suspects: every concept counted only in some games
   (`wheel/work/suspects.tsv`, with the games left out), and every concept whose cards link to quite different
   concepts in one game than in the others (by script). For each: if its cards in the games left out do something
   else, split the concept by what the rows already say (on a unit on the board or on a card in hand; on an enemy or
   on my own unit; on the player or on a unit; the main supply or a side resource), by a fix script with test cases
   (`library/cards_db/START_DATABASE.md`); if it is the same, the limit goes. A game whose player is a unit on the
   board (Duelyst's General; a rule in its `game_rules.jsonl`) gives its player rows both concepts. Rows that can't
   tell: read, within the 500. Then the radius lists lose their game limits, and so does every game list in `axes.py`
   that decides whether a concept counts (each concept in one is a suspect too); cases: `CARD_CASES` in `axes.py`.
   `links.py` is rebuilt (about 7 minutes, Kaptain's OK first). Decided by Kaptain and done here: "doubles a stat" on my own unit joins the radius
   "grows strength"; "can't act" and "can't attack" stay two concepts ("can't act" is the wider one).
2. **The radii and how they work together.** `axes.py` measures the 43 real factions on the 23 radii (1 = the average
   faction of its game). For every two radii (`mechanics_wheel.py links --radii`): `cards` = how much more often than
   chance their cards are linked; `decks` = how much more often real decks heavy in one hold the other; `links` = the
   linked pairs; `level` = that count growing slowly (0, 1, 10, 100+ pairs = 0-3). Joined: `cards` 1.2+ or `decks`
   1.5+; "rewards playing spells" by `decks` only (such a card links to every spell).
3. **The 20 shapes** (`work/shapes.py`). Each shape is 3-6 radii of one real faction valued 1.2+, with its values.
   Every radius in a shape is joined to another of the same shape (strength, defence and "position and combos" need no
   join); at most one shape per real faction, no two alike; every radius a strength of 2-5 shapes; a shape carries a
   kind of play when one of its radii is among the shape's two highest; each shape carries at most 2, each kind of play
   is carried by 2-3 shapes; within that, the shapes are as different as possible. Check by script that every kind of
   play's concepts sit on its radii, and that every shape's highest radius gives it a kind of play.
   **Kaptain agrees the 20 shapes.**
4. **The usable concepts** (`work/concept_catch.py` -> `work/concepts.tsv`). Every concept with 10+ real cards, with
   its card count and the share of its cards on each radius. Left out, each with its reason (Claude's, in
   `work/concept_verdicts.tsv`): it says when or if a card acts (on play, turn end); it is not in this game (player
   health, blocking, answers on the enemy's turn, unit types, shops); it is one of the game's own things (lanes, the
   3x3 camp, carry-over, bases); Kaptain ruled it out (randomness, my units changing form, countdowns); every card does it (choosing the target);
   it is a possibility for single cards (a wall that can't attack); or it is a parent whose children carry its cards
   ("buff" when "attack_gain" carries them), so no effect counts twice.
5. **The links between concepts** (`mechanics_wheel.py`, concept mode -> `wheel/concept_links.tsv`). For every two
   usable concepts, by the same count as step 2: `cards`, `decks`, `links`, `level`; which one makes and which one uses
   (the side of the link); the most common link texts. A game counts for `cards` when chance alone gives it 5+ linked
   pairs. Joined: `cards` 1.2+, or `decks` 1.5+, or, where chance stays under 5 pairs in every game, 3+ real pairs at
   3+ times chance. `apart.py` lists the concept pairs real factions keep apart.
6. **The 20 groups** (one exact solver for all 20 at once, `work/groups.py` -> `work/groups.tsv`).
   - Fit of a concept to a faction = sum over the faction's radii of (radius value x share of the concept's cards on
     that radius); a concept needs a quarter of its cards on one of the faction's radii.
   - A group: 2 pillars joined to each other directly, plus 2-4 others; every concept joined (step 5) to another of
     the group; every concept that uses something has a concept in the group that makes it.
   - A pillar belongs to one faction only; another concept is in at most 3 factions; every usable concept with joins
     is in at least one group (those that fit nowhere are shown to Kaptain, not forced in).
   - Every kind of play the shape carries has a concept in the group, and one pillar belongs to one of them.
   - Score: the strength of the joins inside each group plus the fit, summed over all 20. Fixed by Kaptain: G =
     grows when hurt + I damage my own units.
   - A group holding both ends of a pair real factions keep apart (`apart.py`) is shown to Kaptain.
   - Kaptain sees per faction: its concepts in plain words, and its mechanics (each joined pair: the real link text
     and its count); one sentence per faction, written from those texts. `tools/wheel_table_check.py` checks every
     rule above from the files. **Kaptain agrees the 20 groups.**
7. **Theme, then tools.** First each faction gets a real theme (World War I artillery, the Zulu regiments) picked for
   its group; the 20 themes all differ; the theme is a source of tools, never a reason for one. Then 2-4 tools per
   faction: a tool is a new kind of thing or rule that makes the group's mechanics happen on this game's own things
   (dots and front cells, rows, columns, lanes, the 3x3 camp, unit size, supply per lane, carry-over, round start and
   end, one action per turn, moving, reach, strikes and fixed damage, the hand, the discard pile, Immobile), carried by
   many of its cards. Each tool names the mechanic it grows from; each pillar has a tool; each tool feeds another (one
   makes what the other uses); each is played out cell by cell (which cell, what happens, what the enemy does with his
   one action between; two tools needing the same cell clash). The linked card pairs of the mechanic are its source
   cards. No two factions have the same tool doing the same job, compared by what the card does: one Egg in the whole
   wheel. Countdowns very sparingly; a lane never holds more than 12 supply. A rule the game lacks is marked NEW RULE.
   Written to `wheel/themes.tsv` and `wheel/tools.tsv`. The old candidates (commit d4a3de0^, `factions/3-candidates/`)
   are read last, only to see that no idea Kaptain liked is missing.
8. **Combos on this board.** For every pair of factions (190), the joins between the concepts of one group and the
   other's (step 5 numbers), by script. Claude rates each pair with numbers on the board, from the two factions'
   tools: STRONG (both halves on many cards, helps take or hold a base, the enemy's one action between can't easily
   stop it), OK (real but breakable), WEAK, NONE, AGAINST. Partners = STRONG or OK; every faction has 10+; one under 10
   goes back to step 6. `wheel/combos.tsv` has a test column that playtests fill.
9. **The seven answers** for all 20, made from the tools: how it wins, how it removes a front unit, how it mainly
   removes back-row units, how it mainly acts between lanes, how it holds a base, its best Place effect, its blind spot.
   Every answer differs from every other faction's; each removal uses one of its mechanics; a blind spot never touches
   its group. Then `tools/wheel_table_check.py` and the Stop 1 pages (`work/make_stop1.py` -> `wheel/STOP1*.md`:
   per faction its radii, group and mechanics, theme, tools and how they feed each other, the seven answers, and one
   line per partner saying how the combo plays). Files under 150 lines.

## How to read the radii
Values compare a faction with the average faction of its own game (1 = average), so compare factions of different games
loosely. Into the Breach, Stormbound, Slay the Spire and Inscryption have no value on 9 or more radii. Strength, defence
and the two width radii give a faction its shape; they are not plans.
