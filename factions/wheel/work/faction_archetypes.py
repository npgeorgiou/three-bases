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
FIT = 2.0      # a deck or faction fits a group at twice its game's average share or more, its best BEST groups only (Claude's)
BEST = 2
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

# Louvain (Blondel et al. 2008): every concept starts alone and moves, in a fixed order, to the group where its lines are
# thickest, until no move helps; then the groups are joined as blocks the same way. GAMMA sets how much a move must gain.
W = np.zeros_like(R)
for a, b, wt in edges: W[a, b] = W[b, a] = wt
def louvain(gamma):
    label = list(range(len(nodes)))  # concept -> home group
    A = W.copy(); members = [[i] for i in range(len(nodes))]
    while True:
        n = len(A); k = A.sum(1); m2 = k.sum()
        if m2 == 0: break
        com = list(range(n)); tot = k.copy(); moved_any = False
        while True:
            moved = False
            for i in range(n):
                ci = com[i]; tot[ci] -= k[i]
                links = collections.defaultdict(float)
                for j in np.nonzero(A[i])[0]:
                    if j != i: links[com[j]] += A[i, j]
                best, gain = ci, links.get(ci, 0) - gamma * tot[ci] * k[i] / m2
                for cj in sorted(links):
                    g = links[cj] - gamma * tot[cj] * k[i] / m2
                    if g > gain + 1e-12: best, gain = cj, g
                com[i] = best; tot[best] += k[i]
                if best != ci: moved = moved_any = True
            if not moved: break
        if not moved_any: break
        ids = {c_: n_ for n_, c_ in enumerate(sorted(set(com)))}
        new_members = [[] for _ in ids]
        for i in range(n): new_members[ids[com[i]]] += members[i]
        B = np.zeros((len(ids), len(ids)))
        for i in range(n):
            for j in range(n): B[ids[com[i]], ids[com[j]]] += A[i, j]
        A, members = B, new_members
    for g_, ms in enumerate(members):
        for i in ms: label[i] = g_
    return label

def joins(label):
    """home groups, then every concept that is together with a group's concepts in the same decks more often than chance,
    by the same margin as a line (pooled over the group's concepts), joins it too"""
    home = collections.defaultdict(list)
    for i, g_ in enumerate(label): home[g_].append(i)
    out = []
    for g_, cs in home.items():
        if len(cs) < 2: continue
        shared = []
        for i in range(len(nodes)):
            if i in cs: continue
            o, e = O[i, cs].sum(), E[i, cs].sum()
            if e > 0 and (o - e) / np.sqrt(e) > BEYOND: shared.append(i)
        out.append({'home': sorted(cs), 'shared': shared, 'concepts': sorted(cs + shared)})
    return out

sweep = {}
for gamma in [round(0.2 + 0.1 * t, 1) for t in range(49)]:
    gs = joins(louvain(gamma))
    sweep[gamma] = (sum(1 for gr in gs if 8 <= len(gr['concepts']) <= 10), gs)
GAMMA = max(sweep, key=lambda g_: (sweep[g_][0], -g_))
groups = [gr for gr in sweep[GAMMA][1] if len(gr['concepts']) >= 3]

def share(v, cs): return v[cs].sum() / v.sum() if v.sum() else 0
game_cards = {g: sum((cv[i] for i in pools[g]), np.zeros(len(nodes))) for g in games}
facs = sorted({(r['game'], r['faction']) for r in csv.DictReader(open('axes.tsv', encoding='utf-8'), delimiter='\t')})
fvec = {(g, fa): sum((cv[i] for i, v in pools[g].items() if fa in v[3]), np.zeros(len(nodes))) for g, fa in facs}
for gr in groups:
    cs = gr['concepts']
    avg = {g: np.mean([share(d[2], cs) for d in decks if d[0] == g]) for g in per_game}
    gr['ratio'] = [share(d[2], cs) / avg[d[0]] if avg[d[0]] else 0 for d in decks]
    gr['fratio'] = {f: (share(fvec[f], cs) / share(game_cards[f[0]], cs) if share(game_cards[f[0]], cs) else 0) for f in facs}
    gr['fshare'] = {f: share(fvec[f], cs) for f in facs}
def best_of(r): return sorted(range(len(groups)), key=lambda q: -r[q])[:BEST]
for n, d in enumerate(decks):  # a deck fits its best 2 groups, when at twice its game's average or more
    for q in best_of([gr['ratio'][n] for gr in groups]):
        if groups[q]['ratio'][n] >= FIT: groups[q].setdefault('fit', []).append(n)
fits_f = collections.defaultdict(list)
for f in facs:
    for q in best_of([gr['fratio'][f] for gr in groups]):
        if groups[q]['fratio'][f] >= FIT: fits_f[q].append(f)
for q, gr in enumerate(groups):
    gr['fit_decks'] = sorted(gr.get('fit', []), key=lambda n: -gr['ratio'][n])
    gr['decks'] = [(gr['ratio'][n], n) for n in gr['fit_decks']]
    gr['games'] = collections.Counter(decks[n][0] for n in gr['fit_decks'])
    gr['facs'] = sorted(((gr['fratio'][f], gr['fshare'][f], f) for f in fits_f[q]), reverse=True)
    gr['near'] = sorted(((gr['fratio'][f], gr['fshare'][f], f) for f in facs), reverse=True)[:3]
groups.sort(key=lambda gr: (-len(gr['games']), -len(gr['fit_decks'])))
for n, gr in enumerate(groups, 1): gr['key'] = f'G{n:02d}'
nofit = [gr['key'] for gr in groups if not gr['facs']]
lonely = [f for f in facs if not any(f in fits_f[q] for q in range(len(groups)))]
name = lambda j: plain.get(nodes[j], nodes[j])

def cname(gr, j): return name(j) + (' (shared)' if j in gr['shared'] else '')
with open(os.path.join(HERE, 'faction_archetypes.tsv'), 'w', encoding='utf-8') as o:
    o.write('group\thome_concepts\tshared_concepts\tsize\tfit_decks\tgames\ttop_decks\tfit_factions\tnearest_factions\n')
    for gr in groups:
        o.write('\t'.join([gr['key'], ','.join(nodes[j] for j in gr['home']), ','.join(nodes[j] for j in gr['shared']),
                           str(len(gr['concepts'])), str(len(gr['fit_decks'])),
                           ','.join(f'{g}:{k}' for g, k in sorted(gr['games'].items())),
                           '; '.join(f'{decks[n][0]}:{decks[n][1]}:{r:.2f}' for r, n in gr['decks'][:TOP]),
                           '; '.join(f'{g}:{fa}:{s:.2f}:{r:.2f}' for r, s, (g, fa) in gr['facs']),
                           '; '.join(f'{g}:{fa}:{s:.2f}:{r:.2f}' for r, s, (g, fa) in gr['near'])]) + '\n')

with open(os.path.join(HERE, 'faction_archetypes.md'), 'w', encoding='utf-8') as o:
    o.write('# Step 3: the ways to play that decks put together (made by faction_archetypes.py)\n\n')
    o.write(f'{len(decks)} decks of {len(per_game)} games, {len(nodes)} concepts, {len(edges)} lines above chance. '
            f'{len(groups)} groups (setting {GAMMA}: {sweep[GAMMA][0]} groups of 8 to 10 concepts). A deck or faction fits '
            f'its best {BEST} groups when its share of their concepts is at least {FIT:g} times its game\'s average ("x2").\n\n')
    o.write('Deck card names the library does not know: ' +
            (', '.join(f'{g} {k}' for g, k in sorted(missing.items()) if k) or 'none') + '.\n\n')
    for gr in groups:
        size = len(gr['concepts']); flag = '' if 8 <= size <= 10 else f' **{"under" if size < 8 else "over"} 8 to 10**'
        o.write(f"## {gr['key']}: {size} concepts{flag}; {len(gr['fit_decks'])} decks fit "
                f"({', '.join(f'{g} {k}' for g, k in sorted(gr['games'].items())) or 'none'})\n")
        o.write('- Concepts: ' + '; '.join(cname(gr, j) for j in gr['concepts']) + '\n')
        o.write('- Decks: ' + ('; '.join(f'{decks[n][1]} ({decks[n][0]}, x{r:.1f})' for r, n in gr['decks'][:TOP]) or 'none') + '\n')
        o.write('- Factions that fit: ' + ('; '.join(f'{fa} ({g}, {s:.0%}, x{r:.1f})' for r, s, (g, fa) in gr['facs']) or
                'none; nearest ' + '; '.join(f'{fa} ({g}, x{r:.1f})' for r, s, (g, fa) in gr['near'])) + '\n\n')
    o.write('Groups no faction fits: ' + (', '.join(nofit) or 'none') + '.\n\n')
    o.write('Factions that fit no group: ' + (', '.join(f'{fa} ({g})' for g, fa in lonely) or 'none') + '.\n')
print(len(decks), 'decks;', len(edges), 'lines; setting', GAMMA, ';', len(groups), 'groups,', sweep[GAMMA][0], 'of 8-10;',
      len(nofit), 'with no faction;', len(lonely), 'factions with no group; unknown deck names', sum(missing.values()))
