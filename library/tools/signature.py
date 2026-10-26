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
  signature          the mechanic is prominent in the faction (any number of factions can share a signature)
  splash             another faction that uses a signature mechanic at all: 1+ cards, sorted by share
  keyword_signature  a keyword at least 60% of whose cards (8+) are one faction's (concept 'kw:<keyword>')
  faction_archetypes an archetype is a recipe of weighted mechanics (tools/archetype_recipes.tsv, learned by learn_recipes.py; else the
                     archetypes table's concepts at weight 1). A faction's score is the weighted average of its over-representation
                     of those mechanics (table faction_concept_ov: ln of its share over the rest of the game's share, 0 if not above);
                     it has the archetype when its score is at least 1.5 times the average of the game's other factions; several can hold
Mechanics only: the root concepts and the role, scope and problem facets are left out, and so are concepts on more than 25% of
a game's cards (too common to belong to anyone) unless one faction holds at least 60% of them (Kaptain, 26 Oct 2026). Roles counted: does, grants and cost (how a card is paid for). Columns share and lift (share over the game
average) are kept for reading. Usage: signature.py <db>"""
import collections, json, os, sqlite3, sys
from math import log
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
P_MAX, RATIO = 0.05, 1.5
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from factions import MIN, CARD, tail, members   # noqa

mech = {i for (i,) in q("SELECT id FROM concepts WHERE facet NOT IN ('role','scope','problem') AND id IN (SELECT child FROM concept_parents)")}
tree = collections.defaultdict(set)
for r, i in q('SELECT root, id FROM concept_tree'): tree[r].add(i)
arch = [(a, json.loads(cs) if cs and cs.startswith('[') else [x.strip() for x in (cs or '').split(',') if x.strip()]) for a, cs in q('SELECT id, concepts FROM archetypes')]
c.execute('DROP TABLE IF EXISTS faction_signature')
c.execute('CREATE TABLE faction_signature(game TEXT, faction TEXT, concept TEXT, kind TEXT, entities INTEGER, share REAL, lift REAL, owner TEXT, owner_share REAL)')
c.execute('DELETE FROM faction_archetypes')
c.execute('DROP TABLE IF EXISTS faction_concept_ov')
c.execute('CREATE TABLE faction_concept_ov(game TEXT, faction TEXT, concept TEXT, entities INTEGER, ov REAL)')
# archetype recipes: tools/archetype_recipes.tsv (archetype, concept, weight; learn_recipes.py), else the archetypes table's concepts at weight 1
RF = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'archetype_recipes.tsv')
recipes = {a: [(k, 1.0) for k in cs] for a, cs in arch}
if os.path.exists(RF):
    learned = collections.defaultdict(list)
    for ln in open(RF, encoding='utf-8'):
        if ln.strip() and not ln.startswith('#'): a, k, w = ln.rstrip('\n').split('\t'); learned[a].append((k, float(w)))
    recipes.update(learned)
ins = lambda *v: c.execute('INSERT INTO faction_signature VALUES(?,?,?,?,?,?,?,?,?)', v)
for (g,) in q('SELECT DISTINCT game FROM entities'):
    fac, allc = members(q, g)
    if len(fac) < 2: continue
    N = len(allc)
    has = collections.defaultdict(set)
    for e, k in q(f"SELECT DISTINCT e.id, ec.concept FROM entities e JOIN entity_concepts ec ON ec.entity=e.id WHERE e.game=? AND {CARD} AND e.faction IS NOT NULL AND ec.role IN ('does','grants','cost')", g):
        if e in allc: has[k].add(e)
    def test(ids):
        K = len(ids); res = []
        for f, s in fac.items():
            x = len(s & ids); n = len(s); rest = (K - x) / (N - n) if N > n else 0
            ok = x > 0 and (rest == 0 or (x / n) / rest >= RATIO) and tail(N, K, n, x) < P_MAX
            res.append((x / n, f, x, ok))
        return K, sorted(res, reverse=True)
    for k, ids in has.items():
        if k not in mech: continue
        if len(ids) > 0.25 * N and max(len(s & ids) for s in fac.values()) < 0.6 * len(ids): continue   # common and spread over the factions: no one's own
        K, res = test(ids); avg = K / N
        own = [(sh, f, x) for sh, f, x, ok in res if ok]
        for sh, f, x in own: ins(g, f, k, 'signature', x, round(sh, 3), round(sh / avg, 2), f, round(sh, 3))
        if not own: continue
        top = own[0]
        for sh, f, x, p in res:
            if x and f not in {o[1] for o in own}: ins(g, f, k, 'splash', x, round(sh, 3), round(sh / avg, 2), top[1], round(top[0], 3))
    # keyword signatures: a keyword is a faction's own when at least 60% of the cards that have, grant or mention it are that faction's (8+ cards)
    kwids = collections.defaultdict(set)
    for k, e in q(f"""SELECT kk.name, e.id FROM entity_links l JOIN entities kk ON kk.id=l.dst JOIN entities e ON e.id=l.src WHERE kk.game=? AND kk.category='keyword'
                     AND {CARD} AND l.rel IN ('has_keyword','grants_keyword','mentions_keyword')""", g):
        if e in allc: kwids[k].add(e)
    for k, ids in kwids.items():
        for f, s in fac.items():
            n = len(s & ids)
            if n >= 8 and n / len(ids) >= 0.6: ins(g, f, 'kw:' + k, 'keyword_signature', n, round(n / len(s), 3), round(n / len(ids), 2), f, round(n / len(s), 3))
    # over-representation of every mechanic in every faction: ln(faction share / share in the rest of the game), 0 when not above
    for k in mech:
        ids = set().union(*[has[x] for x in tree.get(k, {k}) if x in has])
        if not ids: continue
        K = len(ids)
        for f, s_ in fac.items():
            x, n = len(s_ & ids), len(s_)
            v = log(((x + 0.5) / (n + 1)) / ((K - x + 0.5) / (N - n + 1)))
            if v > 0: c.execute('INSERT INTO faction_concept_ov VALUES(?,?,?,?,?)', (g, f, k, x, round(v, 4)))
    ov = collections.defaultdict(dict)
    for f, k, v in q('SELECT faction, concept, ov FROM faction_concept_ov WHERE game=?', g): ov[f][k] = v
    # archetypes: a recipe of weighted mechanics; a faction has the archetype when its recipe score is at least RATIO times the
    # average score of the game's other factions (the same "half again as much" as signatures); a faction can have several
    for a, rec in recipes.items():
        if not rec: continue
        sc = {f: sum(w * ov[f].get(k, 0) for k, w in rec) / sum(w for _, w in rec) for f in fac}
        allids = set().union(*[has[x] for k, _ in rec for x in tree.get(k, {k}) if x in has])
        for f, v in sc.items():
            others = [u for h, u in sc.items() if h != f]; m = sum(others) / len(others) if others else 0
            if v > 0 and (m == 0 or v / m >= RATIO):
                c.execute('INSERT INTO faction_archetypes VALUES(?,?,?,?,?,?)', (g, f, a, round(v, 3), round(v / m, 2) if m else 99, len(fac[f] & allids)))
c.commit()
print('faction_signature:', dict(q('SELECT kind, count(*) FROM faction_signature GROUP BY 1')), ' faction_archetypes:', q('SELECT count(*) FROM faction_archetypes')[0][0])
