"""A card that gives a keyword to others ("creatures you control have flying") is not itself doing the keyword's effect.
For every entry with a grants_keyword link to keyword K: each automatic 'does' tag (text_pattern) on a concept of K is
re-checked on the text with K masked where it is given, not where it is an action (Spawn a Frog); if no pattern of that concept still matches, the 'does' tag goes (the
inherited 'grants' tag stays). Entries where K is also the card's own keyword are left alone. Usage: f03_grant_not_does.py <db>"""
import os, re, sqlite3, sys, collections
c = sqlite3.connect(sys.argv[1]); q = lambda s, *a: c.execute(s, a).fetchall()
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
excl = collections.defaultdict(set)
for f in os.listdir(os.path.join(here, 'patterns')):
    for line in open(os.path.join(here, 'patterns', f), encoding='utf-8'):
        if line.startswith('!'): excl[f[:-4]].add(tuple(line[1:].rstrip('\n').split('|', 1)))
pats = collections.defaultdict(list)
for con, role, p, g in q("SELECT concept, role, pattern, game FROM concept_patterns WHERE role='does'"):
    try: pats[con].append((g, p, re.compile(p, re.I)))
    except re.error: pass
kwc = collections.defaultdict(set)
for k, con in q("SELECT entity, concept FROM entity_concepts x JOIN entities e ON e.id=x.entity WHERE e.category='keyword' AND x.role IN ('does','grants')"): kwc[k].add(con)
keep = set()   # tags the hand reviews confirmed (tools/regression.tsv, expect present) are never removed
for line in open(os.path.join(here, 'regression.tsv'), encoding='utf-8'):
    f = line.rstrip('\n').split('\t')
    if len(f) >= 6 and f[5] == 'present' and f[4] in ('does', '*') and f[1].isdigit(): keep.add((int(f[1]), f[3]))
n = 0; C = collections.Counter()
rows = q("""SELECT l.src, l.dst, e.game, e.name, e.text, k.name FROM entity_links l JOIN entities e ON e.id=l.src JOIN entities k ON k.id=l.dst
            WHERE l.rel='grants_keyword' AND NOT EXISTS (SELECT 1 FROM entity_links o WHERE o.src=l.src AND o.dst=l.dst AND o.rel='has_keyword')""")
for i, kid, g, nm, t, kn in rows:
    low = (t or '').lower()
    if g == 'mtg': low = re.sub(r'\([^()]*\)', ' ', low)
    for x in [nm] + nm.split(' // '):
        if len(x) > 2: low = low.replace(x.lower(), 'name')
    kr = re.escape(kn.lower())
    # mask K only where it is given ("gains flying", "give ... Divine Shield", "tokens with flying"), not where it is an action ("Spawn a Frog")
    masked = re.sub(r'(\b(have|has|gains?|give|gives|get|gets|with)\b[^.:;\n]{0,40}?)\b' + kr + r'\b(?!\s+(a|an|one|two|three|\d+|that|the|it|them|x)\b)', lambda m: m.group(1) + '#', low)
    for (con,) in q("SELECT concept FROM entity_concepts WHERE entity=? AND role='does' AND method='text_pattern'", i):
        if con not in kwc[kid] or (i, con) in keep: continue
        ok = [rx for gg, p, rx in pats[con] if (gg is None or gg == g) and not (gg is None and any(con == a and b in p for a, b in excl[g]))]
        if any(rx.search(masked) for rx in ok): continue
        c.execute("DELETE FROM entity_concepts WHERE entity=? AND concept=? AND role='does' AND method='text_pattern'", (i, con)); n += 1; C[g] += 1
c.commit(); print('does tags removed (only the granted keyword named the concept):', n, dict(C))
