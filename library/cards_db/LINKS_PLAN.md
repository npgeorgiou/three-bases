# Plan: check every line between cards, then use them to answer design questions

Read START_DATABASE.md first (its rules hold here), then this file. Work in `library/cards_db/`.
After each game or step: commit, push, and tell Kaptain in a few short lines what was wrong, what was fixed, and one card example.
One question at a time.

## Why
Kaptain designs factions and asks questions like "a faction that attacks again and again". A good answer says which cards
feed which. `links.py` stores every line network.py draws between two cards that can be in one deck: `links.sqlite`
(not in git; `links.py <game>` rebuilds it in seconds, Runeterra about 9 minutes). So the lines must be right.

## Done
Step 1 (which cards can share a deck: deck_analysis.can_share), step 2 (links.py, links.sqlite) and step 3 for all 8 games
(finished 3 Nov 2026; the causes left unfixed then are listed under "Open"). From now on step 3 runs only for a newly
imported game.

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

## Step 3. The line check after importing a game
Done once for the new game, right after its import (PROCESS.md 4b). Fix every error by its cause, for every game, never
card by card (START_DATABASE.md rule 1). Cards are shown by their rows (SYNTAX.md), never by their text.

**Steps, in order:**
1. `links.py` (all games, about 2 minutes), then save the table: `dump_lines.py --table /tmp/tb0.tsv`.
2. `realworld.py <game>`: every combo a guide names that has no line is a missed line found for free.
3. Print the two checks: `links_audit.py <game>` (each reason of the game: is its rule right?) and `deck_audit.py <game>`
   (every deck: cards with no or few partners, the special cards). Both print "about N tokens" to stderr; cut the output
   into pieces of at most 15,000 tokens.
4. Readers: one agent per piece, job text `checks/READER_JOB.md` + the piece path. They write causes in the causes.py format.
5. `causes.py <reader files> --out /tmp/pieces.md`: adds to every cause the line as it is now, the network.py line that made
   it, the cases with both cards (CONFLICT = a case says the opposite) and both cards' rows. Cut it into pieces.
6. Verifiers: one agent per piece, job text `checks/VERIFIER_JOB.md`. They write verdict files.
7. `causes.py <verdict files>` writes `causes_sheet.md`, biggest first: each cause with all a fixer needs, and how many lines
   of the table come from the same reason and network.py line. Fix from the top; skip CONFLICT causes (Kaptain's case wins)
   and GONE ones. No other lookups are needed; `pair.py <game> "A" "B"` only to check a fix.
8. Per fix: one `none` and one `line` case in cases/network.tsv. After about 5 fixes: `check_all.py --no-load`.
9. At the end: `links.py`, `dump_lines.py --table /tmp/tb1.tsv`, `dump_lines.py --diff /tmp/tb0.tsv /tmp/tb1.tsv`,
   `realworld.py`, `check_all.py --no-load` (it lists must-not cases whose reason no deck says any more: rewrite them),
   commit, push, report to Kaptain the lines gone and added per game.

**Rules for the check (Kaptain, 2-3 Nov 2026):**
- Agents only read (readers, verifiers), on Sonnet, with the fixed number of calls their job text gives; each reads its whole
  piece in one call. Fixes are made in the main chat, never by an agent.
- A reader reports causes, not single lines, and judges by the rows, never by card texts.
- A case written by Kaptain ("Kaptain <date>" in its source) is his decision: never flip it without his newer rule.
- A fix that narrows a rule keeps its exceptions for level-ups and Kaptain's cases.
- Wording causes ("one fact said twice") are fixed once in one_link(), never per pair.
- Fix every error the check finds in the same chat; if tokens run out, stop reading new output and fix what was found.

## Open (seen, not fixed)
- Into the Breach: pilots now have no lines. Kaptain (31 Oct 2026): a pilot is like an item a mech carries; it can move to
  any mech, and a mech can have none. So a pilot's effect on its mech can link to the weapons a mech carries (Bethany Jones'
  starting Shield keeps Cryo-Launcher's freeze off; Isaac Jones' extra Reset Turn feeds Adam). Not built yet.
- Into the Breach: Repair Field counts any heal as a repair; Gana acts once at deploy, yet weapons get lines that move units
  next to it; Targeted Strike "summons" Air Strike (a map hazard; decks only).
- Runeterra has Molten Shield twice (a plain and a "(created)" entry).
- The causes the 8-game check left open: `checks/open_causes.md`.

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
