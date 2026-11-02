"""Check 2 of LINKS_PLAN.md step 3: every deck (Kaptain, 2 Nov 2026). For each deck of the game it prints, in this order:
  a) the top 5 reasons for links: are we linking too much for generic reasons?
  b) the 10 cards with the most partners, all their lines: linking too much for generic reasons?
  c) the 10 cards with the fewest partners (at least one), all their lines: is a line missed?
  d) the (up to) 10 cards with no partner at all: is a line missed?
  e) the same cards, beside 10 random cards of the deck: is a line missed?
  f) 10 random lines: is something wrong or missing?
  g) 5 random lines of each of the 5 most used reasons: is something wrong or missing?
  h) the deck's special cards (champions, heroes, Generals, legends), all their lines: is something wrong or missing?
  i) a line printed before (in an earlier part or deck, or read before: cases/links_checked.tsv) is not printed again.
A card's text is printed the first time the card appears, later "(text above)". Read every printed line against both texts.
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
        def show(l, texts=True):  # a line not printed before, with the texts
            key = (nm[l['from']], nm[l['to']])
            if key in done: return False
            done.add(key); print(f"  {key[0]} -> {key[1]}: {LINE[l['kind']]}: {l['why']}")
            if texts: print(f"     {key[0]}: {tx(l['from'])}\n     {key[1]}: {tx(l['to'])}")
            return True
        partners = collections.defaultdict(set)
        for l in d['lines']: partners[l['from']].add(l['to']); partners[l['to']].add(l['from'])
        def card_lines(i):
            print(f"{nm[i]} ({len(partners[i])} partners): {tx(i)}")
            for l in d['lines']:
                if i in (l['from'], l['to']): show(l)
        by = collections.defaultdict(list)
        for l in d['lines']: by[l['why']].append(l)
        top = sorted(by.items(), key=lambda x: -len(x[1]))
        print(f"=== {r['game']} / {r['deck']}: {len(nm)} cards, {len(d['lines'])} lines")
        print('-- a) the top 5 reasons for links: are we linking too much for generic reasons?')
        for why, ls in top[:5]: print(f"- {why} ({len(ls)} lines)")
        linked = [i for i in nm if partners[i]]
        print('-- b) the 10 cards with the most partners, all their lines: linking too much for generic reasons?')
        for i in sorted(linked, key=lambda i: (-len(partners[i]), nm[i]))[:10]: card_lines(i)
        print('-- c) the 10 cards with the fewest partners (at least one), all their lines: is a line missed?')
        for i in sorted(linked, key=lambda i: (len(partners[i]), nm[i]))[:10]: card_lines(i)
        none = sorted((i for i in nm if not partners[i]), key=lambda i: nm[i])[:10]
        print(f'-- d) {len(none)} cards with no partner at all: is a line missed?')
        for i in none: print(f"{nm[i]}: {tx(i)}")
        print('-- e) the same cards, beside 10 random cards of the deck: is a line missed?')
        if none:
            others = [i for i in nm if i not in none]
            for i in R.sample(others, min(10, len(others))): print(f"    ? {nm[i]}: {tx(i)}")
        print('-- f) 10 random lines: is something wrong or missing?')
        n = 0
        for l in R.sample(d['lines'], len(d['lines'])):
            n += show(l)
            if n == 10: break
        print('-- g) 5 random lines of each of the 5 most used reasons: is something wrong or missing?')
        for why, ls in top[:5]:
            print(f'- {why}')
            n = 0
            for l in R.sample(ls, len(ls)):
                n += show(l)
                if n == 5: break
        print('-- h) special cards, all their lines: is something wrong or missing?')
        for i in sorted((i for i in nm if i in special), key=lambda i: nm[i]): card_lines(i)


if __name__ == '__main__': main()
