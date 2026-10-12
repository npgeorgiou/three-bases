"""Remove Magic entries loaded as tokens that are not tokens or emblems (Scryfall bios, minigame and helper cards, bosses,
events). Usage: f10_mtg_token_filter.py <db> <tokens.json from conv_scryfall_tokens.py>"""
import json, sqlite3, sys
c = sqlite3.connect(sys.argv[1]); keep = {x['ext_id'] for x in json.load(open(sys.argv[2], encoding='utf-8'))['cards']}
n = 0
for (i, e) in c.execute("SELECT id, ext_id FROM entities WHERE ext_id LIKE 'add:scryfall_tokens:%'").fetchall():
    if e.split(':')[-1] in keep: continue
    for st in ("DELETE FROM entity_concepts WHERE entity=?", "DELETE FROM trigger_effect WHERE entity=?", "DELETE FROM entity_links WHERE src=? OR dst=?", "DELETE FROM entities WHERE id=?"):
        c.execute(st, (i,) * st.count('?'))
    n += 1
c.execute("UPDATE load_log SET count=(SELECT count(*) FROM entities WHERE ext_id LIKE 'add:scryfall_tokens:%') WHERE game='mtg' AND step='loaded (scryfall_tokens)'")
c.execute("INSERT INTO entity_fts(entity_fts) VALUES('rebuild')"); c.commit(); print('non-token entries removed:', n)
