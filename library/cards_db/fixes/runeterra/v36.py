"""Runeterra keyword records, 29 Oct 2026 (v36), by rule; safe to run twice. Found when the text audit began reading keyword
entries (Inscryption, whose cards are only their sigils):
- "For each <Keyword>:" (Spawn): the effects happen once per point the card writes after the keyword: params times x listed."""
import json, os, re, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE); import source
lib = source.lib()
text = {i: (n, ' '.join((t or '').split())) for i, n, t in lib.execute("select id, name, text from entities where game='runeterra' and category='keyword'")}
P = os.path.join(HERE, 'read', 'runeterra', 'keywords.jsonl')
recs = [json.loads(l) for l in open(P) if l.strip()]; n = 0
for r in recs:
    name, t = text.get(r['id'], ('', ''))
    if not re.match(rf'For each {re.escape(name)}:', t): continue
    for ab in r.get('abilities', []):
        for e in ab.get('do', []):
            if (e.get('params') or {}).get('times') != {'x': 'listed'}:
                e.setdefault('params', {})['times'] = {'x': 'listed'}; n += 1
open(P, 'w').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in recs))
print(n, 'effects changed')
