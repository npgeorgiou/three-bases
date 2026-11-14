# Handoff for the next wheel chat (14 Nov 2026, evening)

Follow `factions/START_DESIGN-1-wheel.md` steps 1-8 and stop at Stop 1. This file says what the first try found, why
the guide changed, and what can be reused. Kaptain didn't follow every explanation: when he asks "why", answer from
here, with a card example, in plain words.

## What happened
- The first try started from mechanics (the old step 1) and skipped the wheel. Kaptain: the design starts from the
  wheel and the radii that work together; mechanics come after, inside each faction's radii.
- Kaptain deleted the seven factions (Horologers ... Long Guns): card files, premades, summary files, designs. "We
  remake everything." Nothing is dropped for being like them any more.
- Kaptain: 30 cards is plenty for a 100-card faction; small mechanics are inspiration, keep them; never merge two
  mechanics into one (the difference is lost and must be found again later); 2 monopolies per faction.

## Why each change to the guide (the reasons Kaptain asked for)
1. **Wheel first.** The 24 radii are measured on real factions; mechanics measured alone have no place on the
   circle. Four mechanics of the first pool (standing beside allies, moving units, weakening enemies, reacting to
   allies placed) sit on no radius with link numbers: only under "position and combos" or "stops them". Starting
   from the radii gives each faction its place first; its mechanics then fill its radii.
2. **"Each radius joined to at least one other", not "all joined to all".** Numbers (cards >= 1.5 x chance):
   only 41 sets of 3 radii are all joined to each other, using 16 of 21 radii. If each radius only needs one join
   (trigger -> payoff), there are 273 sets of 3: plenty for 20 different factions. Real factions are like that
   (Shadow Isles: kills outright, brings back, spends them, position and combos, heals them).
3. **Two radii work with almost nothing:** "stops them" and "grows defence" have no partner with cards >= 1.5 and
   decks >= 1. A faction strong in them needs its join argued from this game's rules, or a partner radius found.
4. **"Rewards playing spells" looks joined to everything** (9 strong partners, the most): a card that rewards
   spells links to every spell. Trust only its deck number.
5. **Agent reads before measuring.** The library's concepts caught the right cards badly for many mechanics:
   1 of 8 right for standing beside allies, guard, discard, weaken, round start; 3 of 8 for countboard, allies
   placed, movement, onattack, strikes, draw, pick, hide. Every count and link number depends on the concept list,
   so fix it first.
6. **Link numbers only after the concepts are fixed.** The first try had agents read the combo pairs, then changed
   the pool: that reading is out of date (in /tmp only, lost). Redo it.
7. **2 monopolies per faction.** 20 x 2 = 40 mechanics. Two factions strong on the same radius own different
   mechanics in it ("brings back" holds both "my dead units come back" and "my unit goes back to hand").
8. **No "biggest real faction has 30+" test.** Real factions are much bigger than ours, so the test doesn't fit:
   concepts with 30+ cards and at least 1.5 x the game's average share, per faction (Claude's yardstick):
   Runeterra 10 factions, 230 cards each, 4.7 such per faction (2 to 8), 43 more with 10+ cards; Gwent 6 x 179
   cards, 3.2 (1 to 8), 43; Slay the Spire 4 x 86, 2.3, 18; Duelyst 6 x 116, 1.0, 19; Faeria 5 x 65, 1.8, 13;
   Monster Train 6 x 42, 0, 12.

## What the radii numbers say (radius_links, all cards; decks in brackets)
21 radii have numbers; 49 of 210 pairs >= 1.5 in cards, 23 pairs >= 1.2 in both cards and decks. Strong partners
per radius: spellpay 9, back 8, spends 6, supply 5, cheaper 5, tall 4, grows 3, strikes 3, picks 3, textdmg 2,
many 2, spelldmg 2, wide 2, kills 1, disrupts 1, one 1, cards 1, heals 1, protects 1, stops 0, growsdef 0.
Remake them: the Python block that made them is `axes.radius_links(games, pools, con, pairs[, deck_lists])`, used
the same way in `mechanics_wheel.py links`.

## What can be reused
- `library/cards_db/mechanics_wheel.py`: reads `factions/wheel/mechanics.tsv`; `measure`, `links`, `cards <file>`
  (8 cards per mechanic for an agent), `pairs a+b,c+d <file>` (linked card pairs with their link reason). Outputs in
  `library/cards_db/wheel/`. Needs links.sqlite (`python3 links.py`, about 4 minutes, not in git). Concepts in the
  tsv: comma list; `concept@game,game` counts only in those games; a game name after an @-concept belongs to it.
  Column 5 = concepts of the cards that make it happen (counted with it).
- `factions/wheel/mechanics.tsv` holds 23 mechanics: merged and cut. Undo that: one line per mechanic again. The
  first list had 44: deathfeed (others grow from deaths), lastwords (Death effects), sacrifice, selfhurt (damage own
  units), revive, recycle (discard pile back to deck/hand), returnhand, tokens, countboard, allyplay, adjacency,
  movement (own), push (enemy), lanes, cells (claimed cells, NEW RULE), onattack, strikes (twice or first),
  overkill (excess hits the unit behind), onkill, fight, ping, area, kill outright, spelldmg, spellpay, hurt (hit
  and survive), silence, weaken, change (transform, steal), hand (enemy hand and costs), junk (clog enemy cells and
  hand), trap (dropped: an answer on the enemy's turn, which this game has none of), supply, cheaper, inhand,
  draw, create, copy, pick, discard, heal, shield, guard, attach (NEW RULE); later also roundstart (the library
  catches player turns: 1 of 8 right), leave, hide, bigstrength (strength 5+), growth (buff alone: not a mechanic).
- Agent verdicts of the first read (before narrowing): KEEP lastwords, revive, overkill (excess must hit the unit
  behind: no player health), spelldmg, create, shield. Wrong catches found: Elusive is blocking only, not "can't be
  targeted"; on_ally_play mostly reacts to its own summon; board_presence rewards being alone; many "heal" cards heal
  the player; deck milling does little here; equipment shows up under return to hand.
- `python3 apart.py 15`: kept apart, e.g. friendly_fire / immunity -0.68, immunity / ping -0.63, count / death
  -0.55, on_kill / on_spell -0.53, evasion / merge_attach -0.45. Together: destroy / sacrifice +0.83,
  death_trigger / sacrifice +0.79, damage_reduction / on_damaged +0.78. Concept level: read cards before trusting.

## The deleted factions: what is left
- Gone: `src/game/js/cards/new-<seven>.js`, their premades (DECKS and PREMADE empty, PREMADE_VERSION 8),
  `summary/11-faction-*.txt`, `factions/designs/`, `factions/11-seven-factions.txt`, their todo items.
- Left in the engine, no card uses it: their keyword rules (fx.js, fx-more.js, keywords.js hovers,
  keyword-worth.js, summary/10-keywords.txt). Remove or reuse when the new factions' rules are built.
- The game and the lab load without errors (smoke). simtest, fxtest, playtest, cardstats, design_gate and the lab's
  games need decks and fail until a new faction exists.
- Examples that name them in START_DESIGN files (the 14 Horologers that all did "round end: strike") are lessons,
  kept on purpose.
