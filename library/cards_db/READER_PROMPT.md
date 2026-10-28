# Reader prompt (used unchanged for every batch; replace BATCH with e.g. batch_019, GAME with e.g. runeterra)

Run as a background agent, model sonnet, type general-purpose.

You describe what card-game cards do as structured JSON records. Work only in /home/claude/three-bases/library/cards_db.
Batch name: BATCH.

1. Read BRIEF.md (all of it) and vocab.tsv (allowed values per field). Follow them exactly; copy the worked examples' style.
2. Read input/GAME/BATCH.jsonl (cards: id, name, category, speed, types, keywords, text, names_in_text).
3. Write one record per card as the brief says. Read every sentence: who "I", "you", "allies", "enemies" are; which event
   triggers; what is a remark with no effect. Never invent rules the text does not state. Do not describe the card's own
   Keywords field.
4. Write records, one compact JSON object per line, in input order, in parts of about 50 cards
   (read/GAME/BATCH.part1.jsonl, part2, ...). If part files already exist, keep them and continue with the cards not in them.
   Then join all parts into read/GAME/BATCH.jsonl with one shell command and delete the parts.
   A card with check_note: the word check found wording its earlier record lacks. Describe that wording if the text
   means it; if the text does not mean it, add the card id to read/GAME/BATCH.rejected.jsonl as {"id": ..., "pattern": ..., "why": ...}.
5. Proposals (only for values that are missing) go to read/GAME/BATCH.proposals.jsonl.
6. Run: python3 check.py GAME read/GAME/BATCH.jsonl --input input/GAME/BATCH.jsonl and fix every problem until it reports
   0 problems.
7. If you write a helper script, keep it in your own folder /tmp/reader_GAME_BATCH/ (never a shared scratch folder).
8. Reply with exactly: records written, number marked unsure, number of proposals.
