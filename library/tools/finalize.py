"""Final clean-up: remove rows that point at entries that no longer exist, refresh faction sizes, and bring the per-game notes
up to date with the later loads. Usage: finalize.py <db>"""
import sqlite3, sys
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
n = 0
n += c.execute('DELETE FROM entity_concepts WHERE entity NOT IN (SELECT id FROM entities)').rowcount
n += c.execute('DELETE FROM entity_links WHERE src NOT IN (SELECT id FROM entities) OR dst NOT IN (SELECT id FROM entities)').rowcount
n += c.execute('DELETE FROM trigger_effect WHERE entity NOT IN (SELECT id FROM entities)').rowcount
n += c.execute("DELETE FROM entity_concepts WHERE concept NOT IN (SELECT id FROM concepts)").rowcount
n += c.execute("DELETE FROM concept_relations WHERE a NOT IN (SELECT id FROM concepts) OR b NOT IN (SELECT id FROM concepts)").rowcount
c.execute("UPDATE factions SET entity_count=(SELECT count(*) FROM entities e WHERE e.game=factions.game AND e.faction=factions.name AND e.category NOT IN ('keyword','tribe'))")
NOTES = {
 'runeterra': " Later loads (Oct 2026, Riot Data Dragon set files): the levelled side of every champion ('<name> (level 2)', linked by transforms_into), created champion units, and the non-collectible cards the first load dropped (tokens, champion spells, created cards, abilities, landmarks; edition 'non-collectible'), linked from the cards that create them (generates). The 'Runeterra' champion region was removed.",
 'hearthstone': " Later loads (Oct 2026, HearthSim hsdata): non-collectible cards of the collectible sets (tokens, generated cards, rewards; edition 'non-collectible', ' (created)' when the name exists) and collectible cards the first build dropped.",
 'hs_battlegrounds': " Later load (Oct 2026, HearthSim hsdata): Battlegrounds cards with text the first build dropped (hero powers, rewards, trinkets). Enchantments are left out: their effect is the text of the card that applies them.",
 'mtg': " Later loads (12 Oct 2026): 640 cards from MTGJSON AtomicCards that bring a mechanic the first build's cards lack (the other 10,560 repeated existing mechanics and were left out); Scryfall Oracle Cards for tokens and emblems with rules text (linked by generates from the cards that make them), set names, related cards and keyword lists (has / grants / mentions).",
 'sts1': " Later load (12 Oct 2026, wiki Module:Cards/data): an upgraded card whose text changes only in numbers keeps them on the base card (extra.upgraded_text, extra.upgraded_cost); an upgrade that changes the mechanic (adds Innate or Retain, drops Exhaust, all cards instead of one, ...) is its own entry '<name>+' linked variant_of to the base card. Cards the first build lacked (Sucker Punch, Pressure Points, created cards such as Shiv, Miracle, Smite) were added.",
 'gwent': " Later load (12 Oct 2026): NonOwnable cards (tokens, created cards) from the same export, ' (created)' when the name exists, linked from the cards that create them (generates).",
 'shadowverse': " Later load (12 Oct 2026): tokens (set 90000, alternate art left out) and cards the first build dropped, linked from the cards that create them (generates).",
 'dnd5e': " Later load (12 Oct 2026, 5e-database): spells, class features, species traits and feats the first build dropped; bookkeeping features and item variants still left out.",
 'wh_40k_10e': " Later load (12 Oct 2026, BSData current): abilities and army rules whose text the library lacked; campaign content (Crusade) left out.",
 'wh_killteam': " Later load (12 Oct 2026, BSData current): abilities, unique actions and rules whose text the library lacked.",
 'wh_aos_4th': " Later load (12 Oct 2026, BSData current): abilities and rules whose text the library lacked; Path to Glory and hero-creation entries left out.",
 'wh_underworlds': " Later load (Oct 2026): the warscroll abilities of 8 warbands and the 4 Grand Alliance warscrolls (category ability, edition 'Embergard warband rules'), paraphrased from the official PDFs; fighter stat lines are not in the data.",
}
NOTES_LATER = {'wh_underworlds': " Later load (12 Oct 2026, yawudb): the deck cards the first build dropped (upgrades tagged items_consumables like every reviewed upgrade; attack profiles read as damage, ranged from range 2)."}
for g, extra in list(NOTES.items()) + list(NOTES_LATER.items()):
    cur = q('SELECT notes FROM games WHERE id=?', g)
    if cur and extra.strip() not in (cur[0][0] or ''):
        c.execute('UPDATE games SET notes=? WHERE id=?', ((cur[0][0] or '') + extra, g))
c.execute("UPDATE games SET notes=replace(notes, 'Champion level-up text appended to the card text.', 'A champion is its level 1 card with its level-up condition plus its levelled side.') WHERE id='runeterra'")
c.execute("UPDATE games SET source='hearthstone.json (HearthstoneJSON export, collectible subset, plus created cards from HearthSim hsdata)' WHERE id='hearthstone'")
SOURCES = {   # later loads (12 Oct 2026), added once to the game's source line
 'mtg': 'MTGJSON AtomicCards.json (5.3.0+20261011) for 640 cards with a new mechanic; Scryfall Oracle Cards (11 Oct 2026) for tokens, emblems, set names and keyword lists',
 'sts1': 'Slay the Spire Wiki Module:Cards/data for upgraded cards',
 'gwent': 'the same export for the NonOwnable set (tokens)',
 'shadowverse': 'the same export for tokens (set 90000)',
 'wh_underworlds': 'yawudb db.js (github.com/PompolutZ/yawudb) for dropped deck cards',
 'wh_40k_10e': 'BSData wh40k-10e (current) for abilities and rules the library lacked',
 'wh_killteam': 'BSData wh40k-killteam (current) for abilities and rules the library lacked',
 'wh_aos_4th': 'BSData age-of-sigmar-4th (current) for abilities and rules the library lacked',
 'dnd5e': '5e-database (github.com/5e-bits/5e-database) for entries the first build dropped',
}
for g, sx in SOURCES.items():
    cur = q('SELECT source FROM games WHERE id=?', g)
    if cur and sx not in (cur[0][0] or ''): c.execute('UPDATE games SET source=? WHERE id=?', ((cur[0][0] or '') + '; later: ' + sx, g))
c.commit(); print('orphan rows removed:', n)
