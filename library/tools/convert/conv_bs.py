"""BSData repo -> load_cards.py JSON: abilities and rules whose text the library does not have yet (campaign content left out,
as in the first build). Usage: conv_bs.py <game> <repo dir> <db> <out>"""
import sys, re, json, collections
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import bs_missing
g, repo, db, out = sys.argv[1:5]
bs_missing.c = __import__('sqlite3').connect(db)
PT = {'wh_40k_10e': ('Abilities', 'rule'),
      'wh_aos_4th': ('Ability (Activated)', 'Ability (Passive)', 'Ability (Spell)', 'Ability (Prayer)', 'Ability (Command)', 'rule')}[g]
CAMP = re.compile(r'crusade|battle honou?r|battle scar|requisition|experience points?|\bxp\b|path to glory|rival (lord|activity)|campaign|glory points|renown|agenda|saint points|martyr points?|complete \w+ battles|at the end of (a|the) battle\b', re.I)
clean = lambda t: re.sub(r'\s+', ' ', re.sub(r'\*\*|\^\^|\*', '', t)).strip()
m = bs_missing.missing(g, repo, PT)
cards = []; C = collections.Counter(); names = set()
for r, t in m:
    if CAMP.search(r['faction']) or CAMP.search(r['name']) or CAMP.search(t): C['campaign'] += 1; continue
    if g == 'wh_aos_4th' and re.search(r"\byour hero('s)?\b", t, re.I): C['hero creation (Path to Glory / Anvil)'] += 1; continue
    if r['kind'] == 'rule':
        st, cat, pre = 'faction/army rule', 'game_rule', 'rule:'
    else:
        p = r['ptype'].lower()
        st = {'abilities': 'abilities', 'ability': 'ability'}.get(p, p)
        cat = 'spell' if any(k in p for k in ('spell', 'prayer', 'psychic')) else 'ability'; pre = 'ab:'
    name = clean(r['name']).lstrip('*').strip()
    if (name, r['faction']) in names: C['same name'] += 1; continue
    names.add((name, r['faction']))
    cards.append(dict(ext_id=pre + name + '|' + r['faction'], name=name, category=cat, source_type=st, faction=r['faction'], text=clean(t)))
    C[st] += 1
json.dump({'_tag': 'bsdata_' + g, '_source': f'BSData {repo.rstrip("/").split("/")[-1]} (GitHub, current HEAD): abilities and rules whose text the library lacked (dropped by the first build or added since); campaign content left out', 'cards': cards}, open(out, 'w', encoding='utf-8'))
print(g, len(cards), dict(C))
