"""Signature-vs-splash view per source faction (factions.txt Part 5, step 5: signatures belong to 1, at most 2, factions;
elsewhere they appear on a very few cards, expressed through that faction's own character).
Builds table faction_signature(game, faction, concept, kind, entities, share, lift, owner, owner_share):
  signature  the faction's own mechanic: at least 5 cards, share >= 6% of the faction, lift >= 1.8 over the game's factions,
             and the faction is one of the top 2 factions of its game for that concept
  splash     another faction's signature mechanic used by a faction below the signature bar: 1+ cards, sorted by share, no upper limit
  keyword_signature  a keyword at least 60% of whose cards (8+) are one faction's (concept 'kw:<keyword>')
Factions with fewer than 30 entries are left out. Also recomputes faction_archetypes from the current tags (share of the
faction's cards with any of the archetype's concepts or their descendants; kept when lift >= 1.25 and 5+ cards).
Mechanics only: the ten root concepts and concepts in the role, scope and problem facets are left out, and so are concepts on more than 25% of a game's cards.
Roles counted: does and grants. Thresholds are Claude's choice; the numbers are in the table to re-filter.
Usage: signature.py <db>"""
import sqlite3, sys, collections
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
c.execute('DROP TABLE IF EXISTS faction_signature')
c.execute('CREATE TABLE faction_signature(game TEXT, faction TEXT, concept TEXT, kind TEXT, entities INTEGER, share REAL, lift REAL, owner TEXT, owner_share REAL)')
MIN = 30   # factions smaller than this get no signature or splash rows (tiny samples inflate lift)
mech = {i for (i,) in q("SELECT id FROM concepts WHERE facet NOT IN ('role','scope','problem') AND id IN (SELECT child FROM concept_parents)")}  # roots left out
for (g,) in q('SELECT DISTINCT game FROM factions'):
    fac = {n: k for n, k in q("""SELECT f.name, count(e.id) FROM factions f JOIN entities e ON e.game=f.game AND e.faction=f.name
                                 AND e.category NOT IN ('keyword','tribe') WHERE f.game=? GROUP BY 1""", g) if k >= MIN}
    tot = sum(fac.values())
    if len(fac) < 2 or not tot: continue
    cnt = collections.Counter()
    for f, k, n in q("""SELECT e.faction, ec.concept, count(DISTINCT e.id) FROM entities e JOIN entity_concepts ec ON ec.entity=e.id
                        WHERE e.game=? AND ec.role IN ('does','grants') AND e.category NOT IN ('keyword','tribe') GROUP BY 1,2""", g):
        if f in fac and k in mech: cnt[f, k] = n
    gtot = collections.Counter()
    for (f, k), n in cnt.items(): gtot[k] += n
    for k, n in gtot.items():
        avg = n / tot
        if avg > 0.25: continue
        shares = sorted(((cnt[f, k] / fac[f], f) for f in fac if cnt[f, k]), reverse=True)
        owners = [(s, f) for s, f in shares[:2] if cnt[f, k] >= 5 and s >= 0.06 and s / avg >= 1.8]
        for s, f in owners: c.execute('INSERT INTO faction_signature VALUES(?,?,?,?,?,?,?,?,?)', (g, f, k, 'signature', cnt[f, k], round(s, 3), round(s / avg, 2), f, round(s, 3)))
        if not owners: continue
        own = {f for _, f in owners}; top = owners[0]
        for s, f in shares:   # every other faction that uses the mechanic at all is a splash, sorted by share (no upper limit)
            if f in own: continue
            c.execute('INSERT INTO faction_signature VALUES(?,?,?,?,?,?,?,?,?)', (g, f, k, 'splash', cnt[f, k], round(s, 3), round(s / avg, 2), top[1], top[0]))
    # keyword signatures: a keyword is a faction's own when at least 60% of the cards that have, grant or mention it are that faction's (8+ cards)
    kwc = collections.Counter(); kwt = collections.Counter()
    for k, f, n in q("""SELECT kk.name, e.faction, count(DISTINCT e.id) FROM entity_links l JOIN entities kk ON kk.id=l.dst JOIN entities e ON e.id=l.src
                         WHERE kk.game=? AND kk.category='keyword' AND e.category NOT IN ('keyword','tribe') AND l.rel IN ('has_keyword','grants_keyword','mentions_keyword')
                         GROUP BY 1,2""", g):
        kwt[k] += n
        if f in fac: kwc[k, f] = n
    for (k, f), n in kwc.items():
        if n >= 8 and n / kwt[k] >= 0.6:
            c.execute('INSERT INTO faction_signature VALUES(?,?,?,?,?,?,?,?,?)', (g, f, 'kw:' + k, 'keyword_signature', n, round(n / fac[f], 3), round(n / kwt[k], 2), f, round(n / fac[f], 3)))
# archetypes recomputed from the current tags: share of a faction's cards with any of the archetype's concepts, lift over the game average
c.execute('DELETE FROM faction_archetypes')
import json
arch = [(a, json.loads(cs) if cs and cs.startswith('[') else [x.strip() for x in (cs or '').split(',') if x.strip()]) for a, cs in q('SELECT id, concepts FROM archetypes')]
tree = {}
for r, i in q('SELECT root, id FROM concept_tree'): tree.setdefault(r, set()).add(i)
for (g,) in q('SELECT DISTINCT game FROM factions'):
    fac = {n: k for n, k in q("""SELECT f.name, count(e.id) FROM factions f JOIN entities e ON e.game=f.game AND e.faction=f.name
                                 AND e.category NOT IN ('keyword','tribe') WHERE f.game=? GROUP BY 1""", g) if k >= MIN}
    if len(fac) < 2: continue
    tot = sum(fac.values())
    tags = {}
    for e, f, k in q("SELECT e.id, e.faction, ec.concept FROM entities e JOIN entity_concepts ec ON ec.entity=e.id WHERE e.game=? AND ec.role IN ('does','grants') AND e.category NOT IN ('keyword','tribe')", g):
        if f in fac: tags.setdefault((e, f), set()).add(k)
    for a, cs in arch:
        want = set().union(*[tree.get(x, {x}) for x in cs]) if cs else set()
        per = collections.Counter(f for (e, f), ks in tags.items() if ks & want)
        avg = sum(per.values()) / tot if tot else 0
        for f, n in per.items():
            sh = n / fac[f]; lift = round(sh / avg, 2) if avg else 0
            if lift >= 1.25 and n >= 5: c.execute('INSERT INTO faction_archetypes VALUES(?,?,?,?,?,?)', (g, f, a, round(sh, 3), lift, n))
# consistency check: a faction's own keywords should show up in its concept signatures; list the factions where none do
weak = []
for g, f in q("SELECT DISTINCT game, faction FROM faction_signature WHERE kind='keyword_signature'"):
    sig = {k for (k,) in q("SELECT concept FROM faction_signature WHERE game=? AND faction=? AND kind='signature'", g, f)}
    kc = set()
    for (k,) in q("SELECT concept FROM faction_signature WHERE game=? AND faction=? AND kind='keyword_signature'", g, f):
        kc |= {x for (x,) in q("SELECT ec.concept FROM entities kk JOIN entity_concepts ec ON ec.entity=kk.id WHERE kk.game=? AND kk.category='keyword' AND kk.name=? AND ec.role IN ('does','grants')", g, k[3:])}
    if kc and not (kc & sig): weak.append(f'{g}/{f}')
c.commit()
print('factions whose own keywords are missing from their concept signatures:', len(weak), weak[:12])
print('faction_signature:', dict(q('SELECT kind, count(*) FROM faction_signature GROUP BY 1')))
