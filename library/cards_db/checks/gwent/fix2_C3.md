FIXED: a plain damage to one chosen unit no longer makes "leaves weak units for its kill" (kill_food_lines now takes only damage on all or random targets). Files: network.py, cases/network.tsv. Cases: n663-n668.
Covers C3 and the "hurt my own units" half of C4 (Void Seeker/Noxian Fervor -> Parrrley); gwent wrong examples were all still wrong before the fix.
Not fixed: "gives it units to kill" from summon/play_card (Coup de Grâce, Waylay, C4 Magic Compass) remains; it is a different branch and cases n646/n649 (Claude's) say summons feed a kill ping.
Seismic Capacitor line from Hydraulic Lifter ("moves enemy units...", site 696) is C8, untouched.
May touch: Kaedweni Revenant-type kill-trigger cards in every game when the feeder only has a chosen-target hit.
