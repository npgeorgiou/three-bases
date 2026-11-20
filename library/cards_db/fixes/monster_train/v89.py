"""Monster Train, 20 Nov 2026 (v89), by rule; safe to run twice.
Kaptain, 20 Nov 2026: hatching from an egg is not a summon, it is a transform (the egg turns into the creature).
A text with 'Hatch:' and a summon in the dies-of-self ability: that row becomes a transform of the card itself into the named unit (no record carries the Hatch keyword, so the transform shape is used; amount kept)."""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE); import source
G = 'monster_train'
HATCH = re.compile(r"\bHatch:", re.I)
TEXT = {i: ' '.join((t or '').split()) for i, t in source.lib().execute('select id, text from entities where game=?', (G,))}
NAME = {i: n for i, n in source.lib().execute('select id, name from entities where game=?', (G,))}

def fix(r):
    n = 0
    for a in r.get('abilities', []):
        if (a.get('when') or {}).get('event') != 'dies' or (a['when'].get('object') or {}).get('pick') != 'self': continue
        for e in a.get('do', []):
            if e.get('act') == 'summon' and e.get('card'):
                n += 1; e['act'] = 'transform'; e['on'] = {'pick': 'self'}
    return n

for p in sorted(glob.glob(os.path.join(HERE, 'read', G, '*.jsonl'))):
    if p.endswith(('proposals.jsonl', 'rejected.jsonl')): continue
    recs = [json.loads(l) for l in open(p) if l.strip()]
    hits = [r['id'] for r in recs if HATCH.search(TEXT.get(r.get('id'), '')) and fix(r)]
    if hits: open(p, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in recs))
    print(os.path.relpath(p, HERE), len(hits), 'changed', [NAME.get(i) for i in hits])
