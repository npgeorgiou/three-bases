# Handoff: card database, Runeterra (28 Oct 2026)

## Start of the next chat
1. Clone with the library (CLAUDE.md "Start of a chat", then `git sparse-checkout disable`).
2. Read only this file. Then, as the task needs: README.md (files, tables, rules for session limits), RESULTS.md (findings),
   GUIDE.md (another game). Check the state from the files: `python3 status.py runeterra` (all done) and
   `python3 load.py runeterra && python3 cases/run.py runeterra` (must say 247 of 247).

## Where it stands
- Runeterra base game fully described (Path of Champions excluded): records in `read/runeterra/` are the source,
  `cards.sqlite` is built from them, the query layer (flat_*) holds keyword meanings and concept-tree concepts.
- 247 of 247 case tests pass (cases/REPORT.md). Example questions with real answers: QUERIES.md.
- Measured accuracy: 9% of a 219-card double-read sample were misread, all corrected. Same-way mistakes of both readers are
  not measured; Kaptain's check of CHECK_20.md / CHECK_20_RAW.txt is the outside test and has not been given yet.

## Open for Runeterra (Kaptain said there is more work; these are the known gaps)
1. Kaptain's verdict on CHECK_20.md: every error he finds is fixed generically (all cards with the same problem).
2. 122 cards marked unsure (table `unsure`; readers' proposals in `read/runeterra/*.proposals.jsonl` and
   `fixes/runeterra/*.proposals.jsonl`): rare mechanics without values ("in 5+ different rounds", "every third time",
   swapping Power and Health, "Recalled this game"). Add the values that repeat (vocab.tsv, BRIEF.md, CHANGES.md), then
   `reread.py make runeterra unsure` and read those batches.
3. 69 stub entries: cards and keywords the texts name but the library lacks (Dauntless Vanguard, Spiderling, Deep...).
   They have names only. Deep has no definition text anywhere in the library: do not write one from memory.
4. 42 cards carry "Missing Translation" in their source text (broken data): those parts are not described.
5. Connections are broad by design (any kill-an-ally card feeds any "when an ally dies" card). The reason given by
   `connections.explain` is the first link found, not always the most natural one (Hecarim -> Shark Chariot shows
   "kill -> dies via Spectral Rider").
6. The old library (tags, answer key, patterns, query.py) is untouched and not connected to cards.sqlite.

## How to work here (learned the hard way)
- Show real cards with their stored rows (`raw.py <id>`) before and after any change; never judge by percentages alone.
- When a query returns too little, check the query against the texts first, then the records.
- Every change: rebuild (`load.py runeterra`), `cases/run.py runeterra` must pass, commit and push at once.
- Readers: READER_PROMPT.md unchanged, model sonnet, background; merge or normalize only after a reader has finished.
