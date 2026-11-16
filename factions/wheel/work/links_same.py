"""links_same.py <before.sqlite> <after.sqlite>: two links.sqlite files hold the same rows (game, a, b, kind, phrase, weight), and the same sites up to a renumbering"""
import sqlite3, sys, collections
def rows(f):
    return sorted(sqlite3.connect(f).execute('select l.game, l.a, l.b, p.kind, p.text, round(l.weight, 9), l.site from link l join phrase p on p.id=l.phrase'))
b, a = rows(sys.argv[1]), rows(sys.argv[2])
same = collections.Counter(x[:6] for x in b) == collections.Counter(x[:6] for x in a)
m = collections.defaultdict(set)
if same:
    for x, y in zip(b, a): m[x[6]].add(y[6])
print('rows', len(b), len(a), 'same rows:', same, 'sites renumbered one to one:', same and all(len(v) == 1 for v in m.values()) and len({min(v) for v in m.values()}) == len(m))
L = sqlite3.connect(sys.argv[2])
print('links with no source: A', L.execute('select count(*) from link where a_ab is null').fetchone()[0], 'B', L.execute('select count(*) from link where b_ab is null').fetchone()[0])
