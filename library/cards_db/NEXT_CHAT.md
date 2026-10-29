# Next chat: deck networks — state, open work, how to work (29 Oct 2026, v33)

Read this file, then HANDOFF.md. Everything below is pushed. Kaptain is out of patience: he has found real errors in every
round, because the work fixed only what he pointed at. **Your job is to find the errors he has not pointed at.**

## How to think (read twice; this is what went wrong three times)
1. Every error Kaptain names is ONE example of a FAMILY. Before fixing it, write down the family ("an ability given to the
   player that boosts a kind of card", "a status keyword read as if it adds damage", "a condition about the card itself
   stored without 'self'"), then find EVERY member in ALL THREE GAMES with a query or a text regex over all cards, read
   20 of them, fix the rule, and read 20 again after. Never fix one card.
2. Think like a player of the game, card by card: for each card in a deck ask "what does this card need to work well
   (its level-up, triggers, conditions, stats, keywords, type) and which cards in the deck give it that?" and "what does
   this card give, and to whom?". Then compare with the network. Missing help is as wrong as a wrong line.
3. Read the card TEXT, not only the rows. If text and rows disagree, the rows are wrong: fix them by rule (fixes/<game>/vNN.py).
4. Never write "not sure" about something you can check: read the texts, the game's glossary (supplement, library/tools/games/
   <game>.md), the wiki. Kaptain's examples: "Spirits Unleashed deals 1 to EVERYTHING" (so it does hit Braum: the line is
   right); "Imps in your deck" — Monster Train's own glossary says Consume removes a card "from the deck for the rest of the
   battle", so deck = all cards of the battle: Imps added to hand count (Imp-in-a-Box -> Imp-olate is right).
5. Use real decks as the mirror: many full decks per game; for each, read every line and every missing line (point 2).
6. Report only what is checked. Say which families you swept and how many cards each touched.

## Open work, in order
1. **Kaptain's check of v33** (CHANGES.md): Tybaulk's family, the new decks, Janna. Fix what he finds as a family.
2. **Monster Train full decks: none found as text.** Searched Steam discussions and guides, GameFAQs, the wiki: players
   post screenshots or prose, not card lists. cases/decks.tsv still holds the guides' core cards. Ask Kaptain for
   screenshots or lists before searching again.
3. **Read the new decks' networks like a player** (PROCESS "Think like a player"): only Janna Nilah was read (found Janna's
   level-up row and the cost reduced family). Read the other 27 Runeterra and 22 Stormbound decks line by line.
4. Not linked on purpose (Claude's call, tell Kaptain if asked): Janna's "the first 3 cards you draw cost 1 less" helps any
   card, so it is no line to each card (it would say nothing about which cards belong together).
5. After any change: `run.py <game>` for all three games (now 290 / 135 / 145 cases), audit_links.py 0 findings,
   `python3 network_page.py`, give Kaptain network.html, push.

## Where things are
- network.py: lines (lines_of, aimed, played_lines, need_lines, boost_lines, gives_lines, families, through-made-card
  level-ups), measures, report. network_page.py -> network.html (game picker, decks, sidebar sections incl. Mechanics).
- refs.py (flat_ref: makes/trigger/condition/state with kinds, self, actor_self), flat.py (query layer, concept RULES),
  audit_links.py (in run.py), cases/network.tsv (Kaptain's checks as tests), fixes/runeterra/v30.py, v31.py.
- PROCESS.md: "Links the deck networks showed missing", "Think like a player"; BRIEF.md rules 23-25; CHANGES.md v30-v32.
