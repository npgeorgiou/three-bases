"""Runeterra records, 29 Oct 2026 (v34), by rule from audit_text.py; safe to run twice.
- "... enemies or the enemy Nexus": a damage on enemy units also has the enemy player as the other choice (Make it Rain).
- "<allies> everywhere": a stat change on all my cards that leaves out where they are reaches hand and deck too (zone
  everywhere; Rek'Sai (level 2))."""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE); import source
lib = source.lib()
text = {i: ' '.join((t or '').split()) for i, t in lib.execute("select id, text from entities where game='runeterra'")}

for p in sorted(glob.glob(os.path.join(HERE, 'read', 'runeterra', 'batch_*.jsonl'))):
    recs = [json.loads(l) for l in open(p) if l.strip()]; n = 0
    for r in recs:
        t = text.get(r.get('id'), '')
        for ab in r.get('abilities', []):
            do = ab.get('do', [])
            if re.search(r'enemies or the enemy Nexus', t):
                for j, e in enumerate(list(do)):
                    on = e.get('on') or {}
                    if e.get('act') == 'damage' and on.get('side') == 'enemy' and on.get('kind') == 'unit' and \
                       not any((x.get('on') or {}).get('kind') == 'player' for x in do):
                        do.insert(j + 1, {'act': 'damage', 'on': {'kind': 'player', 'side': 'enemy'}, 'params': dict(e.get('params') or {}), 'link': 'or'}); n += 1
            if re.search(r'\beverywhere\b', t):
                for e in do:
                    on = e.get('on') or {}
                    if e.get('act') == 'stat_change' and on.get('pick') == 'all' and on.get('side') == 'mine' and 'zone' not in on:
                        on['zone'] = 'everywhere'; n += 1
    if n:
        open(p, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in recs)); print(os.path.basename(p), n)
