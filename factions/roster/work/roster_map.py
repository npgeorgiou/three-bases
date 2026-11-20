"""Step 5, the map (factions/START_DESIGN-1-roster.md) -> factions/roster-map.html. Run from library/cards_db after step 6:
python3 ../../factions/roster/work/roster_map.py  (about 20 seconds)
Every usable concept is a dot. Two concepts sit close when real decks hold both more often than chance (a deck holds a
concept when its share of cards with it is DECK_SHARE times its game's average; work/deck_scores.json); the dots are
laid out by springs (that closeness pulls, every pair pushes alike), so the gaps are even. Each faction of step 6
(work/kernel_factions.tsv) has a colour: a dot takes the colour of the faction whose kernel holds it. Ticking factions
lights their concepts (kernel, concepts, extras) and the strong card links between them (roster/concept_links.tsv)."""
import csv, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, '..', '..', '..', 'library', 'cards_db')

DECK_SHARE, ROUNDS = 2, 600  # Claude's
COLOURS = ['#d62728', '#ff7f0e', '#9467bd', '#1f77b4', '#17becf', '#8c8c00', '#e377c2', '#2ca02c', '#8c564b', '#393b79',
           '#ad494a', '#e7969c', '#637939', '#7b4173', '#3182bd', '#e6550d', '#31a354', '#756bb1', '#636363', '#bd9e39']


def closeness(D, usable):
    """per pair of usable concepts: how many times chance real decks hold both"""
    cs = [c for c in D['nodes'] if c in usable]; ix = {c: i for i, c in enumerate(cs)}
    M = np.zeros((len(D['decks']), len(cs)))
    for n, d in enumerate(D['decks']):
        tot = sum(d['counts'].values()) or 1
        for c, v in d['counts'].items():
            if c in ix: M[n, ix[c]] = v / tot
    for g in {d['game'] for d in D['decks']}:
        rows = [n for n, d in enumerate(D['decks']) if d['game'] == g]
        avg = M[rows].mean(0); M[rows] = (M[rows] >= DECK_SHARE * avg) & (avg > 0)
    p = M.mean(0); both = (M.T @ M) / len(M)
    return cs, both / np.maximum(np.outer(p, p), 1e-9)


def layout(cs, lift):
    """springs: closeness (log of times chance, 0 to 1) pulls, every pair pushes alike; seeded, so every run is the same"""
    n = len(cs); W = np.clip(np.log2(np.maximum(lift, 1)) / 3, 0, 1); np.fill_diagonal(W, 0)
    rng = np.random.default_rng(7); P = rng.random((n, 2)); k = 1 / math.sqrt(n); t = 0.1
    for r in range(ROUNDS):
        d = P[:, None] - P[None]; dist = np.sqrt((d ** 2).sum(-1)) + 1e-9
        push = (k * k / dist ** 2)[..., None] * d; pull = (W * dist / k)[..., None] * d
        move = (push - pull).sum(1); step = np.sqrt((move ** 2).sum(1)) + 1e-9
        P += move / step[:, None] * np.minimum(step, t)[:, None]; t *= 0.995
    lo, hi = P.min(0), P.max(0)
    return {c: [round(float(40 + 920 * (P[i, 0] - lo[0]) / (hi[0] - lo[0])), 1), round(float(40 + 920 * (P[i, 1] - lo[1]) / (hi[1] - lo[1])), 1)]
            for i, c in enumerate(cs)}


def main():
    D = json.load(open(os.path.join(HERE, 'deck_scores.json'), encoding='utf-8'))
    usable = {r['concept'] for r in csv.DictReader(open(os.path.join(HERE, 'concepts.tsv'), encoding='utf-8'), delimiter='\t') if r['kind'] == 'usable'}
    names = dict(D['plain'])
    for line in open(os.path.join(DB, '..', 'concept_tree.txt'), encoding='utf-8'):
        p = line.split(' | ')
        if len(p) > 2 and not line.startswith('#'): names[p[0].strip()] = p[1].strip()
    cs, lift = closeness(D, usable)
    facs = list(csv.DictReader(open(os.path.join(HERE, 'kernel_factions.tsv'), encoding='utf-8'), delimiter='\t'))
    colour = {}
    for i, f in enumerate(facs):
        for c in f['kernel'].split(','): colour.setdefault(c, i)
    strong = {}
    for r in csv.DictReader(open(os.path.join(DB, 'roster', 'concept_links.tsv'), encoding='utf-8'), delimiter='\t'):
        if float(r['cards'] or 0) >= 1.2 and r['a'] in usable and r['b'] in usable and r['a'] != r['b']:
            strong[frozenset((r['a'], r['b']))] = r['texts'].split(' | ')[0] if r['texts'] else ''
    data = {'names': {c: names.get(c, c) for c in cs}, 'pos': layout(cs, lift), 'colours': COLOURS,
            'dot': {c: colour[c] for c in cs if c in colour},
            'factions': [{'name': f['name'], 'does': f['does'], 'theme': f['theme'], 'kernel': f['kernel'].split(','),
                          'concepts': [c for c in f['concepts'].split(',') if c not in f['kernel'].split(',')],
                          'extras': [c for c in f['extras'].split(',') if c]} for f in facs],
            'links': [[*sorted(p), t] for p, t in strong.items() if all(c in set(cs) for c in p)]}
    tpl = open(os.path.join(HERE, 'roster_map_template.html'), encoding='utf-8').read()
    open(os.path.join(HERE, '..', '..', 'roster-map.html'), 'w', encoding='utf-8').write(tpl.replace('/*DATA*/null', json.dumps(data)))
    print(len(cs), 'concepts,', len(facs), 'factions,', len(data['links']), 'strong links')


if __name__ == '__main__':
    main()
