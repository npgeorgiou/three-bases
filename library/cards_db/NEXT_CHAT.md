# Next chat: deck networks — state, open work, how to work (29 Oct 2026, 13:30)

Read this file, then HANDOFF.md. Everything below is pushed. Kaptain is out of patience: he has found real errors in every
round, because the work fixed only what he pointed at. **Your job is to find the errors he has not pointed at.**

## How to think (read twice; this is what went wrong three times)
1. Every error Kaptain names is ONE example of a FAMILY. Before fixing it, write down the family ("an ability given to the
   player that boosts a kind of card", "a status keyword read as if it adds damage", "a condition about the card itself
   stored without 'self'"), then find EVERY member in ALL THREE GAMES with a query or a text regex over all cards, read
   20 of them, fix the rule, and read 20 again after. Never fix one card.
2. Think like a player of the game, card by card: for each card in a deck ask "what does this card need to work well
   (its level-up, triggers, conditions, stats, keywords, type) and which cards in the deck give it that?" and "what does
   this card give, and to whom?". Then compare with the network. Missing help is as wrong as a wrong line.
3. Read the card TEXT, not only the rows. If text and rows disagree, the rows are wrong: fix them by rule (fixes/<game>/vNN.py).
4. Never write "not sure" about something you can check: read the texts, the game's glossary (supplement, library/tools/games/
   <game>.md), the wiki. Kaptain's examples: "Spirits Unleashed deals 1 to EVERYTHING" (so it does hit Braum: the line is
   right); "Imps in your deck" — Monster Train's own glossary says Consume removes a card "from the deck for the rest of the
   battle", so deck = all cards of the battle: Imps added to hand count (Imp-in-a-Box -> Imp-olate is right).
5. Use real decks as the mirror: many full decks per game; for each, read every line and every missing line (point 2).
6. Report only what is checked. Say which families you swept and how many cards each touched.

## Open work, in order
1. **Tybaulk is linked to too few cards** (Kaptain, last message). Text: "grant allies everywhere +1|+0 and for the rest of
   the game, all of your spells and Skills deal 1 extra damage". network.gives_lines links the given ability only to cards
   whose own rows make 'damaged' (origin own); spells that damage through keywords, skills cast by units, and units that
   deal damage are missed, and the +1|+0 to allies everywhere (hand and deck too) is not a help line to units. Fix the
   family: every given or aura effect ("your spells", "allies everywhere", "your Elites") -> every card of that kind in
   the deck, all games; check Senna's spells, Monster Train "spells cast on this floor", Stormbound "friendly units".
2. **Full decks.** Runeterra: 8 full decks in decks.tsv (masteringruneterra archetype pages); found but NOT yet added:
   Janna Nilah (https://masteringruneterra.com/archetype/janna-nilah-bw-pz/standard/three/everyone/: 3 Nilah, 3 Janna,
   1 Sunken Temple, 3 Eager Dedicant, 3 Pool Shark, 3 Maryam, Temple Caretaker, 3 Windborne Mariner, 2 Vikrash the
   Exuberant, 3 Exalted Cloudwinder, 2 Ruined Rex, 3 Mystic Shot, 1 Aftershock, 2 Howling Gale, 3 Eye Of The Storm,
   3 Gotcha!, 2 Divine Whirlwind); 27 meta decks as deck codes at https://riwan.substack.com/p/lor-ladder-decks-221115
   (decode the LoR deck codes: base32 varint format, card codes -> names via the Riot data, supplement_runeterra.py source);
   player decks at masteringruneterra.com/decks/<champion>/ (profile pages). Stormbound: 6 from stormbound-kitty.com/decks
   (119 exist; find more). **Monster Train: cases/decks.tsv has only the guides' core cards (3-8 cards), not full decks;
   Kaptain wants full decks** — search Steam guides/discussions, Reddit winning runs, YouTube descriptions for full card
   lists; replace the partial ones in the page (network_page.py reads decks.tsv and cases/decks.tsv).
3. **Sweep all three games for the families found so far** (list in PROCESS.md "Links the deck networks showed missing"
   and "Think like a player"); also: lethal damage is no "survives damage" help (Sunburst deals 6, Braum has 6 health:
   compare the amount to the taker's health); cards made by description ("2 random Imps") make that type (add them to
   network.lines_of `has` like connections.py does); Stormbound/Monster Train "itself" / "this unit" = self (the I/me
   audit covered only Runeterra's wording).
4. **The 33 keyword concepts**: done this chat with Kaptain's review (another AI's list he agreed with). New concepts in
   library/tools/concept_tree_v3.txt (spell_or_skill, countdown, play_timing_condition, spells_played_condition,
   combat_damage_threshold, nexus_damage_condition, max_mana_condition, card_presence_condition); shape rules in
   flat.py RULES give them to every game (found: Monster Train Burnout = countdown 15 cards; Stormbound "when played
   bordering a friendly X" = card_presence_condition 9 cards); vocab rows updated; keyword conditions give their
   keyword's concept (flat.derive). **Not done yet: write in PROCESS.md how to map a keyword to a concept** (read the
   concept's definition and "not this"; use an existing concept only when its definition says exactly that mechanic,
   else add a precise one and run its shape rule on every game; Claude's first list used loose fits: Enlightened ->
   high_cost, Deep -> self_mill, Plunder -> on_life_loss were wrong) and add a CHANGES.md line (v33).
5. Kaptain's earlier points answered this chat but not yet in the files: Frostbitten units CAN block (Frostbite only sets
   Power to 0); Overwhelm adds no damage, it sends leftover damage to the Nexus (network help line "helps it hit the enemy
   player"). Put both in BRIEF.md "Game words" for Runeterra.
6. Rebuild every game (`run.py <game>`), all cases pass (now 283 / 135 / 143), audit_links.py 0 findings, rebuild
   network.html (`python3 network_page.py`), give it to Kaptain as a download, push.

## Where things are
- network.py: lines (lines_of, aimed, played_lines, need_lines, boost_lines, gives_lines, families, through-made-card
  level-ups), measures, report. network_page.py -> network.html (game picker, decks, sidebar sections incl. Mechanics).
- refs.py (flat_ref: makes/trigger/condition/state with kinds, self, actor_self), flat.py (query layer, concept RULES),
  audit_links.py (in run.py), cases/network.tsv (Kaptain's checks as tests), fixes/runeterra/v30.py, v31.py.
- PROCESS.md: "Links the deck networks showed missing", "Think like a player"; BRIEF.md rules 23-25; CHANGES.md v30-v32.
