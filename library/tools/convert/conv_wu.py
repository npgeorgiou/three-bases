"""yawudb db.js (github.com/PompolutZ/yawudb, src/data/wudb/db.js) -> load_cards.py JSON of Underworlds deck cards the library lacks.
Usage: conv_wu.py <db.js> <db> <out>"""
import json, re, sqlite3, sys, collections
src, db, out = sys.argv[1:4]
s = open(src, encoding='utf-8').read()
def obj(name):
    i = s.index('export const ' + name + ' = '); j = s.index('{', i); depth = 0
    for k in range(j, len(s)):
        if s[k] == '{': depth += 1
        elif s[k] == '}':
            depth -= 1
            if depth == 0: return json.loads(re.sub(r',(\s*[}\]])', r'\1', s[j:k + 1]))
cards, sets, facs = obj('cards'), obj('sets'), obj('factions')
SET = {v['id']: v['displayName'] for v in sets.values()}; FAC = {v['id']: v['displayName'] for v in facs.values()}
c = sqlite3.connect(db)
have = {e for (e,) in c.execute("SELECT ext_id FROM entities WHERE game='wh_underworlds'")}
names = {n for (n,) in c.execute("SELECT name FROM entities WHERE game='wh_underworlds'")} | {n for (n,) in c.execute("SELECT name FROM merged_entities WHERE game='wh_underworlds'")}
CAT = {'Objective': 'modifier', 'Upgrade': 'item', 'Ploy': 'spell', 'Spell': 'spell'}
outc = []; C = collections.Counter(); seen = set()
for v in cards.values():
    ids = {str(v['id'])} | {str(x) for x in v.get('duplicates') or []}
    if ids & have or v['name'] in names: C['already in'] += 1; continue
    key = (v['name'], v['rule'])
    if key in seen: C['duplicate reprint'] += 1; continue
    seen.add(key)
    t = v['type']
    st = f"objective ({v['scoreType'].lower()} scoring)" if t == 'Objective' else t.lower()
    outc.append(dict(ext_id=v['id'], name=v['name'], category=CAT[t], source_type=st, edition=SET.get(v['setId']), faction=FAC.get(v['factionId']),
                     cost=f"{v['glory']} glory" if t == 'Objective' and v.get('glory') is not None else None,
                     cost_num=float(v['glory']) if t == 'Objective' and v.get('glory') is not None else None,
                     text=v['rule'], extra={'rotated_out': v.get('rotated')}))
    C['new'] += 1
json.dump({'_tag': 'yawudb', '_source': 'yawudb db.js (github.com/PompolutZ/yawudb): Underworlds objectives, ploys, upgrades and spells the first build dropped', 'cards': outc}, open(out, 'w', encoding='utf-8'))
print(len(outc), dict(C))
