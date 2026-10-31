"""The check of links.sqlite for one game (LINKS_PLAN.md step 3.2, Kaptain 31 Oct 2026), both card texts beside each line:
  a) the 20 cards with the most partners (a rule that fires for every card: START_DATABASE.md L1, L2)
  b) the 20 cards with the least partners, each with 15 random cards of a deck it is in: should one be linked?
  c) 5 random lines of each of the 20 most used phrases
  d) 30 random lines
  e) 20 cards with no partner, each with 15 random cards of a deck it is in: should one be linked?
  f) the special cards of every deck (champions, heroes, Generals, legends): all their lines inside the deck
Lines already in cases/links_checked.tsv are not shown again (g); --record adds every shown line to it.
Read every printed line against both texts as a player. Each wrong or missing line is fixed by its cause, for every game.
Usage: links_audit.py <game> [--record] > audit.txt"""
import collections, csv, os, random, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import deck_analysis, links, source
CHECKED = os.path.join(HERE, 'cases', 'links_checked.tsv')
SPECIAL_CAT, SPECIAL_RARITY = ('hero', 'leader'), ('legendary', 'champion', 'Champion')


def main():
    game, record = sys.argv[1], '--record' in sys.argv
    c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite')); c.execute(f"attach database '{os.path.join(HERE, 'links.sqlite')}' as L")
    lib = source.lib(); R = random.Random(game)
    nm = {i: n for i, n in c.execute('select id, name from card where game=?', (game,))}
    txt = lambda i: ' '.join(((lib.execute('select text from entities where id=?', (i,)).fetchone() or [''])[0] or '').split()) or '(no text)'
    owned = sorted(links.owned(c, game))
    rows = c.execute('select l.a, l.b, p.kind, p.text from L.link l join L.phrase p on p.id=l.phrase where l.game=?', (game,)).fetchall()
    by_pair = collections.defaultdict(list)
    for a, b, k, t in rows: by_pair[(a, b)].append((k, t))
    partners = collections.defaultdict(set)
    for a, b in by_pair: partners[a].add(b); partners[b].add(a)
    seen = {tuple(r[1:]) for r in csv.reader(open(CHECKED, encoding='utf-8'), delimiter='\t') if r and r[0] == game} if os.path.exists(CHECKED) else set()
    shown = []
    decks = [r for f in ('decks.tsv', os.path.join('cases', 'decks.tsv'))
             for r in csv.DictReader(open(os.path.join(HERE, f), encoding='utf-8'), delimiter='\t') if r['game'] == game]
    deck_ids = [(r['deck'], list(dict.fromkeys(deck_analysis.parse_deck(c, game, r['cards'])[0]))) for r in decks]

    def line(a, b, full=True):
        if (nm[a], nm[b]) in seen: return False
        for k, t in by_pair[(a, b)]:
            print(f"  {nm[a]} -> {nm[b]}: {k}: {t.replace('{A}', nm[a]).replace('{B}', nm[b])}")
        if full: print(f"     {nm[a]}: {txt(a)}\n     {nm[b]}: {txt(b)}")
        seen.add((nm[a], nm[b])); shown.append((nm[a], nm[b])); return True

    def card(i):
        print(f"{nm[i]} ({len(partners[i])} partners): {txt(i)}")

    def compare(i):  # 15 cards of a deck it is in (else of the game, that can share a deck with it)
        pool = next((ids for _, ids in deck_ids if i in ids), None)
        pool = [x for x in (pool or owned) if x != i and x not in partners[i] and deck_analysis.can_share(c, game, i, x)]
        for x in R.sample(pool, min(15, len(pool))): print(f"    ? {nm[x]}: {txt(x)}")

    print(f'=== {game}: {len(owned)} cards, {len(by_pair)} pairs, {len(rows)} rows')
    linked = sorted((i for i in owned if partners[i]), key=lambda i: (-len(partners[i]), nm[i]))
    print('-- a) most partners: is each a real reason, or one that fires for every card?')
    for i in linked[:20]:
        card(i); outs = [b for (a, b) in by_pair if a == i]; ins = [a for (a, b) in by_pair if b == i]
        for b in R.sample(outs, min(3, len(outs))): line(i, b, False)
        for a in R.sample(ins, min(3, len(ins))): line(a, i, False)
    print('-- b) least partners, with 15 cards of a deck it is in: should one be linked?')
    for i in linked[::-1][:20]:
        card(i)
        for a, b in [p for p in by_pair if i in p]: line(a, b, False)
        compare(i)
    print('-- c) 5 random lines of each of the 20 most used reasons')
    per = collections.defaultdict(list)
    for (a, b), ls in by_pair.items():
        for k, t in ls: per[(k, t)].append((a, b))
    for (k, t), ps in sorted(per.items(), key=lambda x: -len(x[1]))[:20]:
        print(f'- {k}: {t} ({len(ps)} lines)')
        for a, b in R.sample(ps, min(5, len(ps))): line(a, b)
    print('-- d) 30 random lines')
    n = 0
    for a, b in R.sample(list(by_pair), len(by_pair)):
        n += line(a, b)
        if n == 30: break
    print('-- e) cards with no partner, with 15 cards of a deck it is in: should one be linked?')
    lone = [i for i in owned if not partners[i]]
    print(f'{len(lone)} cards have no partner')
    for i in R.sample(lone, min(20, len(lone))): card(i); compare(i)
    print('-- f) special cards of each deck: all their lines inside the deck')
    for deck, ids in deck_ids:
        sp = [i for i in ids if c.execute('select 1 from card where id=? and (category in (?, ?) or rarity in (?, ?, ?))', (i,) + SPECIAL_CAT + SPECIAL_RARITY).fetchone()]
        if not sp: continue
        print(f'= {deck}')
        for i in sp:
            card(i)
            for a, b in [p for p in by_pair if i in p and (p[0] in ids and p[1] in ids)]: line(a, b)
    if record:
        with open(CHECKED, 'a', encoding='utf-8') as f:
            for a, b in shown: f.write(f'{game}\t{a}\t{b}\n')


if __name__ == '__main__': main()
