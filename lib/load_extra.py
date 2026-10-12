"""Load cards the first build never had or dropped, from a JSON file of {'_source', 'cards': [...] (created / non-collectible),
'collectible_missing': [...] (collectible cards the first build dropped)}, for one game.
Each card: id, name, type (game code or word), class/faction, cost, atk, hp, text. Tagging: the general and per-game wording patterns
(text_pattern, honouring the game's '!' switch-offs), keyword links (a keyword at the start of a sentence = has_keyword, with its
reviewed concepts inherited via_keyword; elsewhere mentions_keyword), and trigger -> effect pairs are made later by trigger_pairs.py. Entries whose text names a created card get a 'generates' link to it.
A name that already exists in the game gets ' (created)'. Idempotent (ext_id 'extra:<id>').
Usage: load_extra.py <db> <game> <json>"""
import json, os, re, sqlite3, sys
db, G, path = sys.argv[1:4]
c = sqlite3.connect(db); q = lambda s, *a: c.execute(s, a).fetchall()
here = os.path.dirname(os.path.abspath(__file__))
for (i,) in q("SELECT id FROM entities WHERE game=? AND ext_id LIKE 'extra:%'", G):
    for s in ("DELETE FROM entity_concepts WHERE entity=?", "DELETE FROM entity_links WHERE src=? OR dst=?", "DELETE FROM trigger_effect WHERE entity=?", "DELETE FROM entities WHERE id=?"):
        c.execute(s, (i,) * s.count('?'))
d = json.load(open(path, encoding='utf-8'))
CAT = {'4': 'unit', '5': 'spell', '7': 'item', '39': 'building', 'minion': 'unit', 'spell': 'spell', 'weapon': 'item', 'location': 'building', 'unit': 'unit', 'hero': 'hero', 'item': 'item', 'modifier': 'modifier'}
excl = set()
pf = os.path.join(here, 'patterns', G + '.txt')
if os.path.exists(pf):
    for line in open(pf, encoding='utf-8'):
        if line.startswith('!'): excl.add(tuple(line[1:].rstrip('\n').split('|', 1)))
pats = []
for con, role, p, g in q("SELECT concept, role, pattern, game FROM concept_patterns WHERE game IS NULL OR game=?", G):
    if g is None and any(con == a and b in p for a, b in excl): continue
    try: pats.append((con, role, re.compile(p, re.I)))
    except re.error: pass
kw = {n.lower(): i for n, i in q("SELECT name, id FROM entities WHERE game=? AND category='keyword'", G)}
kwrx = [(k, i, re.compile(r'(^|[.:]\s*)' + re.escape(k) + r'\b', re.I), re.compile(r'\b' + re.escape(k) + r'\b', re.I)) for k, i in kw.items() if len(k) >= 3]
names = {n for (n,) in q("SELECT name FROM entities WHERE game=?", G)}
orig = set(names)
nid = q('SELECT max(id) FROM entities')[0][0] + 1
n = 0
for card in [dict(x, _c=False) for x in d['cards']] + [dict(x, _c=True) for x in d.get('collectible_missing', [])]:
    text = card['text']; low = text.lower()
    name = card['name'] if card['name'] not in names else card['name'] + ' (created)'
    stats = f"{card['atk']}|{card['hp']}" if card.get('atk') is not None and card.get('hp') is not None else None
    cost = card.get('cost')
    c.execute("INSERT INTO entities(id, game, ext_id, name, category, source_type, edition, faction, cost, cost_num, stats, text) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (nid, G, 'extra:' + card['id'], name, CAT.get(str(card['type']).lower(), 'unit'), 'card' if card['_c'] else 'created card', 'collectible' if card['_c'] else 'non-collectible', card.get('class'),
               cost, float(cost) if cost not in (None, '') and str(cost).lstrip('-').isdigit() else None, stats, text))
    for con, role, p in pats:
        m = p.search(low)
        if m: c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (nid, con, role, 'text_pattern', low[max(0, m.start() - 20): m.start() + 40]))
    for k, kid, start, any_ in kwrx:
        if start.search(text):
            c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (nid, 'has_keyword', kid, 'keyword in text'))
            c.execute("INSERT OR IGNORE INTO entity_concepts SELECT ?, concept, role, 'via_keyword', 'inherited from a reviewed keyword' FROM entity_concepts WHERE entity=?", (nid, kid))
        elif any_.search(text):
            c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (nid, 'mentions_keyword', kid, 'keyword in text'))
    names.add(name); nid += 1; n += 1
# name links: an entry whose text names a created card generates it (names of 5+ characters, whole words)
new = {nm.split(' (created)')[0]: i for i, nm in q("SELECT id, name FROM entities WHERE game=? AND ext_id LIKE 'extra:%' AND edition='non-collectible'", G)}
cand = sorted((nm for nm in new if len(nm) >= 5 and nm not in orig), key=len, reverse=True)   # a name shared with an existing card is ambiguous
L = 0
for k in range(0, len(cand), 400):
    rx = re.compile(r'\b(' + '|'.join(re.escape(x) for x in cand[k:k + 400]) + r')\b')
    for e, t in q("SELECT id, text FROM entities WHERE game=? AND text IS NOT NULL AND category NOT IN ('keyword','tribe')", G):
        for m in set(rx.findall(t)):
            if new[m] != e: L += c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (e, 'generates', new[m], 'names a created card')).rowcount
print('name links to created cards:', L)
c.execute("DELETE FROM load_log WHERE game=? AND step='created cards loaded'", (G,))
c.execute("INSERT INTO load_log VALUES(?,?,?,?)", (G, 'created cards loaded', n, d['_source']))
c.execute("INSERT INTO entity_fts(entity_fts) VALUES('rebuild')")
c.commit(); print(G, 'created cards loaded:', n)
