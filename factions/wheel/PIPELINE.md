# The wheel pipeline, steps 1-9: the commands and what each step makes
Commands run from `library/cards_db/` unless they start with `factions/`. The rules of each step are in
`factions/START_DESIGN-1-wheel.md`; this file says how each result is made.
Before anything: `python3 links.py` (about 4 minutes; makes links.sqlite, not in git; every number below needs it;
tell Kaptain and wait for his OK). A step is redone only when what it uses changes, and then only for the parts that
changed. Each step says what a script does and what is judgment.

## Step 1. The radii (made 9-10 Nov 2026, before the wheel chats)
- What: 24 radii (`SPOKES` in axes.py: key, name, the library concepts that count a card for it). A faction's value
  on a radius = its share of such cards / its game's average share (1 = average). 43 real factions of 8 games.
- Script: `python3 axes.py` -> `axes.tsv`, `factions/wheel-axes.html`. How the values are made: `factions/13`.
- Judgment: which concepts belong to each radius (checked by agents reading cards, `axes.py --cards <file>`).

## Step 2. The radii that work together (second try, 14 Nov 2026)
- Numbers: `python3 mechanics_wheel.py links --radii` -> `wheel/radius_links.tsv`. Per pair of radii: `cards` = how
  much more often than chance the library links a card of one with a card of the other (same game); `decks` = how much
  more decks heavy in one hold the other. 1 = chance. `links` = the linked card pairs made by the two; `level` = that
  count growing slowly (0, 1 link = 1, 10 = 2, 100+ = 3). "Rewards playing spells" is judged by `decks` only.
- Radii joined = `cards` 1.2 or more, or `decks` 1.5 or more. Mechanics joined (steps 5-6) = `level` 1 or more (the library
  links them at all), or `decks` 1.5 or more.
- A link counts for a radius only when the effect that made it, on that card's side, belongs to the radius (the links'
  `a_ab`/`b_ab` columns), for chance too (the share of a radius' cards' links its own effects make). Numbers only: nobody reads card pairs.

## Step 3. The 20 factions as shapes (second try)
- What: each faction = 3-6 radii with uneven values, like real factions. Each radius joined to at least one other of
  the same faction by a strong number (step 2), or by an argument from this game's rules
  (`factions/wheel/arguments.tsv`: L, M, Q, T).
- How: chosen by hand (Claude), no script. Each shape checked against the real factions:
  `python3 axes.py --near "wide=1.4,spends=1.9,back=1.6"` (closest real faction 0.24-0.81 away).
- Output: `factions/wheel/work/shapes.tsv` (letter A-T, radius=value list). Why each shape was chosen is not saved.
- Checked by: `python3 tools/wheel_table_check.py` (from the repo root; 3-6 radii, each joined, no two shapes the same).

## Step 4. The mechanics list (second try; checked again 15 Nov 2026)
- Start: the first try's 44 mechanics, plus offering, roundstart, leave, hide,
  bigstrength: 48 mechanics, one line each, never two merged (Kaptain).
- File: `factions/wheel/mechanics.tsv`, columns: key; sentence "I do X -> I gain from X"; concepts (the library
  concepts that count a card as this mechanic; `concept@game,game` counts only in those games); NEW RULE mark;
  "made by" concepts (cards that make it happen, counted with it); size (SMALL = under 30 right cards in every real
  faction).
- Reading: `python3 mechanics_wheel.py cards <file>` writes 8 cards per mechanic, taken from cards.sqlite: game,
  the card's concepts, name, the first 220 letters of its text. Agents read the texts and said how many of the 8 are
  really this mechanic, and which concepts to add, drop or limit to some games.
  Output: `factions/wheel/work/concept_fixes_round1.tsv` (47 mechanics), `round2.tsv` (33 again after the change).
- What changed: only the concepts column of mechanics.tsv. The card database (cards.sqlite) was not changed.
- Then: `python3 mechanics_wheel.py measure` -> `wheel/measured.tsv` (per mechanic: cards, games with 10+, the biggest
  real faction's count, the real factions with the highest share, the radii it serves) and
  `python3 mechanics_wheel.py links` -> `wheel/links.tsv` (per pair of mechanics, the same numbers as step 2).
- Not saved: the agents' prompt of this step.

- Rule and archetype check (15 Nov 2026): each mechanic checked against this game's rules (summary/03-07); dropped:
  strike twice or first, lock for good, who acts first; added: steal, place units in the enemy camp, attack the turn
  it is placed, my unit acts again, mark an enemy, hit from afar. Agents read 8 real cards of each new or changed
  mechanic only (`work/newmech_verdicts*.tsv`). 53 mechanics; Kaptain agreed them at Stop A (`STOPA.md`).

## Step 5. Each faction's mechanics (15 Nov 2026)
- Scripts, no reading: `cd factions/wheel/work && python3 signatures.py --write` (2 signatures per faction, best fit,
  each fits its faction 0.8+, the two linked) then `python3 borrow.py --write` (2-4 extras by fit, each in at most
  3 factions) -> `work/assign.tsv`. Checked by `work/check_assign.py`.

## Step 6. Links between mechanics
- Numbers only: `python3 mechanics_wheel.py links` -> `wheel/links.tsv` (per pair of mechanics, the same numbers as
  step 2, counted by the links' own effects). `python3 apart.py` gives the pairs real factions keep apart.

## Step 7. Theme, then tools
- Claude picks one theme per faction -> `factions/wheel/themes.tsv` (faction, theme).
- Claude writes 2-4 tools per faction -> `factions/wheel/tools.tsv` (faction, tool, mechanic, the tools it feeds, the
  cell-by-cell line, source: a library card or CLAUDE, NEW RULE). Card texts read for it go into
  `factions/read-cards.tsv` (within the faction's 100).

## Step 8. Combos on this board
- Agents (`work/combo_prompt.txt`, Kaptain's OK first) rate all 190 pairs of factions from their tools and mechanics ->
  `combos.tsv` (STRONG/OK/WEAK/NONE/AGAINST, how it plays, source, a test column for playtests). Partners = STRONG or OK.

## Step 9. The seven answers and Stop 1
- An agent (`work/answers_prompt.txt`) -> `answers.tsv`, from the tools. `python3 tools/wheel_table_check.py` (repo
  root) checks steps 2-9, including words that break this game's rules. `python3 factions/wheel/work/make_stop1.py`
  writes `STOP1.md` and `STOP1-1..5.md`.

## Files, in order
| step | input | script | output |
|---|---|---|---|
| 1 | cards.sqlite, links.sqlite | axes.py | axes.tsv, factions/wheel-axes.html |
| 2 | links.sqlite | mechanics_wheel.py links --radii | wheel/radius_links.tsv |
| 3 | step 2 | by hand, axes.py --near | work/shapes.tsv, arguments.tsv |
| 4 | mechanics.tsv | mechanics_wheel.py cards, agents, measure, links | mechanics.tsv, work/concept_fixes_*.tsv, wheel/measured.tsv, wheel/links.tsv |
| 5 | steps 3-4 | work/signatures.py, work/borrow.py | work/assign.tsv |
| 6 | links.sqlite | mechanics_wheel.py links, apart.py | wheel/links.tsv |
| 7 | steps 5-6 | Claude | themes.tsv, tools.tsv |
| 8 | steps 6-7 | agents | combos.tsv |
| 9 | steps 7-8 | agent, wheel_table_check.py, make_stop1.py | answers.tsv, STOP1*.md |
