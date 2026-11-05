# Improving the lab's network (handover, 5 Nov 2026)

For the chat that improves the AI lab's learning network. Kaptain's goal: a network that plays well with **any new or
changed card**, ideally also with new keywords and abilities, because cards change all the time during testing and the
network is used to test them. Everything below marked "suggestion" is Claude's, not agreed; agree the plan with Kaptain
before coding (CLAUDE.md), and keep every speed or AI check to about a minute.

## Where it stands
- Files: `src/lab/js/engine/network-encode.js` (inputs, layout, saving and loading), `network-play.js` (choosing moves),
  `src/lab/js/ui/worker.js` (playing and learning in workers), `training-schedule.js`, `running.js`. Built into
  `three-bases-ai-lab.html` by `tools/build.py`; summary/16-ai-lab.txt describes the lab as it is.
- Inputs (format 3, version 7): no card has weights of its own. A card is only its printed values (`cardFeatures`): its
  numbers and keyword flags, and its effects in parts from the card data (`fx`, `aura`, `cast`): when + what
  ("roundEnd:strike"), what + on whom ("strike>nearest"), the whole part ("roundEnd:strike>nearest"), with amounts. About
  640 values on the cards of 5 Nov 2026. Saved networks are moved to a new value list by name (new values start at zero).
- Per board cell (54): the unit anchored there (current strength, defence, damage, build-ups, moved, attacked, orientation,
  and its printed values) or "covered by a unit anchored at ...". Each cell goes through one shared cell layer (16 numbers),
  then the 54 results go side by side into the first main layer (128, then 64, then the output: chance to win), with
  separate weights for every cell. Hand: 10 slots of printed values. Piles (deck, the opponent's unseen cards, dealt hand,
  redrawn cards): card count plus totals of printed values. Lanes, supply, carry-over, round, passes.
- The arithmetic (forward and learning, Adam) is a compiled WebAssembly block (`NET3_WASM`, base64) with **no source in the
  repo**; it takes the sizes as parameters (cards, values per card, cell values, cell layer size, cells, hand slots, other
  inputs, hidden sizes). Learning runs in several workers that share gradients; lessons are also learned mirrored (lanes 1
  and 3 swapped, `F3_MIRROR`); the size check trains bigger copies alongside (`net3Grow`).
- Speed: about 9-12 ms per move playing alone (scoring every legal move once), 0.1-0.2 ms per position.
- Result so far (Kaptain, 5 Nov 2026): stuck at about 50% against the Benchmark (depth 1). The earlier lab reached 70% after
  100,000 games, but on 2 factions with one deck each, a card dictionary, and the earlier, weaker Benchmark: not the same
  test. Units and hand cards were all checked visible to the network (no unknown card keys).

## Checks (5 Nov 2026, headless, about a minute each)
- Learning arithmetic: correct (40 of 40 weights match a slow plain calculation).
- Copying the Benchmark's score: after 25 s of learning, the network agrees with the Benchmark's score (who is ahead)
  on 90% of positions it never saw. So it can see the board well enough; the inputs are not the main problem.
- Predicting the winner (random games, 12,400 positions): network 79% on unseen games after 25 s, the Benchmark's
  score 77%. On learned positions 97%: it learns positions by heart (too many weights: each of the 10 hand slots has
  its own 640 x 128 weights, 820,000 of its 1.3 million).
- Playing: a network trained 35 s to copy the Benchmark's score won 16 of 44 games against the Benchmark (depth 1),
  both looking one move ahead. Knowing who is ahead is not enough; choosing a move needs exact differences between
  the positions each move leads to, which learning from game results alone gives only slowly.
- Shapes (same check, 25 s each, % right on unseen games): as now 78.7, cell layer 32 numbers 77.8, 8 numbers 78.5,
  layers 256/128 79.4, 64/32 79.7, each card its own 8 weights as well 76.3, no hand at all 80.2, hand as totals 80.3.
  All within the check's noise (about 60 unseen games): this check cannot tell shapes apart, and the hand slots give
  it nothing today. Play strength must be tested on a trained network from the lab.
- Kaptain's trained network "Tabula rasa 52%" (369,389 steps), 116 of its positions in games against the Benchmark
  (depth 1), each move compared with the Benchmark at depth 3 (the closest to a referee we have): the network plays
  the same move 29% of the time, the Benchmark at depth 1 67%. Where depth 3 acts, the network passes 24 of 94 times
  (depth 1: never); where depth 3 passes, the network acts 10 of 22 times. Where depth 3 deploys (47), the network
  picks the same card 23 times but mostly another place. Too few games (33) to measure its win rate here.
- Passing (same network, 32 games, 1,934 of its turns): it does not rate round-ending passes too high (it says 56%,
  those games were won 64%). Its win chances match reality well: said under 30% → won 17-18%, said over 70% → won
  94-96%. So its extra passes are not explained by wrong values.
- Hand (same network): hiding the hand moves its win chance by 6 points on Benchmark games (14 on random games), but
  it predicts no better with the hand than without (71.6% against 71.8%): it reacts to the hand without using it well.
- Same wires for a cell in every lane (camp, row and column shared), from scratch, 25 s, 2,437 positions: copying
  the Benchmark's score 89.1% against 87.8% per cell; predicting the winner 76.9% both. No clear gain.
- Look-ahead (same network against the Benchmark depth 1, about 6 minutes): alone 29 of 72 games (40%, 20 ms per
  move here); checking the replies to its 4 best moves 15.5 of 33 (47%, 130 ms per move). The difference is inside
  the noise of so few games; look-ahead does not clearly lift it.
- The Benchmark at depth 1 also scores each move's position once, like the network: the comparison is fair.

- Built for the real test: the training page's "Lessons check" (in place of the size check while on) trains two
  copies on the same games, whose lessons are partly their own win chance one move later (30% and 60%).

- Kaptain's run of 11,107 games from nothing with the Lessons check (tests of 100 games against the Benchmark every
  1,000 games, the last five): end result only 33 25 31 33 35, next move 30% 43 44 46 37 42, next move 60% 37 30 36
  33 40. 30% was ahead in every test from 1,000 games on. Since then every AI learns 30% from the next position, and
  the inputs (version 8) also show what changed on a unit in play and this round's deaths and spells per side.

## Why it may be stuck (suggestion, not proven)
1. **No idea of where units stand relative to each other.** The 54 cell results get separate weights per cell, so any
   relation between two units ("this unit can hit that one", "that aura reaches this unit") must be learned again for
   every pair of cells. A unit can affect any other unit, in any lane or camp (Ranged, auras, round-end strikes on the
   nearest enemy), so limiting the network to neighbours is wrong.
2. **Some keywords are words, not effects.** `kwFx` (`src/game/js/cards/new-00-helpers.js`) writes many keywords out as
   effects (Salvage, Wound, Vigil, Roots, Barrage ...), so the network reads them as effect parts. Others are only flags
   whose rule lives in game code (Ranged, Guard/Bodyguard, Charge, Armoured, Riposte, Flurry ...): the network sees just a
   name. A new keyword of that kind is a new, unknown input.
3. **A new kind of effect is a new word.** A new op or trigger in `fx.js` / `fx-more.js` gets a fresh input that starts at
   zero, so the network knows nothing about it until it has learned it.
4. It may simply need many more games for 14 decks; only training shows.

## What would make it play any new or changed card (suggestions, in the order Claude would try them)
1. **Attention over units** (the main step; Kaptain's choice, todo.md item 8). Each unit is one entry with its values plus
   its position (lane, camp, row, column); every unit looks at every other unit on the board, near or far, and learns
   which ones matter to it. Relative position (how far apart, same lane or not, which camp) is given for every pair, so a
   relation is learned once for every place on the board. This means new arithmetic: write its source into the repo
   this time (plain JavaScript first, or a small WebAssembly written from source kept next to it), so it can be changed
   later. Keep the outer interface (`net3Instance`: `forward`, gradients, `recs`) so workers, mirroring, saving and the
   size check keep working, or change them in the same step.
2. **Every keyword as effect parts.** For each keyword that is only a flag, describe what its rule does in the same parts
   the effects use (e.g. Ranged: "can strike the back rows"; Guard: "takes hits for neighbours"), either in `kwFx` or in a
   lab-side table next to `cardFeatures`. Then a new keyword built from known parts is understood from the start.
3. **Effects as outcome words as well as names.** Next to the op name, give each op its outcome group from
   `library/concept_tree.txt` (damage, removal, debuff, buff, heal, summon, draw, movement ...), kept in a small table in
   the lab; a new op only needs its line in that table to be understood as "a kind of damage" before it is learned.
4. **Train for generality.** Self-play plus the Benchmark (depth 1) as opponents; keep a few earlier versions of the
   network as opponents (a league), so it doesn't learn to beat only itself.

## How to check that it really plays new and changed cards (suggestion)
- **Held-out cards:** train with a set of cards left out of every deck, then test on decks that hold them.
- **Changed cards:** take a trained network, change a few cards' stats or effects (in the lab only), and compare its play
  against the Benchmark before and after a short retraining: it should stay close.
- **Learning check for new arithmetic:** compare its learning steps, number by number, with a slow plain calculation
  (gradient check) on a few positions; a small task with a known answer must be learned; a few minutes of training must
  improve "Predicts the winner".
- Speed: measure on 40 fixed positions (about a minute); playing alone should stay well under 20 ms per move.

## When done
Update summary/16-ai-lab.txt (the network section), todo.md item 8, and the map in CLAUDE.md if parts were added; give
Kaptain the rebuilt `three-bases-ai-lab.html`. Commit; push only when Kaptain asks.
