"""What every card of the library does, as concepts, and how often real cards link two sets of concepts.

tag(): card -> its concepts (flat_concept, plus cheapunit* and dearunit*: a unit in the cheapest or the dearest third of
its game's units); SOURCES: what of each card (an effect row, an ability, a keyword) gives each concept.
pair_links(): for two keys (each a set of concepts), how much more often than chance real cards link them, or how much
more often real decks heavy in one hold the other; a link counts only through what of each card made it (side_concepts).
Used by the roster's scripts (factions/roster/PIPELINE.md) and roster_links.py. Needs links.sqlite for the links (links.py).
"""
import collections, json, os, sqlite3

SUPPLIES = {'inscryption': ('blood', 'energy', 'bones', 'mox')}  # games whose cards are paid in different kinds of supply
UNIT_CATS = ('unit', 'hero', 'leader')

MIN_DECKS_BOTH = 5  # a game gives a decks value for two keys only when at least 5 of its decks hold both
MIN_LINKS_GAME = 5  # a game counts for two keys only when chance alone would give it 5 linked pairs
MIN_LINKS = 20  # two keys get a cards number only when chance alone would give 20 linked pairs  # Faeria Pandora has 1 card in decks


def unit_stats(game, power, health, st):
    """(strength, defence) of a card: Stormbound has one number for both, Gwent power (defence adds armour), Into the
    Breach only health; other games power and health"""
    try: d = json.loads(st) if st else {}
    except ValueError: d = {}
    num = lambda v: float(str(v).split('/')[0]) if v not in (None, '') and str(v).split('/')[0].replace('.', '').isdigit() else None
    if game == 'stormbound':
        v = num(d.get('strength')); return v, v
    if game == 'gwent':
        p = num(d.get('power')) if power is None else power
        return p, None if p is None else p + (num(d.get('armor')) or 0)
    return power, health


def counts(ks, game, concepts):
    """does a card with concepts ks count for a key (the same in every game)"""
    return any(k in ks for k in concepts)


# What of a card makes a link (links.sqlite a_ab / b_ab, written by links.py): an effect row 'ability.seq', an ability, 'kw<id>'
# (a keyword it has), 'c:<concept>' (a concept read from the whole card), 'type' (the card by what it is), 'rule' (the game's
# rules). A link counts for a key only through the concepts of what made it on each side (side_concepts).
SOURCES = collections.defaultdict(lambda: collections.defaultdict(set))  # card -> concept -> what of the card gives it (tag);
# a concept with no source (unit stats, cost, health) belongs to the card by what it is
KW_AB = collections.defaultdict(set)  # (card, ability) -> 'kw<id>' of the keywords it has whose own ability that is
SIDE = {}  # (card, side, keys) -> the keys that side counts for (side_keys)
DO_SRC = "ability || '.' || seq, 'kw' || via"  # flat_do columns naming a row's source
IF_SRC = "ability, 'kw' || via"  # flat_if / flat_when: an ability's conditions and triggers (a keyword's when no ability)


def note_src(card, k, *srcs):
    for x in srcs:
        if x is not None: SOURCES[card][k].add(str(x))


def row_sources(c):
    """SOURCES of the concepts flat.py's derive writes into flat_concept (rows, keywords, its RULES), and KW_AB"""
    import flat
    SOURCES.clear(); KW_AB.clear(); SIDE.clear()
    for t in ('flat_do', 'flat_if', 'flat_when'):
        for card, ab, via in c.execute(f"select distinct card, ability, via from {t} where origin='has_keyword' and ability is not null and via is not null"):
            KW_AB[(card, ab)].add(f'kw{via}')
    for t, cols in (('flat_do', DO_SRC), ('flat_if', IF_SRC), ('flat_when', IF_SRC)):
        for card, k, *src in c.execute(f"select card, concept, {cols} from {t} where coalesce(concept,'')!=''"): note_src(card, k, *src)
    for card, k, kw in c.execute("select distinct ck.card, v.tree, ck.keyword from card_keyword ck join card k on k.id=ck.keyword join vocab v on "
                                 "v.field='keyword' and v.value=coalesce((select s.value from vocab s where s.field='keyword' and s.value=k.game || ':' || k.name), k.name) where v.tree!=''"):
        note_src(card, k, f'kw{kw}')
    for card, k, ab in c.execute("select distinct a.card, v.tree, a.id from cond cd join ability a on a.id=cd.ability join card k on k.id=cd.ref_keyword join vocab v on "
                                 "v.field='keyword' and v.value=coalesce((select s.value from vocab s where s.field='keyword' and s.value=k.game || ':' || k.name), k.name) "
                                 "where cd.test='keyword_condition' and v.tree!=''"):
        note_src(card, k, ab)
    for k, t, cond in flat.RULES:
        for card, *src in c.execute(f"select card, {DO_SRC if t == 'flat_do' else IF_SRC} from {t} where {cond}"): note_src(card, k, *src)


def side_concepts(card, src, con):
    """the concepts of a card that one side of a link comes from (its sources joined by ';'): an effect row gives its own
    concepts and its ability's conditions and triggers; an ability all of them; a keyword's own effect also the keyword"""
    out = set()
    parts = [t for t in (src or '').split(';') if t]
    parts += [k for t in parts if t[0].isdigit() for k in KW_AB.get((card, int(t.split('.')[0])), ())]
    for s in parts:
        if s == 'rule': continue
        if s.startswith('c:'): out.add(s[2:]); continue
        for k in con[card]:
            got = SOURCES[card].get(k)
            if s == 'type': hit = not got
            elif not got: hit = False
            elif s[0].isdigit() and '.' in s: hit = s in got or s.split('.')[0] in got
            elif s[0].isdigit(): hit = s in got or any(t.startswith(s + '.') for t in got)
            else: hit = s in got
            if hit: out.add(k)
    return out


def tag(c, x, games):
    """card -> its concepts, plus the starred ones this file adds; SOURCES: what of each card gives each concept"""
    con = collections.defaultdict(set)
    row_sources(c)
    for card, k in c.execute('select card, concept from flat_concept'):
        con[card].add(k)
    pools = {g: x.pool(g) for g in games}
    raw = {i: (g, cat, cost, unit_stats(g, p, h, st), (ct or '').lower()) for i, g, cat, cost, p, h, st, ct in
           c.execute('select id, game, category, cost, power, health, stats, cost_text from card')}
    kind = lambda i: next((k for k in SUPPLIES.get(raw[i][0], ()) if k in raw[i][4]), '')
    paid = collections.defaultdict(list)  # (game, kind of supply) -> the costs of its units
    for g, pool in pools.items():
        for i in pool:
            if raw[i][1] in UNIT_CATS and raw[i][2]: paid[(g, kind(i))].append(raw[i][2])
    def cost(i):  # in a game with several kinds of supply: the cost against the average cost of its kind
        g, _, v = raw[i][:3]
        return v / (sum(paid[(g, kind(i))]) / len(paid[(g, kind(i))])) if g in SUPPLIES and v and paid[(g, kind(i))] else v
    stats = {i: (r[1], cost(i)) + r[3] for i, r in raw.items()}
    for g, pool in pools.items():
        costs = sorted(stats[i][1] for i in pool if stats[i][0] in UNIT_CATS and stats[i][1] is not None)
        third = lambda n: min(sorted(set(costs)), key=lambda t: abs(n(t) - len(costs) / 3), default=None)
        lo = third(lambda t: sum(1 for v in costs if v <= t))  # the cost up to which the units are nearest to a third of the game's units
        hi = third(lambda t: sum(1 for v in costs if v >= t))  # (when most units share one cost, cheap is under it and dear is over it)
        for i in pool:
            ks, v = con[i], stats[i][1]
            if stats[i][0] not in UNIT_CATS or v is None or lo is None or lo >= hi: continue
            if v <= lo: ks.add('cheapunit*')
            if v >= hi: ks.add('dearunit*')
    return con, pools, stats


def link_pairs():
    """linked card pair (lower id first) -> {(what of the first card made a link, what of the second)}"""
    pairs = collections.defaultdict(set)
    for a, b, sa, sb in sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'links.sqlite')).execute('select a, b, a_ab, b_ab from link'):
        if a != b: pairs[(min(a, b), max(a, b))].add((sa, sb) if a < b else (sb, sa))
    return pairs


def side_keys(card, src, game, keys, con):
    """the keys one side of a link counts for on this card (side_concepts)"""
    key = (card, src, tuple(k[0] for k in keys))
    if key not in SIDE:
        ks = side_concepts(card, src, con)
        SIDE[key] = [k[0] for k in keys if counts(ks, game, k[4])]
    return SIDE[key]


def pair_links(keys, games, pools, con, pairs, deck_lists=None, seen=None, plain=None, pooled=None):
    """All cards (no deck_lists): how much more often than chance the library links a card of one key with a card of the
    other, counted through what of each card made the link (link_pairs, side_concepts). 1 = chance: the share of the game's
    card pairs the library links x the share of A's cards' link ends that A's own part makes x the same share for B.
    Worked out per game, then averaged over the games where chance gives MIN_LINKS_GAME+ pairs: each game counts the same.
    seen (a Counter): filled with the number of games in which real cards link each two keys (sorted).
    plain (a Counter): filled with the linked card pairs of each two keys (sorted), each pair once.
    pooled (a dict): filled with all games' linked pairs over all games' chance, for pairs chance gives under 5 in every game.
    Decks (deck_lists given; Kaptain, 10 Nov 2026: how often two keys appear in the same real decks, linked or not): per deck,
    the share of its cards that count for each key; for two keys A and B, the average of (A share x B share) over the
    game's decks divided by (average A share x average B share). 1 = decks heavy in A hold as much B as usual; 2 = twice as
    much; below 1 = players keep them apart. "Usual" comes from the real decks, so a key every deck plays does not look
    combined with everything. Each game counts the same: the value is the average over the games where at least
    MIN_DECKS_BOTH decks hold both keys.
    keys: [(name, _, _, _, its concepts), ...]."""
    if deck_lists is not None:
        per = collections.defaultdict(list); used = {}
        for g in sorted(deck_lists):
            ds = [d for d in deck_lists[g] if d]
            if not ds: continue
            used[g] = len(ds)
            sh = [{k[0]: sum(1 for i in d if counts(con[i], g, k[4])) / len(d) for k in keys} for d in ds]
            mean = {k[0]: sum(x[k[0]] for x in sh) / len(ds) for k in keys}
            for a in keys:
                for b in keys:
                    both = sum(1 for x in sh if x[a[0]] and x[b[0]])
                    if both >= MIN_DECKS_BOTH and mean[a[0]] and mean[b[0]]:
                        per[(a[0], b[0])].append(sum(x[a[0]] * x[b[0]] for x in sh) / len(ds) / (mean[a[0]] * mean[b[0]]))
        print('decks used:', used)
        return {a[0]: {b[0]: round(sum(per[(a[0], b[0])]) / len(per[(a[0], b[0])]), 2) if per[(a[0], b[0])] else None for b in keys}
                for a in keys}
    per = collections.defaultdict(list); total = collections.Counter(); allobs = collections.Counter()
    for g in games:
        obs, exp = collections.Counter(), collections.Counter()
        ids = list(pools[g])
        of = {i: [s[0] for s in keys if counts(con[i], g, s[4])] for i in ids}
        dens = sum(1 for a, b in pairs if a in of and b in of) / (len(ids) * (len(ids) - 1) / 2)
        n = collections.Counter(k for i in ids for k in of[i])
        both = collections.Counter((ka, kb) for i in ids for ka in of[i] for kb in of[i])
        ends, made = collections.Counter(), collections.Counter()  # per key: link ends on its cards, and those its own part made
        for (a, b), sides in pairs.items():
            if a in of and b in of:
                on = {a: set(), b: set()}; linked = set()
                for sa, sb in sides:
                    ka_, kb_ = side_keys(a, sa, g, keys, con), side_keys(b, sb, g, keys, con)
                    on[a].update(ka_); on[b].update(kb_); linked |= {(ka, kb) for ka in ka_ for kb in kb_}
                for i in (a, b):
                    for k in of[i]: ends[k] += 1; made[k] += k in on[i]
                for ka, kb in linked: obs[(ka, kb)] += 1; obs[(kb, ka)] += 1
                if plain is not None:
                    for t in {tuple(sorted(t)) for t in linked}: plain[t] += 1
        if seen is not None:
            for t in {tuple(sorted(k)) for k, v in obs.items() if v}: seen[t] += 1
        share = {k: made[k] / ends[k] if ends[k] else 0 for k in ends}
        for sa in keys:
            for sb in keys: exp[(sa[0], sb[0])] += (n[sa[0]] * n[sb[0]] - both[(sa[0], sb[0])]) * dens * share.get(sa[0], 0) * share.get(sb[0], 0)
        for k, e in exp.items():
            total[k] += e; allobs[k] += obs[k]
            if e >= MIN_LINKS_GAME: per[k].append(obs[k] / e)
    if pooled is not None:
        pooled.update({k: round(allobs[k] / e, 2) for k, e in total.items() if e and not per[k]})
    return {a[0]: {b[0]: round(sum(per[(a[0], b[0])]) / len(per[(a[0], b[0])]), 2)
                   if total[(a[0], b[0])] >= MIN_LINKS and per[(a[0], b[0])] else None for b in keys} for a in keys}
