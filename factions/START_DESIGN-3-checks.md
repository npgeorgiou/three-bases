# Start design, part 3: lessons, library, player view, before sending
Part of `factions/START_DESIGN.md` (read that first, whole; then parts 2, 3 and 4, whole).

## 2b. Lessons from Kaptain's critiques (3-4 Nov 2026; each one failed once; sources in `factions/10-outside-design-guides.txt`)
**The faction**
- A thin theme gives no cards. "Clockwork" alone gave only winding; the clock city's guilds, apprentices, spare parts,
  commissions and fear of rust each could have given a different kind of card.
- A mechanic is broad: in Runeterra, Shadow Isles' "units die" is made by 103 and used by 55 of its 221 cards. Measure a
  real faction of the same kind (`analyze`, section 3) and match it. If a mechanic could not carry 30+ cards, it is only
  an interaction between a few cards.
- Mechanics are built on the game's basic things: units die, damage, supply and carry-over, cells, rows, the front row,
  dots, round end, cards in hand, the discard pile, moves, spells cast. Buffs and stats alone are not mechanics.
- Before any card, count how many cards each mechanic can give: 100 must fit without filler.
- Never turn each fact of the theme into its own small rule. "Bombs" and "gears" are a few cards inside a mechanic.
- No unit types or card kinds that split the deck (no "crew", no Yin/Yang).
- Kaptain's own ideas (Projectiles, an Immobile faction, Mark, back-in-time) are a few cards or one mechanic, never a
  whole faction.
- A mechanic that limits the player (an order to follow, a card kind, a position) must pay back a lot, or nobody plays it.
- Strong at / a little / weak at, written in the entry. No card gives the faction what its weak list says (a spell faction
  with "weak at melee" gets no melee buffs).
- Conditions come from the identity: "the enemy with the least defence" only in a faction about hunting weak units.

**The cards**
- Every effect changes something that would not happen anyway. Empty example: all Horologers act at round end, so
  "when one acts at round end, the touching ones act too" adds nothing.
- Worth on this board: "this round" penalties (-1 strength, can't attack) are worth almost nothing (the enemy waits);
  "can't move" is near nothing (units rarely move). Effects that last or act now are worth something.
- Rule-bending keywords (Outrider, moving between lanes) sit on a few cards only. A keyword is on a card only if
  something on it uses the keyword (two Push keywords on one card with nothing using Push: wrong).
- Costing: a drawback buys more stats than the curve; Immobile's -2 is small (a cost-1 unit with 0|5 is too much
  defence); a card paid twice (placed, then thrown) is cheaper for it.
- Only the game's own words ("dies", not "breaks"; no "wall"). No flavour text.
- How does it actually happen? For each effect, say how it works with the existing rules. "A card in the enemy's hand
  gives him supply": how? If the game can't do it, mark it NEW RULE.
- Every need of every card has a maker in the same faction, and in every deck made from it: a card that needs enemies
  in the back row needs cards that put them there or reach them.

**Working**
- When Kaptain points out an error on one card or faction, find and fix the same error in all the others first.
- Network tags are specific ("ally-dies-this-round", not "death"); a vague tag makes everything look connected.
- Before sending, go through every line of the four files and know which part of the design passes it.

## 3. Search the library (all 8 games, card by card)
How to ask: part 4, `START_DESIGN-4-asking.md`. Run from `library/cards_db/`.
- For a faction: `ask.py all ways "<faction>"` (its groups of linked cards), `curve` (its cards by cost, each as
  when -> what -> on whom), `spells` (its spells by what they do), `removal` and `protect` (how it removes enemies and
  protects its own), `analyze` on its whole card list (what its cards make happen and which cards use it).
- For a trigger: `ask.py all palette <trigger> [faction]` (everything cards do on Place, death, round end... grouped).
  Use it at step 9: it lists WHATs you haven't used yet.
- For boundaries: `ask.py all only <game>` (what only one faction has: its monopolies), `ask.py all lacks "<faction>"`
  (what a faction never has: its blind spots).
- For a mechanic: `compare`, `factions`, `fed`, `feeds`, `together`, `chains`, `both`. Read 5-10 card texts before trusting
  a count.
- Factions per game: `select game, regions, count(*) from card group by 1,2` in cards.sqlite. Board games first
  (Duelyst, Faeria, Stormbound, Into the Breach, Inscryption), then Runeterra, Monster Train, Slay the Spire.
- Translate every card into Three Bases (section 1b) and say what changed. Example: Runeterra's "Strike the enemy
  Nexus" has no meaning here (no player to hit); the nearest thing is a strike on the unit cancelling your dot.

## 4. Think like a player (every card, every combo)
Part 4, "Think it through like a player" (hand, board, enemy, timing, worth, what a combo is).

## 5. Before sending
- `python3 tools/network_check.py factions/designs/<faction>.txt factions/designs/<faction>-cards.txt`: 0 problems. It
  checks that every need has a maker and counts each card's partners (cards that make what it needs or need what it
  makes). Each champion must have many partners and gather its own way to play; other cards also link to each other.
- `node tools/cardstats.js <letter>`: Benchmark games with the faction's premades; cards that are never played or never
  fire are changed or cut. Never fix a win rate by changing stats off the budget.
- `python3 tools/design_gate.py <letter>`: PASS (it runs the network check and the browser play test too).
- The separate agent's line-by-line check against the four files.
- Tell Kaptain, per mechanic, which library cards it came from and which parts are Claude's own. If the library could
  not answer something the design needed, say so. Talk as CLAUDE.md says: short, plain, one question at a time, last.
