"""Runeterra records, 29 Oct 2026 (v33), by rule; safe to run twice.
- "spells and Skills", "spells or Skills", "Fast spells, Slow spells, and Skills": every spell target the phrase names also
  takes Skills (category in spell, skill; a category list gets skill added). When the text also names plain spells
  ("When you play a spell, stop all enemy spells and Skills", Fizz), only targets on the phrase's side change.
- "Double all damage dealt by ...": the damage again on what was damaged is as much as was dealt (amount event_amount),
  not 1 (The Dreadway).
- "cost reduced cards" counted: the counted cards have state cost_reduced (Janna's level-up)."""
import glob, json, os, re, sys
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE); import source
lib = source.lib()
text = {i: ' '.join((t or '').split()) for i, t in lib.execute("select id, text from entities where game='runeterra'")}
PHRASE = re.compile(r"(?:\b(your|enemy|allied)\s+)?(?:\w+\s+)?(?:(?:Fast|Slow|Burst|Focus)\s+)?spells?(?:,\s*(?:Fast|Slow|Burst|Focus)\s+spells?)*,?\s+(?:and|or)\s+skills?", re.I)
SIDE = {'your': 'mine', 'allied': 'mine', 'enemy': 'enemy'}


def walk(o, f):
    if isinstance(o, dict):
        f(o)
        for v in o.values(): walk(v, f)
    elif isinstance(o, list):
        for v in o: walk(v, f)


def has_skill(t):
    return any(f.get('attr') == 'category' and ('skill' in (f.get('vals') or []) or f.get('val') == 'skill') for f in t.get('with') or [])


for p in sorted(glob.glob(os.path.join(HERE, 'read', 'runeterra', 'batch_*.jsonl'))):
    recs = [json.loads(l) for l in open(p) if l.strip()]; n = 0
    for r in recs:
        t = re.sub(r'^Keywords:[^.]*\.\s*', '', text.get(r.get('id'), ''))
        if re.search(r'\bdouble (all )?damage dealt by', t, re.I):
            for ab in r.get('abilities', []):
                ev = (ab.get('when') or {}).get('event')
                for e in ab.get('do', []):
                    if ev == 'damaged' and e.get('act') == 'damage' and (e.get('on') or {}).get('pick') == 'it' and \
                       (e.get('params') or {}).get('amount') != {'x': 'event_amount'}:
                        e.setdefault('params', {})['amount'] = {'x': 'event_amount'}; n += 1
        if re.search(r'cost reduced cards', t, re.I):
            def reduced(o):
                global n
                if o.get('x') in ('event_count',) or o.get('test') == 'event_count':
                    e = o.get('event') if isinstance(o.get('event'), dict) else {}
                    obj = e.get('object')
                    if e.get('event') == 'played' and isinstance(obj, dict) and not any(f.get('val') == 'cost_reduced' for f in obj.get('with', [])):
                        obj.setdefault('with', []).append({'attr': 'state', 'op': 'is', 'val': 'cost_reduced'}); n += 1
            walk(r, reduced)
        found = list(PHRASE.finditer(t))
        if not found: continue
        rest = PHRASE.sub('', t)
        sides = {SIDE.get((m.group(1) or '').lower()) for m in found}
        mixed = re.search(r'\bspells?\b', rest, re.I) is not None
        def add(o):
            global n
            if o.get('kind') != 'spell' or has_skill(o): return
            if mixed and (None in sides or o.get('side') not in sides): return
            w = o.setdefault('with', [])
            cat = next((f for f in w if f.get('attr') == 'category' and f.get('op') == 'in' and 'vals' in f), None)
            if cat: cat['vals'].append('skill')
            elif any(f.get('attr') == 'category' for f in w): return  # one named spell speed alone: not this phrase
            else: w.append({'attr': 'category', 'op': 'in', 'vals': ['spell', 'skill']})
            n += 1
        walk(r, add)
    if n:
        open(p, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in recs)); print(os.path.basename(p), n)
