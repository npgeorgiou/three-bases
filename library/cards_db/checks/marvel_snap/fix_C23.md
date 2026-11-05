FIXED: Absorbing Man's repeat names the On Reveal keyword in its IF (last card played), not in the repeat row, so the repeat site missed him; network.py now reads it from the IF too. Files: network.py, cases/network.tsv. Cases: n502-n505.
Same rule now also gives lines to any card of any marvel_snap-like game whose "repeat" has a last_card keyword IF (other games with last_card repeats).
Right examples Wong -> Odin and Odin -> Luna Snow stayed. Checked with pair.py; no records, refs.py or flat.py change.
Other keyword repeats in the IF now behave as Wong/Odin do (L21 Kept: every card with the keyword).
