"""Check 1 of LINKS_PLAN.md step 3: the whole game (Kaptain, 2 Nov 2026). It prints, in this order:
  a) the top 10 reasons for links: are we linking too much for generic reasons?
  b) the 2% cards with the most partners, all their lines (by reason, with the partners): linking too much for generic reasons?
  c) the 2% cards with the fewest partners (at least one), all their lines: is a line missed?
  d) 2% of the cards with no partner, their texts: is a line missed?
  e) the same cards, beside 50 random cards of their faction: is a line missed?
  f) 50 random lines: is something wrong or missing?
  g) 50 random lines of each of the 20 most used reasons: is something wrong or missing?
  h) the special cards of every deck (champions, heroes, Generals, legends), all their lines: is something wrong or missing?
  i) a line printed in an earlier part, or read before (cases/links_checked.tsv), is not printed again.
Token limit (Kaptain, 2 Nov 2026): no list holds more than 100 cards. Where more are due, a share is taken from each reason
(or faction), so every reason stays seen: the cards a part starts from are at most 100, and the partners or compared cards
beside them are at most 100. The estimated tokens of the output are printed to stderr.
A card's rows (one line, SYNTAX.md) are printed the first time the card appears, later "(text above)". --record adds every printed line to
cases/links_checked.tsv. Read every printed line against both texts as a player.
Usage: links_audit.py <game> [--record] > a.txt"""
import collections, csv, os, random, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import deck_analysis, links, source
import rows as card_rows
CHECKED = os.path.join(HERE, 'cases', 'links_checked.tsv')
SPECIAL_CAT, SPECIAL_RARITY = ('hero', 'leader'), ('legendary', 'champion', 'Champion')
CAP = 100  # most cards in any list (Kaptain, 2 Nov 2026)


def spread(items, key, n=CAP):
    """At most n items, an equal share from each group of key (round robin), in the given order inside a group."""
    g = collections.defaultdict(list)
    for x in items: g[key(x)].append(x)
    out, qs = [], [list(v) for _, v in sorted(g.items(), key=lambda kv: str(kv[0]))]
    while len(out) < n and any(qs):
        for q in qs:
            if q and len(out) < n: out.append(q.pop(0))
    return out


class Count:  # counts what is printed, for the token estimate
    def __init__(self, f): self.f, self.n = f, 0
    def write(self, s): self.n += len(s); return self.f.write(s)
    def flush(self): self.f.flush()


OUT = Count(sys.stdout)


def main():
    sys.stdout = OUT
    game, record = sys.argv[1], '--record' in sys.argv
    c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite')); c.execute(f"attach database '{os.path.join(HERE, 'links.sqlite')}' as L")
    lib = source.lib(); R = random.Random(game)
    nm = {i: n for i, n in c.execute('select id, name from card where game=?', (game,))}
    region = {i: [x for x in (r or '').split(',') if x] for i, r in c.execute('select id, regions from card where game=?', (game,))}
    full_txt = card_rows.compact  # the card's rows (SYNTAX.md); readers judge lines by them
    told = set()
    def txt(i):  # the text once; after that the name says it
        if i in told: return '(text above)'
        told.add(i); return full_txt(i)
    owned = sorted(links.owned(c, game))
    rows = c.execute('select l.a, l.b, p.kind, p.text from L.link l join L.phrase p on p.id=l.phrase where l.game=?', (game,)).fetchall()
    by_pair = collections.defaultdict(list)
    for a, b, k, t in rows: by_pair[(a, b)].append((k, t))
    partners = collections.defaultdict(set)
    for a, b in by_pair: partners[a].add(b); partners[b].add(a)
    per = collections.defaultdict(list)
    for (a, b), ls in by_pair.items():
        for k, t in ls: per[(k, t)].append((a, b))
    top = sorted(per.items(), key=lambda x: -len(x[1]))
    seen = {tuple(r[1:]) for r in csv.reader(open(CHECKED, encoding='utf-8'), delimiter='\t') if r and r[0] == game} if os.path.exists(CHECKED) else set()
    shown = []
    decks = [r for f in ('decks.tsv', os.path.join('cases', 'decks.tsv'))
             for r in csv.DictReader(open(os.path.join(HERE, f), encoding='utf-8'), delimiter='\t') if r['game'] == game]
    deck_ids = [list(dict.fromkeys(deck_analysis.parse_deck(c, game, r['cards'])[0])) for r in decks]
    say = lambda t, a, b: t.replace('{A}', nm[a]).replace('{B}', nm[b])

    def line(a, b):  # one line with both texts, if not printed before
        if (nm[a], nm[b]) in seen: return False
        for k, t in by_pair[(a, b)]: print(f"  {nm[a]} -> {nm[b]}: {k}: {say(t, a, b)}")
        print(f"     {nm[a]}: {txt(a)}\n     {nm[b]}: {txt(b)}")
        seen.add((nm[a], nm[b])); shown.append((nm[a], nm[b])); return True

    def card(i):
        print(f"{nm[i]} ({len(partners[i])} partners): {txt(i)}")

    def groups(i):  # every line of the card not printed before, one row per direction and reason, with at most 100 partners
        g = collections.defaultdict(list)
        for o in partners[i]:
            for a, b in ((i, o), (o, i)):
                if (a, b) in by_pair and (nm[a], nm[b]) not in seen:
                    for k, t in by_pair[(a, b)]: g[('->' if a == i else '<-', k, t)].append(o)
        pick = set(spread([(r, o) for r, os_ in g.items() for o in R.sample(os_, len(os_))], lambda x: x[0]))
        for (d, k, t), os_ in sorted(g.items(), key=lambda x: (-len(x[1]), x[0])):
            show = sorted((o for o in os_ if ((d, k, t), o) in pick), key=lambda o: nm[o])
            names = ', '.join(nm[o] for o in show) + (f' and {len(os_) - len(show)} more' if len(os_) > len(show) else '')
            print(f"  {d} {k}: {t.replace('{A}', 'A').replace('{B}', 'B')} ({len(os_)}): {names}")
            for o in show:
                p_ = (nm[i], nm[o]) if d == '->' else (nm[o], nm[i])
                if p_ not in seen: seen.add(p_); shown.append(p_)

    def own_lines(i):  # the card's lines not printed before, one by one with the partner's text; at most 100 partners
        main = lambda o: (by_pair.get((i, o)) or by_pair.get((o, i)))[0]
        for o in sorted(spread(R.sample(sorted(partners[i]), len(partners[i])), main), key=lambda o: nm[o]):
            for a, b in ((i, o), (o, i)):
                if (a, b) in by_pair and (nm[a], nm[b]) not in seen:
                    for k, t in by_pair[(a, b)]: print(f"  {nm[a]} -> {nm[b]}: {k}: {say(t, a, b)}")
                    print(f"     {nm[o]}: {txt(o)}")
                    seen.add((nm[a], nm[b])); shown.append((nm[a], nm[b]))

    n2 = max(1, round(len(owned) * 0.02))
    print(f'=== {game}: {len(owned)} cards, {len(by_pair)} pairs, {len(rows)} rows; 2% = {n2} cards')
    print('-- a) the top 10 reasons for links: are we linking too much for generic reasons?')
    for (k, t), ps in top[:10]:
        print(f"- {k}: {t} ({len(ps)} lines, {100 * len(ps) / len(rows):.1f}%; from {len({a for a, _ in ps})} cards to {len({b for _, b in ps})} cards)")
    linked = sorted((i for i in owned if partners[i]), key=lambda i: (-len(partners[i]), nm[i]))
    def main_reason(i):  # the reason most of the card's lines give: the share key for start cards
        n = collections.Counter(r for o in partners[i] for p in ((i, o), (o, i)) for r in by_pair.get(p, []))
        return n.most_common(1)[0][0] if n else ''
    print(f'-- b) the {n2} cards with the most partners, all their lines: linking too much for generic reasons?')
    for i in spread(linked[:n2], main_reason): card(i); groups(i)
    print(f'-- c) the {n2} cards with the fewest partners (at least one), all their lines: is a line missed?')
    for i in spread(sorted(linked, key=lambda i: (len(partners[i]), nm[i]))[:n2], main_reason): card(i); own_lines(i)
    lone = [i for i in owned if not partners[i]]
    pick = sorted(spread(R.sample(lone, min(n2, len(lone))), lambda i: (region[i] or [''])[0]), key=lambda i: nm[i])
    print(f'-- d) {len(pick)} of the {len(lone)} cards with no partner: is a line missed?')
    for i in pick: card(i)
    print('-- e) the same cards, beside 50 random cards of their faction (at most 100 in all, a share per faction): is a line missed?')
    by_fac = collections.defaultdict(list)
    for i in pick: by_fac[(region[i] or [''])[0]].append(i)
    pools = {fac: R.sample(p, min(50, len(p))) for fac, ids in by_fac.items()
             for p in [[x for x in owned if x not in ids and (fac in region[x] if fac else not region[x])]]}
    keep = set(spread([(f, x) for f, xs in pools.items() for x in xs], lambda y: y[0]))
    for fac, ids in sorted(by_fac.items()):
        print(f"= {fac or '(no faction)'}: {', '.join(nm[i] for i in ids)}")
        for x in pools[fac]:
            if (fac, x) in keep: print(f"    ? {nm[x]}: {txt(x)}")
    print('-- f) 50 random lines: is something wrong or missing?')
    n = 0
    for a, b in R.sample(list(by_pair), len(by_pair)):
        n += line(a, b)
        if n == 50: break
    print('-- g) random lines of each of the 20 most used reasons (50 each, at most 100 in all, a share per reason): is something wrong or missing?')
    fresh = {(k, t): [p for p in R.sample(ps, len(ps)) if (nm[p[0]], nm[p[1]]) not in seen][:50] for (k, t), ps in top[:20]}
    keep = set(spread([(r, p) for r, ps in fresh.items() for p in ps], lambda y: y[0]))
    for (k, t), ps in top[:20]:
        print(f'- {k}: {t} ({len(ps)} lines)')
        for p in fresh[(k, t)]:
            if ((k, t), p) in keep: line(*p)
    print('-- h) the special cards of every deck, all their lines: is something wrong or missing?')
    sp = sorted({i for ids in deck_ids for i in ids if c.execute(
        'select 1 from card where id=? and (category in (?, ?) or rarity in (?, ?, ?))', (i,) + SPECIAL_CAT + SPECIAL_RARITY).fetchone()},
        key=lambda i: nm[i])
    for i in sorted(spread(R.sample(sp, len(sp)), lambda i: (region[i] or [''])[0]), key=lambda i: nm[i]): card(i); groups(i)
    print(f'about {OUT.n // 4} tokens printed', file=sys.stderr)
    if record:
        with open(CHECKED, 'a', encoding='utf-8') as f:
            for a, b in shown: f.write(f'{game}\t{a}\t{b}\n')


if __name__ == '__main__': main()
