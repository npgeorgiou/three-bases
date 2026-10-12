"""Game-specific wording: each tools/patterns/<game>.txt line 'concept|role|regex' is stored as a concept_patterns row for that game and
applied to that game's entries (method text_pattern; the text is read lower-cased, own name as 'name', Magic without reminder text). A line removed from a file takes its tags away. A line '!concept|pattern' names a general pattern that misreads this game's wording:
the concept's automatic tag is removed from entries where no other pattern of the concept matches. File _all.txt applies to every game
except Marvel Snap. Usage: game_patterns.py <db> <dir>"""
import os, re, sqlite3, sys
c = sqlite3.connect(sys.argv[1]); d = sys.argv[2]
ok = {r[0] for r in c.execute("select id from concepts")}
for f in sorted(os.listdir(d)):
    if not f.endswith('.txt'): continue
    g = f[:-4]; rows = []; excl = []
    for line in open(os.path.join(d, f), encoding='utf-8'):
        line = line.rstrip('\n')
        if not line or line.startswith('#'): continue
        if line.startswith('!'):
            con, p = line[1:].split('|', 1); assert con in ok, (f, con); excl.append((con, p)); continue
        con, role, p = line.split('|', 2)
        assert con in ok, (f, con)
        rows.append((con, role, p))
    games = [r[0] for r in c.execute("select id from games where id!='marvel_snap'")] if g == '_all' else [g]
    nx = 0
    for con, bad in excl:
        bads = {b for cc, b in excl if cc == con}  # all patterns this file excludes for the concept
        others = [(r, re.compile(p, re.I)) for (p, r) in c.execute("select pattern,role from concept_patterns where concept=? and (game is null or game=?)", (con, g)) if p not in bads]
        badre = re.compile(bad, re.I)
        for gg in games:
            for e, t, role in c.execute("select e.id,e.text,ec.role from entity_concepts ec join entities e on e.id=ec.entity where e.game=? and ec.concept=? and ec.method='text_pattern'", (gg, con)).fetchall():
                low = (t or '').lower()
                if badre.search(low) and not any(r == role and o.search(low) for r, o in others):
                    c.execute("delete from entity_concepts where entity=? and concept=? and role=? and method='text_pattern'", (e, con, role)); nx += 1
    if g == '_all':
        print('_all exclusions removed', nx); continue
    # a line removed from the file also takes its tags away (where no remaining pattern of the concept still matches)
    newset = {(con, role, p) for con, role, p in rows}
    gone = [(con, role, p) for con, role, p in c.execute("select concept, role, pattern from concept_patterns where game=?", (g,)).fetchall() if (con, role, p) not in newset]
    if gone:
        import csv
        keep = {(int(r['entity']), r['concept']) for r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'regression.tsv'), encoding='utf-8'), delimiter='\t') if r['expect'] == 'present'}
        for con, role, p in gone:
            rest = [re.compile(x, re.I) for x, in c.execute("select pattern from concept_patterns where concept=? and role=? and game is null", (con, role))] + [re.compile(x, re.I) for cc, rr, x in rows if cc == con and rr == role]
            bad = re.compile(p, re.I)
            for e, t, nm in c.execute("select e.id, e.text, e.name from entity_concepts ec join entities e on e.id=ec.entity where e.game=? and ec.concept=? and ec.role=? and ec.method='text_pattern'", (g, con, role)).fetchall():
                low = (t or '').lower()
                if g == 'mtg': low = re.sub(r'\([^()]*\)', ' ', low)
                for x in [nm] + nm.split(' // '):
                    if len(x) > 2: low = low.replace(x.lower(), 'name')
                if (e, con) not in keep and bad.search(low) and not any(o.search(low) for o in rest):
                    c.execute("delete from entity_concepts where entity=? and concept=? and role=? and method='text_pattern'", (e, con, role)); nx += 1
    c.execute("delete from concept_patterns where game=?", (g,))
    for con, role, p in rows: c.execute("insert into concept_patterns values(?,?,?,?)", (con, role, p, g))
    n = 0
    comp = [(con, role, re.compile(p, re.I)) for con, role, p in rows]
    for e, t, nm in c.execute("select id,text,name from entities where game=? and text is not null", (g,)).fetchall():
        low = t.lower()
        if g == 'mtg': low = re.sub(r'\([^()]*\)', ' ', low)   # Magic is read without reminder text, as in the first build
        for x in [nm] + nm.split(' // '):
            if len(x) > 2: low = low.replace(x.lower(), 'name')   # the entry's own name, as in the first build
        for con, role, p in comp:
            m = p.search(low)
            if m:
                c.execute("insert or ignore into entity_concepts values(?,?,?,?,?)", (e, con, role, 'text_pattern', low[max(0, m.start() - 20): m.start() + 40])); n += 1
    print(g, 'patterns', len(rows), 'tags', n, 'exclusions removed', nx)
c.commit()
