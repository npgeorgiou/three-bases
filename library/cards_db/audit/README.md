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
- Fixed: old causes 1-11, 13-16, 25, part of 28-29; Runeterra causes 1-6, 8-14, 16-18, 21 (partly where fixlog.md says).
  Test cases n301-n322, n325, n326. All network.tsv cases pass except the ones below.
- Pairs removed against the table before the fixes (links.sqlite, all lines that can exist): Runeterra 21,882 (83 new),
  Faeria 6,809, Duelyst 1,281, Slay the Spire 130, Stormbound 107, Into the Breach 90, Monster Train 39, Inscryption 4.
  Faeria's drop is mostly the move rule above.

## Open, for Kaptain to decide (his own cases now fail under his 3 Nov rule)
1. ndu42 (Kaptain: "Celerity moves the Lion next to enemies", Azurite Lion -> Holy Immolation) and nfa27 (Kaptain: Battle
   Toads' Jump frogs reach the enemy wells) fail: under his 3 Nov rule a unit moving itself gives no line. Ask him which holds.
2. Real-world case Zealous Crusader -> Khalim's Prayer (Faeria guide combo) broke for the same reason (Crusader's own Charge).

## Steps left, in order
1. Fix the causes NOT REACHED in fixlog.md, in one pass: decide each from L1-L22, check with pair.py, edit network.py, add one
   `none` and one `line` case per cause (cases/network.tsv, next id n327). Then `links.py`, `dump_lines.py --table` and
   `--diff /tmp/tb0.tsv` (make tb0 first from the commit before 3 Nov's fixes if /tmp is empty), `check_all.py --no-load`,
   `realworld.py` (237 of 261 hold now; 238 before).
2. Rewrite the must-not cases whose reason no deck says any more (check_all.py lists them; START_DATABASE.md "State").
3. Commit, push, `network_page.py`, load network.html with no errors, send it to Kaptain. Delete this folder.
