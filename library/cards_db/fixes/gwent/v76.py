"""Gwent, 6 Nov 2026 (v76, error kinds of the second reading checked over all cards); safe to run twice.
- Gwent's one stat is strength (BRIEF Game words: Gwent): attr / by / params "power" -> "strength" (6 cards).
- "Profit N" is gaining N Coins when played (BRIEF: Coins), one form: an always ability giving self the keyword Profit with
  a plain number becomes a played ability with mana_gain of that number on the player's Coins (16 cards wrote it as a
  keyword, 36 as mana_gain). A Profit whose number grows ("increase the Profit by 1") keeps its increase_effect."""
import glob, json, os
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'gwent'
COINS = {'kind': 'secondary_resource', 'side': 'mine'}


def strength(o):
    n = 0
    if isinstance(o, dict):
        for k in ('attr', 'by'):
            if o.get(k) == 'power': o[k] = 'strength'; n += 1
        if isinstance(o.get('params'), dict) and 'power' in o['params']: o['params']['strength'] = o['params'].pop('power'); n += 1
        for v in o.values(): n += strength(v)
    elif isinstance(o, list):
        for v in o: n += strength(v)
    return n


def profit(r):
    n = 0
    for ab in r.get('abilities', []):
        if (ab.get('when') or {}).get('event') != 'always' or ab.get('if'): continue
        for d in ab.get('do', []):
            amt = (d.get('params') or {}).get('amount')
            if d.get('act') == 'give_keyword' and d.get('keyword') == 'Profit' and isinstance(amt, (int, float)):
                ab['when'] = {'event': 'played', 'object': {'pick': 'self'}}
                d.clear(); d.update(act='mana_gain', on=dict(COINS), params={'amount': amt}); n += 1
    return n


def main():
    for path in sorted(glob.glob(os.path.join(HERE, 'read', G, '*.jsonl'))):
        if path.endswith('proposals.jsonl') or 'game_rules' in path or 'keywords' in path: continue
        L = [json.loads(l) for l in open(path) if l.strip()]; n = 0
        for r in L: n += strength(r.get('abilities', [])) + profit(r)
        if n: open(path, 'w').write(''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n' for r in L))
        print(os.path.basename(path), n, 'changed')


if __name__ == '__main__':
    main()
