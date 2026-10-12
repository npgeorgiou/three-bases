"""Apply general concept patterns (concept_patterns rows with game NULL) for the given concepts to every game except Marvel Snap
(which its own loader tags), replacing earlier text_pattern tags of those concepts, and add trigger -> effect pairs involving them.
Usage: retag.py <db> <concept,concept,...|@file>"""
import re, sqlite3, sys
db, cons = sys.argv[1], sys.argv[2]
cons = set(open(cons[1:]).read().split()) if cons.startswith('@') else set(cons.split(','))
c = sqlite3.connect(db); q = lambda s, *a: c.execute(s, a).fetchall()
pats = [(con, role, re.compile(p, re.I)) for con, role, p in q("select concept,role,pattern from concept_patterns where game is null")]
mine = [x for x in pats if x[0] in cons]
root = dict(q("select id,root from concept_tree where root in ('trigger','effect')"))
trig_p = [x for x in pats if x[1] == 'does' and root.get(x[0]) == 'trigger']
eff_p = [x for x in pats if x[1] == 'does' and root.get(x[0]) == 'effect']
G = 'marvel_snap'
ph = ','.join('?' * len(cons))
c.execute(f"delete from entity_concepts where method='text_pattern' and concept in ({ph}) and entity in (select id from entities where game!=?)", (*cons, G))
c.execute(f"delete from trigger_effect where game!=? and (trigger in ({ph}) or effect in ({ph}))", (G, *cons, *cons))
SPLIT = re.compile(r'(?<=[.!;])\s+|\n+')
n = npair = 0
for e, g, t in q("select id,game,text from entities where game!=? and text is not null", G):
    low = t.lower()
    hit = False
    for con, role, p in mine:
        m = p.search(low)
        if m:
            hit = True
            c.execute("insert or ignore into entity_concepts values(?,?,?,?,?)", (e, con, role, 'text_pattern', low[max(0, m.start() - 20): m.start() + 40])); n += 1
    if not hit or len(low) > 4000: continue   # pairs only where a retagged concept appears; long rules prose: none
    for cl in SPLIT.split(low):
        if not cl.strip(): continue
        tr = {x[0] for x in trig_p if x[2].search(cl)}; ef = {x[0] for x in eff_p if x[2].search(cl)}
        for a in tr:
            for b in ef:
                if a in cons or b in cons:
                    c.execute("insert into trigger_effect values(?,?,?,?,?)", (e, g, a, b, cl.strip()[:300])); npair += 1
c.commit()
print('tags', n, 'pairs', npair)
