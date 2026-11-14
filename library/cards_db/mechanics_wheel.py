"""The wheel chat's mechanics (factions/START_DESIGN-1-wheel.md steps 1-2), measured on the library.
Reads factions/wheel/mechanics.tsv (key, sentence, concepts as in axes.py SPOKES, new rule). Needs links.sqlite (links.py).
Usage (from library/cards_db):
  mechanics_wheel.py measure          -> library/cards_db/wheel/measured.tsv: cards, games with 10+, top factions, biggest real
                                         faction's count (30+ wanted), radii it serves (share of its cards per radius)
  mechanics_wheel.py links            -> library/cards_db/wheel/links.tsv: per pair, linked x chance in all cards, and in real decks
  mechanics_wheel.py cards <file>     -> per mechanic 8 cards with text (for an agent to read)
  mechanics_wheel.py pairs A B <file> -> linked card pairs of A with B, their link reasons and texts (for an agent)"""
import collections, os, sqlite3, sys
import axes, faction_asks, mechanics, deck_analysis

HERE = os.path.dirname(os.path.abspath(__file__))
WHEEL = os.path.join(HERE, '..', '..', 'factions', 'wheel')
OUT = os.path.join(HERE, 'wheel')
GAMES = ('duelyst', 'faeria', 'gwent', 'inscryption', 'into_the_breach', 'marvel_snap', 'monster_train', 'runeterra', 'stormbound', 'sts1')


def load():
    """[(key, sentence, [concept@games], new rule)] from mechanics.tsv; a game name after an @-concept belongs to it"""
    out = []
    with open(os.path.join(WHEEL, 'mechanics.tsv'), encoding='utf-8') as f:
        next(f)
        for line in f:
            p = line.rstrip('\n').split('\t') + ['', '']
            cons = []
            for t in p[2].split(','):
                t = t.strip()
                if t in GAMES and cons and '@' in cons[-1]: cons[-1] += ',' + t
                elif t: cons.append(t)
            mk = []
            for t in (p[4] if len(p) > 4 else '').split(','):
                t = t.strip()
                if t in GAMES and mk and '@' in mk[-1]: mk[-1] += ',' + t
                elif t: mk.append(t)
            out.append((p[0], p[1], cons, p[3], mk))
    return out


def setup():
    c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))
    games = sorted({g for (g,) in c.execute('select distinct game from card')})
    x = faction_asks.Ctx(c, games, None, {})
    con, pools, stats = axes.tag(c, x, games)
    return c, games, x, con, pools, stats


def members(mechs, con, pools):
    """mechanic key -> {game: [card ids]}"""
    return {k: {g: [i for i in pools[g] if axes.counts(con[i], g, cons)] for g in pools} for k, _, cons, *_ in mechs}


def link_pairs():
    pairs = set()
    for a, b in sqlite3.connect(os.path.join(HERE, 'links.sqlite')).execute('select a, b from link'):
        if a != b: pairs.add((min(a, b), max(a, b)))
    return pairs


def measure(mechs, c, games, x, con, pools):
    mem = members(mechs, con, pools)
    spokes = [s for s in axes.SPOKES if s[0] not in axes.NUMERIC and s[0] != 'together']
    with open(os.path.join(OUT, 'measured.tsv'), 'w', encoding='utf-8') as f:
        f.write('key\tcards\tgames_10plus\tbiggest_faction\twith_makers\ttop_factions\tradii (share of its cards)\n')
        for k, _, _, _, mk in mechs:
            ids = [(g, i) for g in games for i in mem[k][g]]
            fac = collections.Counter((g, fn) for g, i in ids for fn in pools[g][i][3])
            share = lambda g, fn: fac[(g, fn)] / sum(1 for v in pools[g].values() if fn in v[3])
            top = sorted(fac, key=lambda t: -share(*t))[:4]
            rad = collections.Counter(s[0] for g, i in ids for s in spokes if axes.counts(con[i], g, s[4]))
            rads = [f'{r} {n / len(ids):.0%}' for r, n in rad.most_common() if n / len(ids) >= .2][:4] if ids else []
            big = fac.most_common(1)[0] if fac else (('', ''), 0)
            g0, f0 = big[0]
            made = sum(1 for i, v in pools[g0].items() if f0 in v[3] and (i in mem[k][g0] or (mk and axes.counts(con[i], g0, mk)))) if g0 else 0
            f.write(f"{k}\t{len(ids)}\t{sum(1 for g in games if len(mem[k][g]) >= 10)}\t{g0}: {f0} {big[1]}\t{made}\t"
                    + '; '.join(f'{g}: {fn} {fac[(g, fn)]} ({share(g, fn):.0%})' for g, fn in top) + '\t' + ', '.join(rads) + '\n')


def links(mechs, c, games, x, con, pools):
    """as axes.radius_links, with the mechanics in place of the radii"""
    saved = axes.SPOKES
    axes.SPOKES = [(k, 0, '', k, cons, '') for k, _, cons, *_ in mechs]
    pairs = link_pairs()
    deck_lists = collections.defaultdict(list)
    with open(os.path.join(HERE, 'decks.tsv'), encoding='utf-8') as f:
        next(f)
        for line in f:
            p = line.rstrip('\n').split('\t')
            if len(p) >= 4 and p[0] in pools:
                ids, _ = deck_analysis.parse_deck(c, p[0], p[3])
                deck_lists[p[0]].append({i for i in ids if i in pools[p[0]]})
    cards = axes.radius_links(games, pools, con, pairs)
    decks = axes.radius_links(games, pools, con, pairs, deck_lists)
    axes.SPOKES = saved
    keys = [m[0] for m in mechs]
    with open(os.path.join(OUT, 'links.tsv'), 'w', encoding='utf-8') as f:
        f.write('a\tb\tcards\tdecks\n')
        for n, a in enumerate(keys):
            for b in keys[n:]:
                f.write(f"{a}\t{b}\t{'' if cards[a][b] is None else cards[a][b]}\t{'' if decks[a][b] is None else decks[a][b]}\n")


def cards(mechs, c, games, x, con, pools, path, per=8):
    mem = members(mechs, con, pools)
    with open(path, 'w', encoding='utf-8') as f:
        for k, sent, *_ in mechs:
            f.write(f'\n## {k}: {sent}\n')
            ids = [(g, i) for g in games for i in mem[k][g]]
            step = max(1, len(ids) // per)
            for g, i in ids[::step][:per]:
                f.write(f"  {g} | {', '.join(pools[g][i][3]) or '-'} | {mechanics.name(c, i)} | {axes.text(i, 220)}\n")


def pairs(mechs, c, games, x, con, pools, a, b, path, per=12):
    mem = members(mechs, con, pools)
    A = {i for g in games for i in mem[a][g]}
    B = {i for g in games for i in mem[b][g]}
    L = sqlite3.connect(os.path.join(HERE, 'links.sqlite'))
    rows = L.execute('select l.game, l.a, l.b, p.text from link l join phrase p on p.id=l.phrase').fetchall()
    hit = [(g, s, t, ph) for g, s, t, ph in rows if s != t and ((s in A and t in B) or (s in B and t in A))]
    seen, out = set(), []
    for g, s, t, ph in sorted(hit, key=lambda r: (r[0], r[1])):
        if (s, t) in seen: continue
        seen.add((s, t)); out.append((g, s, t, ph))
    by_game = collections.defaultdict(list)
    for r in out: by_game[r[0]].append(r)
    pick = []
    while len(pick) < per and any(by_game.values()):
        for g in list(by_game):
            if by_game[g] and len(pick) < per: pick.append(by_game[g].pop(len(by_game[g]) // 2))
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f'\n## {a} x {b}: {len(out)} linked pairs\n')
        for g, s, t, ph in pick:
            na, nb = mechanics.name(c, s), mechanics.name(c, t)
            f.write(f"  {g} | A {na}: {axes.text(s, 160)}\n      B {nb}: {axes.text(t, 160)}\n      link: {ph.replace('{A}', na).replace('{B}', nb)}\n")


if __name__ == '__main__':
    m = load()
    ctx = setup()
    cmd = sys.argv[1]
    if cmd == 'measure': measure(m, *ctx[:4], ctx[4])
    elif cmd == 'links': links(m, *ctx[:4], ctx[4])
    elif cmd == 'cards': cards(m, *ctx[:4], ctx[4], sys.argv[2])
    elif cmd == 'pairs':
        for a, b in (q.split('+') for q in sys.argv[2].split(',')): pairs(m, *ctx[:4], ctx[4], a, b, sys.argv[3])
