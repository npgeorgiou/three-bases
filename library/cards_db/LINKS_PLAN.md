# Plan: store every line between cards, to answer design questions (31 Oct 2026; for the next database chat)

Read START_DATABASE.md first (its rules hold here), then this file, then QUESTION_BANK.md. Do the steps in order. After
each step, report to Kaptain in a few plain lines (what was done, the numbers, one example) and wait for his OK.

## Why
Kaptain designs factions and asks design questions (QUESTION_BANK.md, group K has his five test questions). Good answers
need to know which mechanics feed which, across whole games, not only inside the ~210 decks we drew. Today lines are
computed per deck and never stored, so "what feeds cost cutting in Runeterra" cannot be counted.

## What we build (keep it this simple)
1. A file `links.sqlite` next to cards.sqlite, built by a new script `links.py`. It holds every line network.py draws
   between two cards of the same game that can be in one deck together. Not committed to git (add it to .gitignore):
   it is rebuilt in a few minutes from cards.sqlite, so the repo stays small and nothing is lost.
2. Tables, integers only, no text per line:
   ```
   phrase(id, kind, text)     -- a line reason with card names replaced by {A} and {B}, e.g. "makes it cheaper when it comes"
   link(game, a, b, phrase, weight)   -- a, b: card ids; one row per reason a pair has (a pair's reasons are joined by
                                      -- "; also " in network.py: split them)
   ```
   Indexes: link(game, a), link(game, b), link(phrase). A link's words = phrase.text with the two names put back.
3. `ask.py` questions over links.sqlite (step 5), used by START_QUESTIONS.md chats.
No new line rules are written for the table: it stores what network.py already draws. So the table is only as right as
network.py: the line rules of START_DATABASE.md come first, and the checks of step 3 find what is still wrong.

## Words used here
- **Deck rule**: which cards may be in one deck together. Duelyst: one faction plus Neutral, so a Lyonar card and a
  Songhai card are never in the same deck, and a line between them is useless: do not store it. Runeterra: any two
  regions, so any two cards can share a deck.
- **Cards a player owns**: cards that can be in a deck or a run. Not: Slay the Spire monsters and bosses, Into the Breach
  Vek, run events and modifiers, keywords, stub names, game-rule entries. No line may have one of these at either end.

## Steps
### Step 1. Deck rules for all 8 games
`deck_analysis.DECK_RULES` has Runeterra (2 regions) and Stormbound (1 faction + Neutral). Add the other six from each
game's own rules (look them up, cite the page in `library/games/<game>.md`; ask Kaptain where no source says):
Duelyst, Faeria (check how colours are limited), Slay the Spire (one character + Colorless; Curses and Statuses are not
build cards), Monster Train (a primary clan and an allied clan + Neutral), Inscryption and Into the Breach (check). Write a
function `can_share(c, game, a, b)` in deck_analysis.py from card.regions and DECK_RULES, with 5 test pairs per game in a
small test at the end of links.py (a pair that must share, a pair that must not). Report the rules to Kaptain.

### Step 2. Build links.sqlite
links.py, per game:
1. The cards a player owns (see "Words used here"): `select id from card where game=? and is_keyword=0 and is_stub=0 and
   coalesce(category,'') not in ('game_rule','boss','monster','event','modifier','tribe')`. Check the list per game by
   eye (10 random names) before going on.
2. `network.network(c, game, ids)` once for the whole game (Runeterra takes about 4 minutes, the rest seconds).
3. For each pair (a, b) and each reason: drop the pair if `can_share` says no; make the phrase (replace both cards'
   names by {A} and {B}); write the row.
4. Print per game: cards, pairs, rows, distinct phrases, file size. Measured 31 Oct (before the deck rule): Inscryption
   3.7 k pairs, Into the Breach 9.2 k, Stormbound 11.8 k, Monster Train 12.8 k, Slay the Spire 28 k, Faeria 39 k,
   Duelyst 123 k, Runeterra 946 k.
Call links.py at the end of run.py (after the cases), and by itself after a change to network.py.

### Step 3. Check the table (Kaptain must not be the one who finds errors)
1. **Same as the decks.** For every deck in decks.tsv and cases/decks.tsv: the table's lines between the deck's cards
   against `dump_lines.py` output (pairs and phrases; weights differ and are not compared). Some differences are expected,
   because network() does a few things only for a deck (a card the deck only makes cannot be drawn from the deck; a
   card found by a "draw a X" counts once per deck; a champion's forms are one card). List every difference; each one
   must be one of those; any other difference is a bug: find its cause.
2. **links_audit.py <game>**, read like deck_audit.py: the 20 cards with the most partners (many partners usually means
   a rule that fires for every card, L1-L2), 5 random lines of each of the 20 most used phrases, 30 random lines, and the
   cards with no partner (should one have a line?). Check each against both card texts.
3. **Zero checks**: no line between two cards that cannot share a deck; no line with an end that is not a card a player
   owns.
4. Every wrong line: name the cause (the thinking, not the card), fix it in network.py for every game, add network.tsv
   cases, rebuild, dump and diff (START_DATABASE.md rules 1-3). Report per cause with counts per game.

### Step 4. Concepts that the questions need (show Kaptain first; change nothing before his OK)
The questions need a few things the concepts do not say. Propose each with 3 example cards per game:
- `cost_increase_self`: my own cards cost more (a drawback). Today cost_increase means only the opponent's cards.
- `copy_enemy`: a copy of an enemy's card or unit (today copy does not say whose).
- `steal_card`: taking a card from the enemy's hand or deck (today steal mixes units, cards and resources).
- attack_now split into `free_attack` (Rally, "start a free attack"), `strike_now` (Single Combat), `summon_attacking`.
- `cost_cut_big`: a cost cut aimed at expensive cards (a cut of 2+ or one naming cost 6+: Bold Bargainer, Age of Dragons).
- Use one "expensive" per game: network.EXPENSIVE (one number per game) and the concept high_cost (top 10% of costs)
  disagree; propose EXPENSIVE for both.
Each new concept is a shape rule in flat.py RULES (like the existing derived concepts), run on every game, and read.

### Step 5. Questions over the table
New ask.py questions (all read links.sqlite and cards.sqlite):
- `ask.py <games> links <concept A> <concept B>`: lines from cards with A to cards with B: per game the count, the 5 most
  common phrases each with one example pair, and the factions where both ends are common.
- `ask.py <games> partners-count <concept>`: per game, how many cards link to cards with the concept (how easy it is
  to build around it), and the median partners per card.
- `ask.py <games> plan <question id>`: runs the parts of a QUESTION_BANK.md question: each part (compare), each pair of
  parts (links), cards that do both (both), and pairs of parts with no line in any game (new ground).
Weight narrow concepts fairly: when ranking factions, divide a faction's share of a concept by the game's share.

### Step 6. Answer Kaptain's five test questions (QUESTION_BANK.md K1-K5)
With `ask.py ... plan`, write each answer in the shape of START_QUESTIONS.md ("What Kaptain wants"). Read each like a
designer: an answer that reads like a card list is a fault of the questions; find why and fix it. Show Kaptain.

### Step 7. Docs
Update START_DATABASE.md (State, Open work, map) and START_QUESTIONS.md (the new questions, the build-an-answer steps).

## Do not
- Do not change line rules to make the table smaller; size is solved by keeping links.sqlite out of git.
- Do not store text per line, or lines between cards that cannot share a deck.
- Do not change concepts or vocab without Kaptain's OK.
- Do not call a step done because counts pass: done is the step's check read and reported.
