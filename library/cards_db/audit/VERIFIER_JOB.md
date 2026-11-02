You verify findings about lines between cards (a card database for 4 games). Change NO file in the repo. Use exactly 4 tool calls, no more:
1. Read /home/claude/three-bases/library/cards_db/START_DATABASE.md with offset 30, limit 79 (rules L1-L22: the owner Kaptain's decisions; they decide, not your taste).
2. Read /home/claude/three-bases/library/cards_db/SYNTAX.md (how to read a card's rows).
3. Read your piece (below) in ONE call (limit 2000).
4. Write your verdict file (below).

Your piece lists causes that earlier readers believed are WRONG lines (or missed lines). Under each example line it shows: "line now" (the line as it exists today; NONE = no line), both cards' rows, and any test case. The readers were often wrong. For each cause decide, from the rows and the rules L1-L22 (including their exceptions, e.g. L18 keeps a line where a card "doubles what is there"):
- REAL: the example lines are wrong (or the missed line should exist) and the cause is stated right;
- NOT REAL: the lines are right (a real combo), the reader misread a rule;
- PARTLY: some examples wrong, some right (say which);
- GONE: every example says "line now: NONE" for a wrong-line cause (already fixed).
Kaptain's own word (2 Nov 2026), use it as a known truth: "The Dreadway -> Decimate is a combo that works." A test case written by Kaptain ("Kaptain" in its source) is his decision.
Think like a player of the game: would a good player build these two cards together for this reason?
Verdict file format, one block per cause, short: "N. VERDICT: one sentence why. Wrong examples: A -> B, ... Right examples: A -> B, ..." Then a final line: counts per verdict.
Reply with only the file path and the counts.

Your piece:
