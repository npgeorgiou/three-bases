# Gwent import, chat 1 (START_DATABASE.md Part 2)
- step 0 (research, data, words, rules, batches): done 5 Nov 2026
- step 1 readers: all done (keywords, batch_001..008, second_001), 6 Nov 2026
- step 2.1-2.4: done 6 Nov 2026. Re-read of 354 cards merged; fixes v75, v76; second reading judged
  (fixes/gwent/second_001.verdicts.jsonl): 32 corrected, 20 same meaning -> normalize N35; word check 0 open;
  rebuild done (Gwent lines 50,360 -> 80,425). Five text-less tokens added from gwent.one (supplement_gwent.py).
- Runeterra n34 already failed before this import (see START_DATABASE "State").

## Next
- Step 2 fix round DONE 6 Nov 2026 (reports checks/gwent/step2/: families, fix_1-fix_9, verify-verify3, deck_cases).
  Three rebuilds (check_all.py gwent) plus links/cases rerun after fix_9. Every other game's cases and lines unchanged
  (Runeterra 428 of 429 was already so in the baseline). Word check 0, text audit 0, link audit all explained.
  8 values added to vocab.tsv (Claude's, adjacent group agreed by Kaptain); 22+4 Gwent keyword meanings added.
- Chat 2 (Part 3) starts here. Gwent cases fail only where the explainer misses a guide pair: 21 network.tsv deck pairs
  (n545-n587) and 10 cases/decks.tsv rows dgw01-12 (25 gaps, step2/deck_cases.md). Real-world: 26 of 33 hold
  (misses: Nilfgaard cast_from_zone, control; Scoiatael ranged, ping, tutor; Monster swarm; Skellige aggro_tempo).

## Before step 2 (chat 2 continues from START_DATABASE.md Part 3 after it)
- Done 6 Nov 2026: Deck pairs (43, games/gwent.md, from 12 guide texts; 18 name none) -> network.tsv n545-n587
  (deck_pairs.py); combos.tsv cgw01-03; regions.tsv rgw01-30 (all pass); mechanics.tsv gw01-gw85, one per keyword
  (checks/gwent/mech_cases.md); run.py gwent and every step after its cases; realworld.py gwent (26 of 33 hold);
  design_questions.py; keyword -> concept list shown to Kaptain.
- Gwent cases: 135 of 174 pass. Failing: 22 deck pairs (n545-n587) and 17 keyword rows (gw: Storm, Frost, Fog, Rain,
  Disloyal, Patience, Deathwish, Bonded, Discard, Echo, Symbiosis, Reset, Armor, Crew, Spring, Predator, Infused; the
  records miss them, mech_cases.md). Real-world misses: Nilfgaard cast_from_zone, control; Scoiatael ranged, ping, tutor;
  Monster swarm; Skellige aggro_tempo. All go to chat 2 step 4 (lr_misses.md) as MISSED causes.
- Open from the rebuild: 3 word flags (patterns/gwent_flags.tsv), 16 text words without rows (audit_text.py), the
  link audit list (audit_links.py): judge each in chat 2. cases/decks.tsv has no Gwent rows yet (needs must phrases).

## Link audit explained
- Sandor de Baccalà, "nothing makes removed_from_deck (enemy)": drawing from a deck and shuffling into it is the game rule; no card makes it. Rows right.
- Aucwenn / Wandering Treant (check 9): the rows react to "Whenever you Spawn a Wandering Treant" (`summoned` with `card is Wandering Treant`) and give Vitality; the card is not given. Rows right; the check reads a `card is` of the event object as a gift.
- Elven Scout (trap_activated), Blood Money (exhausted), King Henselt (counts_down), Sea Serpent (keyword_used Rain/Storm), Cyrus Engelkind Hemmelfart, Eternal Fire Inquisitor, Procession of Penance, Adda: Striga, Lonely Champion (summon/create of tokens): fixed by `causes` in vocab.tsv (6 Nov 2026), see fix_6.md; to be confirmed by the next load.
- Check 10, old tags, 3 cards each read against the rows: summon, generate_cards (Spawn = create/copy/summon rows), graveyard (revive and banish from discard), tutor (play_card or summon from the deck), ping (damage), coin_economy (resource_gained, spend_mana), condition_count (counts and "if you played X this turn"), on_ally_play (played events, Assimilate): the rows show the mechanic in another form. cooldowns (Aedirnian Mauler, Cursed Scroll, Cargo: "Order:" with no Cooldown in the text): old tag wrong, left.
- Check 10, stat_condition (Cyprian Wiley "power 4 or less", Vigo's Muzzle "6 or less power", Alzur's Double-Cross and Yennefer: Conjurer "highest-power"): the rows hold it as a target filter (`strength le`) or a `highest` pick, not as an if row. Rows right.

## Chat 2 (Part 3), started 6 Nov 2026
Steps (START_DATABASE.md Part 3): 1 start · 2 the two checks, cut · 3 line readers · 4 cases by script, misses into
lr_misses.md · 5 verifiers · 6 the sheet · 7 fixers · 8 one rebuild · 9 last checks · 10 done.
- Step 1 DONE: links.py (all games), tb0.tsv (every game), before.tsv.
- Step 2 DONE: la.txt -> la_1-3, da.txt -> da_1-11.
- Step 3 DONE: 14 line readers, lr_la_1-3.md, lr_da_1-11.md (86 findings).
- Step 4 DONE: lr_misses.md (38: 21 deck pairs, 10 decks.tsv rows, 7 real-world), by misses.py.
- Step 5 DONE: vv_1-9.md. Step 6 DONE: causes_sheet.md (94 causes; CONFLICT ones go to Kaptain at the end).
- Step 7: fixers by group (fix_groups.txt, 46 groups; report fix_C<first cause>.md; each fixer runs pair.py first; check_all.py --no-load after every fifth; fixdone.sh gwent fix_C<k>). MISSED CASE WRONG (vv_7 2, vv_8 6) and CONFLICT C92-C94 go to Kaptain at the end.
- 7. Fixers: C1 FIXED; C3 STUCK; C4 FIXED; C8 FIXED; C11 FIXED;
