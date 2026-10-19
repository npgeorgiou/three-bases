"""Trigger -> effect pairs an older database has and a new build lost, grouped by the cause (asked by Kaptain, 19 Oct 2026).
A pair is lost when its trigger or effect concept is no longer on the entry (the tag was removed), or when both tags are still
there but the pair rule no longer pairs them. For a removed tag the cause is looked up in this order:
  key wins      key/key_wins.tsv drops it (the answer key calls the review's tag wrong)
  switch-off    a weak old pattern of that concept was switched off in that game (step3/decisions.tsv '(?!)')
  undo          final/revert.tsv undoes that concept in that game
  other         any other step (narrowing, keyword rule, parent rule...), named by the old tag's method
On key entries the lost tag is also judged by the key (right / wrong). Writes final/lost_pairs.tsv (every lost pair) and prints a
summary per cause and game. Usage: lost_pairs.py <old.sqlite> <new.sqlite>"""
import collections, csv, os, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, 'key'))
import key as K
o, n = sqlite3.connect(sys.argv[1]), sqlite3.connect(sys.argv[2])
kw = {(int(r['entity']), r['concept']) for r in csv.DictReader(open(os.path.join(HERE, 'key', 'key_wins.tsv')), delimiter='\t') if r['action'] == 'drop'} if os.path.exists(os.path.join(HERE, 'key', 'key_wins.tsv')) else set()
off = set()
for l in open(os.path.join(HERE, 'step3', 'decisions.tsv'), encoding='utf-8'):
    if l.startswith('narrow\t') and l.rstrip('\n').endswith('\t(?!)'):
        k = l.split('\t')[1].split('|')[0]
        for g in l.split('\t')[2].split(','): off.add((g, k))
rf = os.path.join(HERE, 'final', 'revert.tsv')
undo = {(r[1], r[2]) for r in (l.rstrip('\n').split('\t') for l in open(rf) if l.startswith('undo\t'))} if os.path.exists(rf) else set()
keys = {int(i): K.narrow({k for k, _ in v['tags']}) for g in K.GAMES for i, v in K.load(g).items()}
def judge(e, k):
    if e not in keys: return ''
    ks = keys[e]; ok = ks | {a for x in ks for a in K.ANC[x]} | {d for x in ks for d in K.DESC[x]}
    return 'right' if k in ok else 'wrong'
newtags = collections.defaultdict(set)
for e, k in n.execute('SELECT entity, concept FROM entity_concepts'): newtags[e].add(k)
oldm = collections.defaultdict(set)
for e, k, m in o.execute('SELECT entity, concept, method FROM entity_concepts'): oldm[e, k].add(m)
newp = {(e, t, f) for e, t, f in n.execute('SELECT entity, trigger, effect FROM trigger_effect')}
live = {i for i, in n.execute('SELECT id FROM entities')}
rows = []; summ = collections.Counter(); judged = collections.Counter()
for e, g, t, f in o.execute('SELECT DISTINCT entity, game, trigger, effect FROM trigger_effect'):
    if (e, t, f) in newp or e not in live: continue
    gone = [k for k in (t, f) if k not in newtags[e]]
    if not gone: cause, k = 'pair rule', ''
    else:
        k = gone[0]
        cause = 'key wins' if (e, k) in kw else 'switch-off' if (g, k) in off else 'undo' if (g, k) in undo else 'other: ' + ','.join(sorted(oldm[e, k])) or 'other'
    j = judge(e, k) if k else ''
    rows.append((g, e, t, f, k, cause, j)); summ[cause] += 1; judged[cause, j] += 1
os.makedirs(os.path.join(HERE, 'final'), exist_ok=True)
with open(os.path.join(HERE, 'final', 'lost_pairs.tsv'), 'w', encoding='utf-8') as fh:
    fh.write('game\tentity\ttrigger\teffect\tremoved tag\tcause\tkey says the removed tag is\n')
    for r in sorted(rows): fh.write('\t'.join(map(str, r)) + '\n')
print('lost pairs', len(rows))
for c, v in summ.most_common():
    print(f'{v:7}  {c:40}  on key entries: right {judged[c, "right"]}, wrong {judged[c, "wrong"]}')
