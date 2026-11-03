# Start here: chats that import a game or change the card database

Read this file whole. Then read only what your task needs (the map below). Commands run from `library/cards_db/`.
Clone with the library: CLAUDE.md "Start of a chat", then `git sparse-checkout disable` (the library is ~120 MB).

## What the database is
Every card of 8 games (Runeterra, Stormbound, Monster Train, Duelyst, Faeria, Inscryption, Into the Breach, Slay the
Spire) described as rows: when it acts (event), if what (conditions), what it does (effects). Every value is from
`vocab.tsv`; equal mechanics of different games share one concept (`library/concept_tree.txt`). From the rows, network.py
draws **lines** between two cards of one game ("A makes B cheaper", "A sets off B"). Kaptain uses the lines and the
concepts to design factions for Three Bases. Wrong lines give wrong design answers, so lines must be right.

## How to talk to Kaptain
Short plain sentences, his words, a card example for every point, one question at a time (last, marked). Answer his
questions first and wait. Never invent rules or mechanics; mark suggestions as yours.

## The five rules most often broken (each cost Kaptain hours)
1. **Fix the cause, never the example.** Every error Kaptain finds is one sample of a family. Write the wrong thinking
   in one sentence, find every place it lives (all games, all rules, the readings, the questions), fix it once.
2. **Every fix gets test cases** (Kaptain, 31 Oct 2026): one `cases/network.tsv` row per point Kaptain made and per
   similar error you found, `line` or `none`, only for lines you checked against both card texts. A fix without cases
   comes back broken.
3. **Dump all lines before and after** (`dump_lines.py`), read EVERY gone and new reason group in every game.
4. **One rebuild per round**: `check_all.py <game>` loads all games once (about 25 minutes). Never `run.py` once per game.
   After a change to network.py only: `check_all.py --no-load` (about 3 minutes).
5. **Read cards like a player**: what does it need, who gives it that, what does it make, what does that card do.
6. **A check is done only when all its output was read.** Never sample less, skip a game or hand over because the output
   is long: split it into pieces (a reader reads its piece in one call: LINKS_PLAN.md "Token economy"). Say plainly what was not checked; never let a partial check look done.

## Rules every line must keep (network.py; each is a rule for every game)
- L1 A line comes from what a card's TEXT does, never from what every card does or is. Every card can be played, drawn,
  discarded, can attack and has Life: none of these makes a line (Chump Whump -> Get Excited!: no; any card can be
  discarded. "Whenever you play a card", After Image: no line from every card).
- L1b Kaptain 1 Nov 2026: a draw, a return to hand or a tutor by kind only ("draw a unit", "return a spell") makes no line: any
  card of that kind can be drawn. "Whenever you play a spell" or "the number of spells in your deck" makes no line where most
  of the game's cards are of that kind (Monster Train's Incant); a minority kind is a deck choice and keeps its line (Annie).
- L2 The game's rules are no combo, also not for a level-up. Kaptain: what every card can do counts for nothing
  (Living Shadow -> Zed, any unit -> Poppy, Jagged Butcher -> Gangplank, Ashe -> LeBlanc: no line). Only a card whose
  own text adds an attack (Rally, a free attack), a strike now, a second strike, or a keyword that does the need
  (Overwhelm and Elusive reach the Nexus for a card that needs it, deathtouch kills) makes the line.
- L3 A makes B, B acts on C: A gets NO line to C (Targonian Tellstones makes Blessing of Targon; only the Blessing helps
  Braum). A's own act of making does link to a card that waits for that making (Zed summons Ephemeral units: Moonlit
  Glenkeeper). Only a planted card that goes off by itself when drawn counts as the planter's act (Chimes for Bard).
- L4 A help must do the very thing needed. Power gets no unit past blockers (For Demacia! does not help Zed hit the
  Nexus) and adds no level-up damage (Tybaulk does not level Gwen). Health and protection do help "survive damage".
  "Another attack" is only Rally or a free attack.
- L5 Limits and drawbacks are no needs ("the first 3 times you draw", Janna; "lose 1 energy when drawn", Void).
- L6 A helper points at what it helps and never "needs" it (Strength -> Attacks; Focus -> Orbs).
- L7 Read who does it. "I've attacked" = the card itself; "I've seen you" = the player; "your General" = the General.
- L8 Costs as paid: "X" and "spend all your mana" are variable (card.cost_x). A made or summoned card has its own kind
  (Tail of the Dragon is a unit, not a landmark).
- L9 My effects feed my needs; an effect on enemies feeds needs about enemies. Lines link only cards a player can own.
- L10 Line words say what a player says: triggers (a reaction), enables (a count or a thing that must be there), makes
  stronger / cheaper, helps it level up, puts it into play, can aim at it. A cost that drops for each X: what does X
  "makes it cheaper" (Gambling Chip -> Eviscerate), never "enables". One reason is said once, by its strongest kind.
- L11 A plain hit on one target (Strike, Mystic Shot) feeds no "when an enemy dies"; poison, hits on all and kill effects do
  (damage boosts: L18).
- L12 Say who gets it: where the player is no card (Slay the Spire), a status on the player is "gives you Strength".
- L14 Kaptain 1 Nov 2026: help aimed at any card of a kind ("give an ally +2|+0", "heal a unit", "copy an ally", "a unit
  strikes", "when you summon an ally, grant it +1|+1") makes a line only to a card whose own text uses that help. Wuju Style ->
  Patched Porobot: no line. A faction or card kind ("a green creature", "a Demacia ally", "a follower") is no narrower than a
  deck. Kept: power and health as L18 says; a strike, attack or ready to a card with "Strike:"/"Attack:" or an activated
  ability; a copy as L19 says; a return to hand of a card with Play or Summon; a sacrifice of a card with Last Words; a cleanse
  to a card that puts that status on my side; help aimed near my leader to a card that acts near it (Roar -> Windblade Adept's
  Zeal); a keyword a card gives itself counts as its own; anything a card waits for, counts or levels from ("when healed",
  "allies with Barrier", "Level up: targeted"). The code: network.uses_help() / use_of(); a new game's keywords join it through
  their concept (vocab.tsv), never by name. A new kind of help gets its use written there, never a line to every card.
- L15 Kaptain 2 Nov 2026: what a keyword does to cards with the same keyword is the keyword's rule, no line (Pyke's Lurk grants
  Lurkers +1|+0: no line from one Lurker to another), unless the receiving card's own text uses it (Xerxa'Reth: "If I have 8+
  Power"; Gwen: "when another ally gains Power from Hallowed"). A card's own needs are its text and its reaction keywords (Revenge, Slay),
  never a keyword's inner working (Barrier pops when damaged, Challenger picks when attacking). "+1|+0" raises no Health.
- L16 A line said only as "can aim at it" is no reason. An act on a card (strike, return, copy, damage) links only with the
  card's own reason ("makes it attack or strike again: its own effect goes off").
- L17 Putting my units into play by kind (revive, summon from the deck or discard) links to cards whose "when I'm summoned" goes
  off (The Harrowing -> Captain Farron). A card that makes a card by description links to a card that counts such cards played
  (Ferros Financier manifests a 6+ cost spell: Jayce, Lux). A count of mana spent on a kind ("6+ mana of spells", Lux) is fed
  like a count of that kind played.
- L18 Kaptain 2 Nov 2026, more damage is generic: more power, Strength, Dexterity, Magic Power, Vulnerable, Wrath, Mantra or
  A.C.I.D. make NO line because a card hits, has Overwhelm, Elusive, Fearsome, Quick or Double Attack, Multistrike, hits several
  times (Twin Strike), or has "Strike:", "Nexus Strike:" or "Slay:". That is the game's goal (more damage is always good), not the
  card's text. Never bring back "after that it can hit for more power". A line stays only where the card's own text reads the
  damage or the stat: it deals damage by its power in a fight its text starts (Deepwood Stalker), needs one big strike (Vi: 10+
  damage), gets something back from the damage (Reaper, Lifesteal), doubles what is there (Burst -> Catalyst), reads its power
  ("double my Power", "grant it my stats"), or is a champion that levels up from Nexus damage and has Overwhelm or Elusive
  (Darius; Kaptain's checks n33, n34). More health links only to Taunt units and to cards that wait to survive damage. Stat
  help is said in three families, never with the numbers: "gives it more power", "gives it more health", "gives it more power
  and health" (Stormbound: "more strength"; less: "lowers its stats").
- L19 Kaptain 2 Nov 2026, copies: a copy put into hand or deck is one more card of any kind, generic, no line. A copy put into
  play links only to cards whose summon or death effect it sets off (Dawn and Dusk -> Vekauran Vagabond); a summoned copy is
  not played, so a Play effect does not count. "When you play a follower" (Beguiling Cobra) is any unit, generic (L1b).
- L20 A fight keyword (Elusive, Fearsome, Overwhelm, Quick Attack...) works for the card that has it: Nasus's Fearsome gets
  Nasus to the Nexus, not Abyssal Eye. A card made by name must be the kind the need asks ("when you summon an Elite": Emperor's
  Divide's Sand Soldiers are none). Giving Overwhelm or Elusive to a card whose text needs to hit the Nexus is a line ("helps
  it hit the enemy player").
- L21 Kaptain 2 Nov 2026, what most cards do is no deck choice: a filter that half the cards of the kind pass ("costs 2 or more",
  "a creature with higher Attack than Life", "summoned near your General") or a type that a fifth of its own kind has (Slay the
  Spire's Skill, Attack) is generic for a pick, tutor, repeat or boost (Secret Technique, Burst: no line); a count of a minority
  type stays (Kunai, Rage: "every Attack played", Kaptain 30 Oct 2026). A repeat or bigger effect for spells, landmarks or
  equipment stays only where they are a minority (Doctor Mia; not Monster Train's spells). Damage or kills that a quarter of the
  game's cards make by their own text feed no "whenever damage is dealt" trigger (Envenom, The Boot), unless it levels up or the
  doer is the enemy (Vek Hormones). Read wants right: "draw until you have 6" (Expertise) wants an empty hand; "if you have no
  Block" (Auto-Shields) wants none; "repeat Summon effects" (Transcendimp) is for cards with Summon.
- L22 Kaptain 2 Nov 2026, resources: what pays a card's cost is a line. A land changed to the colour a card needs pays its land
  cost (Faeria's Ring of Dominion: "turns a land into the colour it needs: helps pay its land cost, and can take that land from
  the enemy").
- L13 Per game settings: network.EXPENSIVE (the cost from which a card is expensive); a deck holds what the game gives
  every deck of its character (Slay the Spire's starting relic) unless a card replaces it; read the game's own limits of
  a mechanic (Dexterity adds only to Block a card gives when played).

## Rules for the data (readings)
- The card text is the truth; no rule from memory. A definition no source has is asked from Kaptain.
- The records in `read/<game>/` are the source; everything else is rebuilt from them. Fix readings by a rule script over
  the texts (`fixes/<game>/vNN.py`, safe to run twice), never card by card, never by a re-read unless no rule can.
- Every value is a `vocab.tsv` row. Reuse before adding; one meaning, one form (normalize.py). A new value gets a BRIEF.md
  line if readers need it. Never change a concept without Kaptain's OK.
- A game's own rules (how units fight, move, pay) are records in `read/<game>/game_rules.jsonl`, taken from the game's
  own sources (cited in `library/games/<game>.md`), never from memory.
- Import pitfalls seen before: the library's entries were not the game's cards (compare by code and text); one wiki page
  held several cards; one name, two cards (a champion and its level-up form: take cards by code); keywords hidden in
  prose; readers using another game's words; guide decks that are only core cards; full decks that exist only as deck
  codes. Look in the repo first (PROCESS.md step 0.3 lists every game's data).

## Map: where things are
| What | File |
|---|---|
| Steps of an import, in order | PROCESS.md (sections 0-5) |
| Reading rules and record shapes (what readers follow) | BRIEF.md, READER_PROMPT.md |
| Values and concepts | vocab.tsv, library/concept_tree.txt |
| Build: rows -> cards.sqlite | run.py (one game's full build), load.py, flat.py, refs.py |
| Lines between cards | network.py; what each part does: LINKS_PLAN.md "How lines are made"; why one line exists: pair.py |
| Decks | decks.tsv, cases/decks.tsv; pages network.html (network_page.py) |
| Per-game review records (needed by the build) | deck_read_<game>.md |
| Questions | ask.py, mechanics.py, connections.py, deck_analysis.py; START_QUESTIONS.md |
| The planned line table (next work) | LINKS_PLAN.md, QUESTION_BANK.md; links.py -> links.sqlite (not in git) |
| Each game's rules, terms, real-world cases | library/games/<game>.md |

## Every check and test, and when it runs
Scripts cost no tokens: running them is free. What costs tokens is reading their output and the card texts; readers
(background agents that write the records of a new game) cost the most. Each process below says what to run and what to read.

**A. Rebuild (`run.py <game>`, or `check_all.py <game>` for all games): a script, run after any change to records,
vocab or shared code.** It stops at the first failure:
1. normalize.py: one form for equal meanings, on every record.
2. check.py: every record uses allowed shapes and values (0 problems needed).
3. load.py: builds cards.sqlite for all 8 games (with flat.py, refs.py: the tables questions use).
4. cases/run.py: every test of the game must pass. The tests (`cases/`):
   mechanics.tsv (a mechanic's cards, found by regex in the texts, must be found by the query, 95%), combos.tsv (a guide's
   combo: the first card must set off the second), regions.tsv (a faction must show its known mechanic), decks.tsv (a
   guide deck's explanation must say the guide's phrases), network.tsv (a deck line that must exist, or must not: 294 rows).
5. pattern_check.py: words in a text that its record must show (open flags listed).
6. audit_text.py: words in a text that its rows miss ("or the enemy Nexus"); each fixed or explained.
7. audit_links.py: links that cannot exist (a need nothing makes, a keyword without concept); each fixed or explained.
8. status.py, examples.py: write STATUS.md and QUERIES.md.
9. review_check.py: each mistake family in deck_read_<game>.md has its cause, the same error elsewhere, and the fix.
Read: any FAILED line, and the audit lists. After a change to network.py only: `check_all.py --no-load` (steps 4 and 7).

**B. Importing a game (PROCESS.md, steps 0-5): Claude's work plus scripts.** In order:
1. Research the game and its decks; write its rules into `library/games/<game>.md` with sources (Claude reads pages).
2. Cards and keywords from the game's data (`supplement_<game>.py`, a script), reader input (`build_input.py`).
3. Readers write the records (agents, the costly part), then a second reading of 10% (`compare.py` lists differences;
   Claude judges each).
4. Process A, until it passes; proposals, word flags, stub names decided by Claude.
5. Deck networks: decks into decks.tsv; Claude reads at least 10 decks card by card; `deck_audit.py <game>` (process C).
6. `realworld.py <game>` (what guides say about the game's factions and combos; read every miss) and
   `design_questions.py` (read the new game's answers).
7. Done when PROCESS.md step 5 holds; Kaptain checks the deck pages (`network_page.py` makes network.html).

**C. Checking lines (after any change to lines, and whenever Kaptain says check):** scripts plus Claude reading. Keep
LINKS_PLAN.md "Token economy" (at most 100 cards per list, one game at a time, readers save findings as they go).
1. Before the change: `dump_lines.py /tmp/before.tsv`. After: `dump_lines.py /tmp/after.tsv` and
   `dump_lines.py --diff /tmp/before.tsv /tmp/after.tsv`. Read every gone and new reason group, in every game.
2. `deck_audit.py <game>` for each game whose lines changed (the deck check of LINKS_PLAN.md step 3). Read all of
   it, plus every level-up line of every deck against both texts.
3. Every error: fix by cause for every game, add network.tsv cases, rebuild (A), repeat 1-2.
4. `realworld.py` for all games: no case that held may break.
5. After a change to the deck pages: `network_page.py`, then load network.html in the browser (Playwright) with no errors.

**The game itself** (not the database) has its own: tools/build.py, tools/simtest.js, tools/smoke.js (CLAUDE.md).

## State (3 Nov 2026)
- All 8 games imported. Kaptain approved Runeterra and Into the Breach; Slay the Spire done; Inscryption reviewed;
  Stormbound, Monster Train, Faeria, Duelyst wait for his check of their deck networks.
- Cases: all pass except Stormbound csb09-csb13 (poisoned-unit combos, an old cause not yet traced) and Kaptain's ndu42, nfa27
  (they conflict with his 3 Nov rule that a unit moving itself gives no line: ask him). Must-not cases whose reason no deck
  says any more (rewrite them): Runeterra n56, Duelyst ndu23 ndu47, Inscryption n299, Into the Breach ntb15-17, Slay the
  Spire nst30 nst36.
- Real-world cases: 237 of 261 hold (Zealous Crusader -> Khalim's Prayer broke by the same 3 Nov rule).
- Lines (3 Nov 2026, pairs in links.sqlite): Runeterra 193,514; Faeria 10,424; Duelyst 13,476; Slay the Spire 9,238; Into the
  Breach 6,138; Monster Train 3,115; Stormbound 2,746; Inscryption 1,080.
- Known open: a card placed by its text near the leader (Conscript) draws no line to a card acting near the leader
  (Fealty); Adaptive Mutation's stat swap has no line; Monster Train has no full decks as text (ask Kaptain). Monster
  Train's Olde Magic is built by the player at an event: its text and record (read/monster_train/event_cards.jsonl) list the
  choices the wiki gives, with no numbers. Stormbound's Fort of Ebonrock has no ability (a plain structure).

## Open work, in Kaptain's order
1. Finish fixing the verified causes of Runeterra and of the old round (all 4 games): handover `audit/README.md`, done and
   not reached in `audit/fixlog.md`. Fixes are made in the main chat, never by an agent (Kaptain, 3 Nov 2026).
2. The line check (LINKS_PLAN.md step 3) of Slay the Spire, Faeria, Duelyst, then Stormbound, Monster Train, Inscryption, Into
   the Breach: a separate chat (Kaptain, 3 Nov 2026).

## When you finish
Commit and push every finished step. Update "State" and "Open work" above (keep them short: no history; git log has it).
