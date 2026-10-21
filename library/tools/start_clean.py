"""Build step right after concept_tree.py restore (21 Oct 2026, one chain): every tag and trigger pair is replaced by the frozen
base (base_tags, base_pairs: the first build's curated tagging, which cannot be re-derived; see make_base.py) and the game pattern
rows by base_patterns, so game_patterns.py always compares the pattern files with the same starting rows. The build's output then
depends only on the base, the card data, the record files and the tools, never on an earlier build.
  start_clean.py <db>                 the step
  start_clean.py <db> keep <game> ... after load_cards.py added new games: their first tags and pairs join the base"""
import sqlite3, sys
c = sqlite3.connect(sys.argv[1])
if sys.argv[2:3] == ['keep']:
    for g in sys.argv[3:]:
        for t, src in (('base_tags', 'entity_concepts'), ('base_pairs', 'trigger_effect')):
            c.execute('DELETE FROM %s WHERE entity IN (SELECT id FROM entities WHERE game=?)' % t, (g,))
            c.execute('INSERT INTO %s SELECT s.* FROM %s s JOIN entities e ON e.id=s.entity WHERE e.game=?' % (t, src), (g,))
    c.commit(); print('start_clean keep:', *sys.argv[3:]); sys.exit(0)
for t in ('tree_v3_moved', 'tree_v3_added'):
    if c.execute("SELECT 1 FROM sqlite_master WHERE name=?", (t,)).fetchone(): c.execute('DELETE FROM %s' % t)
c.execute('DELETE FROM entity_concepts'); c.execute('INSERT INTO entity_concepts SELECT * FROM base_tags')
c.execute('DELETE FROM trigger_effect'); c.execute('INSERT INTO trigger_effect SELECT * FROM base_pairs')
c.execute('DELETE FROM concept_patterns WHERE game IS NOT NULL'); c.execute('INSERT INTO concept_patterns SELECT * FROM base_patterns')
c.commit(); print('start_clean: base tags, pairs and game patterns in place')
