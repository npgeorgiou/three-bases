# Handoff: card database, Runeterra (28 Oct 2026, second session)

## Start of the next chat
1. Clone with the library (CLAUDE.md "Start of a chat", then `git sparse-checkout disable`).
2. Read only this file. Then, as the task needs: README.md (files, tables, the flat_ref rule), RESULTS.md, GUIDE.md.
   Check the state: `python3 status.py runeterra` (all done), `python3 load.py runeterra && python3 cases/run.py runeterra`
   (248 of 248).

## Where it stands
- Runeterra fully read, including 49 cards the library lacked (supplement/, from Riot's own data).
- flat_ref answers "which cards care about X" for every happening in one query (README); case m81 checks allies dying.
- Kaptain's check file: CHECK_20.md, made by check_table.py (stored tables, names instead of ids).
- 60 cards marked unsure: each has a mechanic no other card has (table `unsure`, proposals in read/ and fixes/).

## Open for Runeterra
1. Kaptain's verdict on CHECK_20.md (fix each error for every card with the same problem).
2. The word check against reader records (Kaptain's point 1, 28 Oct): pattern selection, judging and batching are proposed
   in chat and wait for his answer; nothing built yet. The old library (tags, key, patterns, query.py) is still not
   connected to cards.sqlite; that check is the first connection.
3. Names with no text in the library or in Riot's data: Deep, Plant, Stance, Cursed, Release, Ascended (no rules written).
   Still references to names that are no card: Spriteling, Phased Moon Weapon, Treasure (a Riot subtype the library lacks),
   Dragon's Rage, Prank, Mark of the Storm (keyword-field names), Swapbot.

## How to work here (learned the hard way)
- Show real cards with their stored rows (`raw.py <id>`, `rows.py <id>`) before and after any change.
- When a query returns too little, check the query against the texts first, then the records.
- Every change: rebuild (`load.py runeterra`), `cases/run.py runeterra` must pass, commit and push at once.
- Readers: READER_PROMPT.md unchanged, model sonnet, background; merge (`reread.py merge`) only after a reader has finished,
  never load while a reader writes part files.
- A re-read can lose what the old reading had (copies became summons): run the cases after every merge.
