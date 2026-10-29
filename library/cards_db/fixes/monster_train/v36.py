"""Monster Train keyword record, 29 Oct 2026 (v36), safe to run twice: Sacrifice kills a friendly unit to pay for the card,
so it is act sacrifice (one form in every game, normalize N17 for card records; keyword records are not normalized)."""
import json, os
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(HERE, 'read', 'monster_train', 'keywords.jsonl')
recs = [json.loads(l) for l in open(P) if l.strip()]; n = 0
for r in recs:
    if r['id'] != 2000345: continue  # Sacrifice
    for ab in r['abilities']:
        for e in ab['do']:
            if e.get('act') == 'kill' and (e.get('on') or {}).get('side') == 'mine': e['act'] = 'sacrifice'; n += 1
open(P, 'w').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in recs))
print(n, 'effects changed')
