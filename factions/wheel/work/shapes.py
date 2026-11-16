"""Step 3 (START_DESIGN-1-wheel.md): the 20 shapes from today's numbers. Run from library/cards_db.
A candidate is 3-6 of one real faction's strong radii (value 1.2+), every radius joined to another of them (radius_links.tsv:
cards 1.2+ or decks 1.5+; spellpay by decks); its values are that faction's. The 20 are picked from the candidates, at most one
per real faction: every radius a strength of 2-5 shapes, each shape carries at most 2 archetypes of factions/wheel/archetypes.tsv
through its main strengths (the highest and second value), each archetype carried by 2-3 shapes, then as different from each other as possible. "One chosen" is left out: choosing
the target is the default (Kaptain, 16 Nov 2026).
python3 ../../factions/wheel/work/shapes.py [--write]: prints the 20; --write writes factions/wheel/work/shapes.tsv."""
import csv, itertools, random, sys
NUM = {'strong', 'tough', 'together'}  # shape-only radii: give a faction its shape, joined to nothing
OUT = {'one'}
AROWS = list(csv.DictReader(open('../../factions/wheel/archetypes.tsv'), delimiter='\t'))
ARCH = [r['radii (main strength of 1+ shape)'].split(',') for r in AROWS]
def carry(pick, caps):
    # which archetypes each picked shape carries: at most 2 per shape; first up to 2 shapes per archetype, then up to 3
    got = {a: [] for a in range(len(ARCH))}; fill = {i: 0 for i in pick}
    def put(i, seen):
        for a in range(len(ARCH)):
            if a in seen or not set(ARCH[a]) & main[i] or i in got[a]: continue
            seen.add(a)
            if len(got[a]) < cap: got[a].append(i); return True
            for j in got[a]:
                if j != i and fill[j] >= 0 and put(j, seen): got[a].remove(j); got[a].append(i); return True
        return False
    for cap in caps:
        for i in pick:
            while fill[i] < 2 and put(i, set()): fill[i] += 1
    return got
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
    v = {k[:-6]: float(x) for k, x in r.items() if k.endswith('_value') and x and float(x) >= STRONG and k[:-6] not in OUT}
    for n in range(3, min(6, len(v)) + 1):
        for s in itertools.combinations(sorted(v), n):
            if holds(s): cands.append((f"{r['game']}: {r['faction']}", {k: v[k] for k in s}))
RADII = sorted(({a for a, b in RL} | NUM) - OUT)
main = [set(sorted(sh, key=lambda a: -sh[a])[:2]) for f, sh in cands]
def score(pick):
    cnt = {a: 0 for a in RADII}
    for i in pick:
        for a in cands[i][1]: cnt[a] += 1
    bad = sum(max(0, 2 - len(g)) for g in carry(pick, (2,)).values()) + sum(max(0, LO - c) + max(0, c - HI) for a, c in cnt.items() if a not in NUM)
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
    print(k, ','.join(f'{a}={v:.1f}' for a, v in sorted(sh.items(), key=lambda t: -t[1])), '|', f)
got = carry(pick, (2, 3))
for a, g in got.items(): print(AROWS[a]['key'], ''.join(sorted('ABCDEFGHIJKLMNOPQRST'[[cands[x] for x in sorted(pick, key=lambda x: -max(cands[x][1].values()))].index(cands[i])] for i in g)))
print('radius in how many shapes:', ', '.join(f'{a} {c}' for a, c in sorted(cnt.items(), key=lambda t: -t[1])))
if '--write' in sys.argv:
    with open('../../factions/wheel/work/shapes.tsv', 'w') as o:
        for k, (f, sh) in zip('ABCDEFGHIJKLMNOPQRST', rows):
            o.write(k + '\t' + ','.join(f'{a}={v:.1f}' for a, v in sorted(sh.items(), key=lambda t: -t[1])) + '\n')
