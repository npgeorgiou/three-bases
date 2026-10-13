"""Answer key (Step 2 of the tag-fix plan, 13 Oct 2026). It only measures: it is never used to fix library entries and never
edited to agree with the library. Prints counts and sampled lines only.

  key.py defs                         concept definitions for the readers -> key/defs.txt (id | name | counts | not)
  key.py sample <game|all>            200 entries per game, seed 1 (all of a game with 400 or fewer), plus the entries named
                                      in tools/audit/<game>_judgments.json -> key/<game>/entries.json and batch_NN.txt (50 each)
  key.py check <game> <reader>        quote check of key/<game>/<reader>/batch_NN.json: a tag whose words are not in the entry's
                                      text, or whose concept does not exist, is rejected -> <reader>/clean.json (+ rejected count)
  key.py disagree <game> [prefix]     entries where readers A and B differ and C has not settled -> key/<game>/<prefix>_NN.txt
                                      (prefix settle, or covsettle for the coverage round) for the third reader (C)
  key.py final <game>                 agreed tags + C's decisions (quote-checked) -> key/<game>/key.json
  key.py coverage <game>              concepts on fewer than 5 key entries of the game: candidates found by the concept's typical
                                      words (its wording patterns) among the game's other entries -> key/<game>/cov_NN.txt batches
                                      (read like the key; their tags come from reading, never from the search)
  key.py score <db> [game ...]        wrong tags and missed mechanics per 100 key entries (script; see SCORING below)

Reader output (one file per batch): {"<entity id>": [["concept", "exact words from the text"], ...], ...}; an entry with no
mechanic gets []. C's output for a settle batch has the same form and lists the final tags of each entry it settles.

SCORING. Key concepts K (narrowest, as read) and library tags L of an entry, any role. Game-structure tags (method
game_structure: "this game has lanes") and cost-data tags (data_rule) are left out on both sides, since they are not read
from the text. A library tag is right when it is a key concept, an ancestor of one, or a descendant of one; otherwise wrong.
A key concept is missed when no library tag is that concept, a descendant of it, or an ancestor of it below the four
branches and the roots. An older database is scored after its tags are moved through the Step 1 map (concept_tree.py)."""
import json, os, random, re, sqlite3, sys, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.dirname(HERE)
sys.path.insert(0, TOOLS)
from concept_tree import TREE, targets, MAP, REMOVED
DB = os.environ.get('TB_LIB', os.path.join(os.path.dirname(TOOLS), 'three-bases-library.sqlite'))
GROUPS = {'effect', 'helps_me', 'hurts_enemy', 'drawback', 'game_rules'} | {i for i, d in TREE.items() if not d['parents']}
def gdir(g): d = os.path.join(HERE, g); os.makedirs(d, exist_ok=True); return d
def norm(s): return re.sub(r'\s+', ' ', (s or '').lower().replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')).strip()
KIDS = collections.defaultdict(set)
for i, d in TREE.items():
    for p in d['parents']: KIDS[p].add(i)
def desc(i, s=None):
    s = s if s is not None else set()
    for k in KIDS[i]:
        if k not in s: s.add(k); desc(k, s)
    return s
def anc(i, s=None):
    s = s if s is not None else set()
    for p in TREE[i]['parents']:
        if p not in s: s.add(p); anc(p, s)
    return s
DESC = {i: desc(i) for i in TREE}; ANC = {i: anc(i) for i in TREE}

def db(): return sqlite3.connect(DB)

def defs():
    out = [f"{i} | {d['name']} | {d['counts']} | Not: {d['no']}" for i, d in TREE.items() if d['facet'] != 'problem' and i not in GROUPS]
    open(os.path.join(HERE, 'defs.txt'), 'w').write('\n'.join(out) + '\n'); print('defs:', len(out), 'concepts')

def sample(g):
    c = db()
    ids = sorted(i for i, in c.execute('SELECT id FROM entities WHERE game=?', (g,)))
    pick = ids if len(ids) <= 400 else random.Random(1).sample(ids, 200)
    jf = os.path.join(TOOLS, 'audit', f'{g}_judgments.json')
    live = set(ids)
    extra = [int(i) for i in json.load(open(jf))] if os.path.exists(jf) else []
    sel = list(dict.fromkeys(pick + [i for i in extra if i in live]))
    rows = {i: (n, t) for i, n, t in c.execute('SELECT id, name, text FROM entities WHERE game=?', (g,))}
    ents = [{'id': i, 'name': rows[i][0], 'text': rows[i][1] or ''} for i in sel]
    d = gdir(g); json.dump(ents, open(os.path.join(d, 'entries.json'), 'w'), indent=0)
    for f in glob.glob(os.path.join(d, 'batch_*.txt')): os.remove(f)
    for b in range(0, len(ents), 50):
        with open(os.path.join(d, f'batch_{b // 50:02d}.txt'), 'w') as fh:
            for e in ents[b:b + 50]: fh.write(f"{e['id']} | {e['name']} | {e['text'].replace(chr(10), ' / ')}\n")
    print(g, 'key entries', len(ents), '(random', len(pick), '+ audit', len(sel) - len(pick), ') batches', (len(ents) + 49) // 50)

def texts(g):
    return {e['id']: e for e in json.load(open(os.path.join(gdir(g), 'entries.json')))} | \
           {e['id']: e for f in glob.glob(os.path.join(gdir(g), 'cov_entries.json')) for e in json.load(open(f))}

def check_tags(ent, tags):
    ok, bad = [], []
    t = norm(ent['name'] + ' ' + ent['text'])
    for x in tags:
        if not (isinstance(x, list) and len(x) == 2): bad.append((x, 'form')); continue
        k, w = x[0].strip(), norm(x[1])
        if k not in TREE or k in GROUPS or TREE[k]['facet'] == 'problem': bad.append((x, 'concept')); continue
        if not w or w not in t: bad.append((x, 'words')); continue
        ok.append([k, x[1]])
    return ok, bad

def check(g, r):
    ents = texts(g); clean = {}; nb = collections.Counter(); ex = []
    for f in sorted(glob.glob(os.path.join(gdir(g), r, '*.json'))):
        if f.endswith('clean.json'): continue
        for i, tags in json.load(open(f)).items():
            e = ents.get(int(i))
            if not e: nb['unknown entry'] += 1; continue
            ok, bad = check_tags(e, tags); clean[i] = ok
            for x, why in bad: nb[why] += 1; ex.append((i, x, why))
    json.dump(clean, open(os.path.join(gdir(g), r, 'clean.json'), 'w'), indent=0)
    print(g, r, 'entries', len(clean), 'tags kept', sum(map(len, clean.values())), 'rejected', dict(nb))
    for x in ex[:5]: print('  rejected', x)
    return clean

def narrow(ks):   # keep the narrowest: drop a concept when a descendant of it is also there
    return {k for k in ks if not (DESC[k] & ks)}

def disagree(g, prefix='settle'):
    a = check(g, 'A'); b = check(g, 'B'); ents = texts(g); d = gdir(g)
    done = set(check(g, 'C')) if os.path.isdir(os.path.join(d, 'C')) else set()
    for f in glob.glob(os.path.join(d, prefix + '_*.txt')): os.remove(f)
    todo = []
    for i in sorted((set(a) | set(b)) - done, key=int):
        ka, kb = narrow({k for k, _ in a.get(i, [])}), narrow({k for k, _ in b.get(i, [])})
        if ka != kb: todo.append(i)
    for n in range(0, len(todo), 50):
        with open(os.path.join(d, f'{prefix}_{n // 50:02d}.txt'), 'w') as fh:
            for i in todo[n:n + 50]:
                e = ents[int(i)]
                fh.write(f"{i} | {e['name']} | {e['text'].replace(chr(10), ' / ')}\n   A: {json.dumps(a.get(i, []), ensure_ascii=False)}\n   B: {json.dumps(b.get(i, []), ensure_ascii=False)}\n")
    print(g, 'entries read by both', len(set(a) & set(b)), 'disagreements', len(todo), 'settle batches', (len(todo) + 49) // 50)

def final(g):
    a = check(g, 'A'); b = check(g, 'B'); ents = texts(g)
    cdir = os.path.join(gdir(g), 'C'); csets = {}
    if os.path.isdir(cdir): csets = check(g, 'C')
    key = {}; nc = 0; miss = []
    for i in sorted(set(a) & set(b), key=int):
        ka, kb = narrow({k for k, _ in a[i]}), narrow({k for k, _ in b[i]})
        if ka == kb: key[i] = {'tags': a[i], 'by': 'A=B'}
        elif i in csets: key[i] = {'tags': csets[i], 'by': 'C'}; nc += 1
        else: miss.append(i)
    json.dump(key, open(os.path.join(gdir(g), 'key.json'), 'w'), indent=0)
    print(g, 'key entries', len(key), 'settled by C', nc, 'still unsettled', len(miss))

def coverage(g):
    d = gdir(g); key = json.load(open(os.path.join(d, 'key.json')))
    cnt = collections.Counter(k for v in key.values() for k in narrow({k for k, _ in v['tags']}) | {a for k, _ in v['tags'] for a in ANC[k]})
    low = [k for k in TREE if k not in GROUPS and TREE[k]['facet'] != 'problem' and cnt[k] < 5]
    c = db(); pats = collections.defaultdict(list)
    for k, p, gg in c.execute('SELECT concept, pattern, game FROM concept_patterns'):
        if gg in (None, g):
            try: pats[k].append(re.compile(p, re.I))
            except re.error: pass
    inkey = {int(i) for i in key}
    rows = [(i, n, t or '') for i, n, t in c.execute('SELECT id, name, text FROM entities WHERE game=?', (g,)) if i not in inkey]
    rnd = random.Random(1); cand = {}
    for k in low:
        need = 5 - cnt[k]; rx = pats.get(k, [])
        if not rx: continue
        hits = [r for r in rows if any(x.search(r[2].lower()) for x in rx) and r[0] not in cand]
        rnd.shuffle(hits)
        for r in hits[:need]: cand[r[0]] = r   # round 1: as many as the concept still needs; later rounds take more
    ents = [{'id': i, 'name': n, 'text': t} for i, n, t in cand.values()]
    json.dump(ents, open(os.path.join(d, 'cov_entries.json'), 'w'), indent=0)
    for f in glob.glob(os.path.join(d, 'cov_*.txt')): os.remove(f)
    for b in range(0, len(ents), 50):
        with open(os.path.join(d, f'cov_{b // 50:02d}.txt'), 'w') as fh:
            for e in ents[b:b + 50]: fh.write(f"{e['id']} | {e['name']} | {e['text'].replace(chr(10), ' / ')}\n")
    print(g, 'concepts under 5:', len(low), 'with patterns to search:', sum(1 for k in low if pats.get(k)), 'candidates', len(ents))

def lib_tags(c, ids, old=False):
    out = collections.defaultdict(set)
    txt = dict(c.execute('SELECT id, text FROM entities'))
    q = 'SELECT entity, concept, method FROM entity_concepts WHERE entity IN (%s)' % ','.join(str(i) for i in ids)
    for e, k, m in c.execute(q):
        if m in ('game_structure', 'data_rule'): continue
        ks = targets(k, txt.get(e)) if (old and (k in MAP or k in REMOVED)) else {k}
        out[e] |= {x for x in ks if x in TREE}
    return out

def score(dbpath, games):
    c = sqlite3.connect(dbpath)
    old = not c.execute("SELECT 1 FROM concepts WHERE id='helps_me'").fetchone()
    tot = [0, 0, 0]
    for g in games:
        f = os.path.join(HERE, g, 'key.json')
        if not os.path.exists(f): continue
        key = json.load(open(f)); ids = [int(i) for i in key]
        live = {i for i, in c.execute('SELECT id FROM entities WHERE game=?', (g,))}
        ids = [i for i in ids if i in live]
        L = lib_tags(c, ids, old)
        wrong = missed = 0
        for i in ids:
            K = narrow({k for k, _ in key[str(i)]['tags']})
            ok = set(K) | {a for k in K for a in ANC[k]} | {d for k in K for d in DESC[k]}
            wrong += sum(1 for l in L[i] if l not in ok and l not in GROUPS)
            for k in K:
                near = {k} | DESC[k] | (ANC[k] - GROUPS)
                if not (L[i] & near): missed += 1
        n = len(ids); tot[0] += n; tot[1] += wrong; tot[2] += missed
        print(f'{g:18} entries {n:4}  wrong/100 {100 * wrong / max(n, 1):6.1f}  missed/100 {100 * missed / max(n, 1):6.1f}')
    print(f"{'all':18} entries {tot[0]:4}  wrong/100 {100 * tot[1] / max(tot[0], 1):6.1f}  missed/100 {100 * tot[2] / max(tot[0], 1):6.1f}")

GAMES = ['into_the_breach', 'wh_bloodbowl3', 'inscryption', 'faeria', 'duelyst', 'sts1', 'marvel_snap', 'darkest_dungeon', 'dnd5e', 'sts2',
         'gwent', 'hs_battlegrounds', 'wh_killteam', 'runeterra', 'wh_underworlds', 'wh_aos_4th', 'wh_40k_10e', 'shadowverse', 'hearthstone', 'mtg']
if __name__ == '__main__':
    cmd, *a = sys.argv[1:]
    if cmd == 'defs': defs()
    elif cmd == 'sample': [sample(g) for g in (GAMES if a[0] == 'all' else a)]
    elif cmd == 'check': check(a[0], a[1])
    elif cmd == 'disagree': disagree(*a)
    elif cmd == 'final': final(a[0])
    elif cmd == 'coverage': coverage(a[0])
    elif cmd == 'score': score(a[0], a[1:] or GAMES)
