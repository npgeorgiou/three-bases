"""Leave-play triggers (Kaptain's decision, 20 Oct 2026): every entry whose text says "when this leaves play / the battlefield"
gets leave_trigger, "when another unit leaves play" other_leave_trigger, read sentence by sentence with death_side.side() (the
same rule as the answer key). Build step after the concept tree move; never adds a tag a hand review dropped (regression.tsv).
Usage: leave_triggers.py <db>"""
import csv, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import death_side as D
c = sqlite3.connect(sys.argv[1])
kept = dict(c.execute('SELECT old_id, kept_id FROM merged_entities').fetchall()) if c.execute("SELECT 1 FROM sqlite_master WHERE name='merged_entities'").fetchone() else {}
dropped = {(kept.get(int(r['entity']), int(r['entity'])), r['concept']) for r in csv.DictReader(open(os.path.join(HERE, 'regression.tsv'), encoding='utf-8'), delimiter='\t') if r['expect'] == 'absent'}
LEAVE = re.compile(D.LEAVE, re.I)
GRANT = re.compile(r"following effect|\b(gains?|has|have|with|gets?) [\"“]", re.I)
n = {}
for e, g, name, cat, text in c.execute("SELECT id, game, name, category, text FROM entities WHERE text IS NOT NULL AND category != 'tribe'").fetchall():
    if not LEAVE.search(text): continue
    for cl in re.split(r'(?<=[.!;])\s+|\n+', text):
        if not LEAVE.search(cl) or re.search(r"\bat least \d+|\b\d+ or more\b", cl): continue   # counting how many left is not a trigger
        for k in D.side(cl, name, cat in D.SPELLS, g) & {'leave_trigger', 'other_leave_trigger'}:
            if (e, k) in dropped: continue
            role = 'grants' if GRANT.search(cl) else 'does'   # "give a follower the following effect: when this follower leaves play"
            if c.execute('INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)', (e, k, role, 'text_pattern', cl.strip()[:60])).rowcount: n[g, k] = n.get((g, k), 0) + 1
c.commit()
for (g, k), x in sorted(n.items()): print(f'{g:18} {k:20} {x}')
