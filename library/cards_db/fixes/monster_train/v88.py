"""Monster Train, 14 Nov 2026 (v88), by rule; safe to run twice.
A text that names both sides in one effect ("Descend friendly and enemy units on this floor", "Deal 100 damage to friendly and
enemy units") was read as one effect with no side, so nothing marked it as hitting enemies (Cave In, Inferno). The effect is
split in two: one on the mine side, one on the enemy side (same filters, link and)."""
import copy, glob, json, os, re, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE); import source
G = 'monster_train'
BOTH = re.compile(r"\b(?:friendly|allied|your|ally|allies) and (?:enemy|enemies)\b|\b(?:enemy|enemies) and (?:friendly|allied|your)\b", re.I)
TEXT = {i: ' '.join((t or '').split()) for i, t in source.lib().execute('select id, text from entities where game=?', (G,))}


def fix(r):
    if not BOTH.search(TEXT.get(r.get('id'), '')): return 0
    n = 0
    for a in r.get('abilities', []):
        out = []
        for e in a.get('do', []):
            on = e.get('on') or {}
            if e.get('act') != 'give_keyword' and on.get('pick') == 'all' and on.get('kind') in ('unit', 'unit_or_structure') and not on.get('side'):
                m = copy.deepcopy(e); m['on']['side'] = 'mine'
                en = copy.deepcopy(e); en['on']['side'] = 'enemy'; en['link'] = 'and'
                out += [m, en]; n += 1
            else: out.append(e)
        a['do'] = out
    return n


for p in sorted(glob.glob(os.path.join(HERE, 'read', G, '*.jsonl'))):
    if p.endswith(('proposals.jsonl', 'rejected.jsonl')): continue
    recs = [json.loads(l) for l in open(p) if l.strip()]
    n = sum(fix(r) for r in recs)
    if n: open(p, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in recs))
    print(os.path.relpath(p, HERE), n, 'changed')
