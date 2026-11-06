"""Gwent, 6 Nov 2026 (v83); safe to run twice.
- Region value: the Gwent faction is spelled Monster in vocab (v72); v78 wrote Monsters. Every region value Monsters becomes Monster.
- Madame Luiza (756863): "Your next Tribute this round costs 0": the cost_set sits in a given ability (waits for the next Tribute used, limit next_time) that lasts this_round."""
import glob, json, os
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def walk(o, fn):
    if isinstance(o, dict):
        fn(o)
        for v in list(o.values()): walk(v, fn)
    elif isinstance(o, list):
        for v in o: walk(v, fn)


def region(d):
    if d.get('attr') == 'region' and d.get('val') == 'Monsters': d['val'] = 'Monster'


def luiza(r):
    ab = r['abilities'][2]
    if ab['do'][0].get('act') != 'cost_set': return
    c = ab['do'][0]; c.pop('lasts', None); c.pop('limit', None)
    when = {"event": "keyword_used", "actor": {"kind": "player", "side": "mine"}, "object": {"with": [{"attr": "keyword", "op": "is", "ref": "Tribute"}]}}
    ab['do'] = [{"act": "give_ability", "on": {"pick": "self"}, "ability": {"when": when, "limit": "next_time", "do": [c]}, "lasts": "this_round"}]


def main():
    for path in sorted(glob.glob(os.path.join(HERE, 'read', 'gwent', '*.jsonl'))):
        if path.endswith('proposals.jsonl') or 'game_rules' in path or 'keywords' in path: continue
        L = [json.loads(l) for l in open(path) if l.strip()]; n = 0
        for r in L:
            if 'abilities' not in r: continue
            before = json.dumps(r, sort_keys=True)
            walk(r, region)
            if r.get('id') == 756863: luiza(r)
            n += before != json.dumps(r, sort_keys=True)
        if n: open(path, 'w').write(''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':')) + '\n' for r in L))
        print(os.path.basename(path), n, 'changed')


if __name__ == '__main__':
    main()
