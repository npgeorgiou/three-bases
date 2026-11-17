"""Step 6 (START_DESIGN-1-wheel.md): the 20 groups from the directions (radii) and the card links between them. Run from
library/cards_db. Directions with no card links (strength, defence, position and combos) are in no group.
A group is 3-6 directions, each joined (wheel/radius_links.tsv: cards 1.2+ or decks 1.5+; spellpay by decks) to at least
2 others of it; its pillars are its two most strongly linked directions. A link's strength is how much more often than
chance real cards link the two (cards; a join by decks alone counts 1.2); a group's strength is the average over all its
pairs of log2 of that (a pair with no join counts 0). Every group of 3-6 directions is a candidate. The 20 are picked by
one exact solver (scipy milp): two groups share at most one direction, every direction is in 2-5 groups; the most total
strength. A direction joined to only 2-3 others can be in one group only (sharing one direction at most) and needs 1; one
joined to fewer than 2 others is in none (printed).
python3 ../../factions/wheel/work/groups.py [--write]: prints the 20 and how many groups each direction is in;
--write writes factions/wheel/work/groups.tsv."""
import csv, collections, itertools, math, sys
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix

N, LO, HI = 20, 2, 5
f = lambda x: float(x or 0)
link = {}
for r in csv.DictReader(open('wheel/radius_links.tsv'), delimiter='\t'):
    a, b = r['a'], r['b']
    if a == b: continue
    c = f(r['decks']) if 'spellpay' in (a, b) else f(r['cards'])
    if c >= 1.2: w = c
    elif f(r['decks']) >= 1.5: w = 1.2
    else: continue
    link[(a, b)] = link[(b, a)] = w
DIRS = sorted({a for a, b in link})
DEG = collections.Counter(a for a, b in link)
lw = lambda a, b: math.log2(link[(a, b)]) if (a, b) in link else 0.0
strength = lambda g: sum(lw(a, b) for a, b in itertools.combinations(g, 2)) / (len(g) * (len(g) - 1) / 2)
pillars = lambda g: max(((a, b) for a, b in itertools.combinations(g, 2) if (a, b) in link), key=lambda p: link[p])
C = [g for n in range(3, 7) for g in itertools.combinations(DIRS, n)
     if all(sum((x, y) in link for y in g if y != x) >= 2 for x in g)]
S = [strength(g) for g in C]
di = {d: i for i, d in enumerate(DIRS)}
pairs = list(itertools.combinations(DIRS, 2)); pi = {p: i for i, p in enumerate(pairs)}
A = lil_matrix((1 + len(DIRS) + len(pairs), len(C)))
A[0, :] = 1
for j, g in enumerate(C):
    for d in g: A[1 + di[d], j] = 1
    for p in itertools.combinations(g, 2): A[1 + len(DIRS) + pi[p], j] = 1
lo = [N] + [min(LO, DEG[d] // 2) for d in DIRS] + [0] * len(pairs); hi = [N] + [HI] * len(DIRS) + [1] * len(pairs)
res = milp(-np.array(S), constraints=LinearConstraint(A.tocsr(), lo, hi), integrality=np.ones(len(C)), bounds=Bounds(0, 1))
pick = sorted((j for j in range(len(C)) if res.x[j] > 0.5), key=lambda j: -S[j])
print(f'{len(C)} candidates; {res.message}')
L = 'ABCDEFGHIJKLMNOPQRST'
rows = []
for k, j in zip(L, pick):
    g = C[j]; p = pillars(g)
    rows.append((k, p, [d for d in g if d not in p], S[j]))
    print(k, ' + '.join(p), '|', ', '.join(d for d in g if d not in p), f'| strength {S[j]:.2f}')
inn = collections.Counter(d for j in pick for d in C[j])
print('in no group (joined to fewer than 2 others):', ', '.join(d for d in DIRS if DEG[d] < 2) or 'none')
print('groups per direction:', ', '.join(f'{d} {inn[d]}' for d in sorted(DIRS, key=lambda d: -inn[d])))
if '--write' in sys.argv:
    with open('../../factions/wheel/work/groups.tsv', 'w') as o:
        o.write('group\tpillars\tothers\tstrength\n')
        for k, p, rest, s in rows: o.write(f"{k}\t{','.join(p)}\t{','.join(rest)}\t{s:.2f}\n")
