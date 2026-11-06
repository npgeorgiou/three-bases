"""Gwent, 6 Nov 2026 (v77, growing numbers "[N]" in one form, BRIEF Game words: Gwent); safe to run twice.
- "[N]" on a card with Patience and no "Increase this value" is the card's Patience value: {"x": "stat", "attr":
  "keyword_amount", "of": self} (the form most Patience cards already use).
- "[N]. Increase this value by M for each ..." is the start number N plus the count: an unstated item of that sum becomes N
  (dropped when N is 0, so only the count is left)."""
import glob, json, os, re
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
G = 'gwent'
UN = {'x': 'unstated'}
PATIENCE = {'x': 'stat', 'attr': 'keyword_amount', 'of': {'pick': 'self'}}


def texts():
    T = {}
    for f in glob.glob(os.path.join(HERE, 'input', G, '*.jsonl')):
        for l in open(f):
            if l.strip(): d = json.loads(l); T[d['id']] = d.get('text', '')
    return T


def fix(o, start, patience):
    n = 0
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if v == UN and patience: o[k] = dict(PATIENCE); n += 1
            elif isinstance(v, dict) and v.get('x') == 'sum' and UN in v.get('items', []) and start is not None:
                items = [i for i in v['items'] if i != UN] + ([start] if start else [])
                o[k] = items[0] if len(items) == 1 else dict(v, items=items); n += 1
            else: n += fix(v, start, patience)
    elif isinstance(o, list):
        for v in o: n += fix(v, start, patience)
    return n


def main():
    T = texts()
    for path in sorted(glob.glob(os.path.join(HERE, 'read', G, '*.jsonl'))):
        if path.endswith('proposals.jsonl') or 'game_rules' in path or 'keywords' in path: continue
        L = [json.loads(l) for l in open(path) if l.strip()]; n = 0
        for r in L:
            t = T.get(r.get('id'), '')
            m = re.search(r'\[(\d+)\]', t)
            if not m: continue
            grows = re.search(r'[Ii]ncrease this value by', t)
            start = int(m.group(1)) if grows else None
            patience = bool(re.search(r'\bPatience\b', t)) and not grows
            k = fix(r.get('abilities', []), start, patience)
            if k:
                n += k
                if not json.dumps(r).count('"unstated"') - json.dumps(r).count('"lasts": "unstated"'):
                    r['unsure'] = [u for u in r.get('unsure', []) if u != 'x']
                    if not r['unsure']: r.pop('unsure')
        if n: open(path, 'w').write(''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n' for r in L))
        print(os.path.basename(path), n, 'changed')


if __name__ == '__main__':
    main()
