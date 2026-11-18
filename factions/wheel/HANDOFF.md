# The wheel: where we are
Read this, then `factions/START_DESIGN-1-wheel.md` (the steps, their rules and the stops), then only the step you are
on. Clone with the library (`git sparse-checkout disable`); `gunzip -kf links.sqlite.gz` in `library/cards_db`.
One chat does one step; at its end, mark the step done here and say what it left for the next.

## The steps
| step | state | what it made |
|---|---|---|
| 1. Fix the library's concepts | **next**: the split and second reading of the 23 "mixed" families of `work/tag_verdicts.tsv`; the 36 Mirage lines | concepts split by whom a row acts on; "Skill" removed; "Return my unit to hand" split into return_from_board and return_on_leave; `work/tag_check.py`; the first reading (194 cards) and the fixes of its 11 "fix" families (cases wc44-wc55), rebuilt with `check_all.py` and `links.py`; Runeterra's spell mana rule written (`read/runeterra/game_rules.jsonl`) but not built yet |
| 2. The usable concepts | redo after step 1 | `work/concepts.tsv`, `work/concepts.md` |
| 3. The faction archetypes | to do (`work/faction_archetypes.py` to write) | `deck_archetypes.tsv` and `.md`: the deck archetypes' parts, for step 8 (checked once first, `PIPELINE.md` step 8) |
| 4. The radii and how they work together | redo: the new concepts of step 1 get a radius (Kaptain agrees), then `axes.py` | `work/radii.tsv`, `axes.tsv`, `factions/wheel-axes.html`, `wheel/radius_links.tsv` |
| 5. The links between concepts | redo | `library/cards_db/wheel/concept_links.tsv` |
| 6. The archetype map | redo with the faction archetypes | `work/archetype_map.tsv`, `factions/wheel-archetypes.html` |
| 7. The 20 factions | redo: `work/factions.py` (2 archetypes) gets the new limits; `work/concept_list.py` written | `work/answer_concepts.tsv` (agreed): per answer its ways |
| 8. Combos on this board | to do | |
| 9. Game plan, then keywords | to do | |
| 10. Stop 1 | to do | |

## What the next steps find in the files
- How the wheel works: a faction is what it is strong at. It plays 2 faction archetypes, each what a group of real
  factions from 2+ games is strong at. Each archetype is made of parts, each a set of alternative concepts: an engine
  part works through links with another part ("my units die" -> "my units gain when an ally dies"), a brick works
  alone (disruption). Kaptain's list (`archetypes_kaptain.txt`) holds deck archetypes: what a pair of factions plays
  together (step 8). The 23 radii of `work/radii.tsv` show how the 43 real factions spread (`factions/wheel-axes.html`).
- Step 1, the tag check: `work/tag_check.py` groups every usable concept's cards by what put the tag on and marks the
  suspect groups: 517 of 7628, in 52 families (a family: one concept, one action or test, one reason). 5 cards of each
  family were read (`work/tag_reads.tsv`, verdicts in `work/reads/`), summed by `work/tag_read_sum.py` into
  `work/tag_verdicts.tsv`: 18 families stay, 23 are mixed, 11 were fixed in `flat.py`: a count of what is there now is
  "Counts / thresholds"; a cost raised is "Make the opponent's cards cost more" on the enemy and a drawback on mine; a
  unit summoned onto the enemy side is "Clog the opponent's board"; a copy put into the enemy's deck or hand is a
  drawback; a summon trigger on an enemy unit is "When an enemy arrives"; cards traded with the opponent's piles are
  "Swap or replace hands or decks"; a copy of an enemy's card is mine (Unleash the Evil); "-X Power" is no gain.
  Open: Mirage (Marvel Snap) gives +2 Power to its copy of an enemy card, and network.py (rule at line 2446) draws 36
  "more power" lines from it to my cards that read their power; the copy is never one of them.
  Mixed (split by one more
  detail, 5 of each half read): "Absorb one hit" from cancelling a spell (5 of 5 wrong, but not the same way),
  "Mark a target" on my side (5 wrong, different ways), "Grows again and again" that grows once (3 right, 2 wrong),
  "Stat gain" that lowers a stat, buffs given to an enemy, "Ping" on my side, and the rest. Rainbow and Gifts for a
  Guard are known wrong cards; Titanstooth (Offering) and Swinging Glaive (Equipment) are right.
- "Return my unit to hand" is split by what its rows say: return_from_board (my unit in play goes back to hand by an
  effect or its own ability: Recall an ally, Boomerang; 57 cards) and return_on_leave (back to hand when it dies or leaves
  play: Unkillable, Attach, Equipment; 76). No row says "from the discard pile": those cards are recycle or revive. The 17
  whose rows say neither whose unit nor from where (Will of Ionia, Defiant Dance, Ahri) keep return_to_hand and are in
  the reading. The two new concepts are not in `work/concepts.tsv` until step 2 is redone, so the tag check does not
  look at them yet.
- `work/factions.py` and `work/concept_list.py` work (about 6 minutes; `concept_list.Library` scores a set of concepts
  in under a second). `factions.py` still has the main radius limit: change it to the limits of step 7.1. Its last
  output (`work/factions.tsv`) is from the deck archetypes and is remade.
- Open with Kaptain, decided when step 3 starts: is a faction archetype a whole faction (a group of real factions
  strong at the same things; then a faction plays 1) or a smaller piece (concepts the same real factions of 2+ games
  are strong in together, linked or not, so bricks belong; then a faction plays 2, as step 7 says)? The pieces would
  be cut by script, the cut-offs agreed with Kaptain.
- Open with Kaptain: the concept "First strike" is out by a rule Kaptain removed ("strike first is not a plan");
  ask whether it becomes usable in step 2.
- Counts whose rows don't say what they count are counted nowhere: 189 instances of "grows with what happened" and 36
  of "counts and thresholds" (`axes.py` prints them). Most are counts of enemy units or of a keyword the rows don't name.
- The faction check (a finished faction's cards against its archetypes' concepts and extras) and
  `tools/wheel_table_check.py` (the 20 factions' archetypes, extras and answers) are written when step 10 and Stop 3
  need them; `wheel_table_check.py` today measures the radii.
- `work/make_stop1.py` is written for step 10.

## The numbers (library/cards_db)
- `links.sqlite` is rebuilt only after `network.py` or `cards.sqlite` changed: `PYTHONHASHSEED=0 python3 links.py`
  (about 6 minutes; with `check_all.py` 14 more: tell Kaptain and wait for his OK); it ends with `cases/links.tsv` and the sides check.
- Radius keys are not plain words: look up each one's name before talking about it
  (`work/radii.tsv`). `many` is "many at once", `wide` is "many units on my side", `back` is "reuses cards",
  `cards` is "more cards in hand", `picks` is "picks cards".
- A link counts for two concepts or radii only through what of each card made it. Example: Ghost Rider brings a card
  back and Vibro-Shock Gauntlets give +2 Power to it: revive with +2 Power, never revive with supply, though the
  Gauntlets also give Energy. Cases: `cases/wheel.tsv`.
- Two concepts you expect to work together show 0 links: check that one pair by script (what made each link between
  their cards) before trusting it; a wrong source is fixed for every card, with cases. Never read cards for it.

## Kaptain's standing decisions
- Industry words: a **synergy** is a link real cards show between two concepts ("my units die -> my other units
  grow"); a **mechanic** is a keyword, a word on many cards that stands for one rule (Magic's Exploit) (18 Nov 2026).
- Each faction plays 2 archetypes; one archetype is played by at most 3 factions; the 20 are picked so the
  weakest is as strong as possible, while they stay varied: two factions share at most half of their own concepts,
  every faction keeps a blind spot, and some archetypes stay unused (18 Nov 2026).
- Faction archetypes come from real factions; Kaptain's list holds deck archetypes, played by a pair of factions.
  Combo, Control-Combo and Extra Turns are off the list (other archetypes make their own combos); Cycling is part of
  Wheels (18 Nov 2026).
- Cards tagged with the wrong concept are examined and fixed; "Return my unit to hand" is split into smaller concepts
  (18 Nov 2026). From each part of its archetypes it plays only 1 or 2
  concepts, the ones real cards link best (no fruit salad). Its theme is picked right after and breaks ties between
  concepts that score about the same. Its list leaves out its own concepts. Its extras, 8 to 12, the same number for
  every faction, come from its list, first for the answers about the board its concepts don't give, then to feed its
  concepts; an answer no concept gives is fixed with another extra before the archetypes are picked again. Its blind
  spot is a whole radius it never gets ("never draws cards"). Combos
  (step 8) come before the game plan and keywords (step 9); 7+ partners each. A finished faction is checked against its
  archetypes and extras (18 Nov 2026).
- Keywords are shared, which is what makes factions combo: no keyword is barred from any faction, each is mostly on the
  factions that obviously gain from it, and every faction has at least 1 keyword of its own. All keywords are made
  new for the 20 (18 Nov 2026).
Only what Kaptain said himself goes here, in his words; Claude's own rules go elsewhere.
- The game's own things: dots and front cells, rows (front/middle/back), columns, 3 lanes, the 3x3 camp, shapes and
  size, supply per lane, carry-over, round start and round end, one action per turn, moving and turning, reach (melee,
  Ranged), strikes and fixed damage, the hand and the discard pile, Immobile.
- Not in the game: player health, answers on the enemy's turn, supply that grows by itself, unit types, who acts first
  (random in round 1, then alternating), placing at round end.
- The wheel is general; step 9 turns each faction's archetypes into these own things, from scratch.
- Every game counts the same in every number, games with no factions (Marvel Snap) too.
- Factions are made by script to play 2 archetypes. Each archetype is a group of engines and
  bricks and can be played using different concepts. A map of nodes (each node a concept) shows each
  archetype's concepts with the links between them and the strengths we know. Only general archetypes; any specific to
  one game (planeswalkers) is off the list. Triggers and conditions are how cards work, not what a faction is; real
  factions inspire, they are never copied (17 Nov 2026).
- Discard / 8-Rack stays a deck archetype although real cards don't link its two parts: future improved games will beef it
  up (17 Nov 2026).
- Real factions' shapes vary inside each game: the wheel is lax about a faction's shape (17 Nov 2026).
- Interactions with the player (heal, Block, strength on the player; the player hurt) stay off the radii: no player
  health here. They stay in the library as player_<concept>.
- A faction is built from a game plan played out cell by cell and its keywords. The keywords are the backbone, not all
  100 cards: 3 ways to play are built around them. One idea is never the
  whole faction. A keyword that fits the theme but grows from no synergy of the factions that carry it is never made.
- Each faction answers seven questions, one line each: how it wins, how it removes the front unit, how it MAINLY
  removes back-row units, how it MAINLY acts between lanes, how it holds a base, which of the game's own things it
  cares about most (factions may share it), its blind spot (a whole radius it never gets: "never draws
  cards"). Removing: his unit leaves its cell; holding: his unit
  stays, but the base stays mine (18 Nov 2026).
- Stop 1 pages: juicy and easy to read; one line per answer; one line per partner faction saying HOW the combo plays.
- Combos are judged once, on this board (step 8): STRONG / OK / WEAK / NONE / AGAINST; partners =
  STRONG or OK, 7+ each; `combos.tsv` has a test column, and what doesn't work in play is dropped.
- Leaders: 5 per faction, the only cards with a golden border, spread over the costs and the ways to play; their
  special part works by whether I hold the lane's base, helps take and keep a lane, never wins harder in a won lane;
  nine kinds, mixed in each faction (START_DESIGN-2, "What a faction has").
- Countdowns very sparingly.
- A lane never holds more than 12 supply (summary/05).
- Reading cards for one faction's chat: at most 100 (its steps 6 and 7), logged in `factions/read-cards.tsv`, never
  read twice. The wheel reads at most 500 cards in all, by a low-cost model, only where a card's rows can't answer.
- The check script fails on words that break the game's rules ("move first", "strikes first", "placed at round end").
- Keep chats short, scripts first.
