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
- **Archetype** (faction archetype): a way to play that decks of 2+ games lean on, found by NMF (step 3); real
  factions are never copied, only measured against it. None is tied to one game's card types, resources, keywords or multiplayer. One
  archetype can be played with different concepts, so it is made of parts, each a set of alternative concepts that can do
  it. A part is an **engine** (it works through links with another part: "my units die" -> "my units gain when an ally
  dies") or a **brick** (it works alone and links to nothing: disruption, removal).
- **Deck archetype**: what one deck tries to do, from Kaptain's list (`wheel/archetypes_kaptain.txt`: Madness, Storm,
  Reanimator...). A deck mixes 2 factions, so a deck archetype is played by a pair of factions (step 7), never by one.
- **The faction's archetypes**: the 2 archetypes a faction plays (step 6).
- **The faction's concepts**: the 1 or 2 concepts it plays from each part of its archetypes (step 6). They are its
  character (what it is strongest at, what its keywords grow from); the other concepts of those parts are not its own.
- **The faction's list**: every concept of the library (usable, helpers and out) except the faction's concepts, each
  with its score for how strongly it links with them.
- **Helper**: a concept that only says when or how a card acts, one of the game's own things, or a thing for single
  cards (step 2). Never a part of an archetype; always on the faction's list.
- **Strong link**: two concepts joined by the step 4 rule through real card pairs: `cards` 1.2+, or `rare` 3+ with a
  `level` of 1+. A pair joined only by real decks is not a strong link.
- **Synergy**: a strong link between two of the faction's concepts, shown by real card pairs, never written by hand:
  "makes your units die: the other card brings them back (in 7 of 10 games, 3.1 times chance)".
- **Extras**: the concepts of a faction's list that step 6 gives it besides its own concepts.
- **Keyword** (in industry words, a mechanic): a word on many cards that stands for one rule (Magic's Exploit,
  Hearthstone's Overload).
- **The seven answers**: how a faction wins, removes a front unit, MAINLY removes back-row units, MAINLY acts between
  lanes, holds a base, which of the game's own things it cares about most, its blind spot (what none of its concepts
  and extras give: "never draws cards"). Removing: the enemy unit
  leaves its cell (it dies, goes back to hand, is banished, pushed away, taken or turned into a cocoon). Holding: the
  enemy unit stays, but the base stays mine (my units survive or come back, his units are frozen, his cells filled,
  his cards cost more).

## Rules for every step (Kaptain)
- Every game counts the same in every number: worked out in each game alone, then averaged. Games with no factions
  (Marvel Snap, Inscryption, Into the Breach, Slay the Spire, Monster Train) count in every number about concepts and
  their links.
- How well two things link is judged by how much more often than chance real cards link them, worked out per game;
  ties are broken by how many games show it. The linked pairs themselves count only as a level that grows slowly
  (`level`: 1 pair = 1, 10 = 2, 100 or more = 3), so a big game cannot drown the others and a pairing rare in the ten
  games is never lost.
- A concept needs 5+ real cards in the library (all games together).
- Scripts, no reading agents. Card texts are read only where a card's rows can't answer: at most 500 cards for the
  whole wheel, by a low-cost model; count them and get Kaptain's OK first.
- What belongs together in an archetype is decided by what decks play together, never by card links
  alone: a brick (removal, protection) links to nothing and still belongs. Links decide only engine or brick.
- A card's concept is judged with the rules of its keywords, not its printed text alone (Monster Train's Offering plays
  the card for free when it is discarded), and with the rows that gave it the concept.
- A concept that means two things in different games is a library error: it is split in the library, with test cases,
  never limited to some games in a list.

## The stops
- **Kaptain agrees the faction archetypes** (step 3) and **the 20 factions' archetypes** (step 6). **Stop 1: Kaptain
  agrees the 20 factions** (step 9).
- Then one chat per faction (two can run at once): steps 1-6 of `START_DESIGN.md`. **Stop 2: Kaptain agrees them.**
  Then cards, the gate, the faction check (the cards against the faction's archetypes and
  extras), a separate agent's review. **Stop 3: Kaptain gets the finished faction.**
- Pilot: the first two factions are a pair with a STRONG combo; their premades play each other (`cardstats.js`) and
  one mixed deck shows whether the combo fires. **Stop 4: Kaptain decides whether the rest is built.**

## Steps 1-9, in this order (each uses only what the steps before made)
1. **Fix the library's concepts.** The suspects: every concept counted only in some games (`wheel/work/suspects.tsv`),
   and every concept whose cards link to quite different concepts in one game than in the others (by script). For
   each: if its cards in the other games do something else, split the concept by what the rows already say (on a unit
   on the board or on a card in hand; on an enemy or on my own unit; on the player or on a unit; the main supply or a
   side resource), by a fix script with test cases (`library/cards_db/START_DATABASE.md`); if it is the same, no game
   limit. A game whose player is a unit on the board (Duelyst's General; a rule in its `game_rules.jsonl`) gives its
   player rows both concepts. Rows that can't tell: read, within the 500. A concept that only says what kind of record
   a card is (an "ability" record) is a library error and is removed. A rule of a game that no card text says
   (Runeterra: up to 3 unspent mana is kept as spell mana) is a record in its `game_rules.jsonl`, with its source, on
   the cards it concerns.
   Then the tags of every usable concept. A script groups each concept's cards by what put the tag on them (the row's
   action or test, whose side, when it fires, from where; or the general rule and the row that set it off) and marks a
   group suspect when it acts on the wrong side (it helps the enemy) or matches what the concept's definition gives to
   another concept ("counts what is on the board now" is "Counts / thresholds", not "Grows with what happened this
   game"). Kaptain sees how many cards that means first. A low-cost model reads 5 cards of each suspect family (one concept, one action or test, one reason; spread over
   the games), given the
   card's text, its keywords' rules from its game, the cards it names or makes, the rows that gave the tag and the
   concept's definition with the concepts it is not; per card it answers right, wrong (should be X) or unsure, with one
   line why. 4 or 5 wrong the same way: the group is fixed by one rule for all its cards, with test cases. 4 or 5
   right: it stays. Mixed: the script splits the group by one more detail and 5 cards of each half are read (the 4 of 5
   is Claude's). "Return my unit to hand" is split into smaller concepts by what its rows say (from the board, when it
   dies or leaves play, from the discard pile), and the reading gives the rows that lack whose unit or from where.
   Then `check_all.py` (about 14 minutes) and `links.py` (about 6) are rebuilt, Kaptain's OK first.
2. **The usable concepts** (`work/concept_catch.py` -> `work/concepts.tsv`, `work/concepts.md`). Every concept with
   5+ real cards, with its card count (`card_count`) and its games, sorted into three kinds
   (`work/concept_verdicts.tsv`: kind and reason, each marked Kaptain's or Claude's; a concept not in it is usable):
   - Usable: a faction can build on it. It says what a card does ("brings back a dead unit"), or reacts to something
     other cards make happen or build up ("when a card is drawn", "when another unit dies", "if your hand holds 5
     cards"). Where cards are placed and what they stand next to (neighbours, formations, position, long reach),
     auras, attaching, stacking counters, bonuses for this turn, expensive cards and my units that can't attack are
     usable too (Kaptain).
   - Helper: it only says when or how a card acts: every "when" about the card itself ("when played", "when it dies",
     "when it leaves play", "when it attacks", "when it is damaged", "when it becomes a target"; the effect after it
     counts by its own concept), "at end of round", "once per game", "choose one of two effects"; or it is one of the
     game's own things (lanes, bases, carry-over, rows); or it is a thing for single cards (used once, a drawback,
     choosing the target).
   - Out: it is not in this game (player health, blocking, answers on the enemy's turn, unit types, shops, supply that
     grows by itself) or Kaptain ruled it out (randomness).
   A parent in the concept tree keeps only the cards none of its children carry, so no effect counts twice.
   `work/concepts.md` shows the kinds in plain words for Kaptain.
3. **The faction archetypes** (`work/deck_groups_nmf.py` -> `work/deck_groups_nmf.tsv`, `.md`, `.json`).
   The ways to play that decks lean on; they become our factions' archetypes. Real factions are never copied.
   1. Concepts: the usable concepts (step 2); a card counts each concept once (Claude's). Five unit concepts are added,
      each against the card's game: unit, cheap unit, expensive unit, strong for its cost, tough for its cost (above
      the game's straight line of strength or defence by cost, Claude's).
   2. Scores: every deck of `decks.tsv` (the whole deck, all its cards, neutrals and staples too, never split by
      faction) and every real faction (43; Monster Train's clans are not measured), per concept: the log-odds ratio with a prior (Monroe et al.
      2008) against all the cards of its game (Claude's), as a z-score; above 1.96 the deck leans on it. Deck cards the
      library does not know are counted and reported, never guessed. Monster Train and Marvel Snap decks are in
      (Claude's).
   3. Groups: NMF on the deck rows only, with the positive scores; each game weighs the square root of its deck count. The first guess comes from the data (NNDSVD), so one run gives the
      result. The number of groups, from 14 (20 factions of 2 archetypes, each in at most 3 factions) to 30 (Claude's),
      is the one whose groups stay most alike when the run is repeated on 90% of the decks, 10 times (Claude's). A deck
      fits a group that is at least 30% of its mix (Claude's). The wheel's archetypes are the version with 25 groups
      (`--groups 25`, the most stable number above 20, Claude's; Kaptain agreed them, 19 Nov 2026).
   4. Per group: its 10 heaviest concepts, each with the share of its decks that lean on it; its base concepts (more
      than half of its decks have them, more often than their game's decks, Claude's), like "Deal damage"; its unit
      numbers against their games; a group whose decks are 80% or more from one game is marked (Claude's).
   5. The real factions are never rows of the NMF. A faction fits its best 2 groups when its share of their concepts
      is at least twice its game's average (Claude's). The groups no faction fits, the factions that fit no group and
      the concepts in no group are listed.
   `work/make_faction.py "<concept>" ["<concept>"]` makes a faction from one or
   two concepts out of the 25 groups (its header says how). The page `factions/wheel-groups.html` is made
   in its own chat: concept nodes placed by how often decks use them together, coloured by group; selecting a faction
   or a deck lights its concepts; building or changing a group by selecting nodes shows which decks and factions fit it.
4. **The links between concepts** (`mechanics_wheel.py links --concepts` -> `wheel/concept_links.tsv`). For every two
   concepts of `work/concepts.tsv` (usable, helpers and out): `cards` = how much more often than chance their cards are
   linked, counted only through what of each card made the link; `decks` = how much more often real decks heavy in one
   hold the other; `games` = in how many games real cards link them; `level` = the linked pairs as the slow level; `rare` for a pair chance gives under 5 linked pairs in every game (all linked pairs over all chance);
   `makes` (the share of the pair's links where a's card sets off or feeds b's card); the three most common link
   texts. Joined: `cards` 1.2+, or `decks` 1.5+, or `rare` 3+ with a `level` of 1+. `apart.py` lists the concept pairs
   real factions keep apart.
5. **The archetype map** (`work/archetype_map.py` -> `work/archetype_parts.tsv`, `work/archetype_map.tsv` and
   `factions/wheel-archetypes.html`), from the 25 groups of step 3 (`work/step3_groups.py`); each concept of a group is a
   part of its own (Claude's), and the parts with their kind go to `work/archetype_parts.tsv` for step 6.
   Each concept of an archetype's parts is a node; a concept used by several archetypes is one node. A part whose
   concepts have strong links with another part of the same archetype is an engine; any other part is a brick. Between the
   concepts of two engine parts of an archetype, an edge with the step 4 numbers: `cards` (how much more often than
   chance real cards link them), `games`, `level`, the top link text and one real card pair. An edge is marked weak when
   more than half of its card links are about hitting the player (no player health here), or when only real decks join
   it (no card pair) (the half is Claude's). Bricks are nodes with no edges. Two engine parts whose concepts real cards never link are shown to Kaptain with the numbers. On the page
   every usable concept sits at a fixed place, laid out once from all real links between concepts (concepts real cards
   often link sit close); Kaptain ticks one or more archetypes to light their concepts and edges, and between ticked
   archetypes the page draws every real link from a concept of one to a concept of another (any part), to see whether
   archetypes fit together in one faction.
6. **The 20 factions** (by script, from the archetype map and `wheel/concept_links.tsv`; `work/factions.py` ->
   `work/factions.tsv`, and `work/concept_list.py` -> `work/lists/<letter>.tsv`). Every tie in this step is broken by
   the archetype or concept key in alphabetical order, so every run gives the same result. In this order:
   1. **The archetypes.** A group of 2 archetypes scores the strong links between concepts of one archetype and
      concepts of the other, divided by the number of different concepts in the group (so a big archetype does not
      win by its size). The 20 groups are
      picked so the weakest faction is as strong as possible: start from the 20 best groups that keep the limits, then
      swap one group for another while that lifts the weakest score, until no swap does. Limits: no archetype in more
      than 3 factions; no two factions play the same 2 archetypes; two factions share at most half of their own
      concepts (6.2). An archetype may stay unused.
      **Kaptain agrees the 20 factions' archetypes**, seeing per faction its archetypes in plain words, its concepts
      and why each was picked (its strong links into the other parts), its synergies (the real link text, times chance, games) and one sentence written from those texts.
   2. **Its concepts.** From each engine part of its archetypes, the concept with the most strong links into the other
      engine parts of its archetypes (ties: the higher sum of `cards`, then more games), and the second best when it
      has at least half as many; from each brick, the concept with the highest score on the faction's list made from
      its engine concepts. Example: Reanimator plays "sacrifice my units" and "bring dead units back", which real cards
      link, not all 11 concepts of its two parts.
   3. **A real theme** (World War I artillery, the Zulu regiments), written for its archetypes; the 20 themes all
      differ. The theme only breaks ties between concepts that score within 0.1 of each other.
   4. **Its list**: every concept with 5+ cards (usable, helpers and out) except its own concepts, each with its score.
      In each game alone: real links between the concept's instances and the instances of the faction's concepts,
      against the links chance alone gives there; the game's score = (real + 1) / (chance + 1); the score = the
      average over the games where the concept and the faction's concepts both appear (every game weighs the same).
      Beside it: the `level` and in how many games.
   5. **Its extras**, the same number for every faction: 20 minus the most concepts any faction plays, at least 8 and at
      most 12 (a real faction of about 100 cards mostly uses about 20 concepts). Picked from its list in this order:
      (a) each of the four answers about the board (removing a front unit, removing back-row units, acting between
      lanes, holding a base) that its concepts don't give gets the highest-scoring way that gives it in
      `work/answer_concepts.tsv` (agreed with Kaptain: per answer its ways, each one concept, two concepts real cards
      link, or a removal on a spell; a way of two concepts takes two extras); (b) the rest go to the highest-scoring
      concepts with strong links to at least 2 of its concepts; (c) the theme breaks ties.
   6. **Its answers**, from `work/answer_concepts.tsv`: how it wins is the line of its archetypes in
      `work/archetype_parts.tsv`; removing a front unit, removing back-row units, acting between lanes and holding a base are
      each the highest-scoring way its concepts and extras give; what it cares about most is the highest-scoring of
      the game's own things on its list (factions may share it); its blind spot is named at step 9. An answer no way gives is
      fixed first in (5) with another extra; only when its list has no way for it does the faction go back to (1).
7. **Combos on this board.** For every pair of factions (190), the joins between the two factions' concepts (their own
   concepts and extras; step 4 numbers), by script. Claude rates each pair with numbers on the board: STRONG (both halves on many
   cards, helps take or hold a base, the enemy's one action between can't easily stop it), OK (real but breakable),
   WEAK, NONE, AGAINST. Partners = STRONG or OK; every faction has 7+; one under 7 goes back to step 6. For every
   pair the script also lists the deck archetypes (`wheel/deck_archetypes.tsv`: the parts of those of
   `wheel/archetypes_kaptain.txt` that can exist here, and the concepts that can do each) the two factions' concepts can play
   together (one discards, the other gains from discards: Madness); the 190 pairs should cover many of them.
   `wheel/combos.tsv` has a test column that playtests fill.
8. **Game plan, then keywords** (`wheel/plans.tsv`, `wheel/keywords.tsv`).
   1. Each faction's game plan: how it takes and holds 2 bases over a few turns with its synergies, walked through on
      the board (which cell, what happens, what the enemy does with his one action between).
   2. The keywords of all 20 factions are made together, as one pool, on this game's own things (dots and front cells,
      rows, columns, lanes, the 3x3 camp, unit size, supply per lane, carry-over, round start and end, one action per
      turn, moving, reach, strikes and fixed damage, the hand, the discard pile, Immobile). Each grows from a synergy
      and names the real card pairs of that synergy (2+ games) as its sources.
   3. Keywords are shared: one built on a synergy several factions have is on all of them, a lot on those that
      obviously gain from it, a little on the others; none is barred from any faction. Where it can, one faction makes
      what a keyword needs and a partner gains from it. Every faction has at least 1 keyword of its own, from a synergy
      only it has.
   4. A script checks: every faction has a keyword of its own; no shared keyword is on one faction only; every keyword
      uses only concepts of the factions that carry it. A lane never holds more than 12 supply. A rule the game lacks is marked NEW RULE.
   5. Before all 20: on one faction, each new keyword carries 12+ different cards (cost 1 to 6, never the same card
      with other numbers); Kaptain judges.
9. **Stop 1** for all 20: the seven answers made final from the game plan and keywords (every answer but which of the
   game's own things it cares about most differs from every other faction's; the blind spot is named from what none of
   its concepts and extras give, "never draws cards"), the check script (`tools/wheel_table_check.py`:
   against each faction's archetypes, extras and answers) and the Stop 1 pages (`work/make_stop1.py` ->
   `wheel/STOP1*.md`: per faction its archetypes and synergies, theme, game plan, keywords, the seven answers, and one
   line per partner saying how the combo plays). Files under 150 lines.
