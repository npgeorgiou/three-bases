FIXED: C4: summoned or played own units fed a "when I kill" card even when its hit is one-time (Parrrley, Gregoire, Fissure Fist); now only a card with an activated 1-damage ping (Kaedweni Revenant) gets "gives it units to kill" from them. Files: network.py (kill_food_lines). Cases: n669-n674.
C5-C9 not covered (other sites: network.py 1532, 2731 for Seismic Capacitor, played/summon lines); Void Seeker -> Parrrley was already NONE from the C3 fix.
Still shown: Magic Compass -> Gregoire "plays it: its effect goes off" (site 742, other cause).
Cases for Revenant (n646, n649) still hold (pair.py checked).
Other games with the same kill_food shape (runeterra, into_the_breach) changed the same way.
