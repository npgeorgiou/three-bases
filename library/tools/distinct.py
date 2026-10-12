"""Distinct-mechanic marker. Table mechanic_repeat(entity, same_as, game): an entry whose category, concepts (with roles) and
trigger -> effect pairs are exactly those of an earlier entry of the same game (lower id) repeats that entry's mechanic, usually
in other numbers, costs or targets. Nothing is removed; query.py concept/search take distinct=1 to skip repeats.
Usage: distinct.py <db>"""
import sqlite3, sys, collections
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
c.execute("DROP TABLE IF EXISTS mechanic_repeat")
c.execute("CREATE TABLE mechanic_repeat(entity INTEGER PRIMARY KEY, same_as INTEGER, game TEXT)")
tags = collections.defaultdict(set); pairs = collections.defaultdict(set)
for e, k, r in q("SELECT entity, concept, role FROM entity_concepts"): tags[e].add(f'{k}:{r}')
for e, a, b in q("SELECT entity, trigger, effect FROM trigger_effect"): pairs[e].add(f'{a}>{b}')
first = {}; n = 0
for e, g, cat in q("SELECT id, game, category FROM entities WHERE category NOT IN ('keyword','tribe') ORDER BY id"):
    if not tags[e]: continue
    key = (g, cat, frozenset(tags[e]), frozenset(pairs[e]))
    if key in first: c.execute("INSERT INTO mechanic_repeat VALUES(?,?,?)", (e, first[key], g)); n += 1
    else: first[key] = e
c.commit(); print('entries marked as repeats:', n)
