# Real-world checks (Step 7)

Work only in /home/claude/three-bases/library/tools/realworld/. Do not open the database, git or other workers' files.
For each game named in your task, search the web (wikis, strategy guides, community discussion) for each faction's identity,
its known combos and its archetypes. Use few searches (about 3-5 per game); prefer one good wiki or guide page per game.

Write `<game>.tsv`, one test case per line, tab-separated: `type  a  b  why  source URL`
- `signature  <faction>  <concept id>`  the faction is known for this mechanic (concept ids: ../key/defs.txt)
- `archetype  <faction>  <archetype id>`  the faction is known for this archetype (ids: archetypes.txt)
- `combo  <card A>  <card B>`  a well-known combo of two cards of that game (exact card names as the game prints them)
- `splash  <faction>  <concept id>`  a mechanic that is another faction's specialty but this faction uses a little
Faction names must be written exactly as in factions/ (game, faction, size). Up to 10 cases per type per game, fewer where the
sources are thin; cases must differ from each other. Every line needs a source URL that states it; never invent cases.
`why` is one short phrase. Save the file after each game; if it already exists when you start, skip that game.
Reply with one line: `finished: <games>`.
