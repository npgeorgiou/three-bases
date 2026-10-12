"""Precision estimate per concept and game, from the hand reviews (no extra reading needed). On every entry a review touched
(any line of tools/regression.tsv), an automatic tag that is still there was judged right (the reviewer read the entry and kept it),
and a reviewed drop was an automatic tag judged wrong; a reviewed add with no automatic tag is one the patterns missed.
Table concept_precision(game, concept, kept, dropped, missed, precision, recall) for cells with 10+ judged automatic tags.
`concept` prints a warning for a game whose precision for the concept is below 0.7. Usage: precision.py <db>"""
import csv, os, sqlite3, sys, collections
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
here = os.path.dirname(os.path.abspath(__file__))
kept_id = dict(q('SELECT old_id, kept_id FROM merged_entities')) if q("SELECT 1 FROM sqlite_master WHERE name='merged_entities'") else {}
rows = list(csv.DictReader(open(os.path.join(here, 'regression.tsv'), encoding='utf-8'), delimiter='\t'))
game = dict(q('SELECT id, game FROM entities'))
reviewed = {kept_id.get(int(r['entity']), int(r['entity'])) for r in rows}
drop = collections.Counter(); add = collections.Counter(); keep = collections.Counter()
for r in rows:
    e = kept_id.get(int(r['entity']), int(r['entity']))
    if e not in game: continue
    if r['expect'] == 'absent': drop[game[e], r['concept']] += 1
    elif r['expect'] == 'present': add[game[e], r['concept']] += 1
auto = ('text_pattern', 'engine_rule')
for e, k in q("SELECT entity, concept FROM entity_concepts WHERE method IN (?,?)", *auto):
    if e in reviewed and e in game: keep[game[e], k] += 1
c.execute('DROP TABLE IF EXISTS concept_precision')
c.execute('CREATE TABLE concept_precision(game TEXT, concept TEXT, kept INTEGER, dropped INTEGER, missed INTEGER, precision REAL, recall REAL)')
n = 0
for key in set(keep) | set(drop):
    k, d, m = keep[key], drop[key], add[key]
    if k + d < 10: continue
    c.execute('INSERT INTO concept_precision VALUES(?,?,?,?,?,?,?)', (*key, k, d, m, round(k / (k + d), 2), round(k / (k + m), 2) if k + m else None)); n += 1
c.commit()
low = q('SELECT game, concept, precision, kept+dropped FROM concept_precision WHERE precision < 0.7 ORDER BY kept+dropped DESC')
print('precision cells:', n, ' below 0.7:', len(low), [f'{g}/{k} {p}' for g, k, p, _ in low[:15]])
