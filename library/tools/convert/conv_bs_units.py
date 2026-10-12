"""BSData repo -> load_cards.py JSON of unit datasheets, and stat lines for library units that have none (12 Oct 2026).
  - New units: unit entries (not hidden) whose name the game does not have yet; an entry that only groups models the library
    already has is left out. Kill Team datasheets are operatives (model entries); its unit entries (fire teams) are not loaded.
    As in the first build, a unit without any ability or special rule (Kill Team: without an ability) is left out. Text as the first build wrote units: each ability
    'Name: text', then 'Weapon abilities: ...' (weapon keywords) and 'Special rules: ...' (linked rules). Stats = the first stat
    profile (40k/AoS 'Unit', Kill Team 'Operative'); other models' different profiles go to extra.model_stats. Campaign content (and campaign lines in a unit's text) left out.
  - Stat lines: a library unit without stats whose name has exactly one distinct stat profile in the repo gets it (file 'stats_updates').
Usage: conv_bs_units.py <game> <repo dir> <db> <out.json>"""
import collections, json, os, re, sqlite3, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bsdata
from bsdata import strip, kids, walk, txt, profile_text
import xml.etree.ElementTree as ET
g, repo, db, out = sys.argv[1:5]
STAT = {'wh_40k_10e': 'Unit', 'wh_killteam': 'Operative', 'wh_aos_4th': 'Unit'}[g]
ABIL = {'wh_40k_10e': ('Abilities',), 'wh_killteam': ('Abilities', 'Ability', 'Unique Actions'),
        'wh_aos_4th': ('Ability (Activated)', 'Ability (Passive)', 'Ability (Spell)', 'Ability (Prayer)', 'Ability (Command)')}[g]
WEAP = {'wh_40k_10e': (('Ranged Weapons', 'Melee Weapons'), 'Keywords'), 'wh_killteam': (('Weapons', 'Weapon'), 'WR'),
        'wh_aos_4th': (('Melee Weapon', 'Ranged Weapon'), 'Ability')}[g]
ETYPE = 'model' if g == 'wh_killteam' else 'unit'   # a Kill Team datasheet is an operative (model); its 'unit' entries are fire teams
CAMP = re.compile(r'crusade|battle honou?r|battle scar|requisition|experience points?|\bxp\b|path to glory|rival (lord|activity)|spec ops|campaign|glory points|renown|dossier|agenda|saint points|martyr points?|anvil of apotheosis', re.I)
clean = lambda t: re.sub(r'\s+', ' ', re.sub(r'\*\*|\^\^|\*', '', t or '')).strip()
c = sqlite3.connect(db)
names = {n for (n,) in c.execute("SELECT name FROM entities WHERE game=?", (g,))} | {n for (n,) in c.execute("SELECT name FROM merged_entities WHERE game=?", (g,))}
ids, roots = {}, []
for f in sorted(os.listdir(repo)):
    if not (f.endswith('.cat') or f.endswith('.gst')): continue
    try: root = ET.parse(os.path.join(repo, f)).getroot()
    except ET.ParseError: continue
    roots.append((f, root))
    for e in walk(root):
        if e.get('id'): ids.setdefault(e.get('id'), e)
def gather(el, seen=None, weapons_only=False):
    """profiles and rules of a unit: everything in its own entry and what its info links point to; through entry links (shared
    weapon and option lists) only weapon profiles and the rules linked from them, so another model's abilities are not picked up."""
    seen = seen if seen is not None else set()
    for e in walk(el):
        t = strip(e.tag)
        if e.get('hidden') == 'true': continue
        if t == 'profile' and (not weapons_only or (e.get('typeName') or '') in WEAP[0]): yield e
        if t == 'rule': yield e
        tid = e.get('targetId')
        if t in ('infoLink', 'entryLink') and tid and tid not in seen:
            seen.add(tid); tgt = ids.get(tid)
            if tgt is None: continue
            if t == 'infoLink':
                if weapons_only and strip(tgt.tag) == 'profile' and (tgt.get('typeName') or '') not in WEAP[0]: continue
                yield from gather(tgt, seen, weapons_only)
            else: yield from gather(tgt, seen, True)
cards, C, stats_up = [], collections.Counter(), {}
done = set()
profiles = collections.defaultdict(set)
for f, root in roots:
    fac = root.get('name')
    for e in walk(root):
        if strip(e.tag) == 'profile' and e.get('typeName') == STAT and e.get('hidden') != 'true':
            profiles[e.get('name')].add(json.dumps(profile_text(e), sort_keys=True))
        if strip(e.tag) != 'selectionEntry' or e.get('type') != ETYPE or e.get('hidden') == 'true': continue
        name = clean(e.get('name'))
        if name in names or (name, fac) in done: continue
        if CAMP.search(fac) or CAMP.search(name): C['campaign'] += 1; continue
        done.add((name, fac))
        models = {clean((ids.get(x.get('targetId')) if strip(x.tag) == 'entryLink' else x).get('name') or '') for x in walk(e) if x is not e and
                  ((strip(x.tag) == 'selectionEntry' and x.get('type') == 'model') or (strip(x.tag) == 'entryLink' and ids.get(x.get('targetId')) is not None and ids[x.get('targetId')].get('type') == 'model'))}
        if models and models <= names: C['roster of models the library has'] += 1; continue
        ab, wk, sr, st = [], [], [], []
        for p in gather(e):
            ty = p.get('typeName') or ''
            if strip(p.tag) == 'rule':
                if p.get('name') not in sr and not CAMP.search(p.get('name') or ''): sr.append(p.get('name'))
            elif ty == STAT: st.append(profile_text(p))
            elif ty in ABIL:
                ch = profile_text(p); d = clean(ch.get('Description') or ch.get('Effect') or ch.get('Ability') or next(iter(ch.values()), ''))
                line = f"{clean(p.get('name'))}: {d}"
                if d and line not in ab and not CAMP.search(line): ab.append(line)
            elif ty in WEAP[0]:
                for k in re.split(r',\s*', profile_text(p).get(WEAP[1], '') or ''):
                    k = clean(k)
                    if k and k not in ('-', '–') and k not in wk: wk.append(k)
        text = ' '.join(ab)
        if wk: text += (' ' if text else '') + 'Weapon abilities: ' + ', '.join(wk) + '.'
        if sr: text += (' ' if text else '') + 'Special rules: ' + ', '.join(sr) + '.'
        if not st: C['no stat profile'] += 1; continue
        if not ab and (g == 'wh_killteam' or not sr): C['no ability or special rule (left out, as in the first build)'] += 1; continue
        ex = {'source': 'BSData datasheet (12 Oct 2026 load)'}
        others = [s for s in st[1:] if s != st[0]]
        if others: ex['model_stats'] = others
        cards.append(dict(ext_id='unit:' + name + '|' + fac, name=name, category='unit', source_type='unit', faction=fac,
                          stats=st[0] if st else None, text=text, extra=ex))
        C['new unit'] += 1
for (n,) in c.execute("SELECT name FROM entities WHERE game=? AND category='unit' AND (stats IS NULL OR stats='')", (g,)):
    if len(profiles.get(n, ())) == 1: stats_up[n] = json.loads(next(iter(profiles[n])))
C['stat lines for units without stats'] = len(stats_up)
json.dump({'_tag': 'bsdata_units_' + g, '_source': f'BSData {repo.rstrip("/").split("/")[-1]} (GitHub, current HEAD): unit datasheets the library lacked and stat lines for units without stats; campaign content left out',
           'cards': cards, 'stats_updates': stats_up}, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
print(g, dict(C), [x['name'] for x in cards][:60])
