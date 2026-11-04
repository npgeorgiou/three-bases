"""Check 2 of START_DATABASE.md Part 3: every deck (Kaptain, 2 Nov 2026). For each deck of the game it prints:
  a) the deck's cards with no partner inside the deck (up to 10), each beside 10 cards of the deck: first the cards whose
     rows name the same keyword, card or type, then random deck cards. Is a line missed?
  b) the 10 cards with the fewest partners (at least one), all their lines. Is a line missed?
  c) the deck's special cards (champions, heroes, Generals, legends): one line per reason. Is something wrong or missing?
Cards are shown by their rows on one line (SYNTAX.md), the first time they appear; later "(rows above)". A line printed in an
earlier deck, or read before (cases/links_checked.tsv), is not printed again. The estimated tokens go to stderr.
Usage: deck_audit.py <game> [deck name part] > d.txt"""
import collections, csv, os, random, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import network_page, source
import rows as card_rows
from links_audit import OUT
LINE = dict(re.findall(r"(\w+):\['#\w+','([^']+)'\]", network_page.PAGE.split('const LINE=')[1].split(';')[0]))  # the page's kind names
SPECIAL_CAT, SPECIAL_RARITY = ('hero', 'leader'), ('legendary', 'champion', 'Champion')


def things(c, i):
    """The keywords, cards and types a card's rows name (to find the deck cards most likely to work with it)."""
    q = ['select keyword from card_keyword where card=?',
         'select e.keyword_ref from effect e join ability a on a.id=e.ability where a.card=? and e.keyword_ref is not null',
         'select f.ref_keyword from filter f join target t on t.id=f.target where f.ref_keyword is not null and t.id in '
         '(select on_target from effect e join ability a on a.id=e.ability where a.card=?)']
    out = {('k', x) for s in q for (x,) in c.execute(s, (i,)) if x}
    out |= {('c', x) for (x,) in c.execute('select e.card_ref from effect e join ability a on a.id=e.ability where a.card=? and e.card_ref is not null', (i,))}
    out |= {('t', x) for (x,) in c.execute('select type from card_type where card=?', (i,))}
    return out | {('c', i)}


def main():
    sys.stdout = OUT
    game, part = sys.argv[1], (sys.argv[2].lower() if len(sys.argv) > 2 else '')
    c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite')); lib = source.lib()
    rows = [r for f in ('decks.tsv', os.path.join('cases', 'decks.tsv'))
            for r in csv.DictReader(open(os.path.join(HERE, f), encoding='utf-8'), delimiter='\t')]
    rows = list({(r['game'], r['deck']): r for r in rows}.values())
    special = {i for i, cat, rar in c.execute('select id, category, rarity from card where game=?', (game,))
               if cat in SPECIAL_CAT or rar in SPECIAL_RARITY}
    told, done = set(), set()  # cards whose rows were printed; lines printed (by names)
    chk = os.path.join(HERE, 'cases', 'links_checked.tsv')
    done |= {(x[1], x[2]) for x in csv.reader(open(chk, encoding='utf-8'), delimiter='\t') if x and x[0] == game} if os.path.exists(chk) else set()
    th = {}
    for r in rows:
        if r['game'] != game or part not in r['deck'].lower(): continue
        d = network_page.deck_data(c, lib, r['game'], r['deck'], r['source'], r['cards'])
        nm = {n['id']: n['name'] for n in d['nodes']}
        R = random.Random(r['deck'])
        def rw(i):
            if nm[i] in told: return '(rows above)'
            told.add(nm[i]); return card_rows.compact(i)
        def show(l):  # a line not printed before, with both cards' rows
            key = (nm[l['from']], nm[l['to']])
            if key in done: return
            done.add(key); print(f"  {key[0]} -> {key[1]}: {LINE[l['kind']]}: {l['why']}")
            print(f"     {key[0]}: {rw(l['from'])}\n     {key[1]}: {rw(l['to'])}")
        partners = collections.defaultdict(set)
        for l in d['lines']: partners[l['from']].add(l['to']); partners[l['to']].add(l['from'])
        for i in nm:
            if i not in th: th[i] = things(c, i)
        print(f"\n=== {r['game']} / {r['deck']}: {len(nm)} cards, {len(d['lines'])} lines")
        none = sorted((i for i in nm if not partners[i]), key=lambda i: nm[i])[:10]
        print(f'-- a) {len(none)} cards with no partner in the deck, each beside 10 deck cards: is a line missed?')
        for i in none:
            print(f"{nm[i]}: {rw(i)}")
            near = [x for x in nm if x != i and th[x] & th[i]]
            rest = [x for x in R.sample(list(nm), len(nm)) if x != i and x not in near]
            for x in (near + rest)[:10]: print(f"    ? {nm[x]}: {rw(x)}")
        print('-- b) the 10 cards with the fewest partners, all their lines: is a line missed?')
        for i in sorted((i for i in nm if partners[i]), key=lambda i: (len(partners[i]), nm[i]))[:10]:
            print(f"{nm[i]} ({len(partners[i])} partners): {rw(i)}")
            for l in d['lines']:
                if i in (l['from'], l['to']): show(l)
        print('-- c) special cards, one line per reason: is something wrong or missing?')
        for i in sorted((i for i in nm if i in special), key=lambda i: nm[i]):
            print(f"{nm[i]} ({len(partners[i])} partners): {rw(i)}")
            by = {}
            for l in d['lines']:
                if i in (l['from'], l['to']): by.setdefault(('->' if l['from'] == i else '<-', l['why']), l)
            for l in by.values(): show(l)
    print(f'about {OUT.n // 4} tokens printed', file=sys.stderr)


if __name__ == '__main__': main()
