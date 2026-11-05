FIXED: a card that merges (SP//dr) set off no "when merged" card because network.py skipped every self-maker -> self-waiter pair; a merge now also reaches the card it merges onto. Files: network.py, cases/network.tsv. Cases: n486, n487, n488.
- Only the "merged" event is exempt from the "each card about itself" skip (network.py ~line 600); also 'merge' in HELP_MAKES and 'merged' words in ACT/ACT_SELF.
- Other games: only cards with a merge act and a "when merged" trigger (Marvel Snap) change; Symbiote Spider-Man -> Peni Parker line also appears (right: it merges).
- pair.py checked: SP//dr -> Peni Parker and Man-Spider now lines; Peni -> Man-Spider stays none.
