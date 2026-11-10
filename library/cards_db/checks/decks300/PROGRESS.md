# Decks to 300 per game (Gwent, Stormbound, Faeria, Runeterra, Duelyst), 10 Nov 2026
Sources fetched in the built-in browser (the workspace cannot reach the sites); scripts here read the pick files.
- Stormbound: done, stop. Stormbound-Kitty is the only deck source: 119 featured + 72 tournament + 19 guide decks = 207 different, 186 after the 80% rule.
- Duelyst: done, stop. duelspot.com legacy decks: 499 pages, only 107 have an import code with 40 cards (the rest are images); reddit is blocked in the browser.
- Faeria: faeria.com hub, all 5,400 deck ids read: 3,890 full decks, 1,131 with 2+ likes after the 80% rule. faeria_pick.txt = 275 picked by colour and year; plan3.py trims to 221 (after dropping decks too close to the 79 already in decks.tsv). All card codes known.
- Runeterra: masteringruneterra.com, all 1,120 posts read: 4,438 deck codes, 1,892 after the 80% rule. rt_pick.txt = 296 picked by regions and year; plan2.py takes 200. One code in the file is broken (dropped); 4 card codes unknown to the library (04PZ002, 06BC019, 01FR048, 04PZ015): their decks go to Kaptain.
- Gwent: playgwent.com guide list read (51,000 guides, 6 factions, 2019-2026); 706 candidate decks fetched but lost when the browser went offline. Next: refetch, pick 270.
- Next: Kaptain approves the tables, then import, links.py, axes.py, commit, push, send factions/wheel-axes.html.
