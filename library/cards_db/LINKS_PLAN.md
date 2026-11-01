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
Step 3 for Inscryption, Into the Breach, Stormbound and Monster Train. Next: step 3a below, then Slay the Spire.

## NEXT: Step 3a. Drop generic "gives X" lines (Kaptain 1 Nov 2026; do this before any more game checks)

### What Kaptain decided, and why
A line stays only when the texts of BOTH cards work together. "Guardian Stone gives Armor to friendly units" linked to all 103
units of Monster Train, and a Stormbound strength card to 215 units. Such a line only says "A helps any unit" and "B is a unit":
two counts, multiplied into thousands of rows. It makes the table huge and slow (Runeterra about 830,000 rows), and it swamps
every design question (QUESTION_BANK.md group K): the biggest faction always "links" most, and real combos drown.
"Protection buys time for big units" (K1, K6) is a pattern between mechanics; the answer says it from counts of cards per
faction, not from lines. Kaptain's earlier tests that keep generic help (nfa19 Oakling -> Grove Guardian, nfa20 Khalim's
Training -> Manta Rider, ntb7 Repulse -> Jet Mech, lk62 Shield Projector -> Combat Mech, lk83 Moment's Peace -> Mystwives)
are replaced by this decision: flip them to `none`, citing "Kaptain 1 Nov 2026".

### How lines are made today (read these before changing anything)
- `network.aimed()` (with `aimed_rows()`): an effect of card A aimed at my cards of a kind ("give a friendly unit +2|+2",
  "heal a unit", "give allies Armor"). Each card B the filter matches gets a line. Kinds: `boosts`/`stronger` ("can give it
  +2|+2"), `keyword` ("gives it Armor"), `heals` ("can heal it"), `rules` ("changes how it works: gives it Stealth"),
  `targets` ("can aim at it": can move it, can return it to hand, can copy it). `narrowed` says the filter names something
  more than a kind (a type, a keyword, a card, a cost): "your Dragons get +2" is narrowed.
  **This is where almost all generic lines come from.**
- `network.boost_lines()` with `HELPS`: help that fills a NEED written on B ("Overwhelm unit: more power reaches the
  Nexus", "needs to survive damage: more health", "level up when it kills: more power"). These are real: keep them.
- `lines_of()`: waits (A makes what B's trigger waits for: "heals it for its effect", "kills it for its death effect"),
  levels, puts (summons, creates), type (B asks for a type A is), positional lines (A moves units, B acts by place).
  Real: keep them (they were checked game by game).
- `one_link()` joins a pair's reasons; it already drops a `targets` reason when another reason joins the pair.

### The rule to build
Drop a line from `aimed()` when ALL of these hold:
1. the filter is not narrowed (it picks "a unit", "friendly units", "a card", "an ally", maybe with a place like "next to it");
2. the pair has no other reason (no waits, levels, puts, type, HELPS line, positional line);
3. B's own text does not USE what A gives (the list below).
Keep it otherwise. Do it in one place (after all reasons of a pair are known, e.g. in `network()` before `one_link`), so a
generic reason that sits beside a real one is simply not said.

### When B's text USES the help (keep these; some are not obvious)
Check that each exists as a line after the change; where one is missing, add the rule (it is real, not generic):
- B triggers on getting it: "when healed", "when given a keyword/status", "when buffed", "when targeted", Etch/Incant-like
  triggers on being picked. (waits lines; check they survive.)
- B counts it or levels from it: "I've been healed 3 times", "allies with Barrier", "units with 5+ power" where A gives exactly that.
- B's text reads the stat A raises: "deal damage equal to its power", "gain strength equal to..." (Lady Rime spends mana for
  strength; Gift of Steel -> Gabrian Enchantment: more Life becomes more Attack, test nfa35, keep).
- The help multiplies B's own text: more power to a unit that hits several times (Multistrike, Quick Attack's extra strike,
  Into the Breach multi-hit weapons), Overwhelm, Lifesteal, "deals damage to all"; health or armor to a unit that hurts
  itself (Unstable Cannon, Ramming Engines, Hydraulic Legs) or has Taunt/Challenger; a shield to a unit that freezes itself
  (Cryo-Launcher: already a rule, keep).
- Bounce or copy of my own unit with an on-play / Summon / Opening Gambit / Last Breath effect: playing it again repeats the
  effect ("can return it to hand" to Imp units with Summon is real; to a vanilla unit it is generic).
- Ready / untap / an extra action to a unit with an on-attack or activated ability.
- Removing a status from my units (cleanse, "keeps X off it") only toward cards that put that status on my own side
  (Sparkly Kitties confuses a friend, Smoke Pellets smokes allies, Cryo-Launcher freezes itself).
- Movement ("can move it") only toward a card that acts by position (those are the positional type lines; "can move it"
  alone is generic).
- A cost cut only toward cards its filter or size fits: a cut of 2+ already narrows to cards that cost that much (Bargain);
  "makes it cheaper" to every card is generic.
- Help a game's rules tie to a kind (Slay the Spire: Strength only adds to Attacks; Focus only to Orbs; L6, L13): the
  filter is the mechanism, not just a kind. Keep these and check them against test n289 and the sts1 tests.
- Positional help ("+1 to units next to it", Stormbound "units in front") is generic unless B also acts by place.
If unsure about a family, keep it, write it in "Open" with one card example, and ask Kaptain at the end.

### How to do it
1. Save the lines first: `dump_lines.py --table /tmp/tb0.tsv` (after `links.py` for all games; Runeterra about 8 minutes)
   and `dump_lines.py /tmp/d0.tsv`.
2. Change network.py once (above), rebuild all tables, dump again, `--diff` both. Read every gone reason group in every
   game: each must be generic by the rule; any group where B's text uses the help is a bug in the change.
3. Tests (only lines you are ABSOLUTELY CERTAIN about from both texts): for each family above one `line` test that must stay,
   and one `none` test of a generic line that must go, per game where the family exists. Flip the old tests listed above.
4. `check_all.py --no-load` (all games' tests), commit, push.
5. Report to Kaptain: rows before and after per game (table and decks), the families kept, one example each. Tell him the
   deck pages (network.html) lose these lines too.
Then continue step 3 with Slay the Spire.

## Step 3. Check the lines, one game at a time
Order of the games left: Slay the Spire, Faeria, Duelyst, Runeterra.

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
