"""Gwent, 6 Nov 2026 (v80, family 2: Discard written as act `discard`, BRIEF Game words: Gwent); safe to run twice.
- A card whose text has the word Discard and whose rows hold {"act":"discard"} gets {"act":"keyword_action","keyword":"Discard"}
  there, keeping on, params and link (the form the other cards with Discard use)."""
import glob, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'gwent'


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
            if 'id' not in r or not re.search(r'\bDiscard\b', T.get(r['id'], '')): continue
            for ab in r.get('abilities') or []:
                for i, a in enumerate(ab.get('do', [])):
                    if a.get('act') == 'discard':
                        ab['do'][i] = {'act': 'keyword_action', 'keyword': 'Discard', **{k: v for k, v in a.items() if k != 'act'}}; n += 1
        if n: open(path, 'w').write(''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n' for r in L))
        print(os.path.basename(path), n, 'changed')


if __name__ == '__main__':
    main()
