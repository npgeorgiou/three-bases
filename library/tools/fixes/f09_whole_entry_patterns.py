"""trigger_pairs.py read whole-entry patterns clause by clause, so a guard on the whole text ("no Timing: line" for Age of Sigmar
passive, "not a 'score this' objective" for Underworlds destroy) passed on every clause. Tags and pairs made that way are removed
where the whole text fails the guard and no other pattern of the concept matches (reviewed tags kept). Usage: f09_whole_entry_patterns.py <db>"""
import os, re, sqlite3, sys
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
lib = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
keep = set()
for line in open(os.path.join(lib, 'regression.tsv'), encoding='utf-8'):
    f = line.rstrip('\n').split('\t')
    if len(f) >= 6 and f[5] == 'present' and f[1].isdigit(): keep.add((int(f[1]), f[3]))
n = t_ = 0
for g, con, p in q("SELECT game, concept, pattern FROM concept_patterns WHERE pattern LIKE '(?s)^(?!%' AND game IS NOT NULL"):
    whole = re.compile(p, re.I)
    others = [re.compile(x, re.I) for (x,) in q("SELECT pattern FROM concept_patterns WHERE concept=? AND (game IS NULL OR game=?) AND pattern<>?", con, g, p)]
    for e, tx in q("SELECT id, text FROM entities WHERE game=? AND text IS NOT NULL", g):
        low = tx.lower()
        if whole.search(low) or any(o.search(low) for o in others): continue
        if (e, con) not in keep: n += c.execute("DELETE FROM entity_concepts WHERE entity=? AND concept=? AND method='text_pattern'", (e, con)).rowcount
        t_ += c.execute("DELETE FROM trigger_effect WHERE entity=? AND (trigger=? OR effect=?)", (e, con, con)).rowcount
c.commit(); print('tags removed', n, 'pairs removed', t_)
