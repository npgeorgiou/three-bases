"""Load new entries into an existing library, with the same tagging the first build used (incremental; the raw corpus is gone).
Input JSON: {'_source': str, '_tag': str, 'cards': [...]}. Each card: ext_id, name, category, and optionally source_type, edition,
faction, subtypes (list), rarity, cost, cost_num, stats (str or dict), text, extra (dict), extra_updates at file level (merged into existing entries' extra), _game at file level (the games row of a new game), variant_of (name of the entry this one is a version of, same faction; link variant_of), keywords (list of keyword names the
source lists for the card), created (true for tokens / created cards). File options: _strip_reminder (read the text without
reminder text in parentheses, as the first build read Magic), _keywords_from_field (keyword links only from the cards' keywords field: has_keyword when the card has it,
grants_keyword with inherited role 'grants' when the text gives it ("creatures you control have flying"), else mentions_keyword).
Patterns read the text lower-cased, with the entry's own name written as 'name' and a card named in it ('named X') as 'namedcard'.
For each new entry:
  - text patterns: the general patterns (honouring the game's '!' switch-offs in patterns/<game>.txt) and the game's own patterns
    (method text_pattern, evidence = the matched text);
  - keywords: a keyword the source lists for the card, or one that starts a sentence of its text = has_keyword, with the keyword's
    reviewed concepts inherited (via_keyword); a keyword named elsewhere in the text = mentions_keyword;
  - types: each subtype that is a tribe entity of the game = has_type; a tribe named in the text = cares_about_type (not in a
    list of four or more tribes, e.g. "choose Elf, Goblin, Merfolk or ...");
  - names: "named X" or "card named X" for an entry X of the game = references; a created entry named in another entry's text =
    generates (names of 5+ characters that no older entry shares).
A name the game already has in the same faction is skipped (counted in load_log), unless the card is created and the name is free with ' (created)'.
Trigger -> effect pairs, frequency, outcome concepts, link rules and signatures are made by the later build steps.
Idempotent per tag: entries with ext_id 'add:<tag>:...' are removed first. A file from export_game.py (_reload) keeps every entry's id,
ext_id and name, skips no duplicate name, and derives no links: it restores the game's links (_links) with their inherited
keyword tags. Usage: load_cards.py <db> <game> <json>"""
import json, os, re, sqlite3, sys
db, G, path = sys.argv[1:4]
c = sqlite3.connect(db); q = lambda s, *a: c.execute(s, a).fetchall()
here = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(path, encoding='utf-8')); TAG = d['_tag']; PRE = f'add:{TAG}:'
RELOAD = d.get('_reload', False)   # export_game.py: each entry keeps its id and ext_id, so id-keyed reviews, key and regression still apply
for (i,) in [] if RELOAD else q("SELECT id FROM entities WHERE game=? AND ext_id LIKE ?", G, PRE + '%'):
    for s in ("DELETE FROM entity_concepts WHERE entity=?", "DELETE FROM entity_links WHERE src=? OR dst=?", "DELETE FROM trigger_effect WHERE entity=?", "DELETE FROM entities WHERE id=?"):
        c.execute(s, (i,) * s.count('?'))
sys.path.insert(0, here); from concept_tree import primary   # pattern files use the old ids (game_patterns.py runs before the tree move)
excl = set()
pf = os.path.join(here, 'patterns', G + '.txt')
if os.path.exists(pf):
    for line in open(pf, encoding='utf-8'):
        if line.startswith('!'): excl.add(tuple(line[1:].rstrip('\n').split('|', 1)))
pats = []
for con, role, p, g in q("SELECT concept, role, pattern, game FROM concept_patterns WHERE game IS NULL OR game=?", G):
    if g is None and any((con == a or con in primary(a)) and b in p for a, b in excl): continue   # a '!' line in an old id also covers its new ids
    try: pats.append((con, role, re.compile(p, re.I)))
    except re.error: pass
kw = {n.lower(): i for n, i in q("SELECT name, id FROM entities WHERE game=? AND category='keyword'", G)}
kwrx = [(k, i, re.compile(r'(^|[.:\n]\s*)' + re.escape(k) + r'\b', re.I), re.compile(r'\b' + re.escape(k) + r'\b', re.I)) for k, i in kw.items() if len(k) >= 3]
tribes = {n.lower(): i for n, i in q("SELECT name, id FROM entities WHERE game=? AND category='tribe'", G)}
trx = [(t, i, re.compile(r'\b' + re.escape(t) + r'(s|es)?\b', re.I)) for t, i in tribes.items() if len(t) >= 3]
byname = {n: i for n, i in q("SELECT name, id FROM entities WHERE game=? AND category NOT IN ('keyword','tribe')", G)}
orig = set(byname)
seen = set(q("SELECT name, faction FROM entities WHERE game=?", G))
import reading as RD; STRIP = d.get('_strip_reminder', False) or G in RD.NO_REMINDER; FIELD = d.get('_keywords_from_field', False)
NAMED = re.compile(r'\bnamed ' + '(' + '|'.join(re.escape(x.lower()) for x in sorted(byname, key=len, reverse=True) if len(x) >= 4) + r')\b') if byname else re.compile(r'(?!x)x')
nid = q('SELECT max(id) FROM entities')[0][0] + 1
n = skipped = 0; new_ids = []
for card in d['cards']:
    name = card['name']
    if RELOAD: nid = card['id']
    elif (name, card.get('faction')) in seen:
        if not card.get('created') or (name + ' (created)', card.get('faction')) in seen: skipped += 1; continue
        name += ' (created)'
    text = card.get('text') or ''
    low = text.lower()
    if STRIP: low = re.sub(r'\([^()]*\)', ' ', low)   # reminder text, as the first build read Magic cards
    for nm in [name] + name.split(' // '):
        if len(nm) > 2: low = low.replace(nm.lower(), 'name')
    low = NAMED.sub('named namedcard', low)
    mtext = low
    stats = card.get('stats'); stats = json.dumps(stats) if isinstance(stats, dict) else stats
    cost = card.get('cost'); cn = card.get('cost_num')
    if cn is None and cost not in (None, '') and str(cost).lstrip('-').isdigit(): cn = float(cost)
    sub = card.get('subtypes')
    if card.get('created'):   # created cards carry edition 'non-collectible', as in the earlier loads; the source's set goes to extra.set
        card['extra'] = dict(card.get('extra') or {}, **({'set': card['edition']} if card.get('edition') else {})); card['edition'] = 'non-collectible'
    c.execute("INSERT INTO entities(id, game, ext_id, name, category, source_type, edition, faction, subtypes, rarity, cost, cost_num, stats, text, extra, variants) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (nid, G, card['ext_id'] if RELOAD else PRE + str(card['ext_id']), name, card['category'], card.get('source_type'), card.get('edition'), card.get('faction'),
               json.dumps(sub) if sub else None, card.get('rarity'), cost, cn, stats, text or None, json.dumps(card['extra']) if card.get('extra') else None,
               json.dumps(card['variants'], ensure_ascii=False) if card.get('variants') else None))
    if card.get('keep_tags'):   # reload: the entry's current tags instead of today's general patterns
        c.executemany('INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)', [(nid, *t) for t in card['keep_tags']])
    for con, role, p in [] if card.get('keep_tags') else pats:
        m = p.search(low)
        if m: c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (nid, con, role, 'text_pattern', low[max(0, m.start() - 20): m.start() + 40]))
    for con, role, ev in card.get('tags') or []:   # data rules the converter read from the card's fields (method data_rule)
        c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (nid, con, role, 'data_rule', ev))
    listed = {k.lower() for k in card.get('keywords') or []}
    for k, kid, start, any_ in [] if RELOAD else kwrx:
        own = start.search(mtext) or (k in listed and not any_.search(mtext))   # listed and not written out (e.g. a face name) = its own
        if FIELD and not (k in listed and own) and re.search(r'\b(have|has|gains?|gives?|give it)\b[^.]{0,40}\b' + re.escape(k) + r'\b', mtext):
            c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (nid, 'grants_keyword', kid, 'keywords field, given to other cards'))
            c.execute("INSERT OR IGNORE INTO entity_concepts SELECT ?, concept, 'grants', 'via_keyword', 'inherited from a reviewed keyword' FROM entity_concepts WHERE entity=?", (nid, kid))
        elif (k in listed and own) or (not FIELD and start.search(mtext)):
            c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (nid, 'has_keyword', kid, 'keywords field' if k in listed else 'keyword in text'))
            c.execute("INSERT OR IGNORE INTO entity_concepts SELECT ?, concept, role, 'via_keyword', 'inherited from a reviewed keyword' FROM entity_concepts WHERE entity=?", (nid, kid))
        elif FIELD and k in listed:
            c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (nid, 'mentions_keyword', kid, 'keywords field, named in the text'))
        elif not FIELD and any_.search(mtext):
            c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (nid, 'mentions_keyword', kid, 'keyword in text'))
    for s in [] if RELOAD else sub or []:
        if s.lower() in tribes: c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (nid, 'has_type', tribes[s.lower()], 'subtypes field'))
    for sent in [] if RELOAD else re.split(r'(?<=[.\n])', mtext):
        hits = [(t, i, m) for t, i, rx in trx for m in [rx.search(sent)] if m]
        if len(hits) >= 4: continue
        for t, i, m in hits:
            c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (nid, 'cares_about_type', i, sent[max(0, m.start() - 25): m.start() + 30]))
    if card.get('variant_of'):
        r = q("SELECT id FROM entities WHERE game=? AND name=? AND (faction IS ? OR faction=?) AND id<>?", G, card['variant_of'], card.get('faction'), card.get('faction'), nid)
        if r: c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (nid, 'variant_of', r[0][0], card.get('variant_note', 'variant')))
    byname[name] = nid; seen.add((name, card.get('faction'))); new_ids.append((nid, bool(card.get('created')))); nid = max(nid + 1, q('SELECT max(id) FROM entities')[0][0] + 1); n += 1
# names: "named X" -> references; a created entry named in a text -> generates
L = 0
names = [] if RELOAD else sorted((x for x in byname if len(x) >= 4), key=len, reverse=True)
for k in range(0, len(names), 400):
    rx = re.compile(r'\bnamed (' + '|'.join(re.escape(x) for x in names[k:k + 400]) + r')\b')
    for e, t in q("SELECT id, text FROM entities WHERE id IN (%s) AND text IS NOT NULL" % ','.join(str(i) for i, _ in new_ids) if new_ids else "SELECT 1, 2 WHERE 0"):
        for m in set(rx.findall(t)):
            if byname[m] != e: L += c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (e, 'references', byname[m], 'named ' + m)).rowcount
cids = {i for i, cr in new_ids if cr}
created = {nm.split(' (created)')[0]: i for i, nm in q("SELECT id, name FROM entities WHERE game=?", G) if i in cids}
cand = [] if RELOAD else sorted((x for x in created if len(x) >= 5 and x not in orig), key=len, reverse=True)
for k in range(0, len(cand), 400):
    rx = re.compile(r'\b(' + '|'.join(re.escape(x) for x in cand[k:k + 400]) + r')\b')
    for e, t in q("SELECT id, text FROM entities WHERE game=? AND text IS NOT NULL AND category NOT IN ('keyword','tribe')", G):
        for m in set(rx.findall(t)):
            if created[m] != e: L += c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (e, 'generates', created[m], 'names a created card')).rowcount
# extra_updates: [{name, faction, extra:{...}}] merged into an existing entry's extra (e.g. upgraded values that change only numbers)
U = 0
for u in d.get('extra_updates', []):
    for i, ex in q("SELECT id, extra FROM entities WHERE game=? AND name=? AND (faction IS ? OR faction=?)", G, u['name'], u.get('faction'), u.get('faction')):
        e = json.loads(ex) if ex else {}; e.update(u['extra'])
        U += c.execute("UPDATE entities SET extra=? WHERE id=?", (json.dumps(e), i)).rowcount
if U: print('extra updated on', U, 'entries')
for a, rel, b, ev in d.get('_links', []):   # reload: the game's links as they were, with the keyword tags they pass on
    L += c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (a, rel, b, ev)).rowcount
    if rel in ('has_keyword', 'grants_keyword'):
        c.execute("INSERT OR IGNORE INTO entity_concepts SELECT ?, concept, %s, 'via_keyword', 'inherited from a reviewed keyword' FROM entity_concepts WHERE entity=?" % ("'grants'" if rel == 'grants_keyword' else 'role'), (a, b))
if d.get('_game') and not q('SELECT 1 FROM games WHERE id=?', G):   # a new game: its row in games (id, name, family, edition, source, structure, notes)
    g = d['_game']; c.execute('INSERT INTO games VALUES(?,?,?,?,?,?,?)', tuple(g.get(k) for k in ['id', 'name', 'family', 'edition', 'source', 'structure', 'notes']))
c.execute("DELETE FROM load_log WHERE game=? AND step LIKE ?", (G, f'loaded ({TAG})%'))
c.execute("INSERT INTO load_log VALUES(?,?,?,?)", (G, f'loaded ({TAG})', n, d['_source']))
if skipped: c.execute("INSERT INTO load_log VALUES(?,?,?,?)", (G, f'loaded ({TAG}): skipped, name already in the library', skipped, ''))
c.execute("INSERT INTO entity_fts(entity_fts) VALUES('rebuild')")
c.commit(); print(G, TAG, 'loaded', n, 'skipped', skipped, 'name links', L)
