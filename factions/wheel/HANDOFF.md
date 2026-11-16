# Handover: design the 20 factions again
One file for the next chat. Read it whole first, then CLAUDE.md's rules. Part 1 is how the library's numbers are made;
Part 2 is the work, in order; Part 3 is what Kaptain decided and what was learned: never undo it. Clone with the library
(`git sparse-checkout disable`).

## Rules for this work (Kaptain)
- **No card reading to judge links or combos.** The database already holds what every card does; scripts query it.
  Reading is only for a faction's tools and ways to play: at most 100 cards per faction, the key cards of the closest
  real factions' ways, logged in `factions/read-cards.tsv` (never read a card listed there again). A text that shows the database or the
  links wrong gets them fixed, with test cases (START_DESIGN-3).
- Before any agent runs: say how many, the cost (about 110k tokens each) and wait for Kaptain's OK.
- Plan first, in plain words with one example; build only after "go". One question at a time.
- Docs are written cleanly, as if things had always been this way: no history, no "formerly", no archaeology.

## Part 1. The numbers the wheel uses (library/cards_db)
- `links.sqlite` is in git zipped: unzip it first in every new chat, `gunzip -kf links.sqlite.gz`. Rebuild it only after
  `network.py` or `cards.sqlite` changed: `PYTHONHASHSEED=0 python3 links.py` (about 7 minutes: tell Kaptain and wait for
  his OK); it ends with cases/links.tsv and the sides check (START_DATABASE.md, check D) and writes links.sqlite.gz.
- Radius keys are not plain words: look up each one's name before talking about it (`python3 -c "import axes; [print(s[0], s[3]) for s in axes.SPOKES]"`).
  `many` is "many at once", `wide` is "many cheap units", `back` is "brings back".
- A link joins two cards of one game when a rule in `network.py` matches an effect of card A with an effect of card B. It
  keeps what of each card made it (`a_ab`, `b_ab`): an effect row, an ability, a keyword, a concept read from the whole
  card, the card by what it is, or the game's rules.
- The wheel's count (`mechanics_wheel.py links`, `links --radii`; the count itself is `axes.radius_links`) counts a link
  for two mechanics or radii only through what of each card made it. Example: Ghost Rider brings a card back and
  Vibro-Shock Gauntlets give +2 Power to it: revive with the +2 Power, never revive with supply, though the Gauntlets also
  give Energy. Per pair it writes:
  - `cards`: how much more often than chance (1 = chance; chance is counted through what made the links too);
  - `decks`: how much more real decks heavy in one hold the other (1 = as usual);
  - both worked out in each game alone and averaged, so each game counts the same, whatever its size;
  - `links`: the linked card pairs made by the two; `level`: that count growing slowly (0 links = 0, 1 = 1, 10 = 2, 100+ = 3).
- Joined: mechanics by `level` 1+ (any link) or `decks` 1.5+; radii by `cards` 1.2+ or `decks` 1.5+.
- Cases: cases/wheel.tsv (run at the end of `mechanics_wheel.py links`).
- A mechanic pair you expect to work together shows 0 links: check that one pair by script (what made each of the links
  between their cards) before trusting it; a wrong source is fixed for every card, with cases. Never read cards for it.

## Part 2. Design the 20 factions again
Steps of `factions/START_DESIGN-1-wheel.md`. Done: 1 (radii), 2 (`wheel/radius_links.tsv`), 3 (the 20 shapes,
`work/shapes.tsv`, agreed by Kaptain), 4 (the 53 mechanics, Stop A), and the numbers of step 6 (`wheel/links.tsv`).
Next:
5. Each faction's mechanics, by script (`work/signatures.py --write`, `work/borrow.py --write`, `check_assign.py`), for
   the new shapes. First make the scripts follow every rule of step 5, including: every mechanic is a signature or an
   extra of at least one faction, and a faction's mechanics fit the archetypes it carries (`shapes.py` prints them).
   Show Kaptain the plan for the script change before building it.
6. Links between mechanics: `wheel/links.tsv`; `apart.py` for the pairs real factions keep apart.
7. Theme, then tools (`START_DESIGN-1-wheel.md` step 7): new for all 20. `tools/wheel_table_check.py` and
   `work/make_stop1.py` read `themes.tsv` and `tools.tsv` (they fail until step 7 writes them).
8. Combos on this board, from the tools: all 190 pairs. Agents, Kaptain's OK first.
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
- Damage over time and my units changing form are possibilities for cards, not mechanics or archetypes.
- Every game counts the same in every number, whatever its size: a game's share, never its card count.
- Shapes come from real factions (step 3), so a game with no factions (Marvel Snap) gives no shape; its cards still
  count in every number and in the mechanics.
- Archetypes (`archetypes.tsv`): each carried by 2-3 shapes, each shape carries at most 2, so factions are varied.
- "One chosen" target is the default for every faction, in no shape.
- Every mechanic of the list is a signature or an extra of at least one faction.
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
- A pairing rare in the ten games can be splendid on this board: mechanics join by any link (`level` 1+). Radii have
  links enough for the chance number, so they join by `cards` 1.2+ (Part 1).
- Draw on a kill is allowed: killing an enemy is something the player makes happen (START_DESIGN-2).
- "This round" effects that set up another effect of the same round are chains and wanted (START_DESIGN-3).
- Reading cards for a faction: at most 100 (steps 6 and 7 together), logged in `factions/read-cards.tsv`, never read
  twice; a text that shows the database or links wrong gets them fixed with tests. `ask.py ways` shows what each key
  card does, so fewer cards need reading.
- The check script fails on words that break the game's rules ("move first", "strikes first", "placed at round end").
- Earlier chats wasted tokens on readers and on running everything in one long chat: keep chats short, scripts first.
- STOP1.md and STOP1-1..5.md are rewritten at step 9.
