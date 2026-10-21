# Answer-key bug: keywords named on a card were not tagged (found 19 Oct 2026)

## What is wrong
The answer key (`tools/key/<game>/key.json`) was read from each card's own text with the reading rules then in use:
"an entry with no mechanic (... plain stats with nothing else) gets an empty list" and "if the text doesn't say it, it isn't
there". The key applied this to cards whose text is only a list of keyword names, and gave them no tags for those keywords.

Example (Blood Bowl): "Eagle Warrior | Skills: Dodge. Keywords: Human, Lineman. Special rules: Dodge (Active)." has key tags
`[]`. The card has Dodge, so it should carry Dodge's effects. All 168 Blood Bowl players in the key are like this. The same
happens on any card that names a keyword without explaining it ("Taunt", "Flying", "[LETHAL HITS]", "Ward 5+").

The keyword entries themselves were read correctly: `tools/key/kw_<game>/key.json` (1,167 entries)
says what each keyword does. Only the cards that NAME a keyword lack that keyword's tags in the key.

## How big (key entries, today's links)
| game | key entries | empty | entries with a has/grants keyword link | keyword tags missing from their key |
|---|---|---|---|---|
| wh_bloodbowl3 | 347 | 228 | 221 | 1,438 |
| wh_40k_10e | 525 | 4 | 305 | 1,503 |
| gwent | 417 | 15 | 351 | 591 |
| wh_killteam | 466 | 6 | 187 | 512 |
| runeterra | 422 | 0 | 337 | 377 |
| inscryption | 375 | 20 | 176 | 173 |
| into_the_breach | 315 | 3 | 99 | 132 |
| duelyst | 342 | 3 | 159 | 130 |
| mtg | 585 | 5 | 339 | 116 |
| hs_battlegrounds | 405 | 1 | 212 | 100 |
| faeria | 286 | 4 | 186 | 79 |
| sts1 | 348 | 1 | 156 | 66 |
| hearthstone | 564 | 1 | 340 | 52 |
| darkest_dungeon | 342 | 4 | 32 | 50 |
| marvel_snap | 352 | 11 | 244 | 43 |
| shadowverse | 426 | 1 | 338 | 36 |
| wh_underworlds | 436 | 3 | 129 | 29 |
| sts2 | 395 | 1 | 74 | 25 |
| dnd5e, wh_aos_4th | | | 0 | 0 |

(Upper bounds: they count every has/grants link in today's database, including loose ones.)

## What it distorts
Everything scored on the key:
- **Inherited keyword tags count as "wrong"** when they are right. Blood Bowl showed 0 of 1,421 inherited tags right.
- **The Step 4 verdict.** The 7 games where `kw_links.py` looked worse (`tools/step_games.json`) were judged with this bug, so the verdict is unreliable for them.
- **The final comparison.** `final_compare.py` scores and `final_revert.py` "undo" decisions for games with many keyword cards (Blood Bowl, 40k, Kill Team, Gwent, Runeterra).
- **Patterns built or judged on the key.** `tools/step3` verdicts and any key-derived patterns: a pattern that rightly finds a keyword's effect on a card looks wrong, and patterns learned from the key never learn keyword effects.

## Fix (script only)
1. **Credit named keywords in the key**, without touching the key files. Write `tools/key/<game>/key_kw.json`: for each key entry, the
   keywords the card really has, decided from the card's text and source fields only, not from the build being measured
   (that would be circular):
   - a keyword is credited when the card's source data lists it (has_keyword links whose evidence names a field or list:
     Scryfall keywords, keywordRefs, sigils, unit rules/weapon/skill list, special field...), or when its name stands where
     the game prints keywords (`valid()` in `tools/kw_links.py`: start of text, line, sentence or clause, or a "Keywords:"
     list, followed by the end of the clause);
   - the credited tags are that keyword's tags from `tools/key/kw_<game>/key.json`, quoted with the keyword's name as it
     appears in the card's text.
2. **Score with the key plus the credited tags** (`key.py score`, `final_compare.py`, `step3/patterns3.py`). A small
   helper in key.py that loads `key.json` merged with `key_kw.json` covers all three.
3. **Re-run everything that used the key:** pattern verdicts (`patterns3.py eval` / `results`), any key-derived pattern
   generation, the Step 4 per-game choice in `step_games.json` (test kw_links again per game), `final_compare.py revert`, the
   build, and the comparison against c7a77a4.
4. **Leave the original key files unchanged.** The credit is a separate, documented layer, so the key stays as read.
