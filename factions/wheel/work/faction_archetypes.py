"""Step 3 (START_DESIGN-1-wheel.md): ways to play that decks group together; they become our factions' archetypes.
Run from library/cards_db: python3 ../../factions/wheel/work/faction_archetypes.py
 -> factions/wheel/work/faction_archetypes.tsv (one row per group) and faction_archetypes.md (the same in plain words).
1. Scores: for every deck of decks.tsv (all its cards) and every real faction of axes.tsv (its cards), per usable concept
   (concepts.tsv): the log-odds ratio with an informative prior (Monroe et al. 2008) against all the cards of its game, as a
   z-score; above 1.96 is strong. A card counts each concept once per ability or keyword that gives it (axes.instances).
2. Groups: weighted NMF on the deck rows (scores below 0 set to 0); each game weighs the square root of its deck count.
   The number of groups (at least MIN_K) is the one whose groups come back most alike over SEEDS runs. A deck fits a group
   when the group is at least CARRY of its mix; a group is kept when decks of 2+ games fit it.
3. Factions are never rows of the NMF: a faction's fit to a group is the cosine between its positive scores and the group."""
import collections, csv, os, sqlite3, sys, time
import numpy as np
from scipy.optimize import linear_sum_assignment
sys.path.insert(0, os.getcwd())
import axes, deck_analysis, faction_asks

HERE = os.path.dirname(os.path.abspath(__file__))
PRIOR = 100.0       # the prior's size in concept instances (Claude's)
STRONG = 1.96       # a score above this is strong
MIN_K, MAX_K = 14, 30  # groups tried (14: 20 factions x 2 archetypes, each in at most 3 factions; 30 Claude's)
SEEDS = 10          # runs per number of groups, for the stability (Claude's)
CARRY = 0.30        # a deck fits a group that is at least 30% of its mix (Claude's)
FIT = 0.50          # a faction fits a group at cosine 0.5 or more (Claude's)
TOP = 8

c = sqlite3.connect('cards.sqlite')
games = sorted({g for (g,) in c.execute('select distinct game from card')})
x = faction_asks.Ctx(c, games, None, {})
con, pools, _ = axes.tag(c, x, games)

usable = [r['concept'] for r in csv.DictReader(open(os.path.join(HERE, 'concepts.tsv'), encoding='utf-8'), delimiter='\t')
          if r['kind'] == 'usable']
kids = collections.defaultdict(set)
plain = {}
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
col = {k: j for j, k in enumerate(usable)}

def vec(i):
    """a card's instances of each usable concept (a parent counts only on cards none of its children carry)"""
    v = np.zeros(len(usable))
    for k in con.get(i, ()):
        if k in col and not con[i] & sub[k]: v[col[k]] += axes.instances(i, k)
    return v
cv = {i: vec(i) for g in games for i in pools[g]}
game_tot = {g: sum((cv[i] for i in pools[g]), np.zeros(len(usable))) for g in games}

def score(counts, g):
    """Monroe et al. 2008: log-odds of each concept in this set against the game's cards, prior from the game's mix, as z"""
    bg = game_tot[g]; a = PRIOR * bg / bg.sum(); a0 = PRIOR
    y, n = counts, counts.sum()
    ok = a > 0
    z = np.zeros(len(usable))
    li = np.log((y + a)[ok] / (n + a0 - y - a)[ok])
    lj = np.log((bg + a)[ok] / (bg.sum() + a0 - bg - a)[ok])
    z[ok] = (li - lj) / np.sqrt(1 / (y + a)[ok] + 1 / (bg + a)[ok])
    return z

decks, missing, outside = [], collections.Counter(), collections.Counter()
with open('decks.tsv', encoding='utf-8') as f:
    next(f)
    for line in f:
        p = line.rstrip('\n').split('\t')
        if len(p) < 4 or p[0] not in pools: continue
        ids, bad = deck_analysis.parse_deck(c, p[0], p[3])
        missing[p[0]] += len(bad)
        ids = set(ids)
        outside[p[0]] += len(ids - set(pools[p[0]]))
        ids &= set(pools[p[0]])
        if ids: decks.append((p[0], p[1], score(sum(cv[i] for i in ids), p[0])))

facs = sorted({(r['game'], r['faction']) for r in csv.DictReader(open('axes.tsv', encoding='utf-8'), delimiter='\t')})
fscore = {(g, fa): score(sum(cv[i] for i, v in pools[g].items() if fa in v[3]), g) for g, fa in facs}

print('scores', round(time.process_time()), 's', flush=True)
X = np.array([np.maximum(z, 0) for _, _, z in decks])
per_game = collections.Counter(g for g, _, _ in decks)
w = np.array([np.sqrt(per_game[g]) / per_game[g] for g, _, _ in decks])  # each game weighs sqrt(its decks)
w = w / w.mean()

def nmf(k, seed, it=1500):
    r = np.random.default_rng(seed)
    W = r.random((len(X), k)) * X.mean() + 1e-3; H = r.random((k, X.shape[1])) * X.mean() + 1e-3
    D = w[:, None]
    last = None
    for t in range(it):
        H *= (W.T @ (D * X)) / (W.T @ (D * (W @ H)) + 1e-9)
        W *= (X @ H.T) / (W @ H @ H.T + 1e-9)
        if t % 25 == 24:  # stop when the fit improves by under 0.01% in 25 rounds
            loss = float((w * ((X - W @ H) ** 2).sum(1)).sum())
            if last and last - loss < 1e-4 * last: break
            last = loss
    s = np.linalg.norm(H, axis=1) + 1e-12
    return W * s, H / s[:, None], float((w * ((X - W @ H) ** 2).sum(1)).sum())

def alike(H1, H2):
    sim = H1 @ H2.T
    r, q = linear_sum_assignment(-sim)
    return sim[r, q].mean()

stab = {}
best = {}
for k in range(MIN_K, MAX_K + 1):
    runs = [nmf(k, s) for s in range(SEEDS)]
    stab[k] = np.mean([alike(runs[a][1], runs[b][1]) for a in range(SEEDS) for b in range(a + 1, SEEDS)])
    best[k] = min(runs, key=lambda t: t[2])
    print(k, 'groups', round(stab[k], 3), round(time.process_time()), 's', flush=True)
K = max(stab, key=lambda k: (round(stab[k], 3), k))
W, H, _ = best[K]
mix = W / (W.sum(1, keepdims=True) + 1e-12)

groups = []
for j in range(K):
    carry = [d for d in range(len(decks)) if mix[d, j] >= CARRY]
    gs = collections.Counter(decks[d][0] for d in carry)
    fits = sorted(((float(np.maximum(fscore[f], 0) @ H[j] / (np.linalg.norm(np.maximum(fscore[f], 0)) + 1e-12)), f)
                   for f in facs), reverse=True)
    groups.append({'j': j, 'carry': carry, 'games': gs, 'fits': fits, 'kept': len(gs) >= 2,
                   'top': [(usable[t], H[j, t]) for t in np.argsort(-H[j])[:TOP] if H[j, t] > 0.05]})
kept = [gr for gr in groups if gr['kept']]
kept.sort(key=lambda gr: -len(gr['carry']))
for n, gr in enumerate(kept, 1): gr['key'] = f'G{n:02d}'
nofit = [gr['key'] for gr in kept if gr['fits'][0][0] < FIT]
lonely = [f for f in facs if all(gr['fits'][[t[1] for t in gr['fits']].index(f)][0] < FIT for gr in kept)]
name = lambda k: plain.get(k, k)

with open(os.path.join(HERE, 'faction_archetypes.tsv'), 'w', encoding='utf-8') as o:
    o.write('group\tdecks\tgames\ttop_concepts\ttop_decks\tbest_factions\n')
    for gr in kept:
        td = sorted(gr['carry'], key=lambda d: -mix[d, gr['j']])[:TOP]
        o.write('\t'.join([gr['key'], str(len(gr['carry'])), ','.join(f'{g}:{n}' for g, n in sorted(gr['games'].items())),
                           ','.join(f'{k}:{v:.2f}' for k, v in gr['top']),
                           '; '.join(f'{decks[d][0]}:{decks[d][1]}:{mix[d, gr["j"]]:.2f}' for d in td),
                           '; '.join(f'{g}:{fa}:{v:.2f}' for v, (g, fa) in gr['fits'][:5])]) + '\n')

with open(os.path.join(HERE, 'faction_archetypes.md'), 'w', encoding='utf-8') as o:
    o.write('# Step 3: ways to play that decks group together (made by faction_archetypes.py)\n\n')
    o.write(f'{len(decks)} decks of {len(per_game)} games. {K} groups (the most stable from {MIN_K} to {MAX_K}, '
            f'{stab[K]:.2f} alike over {SEEDS} runs); {len(kept)} kept, fitted by decks of 2+ games. '
            f'A deck fits a group that is at least {CARRY:.0%} of its mix; a faction fits at cosine {FIT} or more.\n\n')
    o.write('Deck card names the library does not know: ' + (', '.join(f'{g} {n}' for g, n in sorted(missing.items()) if n) or 'none') +
            '. Known cards that are not player cards (left out): ' + (', '.join(f'{g} {n}' for g, n in sorted(outside.items()) if n) or 'none') + '.\n\n')
    o.write('Stability by number of groups: ' + ', '.join(f'{k} {v:.2f}' for k, v in stab.items()) + '.\n\n')
    dropped = [gr for gr in groups if not gr['kept']]
    if dropped:
        o.write('Groups left out (decks of one game only): ' + '; '.join(
            f"{', '.join(name(k) for k, _ in gr['top'][:3])} ({', '.join(f'{g} {n}' for g, n in gr['games'].items()) or 'no deck'})"
            for gr in dropped) + '.\n\n')
    for gr in kept:
        td = sorted(gr['carry'], key=lambda d: -mix[d, gr['j']])[:TOP]
        o.write(f"## {gr['key']}: {len(gr['carry'])} decks ({', '.join(f'{g} {n}' for g, n in sorted(gr['games'].items()))})\n")
        o.write('- Concepts: ' + '; '.join(f'{name(k)} {v:.2f}' for k, v in gr['top']) + '\n')
        o.write('- Decks: ' + '; '.join(f'{decks[d][1]} ({decks[d][0]}, {mix[d, gr["j"]]:.0%})' for d in td) + '\n')
        o.write('- Factions: ' + '; '.join(f'{fa} ({g}, {v:.2f})' for v, (g, fa) in gr['fits'][:5]) + '\n\n')
    o.write('Groups no faction fits: ' + (', '.join(nofit) or 'none') + '.\n\n')
    o.write('Factions that fit no group: ' + (', '.join(f'{fa} ({g})' for g, fa in lonely) or 'none') + '.\n')
print(len(decks), 'decks;', K, 'groups,', len(kept), 'kept;', len(nofit), 'with no faction;', len(lonely), 'factions with no group;',
      'unknown deck names', sum(missing.values()))
