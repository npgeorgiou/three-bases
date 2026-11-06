"""Gwent, 6 Nov 2026 (v85): Caranthir: Golden Child "the damage dealt by Frost": Frost is who deals the damage (actor, an effect with
keyword Frost), not a property of the unit hit (v82 wrote it on the object). Safe to run twice. Run from library/cards_db."""
import glob, json, os
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
n = 0
for p in glob.glob(os.path.join(HERE, 'read', 'gwent', '*.jsonl')):
    if p.endswith('proposals.jsonl'): continue
    L = [json.loads(l) for l in open(p) if l.strip()]; ch = False
    def walk(d):
        global n; global ch
        if isinstance(d, dict):
            if d.get('x') == 'event_total' and d.get('event', {}).get('event') == 'damaged':
                e = d['event']; o = e.get('object', {})
                if any(w.get('ref') == 'Frost' for w in o.get('with', [])):
                    e['actor'] = {'kind': 'effect', 'with': o.pop('with')}; n += 1; ch = True
            for v in d.values(): walk(v)
        elif isinstance(d, list):
            for v in d: walk(v)
    for r in L: walk(r)
    if ch: open(p, 'w').write(''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n' for r in L))
print('changed', n)
