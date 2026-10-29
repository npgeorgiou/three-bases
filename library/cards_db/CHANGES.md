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
- 28 Oct 2026, v6: supplement (source.py, supplement_runeterra.py): 49 stub cards taken from Riot's set data and read (batch_023); BRIEF rule 19 (names: card, keyword, type, or name_has for families; never a reference for a word that is none) and the 31 cards using wrong stubs re-read (fix_014). connections.reasons() ranks every connection; explain() gives the most direct one (Hecarim -> Shark Chariot: start_attack -> attacks instead of kill -> dies via Spectral Rider).
- 28 Oct 2026, v7: Kaptain's definitions: Deep and Plant (keyword entries in supplement/runeterra_kaptain.jsonl, records in keywords_stub.jsonl; BRIEF: a condition that holds for the rest of the game = span this_game); names.tsv + normalize N6 (Cursed -> Curse, Ascended -> type, Stance -> name family, Release dropped); Stance Swap record rewritten (plays a chosen Stance spell on an ally); Drain is an action keyword (damage, then heal my Nexus that much), so its 10 uses are keyword_action. CHECK_20.md is one table (check_table.py). GUIDE section 5: confusions to avoid.
- 28 Oct 2026, v7 (word check): patterns/patterns.tsv holds every wording rule, each judged once by its meaning in the texts (reasons in the file); pattern_check.py masks all card names, skips judged flags (patterns/verdicts.tsv), --reread makes the batch with check_notes. Run 1: 66 flags; re-read fix_015; remaining 8 judged one by one (verdicts.tsv). Support: = event supports (keyword record and BRIEF rule 20). BRIEF rule 21 + normalize N7: a unit put into play attacking = summon/revive/copy then start_attack (Thresh (level 2) had lost it; 15 records unified). N8: a copy of a dead unit put into play is revive. States attacked_this_round, struck_this_round. Now 0 flags.
- 28 Oct 2026, v8: all 136 Runeterra cards the library lacked (champions such as Neeko, The Poro King, Elder Dragon) taken from Riot's data into the supplement and read (batch_024); missing keywords from Riot's glossary too (Assimilate). Values act grow, attr targets (repeated needs: Lulu, Give It All, Last Caress); BRIEF rule 16: deck-building wording has no effect; word check strips it (use strip). run.py and ask.py; PROCESS.md replaces GUIDE.md; raw.py and show.py removed (rows.py, check_table.py).
- 28 Oct 2026, v9 (Kaptain's check of CHECK_20): Mark of the Storm a keyword (Kaptain's definition; the spell recorded with it), Phased Moon Weapon = type Moon Weapon; BRIEF rule 22 (a card that summons a named card does not copy that card's effects; Brynhir Thundersong fixed); normalize N9 (action keywords that pick their own target carry no on: Toss was read as top of deck). check_table.py: legend, keyword rows. PROCESS.md: games the library lacks entirely.
- 28 Oct 2026, v10: PROCESS step 0 rewritten for games already in the library and new ones (exclusions, supplement only for missing cards, id blocks in source.py, keyword definitions from the game's glossary, the game's words mapped or added before reading, numbers per level as x per_level).
- 28 Oct 2026, v11 (Stormbound, pending Kaptain's check): game words mapped in BRIEF.md "Game words: Stormbound"; new values for board positions (attr position, field position, filters take "of"), strength, movement, spread, turn_start / turn_end / moves / attack_done, the five statuses, kinds unit_or_structure and anything, rarity legendary, test level, x range. load.py keeps card stats and Stormbound's extra unit types (Ancient, Elder, Hero); build_input.py gives them to readers.
- 28 Oct 2026, v12 (Stormbound): the card data is Stormbound Kitty's current card database (284 cards; it replaces the library's 2022 copy of 232 by card code, source.py); game words decided by Claude from the rulebook (Kaptain has not played the game); spawned "<type>" = the token card of that type ("Token Toads"), Nests = "Qordia’s Nest"; words that change by level = one ability per group of levels (test level). PROCESS: as few readers as possible (cost is per reader), approved records of each finished game become worked examples in BRIEF.md.
- 28 Oct 2026, v13 (Stormbound): values state single_use, attr level, positions first_empty_in_front / first_empty_behind (repeated reader needs); normalize N10 (strongest / weakest by strength in strength games), N11 (summon of a named card: an "on" with only its kind is dropped); query layer: effect destinations (flat_do to_kind, to_with, to_pick) and what a position is measured from (of: parts); combo reasons for effect targets, counts and structures; fix_001 re-read 36 cards; Dubious Hags' record fixed by hand (the Raven is spawned for the enemy: on side enemy); check_table.py shows what positions are measured from.
- 28 Oct 2026, v14: concepts for Stormbound's keywords (vocab keyword rows); concept rules for board positions (positional, adjacency, lanes, rows), drain as lifesteal, wider removal and tribal; per-level numbers show their level-1 value in the query layer and computed amounts their kind; ask.py takes a game, several, or all, with compare and both; combos only inside one game; PROCESS rule 9 (stored values are generic) and lessons from Stormbound; CHECK_20.md renamed CHECK_20_runeterra.md.
- 28 Oct 2026, v15: normalize N12 (a trigger on being given a keyword names it as its object filter; Yasuo, Fae Bladetwirler, The Tidedancer), act stun names Stun; concepts (vocab tree) for events, states and durations that games word differently; flat_ref has a concept column (cares/makes take concepts); concepts attack_gain, defence_gain by stat role; mechanics.py: together, feeds, fed, chains, deck (links only inside one game, added up by concept).
- 28 Oct 2026, v16: Stun, stun and stunned are attack_lock (Kaptain: Stun is can't attack, not can't act; region cases r60, r66, r100, r117 ask for disable or attack_lock); counting my mana is fed by mana gain (refs); card names stored without trailing spaces; mechanics.analyze and ask.py analyze (a deck: mechanics, links, needs, deck rules); PROCESS section "Writing data the same way in every game", BRIEF section "Same values in every game".
- 28 Oct 2026, v17: Stun, stun, stunned back to disable and Frostbite, frostbitten to attack_zero (Kaptain: Stun is can't act; Frostbite sets Power to 0); act strike causes dies, killed, survives_damage; deck_analysis.py replaces the deck counts with a plan in plain words (what cards make and which use it, level-ups, control, support, card flow, extra units, repeats, key cards, weak spots).
- 28 Oct 2026, v18 (Kaptain's definitions): Rally multi_attack, Vulnerable target_choice, Fleeting self_destruct, Landmark terrain, Can't Block drawback; Terrify deleted (Path of Champions; exclude.tsv by name, record in excluded/runeterra/terrify.jsonl); PROCESS: the keyword -> concept list is checked twice and shown to Kaptain before a game is done; NETWORK_DRAFT.md.
- 28 Oct 2026, v19 (Kaptain's check of CHECK_20_stormbound): act donate (giving my own unit to the opponent; normalize N13 turns steal on my own side into it: Faithless Prophets) and act random_one (an effect picked at random; BRIEF rule 8: Tegor the Vengeful was read as the player choosing); Temple of Space's teleport measured from the older copy.
- 28 Oct 2026, v20: PROCESS "Two chats on two games at the same time"; BRIEF: direction (steal / donate) and who chooses (choose_one / random_one / otherwise); reader scratch folders per game.
- 28 Oct 2026, v21: network.py (`ask.py <game> network "<cards>" | faction <name> | game [--json file]`): every card a node (level-up forms and made cards too), lines of 7 kinds plus levels into, weighted by rarity; central cards, chains of 2 to 4 cards, groups, loose cards. deck_analysis: supports happens in play by itself (EVERY_GAME); unknown happenings are said with spaces.
- 28 Oct 2026, v22 (Monster Train): supplement_monster_train.py (282 cards, champion paths, wiki glossary); keyword concepts
  (vocab keyword rows; a game can have its own row '<game>:<Name>' where a shared name means something else there:
  monster_train:Frostbite, monster_train:Rally; flat.py, refs.py, connections.py look it up first); game words in BRIEF.md
  (events combat_start, combat_end, eats, exhausted, kept_in_hand, resource_gained; acts eat, capacity_change, gold_gain,
  return_card; kind lane_resource; attr / param size; positions for lanes; zone exhausted; lasts this_run; x x_paid; test
  upgrade_path).
- 28 Oct 2026, v23 (Monster Train, repeated reader needs): x product, rarity uncommon, state boss, kind lane_resource_slot;
  BRIEF: doubling stacks is give_keyword with the count of stacks.
- 29 Oct 2026, v25 (Monster Train): the unsure cards fixed by rule (fixes/monster_train/v25.py: product amounts, doubling
  stacks, rarity pairs, non-boss, Echo slots, Sacrifice targets) instead of a re-read; Sacrifice's keyword record kills the
  card's target; normalize N14 (draw from the top: one form, all games); second reading judged by Claude: Hallowed Halls
  "to this floor" added; the rest same meaning.
- 29 Oct 2026, v26 (Monster Train): tokens Twin of Wax and Mote of Wax (wiki page Legion of Wax) in the supplement,
  recorded by Claude; act copy_upgrades (Legion of Wax, Twin of Wax).
- 29 Oct 2026, v27: an effect on the enemy side takes the enemy counterpart of its concept (movement -> forced_movement,
  return_to_hand -> bounce_enemy, transform -> polymorph; flat.py ON_ENEMY, all games). Monster Train results in RESULTS.md.
- 29 Oct 2026, v28 (all games): connections.py: a played card sets off a trigger only if it has the type or keyword the
  trigger asks for; filters match whole parts; returning my unit to hand links to its own "when played". refs.py: units
  picked by a keyword are fed by giving it. deck_analysis.py: keyword stacks, types, spells for spell triggers, Summon
  repeats only on cards with Summon, combat start/end and end-of-turn holding are not weak spots. load.py: a card using a
  trigger keyword that acts by itself has it. Cases: decks.tsv (guide decks), mechanics mx01-mx03 for every game, guide
  pairs in combos.tsv.
- 29 Oct 2026, v29: normalize N10 for every game (strongest / weakest = pick highest / lowest by power, or strength);
  Monster Train combo cases only from guides (Claude's own text pairs removed); PROCESS.md rewritten: "How to work" first,
  lessons folded into the steps, guide decks as the benchmark.
- 29 Oct 2026, v30 (Kaptain's check of the deck networks; shared code, every game): what a card makes is kept to the kind it
  hits (damage to a base or Nexus is no unit dying, damage to a unit no Nexus damage: Reckless Rushers, Falling Star);
  "I've survived damage" / "when I level up" counts only what happens to that card (flat_if ev_obj_pick: Braum, LeBlanc);
  a stat a condition tests is fed by what changes it (enemy Nexus health: Darius); things picked by position are fed by
  moving units (Stormbound pushes); can't-be-blocked units hit the enemy player; first strikes deal damage; a card's own
  action keywords count as used (Lurk, Support, Evolve); vocab causes: move, swap -> moves, challenge -> challenges,
  capture -> keyword_used:Capture, keyword Predict -> predicts; normalize N15 (a planted card going off is trap_activated:
  Caitlyn); planted cards (Chime, Poison Puffcap, Flashbomb Trap, Mysterious Portal) are cards the planter puts in;
  keyword conditions (Plunder, Reputation, Nightfall ...) are the using card's needs in the network. flat_ref has obj_with
  and ref (the filter of the thing and the card made). Runeterra: 11 champions' level-up forms the library lacked (Bard,
  Jhin, Jax, Evelynn ...) taken from Riot's data with their links (supplement/runeterra_links.jsonl; source.py loads them)
  and read (batch_025).
- 29 Oct 2026, v31: the query layer gives a target "it" the side and kind of the target before it (flat.py); link audit
  (audit_links.py, in run.py), deck network cases (cases/network.tsv), 33 Runeterra keyword concept rows (Claude's, from
  Riot's glossary), BRIEF rules 23-25, PROCESS "Links the deck networks showed missing".
- 29 Oct 2026, v32 (Kaptain's second network check, every game): champion families never link to themselves; skills cast by
  units are cards in the network and count for "spells or Skills"; help lines (power, health, protection, Nexus hits, card
  creation for "different cards", through a made card for level-ups); self-feeding level-ups; given abilities; actor "me"
  (flat_if ev_actor_pick; refs actor_self for killing / dealing damage); "it" falls back to the event's object; "keyword in"
  filters split per keyword; N15 also turns keyword_used of Trap / Boon into trap_activated; Rally makes my units attack;
  combo search lines removed from the network; fixes/runeterra/v31.py (planted card in counts, "<Keyword> me");
  cases/network.tsv n26-n42; PROCESS "Think like a player"; page: curved lines, mechanics section, solid aim lines.
- 29 Oct 2026, v33 (Kaptain: Tybaulk linked to too few cards; families swept in every game): help lines from effects that
  add to what my cards of a kind did (network.adders; Skills and keyword damage included), from lasting changes to all my
  cards of a kind (stat gifts say "gives it +1|+0"), from boosts to a status to its givers; lethal damage is no survival;
  cards made by description make their type; level-up forms read their stats; identical lines merged. Records by rule
  (fixes/runeterra/v33.py): "spells and Skills" includes Skills (28 cards), The Dreadway doubles damage, Janna counts cost
  reduced cards. vocab: event cost_changed (caused by cost_change, cost_set), state cost_reduced. PROCESS: how to map a
  keyword to a concept; BRIEF: Game words: Runeterra. decks.tsv: Janna Nilah and 27 Runeterra decks from deck codes
  (riwan.substack.com, Dec 2021), 22 Stormbound decks (stormbound-kitty.com deck ids). cases/network.tsv n43-n51.
- 29 Oct 2026, v34 (Kaptain: errors in every check; the whole design changed, all games): game rules as data
  (read/<game>/game_rules.jsonl, table game_rule, flat_ref origin game: every unit can attack and strike enemy units or the
  enemy player; not Immobile units); a strike's damage is on what it hits (flat_do to_side); strikes_nexus written one way;
  help as one table (network.py HELPS) instead of special cases; line kinds in players' words (stats, buffs, cheaper and
  more damage are "makes it stronger"; "changes how it works" only for rule changes; aimed lines say "can give it +2|+0");
  audit_text.py in run.py; fixes/runeterra/v34.py (Make it Rain hits the enemy Nexus too, "everywhere" zones); BRIEF
  reading rules 26-32; PROCESS "Why the first three games went wrong" and step 0.10; cases/network.tsv n52-n57 (cases now
  check the line kind).
