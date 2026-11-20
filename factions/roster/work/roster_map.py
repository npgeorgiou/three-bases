"""Step 5, the map (factions/START_DESIGN-1-roster.md) -> factions/roster-map.html. Run from library/cards_db after step 6:
python3 ../../factions/roster/work/roster_map.py  (about 20 seconds)
Every usable concept is a dot. Two concepts sit close when real decks hold both more often than chance (a deck holds a
concept when it has DECK_CARDS or more cards with it and its share of them is DECK_SHARE times its game's average;
work/deck_scores.json); the dots are laid out by springs on that closeness; a concept in no group sits beside
the concepts it is closest to (layout()). The groups: concepts that real decks hold together, found by Louvain on that closeness (two concepts held
together LINK_LIFT times chance or more, by MIN_DECKS decks or more); each dot takes its group's colour. Ticking
factions of step 6 (work/kernel_factions.tsv) lights their concepts in the faction's colour (kernel, concepts, extras),
the strong card links between them (roster/concept_links.tsv) and shows its deck style (design markers)."""
import csv, json, math, os
import networkx as nx
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, '..', '..', '..', 'library', 'cards_db')

DECK_SHARE, DECK_CARDS, LINK_LIFT, MIN_DECKS, PLACE_BY = 2, 2, 1.5, 10, 3  # Claude's
COLOURS = ['#d62728', '#ff7f0e', '#9467bd', '#1f77b4', '#17becf', '#8c8c00', '#e377c2', '#2ca02c', '#8c564b', '#393b79',
           '#ad494a', '#e7969c', '#637939', '#7b4173', '#3182bd', '#e6550d', '#31a354', '#756bb1', '#636363', '#bd9e39']
GROUP_COLOURS = ['#4e79a7', '#f28e2b', '#59a14f', '#e15759', '#b07aa1', '#76b7b2', '#edc948', '#9c755f', '#ff9da7', '#bab0ac']


def closeness(D, usable):
    """per pair of usable concepts: how many times chance real decks hold both"""
    cs = [c for c in D['nodes'] if c in usable]; ix = {c: i for i, c in enumerate(cs)}
    M = np.zeros((len(D['decks']), len(cs))); C = np.zeros_like(M)
    for n, d in enumerate(D['decks']):
        counts = d['counts'] if isinstance(d['counts'], dict) else eval(d['counts'])
        tot = sum(counts.values()) or 1
        for c, v in counts.items():
            if c in ix: M[n, ix[c]] = v / tot; C[n, ix[c]] = v
    for g in {d['game'] for d in D['decks']}:
        rows = [n for n, d in enumerate(D['decks']) if d['game'] == g]
        avg = M[rows].mean(0); M[rows] = (M[rows] >= DECK_SHARE * avg) & (avg > 0) & (C[rows] >= DECK_CARDS)
    p = M.mean(0); both = (M.T @ M) / len(M)
    return cs, both / np.maximum(np.outer(p, p), 1e-9), M.T @ M


def groups(cs, lift, n):
    """the groups of concepts real decks hold together (Louvain, seeded), biggest first; each group's concepts by how
    strongly they are held with the rest of it"""
    G = nx.Graph(); G.add_nodes_from(cs)
    for i in range(len(cs)):
        for j in range(i + 1, len(cs)):
            if n[i, j] >= MIN_DECKS and lift[i, j] >= LINK_LIFT: G.add_edge(cs[i], cs[j], weight=math.log2(lift[i, j]))
    found = nx.community.louvain_communities(G.subgraph([c for c in cs if G.degree(c)]), weight='weight', seed=1)
    pull = lambda c, g: sum(G[c][o]['weight'] for o in G[c] if o in g)
    return G, [sorted(g, key=lambda c: (-pull(c, g), c)) for g in sorted(found, key=lambda g: (-len(g), min(g)))]


def layout(cs, G, lift, both, cards, kin):
    """springs on the groups' closeness (seeded, so every run is the same); a concept in no group sits beside the grouped
    concepts it is closest to: real decks holding both (3+ decks, above chance), else real cards linking them, its best
    PLACE_BY, weighted by how strongly, else its parents and children in the concept tree, else the concepts that
    share a parent with it"""
    linked = [c for c in cs if G.degree(c)]; ix = {c: i for i, c in enumerate(cs)}
    P = nx.spring_layout(G.subgraph(linked), weight='weight', seed=7, iterations=500, k=1.2 / math.sqrt(len(linked)))
    xy = np.array([P[c] for c in linked]); lo, hi = xy.min(0), xy.max(0)
    pos = {c: [round(float(40 + 920 * (P[c][0] - lo[0]) / (hi[0] - lo[0])), 1), round(float(40 + 860 * (P[c][1] - lo[1]) / (hi[1] - lo[1])), 1)] for c in linked}
    rest, todo = [], [c for c in cs if not G.degree(c)]
    for n, c in enumerate(todo + todo):  # twice: a concept placed only by its tree kin may need a kin placed first
        if c in pos: continue
        near = sorted(((lift[ix[c], ix[o]], o) for o in linked if both[ix[c], ix[o]] >= 3 and lift[ix[c], ix[o]] > 1), reverse=True)[:PLACE_BY]
        near = near or sorted(((cards.get(frozenset((c, o)), 0), o) for o in linked if cards.get(frozenset((c, o)), 0) > 1), reverse=True)[:PLACE_BY]
        near = near or [(2, o) for o in sorted(kin.get(c, ())) if o in pos]
        near = near or [(2, o) for o in sorted(set().union(*(kin.get(q, set()) for q in kin.get(c, ()))) - {c}) if o in pos]
        if not near:
            if n >= len(todo): rest.append(c)
            continue
        w = sum(math.log2(v) for v, _ in near) or 1
        x = sum(math.log2(v) * pos[o][0] for v, o in near) / w; y = sum(math.log2(v) * pos[o][1] for v, o in near) / w
        a = 2.4 * n  # a small turn per concept so two placed beside the same concepts do not cover each other
        pos[c] = [round(x + 14 * math.cos(a), 1), round(y + 14 * math.sin(a), 1)]
    pos.update({c: [round(40 + 920 * (i + 0.5) / len(rest), 1), 965] for i, c in enumerate(rest)})
    return pos


def main():
    D = json.load(open(os.path.join(HERE, 'deck_scores.json'), encoding='utf-8'))
    usable = {r['concept'] for r in csv.DictReader(open(os.path.join(HERE, 'concepts.tsv'), encoding='utf-8'), delimiter='\t') if r['kind'] == 'usable'}
    names, kin = dict(D['plain']), {}
    for line in open(os.path.join(DB, '..', 'concept_tree.txt'), encoding='utf-8'):
        p = line.split(' | ')
        if len(p) > 3 and not line.startswith('#'):
            names[p[0].strip()] = p[1].strip()
            for q in filter(None, (x.strip() for x in p[3].split(','))):
                kin.setdefault(p[0].strip(), set()).add(q); kin.setdefault(q, set()).add(p[0].strip())
    cs, lift, both = closeness(D, usable)
    G, found = groups(cs, lift, both)
    facs = list(csv.DictReader(open(os.path.join(HERE, 'kernel_factions.tsv'), encoding='utf-8'), delimiter='\t'))
    strong, cards = {}, {}
    for r in csv.DictReader(open(os.path.join(DB, 'roster', 'concept_links.tsv'), encoding='utf-8'), delimiter='\t'):
        cards[frozenset((r['a'], r['b']))] = float(r['cards'] or 0)
        if float(r['cards'] or 0) >= 1.2 and r['a'] in usable and r['b'] in usable and r['a'] != r['b']:
            strong[frozenset((r['a'], r['b']))] = r['texts'].split(' | ')[0] if r['texts'] else ''
    data = {'names': {c: names.get(c, c) for c in cs}, 'pos': layout(cs, G, lift, both, cards, kin), 'colours': COLOURS,
            'groups': found, 'group_colours': GROUP_COLOURS, 'dot': {c: i for i, g in enumerate(found) for c in g},
            'factions': [{'name': f['name'], 'does': f['does'], 'theme': f['theme'], 'kernel': f['kernel'].split(','),
                          'style': [D['markers'][m.split(':')[0]] for m in f['markers'].split(',') if m],
                          'concepts': [c for c in f['concepts'].split(',') if c not in f['kernel'].split(',')],
                          'extras': [c for c in f['extras'].split(',') if c]} for f in facs],
            'links': [[*sorted(p), t] for p, t in strong.items() if all(c in set(cs) for c in p)]}
    tpl = open(os.path.join(HERE, 'roster_map_template.html'), encoding='utf-8').read()
    open(os.path.join(HERE, '..', '..', 'roster-map.html'), 'w', encoding='utf-8').write(tpl.replace('/*DATA*/null', json.dumps(data)))
    print(len(cs), 'concepts,', len(found), 'groups,', len(facs), 'factions,', len(data['links']), 'strong links')


if __name__ == '__main__':
    main()
