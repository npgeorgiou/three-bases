You check lines between cards in a card database (one game's piece of a line check). Change NO file in the repo. Use exactly
4 tool calls:
1. Read /home/claude/three-bases/library/cards_db/LINE_RULES.md (rules L1-L24: the owner Kaptain's decisions, with their
   exceptions; they decide, not your taste).
2. Read /home/claude/three-bases/library/cards_db/SYNTAX.md (how to read a card's rows).
3. Read your piece (path at the end) in ONE call (limit 2000).
4. Write your findings file (path at the end).
Cards are shown by their ROWS, which are correct: judge only "given these rows, is this line right? is a line missing?".
"(rows above)" = printed earlier in your piece. Think like a good player of the game: would a player put these two cards
together for this reason? Check a rule's exceptions before calling a line wrong ("The Dreadway -> Decimate is a combo that
works"; L24: anything that helps a level-up condition is a line).
Report CAUSES, not single lines. Each cause is ONE line in exactly this format (causes.py reads it):
"N. CAUSE: the wrong thinking in one sentence, with the rule (L-number). Wrong examples: A -> B, A2 -> B2. Right examples: A3 -> B3."
A line that should exist but does not: "N. MISSED CAUSE: ..." with the missing pairs under Wrong examples. 2-4 examples
each, card names exactly as printed, pairs separated by ", ", each list ended by "."; "Right examples: none." when there are
none. Only what the rows clearly show. After the causes, lines starting with "- ": doubtful cases ("- unsure: ..."), then up to
5 lines that are clearly right ("- right: A -> B").
Reply with only the file path and the number of causes.

