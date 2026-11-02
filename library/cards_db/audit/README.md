# Handover: the line check of Runeterra, Slay the Spire, Faeria, Duelyst (2 Nov 2026)

Kaptain asked for the line check (LINKS_PLAN.md step 3) of these 4 games, then a fix of every error by its cause, the
tests, a rewrite of the must-not cases in START_DATABASE.md "State", a push, and network.html sent to him.
Read first: START_DATABASE.md, LINKS_PLAN.md step 3 with "Token economy" (the method changed on 2 Nov 2026), SYNTAX.md.

## Done
- Runeterra is READ in full with the new method (rows, one judgement per reason and rule, all decks). Not fixed yet.
- An older round (card texts, random samples, before the token limits) read about half of all 4 games. Its causes are
  merged and verified: `merged_old.md` (95 causes; its example lines are lines the old readers judged WRONG, and many of
  those judgements were wrong: Kaptain, "The Dreadway -> Decimate is a combo that works"), `merged_with_rows.md` (each
  example with both cards' rows, the line as it is now, its test cases), `verdict_1.md`-`verdict_4.md` (each cause checked
  again: REAL 73, PARTLY 18 with the wrong and right examples named, NOT REAL 4). Fix only REAL causes and the wrong
  examples of PARTLY ones.
- Nothing is fixed yet in network.py; no line changed. Kaptain's case n300 (The Dreadway -> Decimate must stay) is added.

## Files
- `causes_r*/s*/f*/u*.md`: the old round's raw findings (merged into merged_old.md; keep only until fixed).
- Runeterra, new method: `causes_a_runeterra.md` and `causes_d_runeterra_1.md`, `_3.md`, `_4.md` (first pass of the new
  checks), `v3_causes_a_runeterra.md`, `v3_causes_d_runeterra_p2_1.md`-`_3.md` (the rest). About 77 raw causes, NOT merged
  and NOT verified yet.
- `READER_JOB.md`, `VERIFIER_JOB.md`: the job texts given to readers and verifiers (append the piece's path and the output
  file). `../audit_pieces.py`: `split` cuts a check output into pieces read in one call; `verify` adds rows, current line
  and cases under every example of a causes file.

## Steps left, in order
1. Runeterra: merge the 8 Runeterra files above into distinct causes (one Sonnet agent, as merged_old.md was made), then
   `audit_pieces.py verify <merged> <out>`, split it (`audit_pieces.py split`), and give each piece to a verifier
   (`VERIFIER_JOB.md`, a fresh Opus agent per piece; 4 tool calls each).
2. Fix in the main chat, never by an agent (LINKS_PLAN.md "Token economy"). Fix every verified cause once, for every game (old verdicts + Runeterra), in ONE pass: decide each from L1-L22 before
   changing code; one pair is checked with the line functions (LINKS_PLAN.md Lessons), never by a rebuild. Each fix gets
   test cases (cases/network.tsv: one line that must go, one that must stay). Before: `dump_lines.py --table /tmp/tb0.tsv`;
   after `links.py`: the diff, every gone and new reason group read (one line each). Then `check_all.py --no-load`,
   `realworld.py`. Report per game how many lines each fix removed and added.
3. Slay the Spire, then Faeria, then Duelyst, one game at a time: `links_audit.py <game>` and `deck_audit.py <game>`
   (they skip lines in cases/links_checked.tsv), `audit_pieces.py split`, one Sonnet reader per piece (`READER_JOB.md`),
   merge, verify, fix as in 2. 2 Nov 2026 sizes: whole-game checks about 6,000 (Slay the Spire), 8,000 (Faeria), 13,000
   (Duelyst) tokens; deck checks about 23,000, 56,000, 32,000.
4. After each game: `links_audit.py <game> --record`, so a rerun shows only new lines.
5. Rewrite the must-not cases listed in START_DATABASE.md "State" (their reason is said by no deck any more).
6. Commit, push, `network_page.py`, load network.html in a browser with no errors, send it to Kaptain. Delete this folder.

## How to keep it cheap (what this round learned; also in LINKS_PLAN.md "Token economy" and PROCESS.md)
- Scripts are free; reading costs. Check the printed token size before anyone reads.
- The main chat reads no check output itself. Readers do, each in a fresh agent; the main chat reads only their short
  verdicts. A long main chat is expensive: every tool call sends its whole conversation again. Start the fixing in a
  fresh chat when this one is long.
- A reader reads its whole piece (at most about 15,000 tokens) in one call, plus the rules and SYNTAX.md: 4 calls in all.
  Reading in small parts paid for the start of the piece again with every part.
- Judge each reason and rule once, with a few lines from different row shapes, not random samples.
- Readers judge by rows, not texts (a text is read differently each time). Readers are Sonnet; verifiers are Opus.
- Readers are often wrong: never fix from reader findings directly. Merge, then verify with a file that already holds
  everything needed (rows, current line, cases), built by a script.
- Save every finding to the repo as soon as it arrives.
