# Next chat: fix the database's blind spots (30 Oct 2026, v55)

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

## Kaptain's order of 30 Oct 2026, not finished in v55 (do these first, each as THINKING, every game)
Done in v55: a card is judged with what it makes (flat_made table built by refs.py; ask.py counts makers as "Zed (via Living
Shadow)", mechanics.py and deck_analysis.py too); arrival buffs for a keyword state ("an Ephemeral ally") reach only cards that
print it; level-up sentences keep who acts and their kind ("your Ephemeral units attack"); ask.py leaves out enemies, bosses and
run events (--enemies keeps them) and names the nearest concept for an unknown one; deck_audit prints what each card makes.
Still to do, each found by questions that came back empty or wrong (the cause is in the data or the query, never "the game has
none"):
1. Controlling spots on the map: only 2 Faeria cards (zone_control). Find every game's map-control mechanics (Stormbound front
   line, Faeria wells and lands, Duelyst mana springs and positions, Into the Breach buildings and tiles), give them one
   outcome concept, and keep landmarks (Runeterra building, 101 cards, now in "terrain") apart from map spaces.
2. Staying power: regeneration and cheat_death are missing in Duelyst, Faeria, Stormbound (heal each turn, "can't die",
   rebirth). Find the texts by regex, find why their rows lack the concept, fix the concept mapping.
3. Disable: Faeria and Inscryption find none, yet Faeria's "can't attack" rows and Inscryption's skip a turn exist under
   other concepts. Check every concept that means "the enemy can't act" and map it by outcome.
4. Runeterra drowns other games in pair counts (feeds, fed, together): rank by share within each game.
5. Answers are names only: add the card text (short) where a design question needs it.
6. Plan lines in deck_analysis ignore the kind a level-up asks for ("Any units attack ... level up from it: Hecarim", who needs
   Ephemeral attackers): same thinking as the arrival-buff error; check every match of a need against its filters.
7. Kaptain's suggestions, approved: store every card-to-card line of each game as a table in cards.sqlite (from, to, kind,
   reason), built with the database; one design question giving per game the cards with texts, best partners and factions.
8. A full, honest deck check of every game, reading what each card makes (deck_audit "makes"), not a sample.

## Open work (not this chat's game unless asked)
- Deck checks of the other games with `deck_audit.py`: another chat does them (Kaptain, 30 Oct 2026).
- Stormbound csb09-csb13 (poisoned-unit combos) fail; Runeterra n56 must be rewritten (HANDOFF "State").
- Deck check of 30 Oct 2026 (v54), open families (fix by cause, for every game):
  - A card placed by its own text near the leader (Conscript: "summon a Crestfallen in front of your General") draws no line to
    a card acting on units near the leader (Fealty); only moving cards do (Azurite Lion).
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
