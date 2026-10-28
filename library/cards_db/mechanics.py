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
                        where k.game=? and k.is_keyword=0 and k.is_stub=0""", (game,)).fetchall()
    makes, takes = collections.defaultdict(list), collections.defaultdict(list)
    for card, role, h, side, kw, pick in rows:
        if pick == 'self' and role != 'makes':
            if h in ('played', 'summoned'): continue  # a card's own entry (On play) is not something another card feeds
            side = 'mine'  # something happening to the card itself happens on my side
        (makes if role == 'makes' else takes)[h].append((card, side, kw))
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
                                      where k.game=? and k.is_keyword=0 and k.is_stub=0""", (game,)):
            d[card].add(con)
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
        for x, k in with_.items():
            if k >= 2:
                lift = (k / len(have)) / (base[x] / n)
                score[x] += lift * math.log(1 + k); seen[x][g] = k
    return [(x, seen[x]) for x, _ in score.most_common(top)]


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
        for x, (n, w, ex) in agg.items():
            if n >= 3 and base[x]:
                lift = (w / tot_a) / (base[x] / tot)
                if lift > 1.2:
                    score[x] += lift * math.log(1 + n); per[x][g] = (n, f'{name(c, ex[1])} -> {name(c, ex[2])}')
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


# ---- a deck: what mechanics it uses, how its cards feed each other, what it needs that nothing in it makes ----
DECK_RULES = {  # the games' own deck-building rules (not card data)
    'runeterra': {'size': 40, 'copies': 3, 'factions': 2, 'neutral': None},
    'stormbound': {'size': 12, 'copies': 1, 'factions': 1, 'neutral': 'Neutral'},
}
WORDS = {  # plain words for what happens (vocab event values)
    'dies': 'a unit dies', 'killed': 'something is killed', 'damaged': 'something takes damage', 'survives_damage': 'a unit survives damage',
    'nexus_damaged': 'a player takes damage', 'summoned': 'a unit enters play', 'played': 'a card is played', 'drawn': 'a card is drawn',
    'discarded': 'a card is discarded', 'created': 'a card is created', 'given_keyword': 'a unit gets a keyword or status',
    'stat_changed': 'a unit gets stats', 'healed': 'something is healed', 'attacks': 'a unit attacks', 'blocks': 'a unit blocks',
    'strikes': 'a unit strikes', 'strikes_nexus': 'a unit hits the enemy player', 'leaves_play': 'a card leaves play',
    'recalled': 'a unit returns to hand', 'revived': 'a unit comes back from the dead', 'levels_up': 'a champion levels up',
    'obliterated': 'a card is removed from the game', 'transformed': 'a card transforms', 'mana_refilled': 'mana is gained',
    'targeted': 'a card is targeted', 'shuffled': 'a card is shuffled into a deck', 'moves': 'a unit moves', 'equipped': 'a unit gets equipment'}
PLAY = {'played', 'summoned', 'attacks', 'blocks', 'strikes', 'damaged', 'survives_damage', 'round_start', 'round_end', 'turn_start',
        'turn_end', 'drawn', 'mana_refilled', 'strikes_nexus', 'nexus_damaged', 'always', 'activated', 'moves', 'attack_done',
        'targeted', 'spell_resolves', 'game_start'}  # these happen in any game without a card making them


def labels():
    if 'labels' not in CACHE:
        import os
        d = {}
        for line in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools', 'concept_tree_v3.txt')):
            p = [x.strip() for x in line.split('|')]
            if len(p) > 3 and not line.startswith('#'): d[p[0]] = (p[1], p[2])
        CACHE['labels'] = d
    return CACHE['labels']


def parse_deck(c, game, text):
    """card names in a list; a name may itself hold a comma ("Senna, Sentinel of Light"): the longest known name wins"""
    names = sorted({n for (n,) in c.execute('select name from card where game=? and is_keyword=0 and is_stub=0', (game,))}, key=len, reverse=True)
    out, rest, unknown = [], text, []
    while rest.strip(' ,\n'):
        rest = rest.strip(' ,\n'); low = rest.lower()
        m = next((n for n in names if low.startswith(n.lower()) and (len(rest) == len(n) or rest[len(n)] in ',\n')), None)
        if not m:
            cut = rest.find(','); bad = rest if cut < 0 else rest[:cut]; unknown.append(bad.strip()); rest = '' if cut < 0 else rest[cut:]
            continue
        out.append(m); rest = rest[len(m):]
    ids = [c.execute('select id from card where game=? and name=? and is_keyword=0', (game, n)).fetchone()[0] for n in out]
    return ids, unknown


def analyze(c, game, text):
    ids, unknown = parse_deck(c, game, text)
    nm = lambda i: name(c, i)
    deck = list(dict.fromkeys(ids)); dset = set(deck); lines = []
    if unknown: lines.append('Not found in ' + game + ': ' + ', '.join(unknown))
    # the deck's factions and the game's rules
    reg = {i: [r for r in (c.execute('select regions from card where id=?', (i,)).fetchone()[0] or '').split(';') if r] for i in deck}
    rule = DECK_RULES.get(game, {})
    facs = collections.Counter(r for rs in reg.values() for r in rs if r != rule.get('neutral'))
    lines.append(f"{len(deck)} different cards; factions: " + ', '.join(f'{f} ({n})' for f, n in facs.most_common()))
    if rule and len(facs) > rule['factions']: lines.append(f"  Not allowed: {game} decks use at most {rule['factions']} faction(s).")
    if rule: lines.append(f"  A full {game} deck has {rule['size']} cards, up to {rule['copies']} of each: these {len(deck)} are its core.")
    # mechanics: concepts by kind, most cards first
    cc = concepts_of(c, game); lab = labels()
    count = collections.Counter(x for i in deck for x in cc.get(i, ()))
    lines.append('Mechanics (concept: cards):')
    for kind in ('effect', 'trigger', 'condition', 'combat', 'role'):
        xs = [(x, n) for x, n in count.most_common() if lab.get(x, ('', ''))[1] == kind and n >= 2][:8]
        if xs: lines.append(f'  {kind}: ' + ', '.join(f'{lab[x][0]} ({n})' for x, n in xs))
    # how it works: inside the deck, who makes what another card waits for
    rows = c.execute(f"""select card, role, happening, side, keyword, pick, origin from flat_ref where card in ({','.join('?' * len(deck))})""", deck).fetchall()
    makes = collections.defaultdict(set); needs = collections.defaultdict(set)
    for card, role, h, side, kw, pick, origin in rows:
        if role == 'makes': makes[h].add((card, side, kw))
        elif origin == 'own':  # a keyword's own rules (Poison ends when Vitalized) are not what the card needs
            if pick == 'self' and h in ('played', 'summoned'): continue
            needs[card].add((h, 'mine' if pick == 'self' else side, kw))
    links = collections.defaultdict(set)
    for t, ns in needs.items():
        for h, side, kw in ns:
            for m, ms, mk in makes.get(h, ()):
                if m != t and FIT(ms, side) and (mk is None or kw is None or mk == kw): links[(h, kw)].add((m, t))
    kwn = lambda k: c.execute('select name from card where id=?', (k,)).fetchone()[0] if k else ''
    lines.append('How it works (card -> card that uses it), strongest first:')
    for (h, kw), ps in sorted(links.items(), key=lambda x: -len({t for _, t in x[1]})):
        if h in ('played', 'damaged', 'stat_changed') and len(ps) > 12: continue  # too common to explain anything
        what = WORDS.get(h, h) + (f' ({kwn(kw)})' if kw else '')
        makers = sorted({nm(m) for m, _ in ps}); takers = sorted({nm(t) for _, t in ps})
        lines.append(f'  {what}: made by {", ".join(makers)}; used by {", ".join(takers)}')
    # what each card needs that nothing in the deck makes
    lines.append('What the deck needs and where it comes from:')
    for i in deck:
        miss = sorted({WORDS.get(h, h) + (f' ({kwn(kw)})' if kw else '') for h, side, kw in needs.get(i, ())
                       if h not in PLAY and side not in ('enemy',) and not any(m != i and FIT(ms, side) and (mk is None or kw is None or mk == kw)
                                                                                  for m, ms, mk in makes.get(h, ()))})
        if miss: lines.append(f'  {nm(i)} needs: {", ".join(miss)}: nothing else in the deck makes it')
    alone = [nm(i) for i in deck if not any(i in p for ps in links.values() for p in ps)]
    if alone: lines.append('  Not linked to any other card in the deck: ' + ', '.join(alone))
    missing = sum(1 for l in lines if l.endswith('nothing else in the deck makes it'))
    users = {t for ps in links.values() for _, t in ps}
    lines.append(f"Works? {len(users)} of {len(deck)} cards use something another card in the deck makes; "
                 f"{missing} card(s) need something nothing in the deck makes; {len(alone)} card(s) stand alone.")
    return lines
