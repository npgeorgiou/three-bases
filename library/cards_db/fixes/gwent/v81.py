"""Gwent, 6 Nov 2026 (v81, family 5: "ignoring Armor" dropped, BRIEF Game words: Gwent); safe to run twice.
- A card whose text says "ignoring (its|their|the target unit's|enemy) Armor" and whose rows have no ignore_armor gets
  "ignore_armor": 1 in the params of each damage row (the form Reckless Flurry, Ulula, Professor use)."""
import glob, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'gwent'
PAT = r"(?i)ignor\w+ (its|their|the target unit's|enemy)? ?Armor"


def texts():
    T = {}
    for f in glob.glob(os.path.join(HERE, 'input', G, '*.jsonl')):
        for l in open(f):
            if l.strip(): d = json.loads(l); T[d['id']] = d.get('text', '')
    return T


def main():
    T = texts()
    for path in sorted(glob.glob(os.path.join(HERE, 'read', G, '*.jsonl'))):
        if path.endswith('proposals.jsonl') or 'game_rules' in path or 'keywords' in path: continue
        L = [json.loads(l) for l in open(path) if l.strip()]; n = 0
        for r in L:
            if 'id' not in r or not re.search(PAT, T.get(r['id'], '')) or 'ignore_armor' in json.dumps(r): continue
            for ab in r.get('abilities') or []:
                for a in ab.get('do', []):
                    if a.get('act') == 'damage':
                        a.setdefault('params', {})['ignore_armor'] = 1; n += 1
        if n: open(path, 'w').write(''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n' for r in L))
        print(os.path.basename(path), n, 'changed')


if __name__ == '__main__':
    main()
