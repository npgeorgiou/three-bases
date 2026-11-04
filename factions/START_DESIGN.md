# Start here: faction and card design

For every chat that designs factions, cards, mechanics, combos or decks for Three Bases. Read this file whole first.
It says what to read, in which order, how to think, and the limits every design must respect.

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
9. **Cards, 20 at a time**, in the template below, each with its net line, its library card, the costing check (the
   budget of summary/09 exactly) and the frequency check. After each 20: the twin check by effect (NEVER DO, 2).
10. **Checks**: sections 2-5, the network check, the Benchmark report, then play the faction in a browser. Code only
   after Kaptain agreed the cards.

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
   pass to a judgement it must make. Guard: twin check by trigger + effect + target; one combination on more than 2-3
   cards fails. A passed check never means a finished design.
3. **700 cards in one chat.** Why: Claude tries to deliver everything asked; when the amount is too big, it lowers the
   quality silently instead of saying so. Its quality drops with volume and with chat length: rules read at the start
   (the budget) fade later. Guard: one faction per chat, 20 cards per batch. If a request is too big to do well, say so
   before starting.
4. **The library was not used card by card**, although `factions/5` step 1 already said "read 30-50 cards". Why:
   reading cards is slow and shows no output, so Claude skipped it to produce cards sooner and took only mechanic names.
   It also used almost only Runeterra, the game it knows best. Guard: step 7, all 8 games; every card names its
   library card.
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
   play a game and every scenario in a browser before saying it works.
10. **Invented words** ("break" for dies) **and rule words without hover** (wind written without [[Wind]]). Guard: only
   the game's words; every rule word on a card links to its hover.
11. **Design not shown in the game**: champions were marked only in the design files. Guard: what the design marks,
   the game shows.
12. **Spells piled at cost 1-2, units at 3-4.** Guard: section 2, the spell/unit share at every cost.
13. **Answers that deflect.** "Because I did X" is not a reason. When Kaptain asks why something failed, say why Claude
   did X and what Claude can't do, plainly.

## 0. Setup
- Clone with the library (CLAUDE.md "Start of a chat", then `git sparse-checkout disable`). Library commands run from
  `library/cards_db/`; `cards.sqlite` is committed and current.
- Push only what Kaptain asks to be pushed. Design work (new factions, card lists) is given to him as files to read
  unless he says to commit it.

## 1. Know THIS game before designing anything (the most important step)
Cards copied from other games that do not work on this board are the most common failure. Before suggesting any card,
read the rules and be able to answer the questions in 1b without looking.

**1a. Where the rules are.** The authority is the game itself: `three-bases-game.html`, built from `src/game/`. Never read
the built HTML; when a rule is unclear, look it up in `src/game/js/rules/` (map in CLAUDE.md) or with
`python3 tools/find.py where <identifier>`. The written rules are in summary/ (the game as it is now):
- `summary/03-board-and-bases.txt`: lanes, camps, dots, bases.
- `summary/04-winning.txt`: how a game is won and lost.
- `summary/05-rounds-turns-supply.txt`: rounds, turns, supply, draws, carry-over.
- `summary/06-units-general.txt`: shapes, stats, reach, strikes, what units may not have.
- `summary/07-areas-resolution.txt`: rows, columns, facing, order of effects.
- `summary/08-rulings.txt`: how the existing keywords and cards resolve.
- `summary/09-card-design-rules.txt`: costing, the supply-to-stats budget, card text rules.
- `summary/10-keywords.txt` and `summary/11-factions.txt`: every keyword, its value, and which faction has it.
- `summary/11-faction-<name>.txt`: the three current factions (their identities are taken; don't copy them).
If summary/ and the code disagree, the code wins: tell Kaptain.

**1b. What the rules mean for card design** (check every card and deck against this list):
- Supply comes only from your units in that lane (each unit gives its supply each round), plus carry-over (at most 5,
  start 4). A lane with no units has no income. Killing an enemy unit also cuts its lane's income. A spell is paid from
  the lane it is cast in, then carry-over.
- A unit's supply is its cost to deploy AND to every move and every attack. A 6-supply unit costs 6 to move. Moving and
  attacking are two separate actions (two turns, two payments). Big units act rarely.
- Dots are only the 3 front-row cells of each camp. A unit in the facing enemy front cell cancels the dot. Back rows
  never hold dots. To win you hold 2 bases at the start AND the end of a round (earliest win: end of round 2).
- Each camp is 3x3 = 9 cells. Count the cells a deck's units fill in one lane: a 2x2 unit takes 4 cells and 2 of the 3
  front cells.
- Melee reach: only the cells around the unit; the two front rows touch across the base. A melee unit in row 2 or 3
  reaches nothing in the enemy camp (Pike: from row 2 only). Deeper enemy rows are reached only by Ranged, spells,
  abilities and fixed damage. An attack picks any enemy in reach (front units do not protect back units from a Ranged
  attack); strikes made by abilities and spells hit the nearest enemy in reach (`src/game/js/rules/combat.js`).
- No hits between lanes. Units change lane only by special moves (Outrider, throws).
- Alternating single actions: every card you play gives the enemy one action to answer before your next one. Front-row
  units die easily. A setup of two cards is dead if the first dies before the second arrives.
- Round end: both players pass in a row. Round-end effects happen when the enemy can no longer answer; carry-over is
  filled then.
- Hand: start 5, redraw up to 3, 2 draws per round (none in round 1), hand limit 10. Decks 30-40 cards, at most 3
  copies. A card is rarely in hand exactly when wanted; a combo of two named cards is rare.
- Units have no active abilities you press (summary/06). An action that replaces the unit's attack and costs what an
  attack costs is allowed (the Ogre Thrower's throw). No counters or timers ("at 3 counters..."). Round-end abilities,
  Place effects, Death effects, reactions and position bonuses are wanted.
- Place fires every time a unit enters the grid: from hand, defecting, resurrected, returning, a token.
- What does NOT exist here, so never copy it from other games: hitting the enemy player or hero, instant-speed answers
  on the opponent's turn, mana that grows each turn, unit types/tribes (no "Elf", "Knight"; use card names or keywords),
  graveyards other than the discard pile, attacking another lane.
- A rule not written in summary/ and not in the code does not exist. A card that needs one is marked NEW RULE.

## 2. The design rules (agreed with Kaptain)
Full text: `factions/5-card-design-method.txt` (method), `factions/6-faction-entry-format.txt` (how a faction is written),
`summary/09-card-design-rules.txt` (costing). The ideas to draw from: `factions/4-kaptains-ideas.txt` (Kaptain's ideas;
use them), `factions/7-ideas-kept-for-later.txt`, and `factions/8-rejected-and-cut.txt` (never reintroduce these).
Candidates (raw brainstorming, not designs): `factions/3-candidates/`.
- Identity first: who they are, with the depth of Kaptain's Tagma text (`3-candidates/E1-tagma.txt`), and how they win.
  Every mechanic serves the identity. A library way found elsewhere is not a reason to use it.
- About 4-6 signature mechanics (section 2b; mechanics, not keywords: keywords only serve mechanics), and 2-3 characteristic keywords of its own.
- A web of cards that set things up and cards that cash them in: each cash-in card has 3+ cards that set it up, each
  setup card feeds 2+ cash-in cards. Give each card a "needs / makes" line so the web can be checked.
- Signature mechanics (copying, deck search, draw, card creation, forced movement, supply play, resurrection, bonds,
  stealing...) belong to 1, at most 2 factions; elsewhere only on a very few cards, in that faction's own character.
  The 2-3 monopolies of each faction (THE THINKING PROCESS, step 3) belong to that faction alone (Kaptain, 4 Nov 2026).
- Self-sufficiency: every faction alone can hold dots, remove enemies, get supply (plain Supply +1 units are fine), and
  draw (at least 1 draw card, tied to its signature).
- Draw is simple: a plain "draw X", or a condition tied to the faction's mechanics. Never a hard condition such as an
  enemy's death (Kaptain, 4 Nov 2026).
- Draw is rare and bounded: only on effects that fire once per card (spell, Place, own death) or once per round. Never
  on repeated events ("whenever an ally dies, draw").
- Between lanes: every faction has at least 1 card that acts between lanes, fitting the faction (moving units, throws,
  supply used across lanes, a building that reacts to another lane...). Spells paid in one lane and cast in another are
  EXTREMELY rare; paid in one lane and cast in ALL lanes, very rare.
- Back rows: each faction has a real job for rows 2-3 (see 1b: melee there reaches nothing).
- Staying power and removal follow the identity, never zero.
- Spells 20-50% of the cards, and about that share at EVERY cost from 1 to 5 (cost 6+ may be mostly units; Kaptain,
  4 Nov 2026). Exactly 100 cards per faction, no more, no less (Kaptain, 4 Nov 2026).
- Removal: each faction removes threats in its own way (THE THINKING PROCESS, step 2.2), never a plain "kill a unit"
  card shared by all.
- Lane control: cards that check "as long as you hold this lane's base", "if you don't", or both. Never a specific
  base bonus.
- Almost no card without a keyword or text: loads of passives, triggers, Death and Place effects (Kaptain, 4 Nov 2026).
  Every card has its place in the faction's mechanics and is a real decision (when, where, why).
- Each faction has 2-3 characteristic keywords of its own (Kaptain, 4 Nov 2026).
- The 100 cards form a few cohesive, obvious groups (ways to play), and the groups mix with each other within the
  faction. The 5 special units (champions) each have their place in this mesh: each anchors a group and links it to
  another (Kaptain, 4 Nov 2026).
- Interaction with the enemy: high for playful/disruptive factions, lower for straightforward ones.
- Decks will mix 2 factions later: give each faction hooks others can use (e.g. Projectiles, Part 4).
- Unit SUPPLY +/- N to balance a unit is allowed but rare.
- Costing check on every card (summary/09); frequency check on every trigger (per card / per round / unbounded).
- Card text voice: "I / me / my" for the card itself (summary/09). Only mechanics are taken from other games, never
  names or wording.

Old drafts: `factions/designs/` (3 Nov 2026) was made before the chain below; never reuse it.

## 2b. Checks from Kaptain's critique of the five new factions (3 Nov 2026; sources in `factions/10-outside-design-guides.txt`)
Every one of these failed in the first five factions. Check each before sending.
- THE CHAIN (Kaptain, 4 Nov 2026): NAME + ICON -> THEME -> IDENTITY -> MECHANICS -> INTERACTIONS -> CARDS.
  - Theme: a real theme to draw from (World War I, Neolithic megaliths, 1920s gangs...), with 10+ characteristics: how
    they fight, live, trade, believe, what they fear and lack. A thin theme gives no mechanics.
  - Identity: ONE line saying how the faction plays and wins, as clear as Noxus ("aggressive, kills with strikes") or
    Shadow Isles ("death: kill spells, resurrection, Ephemerals"). Never jump from theme to mechanics without it;
    every mechanic serves it.
  - Mechanics: SEVERAL (about 4-6) signature things in play, each broad, all interacting. Shadow Isles: death, damage,
    sacrifice, destroy, Fearsome, Ephemeral; sacrifice and destroy make deaths, Ephemeral units attack and die,
    deaths feed the rest. Written in Kaptain's form "I do X -> I benefit from Y" ("I damage my own units -> I gain
    from damaged units"). Broad means dozens of cards make it AND dozens use it (measured: Shadow Isles' "units die"
    is made by 103 and used by 55 of 221 cards). Built on the game's basic things: units die, damage, supply and
    carry-over, cells, rows and the front row, dots, round end, cards in hand and discard pile, moves, spells cast.
  - Interactions: how cards play off each other inside and between mechanics (a trigger only 5 cards could use).
    Never call an interaction a mechanic, never call one unit's effect (a cannon fires) a mechanic, and never turn
    each trait of the theme into its own narrow rule. Buffs and stats alone are not mechanics.
  - No unit types or card kinds that split the deck (no "crew", no Yin/Yang).
  - The core must also work with OTHER factions' units (a part that joins any unit, any unit wound by carry-over), so
    two-faction decks work; the side ideas (bombs, gears) stay small groups.
- Stages, Kaptain checks each: (1) name, icon, theme, identity, mechanics, groups, strong/weak (several factions may be
  done together at this stage); (2) ~20 key cards of ONE faction with needs/makes lines, network check; (3) the rest.
- Mechanics feed each other (not only through a few example cards); write which mechanic feeds which, and run
  `tools/network_check.py`. About a third of the cards belong to two mechanics, so chains form. The faction is
  playable in 3+ different ways (its groups).
- Every effect must change something that would not happen anyway (all Clockwork units act at round end, so "when
  one acts, the touching ones act too" is empty).
- Only the game's own words (no "wall"); explain with card examples in full plain sentences, never condensed notes.
- Strong at / only a little / weak at: written in the entry; no card gives a faction what its weak list says (Dean of
  Battle Magic, melee buffs, on Arcanists). Factions contrast with each other and each has a few cards against the others.
- Conditions serve the identity: "the enemy with the least defence" only in a faction about hunting weak units.
- Twins: write each card's effect in a few words, sort, compare. Two cards with the same effect, or the same result
  (Spark of Yesterday and Twin Novice), at the same cost: change or cut one. Same for near-twins (Pioneer, Wayside Shrine).
- Rule-breaking keywords (Outrider, moving between lanes, anything that bends the board rules) sit on a few cards only.
- Worth on this board: "this round" penalties (-1 strength, can't attack) are worth almost nothing, the enemy just waits;
  "can't move" is near nothing, units rarely move. Prefer effects that last or act now.
- Costing: a drawback is paid for with more than the curve; Immobile's bonus is small (1:0|5 is too much defence);
  a card paid twice (Projectiles: placed, then thrown) is cheaper for it.
- Keywords on one card only with a reason (two Push keywords on Siegework: what on it uses Push?).
- Feasibility per deck: every need on every card has a maker in the same faction (a Sapper needs a way into the enemy
  camp). Do the needs/makes check for every deck made, and say which deck lines were checked.
- No flavour text on cards.

## 2c. Critique yourself before sending (lessons of the 3-4 Nov 2026 chat; Kaptain should never have to point these out)
- Compare with a real faction: run `analyze` on a real faction of the same kind (Noxus for aggro, Shadow Isles for
  death...) and count what its cards make and use. Your faction must be as broad and as dense: if a mechanic could
  not carry dozens of cards, it is an interaction.
- Can all 100 cards have a place? Before any card, estimate how many cards each mechanic gives (dozens each) and
  check that 100 fit without filler. Too complex to fill, or too narrow to fill: rework before sending.
- A mechanic that limits the player (an order to follow, a card kind, a position) must pay back big; otherwise nobody
  plays it.
- How does it actually happen? For every effect, say how it works with the game's existing rules (supply, hand,
  cells, round end). If it needs something the game doesn't have, mark it NEW RULE; never assume a mechanism ("a card
  in the enemy's hand gives him supply" — how?).
- The identity test: could the identity line describe another faction? Does every mechanic serve it? If you can't say
  in one line how the faction plays and wins, you have no identity yet.
- One critique, every faction: when Kaptain points out an error on one faction or card, find and fix the same error in
  all the others before he does.
- Network check tags must be specific: a generic tag ("supply", "damage") makes everything look connected.
- Kaptain's own ideas (Projectiles, Immobile faction, Mark, back-in-time) are a few cards or one mechanic inside a
  faction, never stretched into a whole faction.
- Before sending, go through every line of 2b and 2c and know which one each part of the design passes.

## 3. Search the library (wide, deep, curious)
How to ask: `library/cards_db/START_QUESTIONS.md` (commands, how to build an answer; read it whole). In short:
- Wide: `ask.py all list concepts`; per mechanic `compare`, `factions`, `fed`, `feeds`, `together`, `chains`, and `both`
  with every other mechanic. Read 5-10 card texts per way before trusting a count.
- Deep: analyse WHOLE factions, not only the few decks in `cases/decks.tsv` (they show a fraction of a faction's depth).
  A whole faction takes ~10 s and a short output:
  ```
  python3 -c "import sqlite3;c=sqlite3.connect('cards.sqlite');print(', '.join(r[0] for r in c.execute(\"select name from card where game=? and regions=? and is_keyword=0 and is_stub=0\",('duelyst','Lyonar Kingdoms'))))" > /tmp/f.txt
  python3 ask.py duelyst analyze "$(cat /tmp/f.txt)"
  ```
  Factions per game: `select game, regions, count(*) from card group by 1,2`. Positional and location games first
  (Duelyst, Faeria, Stormbound, Into the Breach, Inscryption), then all the other games: every search covers all 8.
- Measure a real faction's mechanics: `analyze` lists what its cards make happen and which cards use it, without
  counts; count the names on each line (made by / used by) to see which things carry the faction.
- Curious: at least three unexpected concepts that serve the same outcome; one game where the mechanic is rare or odd.
- Translate each way into Three Bases (section 1b) and say what had to change. Anything with no library source is
  marked as Claude's idea.

## 4. Think like a player (every card, every combo)
- Hand: is it in hand when needed (2 draws a round, 3 copies)?
- Board: which row and column, what does it reach from there, is that cell free then?
- Enemy: what does the enemy do with its next action? Does the setup survive it?
- Timing: during the round, at round end, what counts for the dots?
- Worth: better than a plain unit of the same cost in that spot? If not, drop it.
- A combo changes what the other card does or sets it off again; take either card away and the other loses its point.
  Show it as a played sequence: card, cell, what the enemy can do, result.

## 5. Before sending
The network check is part of the design, not an extra: run it on every faction and every deck to show the interactions are thick (setups per cash-in, cards in two families, needs with no maker). Tool: `python3 tools/network_check.py factions/designs/<faction>.txt` (MECHANIC, CARD and DECK lines; designs live in `factions/designs/`). Show its result; 0 problems before sending.
Partners (Kaptain, 4 Nov 2026): the network check counts each card's partners (cards that make what it needs or need what
it makes). A card with few partners is acceptable, but the 5 champions must have many and each must gather a distinct way
of playing around it; they must not be the only centres: the whole network must be dense. Mark champions with
"champion" in the card's net line.
Library (Kaptain, 4 Nov 2026): take inspiration from the library's existing combos and cards (never copy them); name the
library lead behind each mechanic and behind the champions.
Benchmark report (Kaptain, 4 Nov 2026): `node tools/cardstats.js <letter>` plays Benchmark games with the faction's premade
decks and reports per card how often it was played, how often its effects fired and the win rate when played; cards that
never matter are reworked or cut.
Rosters (Kaptain, 4 Nov 2026):
- The curve follows the supply: round 1 has 4 supply, round 2 at most 4 more, so cards of cost 1-4 must already set up and
  combine (good openings, real interactions); cost 4-6 is each way of playing's middle game; 6+ must do strong things.
- Expensive units build on what the cheaper ones set up: 6-10 supply has been spent in that lane before them, so their
  Place effect or passive uses that board (the allies there, the enemies set up, the deaths, spells or winds of the round),
  and their actions are worth their high cost. Never an average body with a generic ability.
- Place effects on 30-50% of the units and Death effects on 10-15%: immediate, one-time board impact that the player
  organised, not only constant effects.
- Each faction's entry rates its removal, disruption and protection: many / medium / few / very few; cards follow it.
- Cards that check "you hold this lane's base" get a golden border in the game (automatic).
Per mechanic: which commands ran; which parts have no library source. If the library's tables or queries could not
answer something the design needed (a missing link between cards, a missing query), say so to Kaptain. Every card passes 1b, the costing check and the
frequency check. Talk to Kaptain as CLAUDE.md says: short, plain, his words, one question at a time, last.
