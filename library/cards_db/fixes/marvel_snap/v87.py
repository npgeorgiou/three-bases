"""Marvel Snap, 9 Nov 2026 (v87, misreading); safe to run twice. Run from library/cards_db.
A card whose text moves it (or another card) "to a location that wins you the game" (Captain Marvel) had lost what the place must be:
the move went to any chosen location (unsure with). Rule over the text: such a move gets the filter "state is winning_lane" on its
target place, and the "with" doubt is removed."""
import glob, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'marvel_snap'
WINS = re.compile(r'(?:to|at|in) (?:a|an|any|the) (?:other )?(?:location|lane)s? that wins? you the game', re.I)
FILT = {'attr': 'state', 'op': 'is', 'val': 'winning_lane'}


def main():
    txt = {}
    for f in glob.glob(os.path.join(HERE, 'input', G, '*.jsonl')):
        for l in open(f):
            x = json.loads(l)
            if 'id' in x: txt[x['id']] = x.get('text') or ''
    for path in sorted(glob.glob(os.path.join(HERE, 'read', G, '*.jsonl'))):
        if path.endswith('proposals.jsonl') or 'game_rules' in path: continue
        L = [json.loads(l) for l in open(path) if l.strip()]; n = 0
        for r in L:
            if not WINS.search(txt.get(r.get('id'), '')): continue
            for a in r.get('abilities', []):
                for d in a.get('do', []):
                    to = d.get('to') or {}
                    if d.get('act') == 'move' and to.get('kind') == 'position':
                        w = to.setdefault('with', [])
                        if FILT not in w: w.append(dict(FILT)); n += 1
            if n and 'unsure' in r:
                r['unsure'] = [u for u in r['unsure'] if u != 'with'] or None
                if r['unsure'] is None: del r['unsure']
        if n: open(path, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in L))
        print(os.path.basename(path), n, 'changed')


if __name__ == '__main__': main()
