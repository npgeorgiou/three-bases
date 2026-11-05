"""Marvel Snap, 5 Nov 2026 (v68, line check); safe to run twice.
Discarded and destroyed cards lie in two piles: a target in zone discard is zone discarded when the text speaks of discarding
and never of destroying (Hela, Ghost Rider, Khonshu, Sanctum Infinitum), zone discarded_or_dead when it speaks of both (Firelord,
Night Nurse); a text about destroyed cards keeps zone discard (Phoenix Force, Elixir)."""
import glob, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'marvel_snap'


def rezone(x, z):
    if isinstance(x, dict):
        if x.get('zone') == 'discard' and ('kind' in x or 'pick' in x): x['zone'] = z
        for v in x.values(): rezone(v, z)
    elif isinstance(x, list):
        for v in x: rezone(v, z)


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
            text = (inp.get(r['id']) or {}).get('text') or ''; old = json.dumps(r, sort_keys=True)
            dis, des = re.search(r'\bdiscard', text, re.I), re.search(r'\bdestroy', text, re.I)
            if dis: rezone(r.get('abilities', []), 'discarded_or_dead' if des else 'discarded')
            n += json.dumps(r, sort_keys=True) != old
        if n: open(path, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in L))
        print(os.path.basename(path), n, 'changed')


if __name__ == '__main__':
    main()
