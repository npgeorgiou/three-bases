FIXED: Zero silences the unit I play ("it"), a row the line rule skipped; now silence on "it" is kept and links to cards whose own text stops themselves or my hand (Ebony Maw). Files: network.py (aimed_rows filter, use_of, new self_drawbacks). Cases: n494, n495, n496.
Other games: any silence on "it" (units) now links to cards with a self "can't play/attack/move/block" row; pair.py shows Zero -> Ebony Maw "silences it: its drawback is gone", Sauron -> Ebony Maw unchanged, Zero -> Hazmat/Silver Surfer/Brood none.
Full rebuild not run; other games' lines may gain similar silence links.
