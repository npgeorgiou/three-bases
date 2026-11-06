# Gwent import, chat 1 (START_DATABASE.md Part 2)
- step 0 (research, data, words, rules, batches): done 5 Nov 2026
- step 1 readers: all done (keywords, batch_001..008, second_001), 6 Nov 2026
- step 2.1-2.4: done 6 Nov 2026. Re-read of 354 cards merged; fixes v75, v76; second reading judged
  (fixes/gwent/second_001.verdicts.jsonl): 32 corrected, 20 same meaning -> normalize N35; word check 0 open;
  rebuild done (Gwent lines 50,360 -> 80,425). Five text-less tokens added from gwent.one (supplement_gwent.py).
- Runeterra n34 already failed before this import (see START_DATABASE "State").

## Next (a new chat continues here; read START_DATABASE.md whole first)
1. Baseline: done 6 Nov 2026 (checks/gwent/baseline_cases.txt: all pass but Runeterra n34; `links.py`: cases/links.tsv lk96
   Vinemother -> Wyldenten already failed; line table baseline_tb.tsv, 31 MB, not in git).
3a. Decks: no source gives win rates per Gwent deck (leriohub, Dec 2025: no deck trackers); asked Kaptain whether to use
   decks top players climbed the Pro Ladder or won tournaments with. Full lists are on playgwent.com (needs a browser).
2. Growing numbers: done 6 Nov 2026 (v77, BRIEF line). The 167 was wrong: only 7 amounts were {"x": "unstated"}, 2 of
   them growing numbers (Keira Metz, Colossal Ifrit); the other 48 growing-number cards were already read. Left: 5 amounts
   no value says yet (Dol Blathanna Bowman rows between, Vivaldi Bank distance from top, Fucusya unused provisions,
   Caranthir: Golden Child Frost damage, Torres var Emreis: Founder provisions below the limit). Then `run.py gwent`.
3. Step 2.5 decks: 20 full decks (25+ cards, every faction), cases/decks.tsv, network.tsv, "Deck pairs" in games/gwent.md.
4. Step 3 cases: mechanics.tsv one row per keyword and trigger word (85 keywords), regions.tsv rows for the six factions,
   combos.tsv from guides. Gwent has only the 13 shared cases now.
5. Step 4 last checks (realworld.py gwent, design_questions.py), keyword -> concept list shown to Kaptain, one
   check_all.py gwent, State updated. Then chat 2 (Part 3, line check).
