# Three Bases — rules for Claude (read before anything else)

Kaptain's browser card game "Three Bases" lives in this repository. Clone it at the start of every chat that works on the game, work on the clone, and commit and push every change to `main`.

## Where things go (AGREED, 12 Oct 2026; never break this)
1. **summary.txt — the game as it is now.** Built or agreed rules, all factions' current cards (one file, all factions), UI, animations, computer opponents, the AI lab. No plans, no ideas, no open questions, no to-dos.
2. **factions.txt — the game as it might become.** Faction candidates, card ideas, future and planned factions, design principles for new factions (card design method, entry format), and rejected ideas ("don't reintroduce").
3. **todo.md — work not done yet.** Open requests (quoted in Kaptain's own words), bugs, discussions. An item is removed once done or decided; what was decided moves into summary.txt (or factions.txt if it is only an idea).
4. **Claude's memory — only how to work with Kaptain** (answer style, token habits). No game content in memory.
5. **This file (CLAUDE.md) — how Claude works on the files**: locations, workflow, reading rules.

When something changes state (an idea gets built, a to-do gets decided), move it to its home in the same turn.

## Files in this repository
- `three-bases-game.html` — the game (always this one name, no version names).
- `three-bases-scenarios.html` — the game plus a SCENARIOS script and styles appended at the end. Every game edit goes into both files; rebuild it after every game change.
- `three-bases-ai-lab.html` — the AI lab. Never remove the lab or anything related to it.
- `summary.txt`, `factions.txt`, `todo.md` — see above.
- Inspiration library: `three-bases-library.sqlite`, `lib/` (run `python3 lib/query.py <command>` from the repo root), `README.md` and `SEARCH_GUIDE.md` (both are the library's). Library questions go in fresh chats, with compact queries in one go.
  - Library changes are committed and pushed here (no zip). Concepts are organised by outcome (e.g. "no damage output" covers "can't attack" and "strength 0"), not by mechanism; combos emerge from card mechanics as links, never added from outside sources. Shadowverse: Worlds Beyond is excluded entirely; cut any game whose data could drown out the others. Kaptain doesn't have the raw library-corpus.zip, so dropped cards must come from other reachable sources. Improvement ideas: README.md, "Suggestions for improving the library".

## Workflow
- After every change: commit, push, and also give Kaptain the changed game/scenarios/summary file as an immediate download.
- Never publish anything as an artifact.
- Summary updates are done in one pass after the current work; remind Kaptain in every reply to tell Claude to save the summary.

## Reading rules (token economy)
- Never read a whole big file. Find headings with grep and read only the section the task needs (e.g. only the factions a task touches in summary.txt).
- Edit with small scripted replacements, never by re-writing whole files.
- In the game file, read only the code being changed (targeted greps, short line ranges); one short test of the changed behaviour.
