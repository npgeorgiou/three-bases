"""Runeterra records, 31 Oct 2026 (v64), by rule; safe to run twice. Found by Kaptain on Poppy ("helped to level up by all units"):
- "Level up: I've <done> ..." (not "I've seen"): the card itself does it. "I've attacked with allies 3 times" counts Poppy's own
  attacks, so only another attack for her (Rally, a free attack) helps; the reader had "attacks by any allied unit"."""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE); import source
lib = source.lib()
text = {i: ' '.join((t or '').split()) for i, t in lib.execute("select id, text from entities where game='runeterra'")}
n = 0
for P in glob.glob(os.path.join(HERE, 'read', 'runeterra', '*.jsonl')):
    recs = [json.loads(l) for l in open(P) if l.strip()]; changed = False
    for r in recs:
        if not re.search(r"Level up: I've (?!seen)", text.get(r.get('id'), '')): continue
        for ab in r.get('abilities', []):
            if not any(e.get('act') == 'level_up' for e in ab.get('do', [])): continue
            for cd in ab.get('if', []):
                ev = cd.get('event') or {}
                a = ev.get('actor') or {}
                if cd.get('test') == 'event_count' and a and a.get('pick') != 'self' and not (ev.get('object') or {}).get('pick') == 'self':
                    ev['actor'] = {'pick': 'self'}; n += 1; changed = True
    if changed: open(P, 'w').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in recs))
print(n, 'conditions changed')
