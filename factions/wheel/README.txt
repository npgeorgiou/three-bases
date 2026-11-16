THE WHEEL CHAT'S FILES (factions/START_DESIGN-1-wheel.md has the steps)
STOPA.md        Stop A, for Kaptain: the 53 mechanics in plain words
STOP1.md        Stop 1, for Kaptain: index of STOP1-1..5.md, the 20 factions in plain words
themes.tsv      step 7: one theme per faction
tools.tsv       step 7: 2-4 tools per faction (mechanic, the tools it feeds, the cell-by-cell line, source)
board.tsv       the first round's step 7 (board versions), replaced by themes.tsv and tools.tsv
combos.tsv      step 8: every pair of factions rated on this board, with a test column for playtests
answers.tsv     step 9: the seven answers per faction
mechanics.tsv   the 53 mechanics: "I do X -> I gain from X", the library concepts that catch their cards, NEW RULE, size
arguments.tsv   joins with no strong library number, argued from this game's rules (Claude's)
PIPELINE.md     how every step was made (a record, not a to-do)
HANDOFF.md      the next chat's whole job: fix the links, then design the factions again; all decisions
work/           inputs and scripts: shapes.tsv (the 20 shapes), concept_fixes_*.tsv, newmech_verdicts*.tsv,
                assign.tsv, signatures.py, borrow.py, check_assign.py, make_stop1.py, the agents' prompts (combo_prompt.txt,
                answers_prompt.txt); radius_verdicts.tsv, mechanic_pair_verdicts.tsv and board_prompt.txt are from the first
                round and are removed (HANDOFF Part 2 step 0)
