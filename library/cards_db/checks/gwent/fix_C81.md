FIXED: A 1-damage chosen ping (Kaedweni Revenant, Redanian Archer) had no line to a card that sets an enemy to strength 1 (Vincent Meis); kill_food_lines now draws it. Files: network.py, cases/network.tsv. Cases: n651 n652.
Checked with pair.py: both examples now show the line; Philippa -> Revenant and Drakenborg -> Vincent stay.
Other games: any card with a chosen 1-damage ping and any card setting an enemy to strength 1 get this line (Gwent-style one-stat games only; Stormbound has no such pair known).
