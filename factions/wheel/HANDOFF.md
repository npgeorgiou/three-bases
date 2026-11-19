# The wheel: where we are
Read this, then `factions/START_DESIGN-1-wheel.md` (the steps, their rules and the stops), then only the step you are
on. Clone with the library (`git sparse-checkout disable`); `gunzip -kf links.sqlite.gz` in `library/cards_db`.
One chat does one step; at its end, mark the step done here and say what it left for the next.
The Elder Scrolls: Legends (todo.md item 12) runs step 3 again when done.

## The steps
| step | state | what it made |
|---|---|---|
| 1. Fix the library's concepts | done (19 Nov 2026) | the library's concepts (`cards.sqlite`, `links.sqlite`) |
| 2. The usable concepts | done (19 Nov 2026): 133 usable, 44 helper, 33 out; return_from_board (73 cards), return_on_leave (76) and hand_deck_swap (5, new over the bar) usable (Claude's) | `work/concepts.tsv`, `work/concepts.md` |
| 3. The faction archetypes | done (19 Nov 2026): 17 groups by NMF from 3027 decks, the most stable number (0.96), Kaptain's (`work/deck_groups_nmf.py --groups 17`); each carries its design markers; its archetype's concepts are its 10 heaviest and base concepts (about 13), so most pairs share some; `work/make_faction.py` makes a faction from one or two concepts, from the decks alone | `work/deck_groups_nmf_17.tsv`, `.md`, `.json`, `work/step3_groups.py` |
| 4. The links between concepts | done (19 Nov 2026, on 3027 decks): 15933 concept pairs, 3171 strong links; return_from_board has 101 strong links, return_on_leave 36, hand_deck_swap 3 | `library/cards_db/wheel/concept_links.tsv` |
| 5. The archetype map | done (19 Nov 2026, on 3027 decks): 667 edges (37 decks only); 220 of the 222 parts are engines; the page shows design markers (brown), two ticked archetypes as one faction (only when they share a concept), and builds new archetypes | `work/archetype_parts.tsv`, `work/archetype_map.tsv`, `factions/wheel-archetypes.html` |
| 6. The 20 factions | redo (next): `work/factions.py` (2 archetypes) gets the limits of step 6.1; `work/concept_list.py` written | `work/answer_concepts.tsv` (agreed): per answer its ways |
| 7. Combos on this board | to do | |
| 8. Game plan, then keywords | to do | |
| 9. Stop 1 | to do | |

## What the next steps find in the files
- How the wheel works: a faction is what it is strong at. It plays 2 faction archetypes, each a way to play that decks
  of 2+ games lean on (step 3, groups by NMF); real factions are only measured against them. Each archetype is made of
  parts, each a set of alternative concepts: an engine part works through links with another part ("my units die" ->
  "my units gain when an ally dies"), a brick works alone (disruption). Kaptain's list (`archetypes_kaptain.txt`) holds
  deck archetypes: what a pair of factions plays together (step 7).
- Open with Kaptain before step 6 runs (19 Nov 2026, not agreed): which two archetypes may form a faction (share 1 to 3
  concepts; score only the links between concepts that only one of the two holds, since a shared concept counts on both
  sides); how strong a link between two concepts is (both how many times above chance and how many real card pairs,
  in how many games); whether step 5 cuts each archetype to the concepts with a strong card link to another concept
  (inside it or in any archetype) before pairing; how many concepts a faction keeps (about 12 plus 8 extras is like a
  real faction).
- Groups started from chosen concepts (19 Nov 2026, an experiment, not agreed): 15 kernels picked by Claude (30+ decks lean on
  each, in 4+ games, each a different way to play): `deck_groups_nmf.py --kernels sacrifice,on_spell,discard,summon,base_resource_gain,destroy,silence,revive,in_hand_buff,stat_loss,movement,damage_over_time,return_on_leave,adjacency,damage_reduction`
  -> `work/deck_groups_nmf_kernels.*`: stable 0.96, 80% of decks fit a group, 9 of 15 fit a real faction; 9 kernels lead
  their group, 3 sit low in it (summon, revive, adjacency), 3 are not in it (return_on_leave, in_hand_buff, movement); most
  groups match one of the 17. Whether the wheel uses kernels is Kaptain's.
- Factions from what they do (19 Nov 2026, an experiment, not agreed): `python3 factions/wheel/work/kernel_factions.py` ->
  `work/kernel_factions.md`: 10 identities (Claude's: Can't be broken, Kills brutally, Messes you up, Moves, Thrives on
  spells, Waits, Swarms, Grows, Comes back, Eats its own), each a kernel of concept-tree families. Kernels of 3-6
  concepts, 161-329 decks each; their decks add 0-2 concepts (decks lean on about one concept each), so 3-8 in all, not 12;
  Messes you up has no engines (its concepts link to nothing on cards); partners 2-9 (Can't be broken 2, Comes back 9);
  some pairs with many card links fit no deck archetype on the list (Kills brutally + Moves: 25 links, none).
- Runeterra's spell mana rule is written (`read/runeterra/game_rules.jsonl`) but not built into `cards.sqlite` yet.
- `work/factions.py` and `work/concept_list.py` work (about 6 minutes; `concept_list.Library` scores a set of concepts
  in under a second). `factions.py` keeps the limits of step 6.1. Open before it runs: how many own concepts a
  faction keeps (a pair of archetypes holds about 24 that real cards link; a real faction uses about 21, extras included). Its last output (`work/factions.tsv`) is from the deck archetypes and is remade.
- Step 2 left: rerun `work/concept_catch.py` from `library/cards_db` only after a change to the concepts or verdicts.
  Counts moved after step 1's fixes (count_payoff 655 -> 132, condition_count 17 -> 531, permanent_growth 776 -> 584,
  stat_gain 149 -> 59, ping 573 -> 394): steps 3-6 use the new counts.
- The faction check (a finished faction's cards against its archetypes' concepts and extras) and
  `tools/wheel_table_check.py` (the 20 factions' archetypes, extras and answers) are written when step 9 and Stop 3
  need them.
- `work/make_stop1.py` is written for step 9.

## The numbers (library/cards_db)
- `links.sqlite` is rebuilt only after `network.py` or `cards.sqlite` changed: `PYTHONHASHSEED=0 python3 links.py`
  (about 6 minutes; with `check_all.py` 14 more: tell Kaptain and wait for his OK); it ends with `cases/links.tsv` and the sides check.
- A link counts for two concepts only through what of each card made it. Example: Ghost Rider brings a card
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
- Faction archetypes come from the ways to play decks lean on (step 3); Kaptain's list holds deck archetypes, played by a pair of factions.
  Combo, Control-Combo and Extra Turns are off the list (other archetypes make their own combos); Cycling is part of
  Wheels (18 Nov 2026).
- Cards tagged with the wrong concept are examined and fixed; "Return my unit to hand" is split into smaller concepts
  (18 Nov 2026). From each part of its archetypes it plays only 1 or 2
  concepts, the ones real cards link best (no fruit salad). Its theme is picked right after and breaks ties between
  concepts that score about the same. Its list leaves out its own concepts. Its extras, 8 to 12, the same number for
  every faction, come from its list, first for the answers about the board its concepts don't give, then to feed its
  concepts; an answer no concept gives is fixed with another extra before the archetypes are picked again. Its blind
  spot is what none of its concepts and extras give ("never draws cards"), named at step 9 (19 Nov 2026). Combos
  (step 7) come before the game plan and keywords (step 8); 7+ partners each. A finished faction is checked against its
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
- The wheel is general; step 8 turns each faction's archetypes into these own things, from scratch.
- Every game counts the same in every number, games with no factions (Marvel Snap) too.
- Factions are made by script to play 2 archetypes. Each archetype is a group of engines and
  bricks and can be played using different concepts. A map of nodes (each node a concept) shows each
  archetype's concepts with the links between them and the strengths we know. Only general archetypes; any specific to
  one game (planeswalkers) is off the list. Triggers and conditions are how cards work, not what a faction is; real
  factions inspire, they are never copied (17 Nov 2026).
- A faction's kernel is what the faction DOES, never a trigger or a condition ("when another unit dies"): "here is a faction
  that thrives on spells", "one that likes to KILL BRUTALLY", "one that WAITS", "one that CAN'T BE BROKEN", "one that
  FUCKS YOU UP" (19 Nov 2026).
- Discard / 8-Rack stays a deck archetype although real cards don't link its two parts: future improved games will beef it
  up (17 Nov 2026).
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
