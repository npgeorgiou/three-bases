# Plan: check every line between cards, then use them to answer design questions

Read START_DATABASE.md first (its rules hold here), then this file. Work in `library/cards_db/`.
After each game or step: commit, push, and tell Kaptain in a few short lines what was wrong, what was fixed, and one card example.
One question at a time.

## Why
Kaptain designs factions and asks questions like "a faction that attacks again and again". A good answer says which cards
feed which. `links.py` stores every line network.py draws between two cards that can be in one deck: `links.sqlite`
(not in git; `links.py <game>` rebuilds it in seconds, Runeterra about 9 minutes). So the lines must be right.

## Done
Step 1 (which cards can share a deck: deck_analysis.can_share) and step 2 (links.py, links.sqlite). A first step 3 pass for
Inscryption, Into the Breach, Stormbound and Monster Train. Since then the line rules changed a lot (Kaptain 1-2 Nov 2026: rules
L14-L20 in START_DATABASE.md), so every game is checked again.

## How lines are made (read before changing anything; network.py)
- `lines_of()`: what A's text makes happen that B's text waits for, counts or levels from ("kills it for its death effect",
  "damages the enemy player (levels it up)"); A makes or puts B into play; types B asks for; positional lines (A moves units,
  B acts by place); revive or summon by kind to cards with a summon effect (L17).
- `aimed()` with `aimed_rows()`: A's effect aimed at my cards of a kind. Help (stats, keywords, heal, cost) to any card of a
  kind, and every other act on a card (strike, return, copy, damage), links only where `use_of()` finds that B's own text or
  keywords use it, and the line says why (L14, L16). A keyword's effect on cards with the same keyword gives no line (L15).
- `boost_lines()` with `HELPS`: help that fills a need written on B (Overwhelm or Elusive to "hit the Nexus", health to
  "survive damage", more power to a unit whose keywords use power: `HIT_KW`; a stat B's text reads; paying for expensive cards).
- `played_lines()`, `need_lines()`: B counts or asks for cards of a kind ("6+ cost spells played", "6+ mana of spells", "if
  you have a landmark"): the cards of that kind (only a minority kind, L1b) and cards that make such a card (`made_cards()`).
- `object_help_lines()` ("when you summon an ally, grant it +1|+1") and `gives_lines()` ("your spells deal 1 more damage"):
  filtered by `use_of()` like aimed help; more damage alone is never a use (L18). `state_giver_lines()`, `actor_help_lines()`, `stat_reader_lines()`: a keyword or stat
  that B's own text names.
- `one_link()` joins a pair's reasons into one line; a bare "can aim at it" reason is never shown (L16).

## Step 3. Check the lines, one game at a time
Order: Runeterra (Kaptain knows it best), then Slay the Spire, Faeria, Duelyst, Stormbound, Monster Train, Inscryption, Into
the Breach. Fix every error by its cause, for every game, never card by card (START_DATABASE.md rule 1).

Each game gets two checks (Kaptain, 2 Nov 2026; this replaces the old parts a-i, which printed 2.5 MB for four games). A
wrong line always comes from one rule, and each rule shows as one reason ("kills it for its death effect"), so a reason is
judged once, not by many random lines. Cards are shown by their rows (one line each, SYNTAX.md), never by their text.

**Check 1, the whole game:** `links_audit.py <game>`. Its only question: is this reason's rule right?
- A reason is its sentence AND the rule that made it (Kaptain, 2 Nov 2026: one sentence can come from several rules, each
  reading other parts of the rows). links.py stores the rule as `link.site`, the network.py line that added the line
  (network.Out notes it). On 2 Nov 2026 only 6 Runeterra sentences came from 2+ rules, but inside one rule the lines come from
  cards with very different rows.
- The reasons that together hold 90% of the game's lines (Kaptain, 2 Nov 2026), biggest first: 2 lines each, 5 for the 20
  biggest, each from a different row shape (A's acts, B's events) and different cards, quickest to read first. Lines of the
  reason read before count toward that number.
- No missed-line part in the game check (Kaptain, 2 Nov 2026): cards with no partner beside random cards of their faction
  found little; decks are built for cards to work together, so missed lines are looked for in Check 2.
- A line printed or read before (cases/links_checked.tsv) is not printed again.

**Check 2, every deck:** `deck_audit.py <game>`, for ALL decks of the game (Kaptain, 2 Nov 2026). Per deck only:
- a) the deck's cards with no partner inside the deck, each beside 10 cards of the deck: first the deck's cards whose rows
  name the same thing (the same keyword, card name, type or event), then random deck cards up to 10. Is a line missed?
- b) the deck's cards with the fewest partners (at least one), all their lines: in a deck built to work together, one
  partner is suspicious. Is a line missed?
- c) the deck's special cards (champions, heroes, Generals, legends): one line per reason. Is something wrong or missing?
- No top reasons, most partners, random lines or lines per reason in the deck check: Check 1 judges every reason.
- A line or card printed in an earlier deck is not printed again.

**Before Check 2:** run `realworld.py <game>` (a script, no tokens): every combo a guide names that has no line is a missed
line found for free. Readers then look only where realworld.py has no case.

**How to work (fast, few tokens):**
1. `links.py` (all games, about 1 minute), then save the lines as they are now: `dump_lines.py --table /tmp/tb0.tsv` and
   `dump_lines.py /tmp/d0.tsv`.
2. Run both checks for one game. Check "about N tokens printed" first. Readers (Sonnet, one piece of at most 15,000 tokens each, read in one call;
   see "Token economy") read ALL the output against the rows and write each error as a cause (the wrong thinking in one sentence). Do not fix yet.
3. Claude merges the causes of all pieces, checks each against the rows (call the line functions for that pair, see
   Lessons), and fixes each cause once, for every game (network.py, or a fixes/ script for a wrong reading). A change to
   records or refs.py needs `check_all.py <game>`; a change to network.py only needs `links.py`.
4. Save the lines again and read the differences: `dump_lines.py --diff /tmp/tb0.tsv /tmp/tb1.tsv` (and the deck files).
   Every gone and new reason group, one line each.
5. `links_audit.py <game> --record` (marks what was read). Run both checks again: they now show only new lines. Repeat
   until a round finds no error.
6. `check_all.py --no-load` (about 3 minutes, all games' tests), `realworld.py`, commit, push, report.
Everything the checks print is read; if something was not read, say so plainly.

**Token economy (Kaptain, 2 Nov 2026; a chat used up his 5-hour limit on one round of reading; every chat that runs these
checks, also for a new import, keeps this):**
- A reader reads its whole piece in ONE Read call, never in small parts (Kaptain, 2 Nov 2026). Every tool call sends the
  reader's whole conversation again, so reading a piece in 9 parts paid for the start of it 9 times. A piece is at most about
  15,000 tokens (60 KB; the scripts print the size). A reader makes 4 calls: read the rules (START_DATABASE.md lines 30-108),
  read SYNTAX.md, read its piece, write its findings; no card lookups. A fresh reader per piece.
- No list holds more than 100 cards. Where a part has more, the scripts take a share from each reason (start cards: their main
  reason; partners: the reason of the line; compared cards: their faction), so every reason stays seen. Both scripts print
  "about N tokens printed" to stderr: read that number before reading the output.
- What made the cost: four games' output was 2.5 MB (about 620,000 tokens), read by 16 readers at once on the strongest
  model, each also reading the rules and looking up card texts. Most of it was part g (50 lines with both texts for each of
  20 reasons) and the champions' lines.
- Readers: one game at a time, never all games at once. Small pieces with one reader each keep a stop from losing much. It reads only START_DATABASE.md L1-L22, not other docs.
- Readers judge lines by the cards' rows, not by the card texts (Kaptain, 2 Nov 2026: a text is read differently each time;
  rows say one thing). The card reading is done (Kaptain, 2 Nov 2026): the checks print only each card's rows on one line
  (`rows.compact`), no text, and nobody compares rows with texts here. Readers read SYNTAX.md (`rows.py --syntax`) and
  START_DATABASE.md L1-L22 first.
- Readers run on Sonnet (Kaptain, 2 Nov 2026); Claude checks every cause they report against the rows before fixing.
- A reader reports causes, not single lines; once a reason group is judged, it does not look up more texts for it.
- Fixes are made in the main chat, never by an agent (Kaptain, 3 Nov 2026: a fixer agent ran 42 minutes alone, used half his
  tokens and changed nothing). Agents only read (readers, verifiers) with a fixed number of calls; never start an agent whose
  number of calls is not fixed in its job text.
- Findings of a round that stopped early are kept in `audit/` (one file per reader part) until their causes are fixed.

**Lessons (a chat lost an hour on these; do not repeat them):**
- Decide every rule from Kaptain's rules (START_DATABASE L1-L22) BEFORE changing code. Never fix, rebuild, look, fix again in
  a loop: read all the groups first, write the causes, then make all fixes in one pass and rebuild once.
- To see why one line exists, call the line functions for that one pair (a short script importing network: lines_of, aimed,
  played_lines, need_lines, boost_lines, object_help_lines, gives_lines...); it runs in under a second. Never rebuild to test one pair.
- Before running the full tests, look at the existing cases a fix touches (`grep` the card names in cases/*.tsv). A case
  written by Kaptain ("Kaptain <date>" in its source) is his decision: never flip it without his newer rule; a case written by
  Claude may be rewritten when a newer Kaptain rule says so, citing that rule.
- Shares are measured among cards of the same kind (Attacks among playable cards, not among relics and monsters), and
  makers are counted by their own text, not by the game's rules (every unit can kill in a fight).
- A filter's parts that only say where (position, "of:" what a place is measured from) narrow no card.
- Never wait on long blind runs: check one pair or one game first; the full run is the last step.

**Tests:** add a test (cases/links.tsv or cases/network.tsv) for every fixed line you are ABSOLUTELY CERTAIN about from
both card texts: one that must be gone, and one real line of the same cards that must stay. Nothing you are unsure of.
**Report:** after every fix, tell Kaptain how many lines it removed (and added) in each game, from the table diff and the
deck diff (`dump_lines.py --diff`).
**Fix every error the checks find in the same chat, for every game, before you stop** (Kaptain, 31 Oct 2026). Do not leave
found errors as notes for the next chat. If the tokens run out, stop reading new output and fix what you found first.

## Open (seen, not fixed)
- Into the Breach: pilots now have no lines. Kaptain (31 Oct 2026): a pilot is like an item a mech carries; it can move to
  any mech, and a mech can have none. So a pilot's effect on its mech can link to the weapons a mech carries (Bethany Jones'
  starting Shield keeps Cryo-Launcher's freeze off; Isaac Jones' extra Reset Turn feeds Adam). Not built yet.
- Into the Breach: Repair Field counts any heal as a repair; Gana acts once at deploy, yet weapons get lines that move units
  next to it; Targeted Strike "summons" Air Strike (a map hazard; decks only).
- Runeterra has Molten Shield twice (a plain and a "(created)" entry). Stormbound tests csb09-csb11, csb13 fail.
  Must-not tests whose reason no deck says any more: START_DATABASE.md "State"; rewrite them in that game's turn.

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
