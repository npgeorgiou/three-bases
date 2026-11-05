FIXED: King Eitri's "draw created cards from the deck" was fed by deck makers found only by on_zone, missing a made card put into the deck written in eff_zone (Shadowlands Daredevil, wrongly dropped); hand-creators stay dropped. Files: network.py, cases/network.tsv. Cases: n479, n480, n481, n482.
The earlier fixer's line 622 filter already removed the three wrong lines; I only repaired deck_makers (eff_zone like 'deck%').
Other cards that create into the deck now count as deck makers for any "draw created cards from the deck" need, in any game.
