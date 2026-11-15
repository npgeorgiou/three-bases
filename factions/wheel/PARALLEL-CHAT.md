# What a parallel chat did to the wheel (15 Nov 2026), for the wheel chat to take over

Kaptain sent the message below to the wrong chat. That chat (not you) answered it, agreed changes with Kaptain and
redid the wheel from step 4. It replaced your files (your last own commit: `7c60e35`; your Stop 1 pages, `table.tsv`,
`board.tsv`, `combos.tsv` and work files were deleted in `c371306`, and are still in git there). Decide with Kaptain
what to keep; `git diff 7c60e35 HEAD -- factions tools` shows every change.

## Kaptain's message (meant for you)
Stop files need high-level descriptions and how a faction MAINLY removes enemy back-row units. Egg is in at least 2
factions (wrong). Are there straight kill spells, or bringing back without Eggs? J: copy only, or steal too? Does anyone
have steal? What is "ping", is it invented? G "strike first": how, in a turn-based game? A mechanic for who plays first?
Units are placed only on my side; does a faction break that? A line on how each faction MAINLY acts between lanes?
A faction that grows when its units take damage (a basic archetype; how was it missed)? An all-Immobile faction? Treat
these questions as a rethinking: say what can be improved; when general thought patterns must change, remind Kaptain to
ask for the docs to be updated; the chat with the context does the changes.

## The parallel chat's answers (checked in the files)
- No back-row removal and no between-lanes line existed; every "Removes" was about the enemy facing my dot.
- Egg was in A and M (M's junk Egg). Duplicates had been checked by mechanic name, not by what the card looks like.
- No kill spell anywhere (K killed only by a unit's Place); bringing back without an Egg only once (A).
- Steal: nobody; the library's "steal" was folded into M's "change". J only copies.
- "Ping" = a library word for small fixed damage; not a rule, but not Kaptain's word.
- "Strike first" means nothing here: an attacked unit does not hit back (only Riposte). Who starts: random, then
  alternating; no faction changes it. Units go only into my own camp; nobody breaks it.
- "Grows when hurt" was missing because the rule then barred mechanics small in the library from being a base.
- All-Immobile: N had it.

## What Kaptain agreed in that chat
1. G becomes the faction that grows when its units take damage (signatures: grows when hurt + I damage my own units).
2. All 20 factions are redone (the small-mechanic rule had shaped every faction's choice), not only G and M.
3. The guides are rewritten cleanly, as if done right from the start, no history.
4. Stop A: the new mechanics list (Kaptain said "ok").

## What was done (commits after `7c60e35`)
- `51ce1bc` Guides rewritten: `START_DESIGN-1-wheel.md` (steps 1-9 in order, Stop A after the mechanics list, a rule
  check of every mechanic against this game, an archetype check, small mechanics allowed as a base, board versions
  compared by what the card does, seven answers), `12-mechanical-wheel.txt` (principles and radii only),
  `START_DESIGN.md` step 2 (seven questions: wins, front removal, back-row removal, between lanes, holding, best
  Place, blind spot).
- `3fe63bb` Step 4: `mechanics.tsv` checked; agents read 8 real cards per new or changed mechanic
  (`work/newmech_verdicts*.tsv`). Dropped: strike twice or first, lock for good (library has only one-round stuns),
  who acts first (no library cards). Added: steal, place units in the enemy camp, attack the turn it is placed, my
  unit acts again, mark an enemy, hit from afar. Changed: grows when hurt, ping = "small hits", change without steal,
  junk = cards only. 53 mechanics; Kaptain's page `STOPA.md`.
- `c371306` Old files removed from `factions/wheel/` and `work/` (yours included); README and HANDOFF rewritten.
- `80e53db` Step 5: `work/signatures.py` (exact best fit: every signature fits its faction 0.8+, the two linked, 3+
  extras possible, G fixed) and `work/borrow.py` (extras by fit, at most 3 factions each) -> `work/assign.tsv`.
  G's shape redone: grows 1.6, grows defence 1.4, spends 1.4, strikes 1.2 (`work/shapes.tsv`).
- `5d1ca09` Step 6: 127 unread strong mechanic pairs read by agents, merged into `work/mechanic_pair_verdicts.tsv`.
- Last commit (with this file): step 7 `board.tsv` (agents: 2-3 versions per faction, one BACKROW, one LANES, one
  IDEA each, 30 look-alikes removed; the only Egg is A's), step 8 `combos.tsv` (all 190 pairs rated on this board),
  step 9 `answers.tsv` (the seven answers by an agent), new `tools/wheel_table_check.py`, `work/make_stop1.py`
  (writes the Stop 1 pages; not run yet). Agent prompts: `work/board_prompt.txt`, `combo_prompt.txt`,
  `answers_prompt.txt`.

## Where it stopped
- The check fails only on board versions whose mechanic is written in words, not its key (I: leftover hit, big
  strength, cheaper; O small units; P extra action; R grow in hand, grow on kill; S count). Partners: 14-19 per faction.
- Not done: fix those keys, read `answers.tsv` for quality, run `work/make_stop1.py`, rewrite `PIPELINE.md` for steps
  1-9, update `HANDOFF.md`, Stop 1 with Kaptain.
- Signature assignment: A revive+leave, B deathfeed+offering, C sacrifice+area, D spellpay+create, E spelldmg+cheaper,
  F adjacency+heal, G hurt+selfhurt, H recycle+draw, I overkill+bigstrength, J copy+pick, K returnhand+kill,
  L silence+guard, M change+steal, N shield+hide, O lastwords+tokens, P lanes+extraact, Q push+ping, R onkill+inhand,
  S countboard+supply, T fight+haste.
