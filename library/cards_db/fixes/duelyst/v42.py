"""Duelyst, 5 Nov 2026 (line check C7), by rule; safe to run twice.
A text that gives "Grow: +N/+N" gives the Grow keyword, not an unnamed ability (Gargantuan Growth, Godhammer): a given
ability that is Grow's own turn_start stat_change on self, with N from the text, becomes give_keyword Grow with amount N,
so cards that wait for Grow (Oropsisaur) see it."""
import glob, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEXT = {}
for p in glob.glob(os.path.join(HERE, 'input', 'duelyst', '*.jsonl')) + [os.path.join(HERE, 'supplement', 'duelyst.jsonl')]:
    for l in open(p):
        if l.strip():
            e = json.loads(l); TEXT[e['id']] = e.get('text') or ''
def grow_n(ab, text):
    w = ab.get('when') or {}
    d = ab.get('do') or []
    if w.get('event') != 'turn_start' or len(d) != 1 or d[0].get('act') != 'stat_change' or (d[0].get('on') or {}).get('pick') != 'self': return None
    pw = d[0].get('params') or {}
    n = pw.get('power')
    if n is None or n != pw.get('health') or not re.search(r'Grow: \+%d/\+%d' % (n, n), text): return None
    return n
for p in sorted(glob.glob(os.path.join(HERE, 'read', 'duelyst', '*.jsonl'))):
    if p.endswith(('proposals.jsonl', 'rejected.jsonl', 'keywords.jsonl')): continue
    recs = [json.loads(l) for l in open(p) if l.strip()]; k = 0
    for r in recs:
        for a in r.get('abilities', []):
            for e in a.get('do', []):
                if e.get('act') == 'give_ability' and e.get('ability'):
                    n = grow_n(e['ability'], TEXT.get(r.get('id'), ''))
                    if n:
                        del e['ability']; e['act'] = 'give_keyword'; e['keyword'] = 'Grow'
                        e['lasts'] = 'permanent'; e['params'] = {'amount': n}; k += 1
    open(p, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in recs))
    print(os.path.relpath(p, HERE), k, 'changed')
