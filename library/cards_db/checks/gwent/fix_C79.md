FIXED: Kaedweni Revenant (1-damage ping, effect when it kills) had no line from cards that leave weak units (damage) or put units in play; new kill_food_lines in network.py. Files: network.py, cases/network.tsv. Cases: see tail of cases/network.tsv (4 new line cases, after n645).
Rule change, so pair.py shows it at once: all four examples (Redanian Secret Service, Sabrina Glevissig, Philippa: Blind Fury, Vernon Roche -> Kaedweni Revenant) now give a line.
May touch other games: any card with an activated 1-damage ping and an own "when I kill" effect gets lines from any non-1 damage card and any card that summons or plays my units.
Possibly too wide for decks with many summoners; not checked beyond the four examples.
