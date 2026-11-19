"""The faction archetypes of step 3 (the 25 NMF groups Kaptain agreed, deck_groups_nmf_25.json) as rows for steps 5 and 6:
an archetype's concepts as deck_groups_nmf.py made them; one row per part, each concept a part of its own (Claude's); the kind (engine or brick) is set by step 5
(archetype_map.py), which writes the rows with their kind to work/archetype_parts.tsv for step 6 (factions.py).
markers(): per archetype its design markers, each with how many times as often its decks have it."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'deck_groups_nmf_25.json'), encoding='utf-8'))


def concepts():
    """archetype key -> its concepts (deck_groups_nmf.py makes them: heaviest and base, without the unit measures and the
    concepts more than half of the groups hold)"""
    return {g['key']: g['archetype'] for g in D['groups']}


def rows():
    out = []
    for g in D['groups']:
        cs = concepts()[g['key']]
        name = ' + '.join(D['plain'][c] for c in cs[:2])
        for c in cs:
            out.append({'key': g['key'], 'name': name, 'in_this_game': '', 'part': D['plain'][c], 'kind': '', 'concepts': c})
    return out


def markers():
    return {g['key']: g['markers'] for g in D['groups']}
