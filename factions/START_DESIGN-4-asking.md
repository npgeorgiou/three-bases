# Start design, part 4: asking the library (every question, every design request)
Part of `factions/START_DESIGN.md` (read that first, whole; then parts 2, 3 and this file, whole). A plain question to the
library ("how do games do X?", a combo hunt, a deck idea) starts at START_DESIGN.md too; it answers in the shape below.

You answer questions from the card database; you do not change it. If an answer shows a wrong card reading or a wrong
line, tell Kaptain and leave the fix to a database chat (`library/cards_db/START_DATABASE.md`). Commands run from
`library/cards_db/`; cards.sqlite is committed and current, no build is needed.

## What Kaptain wants
He designs factions for Three Bases (summary/ in the repo is the game as it is). He asks things like "how do I make a
faction that lands big costly units early and protects its board until then?" He wants, at a high to mid level:
1. the plan in one or two sentences;
2. its parts, and the ways real games build each part (a steady discount that grows with the board; one big random
   discount; a free play from the deck), with how common each way is;
3. how the parts feed each other (which part makes which part cheaper, sets it off, protects it);
4. what keeps it fair, and what works against it (a part that hurts another part, the usual counters);
5. what no game has done, marked as your idea.
Cards are only short examples, one per way. He rejected an answer that was a list of cards per game ("name-dropping, a
librarian's report"). Never invent rules or mechanics. Describe the way, not the game or card name, unless he asks for
sources.

## What the database holds
- 10 games: Runeterra (regions), Stormbound, Monster Train (clans), Duelyst, Faeria (colours), Inscryption, Into the
  Breach (squads), Slay the Spire (characters), Gwent, Marvel Snap (no factions). Factions are the `regions` of each card.
- Each card as rows: event, conditions, effects. Each row has a concept from `library/concept_tree.txt` (concepts are by
  outcome: "suppress" holds disable, silence, can't block ...; a question on a concept also finds the ones under it).
- Lines between cards of one game, drawn by network.py for any list of cards (decks in decks.tsv).

## How to ask (ask.py; `all` = every game, or one game, or several joined by commas)
| Need | Command |
|---|---|
| How a mechanic works in each game | `ask.py all compare <concept>` |
| Which factions are built on a mechanic (share of cards) | `ask.py all factions <concept>` |
| Factions that combine several mechanics | `ask.py all kit <concept> <concept> ...` (weak: see below) |
| What sets a mechanic off / what it sets off | `ask.py all fed <concept>`, `ask.py all feeds <concept>` |
| What a mechanic is built with | `ask.py all together <concept>` |
| Chains of three | `ask.py all chains <concept>` |
| Cards that do two things | `ask.py all both <A> <B>` |
| Which cards care about something / make it | `ask.py all cares <happening or concept> [mine/enemy]`, `makes ...` |
| One card's rows, with its text | `ask.py <game> card "<name>"` |
| How two cards work together | `ask.py <game> combo "<A>" "<B>"`, `ask.py <game> partners "<card>"` |
| A deck explained, its lines | `ask.py <game> analyze "<card>, <card>, ..."`, `ask.py <game> network "<cards>"` |
| What cards do on one trigger (place, death, round_end, spell_cast, ally_dies, or any trigger concept), grouped, count and 2 examples each | `ask.py all palette <trigger> [faction]` |
| A faction's cards by cost: units and spells per cost, per card trigger -> effect -> target | `ask.py all curve "<faction>"` |
| A faction's spells grouped by what they do | `ask.py all spells "<faction>"` |
| How a faction deals with enemy units (kill, damage, push away, take strength, silence, stop, transform, steal, sacrifice to kill), share of each; a game name gives every faction of it | `ask.py all removal "<faction>"`, `ask.py all removal <game>` |
| How a faction protects its own (armour, shield, immunity, survive death, guard, hide, heal), share of each; a game name gives every faction | `ask.py all protect "<faction>"`, `ask.py all protect <game>` |
| A faction's ways to play: groups of tightly linked cards, key cards, what ties each | `ask.py all ways "<faction>"` |
| Concepts only one faction of a game has (its monopolies) | `ask.py all only <game>` |
| Concepts a faction never has while at least half its game's other factions do (its blind spots) | `ask.py all lacks "<faction>"` |
| The values you can ask for | `ask.py all list concepts`, `ask.py all list happenings` |
| Mechanics real factions keep apart (opposite sides of the wheel) and together (neighbours) | `python3 apart.py [top]` |
| Every real faction on the wheel's radii, closest factions, map | `python3 axes.py` -> `factions/wheel-axes.html` (factions/13) |
Example answers: QUERIES.md. Kaptain's standing questions with their current answers: library/design_questions/
(made by design_questions.py). The full list of questions the database must answer: QUESTION_BANK.md.

## How to build an answer (until the line table of LINKS_PLAN.md exists)
1. Write the question's parts as concepts (QUESTION_BANK.md has many already written).
2. For each part: `compare` and `factions` (which games and factions have it, how), then read 5-10 cards' texts to group
   them into ways. A concept is broad: read texts before trusting a count.
3. For each pair of parts: `fed`/`feeds` and `both`, and `network` on a handful of cards from each part in one faction, to
   see the lines between them. Read the lines' reasons.
4. Direction matters and concepts lose it: "cost_increase" is the opponent's cards costing more, a cost rise on my own cards
   is no concept yet; "copy" does not say whose card is copied. Read the card texts to tell.
5. Write the answer in the shape above. Show the parts and links first, cards as examples.

## Search wide, deep and with curiosity (every design request)
- Wide: start with `list concepts`; for each part of the request pick the obvious concepts and their neighbours (e.g.
  builders: summon, link_formation, terrain, placement_rules). For each concept run `compare`, `factions`, `fed`, `feeds`,
  `together`, `chains`, and `both` with every other part; read texts from every game that has it, not just top counts.
- Deep: for each faction that does the thing, run `network` / `analyze` on its real decks in decks.tsv, to see working
  decks, not single cards. Decks are a small sample of a faction: never the
  only check that mechanics fit together.
- Curious: at least three unexpected concepts that could serve the same outcome; one game where the mechanic is rare or
  done oddly; the older 21-game library (`../three-bases-library.sqlite`) as leads; archetypes and known combos in
  `../realworld/`.
- Translate: turn each way into Three Bases rules (lanes, dots, round end, no active abilities, no counters) and say what
  had to change.
- Board and rules check (Kaptain, 3 Nov 2026), before any card is suggested: read summary/ sections 03-08 and 10
  (board, winning, rounds, units, areas, rulings, keywords); a rule not written there is looked up quickly in the game code
  (map in CLAUDE.md). Test every card and deck against them: each lane camp is 3x3 with 3 front cells (the dots); melee
  reaches only the enemy front row, deeper rows only Ranged, Pike, spells and abilities; front units never shield back units;
  count the cells a deck's units fill in one lane; check what each unit can still reach from where it must stand.
- Think it through like a player (Kaptain, 3 Nov 2026), for every card and every combo, before suggesting it:
  - Hand: decks of 30-40 with 3 copies, 2 draws a round. Is the card in hand when it is needed? A setup of two named cards
    is rare; one that needs a second copy of itself is rarer.
  - Board: where exactly does it stand (row, column), what does it reach from there, and is that cell free then?
  - Enemy: what does the enemy do with its next action? Front-row units die easily. If the first card of a setup dies
    before the second arrives, the setup is dead.
  - Timing: what happens during the round, what at round end (after both pass, when the enemy can't answer), what counts
    for the dots.
  - Worth: is the card better than a plain unit of the same cost in that spot? If not, drop it.
- Identity check: first write the faction's identity in one sentence; every mechanic must serve it. A library way found on
  similar cards elsewhere (e.g. buildings that damage themselves) is not a reason to use it. Never take another faction's
  identity (summary/11-faction-*.txt), e.g. self-damage belongs to the Ashfang Horde; cross-faction ideas only when asked.
- A combo is not a list of buffs. Two cards are a combo only when one changes what the other does or sets it off again
  (a loop, a conversion, a rule change), so together they do something neither does alone, not just bigger numbers.
  Test: take either card away; does the other lose its point? Show each combo as a played sequence: card, cell, what the
  enemy can do, result.
- Self-check before sending: per part, which commands ran; say plainly which parts have no library grounding.
Known weakness: `kit` shows a faction's most-tagged cards, not cards that show the asked mix, and a broad concept
(protection, drawback) drowns a narrow one (selection). Do not answer from `kit` alone.

## Talking to Kaptain
Short plain sentences, his words, a card example per point. One question at a time, last, marked. No recaps.
