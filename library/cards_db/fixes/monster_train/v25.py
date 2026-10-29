"""Monster Train records, 29 Oct 2026 (v25), done by rule instead of a re-read; safe to run twice.
- "15x the number of X", "5x the amount healed", "3/5/7 damage per Shard" were read as a count with inner 15: now x product, items [15, the count] (BRIEF).
- Doubling stacks ("Double the amount of Rage", "Double Armor"): give_keyword with the count of stacks, not double the count.
- "uncommon or rare" / "common or uncommon" Morsels: rarity in both values (the readers kept only one).
- "non-boss": state not boss. "Gain 1 EchoSlot": kind lane_resource_slot. "Sacrifice Imp." / "Sacrifice.": "on" my unit."""
import json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(HERE, 'read', 'monster_train', 'batch_001.jsonl')
text = {}
for l in open(os.path.join(HERE, 'input', 'monster_train', 'batch_001.jsonl')):
    x = json.loads(l); text[x['id']] = (x['name'], x['text'].lower())

def amounts(o, fix):
    if isinstance(o, dict):
        for k, v in list(o.items()):
            inner = v.get('inner') if isinstance(v, dict) else None
            if isinstance(v, dict) and v.get('x') in ('count', 'event_count', 'event_amount', 'stat') and (isinstance(inner, (int, float)) or (isinstance(inner, dict) and inner.get('x') == 'per_level')):
                n = v.pop('inner'); o[k] = {'x': 'product', 'items': [n, v]}; fix.add('x')
            amounts(o[k], fix)
    elif isinstance(o, list):
        for v in o: amounts(v, fix)

recs = [json.loads(l) for l in open(P)]; changed = 0
for r in recs:
    name, t = text[r['id']]; fix = set(); before = json.dumps(r, sort_keys=True)
    amounts(r['abilities'], fix)
    for ab in r['abilities']:
        for e in ab['do']:
            a = (e.get('params') or {}).get('amount')
            if e.get('act') == 'give_keyword' and isinstance(a, dict) and a.get('x') == 'double' and (a.get('inner') or {}).get('x') == 'count':
                e['params']['amount'] = a['inner']; fix.add('act')
            for f in (e.get('on') or {}).get('with', []):
                if f.get('attr') == 'rarity' and f.get('op') == 'is':
                    pair = ['uncommon', 'rare'] if 'uncommon or rare' in t else ['common', 'uncommon'] if 'common or uncommon' in t else None
                    if pair: f.pop('val'); f['op'] = 'in'; f['vals'] = pair; fix.add('rarity')
            if 'non-boss' in t and e.get('act') == 'kill' and (e.get('on') or {}).get('side') in ('enemy', 'any'):
                w = e['on'].setdefault('with', [])
                if {'attr': 'state', 'op': 'not', 'val': 'boss'} not in w: w.append({'attr': 'state', 'op': 'not', 'val': 'boss'})
                fix.add('state')
            if e.get('act') == 'keyword_action' and e.get('keyword') == 'Sacrifice' and 'on' not in e:
                e['on'] = {'kind': 'unit', 'side': 'mine', 'pick': 'chosen', 'zone': 'board'}
                if 'sacrifice imp' in t: e['on']['with'] = [{'attr': 'type', 'op': 'is', 'ref': 'Imp'}]
    if 'echoslot' in t:
        e = next(e for ab in r['abilities'] for e in ab['do'] if e.get('act') == 'mana_gain')
        e['on'] = {'kind': 'lane_resource_slot'}; fix.add('kind')
    if name == 'Soul Siphon': fix.add('kind')  # "fill the Echo slots": lane_resource filled up (x full)
    if fix and r.get('unsure'):
        r['unsure'] = [u for u in r['unsure'] if u not in fix]
        if not r['unsure']: del r['unsure']
    if json.dumps(r, sort_keys=True) != before: changed += 1
open(P, 'w').write(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in recs))
print(changed, 'records changed')
