You verify findings about lines between cards (a card database). Change NO file in the repo. Use exactly 4 tool calls:
1. Read /home/claude/three-bases/library/cards_db/LINE_RULES.md (rules L1-L24: the owner Kaptain's decisions, with their
   exceptions; they decide, not your taste).
2. Read /home/claude/three-bases/library/cards_db/SYNTAX.md (how to read a card's rows).
3. Read your piece (path at the end) in ONE call (limit 2000).
4. Write your verdict file (path at the end).
Your piece is a causes.py sheet of the line readers' causes. Each cause is a "## <file> <n> (...)" heading, its sentence, then
one "- W" (wrong example) or "- R" (right example) line per pair: game, A -> B, the line as it is now (NONE = no line), the
network.py lines that made it, and the test cases with both cards ("cases n12 none"). CONFLICT in the heading = a case says the
opposite; a case written by Kaptain ("Kaptain" in its source) is his decision. Under the examples come both cards' rows, for
the wrong examples that are still open. The readers were often wrong. Decide each cause from the rows and the rules:
- REAL: the wrong examples are wrong (or the missed line should exist) and the cause is stated right;
- NOT REAL: the lines are right (a real combo), the reader misread a rule;
- PARTLY: some examples wrong, some right (move the right ones to Right examples);
- GONE: every wrong example already says "NONE" (a wrong-line cause already fixed).
A cause from a failing case ("(combo case cms..)", "(deck case ..)", "real-world combo") is the game's players' truth
(START_DATABASE.md rule 9): it is MISSED REAL unless a rule of LINE_RULES.md forbids that line in its own words; then write
"MISSED CASE WRONG: rule L<n> says <its words>" so the main chat shows the case to Kaptain. Never NOT REAL for a case.
A missed-line cause keeps "MISSED " before its verdict ("MISSED REAL"). Kaptain's own word, a known truth: "The Dreadway ->
Decimate is a combo that works." Think like a player: would a good player build these two cards together for this reason?
Verdict file: each cause ONE line, in exactly this format (causes.py reads it; it skips NOT REAL and GONE):
"N. VERDICT: one sentence why, with the rule (L-number). Wrong examples: A -> B, A2 -> B2. Right examples: A3 -> B3."
N is the cause's number from its heading, written alone at the line start (never the file name; numbers may repeat across files, the examples tell them apart); card names exactly as printed; "Right examples: none." when there are none. Then a
final line starting with "- counts:" (counts per verdict).
Reply with only the file path and the counts.

