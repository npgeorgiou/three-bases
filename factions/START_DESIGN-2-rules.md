# Start design, part 2: setup, this game, the design rules
Part of `factions/START_DESIGN.md` (read that first, whole; then this file and parts 3 and 4, whole).

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
- `summary/11-faction-<name>.txt`: the seven factions in the game (their identities are taken; don't copy them).
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
  attack costs is allowed (the throw of the removed Ogre Thrower). No counters or timers ("at 3 counters..."). Round-end abilities,
  Place effects, Death effects, reactions and position bonuses are wanted.
- Place fires every time a unit enters the grid: from hand, defecting, resurrected, returning, a token.
- What does NOT exist here, so never copy it from other games: hitting the enemy player or hero, instant-speed answers
  on the opponent's turn, mana that grows each turn, unit types/tribes (no "Elf", "Knight"; use card names or keywords),
  graveyards other than the discard pile, attacking another lane.
- A rule not written in summary/ and not in the code does not exist. A card that needs one is marked NEW RULE.

## 2. The design rules (agreed with Kaptain)
More text: `factions/5-card-design-method.txt`, `factions/6-faction-entry-format.txt`, `summary/09-card-design-rules.txt`
(costing). Ideas to use: `factions/4-kaptains-ideas.txt`, `factions/7-ideas-kept-for-later.txt`. Never reintroduce:
`factions/8-rejected-and-cut.txt`. Old drafts in `factions/designs/` are never reused.

**What a faction has**
- Exactly 100 cards (tokens not counted). Spells are 20-50% of them, and about the same share at every cost from 1 to 5:
  if 30% of the faction is spells, then about 30% of the cost-2 cards are spells too. Cost 6+ may be mostly units.
- 2-3 keywords of its own. A keyword serves a mechanic: Barrage serves "guns in the back rows bombard the rear".
- 5 champions (`champion: true`). Each is the strongest reason to play one way, and is also used by a second way.
  Example: a champion that grows when allies die is the centre of the death way and also pays off the sacrifice way.
- The four things every faction can do alone: hold dots (units with enough defence for the front row), remove enemies
  (its own way, step 2.2), get supply (plain Supply 1 units are fine), and draw (at least 1 draw card).
- Draw: a plain "draw 1", or a condition from the faction's mechanics ("Place: if an ally died this round, draw 1").
  Never a condition the player can't arrange (an enemy's death). Only on effects that happen once per card (a spell,
  Place, its own death) or once per round; never "whenever an ally dies, draw".
- At least 1 card that acts between lanes: moves a unit to another lane, throws something there, or uses one lane's
  supply in another. Spells paid in one lane and cast in another are extremely rare; cast in all lanes, very rare.
- Back rows: melee units in rows 2-3 reach nothing (1b), so the faction needs cards that work from there. Example: a gun
  with Barrage 1 in row 3 hits the enemy furthest back at each round end.
- Lane control: some cards check "while you hold this lane's base", some "while you don't", some do one thing in each
  case. Never a bonus from one specific base (bases are random each game). These cards get a golden border.
- Almost every card has a keyword or text; almost none is only stats.
- Hooks for two-faction decks (decks will mix 2 factions later): a few effects that work with any faction's units.
  Example: a Spare Part winds any unit that has a round-end effect, not only Horologers.

**How cards fit together**
- Every card says what it makes happen and what it needs (its `net` line), and each "needs" has a card in the faction
  that makes it. Example: Toll Warrior needs units to die this round; Willing Victim (dies when offered) makes it.
- Cards that cash something in have 3+ cards that set it up; cards that set something up feed 2+ cards that cash it in.
- Monopolies (step 3) belong to this faction alone. Other strong mechanics (copying, deck search, draw, card creation,
  forced movement, resurrection, stealing) belong to 1, at most 2 factions; elsewhere on very few cards.
- How much it touches the enemy: a disruptive faction has many cards that act on enemy units (push, mark, punish); a
  straightforward one has fewer.

**The curve** (round 1 gives 4 supply, round 2 at most 4 more)
- Cost 1-4 cards must already work together: two cost-2 cards played in round 1 should do more together than apart.
- Cost 4-6 is the middle of each way to play.
- Cost 6+ cards use what the cheaper cards built in that lane: 6-10 supply has been spent there before them, so their
  Place effect or ability counts the allies there, the marked enemies, the deaths or spells of the round. Never an
  average body with a common ability.
- Place effects on 30-50% of the units and Death effects on 10-15%: they change the board at once, when the player chose.
- Each faction's entry rates its removal, disruption and protection as many / medium / few / very few; the cards follow it.

**Costing and wording**
- The budget of summary/09 exactly: strength + defence = budget(supply) - size - keyword values - text value (`tv`). A
  drawback gives a negative `tv`. Changing a unit's supply by 1 to balance it is allowed but rare.
- Costing check on every card (summary/09). Frequency check on every trigger: once per card (Place, own death, a spell),
  once per round (round end of one unit, "once per round"), or unbounded ("whenever an ally dies"). Card advantage and
  supply are never unbounded.
- Card text: "I / me / my" for the card itself. Only mechanics come from other games, never names or wording.
