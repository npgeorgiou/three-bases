# Process: describing a game's cards (the framework for every game)

For the chat that imports a game. Runeterra, Stormbound and Monster Train went through every step; their files are the
templates. Commands run from `library/cards_db/`. Files and tables: README.md.

The database is one place for all games: questions run across games (`ask.py all ...`), so everything stored must be
generic. A game's own words live only in the card texts, its keyword entries and its types; what cards DO is said with
vocab.tsv values and concepts that any game can share.

## Why the first three games went wrong (read before importing a game; 29 Oct 2026)
Kaptain checked a few decks four times and each time found missing and wrong links. The causes, and what now stops them:
1. **The rows held only what card texts say, not the game's rules.** No Runeterra text says "a unit that attacks unblocked
   hits the enemy Nexus", so no unit helped Gangplank, Darius or Gnar level up. Now each game has
   `read/<game>/game_rules.jsonl` (step 0.10): what every unit does by the rules, written once from
   `library/tools/games/<game>.md`; refs.py gives those rows to every card of the category (origin game).
2. **Claude patched the example, not the cause.** Each check added one special rule to the network code (power helps
   damage, health helps survival ...) and the next missing case waited for Kaptain. Now what helps a need is one table
   (network.py HELPS) and every fix is a rule over all cards of all games (fixes/<game>/vNN.py), never one card.
3. **Readers dropped details a verb check cannot see**: a second target ("or the enemy Nexus"), Skills in "spells and
   Skills", a counted card's quality ("cost reduced"), "double" written as +1, "everywhere", the damage of a strike put on
   the striker, one happening written two ways (strikes_nexus with the player or the unit). BRIEF.md reading rules 26-32
   now say each; `audit_text.py` (in run.py) compares every text with its rows and lists every card a rule finds.
4. **Data the build had but did not read**: level-up forms keep power and health as "power|health" in stats, read by no
   query until 29 Oct (246 Runeterra forms had no stats, so "an ally with 5+ Power" matched them all).
5. **Lines were named in Claude's words.** "Changes how it works" was shown for Spirits Unleashed giving +1|+1. Line kinds
   now say what a player says: does what it waits for, helps it level up, makes it stronger (stats, buffs, cheaper, more
   damage), changes how it works (only real rule changes: Fast, can't block), is a card it needs, puts it into play.
6. **"Done" was said on counts.** Cases passing says nothing about the links nobody wrote a case for. Before showing a
   network: run.py passes, audit_text.py and audit_links.py are explained, every guide deck's "lacks" list (network.measure)
   is read card by card (PROCESS "Think like a player").

## How to work (read first; the cost of a game is set here)
Import chats went wrong by going round in circles: fetching data the repo had, fixing one card at a time, rebuilding after
every small edit, and turning a decision one way and later back. Work like this:
1. Follow the steps below in order, once. Make the task list from them at the start and tick them off.
2. Look before you make: the game's data (step 0.3), an existing value (vocab.tsv, search by meaning), an existing rule
   (normalize.py N-rules, BRIEF.md), an earlier decision (CHANGES.md, verdicts.tsv). `grep` first, then write.
3. A decision is written once and kept. Before changing a mapping, value or rule, grep CHANGES.md for it: if it was decided
   (by Kaptain or an earlier chat), do not turn it back; if it truly looks wrong, ask Kaptain, giving the card that shows
   it. (Runeterra's Stun went disable -> attack_lock -> disable in two chats before Kaptain settled it.)
4. Batch the work: collect all problems of one kind (all proposals, all flags, all failing cases), decide them together,
   fix them with one rule or script, then rebuild every game once. Never rebuild between single edits.
5. Fix by rule, for every card: a regex over the texts or a script over the records (`fixes/<game>/vNN.py`, safe to run
   twice). A re-read by a reader is the last resort, for cards no rule can fix.
6. Readers are expensive (~110-125k tokens each, whatever the batch size): one for the cards, one for the keywords, one for
   the second reading. A few cards (tokens, a handful of fixes) are written by Claude directly.
7. Read the answers, not only the counts: before calling a step done, run `ask.py <game> partners <card>` and
   `analyze` on a guide deck and read them. A case count that passes says nothing about a link that should not exist.
8. Shared code (connections.py, refs.py, flat.py, deck_analysis.py, normalize.py, load.py) serves every game: a change
   there gets a mechanics.tsv case with game `*`, and every game's `run.py` must pass before it is pushed.

## Rules that are never broken
1. The card text is the truth. A record says only what the text states. No rule from memory: a definition that neither
   the library nor the game's own data has is asked from Kaptain (Runeterra: Deep, Plant).
2. The records in `read/<game>/` are the source. Everything else is rebuilt from them by `run.py <game>`.
3. Every value is a row of `vocab.tsv`. A new value is a vocab row, a BRIEF.md line if readers need it, and a CHANGES.md
   line, in one commit. A new event or state also gets its `causes` entry, or "which cards care about X" misses it.
4. One meaning, one form. When two forms of one meaning appear, pick one, write a normalize.py rule and a BRIEF rule, and
   rebuild: normalize runs on all records of all games.
5. Judge data against the texts. Never against old library tags, never against agreement between records and patterns.
6. Nothing lives only in a chat. Decisions go into the files at once; commit and push after every finished step.
7. Nothing is "maybe". A card the values cannot describe is marked unsure (table `unsure`); a word-check flag is decided
   once (`patterns/verdicts.tsv`); a dropped test case is written in `cases/DROPPED.md` with its reason.
8. Tests come from the game, never from Claude: card texts (mechanics.tsv), players' guides (decks.tsv, combos.tsv), the
   library's real-world rows (regions.tsv).

## Writing data the same way in every game
`ask.py all ...` only works when every game is written with the same values, shapes and habits.
1. Reuse before adding. For each of the game's terms, search vocab.tsv for a value that means the same and use it (a base
   or hero with life = kind player; a structure = kind landmark). Add a value only when no value means it, worded so any
   game could use it ("start of the owner's turn", "the tile in front"), with the game as an example in brackets.
2. Every keyword gets a vocab keyword row whose concept (column tree) says what it does by the game's own rules. Check each,
   twice, before a game is done: (a) the keyword's meaning from the game's glossary or wiki, not from memory or the old
   library; (b) the concept's definition, including its "not this" part (library/tools/concept_tree_v3.txt); (c) whose
   side it hits (an enemy that can't block is cant_block, my own unit that can't block is a drawback); (d) whether the
   keyword belongs to the game at all (Terrify is Path of Champions: deleted). When a shared keyword name means something
   else in this game, the row is `<game>:<Name>` (monster_train:Frostbite is damage over time, Runeterra's Frostbite is
   attack_zero). Show Kaptain the full keyword -> concept list with each concept's definition.
   How to map a keyword to a concept: read the concept's definition and its "not this" part, then use an existing concept
   only when the definition says exactly that mechanic. A loose fit is wrong (Claude's first list had Enlightened ->
   high_cost, Deep -> self_mill, Plunder -> on_life_loss: Enlightened is a max-mana condition, Deep a deck-size condition,
   Plunder "the enemy Nexus was damaged this round"). When none fits, add a precise concept to concept_tree_v3.txt with
   its definition and "not this", give it a shape rule in flat.py RULES, and run the rule on every game, then read what
   it found in each (v32: spell_or_skill, countdown, max_mana_condition, card_presence_condition ...).
3. Events, states and durations that games word differently get the same concept: round_start and turn_start are
   turn_start; this_round and next_own_turn are temporary_effect; a state takes its keyword's concept (stunned like Stun).
4. Stats by role: Power / Attack is attack (attr power), Health is health, Stormbound's strength is both. Never add a stat
   for one game when an existing one fits. "Strongest" / "weakest" are pick highest / lowest with "by" (normalize N10).
5. Statuses: giving one is give_keyword with the keyword; "a poisoned unit" is a state whose causes is
   given_keyword:<Keyword>; an act that gives a keyword names it in its causes (stun: given_keyword:Stun). A keyword a card
   has in its own text ("Rage 4.") is give_keyword on itself, always, permanent: load.py counts it as the card's keyword.
6. Board positions are filters `{"attr": "position", ..., "of": TARGET}`: always say what the position is measured from.
7. An effect on the enemy side takes the enemy concept (moving an enemy = forced_movement; flat.py ON_ENEMY).
8. Card names are stored without trailing spaces (load.py); look names up the same way.
9. Links between cards (combos, decks) are made only inside one game. Questions over several games add up, by concept,
   what each game shows.

## Two chats on two games at the same time
Each chat writes its own game's files (read/<game>/, input/<game>/, second/<game>/, fixes/<game>/, supplement/<game>*,
supplement_<game>.py, CHECK_20_<game>*). The shared files need care:
- Id block: the first thing each chat does is write its game's line in source.py (the next free block) and push it. If the
  push is refused, pull: the other chat took that block, so take the next one.
- Shared files (vocab.tsv, BRIEF.md, patterns/patterns.tsv, normalize.py, flat.py, refs.py, connections.py,
  deck_analysis.py, load.py, cases/*.tsv, CHANGES.md, PROCESS.md): pull before editing, keep each change small, commit and
  push it at once. Before adding a vocab value, pull and search vocab.tsv again (one meaning, one value). Never edit
  another game's records.
- cards.sqlite, QUERIES.md and cases/REPORT.md are rebuilt: after a pull run `run.py <your game>` (it loads every game);
  on a merge conflict in them, take either side and rebuild.
- Never force-push. Readers never share a scratch folder (/tmp/reader_<game>_<batch>/).

## Steps
### 0. Before reading (in this order)
1. **Research the game** (library/ADDING_GAMES.md section 0.1): rules, the full keyword glossary, factions or tribes,
   board, turn structure. Also search now for players' guides with real decks (Steam guides and discussions, build
   guides, tier lists with card lists): they become the deck tests (step 3). Note each source's URL and check it is about
   this game (Monster Train 1 and 2 guides look alike; a page with card names the game does not have is not a source).
2. **Left out** (`exclude.tsv`): only other modes or products, and only what Kaptain names. Tokens are never left out:
   links to them are how combos are found.
3. **The game's data is already in the repo. Look there before fetching anything.** Kaptain does not know where each file
   is; this list does:
   - `library/tools/convert/conv_<game>.py`: its first lines name the source, date and format of the game's card data. Raw
     files next to them: `monster_train_cards.psv` (282 Monster Train cards, wiki Module:Cards/Data),
     `inscryption_missing_cards.json`. Named sources: Lorcana (npm lorcana-oracle), Star Wars: Unlimited (swucardex-data
     a86faed), Elder Scrolls: Legends (TESLegendsTracker c541e82), Slay the Spire (wiki Module:Cards/data), Slay the Spire 2
     (Kaptain's lists, 12 Oct 2026), Gwent (gwent.one v14.8), Magic (MTGJSON AtomicCards, Scryfall tokens), Shadowverse
     (Portal API), 40k and Age of Sigmar (BSData).
   - `library/tools/games/<game>.md`: research, sources, and the keyword terms with the page each comes from. Check each
     term's source is this game and drop terms marked "assumed" (rule 1).
   - `library/cards_db/supplement/<game>*`: games already imported here.
   Fetch from the web only what none of these has (the built-in browser reaches pages the workspace cannot; a fandom
   wiki's api.php gives its card modules), check the copy against the source (length and checksum), and add the source to
   this list.
4. **Cards.** Compare the library's cards with the game's data, by card code and by name. Missing cards, glossary keywords
   and tokens go into `supplement_<game>.py` -> `supplement/<game>.jsonl` (library entities columns; ext_id = the game's
   card code; category keyword for glossary entries). When the source is newer than the library, the supplement holds
   every card and replaces the library's entry with the same code (source.py). A card with no text is still a card.
   Ids: the game's block in source.py; definitions Kaptain gives (`supplement/<game>_kaptain.jsonl`) from start + 900,000.
   Keywords-field entries that are data artefacts go to NOT_KEYWORDS in build_input.py with the proof.
   **Take every form of a card by its code, not by its name**: a champion's level-up form, a transformed side, a token
   often shares the base card's name (Riot: Bard 06RU001 and Bard 06RU001T4). Taking cards by name lost 11 Runeterra
   level-up forms (Bard, Jhin, Jax ...): their level-ups and everything they do were missing from every network. Write the
   links between the new cards too (`supplement/<game>_links.jsonl`: transforms_into, generates; source.py loads them): the
   library has links only for its own cards.
5. **Keyword definitions** come from the game's own glossary, with the source in source_type. Kaptain is asked only for a
   keyword no source defines. Glossary terms no card uses are left out.
6. **The game's words** (readers can only use values that exist). For every term of the checklist (stats, board, turn
   structure, zones, card kinds, statuses): an existing value with the same meaning, mapped in BRIEF.md "Game words:
   <game>"; or a new vocab row (rule 3). Do not stretch an old value. Decide the mapping from the game's rules (marked as
   Claude's); ask Kaptain only what no source settles. Give every keyword its vocab keyword row now.
7. **Numbers per card level** ("1/2/3/4/5"): `{"x": "per_level", "items": [...]}` in level order.
8. `python3 build_input.py <game> 20000`; a 10% sample for the second reading in `input/<game>/second_001.jsonl`.
9. Add the game's trigger labels and verbs to `patterns/patterns.tsv` (judged as step 2.2 says).
10. **The game's rules** (`read/<game>/game_rules.jsonl`): from `library/tools/games/<game>.md` ("The game" and the terms),
   write what every unit (or card of a category) does that no card text says, as one record: name "Game rule: ...",
   `applies_to` (categories), `source` (the line it comes from), abilities on event always with pick self. The three games
   write how units fight: Runeterra `start_attack` self, `strike` self to an enemy unit, or (link or) to the enemy player;
   Stormbound strike to an enemy unit or structure, or the enemy base; Monster Train strike to an enemy unit. Not written:
   what every unit does all the time and says nothing about which cards belong together (Stormbound units moving forward).
   refs.py copies the rows to every card of the category as origin game, except units that can never attack (Immobile);
   the network weights them less than a card that says it; card queries (ask.py, mechanics.py, connections.py) leave them out.

### 1. Reading
- Readers: background agents, model sonnet, the prompt in READER_PROMPT.md. Three in parallel: cards, keywords, second
  reading. Never merge, normalize or rebuild while a reader runs (`run.py` refuses while part files exist).
- Check every keyword record by eye: all cards with a keyword inherit it. A trigger keyword that does something by itself
  (Monster Train Eaten: the unit is eaten after combat) has that act in its record; cards using its label get the keyword.

### 2. After the readings (each item once, in this order)
1. `python3 run.py <game>`: normalize, check, load, cases, word check, status, examples. It stops at the first failure.
2. Proposals: tally `*.proposals.jsonl`. A need that repeats gets a value (rule 3); then fix the unsure cards by a rule
   script, not a re-read (Monster Train: "15x the number of" -> x product for every card at once). What is left is unique
   to one card and stays unsure.
3. Word check (`pattern_check.py <game>`). Patterns name what a record must contain: trigger labels, standard verbs,
   duration words, keywords named outside the Keywords field. Judge each pattern once by its hits: narrow a regex that
   catches other meanings ("damage shield" is no damage), with the reason in the file. Each flag left is decided by
   Claude against the text and written to `patterns/verdicts.tsv`.
4. Names: every stub is a card, keyword or token from the game's data (add it to the supplement), a family (name_has), a
   type, or a misreading (`names.tsv`). Never guess.
5. Second reading: `compare.py` lists differences; Claude judges them against the text. A kept reading that is wrong is
   fixed; each "same meaning, different form" becomes a normalize rule for all games.
6. Rebuild every game once (`run.py <each game>`); all cases must pass.
7. **Link audit** (`audit_links.py <game>`, also printed by run.py): every line it prints is a link that cannot exist. Each
   is fixed at its cause (a missing `causes`, a keyword with no concept row or no record, a level-up form the source lacks,
   a misread name) or explained in RESULTS.md. A game is not done while a line is unexplained.
8. **Deck networks** (`network_page.py` draws every deck in decks.tsv and cases/decks.tsv; `ask.py <game> network "<deck>"`):
   open the page and read every guide deck's network the way a player would: does each card that waits for something
   get a line from the cards that do it? Kaptain found 15 gaps in 9 decks this way that 500 passing cases had not shown.
   Each gap becomes a cases/network.tsv row (a line that must be there, or must not) and is fixed for every card.

### 3. Case tests (`cases/`)
- mechanics.tsv: a question, the expected cards from the texts (regex on the text, or a Keywords-field keyword) and the
  query. Passes at 95%. Every trigger word, every keyword, every common verb. Shared changes: rows with game `*`.
- decks.tsv: **real decks from players' guides are the benchmark.** Each row: the guide's cards and the phrases
  `ask.py <game> analyze` must say so the deck is explained the way the guide explains it. Run them early: in Monster
  Train they showed the explainer missing keyword stacks, types, spell triggers and Morsels being eaten, all fixed in
  shared code for every game. A guide deck the explainer cannot explain is a gap to fix, not a case to drop.
- combos.tsv: pairs a guide names, plus the library's combos rows; the source column says which guide.
- network.tsv: lines of a guide deck's network that must be there, or must not (Kaptain's checks of the networks; a
  wrong line is a "none" row, with why_not when only one reason is wrong).
- regions.tsv: the library's signature, splash and archetype rows per faction.
- A failing case is fixed at its cause: the query (check it against the texts first), the pattern, the value, the shared
  code or the records. A case built on wrong old tags is dropped with its reason in DROPPED.md.
- Guide decks go to readers? No: readers describe only what a text says, and a deck would invite links the text does not
  state. Decks test the result.

### 4. Kaptain's check
`check_table.py CHECK_20_<game>.md --random <game> 20` (save the ids in CHECK_20_<game>_ids.txt). Each card: one line with
its name and text, then its rows. Every error he finds is fixed for all cards with the same problem.

### 5. Done when
`run.py <game>` passes every step and every other game still passes; the keyword -> concept list checked twice and shown
to Kaptain; word check 0 open flags; no proposal need shared by cards with different texts; stubs only names nothing
defines; `ask.py all compare <its main concepts>` shows its cards next to the other games'; every guide deck explained;
Kaptain approved CHECK_20_<game>; audit_links.py prints nothing unexplained; every guide deck's network read (step 2.8)
and its gaps fixed; RESULTS.md and HANDOFF.md say the state; everything pushed. After his approval, add a few
approved records to BRIEF.md under "Game words: <game>" as worked examples.

## Asking the database
`ask.py <games> ...` where <games> is one game, several (runeterra,stormbound) or all: `cares|makes <happening or concept>
[mine|enemy]`, `concept <concept>`, `both <A> <B>`, `compare <concept> ...`, `together|feeds|fed|chains <concept>`,
`<game> deck <card or concept>`, `<game> analyze "<cards>"`, `<game> network ...`, `combo <A> <B>`, `partners <card>`,
`card <card>`, `list happenings|concepts`. QUERIES.md has example questions with real answers. For "which cards care
about X" use flat_ref (ask.py cares): the same thing is stored as a trigger, a condition, a count or a target filter.

## Surviving session limits
- `python3 status.py <game>` says from the files which batches are done, partial or todo.
- Readers write in parts (`<batch>.partN.jsonl`); a stopped reader is resumed (it continues from its parts).
- Every finished step is pushed at once. Chats end with HANDOFF.md updated.

## Links the deck networks showed missing (29 Oct 2026; Kaptain's check of 9 decks; fixed in every game)
The records were right card by card, but the links between cards were not: a network is only as good as the rule that
joins "A makes X" to "B waits for X". What went wrong, how it was missed, and the rule now:
1. **The kind of thing hit was dropped.** `damage` causes dies, survives_damage and nexus_damaged whatever it hits, so a
   unit damaging its own base "made units die" (Reckless Rushers -> Green Prototypes) and Falling Star (an enemy unit)
   "damaged the Nexus". Missed because every case asked "who makes X", never "who must NOT". Rule: refs.py keeps unit-only
   and player-only happenings to their kinds; network.py joins only kinds that fit (kinds_fit).
2. **"Me" was lost in conditions.** "I've survived 10+ damage" (Braum) stored its event object without the pick, so it
   read as any unit surviving; "when I level up" (LeBlanc) took Ashe levelling up. Rule: flat_if keeps ev_obj_pick and
   attr; a need about the card itself is fed only by what is done to my units; two cards each about themselves never link.
   When the query layer flattens a record, every field that changes the meaning (pick, side, kind, attr, with) is kept.
   "It" keeps the side of the target before it ("give a random enemy +2, then give it Vitalize": the enemy), or a buff
   to an enemy reads as a buff to anyone (Green Prototypes -> Booming Professors).
3. **Planted and placed cards were no cards.** Chime, Poison Puffcap, Flashbomb Trap, Mysterious Portal are planted by a
   keyword action with a card; the network only followed summon/create. Rule: an effect that names a card puts that card
   in (keyword_action included); a planted card going off is trap_activated (normalize N15; "activated" is a player using
   something). Bard levels from Cosmic Binding's Chimes; Caitlyn from every trap planter.
4. **Readers narrowed a class to one card.** "5+ of your traps have been activated" was read as card Flashbomb Trap, so
   Poison Puffcaps did not count; "Trap" as a name family missed Puffcaps. Rule (BRIEF 23): "your traps / boons / spells /
   Imps" is the keyword, category or type filter, never one card or a name family. Fixed by rule (fixes/runeterra/v30.py).
5. **Keyword records were not the card's needs.** Plunder, Reputation, Nightfall, Deep ... are conditions in the keyword's
   record; the network took only a card's own rows. Rule: a keyword condition the card uses is the card's need.
6. **Things a card tests or picks by had no maker.** A stat tested ("the enemy Nexus has half its Health": Darius), a
   position picked by ("the enemy in front", "bordering enemies": Booming Professors, Chaotic Pupil), units that can't be
   blocked (they hit the Nexus), units that strike (they deal damage), moves, challenges, captures, Predict, Countdown: no
   act said it caused them. Rule: refs.py feeds a tested stat from what changes it and a position filter from moves; vocab
   `causes` was completed (move, swap, challenge, capture, Predict, Countdown, Trap, Boon, Elusive, Overwhelm). Every new
   event, state or test needs its makers before a game is done; audit_links.py lists those nothing makes.
7. **Groups of cards acted on were ignored.** Doctor Mia repeats structures, Ava Achiever doubles traps, Teemo 2 copies
   Puffcaps, Norra 2 changes Portals: only Attack/Support repeats were followed. Rule: repeat, increase_effect, copy and
   give_ability on a named group link to every card of the group, on either side when the group is named (traps on enemy
   cards are still mine).
8. **Cards that are what another waits for, and kinds of card another needs.** A spell is what "Fast spells, Slow spells or
   Skills you've played" counts (Ravenbloom Conservatory); a structure is what "units surrounding a friendly structure"
   needs (Fortification Tonic). Rule: played_lines and need_lines match the card itself against the filter.
9. **Helping is a link too.** Power buffs and Elusive, Overwhelm, Quick Attack, Challenger given to my units help every card
   that counts damage my side deals (Darius, LeBlanc, Reputation): weak "makes its damage bigger" lines.
10. **33 Runeterra keywords had no vocab concept row** (Plunder, Countdown, Last Breath ... ; Runeterra predates rule 2 of
   "Writing data the same way"), so concept questions missed them. Mapped from Riot's glossary (Claude's, for Kaptain's
   check); audit_links.py lists any keyword without one.
How it was missed: every test asked whether the query finds the cards that do X; none asked whether two cards of a real
deck are joined, or must not be. Read the networks of guide decks (step 2.8) before calling a game done.
Second check (Kaptain, 29 Oct 2026), fixed in every game: a champion linked to its own level-up form (one card in play);
spells and skills not counted for "N spells or Skills played" (a skill is an ability card the unit casts: it is put in the
network, kind spell takes it when the filter says Skill); "help" that is no event was missing (more health helps a card
that must survive damage; more power helps a card that counts damage dealt or Nexus hits, and Challenger and Overwhelm
units; Elusive or Overwhelm given helps cards that count hits on the enemy player; creating cards helps "N different cards
played"; a planter helps what its planted card levels); a card whose own trigger makes what its level-up counts (Ashe:
Attack -> Frostbite -> level) levels from anything that sets the trigger off (Rally); an ability given to the player that
adds to what happened (Tybaulk: "your spells and Skills deal 1 extra damage") makes those cards stronger, other given
abilities are fed like the card's own; "I strike / I kill" is about the card, not the unit it hits; "it" first refers to
what the event happened to; a "non-X" filter narrows nothing; what a card creates by description ("2 random Imps") is no
need for that type; the combo search (connections.py) is no source of network lines (its weak reasons, "counts card",
"target: type", were noise); a count of a keyword used names the card when the text does ("planted 15+ Poison Puffcaps").

More found 29 Oct 2026 (v33, all games): an effect that adds to what my cards of a kind just did ("your spells and Skills
deal 1 extra damage", "double all damage dealt by your spells") helps every card of that kind in the deck that does it, also
through a keyword it uses (Drain) and through Skills; it waits for nothing itself (Tybaulk, Funsmith, The Dreadway); "it"
there is what was hit only while no earlier effect named a new target (Azir's summoned Sand Soldier is not the attacker);
a lasting change to all my cards of a kind, or to them in hand and deck ("grant allies everywhere +1|+0", "friendly units
in front get 2 strength each turn") helps each of them; a boost to a status ("Rage on friendly units adds +3 Attack")
helps the cards that give it; damage as big as a card's health is no "survives damage" help (Sunburst 6, Braum 6); a
card made by description ("2 random Imps") is a card of that type for what asks for the type; a counted card with a state
("8 cost reduced cards played") is fed only by cards that put it in that state; "spells and Skills" in a text includes
Skills in every target the phrase names (fixes/runeterra/v33.py); a level-up form's power and health are its stats field.

## Think like a player (read before showing any network, any deck explanation, any answer about synergy)
Kaptain checks a few decks and finds errors a player sees at once. Before showing anything, do what he does:
1. Take every guide deck of the game and read its network line by line, both cards' texts side by side. For each line ask
   "would a player who knows this game say A helps B for this reason?" If not, find the rule that made it and fix the
   rule, for every game. Then ask the other way: "what does a player know helps B?" (its level-up, its triggers, its
   conditions, its stats, its keywords) and check each is there.
2. Game facts that are never broken: a champion and its level-up form are one card in play (copies level together); a
   card's "I / me / my / itself / this unit" is that card; damage to a player is not damage to a unit; keywords do what the
   glossary says and nothing more (Overwhelm sends leftover damage to the Nexus, it adds no damage; Frostbite sets Power to
   0, a frostbitten unit can still block); skills are not spells unless the text says "spells or Skills".
3. "Helps" is wider than "makes what it waits for": more stats, protection, extra attacks, more cards, cheaper cards all
   help the card that needs them. A line is right when the help is real, not when the words match.
4. Tell Kaptain which lines you are not sure of, with the card text, instead of leaving them for him to find. Never say a
   check is done when only the counted cases pass.
5. When Kaptain finds one wrong line, look for the whole family of it: list every line of every game made by the same rule
   and read a sample of 20 before and after the fix.

## Mistakes made before (do not repeat)
- Fetching a game's data the repo already had; trusting old library tags; judging data by one narrow question; assuming
  "missing" or "broken" without checking the game's data; writing a definition from memory.
- One value with several meanings (zone discard for dead, discarded and tossed cards; now BRIEF rule 17); a keyword
  recorded as the wrong kind (Drain as a status).
- Re-reads trusted blindly; rebuilding while a reader wrote; patch scripts not safe to run twice; card names inside texts
  taken as wording.
- Shared-code bugs no case caught (a played card "setting off" a trigger that asks for another type; 'type is 1' matched
  inside 'type is 11'): found only by reading `partners` answers.
- Turning a decision back and forth instead of looking up CHANGES.md and asking Kaptain.
