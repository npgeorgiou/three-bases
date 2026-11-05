FIXED: A card that only copies keywords or gives unnamed abilities to others was matched to every need for one named keyword (given_keyword with no keyword on the maker side). Files: network.py (new vague_gift + one skip line in the makes/takes loop). Cases: n489, n490, n491.
- Other games: any maker with copy_keywords or give_ability (not on itself) and no named keyword loses lines to cards waiting for a specific given keyword (166 such cards, mostly Runeterra).
- Basic Arrow -> Mystique (give_ability on self) kept on purpose; case n474 stays.
- The "makes your units get..." lines of such cards to keyword-specific waiters will vanish after the rebuild.
