"""Slay the Spire records, 30 Oct 2026 (v50): readings the deck read showed wrong, fixed by rule over the texts; safe to run twice.
- "<Keyword> affects this card N times" (Heavy Blade): the keyword's effect is bigger on this card only: increase_effect on
  pick self (the readers wrote every keyword of mine, so the card read as making Strength stronger for its givers).
- "your cost X cards" (Chemical X): the target keeps its filter, cost eq the X paid (the readers dropped it: every card).
- A keyword filter on Stance: Stance is no keyword a card gives; the keywords whose glossary text calls them "this Stance"
  (Wrath, Calm, Divinity) are ("whenever you change Stances": entering Wrath or Calm), as v49 did for "Orb".
- "Block gained from cards" (Dexterity, Frail): the Block is given by my cards (actor spell, mine), not by relics or Orbs."""
import glob, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'sts1'
text = {}
for f in glob.glob(os.path.join(HERE, 'input', G, '*.jsonl')):
    for l in open(f):
        x = json.loads(l); text[x['id']] = ' '.join(x['text'].split())
kwtext = {json.loads(l)['name']: json.loads(l)['text'] for l in open(os.path.join(HERE, 'input', G, 'keywords.jsonl')) if l.strip()}
KINDS = {}  # a keyword and the keywords whose own text calls them "this <keyword>"
for n, t in kwtext.items():
    for m in re.finditer(r'\bthis ([A-Z][\w-]+)', t):
        if m.group(1) in kwtext and m.group(1) != n: KINDS.setdefault(m.group(1), []).append(n)


def walk(o, fn):
    if isinstance(o, dict):
        fn(o)
        for v in list(o.values()): walk(v, fn)
    elif isinstance(o, list):
        for v in o: walk(v, fn)


def fix(r):
    t = text.get(r['id'], ''); abs_ = r.get('abilities', [])
    m = re.search(r'\b([A-Z]\w+) affects this card \d+ times', t)
    if m:
        def f(o):
            if o.get('act') == 'increase_effect' and isinstance(o.get('on'), dict) and o['on'].get('kind') == 'keyword' and \
                    any(w.get('ref') == m.group(1) for w in o['on'].get('with', [])):
                o['on']['pick'] = 'self'; o['on'].pop('side', None)
        walk(abs_, f)
    if re.search(r'\bcost X cards\b', t):
        def f(o):
            if o.get('act') == 'increase_effect' and isinstance(o.get('on'), dict):
                ww = o['on'].setdefault('with', [])
                if not any(w.get('attr') == 'cost' for w in ww): ww.append({'attr': 'cost', 'op': 'eq', 'n': {'x': 'x_paid'}})
        walk(abs_, f)
        r.get('unsure', []).remove('on') if 'on' in r.get('unsure', []) else None
    if re.search(r'\bfrom cards\b', t):
        for ab in abs_:
            w = ab.get('when', {})
            if w.get('event') == 'given_keyword' and 'actor' not in w: w['actor'] = {'kind': 'spell', 'side': 'mine'}
    def f(o):
        for w in o.get('with', []) if isinstance(o.get('with'), list) else []:
            if w.get('attr') == 'keyword' and w.get('ref') in KINDS:
                w['refs'] = sorted(KINDS[w.pop('ref')]); w['op'] = 'in'
    walk(abs_, f)


def main():
    n = 0
    for f in sorted(glob.glob(os.path.join(HERE, 'read', G, '*.jsonl'))):
        b = os.path.basename(f)
        if b.endswith(('proposals.jsonl', 'rejected.jsonl')) or b in ('auto.jsonl', 'game_rules.jsonl'): continue
        lines = [l for l in open(f) if l.strip()]; recs = [json.loads(l) for l in lines]; m = 0
        sep = None if lines and lines[0].startswith('{"id": ') else (',', ':')  # each file keeps its own form
        for r in recs:
            before = json.dumps(r, sort_keys=True); fix(r); m += json.dumps(r, sort_keys=True) != before
        if m: open(f, 'w').write(''.join(json.dumps(r, ensure_ascii=False, separators=sep) + '\n' for r in recs))
        n += m
    print(f'{n} records changed; kinds {KINDS}')


main()
