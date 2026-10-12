"""Keep old entries as they were, except for the effect of this session's changes.
final(old) = (orig(old) | (new(old) - base(old))) - (base(old) - new(old))
orig = shipped library; base = the build chain re-run on the shipped library alone; new = chain run with this session's loads and patterns.
Old entries = ids present in orig. Tables: entity_concepts, trigger_effect, entity_links (rows touching only old entries).
Usage: keep_old.py <new.sqlite> <orig.sqlite> <base.sqlite>"""
import sqlite3, sys
new, orig, base = sys.argv[1:4]
c = sqlite3.connect(new)
c.execute(f"ATTACH '{orig}' AS o"); c.execute(f"ATTACH '{base}' AS b")
c.execute("CREATE TEMP TABLE old_ids AS SELECT id FROM o.entities")
c.execute("CREATE INDEX temp.oi ON old_ids(id)")
def redo(tbl, cols, cond):
    sel = lambda s: f"SELECT {cols} FROM {s}.{tbl} WHERE {cond}"
    c.execute(f"CREATE TEMP TABLE keep_{tbl} AS {sel('o')} UNION SELECT * FROM ({sel('main')} EXCEPT {sel('b')})")
    c.execute(f"CREATE TEMP TABLE gone_{tbl} AS {sel('b')} EXCEPT {sel('main')}")
    c.execute(f"DELETE FROM main.{tbl} WHERE {cond}")
    c.execute(f"INSERT OR IGNORE INTO main.{tbl}({cols}) SELECT * FROM keep_{tbl} EXCEPT SELECT * FROM gone_{tbl}")
    # an old entry that this session deleted (merged away) stays deleted
    print(tbl, c.execute(f"SELECT count(*) FROM keep_{tbl}").fetchone()[0], 'kept;', c.execute(f"SELECT count(*) FROM gone_{tbl}").fetchone()[0], 'removed by this session')
ce = ','.join(r[1] for r in c.execute("PRAGMA table_info(entity_concepts)"))
te = ','.join(r[1] for r in c.execute("PRAGMA table_info(trigger_effect)"))
el = ','.join(r[1] for r in c.execute("PRAGMA table_info(entity_links)"))
redo('entity_concepts', ce, "entity IN (SELECT id FROM temp.old_ids)")
redo('trigger_effect', te, "entity IN (SELECT id FROM temp.old_ids)")
redo('entity_links', el, "src IN (SELECT id FROM temp.old_ids) AND dst IN (SELECT id FROM temp.old_ids)")
alive = "(SELECT id FROM main.entities)"
for t, k in (('entity_concepts', 'entity'), ('trigger_effect', 'entity')): c.execute(f"DELETE FROM main.{t} WHERE {k} NOT IN {alive}")
c.execute(f"DELETE FROM main.entity_links WHERE src NOT IN {alive} OR dst NOT IN {alive}")
c.commit()
