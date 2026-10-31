"""dump_lines.py: every deck network line of every game, to compare before and after a fix (PROCESS.md "Fixing a review").

  python3 dump_lines.py <out.tsv>                 write game, deck, from, to, kind, weight, reason for every deck of every game
  python3 dump_lines.py --diff <before> <after>   per game: lines and pairs before -> after; then every lost and every new
                                                  reason with how many lines and three examples (read them all)
  python3 dump_lines.py --table <out.tsv>         the same for links.sqlite (deck "-", reason with {A} and {B}), to diff the table
  python3 dump_lines.py --find <file> <text>      lines whose reason holds the text, counted per game (the same error elsewhere)
"""
import collections, csv, os, sys, sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))


def dump(out):
    sys.path.insert(0, HERE)
    import network, deck_analysis, mechanics
    c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))
    rows = [r for f in ('decks.tsv', os.path.join('cases', 'decks.tsv')) for r in csv.DictReader(open(os.path.join(HERE, f), encoding='utf-8'), delimiter='\t')]
    rows = list({(r['game'], r['deck']): r for r in rows}.values())
    with open(out, 'w', encoding='utf-8') as f:
        for r in rows:
            ids, _ = deck_analysis.parse_deck(c, r['game'], r['cards'])
            nodes, lines = network.network(c, r['game'], list(dict.fromkeys(ids)))
            for (a, b), ls in lines.items():
                for k, w, y in ls:
                    f.write('\t'.join((r['game'], r['deck'], mechanics.name(c, a), mechanics.name(c, b), k, f'{w:.3f}', y)) + '\n')
    print(out)


def table(out):
    c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite')); c.execute(f"attach database '{os.path.join(HERE, 'links.sqlite')}' as L")
    nm = dict(c.execute('select id, name from card'))
    with open(out, 'w', encoding='utf-8') as f:
        for g, a, b, k, w, t in c.execute('select l.game, l.a, l.b, p.kind, l.weight, p.text from L.link l join L.phrase p on p.id=l.phrase'):
            f.write('\t'.join((g, '-', nm[a], nm[b], k, f'{w:.3f}', t)) + '\n')
    print(out)


def load(path):
    return [l.rstrip('\n').split('\t') for l in open(path, encoding='utf-8')]


def diff(before, after):
    B, A = load(before), load(after)
    for g in sorted({r[0] for r in B + A}):
        b = [r for r in B if r[0] == g]; a = [r for r in A if r[0] == g]
        pb, pa = {tuple(r[1:4]) for r in b}, {tuple(r[1:4]) for r in a}
        print(f'{g}: lines {len(b)} -> {len(a)}, pairs {len(pb)} -> {len(pa)} ({len(pb - pa)} gone, {len(pa - pb)} new)')
    same = lambda why: '; also '.join(sorted(why.split('; also ')))  # the order of a pair's reasons is no change
    kb = {tuple(r[:5] + [same(r[6])]) for r in B}; ka = {tuple(r[:5] + [same(r[6])]) for r in A}
    for title, xs in (('GONE', kb - ka), ('NEW', ka - kb)):
        grp = collections.defaultdict(list)
        for g, d, x, y, k, why in xs: grp[(g, k, why)].append(f'{x} -> {y} ({d})')
        print(f'\n{title}')
        for (g, k, why), ex in sorted(grp.items(), key=lambda t: -len(t[1])):
            print(f'{len(ex):5} {g} | {k} | {why} | ' + '; '.join(ex[:3]))


def find(path, text):
    n = collections.Counter(r[0] for r in load(path) if text in r[6])
    print(dict(n) or 'nowhere')


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['--diff']: diff(a[1], a[2])
    elif a[:1] == ['--table']: table(a[1])
    elif a[:1] == ['--find']: find(a[1], ' '.join(a[2:]))
    else: dump(a[0])
