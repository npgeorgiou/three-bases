"""Parent and child rule (agreed 12 Oct 2026, every game): when an entry has a narrower concept (ping), its broader ancestors
(damage, effect) are removed from that entry's tags with the same role, and from its trigger pairs with the same trigger (or the
same effect). Searches find the parent through concept_tree, so nothing is lost. Build step after trigger_pairs.py,
idempotent. Usage: parent_rule.py <db>"""
import sqlite3, sys
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
desc = {}
for r, i in q('SELECT root, id FROM concept_tree'):
    if r != i: desc.setdefault(r, set()).add(i)
tags = {}
for e, k, role in q('SELECT entity, concept, role FROM entity_concepts'): tags.setdefault((e, role), set()).add(k)
drop = [(e, role, k) for (e, role), ks in tags.items() for k in ks if desc.get(k, set()) & ks]
c.executemany('DELETE FROM entity_concepts WHERE entity=? AND role=? AND concept=?', drop)
pairs = {}
for rid, e, t, f in q('SELECT rowid, entity, trigger, effect FROM trigger_effect'): pairs.setdefault(e, []).append((rid, t, f))
pd = []
for ps in pairs.values():
    if len(ps) < 2: continue
    for rid, t, f in ps:
        if any(t2 == t and f2 in desc.get(f, ()) for _, t2, f2 in ps) or any(f2 == f and t2 in desc.get(t, ()) for _, t2, f2 in ps): pd.append((rid,))
c.executemany('DELETE FROM trigger_effect WHERE rowid=?', pd)
c.commit()
print('parent rule: tags removed', len(drop), ' trigger pairs removed', len(pd))
