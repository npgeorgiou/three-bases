"""Marvel Snap, 5 Nov 2026 (v71, line check C99); safe to run twice.
"3 of your cards have stolen Power" (Vampire Deacon Frost) counts cards that took Power from others, not any buffed card.
Rule over the text: a filter state buffed in a card whose text says "stolen Power" becomes state stolen_power."""
import glob, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'marvel_snap'


def fix(o):
    n = 0
    if isinstance(o, dict):
        if o.get('attr') == 'state' and o.get('val') == 'buffed': o['val'] = 'stolen_power'; n += 1
        for v in o.values(): n += fix(v)
    elif isinstance(o, list):
        for v in o: n += fix(v)
    return n


def main():
    inp = {}
    for f in glob.glob(os.path.join(HERE, 'input', G, '*.jsonl')):
        for l in open(f):
            x = json.loads(l)
            if 'id' in x: inp[x['id']] = x
    for path in sorted(glob.glob(os.path.join(HERE, 'read', G, '*.jsonl'))):
        if path.endswith('proposals.jsonl') or 'game_rules' in path: continue
        L = [json.loads(l) for l in open(path) if l.strip()]; n = 0
        for r in L:
            if 'id' in r and re.search(r'stolen Power', ((inp.get(r['id']) or {}).get('text') or ''), re.I): n += fix(r.get('abilities', []))
        if n: open(path, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in L))
        print(os.path.basename(path), n, 'changed')


if __name__ == '__main__':
    main()
