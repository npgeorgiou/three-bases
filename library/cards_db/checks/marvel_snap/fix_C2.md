FIXED: Cards whose only effect gives themselves away (Acid Arrow) no longer get repeat, replay or return lines (L5, drawback). Files: network.py, cases/network.tsv. Cases: n422-n425.
- New drawback_cards(c) (cards whose own effects are all donate) used in generic_use (drops played/summoned) and at the repeat sites (~line 755, BOOST repeat hits).
- Other games: any card whose whole text is "donate itself" (Stormbound convert-itself cards) also loses such lines.
- Checked with pair.py: Astral Projection and Toxin -> Acid Arrow now NONE; Beast, Ultron Mind Stone, Wong -> Absorbing Man stay.
