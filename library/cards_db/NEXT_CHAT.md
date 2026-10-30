# Next chat: deck networks — state, open work, how to work (29 Oct 2026, v34)

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
1. **Kaptain's check of v34** (CHANGES.md): game rules as data, help table, line names, deck-read families. Fix what he
   finds as a family, for all games, and write the lesson in PROCESS.md.
2. **Monster Train full decks: none found as text** (Steam, GameFAQs, the wiki: players post screenshots). Ask Kaptain.
3. Read more decks like a player (PROCESS step 2.9): read so far Janna Nilah, Swain Ziggs, Soraka Tahm Kench, Aphelios
   Zoe, Lurkers, Chronobreak, IC pirate, Frost Deck, Morsel build, Hellhorned armor.
4. Not linked on purpose (Claude's calls): Janna's "the first 3 cards you draw cost 1 less" (helps any card); Stormbound
   units moving forward each turn (every unit, says nothing); removal spells (Hush, Mystic Shot) help no card in particular.
5. After any change: `run.py <game>` for all three games (now 300 / 137 / 146 cases), audit_links.py 0 findings,
   `python3 network_page.py`, give Kaptain network.html, push.

## Where things are
- network.py: lines (lines_of, aimed, played_lines, need_lines, boost_lines, gives_lines, families, through-made-card
  level-ups), measures, report. network_page.py -> network.html (game picker, decks, sidebar sections incl. Mechanics).
- refs.py (flat_ref: makes/trigger/condition/state with kinds, self, actor_self), flat.py (query layer, concept RULES),
  audit_links.py (in run.py), cases/network.tsv (Kaptain's checks as tests), fixes/runeterra/v30.py, v31.py.
- PROCESS.md: "Links the deck networks showed missing", "Think like a player"; BRIEF.md rules 23-25; CHANGES.md v30-v32.

## Slay the Spire (sts1): deck read open (30 Oct 2026, v49)
Imported up to step 2.9: run.py sts1 passes, word check 0 flags, text audit 0, link audit 3 explained (RESULTS.md). All 22
decks read once (`deck_lines.py sts1`); nothing fixed yet. Next: `dump_lines.py /tmp/before.tsv`, trace each family below to
its rule (flat_ref / flat_do of both cards), fix each once for every game, dump after, read the diff, then write the families
into deck_read_sts1.md with Root cause / Same error elsewhere / Fix and a case each (PROCESS "Fixing a review").
Wrong lines found (deck: from -> to):
1. A status that helps a kind of card is read as that kind of card being its need, and the help line is missing: every Attack
   -> Flex, Spot Weakness, Inflame, Limit Break, Vajra, Red Skull, Reprogram, Wish, Wrist Blade ("is an Attack it asks for");
   Skills -> Burst, Powers -> Amplify, cards -> Echo Form, Poison cards -> Snecko Skull ("triggers"); Shiv -> Accuracy beside
   Accuracy -> Shiv (two links); Heavy Blade -> Flex/Inflame/Vajra beside the opposite line (two links). Wanted: Strength,
   Dexterity, Focus givers -> the cards they make stronger (Attacks, Block cards, Orb cards); Burst/Amplify/Echo Form/Snecko
   Skull -> the cards they repeat or boost.
2. Ethereal's "still in hand at the end of turn" read as a need for cards in hand: draws -> Ghostly Armor, Echo Form, Deva Form
   "fills your hand". Gambling Chip's own discard-then-draw read as a need ("fills your hand" from Reflex, Tools of the Trade).
3. Cards with no numeric cost match cost filters: All for One ("cost 0 cards") -> Burn, Void, Girya and Snecko Eye (relics),
   Reinforced Body (X cost); Chemical X ("cost X cards") -> Deus Ex Machina, Miracle, Expunger.
4. A drawback is read as a need: Void ("lose 1 energy when drawn") <- draws "fills your hand", <- TURBO/Nunchaku "lets you
   gain mana".
5. An upper limit is read as a need: FTL ("if you have played less than 3 cards") <- every card; unplayable Void counted as
   played.
6. Damage back to the attacker lands on me: Flame Barrier -> Rupture, Self-Forming Clay, Red Skull ("damages your units or
   players"); the attacker of "whenever you are attacked" has no side.
7. Choosing a card for the run is read as making one: Bottled Flame -> Kunai, Shuriken, Vajra ("makes an Attack").
Missing lines: Barricade -> Body Slam (Block kept); Electrodynamics -> Lightning channelers (Lightning hits all); entering
Wrath/Calm (Crescendo, Tranquility, Teardrop Locket) -> Mental Fortress, Flurry of Blows ("whenever you change Stances").
Not sure (ask Kaptain): every card -> After Image / A Thousand Cuts ("whenever you play a card"); Strike -> Corpse Explosion,
The Specimen ("makes enemy units die": any damage kills); energy gains -> 2-3 cost cards ("pays for it", the Faeria rule).
Known gaps: Blizzard and Thunder Strike count every Channel (which Orb is not kept); Through Violence (made by Reach Heaven)
is not in the library and its wiki page was not reachable.
