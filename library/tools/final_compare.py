"""Final comparison of the tag-fix plan: original database (c7a77a4) against a new build, per game, on the answer key.
  final_compare.py <original.sqlite> <new.sqlite> revert   writes tools/final/revert.tsv and revert_base.tsv for final_revert.py:
       restore  every tag of the original that the key shows right and the new build lacks (no correct tag lost)
       undo     per game still above the original's wrong tags: the concepts whose added tags (not in the original) are wrong on
                the key, most first, until the game is back at or below the original
  final_compare.py <original.sqlite> <new.sqlite> report   tools/final/report.md: wrong and missed per 100 key entries, correct tags
       lost, estimated wrong tags in the whole game (pattern samples), real-world cases met, tags by source, for both databases
The original is scored after its tags are moved through the Step 1 map. Prints counts only."""
import collections, json, os, sqlite3, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'final'); os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(HERE, 'key')); sys.path.insert(0, HERE)
import key as K
from concept_tree import targets, MAP, REMOVED
orig, new, mode = sys.argv[1], sys.argv[2], sys.argv[3]
co, cn = sqlite3.connect(orig), sqlite3.connect(new)

def tags(c, ids, old):
    out = collections.defaultdict(set)
    txt = dict(c.execute('SELECT id, text FROM entities'))
    for e, k, r, m in c.execute('SELECT entity, concept, role, method FROM entity_concepts WHERE entity IN (%s)' % ','.join(map(str, ids))):
        if m in ('game_structure', 'data_rule'): continue
        for x in (targets(k, txt.get(e)) if old and (k in MAP or k in REMOVED) else {k}):
            if x in K.TREE: out[e].add((x, r))
    return out

def judge(Kc):
    ok = set(Kc) | {a for k in Kc for a in K.ANC[k]} | {d for k in Kc for d in K.DESC[k]}
    return ok

res = {}; restore = []; undo = []; basemap = collections.defaultdict(set)
# a later pass keeps the earlier revert lines and undoes further concepts where the earlier undos (which spare key-right and reviewed
# entries) were not enough
PREV = [l.rstrip('\n').split('\t') for l in open(os.path.join(OUT, 'revert.tsv'), encoding='utf-8') if l.strip() and not l.startswith('#')] \
    if mode == 'revert' and os.path.exists(os.path.join(OUT, 'revert.tsv')) else []
done = {(r[1], r[2]) for r in PREV if r[0] == 'undo'}
restore += [(int(r[1]), r[2], r[3]) for r in PREV if r[0] == 'restore']; undo += [(r[1], r[2]) for r in PREV if r[0] == 'undo']
for g in K.GAMES:
    key = json.load(open(os.path.join(HERE, 'key', g, 'key.json'))); ids = [int(i) for i in key]
    live = {i for i, in cn.execute('SELECT id FROM entities WHERE game=?', (g,))}; ids = [i for i in ids if i in live]
    To, Tn = tags(co, ids, True), tags(cn, ids, False)
    wo = wn = mo = mn = lost = 0; added_wrong = collections.Counter()
    for i in ids:
        Kc = K.narrow({k for k, _ in key[str(i)]['tags']}); ok = judge(Kc)
        Lo, Ln = {k for k, _ in To[i]}, {k for k, _ in Tn[i]}
        wo += sum(1 for l in Lo if l not in ok and l not in K.GROUPS); wn += sum(1 for l in Ln if l not in ok and l not in K.GROUPS)
        for l in Ln - Lo:
            if l not in ok and l not in K.GROUPS: added_wrong[l] += 1
        for k in Kc:
            near = {k} | K.DESC[k] | (K.ANC[k] - K.GROUPS)
            mo += not (Lo & near); mn += not (Ln & near)
        for k, r in To[i]:
            if k in ok and k not in K.GROUPS and k not in Ln:
                lost += 1; restore.append((i, k, r))
    res[g] = (len(ids), wo, wn, mo, mn, lost, added_wrong)
    if wn > wo:
        need = wn - wo; s = 0
        for k, n in added_wrong.most_common():
            if s >= need: break
            if (g, k) in done: continue
            undo.append((g, k)); s += n
if mode == 'revert':
    txt = dict(co.execute('SELECT id, text FROM entities'))
    want = {(g, k) for g, k in undo}
    for e, g, k in co.execute('SELECT ec.entity, x.game, ec.concept FROM entity_concepts ec JOIN entities x ON x.id=ec.entity'):
        for x in (targets(k, txt.get(e)) if (k in MAP or k in REMOVED) else {k}):
            if (g, x) in want: basemap[g, x].add(e)
    with open(os.path.join(OUT, 'revert.tsv'), 'w') as fh:
        fh.write('# made by final_compare.py (see final_revert.py)\n')
        for e, k, r in sorted(set(restore)): fh.write(f'restore\t{e}\t{k}\t{r}\n')
        for g, k in dict.fromkeys(undo): fh.write(f'undo\t{g}\t{k}\n')
    with open(os.path.join(OUT, 'revert_base.tsv'), 'w') as fh:
        for (g, k), es in sorted(basemap.items()): fh.write(f'{g}\t{k}\t{",".join(map(str, sorted(es)))}\n')
    print('restore', len(set(restore)), 'undo', len(undo), [u for u in undo if u not in done][:12])
for g, (n, wo, wn, mo, mn, lost, aw) in res.items():
    flag = '' if (wn <= wo and mn <= mo and lost == 0) else '  WORSE'
    print(f'{g:18} n {n:4}  wrong/100 {100 * wo / n:6.1f} -> {100 * wn / n:6.1f}   missed/100 {100 * mo / n:6.1f} -> {100 * mn / n:6.1f}   lost {lost}{flag}')
json.dump({g: v[:6] for g, v in res.items()}, open(os.path.join(OUT, f'compare_{mode}.json'), 'w'))
