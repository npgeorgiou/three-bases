# Three Bases — rules for Claude

Kaptain's browser card game. Work on the clone, commit and push every change to `main`.

## Start of a chat (token budget: read nothing else)
- Clone without the 121 MB library unless the task is about it:
  `git clone -q --depth 1 --filter=blob:none --no-checkout https://github.com/npgeorgiou/three-bases /home/claude/three-bases && cd /home/claude/three-bases && git sparse-checkout set --no-cone '/*' '!/library/' && git checkout -q main`
  (library task: `git sparse-checkout disable`).
- This file is the only file read at the start. Do not open the README, todo.md, summary/ or factions/ indexes, or any code until the task needs it, then use the map below to go straight to the right file.

## Map: where each thing lives
Game source is `src/game/`, joined in `src/game/parts.txt` order by `python3 tools/build.py` into `three-bases-game.html` and `three-bases-scenarios.html` (= game + `src/scenarios/`). **Never read or edit the two built HTML files**; edit `src/` and build.
- Card stats/text: `js/cards/<tagma|ashfang|exanimati>.js` (one line per card). Keyword hover texts: `js/cards/keywords.js`. Decks, premades: `js/cards/decks-premade.js`. Card art (SVG paths): `js/cards/art.js` (never read unless drawing art). Flag list: `js/cards/00-header.js`.
- Rules (`js/rules/`): helpers, geometry, queries `helpers-geometry-queries.js` · keyword flags, strength/defence, costs `keywords.js` · bases, supply, auras, newGame, events `bases-supply-positions-events.js` · attacks, damage, Armoured, Riposte `combat.js` · moves, deploy, Charge `movement-deploy.js` · Place/follow-up choices `followups.js` · death, Plague, discard, Revenant, Afterlife `exanimati-death-plague-discard.js` · round start/end `rounds.js` · unit ability scopes (SCOPE) and effects `abilities.js` · spells (SPELL_SCOPE) `tactics.js` · `ogre-thrower.js` · action list and applyAction `actions.js`.
- Computer: `js/ai/opponent.js` (move filters), `js/ai/benchmark.js` (Benchmark values, search, redraw, Random player). `js/sound.js`.
- Screen (`js/view/`): icons and card HTML `helpers-icons-cards.js` · app state, AI choice, board geometry `app-state-geometry.js` · hover previews `previews.js` · supply bar, bases, unit drawing `board-cells-units.js` · renderBoard, highlights, pointer→cell `board-render-pointer.js` · event replay `animations.js`, `animations-cards-moves.js` (spells, draw, banner, carry, move), `animations-hits-flights.js` (hits, flights, charges, toss) · piles, hand, side panel, prompt, render() `panels.js` · tooltips, card text fitting `tooltips.js` · round-end forecast `forecast.js` · start/decks pages, deck builder `decks-pages.js`.
- Flow: `js/flow/game-flow.js` (after each action, computer turn), `js/flow/replay.js` (replay, startGame). Input: `js/input/input.js` (clicks, drag, hover), `js/input/fullscreen-keys-aipick.js`. `js/boot.js`.
- CSS: `css/1-tokens-layout-toolbar.css` (colours, layout, piles, faction colours, toolbar) · `css/2-board-units-cards-hands.css` · `css/3-tooltips-fx-dialogs-prompt.css`. HTML: `shell/body.html` (pages, dialogs).
- Design docs: `summary/` (the game as it is now; one file per section, faction cards in `summary/11-faction-<name>.txt`, index `summary/README.txt`). `factions/` (ideas: one file per part, one per candidate in `factions/3-candidates/`, index `factions/README.txt`). `todo.md` (open work). Cross-references like "section 7" mean the summary file starting with `07-`.
- AI lab: `three-bases-ai-lab.html` (one file, not split yet; Kaptain will redesign it — split it the same way when that work starts). Never remove the lab or anything related to it.
- Library: `library/` (`python3 library/tools/query.py <command>`, `library/README.md`, `SEARCH_GUIDE.md`). Library questions go in fresh chats, with compact queries in one go. Library changes are committed and pushed here. Concepts are organised by outcome (e.g. "no damage output" covers "can't attack" and "strength 0"), not by mechanism; combos emerge from card mechanics as links, never added from outside sources. Excluded entirely: Shadowverse: Worlds Beyond, D&D 5e, Blood Bowl, Kill Team, Warhammer Underworlds; cut any game whose data could drown out the others. Kaptain doesn't have the raw library-corpus.zip, so dropped cards must come from other reachable sources. Open library work, in order: library/README.md, "Improving the library". After every library change: `library/tools/compare_builds.py`.

## Finding things (before reading anything)
- `python3 tools/find.py kw <Keyword>` — the cards with it and every code line using its flag (fix-all-cards checks start here).
- `python3 tools/find.py card <name>` — the card's data line and its summary lines.
- `python3 tools/find.py where <identifier>` — definition and uses in the game code.
- `python3 tools/find.py doc <text>` — matching lines in summary/ and factions/.
- Otherwise `grep -n` in the one file the map names. Then read only the lines needed (`sed -n 'a,bp'` or Read with offset/limit, usually under 80 lines). Never read a whole part, doc or HTML file; never grep the built HTML.

## Where things go (AGREED, 12 Oct 2026; never break this)
1. **summary/ — the game as it is now.** Built or agreed rules, all factions' current cards, UI, animations, computer opponents, the AI lab. No plans, ideas, open questions or to-dos.
2. **factions/ — the game as it might become.** Faction candidates, card ideas, planned factions, design principles (card design method, entry format), rejected ideas ("don't reintroduce").
3. **todo.md — work not done yet.** Open requests (in Kaptain's own words), bugs, discussions. Removed once done or decided; the decision moves to summary/ (or factions/ if only an idea).
4. **Claude's memory — only how to work with Kaptain.** No game content in memory.
5. **This file — how Claude works on the files.**
When something changes state (an idea gets built, a to-do gets decided), move it to its home in the same turn.

## Workflow
- summary/ is the source of truth for rules and UI: never contradict it without telling Kaptain. Never invent rules, stats or mechanics; mark suggestions as Claude's.
- Change only what was asked. Fix bugs generically: when one card shows a problem, check every card with the same problem (`find.py kw`).
- Visuals (layout, readability, animations) must look deliberate and clear.
- Edit with Edit or small scripted replacements on the part file; never rewrite whole files; never re-read a file after editing it.
- After a code change: `python3 tools/build.py` (joins parts, syntax-checks, warns about oversized files), then `node tools/simtest.js` (headless games; prints a hash). A refactor must keep the hash; a rules change may change it, then check the changed behaviour with one short targeted test. UI changes: `node tools/smoke.js` (page loads without script errors). Paste no command output into replies.
- Commit and push. Give Kaptain only the changed built HTML files (game, scenarios, AI lab) as downloads, never text files (he reads those on GitHub). Never publish anything as an artifact.
- Summary updates are done in one pass after the current work: while game changes are not yet written into summary/, end every reply with a reminder that Kaptain should tell Claude to save the summary (= write those changes into summary/ and push). No unsaved changes, no reminder.

## Keeping the structure (check before every commit)
- New code goes into the part the map names. A new topic gets its own part: add it to `src/game/parts.txt` and to the map above in the same commit. Renamed or split parts: update the map in the same commit.
- `tools/build.py` warns when a code part passes 400 lines, a summary/factions file passes 150, or any other new text file passes 600: split it at a section or function boundary (and update the map/index) before pushing.
- New sections in summary/ or factions/ are new files, listed in that folder's README.txt with their line count and one-line contents. Don't recreate summary.txt or factions.txt.
- Any new big file (doc, tool, page) gets the same treatment from the start: split into parts with an index, and a line in the map above.
- Comments: one line saying what a block is for; no history ("formerly", "v2", "option B"), no change logs. Remove dead code and unused CSS when you touch an area.
- If any rule here gets in the way of a task, say so to Kaptain instead of quietly working around it.
