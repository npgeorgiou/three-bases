STUCK: C89 (Hammond -> Ragh Nar Roog) is fixed in network.py (new block before "paying for big cards": an enemy mover feeds a card that puts a row-damage hazard on enemy rows; pair.py shows "moves an enemy unit into the row it hits"; case n653 added), but C91's Seagull -> Ragh Nar Roog stays NONE: Seagull only deals 1 damage, makes a card and summons itself when an enemy dies, so no card text of it feeds a row hazard and a generic "more units" line would break L1/L2.
Seagull -> Ragh (n586) still needs Kaptain's decision (keep the case or drop it as L2).
The Hammond block touches every game's cards that give enemy positions a keyword with row damage (33 cards in gwent only).
No rebuild run; pair.py shows the network.py change.
