"""Step 6 (START_DESIGN-1-wheel.md): the 20 groups straight from the concept links. Run from library/cards_db.
A group is 4-6 usable concepts (work/concepts.tsv), each linked to at least 2 others in it; its pillars are its two most
strongly linked concepts; a concept that mostly uses what others make (makes under 0.3 over its links) needs a
concept in the group that makes for it (makes 0.5+ towards it). Linked: wheel/concept_links.tsv cards 1.2+, or decks 1.5+, or rare 3+ with a level of 1+.
A link's strength is how much more often than chance real cards link the two (cards, else rare; a link by decks alone
counts 1.2); a group's strength is the average over all its pairs of log2 of that (a pair with no link counts 0).
Candidates: for every linked pair as pillars, the others from the 10 concepts most strongly linked to both, every 2-4 of
them; per pillar pair and size the 3 strongest. The 20 are picked by one exact solver (scipy milp): two groups share at
most one concept, a pillar is a pillar of one group only, a concept is in at most 3 groups; the most total strength
plus 1 for each concept in some group (every usable concept is wanted in a group; those left out are printed).
python3 ../../factions/wheel/work/groups.py [--write]: prints the 20 and the standard concepts (in 7+ of the 10 games)
that are in no group; --write writes factions/wheel/work/groups.tsv."""
import csv, collections, itertools, math, sys
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix

W = '../../factions/wheel/work/'
CROWS = list(csv.DictReader(open(W + 'concepts.tsv'), delimiter='\t'))
USABLE = {r['concept'] for r in CROWS if r['kind'] == 'usable'}
GAMES = {r['concept']: len(r['games'].split(',')) for r in CROWS}
N, MAX_IN, COVER, POOL, KEEP = 20, 3, 1.0, 10, 3
f = lambda x: float(x or 0)
link, mk = {}, {}
for r in csv.DictReader(open('wheel/concept_links.tsv'), delimiter='\t'):
    a, b = r['a'], r['b']
    if a == b or a not in USABLE or b not in USABLE: continue
    if f(r['cards']) >= 1.2: w = f(r['cards'])
    elif f(r['rare']) >= 3 and f(r['level']) >= 1: w = f(r['rare'])
    elif f(r['decks']) >= 1.5: w = 1.2
    else: continue
    link[(a, b)] = link[(b, a)] = (w, int(r['games']))
    if r['makes']: mk[(a, b)] = f(r['makes']); mk[(b, a)] = round(1 - f(r['makes']), 2)
nb = collections.defaultdict(set)
for a, b in link: nb[a].add(b)
own = collections.defaultdict(list)
for (a, b), m in mk.items():
    if (a, b) in link: own[a].append(m)
USER = {c for c, ms in own.items() if sum(ms) / len(ms) < 0.3}  # mostly uses what others make
fed = lambda g: all(any(mk.get((y, x), 0) >= 0.5 for y in g if y != x and (x, y) in link) for x in g if x in USER)
lw = lambda a, b: math.log2(link[(a, b)][0]) if (a, b) in link else 0.0
def strength(g):
    return sum(lw(a, b) for a, b in itertools.combinations(g, 2)) / (len(g) * (len(g) - 1) / 2)
def pillars(g):
    return max(((a, b) for a, b in itertools.combinations(g, 2) if (a, b) in link), key=lambda p: link[p])
cands = {}
for a, b in {tuple(sorted(p)) for p in link}:
    pool = sorted((nb[a] | nb[b]) - {a, b}, key=lambda c: -(lw(a, c) + lw(b, c)))[:POOL]
    for k in (2, 3, 4):
        best = []
        for rest in itertools.combinations(pool, k):
            g = tuple(sorted((a, b) + rest))
            if g in cands or any(sum((x, y) in link for y in g if y != x) < 2 for x in g): continue
            if set(pillars(g)) != {a, b} or not fed(g): continue
            best.append((strength(g), g))
        for s, g in sorted(best, reverse=True)[:KEEP]: cands[g] = s
C = list(cands)
con = sorted(USABLE); ci = {c: i for i, c in enumerate(con)}
pairs = sorted({p for g in C for p in itertools.combinations(g, 2)}); pi = {p: i for i, p in enumerate(pairs)}
nx, ny = len(C), len(con)
A = lil_matrix((1 + ny + len(pairs) + ny + ny, nx + ny))
lo, hi = [N], [N]
A[0, :nx] = 1
for j, g in enumerate(C):
    for c in g: A[1 + ci[c], j] = 1
    for p in itertools.combinations(g, 2): A[1 + ny + pi[p], j] = 1
    for c in g: A[1 + ny + len(pairs) + ci[c], j] = -1
    for c in pillars(g): A[1 + 2 * ny + len(pairs) + ci[c], j] = 1
lo += [0] * ny + [0] * len(pairs) + [-np.inf] * ny + [0] * ny; hi += [MAX_IN] * ny + [1] * len(pairs) + [0] * ny + [1] * ny
for c in con: A[1 + ny + len(pairs) + ci[c], nx + ci[c]] = 1  # covered only when some chosen group holds it
obj = -np.array([cands[g] for g in C] + [COVER] * ny)
res = milp(obj, constraints=LinearConstraint(A.tocsr(), lo, hi), integrality=np.ones(nx + ny), bounds=Bounds(0, 1))
pick = sorted((C[j] for j in range(nx) if res.x[j] > 0.5), key=lambda g: -cands[g])
print(f'{len(C)} candidates; {res.message}')
L = 'ABCDEFGHIJKLMNOPQRST'
for k, g in zip(L, pick):
    p = pillars(g)
    print(k, ' + '.join(p), '|', ', '.join(c for c in g if c not in p), f'| strength {cands[g]:.2f}')
inn = collections.Counter(c for g in pick for c in g)
std = sorted(c for c in USABLE if GAMES[c] >= 7)
print('standard concepts (7+ games) in no group:', ', '.join(c for c in std if not inn[c]) or 'none', f'(of {len(std)})')
print('concepts in some group:', len(inn), 'of', len(USABLE), '| left out:', ', '.join(c for c in sorted(USABLE) if not inn[c]))
if '--write' in sys.argv:
    with open(W + 'groups.tsv', 'w') as o:
        o.write('group\tpillars\tothers\tstrength\n')
        for k, g in zip(L, pick):
            p = pillars(g); o.write(f"{k}\t{','.join(p)}\t{','.join(c for c in g if c not in p)}\t{cands[g]:.2f}\n")
