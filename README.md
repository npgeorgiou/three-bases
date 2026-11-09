# Three Bases

A browser card/board game in one HTML file: three lanes, two armies, take and hold two of the three bases.

- `three-bases-game.html` — the game (open it in a browser)
- `three-bases-scenarios.html` — the game with ready test boards
  (both are built from `src/` by `python3 tools/build.py`; never edit them by hand)
- `src/` — the game's source in parts; `tools/` — build, lookup and test scripts
- `three-bases-ai-lab.html` — the AI lab
- `summary/` — the design document (the game as it is now), one file per section; start at summary/README.txt
- `factions/` — faction and card ideas, one file per part or candidate; start at factions/README.txt
- `todo.md` — open work
- `library/` — the inspiration library of card-game mechanics

## Library games (9 Nov 2026)
Interactive: cards fight or answer the opponent's cards (computer enemies count). Positional: where a unit stands changes what it can do. Base holding: you win or gain by holding places on the board. (These three definitions are Claude's.) Card counts: imported games from `library/cards_db/cards.sqlite` (tokens included), the earlier games from `library/three-bases-library.sqlite`, candidates from the named site (counted on the page itself).

Candidate: a game from Kaptain's list of 9 Nov 2026 whose full card texts are online and that is not low on all three grades. Not imported yet. For candidates, cards and keywords were checked; player decks were seen only for Dawncaster (blightbane.io) and Once Upon a Galaxy (wiki deck lists).

| Imported | Name | Cards | Interactive | Positional | Base holding |
|---|---|---|---|---|---|
| yes | Legends of Runeterra | 2594 | yes | no | no |
| yes | Stormbound | 312 | yes | yes | no |
| yes | Monster Train | 379 | yes | yes | no |
| yes | Duelyst | 1163 | yes | yes | no |
| yes | Faeria | 512 | yes | yes | yes |
| yes | Inscryption | 411 | yes | yes | no |
| yes | Into the Breach | 338 | yes | yes | yes |
| yes | Slay the Spire | 818 | yes | no | no |
| yes | Gwent | 1504 | yes | yes | no |
| yes | Marvel Snap | 885 | yes | yes | yes |
| no | Magic: The Gathering | 19454 | yes | no | no |
| no | Hearthstone | 8129 | yes | no | no |
| no | Lorcana | 1848 | yes | no | yes |
| no | Star Wars: Unlimited | 1886 | yes | yes | no |
| no | Elder Scrolls: Legends | 946 | yes | yes | no |
| no | Shadowverse | 4438 | yes | no | no |
| no | Warhammer 40k 10th edition | 3817 | yes | yes | yes |
| no | StarVaders (candidate) | 302 (starvaders.wiki.gg, official) | yes | yes | no |
| no | HELLCARD (candidate) | 584 (hellcard.fandom.com) | yes | yes | no |
| no | Decktamer (candidate) | 151 creatures (decktamer.miraheze.org) | yes | yes | no |
| no | Wildfrost (candidate) | about 240 (dood.gg: 65 companions, 81 items, 32 clunkers, 62 charms; wildfrostwiki.com, official) | yes | yes | no |
| no | The Bazaar (candidate) | 643 items (thebazaar.wiki.gg) | yes | yes | no |
| no | Once Upon a Galaxy (candidate) | 666 (onceuponagalaxy.wiki.gg: 313 characters, 110 captains, 180 treasures, 63 spells) | yes | yes | no |
| no | Across the Obelisk (candidate) | 792 (ato.fandom.com) | yes | no | no |
| no | Dawncaster (candidate) | 2729 (blightbane.io, official) | yes | no | no |
| no | Astrea: Six-Sided Oracles (candidate) | 742 dice (astrea.wiki.gg, official) | yes | no | no |
| no | Eternal (candidate) | about 3600 collectible (eternalcardgame.fandom.com, sets to Battle Lines 2023) | yes | no | no |

Candidates dropped: Hell Deck (searched only; no wiki or card list found), and these checked in the browser: Gordian Quest (wiki card page is an empty stub), As We Descend (wiki has 14 card pages), Hive Blight (no wiki), Montabi (card list only in the game), Guildrun (not released), Imajica (archive lists names without card text), Grail (fan site has guides, no card list), Might & Magic Fates (rules text only in card pictures on mmdecks.com), Shardmoon (full text only in the app), Wyldernook (no card list), SolForge Fusion (official card search returns nothing; 15,000 generated cards), Mythgard (wiki has 333 stub pages of 676 cards; mythdb.eu is down). Dropped as too big (would drown the others): Yu-Gi-Oh! Master Duel. Gwent was already imported.
