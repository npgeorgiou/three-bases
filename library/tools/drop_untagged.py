"""Drop entries (any load) that no pattern or keyword reached (no concept tag and no keyword link), as the first build
dropped them (README: the library is for mechanics). Run after game_patterns.py. Logged per game. Usage: drop_untagged.py <db>"""
import sqlite3, sys
c = sqlite3.connect(sys.argv[1])
rows = c.execute("""SELECT id, game FROM entities e WHERE category NOT IN ('keyword','tribe')
    AND NOT EXISTS (SELECT 1 FROM entity_concepts x WHERE x.entity=e.id)
    AND NOT EXISTS (SELECT 1 FROM entity_links l WHERE l.src=e.id AND l.rel LIKE '%keyword')""").fetchall()
n = {}
for i, g in rows:
    for s in ("DELETE FROM entity_links WHERE src=? OR dst=?", "DELETE FROM trigger_effect WHERE entity=?", "DELETE FROM entities WHERE id=?"):
        c.execute(s, (i,) * s.count('?'))
    n[g] = n.get(g, 0) + 1
for g, k in n.items():
    c.execute("DELETE FROM load_log WHERE game=? AND step='dropped entries no pattern or keyword reached'", (g,))
    c.execute("INSERT INTO load_log VALUES(?,?,?,?)", (g, 'dropped entries no pattern or keyword reached', k, ''))
c.execute("INSERT INTO entity_fts(entity_fts) VALUES('rebuild')")
c.commit(); print('dropped untagged:', n)
