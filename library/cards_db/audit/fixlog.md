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
lk73 (Sparkly Kitties -> Temple of the Mind): FIXED (the enemy-harm rule reads only a target the player picks).
old 16: FIXED for keyword and stat filters (Drakkar Skycaptain -> Airbot); a tribe filter stays a deck choice by Kaptain's ndu34 (Oakenheart -> Mechs), so Yordle Captain-like tribe lines remain.
old 25, rt 16 (Might -> Scorched Earth), rt 17: FIXED Overwhelm adds no unit damage (HELPS row removed).
old 28-29: PARTLY: a spell does not have the keyword it gives the enemy; Grotesque Gift -> Out Of The Way still says "changes your units' stats" (another rule, not found).
rt 1-3, 6, 8-13: FIXED one fact said once per pair (one_link topic()); rt 10 Akshan -> Warlord's Hoard kept.
rt 4: FIXED a keyword's work on others is the keyword's rule in boost_lines having() (Greathorn Companion -> Greenfang Warden).
rt 5: FIXED a second attack is no Nexus reach (fights_for); own Elusive/Overwhelm still reaches the Nexus for a champion's level-up (n12).
rt 14: PARTLY: keyword and stat filters fixed; tribe filters kept (ndu34); Rek'Sai -> Sharkling still a line (Lurk).
rt 18, 21: PARTLY: more damage to my own cards is no help (gives_lines); The Dreadway -> Darkwater Scourge still a line.
Kaptain 3 Nov 10:21: a unit that moves itself gives no line to cards that depend on positions; ndu42, nfa27 rewritten; Zealous Crusader -> Khalim's Prayer (real-world) accepted as no line.
rt 25: FIXED a made card must be the kind or the card the need asks (lines_of: "if I was created" is about itself, created category vs counted kind).
rt 28: FIXED hand counts with a cost filter take only helpers that bring such cards.
rt 29, old 34 (copies into deck): FIXED a copy with no use is no line (aimed).
rt 32: FIXED a harm on units never hits a landmark (lines_of kind check).
rt 40: FIXED "spells under 3 cost 3" raises costs: pays nothing (boost_lines, aimed).
rt 42: FIXED discards that draw again do not empty the hand.
rt 48, 51: FIXED (missed lines) copies put into play and champions summoned from anywhere set off summon effects.
rt 26, old 33: NOT FIXED: Kaptain's nst26 keeps "makes more cards to play" (Blade Dance -> A Thousand Cuts).
rt 33, old 16 tribes: NOT FIXED: Kaptain's ndu34 keeps help to a tribe (Oakenheart -> Mechs).
NOT REACHED (open for the next chat, in this order): old 17-24, 26-27, 30-32, 35-49, 51-55, 57-75, 77-91, 93-95; rt 19-20, 23-24, 30, 34-35, 37, 39, 41 (Fast part), 44, 46, 49-50, 52-53, 55, 57-61.
