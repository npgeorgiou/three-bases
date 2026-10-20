# Adding a game to the library: cheap and safe

Written 20 Oct 2026 from what the tag-fix plan got wrong. Read this whole file before you add a game.

## Rule zero
- Scripts first. Do not use reading agents (readers, judges, narrowers) unless Kaptain approves a measured cost.
- Every reading step runs on one batch first. Report its tokens before going on.
- Do not repeat experiments in loops. Before you choose a fix, break the errors down by where they come from (the `method` column).

## 0. Before any pattern: the game's material, then its cards
1. Read 2-4 guide or wiki pages per game (faction overviews, keyword glossary, rules summary). Write every mechanic they name,
   with the expected concept and the wording to look for, into `tools/mechanics/<game>.txt` (`name|concept|regex`, source URL in
   a comment). Write the real-world cases (section 6) from the same pages now, so tagging and test read the same sources.
2. Read a random sample of about 300 cards in one go (a script prints `name|faction|text`, one line each, about 20k tokens), or
   all cards when the game has fewer than 500. Note the game's wording families ("exhaust a unit", "When Defeated:", "Apply Rage 3")
   and what each does. Guides are a checklist, not the whole game: the sample shows the wording the patterns must read.
3. Convert and load (sections 1-2), write the patterns (section 3) from the sample and the checklist.
4. After the build, run `tools/coverage.py <db> <game> 40 --mechanics tools/mechanics/<game>.txt`. It prints, per faction, how
   many cards show each listed mechanic and how many carry the expected concept, and the clauses no pattern reads grouped by their
   first words. A GAP line is a missing pattern or a later build step that removed the tag; a frequent unread clause is a
   mechanic nobody listed. Fix and rebuild (insert-only, two minutes).

## 1. Load
1. Write a converter, `tools/convert/conv_<game>.py`. It outputs JSON in the format described at the top of `tools/load_cards.py`:
   ext_id, name, category, faction, subtypes, cost, stats, text, and `keywords` as a field.
2. Keep the source's keyword lists as a field and set `_keywords_from_field`. Links taken from source fields are trusted; links found by matching text are not.
3. Build with the load: `sh tools/build.sh three-bases-library.sqlite <scratch>/new.sqlite <game>=<cards.json>`.
   - Loading is insert-only (`add_games.py`): the steps run on a copy holding only the new games, their rows are added, and the
     build stops if any existing row changed. To reload a game, drop it first (`drop_game.py`).
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

## 4b. Writing a pattern (what went wrong on 19-20 Oct 2026)
1. **Find the wording on the cards first, in every game.** Before a pattern, scan all texts for the word family (for example
   double/twice/extra/additional/more; exile/banish/consume/devour/obliterate) and group the hits by the phrase around them, per
   game (`tools/step3/amp_patterns.py scan` does this). Write the pattern only from phrases you saw. Never assume one game's
   phrasing is the only one: "would ... instead" is Magic only; Runeterra says "traps ... are doubled", Hearthstone "trigger twice".
2. **Cover every grammatical form.** Active and passive ("when you draw" / "when drawn" / "is drawn"), first person ("when I'm
   discarded", "when I block"), every subject ("you", "the player", "an opponent", "your hero/leader/general/nexus"), every starter
   ("when", "whenever", "the first time", "each time", "after"), and any quantity ("draw cards", "draw 10 cards"). Test the
   pattern on a list of such sentences before using it.
3. **Keep look-alikes out, and say why in the file.** "gain block" is armor, not blocking; "pick targets" is not being targeted;
   "exile ..., then return it" is blink, not sacrifice; "this card's damage is doubled" doubles itself, not other cards.
4. **Own side vs enemy is a different concept.** Exiling an enemy is banish; exiling your own unit as a cost is sacrifice.
5. **Doing vs paying off.** A card that rewards something (an amplifier, "whenever you lose life") gets that concept with role
   `benefits`; the answer key only reads what a card does, so a key-based step must never remove `benefits` or `counters` tags.
6. **Read 20 random matches per pattern and game**, and drop the pattern where it is below 90% right (on the key where it has 3+
   key matches). Print the samples; do not judge from counts.
7. **A new concept needs three things**: a line in `tools/concept_tree_v3.txt`, its id in `tools/key/added_concepts.txt` (the key
   never had it, so the scorers skip it), and, for a trigger, an entry in `FEEDS` in `tools/query.py` (what sets it off), or the
   connection search will not use it.
8. **Switching a pattern off can remove the only tag a card has.** Before switching off, check whether the matches are right for
   another concept and point the pattern there (`tools/step3/switch_off.py` does this).

## 4c. Build hygiene
- One build at a time. Before starting another, make sure no `build.sh` and none of its python steps still run: two writers
  corrupt the scratch database ("disk I/O error", "malformed").
- A build step that adds tags must respect the reviewed drops. Steps after the tree move only pair or remove
  (`trigger_pairs.py <db> pairs_only`).
- Scripts that rewrite `tools/step3/decisions.tsv` must keep the other scripts' lines (each script marks its own: `|key`, `|trigger`,
  `|amp`, `|redirect`, `|manual`).
- After any tag change run all of: `regression`, `combo_check.py`, `realworld.py -v`, `realworld_why.py`, `lost_pairs.py <old> <new>`,
  and compare real-world cases one by one, not only the totals.

## 5. Never
- Never run more than 3 or 4 agents at once. Rate limits killed every larger batch.
- Never let agents share helper scripts in a common scratchpad. They overwrite each other.
- Never judge with Opus. Use Haiku for yes/no questions and Sonnet for regexes.
- Never read cards in a chat agent when a stateless batch script can do it (section "Reading cards cheaply").
- Never start an agent without a progress file it saves after each batch and can resume from.
- Never remove a tag unless it has been judged wrong. Hand reviews in `tools/regression.tsv` win, except where the answer key
  disagrees on what a card does: then the key wins (`tools/key_wins.py`), and payoff and answer tags (`benefits`, `counters`) are never touched.
- Never put more than 60 to 80 questions in one judging file.

## 6. Finish
1. All build checks must pass: regression, combos, trigger pairs, query tests, realworld.
2. Add at least 30 real-world cases with source URLs to `tools/realworld/<game>.tsv` (signatures, archetypes, combos, splashes;
   card names exactly as the library stores them). They are the real test: run `realworld_why.py` and fix what misses before finishing.
3. Check the database size. GitHub refuses files over 100 MB; the database is stored compact (`compact_text.py`) and without its indexes (`indexes.py`), about 70 MB on 20 Oct 2026.
4. Copy the build over `three-bases-library.sqlite`, then commit and push after each step together with its progress files, keys and decisions.
5. Update `README.md`. Write a short handoff that says what is done, what the build applies, what is left, and the exact commands.

## Reading cards cheaply (if a step ever needs it)
Patterns are written from the sample of step 0, the mechanics checklist and the coverage scan; reading every card is not needed
for tagging. Where every card must be read (an answer key, a review), use the bulk reader, not chat agents:
- One request = the game block + up to 500 cards, sent once. The game block is the game's rules summary, keyword glossary,
  factions and the concept definitions with their "Not:" lines; the cards are `id|text` lines (identical texts sent once). The
  answer is one line per card, `id|concept:role:quote;...`, which `key.py check` verifies. About 120 requests cover the library.
- Each request is independent, so nothing piles up: cost grows with the number of cards, not with their square. The game block
  is cached by the API and paid in full once per game.
- Check the first request of each game by hand (skipped cards, wrong quotes) before sending the rest; make batches smaller only
  if the end of a 500-card answer is worse than its start.
- It runs as a script on the Anthropic API (Message Batches API: half price, a small model for yes/no judging), so it needs an
  API key and costs API money instead of chat tokens. The chat workspace has no key.
Why not chat agents: an agent is a conversation. Before its first card it holds its system prompt, tool definitions, instructions
and the files it reads (the concept tree file alone is about 51 KB), the measured 90k-200k start-up; every card it reads and every
tag it writes stays in the conversation and is re-sent at every later step, so each card costs more than the one before.

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
