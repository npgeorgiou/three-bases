"""One-time fix (12 Oct 2026): of the 52 entries that had no tags, the one whose text has no mechanic at all is dropped
(Hearthstone, Natural Leader: flavour text only). The other 51 were read and tagged in tools/reviews/. Usage: f14_no_mechanic.py <db>"""
import sqlite3, sys
c = sqlite3.connect(sys.argv[1])
ids = [i for (i,) in c.execute("SELECT id FROM entities WHERE id IN (797729) AND game='hearthstone' AND name='Natural Leader'")]
for i in ids:
    for s in ('DELETE FROM entity_concepts WHERE entity=?', 'DELETE FROM trigger_effect WHERE entity=?', 'DELETE FROM entity_links WHERE src=? OR dst=?',
              'DELETE FROM mechanic_repeat WHERE entity=? OR same_as=?', 'DELETE FROM entities WHERE id=?'):
        c.execute(s, (i,) * s.count('?'))
c.execute("INSERT INTO entity_fts(entity_fts) VALUES('rebuild')")
c.commit(); print('entries with no mechanic dropped:', len(ids))
