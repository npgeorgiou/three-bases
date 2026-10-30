# Next chat: card database (31 Oct 2026, v62)

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
Done 31 Oct (v59-v62, CHANGES.md): Landmark is board_limit; own-unit stops get no concept; own Can't Block is cant_block_self;
Taunt and Provoke stay immobilize (Kaptain: the rules say enemies next to them can't move); rules for concepts no card had
(board_wipe, disruption, board_clog, mill, tank, high_cost ...); realworld.py counts Into the Breach weapons and kw: cases.
Real-world: 205 of 275 hold (was 191). The three checks after an import are in PROCESS 4b.
1. Real-world misses left (`realworld.py`). Cases that look wrong, to show Kaptain with texts: Ionia counter_spell "Deny"
   (Deny is Freljord), Shurima shield "Spellshield", Hellhorned summon (Imp Parade adds Imps to hand: generate_cards),
   Melting Remnant revive (Reform returns to hand; Kaptain 26 Oct: back to hand is not revive), Magick cost_type. The
   "Runeterra" region (97 cards) tops many ranks: ask whether small regions should count. 36 combos with no line: trace them
   as families (Inscryption sigil combos, Slay the Spire Exhaust/Retain/Orb cards, Into the Breach push combos).
2. More design questions, per faction (Kaptain 31 Oct: "ask more, more, MORE"), read every answer, rework wrong ones. Concepts
   still with no card: list with the snippet in this chat's CHANGES v61; roles (finisher, support, snowball) have no rule.
3. Item 7, Kaptain's yes NOT given yet: explained to him; suggestion (Claude's) to also hold lines between all cards of a
   faction, not only deck cards, for faction ideas and deck feasibility (lines per card). Wait for his answer.
4. Item 8, not started: a full deck check of every game, card by card (`deck_audit.py`), not a sample.

## Not this chat's work unless asked
- Stormbound csb09-csb13 (poisoned-unit combos) fail; Runeterra n56 and Slay the Spire nst36 must be rewritten.
- A card placed by its own text near the leader (Conscript) draws no line to a card acting near the leader (Fealty);
  Adaptive Mutation's stat swap has no link.
- Monster Train has no full decks as text: ask Kaptain.
