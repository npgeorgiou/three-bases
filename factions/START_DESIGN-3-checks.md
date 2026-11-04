# Start design, part 3: checks, library, player view, before sending
Part of `factions/START_DESIGN.md` (read that first, whole; then `START_DESIGN-2-rules.md` and this file, whole).

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
