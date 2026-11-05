You fix ONE verified cause of wrong or missing lines in a card database (START_DATABASE.md Part 3 step 7). At most 30 tool
calls in all; count them. At call 25 stop changing things and finish: undo a half-done edit, write the report. Commands run from /home/claude/three-bases/library/cards_db/.
1. Read LINE_RULES.md (rules L1-L24, the owner Kaptain's decisions; they decide, not your taste) and SYNTAX.md.
2. Read only your cause's section of the sheet (path and cause number C<k> at the end; Grep "^## C<k> ", then Read with
   offset/limit): its sentence, its examples with the lines as they are now, the
   network.py lines that made them, the cases, and both cards' rows. That is all you need; look nothing else up except the
   code lines the sheet names (Read with offset/limit, under 80 lines at a time).
3. Find the cause in one sentence: is the data wrong (rows that disagree with the card's words) or the rule (rows right, line
   wrong)? Fix it once, for every card and every game it touches:
   - data: a script fixes/<game>/vNN.py (next free number, safe to run twice, by a rule over the texts, never card by card;
     copy the form of the newest one there), run it once;
   - rule: the smallest change in the code line the sheet names (network.py, refs.py, flat.py), with a one-line comment
     saying what it is for.
   A new vocab value: a vocab.tsv row (date and reason) and a BRIEF.md line.
4. Check with `python3 pair.py <game> "A" "B" ...` (all the examples in one call): the wrong examples must change, the right
   ones must stay. pair.py shows a network.py change at once; a change to records, refs.py or flat.py shows only after the
   main chat's rebuild, so check those with one short python over the changed records instead, and say so in the report.
5. Add cases to cases/network.tsv (append; the next free id is one above the last nNNN): one `none` (or `line` for a missed
   cause) per wrong example you checked, one `line` per right example, game, deck as "A, B", source "Claude <date>, line
   check: <why in a few words>".
Never: run.py, check_all.py, links.py or any rebuild; git; edits to files your fix does not need; a fix for one card only;
more than two tries. If after two tries the examples do not change as they should, undo your edits and stop.
Write your report (path at the end) before you reply. Its first line is exactly one of
"FIXED: <the cause in one sentence>. Files: <files>. Cases: <ids>."
"STUCK: <what you tried and what pair.py showed>."
"CONFLICT: <the case or rule that says the opposite>."
then at most 5 lines: what else the change may touch (other games, other reasons). Reply with only the report's first line.
