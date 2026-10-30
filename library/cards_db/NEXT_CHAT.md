# Next chat: card database (31 Oct 2026, v63)

Read HANDOFF.md first (its boxes are the rules most often broken), then PROCESS.md and PROCESS_LESSONS.md, and
library/README.md (what the library is for and how design questions are asked). Everything below is pushed.

## Open, in Kaptain's order
Done 31 Oct (v59-v63, CHANGES.md). Real-world: 213 of 274 hold. The three checks after an import: PROCESS 4b; how to think:
HANDOFF.md.
1. Item 7 (Kaptain said build it, 31 Oct): every card-to-card line as a table in cards.sqlite (from, to, kind, reason), built
   with the database. Lines between EVERY pair of cards of a game, whatever their faction (not only deck cards): Kaptain
   judges ideas by what worked in other games, so each game's deck rules must hold. Queries limit the lines to the faction
   mixes a deck may have (Runeterra: 2 regions per deck, 10 regions = 45 pairs; deck_analysis.py RULES has each game's
   rule). Then: lines per card as a first measure of deck feasibility and of mechanic feasibility ("ideas for factions").
   Check the table's size per game first.
2. Not finished in this chat (Kaptain wanted it done): 36 real-world combos with no line, in families: Inscryption sigil
   combos (a card wearing a sigil: Fecundity, Unkillable, Corpse Eater), Slay the Spire Exhaust/Retain/Orb pairs, Into the
   Breach push/smoke pairs, Runeterra (Ezreal + spells, Judgment + Deny). `ask.py kit` answers are weak: the examples are the
   faction's most-tagged cards, not cards that show the asked mix, and a broad concept (drawback, protection) swamps a narrow
   one (selection). Fix both before item 7 if Kaptain agrees.

## Not this chat's work unless asked
- Stormbound csb09-csb13 (poisoned-unit combos) fail; Runeterra n56 and Slay the Spire nst36 must be rewritten.
- A card placed by its own text near the leader (Conscript) draws no line to a card acting near the leader (Fealty);
  Adaptive Mutation's stat swap has no link.
- Monster Train has no full decks as text: ask Kaptain.
