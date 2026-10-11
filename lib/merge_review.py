"""Merge a review notes file (lines 'Name: +concept +concept:ben -concept') into a review JSON. Usage: merge_review.py notes.txt review.json"""
import json, sys, os
notes, out = sys.argv[1], sys.argv[2]
d = json.load(open(out)) if os.path.exists(out) else {}
d = {k: {'add': list(v.get('add', [])), 'drop': list(v.get('drop', []))} for k, v in d.items()}
ROLE = {'ben': 'benefits', 'cou': 'counters', 'cos': 'cost', 'cost': 'cost', 'gra': 'grants', 'grants': 'grants'}
for line in open(notes, encoding='utf-8'):
    line = line.rstrip('\n')
    if ': ' not in line: continue
    name, rest = line.rsplit(': ', 1)
    r = d.setdefault(name, {'add': [], 'drop': []})
    for tok in rest.split():
        sign, item = tok[0], tok[1:]
        if ':' in item: con, ro = item.split(':'); item = con + ':' + ROLE[ro]
        if sign == '+':
            if item not in r['add']: r['add'].append(item)
            if item in r['drop']: r['drop'].remove(item)
        else:
            r['add'] = [a for a in r['add'] if a != item and a.split(':')[0] != item]
            if item not in r['drop']: r['drop'].append(item)
json.dump(d, open(out, 'w'), indent=0, ensure_ascii=False)
print('entries', len(d))
