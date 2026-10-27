"""Compares two independent readings of the same cards. A card agrees when both readings give the same set of
(event, conditions' tests, act, target kind/side/pick, numbers) per ability, ignoring order and key spelling.
Usage: compare.py <first.jsonl> <second.jsonl> <input.jsonl>   prints agreement and each differing card with both readings."""
import json, sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
from show import render

def nums(x, out):
    if isinstance(x, bool): return
    if isinstance(x, (int, float)): out.append(x)
    elif isinstance(x, dict): [nums(v, out) for v in x.values()]
    elif isinstance(x, list): [nums(v, out) for v in x]

def key(rec):
    abil = []
    for ab in rec.get('abilities', []):
        w = ab.get('when', {})
        tests = tuple(sorted(c.get('test', '') for c in ab.get('if', [])))
        effs = []
        for e in ab.get('do', []):
            t = e.get('on') or {}
            n = []; nums(e.get('params'), n)
            effs.append((e.get('act'), t.get('kind'), t.get('side'), t.get('pick'), e.get('card'), e.get('keyword'), tuple(sorted(n))))
        abil.append((w.get('event'), tests, tuple(sorted(effs, key=str))))
    return sorted(abil, key=str)

if __name__ == '__main__':
    A = {json.loads(l)['id']: json.loads(l) for l in open(sys.argv[1]) if l.strip()}
    B = {json.loads(l)['id']: json.loads(l) for l in open(sys.argv[2]) if l.strip()}
    inp = {json.loads(l)['id']: json.loads(l) for l in open(sys.argv[3])}
    both = [i for i in B if i in A]; diff = [i for i in both if key(A[i]) != key(B[i])]
    print(f'{len(both)} cards read twice, {len(both) - len(diff)} agree, {len(diff)} differ')
    for i in diff:
        x = inp.get(i, {'name': '?', 'text': ''})
        print(f"\n## {x['name']} {i}\n  TEXT: {x['text']}\n  FIRST:\n{render(A[i])}\n  SECOND:\n{render(B[i])}")
