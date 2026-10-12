"""12 Oct 2026, run once. apply_review.py now copies a hand-review decision only to entries of the same category with the very same
text (a card with a potion's words is not a consumable). This removes the review tags ('claude_review') that older builds copied
across categories: from an entry nobody reviewed, a concept that only a reviewed entry of another category with its text added.
Usage: f12_review_same_category.py <db> <reviews dir>"""
import collections, glob, json, os, sqlite3, sys
c = sqlite3.connect(sys.argv[1]); R = sys.argv[2]
cat = dict(c.execute('SELECT id, category FROM entities')); txt = dict(c.execute('SELECT id, text FROM entities')); game = dict(c.execute('SELECT id, game FROM entities'))
by = collections.defaultdict(list)
for i, t in txt.items():
    if t: by[(game[i], t)].append(i)
rev = {}
for f in glob.glob(os.path.join(R, '*.json')):
    for k, r in json.load(open(f, encoding='utf-8')).items():
        if k.isdigit(): rev[int(k)] = {x.split(':')[0] for x in r.get('add', [])}
cross, same = collections.defaultdict(set), collections.defaultdict(set)
for i, adds in rev.items():
    if i not in txt or not txt[i]: continue
    for j in by[(game[i], txt[i])]:
        if j == i or j in rev: continue
        (same if cat[j] == cat[i] else cross)[j] |= adds
n = 0
for j, cons in cross.items():
    for con in cons - same[j]:
        n += c.execute("DELETE FROM entity_concepts WHERE entity=? AND concept=? AND method='claude_review'", (j, con)).rowcount
c.commit(); print('review tags copied across categories removed:', n)
