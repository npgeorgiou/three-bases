# Tagging per effect

## Reading test: Runeterra (agreed with Kaptain, 27 Oct 2026, evening)
Done 28 Oct 2026: Runeterra fully described, 247 of 247 case tests pass (`library/cards_db/RESULTS.md`). Next games
follow `library/cards_db/GUIDE.md`; files and rules in `library/cards_db/README.md`. The sections below are history.
- Runeterra is read completely, by reading, in a table of fixed values (no free text), keywords described once by their effect
  and inherited by every card, created cards, keywords and tribes as links to their entries.
- The table and its value lists are made perfect gradually while reading: when a card does not fit, the table or a list is
  changed then (new value, new column, clearer meaning), the change is written down with the card that caused it, and the
  cards already read that it touches are corrected before reading on.

## Instructions for the next chat (26 Oct 2026, evening): a library that describes cards
Read this section only; the sections below it are the earlier test and its history.

### What the test found
- The test of "abilities and pieces from existing tags" (sections below, code in `tools/records_test/`) was run on a copy.
  Cutting text into abilities and pieces failed (placement 94.9%, 2 of 21 games at 98%). Grouping tags straight from the
  card (`records_test/abilities.py`: simple cards from their tags alone, the text read only for cards with 2+ triggers) worked
  as grouping: the four known errors come out right, combos found unchanged.
- But Kaptain read the Runeterra results and every tag set was unreadable as a description: the tags are search labels made
  by word patterns ("draw" fires on "when you draw", "random_effect" on any random unit, "cost_condition" says nothing useful),
  and they carry no target, amount or duration (the record schema was dropped on 26 Oct morning). Grouping labels cannot make
  them describe a card. The answer-key scores measured whether each label is defensible, not whether the labels describe the
  card. Lesson: say this kind of limit before building, not after.
- The current library stays good for finding cards by mechanic; it cannot explain a card.

### Agreed (Kaptain, 26 Oct 2026)
- Goal: a library that describes cards, queryable to find combos, mechanics, ideas and possibilities.
- Cost is measured in tokens of Kaptain's Claude subscription (no API). Reuse as much as possible, read as little as possible.
- One record per effect: card, ability, trigger, effect, who it hits (self, ally, enemy, all, random, ...), how much, how long,
  condition. Accepted error: about 95% of records right on a hand-checked sample.
- Games: Age of Sigmar dropped; 40k kept, trimmed; Inscryption kept without its wiki prose; Darkest Dungeon kept (its stat
  lists are easy for scripts). Done and pushed: `tools/trim_text.py` (a build step), `drop_game.py --category`.
- Distinct text left: about 1.17 million tokens (texts that differ only in name or numbers counted once); Magic is two thirds
  of it, and its fixed wording should let scripts cover most of it.

### Plan (Claude's proposal, steps 1-4 agreed as preparation)
1. Record format: a table `effects(entity, ability, trigger, effect, target, amount, duration, condition, source)`; source =
   keyword / script / reading. Write the exact value lists for target and duration first and show them to Kaptain.
   Done: lists agreed (Kaptain, 26 Oct 2026), in `tools/records/common.py`; `tools/records/check_records.py` checks files.
   "this round" in Runeterra is often a condition ("if an ally died this round"), not a duration.
2. Keywords first: about 1,000 keyword definitions read once into records; every card with a keyword inherits them.
   Done (27 Oct 2026): `tools/records/keywords/<game>.txt`, 831 records. Three kinds: effect keywords (full record), trigger
   keywords (Battlecry: trigger only), condition keywords (Combo: condition only). No record for the 228 keywords with no
   definition text (Magic 113, Monster Train 66, Shadowverse 31, Battlegrounds 16, Legends 2), for Magic's Scry (its text is
   a snow-mana line) or for glossary entries (Darkest Dungeon stats and provisions).
3. Started: `tools/records/script_records.py`, Hearthstone wording (18% of cards covered, 1 wrong record in a 30-card check).
   Kaptain (27 Oct 2026): reading costs too much; the vast majority of cards of ALL games must get records by script, using the
   patterns as far as they go, plus new ones. `tools/records/auto_records.py` (every game): sentences of the text, trigger and
   effect from the stored tags' patterns (all patterns of the game when no tag matches), keyword verbs and grants from the
   keyword records, a cross-game target phrase table, amounts, durations, conditions; Darkest Dungeon has its own format reader.
   Result 27 Oct: 50-89% of entries covered per game (Magic 66%, Hearthstone 76%, Lorcana 84%), but a hand check of 48 covered
   cards (Magic, Hearthstone, Lorcana, Gwent) found only about 60% of records right (wrong target or wrong effect most often).
   The strict Hearthstone script was 97% right at 18% coverage.
   Agreed (Kaptain, 27 Oct 2026, night): rows built mostly from the tags (trigger and effect tags; side from the tree, helps my
   side or hurts the enemy; how many from the scope tags; duration words), the text for numbers and to override the side, the
   target read first inside the words the pattern matched. The five games with the patterns check done (Into the Breach,
   Inscryption, Faeria, Duelyst, Darkest Dungeon) first; then the fixed-wording games (Hearthstone, Lorcana, Magic, Star Wars
   Unlimited, Runeterra, Legends, Gwent) with the effect from their wording first and tags as backup; a game whose tags make the
   rows wrong gets its patterns check; 40k, Shadowverse, Marvel Snap, Monster Train last. No tag changes, no reading run.
   `tools/records/key_score.py`: the effect field against the hand answer keys (tools/key/<game>/key.json), no reading needed;
   27 Oct night: effect precision 67-94% per game (Faeria 94, Darkest Dungeon 88, Shadowverse 87, Hearthstone 80, Magic 78),
   recall 39-79%. Targets are checked by hand (about 20 covered cards per game).
   Agreed later (Kaptain, 27 Oct 2026, morning): the card text is the only truth; tags, the key, keyword rows and patterns are
   hints. `tools/records/build_records.py`: each tag placed at the words it stores; a row where hints agree and the words
   support it (in the five checked games a pattern alone is only "maybe:"); keyword rows only for keywords the text names;
   new columns shape (row, line, lane, adjacent, ranks...) and extra (every other concept, card facts, traits), so no tag is
   dropped silently. Checked by reader agents: 50 random + 50 complicated cards per game, stored as fixed test sets
   (`tools/records/tests/<game>.json`, scored by `testset.py score`). Five checked games, 27 Oct morning:
   first reader pass (before fixes): cards fully right ITB 9, Inscryption 61, Faeria 22, Duelyst 24, Darkest Dungeon 31 of ~100;
   after fixes, scored against the test sets: 25, 67, 37, 41, 63 of 100; expected rows met 70, 80, 72, 75, 89%.
   Tags found nowhere in the rows: 15 of 1197, 52 of 769, 37 of 1779, 66 of 2630, 135 of 5564.
   Main errors left: who is hit in long or unusual sentences, wiki prose (ITB) and "Choose one" cards; the test sets carry
   the reader's own mistakes (some expected targets are wrong), so a second reader pass is needed for a true number.
   27 Oct, late morning (Kaptain: ask the questions per card; fix tags, key, keywords and test cards that are surely wrong):
   `tools/records/clauses.py` cuts each sentence into clauses (one per verb) and answers when / what / who / how much / how
   long / condition from each clause; tags make "what" narrower and fill what no clause answers where their own pattern also
   matches. Keyword rows: a card has a keyword only where the keyword opens a line; it is given only after give/gain/grant
   ("summon a 1/2 with Zeal" describes the new card); sigil names match their base ("Green Mox" is Mox Sigils).
   Second reader pass (same 100 cards): fully right ITB 3, Inscryption 67, Faeria 28, Duelyst 43, Darkest Dungeon 41.
   Test sets rebuilt from it; after this round's fixes: 7, 72, 48, 52, 67 of 100 right; expected rows met 58, 78, 72, 73, 94%.
   Tags found nowhere in the rows: 30/1197, 57/768, 40/1779, 92/2630, 13/5556.
   Sure fixes: 8 Darkest Dungeon area-damage tags on skills that deal no damage (reviews, the game's pattern and the step-3
   decision now need "deals damage", not -100%), 5 of them in the key too; Inscryption Skinning Knife "immunity" (from cut wiki
   text). Into the Breach stays low: its wiki prose repeats and describes, and needs its own reading rules.
   Scripts per game: the effect from today's patterns, plus new patterns for target, amount and duration. A card the script
   covers completely is not read. Start with the games with fixed wording (Magic, Hearthstone, Runeterra, Lorcana, SWU).
4. Repeats read once: texts that differ only in name or numbers share one reading.
   Done: `tools/records/repeats.py`; reminder text is left out where the patterns leave it out (Magic, Lorcana, Star Wars
   Unlimited). 50,243 distinct texts, about 1.64 million tokens.
5. Trial, per game: about 25 hard cards (most triggers, most tags, longest distinct text) and about 5 ordinary ones, so the
   estimate can weight each kind by how many cards a game has (hard cards alone would overstate the cost). Measure: share the
   scripts cover, tokens per read card, error rate (checked by reading). Then the full estimate is arithmetic. Present it.
6. Full run in batches per game; results saved as files, loaded by a script, pushed after Kaptain's OK.
7. Check: about 20 hand-read cards per game, `combos.tsv`, and the six fixed questions (step 3 of the earlier test) on old and new.
8. Queries: new `query.py` commands over the records (combo = A's effect on a target matches B's trigger on that target).

### Learnings from the five checked games (27 Oct 2026; use them for every next game)
Measured on the 500 reader-checked cards: a game's current effect tags cover 87-92% of what the reader says the cards do
(Inscryption 81%), and 73-77% of them are right once property concepts are left out (ranged, rank_positions, placement_rules,
items_consumables, drawback, saving_throws: what a card is, not what it does). The tags are the best source for "what".
What worked:
1. Placing each tag at the words it stores (ev_pos), then reading who / how much / how long from those words.
2. Keyword rows copied from the keyword records, but only where the keyword opens a line of the card; "give/gain/grant X"
   makes a row for the receiver; "with X" after summon/create describes the new card; "X minions" is a tribe word.
3. A fixed-format reader where the source has one (Darkest Dungeon skills and stat lines: 94% of expected rows).
4. Reader agents (cheap model, the brief in the check folder) on 50 random + 50 complicated cards, stored as test cards;
   every change re-scored by script, no reading.
What did not work:
5. Own verb lists that ignore the tags: the clause reader added rows from prose (Into the Breach fell from 25 to 7 right).
6. Accepting a wording pattern alone in games whose tags were redone: patterns overfire where the tag pass removed them.
7. Trusting keyword links: wrong in the checked games too (Conscript "with Zeal", Mother of All Yaks' Yak Guards).
8. Scoring against the first reader pass: its expected rows carried the old rows' conventions (+2/+2 as two rows).
Do next time, in this order:
A. Rows from the tags first: one row per effect tag, at its stored words; the clause questions only fill who, how much, how
   long and condition from those words. A clause makes a row of its own only for a verb no tag covers, and only in a short,
   rule-like sentence (not wiki prose, not game_rule / terrain pages).
B. Use the patterns' matched span as the clause: the object after the span is "who", the numbers inside it "how much".
C. Properties (ranged, rank_positions, placement_rules, items_consumables, drawback, saving_throws, cost_type) go to extra.
D. Mine patterns from the checked cards: every reader-confirmed row and every hand-review tag with its words is a candidate
   wording; run it on the game (tools/pattern_eval.py) and add it to the game's pattern file when it stays right. Not done yet.
E. Fix sure errors where they live: tags through reviews/<game>.json or the game's pattern file (a direct database edit is
   lost on the next build), step3/decisions.tsv when a "new" pattern came from a wrong key, the key itself, the keyword file.
   Check with tools/game_check.sh that the fix survives a rebuild (an old review "add" can put the tag back).
F. Into the Breach: its tags cover 92% of the reader's effects and 76% are right; pour the tags into rows (A) and drop own
   clause rows there, instead of more reading rules.
Mistakes Claude made (27 Oct; do not repeat):
- Built a whole method before showing 5-10 real cards, and started work without a clear order from Kaptain.
- Trusted the answer key as truth (it is often wrong) and scored against it.
- Wrote own verb lists instead of using the patterns' matched spans; asked the questions only indirectly.
- Threw away tags that carry who / how many (random_target, scope_self, aoe_damage, adjacency) as "noise".
- Did not run the library's _all.txt patterns at first.
- Explained in internal jargon (coverage, precision, recall) instead of plain words with a card.
Not done yet (open, in this order):
1. Rebuild the five games with A-C above (tags first, clauses only fill fields), then re-score with testset.py.
2. Fix the rest of the second reader pass's findings (check2 *.out.jsonl in the session's scratch folder are gone with the
   session; the stored test cards in tools/records/tests/<game>.json hold the corrected rows).
3. Mine patterns from the checked cards and the hand reviews (D).
4. Fix the wrong keyword links in the build (kw_links.py), not only in the records: a card has a keyword only where it opens
   a line; "with X" after summon/create and "X minions" are not the card's keyword.
5. Open readings: long sentences with two subjects ("Its controller gains ... and draws 2"), "Choose one" cards, Into the
   Breach wiki prose.
6. Then the other 15 games, in the order of step 3 (fixed-wording games first).

### Patterns check (PATTERNS_CHECK.md)
The four games done are reused as they are (better labels = better trigger and effect fields). Do not run more game passes
before the trial: the passes improve labels, not target, amount or duration, and read cards get their whole record from the
reading. If the trial shows wrong labels are a main source of wrong records, run the patterns check on the games where it hurts.

### How to work with Kaptain here
- Explain plainly with a card example; no internal jargon (no "pieces", "spans", "excerpts" without saying what they are).
- Show real cards and results early (5-10 cards), before building on a method.
- State what a method cannot do before building it.

## Agreed with Kaptain (26 Oct 2026, morning; the earlier test)
- **All or nothing.** A new structure is built for every entry of every game, or not at all. No mix of entries with and
  without it. It is built in a copy of the database; the real one is replaced only when the whole test below passes.
- **The full record schema below is not pursued now.** Its slots (filters, amounts, which one, area, duration) need new
  pattern sets for every game, a second round of the pattern work, and its feasibility for the prose games is unproven.
- **What is tested instead** (Claude's suggestion): abilities and effect pieces built only from what exists: the tags, their
  stored text positions, the patterns that made them, and generic rules. No new patterns per game, no new tagging.
- Filters ("the next Jump creature") are left out for now. Wrong tags such as Triton Trainer's movement stay until a review.

### The structure under test
- New table `abilities(id, entity, ord, ev_pos, ev_len, kind)`: one row per ability of an entry, cut at sentence ends,
  line breaks and keyword prefixes (Gift, Battlecry, Deathrattle, Deploy, Last Words, "When/Whenever/At", "{T}:").
  Keywords in a keyword list are one ability each. Kind: keyword, triggered, activated, static.
- New table `pieces(id, ability, ord, ev_pos, ev_len)`: an ability cut at "and" / "then" only when a new effect tag or a
  new number follows ("deal 2 to a random enemy" | "1 to all adjacent ones"). Not cut where "and" joins targets or
  conditions.
- `entity_concepts` gets the columns `ability` and `piece`. Each tag's own pattern is re-run inside its stored span to find
  the exact matched words (wide spans like Wild Avenger's "taunt, dash 2 this gains ..." get narrowed), and the tag goes to
  the ability and piece holding them. A piece without its own effect tag inherits the previous piece's effect. Tags from a
  keyword go to that keyword's ability.
- Computed instead of stored: trigger pairs form only inside one ability (replaces the cross product in `trigger_effect`);
  compound tags (aoe_damage, random_target damage, temporary_buff, permanent_growth, scope_*) form only inside one piece.
- Limits: no amounts, filters or areas by distance beyond existing concepts; where sentences are cut badly (prose
  games) abilities are cut badly.

## The test (all 21 games; one failing game fails the whole test)
Pass numbers are Claude's suggestion.
1. **Does it fly (script only).** Per game: share of tags placed in exactly one ability and piece, tags placed nowhere,
   abilities with no effect tag, pieces holding two different effects, trigger pairs before and after.
   Pass: 98%+ of tags placed in every game; outliers few enough to read.
2. **Is it accurate.**
   - Gold sample: per game 10 random entries + 5 targeted ones (modal "choose one", "would ... instead", "for each", X
     costs, multi-sentence text, keyword lists; Spire intents, Darkest Dungeon skills, 40k/AoS ability blocks where the game
     has them), 315 entries. For each, the correct ability and piece cuts, the piece of each tag and the correct trigger
     pairs are written down once (checking reads, not tagging) in `tools/records_test/gold/<game>.json`. Pass: 95%+ of tags in
     the right piece, and trigger pairs right, in every game.
   - The answer key (`tools/key/<game>/key.json`, all 21 games): precision and recall of the computed compound tags against
     the key, compared with today's (`concept_precision`). Pass: no concept worse in any game.
   - Known errors must come out right: Wild Avenger, Invincible, Mortarion, Buzz Lightyear - Jungle Ranger (section "The
     problem" below).
3. **Does it answer questions better.** Old and new database, same questions:
   - `tools/combos.tsv` through `query.py combo`: at least as many known combos found; a sample of found links checked for
     false ones.
   - Six fixed questions: random-target damage; trigger on own unit's death that summons; temporary attack gain on summon;
     growth on a per-turn trigger; engine pairs inside one faction; a three-card chain in one game. Top 3 results per game
     per question are checked by reading (up to 378 rows). Pass: more correct results than today in every game where the
     question has answers.

## Instructions for the chat that runs the test
- Library task: clone as CLAUDE.md says, then `git sparse-checkout disable`. Read only this section and "The structure
  under test"; read code only where the task needs it (`tools/trigger_pairs.py` for the current sentence split,
  `tools/compact_text.py` for evidence positions, `tools/query.py` for `connections`/`combo`).
- Work on a copy: `cp library/three-bases-library.sqlite <scratchpad>/records.sqlite`, and point the tools at it with
  `TB_LIB`. Never write to the real database; push only code and test files.
- New code goes in `tools/records_test/` (one script per step: build abilities and pieces, place tags, compute pairs and
  compounds, report). Steps 1, 2 (key part) and 3 (combos part) are scripts; write their per-game numbers to
  `tools/records_test/REPORT.md`.
- Gold sample: a script picks the 315 entries with a fixed seed and lists them; Claude writes the gold files in batches per
  game, reading only each entry's text. Then the script scores against them.
- Reading budget: gold entries, the outliers from step 1, the top-3 results of step 3. Nothing else is read entry by entry.
  Before the gold reading starts, tell Kaptain the outlier count and an estimate of the reading left, and wait.
- At the end: the report per game with pass or fail per step, and a one-line verdict. Present it to Kaptain before anything
  goes into the real database.

## Earlier proposal (Claude, 26 Oct 2026; not pursued, kept for reference)

## The problem
A card's tags are one flat list. Nothing says which tags belong to the same effect, so the library glues facts together with
compound concepts: `aoe_damage` (damage + many targets), `multi_target_attack`, `random_target`, `temporary_buff` (stat gain +
this turn), `permanent_growth` (stat gain + again and again + kept), `in_hand_buff`, `friendly_fire`, `scope_self`. That only
works for the combinations someone gave a name: an area lock (Taunt) or an area stat loss has no tag, and a card with two effects
mixes them up.

The library's `trigger_effect` table was meant to keep the pairs, but it is the cross product of every trigger and every effect
it finds in a sentence or paragraph. What it holds today (live examples):
- Wild Avenger (Faeria), "Taunt, Dash 2 / This gains +0/+1 for each time you've been dealt damage this game": on_play -> taunt,
  on_play -> immobilize, on_play -> forced_movement, on_play -> attack_gain. Taunt is not summon-timed, Dash moves its own
  creature, and +0/+1 gains no Attack.
- Invincible (Hearthstone), "Reborn. Battlecry and Deathrattle: Give another random friendly Undead +5/+5 and Taunt": on_play ->
  death_trigger, on_play -> revive, death_trigger -> summon.
- Mortarion (40k): one keyword list ("Special rules: Blast, Deadly Demise, ...") paired with every trigger: aura -> damage,
  death_trigger -> play_restriction, buff -> piercing.
- Buzz Lightyear (Lorcana): Shift (an alternative cost) became activated -> revive and activated -> discard.

## The idea
Tag each effect of a card as one record with fixed slots. The flat tags stay, but they are derived from the records, so search,
signatures, archetypes, combos and the key keep working while the records are built.

### A card
A card has abilities; a keyword is an ability other cards reuse. Each ability has:
- **zone**: where it works: in play (default), hand, deck, hand or deck, discard pile, anywhere.
- **kind**: static (always on), triggered, activated, replacement ("would ... instead"), cost or play rule.
- **trigger** (triggered only): the event (summoned, dies, attacks, is dealt damage, turn start or end, a card is played, a
  card is drawn, a god or player is dealt damage, moves onto a tile ...) and a filter on the event's object: whose (own, enemy,
  any), what (this, a unit, a Yak, a Jump creature, an event, a creature with higher Attack than Life).
- **condition**: a gate ("if you attacked a god this turn", "while you control 2 lakes", "first time").
- **cost**: what is paid (faeria, life, sacrifice a creature, damage to this, discard, exhaust/tap).
- **frequency**: once (per card), first time, once per turn or round, every time the trigger fires.
- **effects**: one or more records, in order, each linked to the one before: and, then, if you do, instead, for each.

### An effect record
- **verb**: what happens: damage, heal, stat change, destroy, remove (exile, swallow), return to hand, draw, discard, create
  card, summon, transform, copy, move, lock (can't move or act), grant (a keyword or an ability), gain resource, change cost,
  change land, win or lose life ...
- **stat** (stat change): attack, defence, both, other (lore, armour); **sign**: up, down, set, double, swap.
- **amount**: a number, X from a count now (cards in hand, lakes you control), a count over the game (times you were dealt
  damage), a stat of something ("equal to its Life"), random range, or unbounded.
- **target**: side (own, enemy, both), kind (unit, structure, god/player, card in hand, deck, discard pile, land, the new card or
  unit just made), and **selection**: self, the trigger's object ("it", "that creature"), chosen (how many), random (how many),
  all.
- **area** (selection all, or anything spatial): none, adjacent, a line or shape, a row or lane, within a distance, whole board.
- **duration**: instant, this turn or round or phase, until a condition, while the source is in play, lasting.
- **payload** (grant, create, summon, delayed effects): the ability or card the effect makes, itself made of abilities and
  records. "Give the next Jump creature you summon +1/+1" is an effect whose payload is a one-shot triggered ability.

## What the old concepts become
Most compound concepts become questions over one record (or one ability), so they cannot be mixed up between effects:
- `aoe_damage`: verb damage, selection all (or a shape) with more than one target. `area_effect` (new, any verb): selection
  all within an area, more than one target. Taunt: static; verb lock (and "must attack this"); target enemy units, all,
  adjacent.
- `multi_target_attack`: verb damage, selection chosen, 2 or more. `random_target`: selection random.
- `scope_self` / `scope_multi` / `scope_global`: selection self / several / all with area whole board.
- `friendly_fire`: a harmful verb whose target side includes own (Famine: damage 1, both sides, all).
- `temporary_buff` / `temporary_effect`: duration this turn, round or phase.
- `permanent_growth` (call it growth): verb stat change up, target self, duration lasting, frequency every time (or a
  turn trigger). The stat tags come from the stat slot, so "repeated, kept, which stat" are three slots of the same record and
  never mix with the card's other effects.
- `in_hand_buff`: target kind card in hand or deck with a beneficial verb, or an ability whose zone is hand or deck and whose
  record targets self (Zealous Crusader, Firebringer, Soul Eater).
- `cost_reduction` / `cost_set`: verb change cost, sign down / set. `cost_type` and `life_payment`: from the cost slot.
- `condition_count` / `count_payoff`: the amount source (a count now / a count over the game).
- `on_kill`, `on_ally_play`, `on_enemy_enter`, `other_death_trigger`, `death_trigger`: trigger event plus whose.
- `delayed`: an effect whose payload is a later trigger. `in_hand_buff` vs `delayed` (Triton Trainer) stops being a judgement.
- What a card benefits from stays a separate list (`benefits`, `counters`), as now.
The tree keeps its outcome groups (what a player gets); the leaves under them that only combine two slots stop being stored.

## Does it work? Cards with many tags
Each card written as records (Claude's reading), then what the model needed.

**Wild Avenger (Faeria)**: "Taunt, Dash 2 / This gains +0/+1 for each time you've been dealt damage this game."
- Taunt (keyword ability, static): lock + must-attack-this, enemy units, all, adjacent.
- Dash 2 (keyword, trigger summoned): move, self, 2 tiles in a line.
- Static: stat change up, defence, amount = count over the game of "you were dealt damage", self, lasting.
Derived: taunt, immobilize, area_effect, adjacency, movement, on_play, defence_gain, count_payoff, scope_self. Not attack_gain,
not growth (it is computed, not gained again and again; today's key says growth: a key question the slots make visible).

**Firebringer (Faeria)**: "This gains +1/+1 whenever you summon a creature with higher Attack than Life (while in your deck or
hand)." Zone hand or deck; trigger summoned, own, filter Attack > Life; every time; stat change up, both, +1, self, lasting.
Derived: on_ally_play, stat_condition (the filter), in_hand_buff, growth, attack_gain, defence_gain, scope_self. All seven come
from one record; today they were seven separate judgements.

**Triton Trainer (Faeria)**: "Gift - Give the next Jump creature you summon +1/+1." Trigger summoned (self); effect grant with
payload: trigger summoned, own, filter has Jump, frequency once; stat change up both +1 to the trigger's object.
Derived: on_play, delayed, on_ally_play, attack_gain, defence_gain. Jump is a keyword filter, not a tribe: no tribal.

**Shozen, the Sky Eater (Faeria)**: "The first time Shozen would kill a creature in combat, instead swallow and gain control of
it." Replacement; trigger would kill in combat; frequency first time; effects: remove (until Shozen dies) the trigger's object,
then take control of it. Derived: on_kill, removal, steal. The "instead" kind keeps destroy away, which today needed a review.

**Doomgate, Door to Oblivion (Faeria)**: activated; cost sacrifice an own creature; effects: draw 1, and stat change up defence
+2 self lasting. Static: condition this has 13 Life or more; effects: destroy self, then summon Ostregoth here. Derived:
activated, sacrifice (cost), draw, defence_gain, growth (repeatable activation), stat_condition, self_destruct, summon. The
Annoying Gnat combo is a cost slot (sacrifice) meeting a trigger (dies): exact, not a guess from two flat lists.

**Invincible (Hearthstone)**: "Reborn. Battlecry and Deathrattle: Give another random friendly Undead +5/+5 and Taunt." Reborn
(keyword: when it dies the first time, return it with 1 Health). One ability with two triggers (summoned, dies) sharing the
records: stat change up both +5 and grant Taunt; target own, Undead, random 1, not self. Derived: on_play, death_trigger,
cheat_death, random_target, attack_gain, defence_gain, tribal, taunt (grants). Gone: revive and summon from the wrong pairs.
Needed: an ability may list several triggers.

**Magtheridon (Hearthstone)**: Dormant (keyword: can't act until a condition); trigger summoned: summon three 1/3 Warders on
the enemy side; nested ability on those Warders' deaths (all three): destroy all minions, both sides, then end Dormant.
Needed: a condition over several made units ("when they die") and a target side that differs from the owner's
(enemy_benefit, from summon + side enemy).

**Dagon: Promised (Gwent)**: Deploy: grant to 5 units in your deck the ability "Deathwish: stat change up 2 to the lowest-power
own unit; worship Dagon"; summon (spawn) Call of the Depths into the discard pile. Order (activated, cooldown): consume an own
unit (remove it, gain its power). Triggered, every time an own Deathwish unit is played: +1 to it. Zone hand or deck: after you
win a round, evolve. Needed: payload abilities on other cards (the 5 infused units), a selection "lowest power" (selection by
stat: stat_condition), and a zone condition for the evolve.

**Buzz Lightyear - Jungle Ranger (Lorcana)**: Shift 5 is a play rule (alternative cost, on top of a Buzz Lightyear): cost slot,
not an activation. On summon: return an action card with cost 7 or less from your discard pile to your hand. Every time you play
an action: chosen character, stat change up lore +1, this turn. Derived: cost_type, upgrade, recycle (graveyard to hand),
cost_condition, on_spell, stat_gain (lore), temporary_effect. Gone: revive, discard.

**Mortarion (Warhammer 40k)**: end of your Movement phase: for each enemy unit within 6", roll (random), on 3+ D3 mortal wounds:
damage, enemy units, all within 6" (area: distance), amount random, chance. Static while 1-6 wounds: own attacks -1 to Hit
(condition_life, drawback). Each keyword in "Special rules" is its own keyword ability, not paired with every trigger.
Needed: area by distance, chance as part of the amount, phases as turn parts.

**The Legend of Kyoshi (MTG)**: chapters I, II, III are triggers "lore counter reaches N" (delayed, by counter). I: draw, amount
= greatest power among own creatures. II: change land (Earthbend), amount = cards in hand. III: remove self, then return it
transformed. Back face: static, own lands, all: grant trample and hexproof; mana ability (activated, cost tap): gain resource,
amount = greatest power. Needed: the two faces as two cards (they are), counters as a trigger.

**Psion Abomination (Into the Breach)**: static aura: all other Vek (enemy side from the player's view), all, whole board: stat
change up Health +1; grant Regeneration; grant "explode on death" (payload: dies -> damage, adjacent, all). Derived: aura,
area_effect, defence_gain, regeneration, death_trigger (granted), aoe_damage (granted). Today the explosion counts as its own
death trigger; the payload keeps it on the Vek it is given to.

**Awakened One (Slay the Spire)**: an enemy with an intent list: each intent is an ability (trigger: chosen intent) with its
records: Slash damage 20; Soul Strike damage 6, four times (repeat count, which is multi_attack); Sludge damage 18 plus the debuff
the library lists; Rebirth, which the library lists as unknown (from general knowledge, Claude: the second phase, revive at full
health). Needed: a repeat count on a record (hits x4).

## What the cards showed
- The slots above were enough for every card once five things were added: several triggers per ability, a repeat count per
  record, area by distance, chance or dice as part of the amount, and payload abilities (granted, delayed, on made units).
- Every wrong pair in today's `trigger_effect` came from mixing abilities; none needed a judgement once the ability boundary
  was right. The boundary is the hard part, not the slots.
- Several key questions of the Faeria pass become slot facts instead of opinions (Wild Avenger growth or count, Triton Trainer
  delayed, Swallow removal or merge, Aquatic as placement plus self-destruct).

## How it would be built
1. **Ability boundaries**: split the text into abilities: keyword lists, "Keyword - " prefixes (Gift, Last Words, Production,
   Battlecry, Deploy, Order), "When/Whenever/At", activations ("{T}:", "Activate -", "Order:"), replacement ("would ...
   instead"), quoted granted abilities (payloads). The clause splitter in `reading.py` is the starting point.
2. **Slots by small shared pattern sets**, one per slot, not per concept: triggers (the existing trigger patterns), verbs (the
   existing effect patterns), selection ("all", "each", "every", "a random", "another", "up to N", "target", "it"), area
   ("adjacent", "within N", "in a row/lane", "all ... in play"), duration ("this turn", "until", "while"), frequency ("first
   time", "once per", "whenever"), amount ("equal to", "for each", "X, where"). Game files add their own words, as now.
3. **Derived flat tags**: the definitions above as queries; they replace the compound concepts in `entity_concepts` (method
   `record`) and keep the rest of the build (signatures, archetypes, combos, the key score) unchanged at first.
4. **Fallback**: an ability the parser cannot fill keeps today's flat tags (marked unbound), so no game loses tags; the share of
   bound abilities per game is the progress measure.
5. **Pilot on Faeria** (443 entries, regular text): derived tags against today's tags and the key, ability by ability. Then
   Hearthstone, Duelyst, TESL, Lorcana, Runeterra (keyworded card text), then the prose games (40k, AoS, Into the Breach,
   Darkest Dungeon, the Spire enemies), where boundaries are hardest.
6. **Links**: combos match a record's verb and target against another card's trigger and filter (Feed the Forest's "destroy a
   friendly creature" meets "Last Words"), and two cards that answer the same trigger become a link type ("both reward attacking
   the god": Khalim's Prayer and Zealous Crusader).

## Risks
- Wrong boundaries make wrong records, and derived tags then fail together. The fallback and the per-game bound share limit it.
- The key stays flat at first. A record-level key (a sample per game) would be the later test of the slots themselves.
- It touches the build chain (`trigger_pairs.py`, `link_types.py`, `engine_links.py`, `query.connections`), the tree (compound
  leaves become derived) and the scoring. Every game must be compared (`compare_builds.py`) at each step.

## Decisions for Kaptain
1. Records per ability as above, with flat tags derived from them?
2. Compound concepts (aoe_damage, multi_target_attack, random_target, scope_*, friendly_fire, temporary_buff, permanent_growth,
   in_hand_buff, cost_* from slots) derived instead of stored, and `area_effect` added for any verb?
3. Faeria as the pilot, then the keyworded games, then the prose games?
