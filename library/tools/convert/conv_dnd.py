"""5e-database (github.com/5e-bits/5e-database) -> load_cards.py JSON: spells, class features, species traits, feats and magic items
the library lacks (2024 first; a 2014 entry only when its name has no 2024 version; bookkeeping features and item variants left out,
as in the first build). Usage: conv_dnd.py <5e-database/src> <db> <out>"""
import json, re, sqlite3, sys, collections
root, db, out = sys.argv[1:4]
c = sqlite3.connect(db)
have = {e for (e,) in c.execute("SELECT ext_id FROM entities WHERE game='dnd5e'")}
names = {n.lower() for (n,) in c.execute("SELECT name FROM entities WHERE game='dnd5e'")} | {n.lower() for (n,) in c.execute("SELECT name FROM merged_entities WHERE game='dnd5e'")}
BOOK = re.compile(r'ability score improvement|proficienc|subclass|epic boon|\blanguages?\b|hit points|starting equipment|^(\w+ )?spellcasting$|spell slots|cantrips? known|spells known|extra language', re.I)
def T(x):
    d = x.get('description') if x.get('description') is not None else x.get('desc')
    if isinstance(d, list): d = ' '.join(d)
    d = re.sub(r'\*\*|\*|#+|\|', ' ', d or ''); return re.sub(r'\s+', ' ', d).strip()
def hl(x):
    h = x.get('higher_level')
    if isinstance(h, list): h = ' '.join(h)
    return (' At higher levels: ' + re.sub(r'\s+', ' ', h).strip()) if h else ''
cards = []; C = collections.Counter(); taken = set()
for ed in ('2024', '2014'):
    for f, kind in (('Spells', 'spell'), ('Features', 'feature'), ('Traits', 'trait'), ('Feats', 'feat'), ('Magic-Items', 'item')):
        try: data = json.load(open(f'{root}/{ed}/en/5e-SRD-{f}.json', encoding='utf-8'))
        except FileNotFoundError: continue
        for x in data:
            eid = f"{ed}:{x['index']}"; nm = x['name']
            if eid in have or (kind == 'spell' and nm.lower() in names) or (nm.lower(), kind) in taken: C['already in'] += 1; continue
            if ed == '2014' and (nm.lower() in names or (nm.lower(), kind) in taken): C['2014 replaced by 2024'] += 1; continue
            if kind == 'feature' and BOOK.search(nm): C['bookkeeping feature'] += 1; continue
            if kind == 'item' and str(x.get('variant')) == 'True': C['magic item variant'] += 1; continue
            text = T(x) + (hl(x) if kind == 'spell' else '')
            if len(text) < 15: C['no text'] += 1; continue
            if kind == 'spell':
                lv = str(x.get('level')); st, cat, fac, cost = f'level {lv} spell', 'spell', (x.get('school') or {}).get('name'), f'level {lv}'
            elif kind == 'feature':
                st, cat, fac, cost = 'class feature', 'ability', (x.get('class') or {}).get('name'), None
            elif kind == 'trait':
                sp = x.get('species') or x.get('races') or []; st, cat, fac, cost = 'species trait', 'ability', (sp[0]['name'] if sp else None), None
            elif kind == 'feat':
                st, cat, fac, cost = 'feat', 'ability', None, None
            else:
                st, cat, fac, cost = 'magic item', 'item', None, None
            taken.add((nm.lower(), kind))
            cards.append(dict(ext_id=eid, name=nm, category=cat, source_type=st, edition=ed, faction=fac, cost=cost, text=text))
            C[f'{ed} {kind}'] += 1
json.dump({'_tag': 'srd', '_source': '5e-database (github.com/5e-bits/5e-database, current HEAD), 2024 and 2014 SRD: entries the first build dropped', 'cards': cards}, open(out, 'w', encoding='utf-8'))
print(len(cards), dict(C))
