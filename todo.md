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
10. **Library improvements.** The open work, in order, is the list at the end of `library/README.md`.
11. **Redo the five new factions** (Kaptain, 3 Nov 2026: "0 imagination, 0 network check"). Follow START_DESIGN 2b, one faction at a time. His points:
   - Projectiles: only defence, Immobile, damage from their text; cost counts that the player pays twice (place, then throw).
   - Pioneer and Wayside Shrine almost the same; Spell Conduit and Star Seer the same effect; Spark of Yesterday and Twin Novice give the same result at the same cost.
   - A 1:0|5 Immobile is too big on defence. Sleeper follows the curve but has a drawback.
   - Sapper in a deck that cannot move him to the enemy camp; "Walls and Sappers" deck has no network check. Siegework has 2 Push keywords with nothing using Push.
   - "Enemies get -1 strength this round" and "can't move or attack this round" are weak in this game.
   - Siegeworks and Monoliths: no mechanics joined, only buffs and damage. Echoes: one recipe (echoes, moments); look in the library for copies and ephemerals. Wanderers: Outrider on almost every unit breaks the board; rare only.
   - Arcanists: why Arcane Missiles hits the enemy with the least defence; more imaginative spells and spell/unit play; Dean of Battle Magic (melee buffs) does not fit.
   - Remove all flavour text. The 5 special units per faction get a special symbol, maybe a gold border.
10. **Old factions' rules code.** Tagma, the Horde, the Exanimati and the five factions of 3 Nov 2026 were removed from the game (4 Nov 2026, Kaptain: "remove old factions"); the rules code written only for their cards (per-card abilities in abilities.js, TACTICS in tactics.js, Exanimati death rules, Ogre Thrower, Link, Revenant, Plague...) is still in src/game/js/rules/ and no card uses it. Remove it in one refactor, keeping what fx.js uses (spawn, kill, auras, strikes).
11. **summary/ for the seven factions.** summary/ still describes the removed factions; the seven factions, their keywords and the new rules (factions/11-seven-factions.txt) go into summary/ when Kaptain asks to save the summary.
12. **Kaptain's review of the seven factions (4 Nov 2026, evening). Do these in this order, one faction at a time per chat.**
   - Each faction is finished only when `python3 tools/design_gate.py <letter>` prints PASS (all seven fail now: no library files, no src/tv/champion fields, 101-111 cards, same cards, spell shares, hovers; the crash fails play).
   - Crash (game and scenarios): `debtCost` in src/game/js/rules/exanimati-death-plague-discard.js reads the removed card `debt`; remove it with the rest of item 10, then play a game and every scenario in a browser (puppeteer: start, mulligan, a few turns), not only smoke.js.
   - "The cost->stats budget is correct, and should be followed": undo the +1 / -1 defence changes of 4 Nov (commits "Balance from Benchmark", "Rootkin -1"); balance with other fixes.
   - Spells/units: inside each faction, at cost 1-5 the split of spells and units is about the faction's own share at every cost level (Horologers: all over the place); high cost may be mostly units.
   - Every rule word on cards has a hover (e.g. Wind is written without [[Wind]]); no invented words: "break" (= dies) goes.
   - Card lists and the deck builder: inside a cost, sort alphabetically, not spells then units.
   - The 5 champions of each faction are shown as champions in the game (marked on the card).
   - Round-end damage everywhere is too strong; and too many cards do the same thing ("strike the nearest enemy", "+strength", "kill"): rebuild each faction from the library's card texts (read 30-50 cards of the closest real factions, write their play patterns), give each faction 5 really different ways to play, and add an effect-level twin check (same trigger + effect + target on more than 2-3 cards is a problem).
   - Library: the missing queries are Kaptain's to give to a library chat (Claude's list of 4 Nov 2026 evening). Every search covers all 8 games of the library, never only Runeterra.
   - Each faction has exactly 100 cards (the seven have 100-111: cut to 100).
