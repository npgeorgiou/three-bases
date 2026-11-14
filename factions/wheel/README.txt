THE WHEEL CHAT'S FILES (START_DESIGN-1-wheel.md), 14 Nov 2026. Made by library/cards_db/mechanics_wheel.py.
mechanics.tsv   step 1: the pool, 23 mechanics, each "I do X -> I gain from X" and the library concepts that catch its cards
measured.tsv    step 1: per mechanic its cards in the library, games with 10+, the biggest real faction's count (with the cards
                that make it happen; 30+ wanted), the real factions with the highest share, the radii it serves
links.tsv       step 2: per pair of mechanics, how much more often than chance the library links their cards (cards) and how
                much more decks heavy in one hold the other (decks); 1 = chance

Step 1, how the pool was cut (an agent read 8 cards per mechanic; its verdicts are kept in each line's concepts):
- Too small (under 30 in the biggest real faction), dropped: kill outright 27, stops 28, lanes 27, cells 22, junk and hand
  12, attach 20. Merged: revive + recycle; fight + forced attacks; ping + area; weaken + silence + transform; cheaper + in
  hand; pick + copy; onattack + strikes twice or first; overkill + strength 5+; guard + can't be targeted; movement + push.
- Copies of the seven factions, dropped: units die -> others grow (Sunfeeders' Toll), hit and survive -> act (Hospice
  Harden, Retaliate), heal (Hospice), units react to spells (Star Priests), round start (the library catches player turns,
  1 of 8 right). Reworded so they don't copy: sacrifice is a trade (an enemy dies), never a gain (Offering); tokens come
  from Place or Death, never round-end seeding (Rootkin Seeds); ping never at round end (Long Guns Barrage).
- Dropped as against this board: hidden reactions (traps are instant answers on the enemy's turn).
- Concepts narrowed where the agent found wrong catches (adjacency 1 of 8 right before, guard 1, discard 1, weaken 1).
