# Marvel Snap

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
*Claude's summary (Oct 2026), from general knowledge of the game and the rules and terms under Mechanics; not from the sources below.*
- Genre: digital collectible card game (Second Dinner, 2022); 12-card decks, games of 6 turns.
- Board: 3 locations, revealed one per turn on turns 1-3; each location changes the rules. Up to 4 cards per side per location.
- Energy: equals the turn number. Both players play face down at the same time; cards reveal in order.
- Win: have more power at 2 of the 3 locations.
- Stakes: cubes; Snap doubles them, retreating loses fewer.
- Keywords: On Reveal, Ongoing, Activate; no factions in the library, combos only.

## Sources and notes

Sources:
[1] https://www.highgroundgaming.com/marvel-snap-best-decks/
[2] https://www.pocketgamer.com/marvel-snap/best-decks/

The library has no factions for Marvel Snap; combos only.

## Combos
- M.O.D.O.K. + Hela: discard the hand, Hela brings the discarded cards back [1]
- Morbius + Swarm / Apocalypse: Morbius grows per discard; these return after discard [1]
- Wong + Odin: Wong doubles Odin's On Reveal [1]
- Ironheart / Black Panther + Odin: Odin repeats their power boosts [1]
- Storm + White Tiger / Doctor Doom: they still place cards in the flooded location [1]
- Brood + Wolfsbane: Brood fills a location, Wolfsbane gains power as the fourth card [1]
- Moon Girl + Devil Dinosaur: doubled hand boosts Devil Dinosaur [1]
- Professor X + Devil Dinosaur [1]
- Shuri + Typhoid Mary / Red Skull: Shuri doubles the next card's power [1]
- Zero / Sauron + Titania / Ebony Maw: removes their drawbacks [1]
- Taskmaster + Red Skull / Typhoid Mary: Taskmaster copies the last card's power [1]
- Cable + Mantis: take cards from the opponent's deck [2]
- Carnage + Nova: buff all cards on the board [2]
- Ant-Man + Angela: points in the third location [2]
- Doctor Octopus + Mojo: +6 when the spot is empty [2]
- Wave + Death: the deck is built around the two [2]
- The Collector + Moon Girl: Collector buffs cards, Moon Girl copies them [2]

## Mechanics
The mechanics the guides name, one per line as `name|concept|regex`, and the rules and terms as `# term:` lines. Read by `coverage.py --mechanics` and `key/key.py`.

```mechanics
# Mechanics the guides name: name|expected concept|wording on the cards. Checked with coverage.py --mechanics (not yet run).
# Sources (21 Oct 2026): highgroundgaming.com/marvel-snap-best-decks, pocketgamer.com/marvel-snap/best-decks (named pairs).
on reveal|on_play|\bon reveal\b
ongoing|aura|\bongoing\b
discard|discard|\bdiscard\b
destroy own cards|sacrifice|\bdestroy (a|another|your)\b
move|movement|\bmoves?\b
copy|copy|\bcop(y|ies)\b
double hand (Moon Girl)|copy|\bduplicate your hand\b
location-based (Storm floods, flooded locations)|lane_closure|\bflood\b
power doubling (Shuri)|stat_multiply|\bdouble (its|the) power\b
take from the opponent's deck|steal|\bopponent's deck\b
# term: Ongoing and On Reveal are card text words; the sources name On Reveal for Wong and Odin (highgroundgaming).
```

## Cases
The real-world cases, one per line, tab-separated: `type  a  b  why  source` (see `realworld/RESEARCH.md`). Read by `realworld.py`, `realworld_report.py`, `realworld_why.py` and `learn_recipes.py`.

```tsv
combo	M.O.D.O.K.	Hela	discard, then Hela brings them back	https://www.highgroundgaming.com/marvel-snap-best-decks/
combo	Morbius	Swarm	Morbius grows per discard	https://www.highgroundgaming.com/marvel-snap-best-decks/
combo	Morbius	Apocalypse	Morbius grows per discard	https://www.highgroundgaming.com/marvel-snap-best-decks/
combo	Wong	Odin	Wong doubles Odin's On Reveal	https://www.highgroundgaming.com/marvel-snap-best-decks/
combo	Ironheart	Odin	Odin repeats the power boost	https://www.highgroundgaming.com/marvel-snap-best-decks/
combo	Black Panther	Odin	Odin repeats the power boost	https://www.highgroundgaming.com/marvel-snap-best-decks/
combo	Storm	White Tiger	places cards in the flooded location	https://www.highgroundgaming.com/marvel-snap-best-decks/
combo	Storm	Doctor Doom	places cards in the flooded location	https://www.highgroundgaming.com/marvel-snap-best-decks/
combo	Brood	Wolfsbane	Wolfsbane gains power as the fourth card	https://www.highgroundgaming.com/marvel-snap-best-decks/
combo	Moon Girl	Devil Dinosaur	doubled hand boosts Devil Dinosaur	https://www.highgroundgaming.com/marvel-snap-best-decks/
combo	Professor X	Devil Dinosaur	named together	https://www.highgroundgaming.com/marvel-snap-best-decks/
combo	Shuri	Typhoid Mary	Shuri doubles the next card's power	https://www.highgroundgaming.com/marvel-snap-best-decks/
combo	Shuri	Red Skull	Shuri doubles the next card's power	https://www.highgroundgaming.com/marvel-snap-best-decks/
combo	Zero	Titania	removes the drawback	https://www.highgroundgaming.com/marvel-snap-best-decks/
combo	Zero	Ebony Maw	removes the drawback	https://www.highgroundgaming.com/marvel-snap-best-decks/
combo	Sauron	Ebony Maw	removes the drawback	https://www.highgroundgaming.com/marvel-snap-best-decks/
combo	Taskmaster	Typhoid Mary	Taskmaster copies the last card's power	https://www.highgroundgaming.com/marvel-snap-best-decks/
combo	Taskmaster	Red Skull	Taskmaster copies the last card's power	https://www.highgroundgaming.com/marvel-snap-best-decks/
combo	Cable	Mantis	take cards from the opponent's deck	https://www.pocketgamer.com/marvel-snap/best-decks/
combo	Carnage	Nova	buff all cards on the board	https://www.pocketgamer.com/marvel-snap/best-decks/
combo	Ant Man	Angela	points in the third location	https://www.pocketgamer.com/marvel-snap/best-decks/
combo	Doctor Octopus	Mojo	+6 when the spot is empty	https://www.pocketgamer.com/marvel-snap/best-decks/
combo	Wave	Death	the deck is built around the two	https://www.pocketgamer.com/marvel-snap/best-decks/
combo	The Collector	Moon Girl	Collector buffs, Moon Girl copies	https://www.pocketgamer.com/marvel-snap/best-decks/
```
