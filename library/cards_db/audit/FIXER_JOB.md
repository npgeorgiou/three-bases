# Fixer job (one fresh Opus agent per batch of verified causes; batches run one after another, never at once)

Work in /home/claude/three-bases/library/cards_db. You fix wrong lines in network.py by their cause, for every game.
1. Read START_DATABASE.md lines 30-108 (rules L1-L22) and LINKS_PLAN.md lines 17-31 (how lines are made). Nothing else
   of the docs.
2. Read your batch (the verdict lines named below; each says REAL / PARTLY, the wrong examples, the right examples).
   Fix only REAL causes and the wrong examples of PARTLY ones; the right examples must keep their line. NOT REAL: skip.
3. For each cause: see why a wrong example line exists with
   `python3 /tmp/claude-0/-home-claude/81579e71-d0e2-55ca-9dda-ca0416b34406/scratchpad/pair.py <game> "A" "B" ["A2" "B2" ...]`
   (games: runeterra sts1 faeria duelyst stormbound monster_train inscryption into_the_breach; prints the line and the
   network.py line numbers (site) that made each reason; about 12 s, several pairs per call). Read only the network.py lines
   around the site (sed -n, under 80 lines). Rows of a card: `python3 rows.py "<name>"` if needed.
4. Change the rule in network.py so the cause is gone for every card of every game with the same rows, not for the
   example names. Never add card names to the code. Keep the code style (one-line comment saying what a block is for,
   citing the L-rule; no history). Small Edit calls; never rewrite the file.
5. Check with pair.py: every wrong example is gone (or has the right words), every right example still has its line.
   If a fix would need a rule Kaptain has not given, or breaks a case written by Kaptain (grep the card names in
   cases/network.tsv; "Kaptain" in the source column), do not fix it: write it as OPEN.
6. Add test cases to cases/network.tsv (append; next free id nNNN, check the last id first): per cause one `none` row for a
   wrong example and, where there is one, a `line` row for a right example. Columns: id, game, deck (the two names joined by
   ", "), from, to, expect (none/line), why_not (for none: the wrong reason's words; for line: the kept words), source
   ("audit 2 Nov 2026: cause <n>, <short reason with L-rule>"). Only pairs you are certain of from the rows.
7. Do not rebuild, do not run links.py, check_all.py or other tests. Do not commit.
8. Append to audit/fixlog.md one line per cause: `<file> <n>: FIXED <what changed, network.py function>` or
   `<file> <n>: OPEN <why>` or `<file> <n>: ALREADY GONE`. Then reply with only "done <batch>, FIXED x, OPEN y".
Spend few tokens: no whole-file reads, few pair.py calls (batch pairs in one call).
