FIXED: Kill lines came from a keyword given only to enemy rows (Naglfar Crew, Red Riders Frost) and from Consume on cards in the discard pile (Ghoul); network.py now gives the first side enemy and skips discard-pile kills. Files: network.py, cases/network.tsv. Cases: n637-n645.
Biting Frost, Aen Elle Aristocrat were already fixed by earlier fixes. Checked with pair.py; no record changes.
Other games: any card giving a keyword only to enemies whose keyword damage had no side, or killing cards in discard, loses its death line.
