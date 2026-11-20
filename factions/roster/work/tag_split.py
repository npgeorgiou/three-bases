"""tag_split.py: the second reading of the mixed families of tag_verdicts.tsv. Each is split by the one detail of its groups
(whom it acts on, from where, when it fires, what gave it, or the game) that best keeps the cards read right apart from those
read wrong; values whose read cards agree form one half, values with no card read form the half "not read". Each half gets 5
cards: the ones already read keep their verdict, the rest are new reads. Writes tag_reads2.tsv (concept, family, why, half,
group, game, card, card id, verdict, reader why; verdict filled for cards read before). Needs tag_cards.tsv (tag_check.py)."""
import collections, csv, glob, os, random, re
HERE = os.path.dirname(os.path.abspath(__file__))
v = {}
for f in sorted(glob.glob(os.path.join(HERE, 'reads', 'batch_*.verdicts.tsv'))):
    for r in csv.reader(open(f), delimiter='\t'):
        if r and r[0].strip().isdigit(): v[r[0].strip()] = (r[1].strip(), r[2].strip() if len(r) > 2 else '')


def cls(x):  # the class of a verdict: right, wrong as what, unsure
    a = x.lower()
    if a.startswith('right'): return 'right'
    if a.startswith('wrong'): return 'wrong: ' + re.sub(r'^wrong:?\s*(should be)?\s*', '', a).strip()[:30]
    return 'unsure'


mixed = [(r['concept'], r['family'], r['why suspect']) for r in csv.DictReader(open(os.path.join(HERE, 'tag_verdicts.tsv')), delimiter='\t') if r['result'] == 'mixed']
cards = collections.defaultdict(list)
for r in csv.DictReader(open(os.path.join(HERE, 'tag_cards.tsv')), delimiter='\t'): cards[(r['concept'], r['family'], r['why suspect'])].append(r)
rnd = random.Random(0)
out = []
for fam in mixed:
    cs = cards.get(fam, [])
    if not cs: continue  # the family is gone after the fixes
    def detail(r, d): g = r['group'].split(' | '); return r['game'] if d == 5 else (g[d] if d < len(g) else '-')
    read = [r for r in cs if r['card id'] in v]
    best = None
    for d in (2, 3, 4, 5, 6):  # on (kind/side/pick), zone, when, game, given by
        by = collections.defaultdict(collections.Counter)
        for r in read: by[detail(r, d)][cls(v[r['card id']][0])] += 1
        pure = sum(c.most_common(1)[0][1] for c in by.values())  # read cards whose value's majority agrees with them
        if best is None or pure > best[0] or (pure == best[0] and len(by) < best[2]): best = (pure, d, len(by))
    d = best[1]
    maj = {}
    for r in read: maj.setdefault(detail(r, d), collections.Counter())[cls(v[r['card id']][0])] += 1
    half = lambda r: (('right' if maj[detail(r, d)].most_common(1)[0][0] == 'right' else 'wrong') if detail(r, d) in maj else 'not read')
    halves = collections.defaultdict(list)
    for r in cs: halves[half(r)].append(r)
    name = {2: 'on', 3: 'zone', 4: 'when', 5: 'game', 6: 'given by'}[d]
    for h, rs in sorted(halves.items()):
        vals = sorted({detail(r, d) for r in rs})
        label = f'{h}: {name} in {", ".join(vals)[:120]}'
        old = [r for r in rs if r['card id'] in v and r['card id'] not in {x[7] for x in out}]
        new = [r for r in rs if r['card id'] not in v]
        pick = old[:5] + rnd.sample(new, min(len(new), 5 - min(5, len(old))))
        for r in pick:
            x = v.get(r['card id'], ('', ''))
            out.append([*fam, label, r['group'], r['game'], r['card'], r['card id'], *x])
with open(os.path.join(HERE, 'tag_reads2.tsv'), 'w') as f:
    f.write('concept\tfamily\twhy suspect\thalf\tgroup\tgame\tcard\tcard id\tverdict\treader why\n')
    for r in out: f.write('\t'.join(r) + '\n')
print(len({tuple(r[:4]) for r in out}), 'halves,', sum(1 for r in out if not r[8]), 'cards to read')
