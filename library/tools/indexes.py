"""The committed database is stored in a smaller form; build.sh turns its working copy back into the full form first
(create) and its output into the stored form last (drop). The stored form leaves out
  - the search indexes and the full-text index (rebuilt from the tables in under a second);
  - the primary-key and unique indexes of the big tables (STRIPPED): the tables are kept without their constraints and their
    original definitions in stored_schema, and create rebuilds them;
  - most of the frozen base (make_base.py): base_tags and base_pairs mostly equal the output's tags and pairs, so only the
    differences are kept (base_*_extra: base rows the output lacks; base_*_skip: output rows the base lacks).
query.py builds the full-text index in memory when it opens a database without one (fts_temp), so queries never change the
committed file.
Usage: indexes.py <db> create|drop"""
import sqlite3, sys
from collections import Counter

INDEXES = [
    'CREATE INDEX IF NOT EXISTS ix_ent_game ON entities(game, category)',
    'CREATE INDEX IF NOT EXISTS ix_ent_name ON entities(name)',
    'CREATE INDEX IF NOT EXISTS ix_el_dst ON entity_links(dst)',
    'CREATE INDEX IF NOT EXISTS ix_ec_concept ON entity_concepts(concept)',
    'CREATE INDEX IF NOT EXISTS ix_te ON trigger_effect(trigger, effect)',
]
NAMES = [s.split()[5] for s in INDEXES]
FTS = "CREATE VIRTUAL TABLE IF NOT EXISTS entity_fts USING fts5(name, text, content='entities', content_rowid='id')"

def has_fts(c, schema='main'):
    return bool(c.execute("SELECT 1 FROM %s.sqlite_master WHERE name='entity_fts'" % schema).fetchone())

STRIPPED = ['entity_concepts', 'base_tags', 'entity_links', 'text_notes']
BASE = [('base_tags', 'entity_concepts', 3), ('base_pairs', 'trigger_effect', None)]   # base, output, key length (None: whole row)
def has(c, t): return bool(c.execute("SELECT 1 FROM sqlite_master WHERE name=?", (t,)).fetchone())
def cols(c, t): return [r[1] for r in c.execute('PRAGMA table_info(%s)' % t)]
def unpack(c):
    """The full form of a stored database: the base tables back from their differences, the constraints back."""
    if not has(c, 'stored_schema'): return
    sql = dict(c.execute('SELECT name, sql FROM stored_schema'))
    for base, out, key in BASE:
        if not has(c, base + '_extra'): continue
        c.execute(sql[base]); n = len(cols(c, base)); ph = ','.join('?' * n)
        skip = Counter(c.execute('SELECT * FROM %s_skip' % base).fetchall())
        rows = []
        for r in c.execute('SELECT * FROM %s' % out).fetchall():
            k = r[:key] if key else r
            if skip[k] > 0: skip[k] -= 1
            else: rows.append(r)
        c.executemany('INSERT INTO %s VALUES(%s)' % (base, ph), rows)
        c.execute('INSERT INTO %s SELECT * FROM %s_extra' % (base, base))
        c.execute('DROP TABLE %s_extra' % base); c.execute('DROP TABLE %s_skip' % base)
    for t in STRIPPED:
        if t not in sql or not has(c, t) or c.execute('SELECT sql FROM sqlite_master WHERE name=?', (t,)).fetchone()[0] == sql[t]: continue
        c.execute('ALTER TABLE %s RENAME TO stored_%s' % (t, t)); c.execute(sql[t])
        c.execute('INSERT INTO %s SELECT * FROM stored_%s' % (t, t)); c.execute('DROP TABLE stored_%s' % t)
    c.execute('DROP TABLE stored_schema')
def pack(c):
    """The stored form (see the top of this file)."""
    if has(c, 'stored_schema'): return
    c.execute('CREATE TABLE stored_schema(name TEXT, sql TEXT)')
    for t in STRIPPED + [b for b, _, _ in BASE]:
        if has(c, t): c.execute('INSERT INTO stored_schema SELECT name, sql FROM sqlite_master WHERE name=?', (t,))
    for base, out, key in BASE:
        if not has(c, base): continue
        b = Counter(c.execute('SELECT * FROM %s' % base).fetchall()); o = Counter(c.execute('SELECT * FROM %s' % out).fetchall())
        extra = b - o; skip = o - b
        if key: skip = Counter(r[:key] for r in skip.elements())
        n = len(cols(c, base))
        c.execute('CREATE TABLE %s_extra AS SELECT * FROM %s WHERE 0' % (base, base))
        c.executemany('INSERT INTO %s_extra VALUES(%s)' % (base, ','.join('?' * n)), list(extra.elements()))
        c.execute('CREATE TABLE %s_skip AS SELECT %s FROM %s WHERE 0' % (base, ', '.join(cols(c, base)[:key] if key else cols(c, base)), base))
        c.executemany('INSERT INTO %s_skip VALUES(%s)' % (base, ','.join('?' * (key or n))), list(skip.elements()))
        c.execute('DROP TABLE %s' % base)
    for t in STRIPPED:
        if not has(c, t): continue
        c.execute('CREATE TABLE stored_%s AS SELECT * FROM %s' % (t, t)); c.execute('DROP TABLE %s' % t)
        c.execute('ALTER TABLE stored_%s RENAME TO %s' % (t, t))
def create(c):
    unpack(c)
    for s in INDEXES: c.execute(s)
    if not has_fts(c):
        c.execute(FTS); c.execute("INSERT INTO entity_fts(entity_fts) VALUES('rebuild')")
    c.commit()
def drop(c):
    for n in NAMES: c.execute('DROP INDEX IF EXISTS %s' % n)
    c.execute('DROP TABLE IF EXISTS entity_fts'); pack(c); c.commit(); c.execute('VACUUM')
def fts_temp(c):
    """A full-text index in the connection's temp schema, for a database stored without one."""
    if has_fts(c) or has_fts(c, 'temp'): return
    c.execute('CREATE VIRTUAL TABLE temp.entity_fts USING fts5(name, text)')
    c.execute('INSERT INTO temp.entity_fts(rowid, name, text) SELECT id, name, text FROM entities')

if __name__ == '__main__':
    c = sqlite3.connect(sys.argv[1])
    {'create': create, 'drop': drop}[sys.argv[2]](c)
