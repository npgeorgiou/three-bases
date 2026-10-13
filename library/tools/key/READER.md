# Answer-key reader (Step 2)

You are one reader of the library's answer key. You see only card text and the concept definitions, never the library's tags.
Work only in the repository at /home/claude/three-bases. Do not open the database, other readers' folders, or any other tool file.

## Setup
1. Read `library/tools/key/defs.txt` once. Each line: `concept_id | name | what counts | Not: what doesn't count and where it goes`.
2. Your folder is `library/tools/key/<game>/<reader>/` (create it). Your progress note is `progress.txt` in it.
3. If `progress.txt` exists, read only it and continue after the last batch it names. Never redo a finished batch.

## Reading a batch
Your batches are the files named in your task (for example `batch_00.txt`, `batch_01.txt` ... in `library/tools/key/<game>/`), in order.
Each line is `id | name | text` (a ` / ` stands for a line break).

For every entry, go clause by clause and write each concept the clause expresses, with the exact words that justify it:
- The words must be copied character for character from the entry's name or text (a short phrase is best). A script rejects any
  tag whose words are not in the text.
- Judge only against the definitions. Use the most specific concept that fits; do not add its parent as well.
- A clause can express several concepts (a trigger, a condition and an effect). Triggers and conditions count too.
- Keyword or glossary entries: tag what the keyword itself does.
- An entry with no mechanic (lore, a bare name, plain stats with nothing else) gets an empty list.
- Do not guess beyond the text. If the text doesn't say it, it isn't there.

Write the batch's result to `<your folder>/<batch name>.json` (for `batch_03.txt`, write `batch_03.json`):
`{"<id>": [["concept_id", "exact words"], ...], ...}` with every id of the batch. Then append one line `done <batch name>` to
`progress.txt`. Save after every batch.

## At the end
Run `python3 library/tools/key/key.py check <game> <reader>`. If it reports tags rejected for `words`, open those entries again and
correct the words so they are copied exactly (or drop the tag if the text doesn't support it), in the same batch file. Then reply
with one line: `finished <game> <reader>: <number of batches> batches`.

## Third reader (C)
If you are reader C, your batch files are `settle_NN.txt` (or `covsettle_NN.txt`). Each entry shows the text and the tags of
readers A and B. Decide the entry's correct tags against the definitions (keep, drop or add), with exact words as above, and
write the full final list for every entry to `C/<batch name>.json`. Same progress note and check (`... check <game> C`).
