# Lessons for future factions

Findings collected while building, playtesting and AI-testing factions, kept as general lessons so the next factions
are made faster and with fewer mistakes. One lesson per entry: what was found, where, and what to do from now on.
Split this file into parts once it passes 150 lines.

## AI testing

- **Write every card effect as data, never as per-card code** (4 Nov 2026, AI lab). The lab's learning AI and the
  Benchmark's effect values see a card only through its data: numbers, keywords and effect parts (when, what, on whom,
  how much), as `fx`, `aura` and `cast` in the card files. A card whose effect lives only in code looks to them like a
  plain unit, so the AI tests would misjudge it. A new effect word (a new kind of op or trigger) is new to the
  network and starts unknown; reusing existing words lets it judge the card from the start.
- **A deck or card judged better from a few hundred games is often just lucky** (4 Nov 2026, Decks tab). Picking the
  lowest or highest of several scores picks luck too. Judge a change only on fresh games that both versions play the
  same way (same opponents, seats and deals). With coin-flip results, 11% of tried decks looked "clearly better"
  without fresh games and 0.4% with them.
