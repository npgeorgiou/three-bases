"""Runeterra records, 29 Oct 2026 (v30), done by rule instead of a re-read; safe to run twice.
- "your traps" / "your traps or boons" are every card with the keyword Trap (or Boon), not one trap card or a name family:
  a filter card is Flashbomb Trap or name_has Trap on a counted or awaited trap_activated is written keyword is Trap
  (Caitlyn, Caitlyn (level 2); Poison Puffcaps are traps too)."""
import glob, json, os
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def fix(o):
    n = 0
    if isinstance(o, dict):
        if o.get('event') == 'trap_activated' and isinstance(o.get('object'), dict):
            w = o['object'].get('with') or []
            for f in w:
                if (f.get('attr') == 'card' and f.get('ref') == 'Flashbomb Trap') or (f.get('attr') == 'name_has' and f.get('ref') == 'Trap'):
                    f.clear(); f.update({'attr': 'keyword', 'op': 'is', 'ref': 'Trap'}); n += 1
        for v in o.values(): n += fix(v)
    elif isinstance(o, list):
        for v in o: n += fix(v)
    return n


for p in sorted(glob.glob(os.path.join(HERE, 'read', 'runeterra', 'batch_*.jsonl'))):
    recs = [json.loads(l) for l in open(p) if l.strip()]
    n = sum(fix(r) for r in recs)
    if n:
        open(p, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in recs)); print(os.path.basename(p), n, 'filters')
