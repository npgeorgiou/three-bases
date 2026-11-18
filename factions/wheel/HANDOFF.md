# The wheel: where we are
Read this, then `factions/START_DESIGN-1-wheel.md` (the steps, their rules and the stops), then only the step you are
on. Clone with the library (`git sparse-checkout disable`); `gunzip -kf links.sqlite.gz` in `library/cards_db`.
One chat does one step; at its end, mark the step done here and say what it left for the next.

## The steps
| step | state | what it made |
|---|---|---|
| 1. Fix the library's concepts | done | concepts split by whom a row acts on; "Skill" removed; Runeterra's spell mana rule written (`read/runeterra/game_rules.jsonl`) but not built yet |
| 2. The usable concepts | done | `work/concepts.tsv`, `work/concepts.md`: 124 usable, 47 helpers, 37 out (a concept needs 5+ real cards) |
| 3. The archetypes | done | `archetypes.tsv` (agreed with Kaptain): the 38 archetypes that can exist here, 91 parts, engine or brick, every usable concept in at least one part; `archetypes.md` the same in plain words |
| 4. The radii and how they work together | done | `work/radii.tsv` (every usable concept on its radius, agreed with Kaptain); `axes.tsv`, `factions/wheel-axes.html`, `wheel/radius_links.tsv` from concept instances |
| 5. The links between concepts | done | `library/cards_db/wheel/concept_links.tsv` (`mechanics_wheel.py links --concepts`, about a minute) |
| 6. The archetype map | done, approved by Kaptain (18 Nov 2026; `RECHECK.md`) | `work/archetype_map.tsv`: 724 edges between the concepts of engine parts; `factions/wheel-archetypes.html`; one gap (`work/archetype_gaps.tsv`): Discard / 8-Rack |
| 7. The 20 factions | **next**: rules agreed, scripts to write | `work/answer_concepts.tsv` (agreed): per answer its ways |
| 8. Combos on this board | to do | |
| 9. Game plan, then keywords | to do | |
| 10. Stop 1 | to do | |

## What the next steps find in the files
- How the wheel works: a faction is what it is strong at. It plays 2 or 3 archetypes from Kaptain's
  list. Each archetype is made of parts, each a set of alternative concepts: an engine part works through links with
  another part ("my units die" -> "my units gain when an ally dies"), a brick works alone and links to nothing
  (disruption). The 23 radii of `work/radii.tsv` show how the 43 real factions spread (`factions/wheel-axes.html`);
  nothing is designed from them.
- Step 7: every rule is agreed (`START_DESIGN-1-wheel.md` step 7). Write `work/factions.py` and `work/concept_list.py`
  exactly as it says, run them, and show Kaptain the 20 factions' archetypes and concepts (7.1-7.2) before themes,
  lists, extras and answers.
- Still open from the recheck (`RECHECK.md` stage 6): thin maps (Pillowfort, Prison, Extra Turns, Discard / 8-Rack);
  89 "instead" cards not read.
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
- Each faction plays 2 or 3 archetypes; one archetype is played by at most 3 factions; the 20 are picked so the
  weakest is as strong as possible, while they stay varied. From each part of its archetypes it plays only 1 or 2
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
- Factions are made by script to play 2 or 3 archetypes. Each archetype is a group of engines and
  bricks and can be played using different concepts. A map of nodes (each node a concept) shows each
  archetype's concepts with the links between them and the strengths we know. Only general archetypes; any specific to
  one game (planeswalkers) is off the list. Triggers and conditions are how cards work, not what a faction is; real
  factions inspire, they are never copied (17 Nov 2026).
- Discard / 8-Rack stays an archetype although real cards don't link its two parts: future improved games will beef it
  up (17 Nov 2026).
- Real factions' shapes vary inside each game: the wheel is lax about a faction's shape (17 Nov 2026).
- Interactions with the player (heal, Block, strength on the player; the player hurt) stay off the radii: no player
  health here. They stay in the library as player_<concept>.
- Damage over time and my units changing form are possibilities for cards, not concepts a faction builds on.
- An all-Immobile faction is allowed.
- "Strike first" is not a plan here. "Ping" is a library word: say "small hits". One Egg in the
  whole wheel: look-alikes are compared by what the card does.
- A faction's 100 cards use its list a lot (every concept of the library, by how strongly it links with the concepts
  of its archetypes): its archetypes are its character (what it is strongest at, what its keywords grow from), not all it may use.
- A faction is built from a game plan played out cell by cell and its keywords. The keywords are the backbone, not all
  100 cards: 3-5 ways to play are built around them, as many as the closest real factions show. One idea is never the
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
- Countdowns very sparingly. A lane never holds more than 12 supply (summary/05).
- Draw on a kill is allowed: killing an enemy is something the player makes happen.
- "This round" effects that set up another effect of the same round are chains and wanted.
- Reading cards for one faction's chat: at most 100 (its steps 6 and 7), logged in `factions/read-cards.tsv`, never
  read twice. The wheel reads at most 500 cards in all, by a low-cost model, only where a card's rows can't answer.
- The check script fails on words that break the game's rules ("move first", "strikes first", "placed at round end").
- Keep chats short, scripts first.
