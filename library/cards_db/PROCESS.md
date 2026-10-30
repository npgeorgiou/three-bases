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
6. **The query layer dropped what the rows had.** The rows said "allied Pykes", "non-combat damage", "a card with
   Nightfall", "Capture is used", but flat.py, refs.py or network.py did not carry or read that part, so the links were
   wrong although the data was right. Now flat_when/flat_if/flat_ref keep who does it (actor_kind, actor_with), the
   network checks it and the origin (combat) filter, label keywords a filter names ("Nightfall:") are the card's keywords
   (load.py), and "used a keyword" matches by the keyword. Rule: a new field or filter in the rows is not done until the
   query layer keeps it and the network reads it; network.PLAY_STATE lists the filters it ignores on purpose.
7. **"Done" was said on counts.** Cases passing says nothing about the links nobody wrote a case for. Before showing a
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
4. Batch the work: collect all problems of one kind (all proposals, all flags, all failing cases, all wrong deck lines),
   decide them together, fix them with one rule or script, then rebuild once. Never rebuild between single edits. (Faeria,
   29 Oct 2026: fixing deck by deck with a rebuild of six games after each fix cost over an hour.)
5. Fix by rule, for every card: a regex over the texts or a script over the records (`fixes/<game>/vNN.py`, safe to run
   twice). A re-read by a reader is the last resort, for cards no rule can fix.
6. Readers are expensive (~110-125k tokens each, whatever the batch size): one for the cards, one for the keywords, one for
   the second reading. A few cards (tokens, a handful of fixes) are written by Claude directly.
7. Read the answers, not only the counts: before calling a step done, run `ask.py <game> partners <card>` and
   `analyze` on a guide deck and read them. A case count that passes says nothing about a link that should not exist.
8. Shared code (connections.py, refs.py, flat.py, deck_analysis.py, normalize.py, load.py) serves every game: a change
   there gets a mechanics.tsv case with game `*`, and every game's cases must pass before it is pushed: run `run.py <your
   game>` (it loads every game into cards.sqlite), then `cases/run.py <other game>` for each other game. Never run
   `run.py` for a game another chat is importing: it normalizes and rewrites that chat's records, flags and reports.

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
     `inscryption_missing_cards.json` (partial: only the cards the library missed; the whole set is
     `inscryption_wiki_cards.jsonl` + `inscryption_wiki_cards_more.jsonl`, wiki pages with their revisions, 29 Oct 2026), `faeria_merlin_shortened.csv` + `faeria_cards_english.csv` (462 Faeria cards,
     Abrakam's github.com/abrakam/Faeria_Cards 12b7207; its README defines the keywords). Named sources: Lorcana (npm lorcana-oracle), Star Wars: Unlimited (swucardex-data
     a86faed), Elder Scrolls: Legends (TESLegendsTracker c541e82), Slay the Spire (wiki Module:Cards/data), Slay the Spire 2
     (Kaptain's lists, 12 Oct 2026), Gwent (gwent.one v14.8), Magic (MTGJSON AtomicCards, Scryfall tokens), Shadowverse
     (Portal API), 40k and Age of Sigmar (BSData). Duelyst: `library/tools/convert/duelyst_cards.psv` (1116 cards, conv_duelyst.py over
     github.com/open-duelyst/duelyst 2843f24; the repo's tutorial and tips are the rules source).
   - `library/tools/games/<game>.md`: research, sources, and the keyword terms with the page each comes from. Check each
     term's source is this game and drop terms marked "assumed" (rule 1).
   - `library/cards_db/supplement/<game>*`: games already imported here.
   Fetch from the web only what none of these has (the built-in browser reaches pages the workspace cannot; a fandom
   wiki's api.php gives its card modules), check the copy against the source (length and checksum), and add the source to
   this list.
4. **Cards.** Compare the library's cards with the game's data, by card code, by name and by text (render the source's
   markup and diff every text: Faeria's library kept markup in 13 cards). Missing cards, glossary keywords
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
6. **The game's words** (readers can only use values that exist). A game with a board maps its words to BRIEF "The board"
   first (spaces, neighbours, areas, ground, movement, placement, board resources), adding a value only for what it lacks. For every term of the checklist (stats, board, turn
   structure, zones, card kinds, statuses): an existing value with the same meaning, mapped in BRIEF.md "Game words:
   <game>"; or a new vocab row (rule 3). Do not stretch an old value. Decide the mapping from the game's rules (marked as
   Claude's); ask Kaptain only what no source settles. Give every keyword its vocab keyword row now.
7. **Numbers per card level** ("1/2/3/4/5"): `{"x": "per_level", "items": [...]}` in level order.
8. `python3 build_input.py <game> 20000`; a 10% sample for the second reading in `input/<game>/second_001.jsonl`.
9. Add the game's trigger labels and verbs to `patterns/patterns.tsv` (judged as step 2.2 says).
10. **The game's rules** (`read/<game>/game_rules.jsonl`), researched before readers run, because they decide most deck-
   network lines: how units fight, move and reach the enemy player, and on a board where cards may enter and how the board
   grows (who may build or claim spaces, next to what; Faeria's were missing and caused most of its network errors). Take
   them from the game's own rules (tutorial, rulebook, help pages, wiki),
   written with their sources into `library/tools/games/<game>.md` ("The game's rules (from sources)" or sourced terms; never
   the "Claude's summary" lines, which came from memory: audit_links check 8),
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
6. Rebuild your game once (`run.py <your game>`) and check every other game read-only (`cases/run.py <game>`); all cases
   must pass. Games no other chat is working on may be rebuilt with their own run.py.
7. **Text audit** (`audit_text.py <game> [--list <rule>]`, also printed by run.py): every card whose text has a word its rows
   do not show ("or the enemy Nexus" without a player target, "spells and Skills" without Skills, "everywhere" without
   the zone). Read each listed card: fix the family by a rule script, or add the card to audit_text_explained.tsv with
   why the rows are right (they say it another way, or the words are no effect).
   A new kind of reading error found later becomes a new rule in audit_text.py, so the next game is checked for it.
8. **Link audit** (`audit_links.py <game>`, also printed by run.py): every line it prints is a link that cannot exist. Each
   is fixed at its cause (a missing `causes`, a keyword with no concept row or no record, a level-up form the source lacks,
   a misread name) or explained in RESULTS.md. A game is not done while a line is unexplained.
9. **Deck networks** (`network_page.py` draws every deck in decks.tsv and cases/decks.tsv; `ask.py <game> network "<deck>"`).
   First read ALL decks and write every wrong or missing line into `deck_read_<game>.md` (deck, from, to, what is wrong);
   only then group them into families and fix each family once:
   find full decks first (players' guides, deck sites, deck codes; full lists, not a guide's core cards). A full deck has
   every copy: the counts add up to the deck size the game sets (Inscryption Act II battle decks: 20), and the source
   column says the counts and the size; decks.tsv lists each card once. A roguelike's starter deck (Inscryption Act I,
   Kaycee's Mod: 4 cards and a side deck) is where a run starts: keep it, marked as a starter, but it does not count
   toward the 10 full decks; when fewer than 10 full decks exist as text, say so in RESULTS.md. Read at least 10
   decks card by card, as a player: for each card, what does it need (level-up, trigger, condition, stats, keywords) and
   which cards in the deck give it that; what does it give, and to whom; is every line's reason true by the texts? Kaptain
   found 15 gaps in 9 decks that 500 passing cases had not shown, and Claude's own read of 9 decks found 8 more families.
   Each gap is fixed for every card of every game (a rule, never one card), becomes a cases/network.tsv row, and its
   lesson is written in "Links the deck networks showed missing".

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
When Kaptain does not know the game (Inscryption), he cannot check rows: Claude checks the 20 cards against their texts
and the sources of step 0.10 itself, writes every error into deck_read_<game>.md ("Check of 20 cards"), fixes each family
once, and adds a case per family. Kaptain then checks the deck networks page (network_page.py) in plain words: does a line
between two cards make sense to a player. Every point he finds is fixed as "Fixing a review" says.

### 5. Done when
`run.py <game>` passes every step and every other game still passes; read/<game>/game_rules.jsonl written (step 0.10);
audit_text.py and audit_links.py print nothing unexplained; the keyword -> concept list checked twice and shown
to Kaptain; word check 0 open flags; no proposal need shared by cards with different texts; stubs only names nothing
defines; `ask.py all compare <its main concepts>` shows its cards next to the other games'; every guide deck explained;
Kaptain approved CHECK_20_<game> (or, for a game he does not know, Claude's check in deck_read_<game>.md); at least 10 full decks' networks read card by card (step 2.9)
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
deck are joined, or must not be. Read the networks of guide decks (step 2.9) before calling a game done.
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

Found by reading guide decks card by card, 29 Oct 2026 (v34, fixed for all games): a count of what happens to my cards of a kind
("destroyed 4+ allied landmarks") is fed by cards of that kind and cards that make one by description (Bomber Twins ->
Ziggs); "non-combat damage" is not fed by units fighting (Swain); a need that names who does it ("allied Pykes have dealt")
is fed only by that doer or a card that makes such a unit fight; "used a keyword" (Capture) matches makers of that keyword
(An Acquired Taste -> Tahm Kench); an ability that helps the card that comes ("the next card with Nightfall costs 1 less",
"when you summon an Elite, grant it +1|+1") makes every card of that kind stronger; what a card does to itself only feeds a
need its own kind fits (Heliotroopers poisoning itself is no Dragon for Sunbeam Serpents); "last card in hand" is helped by
discarding, "cards in hand" by drawing and creating (First Mutineer -> Northsea Dogs).

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

## A card list that looked whole (Inscryption, 29 Oct 2026; checked in every game)
1. **The library's entries were not the game's cards.** Its 164 Inscryption units came from the wiki, but cards with the same
   text had been merged (Hawk, Raven, Sparrow, Mothman into Bat; Skeleton into Revenant), cards without sigils were dropped
   (Wolf, Coyote, Grizzly, Stoat, Opossum), and a page's tabs were stored under the tab's label (Left, Right, Normal, Base
   Form). The starter decks named cards the database did not have. Rule: before the readers, every card of every guide deck
   must be a card of the game; audit_links.py check 5 lists deck cards that are not. When the source is not whole, the
   supplement holds every card and source.py FULL replaces the library's categories for that game.
2. **A wiki page can hold several cards.** Empty Vessel's page has a second box (the three Gem Vessels), Trees a second box
   (Act III trees): take every card box of a page, not the first, and every tab of a box. Read every field of the source's
   card, not only the text: Inscryption's box field special_behaviours names code that changes play (Ouroboros grows each
   time it dies, Cat becomes Undead Cat, Strange Frog leaves a Leaping Trap); without it the Ouroboros decks had no plan.
   Their effects come from the wiki page Special Card Behaviours and are now in the cards' text (case ni09).
3. **Keywords belong in the Keywords field.** Written as "Sigils: Airborne." every card needed a reader and inherited nothing;
   as "Keywords: Airborne." 222 of 285 cards need no reading and take their sigils' records. A game whose cards list keywords
   (sigils, traits that the game defines) writes them in the Keywords field.
4. **Keyword records were never audited.** audit_text.py read card texts only ("a keyword's text is the glossary"); in
   Inscryption every card is its sigils, so a misread sigil is every card's error. It now reads keyword entries too (the
   rulebook line when the entry has one; trigger and condition keywords say it by their form). It found errors in other
   games' keyword records: Runeterra SpellShield and Flow lacked Skills (v33's rule ran on card batches only, now on
   keywords too), Spawn's "For each Spawn" lacked its repetition (fixes/runeterra/v36.py).
5. **Readers used another game's words.** Hefty and Rampager moves were written with keyword Push (a Stormbound keyword),
   and "in the way" with in_front / behind (a column's words on Inscryption's row of spaces). Names: a keyword that is no
   keyword of the game is dropped from the effect, the effect stays (normalize N6); the row's neighbours are sides.
6. **One happening, two forms, found by the second reading.** "Moves" had the moving unit as actor in Sentry: normalize N16
   (the moving unit is the object) and case mx12.
7. **Costs were no needs.** A Zombie (2 Bones) had no line from the Gravedigger that makes Bones, a Hawk (2 Blood) none from
   the Squirrel sacrificed for it: the network never read a card's cost. Now a game rule can name a cost word
   (`"cost_has": "Bones"`, read/<game>/game_rules.jsonl): its conditions become the needs of every card whose cost names it
   (refs.py, network.py "pays its cost"); a resource kind (Bones, gems) is fed by gaining it, and a coloured resource only by
   its colour (a Green Mox cost by a Green gem: network.colour_fit). Cases ni01-ni05. Doing it found a shared bug: load.py had
   lost every card's cost and spell speed (both sat inside a comment since v35); the card table now also keeps the cost text.
8. **Giving up my own unit had three forms** (kill on my unit in Faeria, Monster Train's Sacrifice record, nothing in
   Inscryption): one act sacrifice (causes sacrificed and dies), normalize N17 for card records.
9. **Help through the card that is paid for.** Worthy Sacrifice ("counts as 3 Blood") and Morsel act on the card they are
   sacrificed for (pick actor of event sacrificed): network.actor_help_lines gives them a line to every card of the deck that
   needs that happening (M3atB0t makes Urayuli cheaper, case ni06). An ability that spends a resource ("Activate: pay 1
   Bone") needs it like a cost does (refs.py; Bone Lord's Horn -> Tomb Robber, ni07). A cost of 0 ("0 Blood") is no need (ni08).
10. **A keyword entry without its definition.** The library kept only the wiki's pointer line for Ants and Ant ("This
   article is about the variable stat..."), so the readers wrote nothing and no Ant counted the others. The definitions now
   come from the wiki pages (supplement), audit_links.py check 6 lists any such entry, case ni11. Where a new card is put
   ("Pelt Lice in adjacent slots") needs no units to move (refs.py PLACES, ni12).
11. **The deck explainer and the combo search did not know the game's rules.** "Gravedigger: no clear role" and "Adder waits
   for sacrifices, nothing in the deck does it": ask.py analyze now reads cost needs and counts what the rules make (any
   unit can be sacrificed, a Skeleton's death gives a Bone), deck cases di01-di04; connections.py goes one step through a
   rule about the owner's own cards (Necromancer's second deaths give Bones for Tomb Robber, combo cases ci07-ci08).
12. **Keyword records are not normalized by run.py** (it normalizes card batches only). A game whose cards are mostly their
   keywords (Inscryption) applies the normalize rules to keywords.jsonl in its fix script (fixes/inscryption/v36.py:
   names, moves object, sacrifice form).
13. **Board games, positions (29 Oct 2026, v38-v39; for every positional game).** Read every sigil that names a place and
   write it in BRIEF "The board" forms; check the place, not only the act: a strike into an empty opposing space hits the
   opponent (strike to the player, link or); "moves towards them" = sides of them; "rotate one space" = bordering; a space
   struck on my side is side mine (Burrower). The concepts follow from the forms for every game (flat.py): same_lane ->
   lanes, in_circuit -> link_formation, a strike on the sides of the opposing space -> cross_lane. Lines say where help
   works: an aimed line with a position filter ends "(when next to it)". A circuit needs two conduit cards (wiki Circuits),
   so "within a circuit" also counts two Conduit Cards of mine.
14. **Who benefits from a place: three network gaps (v39, every game).** A keyword's effect on other cards (Leader: "creatures
   adjacent gain 1 Power") made no line, only the card's own text did: aimed lines now read has_keyword rows too (ni15). A
   card that names another card in a filter ("if a Chime or Bell Tentacle is attacked") made no line from that card: it
   now says "is the Bell Tentacle it names" (ni16). A trigger on an enemy attacking my unit took the side of the unit
   attacked, so my own attacks fed it "by fighting": attacks, strikes, fights and challenges take the doer's side (refs.py
   DONE_BY, ni17). A network case's deck column may be a card list when no deck has the cards.
16. **Room and full sides (v40, every positional game).** The Moon "replaces all spaces on its side with itself": a unit's
   room is stat size (Monster Train's unit capacity), here the count of its side's spaces; "board full" = no empty space
   on that side (BRIEF "The board", Room). Size changes are concept board_limit.
17. **Decks that were not full.** Inscryption's decks were starters (4-7 cards) and players' cores without counts; Kaptain
   saw too few cards and lines. Only 5 full 20-card decks exist as text (Steam threads); step 2.9 now says what a full
   deck is and that starters do not count.
15. **More or faster base resource** (Kaptain 29 Oct 2026: not linked to costs, but findable): concept base_resource_gain
   (mana, spell mana, Ember, faeria, Energy; a second resource such as Bones or gems stays resource_gain), `ask.py
   <game> factions base_resource_gain` gives each faction's share, and ask.py analyze names the ramp cards. Cases mx16, ri08.

## Importing Duelyst (29 Oct 2026; checked in every game)
1. **The game file's rules were written from memory.** duelyst.md "The game" (Claude's summary) said a unit on a mana
   spring gains the mana and minions are summoned next to a friendly unit; the game's own tutorial and tips say the player
   gains it and summoning is around any friendly unit. Runeterra's, Monster Train's, Faeria's and Inscryption's game rules
   cited the same kind of summary. Rule: game rules cite the game's own rules with their source (step 0.10); audit_links
   check 8 lists a game whose game_rules.jsonl cites a "The game" section written from memory (Runeterra, Monster Train and
   Faeria now cite Riot's round FAQ, a beginner's guide and Wikipedia's Gameplay section; Inscryption cites the wiki's
   Card Battle, cost and Circuits pages and Wikipedia).
2. **One name, two cards.** The open-sourced data has Tempest and its Bloodbound Spell copy, the tutorial's Argeon Highmayne,
   Cascading Rebirth's follow-up, 14 Build structures called Building: a deck or a text naming one got either. Rule: the
   collectible card keeps the name, the others are "<name> (<kind>)" (supplement_duelyst.py names()); audit_links check 7
   lists names two cards of a game share.
3. **Decks from deck codes.** Duelyst deck pages give a base64 code of card ids; the ids are the game's own (cardsLookup).
   Codes from Duelyst II pages decode to ids the original game lacks: such a deck is another version of the game, not a
   source. Codes and decoded decks are kept (supplement/duelyst_deck_codes.tsv) so the decks can be checked again.
4. **A card kind ending in "Spell" is no type.** build_input.types_of drops subtypes ending in " spell" (Runeterra's spell
   speeds), so "Bloodbound Spell" as a type was refused by check.py. A kind of card that cards filter by and that has a
   keyword entry goes in the Keywords field (the General's spells carry "Keywords: Bloodbound Spell.").
5. **Keywords written as lines.** "Provoke\nCelerity\n..." became "Keywords: Provoke, Celerity." for 178 cards (rule of
   "A card list that looked whole" 3): line breaks in the source must be kept until the Keywords field is cut.

## Duelyst deck read: leaders and the board (29 Oct 2026, v40; deck_read_duelyst.md; checked in every game)
1. **A leader card is its player.** A Duelyst General is a card on the board and the player's life: category `leader`
   (network KIND_CAT player). Help given to "your General" reaches only the leader card; a unit target never matches it;
   the General attacks, strikes and kills as its player (game rules: applies_to unit, leader). Champions stay `hero`.
2. **Who did it keeps its kind and side.** A target picked "actor" (the attacker, a counterattack) takes its event actor's
   kind and side; "it" in an ability on my own attack is the enemy attacked; "it" in a given keyword's record is never the
   holder (Backstab's damage landed on the attacker). Cases ndu01, ndu10.
3. **Positions a card needs are needs for moves.** Backstab (behind an enemy), Zeal (near my General), Infiltrate (enemy
   side): moving the unit or the General feeds them; where a card enters needs no moves (placement). Use the BRIEF "The board"
   positions; concept rules flanking, adjacency (with diagonal), lanes (with center_column), area_templates (corners,
   starting side). Cases du31-du34, ndu07, ndu12.
4. **Help must reach the card it can hit.** A gain on itself helps no other card; a player's extra card handling is no help
   to its leader; effects on the hand or on costs skip tokens only summoned on the board; "anything" chosen on the board is a
   unit or the leader; spells and artifacts are never board targets. Cases ndu04, ndu05, ndu17, ndu23-ndu28.
5. **What a card makes itself it does not wait for** (Abhorrent Unbirth's deaths, Krog's Dinner); a named card asked for in
   play is fed by the cards that make it (Inkling Surge and Wraithlings), not a card naming what it makes itself (Blazing Spines). Cases ndu25, ndu29, ndu30, nfa24.
6. **Card counts by where the card comes from.** "Summoned from your action bar" is played (N24): tokens do not count.
   Stats used as amounts want that stat; a cost equal to a stat wants less of it (Blood Taura). Cases ndu11, ndu18.

## Importing Faeria: the board (29 Oct 2026; checked in every game)
Faeria is played on a hex board that players build; Kaptain uses the library to study positional play, so its board words
were made the shared form for every game with spaces (BRIEF "The board"). What went wrong and the rule now:
1. **The library's texts were not the source's texts.** Its Faeria entries kept export markup ("Choose one: {green.|...")
   and wrote two land icons as "lake lake"; 19 cards were missing. Rule: render the game's own export and compare every text,
   not only the card codes (supplement_faeria.py writes the cards whose text differs). A supplement entry now replaces the
   library entry with the same bare code too (source.py), which also removed Runeterra's duplicate Dragon's Rage.
2. **One board happening, two forms.** "Moves onto enemy land" had the space as object and the mover as actor, "moves" the
   mover as object; "summon adjacent to friendly creatures" was aimed at units, Wind Gate's at spaces; "on or adjacent" was
   one target (Meteor) or two effects (Firestorm); "in its place" had no "of". Rule: BRIEF "The board" (one form each),
   fixes/faeria/v35.py, cases nfa03, nfa04, fa36-fa43.
3. **Board words had no values.** Readers wrote stand-in keywords (Empty, Refill, Extra turn, Destroy) and proposals
   (straight_line). Now: terrain (field and attr), set_terrain, harvest / harvests, moves_onto, same_space, straight_line,
   distance, empty_resource, refill_resource, extra_turn, end_turn, state empty; audit_links lists any stand-in keyword.
4. **Board concepts were never derived.** flat.py RULES now give terrain, territory_trigger, placement_rules, zone_control,
   control_reward, area_templates, adjacency in triggers and positional for ground and distance (cases fa36-fa42).
5. **Who benefits from moves and places.** Movement keywords cause moves and moves_onto (every game's movement keywords).
   network HELPS: what moves another of my units, or gives it a movement keyword, helps a card that must reach enemy land,
   an enemy well, a fight or the enemy player (row by row: the moved unit must be able to be that card; a unit's own Dash
   helps only itself); units that move well help "my units harvest enemy wells". Placement ("summon creatures next to this")
   helps a card whose entry asks for a place. A card counting my lands of a ground is fed by cards making that ground
   (network.terrain_fit: a lake maker feeds "special lands", not "forests"). A place chosen by the player ("on or adjacent
   to a chosen space") and where a card enters need no units to move. Cases nfa12-nfa15.
6. **Needs without a direction.** "Gain faeria equal to its Life" was fed by damage and by a debuff to the god; a threshold
   ("when you would take lethal damage") wanted more Life. Rule: a stat used as an amount or tested high is fed by stat changes
   and healing, never damage; a stat used as a threshold is no need (refs.py); an unnamed stat holder is a unit (nfa06).
7. **The network never read card costs**: "a card with base cost 7 or more" matched every card in every game (cards_of had
   no cost). Fixed for all games (nfa07, nfa08). A big cost cut to a random card in hand aims at cards costing at least that
   much (nfa11).
8. **Tutors.** A draw that names what it draws is from the deck (normalize N23, all games); it links to those cards in the
   deck, never to a card the deck only makes; a keyword on a card drawn or played ("draw a Flying creature") is the card's
   own, not one given in play (nfa05, nfa09, nfa16, nfa17). Triggers on drawing a kind of card are fed by the deck's cards of
   that kind (played_lines also reads drawn).
9. **"It" lost what it was.** "Transform another Rakoan ..., give it Flying" made any unit fly. Rule: "it" keeps the previous
   target's filters, and after a summon of a named card it is that card (flat.py); a need about the card itself is fed only
   by effects that can be that card (network lines_of and HELPS; nfa03).
11. **The deck explainer (ask.py analyze) had the network's old faults**: it joined a god healed with "units healed" (no
   kinds), let a unit moving itself feed another's Corrupt, took the rules' kills of enemies as friendly deaths (every unit
   "made" Soul Eater's deaths), counted cards that make a type by description as caring about it (no Rakoan plan), and had
   no role for paying for big cards. Rule: the explainer joins makers and needs by the same tests as network.py (kinds,
   sides of the rules' rows, "about itself", who the maker acts on); role "Pays for big cards". Deck cases dfa01-dfa05.
10. **Trigger labels written "Name -".** Faeria's "Corrupt - ..." was not the card's keyword (load.py read only "Name:"), so
   "whenever a creature triggers a Corrupt ability" had no makers (fa43).

## Kaptain's check of the Faeria networks (29 Oct 2026; 24 points, fixed for every game; deck_read_faeria.md)
1. **Labels read backwards.** Arrows go from the card that provides to the card that uses it; "is a card it needs" read as
   if the start needed the end. Kinds and page names (30 Oct, agreed): "does what it waits for" (a trigger or a counted
   event), "enables" (a thing that must be there), makes cheaper / makes stronger / gives keyword / moves into place /
   clears the way (help, by how). Reasons are the first card's active verb ("kills it for its death effect").
2. **Help aimed at one chosen or random card was a faint "can aim at it".** A buff, a movement keyword, a cost cut or a
   heal aimed at a card of a kind (Oakling's random green creature, Horsemaster's Charge, Khalim's Training on "a creature"
   of either side) is "helps" to each card it can hit, weight shared (network.helps_it; cases nfa19, nfa20, nfa30).
3. **Paying for big cards.** Mana gain and cost cuts help the game's top tenth of costs when they pay a third of the cost,
   and only the cards a cut names (nfa23, nfa33, nfa39).
4. **The board grows from my units (Faeria game rules: land next to my creatures, summon on my own land).** Whatever moves my
   units or land forward (move effects, movement keywords given or owned, land movers, units made with movement keywords)
   helps cards whose entry asks for a place measured from themselves (Bomb Slinger, Axe Grinder) and cards that need my
   units deep in enemy ground (enemy wells, enemy land); what moves a card helps "units summoned next to this" (Mistral
   Guide). Read only when the game's own rules say the board grows next to units (nfa21, nfa26-nfa28).
5. **A straight line of fire** (a keyword whose strike hits the nearest enemy in a straight line: Faeria Ranged) is helped by
   removing or moving enemy units and by moving the shooter by an effect (nfa22).
6. **Needs that are none.** An ability that only destroys its own card waits for nothing (Krog's Dinner, nfa24); harm aimed
   at "a creature" of either side is no friendly death for death counters (nfa25) but is aimed at my own unit whose own
   death effect it sets off (nfa40); "if Krog has died" kept its card filter. Wrong and removed 30 Oct: "units are struck
   back when they fight, so they can die" (Claude's own addition; it linked every creature to Soul Eater).
7. **A code line lost in a comment.** A scripted replacement left aimed_rows' filter inside a comment for a whole session.
   Rule: after any scripted edit of shared code, read `git diff` of that file before rebuilding.
8. Page: cost and Attack|Life on every card, keywords once, a deck drop-down per game, decks listed once, nodes pulled closer.

## Fixing a review: by cause, never by example (30 Oct 2026; read before touching any point Kaptain raises)
Kaptain reviews a few decks: a sliver of the cards. Each point he finds is a sample of a rule that is wrong everywhere it
fires. Twice Claude fixed the named lines only, and added rules of its own without looking at what they did elsewhere; he
then found the same errors again. Why it happens, so it can be watched for: Claude reads a point as a task ("this line is
wrong"), finds the code that drew that line, changes it until the line goes, sees the counted tests pass, and stops. The
point is answered; the rule behind it is never looked at across the games. Do this instead, in this order, every time:
1. Before any change: `python3 dump_lines.py /tmp/before.tsv` (every line of every deck of every game).
2. For each point: find the rule that drew the line (file, function, condition) and the reading behind it (`flat_ref`,
   `flat_do` rows of both cards). Name the cause in one sentence, not the card.
3. Group the points by cause (families). For each cause ask what else it does: `dump_lines.py --find /tmp/before.tsv <reason>`
   counts the same reason in every game; read 10 examples per game. Ask also which nearby rules share the cause (the same
   filter dropped by another rule, the same "every unit" by another game rule).
4. Fix each cause once, in the shared rule. A rule of your own beyond the point (Faeria: "fighters are struck back") is a
   new cause: dump and read what it does in every game before keeping it.
5. `python3 dump_lines.py /tmp/after.tsv` and `--diff /tmp/before.tsv /tmp/after.tsv`: read EVERY gone and new reason group,
   in every game, as a player. A wrong one is another family: back to 2.
6. Write the families in deck_read_<game>.md, each "## F<n> <name>" with "Root cause:", "Same error elsewhere:" (counts per
   game) and "Fix:" lines; `run.py` fails without them (review_check.py). Add a case per point; rewrite any must-not case
   cases/run.py lists as saying a reason no deck says any more (its wording changed, so it can no longer fail).
7. Report to Kaptain per family: the cause, what it did in every game, the fix, what is still open. Never per card only.
Another chat's game: the dump and the diff show what a shared fix did there; tell Kaptain and that chat, change none of
its records or cases.

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
- Fixing the lines a reviewer named, not the rule that drew them; adding an unasked rule (fighters struck back) without
  checking what it drew in every game (Faeria, 29-30 Oct: "Fixing a review").
