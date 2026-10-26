"""Gold sample for step 2 of the test. `pick`: per game 10 random entries + 5 targeted ones (seed 1) -> gold/sample.json, each with
its text, the computed abilities and pieces, its tags with their piece and the computed trigger pairs (what the reading checks).
`score`: compares gold/<game>.json with the computed structure -> per-game share of tags in the right piece and of right pairs.
Gold file format, per entry id: {"pieces": ["exact text of each correct piece", ...], "tags": {"concept": "exact text of the
piece holding it"}, "pairs": [["trigger", "effect"], ...]}.  Usage: gold.py pick|score <copy.sqlite>"""
import collections, json, os, random, re, sys
import common as C

TARGETS = [('choose', r'\bchoose (one|two|three|any)\b'), ('instead', r'\bwould\b[^.]*\binstead\b'), ('for each', r'\bfor each\b'),
           ('X cost', r'\{X\}|\bX\b'), ('multi-sentence', None), ('keyword list', None), ('blocks', None)]
BLOCK_GAMES = {'sts1', 'sts2', 'darkest_dungeon', 'wh_40k_10e', 'wh_aos_4th'}   # Spire intents, Darkest Dungeon skills, ability blocks

def entry(c, e):
    q = lambda s, *a: c.execute(s, a).fetchall()
    g, n, t = q('SELECT game, name, text FROM entities WHERE id=?', e)[0]
    ab = []
    for a, k, p, l in q('SELECT id, kind, ev_pos, ev_len FROM abilities WHERE entity=? ORDER BY ord', e):
        ab.append({'kind': k, 'pieces': [t[x:x + y] for x, y in q('SELECT ev_pos, ev_len FROM pieces WHERE ability=? ORDER BY ord', a)]})
    piece_text = {i: t[x:x + y] for i, x, y in q('SELECT p.id, p.ev_pos, p.ev_len FROM pieces p JOIN abilities a ON a.id=p.ability WHERE a.entity=?', e)}
    tags = sorted({(k, piece_text.get(p)) for k, p in q('SELECT concept, piece FROM entity_concepts WHERE entity=?', e)}, key=lambda x: (x[1] is None, x))
    pairs = sorted(set(q('SELECT trigger, effect FROM records_pairs WHERE entity=?', e)))
    return {'id': e, 'game': g, 'name': n, 'text': t, 'abilities': ab, 'tags': [list(x) for x in tags], 'pairs': [list(x) for x in pairs]}

def pick(c):
    rnd = random.Random(1); out = []
    nab = collections.Counter(e for (e,) in c.execute('SELECT entity FROM abilities'))
    nkw = collections.Counter(e for (e,) in c.execute("SELECT entity FROM abilities WHERE kind='keyword'"))
    for (g,) in c.execute('SELECT DISTINCT game FROM entities ORDER BY game').fetchall():
        pool = [(e, t) for e, t in c.execute("SELECT id, text FROM entities WHERE game=? AND category NOT IN ('keyword','tribe') AND text IS NOT NULL "
                "AND id IN (SELECT entity FROM entity_concepts) AND length(text) < 1500 ORDER BY id", (g,))]
        chosen = rnd.sample([e for e, _ in pool], min(10, len(pool))); why = {e: 'random' for e in chosen}
        targ = []
        for name, rx in (TARGETS[-1:] + TARGETS[:-1] if g in BLOCK_GAMES else TARGETS):
            if name == 'multi-sentence': cand = [e for e, t in pool if len(re.findall(r'[.!?](\s|$)', t)) >= 3]
            elif name == 'keyword list': cand = [e for e, _ in pool if nkw[e] >= 2]
            elif name == 'blocks': cand = [e for e, _ in pool if g in BLOCK_GAMES and nab[e] >= 3]
            else: cand = [e for e, t in pool if re.search(rx, t)]
            cand = [e for e in cand if e not in why]
            if cand: targ.append((name, rnd.choice(cand)))
        for name, e in targ:
            if sum(v != 'random' for v in why.values()) >= 5: break
            if e not in why: why[e] = name
        extra = [e for e, _ in pool if e not in why]   # fewer than five kinds found: random ones fill the five
        while sum(v != 'random' for v in why.values()) < 5 and extra: why[extra.pop(rnd.randrange(len(extra)))] = 'random (fill)'
        for e, w in why.items(): d = entry(c, e); d['why'] = w; out.append(d)
    os.makedirs(os.path.join(C.HERE, 'gold'), exist_ok=True)
    json.dump(out, open(os.path.join(C.HERE, 'gold', 'sample.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('entries', len(out), 'tags', sum(len(d['tags']) for d in out), 'pairs', sum(len(d['pairs']) for d in out))

def score(c):
    sample = {str(d['id']): d for d in json.load(open(os.path.join(C.HERE, 'gold', 'sample.json'), encoding='utf-8'))}
    res = {}
    for f in sorted(os.listdir(os.path.join(C.HERE, 'gold'))):
        if f == 'sample.json' or not f.endswith('.json'): continue
        gold = json.load(open(os.path.join(C.HERE, 'gold', f), encoding='utf-8')); tr = tt = pr = pt = 0
        for i, gd in gold.items():
            d = entry(c, int(i)); have = {k: p for k, p in d['tags']}
            for k, p in gd['tags'].items(): tt += 1; tr += have.get(k) == p
            want, got = {tuple(x) for x in gd['pairs']}, {tuple(x) for x in d['pairs']}
            pt += len(want | got); pr += len(want & got)
        res[f[:-5]] = (tr, tt, pr, pt)
        print(f"{f[:-5]:18} tags in the right piece {tr}/{tt}  pairs right {pr}/{pt}")
    return res

if __name__ == '__main__':
    c = C.connect(sys.argv[2]); {'pick': pick, 'score': score}[sys.argv[1]](c)
