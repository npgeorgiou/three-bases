"""Why real-world cases miss (20 Oct 2026). For every case of tools/realworld/*.tsv that realworld.py does not meet, the reason:
  signature  no card of the faction has the concept / only 1-4 cards have it / used, but not more than the game's other factions
  splash     missing from the faction's splash list
  archetype  not above the game average (lift < 1.25 in faction_archetypes)
  combo      a card name is not in the library / both cards there, no connection
Tagging can fix only the first two signature reasons and 'no connection'; the others are measurement (lift over other factions,
archetype concept bundles) or missing cards. Prints counts and every case per reason. Usage: realworld_why.py <db>"""
import collections, csv, glob, os, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); db = sys.argv[1]
os.environ['TB_LIB'] = os.path.abspath(db); sys.path.insert(0, HERE); import query as Qy
c = sqlite3.connect(db); q = lambda s, *a: c.execute(s, a).fetchall()
desc = collections.defaultdict(set); anc = collections.defaultdict(set)
for r, i in q('SELECT root, id FROM concept_tree'): desc[r].add(i); anc[i].add(r)
GROUPS = {'effect', 'helps_me', 'hurts_enemy', 'drawback', 'game_rules'} | {i for i, in q('SELECT id FROM concepts WHERE id NOT IN (SELECT child FROM concept_parents)')}
near = lambda k: desc[k] | (anc[k] - GROUPS) | {k}
facs = {(g, f) for g, f in q('SELECT DISTINCT game, faction FROM entities WHERE faction IS NOT NULL')}
why = collections.Counter(); ex = collections.defaultdict(list)
for fn in sorted(glob.glob(os.path.join(HERE, 'realworld', '*.tsv'))):
    g = os.path.basename(fn)[:-4]
    for row in csv.reader(open(fn, encoding='utf-8'), delimiter='\t'):
        if len(row) < 3 or row[0].startswith('#'): continue
        t, a, b = row[0].strip(), row[1].strip(), row[2].strip()
        if t == 'signature':
            if {k for k, in q("SELECT concept FROM faction_signature WHERE game=? AND faction=? AND kind IN ('signature','keyword_signature')", g, a)} & near(b): continue
            ks = near(b); n = q('SELECT count(*) FROM entities WHERE game=? AND faction=?', g, a)[0][0]
            have = q('SELECT count(DISTINCT ec.entity) FROM entity_concepts ec JOIN entities x ON x.id=ec.entity WHERE x.game=? AND x.faction=? AND ec.concept IN (%s)' % ','.join('?' * len(ks)), g, a, *ks)[0][0]
            r = 'faction not in library' if (g, a) not in facs else 'no card of the faction has it' if have == 0 else 'only 1-4 cards have it' if have < 5 else 'used, but not more than other factions'
            b = f'{b} ({have}/{n} cards)'
        elif t == 'splash':
            if {k for k, in q("SELECT concept FROM faction_signature WHERE game=? AND faction=? AND kind='splash'", g, a)} & (desc[b] | {b}): continue
            r = 'missing from the splash list'
        elif t == 'archetype':
            if q('SELECT 1 FROM faction_archetypes WHERE game=? AND faction=? AND archetype=? AND lift>1', g, a, b): continue
            r = 'faction not in library' if (g, a) not in facs else 'not above the game average'
        elif t == 'combo':
            ia = q('SELECT id FROM entities WHERE game=? AND name=? LIMIT 1', g, a); ib = q('SELECT id FROM entities WHERE game=? AND name=? LIMIT 1', g, b)
            if ia and ib and Qy.connections(ia[0][0], ib[0][0]): continue
            r = 'a card name is not in the library' if not (ia and ib) else 'both cards there, no connection'
        else: continue
        why[t, r] += 1; ex[t, r].append(f'{g}: {a} / {b}')
print(sum(why.values()), 'cases missed')
for (t, r), v in sorted(why.items(), key=lambda x: -x[1]): print(f'{v:4}  {t:10} {r}')
for (t, r), v in sorted(ex.items()):
    print(f'== {t}: {r}'); [print('   ', x) for x in v]
