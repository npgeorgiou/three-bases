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
- **Built on, holds**: step 3. A deck is **built on** a concept when it has so many more cards with it than its game's
  decks that chance can't explain it (score 1.96 or more: 8 heal cards where its game's decks average 2). A deck
  **holds** a concept when its share of cards with it is twice its game's average.
- **Identity**: what a faction DOES, in plain words: "can't be broken", "kills brutally", "waits", "messes you up",
  "moves" (Kaptain). Never a trigger or a condition ("when another unit dies"): those are how its cards work.
- **Core**: the concepts that do what the identity says: the effects of a few headings of the concept tree
  (`library/concept_tree.txt`; "can't be broken" = keep my units alive, heal, defence gain) that most decks are
  built on.
- **Kernel**: the core plus, for each board question the core does not answer, up to 2 concepts that answer it and
  go best with the core (step 6).
- **Fit**: how well two concepts go together, 0 to 1: the higher of how many times chance real cards link them and
  real decks hold both (8 times chance = 1). Armour and shield are rarely linked by cards, but decks play them
  together, so they fit.
- **Engine**: a concept of the faction that real cards link to another of its concepts ("my units die" with "my units
  gain when an ally dies"). **Brick**: one that links to nothing but that decks play with the faction's concepts
  (removal, protection).
- **The faction's concepts**: its kernel and the concepts that fit its core best, 12 in all. They are its character
  (what it is strongest at, what its keywords grow from).
- **Partner**: another faction its concepts combine with: real library links between the two factions' concepts, or
  one's decks holding the other's kernel (support: decks that buff also protect). Each partner has one line on how the
  combo plays, from its strongest real card pair.
- **The faction's list**: every concept of the library (usable, helpers and out) except the faction's concepts, each
  with its score for how strongly it links with them.
- **Extras**: the next 10 concepts that fit its core best, after its own 12.
- **Helper**: a concept that only says when or how a card acts, one of the game's own things, or a thing for single
  cards (step 2). Never in a faction.
- **Synergy**: a strong link between two of the faction's concepts, shown by real card pairs, never written by hand:
  "makes your units die: the other card brings them back (in 7 of 10 games, 3.1 times chance)".
- **Design marker**: what a set of decks is like as a whole, read from their cards' type, cost, stats and text
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
- A faction is built from two kinds of proof at once: card links (how its cards work through each other) and real
  decks (what is played with it although no card links them: removal, protection). Fit takes the higher of the two.
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
3. **The real decks' scores** (`work/deck_scores.py` -> `work/deck_scores.json`), read by step 6 and the map. Real
   factions are never copied.
   1. Concepts: the usable concepts (step 2); a card counts each concept once (Claude's). Five unit measures are added,
      each against the card's game: unit, cheap unit, expensive unit, strong for its cost, tough for its cost (above
      the game's straight line of strength or defence by cost, Claude's).
   2. Scores: every deck of `decks.tsv` (the whole deck, all its cards, neutrals and staples too, never split by
      faction) and every real faction (43; Monster Train's clans are not measured), per concept: its cards with it,
      and the log-odds ratio with a prior (Monroe et al. 2008) against all the cards of its game (Claude's), as a
      z-score; 1.96 or more: the deck is built on it. Deck cards the library does not know are counted and reported,
      never guessed. Monster Train and Marvel Snap decks are in (Claude's).
   3. Design markers, per deck. Each is one number per deck against its game's decks: a deck has the marker when
      its number is in the top quarter of its game's decks, its mirror when in the bottom quarter; a set of decks
      carries a marker when its decks have it at least twice as often as their games' decks (both Claude's). The
      markers, each with its mirror:
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
   `work/make_faction.py` makes one faction from concepts Kaptain gives, the way step 6 does (its header says how).
4. **The links between concepts** (`roster_links.py links --concepts` -> `roster/concept_links.tsv`). For every two
   concepts of `work/concepts.tsv` (usable, helpers and out): `cards` = how much more often than chance their cards are
   linked, counted only through what of each card made the link; `decks` = how much more often real decks heavy in one
   hold the other; `games` = in how many games real cards link them; `level` = the linked pairs as the slow level; `rare` for a pair chance gives under 5 linked pairs in every game (all linked pairs over all chance);
   `makes` (the share of the pair's links where a's card sets off or feeds b's card); the three most common link
   texts. Joined: `cards` 1.2+, or `decks` 1.5+, or `rare` 3+ with a `level` of 1+. `apart.py` lists the concept pairs
   real factions keep apart.
5. **The map** (`work/roster_map.py`, run after step 6 -> `factions/roster-map.html`): a page for Kaptain to look at;
   no later step reads it. Every usable concept is a dot. Two concepts sit close when real decks hold both more often
   than chance (a deck holds a concept when it has 2 or more cards with it and their share is twice its game's
   average); springs lay the dots out. The groups: concepts real decks play together (held together 1.5 times chance
   or more by 10 or more decks, found by Louvain); with no faction ticked each dot has its group's colour, the groups
   are listed on the right, and a concept in no group (grey) sits beside the 3 grouped concepts real decks hold with it most, or, when no
   decks do, the 3 real cards link it with most, or else beside its parents and children in the concept tree, or the concepts that share a parent with it. Ticking factions lights their
   kernel, other concepts and extras, draws in the faction's colour the strong card links between its concepts, and
   shows its deck style (its design markers).
6. **The factions, from what they do** (by script: `work/kernel_factions.py` -> `work/kernel_factions.md`, one sheet
   per faction for Kaptain; `work/kernel_factions_summary.json`, the
   numbers that compare two runs; `work/lists/<letter>.tsv`). Every tie is broken by the concept key in alphabetical
   order, so every run gives the same result. In this order:
   1. **Identities.** Claude names what each faction does, in plain words, each made of headings of the concept tree
      (Claude's; the 10 of the trial are in the script). Each is one idea (no fruit salad); together they are spread
      over the seven answers, and the game is a moving game, so moving is one of them.
   2. **The core**: the identity's usable concepts that are effects or "when..." (never a condition, nor a drawback
      unless the identity is about spending its own side) that 10+ decks are built on, the 6 with the most decks. No
      "2+ games" rule: few games move, and Three Bases does (Kaptain). A concept two identities want goes to the one
      whose other concepts' decks hold it more.
   3. **Its decks**: the decks whose cards with any kernel concept make up twice the share its game's decks average or
      more (8 armour, heal or shield cards where the game's decks average 3).
   4. **The ranked fill**: every other usable concept is ranked by its fit to the core, the average over the core
      concepts (fit: the higher of how many times chance real cards link the two and real decks hold both; a deck holds
      a concept when its share of cards with it is twice its game's average; 8 times chance or more = 1). The best fill
      the faction to 12 concepts, then its extras to 22 (a real faction of about 100 cards mostly uses about 20
      concepts). A concept real cards link to another of its concepts is an engine, any other a brick.
   5. **Sharing**: the factions are filled together; a concept that would be in more than 3 factions (kernels, concepts
      and extras together) stays with those it fits best, and the others take their next best; it is never dropped.
   6. **Its list** (`work/concept_list.py`): every concept with 5+ cards (usable, helpers and out) except its own
      concepts, each with its score. In each game alone: real links between the concept's instances and the instances
      of the faction's concepts, against the links chance alone gives there; the game's score = (real + 1) /
      (chance + 1); the score = the average over the games where the concept and the faction's concepts both appear
      (every game weighs the same). Beside it: the `level` and in how many games.
   7. **The kernel** (Kaptain): the core, plus for each question the core does not answer (removes a front unit,
      mainly the back row, holds a base, what it cares about; the ways of each in `work/answer_concepts.tsv`) up to 2
      concepts that answer it (one way of two concepts, or two ways of one), from
      its concepts and extras, and from the top 30 of its list when those give fewer than 3 options; a question none of
      them answers takes the best way from its list. It takes the options that fit best with the core and the other
      answers. Every added concept fits another kernel concept at a third or more; no two factions answer a question
      with the same added concept (it stays where it fits best; what it cares about may be shared); no kernel concept
      is in more than 3 factions. Between lanes comes from the core alone, so it fits what the faction does: the core
      concept whose real cards most often act on a unit or place in another lane than their own (2 or more cards; a
      concept counts the narrower concepts under it), as "<it> in another lane" (Swarms: summon in another lane); when
      no core concept has such cards, it stays open: "nothing in real cards". Then 3 to 5 run again on the kernel, the fill still ranked by fit to the core.
   8. **Missed concepts**: a concept 15+ decks are built on that no faction has replaces the weakest extra of the
      faction it fits best, when it fits at least 0.8 as well; what is still in no faction is listed on the page.
   9. **Its answers**: the kernel's concepts per question (7); how it wins, from its identity and its strongest pair
      of concepts real cards link; its blind spot is named at step 9.
   10. **Partners**: for every two factions, the strong links between their own concepts, plus 3 for each kernel
      concept of one that the other's decks hold 1.5x+ (Claude's). A faction's partners are its strongest pairs: 5
      each among 10 factions, 7+ among the 20 (Kaptain). Each gets its "how it plays" line from its strongest real
      card pair, or from what its decks hold.
   11. **Its people**: one new world for all factions (Veyl, Claude's), and per faction its people there, never a
      real place or people; the real-world model each is written from stays in the script. Their headings only break
      ties between concepts that score within 0.1 of each other.
   12. **Checks**: every faction has an engine pair (two of its concepts real cards link), or its identity is changed;
      two factions share at most half of their concepts.
   **Kaptain agrees the factions**, seeing per faction its identity, people, kernel with its answers, other concepts,
   extras and partners (`work/kernel_factions.md`).
7. **Combos on this board.** For every two partners, Claude rates the combo with numbers on the board: STRONG (both
   halves on many cards, helps take or hold a base, the enemy's one action between can't easily stop it), OK (real but
   breakable), WEAK, NONE, AGAINST. Partners = STRONG or OK; every faction has 7+ (5 among 10); one short goes back to
   step 6 (its identity). `roster/combos.tsv` (pair, rating, how it plays, the numbers, a test column that playtests fill).
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
   against each faction's concepts, extras and answers) and the Stop 1 pages (written at step 9 from `work/kernel_factions.tsv`, the plans and the keywords ->
   `roster/STOP1*.md`: per faction its identity, concepts and synergies, theme, game plan, keywords, the seven answers,
   and one line per partner saying how the combo plays). Files under 150 lines.
