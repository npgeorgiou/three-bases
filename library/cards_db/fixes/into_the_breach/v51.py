"""Into the Breach, 30 Oct 2026, Claude's check of 20 cards (CHECK_20_into_the_breach.md): the families of
deck_read_into_the_breach.md "Check of 20 cards", by rule; safe to run twice.
F13 Flying "can be positioned at any terrain tile, except mountains and other units; mountains and unfriendly units can be
    overflown": passing over is no place to stop; the can-move rows onto mountains and onto enemy units go.
F14 "Shield adjacent ally or Building" (Repulse, Pulse Mech): every adjacent ally or building, nothing is chosen.
F15 Burrowers "3 tiles in a row", "a 3-tile wide area in front of them": the tile in front and its two sides, all of them.
F16 "Increases area hit by 1 tile" (Explosive Goo): the hit area grows, increase_effect params area 1 (vocab v51)."""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE); import source
G = 'into_the_breach'
TEXT = {i: ' '.join((t or '').split()) for i, t in source.lib().execute('select id, text from entities where game=?', (G,))}


def upgrades(t):
    return re.findall(r'(?:Upgrades: |; )([^;]+?) \(\d Reactor Cores?\):\s*([^;]*)', t)


def upgrade_abilities(r, n):
    return [a for a in r.get('abilities', []) if any(c.get('test') == 'upgraded' and c.get('n') == n for c in a.get('if', []))]


def fix(r):
    t = TEXT.get(r.get('id'), ''); n = 0
    # F13
    if re.search(r'except mountains and other units', t):
        for a in r.get('abilities', []):
            keep = [e for e in a['do'] if not (e.get('act') == 'can' and (e.get('params') or {}).get('event') == 'moves' and any(
                    (f.get('attr') == 'terrain' and f.get('op') == 'is' and f.get('val') == 'mountain') or
                    (f.get('attr') == 'position' and f.get('val') == 'same_space') for f in (e.get('to') or {}).get('with', [])))]
            if len(keep) != len(a['do']):
                n += len(a['do']) - len(keep); a['do'] = keep
                if keep and 'link' in keep[0]: keep[0].pop('link')
    # F14
    if re.search(r'\bShield adjacent ally or Building\b', t):
        for a in r.get('abilities', []):
            for e in a['do']:
                on = e.get('on') or {}
                if e.get('act') == 'give_keyword' and on.get('pick') == 'chosen' and 'bordering' in json.dumps(on.get('with', [])):
                    on['pick'] = 'all'; n += 1
    # F15
    if re.search(r'3-tile wide area in front of them', t):
        for a in r.get('abilities', []):
            for e in a['do']:
                on = e.get('on') or {}
                if e.get('act') == 'damage' and on.get('n') == 3 and 'surrounding' in json.dumps(on.get('with', [])):
                    on.pop('n'); on['pick'] = 'all'
                    on['with'] = [{'attr': 'position', 'op': 'in', 'vals': ['same_space', 'sides'], 'of': {'kind': 'position', 'with': [
                        {'attr': 'position', 'op': 'is', 'val': 'in_front', 'of': {'pick': 'self'}}]}}]; n += 1
    # F16
    for k, (name, desc) in enumerate(upgrades(t), 1):
        m = re.search(r'Increases area hit by (\d) tiles?', desc)
        if not m: continue
        for a in upgrade_abilities(r, k):
            new = [{'act': 'increase_effect', 'on': {'pick': 'self'}, 'params': {'area': int(m.group(1))}}]
            if a['do'] != new: a['do'] = new; n += 1
    return n


for p in sorted(glob.glob(os.path.join(HERE, 'read', G, '*.jsonl'))):
    if p.endswith(('proposals.jsonl', 'rejected.jsonl')): continue
    recs = [json.loads(l) for l in open(p) if l.strip()]
    n = sum(fix(r) for r in recs)
    open(p, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in recs))
    print(os.path.relpath(p, HERE), n, 'changed')
