"""Which stored patterns (concept_patterns: general and the game's) give a concept to the game's key entries whose key lacks it, with one
example each; "(none)" = no stored pattern matches, so another step added the tag. Usage: pattern_hits.py <db> <game> <concept> ..."""
import sys, sqlite3, re, json, collections
import os; HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import reading as RD
db, g, cons = sys.argv[1], sys.argv[2], sys.argv[3:]
c = sqlite3.connect(db); key = json.load(open(os.path.join(HERE, 'key', g, 'key.json')))
for con in cons:
    pats = c.execute('SELECT pattern, game FROM concept_patterns WHERE concept=? AND (game IS NULL OR game=?)', (con, g)).fetchall()
    ents = c.execute(f"SELECT e.id, e.name, e.text FROM entities e JOIN entity_concepts ec ON ec.entity=e.id WHERE ec.concept=? AND ec.method='text_pattern' AND e.id IN ({','.join(key)})", (con,)).fetchall()
    cnt = collections.Counter(); ex = {}
    for i, n, t in ents:
        if any(x[0] == con for x in key[str(i)]['tags']): continue
        low = RD.strip(g, (t or '').lower()).replace(n.lower(), 'name') if len(n) > 2 else RD.strip(g, (t or '').lower())
        hit = [p for p, gg in pats if re.search(p, low, re.I)] or ['(none)']
        for p in hit:
            cnt[p] += 1
            m = re.search(p, low, re.I) if p != '(none)' else None
            ex.setdefault(p, f"{n}: ...{low[max(0, m.start()-40):m.end()+30] if m else low[:80]}...")
    print('==', con)
    for p, n in cnt.most_common(8): print(f'  {n:3} {p[:110]}  e.g. {ex[p][:170]!r}')
