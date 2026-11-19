"""The faction archetypes of step 3 (the 25 NMF groups Kaptain agreed, deck_groups_nmf_25.json) as rows for steps 5 and 6:
one row per part, each concept of a group a part of its own (Claude's); the kind (engine or brick) is set by step 5
(archetype_map.py), which writes the rows with their kind to work/archetype_parts.tsv for step 6 (factions.py)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))


def rows():
    D = json.load(open(os.path.join(HERE, 'deck_groups_nmf_25.json'), encoding='utf-8'))
    out = []
    for g in D['groups']:
        name = ' + '.join(D['plain'][c] for c in g['concepts'][:2])
        for c in g['concepts']:
            out.append({'key': g['key'], 'name': name, 'in_this_game': '', 'part': D['plain'][c], 'kind': '', 'concepts': c})
    return out
