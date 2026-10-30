"""Shadowverse Portal card API export -> load_cards.py JSON: tokens (set 90000) and cards the first build dropped.
Usage: conv_sv.py <shadowverse.json> <db> <out>"""
import json, re, sqlite3, sys, collections
src, db, out = sys.argv[1:4]
D = json.load(open(src, encoding='utf-8'))['data']['cards']
c = sqlite3.connect(db)
have = {e for (e,) in c.execute("SELECT ext_id FROM entities WHERE game='shadowverse'")}
names = {n for (n,) in c.execute("SELECT name FROM entities WHERE game='shadowverse'")} | {n for (n,) in c.execute("SELECT name FROM merged_entities WHERE game='shadowverse'")}
CLAN = {0: 'Neutral', 1: 'Forestcraft', 2: 'Swordcraft', 3: 'Runecraft', 4: 'Dragoncraft', 5: 'Shadowcraft', 6: 'Bloodcraft', 7: 'Havencraft', 8: 'Portalcraft'}
TYPE = {1: ('follower', 'unit'), 2: ('amulet', 'building'), 3: ('countdown amulet', 'building'), 4: ('spell', 'spell')}
RAR = {1: 'bronze', 2: 'silver', 3: 'gold', 4: 'legendary'}
cl = lambda t: re.sub(r'\s+', ' ', re.sub(r'<br\s*/?>', ' ', t or '')).strip()
cards = []; C = collections.Counter(); done = set()
for x in D:
    if x['card_id'] != x['base_card_id']: C['alternate art'] += 1; continue
    if str(x['card_id']) in have or x['card_name'] in names: C['already in'] += 1; continue
    s, e = cl(x['skill_disc']), cl(x['evo_skill_disc'])
    text = s + (' Evolved: ' + e if e and e != s else '')
    if not text: C['no rules text'] += 1; continue
    key = (x['card_name'], text)
    if key in done: C['same name and text'] += 1; continue
    done.add(key)
    tok = x['card_set_id'] == 90000
    st, cat = TYPE[x['char_type']]
    stats = {'attack': x['atk'], 'defense': x['life'], 'evolved_attack': x['evo_atk'], 'evolved_defense': x['evo_life']} if x['char_type'] == 1 else None
    tr = [t for t in re.split(r'\s*/\s*', x.get('tribe_name') or '') if t and t != '-']
    cards.append(dict(ext_id=x['card_id'], name=x['card_name'], category=cat, source_type=st, edition=str(x['card_set_id']), faction=CLAN.get(x['clan']),
                      subtypes=tr or None, rarity=RAR.get(x['rarity']), cost=f"{x['cost']} play points", cost_num=float(x['cost']), stats=stats, text=text, created=tok))
    C['token' if tok else 'dropped before'] += 1
json.dump({'_tag': 'sv_tokens', '_source': 'Shadowverse Portal card API export (5,933 cards): tokens (set 90000) and cards the first build dropped; alternate art left out', 'cards': cards}, open(out, 'w', encoding='utf-8'))
print(len(cards), dict(C))
