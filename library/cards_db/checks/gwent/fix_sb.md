FIXED: Stormbound is back to 149 of 149 and Gwent stays at 259 of 278.

Case: n25 (Nu Bad Medicine, Ozone Purifiers -> Chaotic Pupil, "moving enemies changes who borders whom").
Commit: 0a47eb2 (fix2_C8), whose rule dropped every "moves" line to a card hitting units "next to it".
Change: in network.py that rule now skips only a hit on a chosen target (Seismic Capacitor, tpick == 'chosen'); a hit on all units that border it (Chaotic Pupil, tpick 'all') keeps its line.
