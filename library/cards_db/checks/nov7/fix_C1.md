FIXED: A card that transforms itself when its own stat or a count it reads is reached (Xolaani) now counts as a level-up, so Kayle -> Xolaani reads "gives it more power and health: helps it level up". Files: network.py, cases/network.tsv. Cases: n702, n703.
- Rule fix in network.py: level_abilities() adds transform-self abilities with a stat / amount_stat / event_count test; lines_of uses it; generic_use flag level_stat; the stat-help branch accepts it; the duplicate "(levels it up)" line is dropped.
- May touch every game: other self-transforming cards with such tests (Runeterra Spotted Toad, Minitee, Teenydactyl; Gwent Vildkaarl, Svalblod Fanatic, Letho) now get "helps it level up" lines and stronger weight.
- Needs rebuild to show in tables; only Kayle -> Xolaani checked with pair.py.
