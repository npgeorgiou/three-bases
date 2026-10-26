"""Step 4: texts that differ only in the card's name, in numbers or in reminder text share one reading.
groups(db) -> {entity id: id of the first entity with the same game, category and normalised text}.
Run alone it prints, per game, entries, distinct texts and their size in tokens (about 4 characters per token, reminder text left out).
Usage: repeats.py <db>"""
import collections, os, sqlite3, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import norm


def groups(c):
    first, out = {}, {}
    for i, g, cat, name, text in c.execute("SELECT id, game, category, name, text FROM entities "
                                           "WHERE category NOT IN ('keyword','tribe') AND text IS NOT NULL AND text != '' ORDER BY id"):
        k = (g, cat, norm(g, name, text))
        out[i] = first.setdefault(k, i)
    return out


if __name__ == '__main__':
    c = sqlite3.connect(sys.argv[1])
    gr = groups(c)
    size = {i: len(norm(g, n, t)) for i, g, n, t in c.execute("SELECT id, game, name, text FROM entities")}
    game = dict(c.execute("SELECT id, game FROM entities"))
    n, d, tok = collections.Counter(), collections.Counter(), collections.Counter()
    for i, f in gr.items():
        n[game[i]] += 1
        if i == f: d[game[i]] += 1; tok[game[i]] += size[i] / 4
    for g, _ in n.most_common():
        print(f'{g:18} {n[g]:6} {d[g]:6} {tok[g]:9.0f}')
    print(f"{'all':18} {sum(n.values()):6} {sum(d.values()):6} {sum(tok.values()):9.0f}")
