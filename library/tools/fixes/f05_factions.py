"""Faction names (Warhammer games), from the BSData catalogue names. Usage: f05_factions.py <db> [dry]
  - "<army> - Library" and "<army> Library" are the catalogue files that hold an army's shared datasheets and rules: the faction is
    the army ("Library - Tyranids" -> "Xenos - Tyranids", the army that imports it; "Library - Titans" -> "Titans").
  - Age of Sigmar "<army> - <list>" (armies of renown) and "<army> [LEGENDS]": the faction is the army; the list name goes to
    extra.army_of_renown, the Legends mark to extra.legends.
  - Names cut at a hyphen by the first build ("Flesh", "Lumineth Realm") get the full army name.
Then the factions table is rebuilt from the entries (every faction, its size, and its concept profile: concepts with 3+ cards
and share >= 5%, by lift, top 12)."""
import json, re, sqlite3, sys, collections
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall(); dry = len(sys.argv) > 2
moves = []   # (game, old, new, extra)
for g in ('wh_40k_10e', 'wh_aos_4th'):
    F = dict(q("SELECT faction, count(*) FROM entities WHERE game=? AND faction IS NOT NULL AND category NOT IN ('keyword','tribe') GROUP BY 1", g))
    for f in F:
        new, ex = None, {}
        m = re.match(r'^(.*?)\s*-?\s*Library$', f) or re.match(r'^Library - (.*)$', f)
        if m:
            base = m.group(1).strip()
            cand = [x for x in F if x != f and 'Library' not in x and (x == base or x.endswith(' - ' + base) or x.endswith(' ' + base))]
            new = base if base in F or not cand else sorted(cand, key=lambda x: -F[x])[0]
            # "Aeldari - Aeldari" -> "Aeldari"
            parts = new.split(' - ')
            if len(parts) == 2 and parts[0] == parts[1]: new = parts[0]
        elif g == 'wh_aos_4th':
            b = f
            if b.endswith(' [LEGENDS]'): b = b[:-10]; ex['legends'] = True
            if ' - ' in b and b.split(' - ')[0] in F and not b.startswith(('✦', 'þ', '۞', '❖')):
                ex['army_of_renown'] = b.split(' - ', 1)[1]; b = b.split(' - ')[0]
            if b != f: new = b
        if new is None:
            full = [x for x in F if x != f and x.startswith(f + '-') and ' - ' not in x[len(f):]]
            if len(full) == 1: new = full[0]
        if new and new != f: moves.append((g, f, new, ex))
for g, a, b, ex in moves: print(g, '|', a, '->', b, ex if ex else '')
if dry: sys.exit()
for g, a, b, ex in moves:
    for i, e in q("SELECT id, extra FROM entities WHERE game=? AND faction=?", g, a):
        d = json.loads(e) if e else {}; d.update(ex)
        c.execute("UPDATE entities SET faction=?, extra=? WHERE id=?", (b, json.dumps(d) if d else None, i))
# rebuild the factions table
mech = {i for (i,) in q("SELECT id FROM concepts WHERE facet NOT IN ('role','scope','problem') AND id IN (SELECT child FROM concept_parents)")}
c.execute("DELETE FROM factions")
for (g,) in q("SELECT DISTINCT game FROM entities"):
    size = dict(q("SELECT faction, count(*) FROM entities WHERE game=? AND faction IS NOT NULL AND category NOT IN ('keyword','tribe') GROUP BY 1", g))
    if not size: continue
    tot = sum(size.values())
    cnt = collections.Counter(); gcnt = collections.Counter()
    for f, k, n in q("""SELECT e.faction, x.concept, count(DISTINCT e.id) FROM entities e JOIN entity_concepts x ON x.entity=e.id WHERE e.game=?
                        AND x.role IN ('does','grants') AND e.category NOT IN ('keyword','tribe') AND e.faction IS NOT NULL GROUP BY 1,2""", g):
        if k in mech: cnt[f, k] = n; gcnt[k] += n
    for f, n in size.items():
        prof = []
        for (ff, k), m in cnt.items():
            if ff != f or m < 3: continue
            sh = m / n; avg = gcnt[k] / tot
            if sh >= 0.05 and avg: prof.append({'concept': k, 'share': round(sh, 3), 'lift': round(sh / avg, 2)})
        prof = sorted(prof, key=lambda x: -x['lift'])[:12]
        c.execute("INSERT INTO factions VALUES(?,?,?,?)", (g, f, n, json.dumps(prof)))
c.commit(); print('faction renames:', len(moves), 'factions:', q("SELECT count(*) FROM factions")[0][0])
