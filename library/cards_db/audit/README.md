# Handover: fixing the verified causes (3 Nov 2026)

Kaptain asked (2-3 Nov 2026) for the line check of Runeterra, Slay the Spire, Faeria and Duelyst, then a fix of every error
by its cause. Runeterra is read and verified; the old round's causes of all 4 games are verified. Fixing is half done.
Read first: START_DATABASE.md, LINKS_PLAN.md step 3 with "Token economy" and "Lessons".

## Rules for this work (Kaptain, 3 Nov 2026)
- Fixes are made in the main chat, never by an agent. No agent starts without a fixed number of calls in its job text.
- A unit's own Flying, Dash, Jump, Charge or Celerity moves only that unit: it gives no line to cards that need to enter near the
  enemy or act around units (Ghost Dragon -> Lost Explorer, Dragonlark -> Vigilator: no line). A card that gives a move keyword
  to my units keeps its line (Syland Horsemaster -> Bomb Slinger, nfa21).
- The fixing chat does not start the checks of Slay the Spire, Faeria or Duelyst (LINKS_PLAN.md step 3): another chat does.

## Files
- `verdict_1.md`-`verdict_4.md`: the old round's causes (1-95; Faeria, Duelyst, Runeterra, Slay the Spire), each REAL / PARTLY /
  NOT REAL with wrong and right examples. `verdict_rt_1.md`, `verdict_rt_2.md`: Runeterra's causes (1-31 and 31-61).
- `fixlog.md`: what is fixed, how (which network.py function), what is partly fixed, and the causes NOT REACHED.
- `READER_JOB.md`, `VERIFIER_JOB.md`: job texts for the checks of the other games.
- `../pair.py <game> "A" "B" ...`: why one line exists (the network.py line of each reason). Use it for every cause.

## Done (3 Nov 2026)
- Fixed: see fixlog.md. Test cases n301-n342. All network.tsv cases pass except Stormbound csb09-csb13 (old, not traced).
- Pairs gone (new) against the table before the fixes: Runeterra 25,475 (5,776 new), Faeria 6,946, Duelyst 1,387, Slay the
  Spire 289, Stormbound 156, Into the Breach 90, Monster Train 45, Inscryption 4. Real-world: 237 of 261 (238 before: Zealous
  Crusader -> Khalim's Prayer is gone by Kaptain's 3 Nov rule; the other 23 misses are faction-label checks, not lines).

## Steps left, in order
1. Runeterra: the causes in fixlog.md "NOT REACHED, Runeterra" (16 left: wrong lines and missed lines).
2. Old round: the causes in fixlog.md "NOT REACHED, old round", in one pass. Check each with pair.py, decide from L1-L22, grep
   the card names in cases/*.tsv first (Kaptain's cases win), edit network.py, add one `none` and one `line` case per cause
   (next id n343). Run check_all.py --no-load after each group of about 5 causes.
3. Then `links.py`; save the table before the first fix (`dump_lines.py --table /tmp/tb0.tsv`) and diff after; `realworld.py`
   (237 of 261 must hold).
4. Rewrite the must-not cases whose reason no deck says any more (check_all.py lists them).
5. The new-method check (LINKS_PLAN.md step 3) of Slay the Spire, Faeria, Duelyst was not started (Kaptain: another chat).
6. Commit, push, `network_page.py`, load network.html with no errors, send it to Kaptain. Delete this folder when 1-2 are done.
