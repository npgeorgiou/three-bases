"""Make inherited keyword concepts match the keyword's own (reviewed) concepts. For every entry that has a keyword (entity_links
rel has_keyword or mentions_keyword), its via_keyword tags from those keywords become exactly the union of the keywords' current concepts and roles:
stale inherited tags are removed and missing ones added. A keyword the card grants (grants_keyword) adds its does-concepts as grants (never removed here; fix_grants.py corrects roles).
Usage: kw_sync.py <db> <game> [<game> ...]; a game written as h:<game> syncs has_keyword links only (mentions are not inherited)."""
import sqlite3, sys
db, games = sys.argv[1], sys.argv[2:]
c = sqlite3.connect(db); q = lambda s, *a: c.execute(s, a).fetchall()
ndel = nadd = 0
for g in games:
    rels = ('has_keyword',) if g.startswith('h:') else ('has_keyword', 'mentions_keyword')
    g = g[2:] if g.startswith('h:') else g
    kw = {k: n for k, n in q("select id,name from entities where game=? and category='keyword'", g)}
    tags = {}
    for k in kw:
        tags[k] = set(q("select concept,role from entity_concepts where entity=?", k))
    links = {}
    for s, d in q("select l.src,l.dst from entity_links l join entities e on e.id=l.src where e.game=? and l.rel in (" + ','.join('?' * len(rels)) + ")", g, *rels):
        if d in kw: links.setdefault(s, set()).add(d)
    for x, ks in links.items():
        names = {kw[k] for k in ks}
        want = {}
        for k in sorted(ks):
            for con, role in tags[k]: want.setdefault((con, role), kw[k])
        for con, role, ev in q("select concept,role,evidence from entity_concepts where entity=? and method='via_keyword'", x):
            if ev in names and (con, role) not in want:
                c.execute("delete from entity_concepts where entity=? and concept=? and role=? and method='via_keyword'", (x, con, role)); ndel += 1
        for (con, role), ev in want.items():
            cur = c.execute("insert or ignore into entity_concepts values(?,?,?,?,?)", (x, con, role, 'via_keyword', ev)); nadd += cur.rowcount
    # a keyword the card gives to other cards (grants_keyword): its 'does' concepts become the card's 'grants' tags
    for x, k in q("select l.src, l.dst from entity_links l join entities e on e.id=l.src where e.game=? and l.rel='grants_keyword'", g):
        for con, role in tags.get(k, ()):
            if role == 'does': nadd += c.execute("insert or ignore into entity_concepts values(?,?,?,?,?)", (x, con, 'grants', 'via_keyword', kw[k])).rowcount
c.commit()
print('kw_sync removed', ndel, 'added', nadd)
