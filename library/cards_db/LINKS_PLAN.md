# Plan: check every line between cards, then use them to answer design questions

Read START_DATABASE.md first (its rules hold here), then this file. Work in `library/cards_db/`.
After each game or step: commit, push, and tell Kaptain in a few short lines what was wrong, what was fixed, and one card example.
One question at a time.

## Why
Kaptain designs factions and asks questions like "a faction that attacks again and again". A good answer says which cards
feed which. `links.py` stores every line network.py draws between two cards that can be in one deck: `links.sqlite`
(not in git; `links.py <game>` rebuilds it in seconds, Runeterra about 9 minutes). So the lines must be right.

## Done
Step 1 (which cards can share a deck: deck_analysis.can_share) and step 2 (links.py, links.sqlite).
Step 3 for Inscryption and Into the Breach.

## Step 3. Check the lines, one game at a time
Order of the games left: Stormbound, Monster Train, Slay the Spire, Faeria, Duelyst, Runeterra.

Each game gets two checks. Both scripts print a card's text only the first time, and skip lines read before
(cases/links_checked.tsv) or already printed.

**Check 1, the whole game:** `links_audit.py <game> > /tmp/a.txt`
- a) the 30 cards with the most partners, all their lines (many partners usually means a rule that fires for every card: L1, L2)
- b) the 30 cards with the fewest partners, all their lines, beside 15 random cards of a deck: is a line missed?
- c) 5 random lines of each of the 20 most used reasons
- d) 30 random lines
- e) up to 20 cards with no partner, beside 15 random cards of a deck: is a line missed?
- f) the special cards of every deck (champions, heroes, Generals, legends): all their lines

**Check 2, every deck:** `deck_audit.py <game> > /tmp/d.txt`, for each deck of the game:
- a) the 20 cards with the most lines, all their lines
- b) the 20 cards with the fewest lines, all their lines, beside 15 random cards of the deck: is a line missed?
- c) 5 random lines of each of the deck's 20 most used reasons
- d) 30 random lines
- e) up to 20 cards with no line, beside 15 random cards of the deck: is a line missed?
- f) the deck's special cards: all their lines

**How to work (fast, few tokens):**
1. `links.py <game>`, then save the lines as they are now: `dump_lines.py --table /tmp/tb0.tsv` and `dump_lines.py /tmp/d0.tsv`.
2. Run both checks. Read ALL their output, in parts of about 150 lines, as a player, against the card texts.
   Write each error down in one sentence (the wrong thinking). Do not fix yet.
3. Fix each cause once, for every game (network.py, or a fixes/ script for a wrong reading). Add a test case for each
   (cases/links.tsv or cases/network.tsv). A change to records or refs.py needs `check_all.py <game>` (25 minutes);
   a change to network.py only needs `links.py <game>`.
4. Save the lines again (`/tmp/tb1.tsv`, `/tmp/d1.tsv`) and read the differences: `dump_lines.py --diff /tmp/tb0.tsv
   /tmp/tb1.tsv` and `--diff /tmp/d0.tsv /tmp/d1.tsv`. Every gone and new group, against the texts.
5. `links_audit.py <game> --record` (marks what was read). Run both checks again: they now show only new lines. Repeat
   until a round finds no error.
6. `check_all.py --no-load` (3 minutes, all games' tests), commit, push, report.
Everything the checks print is read; if something was not read, say so plainly.

## Open (seen, not fixed)
- Into the Breach: pilots now have no lines. Kaptain (31 Oct 2026): a pilot is like an item a mech carries; it can move to
  any mech, and a mech can have none. So a pilot's effect on its mech can link to the weapons a mech carries (Bethany Jones'
  starting Shield keeps Cryo-Launcher's freeze off; Isaac Jones' extra Reset Turn feeds Adam). Not built yet.
- Into the Breach: Repair Field counts any heal as a repair; Gana acts once at deploy, yet weapons get lines that move units
  next to it; Targeted Strike "summons" Air Strike (a map hazard; decks only).
- Runeterra has Molten Shield twice (a plain and a "(created)" entry). Stormbound tests csb09-csb11, csb13 fail.
  Runeterra n56 and Slay the Spire nst36 are must-not tests whose reason no deck says any more: rewrite them in that game's turn.

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
