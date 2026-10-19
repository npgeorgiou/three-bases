# Adding a game to the library: cheap and safe

Written 20 Oct 2026 from what the tag-fix plan got wrong. Read this whole file before you add a game.

## Rule zero
- Scripts first. Do not use reading agents (readers, judges, narrowers) unless Kaptain approves a measured cost.
- Every reading step runs on one batch first. Report its tokens before going on.
- Do not repeat experiments in loops. Before you choose a fix, break the errors down by where they come from (the `method` column).

## 1. Load
1. Write a converter, `tools/convert/conv_<game>.py`. It outputs JSON in the format described at the top of `tools/load_cards.py`:
   ext_id, name, category, faction, subtypes, cost, stats, text, and `keywords` as a field.
2. Keep the source's keyword lists as a field and set `_keywords_from_field`. Links taken from source fields are trusted; links found by matching text are not.
3. Build with the load: `sh tools/build.sh three-bases-library.sqlite <scratch>/new.sqlite <game>=<cards.json>`.
   - The build keeps every older entry exactly as it was (`keep_old.py`).
   - Never run a build without loads just "to see". It re-applies every pattern and review file to all games and changes other games' tags.
     That is how the plan's first full rebuild made some games worse.

## 2. Keywords before cards
1. Add the game's glossary keywords as category `keyword` entries, each with its definition text.
2. Tag the keywords with patterns, using the concept definitions in `tools/key/defs.txt` and each concept's "Not:" line in `tools/concept_tree_v3.txt`.
3. If the game has more than about 50 keywords, ask Kaptain whether they should be read. If he says yes, use one Sonnet reader with the script quote check (`key.py check`).
4. A card has a keyword only in these cases:
   - the source field lists it;
   - the keyword stands where the game prints keywords: at the start of the text, a line, a sentence or a clause, or in a "Keywords:" list (`valid()` in `tools/kw_links.py`).

   Anything else is `mentions_keyword`. Cards inherit a keyword's tags only through has/grants links.
5. Test `kw_links` on the new game before switching it on in `tools/step_games.json`. It made 7 games worse and helps the rest.

## 3. Patterns
- Put the game's own patterns in `tools/patterns/<game>.txt`. Patterns go per game because each game words things its own way.
  To stop a general pattern for this game, use the `!` lines there (`tools/step3/switch_off.py`).
- Write regexes against the text as the build reads it: lower case, the entry's own name as `name`, a named card as `namedcard`,
  and for Magic no reminder text.
- Tag the outcome the player gets (concepts are organised by outcome, not mechanism), and the narrowest concept that fits.
- Check the siblings using their "Not:" lines, for example stat_gain vs temporary_buff vs permanent_growth.
  Most wrong tags were sibling confusions, and narrowing a pattern cannot fix those.
- A pattern that matches 10 or more entries in the key needs no outside sample.

## 4. Measuring (only if Kaptain approves reading)
1. Take a sample of at most 100 entries with `key.py sample`, seed 1.
2. Use one Sonnet reader. `key.py check` must verify every tag's quote.
   Add a second reader only on 20 entries, to estimate agreement.
3. The reader instructions MUST say: "a keyword or ability named on the card counts: tag that keyword's effects, quoting the keyword's name".
   Without this, all 168 Blood Bowl players were read as empty, and every score for keyword-heavy games went wrong (`KEY_BUG.md`).
4. Score with `key.py score`, crediting named keywords (the `key_kw` layer in `KEY_BUG.md`).
5. To make patterns from the key, run `tools/step3/key_patterns.py`. It builds on one half of the key, tests on the other half,
   and keeps a pattern only if it is 90%+ right there.
6. To get rid of wrong tags, narrow a pattern only after a sample of what the narrowing drops has been judged 90%+ wrong (`patterns3.py accept`).
   Narrowing cannot fix misses or sibling confusions.

## 5. Never
- Never run more than 3 or 4 agents at once. Rate limits killed every larger batch.
- Never let agents share helper scripts in a common scratchpad. They overwrite each other.
- Never judge with Opus. Use Haiku for yes/no questions and Sonnet for regexes.
- Never start an agent without a progress file it saves after each batch and can resume from.
- Never remove a tag unless it has been judged wrong. Hand reviews in `tools/regression.tsv` always win.
- Never put more than 60 to 80 questions in one judging file.

## 6. Finish
1. All build checks must pass: regression, combos, trigger pairs, query tests, realworld.
2. Add 10 to 20 real-world cases with source URLs to `tools/realworld/<game>.tsv`.
3. Check the database size. GitHub refuses files over 100 MB; `compact_text.py` keeps the database at about 87 MB.
4. Copy the build over `three-bases-library.sqlite`, then commit and push after each step together with its progress files, keys and decisions.
5. Update `README.md`. Write a short handoff that says what is done, what the build applies, what is left, and the exact commands.

## Cost guide (measured)
| work | tokens |
|---|---|
| scripts, builds, checks | about 0 beyond the commands |
| one Opus reader, 50 entries | 25k to 30k |
| one agent doing 5 batches | 120k to 150k |
| any subagent, startup and context alone | 90k to 200k |
| Haiku yes/no judging, 560 questions | about 150k |
| Sonnet regex narrowing, 12 patterns | about 100k |

A game added with converter, keywords from fields, patterns and build only costs one chat and no agents.
