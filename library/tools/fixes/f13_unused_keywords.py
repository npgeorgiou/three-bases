"""One-time fix (12 Oct 2026, agreed with Kaptain): drop the keywords no card text uses (marked by f07 with extra.note
'used by no card text in this library'), with their tags, links and pairs, and their regression lines. Usage: f13_unused_keywords.py <db>"""
import csv, os, sqlite3, sys
c = sqlite3.connect(sys.argv[1])
ids = [i for (i,) in c.execute("SELECT id FROM entities WHERE category='keyword' AND extra LIKE '%used by no card text in this library%'")]
for i in ids:
    for s in ('DELETE FROM entity_concepts WHERE entity=?', 'DELETE FROM trigger_effect WHERE entity=?', 'DELETE FROM entity_links WHERE src=? OR dst=?',
              'DELETE FROM mechanic_repeat WHERE entity=? OR same_as=?', 'DELETE FROM merged_entities WHERE kept_id=?', 'DELETE FROM entities WHERE id=?'):
        c.execute(s, (i,) * s.count('?'))
c.execute("INSERT INTO entity_fts(entity_fts) VALUES('rebuild')")
c.commit()
f = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'regression.tsv')
rows = list(csv.reader(open(f, encoding='utf-8'), delimiter='\t'))
keep = [r for r in rows if r[1] == 'entity' or int(r[1]) not in ids]
with open(f, 'w', newline='', encoding='utf-8') as fh: csv.writer(fh, delimiter='\t').writerows(keep)
print('unused keywords dropped:', len(ids), ' regression lines removed:', len(rows) - len(keep))
