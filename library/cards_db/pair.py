"""pair.py <game> "A" "B" ["A2" "B2" ...]: the line network.py draws for just those two cards, with the network.py line (site) of each
reason; about 12 s per call, many pairs per call. Use it to see why one line exists (LINKS_PLAN.md "How lines are made"); never rebuild for that."""
import sys, os
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D); os.chdir(D)
import sqlite3, network, rows
c = rows.c
game = sys.argv[1]; args = sys.argv[2:]


def ids(n):
    r = [x[0] for x in c.execute("select id from card where game=? and name=? and is_keyword=0", (game, n))]
    if not r: r = [x[0] for x in c.execute("select id from card where game=? and name like ? and is_keyword=0", (game, n + '%'))]
    return r


for i in range(0, len(args), 2):
    A, B = args[i], args[i + 1]
    for a in ids(A):
        for b in ids(B):
            network.SITE.clear()
            _, ls = network.network(c, game, [a, b])
            out = ls.get((a, b), [])
            print(f'{A} ({a}) -> {B} ({b}):', '; '.join(y for _, _, y in out) or 'NONE')
            for k, v in network.SITE.items():
                if k[0] == a and k[1] == b: print('   site', sorted(v), k[2][:110])
