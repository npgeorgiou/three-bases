# The roster chat: 20 factions designed together, with their combos

Read `factions/START_DESIGN.md` and its parts 2-4 whole first, then `factions/roster/HANDOFF.md` (which step is next,
Kaptain's standing decisions) and this file. Commands of every step: `factions/roster/PIPELINE.md`. Library commands run
from `library/cards_db/`; first `gunzip -kf links.sqlite.gz` there. The roster writes no cards, no stats and no game code.

Three Bases is a game of combos: decks mix 2 factions, and every faction combines well with at least 7 others (its
partners). Every
number comes from the library by script; anything with no library source is marked as Claude's. Faction text uses plain
words Kaptain uses ("small hits", "the rest of the hit goes into the unit behind"), never library names.

## The words
- **Concept**: a tag the library gives an effect ("revive": a unit comes back; "attack_gain": gains strength).
- **Concept instance**: one effect of one card that gives a concept (one row in the database). "Deal 2 to an enemy,
  then draw a card" is two instances: one of damage, one of drawing.
- **Card link**: two real cards of one game where an effect of one sets off or feeds an effect of the other
  (`links.sqlite`). Each link keeps which effect of each card made it, so it counts only for those effects' concepts.
- **Strong link**: two concepts joined by the step 4 rule through real card pairs: `cards` 1.2+, or `rare` 3+ with a
  `level` of 1+. A pair joined only by real decks is not a strong link.
- **What decks play together**: step 3. A deck is **built on** a concept when it has so many more cards with it than
  its game's decks that chance can't explain it (score 1.96 or more: 8 heal cards where its game's decks average 2); a deck **holds** a concept by its share of cards with it, against its game's share. The
  17 groups of step 3 are concepts that real decks play together; they are not factions.
- **Identity**: what a faction DOES, in plain words: "can't be broken", "kills brutally", "waits", "messes you up",
  "moves" (Kaptain). Never a trigger or a condition ("when another unit dies"): those are how its cards work.
- **Kernel**: the concepts that do what the identity says: the effects of a few families of the concept tree
  (`library/concept_tree.txt`; "can't be broken" = keep my units alive, heal, defence gain).
- **Engine**: a concept of the faction that works through another of its concepts on real cards (a strong link):
  "my units die" with "my units gain when an ally dies". Engines come from card links.
- **Brick**: a concept of the faction that works alone and links to nothing, but that the kernel's decks play with
  it: removal, protection, disruption. Bricks come from decks.
- **The faction's concepts**: its kernel, engines and bricks, about 12. They are its character (what it is strongest
  at, what its keywords grow from).
- **Partner**: another faction its concepts combine with: real library links between the two factions' concepts, or
  one's decks holding the other's kernel (support: decks that buff also protect). Each partner has one line on how the
  combo plays, from its strongest real card pair.
- **The faction's list**: every concept of the library (usable, helpers and out) except the faction's concepts, each
  with its score for how strongly it links with them.
- **Extras**: the concepts of a faction's list that step 6 gives it besides its own concepts.
- **Helper**: a concept that only says when or how a card acts, one of the game's own things, or a thing for single
  cards (step 2). Never in a kernel; it can be an engine only if it is usable.
- **Synergy**: a strong link between two of the faction's concepts, shown by real card pairs, never written by hand:
  "makes your units die: the other card brings them back (in 7 of 10 games, 3.1 times chance)".
- **Design marker**: what a group of decks is like as a whole, read from their cards' type, cost, stats and text
  against their game's decks ("many spells", "cheap units", "low curve"; step 3). Never a concept.
- **Deck archetype**: what one deck tries to do, from Kaptain's list (`roster/archetypes_kaptain.txt`,
  `roster/deck_archetypes.tsv`: Madness, Storm, Reanimator...). A reference only: factions, partners and combos are
  never built from it.
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
  whole roster, by a low-cost model, within the budget Kaptain gives each time; logged in `factions/read-cards.tsv`,
  never read twice. A reading agent is told its budget and every card already in `read-cards.tsv`, and never runs a
  command that prints the texts of cards it did not name (a search over texts): such a search spent 10 texts at once
  on 20 Nov 2026.
- A faction is built at two levels: its engines come from card links (how its cards work through each other), its
  bricks from what its decks play (what goes with it although no card links them: removal, protection). Neither alone
  makes a faction.
- A concept several factions want is never dropped: it goes to the faction it fits best, and the others take their
  next best.
- A card's concept is judged with the rules of its keywords, not its printed text alone (Monster Train's Offering plays
  the card for free when it is discarded), and with the rows that gave it the concept.
- A concept that means two things in different games is a library error: it is split in the library, with test cases,
  never limited to some games in a list.

## The stops
- **Kaptain agrees the factions** (step 6: identities, concepts, partners) and **Stop 1: Kaptain agrees the 20
  factions** (step 9). The process is tried on 10 factions first (5 partners each); then the 20 (7+ partners each).
- Then one chat per faction (two can run at once): steps 1-6 of `START_DESIGN.md`. **Stop 2: Kaptain agrees them.**
  Then cards, the gate, the faction check (the cards against the faction's concepts and extras), a separate agent's
  review. **Stop 3: Kaptain gets the finished faction.**
- Pilot: the first two factions are partners with a STRONG combo; their premades play each other (`cardstats.js`) and
  one mixed deck shows whether the combo fires. **Stop 4: Kaptain decides whether the rest is built.**

## Steps 1-9, in this order (each uses only what the steps before made)
1. **Fix the library's concepts.** The suspects: every concept counted only in some games (`roster/work/suspects.tsv`),
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
   Then `check_all.py <any game>` (about 14 minutes; with no game it reloads nothing) and `links.py` (about 6) are rebuilt, Kaptain's OK first.
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
3. **What decks play together** (`work/deck_groups_nmf.py` -> `work/deck_groups_nmf.tsv`, `.md`, `.json`).
   Every deck's scores per concept, and the groups of concepts that real decks play together. Step 6 uses the decks'
   scores and cards (which decks lean on a kernel, what those decks hold); the groups are shown on the map (step 5)
   and are no factions. Real factions are never copied.
   1. Concepts: the usable concepts (step 2); a card counts each concept once (Claude's). Five unit measures are added
      to the NMF's input only, each against the card's game: unit, cheap unit, expensive unit, strong for its cost,
      tough for its cost (above the game's straight line of strength or defence by cost, Claude's).
   2. Scores: every deck of `decks.tsv` (the whole deck, all its cards, neutrals and staples too, never split by
      faction) and every real faction (43; Monster Train's clans are not measured), per concept: the log-odds ratio with a prior (Monroe et al.
      2008) against all the cards of its game (Claude's), as a z-score; above 1.96 the deck leans on it. Deck cards the
      library does not know are counted and reported, never guessed. Monster Train and Marvel Snap decks are in
      (Claude's).
   3. Groups: NMF (it splits each deck into a mix of a few groups of concepts) on the deck rows only, with the positive
      scores; each game weighs the square root of its deck count. The first guess comes from the data (NNDSVD), so one run gives the
      result. The number of groups, from 14 to 30 (Claude's),
      is the one whose groups stay most alike when the run is repeated on 90% of the decks, 10 times (Claude's). A deck
      fits a group that is at least 30% of its mix (Claude's). The roster keeps the version with 17 groups
      (`--groups 17`, the most stable number on the 3027 decks, 0.96; Kaptain's, 19 Nov 2026).
   4. Per group: its 10 heaviest concepts, each with the share of its decks that lean on it; its base concepts (more
      than half of its decks have them, more often than their game's decks, Claude's), like "Deal damage"; its unit
      numbers against their games; a group whose decks are 80% or more from one game is marked (Claude's).
      Its concepts on the map (`work/step3_groups.py`): its 10 heaviest and its base concepts, without the five unit
      measures and without the concepts more than half of the groups hold ("Attack gain"; Claude's).
   5. Per group, its design markers. Each is one number per deck against its game's decks: a deck has the marker when
      its number is in the top quarter of its game's decks, its mirror when in the bottom quarter; a group carries a
      marker when its decks have it at least twice as often as their games' decks (both Claude's). The markers, each
      with its mirror: many units / many spells (share of units, of spells); many buildings, cards that stay in play
      and never move (Immobile here; no mirror: almost every deck has few); low curve / high curve (the deck's average
      cost); cheap units / expensive units; cheap spells / expensive spells; few big units / many small units (how many
      units and their cost); strong for its cost / weak for its cost; tough for its cost / fragile for its cost (the
      units against their game's straight line of strength or defence by cost); hits more than it lasts / lasts more
      than it hits (strength against defence); plain cards / busy cards (effects per card); mostly summoned units /
      mostly units played from hand (cards that summon against its unit cards). "Many spells", "few big units" and
      "mostly summoned units" are Kaptain's, the rest Claude's.
   6. The real factions are never rows of the NMF. A faction fits its best 2 groups when its share of their concepts
      is at least twice its game's average (Claude's). The groups no faction fits, the factions that fit no group and
      the concepts in no group are listed.
   `work/make_faction.py "<concept>" ["<concept>"]` shows what the decks that lean on one or two concepts play (its
   header says how): a quick look, never a faction of the roster.
4. **The links between concepts** (`roster_links.py links --concepts` -> `roster/concept_links.tsv`). For every two
   concepts of `work/concepts.tsv` (usable, helpers and out): `cards` = how much more often than chance their cards are
   linked, counted only through what of each card made the link; `decks` = how much more often real decks heavy in one
   hold the other; `games` = in how many games real cards link them; `level` = the linked pairs as the slow level; `rare` for a pair chance gives under 5 linked pairs in every game (all linked pairs over all chance);
   `makes` (the share of the pair's links where a's card sets off or feeds b's card); the three most common link
   texts. Joined: `cards` 1.2+, or `decks` 1.5+, or `rare` 3+ with a `level` of 1+. `apart.py` lists the concept pairs
   real factions keep apart.
5. **The map of what decks play together** (`work/archetype_map.py` -> `factions/roster-map.html`, with
   `work/archetype_parts.tsv`, `work/archetype_map.tsv` and `work/archetype_gaps.tsv`): a page for Kaptain to look at;
   no later step reads it. Every concept of step 3 is a node at a fixed place, laid out once from the 17 groups of real
   decks: two concepts sit close when the same groups' decks lean on them more than all decks do (t-SNE, seeded;
   Claude's). Each group is a set of nodes; between two of its concepts that real cards link, an edge with the step 4
   numbers (`cards`, `games`, `level`), the top link text and one real card pair; an edge is marked weak when more than
   half of its card links are about hitting the player (no player health here), or when only real decks join it. A
   group's design markers are shown beside it, brown. Kaptain ticks groups to light their concepts and edges; between
   ticked groups the page draws every real link from a concept of one to a concept of another. Clicking concepts builds
   a set: the page shows how many real decks lean on at least half of them and in how many games, what else those decks
   lean on, which real factions fit it (its cards hold the concepts at least twice as much as its game's cards) and
   which groups are closest.
6. **The factions, from what they do** (by script: `work/kernel_factions.py` -> `work/kernel_factions.md`; then
   `work/concept_list.py` -> `work/lists/<letter>.tsv`). Every tie is broken by the concept key in alphabetical order,
   so every run gives the same result. In this order:
   1. **Identities.** Claude names what each faction does, in plain words, each made of families of the concept tree
      (Claude's; the 10 of the trial are in the script). Each is one idea (no fruit salad); together they are spread
      over the seven answers, and the game is a moving game, so moving is one of them.
   2. **The kernel**: the identity's usable concepts that are effects (never a trigger, a condition, or a drawback
      unless the identity is about spending its own side) that 10+ decks are built on, the 6 with the most decks. No
      "2+ games" rule: few games move, and Three Bases does (Kaptain). A concept two identities want goes to the one
      whose other kernel concepts' decks hold it more. A kernel under 4 concepts is widened by Claude with the family
      whose concepts its decks hold most and that fits the identity.
   3. **Engines, from card links**: usable concepts (triggers and conditions too) with a strong link to 2+ kernel
      concepts (in any number of games: a card pair that looks wrong is read and fixed in the library, never filtered
      out), and held by the kernel's decks at least as often as normal; ranked
      by kernel links times the share of all its links that go to this kernel (so a concept real cards link to
      everything does not join every faction, nor a rare one with two links); at most 4. Each shows the real card pair
      behind its strongest kernel link.
   4. **Bricks, from decks**: the kernel's decks are the decks built on at least half of its concepts (Kaptain). The
      concepts the kernel's decks hold 1.5x+ as often as their game's cards (per game with
      3+ of its decks, averaged), held by a quarter of those decks, with no strong link to the kernel; another
      faction's kernel concept can be one (support: removal for "can't be broken"). Most held first, until about 12
      concepts in all. A faction still under 12 then takes what its kernel's decks hold the same way that real cards
      also link to its concepts (an engine past the 4, or another faction's kernel concept), most held first (Claude's).
   5. **Many-level sharing**: the factions are filled together, level by level (kernels, then engines, then bricks,
      then what decks hold and cards link, then extras). A concept that would then be in more than 3 factions, counting those that
      have it from an earlier level, is never dropped: it goes to those it fits best (most kernel links for an engine,
      most held otherwise), and the others take their next best.
   6. **Checks**: every faction has an engine pair (two of its concepts real cards link), or its identity is changed;
      two factions share at most half of their concepts.
   7. **Partners**: for every two factions, the strong links between their own concepts, plus 3 for each kernel concept
      of one that the other's decks hold 1.5x+ (Claude's). A faction's partners are its strongest pairs: 5 each among
      10 factions, 7+ among the 20 (Kaptain). Each gets its "how it plays" line from its strongest real card pair, or
      from what its decks hold. A faction short of partners takes extras that link to others' kernels (6.10).
   8. **A real theme** (World War I artillery, the Zulu regiments), written for its identity; the themes all differ.
      The theme only breaks ties between concepts that score within 0.1 of each other.
   9. **Its list** (`work/concept_list.py`): every concept with 5+ cards (usable, helpers and out) except its own
      concepts, each with its score. In each game alone: real links between the concept's instances and the instances
      of the faction's concepts, against the links chance alone gives there; the game's score = (real + 1) /
      (chance + 1); the score = the average over the games where the concept and the faction's concepts both appear
      (every game weighs the same). Beside it: the `level` and in how many games.
   10. **Its extras**, the same number for every faction, 8 to 12 (10, Claude's; a real faction of about 100 cards mostly uses about
      20 concepts). Picked from its list in this order: (a) each of the four answers about the board (removing a front
      unit, removing back-row units, acting between lanes, holding a base) that its concepts don't give gets the
      highest-scoring way that gives it in `work/answer_concepts.tsv` (agreed with Kaptain: per answer its ways, each
      one concept, two concepts real cards link, or a removal on a spell; a way of two concepts takes two extras);
      (b) a faction short of partners: concepts that link to other factions' kernels; (c) the rest go to the
      highest-scoring concepts with strong links to at least 2 of its concepts; (d) the theme breaks ties.
   11. **Its answers**, from `work/answer_concepts.tsv`: how it wins comes from its identity and engines; removing a
      front unit, removing back-row units, acting between lanes and holding a base are each the first way of
      `work/answer_concepts.tsv` its own concepts give, else the way its extras give; what it cares about most is the
      first of the game's own things it has, else the highest-scoring on its list (factions may share it); its blind spot is named at step 9. An answer no way gives is fixed first in (10) with
      another extra; only when its list has no way for it is the identity changed.
   12. **The real kernel, then a second pass** (Kaptain): from each faction's concepts and extras, per question (removes
      a front unit, the back row, acts between lanes, holds a base, what it cares about) up to 2 concepts that answer
      it (one way of two concepts, or two ways of one); a question none of them answers takes the best way from its
      list. Each faction takes the options whose concepts go best together: two concepts score the higher of how many
      times chance real cards link them and real decks are built on both (8 times chance or more = 1; a brick has no
      card links, so decks carry it). Every kernel concept goes with another at a third of that or more; no two
      factions answer a question with the same concept (it stays where it fits best; what it cares about may be
      shared); no kernel concept is in more than 3 factions. Steps 3 to 11 then run again on the real kernel; the
      identity's families are not used again.
   **Kaptain agrees the factions**, seeing per faction its identity, kernel, engines (with their real card pairs),
   bricks, partners with their lines, and answers.
7. **Combos on this board.** For every two partners, Claude rates the combo with numbers on the board: STRONG (both
   halves on many cards, helps take or hold a base, the enemy's one action between can't easily stop it), OK (real but
   breakable), WEAK, NONE, AGAINST. Partners = STRONG or OK; every faction has 7+ (5 among 10); one short goes back to
   step 6.10. `roster/combos.tsv` (pair, rating, how it plays, the numbers, a test column that playtests fill).
8. **Game plan, then keywords** (`roster/plans.tsv`, `roster/keywords.tsv`).
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
   its concepts and extras give, "never draws cards"), the check script (`tools/roster_table_check.py`:
   against each faction's concepts, extras and answers) and the Stop 1 pages (`work/make_stop1.py` ->
   `roster/STOP1*.md`: per faction its identity, concepts and synergies, theme, game plan, keywords, the seven answers,
   and one line per partner saying how the combo plays). Files under 150 lines.
