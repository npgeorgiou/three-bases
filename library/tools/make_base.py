"""One-time (21 Oct 2026, one chain): freeze the library's tagging as source tables, because the first build's corpus and code are
gone and its curated tags cannot be re-derived (a build from the card data alone was reproducible but far worse on the key).
From the stored library, with the last tree move undone (the old ids the early build steps work in), it copies
entity_concepts -> base_tags, trigger_effect -> base_pairs and the game pattern rows -> base_patterns. Every build then starts
from these (start_clean.py), so its output depends only on them, the card data, the record files and the tools.
Usage: make_base.py <db>   (run on an expanded copy; compact it again afterwards)"""
import os, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import concept_tree as T
c = sqlite3.connect(sys.argv[1])
T.restore(c)
for base, src in (('base_tags', 'entity_concepts'), ('base_pairs', 'trigger_effect')):
    c.execute('DROP TABLE IF EXISTS %s' % base); c.execute('CREATE TABLE %s AS SELECT * FROM %s' % (base, src))
c.execute('DROP TABLE IF EXISTS base_patterns'); c.execute('CREATE TABLE base_patterns AS SELECT * FROM concept_patterns WHERE game IS NOT NULL')
c.commit()
print('base:', *(c.execute('SELECT count(*) FROM %s' % t).fetchone()[0] for t in ('base_tags', 'base_pairs', 'base_patterns')))
