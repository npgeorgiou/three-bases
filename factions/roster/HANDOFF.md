# The roster: where we are
Read this, then `factions/START_DESIGN-1-roster.md` (the steps, their rules and the stops), then only the step you are
on. Clone with the library (`git sparse-checkout disable`); `gunzip -kf links.sqlite.gz` in `library/cards_db`.
One chat does one step; at its end, mark the step done here and say what it left for the next.

## The steps
| step | state | what it made |
|---|---|---|
| 1. Fix the library's concepts | done | `cards.sqlite`, `links.sqlite` |
| 2. The usable concepts | done: 131 usable, 44 helper, 33 out | `work/concepts.tsv`, `.md` |
| 3. The real decks' scores | done: 3027 decks of 10 games | `work/deck_scores.json` |
| 4. The links between concepts | done: 15745 concept pairs | `library/cards_db/roster/concept_links.tsv` |
| 5. The map | done (a page only; made after step 6) | `factions/roster-map.html` |
| 6. The factions, from what they do | the 10 of the trial made the agreed way; Kaptain checks them | `work/kernel_factions.md`, `.tsv`, `work/lists/` |
| 7. Combos on this board | to do | |
| 8. Game plan, then keywords | to do | |
| 9. Stop 1 | to do | |

## Work for the next chat, in this order
1. **Fix the library errors found on 20 Nov 2026**, each in the library with test cases (`library/cards_db/START_DATABASE.md`,
   "Fixing errors"; a reading budget from Kaptain):
   - A link does not reliably record which of its two cards acts and which answers (`links.sqlite`: a and b). So a
     card's "when..." part counts for every link its sentence makes: Harold Schmidt pushes "when healed", his push
     links him to Prime Spear's line hit, and "when health is restored" counts as linked to the line. That makes odd
     links like "when health is restored" with moving units. Fix: every link records which card acts; then a card's
     "when..." part counts only when the other card sets it off (a card that kills my unit with my "when a unit dies").
     Before and after: real combos like discard with "when a card is discarded" must keep their links (`cases/roster.tsv`).
   - Into the Breach: the repair that cures Fire or A.C.I.D. counts as "when health is restored" (36 cards).
   - Gwent: giving Spying counts as "give to the opponent" (44 cards) and Reset counts as heal; both unchecked.
   - Spawner (Into the Breach) and Spikedriver Colony (Monster Train) count as cheating death; neither comes back.
   - Marvel Snap: Lady Deathstrike lost 7 links (does she destroy only enemies?); Lockjaw -> Enchantress is new.
   - A card that takes allies' keywords (Mask Mother) has no link to the cards that give an ally a keyword.
   - Stormbound: "kills it" tests read a unit's first-level strength only (Dubious Hags 2/3/4/5/6).
   - `roster/concept_links.tsv`: its `decks` column is empty for most pairs; step 6 counts decks itself. Make it the
     same measure as step 6 or remove it.
   Then rebuild (`check_all.py <any game>`, `links.py`) and rerun steps 2 to 6 and the map
   (`factions/roster/PIPELINE.md`). Keep the old `work/kernel_factions.md` and `work/kernel_factions_summary.json`
   before the rerun, compare both with the new ones, and show Kaptain what moved and why.
2. **Kaptain checks the 10** (`work/kernel_factions.md`); the method stays on 10 factions until he is happy, then 20
   with a limit of 4-5 factions per concept and 7 partners.
3. **Kaptain brainstorms factions** with `work/make_faction.py` (one faction from concepts he gives).
4. Odd answers to look at with Kaptain: Can't be broken removes back-row units with "hits my own side too"; Comes back
   removes front units with "swap positions".

## What the next steps find in the files
- Runeterra's spell mana rule is written (`read/runeterra/game_rules.jsonl`) but not built into `cards.sqlite` yet.
- `work/concept_list.py`: `concept_list.Library` scores a set of concepts in under a second.
- The faction check and `tools/roster_table_check.py` are written when step 9 and Stop 3 need them.

## The numbers (library/cards_db)
- After a change to records, `vocab.tsv` or `flat.py`: `python3 check_all.py <any game>` (about 14 minutes; with no
  game it reloads nothing), then `PYTHONHASHSEED=0 python3 links.py` (about 6); tell Kaptain and wait for his OK.
- A link counts for two concepts only through what of each card made it (Ghost Rider brings a card back, Vibro-Shock
  Gauntlets give it +2 Power: revive with +2 Power, never revive with supply). Cases: `cases/roster.tsv`.
- Two concepts you expect to work together show 0 links: check that one pair by script before trusting it.
- Card pairs that look wrong are library errors: they are read, fixed in the library with test cases, and never
  filtered out by a rule (the 8 suspect pairs of 20 Nov 2026: 6 library errors, fixed; 2 real).

## Kaptain's standing decisions
Only what Kaptain said himself goes here, in his words; Claude's own rules go elsewhere.
- Industry words: a **synergy** is a link real cards show between two concepts ("my units die -> my other units
  grow"); a **mechanic** is a keyword, a word on many cards that stands for one rule (Magic's Exploit) (18 Nov 2026).
- "I want to create whole factions" (20 Nov 2026). A faction's kernel is what the faction DOES, never a trigger or a
  condition ("when another unit dies"): "here is a faction that thrives on spells", "one that likes to KILL BRUTALLY",
  "one that WAITS", "one that CAN'T BE BROKEN", "one that FUCKS YOU UP" (19 Nov 2026).
- A faction is not made of 2 archetypes (20 Nov 2026: "is it still needed to be talking about 2 archetypes? this is
  maybe leftover from a process that had a very different beginning").
- Both card links and decks count: "a faction that protects, its not gonna have any links to
  anything, but it can protect"; the decks inform which supporting concepts go together (20 Nov 2026).
- "A partner needs real library links between the 2 faction's concepts"; 5 partners each while we make 10 factions
  (20 Nov 2026); 7+ partners each among the 20.
- Concepts that land in many factions (silence) "shouldnt be dropped, just given to the most appropriate" (20 Nov 2026).
- No "2+ games" rule for a kernel: "we dont have many moving games, and my game is a moving game" (20 Nov 2026).
- Claude does the bulk of the work, "so we have something that more or less works" (20 Nov 2026).
- Step 3 keeps only each real deck's scores; no groups of decks (20 Nov 2026).
- The kernel is the identity's core plus, for each board question the core does not answer, about 2 concepts that
  answer it; the rest of the faction is what fits the core best (20 Nov 2026: way C of three compared).
- A deck counts for a faction when it holds the kernel's concepts together, as a share of its cards; fit counts both
  card links and decks; extras count toward the limit of 3 factions per concept (20 Nov 2026).
- The factions' peoples come from one new world, never a real one; a hidden real-world model is fine (20 Nov 2026).
- The factions page is one plain sheet per faction; numbers go to a separate page (20 Nov 2026).
- Hatching from an egg is NOT a summon (20 Nov 2026).
- Two factions share at most half of their own concepts; every faction keeps a blind spot (18 Nov 2026). One idea per
  faction, no fruit salad.
- Kaptain's list holds deck archetypes, what a deck tries to do; a reference only. Combo, Control-Combo and Extra Turns
  are off the list (other archetypes make their own combos); Cycling is part of Wheels (18 Nov 2026). Discard / 8-Rack
  stays on it although real cards don't link its two parts: future improved games will beef it up (17 Nov 2026).
- Cards tagged with the wrong concept are examined and fixed; "Return my unit to hand" is split into smaller concepts
  (18 Nov 2026). Its theme is picked right after its concepts and breaks ties between concepts that score about the
  same. Its list leaves out its own concepts. Its extras, 8 to 12, the same number for every faction. Its blind spot is what none of its concepts and extras give ("never draws cards"),
  named at step 9 (19 Nov 2026). Combos (step 7) come before the game plan and keywords (step 8). A finished faction
  is checked against its concepts and extras (18 Nov 2026).
- Keywords are shared, which is what makes factions combo: no keyword is barred from any faction, each is mostly on the
  factions that obviously gain from it, and every faction has at least 1 keyword of its own. All keywords are made
  new for the 20 (18 Nov 2026).
- The game's own things: dots and front cells, rows (front/middle/back), columns, 3 lanes, the 3x3 camp, shapes and
  size, supply per lane, carry-over, round start and round end, one action per turn, moving and turning, reach (melee,
  Ranged), strikes and fixed damage, the hand and the discard pile, Immobile.
- Not in the game: player health, answers on the enemy's turn, supply that grows by itself, unit types, who acts first
  (random in round 1, then alternating), placing at round end.
- The roster is general; step 8 turns each faction's concepts into these own things, from scratch.
- Every game counts the same in every number, games with no factions (Marvel Snap) too.
- Only general ideas; anything specific to one game (planeswalkers) is off. Triggers and conditions are how cards
  work, not what a faction is; real factions inspire, they are never copied (17 Nov 2026).
- Real factions' shapes vary inside each game: the roster is lax about a faction's shape (17 Nov 2026).
- Interactions with the player (heal, Block, strength on the player; the player hurt) stay out of the roster: no player
  health here. They stay in the library as player_<concept>.
- A faction is built from a game plan played out cell by cell and its keywords. The keywords are the backbone, not all
  100 cards: 3 ways to play are built around them. One idea is never the
  whole faction. A keyword that fits the theme but grows from no synergy of the factions that carry it is never made.
- Each faction answers seven questions, one line each: how it wins, how it removes the front unit, how it MAINLY
  removes back-row units, how it MAINLY acts between lanes, how it holds a base, which of the game's own things it
  cares about most (factions may share it), its blind spot (what none of its concepts and extras give: "never draws
  cards"). Removing: his unit leaves its cell; holding: his unit
  stays, but the base stays mine (18 Nov 2026).
- Stop 1 pages: juicy and easy to read; one line per answer; one line per partner faction saying HOW the combo plays.
- Combos are judged once, on this board (step 7): STRONG / OK / WEAK / NONE / AGAINST; partners =
  STRONG or OK, 7+ each; `combos.tsv` has a test column, and what doesn't work in play is dropped.
- Leaders: 5 per faction, the only cards with a golden border, spread over the costs and the ways to play; their
  special part works by whether I hold the lane's base, helps take and keep a lane, never wins harder in a won lane;
  nine kinds, mixed in each faction (START_DESIGN-2, "What a faction has").
- First strike stays out: it does not belong to our game rules (19 Nov 2026).
- A lane never holds more than 12 supply (summary/05).
- Reading cards for one faction's chat: at most 100 (its steps 6 and 7), logged in `factions/read-cards.tsv`, never
  read twice. The roster reads at most 500 cards in all, by a low-cost model, only where a card's rows can't answer.
- The check script fails on words that break the game's rules ("move first", "strikes first", "placed at round end").
- Keep chats short, scripts first.
