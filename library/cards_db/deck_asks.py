"""Faction design questions over the real decks of decks.tsv (run through ask.py): how players build with a faction, which
cards they put together, which mechanics they choose more than the card pool offers. Every deck counts once; copies of a card
in one deck count once. Only games with decks in decks.tsv answer."""
import collections, csv, os
import deck_analysis, mechanics

HERE = os.path.dirname(os.path.abspath(__file__))


def decks(x, game):
    """every deck of one game: (name, set of player card ids), parsed the way axes.py parses them"""
    if not hasattr(x, '_decks'): x._decks = {}
    if game not in x._decks:
        pool = x.pool(game); out = []
        with open(os.path.join(HERE, 'decks.tsv'), encoding='utf-8') as f:
            for r in csv.DictReader(f, delimiter='\t'):
                if r['game'] == game:
                    ids = deck_analysis.parse_deck(x.c, game, r['cards'])[0]
                    out.append((r['deck'], {i for i in ids if i in pool}))
        x._decks[game] = out
    return x._decks[game]


def played(x, args):
    """ask.py <games> played <faction>: the decks that play the faction, the factions it is paired with, its cards by the share
    of those decks that play them, and its cards no deck plays"""
    hit = x.find(args[0])
    if not hit: return
    g, fac, ids = hit; pool = x.pool(g); mine = set(ids)
    ds = [d for _, d in decks(x, g) if d & mine]
    if not ds: print(f'{g} {fac}: no deck of decks.tsv plays it'); return
    pair = collections.Counter(f for d in ds for f in sorted({f for i in d for f in pool[i][3]}) if f != fac)
    n = collections.Counter(i for d in ds for i in d & mine)
    print(f'{g} {fac}: {len(ds)} of {len(decks(x, g))} decks play its cards ({len(mine)} cards)')
    if pair: print('paired with: ' + ', '.join(f'{f} {k} ({100 * k // len(ds)}%)' for f, k in pair.most_common()))
    print('most played: ' + ', '.join(f'{pool[i][0]} {100 * k // len(ds)}%' for i, k in n.most_common(25)))
    never = sorted(pool[i][0] for i in mine if not n[i])
    print(f'in no deck ({len(never)}): ' + ', '.join(never[:40]) + (' ...' if len(never) > 40 else ''))


def deckmates(x, args):
    """ask.py <games> deckmates <card>: the cards most often in the same decks as this one, with how much more often than
    chance (lift = share with the card / share in all decks of the game)"""
    name = ' '.join(args)
    for g in x.games:
        pool = x.pool(g)
        me = [i for i, v in pool.items() if v[0].lower() == name.lower()]
        if not me: continue
        ds = [d for _, d in decks(x, g)]; mine = [d for d in ds if me[0] in d]
        if not mine: print(f'{g} {name}: in no deck of decks.tsv'); continue
        alln = collections.Counter(i for d in ds for i in d); withn = collections.Counter(i for d in mine for i in d if i != me[0])
        top = sorted(withn, key=lambda i: (-withn[i], -withn[i] / alln[i]))[:25]
        print(f'{g} {pool[me[0]][0]}: in {len(mine)} of {len(ds)} decks')
        print('  ' + ', '.join(f'{pool[i][0]} {withn[i]} (x{withn[i] / len(mine) / (alln[i] / len(ds)):.1f})' for i in top))
        return
    print(f'No card "{name}" in {", ".join(x.games)}')


def deckconcepts(x, args):
    """ask.py <games> deckconcepts <faction>: the faction's mechanics (concepts) by how much players choose them: share of the
    faction's card plays in real decks against share of its cards; above 1 = players pick it more than the pool offers"""
    hit = x.find(args[0])
    if not hit: return
    g, fac, ids = hit; mine = set(ids)
    plays = collections.Counter(i for _, d in decks(x, g) for i in d & mine)
    if not plays: print(f'{g} {fac}: no deck of decks.tsv plays it'); return
    con = collections.defaultdict(set)
    for card, k in x.c.execute(f"select distinct card, concept from flat_concept where card in ({','.join(map(str, mine))})"):
        con[k].add(card)
    tot_p, tot_c = sum(plays.values()), len(mine)
    rows = []
    for k, cs in con.items():
        if len(cs) < 3: continue
        p = sum(plays[i] for i in cs) / tot_p; s = len(cs) / tot_c
        rows.append((p / s, k, len(cs), p))
    rows.sort(reverse=True)
    print(f'{g} {fac}: concept, ratio (deck plays share / card share), cards, share of plays')
    for r, k, n, p in rows[:20]: print(f'  {k}: x{r:.2f}, {n} cards, {100 * p:.0f}% of plays')
    print('  least chosen: ' + ', '.join(f'{k} x{r:.2f}' for r, k, _, _ in rows[-8:]))


ASKS = {'played': played, 'deckmates': deckmates, 'deckconcepts': deckconcepts}
