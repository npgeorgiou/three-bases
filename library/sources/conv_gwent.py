"""gwent.one export (v14.8) -> load_cards.py JSON of the cards the library lacks (NonOwnable tokens, cards the first build dropped).
Usage: conv_gwent.py <gwent.json> <db> <out>"""
import json, sqlite3, sys, collections
src, db, out = sys.argv[1:4]
D = json.load(open(src, encoding='utf-8'))['response']
c = sqlite3.connect(db)
have = {e for (e,) in c.execute("SELECT ext_id FROM entities WHERE game='gwent'")}
merged = {n for (n,) in c.execute("SELECT name FROM merged_entities WHERE game='gwent'")}
CAT = {'Unit': 'unit', 'Special': 'spell', 'Stratagem': 'spell', 'Artifact': 'building', 'Ability': 'hero'}
cards = []; C = collections.Counter()
for x in D.values():
    a = x['attributes']; cid = str(x['id']['card'])
    if cid in have or (x['name'] in merged and a['set'] != 'NonOwnable'): C['already in'] += 1; continue
    text = (x.get('ability') or '').strip()
    if not text: C['no text'] += 1; continue
    tok = a['set'] == 'NonOwnable'
    st = {'power': a.get('power'), 'armor': a.get('armor')} if a['type'] == 'Unit' else None
    cards.append(dict(ext_id=cid, name=x['name'], category=CAT[a['type']], source_type=a['type'], edition=a['set'], faction=a['faction'],
                      subtypes=[s.strip() for s in (x.get('category') or '').split(',') if s.strip()] or None, rarity=a['rarity'].lower(),
                      cost=f"{a['provision']} provisions" if a.get('provision') else None, cost_num=float(a['provision']) if a.get('provision') else None,
                      stats=st, text=text, extra={'color': a.get('color'), 'reach': a.get('reach')}, created=tok))
    C['token' if tok else 'dropped before'] += 1
json.dump({'_tag': 'gwent_tokens', '_source': 'gwent.one export v14.8: NonOwnable cards (tokens and created cards) and cards the first build dropped', 'cards': cards}, open(out, 'w', encoding='utf-8'))
print(len(cards), dict(C))
