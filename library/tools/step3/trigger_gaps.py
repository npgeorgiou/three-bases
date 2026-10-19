"""Find trigger wording no trigger concept covers (asked by Kaptain, 19 Oct 2026; script only, no readers).
Collects trigger-shaped clauses from every entry's text ('when/whenever/after/each time ...', 'at the start/end of ...') up to
the first ',' ':' '.' or line break, keeps those that no pattern of a trigger concept (concept_tree_v3 facet 'trigger')
matches, and prints the most frequent groups (first four words, numbers as N) with counts per game and two example entries.
Usage: trigger_gaps.py [db] [top]"""
import collections, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, TOOLS)
import patterns3 as P
from concept_tree import TREE
DB = sys.argv[1] if len(sys.argv) > 1 else P.DB; TOP = int(sys.argv[2]) if len(sys.argv) > 2 else 40
c = sqlite3.connect(DB)
trig = {k for k, d in TREE.items() if d.get('facet') == 'trigger'}
pats = [re.compile(p, re.I) for k, p in c.execute('SELECT concept, pattern FROM concept_patterns') if k in trig]
CL = re.compile(r"(?:^|[\n.;:]\s*|,\s*)((?:whenever|when|after|each time|every time|at the (?:start|end|beginning) of)\b[^,:.\n]{2,60})", re.I)
grp = collections.defaultdict(lambda: [collections.Counter(), []])
for i, g, n, t in c.execute('SELECT id, game, name, text FROM entities WHERE text IS NOT NULL'):
    low = P.norm_text(g, n, t)
    for m in CL.finditer(low):
        cl = m.group(1).strip()
        if any(p.search(cl) for p in pats): continue
        key = ' '.join(re.sub(r'\d+', 'N', cl).split()[:4])
        grp[key][0][g] += 1
        if len(grp[key][1]) < 2: grp[key][1].append(f'{n}: {cl}')
for key, (cnt, ex) in sorted(grp.items(), key=lambda x: -sum(x[1][0].values()))[:TOP]:
    print(f'{sum(cnt.values()):5}  {key:35}  {", ".join(f"{g} {v}" for g, v in cnt.most_common(4))}  | {" / ".join(ex)[:150]}')
