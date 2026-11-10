THREE BASES — FACTIONS
The game as it might become: planned factions, faction candidates, card and rule ideas, the design method for new factions, and rejected ideas. The current factions and their cards are in summary/ section 11.
Goal (AGREED, 11 Oct 2026): at least 100 cards per faction, usually more (3 Nov 2026); spells are 20% to 50% of a faction's cards, depending on its profile.
Work plan (AGREED): step 1, faction candidates from the inspiration library (part 3), discussed at length; step 2, the list of factions to use, then their cards.


Files (lines, then contents). Read only the file a task needs; find lines across files with: python3 tools/find.py doc <text>

START_DESIGN.md                   141  START HERE for every chat that uses the library (faction and card design, every question to the library): the thinking process, NEVER DO
START_DESIGN-1-wheel.md            27  its part 1: the wheel chat, the first step: a high-level design of 20 factions based on the wheel
START_DESIGN-2-rules.md           114  its part 2: setup, this game's rules for design, the design rules
START_DESIGN-3-checks.md           71  its part 3: Kaptain's checks, self-critique, library search, before sending
START_DESIGN-4-asking.md          105  its part 4: how to ask the library, the shape of an answer, searching wide, thinking like a player
LESSONS.md                         17  lessons for future factions from building, playtesting and AI-testing (one entry per lesson)
3-candidates/00-notes.txt             9  3. Candidates: review notes, how the list was built, terms
3-candidates/E1-tagma.txt            18  E1. TAGMA — the Byzantine army (all-round)
3-candidates/E2-ashfang-horde.txt    12  E2. ASHFANG HORDE — the war host of fury and fire
3-candidates/E3-exanimati.txt        11  E3. EXANIMATI — the march of the unburied
3-candidates/C1-blitz.txt            22  C1. BLITZ — the relentless rotation (aggro + positional)
3-candidates/C2-arcanists.txt        21  C2. ARCANISTS — spells are the army (burn + card advantage)
3-candidates/C3-wardens.txt          21  C3. WARDENS — lock and answer (control)
3-candidates/C4-menders.txt          20  C4. MENDERS — refuse to die (sustain + fortress)
3-candidates/C5-legion.txt           21  C5. LEGION — strength in numbers (swarm + formation)
3-candidates/C6-titans.txt           20  C6. TITANS — few, huge, crushing (big units + ramp)
3-candidates/C7-treasury.txt         21  C7. TREASURY — save, then buy big (ramp + kicker)
3-candidates/C8-bastion.txt          19  C8. BASTION — the unbreakable line (fortress + punishment)
3-candidates/C9-ascendants.txt       20  C9. ASCENDANTS — grow in safety, then step forward (scaling)
3-candidates/C10-sunderers.txt       21  C10. SUNDERERS — break defence for good (defence-lowering + punishment)
3-candidates/C11-measurers.txt       20  C11. MEASURERS — exact numbers (precision + control)
3-candidates/C12-monoliths.txt       20  C12. MONOLITHS — never moves, owns its columns (every unit Immobile; Kaptain's idea)
3-candidates/C13-forge.txt           21  C13. FORGE — builds constructs, arms its units (assembly + items; Kaptain's items idea)
3-candidates/C14-wanderers.txt       20  C14. WANDERERS — decides which lane the fight is in (moving its own and enemy units betwee
3-candidates/C15-collision.txt       20  C15. COLLISION — the lane is a battering ground (forced movement)
3-candidates/C16-edicts.txt          21  C16. EDICTS — rewrites the laws of a lane
3-candidates/C17-dot-brokers.txt     19  C17. DOT BROKERS — changes who holds the dots (objectives + positional)
3-candidates/C18-thieves.txt         19  C18. THIEVES — sees and takes what the enemy has (disruption + infiltration)
3-candidates/C19-echoes.txt          19  C19. ECHOES — everything happens twice (copies + Place value)
3-candidates/C20-bonds.txt           19  C20. BONDS — paired units share everything (new idea)
3-candidates/C21-terraformers.txt    18  C21. TERRAFORMERS — shapes the cells (terrain; new idea)
3-candidates/C22-rotborn.txt         18  C22. ROTBORN — remains that feed growth (planned; part 2)
4-kaptains-ideas.txt                64  4. KAPTAIN'S IDEAS (11 Oct 2026, written while reading Runeterra's Noxus and Faeria's red 
5-card-design-method.txt            21  5. CARD DESIGN METHOD (11 Oct 2026; Claude's proposal after Kaptain's critique of the thre
6-faction-entry-format.txt          17  6. FACTION ENTRY FORMAT (11 Oct 2026; Claude's proposal from the agreed points in Part 5)
7-ideas-kept-for-later.txt          18  7. IDEAS KEPT FOR LATER (moved from summary/, 12 Oct 2026)
9-new-factions.txt                  41  9. THE FIVE NEW FACTIONS in the game for testing (identity, mechanics, specials)
8-rejected-and-cut.txt               6  8. REJECTED AND CUT (don't reintroduce without asking)
10-outside-design-guides.txt        79  10. What outside design guides teach (Hearthstone, Rosewater, Slay the Spire...) and what they mean here
11-seven-factions.txt               61  11. The seven factions of 4 Nov 2026 (clockwork, death, aggro, defence, spells, all-Immobile, WWI artillery): overview, new rules, checks
12-mechanical-wheel.txt             81  12. The mechanical wheel: designing 20 factions together; its radii and the agreed design process
13-wheel-measurement.txt            113  13. How the wheel's radii are measured (axes.py, wheel-axes.html) and how to redo it
designs/00-five-identities.txt      52  The five new factions from zero: overview, contrast, signatures, new rules needed
designs/ironfront.txt               90  Ironfront (World War I) stage 1: theme, mechanics, web, ways to play
designs/lodestones.txt              88  Lodestones (megaliths, all Immobile) stage 1
designs/glyphwrights.txt            96  Glyphwrights (Daoist talismans) stage 1
designs/brokers.txt                 95  Brokers (Prohibition gangs) stage 1
designs/hunters.txt                 91  Wild Hunt stage 1
designs/horologers.txt             118  Horologers (clockwork) stage 1: theme, identity, mechanics, groups, champions
designs/horologers-cards.txt       111  its card lines (made from the game by tools/design_cards.js)
designs/sunfeeders.txt             113  Sunfeeders (death, Mexica) stage 1
designs/sunfeeders-cards.txt       106  its card lines (made from the game by tools/design_cards.js)
designs/impi.txt                   111  Impi (aggro, Zulu regiments) stage 1
designs/impi-cards.txt             107  its card lines (made from the game by tools/design_cards.js)
designs/hospice.txt                109  Hospice Knights (defence, hospital orders) stage 1
designs/hospice-cards.txt          104  its card lines (made from the game by tools/design_cards.js)
designs/starpriests.txt            107  Star Priests (spells, Babylon) stage 1
designs/starpriests-cards.txt      103  its card lines (made from the game by tools/design_cards.js)
designs/rootkin.txt                107  Rootkin (all Immobile, living forest) stage 1
designs/rootkin-cards.txt          102  its card lines (made from the game by tools/design_cards.js)
designs/longguns.txt               112  The Long Guns (World War I artillery) stage 1
designs/longguns-cards.txt         103  its card lines (made from the game by tools/design_cards.js)
designs/benchmark-seven.txt         40  Benchmark report of the seven factions (win rates, cards never played)
removed/                                The removed factions (Tagma, Ashfang Horde, Exanimati): their summary card files, and
                                        their rulings, keyword values and texts and premade decks (rulings-keywords-decks.txt)

==================================================================
1. CURRENT FACTIONS
==================================================================
In summary/ section 11 (the game as it is now).

==================================================================
2. PLANNED FACTIONS (not designed yet)
==================================================================
THE ROTBORN: decay is transformation, not destruction ("Nothing dies. It becomes something else."). Mold, mushrooms, moss, swollen roots, decaying flesh, and rats (growth, spread, disease); magic of blight, fungal growth, regeneration, decomposition; spore priests, plague beasts, corpse-fungi, rot giants. Twist: their diseases can heal ecosystems and restore dead soil. Leaving remains behind is its main thing (AGREED, 10 Oct 2026): its units leave remains (e.g. Fungal Corpses: 0|0, Immobile, destroyed by any damage, holding dots) that its other cards feed on, sprout from or spread through; what remains do is to be designed. Moldering Pilgrim (2 - 2|2, leaves a Fungal Corpse) may return here. Has Blight too, so it synergises with the Exanimati.
Other planned factions: a defence-heavy one, a supply-heavy one, one that mostly lowers defence, a precise one that fine-tunes (its X effects let the player choose exactly how much supply to spend), possibly a cold/ice one (Freeze was removed from the Exanimati), and one whose units are all Immobile (Kaptain's idea). Items (cards attached to units; Kaptain's idea) are in Part 7.
