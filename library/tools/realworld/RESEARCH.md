# Real-world cases: how they are made

The cases are the benchmark the library's queries are checked against (`realworld.py`, `realworld_why.py`). They come from
sources only, in four steps per game, one game at a time:

1. **Find sources.** Per faction: the official or wiki page on the faction or class, strategy guides, deck or tier pages for
   archetypes, guide or community pages for known combos. Prefer pages that cover all factions at once.
2. **Read them**, faction by faction.
3. **Summarise** in `tools/games/<game>.md` (after its overview and factions): terse, one block per faction: what it is known for, its archetypes, what it uses a little
   that is another faction's specialty, and known combos with why they work. Every line ends with its source URL (or a short key such as
   [1] or [st] that the file's source list resolves). Only what the sources say; a source claim with no matching concept says so.
4. **Write the cases** in the ```tsv block of the same file, from the summary, in the library's own names, written correctly from the start:
   one case per line, tab-separated: `type  a  b  why  source URL`
   - `signature  <faction>  <concept id>`  the faction is known for this mechanic
   - `archetype  <faction>  <archetype id>`  the faction is known for this archetype (`archetypes.txt`)
   - `splash  <faction>  <concept id>`  another faction's specialty that this faction uses a little
   - `combo  <card A>  <card B>`  a known two-card combo, card names as the library has them
   Faction names as the library has them (`faction_signature`); concept ids from `../key/defs.txt`, the most specific one
   that means the same outcome (the check also accepts narrower and broader concepts below the four branches). `why` is one
   short phrase. Cases must differ from each other. A combo with a card the library lacks stays: it marks missing data.

Not factions, so no faction cases: Neutral, Colorless, Curse, Status, Token, Event, Shared, Universal, Lores, Path to Glory,
Regiments of Renown, rule-book entries named after the game. Games without factions in the library get combos only.

When a case misses, read the cards before changing anything: if their text supports the case, the tags are wrong (fix the
game's pattern so every card with that wording gets the tag); if not, the case or its source is wrong.
