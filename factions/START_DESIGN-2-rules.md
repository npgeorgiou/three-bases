# Start design, part 2: setup, this game, the design rules
Part of `factions/START_DESIGN.md` (read that first, whole; then this file and parts 3 and 4, whole).

## 0. Setup
- Clone with the library (CLAUDE.md "Start of a chat", then `git sparse-checkout disable`). Library commands run from
  `library/cards_db/`; `cards.sqlite` is committed and current.
- Design files are committed to main and pushed (the project's rule); Kaptain reads them on GitHub. Only built HTML
  files are sent to him as downloads.

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
If summary/ and the code disagree, the code wins: tell Kaptain.

**1b. What the rules mean for card design** (check every card and deck against this list):
- Supply comes only from your units in that lane (each unit gives its supply each round), plus carry-over (at most 5,
  start 4). A lane with no units has no income. Killing an enemy unit also cuts its lane's income. A spell is paid from
  the lane it is cast in, then carry-over. A lane never holds more than 12 supply (summary/05).
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
  attack costs is allowed (the throw of the removed Ogre Thrower). Counters and timers ("at 3 counters...") very sparingly. Round-end abilities,
  Place effects, Death effects, reactions and position bonuses are wanted.
- Place fires every time a unit enters the grid: from hand, defecting, resurrected, returning, a token.
- What does NOT exist here, so never copy it from other games: hitting the enemy player or hero, instant-speed answers
  on the opponent's turn, mana that grows each turn, unit types/tribes (no "Elf", "Knight"; use card names or keywords),
  graveyards other than the discard pile, attacking another lane.
- High-level plans (axes, archetypes, ways to play) follow the board too (Kaptain, 5 Nov 2026): players act now; round
  end is something they build FOR, never a style of waiting for it. Every faction must win 2 of 3 lanes, so "stays in one
  lane / spreads over lanes" is no style. Read section 1a before suggesting any axis.
- A rule not written in summary/ and not in the code does not exist. A card that needs one is marked NEW RULE.

## 2. The design rules (agreed with Kaptain)
More text: `summary/09-card-design-rules.txt`
(costing). Ideas to use: `factions/4-kaptains-ideas.txt`, `factions/7-ideas-kept-for-later.txt`. Never reintroduce:
`factions/8-rejected-and-cut.txt`. Removed factions and drafts (`factions/removed/`) are never reused.

**What a faction has**
- Exactly 100 cards (tokens not counted). Spells are 20-50% of them, and about the same share at every cost from 1 to 5:
  if 30% of the faction is spells, then about 30% of the cost-2 cards are spells too. Cost 6+ may be mostly units.
- 2-3 keywords of its own. A keyword serves a mechanic: Barrage serves "guns in the back rows bombard the rear".
- 5 Leaders (`leader: true`; they are the only cards with a golden border). Each has a special part that works by
  whether I hold its lane's base. It helps me take a lane I don't hold and keep one I hold; it never just makes me
  stronger in a lane already won. The five are spread over the faction's ways to play, and their costs follow its
  playstyle and curve: one faction may have mostly cheap and middle Leaders, another middle and expensive ones; never
  one per cost by rule. Each is a focus for designing cards: cheaper cards make what it needs. A faction's five mix these
  kinds (variety is wanted):
  1. Two sides: helps take while the enemy holds the lane; only defends while I hold it.
  2. On the change: acts once when I take the base and once when I lose it.
  3. Helps the next lane: while I hold this lane, the bonus goes to my units in the other lanes.
  4. Answers only: while I hold the lane, acts only when the enemy tries to take it back.
  5. Keeping costs: while I hold the lane, a strong effect that I pay for each round (carry-over, a card).
  6. Behind in the game: while the enemy holds this lane's base and one more, stronger here.
  7. Takes, then leaves: when I take the base, it goes back to hand or to another lane.
  8. A rule for both: while I hold the lane, a rule there changes for both players.
  9. Any unit of mine: while I hold this lane's base, its bonus works for every unit of mine here, so it helps the
     partner faction too.
  Example (kind 1): "While the enemy holds this lane's base, the unit facing me is marked. While I hold it, enemies
  placed facing me arrive marked."
- The two things every faction can do alone: hold dots (units with enough defence for the front row) and remove enemies
  (its own way, step 2.2). Extra supply and extra draw are strengths a faction may have or lack (Kaptain, 5 Nov 2026):
  placed units already give supply and every player draws 2 cards a round.
- Draw, when a faction has it: a plain "draw 1", or a condition the player makes happen with the faction's cards ("Place:
  if an ally died this round, draw 1"; "the first time each round I kill an enemy, draw 1"). Never a condition only the enemy decides (the
  enemy casting a spell, the enemy passing). Only on effects that happen once per card (a spell,
  Place, its own death) or once per round; never "whenever an ally dies, draw".
- At least 1 card that acts between lanes: moves a unit to another lane, throws something there, or uses one lane's
  supply in another. Spells paid in one lane and cast in another are extremely rare; cast in all lanes, very rare.
- Back rows: melee units in rows 2-3 reach nothing (1b), so the faction needs cards that work from there. Example: a gun
  with Barrage 1 in row 3 hits the enemy furthest back at each round end.
- Lane control: some cards check "while you hold this lane's base", some "while you don't", some do one thing in each
  case. Never a bonus from one specific base (bases are random each game).
- Almost every card has a keyword or text; almost none is only stats.
- Hooks for two-faction decks (decks will mix 2 factions later): the combos planned on the wheel with other factions,
  and more (Kaptain, 9 Nov 2026: hooks made only from planned overlaps are poor; what else goes in is worked out in the
  wheel chat); also a few effects that work with any faction's units.
  Example: a Spare Part winds any unit that has a round-end effect, not only Horologers.

**How cards fit together**
- Every card says what it makes happen and what it needs (its `net` line), and each "needs" has a card in the faction
  that makes it. Example: Toll Warrior needs units to die this round; Willing Victim (dies when offered) makes it.
- Cards that cash something in have 3+ cards that set it up; cards that set something up feed 2+ cards that cash it in.
- Tools (the wheel's step 7): 2-4 new kinds of things or rules, each from one mechanic of the group, feeding each
  other; many cards carry them, the rest of the faction's cards build the ways to play around them.
- The group (the wheel's step 6): 2 pillars only this faction builds on, and 2-4 other concepts, each in at most 3
  factions; its mechanics are the links between them, each on several cards. The faction's list (every usable concept
  and helper, strongest links to the group first) is used A LOT, by most cards: a concept from it makes the group's
  concepts possible, starts them or makes them stronger (Kaptain). Example (Claude's): a faction built on units dying
  has units that come back, so more units can die. The list is not tracked on the wheel; without it cards are poorly
  designed.
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
