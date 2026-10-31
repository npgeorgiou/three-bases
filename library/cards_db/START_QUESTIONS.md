# Start here: chats that answer Kaptain's design questions

Read this file whole. You answer questions from the card database; you do not change it. If an answer shows a wrong
card reading or a wrong line, tell Kaptain and leave the fix to a database chat (START_DATABASE.md).
Clone with the library: CLAUDE.md "Start of a chat", then `git sparse-checkout disable`. Commands run from
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
librarian's report"). Never invent rules or mechanics; say which game a way comes from.

## What the database holds
- 8 games: Runeterra (regions), Stormbound, Monster Train (clans), Duelyst, Faeria (colours), Inscryption, Into the
  Breach (squads), Slay the Spire (characters). Factions are the `regions` of each card.
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
| The values you can ask for | `ask.py all list concepts`, `ask.py all list happenings` |
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
Known weakness: `kit` shows a faction's most-tagged cards, not cards that show the asked mix, and a broad concept
(protection, drawback) drowns a narrow one (selection). Do not answer from `kit` alone.

## Talking to Kaptain
Short plain sentences, his words, a card example per point. One question at a time, last, marked. No recaps.
