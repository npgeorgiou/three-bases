FIXED: Cards that only create cards fed "play a unit in a lane" triggers (Angela, Agony) and cards that create into the hand fed a deck draw of created cards (King Eitri). Files: network.py, cases/network.tsv. Cases: see below.
- Cases added: the four after n428 (n429-n432).
- Rule change 1: the "whenever you play a card" makers block (~line 1714) is skipped when the kind is explicit and every card is of it (unit in Marvel Snap).
- Rule change 2: new deck_created_draw / deck_makers sets before the makes loop: "draw created cards from the deck" needs a maker that puts cards into the deck.
- Other games: any game where all cards are units and a trigger says "play a unit with a filter" loses the Blade Dance style maker lines; plain "play a card" is unchanged.
- pair.py checked: three wrong examples now NONE, Agent 13 -> Devil Dinosaur stays.
