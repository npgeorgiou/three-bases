"""Final comparison of the tag-fix plan (19 Oct 2026): no game may end worse than the original database (c7a77a4) on the answer
key. The full rebuild in this plan applied every pattern and review file to every entry, and some games gained wrong tags or lost
right ones that way. This step reverts those changes per game, from tools/final/revert.tsv (made by final_compare.py):
  restore  entity  concept  role   a tag of the original that the answer key shows right, missing now: put back (method 'restored'),
                                   only while the key (with today's tree), a judged sample or a hand review still shows it right
  undo     game    concept         tags of this concept that the original did not have in this game, which made the game worse:
                                   removed again, except where the key, a judged sample or a hand review says the entry has it
Build step right after parent_rule.py (a restored broader tag stays even where a narrower one is present). Idempotent. Usage: final_revert.py <db>"""
import collections, csv, json, os, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(HERE, 'final', 'revert.tsv')
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
if not os.path.exists(F): print('final revert: none'); sys.exit(0)
rows = [l.rstrip('\n').split('\t') for l in open(F, encoding='utf-8') if l.strip() and not l.startswith('#')]
base = collections.defaultdict(set)   # (game, concept) -> entities that had it in the original (from revert_base.tsv)
bf = os.path.join(HERE, 'final', 'revert_base.tsv')
if os.path.exists(bf):
    for l in open(bf, encoding='utf-8'):
        g, k, ids = l.rstrip('\n').split('\t'); base[g, k] = {int(x) for x in ids.split(',') if x}
sys.path.insert(0, os.path.join(HERE, 'step3')); sys.path.insert(0, HERE)
import patterns3 as P
from concept_tree import primary
known = collections.defaultdict(set)
for g, kk in P.keys().items():
    for e, ks in kk.items():
        for k in ks: known[e] |= {k} | P.K.ANC[k] | P.K.DESC[k]
Qs, ans, _, _ = P.answers()
for qid, (e, k, d) in Qs['q'].items():
    if ans.get(qid) is True: known[e].add(k)
mk = dict(q('SELECT old_id, kept_id FROM merged_entities'))
for r in csv.DictReader(open(os.path.join(HERE, 'regression.tsv'), encoding='utf-8'), delimiter='\t'):
    if r['expect'] == 'present': known[mk.get(int(r['entity']), int(r['entity']))] |= {r['concept']}
game = dict(q('SELECT id, game FROM entities'))
put = rem = 0
for r in rows:
    if r[0] == 'restore':
        e, k, role = int(r[1]), r[2], r[3]
        if e in game and k in known[e]: put += c.execute('INSERT OR IGNORE INTO entity_concepts VALUES(?,?,?,?,?)', (e, k, role, 'restored', 'right in the original (final comparison)')).rowcount
    elif r[0] == 'undo':
        g, k = r[1], r[2]
        for e, in q('SELECT DISTINCT ec.entity FROM entity_concepts ec JOIN entities x ON x.id=ec.entity WHERE x.game=? AND ec.concept=? AND ec.method NOT IN (?,?,?)', g, k, 'restored', 'game_structure', 'data_rule'):
            if e in base[g, k] or k in known[e]: continue
            rem += c.execute("DELETE FROM entity_concepts WHERE entity=? AND concept=? AND method NOT IN ('restored','game_structure','data_rule')", (e, k)).rowcount
c.commit()
print('final revert: restored', put, 'tags right in the original; undid', rem, 'tags added since the original in games they made worse')
