# Gwent import, chat 1 (START_DATABASE.md Part 2)
- step 0 (research, data, words, rules, batches): done 5 Nov 2026
- step 1 readers: all done (keywords, batch_001..008, second_001), 6 Nov 2026
- step 2.1-2.4: done 6 Nov 2026. Re-read of 354 cards merged; fixes v75, v76; second reading judged
  (fixes/gwent/second_001.verdicts.jsonl): 32 corrected, 20 same meaning -> normalize N35; word check 0 open;
  rebuild done (Gwent lines 50,360 -> 80,425). Five text-less tokens added from gwent.one (supplement_gwent.py).
- Runeterra n34 already failed before this import (see START_DATABASE "State").

## Next
- Step 2 fix round (Kaptain, 6 Nov 2026: the import chat fixes every open item itself, no stopping to ask).
  Done: baseline (step2/baseline/), families (step2/families.md), keyword definitions check (step2/keyword_defs.md),
  fix_1 (v78-v81: Create, Discard, ignoring Armor), fix_2 (keyword case queries, 80 of 85).
  Running: fix_3 (new values for families 3, 4, 6, all games; Kaptain agreed the adjacent-group value).
  Next, one fixer at a time: fix_4 Frost/Disloyal rows, Gwent meanings for shared keyword names, the 3 backed definitions,
  RIGHT lines, word flags; fix_5 text-audit and link-audit RULE items 7-11, 15-19 and the Predator/Symbiosis code item;
  fix_6 link audit 10 (old tags) leads; then one rebuild (check_all.py), diff, every case passes.

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

## Link audit explained
- Sandor de Baccalà, "nothing makes removed_from_deck (enemy)": drawing from a deck and shuffling into it is the game rule; no card makes it. Rows right.
- Aucwenn / Wandering Treant (check 9): the rows react to "Whenever you Spawn a Wandering Treant" (`summoned` with `card is Wandering Treant`) and give Vitality; the card is not given. Rows right; the check reads a `card is` of the event object as a gift.
- Elven Scout (trap_activated), Blood Money (exhausted), King Henselt (counts_down), Sea Serpent (keyword_used Rain/Storm), Cyrus Engelkind Hemmelfart, Eternal Fire Inquisitor, Procession of Penance, Adda: Striga, Lonely Champion (summon/create of tokens): fixed by `causes` in vocab.tsv (6 Nov 2026), see fix_6.md; to be confirmed by the next load.
- Check 10, old tags, 3 cards each read against the rows: summon, generate_cards (Spawn = create/copy/summon rows), graveyard (revive and banish from discard), tutor (play_card or summon from the deck), ping (damage), coin_economy (resource_gained, spend_mana), condition_count (counts and "if you played X this turn"), on_ally_play (played events, Assimilate): the rows show the mechanic in another form. cooldowns (Aedirnian Mauler, Cursed Scroll, Cargo: "Order:" with no Cooldown in the text): old tag wrong, left.
