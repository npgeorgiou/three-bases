"""Marvel Snap, 5 Nov 2026 (v67, step 2.7 text audit); safe to run twice.
- A location's "this turn" is the turn it is revealed: "After this turn" = round_end with limit next_time (as Sakaar); an
  effect or trigger "this turn" = given to the location itself on its reveal, lasts this_round (Hotel Inferno, Fractured
  Frontier, Parker Industries' one-card limit). Kid Omega's "the next card you play this turn": the given trigger lasts
  this_round."""
import glob, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'marvel_snap'
REVEAL = {'event': 'played', 'object': {'pick': 'self'}}


def main():
    inp = {}
    for f in glob.glob(os.path.join(HERE, 'input', G, '*.jsonl')):
        for l in open(f):
            x = json.loads(l)
            if 'id' in x: inp[x['id']] = x
    for path in sorted(glob.glob(os.path.join(HERE, 'read', G, 'batch_*.jsonl'))):
        if path.endswith('proposals.jsonl'): continue
        L = [json.loads(l) for l in open(path) if l.strip()]; n = 0
        for r in L:
            d = inp.get(r['id']) or {}; text = d.get('text') or ''; old = json.dumps(r, sort_keys=True)
            if d.get('category') == 'terrain' and re.search(r'\bthis turn\b', text, re.I):
                new = []
                for ab in r.get('abilities', []):
                    w = ab.get('when') or {}
                    if re.search(r'\bAfter this turn\b', text) and w.get('event') == 'round_end': ab.setdefault('limit', 'next_time'); new.append(ab)
                    elif w.get('event') == 'always' or (w.get('event') == 'played' and (w.get('object') or {}).get('pick') != 'self'):
                        new.append({'when': dict(REVEAL), 'do': [{'act': 'give_ability', 'on': {'pick': 'self'}, 'ability': ab, 'lasts': 'this_round'}]})
                    else: new.append(ab)
                r['abilities'] = new
            if d.get('name') == 'Kid Omega':
                for ab in r.get('abilities', []):
                    for e in ab.get('do', []):
                        if e.get('act') == 'give_ability': e['lasts'] = 'this_round'
            n += json.dumps(r, sort_keys=True) != old
        open(path, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in L))
        print(os.path.basename(path), n, 'changed')


if __name__ == '__main__':
    main()
