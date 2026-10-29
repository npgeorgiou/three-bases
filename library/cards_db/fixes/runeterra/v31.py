"""Runeterra records, 29 Oct 2026 (v31), by rule; safe to run twice.
- "You've planted 15+ Poison Puffcaps": a count of Plant used names the planted card (card filter on the object), so
  planting other cards (Flashbomb Traps, Chimes) does not count (Teemo).
- "<Keyword> me" ("Round Start: Boost me."): the keyword action acts on the card itself (on pick self) when the record
  left out what it acts on (Beefcake Mayor)."""
import glob, json, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE); import source
lib = source.lib()
text = {i: ' '.join((t or '').split()) for i, t in lib.execute("select id, text from entities where game='runeterra'")}
cards = {n for (n,) in lib.execute("select name from entities where game='runeterra' and category!='keyword'")}


def walk(o, f):
    if isinstance(o, dict):
        f(o)
        for v in o.values(): walk(v, f)
    elif isinstance(o, list):
        for v in o: walk(v, f)


for p in sorted(glob.glob(os.path.join(HERE, 'read', 'runeterra', 'batch_*.jsonl'))):
    recs = [json.loads(l) for l in open(p) if l.strip()]; n = 0
    for r in recs:
        t = text.get(r.get('id'), '')
        m = re.search(r"planted (\d+)\+? ([A-Z][\w' ]+?)s?\b(?:\.|$)", t)
        planted = m and next((x for x in (m.group(2), m.group(2) + 's', m.group(2).rstrip('s')) if x in cards), None)
        def plant(o):
            global n
            ev = o.get('event'); obj = o.get('object')
            if planted and ev == 'keyword_used' and isinstance(obj, dict) and any(f.get('ref') == 'Plant' for f in obj.get('with', [])) \
               and not any(f.get('attr') == 'card' for f in obj.get('with', [])):
                obj['with'].append({'attr': 'card', 'op': 'is', 'ref': planted}); n += 1
        walk(r, plant)
        for ab in r.get('abilities', []):
            for e in ab.get('do', []):
                kw = e.get('keyword')
                if e.get('act') == 'keyword_action' and kw and 'on' not in e and re.search(rf'\b{re.escape(kw)} me\b', t):
                    e['on'] = {'pick': 'self'}; n += 1
    if n:
        open(p, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in recs)); print(os.path.basename(p), n)
