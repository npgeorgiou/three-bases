"""Slay the Spire wiki Module:Cards/data (Lua) -> load_cards.py JSON of upgraded cards ('Name+'). Usage: conv_sts.py <lua> <db> <out>"""
import json, re, sqlite3, sys
src, db, out = sys.argv[1:4]
L = open(src, encoding='utf-8').read()
c = sqlite3.connect(db)
have = {(n, f): (i, cost, st) for i, n, f, cost, st in c.execute("SELECT id, name, faction, cost, source_type FROM entities WHERE game='sts1' AND source_type LIKE '%card'")}
COL = {'Red': 'Ironclad', 'Green': 'Silent', 'Blue': 'Defect', 'Purple': 'Watcher', 'Colorless': 'Colorless', 'Curse': 'Curse'}
ents = re.findall(r'\n  \["([^"]+)"\] = \{(.*?)\n  \}', L, re.S)
cards, miss, same, upd = [], [], 0, []
def field(b, k):
    m = re.search(r'\b' + k + r' = ("((?:[^"\\]|\\.)*)"|[-\w.]+)', b)
    return None if not m else (m.group(2) if m.group(2) is not None else m.group(1))
def clean(t):
    t = t.replace('\\"', '"').replace('<br>', ' ')
    t = re.sub(r'\{\{(?:[^{}|]*\|)*([^{}|]*)\}\}', r'\1', t)
    t = re.sub(r'((?:@[A-Z]E\s*)+)', lambda m: (lambda k: 'energy ' if k == 1 else f'{k} energy ')(len(re.findall('@', m.group(1)))), t)
    t = re.sub(r'\$(\w+)', r'\1', t); t = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', t)
    return re.sub(r'\s+([.,])', r'\1', re.sub(r'\s+', ' ', t)).strip()
for name, b in ents:
    if name == 'nodata_fallback' or 'NoUpgrade' in b: continue
    base = re.sub(r' \((Ironclad|Silent|Defect|Watcher)\)$', '', name)
    fac = COL.get(field(b, 'Color'))
    t0 = field(b, 'Text') or ''
    if (base, fac) not in have:
        st = (field(b, 'Type') or '').lower() + ' card'; cb0 = field(b, 'Cost')
        bc = None if cb0 is None else ('X energy' if cb0 == '-1' else 'unplayable' if cb0 == '-2' else f'{cb0} energy')
        cards.append(dict(ext_id=f'{base}|{fac}', name=base, category='spell', source_type=st, faction=fac, cost=bc, rarity=(field(b, 'Rarity') or '').lower() or None,
                          cost_num=float(cb0) if cb0 and cb0.isdigit() else None, text=clean(re.sub(r'\[([^|\]]*)\|([^\]]*)\]', r'\1', t0)),
                          created=(field(b, 'Rarity') or '') == 'Special', extra={'missing_from_first_build': True}))
        miss.append(name); i = None
    else:
        i, cost, st = have[(base, fac)]
    t = field(b, 'Text') or ''
    up = clean(re.sub(r'\[([^|\]]*)\|([^\]]*)\]', r'\2', t)); low = clean(re.sub(r'\[([^|\]]*)\|([^\]]*)\]', r'\1', t))
    cp = field(b, 'CostPlus'); cb = field(b, 'Cost')
    ucost = (cp if cp is not None else cb)
    ucost = None if ucost is None else ('X energy' if ucost == '-1' else 'unplayable' if ucost == '-2' else f'{ucost} energy')
    if up == low and cp is None: same += 1
    N = lambda x: re.sub(r's\b', '', re.sub(r'\b(\d+|a|an|one|x\+\d|x|once|twice|copy|copie)\b', 'N', re.sub(r'\+\d+', '', x.lower())))
    if i and N(up) == N(low):   # only numbers change: kept on the base entry
        upd.append(dict(name=base, faction=fac, extra={'upgraded_text': up, **({'upgraded_cost': ucost} if cp is not None else {})})); continue
    cards.append(dict(ext_id=f'{base}|{fac}|upgraded', name=base + '+', category='spell', source_type=st, faction=fac, cost=ucost,
                      cost_num=float(ucost.split()[0]) if ucost and ucost.split()[0].isdigit() else None, text=up,
                      variant_of=base, variant_note='upgraded version (Smith)', extra={'upgrade_of': base, **({'upgrade_of_id': i} if i else {})}))
json.dump({'_tag': 'sts1_upgrades', '_source': 'Slay the Spire Wiki, Module:Cards/data (raw), upgraded values [regular|upgraded] and CostPlus', 'cards': cards, 'extra_updates': upd}, open(out, 'w', encoding='utf-8'))
print(len(cards), 'number-only upgrades', len(upd), 'unmatched', len(miss), miss[:15], 'text identical to base', same)
