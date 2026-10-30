"""Slay the Spire 2 wiki card lists (normal and upgraded, same card order, supplied by Kaptain on 12 Oct 2026) -> load_cards.py JSON.
Same model as Slay the Spire 1 (conv_sts.py): an upgrade that only changes numbers is kept on its base card (extra.upgraded_text);
an upgrade that changes the mechanic is its own entry '<name>+', variant_of the base card. Cards the library lacks are added as base
cards (extra.missing_from_first_build). The lists give no energy costs, so new cards and upgrades carry no cost and upgraded costs are unknown.
Each record: image line, name, 'Rarity - Class - Type', text lines. Icons are written as words ('2 energy', '3 stars').
Usage: conv_sts2.py <normal.txt> <upgraded.txt> <db> <out.json>"""
import json, re, sqlite3, sys
bp, up, db, out = sys.argv[1:5]
HDR = re.compile(r'^([A-Z][a-z]+) - ([A-Za-z]+) - ([A-Za-z ]+)$')
def parse(p):
    L = [l.rstrip('\n') for l in open(p, encoding='utf-8')]
    idx = [k for k in range(2, len(L)) if HDR.match(L[k]) and L[k - 2].startswith('StS2 ')]
    return [dict(name=L[k - 1].strip(), hdr=HDR.match(L[k]).groups(), text=L[k + 1:(idx[n + 1] - 2 if n + 1 < len(idx) else len(L))]) for n, k in enumerate(idx)]
def clean(lines):
    t = ' '.join(x.strip() for x in lines if x.strip())
    def run(m, word, plural):
        k = len(re.findall(r'StS2 ' + m.group(3) + r'\.png', m.group(0)))
        return word if k == 1 else f'{k} {plural}'
    t = re.sub(r'\b(\d+) ?StS2 Energy\w+\.png', r'\1 energy', t)
    t = re.sub(r'\b(\d+) ?StS2 StarRegent\.png', lambda m: m.group(1) + (' star' if m.group(1) == '1' else ' stars'), t)
    t = re.sub(r'((StS2 (Energy\w+)\.png)\s*)+', lambda m: run(m, 'energy', 'energy') + ' ', t)
    t = re.sub(r'((StS2 (StarRegent)\.png)\s*)+', lambda m: run(m, 'star', 'stars') + ' ', t)
    t = re.sub(r'(StS2|Enchant) [^.]*?\.png\s*', '', t)   # an icon before the word it shows (Block, Vulnerable, Osty, Shiv, ...)
    return re.sub(r'\s+([.,])', r'\1', re.sub(r'\s+', ' ', t)).strip()
B, U = parse(bp), parse(up)
assert len(B) == len(U) and all(a['name'] == b['name'] for a, b in zip(B, U)), 'lists do not line up'
c = sqlite3.connect(db)
have = {}
for i, n, f in c.execute("SELECT id, name, faction FROM entities WHERE game='sts2' AND source_type LIKE '%card'"): have[(n, f)] = i
for n, i, f in c.execute("SELECT m.name, m.kept_id, e.faction FROM merged_entities m JOIN entities e ON e.id=m.kept_id WHERE m.game='sts2'"): have.setdefault((n, f), i)
byname = {}
for (n, f), i in have.items(): byname.setdefault(n, []).append((f, i))
SPECIAL = {'Event': 'Event', 'Curse': 'Curse', 'Status': 'Status', 'Token': 'Token', 'Quest': 'Quest'}
N = lambda x: re.sub(r's\b', '', re.sub(r'\b(\d+|a|an|one|x\+\d|x|once|twice|copy|copie)\b', 'N', re.sub(r'\+\d+', '', x.lower())))
N1 = lambda x: N(re.sub(r'(?<!\d )\b(energy|stars?)\b', r'1 \1', ' ' + x))
cards, upd, new, same, numonly = [], [], [], 0, 0
for a, b in zip(B, U):
    rar, cls, typ = a['hdr']
    base = re.sub(r' \((Ironclad|Silent|Defect|Regent|Necrobinder)\)$', '', a['name'])
    fac = SPECIAL.get(rar, cls)
    t0, t1 = clean(a['text']), clean(b['text'])
    i = have.get((base, fac))
    if i is None and len(byname.get(base, [])) == 1: fac, i = byname[base][0]
    st = typ.lower() + ' card'
    if i is None:
        cards.append(dict(ext_id=f'{base}|{fac}', name=base, category='spell', source_type=st, faction=fac, rarity=rar.lower(), text=t0,
                          created=rar in ('Token', 'Status'), extra={'missing_from_first_build': True}))
        new.append(base)
    if t1 == t0: same += 1; continue
    if N1(t1) == N1(t0):
        numonly += 1
        if i is not None: upd.append(dict(name=base, faction=fac, extra={'upgraded_text': t1}))
        else: cards[-1]['extra']['upgraded_text'] = t1
        continue
    cards.append(dict(ext_id=f'{base}|{fac}|upgraded', name=base + '+', category='spell', source_type=st, faction=fac, rarity=rar.lower(), text=t1,
                      variant_of=base, variant_note='upgraded version (Smith)', extra={'upgrade_of': base, **({'upgrade_of_id': i} if i else {})}))
json.dump({'_tag': 'sts2_upgrades', '_source': 'Slay the Spire 2 wiki card lists, normal and upgraded (supplied by Kaptain, 12 Oct 2026)',
           'cards': cards, 'extra_updates': upd}, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
print('records', len(B), 'new base cards', len(new), 'mechanic upgrades', sum(1 for x in cards if x['name'].endswith('+')),
      'number-only', numonly, 'no change', same, new[:40])
