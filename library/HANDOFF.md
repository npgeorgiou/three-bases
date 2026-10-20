# Library: state and next steps (20 Oct 2026, evening)

Kaptain asked for README suggestions 1, 2, 3, 4, 5, 6, 7 and 9, then a new real-world test. Done in this chat: 2, 3, 4.
Open: 1 (Into the Breach done, 18 games left), 5 (started), 6, 7, 9. The database file was not changed in this chat.

Rules for the next chat: **no readers, judges or agents** without Kaptain's OK and a measured cost. Scripts and builds first.
Commit and push after each step. Read `ADDING_GAMES.md` sections 4b and 4c before writing any pattern. **The library itself is
never changed to fit a case**: when a source writes a card's name differently, change the name in the case file to the library's.

## Done
- **Step log (suggestion 3):** `tools/step_log.py` runs after every step of `build.sh`; drops go to `<out>.steps.tsv`, warnings
  to the build output. A full rebuild without loads (scratch only) gave many warnings; most are steps meant to remove (parent_rule,
  pattern_fix, key_wins). Not yet read one by one: Lorcana delayed 154 -> 0 and Duelyst evasion 30 -> 0 at game_patterns,
  Shadowverse cast_from_zone 44 -> 0 at link_types, Gwent passive 42 -> 0 at pattern_fix. Check these first.
- **Reload (suggestion 2):** `tools/reload_game.sh <scratch> <game> [...]` writes `<scratch>/reloaded.sqlite`. Entries keep their
  ids, so reviews, key, regression and revert lists apply. `drop_untagged.py` now keeps entries that regression.tsv gives a tag
  (they were dropped before the review step could tag them). Into the Breach test: regression 21282/21282, real-world unchanged,
  key wrong tags 74 -> 130 per 100 entries (today's patterns; mostly a general "tile" match tagged terrain). So a reload is kept
  only after the game's patterns are fixed and the key is not worse than the current library.
- **Case audit (suggestion 4):** every case checked against its source (built-in browser for pages WebFetch cannot read); `why`
  holds the source's words. 405 -> 362 cases; then 43 new cases from the same pages (suggestion 5, started): **real-world
  test 245 of 405** on the current library. Next for suggestion 5: more pages per game, thinnest games first (Blood Bowl 2,
  Darkest Dungeon 3, Inscryption 3, Kill Team 8, Monster Train 9).

## Mechanics check (suggestion 1), progress
- **Into the Breach: done and kept (20 Oct 2026).** Research on the wiki (Weapons, Status_Effects, Tiles, Environments,
  Passives, Pilots, Squads, Vek, Tips_and_tricks) and two squad guides gave the checklist `tools/mechanics/into_the_breach.txt`
  (36 mechanics). Patterns for its gaps and switch-offs for general wordings that misread this game are in
  `tools/patterns/into_the_breach.txt`, each with its reason. Reloaded and kept: key wrong 74.0 -> 73.7 and missed 43.2 -> 39.4
  per 100 entries, regression 21282/21282, real-world 245 -> 246, other games unchanged (insert-only check). One checklist line
  still shows a gap (water/chasm deaths, 7 Vek entries). Reload fixes made on the way: keyword entries keep their tags
  (`export_game.py` keep_tags), and `drop_untagged.py` keeps entries of the answer key and of regression.tsv.
- **Inscryption: checked, nothing to change.** Its cards only list their sigils, so the check reads the sigil (keyword) entries:
  `coverage.py <db> inscryption 0 --mechanics tools/mechanics/inscryption.txt --keywords` (new option). Research: the wiki's
  Sigils page (all acts and the rulebook). Every one of 27 mechanics carries its concept; one doubtful tag left: Double Strike
  has counterattack (it strikes twice; a hand review in `tools/reviews/inscryption.json` would drop it).
- **The other 17 older games:** not started. Same procedure (ADDING_GAMES.md 0.1, then 0.1-4), one game per pass, keep only when
  `final_compare.py` wrong and missed are not worse than before, regression passes and real-world is not lower. Measure with a
  script like `keydiff` (new wrong key tags by concept and entry, base vs reloaded), which made each fix here a single look.

## Next steps, in order
1. **Combos (suggestion 7, scripts only).** `realworld_why.py` lists 11 pairs with both cards and no connection: Unleash the
   Hounds / Stormwind Champion, Injured Blademaster / Circle of Healing, Force of Nature / Savage Roar, Defias Ringleader / The
   Coin, Electric Whip / Grappling Hook, Tinker Bell - Giant Fairy / Grab Your Sword and / A Whole New World, Inverter of Truth /
   Thassa's Oracle, All for One / Claw, Parry / Sword Sage, Impulsor / Sternguard Veteran Squad (Impulsor is missing). For each,
   print both cards' text and tags, find the missing tag or link, fix the pattern generically (every card with the same wording).
   Cards the library lacks: Inner Fire, Cobalt Guardian, Obol, Wong, Pestermite, Star Battery, Impulsor; check whether the source
   data of that game has them before loading anything.
2. **Tribal (suggestion 6).** A rule in a build step: a card whose text names a type of its game gets `tribal` (benefits), with a
   per-game stop list (Star Wars Unlimited traits like Force or Plan). Measure Hearthstone and Lorcana before and after.
3. **Mechanics check (suggestion 1), one game at a time:** 2-4 guide pages -> `tools/mechanics/<game>.txt` -> `coverage.py <db>
   <game> 40 --mechanics ...` -> patterns -> `reload_game.sh` -> keep only if key (`final_compare.py`), regression and real-world
   are not worse. Start with Into the Breach (its weapon list, class by class, is on intothebreach.fandom.com/wiki/Weapons).
4. **Missing data (suggestion 9).** The built-in browser reaches stormboundkingdomwars.fandom.com and en.uesp.net. Legends sets
   after Houses of Morrowind and Stormbound cards after Feb 2022: read the card tables there, write a converter, load insert-only.
5. **More cases, then recipes (suggestion 5).** About 50 cases per game with source words, split 50/50 seed 1; then
   `learn_recipes.py` and report the test half only. Measure the tokens of one game first and show Kaptain.
6. After each step: build, all checks, `realworld.py -v`, `realworld_why.py`, `final_compare.py ... check`.

## Commands
- Build: `sh library/tools/build.sh library/three-bases-library.sqlite <scratch>/new.sqlite`
- Original for comparison: `git show c7a77a4:library/three-bases-library.sqlite > <scratch>/baseline.sqlite`
- Key score: `python3 library/tools/final_compare.py <scratch>/baseline.sqlite <scratch>/new.sqlite check`
- Real world: `python3 library/tools/realworld.py <db> -v` and `python3 library/tools/realworld_why.py <db>`
- Combos: `python3 library/tools/combo_check.py <db> -v`
- Before a final run: delete `tools/final/revert.tsv` and `revert_base.tsv`, then alternate `final_compare.py ... revert` and a
  rebuild until no game is worse. Never run two builds at once.
- Reload a game: `sh library/tools/reload_game.sh <scratch> <game>`; build drops: `<out>.steps.tsv`
