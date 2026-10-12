"""Duplicate mechanics (README suggestion 8). The library is for mechanics, not card counts, so entries that repeat the same
mechanic are merged. Two entries are duplicates when they are in the same game, faction and category and their rules text is
identical after masking the entry's own name and every number (a 40k ability printed on ten datasheets, a trinket with other
numbers, a reprint under another name). Nothing about the mechanic is lost:
  - the kept entry (lowest id) takes every concept tag and link of the others, and their names go to its `variants` list;
  - merged entries are listed in table merged_entities(old_id, kept_id, game, name), so names and ids still resolve;
  - duplicates in DIFFERENT factions are kept (the faction is information: signature/splash), joined by variant_of links.
Entries with no text or 15 characters or less (vanilla bodies) are left alone. Usage: dedupe.py <db>"""
import re, sqlite3, sys, json, collections
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
c.execute('CREATE TABLE IF NOT EXISTS merged_entities(old_id INTEGER PRIMARY KEY, kept_id INTEGER, game TEXT, name TEXT)')

def norm(t, n):
    t = (t or '').lower(); n = (n or '').lower()
    for part in sorted({n, n.split(',')[0], n.split(' [')[0], n.split(' (')[0], n.split(' // ')[0]}, key=len, reverse=True):
        if len(part) > 2: t = t.replace(part, '~')
    t = re.sub(r'\d+', '#', t)
    return re.sub(r'[^a-z#~]+', ' ', t).strip()

groups = collections.defaultdict(list)
for i, g, f, cat, n, t in q("SELECT id, game, faction, category, name, text FROM entities WHERE category NOT IN ('keyword','tribe') AND text IS NOT NULL AND length(text) > 15 ORDER BY id"):
    groups[(g, f, cat, norm(t, n))].append((i, n))
merged = collections.Counter(); var = 0
for (g, f, cat, nt), members in groups.items():
    if len(members) < 2: continue
    keep, kname = members[0]
    vs = json.loads(q('SELECT variants FROM entities WHERE id=?', keep)[0][0] or '[]')
    for i, n in members[1:]:
        c.execute("INSERT OR IGNORE INTO entity_concepts SELECT ?, concept, role, method, evidence FROM entity_concepts WHERE entity=?", (keep, i))
        c.execute("INSERT OR IGNORE INTO entity_links SELECT ?, rel, dst, evidence FROM entity_links WHERE src=? AND dst<>?", (keep, i, keep))
        c.execute("INSERT OR IGNORE INTO entity_links SELECT src, rel, ?, evidence FROM entity_links WHERE dst=? AND src<>?", (keep, i, keep))
        for t in (json.loads(q('SELECT variants FROM entities WHERE id=?', i)[0][0] or '[]') + [n]):
            if t != kname and t not in vs: vs.append(t)
        for tbl, col in (('entity_concepts', 'entity'), ('trigger_effect', 'entity')): c.execute(f'DELETE FROM {tbl} WHERE {col}=?', (i,))
        c.execute('DELETE FROM entity_links WHERE src=? OR dst=?', (i, i))
        c.execute('DELETE FROM entities WHERE id=?', (i,))
        c.execute('UPDATE merged_entities SET kept_id=? WHERE kept_id=?', (keep, i))
        c.execute('INSERT OR REPLACE INTO merged_entities VALUES(?,?,?,?)', (i, keep, g, n))
        merged[g] += 1
    c.execute('UPDATE entities SET variants=? WHERE id=?', (json.dumps(vs, ensure_ascii=False), keep))
# the same mechanic in different factions: variant_of between the kept entries
cross = collections.defaultdict(list)
for (g, f, cat, nt), members in groups.items(): cross[(g, cat, nt)].append(members[0][0])
for k, ids in cross.items():
    for i in ids[1:]: var += c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (i, 'variant_of', ids[0], 'same mechanic in another faction (dedupe.py)')).rowcount
for g, n in merged.items():
    c.execute("DELETE FROM load_log WHERE game=? AND step='dedupe'", (g,))
    c.execute("INSERT INTO load_log VALUES(?,?,?,?)", (g, 'dedupe', n, 'entries merged into an entry with the same mechanic (same faction and category, same text apart from names and numbers); names kept in variants and merged_entities'))
c.execute("INSERT INTO entity_fts(entity_fts) VALUES('rebuild')")
c.commit()
print('merged:', sum(merged.values()), dict(merged.most_common()), ' cross-faction variant_of links:', var)
