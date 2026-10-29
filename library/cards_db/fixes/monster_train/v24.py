"""Monster Train records, 28 Oct 2026 (v24; Sacrifice 29 Oct); safe to run twice.
- Consume (keyword entry): the card goes to the Consume pile = act exhaust (it causes the event exhausted, which Etch waits for).
- "Gorge:" triggers: the wiki says Gorge triggers when this unit eats a Morsel unit, so the eaten unit is a Morsel (object filter)."""
import json, os
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
names = {}
for f in ('batch_001', 'keywords'):
    for l in open(os.path.join(HERE, 'input', 'monster_train', f + '.jsonl')):
        r = json.loads(l); names[r['id']] = r['name']
# Sacrifice (keyword entry): the card names the type of unit to kill ("Sacrifice Imp"), so the unit is the card's target
# (pick it), not one the keyword picks itself (normalize N9 would drop the card's target otherwise)
SACRIFICE = [{'when': {'event': 'activated'}, 'do': [{'act': 'kill', 'on': {'kind': 'unit', 'side': 'mine', 'pick': 'it', 'zone': 'board'}}]}]
CONSUME = [{'when': {'event': 'played', 'object': {'pick': 'self'}}, 'do': [{'act': 'exhaust', 'on': {'pick': 'self'}}]}]
for f in ('batch_001.jsonl', 'keywords.jsonl'):
    p = os.path.join(HERE, 'read', 'monster_train', f); recs = [json.loads(l) for l in open(p)]; n = 0
    for r in recs:
        if names.get(r['id']) == 'Sacrifice' and r['abilities'] != SACRIFICE:
            r['abilities'] = SACRIFICE; n += 1
        if names.get(r['id']) == 'Consume' and r['abilities'] != CONSUME:
            r['abilities'] = CONSUME; n += 1
        for ab in r.get('abilities', []):
            w = ab.get('when') or {}
            if w.get('event') == 'eats' and w.get('actor') == {'pick': 'self'}:
                o = w.setdefault('object', {'kind': 'unit'})
                if not any(x.get('attr') == 'type' for x in o.get('with', [])):
                    o.setdefault('kind', 'unit'); o.setdefault('with', []).append({'attr': 'type', 'op': 'is', 'ref': 'Morsel'}); n += 1
    open(p, 'w').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in recs))
    print(f, n, 'changed')
