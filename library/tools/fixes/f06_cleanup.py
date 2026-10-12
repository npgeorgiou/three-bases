"""Leftovers. Usage: f06_cleanup.py <db>
  - Hearthstone: hsdata helper entries that are not cards (names with Dummy / FX, text "Holds an effect / the FX", text "???"),
    puzzle and anomaly entries (PvE modes, which the load meant to leave out).
  - Exact duplicates (same game, name, faction, category and text) are merged into the lowest id (tags, links and pairs move over).
  - load_log: per-game "post-pass dropped ... no concept tags" lines of the first build are kept as history but say so; the later
    loads have their own lines."""
import sqlite3, sys, re, collections
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
C = collections.Counter()
def drop(i):
    for st in ("DELETE FROM entity_concepts WHERE entity=?", "DELETE FROM trigger_effect WHERE entity=?", "DELETE FROM entity_links WHERE src=? OR dst=?", "DELETE FROM entities WHERE id=?"):
        c.execute(st, (i,) * st.count('?'))
for i, n, t in q("SELECT id, name, coalesce(text,'') FROM entities WHERE game IN ('hearthstone','hs_battlegrounds') AND category NOT IN ('keyword','tribe')"):
    if re.search(r'\b(Dummy|FX)\b', n) or re.match(r'Holds (an|the) (effect|FX)', t) or t.strip() == '???' or re.search(r'\bPuzzle\b', t) or n.startswith('Anomaly - '):
        drop(i); C['hearthstone helper / PvE entry removed'] += 1
for g, n, f, k, t in q("""SELECT game, name, faction, category, text FROM entities WHERE category NOT IN ('keyword','tribe')
                          GROUP BY game, name, faction, category, text HAVING count(*) > 1"""):
    ids = [i for (i,) in q("SELECT id FROM entities WHERE game=? AND name=? AND faction IS ? AND category=? AND text IS ? ORDER BY id", g, n, f, k, t)]
    keep, rest = ids[0], ids[1:]
    for r in rest:
        c.execute("INSERT OR IGNORE INTO entity_concepts SELECT ?, concept, role, method, evidence FROM entity_concepts WHERE entity=?", (keep, r))
        c.execute("INSERT OR IGNORE INTO entity_links SELECT ?, rel, dst, evidence FROM entity_links WHERE src=? AND dst<>?", (keep, r, keep))
        c.execute("INSERT OR IGNORE INTO entity_links SELECT src, rel, ?, evidence FROM entity_links WHERE dst=? AND src<>?", (keep, r, keep))
        c.execute("INSERT INTO trigger_effect(entity, game, trigger, effect, clause, frequency, basis) SELECT ?, game, trigger, effect, clause, frequency, basis FROM trigger_effect t WHERE entity=? AND NOT EXISTS (SELECT 1 FROM trigger_effect u WHERE u.entity=? AND u.trigger=t.trigger AND u.effect=t.effect)", (keep, r, keep))
        c.execute("INSERT INTO merged_entities VALUES(?,?,?,?)", (r, keep, g, n))
        drop(r); C['exact duplicate merged'] += 1
C['load_log lines marked'] = c.execute("""UPDATE load_log SET step='first build: post-pass dropped entries with no concept tags (no pattern or keyword matched); later loads re-added those they reach'
    WHERE step='post-pass dropped entries with no concept tags (no pattern or keyword matched)'""").rowcount
c.execute("INSERT INTO entity_fts(entity_fts) VALUES('rebuild')")
c.commit(); print(dict(C))
