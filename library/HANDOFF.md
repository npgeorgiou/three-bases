# Library: state and next steps (20 Oct 2026)

Later on 20 Oct 2026: D&D 5e was removed (`tools/fixes/f16_drop_dnd.py`), and the database is stored without its search and
full-text indexes (`tools/indexes.py`; the build creates them first and drops them last). The file went from 86.2 MB to 63.1 MB.
The numbers below are after the removal.

Later still on 20 Oct 2026: Disney Lorcana, Stormbound, Star Wars: Unlimited and The Elder Scrolls: Legends were added; Monster
Train's card data (282 cards, fandom wiki Module:Cards/Data, read through Kaptain's Chrome) is in hand but not loaded.
Real-world test now **215 of 391**. Agreed work, in order (Kaptain, 20 Oct 2026):
1. Insert-only loading: adding a game only adds rows; the build proves old rows are untouched.
2. Monster Train: read a sample of ~300 cards first, then patterns, cases, load with the insert-only build.
3. Prominence: drop the "top 2 factions" condition (a signature is any mechanic prominent in the faction); archetypes become
   weighted recipes scored per faction (a faction can have several), weights learned on half the cases, tested on the other half.
4. ADDING_GAMES: per game read the material, then a bulk sample of cards, then patterns, then the mechanics check; the cheap
   bulk reader (one request = game block + up to 500 cards).
5. Detailed real-world report (`tools/realworld_report.py` -> REALWORLD_REPORT.md) and whole-library cheap tagging suggestions.

Rules for the next chat: **no readers, judges or agents** without Kaptain's OK and a measured cost. Scripts and builds first.
Commit and push after each step. Read `ADDING_GAMES.md` sections 4b and 4c before writing any pattern.

## Where it stands
The tag-fix plan is finished and its build is the library (`tools/final/report.md`). On the answer key every game has about half the
wrong tags and fewer missed tags than the original (c7a77a4). But the real test, the 300 real-world cases from wikis and guides
(`tools/realworld/<game>.tsv`), is met only **150 of 300 (50%)**; before the removal of D&D it was 162 of 322, almost the same as the original (161). The tag fix improved
agreement with the key, not the library's use for real decks and combos. That is the next goal: **raise the real-world rate.**

## Why the 150 misses miss
Run `python3 library/tools/realworld_why.py library/three-bases-library.sqlite` (it prints every missed case with its reason):

| cases | type | reason | what fixes it |
|---|---|---|---|
| 53 | archetype | the faction is not above the game average for that archetype | the archetype model (below) |
| 35 | signature | the faction's cards use the concept, but not more than other factions | the signature model (below) |
| 15 | signature | only 1-4 of the faction's cards have the concept | tagging |
| 10 | signature | no card of the faction has the concept | tagging (or the case names the wrong concept) |
| 15 | combo | a card name is not in the library | missing cards or name forms |
| 12 | combo | both cards are there, no connection | tagging or the connection search |
| 10 | splash | missing from the faction's splash list | the signature model |

So only about 37 misses (15 + 10 + 12) are tagging. About 98 come from **how signatures and archetypes are measured**, and 15
from **missing cards**.

What is measured now (`tools/signature.py`):
- A faction's **signature** is a concept on 5+ of its cards, 6%+ of them, with lift 1.8+ over the game's other factions.
- An **archetype** counts when the share of the faction's cards with any of the archetype's concepts (`archetypes` table, for
  example swarm = summon, board_presence, fodder, aura, on_ally_play) has lift 1.25+ over the game average.

Tested on 20 Oct 2026: ranking a faction's archetypes and taking its top 3, 4 or 5 instead does **not** help (top 5: 50 of 99,
against 49 now). The thresholds are not the problem. **The share of all cards is not what makes a faction "a swarm deck".** Real
archetypes are decided by the cards decks actually play and by a few key mechanics, not by how common a broad concept is.

## Next steps, in order
1. **Collect more real-world cases (Kaptain's direction).**
   - Target: 50+ per game (about 950), in the same format, each with a source URL: signatures, archetypes, combos and splashes.
   - Also collect **the key cards each source names for an archetype**, as a new case type:
     `archetype_card <faction> <archetype> <card>`.
   - Card names exactly as the library stores them (check with `query.py`).
   - Split every game's cases 50/50 with seed 1. Build rules from one half; use the other half only to test, and report the test
     half only, or the rate will be fitted to the cases.
   - Research with web search in the main chat. Measure the tokens of one game first and show Kaptain before doing the rest.
2. **Check the existing 300 against their sources.** A Claude wrote them, and some may name the wrong concept (for example Duelyst
   Songhai "stealth": 0 of 98 cards). Fix or drop cases the source does not support.
3. **Missing cards (15 combos).** Find why each name is missing (another name form, a merged entry, a card never loaded) with
   `query.py`. Add aliases, or load the cards from a reachable source.
4. **Rebuild the archetype and signature model from the cases.** This is the biggest lever (about 98 misses).
   - From the build half, learn which concepts and which key cards separate the factions sources call "swarm", "control", and so on.
   - Use that instead of the hand-made concept bundles. For example: an archetype counts when the faction has enough cards with
     the archetype's *distinctive* concepts, weighted by how often those cards are its named key cards.
   - Decide the rule on the build half; report the test half.
5. **Tagging from the cases.** For every missed signature with 0-4 cards and every unconnected combo:
   - find the faction's cards that do it;
   - scan their wording in every game (ADDING_GAMES.md 4b) and write per-game patterns;
   - read 20 matches per pattern, then rebuild.
   Example: Gwent Skellige "revive" has 0 of 181 cards tagged.
6. **After each step**: build, all checks, `realworld.py -v`, `realworld_why.py`, and `final_compare.py ... check` against the
   original. No game may get worse on the key.

## Also open
- Payoff tags (`benefits`) count as wrong in `final_compare.py`, because the key reads only what a card does. Decide whether the
  scorers skip them.
- `tools/lost_pairs.py <old> <new>`: look at the trigger pairs that are truly lost (not replaced by a narrower one).
- Step 5 of the plan (reading what rules cannot decide) needs Kaptain's choice first.

## Commands
- Build: `sh library/tools/build.sh library/three-bases-library.sqlite <scratch>/new.sqlite`
- Original for comparison: `git show c7a77a4:library/three-bases-library.sqlite > <scratch>/baseline.sqlite`
- Key score: `python3 library/tools/final_compare.py <scratch>/baseline.sqlite <scratch>/new.sqlite check`
- Real world: `python3 library/tools/realworld.py <db> -v` and `python3 library/tools/realworld_why.py <db>`
- Combos: `python3 library/tools/combo_check.py <db> -v`
- Before a final run: delete `tools/final/revert.tsv` and `revert_base.tsv`, then alternate `final_compare.py ... revert` and a
  rebuild until no game is worse. Never run two builds at once.
