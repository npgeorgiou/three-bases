"""Into the Breach, 31 Oct 2026 (links check, round 1):
F26 a pilot's "After Move" (Rosie Rivets) is its mech's own Move, not being pushed: the trigger "moves_onto self" gets the
    pilot as its actor (actor self, no object), so pushes by other cards do not set it off. Safe to run twice."""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE); import source
G = 'into_the_breach'
TEXT = {i: ' '.join((t or '').split()) for i, t in source.lib().execute('select id, text from entities where game=?', (G,))}


def fix(r):
    if not re.search(r'Pilot ability: [^:]+: After Move\b', TEXT.get(r.get('id'), '')): return 0
    n = 0
    for a in r.get('abilities', []):
        w = a.get('when') or {}
        if w.get('event') in ('moves', 'moves_onto') and (w.get('object') or {}).get('pick') == 'self':
            w.pop('object'); w['actor'] = {'pick': 'self'}; n += 1
    return n


for p in sorted(glob.glob(os.path.join(HERE, 'read', G, '*.jsonl'))):
    if p.endswith(('proposals.jsonl', 'rejected.jsonl')): continue
    recs = [json.loads(l) for l in open(p) if l.strip()]
    n = sum(fix(r) for r in recs)
    open(p, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in recs))
    print(os.path.relpath(p, HERE), n, 'changed')
