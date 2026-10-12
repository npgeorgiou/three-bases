"""Keep only the Magic cards loaded from MTGJSON (ext_id 'add:mtgjson:') that bring a mechanic the older Magic cards lack:
a pair of concepts (role does) no older Magic card has together, a concept fewer than 10 older Magic cards have, or a
trigger -> effect pair no older Magic card has. The rest repeat existing mechanics (commons, Commander cards) and are removed;
their names stay in variants / merged_entities where dedupe had already merged them. Usage: f01_mtg_cut.py <db>"""
import sqlite3, sys, itertools, collections
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
tags = collections.defaultdict(set); new = {}
for e, con, n in q("SELECT x.entity, x.concept, e.ext_id LIKE 'add:mtgjson:%' FROM entity_concepts x JOIN entities e ON e.id=x.entity WHERE e.game='mtg' AND e.category NOT IN ('keyword','tribe') AND x.role='does'"):
    tags[e].add(con); new[e] = n
for (e,) in q("SELECT id FROM entities WHERE game='mtg' AND ext_id LIKE 'add:mtgjson:%'"): new.setdefault(e, 1)
oldpairs, oldcount = set(), collections.Counter()
for e, s in tags.items():
    if not new.get(e): oldcount.update(s); oldpairs.update(itertools.combinations(sorted(s), 2))
oldtp = set(q("SELECT trigger, effect FROM trigger_effect t JOIN entities e ON e.id=t.entity WHERE e.game='mtg' AND e.ext_id NOT LIKE 'add:%'"))
tp = collections.defaultdict(set)
for e, a, b in q("SELECT entity, trigger, effect FROM trigger_effect t JOIN entities e ON e.id=t.entity WHERE e.ext_id LIKE 'add:mtgjson:%'"): tp[e].add((a, b))
keep = drop = 0
for e, n in new.items():
    if not n: continue
    s = tags.get(e, set())
    if (set(itertools.combinations(sorted(s), 2)) - oldpairs) or any(oldcount[x] < 10 for x in s) or (tp[e] - oldtp): keep += 1; continue
    for st in ("DELETE FROM entity_concepts WHERE entity=?", "DELETE FROM trigger_effect WHERE entity=?", "DELETE FROM entity_links WHERE src=? OR dst=?", "DELETE FROM entities WHERE id=?"):
        c.execute(st, (e,) * st.count('?'))
    drop += 1
c.execute("DELETE FROM load_log WHERE game='mtg' AND step LIKE 'loaded (mtgjson)%'")
c.execute("INSERT INTO load_log VALUES('mtg','loaded (mtgjson): cards with a mechanic the older Magic cards lack',?,'MTGJSON AtomicCards 5.3.0+20261011; the other new cards repeated existing mechanics and were removed')", (keep,))
c.execute("INSERT INTO load_log VALUES('mtg','loaded (mtgjson): removed, mechanic already present',?,'')", (drop,))
c.execute("INSERT INTO entity_fts(entity_fts) VALUES('rebuild')")
c.commit(); print('kept', keep, 'removed', drop)
