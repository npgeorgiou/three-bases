FIXED: draws that shuffle a card back (net zero) or draw by kind only no longer fill a hand a card reads, and a hand-size limit the keyword lists ("count le listed card in hand") is no need for a fuller hand. Files: network.py. Cases: n588-n594.
Two edits near the hand-size block (about line 2118-2145): `nodraw` set subtracted from the draw helpers, and a skip for op le/lt with n 'listed'.
Checked with pair.py: all six wrong examples lost "fills your hand"; Eventide Plunder -> Carlo Varese (create) stays.
Other games: any card with a "fewer than N (listed)" hand test, or a draw by kind plus shuffle-back, loses its hand-fill line.
Selective Mutation -> Geralt: Quen "draws it from the deck" (site 764) is another cause and stays.
