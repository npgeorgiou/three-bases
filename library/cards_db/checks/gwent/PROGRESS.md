# Gwent import, chat 1 (START_DATABASE.md Part 2)
- step 0 (research, data, words, rules, batches): done 5 Nov 2026
- step 1 readers: all done (keywords, batch_001..008, second_001), 6 Nov 2026
- step 2.1-2.4: done 6 Nov 2026. Re-read of 354 cards merged; fixes v75, v76; second reading judged
  (fixes/gwent/second_001.verdicts.jsonl): 32 corrected, 20 same meaning -> normalize N35; word check 0 open;
  rebuild done (Gwent lines 50,360 -> 80,425). Five text-less tokens added from gwent.one (supplement_gwent.py).
- Runeterra n34 already failed before this import (see START_DATABASE "State").

## Next
- Step 2 fix round (Kaptain, 6 Nov 2026: the import chat fixes every open item itself). Running: baseline (check_all.py
  --no-load, scratchpad), agent grouping checks/gwent/step2/findings.md into step2/families.md, agent checking 16
  suggested keyword definitions into step2/keyword_defs.md. Then fixers one family at a time, one rebuild.

## Before step 2 (chat 2 continues from START_DATABASE.md Part 3 after it)
- Done 6 Nov 2026: Deck pairs (43, games/gwent.md, from the guide texts; 13 guides name none) -> network.tsv n545-n587
  (deck_pairs.py); combos.tsv cgw01-03; regions.tsv rgw01-30 (all pass); mechanics.tsv gw01-gw85, one per keyword
  (checks/gwent/mech_cases.md); run.py gwent and every step after its cases; realworld.py gwent (26 of 33 hold);
  design_questions.py; keyword -> concept list shown to Kaptain.
- Gwent cases: 135 of 174 pass. Failing: 22 deck pairs (n545-n587) and 17 keyword rows (gw: Storm, Frost, Fog, Rain,
  Disloyal, Patience, Deathwish, Bonded, Discard, Echo, Symbiosis, Reset, Armor, Crew, Spring, Predator, Infused; the
  records miss them, mech_cases.md). Real-world misses: Nilfgaard cast_from_zone, control; Scoiatael ranged, ping, tutor;
  Monster swarm; Skellige aggro_tempo. All go to chat 2 step 4 (lr_misses.md) as MISSED causes.
- Open from the rebuild: 3 word flags (patterns/gwent_flags.tsv), 16 text words without rows (audit_text.py), the
  link audit list (audit_links.py): judge each in chat 2. cases/decks.tsv has no Gwent rows yet (needs must phrases).
