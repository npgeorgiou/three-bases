# Writes wheel/archetypes.md: archetypes.tsv in plain words, each concept by its name in library/concept_tree.txt.
import csv, os
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(here, '..', '..', '..')
names = {}
for line in open(os.path.join(root, 'library', 'concept_tree.txt')):
    p = line.split(' | ')
    if len(p) > 2 and not line.startswith('#'): names[p[0].strip()] = p[1].strip()
rows = list(csv.DictReader(open(os.path.join(here, '..', 'archetypes.tsv')), delimiter='\t'))
out = ['# The archetypes in this game (made from archetypes.tsv by work/archetypes_plain.py; all Claude\'s)', '',
       'Engine: a part that works by feeding another part of the same archetype. Brick: a part that works alone.', '']
last = None
for r in rows:
    if r['key'] != last:
        last = r['key']
        out += ['## ' + r['name'], r['in_this_game'][0].upper() + r['in_this_game'][1:] + '.', '']
    out.append('- **' + r['part'] + '** (' + r['kind'] + '): ' + '; '.join(names.get(c, c) for c in r['concepts'].split(',')) + '.')
    nxt = rows.index(r) + 1
    if nxt == len(rows) or rows[nxt]['key'] != r['key']: out.append('')
open(os.path.join(here, '..', 'archetypes.md'), 'w').write('\n'.join(out))
