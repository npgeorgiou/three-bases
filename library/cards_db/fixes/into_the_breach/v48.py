"""Into the Breach, 30 Oct 2026, after the first build: the families of deck_read_into_the_breach.md "Before the fix", by
rule; safe to run twice.
F1 damage that changes with distance or hits ("Damage: 3-1", "2 damage reduced by range"): amount x range, lowest first.
F2 "flip its attack direction": act redirect_attack (vocab v48).
F3 "+N Range" when the text gives no base reach: increase_effect params range N; "max distance and damage by 1": +1 damage.
F4 weapon damage, bumps, blocking emerging Vek: a condition on the damage's origin (states weapon, bump, blocking_emerging).
F5 tiles that turn into Lava: terrain lava.
F6 a jump over obstacles (Leaper) is can move, not a keyword; a keyword written on a move act (Flying, Smoke Bombs) is no
   keyword of that move."""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE); import source
G = 'into_the_breach'
TEXT = {i: ' '.join((t or '').split()) for i, t in source.lib().execute('select id, text from entities where game=?', (G,))}
NOW_SURE = {'params': set(), 'act': set(), 'if': set(), 'to': set()}


def effects(x):
    if isinstance(x, dict):
        if isinstance(x.get('do'), list):
            for e in x['do']: yield x, e
        for v in x.values(): yield from effects(v)
    elif isinstance(x, list):
        for v in x: yield from effects(v)


def upgrades(t):
    """[(name, description)] in the card's order; a mech's text lists its weapon's upgrades"""
    return re.findall(r'(?:Upgrades: |; )([^;]+?) \(\d Reactor Cores?\):\s*([^;]*)', t)


def upgrade_abilities(r, n):
    return [a for a in r.get('abilities', []) if any(c.get('test') == 'upgraded' and c.get('n') == n for c in a.get('if', []))]


def origin_if(vals):
    f = {'attr': 'origin', 'op': 'is', 'val': vals[0]} if len(vals) == 1 else {'attr': 'origin', 'op': 'in', 'vals': vals}
    return {'test': 'it_matches', 'of': {'with': [f]}}


def fix(r):
    t = TEXT.get(r.get('id'), ''); n = 0
    for ab, e in list(effects(r)):
        p = e.get('params') or {}
        # F1
        if e.get('act') == 'damage' and 'min' in p and 'max' in p and isinstance(p['min'], int) and isinstance(p['max'], int):
            lo, hi = sorted((p.pop('min'), p.pop('max'))); p['amount'] = {'x': 'range', 'items': [lo, hi]}
            NOW_SURE['params'].add(r['id']); n += 1
        # F2
        if e.get('act') == 'keyword_action' and e.get('keyword') == 'Flip attack direction':
            e['act'] = 'redirect_attack'; e.pop('keyword'); NOW_SURE['act'].add(r['id']); n += 1
        # F5
        if e.get('act') == 'set_terrain' and re.search(r'\binto Lava\b', t):
            for f in (e.get('to') or {}).get('with', []):
                if f.get('attr') == 'terrain' and f.get('val') != 'lava': f['val'] = 'lava'; NOW_SURE['to'].add(r['id']); n += 1
        # F6
        if e.get('act') == 'give_keyword' and e.get('keyword') == 'Jump' and (e.get('on') or {}).get('pick') == 'self':
            for k in ('keyword',): e.pop(k)
            e.update({'act': 'can', 'params': {'event': 'moves'}, 'to': {'kind': 'position'}, 'lasts': 'while'}); n += 1
        if e.get('act') == 'move' and e.get('keyword') == 'Flying': e.pop('keyword'); n += 1
    # F3
    for k, (name, desc) in enumerate(upgrades(t), 1):
        m = re.match(r'\+(\d) Range$', name.strip())
        for a in upgrade_abilities(r, k):
            if m and [e.get('act') for e in a['do']] == ['increase_effect'] and (a['do'][0].get('params') or {}).get('amount') == 1:
                a['do'][0]['params'] = {'range': int(m.group(1))}; NOW_SURE['params'].add(r['id']); n += 1
            d = re.search(r'max distance and damage by (\d)', desc)
            if d and not any(e.get('act') == 'damage' for e in a['do']):
                base = next((e for ab0 in r['abilities'] if not ab0.get('if') for e in ab0['do']
                             if e.get('act') == 'damage' and (e.get('on') or {}).get('pick') != 'self'), None)
                if base: a['do'].append({'act': 'damage', 'on': json.loads(json.dumps(base['on'])), 'params': {'amount': int(d.group(1))}, 'link': 'and'}); n += 1
    # F4
    want = (['weapon'] if re.search(r'\bWeapon damage (?:to|against) this unit\b', t) else
            ['bump', 'blocking_emerging'] if re.search(r'\bfrom Bumps and blocking emerging Vek\b', t) else
            ['blocking_emerging'] if re.search(r'\bdamage when blocking emerging Vek\b', t) else None)
    if want:
        for a in r.get('abilities', []):
            if (a.get('when') or {}).get('event') != 'damaged': continue
            ifs = [c for c in a.get('if', []) if not (c.get('test') == 'it_matches' and
                   any(f.get('attr') in ('state', 'origin') for f in (c.get('of') or {}).get('with', [])))]
            new = ifs + [origin_if(want)]
            if a.get('if') != new: a['if'] = new; n += 1
            NOW_SURE['if'].add(r['id'])
    for field, ids in NOW_SURE.items():
        if r.get('id') in ids and field in r.get('unsure', []):
            r['unsure'].remove(field)
            if not r['unsure']: r.pop('unsure')
    if re.search(r'\bDamage and flip target\b', t) and 'act' not in r.get('unsure', []):
        r.setdefault('unsure', []).append('act'); n += 1
    return n


for p in sorted(glob.glob(os.path.join(HERE, 'read', G, '*.jsonl'))):
    if p.endswith(('proposals.jsonl', 'rejected.jsonl')): continue
    recs = [json.loads(l) for l in open(p) if l.strip()]
    n = sum(fix(r) for r in recs)
    open(p, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in recs))
    print(os.path.relpath(p, HERE), n, 'changed')
