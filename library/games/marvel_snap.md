# Marvel Snap

One file per game: the game, its factions, the source summary, the mechanics (patterns) and the real-world cases.

## The game
Digital collectible card game (Second Dinner, 2022). No factions: cards come in series; the library's tribes are teams named
on the cards. Claude's earlier summary from memory is replaced by the sourced rules below (5 Nov 2026).

## The game's rules (from sources, read 5 Nov 2026; Claude's words)
- Deck of 12 cards, one copy of each; 3 cards in the starting hand, one more drawn each turn [R1].
- Energy starts at 1 and grows by 1 each turn (6 on the last turn); unspent energy is lost [R1].
- 6 turns; both players play at the same time, then the cards are revealed [R1].
- Three locations: the left one shows at the start, the middle one before turn 2, the right one before turn 3; each
  carries its own rule [R1].
- At most 4 cards per player at a location [R1]; a card can't move past the left or right location or into a full one
  [T1].
- After the last turn, whoever has more Power at a location wins it (unless the location says otherwise); 2 of 3 wins
  the game; a tie in locations goes to total Power, then it is a draw [R1].
- Reveal order: the player winning more locations reveals first; then the one ahead on Power; else random [U1], [R1].
- Card abilities resolve first, in reveal order; location abilities after all card abilities [H1].
- Play / Add / Put / Move: only a card played from hand counts as played; Add and Put place a card without the played
  effects; Move relocates a card already in play [H2]. On Reveal still happens when a location puts a card into play,
  unless something stops it [H4].
- Most cards work only in play; some act from hand (when discarded or destroyed there) or from the deck [H5].
- An ability tied to a location stays there when the card is moved by another card, and moves with the location when
  locations swap [H6].
- Snap doubles the cubes at stake; the final turn doubles them again; retreating loses only the cubes at stake at the
  start of that turn [R1]. Stakes say nothing about which cards belong together: not written as records.

[R1] marvelsnapzone.com/how-to-play-marvel-snap-for-beginners  [U1] blog.snap.untapped.gg/marvel-snap-wiki-how-priority-works
[H1]-[H6] marvelsnap.helpshift.com gameplay FAQ: 40 order of operations, 42 Play/Add/Put/Move, 94 cards per location,
48 On Reveal, 39 when card text has an effect, 50 location-tied abilities. [T1] thegamer.com Marvel Snap cards effects
explained (8 Nov 2022). Keyword sources: supplement_marvel_snap.py KEYWORDS.
Written as game_rules.jsonl: the 4-card limit (it links cards that fill a location and cards that need room). The rest is
what every card does and draws no line between cards.

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
