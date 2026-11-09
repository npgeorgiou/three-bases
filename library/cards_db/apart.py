"""Mechanics that real factions keep apart, and mechanics they keep together (for placing factions on the wheel).

Run from library/cards_db: python3 apart.py [top]   (default top 25)
For every concept, each real faction's share of cards with it, minus its game's average (so a game that marks a concept
often does not count). Concepts with at least MIN_SHARE of the cards in at least MIN_FACTIONS factions are compared in
pairs: the correlation over all factions. Most negative = factions strong in one are weak in the other (opposite sides of
the wheel); most positive = they come together (neighbours). Read card texts before trusting a pair: a concept is broad.
"""
import collections, math, sqlite3, sys
import faction_asks

MIN_SHARE, MIN_FACTIONS = 0.03, 10


def main(top=25):
    c = sqlite3.connect('cards.sqlite')
    games = sorted({g for (g,) in c.execute('select distinct game from card')})
    x = faction_asks.Ctx(c, games, None, {})
    con = collections.defaultdict(set)
    for card, k in c.execute('select card, concept from flat_concept'):
        con[card].add(k)
    rows = []  # (game, faction, {concept: share})
    for g in games:
        pool = x.pool(g)
        for fac in x.factions(g):
            ids = [i for i, v in pool.items() if fac in v[3]]
            cnt = collections.Counter(k for i in ids for k in con[i])
            rows.append((g, fac, {k: n / len(ids) for k, n in cnt.items()}))
    concepts = [k for k in {k for r in rows for k in r[2]} if sum(1 for r in rows if r[2].get(k, 0) >= MIN_SHARE) >= MIN_FACTIONS]
    cen = {}
    for k in concepts:
        for g in games:
            gr = [r for r in rows if r[0] == g]
            m = sum(r[2].get(k, 0) for r in gr) / len(gr) if gr else 0
            for r in gr: cen[(r[1], g, k)] = r[2].get(k, 0) - m
    vec = {k: [cen[(r[1], r[0], k)] for r in rows] for k in concepts}
    pairs = []
    for a_i, a in enumerate(sorted(concepts)):
        for b in sorted(concepts)[a_i + 1:]:
            va, vb = vec[a], vec[b]
            sa, sb = math.sqrt(sum(v * v for v in va)), math.sqrt(sum(v * v for v in vb))
            if sa and sb: pairs.append((sum(p * q for p, q in zip(va, vb)) / sa / sb, a, b))
    pairs.sort()
    print(f'{len(rows)} factions, {len(concepts)} concepts compared')
    print('KEPT APART (factions strong in one are weak in the other):')
    for r, a, b in pairs[:top]: print(f'  {r:+.2f}  {a} / {b}')
    print('KEPT TOGETHER:')
    for r, a, b in pairs[::-1][:top]: print(f'  {r:+.2f}  {a} / {b}')


if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 25)
