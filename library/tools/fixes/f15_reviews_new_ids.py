"""One-time fix (19 Oct 2026, asked by Kaptain): the review records named concepts of the old tree. This rewrites them in the tree v3
ids, with the Step 1 rules of concept_tree.py (per entry, by its text):
  - a reviewed add becomes the concepts the old tag moves to on that entry (targets(): stat_swap -> stat_gain and/or stat_loss,
    attack_mod -> buff and/or debuff, return_to_hand -> also bounce_enemy for enemy units, ...);
  - a reviewed drop becomes the old concept's main new id(s) that the entry's text points to (never a parent carried along);
    a drop of a removed mechanism (stat_set, stat_swap, attack_mod, control) is left out: "it doesn't set stats" says nothing
    about stat gain from other wording.
Files: tools/reviews/*.json, tools/reviews_outcome/*.json, tools/snap_review.json and tools/regression.tsv.
Usage: f15_reviews_new_ids.py <db> <regression.tsv to convert>   (prints counts only)"""
import csv, glob, json, os, sqlite3, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, HERE)
from concept_tree import MAP, REMOVED, primary, targets, TREE
c = sqlite3.connect(sys.argv[1]); src = sys.argv[2]
mk = dict(c.execute('SELECT old_id, kept_id FROM merged_entities'))
txt = {i: t for i, t in c.execute('SELECT id, text FROM entities')}
byname = {(g, n): i for i, g, n in c.execute('SELECT id, game, name FROM entities')}

def conv(k, text, drop):
    if k not in MAP: return [k]
    if drop:
        if k in REMOVED: return []
        return sorted(set(targets(k, text)) & set(primary(k))) or primary(k)[:1]
    return sorted(targets(k, text))

n = {'changed': 0, 'files': 0}
for f in sorted(glob.glob(os.path.join(HERE, 'reviews', '*.json')) + glob.glob(os.path.join(HERE, 'reviews_outcome', '*.json')) + [os.path.join(HERE, 'snap_review.json')]):
    game = 'marvel_snap' if f.endswith('snap_review.json') else os.path.basename(f)[:-5]
    d = json.load(open(f, encoding='utf-8'))
    for key, r in d.items():
        if not isinstance(r, dict): continue
        i = int(key) if key.isdigit() else byname.get((game, key))
        text = txt.get(mk.get(i, i)) if i else None
        for a in ('add', 'drop'):
            out = []
            for it in r.get(a, []):
                k, *role = it.split(':')
                for x in conv(k, text, a == 'drop'):
                    y = ':'.join([x] + role)
                    if y not in out: out.append(y)
                if k in MAP: n['changed'] += 1
            r[a] = out
    json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); n['files'] += 1
rows = list(csv.DictReader(open(src, encoding='utf-8'), delimiter='\t')); fields = list(rows[0].keys()); out = []; seen = set()
for r in rows:
    e = mk.get(int(r['entity']), int(r['entity']))
    for x in conv(r['concept'], txt.get(e), r['expect'] == 'absent'):
        key = (r['entity'], x, r['role'], r['expect'])
        if key not in seen: seen.add(key); out.append(dict(r, concept=x))
with open(os.path.join(HERE, 'regression.tsv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=fields, delimiter='\t', lineterminator='\n'); w.writeheader(); w.writerows(out)
bad = sorted({r['concept'] for r in out if r['concept'] not in TREE})
print('review files', n['files'], 'old concepts converted', n['changed'], '; regression lines', len(rows), '->', len(out), '; not in tree v3:', bad)
