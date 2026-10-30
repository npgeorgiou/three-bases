# Handoff: card database (30 Oct 2026, v54)

> **CHECKING AFTER A CHANGE: LOAD THE DATABASE ONCE. NEVER RUN `run.py <game>` ONCE PER GAME.**
> Every `run.py` reloads ALL eight games (load.py loads every game, every time). Eight runs = eight reloads = over an hour
> (30 Oct 2026, it happened). Use `python3 check_all.py <your game>` (one reload, then every other game's cases and link
> audit) or, after a change to network.py only, `python3 check_all.py --no-load` (no reload at all: the networks read
> cards.sqlite). Then `dump_lines.py` before/after (PROCESS "Fixing a review").

> **AFTER EVERY NETWORK BUILD OR CHANGE: `deck_audit.py <game>` AND READ IT (PROCESS "Audit every deck yourself").** For every
> deck: the 3 most and 3 least linked cards with all their lines, 10 other random cards (should one be linked with a least
> linked card?), and 10 random lines, each checked against the card texts.
> Fix what you find by its cause, for every game, and ask what else that cause breaks outside the decks. Kaptain must not be
> the one who finds these.

## Start of a chat
1. Clone with the library (CLAUDE.md "Start of a chat", then `git sparse-checkout disable`). Read only this file first.
2. cards.sqlite is committed and current: questions need no build (`ask.py runeterra ...`).
3. Then, as the task needs: PROCESS.md (how to work, the steps, fixing a review, checking networks), PROCESS_LESSONS.md (what
   each import and review taught, for every game), README.md (files, tables, questions), RESULTS.md (results per game),
   NEXT_CHAT.md (the next chat's work).

## Importing a new game: start here
Read PROCESS.md in order ("Why the first three games went wrong", "How to work", "Rules that are never broken", "Writing
data the same way in every game", "Steps"), then PROCESS_LESSONS.md, the sections closest to your kind of game. Follow the
steps once, in order. The order that saves the most time:
1. **Before readers.** The game's data is already in the repo (step 0.3); its rules and terms are in
   `library/tools/games/<game>.md`. Research how the game works first (fights, moves, boards, statuses, what cards put in
   play) and write it as game rules (step 0.10). Every card of every guide deck must be a card of the game (`audit_links.py`
   check 5): if not, build the supplement first. Read 20 cards' source boxes and their keyword definitions field by field.
   Decks: at least 20, spread over the game's factions and mechanics; full ones with counts if they exist (step 2.9); a
   guide's core cards is no full deck: mark it so. After the networks are built: the deck check (`deck_audit.py`, box above).
2. **Readers** get READER_PROMPT.md unchanged; BRIEF.md reading rules are what they follow. Fix what they get wrong by rule
   scripts over the texts (`fixes/<game>/vNN.py`, safe to run twice, each file keeps its own JSON form), never by re-reading.
3. **After readers, before any fix:** one pass that lists everything wrong (all decks with `deck_lines.py`, `deck_audit.py`,
   the 20-card check, audit_text, audit_links). Then one fix per cause, one reload (`check_all.py`), one case per family.
4. **Set the game's values:** network.EXPENSIVE (what is an expensive card), starter items if the game has them
   (rarity starter), the game's words in BRIEF.md.
5. **Done** only by PROCESS "Done when", never by passing counts.

**Do and don't (Kaptain's rules, 29-30 Oct 2026):**
- Fix every point by its cause, in the shared rule, for every game (PROCESS "Fixing a review"); dump every line of every game
  before and after (`dump_lines.py`) and read every gone and new reason. A point fixed for the named cards only comes back.
- Links come from what a card's text does, never from what every card does (PROCESS "Rules for links"); a helper points at
  what it helps; what a card gives or puts in play acts through it.
- Read networks with `deck_lines.py` / `deck_audit.py` only (the page's own text); never write your own export scripts.
- Pull before you rebuild and before you commit. Generated files (cards.sqlite, cases/REPORT.md, QUERIES.md, STATUS.md,
  network.html) conflict on every merge: take either side and rebuild; merge code by hand, keeping both sides.
- Never run `run.py` for another chat's game, never change its records, fixes or flags.
- Answer Kaptain's questions first and wait; explain in plain words with a card example; one question at a time.

## State
- Done and approved: Runeterra, Into the Breach (RESULTS.md). Slay the Spire: done (v49-v53), deck_read_sts1.md F1-F20,
  every Kaptain point fixed by rule; Through Violence added from Kaptain's definition (supplement/sts1_kaptain.jsonl).
- Waiting for Kaptain's check: Stormbound and Monster Train (CHECK_20_<game>.md), Faeria, Duelyst (CHECK_20, CONCEPTS);
  Inscryption reviewed (deck_read_inscryption.md).
- Cases, all passing except: Stormbound 141 of 145, csb09-csb13 (poisoned-unit combos), which fail also without the Slay the
  Spire rows: an older Stormbound issue, not yet traced. Runeterra n56 is a must-not case whose reason no deck says any more
  (cases/run.py lists it): rewrite it.
- Deck networks of every game: network.py, the page `network_page.py` -> network.html (decks.tsv, cases/decks.tsv).
