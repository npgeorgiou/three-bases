# Handover: fix the links, then design the 20 factions again (written 15 Nov 2026)
One file for the next chat. Read it whole first, then CLAUDE.md's rules. Do Part 1, then Part 2, in order. Part 3 is
what Kaptain decided and what was learned: never undo it. Clone with the library (`git sparse-checkout disable`).

## Rules for this work (Kaptain)
- **No card reading to judge links or combos.** The database already holds what every card does; scripts query it.
  Reading is only for a faction's tools and ways to play: at most 100 cards per faction, the key cards of the closest
  real factions' ways, logged in `factions/read-cards.tsv` (never read a card listed there again). A text that shows the database or the
  links wrong gets them fixed, with test cases (START_DESIGN-3).
- Before any agent runs: say how many, the cost (about 110k tokens each) and wait for Kaptain's OK.
- Plan first, in plain words with one example; build only after "go". One question at a time.
- Docs are written cleanly, as if things had always been this way: no history, no "formerly", no archaeology.

## Part 1. Fix the links (library/cards_db)
Read first: `library/cards_db/START_DATABASE.md` Part 1 (rules for changing the database), `LINE_RULES.md` only if a line
itself must change (it must not here).

### The problem, with real cards
A link joins two cards of one game when a rule in `network.py` matches an effect of card A with an effect of card B.
The link is stored as (game, a, b, phrase, weight, site); it does NOT store which effect of each card made it. The wheel
(`mechanics_wheel.py links` and `--radii`) then takes all cards of mechanic A and all cards of mechanic B (by their
concepts) and counts every link between them. A card has many effects, so links made by OTHER effects are counted:
- Marvel Snap: Ghost Rider ("Bring back one of your discarded cards to this location") x Vibro-Shock Gauntlets ("+2 Power
  to your highest card here. +1 Energy next turn"). Link: "puts your units there, and Gauntlets act on units in its
  lane". It was made by the +2 Power, but it was counted as "comes back + extra supply", because the Gauntlets also
  give Energy.
- Slay the Spire: Ritual Dagger ("Deal 15 damage; if it kills, grows") x Nunchaku ("every 10 Attacks, gain 1 energy").
  Link: "is an Attack it needs played for its count". Counted as "gains when it kills + supply"; it has nothing to do
  with killing.
- Monster Train: Mine Collapse x Kindle: "more energy: a bigger X". Counted as "kill + supply".
So the database is right; the count gives links to the wrong mechanics. Earlier chats then had agents read card pairs to
throw such pairs out (that reading is now forbidden), and the readers looked as if they disagreed with the database: they
answered "is this a strong combo?", the database answers "can A set off B?". Both were right, to different questions.
Tested: the link's kind does not tell real from false (`factions/wheel/work/kind_test.py`: KEEP and DROP pairs both
~95% "combo" kinds; correlation with the readers' rate 0.09). Only storing the effect fixes it.

### The fix
1. Every link also stores the ability of A and the ability of B that made it (`ability.id`; each ability's rows in
   `flat_do` / `flat_if` carry `concept`, so the wheel can tell which mechanic made the link). Where a rule uses no
   ability (a printed keyword, a type, a stat, a game rule), store that instead (keyword id, 'type', 'rule'), never NULL
   without a reason.
2. Where: links are drawn by 68 rules in `network.py` (3,284 lines); `Out.append` already notes each rule's code line in
   `SITE`. Each rule must pass its two effects on. The 6 biggest rules make about 70% of the links; do them first and
   show Kaptain (sites by link count, 15 Nov 2026: line 737 = 128k links ("A makes it happen, B reacts or needs it",
   with 732 and 736 next to it), 1954 = 41k, 789 = 23k, 1628 = 20k, 1619 = 14k, 2243 = 12k; site 0 = 32k links with no
   site: find why). Line numbers move when the file changes: find them by `SITE`.
3. `links.py` writes the new columns into links.sqlite (table link: add `a_ab`, `b_ab`; same rows as now).
4. Proof nothing else changed: dump every link before and after (`dump_lines.py`; the "before" from the code just
   before the change) and compare by script: the same pairs, phrases and weights. Only the new columns may differ.
5. Many test cases (Kaptain: "important, add many"), in `cases/links.tsv` with new columns for the expected ability or
   concept on each side: Ghost Rider x Gauntlets (A: revive, B: the +2 Power, never energy); Ritual Dagger x Nunchaku
   (A: is an Attack, never kill); Mine Collapse x Kindle (never kill); at least one case per rule changed (about 70),
   one per game, and one per similar error found. `links.py` runs the cases at the end.
6. Known before this work: lk96 (Monster Train, Vinemother -> Wyldenten) already fails; leave it.
Costs: `links.py` about 4 minutes; `check_all.py` 7 (start in background mode, START_DATABASE rule 4).

### Where Part 1 stands (16 Nov 2026)
- Done: every rule. All 374,236 links have both sources; links, phrases and weights are unchanged (proof below).
  a_ab/b_ab hold an effect row `ability.seq` where the rule knows it (Gauntlets' +2 Power and +1 Energy are one ability),
  else the ability, `kw<id>`, `c:<concept>` (a concept read from the whole card: cheat_death, x_cost), `type` (the card
  only by what it is), `rule`. Rules that append after a cleanup rebuilt the pair's list use `note()`; a reason joined from
  two lines takes the sources of both (links.py `src_by`).
- Cases lk145-lk390 (`a_side`, `b_side`: a concept that must be there, `!concept` that must not): the three examples and
  one per rule and game. All pass; lk96 fixed too (a free made card counts as more cards to play; cases lk391-lk394).
- Proof: build before and after with the same `PYTHONHASHSEED=0`, then `python3 factions/wheel/work/links_same.py before after`.
  Without a fixed seed two builds of the same code differ in ~460 links (which reason a pair keeps follows Python's set order).
- Site 0 (32k links): the rule notes the sentence before the card names are filled in and before move reasons are joined;
  links.py looks up the final sentence. Sources are carried over; the site column is left as it was.
- Next: the wheel's count below.

### Then the wheel's count
`library/cards_db/mechanics_wheel.py` (`links`, `links --radii`, `measure`): a link counts for mechanic X only when its
A-side (or B-side) ability has one of X's concepts (`mechanics.tsv` column 3; radii: `axes.SPOKES`). A test case for each
example above (the pair must not count). Then the docs (Part 2 step 0).

## Part 2. Design the 20 factions again
Steps of `factions/START_DESIGN-1-wheel.md`. What stays and what is redone:
0. Docs first, cleanly: `START_DESIGN-1-wheel.md` (steps 2 and 6 = numbers only), `PIPELINE.md`,
   `START_DESIGN-4-asking.md`, `library/README.md`, START_DATABASE's links part (the new columns). Remove the reading
   files no step uses any more (`work/radius_verdicts.tsv`, `work/mechanic_pair_verdicts.tsv`, the reading prompts); the check
   script no longer uses them.
1. Radii: STAY (shares of cards, no links).
2. Radii that work together: REDO, numbers only (`mechanics_wheel.py links --radii`).
3. The 20 shapes: re-check every join with the new numbers (`tools/wheel_table_check.py`); change only shapes whose
   join falls away (`axes.py --near` for the check against real factions).
4. Mechanics list: STAYS (Kaptain agreed it at Stop A: `STOPA.md`, `mechanics.tsv`, 53 mechanics).
5. Each faction's mechanics: REDO by script (`work/signatures.py --write`, `work/borrow.py --write`, `check_assign.py`).
6. Links between mechanics: numbers only (`mechanics_wheel.py links`).
7. Theme, then tools (`START_DESIGN-1-wheel.md` step 7): new for all 20, the step changed. `tools/wheel_table_check.py`
   and `work/make_stop1.py` already read `themes.tsv` and `tools.tsv` (they fail until step 7 writes them).
8. Combos on this board, from the tools: all 190 pairs, since every faction's tools are new. Agents, Kaptain's OK first.
9. Seven answers from the tools, check script, Stop 1 pages (`work/make_stop1.py`). Then Stop 1 with Kaptain.

## Part 3. What Kaptain decided and what was learned (never lose)
- The game's own things (agreed): dots and front cells, rows (front/middle/back), columns, 3 lanes, the 3x3 camp,
  shapes and size, supply per lane, carry-over, round start and round end, one action per turn, moving and turning,
  reach (melee, Pike, Ranged), strikes and fixed damage, the hand and the discard pile, Immobile. Not in the game:
  player health, answers on the enemy's turn, supply that grows by itself, unit types, who acts first (random in round
  1, then alternating), attacked units hitting back (only Riposte), placing at round end.
- The wheel is general; step 7 turns each faction's mechanics into these own things, from scratch. The old candidates
  (commit d4a3de0^, `factions/3-candidates/`, e.g. C17 Dot Brokers, C12 Monoliths) are read last, only to check no idea
  Kaptain liked is missing.
- An all-Immobile faction is allowed (the old rule against it is deleted).
- Each faction answers seven questions, one line each: how it wins, how it removes the front unit, how it MAINLY removes
  back-row units, how it MAINLY acts between lanes, how it holds a base, its best Place effect, its blind spot.
- Stop 1 pages: juicy and easy to read; one line per answer; one line per partner faction saying HOW the combo plays.
- Combos: judged once, on this board (step 8): STRONG / OK / WEAK / NONE / AGAINST. Partners = STRONG or OK; 10+ each.
  `combos.tsv` has a test column; playtests fill it and what doesn't work is dropped.
- Things that were missing and must stay in: G = grows when hurt + I damage my own units; steal; kill spells; placing
  units in the enemy camp; bringing back without an Egg. Only one Egg in the whole wheel: look-alikes are compared by
  what the card does, not by mechanic name. "Strike first" is not a mechanic. "Ping" is a library word: say "small hits".
- A faction is built from 2-4 tools that feed each other, each from one of its mechanics, played out cell by cell
  (`START_DESIGN-1-wheel.md` step 7). The tools are the backbone, not all 100 cards: 3-5 ways to play are built around
  them, as many as the closest real factions show (START_DESIGN.md step 6). One idea is never the whole faction.
- The theme is picked in the wheel chat after step 6, before the tools, for the faction's mechanics; a tool that
  fits the theme but grows from no mechanic is dropped.
- Leaders: 5 per faction, the only cards with a golden border, spread over the costs and the ways to play; their
  special part works by whether I hold the lane's base, helps take and keep a lane, never wins harder in a won lane;
  nine kinds, mixed in each faction (START_DESIGN-2, "What a faction has").
- Countdowns ("at 3 counters...") very sparingly. A lane never holds more than 12 supply (summary/05).
- Draw on a kill is allowed: killing an enemy is something the player makes happen (START_DESIGN-2).
- "This round" effects that set up another effect of the same round are chains and wanted (START_DESIGN-3).
- Reading cards for a faction: at most 100 (steps 6 and 7 together), logged in `factions/read-cards.tsv`, never read
  twice; a text that shows the database or links wrong gets them fixed with tests. `ask.py ways` shows what each key
  card does, so fewer cards need reading.
- The check script fails on words that break the game's rules ("move first", "strikes first", "placed at round end").
- Earlier chats wasted tokens on readers and on running everything in one long chat: keep chats short, scripts first.
- Where the work stood: steps 1-9 were done once on the old counts (STOP1.md and STOP1-1..5.md exist, check passes);
  they will be replaced by Part 2.
