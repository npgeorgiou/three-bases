"""Which mechanics are prominent in which faction (rebuilt 20 Oct 2026). Tables faction_signature and faction_archetypes.

Prominence is one rule, the same for every game, concept and archetype. A faction's mechanic is prominent when both hold:
  1. the faction uses it at least half again as often as the rest of the game: its share of cards with the mechanic is at
     least RATIO (1.5) times the share among all the game's other cards;
  2. that difference is not chance: if the faction's cards were drawn at random from the game's cards, at least this many
     would have the mechanic with probability under P_MAX (0.05, the usual bar; the hypergeometric tail, a one-sided Fisher
     exact test). This keeps a 3-card coincidence in a small faction out, and lets a small faction with a clear mechanic in.
(Tried first, 20 Oct 2026: the test alone at 1 in 1,000. It measures how sure the difference is, not how big, so small games
failed and big factions passed on small differences; hence rule 1 for size, rule 2 for chance.)

Factions: a card of a combined faction (Lorcana 'Amber-Steel', Legends 'Strength-Willpower', Star Wars Unlimited 'Command-
Cunning', Gwent 'Syndicate / Monster', Magic 'Multicolor (BR)') counts for each of its factions; combined factions are not
factions of their own. Factions with fewer than MIN cards (after that) are left out.
  signature          the mechanic is prominent in the faction and it is one of the two factions with the highest share of cards with the concept
  splash             another faction that uses a signature mechanic at all: 1+ cards, sorted by share
  keyword_signature  a keyword at least 60% of whose cards (8+) are one faction's (concept 'kw:<keyword>')
  faction_archetypes the archetype is prominent: the rule applied to the archetype's concepts taken together (any of them, or a narrower one)
Mechanics only: the root concepts and the role, scope and problem facets are left out, and so are concepts on more than 25% of
a game's cards (too common to belong to anyone). Roles counted: does and grants. Columns share and lift (share over the game
average) are kept for reading. Usage: signature.py <db>"""
import collections, json, re, sqlite3, sys
from math import lgamma, exp, log
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
MIN, P_MAX, RATIO = 20, 0.05, 1.5
CARD = "e.category NOT IN ('keyword','tribe')"
MTG = {'W': 'White', 'U': 'Blue', 'B': 'Black', 'R': 'Red', 'G': 'Green'}

def tail(N, K, n, x):
    """P(X >= x) for X hypergeometric: x successes in n draws from N items of which K are successes"""
    if x <= 0: return 1.0
    lc = lambda a, b: lgamma(a + 1) - lgamma(b + 1) - lgamma(a - b + 1)
    hi = min(K, n); base = lc(N, n)
    terms = [lc(K, i) + lc(N - K, n - i) - base for i in range(x, hi + 1) if n - i <= N - K]
    if not terms: return 0.0
    m = max(terms); return min(1.0, exp(m) * sum(exp(t - m) for t in terms))

def parts(name, plain):
    """the factions a combined faction name stands for, or None"""
    m = re.fullmatch(r'Multicolor \(([WUBRG]+)\)', name or '')
    if m: return [MTG[ch] for ch in m.group(1) if MTG[ch] in plain] or None
    for sep in (' / ', '-'):
        if sep == '-' and ' ' in (name or ''): continue
        ps = (name or '').split(sep)
        if len(ps) > 1 and all(p in plain for p in ps): return ps
    return None

def members(g):
    """faction -> set of its card ids (combined cards in each of their factions); all card ids with a faction"""
    rows = q(f'SELECT e.id, e.faction FROM entities e WHERE e.game=? AND {CARD} AND e.faction IS NOT NULL', g)
    names = {f for _, f in rows}; plain = {f for f in names if not parts(f, names - {f})}
    mem = collections.defaultdict(set)
    for i, f in rows:
        for p in (parts(f, plain) or [f]): mem[p].add(i)
    return {f: s for f, s in mem.items() if len(s) >= MIN}, {i for i, _ in rows}

mech = {i for (i,) in q("SELECT id FROM concepts WHERE facet NOT IN ('role','scope','problem') AND id IN (SELECT child FROM concept_parents)")}
tree = collections.defaultdict(set)
for r, i in q('SELECT root, id FROM concept_tree'): tree[r].add(i)
arch = [(a, json.loads(cs) if cs and cs.startswith('[') else [x.strip() for x in (cs or '').split(',') if x.strip()]) for a, cs in q('SELECT id, concepts FROM archetypes')]
c.execute('DROP TABLE IF EXISTS faction_signature')
c.execute('CREATE TABLE faction_signature(game TEXT, faction TEXT, concept TEXT, kind TEXT, entities INTEGER, share REAL, lift REAL, owner TEXT, owner_share REAL)')
c.execute('DELETE FROM faction_archetypes')
ins = lambda *v: c.execute('INSERT INTO faction_signature VALUES(?,?,?,?,?,?,?,?,?)', v)
for (g,) in q('SELECT DISTINCT game FROM entities'):
    fac, allc = members(g)
    if len(fac) < 2: continue
    N = len(allc)
    has = collections.defaultdict(set)
    for e, k in q(f"SELECT DISTINCT e.id, ec.concept FROM entities e JOIN entity_concepts ec ON ec.entity=e.id WHERE e.game=? AND {CARD} AND e.faction IS NOT NULL AND ec.role IN ('does','grants')", g):
        has[k].add(e)
    def test(ids):
        K = len(ids); res = []
        for f, s in fac.items():
            x = len(s & ids); n = len(s); rest = (K - x) / (N - n) if N > n else 0
            ok = x > 0 and (rest == 0 or (x / n) / rest >= RATIO) and tail(N, K, n, x) < P_MAX
            res.append((x / n, f, x, ok))
        return K, sorted(res, reverse=True)
    for k, ids in has.items():
        if k not in mech or len(ids) > 0.25 * N: continue
        K, res = test(ids); avg = K / N
        own = [(sh, f, x) for sh, f, x, ok in res[:2] if ok]
        for sh, f, x in own: ins(g, f, k, 'signature', x, round(sh, 3), round(sh / avg, 2), f, round(sh, 3))
        if not own: continue
        top = own[0]
        for sh, f, x, p in res:
            if x and f not in {o[1] for o in own}: ins(g, f, k, 'splash', x, round(sh, 3), round(sh / avg, 2), top[1], round(top[0], 3))
    # keyword signatures: a keyword is a faction's own when at least 60% of the cards that have, grant or mention it are that faction's (8+ cards)
    kwids = collections.defaultdict(set)
    for k, e in q(f"""SELECT kk.name, e.id FROM entity_links l JOIN entities kk ON kk.id=l.dst JOIN entities e ON e.id=l.src WHERE kk.game=? AND kk.category='keyword'
                     AND {CARD} AND l.rel IN ('has_keyword','grants_keyword','mentions_keyword')""", g): kwids[k].add(e)
    for k, ids in kwids.items():
        for f, s in fac.items():
            n = len(s & ids)
            if n >= 8 and n / len(ids) >= 0.6: ins(g, f, 'kw:' + k, 'keyword_signature', n, round(n / len(s), 3), round(n / len(ids), 2), f, round(n / len(s), 3))
    for a, cs in arch:
        want = set().union(*[tree.get(x, {x}) for x in cs]) if cs else set()
        ids = set().union(*[has[k] for k in want if k in has]) if want else set()
        K, res = test(ids)
        for sh, f, x, p in res:
            if p: c.execute('INSERT INTO faction_archetypes VALUES(?,?,?,?,?,?)', (g, f, a, round(sh, 3), round(sh / (K / N), 2), x))
c.commit()
print('faction_signature:', dict(q('SELECT kind, count(*) FROM faction_signature GROUP BY 1')), ' faction_archetypes:', q('SELECT count(*) FROM faction_archetypes')[0][0])
