"""Marvel Snap, 5 Nov 2026 (v66, step 2.5 second reading); safe to run twice.
- Families 9 and 11 of second/marvel_snap/compare_verdict.md: first readings wrong in what the card does. The second reading
  is taken where it follows the text: Hospice (each Power change here happens once more), Boomerang (4 Power spread randomly),
  Majestic Wingbeat (the -1 Cost is on the same card), Stryfe (uses the On Reveal: repeat, not play), Swarm (two copies of
  itself that cost 0), Marvel Boy (1-Cost cards in any zone). Super-Adaptoid: "steal the text" is copy_text (BRIEF Game words).
- Locations that become a named location (Eternals' Ark floods, Los Diablos Sauce makes Taco Truck): "to" names it, as Magik."""
import glob, json, os
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'marvel_snap'
FROM_SECOND = {796224, 8000063, 8000347, 8000613, 8000626, 8000358}
LANE = {'attr': 'position', 'op': 'is', 'val': 'same_lane'}
SET = {8000619: [{'when': {'event': 'played', 'object': {'pick': 'self'}}, 'do': [{'act': 'copy_text', 'on': {'pick': 'self'},
        'to': {'kind': 'unit', 'side': 'enemy', 'pick': 'chosen', 'zone': 'board',
               'with': [LANE, {'attr': 'keyword', 'op': 'is', 'ref': 'Activate'}]}}]}]}
NAMED_TO = {"Eternals' Ark": 'Flooded', 'Los Diablos Sauce': 'Taco Truck'}


def main():
    second = {json.loads(l)['id']: json.loads(l) for l in open(os.path.join(HERE, 'second', G, 'second_001.jsonl')) if l.strip()}
    names = {}
    for f in glob.glob(os.path.join(HERE, 'input', G, '*.jsonl')):
        for l in open(f):
            x = json.loads(l)
            if 'id' in x: names[x['id']] = x['name']
    for path in sorted(glob.glob(os.path.join(HERE, 'read', G, 'batch_*.jsonl'))):
        if path.endswith('proposals.jsonl'): continue
        L = [json.loads(l) for l in open(path) if l.strip()]; n = 0
        for r in L:
            old = json.dumps(r, sort_keys=True)
            if r['id'] in FROM_SECOND: r['abilities'] = second[r['id']]['abilities']
            if r['id'] in SET: r['abilities'] = SET[r['id']]
            to = NAMED_TO.get(names.get(r['id']))
            for ab in r.get('abilities', []) if to else []:
                for e in ab.get('do', []):
                    if e.get('act') in ('transform', 'set_terrain') and (e.get('on') or {}).get('kind') == 'position':
                        e['act'] = 'set_terrain'; e['to'] = {'kind': 'position', 'with': [{'attr': 'name_has', 'op': 'is', 'ref': to}]}
            n += json.dumps(r, sort_keys=True) != old
        open(path, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in L))
        print(os.path.basename(path), n, 'changed')


if __name__ == '__main__':
    main()
