FIXED 22 cards, STUCK 5
Scripts: fixes/runeterra/v65.py, fixes/gwent/v86.py, fixes/sts1/v53.py (each run once; they rewrite the touched batch files with json.dumps default spacing, as v64 does).
1. Runeterra Flow (14 cards): condition keyword_condition Flow -> event_count played spell (category fast_spell/slow_spell/skill), mine, op ge n 2, span last_round (the existing 6/12 spells shape with the last_round span from vocab). No Flow condition is left.
2. Faeria Time of Legends, Faeria Compass of Gagana, Runeterra Volibear, Marvel Snap Cannonball, Runeterra Delve Into The Past: already right (the second effect has link "otherwise", the game's "if that failed" shape).
3. Faeria Exotic Pet: already right (position bordering my units with region not Green).
3. Runeterra Curious Shellfolk: the event had no object; now object = my card with category not champion.
3. Runeterra Anaakca: STUCK: needs "follower OR non-Champion Darkin"; no OR shape for filters exists in the records or vocab (current rows keep only "follower").
3. Runeterra The Poro King's Decree: STUCK: a deckbuilding rule, abilities is empty, nothing to hold a filter.
3. Gwent Stockpile: the Cooldown step had no target; now my units on the summoned unit's row (same_row) with region not Neutral.
3. Gwent Ship Ballista: already right (target is a unit in my deck with boost eq 0, i.e. non-boosted).
3. Into the Breach Beetle: already right ("non-Alpha" is only a comparison in the description, no effect uses it).
3. Slay the Spire Cursed Key, Matryoshka, N'loth's Hungry Face, Smoke Bomb: "non-boss" was lost; each ability now has if it_matches state not boss (shape of the existing boss condition).
3. Into the Breach "non-fatal", "non-liquid", "non-damaging", Runeterra "non-targeted", Gwent "non-status": not touched (no card listed to check).
4. Runeterra Restored Sun Disc: the can (no event) is now level_up on my board Ascended units, lasts permanent.
4. Runeterra Skirmisher: STUCK: no card of that name (only Skirmisher's Sabre, Brutal Skirmish; neither has "if it survived").
4. Runeterra Blood for Blood, Heroic Charge: STUCK: rows use link if_done (same as Dragon's Rage); vocab has no way to say "if it survived" for one step (links: and/then/if_done/otherwise/or/instead/for_each).
4. Gwent Whoreson Senior: single transform now has if Tribute not paid (as Blindeye Apothecary); a second ability spends 3 and transforms both neighbours. Note: Renegade Mage, Moreelse, Tamara Strenger still use the old if_done/instead shape.
4. Duelyst Flash Reincarnation: already right (given ability on played minion, next_time, cost -2 and damage 2).
4. Marvel Snap Incursion Event: already right (set_terrain of the lane, then can move for all cards there, next_round).
4. Slay the Spire Blue Candle: already right (Unplayable Curses can be played; on playing a Curse lose 1 HP and exhaust it).
