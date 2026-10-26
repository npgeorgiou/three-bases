"""Gold sample for step 2 of the test. `pick`: per game 10 random entries + 5 targeted ones (seed 1) -> gold/sample.json, each with
its text, its computed abilities (the tags grouped) and its computed trigger pairs (what the reading checks).
`score`: compares gold/<game>.json with the abilities -> per game, the share of tags whose row mates are right, and of right pairs.
Gold file format, per entry id: {"rows": [["concept", ...], ...] (the tags that belong together; whole-card tags in one row),
"pairs": [["trigger", "effect"], ...]}.  Usage: gold.py pick|score <copy.sqlite>"""
import collections, json, os, random, re, sys
import common as C

TARGETS = [('choose', r'\bchoose (one|two|three|any)\b'), ('instead', r'\bwould\b[^.]*\binstead\b'), ('for each', r'\bfor each\b'),
           ('X cost', r'\{X\}|\bX\b'), ('multi-sentence', None), ('keyword list', None), ('blocks', None)]
BLOCK_GAMES = {'sts1', 'sts2', 'darkest_dungeon', 'wh_40k_10e', 'wh_aos_4th'}   # Spire intents, Darkest Dungeon skills, ability blocks

def entry(c, e):
    q = lambda s, *a: c.execute(s, a).fetchall()
    g, n, t = q('SELECT game, name, text FROM entities WHERE id=?', e)[0]
    rows = []
    for r, k, tr in q('SELECT id, kind, triggers FROM abilities WHERE entity=? ORDER BY ord', e):
        rows.append({'kind': k, 'triggers': tr, 'tags': sorted(x for (x,) in q(
            'SELECT DISTINCT ec.concept FROM ability_tags t JOIN entity_concepts ec ON ec.rowid=t.rid WHERE t.ability=?', r))})
    pairs = sorted(set(q('SELECT trigger, effect FROM records_pairs WHERE entity=?', e)))
    return {'id': e, 'game': g, 'name': n, 'text': t, 'rows': rows, 'pairs': [list(x) for x in pairs]}

def pick(c):
    rnd = random.Random(1); out = []
    nab = collections.Counter(e for (e,) in c.execute("SELECT entity FROM abilities WHERE kind != 'card'"))
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
    print('entries', len(out), 'rows', sum(len(d['rows']) for d in out), 'pairs', sum(len(d['pairs']) for d in out))

def score(c):
    res = {}
    for f in sorted(os.listdir(os.path.join(C.HERE, 'gold'))):
        if f == 'sample.json' or not f.endswith('.json'): continue
        gold = json.load(open(os.path.join(C.HERE, 'gold', f), encoding='utf-8')); tr = tt = pr = pt = 0
        for i, gd in gold.items():
            d = entry(c, int(i))
            mates = lambda rows: {k: frozenset(r) - {k} for r in rows for k in r}
            want, got = mates(gd['rows']), mates([r['tags'] for r in d['rows']])
            for k in want: tt += 1; tr += got.get(k) == want[k]
            wp, gp = {tuple(x) for x in gd['pairs']}, {tuple(x) for x in d['pairs']}
            pt += len(wp | gp); pr += len(wp & gp)
        res[f[:-5]] = (tr, tt, pr, pt)
        print(f"{f[:-5]:18} tags with the right row mates {tr}/{tt}  pairs right {pr}/{pt}")
    return res

if __name__ == '__main__':
    c = C.connect(sys.argv[2]); {'pick': pick, 'score': score}[sys.argv[1]](c)
