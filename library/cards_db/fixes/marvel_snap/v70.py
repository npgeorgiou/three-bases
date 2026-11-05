"""Marvel Snap, 5 Nov 2026 (v70, line check C12); safe to run twice.
"Destroy the other locations" (Galactus, Worldship) destroys the cards there: after the kill of the locations the ability also
kills all units on the board in those locations, like Destroyer's "destroy your cards at other locations", so the cards that
wait for deaths (Knull, Death) get their line. Rule over the text: a kill on all positions in a card whose text says destroy ... locations."""
import glob, json, os, re
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
            if not re.search(r'destroy (all |the )?(your )?other locations', ((inp.get(r['id']) or {}).get('text') or ''), re.I): continue
            for a in r.get('abilities', []):
                do = a.get('do') or []
                for i, e in enumerate(do):
                    if e.get('act') == 'kill' and (e.get('on') or {}).get('kind') == 'position' and e['on'].get('pick') == 'all':
                        if any(d.get('act') == 'kill' and (d.get('on') or {}).get('kind') == 'unit' for d in do): continue
                        on = {'kind': 'unit', 'side': 'any', 'pick': 'all', 'zone': 'board', 'with': e['on'].get('with', [])}
                        do.insert(i + 1, {'act': 'kill', 'on': on}); n += 1; break
        if n: open(path, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in L))
        print(os.path.basename(path), n, 'changed')


if __name__ == '__main__':
    main()
