"""Marvel Snap, 6 Nov 2026 (v86, position family); safe to run twice. Run from library/cards_db.
1. "Add an Ice Cube to each side of this location" (Luna Snow) was read as the spaces bordering it. Rule over the text: a card whose
   text says "each side" or "both sides" and puts a card at a place with no side gets the game's form for it (Savage Land, Project
   Unicorn): one put on my side of this location and one on the enemy's side.
2. "Give one of your cards at each location +4 Power" (Wolverine Horseman of War) was read as 3 chosen cards anywhere. Rule over the
   text: a card whose text picks cards "at each (other) location" gets position each_lane on every pick of board cards it makes; a
   count of locations as n goes ("one" is one per lane), a number said in the text stays ("2 of your cards at each other location")."""
import glob, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'marvel_snap'
EACH = re.compile(r'(?:cards?|characters?)(?: here)? at each (?:other )?location', re.I)
NUM = re.compile(r'\b(\d+) of your [^.]*? at each (?:other )?location', re.I)
PICKS = ('chosen', 'lowest', 'highest', 'random', 'top', 'highest_cost', 'lowest_cost')


def sides(r):
    n = 0
    for a in r.get('abilities', []):
        out = []
        for d in a.get('do', []):
            to = d.get('to') or {}
            if d.get('act') == 'summon' and to.get('kind') == 'position' and not to.get('side'):
                for i, sd in enumerate(('mine', 'enemy')):
                    e = json.loads(json.dumps(d)); e['to'] = {'kind': 'position', 'side': sd, 'with': [{'attr': 'position', 'op': 'is', 'val': 'same_lane'}]}
                    if i: e['link'] = 'and'
                    out.append(e)
                n += 1
            else: out.append(d)
        a['do'] = out
    return n


def each_lane(r, keep_n):
    n = 0
    for a in r.get('abilities', []):
        for d in a.get('do', []):
            on = d.get('on') or {}
            if on.get('kind') not in ('unit', 'card') or on.get('pick') not in PICKS or on.get('zone') not in (None, 'board'): continue
            w = on.setdefault('with', [])
            if not any(x.get('attr') == 'position' and x.get('val') == 'each_lane' for x in w):
                w.append({'attr': 'position', 'op': 'is', 'val': 'each_lane'}); n += 1
            if 'n' in on and not keep_n: on.pop('n'); n += 1
    return n


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
            t = txt.get(r.get('id'), '')
            if re.search(r'each side|both sides', t, re.I): n += sides(r)
            if EACH.search(t): n += each_lane(r, bool(NUM.search(t)))
        if n: open(path, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in L))
        print(os.path.basename(path), n, 'changed')


if __name__ == '__main__':
    main()
