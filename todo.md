# Three Bases — TODO
Work not done yet. Kaptain's requests in his own words where he gave them. Remove an item once done or decided, and move what was decided into summary/ (or factions/ if it is only an idea).

1. **Crown rule.** "Only the player who holds the crown can attack": how that rule would change the game. Not yet discussed.
2. **File size.** The game file is large. Look at ways to shrink it.
3. **Playtesting.** Kaptain's task.
4. **Stronger Benchmark AI.** Tuning at the true depth takes hours of computing, or new evaluation terms for the new rules (tombstones, deaths in chains, abilities); needs Kaptain's go-ahead first. It has no hand-set ability values for the new cards.
5. **Strength/defence split for each unit.** Review every unit's stats (the split is Claude's, within the agreed budget).
6. **Mixed decks and base abilities.** Decks that use two factions (once each faction has a solid character and playstyle); base bonuses for the side holding a base.
7. **Artwork.** Unit glyphs are drawn by Claude, one per unit; proper individual artwork may replace them.
8. **AI lab.** Move it to the current card set, let its tournament tune the coded AIs on them, then retrain the learning AIs.
   - Planned for the retrain on the current cards: the cell layer (16 numbers per cell) may need widening (e.g. 24 or 32) as keywords and a "gained keywords" input per cell are added; replace the side-by-side cell combination with a convolution-style layer (each cell read with its neighbours) or attention (every unit looks at every other unit). Kaptain prefers attention.
   - Gained keywords (Plague, Revenant, Doctor Vessane, Embalmer, Embalming Rite, Hungering Mass) need a "gained keywords" input per cell in the AI network (one slot per keyword, in the shared cell layer).
9. **Faction candidates remake** (factions/ part 3, into the Part 6 format). Known fixes:
   - Every entry: separate the 3-5 core mechanics from the keywords that serve them; name owned signatures; add interaction level, lane-control cards, row 2-3 job, frequency bound on every trigger.
   - Draw: C14 Scout and C22 Decompose break the draw rule; C3, C16, C21 to check; C2 cantrips depend on the allocation table (all marked on their Self-sufficiency lines).
   - Card copying, card creation and deck search are spread over several candidates: settle them in the allocation table.
   - Supply: plain supply units (Supply +1) stay allowed in every faction (needed for self-sufficiency); supply as a mechanic (Treasury-style) is a signature. Claude's suggestion, not agreed.
   - Horde (E2): wins with its big units (measured), so self-harm must feed the big units.
   - Not yet applied: Blitz Ambush loop (Ambush, Fall Back, Reserves, Momentum), Bastion defence web (Cover, Unbroken, Brace, Answering Fire, Palisades), Pierce removed, Gravity as a swap of the enemy front unit with the one behind.
10. **Library: mechanics files for the games that miss one.** Every game needs `library/tools/mechanics/<game>.txt` (the mechanics its guides name, plus its rules and terms as `# term:` lines with their source), which the reading request and `coverage.py --mechanics` use. Missing for: darkest_dungeon, duelyst, gwent, hearthstone, hs_battlegrounds, marvel_snap, mtg, runeterra, shadowverse, sts1, sts2, wh_40k_10e, wh_aos_4th, wh_bloodbowl3, wh_killteam, wh_underworlds.
