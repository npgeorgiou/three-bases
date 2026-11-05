FIXED: A buff on a unit already in play (Eye Of The Storm, Arena Mechacaster, Yordles in Arms) gave a line to Dashing Dandy, whose doubling goes off only on play, before any such buff; power doublers whose every doubling is on play now take only power given in hand or deck (Okoye -> Black Panther stays). Files: network.py, cases/network.tsv. Cases: n520-n524.
- Touches every game with an "double my power on play" card (Marvel Snap Black Panther-like cards): board buffs lose the line, hand/deck buffs keep it.
- w now also carries "zone deck" for deck givers (to_deck), used only by the new check.
- Earthshaker examples (rule rows, power read in play) unchanged, as intended.
