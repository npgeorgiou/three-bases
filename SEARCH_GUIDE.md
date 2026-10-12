# Three Bases inspiration library — how to search

The library is `three-bases-library.sqlite`, queried with `python3 lib/query.py <command>`. It holds mechanics from other games for designing Three Bases (rules: summary.txt in the project). Only mechanics are reused, never names or wording. Never present a link or count as more than it is: automatic tags can be wrong.

## Model
`entities`: every card, unit, spell, item, location, ability, rule, keyword (definition as text) and tribe (card type). `concepts`: Claude's cross-game network, sorted by outcome first and mechanism second; a concept can have several parents, and a query on a parent includes all its descendants (`concept_tree`). So `concept no_damage_output` finds Hearthstone Freeze (attack_lock), Runeterra Frostbite (attack_zero) and damage prevention together, and `concept suppress` adds can't block, immobilize, silence and total disable. Stat loss is `debuff`; "this turn / round only" is the separate marker `temporary_effect`. `entity_concepts`: entry → concept with a role: does, grants, benefits, counters, cost, exhibits (design problems). `concept_relations`: synergizes, enables, counters, mitigates, tension, variant_of between concepts (Claude's analysis). `entity_links`: keyword links (has, grants, mentions; D&D conditions: inflicts, counters, suffers, benefits), type links (has_type, cares_about_type), name links (references, summons, generates, transforms_into), variant_of, equivalent_keyword (the same keyword in another game; for jumping between games only). `trigger_effect`: "when X, do Y" pairs with a frequency limit; a clause starting "via keyword K:" comes from the entry's keyword. `faction_signature`: signature mechanics, keyword signatures (`kw:<keyword>`) and splash per source faction. `concept_precision`: how often automatic tags were right per concept and game. `factions` / `faction_archetypes`: concept profiles and archetypes per faction (share of the faction, lift over the game average).

## Commands
- `concepts <term>`: find concept ids.
- `concept <id> [per_game=4] [role=does] [game=x]`: entries for a concept, per game; warns where its automatic tags are often wrong.
- `cooccur <id> [game=x]`: concepts printed together with it on cards.
- `problem <p_id>`: mechanics that ease or worsen a design problem, with examples.
- `faction <game> [name]`, `archetypes [id] [game=x]`: faction profiles and archetypes.
- `signature <game> [faction]`: each faction's signature mechanics with example cards, its own keywords, and the other factions' mechanics it splashes.
- `splash <concept> [game=x]`: who owns a mechanic, and which other factions use it on a few cards, with the splashing faction's own signatures on each card (how the splash fits that faction).
- `grid [trigger] [effect] [game=x] [freq=bound]`, `unused_pairs <trigger>`: the trigger × effect design space and its gaps.
- `frequency [bound] [trigger=x] [effect=x] [game=x]`: pairs by frequency limit: per_card (spell, Place/on-play, own death, once per game), per_round (once-per-turn cap, own turn start/end, attack, kill, tap), unbounded (other units' or repeated events), static (aura). The basis column says why. Use it for the frequency check: card advantage and resources must be bounded unless they are the faction's signature.
- `interactions "<card>" [game=x]`: a card's partners by link, type, keyword and concept role.
- `combo "<A>" "<B>" [game=x]`: every connection between two cards, by layer: link, engine (an effect of A sets off a trigger of B: summoning sets off "an ally is played", destroying or sacrificing sets off "a unit dies", damage sets off "takes damage", an immediate attack sets off attack effects, a spell sets off spell triggers), role (A does or pays what B benefits from), role_tree, keyword, type, relation.
- `search "<fts query>" [game=x]`, `entity "<name>" [game=x]`, `games`.
- A merged name still resolves: the commands say which entry kept it. Created cards have edition `non-collectible`. Direct SQL is fine for anything else.
- Checks after any change: `lib/regression.py <db> check`, `lib/combo_check.py <db>`, `lib/trigger_pairs.py <db> check`, `lib/test_query.py <db>`.

## Typical questions
"Ideas for a faction that …": translate the idea into 3–6 concepts; run `concept` on each and `signature` / `faction` on the games whose factions match; read those factions' keywords and top cards; look at how each game builds the identity (resource, positional rules, triggers), not only which effects it uses.

"Alternatives to this mechanic": find its concepts; look at siblings under the same parents, variant_of relations, and how other games reach the same role with a different trigger, cost or scope.

"Cards that work with X": entries that benefit from X or grant it, concept relations synergizes/enables, `cooccur`, and `combo` to check a pair.

"The game has this issue": map it to a `p_*` concept (`concepts p_`), run `problem`, pull examples of each mitigating mechanic from several games. If none fits, say so.

## Reading results efficiently
- One or two targeted commands per question; never dump tables.
- Results come per game with a cap per game; compare games by share of their own entries, never by totals. Magic (about 17,800 entries) and Hearthstone (5,500) would otherwise drown out Inscryption, Into the Breach, Blood Bowl, Faeria or Marvel Snap, which often hold the most original ideas. Say when a game has nothing for a concept.
- Read each game's own wording for a concept before generalising; the differences between games are the useful part.
- Check the role: "does heal", "benefits from heal" and "counters heal" are different design spaces.
- Before relying on an automatic tag, print the text of the two or three cards the answer rests on (a few lines).

## Reliability
Link methods, most to least trusted: `claude_review` (read by hand) > `via_keyword` (inherited from a reviewed keyword) > `via_link` (inherited from a card it names) > `claude_inference` (keyword mapped from Claude's knowledge, no source definition) > `data_rule` / `game_structure` (rule for a whole category) > `engine_rule` / `text_pattern` (automatic wording rules). Short card text (Hearthstone, Runeterra, Shadowverse, Gwent, Faeria, Duelyst, Magic, Snap, Underworlds) tags well; long prose (D&D, Warhammer army rules, Inscryption and Into the Breach wiki text) is noisier. Keyword definitions from Claude's inference say so in source_type (Faeria, Hearthstone, Battlegrounds, Shadowverse, Underworlds, Marvel Snap). Darkest Dungeon text was built by Claude from raw data fields; Underworlds warscroll abilities are Claude's paraphrase of the official PDFs.

## What the tags mean in each game
- Everywhere: put a card from your deck into your hand = tutor or draw; put a new card into your hand = generate_cards; "discard pile" is not discard; "N% chance" is random, a plain percentage is not.
- Kill Team, 40k, Age of Sigmar, Blood Bowl: a unit being activated = turn_start; real action abilities (1AP, Timing:, Special Action) = activated. Re-rolls = advantage; only D6 and random-number rolls are random_effect. Invulnerable saves, Feel No Pain, Ward and "-1 to hit for attacks that target this unit" = damage_reduction; debuff needs an enemy target. Objectives and control scores = zone_control; engagement range, combat range and tackle zones = zone_of_control. Once per battle = once_per_game; once per turn/turning point/phase = cooldowns. Blood Bowl: Block/Blitz/Foul are combat (not blocking); "player" means a piece on the pitch.
- Underworlds: "out of action" = destroy; upgrades = items_consumables; Inspired = upgrade.
- Slay the Spire 1–2: Curse = junk_cards (not debuff); self "Lose N HP" = life_payment. Monster moves = telegraphed_threats; relics = items_consumables + passive. STS2 Stars = multiple_resources; Osty = summon:benefits; co-op cards = team_play.
- Darkest Dungeon: a hero's own minus stats = drawback, minus stats on enemies = debuff. Trinkets = items_consumables; quirks, diseases, afflictions and virtues = traits_quirks. Stress = stress_morale; bleed/blight = damage_over_time, cures and resistances = damage_over_time:counters. "vs beast/eldritch/man/unholy" = tribal.
- D&D 5e: paralyzed, stunned, incapacitated, unconscious, petrified = total disable; grappled and restrained = immobilize; prone = debuff; blinded, poisoned, disadvantage = debuff; Charmed = control; Exhaustion = fatigue — each with the role the entry has (inflicts → does, ends or resists → counters, suffers → cost, profits from it → benefits). Conjure/summon = summon; Piercing is a damage type, not piercing.
- Hearthstone: Freeze = attack_lock + temporary_effect (the frozen character misses its next attack), not a total disable. Battlegrounds: Freeze keeps the tavern's offers (selection); team_play covers Duos passing and teammates. Shadowverse: Ward = taunt, not shield.
- Into the Breach: Smoke and being submerged = attack_lock, Webbed = immobilize, Frozen = total disable. Duelyst Provoke and Faeria Taunt = taunt + immobilize.
- Marvel Snap: locations are terrain + lane_rule; cross_lane, lane_identity, lane_closure and forced_placement describe lane play.
- Text layout: a Runeterra champion is its level 1 card (with its level-up condition) plus its levelled side, "<name> (level 2)", linked by transforms_into; Shadowverse "Evolved:" text is appended to the card; Shadowverse crafts are named (Forest, Sword, Rune, Dragon, Shadow, Blood, Haven, Portal, Neutral).
