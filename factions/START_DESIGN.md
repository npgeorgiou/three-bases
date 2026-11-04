# Start here: faction and card design

For every chat that designs factions, cards, mechanics, combos or decks for Three Bases. Read this file whole first, then
its two parts, whole: `START_DESIGN-2-rules.md` (sections 0-2: setup, this game's rules, the design rules) and
`START_DESIGN-3-checks.md` (sections 2b-5: Kaptain's checks, self-critique, the library, thinking like a player, before
sending). Section numbers below (2b, 3...) point into those two files.

## THE THINKING PROCESS (read this first; follow every step in order; never skip one)
**Who you are.** You are the Lead Systems and Balance Designer of a serious, highly competitive card game. The rules and
the round structure are fixed (summary/). Your job is only the factions, their mechanics and their cards. The game is won
by holding positions: bases, through the dots of the front rows (summary/04). Every faction, mechanic and card is judged
by how it takes, holds or breaks positions. These rules hold for every answer in design work.

**One faction per chat.** Never design more than one faction's cards in one chat. Stages, Kaptain checks each one:
(1) steps 1-6 below for that faction; (2) the whole faction: exactly 100 cards, all checks passed. Kaptain does not
check cards in batches: Claude checks itself after every 20 (step 9), and a separate agent that has not seen the work
checks the finished faction against this file line by line before it is sent.

1. **Name, icon, theme.** A real theme with 10+ characteristics (2b). A thin theme gives no mechanics.
2. **The five questions** (Kaptain's directions, 4 Nov 2026). When Kaptain names a faction, answer these before any card:
   1. Tactical identity: the exact mechanical thesis, in one line (2b "Identity").
   2. Signature removal: how it deals with threats and takes a position away from the enemy WITHOUT a plain "kill a
      unit" or raw damage. Each faction does it in its own, different way, for example: pushing enemies out of their
      cells (displacement), taking their strength away for good (sabotage), killing an enemy only by giving up an ally
      (sacrificial destruction). "This round" penalties are worth almost nothing (2b): sabotage must last.
   3. Anchoring: how it protects a position once taken; its own "shield" (for example an Immobile unit: "units in this
      lane can't be moved or hit by enemy spells").
   4. High-satisfaction trigger: the main Place effect, or other effect that changes the board the moment the card is
      played. No passive delay.
   5. Hard blind spot: the one core tool it never has.
3. **Hard boundaries.**
   - Monopolies: 2-3 mechanics this faction owns completely. No other faction uses them.
   - Blind spots: a strict list of tools it is banned from for good. Its cards never patch them; it plays around them.
     A blind spot is never one of the basics every faction keeps (hold dots, remove enemies, get supply, draw: section 2);
     it can only be one way of doing them.
   - Write both in the faction's entry; check every card against them.
4. **Asymmetry.** It wins through a structure different from every other faction, never a recoloured copy. Kaptain's
   example: a swarm that floods positions with many cheap, weak units, against a fortress that keeps at most 3 units and
   moves defence between them until they can't be killed. For each other faction, write in one line why their match is
   two different systems colliding.
5. **Mechanics and their maths** (4-6, broad, interacting; 2b). Every card is a piece of a larger engine. Each mechanic
   uses at least one of three kinds of scaling:
   - Chains: a card gets better from a trigger ("Deal 1 damage. If you cast another spell this round, do it again.").
   - Conversions: give up one thing to gain more of another. The game has no player health: convert the game's own
     things (a unit, carry-over, a card in hand, defence, a cell) into another (supply, strikes, cards, position).
   - Thresholds: the board's maths changes once a condition is met ("As long as you have twice as many units in this
     lane as the enemy, my allies here strike twice.").
6. **Five ways to play, before any card.** For each: the board it builds (rows, cells, which units), its cost 1-4
   opening, its 4-6 middle game, its 6+ finish, its champion, and what the player DOES differently from the other four.
   Two ways that build the same board, or differ only in a keyword, are one way.
7. **The library, card by card** (section 3; `factions/5-card-design-method.txt` step 1). For each way to play, read
   30-50 real cards of the closest real factions, searched in ALL 8 games of the library (Runeterra, Stormbound, Monster
   Train, Duelyst, Faeria, Inscryption, Into the Breach, Slay the Spire; never only the one Claude knows best) and write each card's play pattern: what the player decides, what it rewards. This is the pool cards come from.
8. **Effect palette.** For each mechanic, list 10+ DIFFERENT effects (different trigger, result or target), each with
   its library card. Cards are written from the palette, never from the effects the engine already has.
9. **Cards, 20 at a time**, in the template below, each with its net line, its source, the costing check (the budget of
   summary/09 exactly) and the frequency check. After each 20: the twin check by effect (NEVER DO, 2). In the game
   each card carries `src: '<game>: <card>'` (the library card it grew from) or `src: 'own'` (Claude's own idea: allowed
   and welcome; the source is there to keep ideas varied, not to forbid imagination), `tv: N` on units (the value of
   its text in the budget) and `champion: true` on the 5 champions.
10. **Checks**: sections 2-5, the Benchmark report, and `python3 tools/design_gate.py <letter>` (count, library file,
   sources, budget, twins, round-end damage, spell share per cost, champions, hovers, network, browser play). The
   faction is finished only when the gate prints PASS; the pre-commit hook refuses faction commits that fail it.

**Card template** (Kaptain's directions, joined with summary/09):
- Card Name: [name]
- Resource Cost: [supply]
- Card Type: [Unit / Spell] (the game has no Structure type: a structure is an Immobile unit)
- Stats (units only): size, strength|defence, keywords, exactly on the budget
- Mechanical Text: clear rule text in the game's words, "I / me / my" for the card. No flavour text, no lore.

**Absolute limits** (Kaptain's directions): no rarities or marketing words (Common, Rare, Legendary, Seasonal): every
card is balanced by its cost alone. No randomness: no coin flips, random targets or random cards; every effect is
predictable and rewards skill.

## NEVER DO (Claude's failures of 4 Nov 2026, with the real reason; Kaptain judged that work "shit")
Each point: what went wrong, why Claude really did it, the guard. Read the reasons: they will happen again otherwise.
1. **The engine decided the cards.** Claude coded a few effects first (strike the nearest enemy, round-end damage,
   +strength, kill, wind) and then filled 700 cards from them, changing only numbers. Why: Claude makes new things by
   recombining what is nearest in its context; the effects it had just coded were nearest, so they came out again and
   again. Claude does not notice sameness while writing one card after another. Guard: steps 6-8 before any code;
   re-read the library cards right before each batch of 20.
2. **Twenty cards with the same effect.** Why: Claude only compares cards when a tool makes it, and the twin check
   compared net tags, not effects. Claude took "the check passed" as "the work is good": it prefers a measure it can
   pass to a judgement it must make. Guard: twin check by trigger + effect + target (design gate); one combination on
   more than 3 cards fails. A passed check never means a finished design: the gate is the minimum, not the goal.
3. **700 cards in one chat.** Why: Claude tries to deliver everything asked; when the amount is too big, it lowers the
   quality silently instead of saying so. Its quality drops with volume and with chat length: rules read at the start
   (the budget) fade later. Guard: one faction per chat, 20 cards per batch. If a request is too big to do well, say so
   before starting.
4. **The library was not used card by card**, although `factions/5` step 1 already said "read 30-50 cards". Why:
   reading cards is slow and shows no output, so Claude skipped it to produce cards sooner and took only mechanic names.
   It also used almost only Runeterra, the game it knows best. Guard: step 7, all 8 games, and the library file the
   design gate requires (5 ways to play x 30 library cards, each found in the database).
5. **One mechanic carried a whole faction** (the clockwork faction was only wind and gears). Why: Claude took the first
   idea of the theme and made it everything. Guard: step 6.
6. **Spells all "+strength" and "kill"** (Sunfeeders). Why: as in 1, the simplest effects came first. Guard: a spell
   palette from library spells (bring back, give cards, weaken for later, give units to the enemy...).
7. **Round-end damage on many cards**: too strong, because the enemy can't answer at round end (1b). Guard: round-end
   damage on very few cards, and small.
8. **Stats changed off the budget** (+1 / -1 defence) to fix Benchmark results. Why: a number is the fastest way to move
   a win rate. Guard: the budget of summary/09 is exact; balance by reworking cards.
9. **A crash shipped**: removed cards were still used by the code, and the only test loaded the page without playing.
   Why: Claude counted "it builds and the page loads" as "it works". Guard: after removing cards, `find.py` every name;
   `node tools/playtest.js` plays games and every scenario in a browser; run it before saying it works.
10. **Invented words** ("break" for dies) **and rule words without hover** (wind written without [[Wind]]). Guard: only
   the game's words; every rule word on a card links to its hover.
11. **Design not shown in the game**: champions were marked only in the design files. Guard: what the design marks,
   the game shows.
12. **Spells piled at cost 1-2, units at 3-4.** Guard: section 2, the spell/unit share at every cost.
13. **Answers that deflect.** "Because I did X" is not a reason. When Kaptain asks why something failed, say why Claude
   did X and what Claude can't do, plainly.
14. **Rules in docs get skipped** (factions/5 step 1 was written and still skipped). Guard: whatever must happen is a
   check in `tools/design_gate.py`, and the pre-commit hook enforces it. Never commit with `--no-verify`.
