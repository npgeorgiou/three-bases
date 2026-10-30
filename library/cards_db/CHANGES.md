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
- 29 Oct 2026, v34 (deck read by Claude, 10 decks, all games): who does it kept in the query layer (flat_when actor_with,
  flat_if ev_actor_kind/side/with, flat_ref actor_kind/actor_with) and checked by the network; "non-combat" not fed by
  fighting; counted kinds of my cards fed by cards of that kind or that make one; "used a keyword" matches by keyword;
  label keywords a filter names are the card's keywords (load.py; vocab keyword Attack); help to the card that comes
  (object_help_lines); a card's effects on itself only feed needs its kind fits; hand-size needs; audit_text Rally only in
  Runeterra; PROCESS lesson 6 (query layer), steps 2.7 (text audit) and 2.9 (read 10 full decks), "Done when"; HANDOFF
  "Importing a new game: start here"; cases n58-n64.

## 29 Oct 2026, v35 (Faeria import, Claude's mapping from Abrakam's glossary and the faeria.com Keyword Rulings guide)
- Source: Abrakam's card export (library/tools/convert/faeria_*.csv); supplement_faeria.py writes 19 cards the library lacked,
  13 whose library text kept export markup or wrote two land icons as "lake lake" (now "2 lakes"), and glossary terms Wild,
  Fight, Teleport, Transform. source.py: a supplement entry now replaces the library entry with the same bare card code too
  (Faeria "45"; this also removed Runeterra's duplicate Dragon's Rage, 02IO007).
- Board ground: attr terrain with values land, ocean, prairie, lake, forest, mountain, desert, special_land, resource_well;
  act set_terrain (create, transform or destroy a land), event terrain_changed; position same_space; state empty; bordering
  also means the 6 hex neighbours; steal also takes a board space. flat.py: terrain and territory_trigger shape rules.
- Harvest: act harvest, event harvests (concept on_harvest, new). Combat: event fights (concept on_fight, new; start_attack
  causes it). Corrupt: event moves_onto (move causes it). Power wheel: event turn_option_chosen.
- Keywords: Gift on_play, Last Words death_trigger, Production turn_start, Combat on_fight, Corrupt territory_trigger,
  Activate activated, Flying / Charge / Jump / Dash / Aquatic / Teleport movement (Flying, Jump, Aquatic: Kaptain 26 Oct),
  Taunt taunt, Haste haste, Protection shield, Discover selection, Ranged Attack ranged, Divine immunity, Deathtouch
  deathtouch, Swallow banish (as Runeterra Capture), Wild cost_type, Fight attack_now, Transform transform. Regions Blue,
  Green, Red, Yellow, Neutral (Human), Pandora.
- refs.py: a game rule is skipped only for cards that can never do what that rule makes ("Can't harvest faeria" skips the
  harvest rule; "can only attack gods", a can't limited to some targets, skips nothing).
- read/faeria/game_rules.jsonl: units fight (strike an enemy unit or structure, or the enemy god) and harvest wells.
- 29 Oct 2026, v36 (Inscryption): supplement_inscryption.py (251 cards from the wiki's card boxes, replacing the library's
  merged entries: source.py FULL; 5 sigils the library lacks); sigils are the Keywords field; vocab keyword rows for all 107
  sigils and traits (inscryption:Armored is shield); kind secondary_resource (Bones), event sacrificed (Blood); BRIEF "Game
  words: Inscryption"; read/inscryption/game_rules.jsonl (units fight, Bones from deaths); 19 decks in decks.tsv.
- 29 Oct 2026, v36 (Inscryption, after the readings): vocab position in_circuit, kind gem, region Orange, x unstated, keyword
  Gemified; fixes/inscryption/v36.py (circuits, inscribed direction = sides, gems, unstated heals, names for keyword records,
  second reading); names.tsv (Push/Pull dropped, Explode Bots, Pelts family, Nano Armor = Armored, Ancient Obol dropped);
  normalize: a dropped keyword keeps its effect, abilities left without effects go, N16 (moves: the mover is the object);
  audit_text.py reads keyword entries (rulebook line); audit_links.py check 5 (deck cards that are no card); Runeterra
  keyword records: Skills in SpellShield and Flow (v33 now on keywords), Spawn repeats per Spawn (fixes/runeterra/v36.py).
- 29 Oct 2026, v36 (Inscryption networks): game rules may name a cost (cost_has): Blood costs (sacrifices), Bones costs,
  Green/Orange/Blue Mox costs; units can be sacrificed; refs.py copies a cost rule's needs to the cards whose cost names it;
  network: cost needs ("pays its cost"), resource words, colour_fit; act sacrifice (normalize N17; Monster Train Sacrifice
  record, fixes/monster_train/v36.py); load.py: card cost and speed loaded again (lost in a comment), cost_text kept.
- 29 Oct 2026, v36 (Inscryption networks, 2): network.actor_help_lines (effects on the card a sacrifice pays for); refs: an
  ability that spends a resource needs it; a cost rule skips cost 0; Worthy Sacrifice record (Claude): the card it is
  sacrificed for costs 2 less; cases ni06-ni08.
- 29 Oct 2026, v37 (Duelyst, 1): cards from open-duelyst 2843f24 (supplement_duelyst.py, tools/convert/conv_duelyst.py;
  the library's copy lacked the basic cards and tokens); keyword rows for 42 Duelyst keywords (concepts Claude's); terrain
  damage_space, heal_space, summon_space, growth_space, bonus_mana_space; positions corner, area_2x2, area_3x3,
  starting_side, diagonal, center_column; concept cant_move (Duelyst Wall) with flat.py rules cant_move and immobilize
  (cant moves on an enemy); BRIEF "Game words: Duelyst"; read/duelyst/game_rules.jsonl (fight, counterattack).

## 29 Oct 2026, v38 (Faeria positional pass; shared code, every game rebuilt)
- BRIEF "The board": one form for spaces, neighbours, areas, ground, movement, placement and board resources in every game.
- vocab: position straight_line, attr distance (numeric, check.py, network PLAY_STATE), acts empty_resource,
  refill_resource, extra_turn, end_turn, state struck_player_this_round; moves_onto has the mover as object (like moves);
  harvests: actor the unit, object the space; movement keywords of every game cause moves and moves_onto.
- normalize N23: a draw that names what it draws is from the deck (N14 only for plain draws).
- flat.py: "it" keeps the previous target's filters (after a summon of a named card, that card); RULES terrain,
  territory_trigger (conditions), placement_rules, zone_control, control_reward, area_templates, adjacency in triggers,
  positional for ground and distance.
- refs.py: stat needs by direction (damage never feeds "more"; thresholds want nothing; unnamed holder = unit); land counts
  need terrain_changed; set_terrain makes the new ground; harvests made on the space with the harvester as self; spaces and
  chosen-space areas and entering positions need no moves; no keyword-given needs for cards drawn or played or in the deck;
  effects on "it" make no needs; what a card does to itself is on my side; keyword causes keep their target.
- network.py: reads card costs (was never read: cost filters matched every card); terrain_fit; movement HELPS (reach enemy
  land, wells, fights, the enemy player); placement help; tutors ("draws it from the deck") only to deck cards; drawn
  triggers fed by the deck's cards; a big cost cut aims at cards costing that much; can / can't lines say what they allow;
  help to a card about itself only from effects that can be that card.
- load.py: trigger labels written "Name -" on their own line are the card's keyword (Faeria Corrupt).
- connections.py: an effect on every unit hits each type ("ALL creatures" damages the Yaks); a payoff acting on all my
  units is fed by summoners; turning my units into copies of a chosen unit makes more of the payoff.
- audit_text.py: Faeria player words; board rules (this turn, land act, adjacent, harvest); "+1/+1" stat gifts.
- deck_analysis.py: kinds must fit (a god healed is no unit healed); a need about the card itself is not met by another card
  acting on itself unless the need names that kind of card; the rules' rows on enemies make no friendly happening; making a
  type by description is no caring about it; role "Pays for big cards (more mana, cheaper cards)". Cases dfa01-dfa05.

## 29 Oct 2026, v39 (Kaptain's check of the Faeria networks)
- network.py: helps_it (help aimed at one card of a kind helps each card it can hit); payers for the top quarter of costs;
  line of fire (data-driven: a keyword striking the nearest enemy in a straight line); board growth (data-driven: a game
  rule letting land or entry spaces sit next to units); harvest help only from move effects; the aimed_rows filter restored.
- refs.py: abilities that only destroy their own card wait for nothing; chosen harm of either side goes to enemies; fighters
  are struck back (damaged, dies on my side, weak); zone needs keep their filters ("if Krog has died").
- deck_analysis.py: fight deaths are not listed as makers.
- Faeria: game rules for land building and summoning; Ranged strikes the nearest enemy in a straight line; faeria.md rules
  from the Battlefield page and Kaptain. network_page.py: labels "enables" / "helps", cost and stats, deck drop-down.

## 29 Oct 2026, v39 (Inscryption: positions, Claude's check of 20 cards)
- network.py: aimed lines also read a card's keyword effects on other cards (Leader boosts the units next to Alpha); a
  card named in a filter is fed by that card or a card that makes it ("is the Bell Tentacle it names"); a grown form pays
  no cost (Tadpole -> Bullfrog). refs.py DONE_BY: attacks, strikes, fights and challenges take the doer's side, so an enemy
  attacking my unit is not fed by my attacks. cases/run.py: a network case's deck may be a card list.
- Inscryption: fixes/inscryption/v38.py (strikes into empty spaces, Double Strike, Clinger, Loose Tail, Hefty, Sentry,
  Finical Hatchling, circuits) and v39.py (Burrower's space is mine, "rotate one space" = bordering); Tadpole -> Bullfrog;
  Conduit Card type. Concepts base_resource_gain (every game), lanes, link_formation, cross_lane; ask.py factions.
- Cases ni15-ni17, mi22-mi23. Other games checked read-only with cases/run.py: all pass.

## 29 Oct 2026, v40 (Duelyst deck read: leaders and the board; shared code, Duelyst rebuilt, other games checked)
- Category `leader` (Duelyst Generals): network KIND_CAT player and board; leaders fight as their player; help to the
  player reaches only the leader; aim of help checked only in games with leaders.
- refs.py: pick actor takes the event actor's kind and side; "it" in an attack ability is the enemy; equipment kills make
  only leaves_play; summons with no side are mine; positional needs (Backstab, Zeal, Infiltrate, positions of my General,
  same_space) make moves needs; entering abilities need no moves; costs equal to a stat want less; death needs an ability
  makes itself are dropped.
- flat.py: given abilities flip sides for enemies; applied_to replaces only "self"; RULES flanking, adjacency diagonal, lanes
  center_column, area_templates corners and starting side.
- network.py: power and health makers row by row (no self gains); "can" on the player for card handling is no help;
  hand and cost effects skip board-only tokens; chosen help on "anything" reaches units and leaders; named cards asked for
  in play; tutors from hand; "a copy of it" keeps the first target; harm triggers skipped; stat needs by stat made.
- normalize N24: summoned from the hand (action bar) is played. load.py: "Opening Gambit and Dying Wish:" labels.
- Duelyst: fixes/duelyst/v38.py (MECHAZ0R build count; Spellsword's four swords); cases ndu01-ndu30, du31-du34;
  CONCEPTS_duelyst.md; deck_read_duelyst.md.

## 30 Oct 2026, v40 (Inscryption: room on the board, full decks)
- BRIEF "The board": Room (stat size = spaces a unit takes; "board full" = no empty space on that side); vocab size widened;
  flat.py: size changes are board_limit. Inscryption: The Moon and The Limoncello take every space of their side
  (fixes/inscryption/v39.py, case mi24).
- decks.tsv: Inscryption players' decks carry their counts (20 cards each); BEAR's 20-card deck added; starters marked.
  PROCESS 2.9: what a full deck is. HANDOFF: the order that saves the most time.


## 30 Oct 2026, v41 (Kaptain's second Faeria check, fixed by cause in every game; deck_read_faeria.md F1-F13)
- network.py: a line's kind from the need (trigger or counted event: waits; a thing that must be there: type "enables");
  help split into cheaper, stronger, keyword, moves, clears (help_kind); reasons in active verbs (ACT, ACT_SELF); the
  rules' harm to my own units and rules that need a place feed nothing (costs kept); either-side harm aimed at my own unit
  whose death or damage effect it sets off (self_harm_lines; not shield keywords); payers: game's top tenth of costs, a
  third of the cost, only the cards a cut names; help that names its targets lands only on them (lands_on); a tutor's
  line split over the deck's matching cards.
- refs.py: the struck-back rule removed; a number taken from a stat waits for nothing; a unit that comes back after dying
  makes deaths (Ruunin). connections.py: what a card does to itself meets the payoff's trigger about my units.
- cases/run.py lists must-not cases whose reason no deck says; review_check.py (in run.py); dump_lines.py.
- network_page.py: kinds and names agreed 30 Oct; links hover and click like cards; labels only the reason.
- Lines before -> after: Runeterra 6952 -> 6729, Stormbound 959 -> 925, Monster Train 106 -> 109, Duelyst 574 -> 569,
  Inscryption 325 -> 324, Faeria 651 -> 571. Cases nfa31-nfa40.

## 30 Oct 2026, v42 (Kaptain's check of the Duelyst networks; shared code, Duelyst rebuilt, other games checked)
- network.py: helpful effects and help triggers are no asks or "cards it counts"; rule lines only from cards that fight
  more, needs naming the leader, or level-ups; power no help to damaged enemies (except level-ups); chosen harm wants no stat;
  stat makers by stat and target; level forms keep types; made nodes take their makers' lines; buff keywords Ranged,
  Backstab, Rush, Provoke, Airdrop; ready, countdown and damage prevention help; self makes keep the card's kind; protection
  triggers wait for nothing; tokens are never played; a leader's spell is a node ("casts its own spell"); leader wording.
- refs.py: help to keyword holders makes no keyword need; positions from my unit need its moves; chosen harm wants no stat.
- vocab: Duelyst Celerity causes attacks and moves. supplement_duelyst.py: a General's text names its spell card;
  fixes/duelyst/v41.py drops the spell copy from the General's record.
- network_page.py: right click copies a terse card or line text; tooltips show types. deck_lines.py prints the same text.
## 30 Oct 2026, v43 (Inscryption: rule lines from every unit, decks; deck_read_inscryption.md F9-F12)
- network.py: a cost or resource need (Blood, Bones, Bones spent by an ability) is fed by the rules only from a unit that
  costs nothing to play; other units only by their text (F9). A cost rule's sacrifice still feeds a card's trigger on its
  own death, Mantis God -> Ouroboros (F10). where() reads "of self" filters ("(when in its circuit)", Stormbound "(when
  around it)"). A need whose only filter is a type makes no "is a unit it asks for" line: the type line says it (every
  game: Stormbound 13, Duelyst 8, Faeria 5, Monster Train 5, Inscryption 5, Runeterra 4 duplicates gone, no pair lost).
  Forms that turn into each other (Swapbot) are one card (forms_of; it looped before).
- deck_analysis.parse_deck: a name written with other spaces ("Fish Bot") finds the card, every game.
- supplement_inscryption.py: a first tab that is the state a card is played in keeps the card's name (Child 13, GR1ZZ,
  Swapbot, S0N1A, QU177), ids kept (F11).
- decks.tsv: 12 Inscryption decks added (10 core lists from gamersdecide.com, 2 full ones from a Steam guide); 31 in all.
- Cases ni10, ni12 rewritten, ni17 dropped for mi25, ni18-ni21 added. Lines: Inscryption 371 -> 289.

## 30 Oct 2026, v44 (Kaptain's review of the Inscryption networks; deck_read_inscryption.md F13-F17)
- network.py: the cost rules (Blood by sacrifice, Bones from deaths) make no lines; only cards that pay by their own text do.
  No cost or cheaper line to grown or level forms (Runeterra level 2: 5 lines gone).
- refs.py: "it" in an ability on my own damage or fight is an enemy (Touch of Death).
- supplement_inscryption.py: traits that do nothing in battle leave the text (wiki page Traits).
- network_page.py: a "Keywords: ..." sentence is not repeated in the card text.
- Cases: ni02, ni03, ni09, ni18, ni19 now "none"; stale must-not cases rewritten: n15, nfa03, nfa04, nfa06, nfa12, ndu25, ndu43.

## 30 Oct 2026, v45 (Inscryption decks; deck_read_inscryption.md F18)
- decks.tsv: 17 Inscryption decks kept, 3 added from the wiki's Kaycee's Mod tips page; 20 weak decks moved to
  decks_dropped_inscryption.tsv, which network_page.py does not draw (any game can have such a file); cases keep their lists.
- supplement_inscryption.py: Larva is Strange Larva (wiki page name), id kept (KEEP_ID).
- RESULTS.md: why Inscryption's networks are thin, with numbers per game.

## 30 Oct 2026, v46 (Kaptain's second check of the networks, from the Duelyst chat; shared code, every game checked)
- network.py: one link per pair of cards (one_link: kind by a fixed order, every reason listed); one rule per need (triggers
  on played, summoned, drawn and counted played cards only in played_lines); no second saying of a fact (stat gain and more
  power, cost cut and pays for it, rule line beside the card's own ability, through lines); heals its own kind; help on itself
  or the player helps no unit (Rally still does); making keywords (Invoke, Manifest) name what they make; trap wording; the
  leader exemption only in leader games. refs.py: a keyword in a create or summon filter is no need.
- network_page.py: layout tried from several starts, the one with fewest crossing lines and lines through cards kept, a card
  and what it makes or levels into close; help lines softer; a line's tooltip names both cards; focused labels bold; while a
  card or line is locked, pointing reacts only to the locked part and a right click copies only it.
- Families F10-F15 in deck_read_duelyst.md; cases n38 (rewritten, Kaptain), n70, n71.

## 30 Oct 2026, v47 (Kaptain: "triggers" and "enables")
- network.py: a reaction (refs role trigger) is a "triggers" link; a count or a needed thing is "enables" (played_lines, counted
  needs, HELPS by the need's role). network_page.py: the label "triggers". Cases nfa31, nfa37, nfa42, nfa47 rewritten by
  Kaptain's word. PROCESS "Link kinds and what this chat learned".


## 30 Oct 2026, v48 (Into the Breach import)
- source.py: id block 6000001 for into_the_breach; FULL replaces the library's unit, ability, item and hero entries with the
  supplement (every mech, weapon, passive and pilot from the wiki tables; Walking Bomb, Arachnoid and four tanks as tokens).
- vocab: keyword rows for the game's statuses and Vek abilities (Boost, Frozen, Burrower are into_the_breach:<Name>: other games
  use the names for other meanings); terrain chasm, cracked_space; test upgraded (a weapon upgrade is powered).
- BRIEF "Game words: Into the Breach"; patterns TB01-TB14; exclude.tsv: the library's 10 wiki article pages (category
  game_rule) are not cards (Claude, for Kaptain's check).
- decks.tsv: the 14 official squads and 6 players' custom squads (a squad of 3 mechs is the deck).

## 30 Oct 2026, v49 (Slay the Spire import)
- source.py: id block 7000001 for sts1 (first taken for The Elder Scrolls: Legends, released unused: its later sets are not
  reachable from here). supplement_sts1.py holds every sts1 entry (FULL): energy icons counted ("Gain energy energy" = 2),
  numbers the library's conversion lost (Genetic Algorithm, Ritual Dagger from the source's upgraded_text; Happy Flower,
  Sundial, Nunchaku from the wiki's Module:Relics/data), powers' format strings replaced by Module:Powers/data texts, Exhaust,
  Ethereal, Innate, Retain, Unplayable in the Keywords field, card kinds (Attack, Skill, Power, Status, Curse) as types.
  Powers kept only when a text names them and nothing else holds them (Plated Armor, Mark, Hex, Stasis, Surrounded, as
  keywords); glossary words no text uses left out (Opener, Vigor). Claude's choices, for Kaptain's check.
- vocab.tsv: 43 keyword rows (Slay the Spire); sts1:Vulnerable, sts1:Dazed, sts1:Focus, sts1:Curse mean something else than
  the shared rows; Poison, Regen, Unplayable, Transform use the shared rows (same concept).
- BRIEF "Game words: Slay the Spire"; patterns SS01-SS18; tools/games/sts1.md "The game's rules (from sources)";
  read/sts1/game_rules.jsonl has no record (no card category does anything its text does not say).
- decks.tsv: 22 guide decks (guides' core cards and relics; no full end-of-run deck exists as text that can be reached here,
  and the game sets no deck size).
