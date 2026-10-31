# Design answers: what is wrong and the plan (31 Oct 2026, Claude; waiting for Kaptain)

Test set: Kaptain's five questions (library/design_questions, and the answer he rejected):
a) speed up big costly units and protect the board until they land; b) the same by earning resources faster;
c) spell-based, units mostly as spell enhancers; d) choose what you draw from the top 2, but everything costs 1 more;
e) steal the opponent's cards and copy its units and spells.
A good answer reads like a faction outline: the plan, its parts, how the parts feed each other, what keeps it fair, what is
new. Cards only as short examples. The rejected answer was a list of cards per game.

## Why the answers are bad (causes, not examples)
1. **The question is asked in concepts, the answer is tag counts.** `ask.py kit` counts, per faction, cards tagged with each
   concept and prints the most-tagged cards. A plan ("land big units early") is not a concept; it is parts that feed each other.
2. **Nothing records how mechanics feed each other across a whole game.** Lines exist only inside the decks we drew. So "how
   do the parts connect" and "is this viable" cannot be read from data; the answer falls back to naming cards.
3. **Concepts have no direction.** "Cost more" on my cards (question d) and on the enemy's are one concept; so are "copy my
   unit" and "copy an enemy's" (e); "cost cut" on a 7-cost unit and on any card (a). The rows know the side and the target
   (on_side, on_with, cost); the concepts drop it.
4. **Broad concepts drown narrow ones.** Protection or drawback tags hundreds of cards; selection a few dozen. Counts are not
   weighted by how common a concept is, so the narrow part of the question vanishes.
5. **Examples are single cards, not pairs.** A card with many tags shows nothing about how two parts work together; a pair
   with a line between them does (Bold Bargainer -> a 9-cost creature: "makes it cheaper").

## The plan
1. **Every line of every game (item 7).** One table in cards.sqlite: from card, to card, kind, reason pattern (card names
   taken out), and the two abilities the line joins (what the first card does, what the second needs). Built with the
   database, only between cards that a legal deck can hold together. Measured today, whole games before the deck rule:
   Inscryption 3.7 k lines, Into the Breach 9 k, Stormbound 12 k, Monster Train 13 k, Slay the Spire 28 k, Faeria 39 k,
   Duelyst 128 k, Runeterra 1.0 M (4 minutes; its 2-regions rule cuts it a lot). Deck rules exist for Runeterra and
   Stormbound only; the other six come from their own sources (Kaptain where none says it).
2. **Links between mechanics.** Lines grouped by what the first card does and what the second needs ("cuts the cost of" ->
   "an expensive unit"; "creates cards in hand" -> "is played by discarding"). Counted per game and per faction. This answers
   "what works with what", and "is it viable": a faction is viable for a link when it has many cards on both ends.
   Lines per card: how easy a card is to build a deck around; per mechanic: how easy the mechanic is.
3. **Roles with direction.** A role is a concept plus whose (mine, enemy) and on what (units, spells, expensive cards, the
   top of my deck). Read from the rows, not new tags: "cost_increase on my cards" (d), "copy of enemy cards" (e).
4. **Plan words.** Kaptain's words mapped once to roles, shown to him first (like the archetype list of realworld.py):
   "big costly units" = my expensive units; "speed up" = cost cuts aimed at them, extra resource, putting them into play
   without paying; "protect the board" = blockers, Taunt, protection, healing, early removal.
5. **The answer.** The tool gives, per question: each part and the ways real games build it, grouped by how they work
   (a steady discount that grows with my board; one big random discount; free play from hand or deck), with how common each
   is; how the parts connect (the links of step 2, with counts over games); where the engine is densest (faction, game);
   the tensions (a part that hurts another: discounts per ally vs a board kept small); and what no game does (new ground,
   marked as Claude's). Narrow roles weigh more than broad ones. Examples are pairs with their line. Claude writes the
   faction outline from that, high to mid level, cards only as examples.
6. **Check.** The five questions above, answered after each step; an answer that still reads like a card list is a cause
   to fix.

Order: 1, then 3 and 4 (small), then 2 and 5, then the check.
