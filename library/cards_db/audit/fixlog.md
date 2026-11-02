# Fix log (main chat, 3 Nov 2026). "old N" = verdict_1-4 cause N; "rt N" = verdict_rt cause N.
old 1, 4, 5: FIXED own move keywords move only their card (lines_of pick self, no self-move positional lines; boost_lines movers = helpers; grows: no mobile/put_movers). Kaptain 3 Nov: drop them all.
old 2: FIXED making land moves no unit (grows: land_movers = act move only).
old 3: FIXED moves onto my own land reach no enemy land (home_only(): lines_of, aimed, boost_lines).
old 6: FIXED General moves are not minion moves (lines_of: tpick self + mkind player needs a leader); keyword filters count for "ready all Ranged" (who list + keyword).
old 7: FIXED move help to a fight effect dropped (boost_lines: only strikes_nexus).
old 8: FIXED needs done by the enemy get no help (boost_lines by_enemy); rule_fighters only own text.
old 9: FIXED help in an ability that transforms is none (boost_lines move_rows).
old 10: FIXED given "when this is built" is about itself (gives rule: obj_pick not self). Disciple of Yggdra -> Architect kept.
old 11: FIXED a harm aimed by a filter with no side is for enemies (lines_of hit_abs).
old 12: NOT REAL: Path to Paradise costs 1 forest, 1 mountain (cost_text); lines kept.
old 13: FIXED own fight keyword feeds only the card itself (lines_of made_by fight_kw; boost_lines own_kw always skipped).
old 14: FIXED rule lines need no victim filter (Resonance Scythe); Frenzy feeds only enemy-side deaths.
old 15: FIXED card makers are no helpers (boost_lines having: acting without create/summon; counter is own). Tybaulk -> Snip Snip Snip! kept.
