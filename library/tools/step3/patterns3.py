"""Step 3 of the tag-fix plan: score the wording patterns, per game, on the answer key and on samples of their own matches.
Scripts print counts and sampled lines only.

  patterns3.py eval [db]          every pattern row x every game it reaches: matches, key matches, key right (from key/<game>/key.json)
                                  -> step3/eval.tsv. A key match is right when the key's concepts for that entry include the pattern's
                                  concept, a narrower one, or a broader one below the four branches (as key.py scores).
  patterns3.py sample [db] [N]    the next N patterns in plan order (most matches first) that have no judgment yet: up to 10 random
                                  matches outside the key per game (seed 1) -> judgment questions, one per distinct (entry, concept),
                                  written as step3/judge/<NNN>.txt batches of 60. Identical texts are asked once.
  patterns3.py results            judgments + key -> step3/results.tsv (pattern, game, matches, key n/right, sample n/right, verdict)
                                  and step3/to_read/<game>.txt (matches a weak pattern still cannot tell apart)

Verdicts per pattern and game: 'ok' (90%+ right), 'weak' (below 90%: narrow), 'thin' (one or two key matches and no sample).
When a pattern has one or two key matches in a game, it passes or fails on the outside sample alone, and that sample gets two
readers and a third for disagreements (agreed with Kaptain, 13 Oct 2026)."""
import collections, glob, json, os, random, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.dirname(HERE); KEY = os.path.join(TOOLS, 'key')
sys.path.insert(0, TOOLS); sys.path.insert(0, KEY)
from concept_tree import TREE
import key as K
DB = os.path.join(os.path.dirname(TOOLS), 'three-bases-library.sqlite')
GAMES = K.GAMES

def norm_text(g, name, text):
    low = (text or '').lower()
    if g == 'mtg': low = re.sub(r'\([^()]*\)', ' ', low)
    for x in [name] + (name or '').split(' // '):
        if x and len(x) > 2: low = low.replace(x.lower(), 'name')
    return low

def load(db):
    c = sqlite3.connect(db)
    ents = collections.defaultdict(list); raw = {}
    for i, g, n, t in c.execute('SELECT id, game, name, text FROM entities'):
        ents[g].append((i, norm_text(g, n, t))); raw[i] = (g, n, t or '')
    pats = c.execute('SELECT rowid, concept, role, pattern, game FROM concept_patterns ORDER BY rowid').fetchall()
    return c, ents, raw, pats

def keys():
    out = {}
    for g in GAMES:
        f = os.path.join(KEY, g, 'key.json')
        if os.path.exists(f):
            out[g] = {int(i): K.narrow({k for k, _ in v['tags']}) for i, v in json.load(open(f)).items()}
    return out

def right(concept, kset):
    ok = set(kset) | {a for k in kset for a in K.ANC[k] if a not in K.GROUPS} | {d for k in kset for d in K.DESC[k]}
    return concept in ok

def pid(concept, role, pattern, game): return f'{concept}|{role}|{game or "*"}|{pattern}'

def evaluate(db):
    c, ents, raw, pats = load(db); ky = keys()
    rows = []
    for rid, k, role, p, g in pats:
        if k not in TREE: continue
        try: rx = re.compile(p, re.I)
        except re.error: continue
        for gg in ([g] if g else [x for x in GAMES if x != 'marvel_snap']):
            hits = [i for i, t in ents[gg] if rx.search(t)]
            if not hits: continue
            kk = ky.get(gg, {})
            km = [i for i in hits if i in kk]; kr = sum(1 for i in km if right(k, kk[i]))
            rows.append((pid(k, role, p, g), gg, len(hits), len(km), kr))
    with open(os.path.join(HERE, 'eval.tsv'), 'w') as fh:
        fh.write('pattern\tgame\tmatches\tkey_n\tkey_right\n')
        for r in rows: fh.write('\t'.join(map(str, r)) + '\n')
    weak = [r for r in rows if r[3] >= 3 and r[4] / r[3] < 0.9]
    print('pattern x game pairs', len(rows), ' with 3+ key matches', sum(1 for r in rows if r[3] >= 3), ' below 90% on the key', len(weak),
          ' matches in weak pairs', sum(r[2] for r in weak))

def plan_order():
    rows = [l.rstrip('\n').split('\t') for l in open(os.path.join(HERE, 'eval.tsv'))][1:]
    tot = collections.Counter()
    for p, g, m, kn, kr in rows: tot[p] += int(m)
    return rows, [p for p, _ in tot.most_common()]

def judged():
    out = {}
    for f in glob.glob(os.path.join(HERE, 'judge', '*.json')) + glob.glob(os.path.join(HERE, 'judge', '*', '*.json')):
        pass
    return out

def sample(db, n):
    c, ents, raw, pats = load(db); ky = keys()
    rows, order = plan_order()
    jd = os.path.join(HERE, 'judge'); os.makedirs(jd, exist_ok=True)
    qfile = os.path.join(HERE, 'questions.json')
    Q = json.load(open(qfile)) if os.path.exists(qfile) else {'q': {}, 'pairs': {}}   # q: qid -> [entity, concept, double]; pairs: pattern|game -> qids
    done_p = {k.rsplit('@', 1)[0] for k in Q['pairs']}
    todo = [p for p in order if p not in done_p][:n]
    bygame = collections.defaultdict(list)
    for r in rows:
        if r[0] in todo: bygame[r[0]].append(r)
    textq = {}
    for qid, (e, k, dbl) in Q['q'].items(): textq[(raw[e][2].strip().lower(), raw[e][0], k)] = qid
    newq = []
    for p in todo:
        k, role, g, pat = p.split('|', 3); rx = re.compile(pat, re.I)
        for _, gg, m, kn, kr in bygame[p]:
            kk = ky.get(gg, {})
            hits = sorted(i for i, t in ents[gg] if rx.search(t) and i not in kk)
            pick = hits if len(hits) <= 10 else random.Random(1).sample(hits, 10)
            dbl = int(kn) <= 2
            qs = []
            for e in pick:
                tk = (raw[e][2].strip().lower(), gg, k)
                qid = textq.get(tk)
                if qid is None:
                    qid = str(len(Q['q'])); Q['q'][qid] = [e, k, dbl]; textq[tk] = qid; newq.append(qid)
                elif dbl and not Q['q'][qid][2]:
                    Q['q'][qid][2] = True; newq.append(qid)   # needs a second reader now
                qs.append(qid)
            Q['pairs'][p + '@' + gg] = qs
    json.dump(Q, open(qfile, 'w'))
    # batches of 60 new questions, grouped by game and concept so a reader sees one definition many times
    newq = sorted(set(newq), key=lambda q: (raw[Q['q'][q][0]][0], Q['q'][q][1], int(q)))
    start = len(glob.glob(os.path.join(jd, '*.txt')))
    for b in range(0, len(newq), 60):
        part = newq[b:b + 60]; ks = sorted({Q['q'][q][1] for q in part})
        with open(os.path.join(jd, f'{start + b // 60:03d}.txt'), 'w') as fh:
            fh.write('# definitions\n')
            for k in ks: fh.write(f"{k} | {TREE[k]['name']} | {TREE[k]['counts']} | Not: {TREE[k]['no']}\n")
            fh.write('# questions: qid | concept | game | name | text\n')
            for q in part:
                e, k, dbl = Q['q'][q]; g, nm, t = raw[e]
                tt = t.replace(chr(10), ' / '); tt = tt if len(tt) <= 700 else tt[:700] + ' ...'
                fh.write(f"{q}{'*' if dbl else ''} | {k} | {g} | {nm} | {tt}\n")
    print('patterns sampled', len(todo), ' questions so far', len(Q['q']), ' new', len(newq), ' new batches', (len(newq) + 59) // 60)

def answers():
    """qid -> verdict (True right / False wrong / None unsettled). Single questions: reader A. Double ones (*): A and B, C if they differ."""
    A, B, C = {}, {}, {}
    for r, d in (('A', A), ('B', B), ('C', C)):
        for f in glob.glob(os.path.join(HERE, 'judge', r, '*.json')): d.update(json.load(open(f)))
    Q = json.load(open(os.path.join(HERE, 'questions.json')))
    out = {}
    for q, (e, k, dbl) in Q['q'].items():
        a = A.get(q)
        if not dbl: out[q] = None if a is None else a == 'yes'
        else:
            b = B.get(q)
            if a is not None and a == b: out[q] = a == 'yes'
            elif q in C: out[q] = C[q] == 'yes'
            else: out[q] = None
    return Q, out, A, B

def results():
    Q, ans, A, B = answers(); rows, order = plan_order(); ky = keys()
    os.makedirs(os.path.join(HERE, 'to_read'), exist_ok=True)
    res = []; toread = collections.defaultdict(set)
    for p, g, m, kn, kr in rows:
        qs = Q['pairs'].get(p + '@' + g)
        if qs is None: continue
        vals = [ans[q] for q in qs if ans.get(q) is not None]
        kn, kr = int(kn), int(kr); sn, sr = len(vals), sum(vals)
        if any(ans.get(q) is None for q in qs): verdict = 'pending'
        elif kn <= 2: verdict = ('ok' if sr >= 0.9 * sn else 'weak') if sn else 'thin'
        else:
            n, r = kn + sn, kr + sr
            verdict = 'ok' if r >= 0.9 * n else 'weak'
        res.append((p, g, m, kn, kr, sn, sr, verdict))
    with open(os.path.join(HERE, 'results.tsv'), 'w') as fh:
        fh.write('pattern\tgame\tmatches\tkey_n\tkey_right\tsample_n\tsample_right\tverdict\n')
        for r in res: fh.write('\t'.join(map(str, r)) + '\n')
    print(collections.Counter(r[-1] for r in res))

# ---------- narrowing (after the sample judgments are in) ----------
def snippet(low, rx, w=90):
    m = rx.search(low)
    if not m: return low[:2 * w]
    a = max(0, m.start() - w); b = min(len(low), m.end() + w)
    return ('...' if a else '') + low[a:m.start()] + '[[' + low[m.start():m.end()] + ']]' + low[m.end():b] + ('...' if b < len(low) else '')

def labelled(p, games, ents, raw, ky, Q, ans):
    """Known right/wrong matches of pattern p in the games: key entries and judged sample entries."""
    k, role, g, pat = p.split('|', 3); rx = re.compile(pat, re.I)
    q_of = {}
    for qid, (e, kk, d) in Q['q'].items():
        if kk == k: q_of[e] = qid
    textq = {}
    for qid, (e, kk, d) in Q['q'].items():
        if kk == k: textq[(raw[e][2].strip().lower(), raw[e][0])] = qid
    out = []
    for gg in games:
        kk = ky.get(gg, {})
        for i, t in ents[gg]:
            if not rx.search(t): continue
            if i in kk: out.append((gg, i, right(k, kk[i]), 'key', t))
            else:
                qid = q_of.get(i) or textq.get((raw[i][2].strip().lower(), gg))
                if qid is not None and ans.get(qid) is not None: out.append((gg, i, ans[qid], 'judged', t))
    return out

def pack(n_per_file=12):
    """Weak patterns (results.tsv), in plan order -> narrow/NN.md work files with labelled examples."""
    c, ents, raw, pats = load(DB); ky = keys(); Q, ans, A, B = answers()
    res = [l.rstrip('\n').split('\t') for l in open(os.path.join(HERE, 'results.tsv'))][1:]
    rows, order = plan_order()
    weak = collections.defaultdict(list)
    for p, g, m, kn, kr, sn, sr, v in res:
        if v == 'weak': weak[p].append(g)
    todo = [p for p in order if p in weak]
    d = os.path.join(HERE, 'narrow'); os.makedirs(d, exist_ok=True)
    for f in glob.glob(os.path.join(d, '[0-9]*.md')): os.remove(f)
    for b in range(0, len(todo), n_per_file):
        with open(os.path.join(d, f'{b // n_per_file:02d}.md'), 'w') as fh:
            for p in todo[b:b + n_per_file]:
                k, role, g, pat = p.split('|', 3); rx = re.compile(pat, re.I)
                lab = labelled(p, weak[p], ents, raw, ky, Q, ans)
                fh.write(f"\n## PATTERN {p}\nconcept {k}: {TREE[k]['counts']} Not: {TREE[k]['no']}\nweak in: {', '.join(weak[p])}\n")
                rnd = random.Random(1)
                for lbl, val in (('WRONG', False), ('RIGHT', True)):
                    xs = [x for x in lab if x[2] == val]; rnd.shuffle(xs)
                    fh.write(f"{lbl} ({len(xs)} known):\n")
                    for gg, i, ok, src, t in xs[:14]: fh.write(f"  {gg} {i}: {snippet(t, rx)}\n")
    print('weak patterns', len(todo), 'files', (len(todo) + n_per_file - 1) // n_per_file)

def trial(p, newpat, games=None):
    """Compare a narrowed regex with the old one on the known (key + judged) matches and count what it drops."""
    c, ents, raw, pats = load(DB); ky = keys(); Q, ans, A, B = answers()
    k, role, g, pat = p.split('|', 3); old = re.compile(pat, re.I); new = re.compile(newpat, re.I)
    games = games or ([g] if g != '*' else [x for x in GAMES if x != 'marvel_snap'])
    lab = {(gg, i): ok for gg, i, ok, src, t in labelled(p, games, ents, raw, ky, Q, ans)}
    tot = [0, 0, 0, 0, 0, 0]
    for gg in games:
        om = {i for i, t in ents[gg] if old.search(t)}; nm = {i for i, t in ents[gg] if new.search(t)}
        if not om: continue
        kn = [lab[(gg, i)] for i in nm if (gg, i) in lab]; lost_right = sum(1 for i in om - nm if lab.get((gg, i)) is True)
        dropped_known = [lab[(gg, i)] for i in om - nm if (gg, i) in lab]
        print(f'{gg:18} matches {len(om):5} -> {len(nm):5}  known kept {len(kn):3} right {sum(kn):3} ({100 * sum(kn) / max(len(kn), 1):.0f}%)  '
              f'known dropped {len(dropped_known):3} of them right {lost_right}  new matches {len(nm - om)}')

if __name__ == '__main__':
    cmd, *a = sys.argv[1:]
    if cmd == 'eval': evaluate(a[0] if a else DB)
    elif cmd == 'sample': sample(DB, int(a[0]) if a else 50)
    elif cmd == 'results': results()
    elif cmd == 'pack': pack()
    elif cmd == 'try': trial(a[0], a[1], a[2].split(',') if len(a) > 2 else None)
