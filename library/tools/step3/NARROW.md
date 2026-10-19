# Narrowing weak patterns (Step 3)

Work only in /home/claude/three-bases/library/tools/step3/. Do not open the database directly, git, or other workers' files.

Your work file is `narrow/NN.md` (named in your task). It holds weak wording patterns. For each `## PATTERN <id>` you see the
concept's definition, the games where it is below 90% right, and known WRONG and RIGHT matches (from the answer key and from
judged samples), each with the matched words in `[[ ]]`. Texts are lower-case, the entry's own name is written `name`, and Magic
is read without its reminder text (in parentheses).

Pattern id: `concept|role|game or *|regex`. Patterns are Python regular expressions, searched case-insensitively.

For each pattern:
1. Find what separates the wrong matches from the right ones in the wording (who is targeted, the verb, a following word...).
2. Write a narrower regex: it must only match text the old one matches (add context, lookaheads or lookbehinds to the old regex
   rather than inventing new wording), keep as many known RIGHT matches as possible and drop the WRONG ones.
3. Test it: `python3 patterns3.py try '<pattern id>' '<new regex>' [game,game]` prints, per game, the matches before and after,
   the known matches it keeps and how many are right, and the known-right matches it would drop. Aim for 90%+ right on the known
   kept matches while dropping as few known-right ones as possible. Try a few versions; each run takes a while, so think first.
4. If no narrower regex reaches 90% in a game without dropping most of the right matches, answer `keep` for that game.

Write one line per decision to `narrow/out_NN.tsv` (tab-separated), right after deciding each pattern:
`<pattern id>\t<games, comma-separated>\t<new regex or keep>`
A pattern can get different decisions for different games (several lines). Your progress is that file: if it exists when you
start, continue with the first pattern it does not yet list. Never invent rules or mechanics; judge by the definitions only.
Reply with one line: `finished NN: <n> narrowed, <n> keep`.
