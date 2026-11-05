"""Marvel Snap, 5 Nov 2026 (v69, line check C5); safe to run twice.
A card whose text starts "Activate:" has its own Activate ability: its "when activated" is that card being activated, so the
when gets object pick self (Magus, Sparky, Zombie Captain Marvel), like Awesome Andy. Without it other Activate cards looked
like makers of its trigger (Arana -> Magus)."""
import glob, json, os
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'marvel_snap'


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
            if not ((inp.get(r['id']) or {}).get('text') or '').startswith('Activate:'): continue
            for a in r.get('abilities', []):
                w = a.get('when') or {}
                if w.get('event') == 'activated' and not w.get('object') and not w.get('actor'):
                    w['object'] = {'pick': 'self'}; n += 1
        if n: open(path, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in L))
        print(os.path.basename(path), n, 'changed')


if __name__ == '__main__':
    main()
