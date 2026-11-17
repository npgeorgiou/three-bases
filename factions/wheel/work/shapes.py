"""Step 5 (START_DESIGN-1-wheel.md): the 20 shapes from today's numbers. Run from library/cards_db.
A candidate is 3-6 of one real faction's strong radii (value 1.2+), every radius joined to another of them (radius_links.tsv:
cards 1.2+ or decks 1.5+; spellpay by decks); its values are that faction's. A candidate fits an archetype of
factions/wheel/archetypes.tsv when every need of the archetype has a radius among the candidate's; a candidate that fits fewer
than 2 archetypes is no candidate. The 20 are picked from the candidates, at most one per real faction: every radius a strength
of 2-5 shapes, then as different from each other as possible. A radius fewer than 2 real factions are strong at is only kept under 5.
python3 ../../factions/wheel/work/shapes.py [--write]: prints the 20; --write writes factions/wheel/work/shapes.tsv."""
import csv, itertools, random, sys
NUM = {'strong', 'tough', 'tall', 'together'}  # strength, defence, a few big units, position and combos: need no join
AROWS = [r for r in csv.DictReader(open('../../factions/wheel/archetypes.tsv'), delimiter='\t') if r['can exist'] == 'yes']
ARCH = [[set(n.split('/')) for n in r['radii of each need'].split('; ')] for r in AROWS]  # per archetype: the radii each need can use
MIN_FITS = 2
def fits(sh):
    """the archetypes a shape fits: every need has a radius among the shape's"""
    return [a for a, needs in enumerate(ARCH) if all(n & set(sh) for n in needs)]
STRONG, LO, HI, N = 1.2, 2, 5, 20
RL = {}
for x in csv.DictReader(open('wheel/radius_links.tsv'), delimiter='\t'):
    c, d = float(x['cards'] or 0), float(x['decks'] or 0)
    RL[(x['a'], x['b'])] = RL[(x['b'], x['a'])] = (d if 'spellpay' in (x['a'], x['b']) else c, d)
joined = lambda a, b: (lambda n: n[0] >= 1.2 or n[1] >= 1.5)(RL.get((a, b), (0, 0)))
def holds(s):
    r = [a for a in s if a not in NUM]
    return len(r) >= 2 and all(any(joined(a, b) for b in r if b != a) for a in r)
cands, facs = [], []
for r in csv.DictReader(open('axes.tsv'), delimiter='\t'):
    if r['mode'] != 'cards': continue
    v = {k[:-6]: float(x) for k, x in r.items() if k.endswith('_value') and x and float(x) >= STRONG}
    for n in range(3, min(6, len(v)) + 1):
        for s in itertools.combinations(sorted(v), n):
            if holds(s) and len(fits(s)) >= MIN_FITS: cands.append((f"{r['game']}: {r['faction']}", {k: v[k] for k in s}))
RADII = sorted({a for a, b in RL} | NUM)
# a radius fewer than LO real factions are strong at can't be in LO shapes: it is only kept under HI
FEW = {a for a in RADII if len({f for f, sh in cands if a in sh}) < LO}
def score(pick):
    cnt = {a: 0 for a in RADII}
    for i in pick:
        for a in cands[i][1]: cnt[a] += 1
    bad = sum(max(0, LO - c) * (a not in FEW) + max(0, c - HI) for a, c in cnt.items())
    same = sum((len(set(cands[i][1]) & set(cands[j][1])) / len(set(cands[i][1]) | set(cands[j][1]))) ** 2 for i, j in itertools.combinations(pick, 2))
    return bad * 100 + same + 100 * (len(pick) - len({cands[i][0] for i in pick}))
def search(seed):
    rnd = random.Random(seed); pick = rnd.sample(range(len(cands)), N); s = score(pick); t = 2.0
    for step in range(60000):
        k = rnd.randrange(N); new = pick[:]; new[k] = rnd.randrange(len(cands))
        if new[k] in pick: continue
        ns = score(new)
        if ns <= s or rnd.random() < 2.718 ** ((s - ns) / t): pick, s = new, ns
        t = max(0.01, t * 0.99985)
    return s, pick
best = min(search(seed) for seed in range(4))
s, pick = best
cnt = {a: sum(a in cands[i][1] for i in pick) for a in RADII}
print(f'{len(cands)} candidates; score {s:.2f} (coverage misses x100 + sameness)')
rows = sorted((cands[i] for i in pick), key=lambda c: -max(c[1].values()))
for k, (f, sh) in zip('ABCDEFGHIJKLMNOPQRST', rows):
    print(k, ','.join(f'{a}={v:.1f}' for a, v in sorted(sh.items(), key=lambda t: -t[1])), '|', f, '| fits:', ', '.join(AROWS[a]['key'] for a in fits(sh)))
L = 'ABCDEFGHIJKLMNOPQRST'; order = sorted(pick, key=lambda x: -max(cands[x][1].values()))
fit = {AROWS[a]['key'] for i in pick for a in fits(cands[i][1])}
print('archetypes that fit no shape:', ', '.join(r['key'] for r in AROWS if r['key'] not in fit) or 'none')
miss = [f'{a} in {c} shapes' for a, c in cnt.items() if (c < LO and a not in FEW) or c > HI]
miss += [f'{f} twice' for f in {cands[i][0] for i in pick} if sum(cands[j][0] == f for j in pick) > 1]
print('rules missed:', '; '.join(miss) or 'none', '| strong at by too few real factions:', ', '.join(sorted(FEW)))
print('radius in how many shapes:', ', '.join(f'{a} {c}' for a, c in sorted(cnt.items(), key=lambda t: -t[1])))
if '--write' in sys.argv:
    with open('../../factions/wheel/work/shapes.tsv', 'w') as o:
        for k, (f, sh) in zip('ABCDEFGHIJKLMNOPQRST', rows):
            o.write(k + '\t' + ','.join(f'{a}={v:.1f}' for a, v in sorted(sh.items(), key=lambda t: -t[1])) + '\n')
