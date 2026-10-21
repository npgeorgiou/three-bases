# Pattern-sample judge (Step 3)

You judge whether a card text expresses a concept. You see only the text and the concept's definition, never the library's tags.
Work only in /home/claude/three-bases/library/tools/step3/. Do not open the database, git, other readers' folders or other files.

Your batches are files `judge/NNN.txt` named in your task. Each starts with the definitions of the concepts it asks about
(`id | name | what counts | Not: what doesn't count and where it goes`), then one question per line:
`qid | concept | game | name | text`. A qid ending in `*` is asked to two readers; answer it the same way as the others.

For each question answer `yes` if the text (any clause of it) expresses that concept as the definition says, else `no`.
- Judge against the definition only, including its "Not" sentence: if the text fits the concept named there instead, answer `no`.
- A concept that is a narrower kind of the one asked still counts as `yes` (an area-damage card expresses "Deal damage").
- Do not guess beyond the text.

Write `judge/<your reader letter>/NNN.json` (for `judge/007.txt` reader A writes `judge/A/007.json`): `{"<qid without *>": "yes"|"no", ...}`
for every question of the batch. Save after each batch and append `done NNN` to `judge/<letter>/progress.txt`. If that progress file
exists when you start, read only it and continue after the last batch it names; never redo a finished batch.
Keep any helper script in `judge/<letter>/` with a name that includes your batch numbers. Reply with one line: `finished <letter>: <batches>`.

Reader B gets `b_NNN.txt` files that hold only the questions marked `*`; it writes `judge/B/b_NNN.json`. Reader C gets `settle_NNN.txt` files listing
questions where A and B differ, with both answers; write the final answer to `judge/C/settle_NNN.json`.

## Second round files
Reader A: `judge/rNNN.txt` -> `judge/A/rNNN.json`. Reader B: `judge/rb_NNN.txt` -> `judge/B/rb_NNN.json`. Write the json with one
short python or shell command per batch; keep reasoning brief.
