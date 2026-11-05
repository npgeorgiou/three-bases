FIXED: Swarm and Apocalypse put themselves back (copy / return to hand) when discarded but made no discard for Morbius's count; network.py now lets such a card make "discarded" (comes back after it is discarded, to be discarded again). Files: network.py, cases/network.tsv. Cases: n506-n509.
- Any game: every card with "when discarded, I return/copy myself" now links to cards counting or waiting for discards (L10 enables).
- Checked with pair.py only; Swarm -> Dracula stays NONE, Blade -> Morbius unchanged.
- Cards that wait for "when I'm discarded" may now get this line too from such cards.
