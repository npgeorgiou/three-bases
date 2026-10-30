# Process: describing a game's cards (the framework for every game)

For the chat that imports a game. Runeterra, Stormbound and Monster Train went through every step; their files are the
templates. Commands run from `library/cards_db/`. Files and tables: README.md.

The database is one place for all games: questions run across games (`ask.py all ...`), so everything stored must be
generic. A game's own words live only in the card texts, its keyword entries and its types; what cards DO is said with
vocab.tsv values and concepts that any game can share.

## Think in families, every time (Kaptain, 30 Oct 2026: the lesson every import repeated)
Kaptain checks one deck and finds errors in every round, because each fix covered only the cards he named. Before you say
"done" or "no other card has this", do all of these:
1. **Name the cause, not the card.** One sentence: what thinking or what reading made it wrong ("Start a free attack with 2
   Dragonlings" read as using Dragonlings in play). Then ask: where else does the same thinking live? The same meaning in
   other words ("Nagakabouros starts a free attack with 4 Tentacles", "an exact copy of each Cat attacks"), other games,
   other scripts (lines, deck plans, combos, questions).
2. **Search by meaning, not by wording.** A regex over one sentence finds one card. Search the rows for the shape of the
   error (`audit_links.py` 9: a card acting on N cards it names but never makes) and read every hit against its text.
3. **Data or script?** Read the card's text and its rows (`ask.py <game> card <name>`). Rows that disagree with the text:
   the data is wrong, fix it by a text rule (fixes/<game>/vNN.py). Rows right but the line wrong: a script rule is wrong,
   fix it for every game. Say which one it was.
4. **Check who, what and what it makes.** Who must do it (Zed's own strikes, Ephemeral attackers), what the effect lands on
   ("it" after "revive me" is the card itself), what a card makes (Zed's Living Shadow, The Iron Conquest's skill), and
   abilities a card gives itself (Shark Chariot's Last Breath).
5. **Dump every line before and after** (`dump_lines.py`) and read every gone and new reason: a fix that removes good lines
   is a new error (a too wide rule broke Surgeforger's "give them both").
6. **Use every check you have**: `audit_links.py` (10: what the earlier library's tags say a card does that its rows lack:
   leads to read, not truth), `realworld.py` (what players and guides say about each game), `design_questions.py` (the
   answers to the questions Kaptain will ask, read like a designer). A thin or odd answer is an error to trace.
7. **Report** each family: the cause, data or script, the fix, how many cards in which games, and what was not checked.

**Two files.** This file: how to work, the steps, how to fix a review, how to check networks. PROCESS_LESSONS.md: what each
import and each review by Kaptain taught (one section per game or review; every rule in it holds for every game). Read both
before importing a game.

## Why the first three games went wrong (read before importing a game; 29 Oct 2026)
Kaptain checked a few decks four times and each time found missing and wrong links. The causes, and what now stops them:
1. **The rows held only what card texts say, not the game's rules.** No Runeterra text says "a unit that attacks unblocked
   hits the enemy Nexus", so no unit helped Gangplank, Darius or Gnar level up. Now each game has
   `read/<game>/game_rules.jsonl` (step 0.10): what every unit does by the rules, written once from
   `library/games/<game>.md`; refs.py gives those rows to every card of the category (origin game).
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
   there gets a mechanics.tsv case with game `*`, and every game's cases must pass before it is pushed: run
   `check_all.py <your game>` (ONE reload of every game, then every other game's cases; HANDOFF box). Never run
   `run.py` for a game another chat is importing: it normalizes and rewrites that chat's records, flags and reports.

## Rules that are never broken
- **A card is everything it makes** (summons, creates, shuffles in, transforms into, levels into), and a wrong judgment is
  wrong thinking: fix the thinking in every place it lives (HANDOFF box), never only the example.
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
   library; (b) the concept's definition, including its "not this" part (library/concept_tree.txt); (c) whose
   side it hits (an enemy that can't block is cant_block, my own unit that can't block is a drawback); (d) whether the
   keyword belongs to the game at all (Terrify is Path of Champions: deleted). When a shared keyword name means something
   else in this game, the row is `<game>:<Name>` (monster_train:Frostbite is damage over time, Runeterra's Frostbite is
   attack_zero). Show Kaptain the full keyword -> concept list with each concept's definition.
   How to map a keyword to a concept: read the concept's definition and its "not this" part, then use an existing concept
   only when the definition says exactly that mechanic. A loose fit is wrong (Claude's first list had Enlightened ->
   high_cost, Deep -> self_mill, Plunder -> on_life_loss: Enlightened is a max-mana condition, Deep a deck-size condition,
   Plunder "the enemy Nexus was damaged this round"). When none fits, add a precise concept to concept_tree.txt with
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
supplement_<game>.py). The shared files need care:
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
1. **Research the game** (the game's wiki rules and full glossary, every faction page, two or more strategy guides; note each mechanic with its page): rules, the full keyword glossary, factions or tribes,
   board, turn structure. Also search now for players' guides with real decks (Steam guides and discussions, build
   guides, tier lists with card lists): they become the deck tests (step 3). Note each source's URL and check it is about
   this game (Monster Train 1 and 2 guides look alike; a page with card names the game does not have is not a source).
2. **Left out** (`exclude.tsv`): only other modes or products, and only what Kaptain names. Tokens are never left out:
   links to them are how combos are found.
3. **The game's data is already in the repo. Look there before fetching anything.** Kaptain does not know where each file
   is; this list does:
   - `library/sources/conv_<game>.py`: its first lines name the source, date and format of the game's card data. Raw
     files next to them: `monster_train_cards.psv` (282 Monster Train cards, wiki Module:Cards/Data),
     `inscryption_missing_cards.json` (partial: only the cards the library missed; the whole set is
     `inscryption_wiki_cards.jsonl` + `inscryption_wiki_cards_more.jsonl`, wiki pages with their revisions, 29 Oct 2026), `faeria_merlin_shortened.csv` + `faeria_cards_english.csv` (462 Faeria cards,
     Abrakam's github.com/abrakam/Faeria_Cards 12b7207; its README defines the keywords). Named sources: Lorcana (npm lorcana-oracle), Star Wars: Unlimited (swucardex-data
     a86faed), Elder Scrolls: Legends (TESLegendsTracker c541e82), Slay the Spire (wiki Module:Cards/data), Slay the Spire 2
     (Kaptain's lists, 12 Oct 2026), Gwent (gwent.one v14.8), Magic (MTGJSON AtomicCards, Scryfall tokens), Shadowverse
     (Portal API), 40k and Age of Sigmar (BSData). Duelyst: `library/sources/duelyst_cards.psv` (1116 cards, conv_duelyst.py over
     github.com/open-duelyst/duelyst 2843f24; the repo's tutorial and tips are the rules source).
   - `library/games/<game>.md`: research, sources, and the keyword terms with the page each comes from. Check each
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
   written with their sources into `library/games/<game>.md` ("The game's rules (from sources)" or sourced terms; never
   the "Claude's summary" lines, which came from memory: audit_links check 8),
   write what every unit (or card of a category) does that no card text says, as one record: name "Game rule: ...",
   `applies_to` (categories), `source` (the line it comes from), abilities on event always with pick self. The three games
   write how units fight: Runeterra `start_attack` self, `strike` self to an enemy unit, or (link or) to the enemy player;
   Stormbound strike to an enemy unit or structure, or the enemy base; Monster Train strike to an enemy unit. Not written:
   what every unit does all the time and says nothing about which cards belong together (Stormbound units moving forward).
   refs.py copies the rows to every card of the category as origin game, except units that can never attack (Immobile);
   the network weights them less than a card that says it; card queries (ask.py, mechanics.py, connections.py) leave them out.

11. **What a deck is in this game** (Into the Breach, 30 Oct 2026: a squad was first written as 3 mechs, and Kaptain found
   "no weapons in your networks"). Before writing decks.tsv, write into `library/games/<game>.md` what the player
   really brings to a battle and its limits: which cards ride on which (a mech carries 2 slots: its starting weapon and its
   passive or one extra weapon, never two extra), slot and class rules, copies allowed. Each deck lists every card the player
   brings, in an order that says what rides on what (each mech, then what it carries); check every deck against the limits
   with a short script before building networks.
12. **Every rule of the game becomes a record or a line rule.** Read the rules notes line by line and ask for each: which
   cards does it link? Into the Breach's "a ground unit pushed into a Chasm is destroyed", "most Vek drown in Water", "Frozen
   ends when hit", "bumps deal 1 damage" sat in the notes and drew no line until Kaptain pointed at Flood Drill. Write such a
   rule as a record (game_rules.jsonl) or, when it links two kinds of card (makers of holes -> pushers), as a sourced rule in
   network.py (DEADLY_GROUND), and give it a case.

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
   **find at least 20 decks for the game (Kaptain, 30 Oct 2026), with a good spread over its factions and its mechanics**
   (count the factions the decks cover, and add decks for the factions and kinds of play that have few or none; Duelyst:
   every General's faction, Runeterra: every region; a list Kaptain gives is used whole, and a name cut short by a page is
   matched to the real card, never dropped). Find full decks first (players' guides, deck sites, deck codes; full lists,
   not a guide's core cards; a roguelike's guide builds are core cards: the source column says so). The source column
   starts with the URL (the page links its first word). A full deck has
   every copy: the counts add up to the deck size the game sets (Inscryption Act II battle decks: 20), and the source
   column says the counts and the size; decks.tsv lists each card once. A roguelike's starter deck (Inscryption Act I,
   Kaycee's Mod: 4 cards and a side deck) is where a run starts: keep it, marked as a starter, but it does not count
   toward the 10 full decks; when fewer than 10 full decks exist as text, say so in RESULTS.md. Read at least 10
   decks card by card, as a player: for each card, what does it need (level-up, trigger, condition, stats, keywords) and
   which cards in the deck give it that; what does it give, and to whom; is every line's reason true by the texts? Kaptain
   found 15 gaps in 9 decks that 500 passing cases had not shown, and Claude's own read of 9 decks found 8 more families.
   Each gap is fixed for every card of every game (a rule, never one card), becomes a cases/network.tsv row, and its
   lesson is written in "Links the deck networks showed missing".
   **Then the deck check (Kaptain, 30 Oct 2026; part of every import, and of every later network change):**
   `deck_audit.py <game>` and read all of it, as "Audit every deck yourself" says: per deck the 3 most linked and the 3 least
   linked cards with every line and the cards they link to, 10 other cards at random (should one of them be linked with a
   least linked card?), and 10 other random lines, each checked yourself against both
   card texts. Every mistake found is fixed generally: by its cause, in the shared rule, for every game, and before fixing,
   ask what else the same cause breaks outside the decks (the decks show only a tiny part of each game). Dump before and
   after, read the diff, add a case. A game is not done before its deck check is written in deck_read_<game>.md.

### 3. Case tests (`cases/`)
- mechanics.tsv: a question, the expected cards from the texts (regex on the text, or a Keywords-field keyword) and the
  query. Passes at 95%. Every trigger word, every keyword, every common verb. Shared changes: rows with game `*`.
- decks.tsv: **real decks from players' guides are the benchmark.** Each row: the guide's cards and the phrases
  `ask.py <game> analyze` must say so the deck is explained the way the guide explains it. Run them early: in Monster
  Train they showed the explainer missing keyword stacks, types, spell triggers and Morsels being eaten, all fixed in
  shared code for every game. A guide deck the explainer cannot explain is a gap to fix, not a case to drop.
- combos.tsv: pairs a guide names, plus the library's combos rows; the source column says which guide.
- network.tsv: lines of a guide deck's network that must be there, or must not (Kaptain's checks of the networks; a
  wrong line is a "none" row, with why_not when only one reason is wrong; a "line" row with text in that column needs a
  line whose "kind: reason" holds it, e.g. "cheaper:" or "kills it for its death effect"). Every point Kaptain confirms
  becomes a row that checks the kind too, not only that some line exists.
- regions.tsv: the library's signature, splash and archetype rows per faction.
- A failing case is fixed at its cause: the query (check it against the texts first), the pattern, the value, the shared
  code or the records. A case built on wrong old tags is dropped with its reason in DROPPED.md.
- Guide decks go to readers? No: readers describe only what a text says, and a deck would invite links the text does not
  state. Decks test the result.

### 4. Kaptain's check
Claude checks 20 random cards against their texts and the sources of step 0.10 (`ask.py <game> card <name>` shows text and
rows), writes every error family into deck_read_<game>.md ("Check of 20 cards"), fixes each family once, and adds a case
per family. No check files are written for Kaptain. Kaptain checks the deck networks page (network_page.py) in plain words:
does a line between two cards make sense to a player. Every point he finds is fixed as "Fixing a review" says.

### 5. Done when
`run.py <game>` passes every step and every other game still passes; read/<game>/game_rules.jsonl written (step 0.10);
audit_text.py and audit_links.py print nothing unexplained; the keyword -> concept list checked twice and shown
to Kaptain; word check 0 open flags; no proposal need shared by cards with different texts; stubs only names nothing
defines; `ask.py all compare <its main concepts>` shows its cards next to the other games'; every guide deck explained;
Claude's check of 20 cards in deck_read_<game>.md; at least 20 decks found with a spread over factions and mechanics, at least 10 full decks' networks read card by card and the deck check done (step 2.9)
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
Working smarter on a review (lessons, 30 Oct 2026):
- A line's label must say why both cards belong together, with both names where "it" is unclear: "Combat Mech moves units,
  and Artillery Mech acts on units in a line from it", not "makes units move" (Kaptain, 30 Oct 2026). Use {A} and {B} in a
  reason; network() fills in the names (moves_said, doer_help_lines). Check help_kind() when a reason's first words change.
- After the counted fix, read EVERY line of the game's decks once more as a player before reporting: three more errors of
  the same family were found that way (a card moving only itself, a swap, a card that aims at any space).
- Finishing a network task always ends with `network_page.py`, a Playwright load of every deck (no script errors, one
  hover), push, and network.html given to Kaptain.
- A must-not case whose reason the fix removed from the whole game is flagged as stale: test it on a card-list deck with
  no other line ("Swap Mech, Flame Shielding", expect none), or keep the reason said by a positive case (ntb6 keeps ntb4).
- A keyword can have two vocab entries (another game's "Boost" and "into_the_breach:Boost"): the game's own entry wins
  (network.kw_tree); a lookup with fetchone() and no order picks either.
- Another chat pushed meanwhile: rebase, take the upstream cards.sqlite, network.html and QUERIES.md, keep both sides of
  code, rebuild with run.py, run cases/run.py for every game, compare your game's lines with your last dump.
- Answer Kaptain's questions first and wait; then do all points in one pass: dump, causes, one fix per cause, one rebuild,
  one diff read, one report. No rebuild per point.
- Trace a wrong line to its rows before guessing: `flat_ref` (needs and makes) and `flat_do` (acts, filters) of both cards
  show which rule fired. Most wrong lines were one rule firing for every card (game rules, a dropped filter, either side).
- A line is right when a player would say "A does this for B"; "every unit can do it" is no reason for a line, unless
  Kaptain asked for it (Runeterra units hitting the Nexus for champions).
- Say every rule with a number in it (top tenth of costs, a third of the cost) and the cases it was checked on; a
  threshold tuned to make one case pass is a new error.
- Changing reason wording can make must-not cases pass whatever the network says: run cases/run.py and rewrite the cases
  it lists.
- Check a page change in the browser (Playwright: load every deck, no script errors; hover and click on a line).
- Kaptain asked about a line he could not see: check the page data and a screenshot first, then answer in plain words
  about what is drawn, not about weights.
- Report per cause with counts per game, and say honestly what was only fixed for the named cards.

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

**Audit every deck yourself (Kaptain, 30 Oct 2026; every worker, every game, after building or changing the networks, before
showing Kaptain anything):** run `python3 deck_audit.py <game> > audit.txt`. For EACH deck it prints (1) the 3 most linked
cards with every line and the other card's text, (2) the 3 least linked cards the same way, plus 10 other cards of the deck at random with their texts (should one of
them be linked with a least linked card?), (3) 10 other lines at random,
with both texts. Read every printed line against both card texts as a player: is the line true, is its kind right (triggers,
enables, makes stronger, makes cheaper ...), is its wording right, and what does a least-linked card obviously need or give
that no line shows? Every error found is fixed the way "Fixing a review" says: by its cause, in the shared rule, for every
game, never for the one card; and before fixing, ask what else the same cause breaks OUTSIDE the decks (the decks show a
tiny part of each game: the cause is wrong for every card it touches). Dump before and after, read the diff, add a case.
Then audit again. Write the families found in deck_read_<game>.md.

**Rules for links (Kaptain, 30 Oct 2026; each is a rule in network.py for every game, never a list of cards):**
- **Links come from what a card's TEXT does, never from what every card does.** Playing, drawing or summoning a card is
  what all cards do: "whenever you play a card" (After Image) gets no link from every card. Only a narrowed kind counts
  ("whenever you play a Skill"), and a kind that every playable card of the game is counts as not narrowed (Slay the Spire:
  every card is a spell). The same for help: "play the first card each turn twice" (Echo Form) links to no card.
- **The game's normal attack feeds nothing.** A card whose only effect is plain damage to one target (Strike, Mystic Shot)
  is no link to "when an enemy dies" (Corpse Explosion). Only cards with something special that makes or helps the kill:
  poison and damage over time, hits on all enemies, kill effects, damage boosts (Strength, Vulnerable).
- **A helper points at what it helps; it never "needs" it.** Strength, Dexterity, Focus, Vulnerable, Wrath givers -> the
  cards whose damage or Block they make bigger; "your next Skill is played twice" (Burst) -> the Skills; "Block is not
  removed" (Barricade) -> the Block cards. The cards helped are never drawn as enabling the helper.
- **A cost that drops for each X: what does X makes it cheaper** (Gambling Chip discards -> Eviscerate, events ->
  Windstorm Colossus): kind "makes cheaper", never "enables".
- **Kinds (Kaptain, 30 Oct):** a reaction ("whenever", "every 3rd Attack") is "triggers"; a count or a thing that must be
  there ("for each Attack played", "if you have Block") is "enables"; help says how (stronger, cheaper ...). One reason is
  said once per line, by its strongest kind.
- **Say who gets it.** In a game where the player is no card, a status on the player is "gives you Strength", never
  "makes your units get Strength".
- **What is expensive is set per game** (network.py EXPENSIVE: the cost from which a card counts as expensive). Every game's
  import sets it, from that game's own costs; a game missing there gets no "pays for it" lines.
- **A deck holds what the game gives every deck of its character** (Slay the Spire's starting relic: Burning Blood),
  unless a card of the deck replaces it ("Replaces Burning Blood": Black Blood). deck_analysis.starters, rarity starter.
- **Read the game's own limits on a mechanic** (wiki): Dexterity adds only to Block a card gives when played, not to a
  Power's later Block or Entrench's doubling; Lock-On only to Orb damage.
- **Drawbacks and limits are no needs.** "Lose 1 energy when drawn" (Void) wants no draws; "if you played fewer than 3
  cards" (FTL) wants no plays; "if this is still in your hand" (Ethereal) wants no full hand.

## Mistakes made before (do not repeat)
- **Read what a card makes before judging a line (Kaptain, 30 Oct 2026).** Claude called "Zed -> Moonlit Glenkeeper" wrong
  because Zed is not Ephemeral; Zed summons Living Shadows, which are, so the link is true through them. The real error was
  the other line, "Glenkeeper gives Zed +1|+0 when he comes" (fixed: a state that is a keyword, "an Ephemeral ally", is had on
  arrival only by cards that print it). Before calling a line wrong or missing, read the texts of every card both cards make
  (deck_audit prints them under "makes"), the keywords those cards have, and what the game's rules add.
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
