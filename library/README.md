# Three Bases library

Material from other card games, to help design Three Bases: factions, mechanics, cards and combos. Every answer comes from
the cards' own texts, written as rows (what each card does, when, to whom), the same way in every game.

## What is here
| Path | What it is |
|---|---|
| `cards_db/` | The card database: every card of 8 games as rows, the networks of their decks, and the questions (`ask.py`). Start with `cards_db/HANDOFF.md`. |
| `three-bases-library.sqlite` | The card texts of 21 games (table `entities`), from an earlier library. The card database reads its texts from here. |
| `games/<game>.md` | Each game's rules, terms, keywords and mechanics with the wording to look for, and the pages they come from. Read before importing a game. |
| `game_patterns/<game>.txt` | Each game's wording rules (regexes) for its mechanics. A help when reading a new game's cards. |
| `sources/` | Each game's raw card data and the script that converted it (`conv_<game>.py`, first lines name the source). |
| `concept_tree.txt` | The concepts, organised by outcome (what an effect does for whom), the same in every game. |

Games in the card database: Legends of Runeterra, Stormbound, Monster Train, Duelyst, Faeria, Inscryption, Into the Breach,
Slay the Spire. Excluded entirely: Shadowverse: Worlds Beyond, D&D 5e, Blood Bowl, Kill Team, Warhammer Underworlds.

## How to ask (from `library/cards_db`)
`python3 ask.py all <question>`; `all` can be one game or several joined by commas. A concept also finds the concepts under
it in the tree (`suppress` finds disable, silence, can't block, can't move). Cards are shown with their short text when a
game has 10 or fewer (`--texts` for all). Each game counts the same in rankings, so Runeterra's many cards don't drown the rest.

| Design question | Command |
|---|---|
| How does a mechanic work in each game? | `compare <concept>` |
| How can a faction stop enemy units? | `compare suppress` (`disable`, `attack_lock`, `immobilize`, `silence`) |
| How can a faction have staying power? | `compare protection`, `compare heal` (`regeneration`, `cheat_death`, `shield`) |
| How can a faction be disruptive? | `compare disruption` (`counter_spell`, `hand_disruption`, `cost_increase`) |
| How can a faction control spots on the map? | `compare zone_control`, `compare terrain` |
| How can a faction be spell-centric? | `compare spells_played_condition`, `compare spell_power` |
| Which factions are built around a mechanic? | `factions <concept>` (share of each faction's cards) |
| What works well with a mechanic? | `feeds <concept>`, `fed <concept>`, `together <concept>` |
| Which combos chain into other combos? | `chains <concept>` (A sets off B sets off C, and in which games) |
| Ideas for a card that does X and Y | `both <X> <Y>` (cards that do both, with texts) |
| How do two cards work together? | `<game> combo "<A>" "<B>"`, `<game> partners "<card>"` |
| Is a set of cards a working deck or faction? | `<game> analyze "<card>, <card>, ..."` (plan, what feeds what, what is missing) |
| Which values can I ask for? | `list concepts`, `list happenings` |

## Known gaps
- Landmarks (Runeterra buildings) still sit under `terrain`, with map spaces; they need a concept of their own (Kaptain's call).
- Faction answers work only where the game has factions (Into the Breach squads, Slay the Spire characters count as factions).
- A question names concepts by their ids (`list concepts`); there is no search by plain words yet.
