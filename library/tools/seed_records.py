"""Tags and trigger pairs that no build step makes (21 Oct 2026, one chain): whole-game structure tags (game_structure: every
Battlegrounds minion is auto_battle...), card-field tags of the converters (data_rule), hand reviews and inferences kept only in
the database (claude_review, claude_inference), and the hand-made Warhammer Underworlds and Marvel Snap pairs. They live in
records/seed_tags.tsv and records/seed_pairs.tsv (tree v3 ids) and the build inserts them, so it can start from the card data.
  seed_records.py <db> before   early, in the old ids (concept_tree.to_old); tags with no old id wait for 'after'
  seed_records.py <db> after    right after the tree move: the remaining tags and the pairs
  seed_records.py <db> keep <game> ...   after loading new games: their card-field tags (data_rule, old ids) are added to
                                         records/seed_tags.tsv in the tree v3 ids, so the clean start keeps them"""
import csv, os, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from concept_tree import to_old
c = sqlite3.connect(sys.argv[1]); when = sys.argv[2]
if when == 'keep':
    from concept_tree import primary
    f = os.path.join(HERE, 'records', 'seed_tags.tsv'); have = set(open(f, encoding='utf-8').read().split('\n'))
    add = []
    for g in sys.argv[3:]:
        for e, k, r, ev in c.execute("SELECT ec.entity, ec.concept, ec.role, ec.evidence FROM entity_concepts ec JOIN entities x ON x.id=ec.entity WHERE x.game=? AND ec.method='data_rule'", (g,)):
            line = '\t'.join([str(e), primary(k)[0], r, 'data_rule', (ev or '').replace('\t', ' ').replace('\n', ' ')])
            if line not in have: add.append(line); have.add(line)
    open(f, 'a', encoding='utf-8').write(''.join(l + '\n' for l in add)); print('seed_records keep:', len(add)); sys.exit(0)
live = {i for i, in c.execute('SELECT id FROM entities')}
n = 0
for r in csv.DictReader(open(os.path.join(HERE, 'records', 'seed_tags.tsv'), encoding='utf-8'), delimiter='\t'):
    e = int(r['entity'])
    if e not in live: continue
    k = to_old(r['concept']) if when == 'before' else r['concept']
    if when == 'before' and k is None: continue
    if when == 'after' and to_old(r['concept']) is not None: continue
    n += c.execute('INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)', (e, k, r['role'], r['method'], r['evidence'])).rowcount
p = 0
if when == 'after':
    for r in csv.DictReader(open(os.path.join(HERE, 'records', 'seed_pairs.tsv'), encoding='utf-8'), delimiter='\t'):
        e = int(r['entity'])
        if e not in live or c.execute('SELECT 1 FROM trigger_effect WHERE entity=? AND trigger=? AND effect=?', (e, r['trigger'], r['effect'])).fetchone(): continue
        c.execute('INSERT INTO trigger_effect(entity, game, trigger, effect, clause, frequency, basis) VALUES(?,?,?,?,?,?,?)',
                  (e, r['game'], r['trigger'], r['effect'], r['clause'] or None, r['frequency'] or None, r['basis'] or None)); p += 1
c.commit()
print(f'seed_records {when}: tags {n}, pairs {p}')
