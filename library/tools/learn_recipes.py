"""Learn archetype recipes from the real-world archetype cases (the ```tsv blocks of tools/games/*.md). Each game's archetype cases are split in
two halves (seed 1): the build half teaches, the test half only measures.
For an archetype, an ingredient's weight is how much more the factions the build half calls that archetype use the mechanic than
the average faction of the same games (mean over-representation from table faction_concept_ov, signature.py); the 12 heaviest
positive ingredients make the recipe. Archetypes without build cases keep their fixed concepts. Writes tools/archetype_recipes.tsv,
then signature.py must run again. Prints the test half met with the fixed concepts and with the recipes.
Usage: learn_recipes.py <db> [measure]   (measure: only print the test-half result of the current faction_archetypes)"""
import collections, csv, glob, os, random, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); db = sys.argv[1]; sys.path.insert(0, HERE); import games
c = sqlite3.connect(db); q = lambda s, *a: c.execute(s, a).fetchall()
build, test = [], []
for g, fn in games.files():
    rows = [(g, r[1].strip(), r[2].strip()) for r in csv.reader(games.block(fn, 'tsv'), delimiter='\t') if len(r) > 2 and r[0].strip() == 'archetype']
    random.Random(1).shuffle(rows); h = len(rows) // 2
    build += rows[:h]; test += rows[h:]
met = lambda rows: sum(1 for g, f, a in rows if q('SELECT 1 FROM faction_archetypes WHERE game=? AND faction=? AND archetype=? AND lift>1', g, f, a))
if sys.argv[2:] == ['measure']:
    print(f'test half: {met(test)}/{len(test)}  (build half: {met(build)}/{len(build)})'); sys.exit()
ov = collections.defaultdict(dict)
for g, f, k, v in q('SELECT game, faction, concept, ov FROM faction_concept_ov'): ov[g, f][k] = v
facs = collections.defaultdict(list)
for g, f in ov: facs[g].append(f)
out = ['# archetype\tconcept\tweight  (learn_recipes.py: build half of the real-world archetype cases, seed 1)']
for a in sorted({a for _, _, a in build}):
    pos = [(g, f) for g, f, aa in build if aa == a and (g, f) in ov]
    if not pos: continue
    games = {g for g, _ in pos}; base = [(g, f) for g in games for f in facs[g]]
    ks = set().union(*[ov[p].keys() for p in pos])
    w = {k: sum(ov[p].get(k, 0) for p in pos) / len(pos) - sum(ov[b].get(k, 0) for b in base) / len(base) for k in ks}
    for k, v in sorted(((k, v) for k, v in w.items() if v > 0), key=lambda x: -x[1])[:12]: out.append(f'{a}\t{k}\t{v:.3f}')
open(os.path.join(HERE, 'archetype_recipes.tsv'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(f'recipes for {len({l.split(chr(9))[0] for l in out[1:]})} archetypes from {len(build)} build cases; test half {len(test)} cases')
print(f'test half with the current faction_archetypes: {met(test)}/{len(test)}  (run signature.py, then "measure")')
