"""Slay the Spire records, 30 Oct 2026 (v51), by rule over the texts; safe to run twice.
- "your next Orb", "all Orbs" (Loop, ...): an effect on a keyword with no filter, in a card whose text names Orbs, acts on the
  four Orbs (keyword in Lightning, Frost, Dark, Plasma), as v49 did for filters naming "Orb"."""
import glob, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'sts1'
text = {}
for f in glob.glob(os.path.join(HERE, 'input', G, '*.jsonl')):
    for l in open(f):
        x = json.loads(l); text[x['id']] = ' '.join(x['text'].split())


def fix(r):
    if not re.search(r'\bOrbs?\b', text.get(r['id'], '')): return
    for ab in r.get('abilities', []):
        for d in ab.get('do', []):
            on = d.get('on')
            if isinstance(on, dict) and on.get('kind') == 'keyword' and not on.get('with') and 'keyword' not in d:
                on['with'] = [{'attr': 'keyword', 'op': 'in', 'refs': ['Lightning', 'Frost', 'Dark', 'Plasma']}]


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
