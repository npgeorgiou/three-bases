FIXED: A mana count that must be zero or at most N ("no unspent mana", Wiccan) was made a need fed by gaining mana; refs.py now skips it like the event counts. Files: refs.py, cases/network.tsv. Cases: n444, n445, n446.
- Shows only after the main chat's rebuild (refs.py); not checked by pair.py (Herbie -> Wiccan still showed before the rebuild).
- Ghost-Spider -> Galactus was already NONE (earlier fixer's same_lane skip).
- Any card with a "count le/lt/eq 0" test on mana, secondary resource, gem or lane resource loses its "gain" line, in every game.
- Counts with "ge"/"gt" are unchanged (Djinn -> Jim Hammond Human Torch stays).
