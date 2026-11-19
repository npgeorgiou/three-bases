"""Step 3 (START_DESIGN-1-wheel.md): the ways to play that decks lean on, by NMF; they become our factions' archetypes.
Run from library/cards_db: python3 ../../factions/wheel/work/deck_groups_nmf.py [--groups N]  (about 2.5 minutes, 2 cores;
 with --groups, N groups and no stability runs, a few seconds)
 -> factions/wheel/work/deck_groups_nmf.tsv (one row per group), deck_groups_nmf.md (the same in plain words) and
    deck_groups_nmf.json (groups, decks and factions, read by make_faction.py); with --groups N the files end in _N.
1. Concepts: the usable concepts of concepts.tsv (a card counts each once; a parent only on cards none of its children
   carry), plus five unit concepts against the card's game: unit, cheap unit, expensive unit (concept_tags.py), strong for its
   cost and tough for its cost (above the game's straight line of strength or defence by cost).
2. Scores: every deck of decks.tsv (all its cards) and every real faction (Monster Train's clans left out, NOT_FACTIONS), per concept: the log-odds ratio
   with a prior (Monroe et al. 2008) against all the cards of its game, as a z-score; above STRONG the deck leans on it.
3. Groups: NMF on the deck rows only (scores below 0 set to 0); each game weighs the square root of its deck count. The first guess comes from the data (NNDSVD, Boutsidis and Gallopoulos 2008), so one
   run gives the result. The number of groups (MIN_K to MAX_K) is the one whose groups stay most alike when the run is
   repeated on 90% of the decks, RESAMPLES times. A deck fits a group that is at least CARRY of its mix.
4. Per group: its TOP heaviest concepts, with the share of its decks that lean on each; the base concepts (more than half of its decks have them,
   more often than their game's decks); its unit numbers against its games; a group whose decks are 80% or more from one
   game is marked. Factions are never used to make the groups: a faction fits its best BEST groups when its share of
   their concepts is at least FIT times its game's average."""
import collections, csv, json, multiprocessing, os, sqlite3, sys
import numpy as np
from scipy.optimize import linear_sum_assignment
sys.path.insert(0, os.getcwd())
import concept_tags, deck_analysis, faction_asks

HERE = os.path.dirname(os.path.abspath(__file__))
PRIOR = 100.0       # the prior's size in concept instances (Claude's)
STRONG = 1.96       # a deck leans on a concept above this score
MIN_K, MAX_K = 14, 30  # groups tried (14: 20 factions x 2 archetypes, each in at most 3 factions; 30 Claude's)
RESAMPLES = 10      # runs on 90% of the decks, for the stability (Claude's)
CARRY = 0.30        # a deck fits a group that is at least 30% of its mix (Claude's)
TOP = 10            # a group lists its 10 heaviest concepts, each with the share of its decks that lean on it (Claude's)
BASE = 0.5          # base concepts: more than half of the group's decks have them (Claude's)
ONE_GAME = 0.8      # a group whose decks are 80% from one game is marked (Claude's)
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
            decks.append({'game': p[0], 'name': p[1], 'size': len(ids), 'counts': cnt, 'z': score(cnt, p[0])})
facs = sorted({(g, fa) for g in games if g not in NOT_FACTIONS for fa in x.factions(g)})
fcount = {(g, fa): sum((cv[i] for i, v in pools[g].items() if fa in v[3]), np.zeros(len(nodes))) for g, fa in facs}

X = np.array([np.maximum(d['z'], 0) for d in decks])
per_game = collections.Counter(d['game'] for d in decks)
w = np.array([np.sqrt(per_game[d['game']]) / per_game[d['game']] for d in decks]); w = w / w.mean()

def nndsvd(A, k):
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    W = np.zeros((A.shape[0], k)); H = np.zeros((k, A.shape[1]))
    W[:, 0] = np.sqrt(S[0]) * np.abs(U[:, 0]); H[0] = np.sqrt(S[0]) * np.abs(Vt[0])
    for j in range(1, k):
        u, v = U[:, j], Vt[j]
        up, un, vp, vn = np.maximum(u, 0), np.maximum(-u, 0), np.maximum(v, 0), np.maximum(-v, 0)
        mp, mn = np.linalg.norm(up) * np.linalg.norm(vp), np.linalg.norm(un) * np.linalg.norm(vn)
        a, b, m = (up, vp, mp) if mp >= mn else (un, vn, mn)
        if m == 0: continue
        W[:, j] = np.sqrt(S[j] * m) * a / np.linalg.norm(a); H[j] = np.sqrt(S[j] * m) * b / np.linalg.norm(b)
    avg = A.mean()
    return W + avg / 100, H + avg / 100  # a small floor so multiplicative updates can move every value

def nmf(rows, k, it=2000):
    A, D = X[rows], w[rows][:, None]
    W, H = nndsvd(np.sqrt(D) * A, k); W = W / np.sqrt(D)
    last = None
    for t in range(it):
        H *= (W.T @ (D * A)) / (W.T @ (D * (W @ H)) + 1e-9)
        W *= (A @ H.T) / (W @ H @ H.T + 1e-9)
        if t % 25 == 24:  # stop when the fit improves by under 0.01% in 25 rounds
            loss = float((D[:, 0] * ((A - W @ H) ** 2).sum(1)).sum())
            if last and last - loss < 1e-4 * last: break
            last = loss
    s = np.linalg.norm(H, axis=1) + 1e-12
    return W * s, H / s[:, None]

def alike(H1, H2):
    sim = H1 @ H2.T
    r, q = linear_sum_assignment(-sim)
    return sim[r, q].mean()

def runs(k):
    full = nmf(np.arange(len(X)), k)
    rng = np.random.default_rng(k)  # the same 90% samples every time
    sims = [alike(full[1], nmf(np.sort(rng.choice(len(X), int(0.9 * len(X)), replace=False)), k)[1]) for _ in range(RESAMPLES)]
    return k, float(np.mean(sims)), full
FORCED = int(sys.argv[sys.argv.index('--groups') + 1]) if '--groups' in sys.argv else None
SUFFIX = f'_{FORCED}' if FORCED else ''
if FORCED:
    stab, K = {}, FORCED
    W, H = nmf(np.arange(len(X)), K)
else:
    with multiprocessing.get_context('fork').Pool(2) as pool:
        res = pool.map(runs, range(MIN_K, MAX_K + 1))
    stab = {k: s for k, s, _ in res}
    K = max(stab, key=lambda k: (round(stab[k], 3), k))
    W, H = next(r for k, _, r in res if k == K)
mix = W / (W.sum(1, keepdims=True) + 1e-12)

Z = np.array([d['z'] for d in decks])
HAS = np.array([d['counts'] > 0 for d in decks])
gname = np.array([d['game'] for d in decks])
ghas = {g: HAS[gname == g].mean(0) for g in per_game}
gunit = {g: np.array([(d['counts'][col[k]] / d['size']) for d in decks if d['game'] == g for k in UNIT]).reshape(-1, len(UNIT)).mean(0)
         for g in per_game}
def share(v, cs): return v[cs].sum() / v.sum() if v.sum() else 0
groups = []
for j in range(K):
    fit = [n for n in range(len(decks)) if mix[n, j] >= CARRY]
    if not fit: continue
    fit.sort(key=lambda n: -mix[n, j])
    lean = (Z[fit] > STRONG).mean(0)
    order = np.argsort(-H[j])
    cs = [int(t) for t in order[:TOP] if H[j, t] > 0]
    has = HAS[fit].mean(0); avg = np.array([ghas[decks[n]['game']] for n in fit]).mean(0)
    base = sorted(((float(has[t]), int(t)) for t in range(len(nodes))
                   if t not in cs and nodes[t] not in UNIT and has[t] > BASE and has[t] > avg[t]), reverse=True)
    uu = np.array([[decks[n]['counts'][col[k]] / decks[n]['size'] for k in UNIT] for n in fit]).mean(0)
    ug = np.array([gunit[decks[n]['game']] for n in fit]).mean(0)
    gs = collections.Counter(decks[n]['game'] for n in fit)
    groups.append({'j': j, 'concepts': cs, 'lean': {int(t): float(lean[t]) for t in cs}, 'base': base, 'fit': fit,
                   'games': gs, 'one_game': gs.most_common(1)[0][1] >= ONE_GAME * len(fit),
                   'units': {k: float(uu[q] / ug[q]) if ug[q] else 0 for q, k in enumerate(UNIT)}})
groups.sort(key=lambda gr: -len(gr['fit']))
for n, gr in enumerate(groups, 1): gr['key'] = f'G{n:02d}'
for gr in groups:
    gr['fratio'] = {f: (share(fcount[f], gr['concepts']) / share(game_tot[f[0]], gr['concepts'])
                        if share(game_tot[f[0]], gr['concepts']) else 0) for f in facs}
fits_f = collections.defaultdict(list)
for f in facs:
    for q in sorted(range(len(groups)), key=lambda q: -groups[q]['fratio'][f])[:BEST]:
        if groups[q]['fratio'][f] >= FIT: fits_f[q].append(f)
for q, gr in enumerate(groups):
    gr['facs'] = sorted(((gr['fratio'][f], f) for f in fits_f[q]), reverse=True)
    gr['near'] = sorted(((gr['fratio'][f], f) for f in facs), reverse=True)[:3]
nofit = [gr['key'] for gr in groups if not gr['facs']]
lonely = [f for f in facs if not any(f in fits_f[q] for q in range(len(groups)))]
left = [t for t in range(len(nodes)) if not any(t in gr['concepts'] for gr in groups)]
name = lambda t: plain.get(nodes[t], nodes[t])
def units_line(gr): return '; '.join(f'{UNIT[k]} x{v:.1f}' for k, v in gr['units'].items())

with open(os.path.join(HERE, f'deck_groups_nmf{SUFFIX}.tsv'), 'w', encoding='utf-8') as o:
    o.write('group\tdecks\tgames\tone_game\tconcepts\tbase_concepts\tunits\tfit_factions\n')
    for gr in groups:
        o.write('\t'.join([gr['key'], str(len(gr['fit'])), ','.join(f'{g}:{k}' for g, k in sorted(gr['games'].items())),
                           'yes' if gr['one_game'] else '', ','.join(f"{nodes[t]}:{gr['lean'][t]:.2f}" for t in gr['concepts']),
                           ','.join(f'{nodes[t]}:{v:.2f}' for v, t in gr['base']),
                           ','.join(f'{k}:{v:.2f}' for k, v in gr['units'].items()),
                           '; '.join(f'{g}:{fa}:{r:.2f}' for r, (g, fa) in gr['facs'])]) + '\n')

with open(os.path.join(HERE, f'deck_groups_nmf{SUFFIX}.md'), 'w', encoding='utf-8') as o:
    o.write('# Step 3: the ways to play that decks lean on, by NMF (made by deck_groups_nmf.py)\n\n')
    o.write(f'{len(decks)} decks of {len(per_game)} games, {len(nodes)} concepts. {K} groups' +
            (' (set by hand). ' if FORCED else f': the number from {MIN_K} to {MAX_K} whose groups stay most alike on 90% of '
             f'the decks ({stab[K]:.2f}; 1 = the same). ') + f'A deck fits a group that is '
            f'{CARRY:.0%} or more of its mix. Concepts: the group\'s 10 heaviest, with the share of its decks that lean on each. '
            f'Base concepts: what more than half of its decks have. Units: against their games (x1 = as usual). A faction fits '
            f'its best {BEST} groups at {FIT:g} times its game\'s average share of their concepts ("x2").\n\n')
    o.write('Deck card names the library does not know: ' +
            (', '.join(f'{g} {k}' for g, k in sorted(missing.items()) if k) or 'none') + '.\n\n')
    if stab: o.write('Stability by number of groups: ' + ', '.join(f'{k} {v:.2f}' for k, v in stab.items()) + '.\n\n')
    for gr in groups:
        o.write(f"## {gr['key']}: {len(gr['fit'])} decks ({', '.join(f'{g} {k}' for g, k in sorted(gr['games'].items()))})"
                + (' **one game**' if gr['one_game'] else '') + '\n')
        o.write('- Concepts: ' + '; '.join(f"{name(t)} {gr['lean'][t]:.0%}" for t in gr['concepts']) + '\n')
        o.write('- Base concepts: ' + ('; '.join(f'{name(t)} {v:.0%}' for v, t in gr['base'][:10]) or 'none') + '\n')
        o.write('- Units: ' + units_line(gr) + '\n')
        o.write('- Decks: ' + '; '.join(f"{decks[n]['name']} ({decks[n]['game']}, {mix[n, gr['j']]:.0%})" for n in gr['fit'][:6]) + '\n')
        o.write('- Factions that fit: ' + ('; '.join(f'{fa} ({g}, x{r:.1f})' for r, (g, fa) in gr['facs']) or
                'none; nearest ' + '; '.join(f'{fa} ({g}, x{r:.1f})' for r, (g, fa) in gr['near'])) + '\n\n')
    o.write('Concepts in no group: ' + ('; '.join(name(t) for t in left) or 'none') + '.\n\n')
    o.write('Groups no faction fits: ' + (', '.join(nofit) or 'none') + '.\n\n')
    o.write('Factions that fit no group: ' + (', '.join(f'{fa} ({g})' for g, fa in lonely) or 'none') + '.\n')

json.dump({'nodes': nodes, 'plain': {k: plain.get(k, k) for k in nodes}, 'unit': list(UNIT), 'strong': STRONG,
           'groups': [{'key': gr['key'], 'concepts': [nodes[t] for t in gr['concepts']],
                       'lean': {nodes[t]: round(v, 3) for t, v in gr['lean'].items()},
                       'base': [[nodes[t], round(v, 3)] for v, t in gr['base']], 'units': gr['units'],
                       'one_game': gr['one_game'], 'decks': gr['fit'],
                       'factions': [[g, fa, round(r, 2)] for r, (g, fa) in gr['facs']]} for gr in groups],
           'decks': [{'game': d['game'], 'name': d['name'], 'size': d['size'],
                      'mix': {gr['key']: round(float(mix[n, gr['j']]), 3) for gr in groups if mix[n, gr['j']] >= 0.05},
                      'counts': {nodes[t]: int(v) for t, v in enumerate(d['counts']) if v},
                      'z': {nodes[t]: round(float(v), 2) for t, v in enumerate(d['z']) if v > STRONG}} for n, d in enumerate(decks)],
           'factions': [{'game': g, 'faction': fa, 'fit': {gr['key']: round(gr['fratio'][(g, fa)], 2) for gr in groups},
                         'counts': {nodes[t]: int(v) for t, v in enumerate(fcount[(g, fa)]) if v}} for g, fa in facs],
           'game_counts': {g: {nodes[t]: int(v) for t, v in enumerate(game_tot[g]) if v} for g in game_tot}},
          open(os.path.join(HERE, f'deck_groups_nmf{SUFFIX}.json'), 'w', encoding='utf-8'))
print(len(decks), 'decks;', K, 'groups;', sum(gr['one_game'] for gr in groups), 'one game;', len(nofit), 'with no faction;',
      len(lonely), 'factions with no group;', len(left), 'concepts in no group; unknown deck names', sum(missing.values()))
