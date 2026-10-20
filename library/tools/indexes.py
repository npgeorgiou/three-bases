"""The search indexes and the full-text index are not stored in the committed database: they are rebuilt from the tables in
under a second and would add about 21 MB to the file. build.sh creates them on its working copies first (the build steps
need them) and drops them from the output last. query.py builds the full-text index in memory when it opens a database
without one (fts_temp), so queries never change the committed file.
Usage: indexes.py <db> create|drop"""
import sqlite3, sys

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

def create(c):
    for s in INDEXES: c.execute(s)
    if not has_fts(c):
        c.execute(FTS); c.execute("INSERT INTO entity_fts(entity_fts) VALUES('rebuild')")
    c.commit()

def drop(c):
    for n in NAMES: c.execute('DROP INDEX IF EXISTS %s' % n)
    c.execute('DROP TABLE IF EXISTS entity_fts'); c.commit(); c.execute('VACUUM')

def fts_temp(c):
    """A full-text index in the connection's temp schema, for a database stored without one."""
    if has_fts(c) or has_fts(c, 'temp'): return
    c.execute('CREATE VIRTUAL TABLE temp.entity_fts USING fts5(name, text)')
    c.execute('INSERT INTO temp.entity_fts(rowid, name, text) SELECT id, name, text FROM entities')

if __name__ == '__main__':
    c = sqlite3.connect(sys.argv[1])
    {'create': create, 'drop': drop}[sys.argv[2]](c)
