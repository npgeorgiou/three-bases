FIXED: Zombie Captain Marvel's "when activated" had no "self" (the data), so Fantomex's Activate keyword looked like a maker of it; fix v69.py (C5) already sets it, and the line goes away at the main chat's rebuild. Files: fixes/marvel_snap/v69.py (no new change). Cases: n475, n476.
- pair.py still shows the old line only because cards.sqlite is not rebuilt; read/marvel_snap has object pick self for card 8000739 (checked by reading the file).
- Checked every marvel_snap read row with "when activated" and no object: only keyword entries (Merge, Afflict, Discard, Move, Destroy) and Collapsed Mine remain, none with an "Activate:" text.
- The right example (Zombie Captain Marvel -> Fantomex) already shows "makes your units die".
