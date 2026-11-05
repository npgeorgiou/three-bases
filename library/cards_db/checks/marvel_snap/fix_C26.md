FIXED: Cards that stop all cards being played (Storm's flood) had no line to cards whose own text summons units, though a summon is not a played card. Files: network.py (new flood_lines, joined in the line makers), cases/network.tsv. Cases: n510, n511, n512, n513.
- C26 (Storm -> White Tiger) and C27 (Storm -> Doctor Doom): both now show the line (pair.py), Storm -> Odin and Ebony Maw -> Doctor Doom stay NONE.
- Other blockers of all non-mine hands (Professor X, Goose, Jean Grey, Supergiant, Electro-like cards in a deck) now also link to every Marvel Snap summoner (56 cards have a summon row), weight 0.5, kind "enables".
- Locations (Flooded, Kyln etc.) are not deck cards, so no lines; Runeterra Suppression and Duelyst Magesworn are not matched (zone hand and kind card only).
- No other game has a card matching, so no other game changes.
