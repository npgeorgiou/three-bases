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
