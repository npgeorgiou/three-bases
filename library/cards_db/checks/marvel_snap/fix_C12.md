FIXED: Galactus's "destroy the other locations" was read as a kill of locations only; a data fix (fixes/marvel_snap/v70.py) adds a kill of all units there, like Destroyer, so Knull and Death get their lines. Files: fixes/marvel_snap/v70.py, read/marvel_snap/batch_001.jsonl, batch_002.jsonl, cases/network.tsv. Cases: n466-n469.
- Records changed, so pair.py shows it only after the main chat's rebuild (not checked with pair.py; pair.py before the fix showed Galactus -> Knull/Death NONE, Destroyer lines present).
- Also touches Worldship (terrain, not in decks): same kill of units added.
- Los Diablos Base ("ruin a random location") left alone: ruin is not destroy.
- Galactus now counts as a unit killer (board_wipe tag in flat.py, removal tags): true to its text.
