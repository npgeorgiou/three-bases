# Fixer job: wrong card readings found by the wheel probes (18 Nov 2026)

You fix card records (rows) so that they say what the card text says. Budget: at most 30 tool calls; finish from call 25.
Never run git, run.py, check_all.py, links.py or any rebuild; never edit network.py, flat.py or any other script; change only
`library/cards_db/read/<game>/*.jsonl` (through the fix scripts below) and write your report. Two tries at most per card: a
change that does not do what you want is written as "STUCK: <card>: <what you saw>" and left.

## How
- The records are JSON lines in `library/cards_db/read/<game>/*.jsonl` (find a card with `grep -l '"name": "<Name>"'`).
  Values must exist in `library/cards_db/vocab.tsv` (grep it; never invent a value). `library/cards_db/SYNTAX.md` and
  `BRIEF.md` explain the shapes; copy the shape of a similar correct card in the same game (grep for a phrase).
- Card text: `python3 -c "import sys;sys.path.insert(0,'library/cards_db');import source;print(source.lib().execute('select text from entities where name=?',('<Name>',)).fetchall())"`.
- Write one script per game, `library/cards_db/fixes/<game>/v<N>.py`, N = the number after the game's highest existing vNN
  (runeterra v65, faeria v37, gwent v86, duelyst v43, sts1 v53, marvel_snap v88, into_the_breach v67, inscryption v40).
  Model: `library/cards_db/fixes/runeterra/v64.py` (docstring: what was wrong and why; edits records by card name or text rule;
  safe to run twice: it checks the record still has the wrong shape before changing it). Run each script once.
- Be extremely careful: change only the part named below. Everything else in the record was read right; keep it.

## What to fix
1. **Runeterra, Flow** (a rule for every card with it): the keyword Flow means "activates at Round Start if you played 2+
   spells or skills last round" (the keyword's own text). Cards with Flow have the condition `keyword_condition` Flow, which
   the database cannot link to anything. Replace it, on every card that has it, with the same event_count condition other
   Runeterra cards use for "if you played 2+ spells last round" (find one by grep; if no card has "last round", use the
   shape of "this round" with the span value vocab.tsv gives for the previous round, and say which). If no correct shape
   exists, STUCK, and say what is missing.
2. **A condition "if there is none" lost** (the effect happens only when the first part fails): Faeria Time of Legends
   ("If there are no legends to answer the call, add 1 random legend"), Faeria Compass of Gagana, Runeterra Volibear (level 2),
   Marvel Snap Cannonball, Runeterra Delve Into The Past. Read each text; add the missing condition the way other cards of
   the game write "if ... none / otherwise" (or the OR shape). If a card's rows are already right, say so and leave it.
3. **"non-X" filter lost** (the text excludes a kind, the rows do not): Faeria Exotic Pet (non-green), Runeterra Curious
   Shellfolk, Anaakca, The Poro King's Decree (non-champion), Gwent Stockpile (non-Neutral), Ship Ballista (non-boosted),
   Into the Breach Beetle (non-Alpha), Slay the Spire Cursed Key, Matryoshka, N'loth's Hungry Face, Smoke Bomb (non-boss).
   Add the excluding filter in the shape other cards use (grep `"op": "not"` or the game's "not" filter). Leave words that
   are no filter on a card (Into the Breach "non-fatal", "non-liquid", "non-damaging", Runeterra "non-targeted", Gwent
   "non-status"): say for each whether the rows already say it.
4. **Single cards** (say what each text says, fix only that part):
   - Runeterra Restored Sun Disc: "your level 2 Ascended allies are level 3" is read as `can mine unit [Ascended]` with no
     event; it should say they count as levelled up (level_up on my Ascended units, permanent), the shape other cards use.
   - Runeterra Skirmisher, Blood for Blood, Heroic Charge: the effect happens only "if it survived"; the rows do it always.
   - Gwent Whoreson Senior: Tribute 3 replaces ("instead") the single transform; the rows do both every time.
   - Duelyst Flash Reincarnation: the next minion I play costs 2 less and takes 2 damage; the rows only say "give ability
     to player".
   - Marvel Snap Incursion Event and Slay the Spire Blue Candle: the helper found their rows partly wrong; read the text
     and the rows and fix what is wrong, or say they are right.

## Report
Write `library/cards_db/checks/wheel_probe/fix_report.md`: first line `FIXED <n> cards, STUCK <m>`; then one line per card:
the card, what was wrong, what the record says now (or "already right", or STUCK and why). Then reply with that first line.
