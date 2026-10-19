"""Concept relations added after the tree v3 move (Claude's analysis, 20 Oct 2026, asked by Kaptain): tools/relations_added.tsv,
one per line (a, rel, b, note). Build step after concept_tree.py apply (that step rewrites the relations table from the old ids).
Idempotent. Usage: relations_added.py <db>"""
import csv, os, sqlite3, sys
c = sqlite3.connect(sys.argv[1]); n = 0
ok = {i for i, in c.execute('SELECT id FROM concepts')}
for r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'relations_added.tsv'), encoding='utf-8'), delimiter='\t'):
    assert r['a'] in ok and r['b'] in ok, (r['a'], r['b'])
    if not c.execute('SELECT 1 FROM concept_relations WHERE a=? AND rel=? AND b=?', (r['a'], r['rel'], r['b'])).fetchone():
        c.execute("INSERT INTO concept_relations VALUES(?,?,?,?,'claude_analysis')", (r['a'], r['rel'], r['b'], r['note'])); n += 1
c.commit(); print('relations added:', n)
