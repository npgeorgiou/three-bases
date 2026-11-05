FIXED: Power given to cards in hand or deck had no line to Black Panther, who doubles his own power; now it does. Files: network.py, cases/network.tsv. Cases: n461-n465.
Change: new power_doublers(); aimed_rows keeps "power to cards in hand/deck" rows; use_of gives the reason. Checked with pair.py (Okoye, Nakia now line; Wong, Odin stay; Okoye -> Zabu none).
May touch: any other game card that sets its own power from its power (32 cards have power=stat on self), and any card giving power in hand or deck to all cards (Marvel Snap).
New lines show only after the main chat rebuild.
