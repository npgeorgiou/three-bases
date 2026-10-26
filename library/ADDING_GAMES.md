# Adding a game to the library: cheap and safe

Read this whole file before you add a game.

## Rule zero
- Scripts first. Cards are read only as in "Reading cards" at the end of this file, and only when Kaptain approves.
- Every reading starts with one game: check its answer and report its tokens before reading the next.
- Do not repeat experiments in loops. Before you choose a fix, break the errors down by where they come from (the `method` column).

## 0. Before any pattern: the game's material, then its cards
0.1 **Research the game properly first.** Not 2-4 pages: go through the game's wiki (its rules or gameplay pages, the full
   keyword/status/effect glossary, every faction, class or squad page, the unit/enemy and environment pages) and at least two
   strategy guides or community pages on how it is played (builds, archetypes, combos). Note every mechanic, status, keyword and
   board rule the game has, with the page it comes from. Use the built-in browser for pages WebFetch cannot read (fandom wikis,
   pages behind scripts). This is the checklist the patterns are measured against; a thin checklist hides gaps.
1. From that research, write every mechanic it names,
   with the expected concept and the wording to look for, into the ```mechanics block of `tools/games/<game>.md` (`name|concept|regex`, source URL in
   a comment). Write the real-world cases (section 6) from the same pages now, so tagging and test read the same sources.
2. Read a random sample of about 300 cards in one go (a script prints `name|faction|text`, one line each, about 20k tokens), or
   all cards when the game has fewer than 500. Note the game's wording families ("exhaust a unit", "When Defeated:", "Apply Rage 3")
   and what each does. Guides are a checklist, not the whole game: the sample shows the wording the patterns must read.
3. Convert and load (sections 1-2), write the patterns (section 3) from the sample and the checklist.
4. After the build, run `tools/coverage.py <db> <game> 40 --mechanics tools/games/<game>.md`. It prints, per faction, how
   many cards show each listed mechanic and how many carry the expected concept, and the clauses no pattern reads grouped by their
   first words. A GAP line is a missing pattern or a later build step that removed the tag; a frequent unread clause is a
   mechanic nobody listed. Fix and rebuild (insert-only, two minutes).

## 1. Load
1. Write a converter, `tools/convert/conv_<game>.py`. It outputs JSON in the format described at the top of `tools/load_cards.py`:
   ext_id, name, category, faction, subtypes, cost, stats, text, and `keywords` as a field.
2. Keep the source's keyword lists as a field and set `_keywords_from_field`. Links taken from source fields are trusted; links found by matching text are not.
3. Build with the load: `sh tools/build.sh three-bases-library.sqlite <scratch>/new.sqlite <game>=<cards.json>`.
   - One chain: the new cards are added, their first tags join the frozen base (`start_clean.py keep`), and every
     step runs over all games. The stored database is always the output of one such build; building twice gives identical tags.
     To reload a game, drop it first (`drop_game.py`).

## 2. Keywords before cards
1. Add the game's glossary keywords as category `keyword` entries, each with its definition text.
2. Tag the keywords with patterns, using the concept definitions in `tools/key/defs.txt` and each concept's "Not:" line in `tools/concept_tree_v3.txt`.
3. If the game has more than about 50 keywords, ask Kaptain whether they should be read. If he says yes, read them as in "Reading cards".
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
1. Take the sample with `key.py sample <game>` (500 entries, seed 1; all of a game with 500 or fewer).
2. Read it as in "Reading cards".
3. `key.py answer <game>` checks every quote and writes `key.json`; `key.py credit <game>` then adds the keyword tags (below).
4. Score with `key.py score`.
5. To make patterns from the key, run `tools/step3/key_patterns.py`. It builds on one half of the key, tests on the other half,
   and keeps a pattern only if it is 90%+ right there.
6. To get rid of wrong tags, narrow a pattern only after a sample of what the narrowing drops has been judged 90%+ wrong (`patterns3.py accept`).
   Narrowing cannot fix misses or sibling confusions.

## 4b. Writing a pattern
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
- While working on one game, check each try with `tools/game_check.sh` (`PATTERNS_CHECK.md`). After a tag change that reaches
  other games (shared code, `_all.txt`, the concept tree), and after adding a game, run `compare_builds.py <stored> <new>` (key, real-world cases per game and kind, regression, combos, lost
  pairs, with every case newly met or missed) and keep the change only if nothing is worse; `realworld_why.py` says why a case misses.

## 5. Never
- Never read cards any other way than "Reading cards" below: no reading agents, no batches, no second or third reader.
- Never remove a tag unless it has been judged wrong. Hand reviews in `tools/regression.tsv` win, except where the answer key
  disagrees on what a card does: then the key wins (`tools/key_wins.py`), and payoff and answer tags (`benefits`, `counters`) are never touched.

## 6. Finish
1. All build checks must pass: regression, combos, trigger pairs, query tests, realworld.
2. Make the real-world cases as `tools/realworld/RESEARCH.md` says: a source summary in `tools/games/<game>.md`, then the cases
   in its ```tsv block (signatures, archetypes, combos, splashes in the library's own names). They are the real test: run
   `realworld_why.py` and fix what misses before finishing.
3. Check the database size. GitHub refuses files over 100 MB; the database is stored compact (`compact_text.py`) and without its indexes (`indexes.py`), about 55 MB (`indexes.py` also keeps the frozen base only as its differences from the output).
4. Copy the build over `three-bases-library.sqlite`, then commit and push after each step together with its progress files, keys and decisions.
5. Update `README.md`. Write a short handoff that says what is done, what the build applies, what is left, and the exact commands.

## Lessons from the patterns checks (26 Oct 2026)
- Keyword and glossary entries pass their tags to every card that has them: tag only what the keyword itself does. If the source
  is a wiki page with notes about single cards, the notes' effects belong to those cards, not to the keyword.
- Data that cards print outside their text (costs, types, stats) is read from its field with a data rule (`tools/cost_rules.py`,
  the converter's `tags`), not with text patterns.
- Before writing patterns, see where errors come from (`tools/entry_diff.py`), test candidate lines on the key
  (`tools/pattern_eval.py`), and check that each real-world case shows a lead in the cards (`tools/case_lead.py`). Build once per
  batch, not once per pattern.
- Key quotes must be words of the card. A tag quoted with a definition or with a name that does not say the effect is unverified.
- A combo case can name a card, a merged card (it resolves to the kept entry), a keyword or a tribe: in games where abilities move
  between cards (Inscryption sigils and totems) a combo is "card + keyword" or "tribe + keyword".
- Adding cards to a game that is already in the library: `tools/reload_game.sh <scratch> <game> <game>=<cards.json>`. Never
  `build.sh ... <game>=<cards.json>` for an existing game: its `start_clean.py keep` makes the game's built tags its base and every
  game came out worse (26 Oct 2026). A card with no tag is dropped by `drop_untagged.py`; a card with no text needs a review entry
  keyed by its name. Faction counts include cards merged into another with the same text (`signature.py`).

## Reading cards (Kaptain's decision; the only way cards are read)
**Why there is a key.** The library's tags come from regexes (patterns). The answer key is the only place where cards are
read and tagged by judgement, so it is the only measure of whether the patterns are right: every score (wrong and missed per 100
cards), every pattern accepted or narrowed, and every key-based fix is decided against it. A wrong or empty key tag makes a wrong
pattern look right, or a right one look wrong. So the key must be read with everything needed to understand the cards, and a
gap in the game block is a gap in every score of that game.

**Before reading: no undefined keyword or term.** Every keyword the game has needs a definition in the game block: its entry's
text, or a `# term:` line in the ```mechanics block of `tools/games/<game>.md`. Research each missing one in the game's rules pages and wikis (several
sources if the first lacks it). If no source defines it, write the definition from game knowledge and common sense, marked
`(assumed)` (Kaptain's decision). `key.py read` refuses to write the request while any keyword is undefined.

**Keywords on cards.** A card that has a keyword has that keyword's effects, so its key entry carries the keyword's tags
(without this, a card whose text is only "Skills: Dodge." would be read as empty). `key.py credit
<game>` writes them into the card's entry in `key.json`: a card has a keyword when its source data lists it or when the name stands
where the game prints keywords (start of the text, a line, sentence or clause, or a "Keywords:" list; the name may be in square
brackets), and the tags are the keyword entry's own key tags, quoted with the keyword's name. The added tags are also listed in
the entry's `credited` field, so running `credit` again replaces them. So the keyword entries must be read with their definitions.

Patterns are written from the sample of step 0, the mechanics checklist and the coverage scan; reading every card is not needed
for tagging. Where cards must be read (an answer key, a review, judging a pattern sample), it goes like this:
1. `python3 library/tools/key/key.py sample <game>`: 500 random cards, seed 1 (all cards of a game with 500 or fewer).
2. `python3 library/tools/key/key.py read <game>` writes the one request, `tools/key/<game>/read.txt`: the reading rules, the
   game block and the cards. The game block is everything the library holds about how the game is played: the rules summary
   (`games.structure`, `games.notes`), the keyword glossary (the game's `keyword` entries), factions, card types and tribes, the
   game's mechanics (the ```mechanics block of `tools/games/<game>.md`: the mechanics its guides name, and its rules and terms as `# term:` lines,
   sourced, only facts the pages state), and the concept definitions with their "Not:" lines (`tools/key/defs.txt`). Keep the
   mechanics file as full as the game's rules pages allow before reading. Cards are `<ids>|<name>: <text>` lines; identical cards are sent once.
3. One fresh process reads `read.txt` once and writes `tools/key/<game>/answer.txt`: one line per card line,
   `<ids>|concept:role:exact words;...` (empty after `|` for a card with no mechanic). It opens no other file and nothing else is
   in its context. One process per game; nothing is read twice, so cost grows with the number of cards only.
4. `python3 library/tools/key/key.py answer <game>` checks every quote and concept, lists cards left unanswered, and writes
   `key.json` (`--force` replaces an existing one). Then `key.py credit <game>`. Check the first answer of each game by hand (skipped cards, wrong quotes).
   Coverage cards: `key.py coverage <game>`, then `read <game> cov` and `answer <game> cov`.

## Cost guide (measured)
| work | tokens |
|---|---|
| scripts, builds, checks | about 0 beyond the commands |
| one reading request, 500 cards | about 35k to read (game block about 12k) plus about 15k to 25k of answer |
