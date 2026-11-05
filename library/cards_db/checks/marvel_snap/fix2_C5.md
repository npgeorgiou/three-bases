FIXED: The "makes a unit it counts" line for a keyword need (Ongoing, On Reveal) was given to every maker of a random unit; now the making's own filter must name that keyword. Files: network.py, cases/network.tsv. Cases: n534-n538.
- Touches every game's need lines of the form "a unit with <keyword>" fed by a described (not named) maker; n51 (Imps) checked, stays.
- Needs with a card/name/type filter were already excluded; unchanged.
- pair.py shows it at once (network.py change); no records changed.
