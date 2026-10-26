"""Scores the effect field of the script's records against the hand answer keys (tools/key/<game>/key.json), with no card
reading. A record's effect is right when it is a key concept of that entry, or an ancestor or descendant of one (key.py's rule).
precision: share of records (on keyed entries) whose effect is right; recall: share of key effect concepts some record meets.
Usage: key_score.py <db> [game ...]"""
import collections, json, os, sqlite3, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auto_records as A
KEY = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'key')

c = sqlite3.connect(sys.argv[1])
facet, anc, pats = A.load(c)
tags = collections.defaultdict(set)
for e, k in c.execute("SELECT entity, concept FROM entity_concepts WHERE role IN ('does','grants','trigger','cost')"): tags[e].add(k)
games = sys.argv[2:] or sorted(g for g in os.listdir(KEY) if os.path.exists(os.path.join(KEY, g, 'key.json')))
near = lambda a, b: a == b or b in anc.get(a, ()) or a in anc.get(b, ())
for g in games:
    key = json.load(open(os.path.join(KEY, g, 'key.json')))
    P = A.prep(c, g, facet, pats)
    good = tot = met = keyn = 0
    for eid, v in key.items():
        r = c.execute("SELECT id, name, category, text FROM entities WHERE id=?", (int(eid),)).fetchone()
        if not r or not r[3]: continue
        recs, _ = A.records(c, r[0], g, r[1], r[2], r[3], tags[r[0]], facet, anc, pats, *P)
        kc = {k for k, *_ in v['tags'] if facet.get(k) in A.EFFECT_FACETS and k not in A.SKIP}
        fx = {x[3] for x in recs}
        good += sum(1 for f in fx if any(near(f, k) for k in kc)); tot += len(fx)
        met += sum(1 for k in kc if any(near(f, k) for f in fx)); keyn += len(kc)
    print(f'{g:18} keyed {len(key):4}  effect precision {100 * good / max(1, tot):5.1f}%  recall {100 * met / max(1, keyn):5.1f}%')
