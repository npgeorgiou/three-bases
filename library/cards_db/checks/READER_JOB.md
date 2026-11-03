You check lines between cards in a card database. Change NO file in the repo. Use exactly 4 tool calls:
1. Read /home/claude/three-bases/library/cards_db/START_DATABASE.md with offset 30, limit 79 (rules L1-L22: the owner Kaptain's decisions, including their exceptions; they decide, not your taste).
2. Read /home/claude/three-bases/library/cards_db/SYNTAX.md (how to read a card's rows).
3. Read your piece (below) in ONE call (limit 2000).
4. Write your findings file (below).
Cards are shown by their ROWS, which are correct (the card reading is done): judge only "given these rows, is this line right? is a line missing?". "(rows above)" = printed earlier in the file. Think like a good player of the game: would a player put these two cards together for this reason? A line can be right even when a rule seems to say no: check the rule's exceptions (e.g. L18 keeps a line where a card doubles what is there; Kaptain: "The Dreadway -> Decimate is a combo that works").
Report CAUSES, not single lines, one per line in this exact format (causes.py reads it): "N. CAUSE: the wrong thinking in one sentence, with the rule (L-number). Wrong examples: A -> B, A2 -> B2. Right examples: A3 -> B3." For a line that should exist but does not, start with "N. MISSED CAUSE:" and put the missing pairs under Wrong examples. 2-4 examples each, card names exactly as printed. Only what the rows clearly show; doubtful cases in a short "unsure" list. Then up to 5 lines that are clearly right.
Reply with only the file path and the number of causes.

Your piece:
