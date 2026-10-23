"""Step 7: real-world test cases (the ```tsv block of tools/games/<game>.md, from wikis and guides, each with its source URL) checked against
the library. Build check that reports how many cases are met per game (the final comparison needs final >= original).
  signature  faction, concept     met when the faction's signature (or keyword signature) concepts include it, a narrower or
                                  a broader one below the four branches
  archetype  faction, archetype   met when faction_archetypes lists it for that faction with lift above 1
  combo      card A, card B       met when query.connections finds any connection between the two cards
  splash     faction, concept     met when the concept (or a narrower one) is a splash of that faction
Usage: realworld.py <db> [-v]"""
import csv, glob, os, sqlite3, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
db = sys.argv[1]; os.environ['TB_LIB'] = os.path.abspath(db); sys.path.insert(0, HERE)
import query as Qy, games
c = sqlite3.connect(db); q = lambda s, *a: c.execute(s, a).fetchall()
desc = collections.defaultdict(set); anc = collections.defaultdict(set)
for r, i in q('SELECT root, id FROM concept_tree'): desc[r].add(i); anc[i].add(r)
GROUPS = {'effect', 'helps_me', 'hurts_enemy', 'drawback', 'game_rules'} | {i for i, in q('SELECT id FROM concepts WHERE id NOT IN (SELECT child FROM concept_parents)')}
def near(k): return desc[k] | (anc[k] - GROUPS)
tot = collections.Counter(); met = collections.Counter(); miss = []
for g, f in games.files():
    for row in csv.reader(games.block(f, 'tsv'), delimiter='\t'):
        if len(row) < 3 or row[0].startswith('#'): continue
        t, a, b = row[0].strip(), row[1].strip(), row[2].strip(); ok = False
        if t == 'signature':
            ks = {k for k, in q("SELECT concept FROM faction_signature WHERE game=? AND faction=? AND kind IN ('signature','keyword_signature')", g, a)}
            ok = bool(ks & near(b))
        elif t == 'splash':
            ks = {k for k, in q("SELECT concept FROM faction_signature WHERE game=? AND faction=? AND kind='splash'", g, a)}
            ok = bool(ks & (desc[b] | {b}))
        elif t == 'archetype':
            ok = bool(q('SELECT 1 FROM faction_archetypes WHERE game=? AND faction=? AND archetype=? AND lift>1', g, a, b))
        elif t == 'combo':
            ia = q('SELECT id FROM entities WHERE game=? AND name=? LIMIT 1', g, a); ib = q('SELECT id FROM entities WHERE game=? AND name=? LIMIT 1', g, b)
            ok = bool(ia and ib and Qy.connections(ia[0][0], ib[0][0]))
        else: continue
        tot[g, t] += 1; met[g, t] += ok
        if not ok: miss.append((g, t, a, b))
games = sorted({g for g, _ in tot})
for g in games:
    print(f'{g:18} ' + '  '.join(f'{t} {met[g, t]}/{tot[g, t]}' for t in ('signature', 'archetype', 'combo', 'splash') if tot[g, t]))
print('real-world cases met:', sum(met.values()), '/', sum(tot.values()))
if '-v' in sys.argv:
    for m in miss: print('  miss', *m)
