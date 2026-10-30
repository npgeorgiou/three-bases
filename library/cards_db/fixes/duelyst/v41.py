"""Duelyst, 30 Oct 2026 (Kaptain: each General's spell is its own card), by rule; safe to run twice.
A General's Bloodbound Spell is its own card (the General's signature card in open-duelyst, already read with its own
record); the General's text now names it ("Bloodbound Spell: Roar."). The General's record drops the copy of that spell
(the ability set off when my Bloodbound Spell is played), so the spell's effects sit on the spell card only."""
import glob, json, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEAD = {e['id'] for e in map(json.loads, open(os.path.join(HERE, 'supplement', 'duelyst.jsonl')))
        if e['category'] == 'leader' and (e['text'] or '').startswith('Bloodbound Spell: ')}
def bbs_copy(a):
    w = a.get('when') or {}
    return w.get('event') == 'played' and any(f.get('attr') == 'keyword' and f.get('ref') == 'Bloodbound Spell'
                                              for f in ((w.get('object') or {}).get('with') or []))
for p in sorted(glob.glob(os.path.join(HERE, 'read', 'duelyst', '*.jsonl'))):
    if p.endswith(('proposals.jsonl', 'rejected.jsonl')): continue
    recs = [json.loads(l) for l in open(p) if l.strip()]; n = 0
    for r in recs:
        if r.get('id') in LEAD and any(bbs_copy(a) for a in r.get('abilities', [])):
            r['abilities'] = [a for a in r['abilities'] if not bbs_copy(a)]; n += 1
    open(p, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in recs))
    print(os.path.relpath(p, HERE), n, 'changed')
