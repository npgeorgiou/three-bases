# Next chat: card database (30 Oct 2026, v58)

Read HANDOFF.md first (its boxes are the rules most often broken), then PROCESS.md and PROCESS_LESSONS.md, and
library/README.md (what the library is for and how design questions are asked). Everything below is pushed.

## How to think (what went wrong, game after game)
1. Every error Kaptain finds is ONE example of a family. Name the cause in one sentence, decide whether it lives in the data
   (the rows) or in the scripts (the line rules, the questions), find every member in ALL games, fix the shared rule once,
   dump all lines before and after (`dump_lines.py`), read every gone and new reason.
2. Think like a player, card by card: what does it need, who gives it that, who must do it (Zed's own strikes, Ephemeral
   attackers), what it makes and what that made card does. Read the card TEXT, not only the rows.
3. Report per family: the cause, data or script, the fix, and the counts per game.

## Open, in Kaptain's order
1. Kaptain's answer on landmarks: Runeterra's Landmark keyword maps to `terrain` with map spaces; a new concept
   "Buildings that stay on the board" was proposed. Do not change concepts before he says yes.
2. Item 7, approved, not started (Kaptain wants it explained first, then built): every card-to-card line of every deck stored
   as a table in cards.sqlite (from, to, kind, reason), built with the database; one design question giving per game the
   cards with their texts, best partners and factions.
3. Item 8, not started: a full deck check of every game, card by card, reading what each card makes (`deck_audit.py`), not a
   sample; fix every family by cause.
4. Proposals for design questions, not started (library/README.md "Known gaps"): search concepts by plain words; a
   "faction kit" question (for a set of concepts: per game the factions that combine them, their key cards with texts).

## Not this chat's work unless asked
- Stormbound csb09-csb13 (poisoned-unit combos) fail; Runeterra n56 and Slay the Spire nst36 must be rewritten.
- A card placed by its own text near the leader (Conscript) draws no line to a card acting near the leader (Fealty);
  Adaptive Mutation's stat swap has no link.
- Monster Train has no full decks as text: ask Kaptain.
