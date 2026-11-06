# Fix 3 (gwent step 2, families 3, 4, 6; 6 Nov 2026)
Script: fixes/gwent/v82.py (the only one; no other game had a card needing these values).

## Values added to vocab.tsv (all "Claude's value, agreed by Kaptain 6 Nov 2026")
- position adjacent_group: several units touching each other in one run (n chosen form a run); not `sides`.
- state applied_this_turn: a status or row effect applied during the current turn.
- attr unused_provisions: provisions of the limit not used by the deck (x stat, of the player).
- attr provisions_below_limit: gap between the limit named in the text and the provision cost, summed over of.
- attr distance_from_top: places from the top card of a looked-at deck.
- attr rows_between: rows that separate a unit from the card itself.
- x event_total: sum of the amounts of an event over a span.
- span last_5_enemy_turns: the last 5 enemy turns.
Reused: lasts this_round (Madame Luiza), limit next_time + link instead (Leticia).

## Cards changed: gwent 15, other games 0
- Family 4 (7): Commander's Horn, Colossal Ifrit, Golden Froth, Drummond Warmonger, Salamandra Mage, Temple Guard (was all units beside self, now 3 chosen in a run), Armorer's Workshop (no filter before). Other games: all "adjacent" hits (Faeria, Inscryption, Into the Breach, Marvel Snap, Duelyst "in a row") are beside one thing, an area, or a line of tiles; none picks several units that must touch. Per game: gwent 7, others 0.
- Family 3 (3): Leticia Charbonneau, Aen Elle Aristocrat, Madame Luiza.
- Family 6 (5): Fucusya, Vivaldi Bank, Dol Blathanna Bowman, Torres var Emreis: Founder, Caranthir: Golden Child.
- Other games for the new values' meanings: grep found none (Runeterra "next ... this round" already written its own way, left alone).

## Notes
- Madame Luiza: "next Tribute" is now `lasts this_round` only; the "next one only" is not in the rows (no key for it).
- Torres: the limit 10 is read from the card's own `cost le 10` filter.
- batch_002 shows 1 old problem (Hyena? id 756623: region 'Monsters'), not from this fix.
