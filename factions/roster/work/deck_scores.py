"""Step 3 (START_DESIGN-1-roster.md): every real deck's scores, read by step 6 (kernel_factions.py) and make_faction.py.
Run from library/cards_db: python3 ../../factions/roster/work/deck_scores.py  (a few seconds) -> factions/roster/work/deck_scores.json
1. Concepts: the usable concepts of concepts.tsv (a card counts each once; a parent only on cards none of its children
   carry), plus five unit concepts against the card's game: unit, cheap unit, expensive unit (concept_tags.py), strong for its
   cost and tough for its cost (above the game's straight line of strength or defence by cost).
2. Scores: every deck of decks.tsv (all its cards) and every real faction (Monster Train's clans left out, NOT_FACTIONS),
   per concept: its cards with the concept, and the log-odds ratio with a prior (Monroe et al. 2008) against all the
   cards of its game, as a z-score; STRONG or more: the deck is built on the concept.
3. Design markers: per deck, whether it is in the top or bottom quarter of its game's decks on each number (MARKERS)."""
import collections, csv, json, os, sqlite3, sys
import numpy as np
sys.path.insert(0, os.getcwd())
import concept_tags, deck_analysis, faction_asks

HERE = os.path.dirname(os.path.abspath(__file__))
PRIOR = 100.0       # the prior's size in concept instances (Claude's)
STRONG = 1.96       # a deck leans on a concept above this score
NOT_FACTIONS = ('monster_train',)  # Kaptain, 9 Nov 2026: a different kind of game, its clans are not measured
FIT, BEST = 2.0, 2  # a faction fits its best 2 groups at twice its game's average share (Claude's)
UNIT = {'unit*': 'Unit', 'cheapunit*': 'Cheap unit', 'dearunit*': 'Expensive unit',
        'strongcost*': 'Strong for its cost', 'toughcost*': 'Tough for its cost'}

c = sqlite3.connect('cards.sqlite')
games = sorted({g for (g,) in c.execute('select distinct game from card')})
x = faction_asks.Ctx(c, games, None, {})
con, pools, stats = concept_tags.tag(c, x, games)
usable = [r['concept'] for r in csv.DictReader(open(os.path.join(HERE, 'concepts.tsv'), encoding='utf-8'), delimiter='\t')
          if r['kind'] == 'usable']
kids, plain = collections.defaultdict(set), dict(UNIT)
for line in open('../concept_tree.txt', encoding='utf-8'):
    p = [t.strip() for t in line.split('|')]
    if line.startswith('#') or len(p) < 2: continue
    plain[p[0]] = p[1]
    if len(p) > 3:
        for par in filter(None, p[3].split(',')): kids[par.strip()].add(p[0])
def below(k, seen=None):
    seen = set() if seen is None else seen
    for q in kids[k] - seen: seen.add(q); below(q, seen)
    return seen
sub = {k: below(k) for k in usable}
sub.update({k: set() for k in UNIT})
nodes = usable + list(UNIT)
col = {k: j for j, k in enumerate(nodes)}
for g in games:  # strong / tough for its cost: above the game's straight line of strength (defence) by cost
    us = [i for i in pools[g] if stats[i][0] in concept_tags.UNIT_CATS and stats[i][1] is not None]
    for i in us: con[i].add('unit*')
    for pos, key in ((2, 'strongcost*'), (3, 'toughcost*')):
        pts = [(stats[i][1], stats[i][pos], i) for i in us if stats[i][pos] is not None]
        if len(pts) < 10: continue
        a, b = np.polyfit([p[0] for p in pts], [p[1] for p in pts], 1)
        for cost, v, i in pts:
            if v > a * cost + b: con[i].add(key)
def vec(i):
    v = np.zeros(len(nodes))
    for k in con.get(i, ()):
        if k in col and not con[i] & sub[k]: v[col[k]] = 1
    return v
cv = {i: vec(i) for g in games for i in pools[g]}
game_tot = {g: sum((cv[i] for i in pools[g]), np.zeros(len(nodes))) for g in games}

def score(counts, g):
    """Monroe et al. 2008: log-odds of each concept in this set against the game's cards, prior from the game's mix, as z"""
    bg = game_tot[g]; a = PRIOR * bg / bg.sum(); a0 = PRIOR
    y, n = counts, counts.sum()
    ok = a > 0
    z = np.zeros(len(nodes))
    li = np.log((y + a)[ok] / (n + a0 - y - a)[ok])
    lj = np.log((bg + a)[ok] / (bg.sum() + a0 - bg - a)[ok])
    z[ok] = (li - lj) / np.sqrt(1 / (y + a)[ok] + 1 / (bg + a)[ok])
    return z

decks, missing = [], collections.Counter()
with open('decks.tsv', encoding='utf-8') as f:
    next(f)
    for line in f:
        p = line.rstrip('\n').split('\t')
        if len(p) < 4 or p[0] not in pools: continue
        ids, bad = deck_analysis.parse_deck(c, p[0], p[3])
        missing[p[0]] += len(bad)
        ids = set(ids) & set(pools[p[0]])
        if ids:
            cnt = sum(cv[i] for i in ids)
            decks.append({'game': p[0], 'name': p[1], 'size': len(ids), 'counts': cnt, 'z': score(cnt, p[0]), 'ids': ids})
facs = sorted({(g, fa) for g in games if g not in NOT_FACTIONS for fa in x.factions(g)})
fcount = {(g, fa): sum((cv[i] for i, v in pools[g].items() if fa in v[3]), np.zeros(len(nodes))) for g, fa in facs}

per_game = collections.Counter(d['game'] for d in decks)
Z = np.array([d['z'] for d in decks])
HAS = np.array([d['counts'] > 0 for d in decks])
gname = np.array([d['game'] for d in decks])
ghas = {g: HAS[gname == g].mean(0) for g in per_game}
effects = collections.Counter(card for (card,) in c.execute('select card from ability'))
summons = {card for (card,) in c.execute("select distinct card from flat_concept where concept='summon'")}
def avg(v): return sum(v) / len(v) if v else None
lines = {}
for g in games:
    us = [i for i in pools[g] if stats[i][0] in concept_tags.UNIT_CATS and stats[i][1] is not None]
    for pos in (2, 3):
        pts = [(stats[i][1], stats[i][pos]) for i in us if stats[i][pos] is not None]
        lines[(g, pos)] = np.polyfit([q[0] for q in pts], [q[1] for q in pts], 1) if len(pts) >= 10 else None
def above(i, pos):
    g = cards_game[i]; ab = lines.get((g, pos))
    return None if ab is None or stats[i][pos] is None or stats[i][1] is None else stats[i][pos] - (ab[0] * stats[i][1] + ab[1])
cards_game = {i: g for g in games for i in pools[g]}
def numbers(d):
    """per deck: the numbers its markers come from (None when the deck has none of the cards a number needs)"""
    ids = d['ids']; cat = lambda i: stats[i][0]
    un = [i for i in ids if cat(i) in concept_tags.UNIT_CATS]; sp = [i for i in ids if cat(i) == 'spell']
    cost = lambda xs: avg([stats[i][1] for i in xs if stats[i][1] is not None])
    lean = [stats[i][2] - stats[i][3] for i in un if stats[i][2] is not None and stats[i][3] is not None]
    return {'units': len(un) / len(ids), 'spells': len(sp) / len(ids),
            'buildings': sum(1 for i in ids if cat(i) in ('building', 'terrain', 'item', 'relic')) / len(ids),
            'curve': cost(ids), 'unitcost': cost(un), 'spellcost': cost(sp) if len(sp) >= 3 else None, 'unitcount': len(un),
            'strong': avg([v for v in (above(i, 2) for i in un) if v is not None]),
            'tough': avg([v for v in (above(i, 3) for i in un) if v is not None]),
            'lean': avg(lean), 'text': avg([effects[i] for i in ids]),
            'summoned': sum(1 for i in ids if i in summons) / len(un) if un else None}
MARKERS = [  # (key, name, number, end): 'high' = top quarter of its game's decks, 'low' = bottom quarter
    ('many_units', 'Many units', 'units', 'high'), ('many_spells', 'Many spells', 'spells', 'high'),
    ('buildings', 'Many buildings (stay in play, never move)', 'buildings', 'high'),
    ('low_curve', 'Low curve', 'curve', 'low'), ('high_curve', 'High curve', 'curve', 'high'),
    ('cheap_units', 'Cheap units', 'unitcost', 'low'), ('expensive_units', 'Expensive units', 'unitcost', 'high'),
    ('cheap_spells', 'Cheap spells', 'spellcost', 'low'), ('expensive_spells', 'Expensive spells', 'spellcost', 'high'),
    ('few_big', 'Few big units', ('unitcount', 'unitcost'), ('low', 'high')),
    ('many_small', 'Many small units', ('unitcount', 'unitcost'), ('high', 'low')),
    ('strong', 'Strong for its cost', 'strong', 'high'), ('weak', 'Weak for its cost', 'strong', 'low'),
    ('tough', 'Tough for its cost', 'tough', 'high'), ('fragile', 'Fragile for its cost', 'tough', 'low'),
    ('hits', 'Hits more than it lasts', 'lean', 'high'), ('lasts', 'Lasts more than it hits', 'lean', 'low'),
    ('plain', 'Plain cards (little text)', 'text', 'low'), ('busy', 'Busy cards (several effects each)', 'text', 'high'),
    ('summoned', 'Mostly summoned units', 'summoned', 'high'), ('played', 'Mostly units played from hand', 'summoned', 'low')]
MARK_FIT = 2.0
nums = [numbers(d) for d in decks]
cut = {}
for g in per_game:
    for k in nums[0]:
        vs = sorted(nums[n][k] for n in range(len(decks)) if decks[n]['game'] == g and nums[n][k] is not None)
        if len(vs) >= 8 and vs[len(vs) // 4] != vs[-1 - len(vs) // 4]: cut[(g, k)] = (vs[len(vs) // 4], vs[-1 - len(vs) // 4])
def has(n, num, end):
    if isinstance(num, tuple): return all(has(n, a, b) for a, b in zip(num, end))
    g, v = decks[n]['game'], nums[n][num]
    if v is None or (g, num) not in cut: return None
    lo, hi = cut[(g, num)]
    return v < lo if end == 'low' else v > hi
HASM = {m[0]: [has(n, m[2], m[3]) for n in range(len(decks))] for m in MARKERS}
json.dump({'markers': {m[0]: m[1] for m in MARKERS}, 'mark_fit': MARK_FIT, 'nodes': nodes, 'plain': {k: plain.get(k, k) for k in nodes},
           'unit': list(UNIT), 'strong': STRONG,
           'decks': [{'game': d['game'], 'name': d['name'], 'size': d['size'],
                      'counts': {nodes[t]: int(v) for t, v in enumerate(d['counts']) if v},
                      'z': {nodes[t]: round(float(v), 2) for t, v in enumerate(d['z']) if v > STRONG},
                      'marks': {k: int(v[n]) for k, v in HASM.items() if v[n] is not None}} for n, d in enumerate(decks)],
           'factions': [{'game': g, 'faction': fa, 'counts': {nodes[t]: int(v) for t, v in enumerate(fcount[(g, fa)]) if v}} for g, fa in facs],
           'game_counts': {g: {nodes[t]: int(v) for t, v in enumerate(game_tot[g]) if v} for g in game_tot}},
          open(os.path.join(HERE, 'deck_scores.json'), 'w', encoding='utf-8'))
print(len(decks), 'decks; unknown deck card names', sum(missing.values()))
