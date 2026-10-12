"""Legends of Runeterra fixes:
1. The 'Runeterra' champion region is removed completely (its cards, tags, links, pairs and faction rows), as if it did not exist.
2. Levelled champions are added (tools/runeterra_levelled.json, from Riot's Data Dragon set files): the base loader dropped every
   non-collectible card, which removed the levelled side of each champion. Each levelled side is an entry '<name> (level 2)' in the
   base card's faction, linked base -> transforms_into -> levelled; tagged with the general and Runeterra patterns (text_pattern),
   its keywords (has_keyword, concepts inherited via_keyword) and trigger -> effect pairs per clause.
3. The other cards the first load dropped (tools/runeterra_extra.json), linked from the cards that create them (generates).
Idempotent. Usage: runeterra_fixes.py <db>"""
import json, os, re, sqlite3, sys
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
here = os.path.dirname(os.path.abspath(__file__)); G = 'runeterra'

def drop(ids):
    for i in ids:
        for s in ("DELETE FROM entity_concepts WHERE entity=?", "DELETE FROM entity_links WHERE src=? OR dst=?", "DELETE FROM trigger_effect WHERE entity=?", "DELETE FROM entities WHERE id=?"):
            c.execute(s, (i,) * s.count('?'))

# 1. drop the Runeterra region
reg = [i for (i,) in q("SELECT id FROM entities WHERE game=? AND faction='Runeterra'", G)]
drop(reg)
for t in ('factions', 'faction_archetypes'): c.execute(f"DELETE FROM {t} WHERE game=? AND {'name' if t == 'factions' else 'faction'}='Runeterra'", (G,))
if q("SELECT 1 FROM sqlite_master WHERE name='faction_signature'"): c.execute("DELETE FROM faction_signature WHERE game=? AND (faction='Runeterra' OR owner='Runeterra')", (G,))
if q("SELECT 1 FROM sqlite_master WHERE name='merged_entities'"): c.execute("DELETE FROM merged_entities WHERE game=? AND kept_id NOT IN (SELECT id FROM entities)", (G,))

# 2. levelled champions
drop([i for (i,) in q("SELECT id FROM entities WHERE game=? AND ext_id LIKE 'lvl:%'", G)])
d = json.load(open(os.path.join(here, 'runeterra_levelled.json'), encoding='utf-8'))
excl = set()
for line in open(os.path.join(here, 'patterns', 'runeterra.txt'), encoding='utf-8'):
    if line.startswith('!'): excl.add(tuple(line[1:].rstrip('\n').split('|', 1)))
pats = []
for con, role, p, g in q("SELECT concept, role, pattern, game FROM concept_patterns WHERE game IS NULL OR game=?", G):
    if g is None and any(con == a and b in p for a, b in excl): continue
    try: pats.append((con, role, re.compile(p, re.I)))
    except re.error: pass
root = dict(q("SELECT id, root FROM concept_tree WHERE root IN ('trigger','effect')"))
trig = [x for x in pats if x[1] == 'does' and root.get(x[0]) == 'trigger']; eff = [x for x in pats if x[1] == 'does' and root.get(x[0]) == 'effect']
kw = {n.lower(): i for n, i in q("SELECT name, id FROM entities WHERE game=? AND category='keyword'", G)}
base = {e: (i, f, nm) for e, i, f, nm in q("SELECT ext_id, id, faction, name FROM entities WHERE game=? AND category NOT IN ('keyword','tribe')", G)}
SPLIT = re.compile(r'(?<=[.!;])\s+|\n+')
def tag(nid, text, keywords):
    low = text.lower()
    for con, role, p in pats:
        m = p.search(low)
        if m: c.execute("INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)", (nid, con, role, 'text_pattern', low[max(0, m.start() - 20): m.start() + 40]))
    for k in keywords:
        kid = kw.get(k.lower())
        if kid:
            c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (nid, 'has_keyword', kid, 'keyword field'))
            c.execute("INSERT OR IGNORE INTO entity_concepts SELECT ?, concept, role, 'via_keyword', 'inherited from a reviewed keyword' FROM entity_concepts WHERE entity=?", (nid, kid))
    for cl in SPLIT.split(low):
        tr = {x[0] for x in trig if x[2].search(cl)}; ef = {x[0] for x in eff if x[2].search(cl)}
        for a in tr:
            for b in ef: c.execute("INSERT INTO trigger_effect(entity, game, trigger, effect, clause) VALUES(?,?,?,?,?)", (nid, G, a, b, cl.strip()[:300]))

nid = q('SELECT max(id) FROM entities')[0][0] + 1
n = 0
# the levelled side of each champion: the champion unit with the champion's own name, else the one with the lowest T number
bynm = {e: nm for e, (i, f, nm) in base.items()}
levelled = set()
for b0 in {cd['base'] for cd in d['cards']}:
    cs = [cd for cd in d['cards'] if cd['base'] == b0]
    same = [cd for cd in cs if cd['name'] == bynm.get(b0)]
    pick = same or sorted(cs, key=lambda cd: int(re.sub(r'\D', '', cd['code'][8:]) or 0))
    if pick: levelled.add(pick[0]['code'])
for card in d['cards']:
    if 'Runeterra' in card['regions'] or card['base'] not in base: continue
    bid, fac, bname = base[card['base']]
    lvl = card['code'] in levelled   # the levelled side; other champion units are ones the champion creates (Sion Returned)
    text = (f"Keywords: {', '.join(card['keywords'])}. " if card['keywords'] else '') + card['text'].replace('\r\n', ' ').strip()
    c.execute("INSERT INTO entities(id, game, ext_id, name, category, source_type, edition, faction, cost, cost_num, stats, text) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (nid, G, 'lvl:' + card['code'], card['name'] + (' (level 2)' if lvl else (' (other form)' if card['name'] == bname else '')), 'hero', ('levelled champion' if lvl else 'created champion unit') + ' (Data Dragon)', 'level 2' if lvl else 'non-collectible', fac,
               str(card['cost']), card['cost'], f"{card['attack']}|{card['health']}", text))
    c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (bid, 'transforms_into' if lvl else 'generates', nid, 'levels up into' if lvl else 'creates'))
    tag(nid, text, card['keywords'])
    nid += 1; n += 1
# 3. the other cards the first load dropped (tools/runeterra_extra.json): tokens, champion spells, created cards, abilities,
#    landmarks, equipment, and collectible cards no pattern matched; links from the card that creates them (associatedCardRefs)
drop([i for (i,) in q("SELECT id FROM entities WHERE game=? AND ext_id LIKE 'extra:%'", G)])
x = json.load(open(os.path.join(here, 'runeterra_extra.json'), encoding='utf-8'))
CAT = {'Unit': 'unit', 'Spell': 'spell', 'Ability': 'ability', 'Landmark': 'building', 'Equipment': 'item', 'Trap': 'spell'}
names = {nm for (nm,) in q("SELECT name FROM entities WHERE game=?", G)}
code_id = {e: i for e, i in q("SELECT ext_id, id FROM entities WHERE game=? AND ext_id NOT LIKE 'lvl:%'", G)}
code_id.update({e[4:]: i for e, i in q("SELECT ext_id, id FROM entities WHERE game=? AND ext_id LIKE 'lvl:%'", G)})
m = 0
for card in x['cards']:
    text = (f"Keywords: {', '.join(card['keywords'])}. " if card['keywords'] else '') + card['text'].replace('\r\n', ' ').strip()
    if card['levelup']: text += ' Level up: ' + card['levelup'].replace('\r\n', ' ').strip()
    name = card['name'] if card['collectible'] or card['name'] not in names else card['name'] + ' (created)'
    c.execute("INSERT INTO entities(id, game, ext_id, name, category, source_type, edition, faction, subtypes, cost, cost_num, stats, text) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
              (nid, G, 'extra:' + card['code'], name, CAT.get(card['type'], 'unit'), ('card' if card['collectible'] else 'created card') + ' (Data Dragon)',
               'collectible' if card['collectible'] else 'non-collectible', card['regions'][0] if card['regions'] else None, ', '.join(card['subtypes']) or None,
               str(card['cost']), card['cost'], f"{card['attack']}|{card['health']}" if card['type'] == 'Unit' else None, text))
    tag(nid, text, card['keywords'])
    code_id[card['code']] = nid; names.add(name); nid += 1; m += 1
for src, dsts in x['refs'].items():
    for d2 in dsts:
        if src in code_id and d2 in code_id and code_id[src] != code_id[d2]:
            c.execute("INSERT OR IGNORE INTO entity_links VALUES(?,?,?,?)", (code_id[src], 'generates', code_id[d2], 'associated card (Data Dragon)'))
c.execute("DELETE FROM load_log WHERE game=? AND step='dropped cards restored'", (G,))
c.execute("INSERT INTO load_log VALUES(?,?,?,?)", (G, 'dropped cards restored', m, x['_source']))
c.execute("DELETE FROM load_log WHERE game=? AND step='levelled champions'", (G,))
if reg: c.execute("INSERT INTO load_log VALUES(?,?,?,?)", (G, 'runeterra region dropped', len(reg), "the 'Runeterra' champion region removed completely"))
c.execute("INSERT INTO load_log VALUES(?,?,?,?)", (G, 'levelled champions', n, d['_source']))
c.execute("INSERT INTO entity_fts(entity_fts) VALUES('rebuild')")
c.commit(); print('Runeterra region entries dropped:', len(reg), ' levelled champions added:', n, ' dropped cards restored:', m)
