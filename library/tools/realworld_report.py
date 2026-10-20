"""Readable report of the real-world test: every case of tools/realworld/*.tsv with its result, the number behind it and its source.
  signature  the faction's share of cards with the concept, its rank among the game's factions, and its lift over the game
  archetype  the faction's lift for the archetype (counts when above 1.25 in faction_archetypes)
  splash     whether the concept is a splash of the faction
  combo      whether both cards are in the library and which connection layers link them
Writes library/REALWORLD_REPORT.md (or the path given). Usage: realworld_report.py <db> [<out.md>]"""
import collections, csv, glob, os, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); db = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(HERE), 'REALWORLD_REPORT.md')
os.environ['TB_LIB'] = os.path.abspath(db); sys.path.insert(0, HERE); import query as Qy
c = sqlite3.connect(db); q = lambda s, *a: c.execute(s, a).fetchall()
desc = collections.defaultdict(set); anc = collections.defaultdict(set)
for r, i in q('SELECT root, id FROM concept_tree'): desc[r].add(i); anc[i].add(r)
GROUPS = {'effect', 'helps_me', 'hurts_enemy', 'drawback', 'game_rules'} | {i for i, in q('SELECT id FROM concepts WHERE id NOT IN (SELECT child FROM concept_parents)')}
near = lambda k: desc[k] | (anc[k] - GROUPS) | {k}
names = dict(q('SELECT id, name FROM games'))
CARD = "e.category NOT IN ('keyword','tribe')"

def share(g, ks):
    """cards with any of the concepts (does/grants) per faction of the game, over the faction's size"""
    n = dict(q(f"SELECT e.faction, count(*) FROM entities e WHERE e.game=? AND {CARD} AND e.faction IS NOT NULL GROUP BY 1", g))
    h = dict(q(f"""SELECT e.faction, count(DISTINCT e.id) FROM entities e JOIN entity_concepts ec ON ec.entity=e.id WHERE e.game=? AND {CARD}
                   AND ec.role IN ('does','grants') AND ec.concept IN ({','.join('?' * len(ks))}) GROUP BY 1""", g, *ks))
    tot = sum(n.values()); avg = sum(h.values()) / tot if tot else 0
    return n, h, avg

rows, tot, met, why = [], collections.Counter(), collections.Counter(), collections.Counter()
for fn in sorted(glob.glob(os.path.join(HERE, 'realworld', '*.tsv'))):
    g = os.path.basename(fn)[:-4]
    for row in csv.reader(open(fn, encoding='utf-8'), delimiter='\t'):
        if len(row) < 3 or row[0].startswith('#'): continue
        t, a, b = (x.strip() for x in row[:3]); note = row[3].strip() if len(row) > 3 else ''; url = row[-1].strip() if row[-1].startswith('http') else ''
        if t == 'signature':
            sig = {k for k, in q("SELECT concept FROM faction_signature WHERE game=? AND faction=? AND kind IN ('signature','keyword_signature')", g, a)}
            ok = bool(sig & near(b)); n, h, avg = share(g, near(b))
            sh = h.get(a, 0) / n[a] if n.get(a) else 0
            rank = 1 + sum(1 for f in n if n[f] and h.get(f, 0) / n[f] > sh)
            detail = f"{h.get(a, 0)}/{n.get(a, 0)} cards ({sh:.0%}), rank {rank} of {len(n)}, lift {sh / avg:.1f}" if avg else f"0/{n.get(a, 0)} cards"
            r = '' if ok else 'faction not in library' if a not in n else 'no card of the faction has it' if not h.get(a) else 'only 1-4 cards have it' if h[a] < 5 else 'faction size under 20' if n[a] < 20 else 'used, but not more than other factions'
        elif t == 'splash':
            ok = bool({k for k, in q("SELECT concept FROM faction_signature WHERE game=? AND faction=? AND kind='splash'", g, a)} & (desc[b] | {b}))
            detail = ''; r = '' if ok else 'missing from the splash list'
        elif t == 'archetype':
            lf = q('SELECT lift, entities FROM faction_archetypes WHERE game=? AND faction=? AND archetype=?', g, a, b)
            ok = bool(lf and lf[0][0] > 1); detail = f'lift {lf[0][0]:.2f}, {lf[0][1]} cards' if lf else 'lift under 1.25'
            r = '' if ok else 'not above the game average'
        elif t == 'combo':
            ia = q('SELECT id FROM entities WHERE game=? AND name=? LIMIT 1', g, a); ib = q('SELECT id FROM entities WHERE game=? AND name=? LIMIT 1', g, b)
            res = Qy.connections(ia[0][0], ib[0][0]) if ia and ib else None
            ok = bool(res); detail = ('linked by ' + ', '.join(sorted({x[0] if isinstance(x, (tuple, list)) else str(x) for x in res}))) if res else ''
            r = '' if ok else 'a card name is not in the library' if not (ia and ib) else 'both cards there, no connection'
        else: continue
        tot[g, t] += 1; met[g, t] += ok
        if not ok: why[t, r] += 1
        rows.append((g, t, a, b, ok, detail, r, note, url))

L = ['# Real-world test: every case', '', f'Made by `tools/realworld_report.py` from the library build. A case is a fact a wiki or guide states about a game '
     '(a faction\'s signature mechanic, its archetype, a two-card combo, a splash); the test checks whether the library finds it.', '',
     '## Totals', '', '| Game | Signature | Archetype | Combo | Splash | All |', '|---|---|---|---|---|---|']
gs = sorted({g for g, _ in tot})
cell = lambda g, t: f'{met[g, t]}/{tot[g, t]}' if tot[g, t] else ''
for g in gs:
    L.append(f'| {names.get(g, g)} | ' + ' | '.join(cell(g, t) for t in ('signature', 'archetype', 'combo', 'splash')) +
             f' | {sum(met[g, t] for t in ("signature", "archetype", "combo", "splash"))}/{sum(tot[g, t] for t in ("signature", "archetype", "combo", "splash"))} |')
L.append(f'| **All** | ' + ' | '.join(f'{sum(met[g, t] for g in gs)}/{sum(tot[g, t] for g in gs)}' for t in ('signature', 'archetype', 'combo', 'splash')) +
         f' | **{sum(met.values())}/{sum(tot.values())}** |')
L += ['', '## Why cases miss', '', '| Cases | Type | Reason |', '|---|---|---|'] + [f'| {v} | {t} | {r} |' for (t, r), v in why.most_common()]
for g in gs:
    L += ['', f'## {names.get(g, g)}', '', '| | Type | Faction or card | Concept or card | Measured | Why it misses | Source says |', '|---|---|---|---|---|---|---|']
    for (gg, t, a, b, ok, detail, r, note, url) in rows:
        if gg != g: continue
        src = f'[{note or "source"}]({url})' if url else note
        L.append(f"| {'✓' if ok else '✗'} | {t} | {a} | {b} | {detail} | {r} | {src.replace('|', '/')} |")
open(out, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('real-world cases met:', sum(met.values()), '/', sum(tot.values()), '->', out)
