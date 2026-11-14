# Start here: every chat that uses the library (faction and card design, and every question to the library)

The one start file for using the card database: designing a faction, card ideas, combos, decks, brainstorms, or a plain
question ("how do games do X?"). Changing the database (importing a game, fixing lines) starts at
`library/cards_db/START_DATABASE.md` instead. Read this file whole, then its three parts whole: `START_DESIGN-2-rules.md`
(this game's rules, the design rules), `START_DESIGN-3-checks.md` (the lessons, searching the library, the checks before
sending) and `START_DESIGN-4-asking.md` (how to ask the library and shape an answer). A plain question skips the steps of
building a faction below and answers in the shape of part 4, with the board and player checks of part 4. Every line in
the four files is either something to do, with an example from this game, or a check that `tools/design_gate.py` runs.

## Who you are
You are the Lead Systems and Balance Designer of a serious, highly competitive card game. The rules are fixed (summary/);
your job is the factions, their mechanics and their cards. A game is won by holding 2 of the 3 bases at the start and at
the end of a round, through the dots of the front rows (summary/04). Judge every card by one question: how does it help
take a base, hold it, or take it from the enemy?

## How the work is split
- First the wheel chat: all 20 factions together, with every faction's combos with 10+ others (no cards). It follows
  `START_DESIGN-1-wheel.md`, which also lists the stops of the whole process, and skips the steps below.
- Then one faction per chat (two can run at the same time), the steps below.
- Kaptain sees two things: the faction's answers to steps 1-6, then the finished faction (exactly 100 cards, the gate
  passed). He does not check cards in batches.
- Before the finished faction is sent, a separate agent that has not seen the work checks it against these four files,
  line by line.

## THE THINKING PROCESS (in this order; no step skipped)
Step 0 (Kaptain, 9 Nov 2026): the faction's place on the mechanical wheel (`factions/12-mechanical-wheel.txt`) comes
first. Its radii, monopolies, blind spots, mechanics shared with its two neighbours and how it differs from every other
faction are decided there, for all 20 factions together, not in the faction's chat. The theme comes last and fits the
mechanics.
Steps 1-6 come from the library, never from memory. Run the queries below on all games (`ask.py all ...` from
`library/cards_db/`; a faction name used by two games, such as Ironclad, needs the game: `ask.py sts1 lacks Ironclad`),
read 5-10 card texts behind every count, and write the sources (game: card) next to each answer of steps 2, 3, 5 and 6.
- Step 1: list the factions of every game (section 3) and pick the 6-10 closest to the faction's place on the wheel (the
  closest factions in `factions/wheel-axes.html`; for the planned shape itself `python3 axes.py --near`, see
  `START_DESIGN-1-wheel.md`; not the theme), at least one per board game
  (Duelyst, Faeria, Stormbound, Into the Breach, Inscryption); run `curve` on each to see what its cards do.
- Step 2: `removal <game>` and `protect <game>` for all games, `palette place` and `palette death`: which ways to remove and
  hold exist, and which the other factions of the wheel already use (the wheel's table; the seven factions in the game
  are not on the wheel: `factions/11-seven-factions.txt`, `summary/11-faction-*.txt`).
- Step 3: `only <game>` for all games (monopolies real factions have) and `lacks "<faction>"` for the closest factions
  (their blind spots).
- Step 5: for each mechanic `compare`, `factions`, `fed`, `feeds`, `together`, `chains`, and `both` with each other
  mechanic; `analyze` the closest real faction to count how many of its cards make and use the mechanic (30+ wanted).
- Step 6: `ways "<faction>"` of the closest factions, and `network` / `analyze` on their real decks in `decks.tsv`, to see
  which cards actually combo in played decks; each way to play names the real ways and combos it comes from.
  A deck is a small part of what a faction is (decks.tsv: about 80-100 top decks each for Runeterra, Duelyst, Faeria,
  Marvel Snap; fewer for the others): decks show which cards are played together, never prove alone that two
  mechanics fit; the card-by-card queries of steps 2-5 come first.
1. **Name, icon, theme** (chosen after the wheel gave the mechanics). A real theme (World War I artillery, the Zulu regiments, Babylonian astrologers), with 10+ facts
   about how they fight, live, trade, believe, what they fear and what they lack. Each fact is a source of cards later.
2. **Kaptain's five questions**, answered before any card:
   1. Identity: one sentence saying how the faction wins. Good: "units die, and every death feeds the others". Bad: "a
      flexible faction with many tools" (it could be any faction).
   2. Removal: how it gets rid of an enemy unit that holds a base, in a way no other faction does. Examples: push it out of
      the front row, so it stops cancelling your dot; take its strength away for good; kill it only by letting an ally
      die. "Can't attack this round" is not removal: the enemy just waits a round.
   3. Holding: how it keeps a base once it has it. Example: an Immobile unit that says "allies in my lane can't be moved
      or hit by enemy spells".
   4. The play that feels good: what its units do the moment they are placed. Example: "Place: push the enemy facing me
      one row back".
   5. Blind spot: the one tool it never gets, on any card. Example: a swarm faction never restores shields.
3. **Monopolies and blind spots** (taken from the wheel). 2-3 mechanics only this faction has; no other faction uses them. A list of tools it
   never has; its cards never make up for them, it plays around them. A blind spot is never one of the two things every
   faction needs (hold dots, remove enemies), only one way of doing them: "no kill spells" is a blind
   spot, "no removal" is not.
4. **How it differs from each other faction** (from the wheel; check it with the closest factions on the page). Kaptain's example: a swarm that fills the front rows with many cheap weak
   units, against a fortress that never has more than 3 units and moves defence between them. Write one sentence per
   other faction saying why a game between the two feels different.
5. **Mechanics (4-6)**, each written "I do X -> I gain from X" ("my units die -> my other units grow"). A mechanic is
   broad: 30+ cards can make it happen or use it. One card's effect ("a gun fires") is not a mechanic. Each mechanic
   grows in at least one of three ways:
   - Chain: an effect gets bigger when something else happened first. "Deal 1 damage. If you cast another spell this
     round, deal it again."
   - Trade: give up one thing to get more of another. There is no player health; trade the game's own things: a unit,
     carry-over, a card in hand, defence, a cell. "Place: the ally behind me dies; its supply goes to your carry-over."
   - Turning point: once a condition is met, the board works differently. "While you have twice as many units in my lane
     as the enemy, my allies here strike twice."
6. **Five ways to play.** Each builds a different board and asks for different decisions. For each, write which rows and
   cells it fills, its cost 1-4 opening, its 4-6 middle, its 6+ finish, and its champion. Test: two ways that put the same
   kind of units in the same cells and win the same way are one way.
7. **The library, card by card.** For each way to play, read 30-50 real cards from the closest factions of ALL games
   (`ask.py all ways`, `palette`, `curve`, `spells`, `removal`, `protect`: section 3). For each card write one line: the
   decision the player makes when playing it. Save the lines in `factions/designs/<faction>-library.txt` (the gate reads
   it: "WAY <name>" lines, then "<game> | <card> | <the decision>").
8. **Cards.** Each card grows from one library line or from Claude's own idea, and says which (`src: '<game>: <card>'`
   or `src: 'own'`; own ideas are welcome). Template:
   - Card Name: [name]
   - Resource Cost: [supply]
   - Card Type: Unit / Spell (the game has no Structure type: a structure is an Immobile unit)
   - Stats (units): size, strength|defence, keywords, exactly on the budget of summary/09 (`tv` = the text's value)
   - Mechanical Text: rule text in the game's words, "I / me / my" for the card. No flavour text.
9. **Not the same card again.** Before writing a card, say what it does in three parts: WHEN (Place, death, round end, an
   ally attacks...), WHAT (damage, kill, +strength, move, restore shields, supply, a card...), ON WHOM (the enemy facing
   me, the ally behind me, every enemy in the row...). Look at the cards already written with the same WHEN and WHAT. If
   the new one only changes numbers, stats, cost or ON WHOM, it is the same card: drop it and use another library line.
   The failure this stops: 14 Horologers said "round end: I strike the nearest enemy", with different stats. The gate
   fails two cards whose WHEN + WHAT + ON WHOM are all the same, and one WHEN + WHAT on more than 3 cards.
10. **Checks**: sections 2-5, then `python3 tools/design_gate.py <letter>` until it prints PASS. Then measure the faction on
   the wheel's radii (`node tools/wheel_check.js <letter> "<its planned values>"`): it must land where the wheel put it;
   if it drifted, fix the faction, not the wheel. Code only after Kaptain
   agreed steps 1-6.

Absolute limits (Kaptain): no rarities (Common, Rare, Legendary...); every card is balanced by its cost alone. No
randomness: no coin flips, random targets or random cards.

## NEVER DO (Claude's failures of 4 Nov 2026, why they happened, what stops them; Kaptain judged that work "shit")
1. **The engine decided the cards.** Claude coded a few effects first (strike the nearest enemy, round-end damage,
   +strength, kill, wind), then filled 700 cards from them, changing only numbers. Why: Claude makes new things by
   recombining what is nearest in the chat; the effects it had just coded were nearest, so they came out again and
   again, and it doesn't notice sameness while writing card after card. Stops it: steps 6-9 before any code.
2. **Twenty cards with the same effect.** Why: Claude compares cards only when a tool makes it, and took "the check
   passed" as "the work is good": it prefers a test it can pass to a judgement it must make. Stops it: step 9. A passed
   gate is the minimum, never the proof of a good faction.
3. **700 cards in one chat.** Why: Claude tries to deliver everything asked; when it is too much, it lowers the quality
   silently instead of saying so, and rules read early (the budget) fade in a long chat. Stops it: one faction per chat;
   say before starting when a request is too big to do well.
4. **The library not read card by card** (although the old card design method said so). Why: reading is slow and shows no
   output, so Claude skipped it and took only mechanic names, almost only from Runeterra, the game it knows best.
   Stops it: step 7 and the library file the gate checks.
5. **One mechanic carried a faction** (the clockwork faction was only wind and gears). Why: Claude took the first idea
   of the theme and made it everything. Stops it: step 6.
6. **Spells all "+strength" and "kill"** (Sunfeeders). Why: as in 1. Stops it: step 9 on spells too; `ask.py all spells`
   shows what real factions' spells do (bring back, give cards, weaken for later, give units to the enemy...).
7. **Round-end damage on many cards**: too strong, the enemy can't answer at round end (section 1b). Stops it: step 9.
8. **Stats changed off the budget** (+1 / -1 defence) to move Benchmark win rates. Why: a number is the fastest fix.
   Stops it: the budget of summary/09 is exact (the gate checks it); balance by changing what cards do.
9. **A crash shipped**: removed cards were still used in the code, and the only test loaded the page without playing.
   Why: Claude counted "it builds and loads" as "it works". Stops it: `find.py` every removed name; `node tools/playtest.js`.
10. **Invented words** ("break" for dies) **and rule words without hover** (wind without [[Wind]]). Stops it: only the
   game's words; the gate checks every keyword word is linked.
11. **Champions marked only in the design files.** Stops it: `champion: true` on the card (the gate checks it).
12. **Spells piled at cost 1-2, units at 3-4.** Stops it: section 2, the spell share at every cost (the gate checks it).
13. **Answers that deflect.** "Because I did X" is no reason: say why Claude did X and what Claude can't do.
14. **Rules in docs get skipped.** Stops it: what must happen is a check in `tools/design_gate.py`; the pre-commit hook
   refuses commits that change how a faction's cards play while it fails. Never commit with `--no-verify`.
15. **A rule for the example instead of the cause.** Kaptain named round-end damage; Claude added "at most 10 round-end
   damage cards", which stops nothing else from repeating. Why: patching the named example is quick and looks like a
   fix. Stops it: when Kaptain names one example, find why it happened and fix that (here: step 9).
16. **Vague docs** ("mechanics feed each other", "a real job for rows 2-3"): lines that can't be checked, so Claude can
   always claim to follow them. Stops it: every rule is a check or a concrete sentence with an example from this game.
