"""The wheel's link counts (factions/START_DESIGN-1-wheel.md step 4): for every two concepts of
factions/wheel/work/concepts.tsv (usable, helpers and out), how much more often than chance their cards are linked (cards), how much more often real decks heavy in one hold the other (decks), in how many games
real cards link them (games), and the linked card pairs as a level that grows slowly (level, Kaptain: a pairing rare in the
ten games can be splendid on this board); a link counts only through what of each card made it
(concept_tags.pair_links). Needs links.sqlite (links.py). Also
rare (for a pair chance gives under 5 linked pairs in every game: all linked pairs over all chance), which one makes and which one uses (makes: the share of the pair's links where a's card is the one that sets off or feeds
b's card) and the three most common link texts.
Usage (from library/cards_db): mechanics_wheel.py links --concepts -> wheel/concept_links.tsv, then cases/wheel.tsv"""
import collections, csv, math, os, sqlite3, sys
import concept_tags, faction_asks, deck_analysis

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'wheel')


def setup():
    c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))
    games = sorted({g for (g,) in c.execute('select distinct game from card')})
    x = faction_asks.Ctx(c, games, None, {})
    con, pools, stats = concept_tags.tag(c, x, games)
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
                        got |= {(ka, kb) for ka in concept_tags.side_keys(i, si, r['game'], keys, con) for kb in concept_tags.side_keys(j, sj, r['game'], keys, con)}
            hit = any(r['a'] in ('*', ka) and r['b'] in ('*', kb) for ka, kb in got)
            if hit != (r['expect'] == 'count'):
                bad.append(f"{r['id']} {r['from']} x {r['to']} {r['a']}+{r['b']} {r['expect']}: counts for {', '.join(sorted(f'{a}+{b}' for a, b in got)) or 'nothing'}")
    return bad


def links(ckeys, c, games, x, con, pools):
    """per pair of concepts: cards, decks, games, level, rare, makes and texts; then the cases"""
    pairs = concept_tags.link_pairs()
    deck_lists = collections.defaultdict(list)
    with open(os.path.join(HERE, 'decks.tsv'), encoding='utf-8') as f:
        next(f)
        for line in f:
            p = line.rstrip('\n').split('\t')
            if len(p) >= 4 and p[0] in pools:
                ids, _ = deck_analysis.parse_deck(c, p[0], p[3])
                deck_lists[p[0]].append({i for i in ids if i in pools[p[0]]})
    seen, plain, pooled = collections.Counter(), collections.Counter(), {}
    cards = concept_tags.pair_links(ckeys, games, pools, con, pairs, seen=seen, plain=plain, pooled=pooled)
    decks = concept_tags.pair_links(ckeys, games, pools, con, pairs, deck_lists)
    bad = case_failures(c, con, ckeys, pairs)
    keys = [m[0] for m in ckeys]
    made, texts = directed(c, con, ckeys)
    with open(os.path.join(OUT, 'concept_links.tsv'), 'w', encoding='utf-8') as f:
        f.write('a\tb\tcards\tdecks\tgames\tlevel\trare\tmakes\ttexts\n')
        for n, a in enumerate(keys):
            for b in keys[n:]:
                t = tuple(sorted((a, b)))
                if not plain[t] and cards[a][b] is None and decks[a][b] is None: continue
                row = f"{a}\t{b}\t{'' if cards[a][b] is None else cards[a][b]}\t{'' if decks[a][b] is None else decks[a][b]}\t{seen[t]}\t{level(plain[t])}"
                ab, ba = made[(a, b)], made[(b, a)]
                row += f"\t{pooled.get((a, b), '')}\t{round(ab / (ab + ba), 2) if ab + ba else ''}\t{' | '.join(x for x, _ in texts[t].most_common(3))}"
                f.write(row + '\n')
    print('cases/wheel.tsv: ' + ('all pass' if not bad else f'{len(bad)} fail\n' + '\n'.join(bad)))


def directed(c, con, keys):
    """per ordered pair of concepts: links where a's card sets off or feeds b's card ({A} acts, {B} answers); per pair the link texts"""
    made, texts = collections.Counter(), collections.defaultdict(collections.Counter)
    L = sqlite3.connect(os.path.join(HERE, 'links.sqlite'))
    for g, a, b, sa, sb, kind, text in L.execute('select l.game, a, b, a_ab, b_ab, p.kind, p.text from link l join phrase p on p.id=l.phrase where a != b'):
        ka, kb = concept_tags.side_keys(a, sa, g, keys, con), concept_tags.side_keys(b, sb, g, keys, con)
        for x in ka:
            for y in kb:
                made[(x, y)] += 1
                texts[tuple(sorted((x, y)))][f'{kind}: {text}'] += 1
    return made, texts


def concepts(con):
    """every concept of concepts.tsv as a key (name, _, _, _, {name})"""
    with open(os.path.join(HERE, '..', '..', 'factions', 'wheel', 'work', 'concepts.tsv'), encoding='utf-8') as f:
        names = [r['concept'] for r in csv.DictReader(f, delimiter='\t')]
    return [(n, 0, '', n, {n}) for n in names]


def level(links):
    """the linked card pairs as a level that grows slowly: 0 pairs = 0, 1 = 1, 10 = 2, 100 or more = 3"""
    return 0 if not links else round(min(3, 1 + math.log10(links)), 2)


if __name__ == '__main__':
    if sys.argv[1:] != ['links', '--concepts']: sys.exit('usage: mechanics_wheel.py links --concepts')
    ctx = setup()
    links(concepts(ctx[3]), *ctx[:4], ctx[4])
