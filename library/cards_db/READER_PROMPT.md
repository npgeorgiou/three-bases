# Card reader job (used unchanged for every batch; replace BATCH with e.g. batch_019, GAME with e.g. runeterra)

Run as a background agent, model sonnet, type general-purpose.

You describe what card-game cards do as structured JSON records. Work only in /home/claude/three-bases/library/cards_db.
Batch name: BATCH.

1. Know the game first: read ../games/GAME.md, the sections "The game", "The game's rules (from sources)", "Factions",
   "Combos" and any notes for readers (skip sources, mechanics lists and cases).
2. Read BRIEF.md: everything above "## Game words: Runeterra", then the "Game words" section of GAME. Read vocab.tsv
   (allowed values per field). Follow them exactly; copy the worked examples' style.
3. Read input/GAME/BATCH.jsonl (cards: id, name, category, speed, types, keywords, text, names_in_text).
4. Write one record per card as the brief says. Read every sentence: who "I", "you", "allies", "enemies" are; which event
   triggers; what is a remark with no effect. Never invent rules the text does not state; never write what the game's rules
   do for every card. Do not describe the card's own Keywords field.
5. Write records, one compact JSON object per line, in input order, in parts of about 25 cards
   (read/GAME/BATCH.part1.jsonl, part2, ...), each part written as soon as its cards are read, so a reader stopped by a
   token or session limit loses at most one part. If part files already exist, keep them and continue with the cards not
   in them. When all cards are in parts: join the parts into read/GAME/BATCH.jsonl, count its lines against the cards of
   input/GAME/BATCH.jsonl, and delete the parts only if every card is there.
   A card with check_note: the word check found wording its earlier record lacks. Describe that wording if the text means it;
   if not, add the card id to read/GAME/BATCH.rejected.jsonl as {"id": ..., "pattern": ..., "why": ...}.
6. Proposals (only for values that are missing) go to read/GAME/BATCH.proposals.jsonl.
7. Run: python3 check.py GAME read/GAME/BATCH.jsonl --input input/GAME/BATCH.jsonl and fix the problems it reports. At most
   3 rounds of check and fix: then mark every card still failing as unsure (BRIEF.md) and stop; never loop on one card.
8. If you write a helper script, keep it in your own folder /tmp/reader_GAME_BATCH/ (never a shared scratch folder).
   Never write, move or delete any file but your own batch's (read/GAME/BATCH.*, /tmp/reader_GAME_BATCH/); never run git,
   run.py or any rebuild; never overwrite read/GAME/BATCH.jsonl if it already holds a finished batch (stop and say so).
9. Reply with exactly: records written, number marked unsure, number of proposals.
