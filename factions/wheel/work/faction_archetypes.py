"""Step 3 (START_DESIGN-1-wheel.md): the ways to play that decks put together; they become our factions' archetypes.
Run from library/cards_db: python3 ../../factions/wheel/work/faction_archetypes.py
 -> factions/wheel/work/faction_archetypes.tsv (one row per group) and faction_archetypes.md (the same in plain words).
1. Counts: every deck of decks.tsv, all its cards: how many of them have each usable concept (concepts.tsv; a card counts
   once per concept, a parent only on cards none of its children carry), plus five unit concepts against the card's game:
   unit, cheap unit, expensive unit (axes.py), strong for its cost and tough for its cost (above the game's line of
   strength or defence by cost).
2. Lines: for every two concepts, how much more often they are together in the same decks than chance gives within each
   game (chance from how common each is in the game's decks and the deck's size); each game weighs the square root of its
   deck count. A line is kept when it is above chance by more than BEYOND (Pearson residual).
3. Groups: link clustering (Ahn, Bagrow and Lehmann, Nature 2010) groups the lines, so a concept can be in several
   groups; the tree of lines is cut where the groups are densest (partition density). Groups of 3+ concepts are shown.
4. Decks and factions are measured against each group: the share of their cards' concepts on the group's concepts,
   against their game's average share; they fit the group at FIT times the average or more."""
import collections, csv, os, sqlite3, sys
import numpy as np
sys.path.insert(0, os.getcwd())
import axes, deck_analysis, faction_asks

HERE = os.path.dirname(os.path.abspath(__file__))
BEYOND = 1.96  # a line is kept when it is above chance by more than this (Claude's)
FIT = 1.5      # a deck or faction fits a group at 1.5 times its game's average share or more (Claude's)
TOP = 8
UNIT = {'unit*': 'Unit', 'cheapunit*': 'Cheap unit', 'dearunit*': 'Expensive unit',
        'strongcost*': 'Strong for its cost', 'toughcost*': 'Tough for its cost'}

c = sqlite3.connect('cards.sqlite')
games = sorted({g for (g,) in c.execute('select distinct game from card')})
x = faction_asks.Ctx(c, games, None, {})
con, pools, stats = axes.tag(c, x, games)

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
nodes = usable + list(UNIT)
col = {k: j for j, k in enumerate(nodes)}

for g in games:  # strong / tough for its cost: above the game's straight line of strength (defence) by cost
    us = [i for i in pools[g] if stats[i][0] in axes.UNIT_CATS and stats[i][1] is not None]
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
        if k in col and (k in UNIT or not con[i] & sub[k]): v[col[k]] = 1
    return v
cv = {i: vec(i) for g in games for i in pools[g]}

decks, missing = [], collections.Counter()
with open('decks.tsv', encoding='utf-8') as f:
    next(f)
    for line in f:
        p = line.rstrip('\n').split('\t')
        if len(p) < 4 or p[0] not in pools: continue
        ids, bad = deck_analysis.parse_deck(c, p[0], p[3])
        missing[p[0]] += len(bad)
        ids = set(ids) & set(pools[p[0]])
        if ids: decks.append((p[0], p[1], sum(cv[i] for i in ids), len(ids)))
per_game = collections.Counter(d[0] for d in decks)

O = np.zeros((len(nodes), len(nodes))); E = np.zeros_like(O)
for g in per_game:
    ds = [d for d in decks if d[0] == g]
    u = np.sqrt(len(ds)) / len(ds)
    C = np.array([d[2] for d in ds]); n = np.array([d[3] for d in ds], float)
    pg = C.sum(0) / n.sum()
    O += u * C.T @ C
    E += u * (n ** 2).sum() * np.outer(pg, pg)
np.fill_diagonal(O, 0); np.fill_diagonal(E, 0)
R = np.where(E > 0, (O - E) / np.sqrt(np.where(E > 0, E, 1)), 0)
edges = [(a, b, R[a, b]) for a in range(len(nodes)) for b in range(a + 1, len(nodes)) if R[a, b] > BEYOND]

# link clustering: two lines that share a concept are as alike as the neighbourhoods of their other two ends
nbr = collections.defaultdict(dict)
for a, b, wt in edges: nbr[a][b] = wt; nbr[b][a] = wt
vecs = {}
for i, nb in nbr.items():
    v = dict(nb); v[i] = sum(nb.values()) / len(nb); vecs[i] = v
def tanimoto(i, j):
    vi, vj = vecs[i], vecs[j]
    dot = sum(w * vj.get(k, 0) for k, w in vi.items())
    return dot / (sum(w * w for w in vi.values()) + sum(w * w for w in vj.values()) - dot)
eid = {}
for n_, (a, b, _) in enumerate(edges): eid[(a, b)] = eid[(b, a)] = n_
pairs = []
for k, nb in nbr.items():
    ns = sorted(nb)
    for s in range(len(ns)):
        for t in range(s + 1, len(ns)):
            pairs.append((tanimoto(ns[s], ns[t]), eid[(ns[s], k)], eid[(ns[t], k)]))
pairs.sort(key=lambda q: (-q[0], q[1], q[2]))
M = len(edges)
parent = list(range(M)); m = [1] * M; nset = [{a, b} for a, b, _ in edges]
def find(e):
    while parent[e] != e: parent[e] = parent[parent[e]]; e = parent[e]
    return e
def dens(mc, nc): return 0 if nc <= 2 else mc * (mc - nc + 1) / ((nc - 2) * (nc - 1))
total = 0.0; bestD, best = -1, None
for q, (s, e1, e2) in enumerate(pairs):
    r1, r2 = find(e1), find(e2)
    if r1 != r2:
        total -= dens(m[r1], len(nset[r1])) + dens(m[r2], len(nset[r2]))
        if len(nset[r1]) < len(nset[r2]): r1, r2 = r2, r1
        parent[r2] = r1; m[r1] += m[r2]; nset[r1] |= nset[r2]; nset[r2] = set()
        total += dens(m[r1], len(nset[r1]))
    if q + 1 == len(pairs) or pairs[q + 1][0] != s:  # the end of one level of the tree
        D = 2 * total / M
        if D > bestD: bestD, best = D, [find(e) for e in range(M)]
comm = collections.defaultdict(list)
for e, r in enumerate(best or range(M)): comm[r].append(e)

groups = []
for es in comm.values():
    cs = sorted({v for e in es for v in edges[e][:2]})
    if len(cs) >= 3: groups.append({'concepts': cs, 'lines': len(es)})

def share(v, cs): return v[cs].sum() / v.sum() if v.sum() else 0
game_cards = {g: sum((cv[i] for i in pools[g]), np.zeros(len(nodes))) for g in games}
facs = sorted({(r['game'], r['faction']) for r in csv.DictReader(open('axes.tsv', encoding='utf-8'), delimiter='\t')})
fvec = {(g, fa): sum((cv[i] for i, v in pools[g].items() if fa in v[3]), np.zeros(len(nodes))) for g, fa in facs}
for gr in groups:
    cs = gr['concepts']
    avg = {g: np.mean([share(d[2], cs) for d in decks if d[0] == g]) for g in per_game}
    gr['decks'] = sorted(((share(d[2], cs) / avg[d[0]] if avg[d[0]] else 0, n) for n, d in enumerate(decks)), reverse=True)
    gr['fit_decks'] = [n for r, n in gr['decks'] if r >= FIT]
    gr['games'] = collections.Counter(decks[n][0] for n in gr['fit_decks'])
    gr['facs'] = sorted(((share(fvec[f], cs) / share(game_cards[f[0]], cs) if share(game_cards[f[0]], cs) else 0,
                          share(fvec[f], cs), f) for f in facs), reverse=True)
groups.sort(key=lambda gr: (-len(gr['games']), -len(gr['fit_decks'])))
for n, gr in enumerate(groups, 1): gr['key'] = f'G{n:02d}'
nofit = [gr['key'] for gr in groups if gr['facs'][0][0] < FIT]
lonely = [f for f in facs if all(next(t[0] for t in gr['facs'] if t[2] == f) < FIT for gr in groups)]
name = lambda j: plain.get(nodes[j], nodes[j])

with open(os.path.join(HERE, 'faction_archetypes.tsv'), 'w', encoding='utf-8') as o:
    o.write('group\tconcepts\tlines\tfit_decks\tgames\ttop_decks\tbest_factions\n')
    for gr in groups:
        o.write('\t'.join([gr['key'], ','.join(nodes[j] for j in gr['concepts']), str(gr['lines']), str(len(gr['fit_decks'])),
                           ','.join(f'{g}:{k}' for g, k in sorted(gr['games'].items())),
                           '; '.join(f'{decks[n][0]}:{decks[n][1]}:{r:.2f}' for r, n in gr['decks'][:TOP]),
                           '; '.join(f'{g}:{fa}:{s:.2f}:{r:.2f}' for r, s, (g, fa) in gr['facs'][:5])]) + '\n')

with open(os.path.join(HERE, 'faction_archetypes.md'), 'w', encoding='utf-8') as o:
    o.write('# Step 3: the ways to play that decks put together (made by faction_archetypes.py)\n\n')
    o.write(f'{len(decks)} decks of {len(per_game)} games, {len(nodes)} concepts, {M} lines above chance. '
            f'{len(groups)} groups of 3+ concepts. A deck or faction fits a group when its share of concepts on the group '
            f'is at least {FIT} times its game\'s average ("x1.5").\n\n')
    o.write('Deck card names the library does not know: ' +
            (', '.join(f'{g} {k}' for g, k in sorted(missing.items()) if k) or 'none') + '.\n\n')
    for gr in groups:
        o.write(f"## {gr['key']}: {len(gr['concepts'])} concepts; {len(gr['fit_decks'])} decks fit "
                f"({', '.join(f'{g} {k}' for g, k in sorted(gr['games'].items())) or 'none'})\n")
        o.write('- Concepts: ' + '; '.join(name(j) for j in gr['concepts']) + '\n')
        o.write('- Decks: ' + '; '.join(f'{decks[n][1]} ({decks[n][0]}, x{r:.1f})' for r, n in gr['decks'][:TOP]) + '\n')
        o.write('- Factions: ' + '; '.join(f'{fa} ({g}, {s:.0%}, x{r:.1f})' for r, s, (g, fa) in gr['facs'][:5]) + '\n\n')
    o.write('Groups no faction fits: ' + (', '.join(nofit) or 'none') + '.\n\n')
    o.write('Factions that fit no group: ' + (', '.join(f'{fa} ({g})' for g, fa in lonely) or 'none') + '.\n')
print(len(decks), 'decks;', M, 'lines;', len(groups), 'groups;', len(nofit), 'with no faction;', len(lonely),
      'factions with no group; unknown deck names', sum(missing.values()))
