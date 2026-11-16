"""The wheel chat's mechanics (factions/START_DESIGN-1-wheel.md steps 1-2), measured on the library.
Reads factions/wheel/mechanics.tsv (key, sentence, concepts as in axes.py SPOKES, new rule). Needs links.sqlite (links.py).
Usage (from library/cards_db):
  mechanics_wheel.py measure          -> library/cards_db/wheel/measured.tsv: cards, games with 10+, top factions, biggest real
                                         faction's count (30+ wanted), radii it serves (share of its cards per radius)
  mechanics_wheel.py links            -> library/cards_db/wheel/links.tsv: per pair, linked x chance in all cards (a link counts
                                         for a mechanic only through what of each card made it: links.sqlite a_ab, b_ab), and in real
                                         decks; links = the linked card pairs made by the two mechanics, level = that
                                         count growing slowly (level()); runs cases/wheel.tsv
  mechanics_wheel.py cards <file>     -> per mechanic 8 cards with text (for an agent to read)
  mechanics_wheel.py pairs A+B,C+D <file> -> linked card pairs of A with B, their link reasons and texts (for an agent)
  --radii after the command: the wheel's radii (axes.SPOKES, not the numbers) in place of the mechanics; links writes
                                         library/cards_db/wheel/radius_links.tsv (step 2)"""
import collections, csv, math, os, sqlite3, sys
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
    """linked card pair (lower id first) -> {(what of the first card made a link, what of the second)}"""
    pairs = collections.defaultdict(set)
    for a, b, sa, sb in sqlite3.connect(os.path.join(HERE, 'links.sqlite')).execute('select a, b, a_ab, b_ab from link'):
        if a != b: pairs[(min(a, b), max(a, b))].add((sa, sb) if a < b else (sb, sa))
    return pairs


def case_failures(c, con, keys, pairs):
    """cases/wheel.tsv: a linked pair that must (count) or must not (none) count for mechanic a on card from and b on card to
    ('*': any); only the cases whose keys are in this run (the mechanics or the radii)"""
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
    plain = collections.Counter()
    cards = axes.radius_links(games, pools, con, pairs, plain=plain)
    decks = axes.radius_links(games, pools, con, pairs, deck_lists)
    bad = case_failures(c, con, axes.SPOKES, pairs)
    axes.SPOKES = saved
    keys = [m[0] for m in mechs]
    with open(os.path.join(OUT, 'radius_links.tsv' if keys == [r[0] for r in radii()] else 'links.tsv'), 'w', encoding='utf-8') as f:
        f.write('a\tb\tcards\tdecks\tlinks\tlevel\n')
        for n, a in enumerate(keys):
            for b in keys[n:]:
                k = plain[tuple(sorted((a, b)))]
                f.write(f"{a}\t{b}\t{'' if cards[a][b] is None else cards[a][b]}\t{'' if decks[a][b] is None else decks[a][b]}\t{k}\t{level(k)}\n")
    print('cases/wheel.tsv: ' + ('all pass' if not bad else f'{len(bad)} fail\n' + '\n'.join(bad)))


def level(links):
    """the plain count of linked card pairs as a level that grows slowly (Kaptain, 16 Nov 2026: a pairing rare in the ten
    games can be splendid on this board): 0 links = 0, 1 = 1, 10 = 2, 100 or more = 3"""
    return 0 if not links else round(min(3, 1 + math.log10(links)), 2)


def cards(mechs, c, games, x, con, pools, path, per=8):
    mem = members(mechs, con, pools)
    with open(path, 'w', encoding='utf-8') as f:
        for k, sent, *_ in mechs:
            f.write(f'\n## {k}: {sent}\n')
            ids = [(g, i) for g in games for i in mem[k][g]]
            step = max(1, len(ids) // per)
            for g, i in ids[::step][:per]:
                f.write(f"  {g} | {', '.join(pools[g][i][3]) or '-'} | {mechanics.name(c, i)} | {axes.text(i, 220)}\n")


def pairs(mechs, c, games, x, con, pools, a, b, path, per=int(os.environ.get("PER", 12))):
    mem = members(mechs, con, pools)
    A = {i for g in games for i in mem[a][g]}
    B = {i for g in games for i in mem[b][g]}
    L = sqlite3.connect(os.path.join(HERE, 'links.sqlite'))
    rows = L.execute('select l.game, l.a, l.b, p.text, l.a_ab, l.b_ab from link l join phrase p on p.id=l.phrase').fetchall()
    keys = [(k, 0, '', k, cons, '') for k, _, cons, *_ in mechs if k in (a, b)]
    on = lambda i, src, g, m: m in axes.side_keys(i, src, g, keys, con)  # the link counts for m through what of the card made it
    hit = [(g, s, t, ph) for g, s, t, ph, sa, sb in rows if s != t and ((s in A and t in B and on(s, sa, g, a) and on(t, sb, g, b))
                                                                       or (s in B and t in A and on(s, sa, g, b) and on(t, sb, g, a)))]
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


def radii():
    """the radii of axes.SPOKES that are cards, not numbers, in the shape of load()"""
    return [(s[0], s[3], s[4], '', []) for s in axes.SPOKES if s[0] not in axes.NUMERIC and s[0] != 'together']


if __name__ == '__main__':
    RADII = '--radii' in sys.argv
    if RADII: sys.argv.remove('--radii')
    m = radii() if RADII else load()
    ctx = setup()
    cmd = sys.argv[1]
    if cmd == 'measure': measure(m, *ctx[:4], ctx[4])
    elif cmd == 'links': links(m, *ctx[:4], ctx[4])
    elif cmd == 'cards': cards(m, *ctx[:4], ctx[4], sys.argv[2])
    elif cmd == 'pairs':
        for a, b in (q.split('+') for q in sys.argv[2].split(',')): pairs(m, *ctx[:4], ctx[4], a, b, sys.argv[3])
