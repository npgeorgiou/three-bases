"""Combo validation set: checks that `combo` (query.connections) finds every known combo in tools/combos.tsv.
Each line is enabler -> payoff in one game (Claude's list of well-known combos; the 'why' column is Claude's summary).
Usage: combo_check.py <db> [-v]   prints found/missed and the strongest layer that found each one; exit 1 on a miss not listed as known_miss.
A known_miss line names the link type the library lacks; when a new link type finds it, clear the column."""
import os, sys, csv
os.environ['TB_LIB'] = os.path.abspath(sys.argv[1]); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import query
rank = ['link', 'engine', 'role', 'role_tree', 'keyword', 'type', 'relation']
miss, known, found, by = [], [], 0, {}
for r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'combos.tsv'), encoding='utf-8'), delimiter='\t'):
    ids = []
    for n in (r['enabler'], r['payoff']):
        x = query.q("SELECT id FROM entities WHERE game=? AND name=? COLLATE NOCASE AND category NOT IN ('keyword','tribe')", r['game'], n) or query.q("SELECT kept_id FROM merged_entities WHERE game=? AND name=? COLLATE NOCASE", r['game'], n)
        ids.append(x[0][0] if x else None)
    if None in ids: miss.append((r, 'card not in library')); continue
    res = query.connections(*ids)
    layers = {l for l, _ in res}
    best = next((l for l in rank if l in layers), None)
    if best: found += 1; by[best] = by.get(best, 0) + 1
    elif r.get('known_miss (link type the library lacks)'): known.append(r)
    else: miss.append((r, 'no connection'))
    if '-v' in sys.argv: print(f"{r['game']:12} {r['enabler'][:24]:24} -> {r['payoff'][:24]:24} {best or 'MISS'}")
print(f'combos found: {found}/{found + len(miss) + len(known)}  known misses: {len(known)}  new misses: {len(miss)}  by strongest layer: {by}')
for r, why in miss: print(f"  MISS {r['game']}: {r['enabler']} -> {r['payoff']} ({why})")
sys.exit(1 if miss else 0)
