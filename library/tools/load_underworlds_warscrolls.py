"""Warhammer Underworlds warband rules (Embergard edition): the warscroll abilities of 8 warbands and the shared Grand Alliance
warscrolls, from the official PDFs listed in lib/underworlds_warscrolls.json (paraphrased; concepts hand-mapped, claude_review).
Each entry is an 'ability' with the warband (or Grand Alliance) as faction and the warscroll as subtype. Idempotent.
Usage: load_underworlds_warscrolls.py <db>"""
import json, sqlite3, sys, os, re
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'underworlds_warscrolls.json'), encoding='utf-8'))
G = 'wh_underworlds'
old = [i for (i,) in q("SELECT id FROM entities WHERE game=? AND ext_id LIKE 'warscroll:%'", G)]
for i in old:
    for s in ("DELETE FROM entity_concepts WHERE entity=?", "DELETE FROM entity_links WHERE src=? OR dst=?", "DELETE FROM trigger_effect WHERE entity=?", "DELETE FROM entities WHERE id=?"):
        c.execute(s, (i,) * s.count('?'))
ok = {i for (i,) in q('SELECT id FROM concepts')}
kw = {n.lower(): i for n, i in q("SELECT name, id FROM entities WHERE game=? AND category='keyword'", G)}
kw_forms = {'inspired': r'\binspire[ds]?\b', 'push': r'\bpush(es|ed)?\b'}
nid = q('SELECT max(id) FROM entities')[0][0] + 1
n = bad = 0
for fac, scroll, name, text, cons, pairs in d['entries']:
    c.execute("INSERT INTO entities(id, game, ext_id, name, category, source_type, edition, faction, subtypes, text) VALUES(?,?,?,?,?,?,?,?,?,?)",
              (nid, G, 'warscroll:' + name, name, 'ability', 'warband warscroll (official PDF, paraphrased by Claude)', 'Embergard warband rules', fac, scroll, text))
    for it in cons:
        con, role = (it.split(':') + ['does'])[:2]
        if con not in ok: print('unknown concept', con, name); bad += 1; continue
        c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (nid, con, role, 'claude_review', 'hand-mapped from the warscroll'))
    for p in pairs:
        t, e = p.split('>')
        c.execute("INSERT INTO trigger_effect(entity, game, trigger, effect, clause) VALUES(?,?,?,?,?)", (nid, G, t, e, text))
    for k, i in kw.items():
        if re.search(kw_forms.get(k, r'\b' + re.escape(k) + r'\b'), text, re.I):
            c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (nid, 'mentions_keyword', i, 'warscroll text'))
    nid += 1; n += 1
c.execute("DELETE FROM load_log WHERE game=? AND step='warscrolls'", (G,))
c.execute("INSERT INTO load_log VALUES(?,?,?,?)", (G, 'warscrolls', n, d['_source']))
c.execute("INSERT INTO entity_fts(entity_fts) VALUES('rebuild')")
c.commit(); print('Underworlds warscroll abilities loaded:', n, ' unknown concepts:', bad)
