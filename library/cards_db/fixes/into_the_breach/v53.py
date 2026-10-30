"""Into the Breach, 30 Oct 2026, reading the networks of Claude's builds (every mech with its second weapon):
F25 "No longer applies Smoke on self or allies" (Smoke Pellets' Ally Immune) was read as removing Smoke from allies; it is
    that my units are not given Smoke by it: cant given_keyword Smoke on my units there (as Smoke Immunity). Safe to run twice."""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE); import source
G = 'into_the_breach'
TEXT = {i: ' '.join((t or '').split()) for i, t in source.lib().execute('select id, text from entities where game=?', (G,))}


def fix(r):
    m = re.search(r'No longer applies (\w+) on self or allies', TEXT.get(r.get('id'), ''))
    if not m: return 0
    n = 0
    for a in r.get('abilities', []):
        for e in a['do']:
            if e.get('act') == 'remove_keyword' and e.get('keyword') == m.group(1) and (e.get('on') or {}).get('side') == 'mine':
                e.update({'act': 'cant', 'params': {'event': 'given_keyword'}, 'lasts': 'while'}); n += 1
    return n


for p in sorted(glob.glob(os.path.join(HERE, 'read', G, '*.jsonl'))):
    if p.endswith(('proposals.jsonl', 'rejected.jsonl')): continue
    recs = [json.loads(l) for l in open(p) if l.strip()]
    n = sum(fix(r) for r in recs)
    open(p, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in recs))
    print(os.path.relpath(p, HERE), n, 'changed')
