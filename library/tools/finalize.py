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
 'wh_underworlds': " Later load (Oct 2026): the warscroll abilities of 8 warbands and the 4 Grand Alliance warscrolls (category ability, edition 'Embergard warband rules'), paraphrased from the official PDFs; fighter stat lines are not in the data.",
}
for g, extra in NOTES.items():
    cur = q('SELECT notes FROM games WHERE id=?', g)
    if cur and extra.strip() not in (cur[0][0] or ''):
        c.execute('UPDATE games SET notes=? WHERE id=?', ((cur[0][0] or '') + extra, g))
c.execute("UPDATE games SET notes=replace(notes, 'Champion level-up text appended to the card text.', 'A champion is its level 1 card with its level-up condition plus its levelled side.') WHERE id='runeterra'")
c.execute("UPDATE games SET source=replace(source, 'collectible subset', 'collectible subset, plus created cards from HearthSim hsdata') WHERE id='hearthstone'")
c.commit(); print('orphan rows removed:', n)
