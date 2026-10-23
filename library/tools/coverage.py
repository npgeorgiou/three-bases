"""Coverage scan: the wording that no pattern reads. Every entry's text is cut into clauses (lines and sentences), read as the
patterns read it (reading.py, own name as 'name'); a clause is covered when a general pattern, a pattern of the game (table and
patterns/<game>.txt) or a keyword of the game at its start matches it. Uncovered clauses are grouped by their first words and
printed most common first, with one example each: the mechanics the tagging misses, found without reading every card.
Also, with --mechanics <file> (one mechanic per line: 'name|concept|regex', from guides and wikis), per faction: how many entries
show the mechanic's wording, and how many of those carry the expected concept (or a narrower one) after the build. A faction
whose cards show the wording but lack the concept is a tagging gap (a missing pattern, or a later build step that removed it).
Usage: coverage.py <db> <game> [top_n] [--mechanics <file>] [--keywords]   (top_n 0: only the mechanics)"""
import collections, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import reading as RD, games as G_
args = [a for a in sys.argv[1:] if not a.startswith('--')]; db, G = args[:2]; top = int(args[2]) if len(args) > 2 and args[2].isdigit() else 40
c = sqlite3.connect(db); q = lambda s, *a: c.execute(s, a).fetchall()
pats = []
for (p,) in q('SELECT pattern FROM concept_patterns WHERE game IS NULL OR game=?', G):
    try: pats.append(re.compile(p, re.I))
    except re.error: pass
pf = os.path.join(HERE, 'patterns', G + '.txt')
if os.path.exists(pf):
    for ln in open(pf, encoding='utf-8'):
        if ln.strip() and ln[0] not in '#!': pats.append(re.compile(ln.rstrip('\n').split('|', 2)[2], re.I))
kws = sorted((n.lower() for (n,) in q("SELECT name FROM entities WHERE game=? AND category='keyword'", G)), key=len, reverse=True)
kwstart = re.compile(r'^\W*(' + '|'.join(re.escape(k) for k in kws) + r')\b') if kws else None
ents = q("SELECT id, name, faction, text FROM entities WHERE game=? AND category %s AND text IS NOT NULL" % ("= 'keyword'" if '--keywords' in sys.argv else "NOT IN ('keyword','tribe')"), G)   # --keywords: read the keyword entries (games whose cards only list keywords)
groups = collections.defaultdict(list); ncl = nun = 0
for i, nm, f, t in ents:
    low = RD.strip(G, t.lower()).replace((nm or '').lower(), 'name') if nm and len(nm) > 2 else RD.strip(G, t.lower())
    for cl in re.split(r'\n|(?<=[.!?])\s+', low):
        cl = cl.strip(' /•-–—')
        if len(cl) < 4: continue
        ncl += 1
        if (kwstart and kwstart.match(cl)) or any(p.search(cl) for p in pats): continue
        nun += 1; groups[' '.join(re.findall(r"[a-z']+", cl)[:3])].append(cl)
print(f'{G}: {len(ents)} entries, {ncl} clauses, {nun} not read by any pattern ({nun / max(ncl, 1):.0%})')
for k, v in sorted(groups.items(), key=lambda x: -len(x[1]))[:top]:
    print(f'{len(v):4}  {k:30} e.g. {v[0][:110]}')
if '--mechanics' in sys.argv:
    mf = sys.argv[sys.argv.index('--mechanics') + 1]
    tree = collections.defaultdict(set)
    for r_, i_ in q('SELECT root, id FROM concept_tree'): tree[r_].add(i_)
    for ln in G_.block(mf, 'mechanics'):
        if not ln.strip() or ln.startswith('#'): continue
        name, con, rx = ln.rstrip('\n').split('|', 2); r = re.compile(rx, re.I)
        want = tree.get(con, {con})
        have = {e for (e,) in q('SELECT DISTINCT entity FROM entity_concepts WHERE concept IN (%s)' % ','.join('?' * len(want)), *want)}
        hit = [(i, f) for i, nm, f, t in ents if r.search(RD.strip(G, t.lower()))]
        per = collections.Counter(f for _, f in hit); ok = collections.Counter(f for i, f in hit if i in have)
        gap = sum(per.values()) - sum(ok.values())
        print(f'{"GAP " if hit and gap > len(hit) / 2 else ""}mechanic {name} ({con}): {len(hit)} entries show it, {len(hit) - gap} carry the concept; by faction',
              ', '.join(f'{f} {ok[f]}/{n}' for f, n in per.most_common(5)))
