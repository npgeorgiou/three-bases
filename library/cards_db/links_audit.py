"""Check 1 of START_DATABASE.md Part 3: the whole game (Kaptain, 2 Nov 2026). Is each reason's rule right?
A reason is its sentence AND the rule (network.py line, stored as link.site) that made it: one sentence can come from several
rules. For the biggest reasons that together hold 90% of the game's lines, it prints 2 lines per reason, 5 for the 20 biggest,
each from a different row shape (A's acts, B's events) and different cards, quickest to read first. Cards are shown
by their rows on one line (SYNTAX.md), the first time they appear; later "(rows above)". A line printed before or read before
(cases/links_checked.tsv) is not printed again. --record adds every printed line to cases/links_checked.tsv. The estimated
tokens of the output go to stderr.
Usage: links_audit.py <game> [--record] > a.txt"""
import collections, csv, os, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import rows as card_rows
CHECKED = os.path.join(HERE, 'cases', 'links_checked.tsv')
SHARE, TOP, N_TOP, N = 0.9, 20, 5, 2  # reasons holding 90% of lines; lines per reason: 5 for the 20 biggest, else 2


class Count:  # counts what is printed, for the token estimate
    def __init__(self, f): self.f, self.n = f, 0
    def write(self, s): self.n += len(s); return self.f.write(s)
    def flush(self): self.f.flush()


OUT = Count(sys.stdout)


def size(c):  # rows per card, to pick quick-to-read pairs
    return collections.Counter(i for (i,) in c.execute('select a.card from effect e join ability a on a.id=e.ability'))


def shapes(c):  # a card's acts and events: lines of one reason from different shapes test different parts of the rule
    act, ev = collections.defaultdict(set), collections.defaultdict(set)
    for i, a in c.execute('select a.card, e.act from effect e join ability a on a.id=e.ability'): act[i].add(a)
    for i, e in c.execute('select a.card, v.event from ability a join event v on v.id=a.event'): ev[i].add(e)
    return act, ev


def main():
    sys.stdout = OUT
    game, record = sys.argv[1], '--record' in sys.argv
    c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite')); c.execute(f"attach database '{os.path.join(HERE, 'links.sqlite')}' as L")
    nm = {i: n for i, n in c.execute('select id, name from card where game=?', (game,))}
    told = set()
    def rw(i):
        if i in told: return '(rows above)'
        told.add(i); return card_rows.compact(i)
    per = collections.defaultdict(list)
    for a, b, k, t, site in c.execute('select l.a, l.b, p.kind, p.text, l.site from L.link l join L.phrase p on p.id=l.phrase where l.game=?', (game,)):
        per[(k, t, site)].append((a, b))
    total = sum(len(v) for v in per.values())
    seen = {tuple(r[1:]) for r in csv.reader(open(CHECKED, encoding='utf-8'), delimiter='\t') if r and r[0] == game} if os.path.exists(CHECKED) else set()
    n_rows = size(c); act, ev = shapes(c); shown = []
    keep, s = [], 0
    for r, ps in sorted(per.items(), key=lambda x: -len(x[1])):
        if s >= SHARE * total: break
        keep.append((r, ps)); s += len(ps)
    print(f'=== {game}: {total} lines, {len(per)} reasons; the {len(keep)} biggest hold {100 * s / total:.0f}% of the lines')
    for rank, ((k, t, site), ps) in enumerate(keep):
        fresh = sorted((p for p in ps if (nm[p[0]], nm[p[1]]) not in seen), key=lambda p: (n_rows[p[0]] + n_rows[p[1]], nm[p[0]], nm[p[1]]))
        if not fresh: continue
        want = (N_TOP if rank < TOP else N) - sum(1 for p in ps if (nm[p[0]], nm[p[1]]) in seen)  # lines read before count
        if want <= 0: continue
        shape = lambda p: (frozenset(act[p[0]]), frozenset(ev[p[1]]))
        pick, used, got = [fresh[0]], {fresh[0][0], fresh[0][1]}, {shape(fresh[0])}
        for p in fresh[1:]:  # a new row shape and new cards first
            if len(pick) == want: break
            if shape(p) not in got and p[0] not in used and p[1] not in used: pick.append(p); used |= set(p); got.add(shape(p))
        print(f'\n## {k}: {t} ({len(ps)} lines; rule at network.py line {site})')
        for a, b in pick:
            print(f'  {nm[a]} -> {nm[b]}\n     {nm[a]}: {rw(a)}\n     {nm[b]}: {rw(b)}')
            seen.add((nm[a], nm[b])); shown.append((nm[a], nm[b]))
    print(f'about {OUT.n // 4} tokens printed', file=sys.stderr)
    if record:
        with open(CHECKED, 'a', encoding='utf-8') as f:
            for a, b in shown: f.write(f'{game}\t{a}\t{b}\n')


if __name__ == '__main__': main()
