FIXED: C2 - strength_readers counted the generic keyword rows (kill/stat_change "amount_stat strength it", origin uses_keyword/has_keyword) as the card's own text reading strength; they are now skipped. Files: network.py (strength_readers, ~line 1371), cases/network.tsv. Cases: n659-n662.
pair.py: Tactical Advantage->Toad Prince and Bone Talisman->Kikimore Stalker now NONE; Target Practice/Squire->Knight-Errant and Squire->Redanian Knight unchanged.
C3-C9 have other reasons (kill triggers, keyword-given, summon, move), not covered.
Note: Imposter -> False Ciri is NONE before and after my change (case n614 line fails); not caused by this fix, another site.
