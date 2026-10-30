"""Slay the Spire records, 30 Oct 2026 (v52), by rule over the texts; safe to run twice.
- "N Frost / Lightning Channeled this combat" (Blizzard, Thunder Strike) counts the Orb named, not every Channel: the Orb
  used is the keyword of the count (refs.py: "Channel 1 Lightning" now makes Lightning used)."""
import glob, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'sts1'
text = {}
for f in glob.glob(os.path.join(HERE, 'input', G, '*.jsonl')):
    for l in open(f):
        x = json.loads(l); text[x['id']] = ' '.join(x['text'].split())


def walk(o, fn):
    if isinstance(o, dict):
        fn(o)
        for v in list(o.values()): walk(v, fn)
    elif isinstance(o, list):
        for v in o: walk(v, fn)


def fix(r):
    m = re.search(r'\b(Frost|Lightning|Dark|Plasma) Channeled\b', text.get(r['id'], ''))
    if not m: return
    def f(o):
        if o.get('event') == 'keyword_used' and isinstance(o.get('object'), dict):
            for w in o['object'].get('with', []):
                if w.get('attr') == 'keyword' and w.get('ref') == 'Channel': w['ref'] = m.group(1)
    walk(r.get('abilities', []), f)


n = 0
for f in sorted(glob.glob(os.path.join(HERE, 'read', G, '*.jsonl'))):
    b = os.path.basename(f)
    if b.endswith(('proposals.jsonl', 'rejected.jsonl')) or b in ('auto.jsonl', 'game_rules.jsonl', 'keywords.jsonl'): continue
    lines = [l for l in open(f) if l.strip()]; recs = [json.loads(l) for l in lines]; m = 0
    sep = None if lines and lines[0].startswith('{"id": ') else (',', ':')
    for r in recs:
        before = json.dumps(r, sort_keys=True); fix(r); m += json.dumps(r, sort_keys=True) != before
    if m: open(f, 'w').write(''.join(json.dumps(r, ensure_ascii=False, separators=sep) + '\n' for r in recs))
    n += m
print(f'{n} records changed')
