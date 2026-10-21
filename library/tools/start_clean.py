"""First build step after expand (21 Oct 2026, one chain): every derived tag and trigger pair is removed, so the build starts
from the card data (entities, links, games, merges) and the record files, and its output never depends on an earlier build.
The tree move's logs are emptied too, so concept_tree.py restore only switches the concept tables back. Usage: start_clean.py <db>"""
import sqlite3, sys
c = sqlite3.connect(sys.argv[1])
for t in ('entity_concepts', 'trigger_effect', 'tree_v3_moved', 'tree_v3_added'):
    if c.execute("SELECT 1 FROM sqlite_master WHERE name=?", (t,)).fetchone(): c.execute('DELETE FROM %s' % t)
c.commit(); print('start_clean: tags and pairs removed')
