"""Step 3 (START_DESIGN-1-wheel.md): the ways to play that decks put together; they become our factions' archetypes.
Run from library/cards_db: python3 ../../factions/wheel/work/faction_archetypes.py
 -> factions/wheel/work/faction_archetypes.tsv (one row per group) and faction_archetypes.md (the same in plain words).
1. Concepts: every deck of decks.tsv, all its cards: a deck has a concept when one of its cards has it (concepts.tsv; a
   parent only on cards none of its children carry), plus five unit concepts against the card's game: unit, cheap unit,
   expensive unit (axes.py), strong for its cost and tough for its cost (above the game's line of strength or defence by cost).
2. Groups (association rules with lift, Agrawal et al. 1993): a group of 3 to 5 concepts where each concept, added in
   turn, is in the decks that hold the rest of the group more often than chance (its share of all the game's decks), by
   more than BEYOND; the whole group is in MIN_DECKS decks or more, of 2+ games. Every such group is listed; a group whose
   one-bigger group is in at least half as many decks is left for that bigger one.
3. Choosing: the group in the most decks first, then each next group in the most decks that brings at least NEW concepts
   no chosen group has yet; a concept can be in several groups.
4. Base concepts: the common concepts at least half of the group's decks have, more often than their game's decks do.
5. A deck fits a group when it has every concept of it. Factions are never used to make the groups: a faction fits its
   best BEST groups at FIT times its game's average share of their concepts or more."""
import collections, csv, os, sqlite3, sys
import numpy as np
sys.path.insert(0, os.getcwd())
import axes, deck_analysis, faction_asks

HERE = os.path.dirname(os.path.abspath(__file__))
BEYOND = 1.96  # a concept joins a group when it is with the whole group above chance by more than this (Claude's)
MIN_DECKS = 10  # a group must be whole in at least 10 decks, of 2+ games (Claude's)
MIN_SIZE, MAX_SIZE = 3, 5  # Kaptain
NEW = 2  # each chosen group brings at least 2 concepts no chosen group has yet (Claude's)
BASE = 0.5  # a common concept is a base of a group when at least half of its decks have it (Claude's)
FIT = 2.0  # a faction fits a group at twice its game's average share or more, its best BEST groups only (Claude's)
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

P = np.array([(d[2] > 0) for d in decks]).astype(float)  # deck -> has the concept
gi = np.array([d[0] for d in decks])
gbase = {g: P[gi == g].mean(0) for g in per_game}
B = np.array([gbase[g] for g in gi])  # each deck: how often its game's decks have each concept

def grow(S):
    """the concepts that can join group S: with the whole group above chance, in MIN_DECKS decks of 2+ games"""
    m = P[:, S].all(1)
    obs, exp = m @ P, m @ B
    z = np.where(exp > 0, (obs - exp) / np.sqrt(np.where(exp > 0, exp, 1)), 0)
    out = {}
    for D in np.nonzero((z > BEYOND) & (obs >= MIN_DECKS))[0]:
        if D in S: continue
        both = m * P[:, D] > 0
        if len(set(gi[both])) >= 2: out[int(D)] = int(obs[D])
    return out

found = {frozenset([i]): int(P[:, i].sum()) for i in range(len(nodes))}
level = list(found)
for size in range(2, MAX_SIZE + 1):
    new = {}
    for S in level:
        for D, n in grow(sorted(S)).items(): new[frozenset(S | {D})] = n
    found.update(new); level = list(new)
cands = {S: n for S, n in found.items() if MIN_SIZE <= len(S) <= MAX_SIZE}
cands = {S: n for S, n in cands.items()  # left for a one-bigger group in at least half as many decks
         if not any(len(T) == len(S) + 1 and S < T and 2 * n2 >= n for T, n2 in cands.items())}

groups, have = [], set()
for S, n in sorted(cands.items(), key=lambda kv: (-kv[1], -len(kv[0]), sorted(kv[0]))):
    if len(S - have) >= NEW:
        groups.append({'concepts': sorted(S), 'n': n}); have |= S
for gr in groups:
    gr['shared'] = [j for j in gr['concepts'] if sum(j in g2['concepts'] for g2 in groups) > 1]
    m = P[:, gr['concepts']].all(1) > 0
    gr['fit_decks'] = list(np.nonzero(m)[0])
    rate = P[m].mean(0); avg = B[m].mean(0)
    gr['base'] = sorted(((rate[j], j) for j in range(len(nodes)) if j not in gr['concepts'] and rate[j] >= BASE and rate[j] > avg[j]),
                        reverse=True)

def share(v, cs): return v[cs].sum() / v.sum() if v.sum() else 0
game_cards = {g: sum((cv[i] for i in pools[g]), np.zeros(len(nodes))) for g in games}
facs = sorted({(r['game'], r['faction']) for r in csv.DictReader(open('axes.tsv', encoding='utf-8'), delimiter='\t')})
fvec = {(g, fa): sum((cv[i] for i, v in pools[g].items() if fa in v[3]), np.zeros(len(nodes))) for g, fa in facs}
for gr in groups:
    cs = gr['concepts']
    gr['fratio'] = {f: (share(fvec[f], cs) / share(game_cards[f[0]], cs) if share(game_cards[f[0]], cs) else 0) for f in facs}
    gr['games'] = collections.Counter(decks[n][0] for n in gr['fit_decks'])
fits_f = collections.defaultdict(list)
for f in facs:
    for q in sorted(range(len(groups)), key=lambda q: -groups[q]['fratio'][f])[:BEST]:
        if groups[q]['fratio'][f] >= FIT: fits_f[q].append(f)
for q, gr in enumerate(groups):
    gr['facs'] = sorted(((gr['fratio'][f], f) for f in fits_f[q]), reverse=True)
    gr['near'] = sorted(((gr['fratio'][f], f) for f in facs), reverse=True)[:3]
    gr['key'] = f'G{q + 1:02d}'
nofit = [gr['key'] for gr in groups if not gr['facs']]
lonely = [f for f in facs if not any(f in fits_f[q] for q in range(len(groups)))]
left = [j for j in range(len(nodes)) if j not in have]
name = lambda j: plain.get(nodes[j], nodes[j])
def cname(gr, j): return name(j) + (' (also in another group)' if j in gr['shared'] else '')

with open(os.path.join(HERE, 'faction_archetypes.tsv'), 'w', encoding='utf-8') as o:
    o.write('group\tconcepts\tbase_concepts\tdecks\tgames\tfit_factions\tnearest_factions\n')
    for gr in groups:
        o.write('\t'.join([gr['key'], ','.join(nodes[j] for j in gr['concepts']),
                           ','.join(f'{nodes[j]}:{r:.2f}' for r, j in gr['base']), str(gr['n']),
                           ','.join(f'{g}:{k}' for g, k in sorted(gr['games'].items())),
                           '; '.join(f'{g}:{fa}:{r:.2f}' for r, (g, fa) in gr['facs']),
                           '; '.join(f'{g}:{fa}:{r:.2f}' for r, (g, fa) in gr['near'])]) + '\n')

with open(os.path.join(HERE, 'faction_archetypes.md'), 'w', encoding='utf-8') as o:
    o.write('# Step 3: the ways to play that decks put together (made by faction_archetypes.py)\n\n')
    o.write(f'{len(decks)} decks of {len(per_game)} games, {len(nodes)} concepts; {len(cands)} groups of {MIN_SIZE} to {MAX_SIZE} '
            f'concepts pass, {len(groups)} chosen. A deck fits a group when it has all its concepts. A faction fits its best '
            f'{BEST} groups at {FIT:g} times its game\'s average share of their concepts or more ("x2").\n\n')
    o.write('Deck card names the library does not know: ' +
            (', '.join(f'{g} {k}' for g, k in sorted(missing.items()) if k) or 'none') + '.\n\n')
    for gr in groups:
        o.write(f"## {gr['key']}: in {gr['n']} decks ({', '.join(f'{g} {k}' for g, k in sorted(gr['games'].items()))})\n")
        o.write('- Concepts: ' + '; '.join(cname(gr, j) for j in gr['concepts']) + '\n')
        o.write('- Base concepts (share of its decks): ' + ('; '.join(f'{name(j)} {r:.0%}' for r, j in gr['base'][:10]) or 'none') + '\n')
        o.write('- Decks: ' + '; '.join(f'{decks[n][1]} ({decks[n][0]})' for n in gr['fit_decks'][:6]) + '\n')
        o.write('- Factions that fit: ' + ('; '.join(f'{fa} ({g}, x{r:.1f})' for r, (g, fa) in gr['facs']) or
                'none; nearest ' + '; '.join(f'{fa} ({g}, x{r:.1f})' for r, (g, fa) in gr['near'])) + '\n\n')
    o.write('Concepts in no group: ' + ('; '.join(name(j) for j in left) or 'none') + '.\n\n')
    o.write('Groups no faction fits: ' + (', '.join(nofit) or 'none') + '.\n\n')
    o.write('Factions that fit no group: ' + (', '.join(f'{fa} ({g})' for g, fa in lonely) or 'none') + '.\n')
print(len(decks), 'decks;', len(cands), 'groups pass,', len(groups), 'chosen;', len(left), 'concepts in no group;',
      len(nofit), 'groups with no faction;', len(lonely), 'factions with no group; unknown deck names', sum(missing.values()))
