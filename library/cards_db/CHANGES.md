# Changes to shapes and values

Each change: date, what changed, the card that caused it, and which records were corrected.

- 27 Oct 2026: v1 of shapes (BRIEF.md) and values (vocab.tsv), drafted from 13 Runeterra cards and the concept tree.
- 27 Oct 2026: state values `combat` (damage origin; Swain level 2, non-combat damage) and `spent` (mana; Jack's level up).
- 27 Oct 2026, v2 (from the trial: 104 keywords, 143 cards): acts first_strike, double_strike, excess_damage,
  damage_reduction, strike_with (Quick Attack, Double Attack, Overwhelm, Tough, Formidable had no way to be said); events
  mana_spent, keyword_used (Teemo's Plant, Heimerdinger); x full (Regeneration), x sum with items (Lucian-type "or" counts);
  filter op in with vals/refs (Deny: "Fast spell, Slow spell, or Skill"); attr name_has (Crimson units, Storm Conduits),
  base_power, base_health; kind keyword, state positive (Evolve); regions own_regions, same_as_self (Allegiance);
  zone attached; cards and keywords named in a text but missing from the library become stub entries (Dauntless Vanguard,
  Spiderling, Living Shadow, Plant, Turret); rules 10-12 in BRIEF.md.
- 27 Oct 2026, v2: x listed (Empowered N: the number the card writes; Empowered corrected), state from_hand (Improvise).
- 27 Oct 2026, v2: x minus (Remembrance, "1 less for each"); rule 13 and test amount with cond key value: stat sums over events (Heimerdinger), one total over two events (Yasuo).
- 28 Oct 2026, v3 (from 284 reader proposals over batches 1-15, the recurring ones): acts give_ability (nested ability in
  the effect), give_random_keyword, give_type (effect key type), cost_set, max_mana_change, spend_mana, play_card; events
  challenges, supports, attack_token_gained, trap_activated; states new, multi_region, summoned_this_round,
  targeted_this_round; attrs damage, rarity (field rarity), countdown; x distinct; limit next_time; lasts next_card,
  unstated; picks highest/lowest with target key by; filter n may be an amount (relative to another stat); rule 14.
  Records marked unsure under v2 are re-read under v3 after all batches are in.
- 28 Oct 2026, v3: param except (Watcher: "leaving 3"); numeric filters accept op in with vals (Elnuk-type "cost 2 or 3"); null keys dropped from records; Tentacle is a card, Udyr's stances a name family (batch 17).
- 28 Oct 2026: normalize.py (from the first comparison of first and second readings, 200 cards): N1 create/summon of a named
  card drop the receiving player; N2 keyword use is keyword_action for action keywords and give_keyword for statuses,
  decided by the keyword's own record; N3 empty values dropped. Vulnerable's record corrected to a status (the enemy can
  challenge it). Applied to all records read so far (575 records changed).
- 28 Oct 2026: N4 in normalize.py (follower/champion are categories; redundant category unit dropped), from the judged disagreements; queries count a used or given keyword as doing what the keyword's record does.
- 28 Oct 2026: Path of Champions items excluded (exclude.tsv; 156 entries; their records moved to excluded/). pattern_check.py: plain wording (triggers, verbs, keywords named in the text) must show up in the record; 61 flagged cards re-read as fix_007.
- 28 Oct 2026: acts gain_attack_token, spend_mana, keyword_action, max_mana_change now cause attack_token_gained, mana_spent, keyword_used, mana_refilled (combo tests c34, c35 found them missing). Query layer flat.py, derived concepts, keyword concepts in vocab (field keyword), Can't Block record (keywords_stub.jsonl).
- 28 Oct 2026, v4: acts copy_keywords, remove_keywords, state negative (Zoe level 2, Adaptatron, Kai'Sa level 2, Husks: keywords passed between units had no value); rule 15 also requires the not-self filter for "another ally" (Petricite Broadwing). The 52 cards whose text speaks of keywords are re-read (fix_009).
- 28 Oct 2026, v5: flat_ref (refs.py): every way a card works with a happening, so one query finds all cards that care about it (Kaptain: "rewards an ally dying" found 15 of 48+ cards). States and zone discard get `causes` in vocab.tsv; BRIEF rule 17 (dead units are units in discard; Tossed is removed; Nautilus fixed). Case m81. CHECK files are made by check_table.py.
- 28 Oct 2026, v5 values (repeated needs of the 122 unsure cards): acts swap_stats, shuffle_stats, steal, unequip; event counts_down; span different_rounds; attr total_stats; states played_last_round, started_in_deck, has_subtype, subtype_not_on_board, shares_subtype_with_it, copy_of_it (Swapbot's Swap, Slotbot, Mercenary Manners, Fish Fight, Reaver's Row, Pantheon, Quietus, Zilean (level 2), Hate Spike, Poro Captain, Deck Hunter, Ingvar the Younger, Entrapment). Unsure cards re-read.
- 28 Oct 2026, v5: the unsure cards re-read (fix_010-012). BRIEF rule 17 also: Captured cards are zone removed; rule 18: a copy is act copy, never summon/create/attach of the original (Ornn, Frozen Tomb, Eye of the Ra-Horak lost copy in the re-read). Keywords-field entry "Missing Translation" is not a keyword (NOT_KEYWORDS in build_input.py: Riot's data has AuraVisualFakeKeyword there, no rule text).
- 28 Oct 2026, v6: params max, min; attrs right_of, does; state recalled_this_game (repeated needs left after the re-read: Howling Gale, Snip Snip Snip!, Crimson Pact, Children of the Forest, Senna). Those cards re-read (fix_013).
