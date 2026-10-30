# Next chat: import the next game (30 Oct 2026, v53)

Read HANDOFF.md first (its two boxes are the rules most often broken), then PROCESS.md and PROCESS_LESSONS.md. Everything
below is pushed. Kaptain checks a few decks and has found real errors in every round, because work fixed only what he
pointed at. **Your job is to find the errors he has not pointed at, before he looks.**

## How to think (this is what went wrong, game after game)
1. Every error is ONE example of a FAMILY. Name the cause in one sentence, find every member in ALL games (a query, a text
   regex, `dump_lines.py --find`), fix the shared rule once, dump before and after, read the diff. Never fix one card.
2. Think like a player, card by card: what does this card need, and which cards give it that? What does it give, and to
   whom? Missing help is as wrong as a wrong line. Run `deck_audit.py <game>` and read all of it.
3. Read the card TEXT, not only the rows. If they disagree, the rows are wrong: fix them by a text rule (fixes/<game>/vNN.py).
4. Never write "not sure" about something you can check: the texts, the game's glossary, the wiki. Read the game's own
   limits on a mechanic before drawing a line (Slay the Spire's Dexterity: only Block a card gives when played).
5. What a card gives (a status) or puts in play (a token, an Orb) acts through it: check the database says so, or every
   question over damage, Block or energy misses those cards (PROCESS_LESSONS "Importing Slay the Spire" 2).
6. Report per family, with counts per game, and say honestly what was not checked.

## Open work (not this chat's game unless asked)
- Deck checks of the other games with `deck_audit.py`: another chat does them (Kaptain, 30 Oct 2026).
- Stormbound csb09-csb13 (poisoned-unit combos) fail; Runeterra n56 must be rewritten (HANDOFF "State").
- Deck check of 30 Oct 2026 (v54), open families (fix by cause, for every game):
  - A card placed by its own text near the leader (Conscript: "summon a Crestfallen in front of your General") draws no line to
    a card acting on units near the leader (Fealty); only moving cards do (Azurite Lion).
  - "When you summon an Ephemeral ally, grant it +1|+0" (Moonlit Glenkeeper) links to non-Ephemeral units (Zed, Hecarim): the
    state filter counts as possible because some card of the game gives Ephemeral, even when no card of the deck does.
  - Adaptive Mutation (swap Attack and Health) shows only "can heal it" to Deranged Brute: the swap of stats has no link.
- Monster Train has no full decks as text (players post screenshots): ask Kaptain.
- Not linked on purpose (Claude's calls, keep unless Kaptain says otherwise): Janna's "the first 3 cards you draw cost 1
  less" (helps any card); Stormbound units moving forward each turn (every unit); plain single-target damage (Strike, Mystic
  Shot) feeds no "when an enemy dies".

## Where things are
- network.py: every line rule (lines_of, aimed, played_lines, need_lines, boost_lines, gives_lines, keyword_adders,
  status_damage_givers, special_abilities, EXPENSIVE); network_page.py -> network.html; deck_lines.py, deck_audit.py.
- refs.py (what each card makes and needs), flat.py (query layer: keywords given, used or put in play are expanded onto the
  card), deck_analysis.py (deck parsing, starter items), check_all.py, dump_lines.py, review_check.py.
- cases/network.tsv (line or no line, per deck), cases/mechanics.tsv (questions over records); deck_read_<game>.md (families).
