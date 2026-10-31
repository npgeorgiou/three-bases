"""The deck check (LINKS_PLAN.md step 3, check 2; Kaptain 31 Oct 2026). For each deck of the game it prints:
  a) the 10 cards with the most lines, every line in or out (many lines usually means a rule that fires for every card: L1, L2)
  b) the 10 cards with the fewest lines (at least one), every line, beside 10 random cards of the deck: is a line missed?
  c) 5 random lines of each of the deck's 10 most used reasons
  d) 10 random lines
  e) up to 10 cards with no line, beside 10 random cards of the deck: is a line missed?
  f) the deck's special cards (champions, heroes, Generals, legends): every line
A line printed once (in any deck, or read before: cases/links_checked.tsv) is not printed again. A card's text is printed the
first time the card appears, later "(text above)". Read every printed line against both texts as a player.
Usage: deck_audit.py <game> [deck name part] > d.txt"""
import collections, csv, os, random, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import network_page, source
LINE = dict(re.findall(r"(\w+):\['#\w+','([^']+)'\]", network_page.PAGE.split('const LINE=')[1].split(';')[0]))  # the page's kind names
SPECIAL_CAT, SPECIAL_RARITY = ('hero', 'leader'), ('legendary', 'champion', 'Champion')


def main():
    game, part = sys.argv[1], (sys.argv[2].lower() if len(sys.argv) > 2 else '')
    c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite')); lib = source.lib()
    rows = [r for f in ('decks.tsv', os.path.join('cases', 'decks.tsv'))
            for r in csv.DictReader(open(os.path.join(HERE, f), encoding='utf-8'), delimiter='\t')]
    rows = list({(r['game'], r['deck']): r for r in rows}.values())
    special = {i for i, cat, rar in c.execute('select id, category, rarity from card where game=?', (game,))
               if cat in SPECIAL_CAT or rar in SPECIAL_RARITY}
    told, done = set(), set()  # cards whose text was printed; lines printed (by names)
    chk = os.path.join(HERE, 'cases', 'links_checked.tsv')
    done |= {(x[1], x[2]) for x in csv.reader(open(chk, encoding='utf-8'), delimiter='\t') if x and x[0] == game} if os.path.exists(chk) else set()
    for r in rows:
        if r['game'] != game or part not in r['deck'].lower(): continue
        d = network_page.deck_data(c, lib, r['game'], r['deck'], r['source'], r['cards'])
        nm = {n['id']: n['name'] for n in d['nodes']}; tx0 = {n['id']: n['text'] for n in d['nodes']}
        R = random.Random(r['deck'])
        def tx(i):
            if nm[i] in told: return '(text above)'
            told.add(nm[i]); return tx0[i]
        def show(l, texts=True):  # a line not printed before, with both texts
            key = (nm[l['from']], nm[l['to']])
            if key in done: return
            done.add(key); print(f"  {key[0]} -> {key[1]}: {LINE[l['kind']]}: {l['why']}")
            if texts: print(f"     {key[0]}: {tx(l['from'])}\n     {key[1]}: {tx(l['to'])}")
        def card_lines(i):
            print(f"{nm[i]} ({deg[i]} lines): {tx(i)}")
            for l in d['lines']:
                if i in (l['from'], l['to']): show(l)
        def beside(group):
            others = [i for i in nm if i not in group]
            for i in R.sample(others, min(10, len(others))): print(f"    ? {nm[i]}: {tx(i)}")
        deg = {i: sum(1 for l in d['lines'] if i in (l['from'], l['to'])) for i in nm}
        print(f"=== {r['game']} / {r['deck']}: {len(nm)} cards, {len(d['lines'])} lines")
        print('-- a) the 10 cards with the most lines')
        for i in sorted(nm, key=lambda i: (-deg[i], nm[i]))[:10]: card_lines(i)
        print('-- b) the 10 cards with the fewest lines, beside 10 random cards of the deck: is a line missed?')
        low = sorted((i for i in nm if deg[i]), key=lambda i: (deg[i], nm[i]))[:10]
        for i in low: card_lines(i)
        beside(low)
        print("-- c) 5 random lines of each of the deck's 10 most used reasons")
        by = collections.defaultdict(list)
        for l in d['lines']: by[l['why']].append(l)
        for why, ls in sorted(by.items(), key=lambda x: -len(x[1]))[:10]:
            for l in R.sample(ls, min(5, len(ls))): show(l)
        print('-- d) 10 random lines')
        for l in R.sample(d['lines'], min(10, len(d['lines']))): show(l)
        none = sorted(i for i in nm if not deg[i])[:10]
        print(f'-- e) {len(none)} cards with no line, beside 10 random cards of the deck: is a line missed?')
        for i in none: print(f"{nm[i]}: {tx(i)}")
        if none: beside(none)
        print('-- f) special cards: every line')
        for i in sorted(i for i in nm if i in special): card_lines(i)


if __name__ == '__main__': main()
