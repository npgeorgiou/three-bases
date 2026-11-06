FIXED: Monster Train case n292 passes again (155 of 155) and Gwent stays at 225 of 248.

- Case: n292 (Dreg -> Wickless Baron, line "dies").
- Commit: c215775 (gwent fixer C40), its new `grave_kill` set.
- Change: `grave_kill` held bare ability ids, but a keyword ability (Burnout, 7060) is shared by many cards, and four of them kill a card in the discard pile, so Dreg's own Burnout death was skipped. It now holds (card, ability) pairs and the skip checks `(card, ab)`, so only the card that really eats a discard-pile card loses the kill line.
