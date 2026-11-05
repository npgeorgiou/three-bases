FIXED: A power read of an enemy unit, or of one named card, was fed by any power gain; now enemy reads get no line and a named-card read (Zombie Giant-Man's Zombie Hulk) only from a gain aimed at that card. Files: network.py, cases/network.tsv. Cases: n417-n421.
Change is at the "more power" site (network.py ~2036-2047), shown at once by pair.py.
Other games: any card that reads an enemy's power or one named card's power loses lines from generic power gains.
Right examples kept: Zombie Mister Fantastic -> Zombie Giant-Man, Excalibur -> Iron Man.
Not changed: the health site below (same shape) was not touched.
