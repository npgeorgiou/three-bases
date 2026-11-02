# Findings of the stopped check round (2 Nov 2026), and what is left of the check of 4 games

## Where these files come from
Kaptain asked for the line check of Runeterra, Slay the Spire, Faeria and Duelyst. Claude ran the OLD checks of
LINKS_PLAN.md step 3 (before the token limits): `links_audit.py <game>` (Check 1, the whole game: top 10 reasons, the 2% of
cards with most partners, the 2% with fewest, the 2% with none beside 50 cards of their faction, 50 random lines, 50 lines
of each of the 20 biggest reasons, the champions/Generals/legends) and `deck_audit.py <game>` (Check 2, per deck: top 5
reasons, 10 cards with most partners, 10 with fewest, 10 with none beside 10 deck cards, 10 random lines, 5 lines of each of
the 5 biggest reasons, special cards). Cards were shown by their TEXT. 16 readers (Opus) read pieces at once and used up
Kaptain's 5-hour limit; each was then told to write what it had found and stop.

Each file: the reader's piece, its causes (the wrong thinking, the rule it breaks, example lines), an unsure list and lines
checked as correct. File names: r = Runeterra, s = Slay the Spire, f = Faeria, u = Duelyst. Line numbers are of the old
output files, which are gone (the scripts changed); the causes and example lines stay valid, because no line was changed.

| Game | Check | Files | Read |
|---|---|---|---|
| Runeterra | 1, whole game | r1-r5 | about 58%: top reasons, most/fewest/no partners all; random lines partly; 6 of the 20 biggest reasons; champions A to Janna |
| Runeterra | 2, decks | r6, r7 | about 30% of the deck output |
| Slay the Spire | 1 | s1 | about 45%: parts up to the random lines all; the 20 biggest reasons partly |
| Slay the Spire | 2 | s2 | all |
| Faeria | 1 | f1, f2 | about 56%: all but the second half of the 20 biggest reasons |
| Faeria | 2 | f3, f4 | about 57% |
| Duelyst | 1 | u1, u2 | all |
| Duelyst | 2 | u3 | about 46% |

The files hold about 160 causes; many repeat across files (the same rule seen by several readers). They are not merged yet.

## Later files (2 Nov 2026, evening)
- `merged_old.md`: the 16 files above merged into 95 distinct causes. Its example lines are lines the OLD readers judged
  WRONG; many of those judgements were themselves wrong (Kaptain: "The Dreadway -> Decimate" is a combo that works).
- `merged_with_rows.md`: the same, with both cards' rows, the line as it is now and any test case under each example.
- `verdict_1.md`-`verdict_4.md`: each cause checked again against the rows and L1-L22: REAL 73, PARTLY 18 (which examples
  are wrong and which right is written there), NOT REAL 4. Fix only REAL causes and the wrong examples of PARTLY ones.
- `causes_a_runeterra.md`, `causes_d_runeterra_*.md`: the NEW check of Runeterra (rows, Sonnet readers).

## What is left (for whichever chat finishes the check)
1. Merge the causes of all 16 files into one list of distinct causes. Check each against the rows of its example pairs
   (LINKS_PLAN.md Lessons: call the line functions for that pair). Drop what the rows do not support.
2. Fix every remaining cause once, for every game, with test cases (LINKS_PLAN.md "Tests"); `links.py`,
   `check_all.py --no-load`, `realworld.py`.
3. (done) links_audit.py and deck_audit.py print the NEW checks (LINKS_PLAN.md step 3).
4. Run the new checks for the 4 games, one game at a time (Sonnet readers, findings saved as they go); fix what they find.
   The new Check 1 is needed for all 4 games (the old one read random lines, not every reason). The new Check 2 is needed
   for all decks of Runeterra, Faeria and Duelyst; Slay the Spire's decks were read whole by the old check, run the new one
   anyway for its no-partner part with rows.
5. Rewrite the must-not cases listed in START_DATABASE.md "State".
6. Commit, push, send Kaptain network.html (`network_page.py`). Then delete this folder.
