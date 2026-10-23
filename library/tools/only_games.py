"""A build of only some games (build.sh --only): the other games' rows are copied unchanged from the input.
No build step crosses games (checked 23 Oct 2026: builds and a reload of two games, merged, equal the full build row for row), so the
steps run on a copy that holds only the named games, and their rows then replace those games' rows in the full input.
A row belongs to a game by its game column (games: id), else by its entity (entity_links: src); a table with neither, and
rows with no game (general patterns), are shared and come from the partial build; the games table stays whole in the copy. Both databases are in the full form
(indexes.py create, compact_text.py expand).
  only_games.py split <full.db> <part.db> <game> ...   part = full without the other games' rows
  only_games.py merge <full.db> <part.db> <game> ...   full = full with the games' rows (and the shared tables) from part"""
import sqlite3, sys

def tables(c):
    return [t for t, in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'entity_fts%' AND name NOT LIKE 'sqlite_%'")]
def cols(c, t): return [r[1] for r in c.execute('PRAGMA table_info("%s")' % t)]
def key(c, t, db='main'):   # the SQL that names a row's game (entities of database db), or None for a shared table
    cs = cols(c, t)
    if t == 'games': return 'id'
    if 'game' in cs: return 'game'
    for e in ('entity', 'src'):
        if e in cs: return '(SELECT game FROM %s.entities WHERE id=%s)' % (db, e)
    return None

def split(full, part, games):
    import shutil; shutil.copy(full, part)
    c = sqlite3.connect(part); ph = ','.join('?' * len(games))
    for t in tables(c):   # entities last: the other tables find a row's game through it; the games list stays whole (pattern_fix.py reads it)
        k = key(c, t)
        if t not in ('entities', 'games') and k: c.execute('DELETE FROM "%s" WHERE %s IS NOT NULL AND %s NOT IN (%s)' % (t, k, k, ph), games)
    c.execute('CREATE TABLE only_games_ids AS SELECT max(id) AS max_id FROM entities')   # new entries get ids above every game's (load_cards.py)
    c.execute('DELETE FROM entities WHERE game NOT IN (%s)' % ph, games)
    c.execute("INSERT INTO entity_fts(entity_fts) VALUES('rebuild')"); c.commit(); c.execute('VACUUM')

def merge(full, part, games):
    c = sqlite3.connect(full); c.execute('ATTACH ? AS p', (part,)); ph = ','.join('?' * len(games))
    c.execute('DROP TABLE IF EXISTS p.only_games_ids')
    mine, theirs = set(tables(c)), {t for t, in c.execute("SELECT name FROM p.sqlite_master WHERE type='table' AND name NOT LIKE 'entity_fts%' AND name NOT LIKE 'sqlite_%'")}
    for t in mine - theirs: c.execute('DROP TABLE "%s"' % t)   # dropped by the build
    for t in theirs - mine: c.execute('CREATE TABLE "%s" AS SELECT * FROM p."%s"' % (t, t))
    order = sorted(mine & theirs, key=lambda t: t == 'entities')   # entities last, as in split
    for t in order:
        if cols(c, t) != [r[1] for r in c.execute('PRAGMA p.table_info("%s")' % t)]:
            sys.exit('only_games.py: table %s changed its columns; run a full build' % t)
        k = key(c, t)
        if k: c.execute('DELETE FROM "%s" WHERE %s IS NULL OR %s IN (%s)' % (t, k, k, ph), games)
        else: c.execute('DELETE FROM "%s"' % t)
    for t in order:   # a step may write rows of every game (patterns from the files): only the named games' rows are taken
        k = key(c, t, 'p')
        if k: c.execute('INSERT INTO "%s" SELECT * FROM p."%s" WHERE %s IS NULL OR %s IN (%s)' % (t, t, k, k, ph), games)
        else: c.execute('INSERT INTO "%s" SELECT * FROM p."%s"' % (t, t))
    c.execute("INSERT INTO entity_fts(entity_fts) VALUES('rebuild')"); c.commit()
    print('only_games: rows of', ' '.join(games), 'replaced')

if __name__ == '__main__':
    {'split': split, 'merge': merge}[sys.argv[1]](sys.argv[2], sys.argv[3], sys.argv[4:])
