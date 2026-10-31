# Plan: every card connection in the database, built to answer design questions (31 Oct 2026, Claude; Kaptain asked for it)

Read first: HANDOFF.md (its boxes), PROCESS.md "Rules for links" and "Fixing a review", this file, then QUESTION_BANK.md.
This replaces DESIGN_ANSWERS.md. Kaptain approves each step's result before the next one starts. Report to him as CLAUDE.md
says: short, plain words, a card example, one question at a time.

## 1. Why we do this
Kaptain designs factions for Three Bases. He asks design questions ("how do I make a faction that lands big units early and
holds the board until then?") and wants answers from what worked in real games, at a high to mid level: the plan, its
parts, how the parts feed each other, what keeps it fair, what no game has done. Cards are only short examples.
Today the answers are bad (Kaptain: "name-dropping, a librarian's report"). The causes, all checked:
1. **The answer is tag counts.** `ask.py kit` counts each faction's cards per concept and prints the most-tagged cards. A plan
   is parts that feed each other, and nothing in the data says which parts feed which across a game.
2. **Lines exist only inside the ~210 decks we drew** (network.py computes them per deck, on the fly). Nothing is stored, so
   "what does cost cutting feed in Runeterra" or "how many cards make this combo possible" cannot be asked.
3. **Concepts have no direction.** "My cards cost more" and "the enemy's cards cost more" are one idea to a tag count; so are
   copying my unit and copying an enemy's, a cut on a 7-cost unit and on any card. The rows know side, target and cost; the
   concepts drop them.
4. **Broad concepts drown narrow ones.** protection or drawback tags hundreds of cards, selection a few dozen; counts are
   not weighted, so the narrow part of a question disappears.
5. **Examples are single cards.** A card with many tags shows nothing about how two parts work together. A pair with a
   line between them does ("Bold Bargainer makes a 9-cost creature cheaper").
6. **Many lines are wrong** (Kaptain's checks, 30-31 Oct: most Runeterra decks had wrong level-up lines). A table of wrong
   lines answers questions wrongly at scale. Accuracy comes first (section 3), then the table.

## 2. What we build (overview)
1. Every structured line between every two cards of a game that a legal deck can hold together, stored in cards.sqlite
   with the rows each end comes from (what A does, what B needs), never as text. Lines between any two cards, whatever their
   faction, when the game's deck rules allow them together.
2. Roles: each card's rows read with direction (whose, on what, where, cost band, how long), so questions can name
   "cost cuts aimed at my expensive units" exactly.
3. Mechanic links: lines grouped by (A's role, B's role): what feeds what, per game and per faction, with counts.
4. A question bank (QUESTION_BANK.md) with each question's parts written as roles, and `ask.py plan <id>` that answers it
   in a fixed shape (section 7). design_questions.py runs the bank.

## 3. Accuracy before the table (do first; the rules every line must keep)
The line rules live in network.py. Every rule below is for every game, never for a card list. Each was broken at least once;
the card in brackets is the example Kaptain found. Before the table is built, check each rule holds in the code (read the
function, then `dump_lines.py --find` the reason in every game).
- R1 **A line comes from what a card's TEXT does, never from what every card does or is.** Playing, drawing, summoning,
  attacking, discarding, having Life: every card does or has these. (Chump Whump -> Get Excited!: any card can be discarded,
  so making cards is no fuel; v65 removed it. Gabrian Enchantment -> a unit with high Life: every unit has Life.)
- R2 **The game's rules are no combo, also not for a level-up** (Kaptain 31 Oct: "we know units can attack"; Poppy, Zed,
  cases n15 and n53 flipped). A card whose own text makes it fight more (Rally, a free attack, a strike now, double strike,
  Overwhelm) keeps its line; a unit summoned attacking joins the attack under way and adds none (Zed's Living Shadow).
- R3 **A makes B, B acts on C: A gets no line to C** (Targonian Tellstones -> Blessing of Targon -> Braum; Ravenbloom
  Conservatory -> Tybaulk -> Gwen; Vikrash -> Slipstream -> Janna). A's own act of making (summon, create, plant) links to a
  C that waits for that making ("when an Ephemeral ally is summoned": Zed -> Moonlit Glenkeeper). Only a planted card that
  goes off by itself when drawn is the planter's act (Kaptain n31, n32: planting Chimes levels Bard).
- R4 **A help must do the very thing needed** (Kaptain 31 Oct). Power gets no unit past blockers (Sharpsight, For Demacia!
  -> Zed: no) and adds no level-up damage (Tybaulk -> Gwen: no). What reaches the Nexus: evasion, Overwhelm, another attack.
  Another attack: an attack token (Rally) or a free attack; never striking twice or a strike now. Health and protection do
  help "survive damage" (Blessing of Targon -> Braum: yes). network.HELPS holds these; each entry says why.
- R5 **A cap or a drawback is no need.** "The first 3 times you draw each round" (Janna) is not helped by drawing more
  (refs.py skips count conditions with op le/lt or eq 0); "lose 1 energy when drawn" wants no draws.
- R6 **A helper points at what it helps, never "needs" it** (Strength -> Attacks; Focus -> the Orbs and what repeats them).
- R7 **Read who does it.** "Level up: I've attacked with allies 3 times" is Poppy's own attacks (fixes/runeterra/v64.py
  fixed it by rule: "I've" without "seen" = the card itself). Check every count's actor against the text in every game.
- R8 **Costs as paid.** A card's cost can be variable: card.cost_x = 1 for "X" costs and for "spend all your mana"
  (Thermogenic Beam, printed 0). A count of mana spent on a kind ("6+ mana of spells", Lux) is met by a card of that kind
  costing that much or more, or with a variable cost (network.spent_lines).
- R9 **Sides.** My effects feed needs on my side; an effect on enemies feeds only needs about enemies. Enemy-only entries
  (Slay the Spire and Into the Breach monsters and bosses, events, modifiers), stubs and keywords are never line ends: a
  keyword's rows reach lines through the cards that have it (origin has_keyword).
- R10 **A card is judged with its own makings for its own acts** (Zed summons Ephemeral units), but per R3 never with what
  the made card then does.
How to check, before and after any change: `dump_lines.py` before/after, `--diff`, read EVERY gone and new reason group;
`check_all.py <game>` once; `deck_audit.py <game>`; then for the whole-game table the table check of step 5.

## 4. The table: shape, size, how to build it
### 4.1 Ids on the rows
flat_ref, flat_do, flat_if and flat_when get `id integer primary key` (refs.py, flat.py). A line end points at one row. A
row id changes on every rebuild; the table is rebuilt with the database (load.py end), so this is fine. Never store ids
outside cards.sqlite.

### 4.2 Tables (all integers; no text per line)
```
link_rule(id, name, kind)        -- one per line rule in network.py: 'event_maker', 'help_nexus', 'aim', 'tutor', 'carries',
                                 -- 'spent', 'stat_reader', 'repeat', 'level_into' ...; kind = the line kind (puts, levels, ...)
link(id, game, a, b, rule, a_row, b_row, a_concept, b_concept, via, weight)
     -- a, b: card ids; a_row: the flat_do / flat_ref row of A that does it; b_row: the flat_ref / flat_if row of B that needs
     -- it (null when the rule has no row on that end: carries, levels into); a_concept, b_concept: concept ids (vocab tree)
     -- of those rows; via: a third card when the rule names one (the planted Chime), else null; weight as network.py gives
cset(id, game, kind, with_key, n)          -- a set of cards picked by one filter ("all my units", "spells costing 6+")
cset_member(cset, card)
link_set(id, game, a, rule, a_row, a_concept, cset, weight)
     -- a broad line: A's row aims at every card of the set ("can give it +1|+0" to all units). Stored once, expanded by a
     -- join with cset_member. Lossless: every pair line the deck networks draw is a link row or a link_set member.
concept_code(id, value)                    -- concept names once; vocab ids are fine if stable
```
Text is made from (rule, a_row, b_row) by one function in network.py (`say(c, link)`), the same words the pages show today.

### 4.3 Which lines are pairs and which are sets
A rule that picks B by matching a filter over all cards (network.aimed, tutors, type asks, HELPS by concept, cost bands)
writes a link_set with the filter's cset. A rule that pairs two specific rows (A makes the event B waits for, A names B,
A carries B, B levels into C) writes link rows. If an event rule makes more than 2,000 pairs for one happening in one game,
store it as two csets (makers, takers) joined by a `link_hub(game, rule, happening, makers_cset, takers_cset)` instead, BUT
only when no pair filter applies (names_fit, doer_fits, kinds_fit, weak/lethal, terrain_fit, colour_fit); otherwise pairs.

### 4.4 Deck rules (only cards that can share a deck)
deck_analysis.DECK_RULES has Runeterra (2 regions) and Stormbound (1 faction + Neutral). Add every game from its own
sources first (cite them in library/games/<game>.md; ask Kaptain where no source says): Duelyst (1 faction + Neutral),
Faeria (colours by land, check the rule), Slay the Spire (one character + Colorless; Curses and Statuses are no build
cards), Monster Train (a primary and an allied clan + Neutral), Inscryption (any card), Into the Breach (any 3 mechs and
their weapons). A pair is stored only when some legal deck holds both. In Runeterra any two cards can share a deck (two
regions), so nothing is cut there; queries limited to one faction or one region pair filter by card.regions.

### 4.5 Size (measure first, then decide; Kaptain: lose nothing, mind the size)
Whole-game line pairs (31 Oct, v65, before the deck rule; network() joins a pair's reasons into one, so structured reasons
are more): Inscryption 3.7 k, Into the Breach 9.2 k, Stormbound 11.8 k, Monster Train 12.8 k, Slay the Spire 28 k, Faeria
39 k, Duelyst 123 k, Runeterra 946 k (233 s). Lines by kind in Runeterra: stronger 302 k, targets 164 k, waits 117 k,
keyword 100 k, type 86 k, puts 80 k; stronger, targets and keyword are mostly aims at every card of a kind (the link_set
candidates: about 60%). Duelyst: stronger 48 k, waits 18 k, targets 13 k. cards.sqlite is 19 MB.
Step 1 of the work measures, per game and per rule, how many pairs come from filters (sets) and how many are true pairs,
and the size of link + link_set + cset_member in a test file. Budget: cards.sqlite at most 60 MB; if more, use link_hub
for the biggest event rules and say so to Kaptain with the numbers. Indexes: link(game, a), link(game, b),
link(game, a_concept, b_concept), cset_member(card), link_set(game, a). VACUUM after the build.

### 4.6 How to build it (code)
1. network.py: each *_lines function today appends `(kind, weight, why)`. Change each to append a structured reason
   `(kind, weight, rule, a_row, b_row, via, cset)`; `why` is made by `say()`. Keep `network(c, game, ids)` returning the
   same lines and the same text as today for any card list: the deck pages and every case must not change.
2. A new links.py: for each game, the whole game's node list (cards with is_keyword=0, is_stub=0, categories that a build
   can hold: not game_rule, boss, monster, event, modifier, tribe), run the rules once over the whole game, write link,
   link_set, cset, cset_member. Called at the end of run.py (after refs), and by itself (`links.py <game>`) after a
   network.py change.
3. The per-deck post-filters in network() (made-card needs said once on the skill, via_made, grown forms, found-once
   draws, families, carried weapons) are deck-specific: keep them in network(); store the raw whole-game lines, and say
   in links.py which post-filters are deck-only.
4. Regression check (must pass before anything else uses the table): for every deck in decks.tsv and cases/decks.tsv, the
   lines read from the table (pairs plus set members, restricted to the deck's cards, then the deck post-filters) give
   exactly `dump_lines.py` output. A script `links_check.py` prints the differences; zero is required.

## 5. Checking the whole-game table (after each build; this is where Kaptain must not be the one who finds errors)
Per game, print and read like a player, against the card texts (a `links_audit.py <game>`, like deck_audit.py):
1. The 20 cards with the most partners (out and in). Many partners usually means a generic rule (R1, R2): name it.
2. The 20 rules x concept pairs with the most lines: read 5 random lines of each.
3. 30 random lines, and every level-up line of 10 random champions or level-up cards.
4. Cards with no partner at all: should one be linked? (a missing rule).
5. Lines between factions that no deck can hold (must be zero) and lines with an enemy-only end (must be zero).
Every wrong line: name the cause in one sentence (the thinking, not the card), find every place that thinking lives (other
rules, the readings, the questions, the docs), fix once for all games, rebuild once, diff, report to Kaptain per cause with
counts per game.

## 6. Roles: concepts with direction (needed by the questions; changes to concepts go to Kaptain first)
A role is a row's concept plus facets read from the same row. No new tags on cards: a view over flat_do / flat_ref / flat_if.
```
role(card, ability, row, concept, whose, on, zone, pick, cost_band, lasts, amount, when, cond)
  whose     mine | enemy | any            (on_side; "a creature" harming = enemy, helping = mine, as network.py does)
  on        unit | spell | card | player | position | keyword | resource
  zone      board | hand | deck | deck_top | discard | everywhere
  pick      self | chosen | all | random | it | top
  cost_band cheap | mid | expensive | any  (from a cost filter on the target, or the card's own cost; EXPENSIVE per game)
  lasts     now | this_round | permanent | while
  amount    the number, or 'variable'
  when      the trigger's concept (on_play, turn_start, on_death ...); cond: the condition's concept
```
Facets the questions need that the concepts lose today, each to be checked on 10 cards per game before use:
- cost_reduction / cost_set / free_play with cost_band of the target ("cuts aimed at expensive cards", Bold Bargainer,
  Age of Dragons) and with zone (hand, deck: "summon from the deck").
- cost_change upward on my own cards (whose=mine): a drawback. The tree's cost_increase is only "the opponent's cards cost
  more"; my own cost going up has no concept. Proposal for Kaptain: `cost_increase_self` under drawback.
- copy and steal by source side: copy of my card vs of an enemy card (on_side of the copied thing); stealing a unit, a card
  in hand or deck, a spell. Proposal: facets only, no new concepts.
- attack_now is three things: a free attack (start_attack, Rally), a strike now (strike: Single Combat), a unit summoned
  attacking. Proposal: split into `free_attack`, `strike_now`, `summon_attacking` (R2, R4 already treat them apart).
- selection with how many cards are seen ("look at the top 2": amount) and whether the rest go to the bottom or discard.
- resource_gain by lasts (now, this round, permanent, growing each turn: Deva Form) and by which resource (base or second).
- protection by reach: one unit, all my units, my player; taunt and blockers as board protection.
- high_cost: concept high_cost (top 10% of costs, flat.py) and network.EXPENSIVE (one number per game) disagree; use one
  (EXPENSIVE, set per game, Into the Breach has none) and say so to Kaptain.
- spell enhancers: a unit whose effect makes my spells stronger (spell_power) or fires when I cast a spell (on_spell).

## 7. Answers (ask.py plan <question id>)
Shape of every answer, filled from link, link_set and role; Claude writes the outline from it in plain words:
1. **The parts** of the question (QUESTION_BANK.md lists them as roles), and for each part the ways games build it, grouped
   by how they work (a steady discount that grows with the board; one big random discount; a free play from the deck), each
   way with how many cards in how many games and factions, and one example card with a 10-word text.
2. **How the parts connect**: mechanic links between the parts' roles (section 2.3): count of lines per game and per
   faction, the kind (makes cheaper, triggers, protects), one example pair with its line in words.
3. **Where it is densest**: factions where both ends of each link are common (share of the faction's cards on each end,
   weighted so a narrow role counts as much as a broad one: share divided by the role's share in the whole game).
4. **Tensions**: links that hurt (a part that is a drawback for another part: discounts per ally vs a board kept small;
   self-damage vs healing needs), from drawback roles linked to the parts.
5. **What no game does**: part combinations with zero links in every game; marked as Claude's ideas, never as facts.
6. **Feasibility**: per part, the number of cards that link to it per game (a mechanic with few partners is hard to build
   a deck around); per faction, how many of its cards take part in the plan.
Never print a card list as the answer. Never more than one example per way.

## 8. Steps, in order (each ends with a report to Kaptain and his OK)
1. Measure (4.5) and write the numbers in this file. Add the deck rules of the six games (4.4) with sources.
2. Row ids (4.1). Structured reasons in network.py (4.6.1) with `say()`; `dump_lines.py` before/after must be identical.
3. links.py and the tables (4.2, 4.3); links_check.py: zero differences on every deck (4.6.4). Size within budget.
4. links_audit.py and the table check (section 5) for all eight games; fix by cause; report.
5. Roles view (section 6); the facet checks on 10 cards per game; the concept proposals shown to Kaptain.
6. Mechanic links (section 2.3) and `ask.py plan` (section 7); design_questions.py runs QUESTION_BANK.md.
7. Answer Kaptain's five test questions (QUESTION_BANK.md K1-K5) and 10 others; read each like a designer; any answer that
   reads like a card list is a cause to fix.
8. Docs: HANDOFF.md state, README.md files and tables, PROCESS.md (the R rules above into "Rules for links"), CHANGES.md.

## 9. Do not
- Do not run run.py once per game (HANDOFF box); one `check_all.py <game>`, or `links.py` alone after a network change.
- Do not store reason text, card names or JSON per line. Do not store lines with a deck-only post-filter applied.
- Do not change concepts or vocab without Kaptain's OK; facets need no OK, but show what they do on example cards.
- Do not answer a design question with card names first; parts and links first, cards as examples.
- Do not treat a passing case count as done: done is section 8 with every step reported and approved.
