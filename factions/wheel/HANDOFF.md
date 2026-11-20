# The wheel: where we are
Read this, then `factions/START_DESIGN-1-wheel.md` (the steps, their rules and the stops), then only the step you are
on. Clone with the library (`git sparse-checkout disable`); `gunzip -kf links.sqlite.gz` in `library/cards_db`.
One chat does one step; at its end, mark the step done here and say what it left for the next.
The Elder Scrolls: Legends (todo.md item 12) runs step 3 again when done.

## The steps
| step | state | what it made |
|---|---|---|
| 1. Fix the library's concepts | done (19 Nov 2026); suspects from the reading of 20 Nov 2026 are open (below) | the library's concepts (`cards.sqlite`, `links.sqlite`) |
| 2. The usable concepts | done (19 Nov 2026): 133 usable, 44 helper, 33 out; return_from_board (73 cards), return_on_leave (76) and hand_deck_swap (5, new over the bar) usable (Claude's) | `work/concepts.tsv`, `work/concepts.md` |
| 3. What decks play together | done (19 Nov 2026): 3027 decks of 10 games; 17 groups by NMF, the most stable number (0.96), Kaptain's (`work/deck_groups_nmf.py --groups 17`) | `work/deck_groups_nmf_17.tsv`, `.md`, `.json` (every deck's card counts and the concepts it leans on, read by step 6) |
| 4. The links between concepts | done (19 Nov 2026, on 3027 decks): 15933 concept pairs, 3171 strong links | `library/cards_db/wheel/concept_links.tsv` |
| 5. The map of what decks play together | done (19 Nov 2026): a page to look at, no later step reads it | `factions/wheel-archetypes.html` |
| 6. The factions, from what they do | in progress: `work/kernel_factions.py` makes the 10 of the trial whole (concepts, theme, markers, list, extras, answers); it runs again on the fixed library, then Kaptain agrees the 10 | `work/kernel_factions.md`, `.tsv`, `work/lists/` |
| 7. Combos on this board | to do | |
| 8. Game plan, then keywords | to do | |
| 9. Stop 1 | to do | |

## Where step 6 stands (20 Nov 2026)
- How the wheel makes a faction (agreed with Kaptain 19-20 Nov 2026; the rules in `START_DESIGN-1-wheel.md` step 6):
  an identity, what the faction DOES in plain words ("can't be broken"), made of concept-tree families; its kernel, the
  effects of those families that 10+ decks lean on; its engines, the concepts real cards strongly link to 2+ kernel
  concepts (links in 2+ games, played by the kernel's decks); its bricks, what the kernel's decks hold 1.5x+ as often as
  their games with no card link; a faction still under 12 takes what its decks hold that cards also link (Claude's);
  every level shared by at most 3 factions; then its theme, design markers, list, 10 extras and answers.
- `python3 factions/wheel/work/kernel_factions.py` (from the repo, about a minute) runs it on the 10 identities of the
  trial (Claude's, `IDENTITIES` and `THEMES`): 8-12 concepts each (Swarms 8, Grows 9 and Waits 10: what they could
  take is held by 3 factions already).
- The library was fixed on 20 Nov 2026 (55 cards read for it, logged in `factions/read-cards.tsv`): Challenger is
  target choice, not forcing attacks (97 Runeterra cards); Duelyst Rebirth and five eggs in Monster Train, Into the
  Breach and Stormbound hatch (transform), never summon or revive; strikes on the neighbouring lanes are neighbours,
  not other lanes (9 Inscryption cards); a unit back to hand when it dies does not cheat death; removing a keyword
  is not having it (Gwent Seize removing Spying is no "give to the opponent"); in the links, Emberdrain given to my own
  units is no help, a card that takes allies' keywords passes none on (426 Runeterra links), and Lightbender's
  dispel on all around it needs enemies moved there, not my units. The concept fixes are in `cards.sqlite`; the egg
  fixes (`fixes/*/v89, v54, v02`) and the links come with the rebuild below.

## Work for the next chat, in this order
1. **The rebuild, after Kaptain's OK**: `check_all.py` (about 14 minutes, loads the egg fixes) and
   `PYTHONHASHSEED=0 python3 links.py` (about 6; its cases include the new ones); then step 2
   (`work/concept_catch.py`: "Force enemy units to attack" and "Reaches other lanes" now have no cards), step 3
   (`deck_groups_nmf.py --groups 17`), step 4 (`mechanics_wheel.py links --concepts`, its wheel cases) and step 6.
2. **Open library findings** (found on 20 Nov 2026, not fixed): (a) the odd engines ("when life or health is
   restored" in Moves and Kills brutally, "damage over time" in Moves) come from how a link counts: a card's trigger
   is counted although the link was made by its effect (Harold Schmidt heals, then pushes; the push makes the link).
   A change to `concept_tags.side_concepts` (count a giver's own effect only, a user's trigger too) is a plan for
   Kaptain first. (b) Into the Breach's repair that cures Fire or A.C.I.D. counts as "when health is restored" on 36
   cards. (c) Gwent: giving Spying counts as "give to the opponent" on 44 cards, unchecked. (d) Gwent Reset counts as
   heal, unchecked. (e) Spawner (Into the Breach) and Spikedriver Colony (Monster Train) cheat death without coming
   back. (f) Lines left to look at after the links fix: Marvel Snap Lady Deathstrike lost 7 lines (does she destroy
   only enemies?) and Lockjaw -> Enchantress is new; a card that takes allies' keywords (Mask Mother) has no line to
   the cards that give an ally a keyword (a missing line, Claude's suggestion in network.py `use_of`).
3. **Kaptain agrees the 10**, then the 20 identities (7+ partners each), then step 7.

## What the next steps find in the files
- Runeterra's spell mana rule is written (`read/runeterra/game_rules.jsonl`) but not built into `cards.sqlite` yet.
- `work/concept_list.py`: `concept_list.Library` scores a set of concepts in under a second.
- Step 2 left: rerun `work/concept_catch.py` from `library/cards_db` only after a change to the concepts or verdicts.
- The faction check (a finished faction's cards against its concepts and extras) and `tools/wheel_table_check.py`
  (the 20 factions' concepts, extras and answers) are written when step 9 and Stop 3 need them.
- `work/make_stop1.py` (step 9) reads files of an earlier way of working (`assign.tsv`, `themes.tsv`, `tools.tsv`); step 9
  rewrites it to read `work/kernel_factions.tsv`.

## The numbers (library/cards_db)
- `links.sqlite` is rebuilt only after `network.py` or `cards.sqlite` changed: `PYTHONHASHSEED=0 python3 links.py`
  (about 6 minutes; with `check_all.py` 14 more: tell Kaptain and wait for his OK); it ends with `cases/links.tsv` and the sides check.
- A link counts for two concepts only through what of each card made it. Example: Ghost Rider brings a card
  back and Vibro-Shock Gauntlets give +2 Power to it: revive with +2 Power, never revive with supply, though the
  Gauntlets also give Energy. Cases: `cases/wheel.tsv`.
- Two concepts you expect to work together show 0 links: check that one pair by script (what made each link between
  their cards) before trusting it; a wrong source is fixed for every card, with cases. Never read cards for it.
- A link seen in one game only can be an accident: of 10 such card pairs read on 20 Nov 2026, 8 did not work together.

## Kaptain's standing decisions
Only what Kaptain said himself goes here, in his words; Claude's own rules go elsewhere.
- Industry words: a **synergy** is a link real cards show between two concepts ("my units die -> my other units
  grow"); a **mechanic** is a keyword, a word on many cards that stands for one rule (Magic's Exploit) (18 Nov 2026).
- "I want to create whole factions" (20 Nov 2026). A faction's kernel is what the faction DOES, never a trigger or a
  condition ("when another unit dies"): "here is a faction that thrives on spells", "one that likes to KILL BRUTALLY",
  "one that WAITS", "one that CAN'T BE BROKEN", "one that FUCKS YOU UP" (19 Nov 2026).
- A faction is not made of 2 archetypes (20 Nov 2026: "is it still needed to be talking about 2 archetypes? this is
  maybe leftover from a process that had a very different beginning").
- Engines come from library links, bricks from deck links: "a faction that protects, its not gonna have any links to
  anything, but it can protect"; the decks inform which supporting concepts go together (20 Nov 2026).
- "A partner needs real library links between the 2 faction's concepts"; 5 partners each while we make 10 factions
  (20 Nov 2026); 7+ partners each among the 20.
- Concepts that land in many factions (silence) "shouldnt be dropped, just given to the most appropriate", maybe by a
  many-level approach (20 Nov 2026).
- No "2+ games" rule for a kernel: "we dont have many moving games, and my game is a moving game" (20 Nov 2026).
- Claude does the bulk of the work (thin kernels are widened by Claude), "so we have something that more or less
  works" (20 Nov 2026).
- Step 3 is "what gets played together" (20 Nov 2026); the wheel keeps 17 groups (19 Nov 2026).
- Hatching from an egg is NOT a summon (20 Nov 2026).
- Reading budget for the next look at the library suspects: 60 cards (20 Nov 2026).
- Two factions share at most half of their own concepts; every faction keeps a blind spot (18 Nov 2026). One idea per
  faction, no fruit salad.
- Kaptain's list holds deck archetypes, what a deck tries to do; a reference only. Combo, Control-Combo and Extra Turns
  are off the list (other archetypes make their own combos); Cycling is part of Wheels (18 Nov 2026). Discard / 8-Rack
  stays on it although real cards don't link its two parts: future improved games will beef it up (17 Nov 2026).
- Cards tagged with the wrong concept are examined and fixed; "Return my unit to hand" is split into smaller concepts
  (18 Nov 2026). Its theme is picked right after its concepts and breaks ties between concepts that score about the
  same. Its list leaves out its own concepts. Its extras, 8 to 12, the same number for every faction, come from its
  list, first for the answers about the board its concepts don't give, then to feed its concepts; an answer no concept
  gives is fixed with another extra. Its blind spot is what none of its concepts and extras give ("never draws cards"),
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
- The wheel is general; step 8 turns each faction's concepts into these own things, from scratch.
- Every game counts the same in every number, games with no factions (Marvel Snap) too.
- Only general ideas; anything specific to one game (planeswalkers) is off. Triggers and conditions are how cards
  work, not what a faction is; real factions inspire, they are never copied (17 Nov 2026).
- Real factions' shapes vary inside each game: the wheel is lax about a faction's shape (17 Nov 2026).
- Interactions with the player (heal, Block, strength on the player; the player hurt) stay out of the wheel: no player
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
  read twice. The wheel reads at most 500 cards in all, by a low-cost model, only where a card's rows can't answer.
- The check script fails on words that break the game's rules ("move first", "strikes first", "placed at round end").
- Keep chats short, scripts first.
