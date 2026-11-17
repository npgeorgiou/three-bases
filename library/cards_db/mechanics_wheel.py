"""The wheel's link counts (factions/START_DESIGN-1-wheel.md step 2): for every two radii, how much more often than chance
their cards are linked (cards), how much more often real decks heavy in one hold the other (decks), in how many games
real cards link them (games), and the linked card pairs as a level that grows slowly (level, Kaptain: a pairing rare in the
ten games can be splendid on this board); a link counts only through what of each card made it
(axes.radius_links). Needs links.sqlite (links.py).
Usage (from library/cards_db): mechanics_wheel.py links --radii -> wheel/radius_links.tsv, then cases/wheel.tsv"""
import collections, csv, math, os, sqlite3, sys
import axes, faction_asks, deck_analysis

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'wheel')


def setup():
    c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))
    games = sorted({g for (g,) in c.execute('select distinct game from card')})
    x = faction_asks.Ctx(c, games, None, {})
    con, pools, stats = axes.tag(c, x, games)
    return c, games, x, con, pools, stats


def case_failures(c, con, keys, pairs):
    """cases/wheel.tsv: a linked pair that must (count) or must not (none) count for key a on card from and b on card to
    ('*': any); only the cases whose keys are in this run"""
    names = [k[0] for k in keys]
    bad = []
    with open(os.path.join(HERE, 'cases', 'wheel.tsv'), encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            if any(k != '*' and k not in names for k in (r['a'], r['b'])): continue
            ids = lambda n: [i for (i,) in c.execute('select id from card where game=? and name=?', (r['game'], n))]
            got = set()
            for i in ids(r['from']):
                for j in ids(r['to']):
                    for sa, sb in pairs.get((min(i, j), max(i, j)), ()):
                        si, sj = (sa, sb) if i < j else (sb, sa)
                        got |= {(ka, kb) for ka in axes.side_keys(i, si, r['game'], keys, con) for kb in axes.side_keys(j, sj, r['game'], keys, con)}
            hit = any(r['a'] in ('*', ka) and r['b'] in ('*', kb) for ka, kb in got)
            if hit != (r['expect'] == 'count'):
                bad.append(f"{r['id']} {r['from']} x {r['to']} {r['a']}+{r['b']} {r['expect']}: counts for {', '.join(sorted(f'{a}+{b}' for a, b in got)) or 'nothing'}")
    return bad


def links(spokes, c, games, x, con, pools):
    """per pair of keys (radii): cards, decks, games, level; then the cases"""
    saved = axes.SPOKES
    axes.SPOKES = [(k, 0, '', k, cons, '') for k, _, cons, *_ in spokes]
    pairs = axes.link_pairs()
    deck_lists = collections.defaultdict(list)
    with open(os.path.join(HERE, 'decks.tsv'), encoding='utf-8') as f:
        next(f)
        for line in f:
            p = line.rstrip('\n').split('\t')
            if len(p) >= 4 and p[0] in pools:
                ids, _ = deck_analysis.parse_deck(c, p[0], p[3])
                deck_lists[p[0]].append({i for i in ids if i in pools[p[0]]})
    seen, plain = collections.Counter(), collections.Counter()
    cards = axes.radius_links(games, pools, con, pairs, seen=seen, plain=plain)
    decks = axes.radius_links(games, pools, con, pairs, deck_lists)
    bad = case_failures(c, con, axes.SPOKES, pairs)
    axes.SPOKES = saved
    keys = [m[0] for m in spokes]
    with open(os.path.join(OUT, 'radius_links.tsv'), 'w', encoding='utf-8') as f:
        f.write('a\tb\tcards\tdecks\tgames\tlevel\n')
        for n, a in enumerate(keys):
            for b in keys[n:]:
                f.write(f"{a}\t{b}\t{'' if cards[a][b] is None else cards[a][b]}\t{'' if decks[a][b] is None else decks[a][b]}\t{seen[tuple(sorted((a, b)))]}\t{level(plain[tuple(sorted((a, b)))])}\n")
    print('cases/wheel.tsv: ' + ('all pass' if not bad else f'{len(bad)} fail\n' + '\n'.join(bad)))


def level(links):
    """the linked card pairs as a level that grows slowly: 0 pairs = 0, 1 = 1, 10 = 2, 100 or more = 3"""
    return 0 if not links else round(min(3, 1 + math.log10(links)), 2)


def radii():
    """the radii of axes.SPOKES that are cards, not numbers, in the shape of load()"""
    return [(s[0], s[3], s[4], '', []) for s in axes.SPOKES if s[0] not in axes.NUMERIC and s[0] != 'together']


if __name__ == '__main__':
    if sys.argv[1:] != ['links', '--radii']: sys.exit('usage: mechanics_wheel.py links --radii (the concepts come in wheel step 5)')
    ctx = setup()
    links(radii(), *ctx[:4], ctx[4])
