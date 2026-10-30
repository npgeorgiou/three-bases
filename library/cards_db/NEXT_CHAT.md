# Next chat: card database (30 Oct 2026, v59)

Read HANDOFF.md first (its boxes are the rules most often broken), then PROCESS.md and PROCESS_LESSONS.md, and
library/README.md (what the library is for and how design questions are asked). Everything below is pushed.

## How to think (what went wrong, game after game)
1. Every error Kaptain finds is ONE example of a family. Name the cause in one sentence, decide whether it lives in the data
   (the rows) or in the scripts (the line rules, the questions), find every member in ALL games, fix the shared rule once,
   dump all lines before and after (`dump_lines.py`), read every gone and new reason.
1. Think like a player, card by card: what does it need, who gives it that, who must do it (Zed's own strikes, Ephemeral
   attackers), what it makes and what that made card does. Read the card TEXT, not only the rows.
2. Report per family: the cause, data or script, the fix, and the counts per game.

## Open, in Kaptain's order
2. Read every answer in library/design_questions/ like a designer and trace each wrong or thin one (seen: Taunt and Provoke
   count as stopping enemies; Inscryption's Waterborne counts as stopping enemies; Duelyst and Faeria disruption near 0).
3. Trace every miss of `realworld.py` (84 of 275 cases miss; Inscryption combos with sigils find no line; Ironclad has no
   permanent_growth) and every lead of `audit_links.py` 10 (Runeterra: 379 cards tagged on_kill before have no row for it).
3. Item 7, approved, not started: every card-to-card line of every deck as a table in cards.sqlite (from, to, kind, reason),
   built with the database, so any question can use the lines; one design question giving per game the cards with texts,
   best partners and factions (`kit` covers part of it).
4. Item 8, not started: a full deck check of every game, card by card (`deck_audit.py`), not a sample.

## Not this chat's work unless asked
- Stormbound csb09-csb13 (poisoned-unit combos) fail; Runeterra n56 and Slay the Spire nst36 must be rewritten.
- A card placed by its own text near the leader (Conscript) draws no line to a card acting near the leader (Fealty);
  Adaptive Mutation's stat swap has no link.
- Monster Train has no full decks as text: ask Kaptain.
