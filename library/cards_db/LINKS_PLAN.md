# Plan: store every line between cards, to answer design questions (31 Oct 2026; for the next database chat)

## Before you start
- Read START_DATABASE.md whole (its rules hold here), then this file whole, then QUESTION_BANK.md group K.
- Clone with the library (CLAUDE.md "Start of a chat", then `git sparse-checkout disable`). Work in `library/cards_db/`.
  cards.sqlite is committed and current: do not rebuild it unless a step changes records or shared code.
- Do the steps in order. After each step, report to Kaptain in a few plain lines: what was done, the numbers, one card
  example. Wait for his OK before the next step. One question at a time.
- Scripts are free to run; reading their output costs tokens: read what the step says to read, not more.

## Why
Kaptain designs factions for Three Bases and asks questions like "a faction that attacks again and again" or "units that
can't move but still control points on the map" (QUESTION_BANK.md, group K). A good answer says which mechanics feed
which, across whole games. Today network.py draws lines only for a given list of cards (the ~210 decks), and nothing is
stored, so "what feeds cost cutting in Runeterra" cannot be counted.

## What you build
1. A script `links.py` that writes `links.sqlite` (next to cards.sqlite) with every line network.py draws between two
   cards of one game that can be in one deck together. links.sqlite is not committed (it is in .gitignore): it is
   rebuilt from cards.sqlite in about 5 minutes. So the repo stays small and nothing is lost.
2. Two tables, integers only:
   ```
   phrase(id integer primary key, kind text, text text)
       -- one line reason with the two cards' names replaced by {A} and {B}: ('cheaper', 'makes it cheaper when it comes')
   link(game text, a integer, b integer, phrase integer, weight real)
       -- a, b: card ids from cards.sqlite; one row per reason of the pair
   create index la on link(game, a); create index lb on link(game, b); create index lp on link(phrase);
   ```
3. New ask.py questions that read links.sqlite (step 5).
You write no new line rules: the table stores what network.py already draws. So the table is only as right as
network.py; step 3 finds what is still wrong, and each error is fixed in network.py by cause (START_DATABASE.md).

## What network.py gives you (read this before coding)
`network.network(c, game, ids)` returns `(nodes, lines)`. `lines` is a dict `(a, b) -> [(kind, weight, why)]`. A pair's
reasons arrive already joined in one `why`: "costs 6: pays it alone (levels it up); also makes stronger: can give it
+3|+3". Split it on `"; also "`. The first part has the tuple's kind. Every later part starts with a kind word and a colon
("makes stronger: "): map it back to its kind with the inverse of `network.KIND_WORD` and cut it off. Some reasons name a
third card ("through Chime: ...", "Rocket Mech carries Storm Generator"): keep that name in the phrase. When you replace
names, replace the longer name first ("Zed (level 2)" before "Zed"). Store the pair's weight on each of its rows.

## Words used here
- **Deck rule**: which cards may be in one deck together. Duelyst: one faction plus Neutral, so a Lyonar card and a
  Songhai card are never in one deck; a line between them is useless and is not stored. Runeterra: two regions per deck,
  so any two cards can be in one deck.
- **Cards a player owns**: cards that can be in a deck or a run. Not: Slay the Spire monsters and bosses, Into the
  Breach Vek, run events and modifiers, keywords, stub names, game-rule entries. No stored line has one of these at an end.

## Step 1. Deck rules for all 8 games
`deck_analysis.DECK_RULES` has Runeterra (2 regions) and Stormbound (1 faction + Neutral). Look up the other six in each
game's own rules and cite the page in `library/games/<game>.md`: Duelyst, Faeria (how colours are limited), Slay the
Spire (one character plus Colorless cards; Curses and Statuses are not build cards), Monster Train (a primary and an
allied clan plus Neutral), Inscryption, Into the Breach. Ask Kaptain only where no source says. The factions are each
card's `card.regions` (several joined by ";"). Write `can_share(c, game, a, b)` in deck_analysis.py, with 5 pairs per
game that must share and 5 that must not, checked by a small test at the end of links.py.
Report: each game's rule in one line, with its source.

## Step 2. Build links.sqlite
links.py, for each game:
1. The cards a player owns: `select id from card where game=? and is_keyword=0 and is_stub=0 and coalesce(category,'')
   not in ('game_rule','boss','monster','event','modifier','tribe')`. Print 10 random names per game and check them.
2. `nodes, lines = network.network(c, game, ids)` once (Runeterra about 4 minutes, the others seconds).
3. For each pair: skip it if `not can_share(...)`; split its reasons (see "What network.py gives you"); write the rows.
4. Print per game: cards, pairs, rows, distinct phrases, the file size.
Measured 31 Oct before the deck rule: pairs Inscryption 3.7 k, Into the Breach 9.2 k, Stormbound 11.8 k, Monster Train
12.8 k, Slay the Spire 28 k, Faeria 39 k, Duelyst 123 k, Runeterra 946 k. Add links.py at the end of run.py.
Report: the numbers.

## Step 3. Check the table (Kaptain must not be the one who finds errors)
1. **Same as the decks.** For every deck in decks.tsv and cases/decks.tsv, compare the table's lines between the deck's
   cards with `dump_lines.py` output (pairs and phrases; not weights). Expected differences, because network() does some
   things only for a given card list: (a) a card that the list only makes (not listed) is marked "made", so a line like
   "draws it from the deck" to it is dropped in the deck; in the whole game no card is "made", so the table has it;
   (b) "draws a card of kind X" is shared among the X cards of the list, so phrases match but weights do not;
   (c) Into the Breach "carries" lines come from the deck's order (a mech, then what it carries) and are not card links:
   the table has none. Every other difference is a bug: find its cause.
2. **links_audit.py <game>** (write it like deck_audit.py, both card texts beside each line): the 20 cards with the most
   partners (many partners usually means a rule that fires for every card: START_DATABASE.md L1, L2), 5 random lines of
   each of the 20 most used phrases, 30 random lines, and 20 cards with no partner (should one have a line?). Read each
   against both texts.
3. **Zero checks** (a query each, must give 0): lines between two cards that cannot share a deck; lines with an end that
   is not a card a player owns.
4. Every wrong line: name the cause in one sentence (the thinking, not the card), fix it in network.py for every game,
   add network.tsv cases, `check_all.py --no-load`, dump and diff (START_DATABASE.md process C), rebuild links.sqlite.
Report: per cause, what was wrong, the fix, counts per game.

## Step 4. Missing concepts (show Kaptain first; change nothing before his OK)
The questions need things the concepts do not say. Propose each with 3 example cards per game that has it:
- `cost_increase_self`: my own cards cost more (a drawback; QUESTION_BANK K4). Today cost_increase means only the
  opponent's cards cost more.
- `copy_enemy`: a copy of an enemy's card or unit (K5). Today copy does not say whose.
- `steal_card`: taking a card from the enemy's hand or deck (K5). Today steal mixes units, cards and resources.
- attack_now split in three (K10): `free_attack` (Rally, "start a free attack"), `strike_now` (Single Combat: two units
  strike, no attack), `summon_attacking` (Zed's Living Shadow).
- `cost_cut_big`: a cost cut aimed at expensive cards (K1: Bold Bargainer's "costs 7 less", Age of Dragons' "cost 0").
- One "expensive" per game: network.EXPENSIVE (one number per game) and the concept high_cost (top 10% of costs)
  disagree; propose EXPENSIVE for both.
How a new concept is made: a line in library/concept_tree.txt and a shape rule in flat.py RULES (read the existing ones
first), then a rebuild (`check_all.py <any game>`), then read what it found in every game.
Report: each concept, its cards per game, what looked wrong.

## Step 5. Questions over the table
Add to ask.py (open links.sqlite with `c.execute("attach database 'links.sqlite' as L")`; ask.py already has
`under(concept, x)` for "this concept or one under it"):
- `ask.py <games> links <concept A> <concept B>`: lines from cards with A (flat_concept, under) to cards with B: per game
  the number of lines, the 5 most used phrases each with one example pair in words, and the 3 factions where both ends
  are most common. Rank factions by share of their cards with the concept divided by the game's share, so a narrow
  concept counts as much as a broad one.
- `ask.py <games> partners-count <concept>`: per game, how many cards link to cards with the concept, and the median
  number of partners of a card with it (how easy it is to build around).
- `ask.py <games> plan <question id>`: reads the question's parts from QUESTION_BANK.md and runs: each part (`compare`,
  factions), each pair of parts (`links`, both ways), cards that do two parts (`both`), and pairs of parts with no line in
  any game (new ground). Plain text, grouped by part and by pair.
Report: the output of `plan K1` and `plan K10`, cut to the first 40 lines each.

## Step 6. Answer Kaptain's test questions (QUESTION_BANK.md K1-K12)
Run `plan` for each, then write each answer in the shape of START_QUESTIONS.md "What Kaptain wants" (plan, parts and
the ways games build them, how they feed each other, tensions and counters, new ground; one example card per way).
Read each like a designer: an answer that reads like a card list, or a part that found nothing, is a fault of the
data or of the question; find the cause and fix it (steps 3-5). Show Kaptain three answers first (K1, K8, K10).

## Step 7. Docs
Update START_DATABASE.md (State, Open work, the map: links.py, links.sqlite) and START_QUESTIONS.md (the new questions;
"How to build an answer" now starts with `plan`). Remove this plan's finished steps; keep what a later chat needs.

## Do not
- Do not change line rules to make the table smaller; size is solved by keeping links.sqlite out of git.
- Do not store text per line, or lines between cards that cannot share a deck.
- Do not change concepts or vocab without Kaptain's OK.
- Do not call a step done because counts pass: done is the step's check read and reported.
