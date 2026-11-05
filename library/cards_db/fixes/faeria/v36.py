"""All games, 5 Nov 2026 (v36), by rule; safe to run twice.
- A named card made for the opponent ("your opponent gets a Chimichanga", "add 2 Sentinel to your opponent's hand", "Fill your
  opponent's hand with Ruby Fish"): the create gets on kind card, side enemy (normalize N35, Korg's form). normalize N1 dropped
  the receiving player with its side, so these cards gave the card to me (Munchineworld, Black Widow, Master Mold; Faeria
  Rapala, the Dopefish). Only in the sentence that names the card (Nautilus' Riptide places a unit into the enemy
  deck but creates Nautilus in mine)."""
import glob, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MAKE = re.compile(r'\b(?:add|gets?|fill|shuffle|create)\b', re.I)
TO_ENEMY = re.compile(r"opponent gets|(?:to|into|fill) (?:your|the) (?:opponent|enemy)'?s? (?:hand|deck)", re.I)


def main():
    for g in sorted(os.listdir(os.path.join(HERE, 'read'))):
        inp = {}
        for f in glob.glob(os.path.join(HERE, 'input', g, '*.jsonl')):
            for l in open(f):
                x = json.loads(l)
                if 'id' in x: inp[x['id']] = x
        for path in sorted(glob.glob(os.path.join(HERE, 'read', g, 'batch_*.jsonl'))):
            if path.endswith('proposals.jsonl'): continue
            L = [json.loads(l) for l in open(path) if l.strip()]; n = 0
            for r in L:
                text = (inp.get(r['id']) or {}).get('text') or ''
                for ab in r.get('abilities', []):
                    for e in ab.get('do', []):
                        said = [x for x in re.split(r'(?<=[.!?])\s+', text) if e.get('card') and e['card'] in x and MAKE.search(x)]  # the sentence making it
                        if e.get('act') == 'create' and any(TO_ENEMY.search(x) for x in said) and 'on' not in e and 'to' not in e:
                            e['on'] = {'kind': 'card', 'side': 'enemy'}; n += 1
            if n:
                open(path, 'w').write(''.join(json.dumps(r, separators=(',', ':')) + '\n' for r in L))
                print(g, os.path.basename(path), n, 'changed')


if __name__ == '__main__':
    main()
