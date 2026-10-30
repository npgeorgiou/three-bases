"""Questions about mechanics (concepts), not single cards, answered over every game at once. A link between two cards is only
ever made inside one game (each game is its own world); the answers add up what each game shows, by concept.
  together(c, games, concept)   concepts found on the same cards as this one, strongest first (lift): what it is built with
  feeds(c, games, concept)      concepts whose cards are set off by cards with this concept, inside each game: A feeds B
  chains(c, games, concept)     A feeds B feeds C, the strongest three-step families
  deck(c, game, seed, size)     cards of one game that feed each other around a card or a concept, within the seed's faction
A card sets off another when it makes something (flat_ref role makes) that the other waits for, tests, counts or picks by
(any other role), on fitting sides, with the same keyword when both name one. A thing many cards care about (damage) counts
less than a rare one (weight 1 / number of cards caring about it in that game)."""
import collections, math

FIT = lambda a, b: not a or not b or a == b or 'any' in (a, b)


def edges(c, game):
    """(maker, taker) -> weight, inside one game"""
    key = ('edges', game)
    if key in CACHE: return CACHE[key]
    rows = c.execute("""select f.card, f.role, f.happening, f.side, f.keyword, f.pick from flat_ref f join card k on k.id=f.card
                        where k.game=? and k.is_keyword=0 and k.is_stub=0 and f.origin!='game'
                        and coalesce(k.category,'') not in ('boss','monster','event','modifier')""", (game,)).fetchall()  # no enemies
    makes, takes = collections.defaultdict(list), collections.defaultdict(list)
    for card, role, h, side, kw, pick in rows:
        if pick == 'self' and role != 'makes':
            if h in ('played', 'summoned'): continue  # a card's own entry (On play) is not something another card feeds
            side = 'mine'  # something happening to the card itself happens on my side
        (makes if role == 'makes' else takes)[h].append((card, side, kw))
    made = collections.defaultdict(set)  # a card is everything it makes: what Living Shadow does, Zed brings
    for a, b in c.execute("select m.card, m.made from flat_made m join card k on k.id=m.card where k.game=?", (game,)): made[b].add(a)
    for h, ms in list(makes.items()):
        makes[h] = ms + [(a, side, kw) for b, side, kw in ms for a in made.get(b, ()) if a != b]
    out = collections.defaultdict(float)
    for h, ts in takes.items():
        carers = collections.defaultdict(set)  # a thing about one keyword (frozen units) is rarer than the happening in general
        for t, _, tk in ts: carers[tk].add(t)
        for m, ms, mk in set(makes.get(h, [])):
            for t, ts_, tk in set(ts):
                if m != t and FIT(ms, ts_) and (mk is None or tk is None or mk == tk):
                    out[(m, t)] = max(out[(m, t)], 1.0 / len(carers[tk] | (carers[None] if tk else set())))
    # types: a card that asks for a type (friendly Satyrs, a Dragon) is fed by cards of that type and cards that make them
    asks = collections.defaultdict(set)
    for card, w in c.execute("""select card, coalesce(on_with,'') || ';' || coalesce(to_with,'') from flat_do where card in
                                (select id from card where game=?) union all select card, obj_with from flat_when where card in
                                (select id from card where game=?) union all select card, coalesce(of_with,'') || ';' ||
                                coalesce(ev_obj_with,'') from flat_if where card in (select id from card where game=?)""", (game,) * 3):
        for part in (w or '').split(';'):
            b = part.removeprefix('of:').split(' ')
            if len(b) == 3 and b[0] == 'type' and b[1] in ('is', 'in') and b[2].isdigit(): asks[int(b[2])].add(card)
    has = collections.defaultdict(set)
    for card, t in c.execute('select ct.card, ct.type from card_type ct join card k on k.id=ct.card where k.game=?', (game,)):
        has[t].add(card)
    for m, ref in c.execute("""select d.card, d.card_ref from flat_do d join card k on k.id=d.card where k.game=? and
                               d.act in ('summon','create','copy','play_card') and d.card_ref is not null""", (game,)):
        for (t,) in c.execute('select type from card_type where card=?', (ref,)): has[t].add(m)
    for t, ts in asks.items():
        for m in has.get(t, ()):
            for x in ts:
                if m != x: out[(m, x)] = max(out[(m, x)], 1.0 / len(ts))
    CACHE[key] = out
    return out


CACHE = {}


def concepts_of(c, game):
    key = ('concepts', game)
    if key not in CACHE:
        d = collections.defaultdict(set)
        for card, con in c.execute("""select f.card, f.concept from flat_concept f join card k on k.id=f.card
                                      where k.game=? and k.is_keyword=0 and k.is_stub=0
                                      and coalesce(k.category,'') not in ('boss','monster','event','modifier')""", (game,)):
            d[card].add(con)
        for a, b in c.execute("select m.card, m.made from flat_made m join card k on k.id=m.card where k.game=?", (game,)):
            d[a] |= d.get(b, set())  # a card is everything it makes (Zed brings his Living Shadow's Ephemeral)
        CACHE[key] = d
    return CACHE[key]


def name(c, i):
    return c.execute('select name from card where id=?', (i,)).fetchone()[0]


def together(c, games, concept, top=12):
    score, seen = collections.Counter(), collections.defaultdict(dict)
    for g in games:
        cc = concepts_of(c, g); n = len(cc) or 1
        have = [k for k, s in cc.items() if concept in s]
        if not have: continue
        base = collections.Counter(x for s in cc.values() for x in s)
        with_ = collections.Counter(x for k in have for x in cc[k] if x != concept)
        gs = {}
        for x, k in with_.items():
            if k >= 2:
                lift = (k / len(have)) / (base[x] / n)
                gs[x] = lift * math.log(1 + k); seen[x][g] = k
        add_share(score, gs)
    return [(x, seen[x]) for x, _ in score.most_common(top)]


def add_share(score, gs):
    """each game counts the same: its scores as a share of its best one (Runeterra's many cards must not drown the other games)"""
    top_ = max(gs.values(), default=0)
    for x, v in gs.items(): score[x] += v / top_ if top_ else 0


def feeds(c, games, concept, top=12, reverse=False):
    """concept B with, per game, the number of card pairs A->B and one example (reverse: what feeds this concept). Ranked by
    lift: how much more often A's links land on B cards than links in general do, so mechanics every card has (on play,
    passive) do not crowd out the real families."""
    score, per = collections.Counter(), collections.defaultdict(dict)
    for g in games:
        cc = concepts_of(c, g); E = edges(c, g)
        agg = collections.defaultdict(lambda: [0, 0.0, None]); base = collections.Counter(); tot_a = tot = 0.0
        for (m, t), w in E.items():
            src, dst = (t, m) if reverse else (m, t)
            tot += w
            for x in cc.get(dst, ()): base[x] += w
            if concept not in cc.get(src, ()): continue
            tot_a += w
            for x in cc.get(dst, ()):
                if x == concept: continue
                a = agg[x]; a[0] += 1; a[1] += w
                if a[2] is None or w > a[2][0]: a[2] = (w, m, t)
        gs = {}
        for x, (n, w, ex) in agg.items():
            if n >= 3 and base[x]:
                lift = (w / tot_a) / (base[x] / tot)
                if lift > 1.2:
                    gs[x] = lift * math.log(1 + n); per[x][g] = (n, f'{name(c, ex[1])} -> {name(c, ex[2])}')
        add_share(score, gs)
    return [(x, per[x]) for x, _ in score.most_common(top)]


def chains(c, games, concept, top=10):
    out = []
    first = feeds(c, games, concept, top=8)
    for b, pb in first:
        for x, px in feeds(c, games, b, top=6):
            if x in (concept, b): continue
            both = set(pb) & set(px)
            if both: out.append((sum(pb[g][0] * px[g][0] for g in both), concept, b, x, sorted(both)))
    out.sort(reverse=True)
    return out[:top]


def deck(c, game, seed, size):
    """greedy: start from the seed card (or the best-linked cards with the seed concept), keep adding the card linked to the
    most cards already in (then the most weight), inside the seed's factions plus neutral cards; no tokens or level forms"""
    E = edges(c, game); cc = concepts_of(c, game)
    reg = {i: set((r or '').split(';')) - {''} for i, r in c.execute('select id, regions from card where game=? and is_keyword=0 and is_stub=0', (game,))}
    ids = [i for (i,) in c.execute('select id from card where game=? and lower(name)=lower(?) and is_keyword=0', (game, seed))]
    start = ids[:1] or [k for k, s in cc.items() if seed in s]
    if not start: return [], set()
    fac = collections.Counter(r for i in start for r in reg.get(i, ()) if r != 'Neutral')
    allowed = {f for f, _ in fac.most_common(2 if game == 'runeterra' else 1)} | {'Neutral'}
    deckable = {i for (i,) in c.execute('select id from card where game=? and rarity is not null', (game,))}  # no tokens, no level forms
    pool = [i for i in reg if reg[i] and reg[i] <= allowed and i in cc and i in deckable]
    links = collections.defaultdict(float)
    for (m, t), w in E.items(): links[(m, t)] += w; links[(t, m)] += w
    chosen = list(start[:1]) if ids else sorted(start, key=lambda i: -sum(links[(i, j)] for j in start))[:3]
    score = lambda i: (sum(1 for j in chosen if links[(i, j)]), sum(links[(i, j)] for j in chosen))  # cards linked, then weight
    while len(chosen) < size:
        best = max((i for i in pool if i not in chosen), key=score, default=None)
        if best is None or score(best)[0] == 0: break
        chosen.append(best)
    return chosen, allowed
