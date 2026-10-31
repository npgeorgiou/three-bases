"""The self-check every worker runs after building or changing a game's networks (Kaptain, 30 Oct 2026; PROCESS "Audit every
deck yourself"). For each deck of the game it prints:
  1. the 3 most linked cards, each with every line in or out and the other card's text
  2. the 3 least linked cards (none counts), the same, plus 10 other cards of the deck picked at random, with their texts:
     should one of them be linked with one of the 3 least linked cards?
  3. 10 other lines picked at random (fixed per deck, so a rerun shows the same ones), not in 1 or 2, with both texts
A card's text is printed the first time the card appears in the output, later "(text above)"; a line already printed for
another deck is not printed again (the same two cards give the same line in every deck).
Read every printed line against both texts as a player. Each wrong or missing line is fixed by its cause, for every game.
Usage: deck_audit.py <game> [deck name part] > audit.txt"""
import csv, os, random, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import network_page, source
LINE = dict(re.findall(r"(\w+):\['#\w+','([^']+)'\]", network_page.PAGE.split('const LINE=')[1].split(';')[0]))  # the page's kind names


def main():
    game, part = sys.argv[1], (sys.argv[2].lower() if len(sys.argv) > 2 else '')
    c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite')); lib = source.lib()
    rows = [r for f in ('decks.tsv', os.path.join('cases', 'decks.tsv'))
            for r in csv.DictReader(open(os.path.join(HERE, f), encoding='utf-8'), delimiter='\t')]
    rows = list({(r['game'], r['deck']): r for r in rows}.values())
    told, done = set(), set()  # cards whose text was printed; lines printed (by names)
    chk = os.path.join(HERE, 'cases', 'links_checked.tsv')  # lines read in links_audit (--record): not printed again
    checked = {(x[1], x[2]) for x in csv.reader(open(chk, encoding='utf-8'), delimiter='\t') if x and x[0] == game} if os.path.exists(chk) else set()
    for r in rows:
        if r['game'] != game or part not in r['deck'].lower(): continue
        d = network_page.deck_data(c, lib, r['game'], r['deck'], r['source'], r['cards'])
        nm = {n['id']: n['name'] for n in d['nodes']}; tx0 = {n['id']: n['text'] for n in d['nodes']}
        class Once(dict):  # the text once, then "(text above)"
            def __missing__(self, i):
                if nm[i] in told: return '(text above)'
                told.add(nm[i]); return tx0[i]
        tx = Once()
        say = lambda l: f"  {nm[l['from']]} -> {nm[l['to']]}: {LINE[l['kind']]}: {l['why']}"
        deg = {i: sum(1 for l in d['lines'] if i in (l['from'], l['to'])) for i in nm}
        order = sorted(nm, key=lambda i: (-deg[i], nm[i]))
        top, low = order[:3], sorted(nm, key=lambda i: (deg[i], nm[i]))[:3]
        print(f"=== {r['game']} / {r['deck']}: {len(nm)} cards, {len(d['lines'])} lines")
        seen = set()
        for title, group in (('most linked', top), ('least linked', low)):
            print(f'-- {title}')
            for i in group:
                print(f"{nm[i]} ({deg[i]} lines): {tx[i]}")
                made = [l['to'] for l in d['lines'] if l['from'] == i and 'puts it into play' in l['why'] and l['to'] != i]
                for o in dict.fromkeys(made):  # what it makes acts through it (Zed's Living Shadow is the Ephemeral ally)
                    print(f"    makes {nm[o]}: {tx[o]}")
                for l in d['lines']:
                    if i in (l['from'], l['to']):
                        o = l['to'] if l['from'] == i else l['from']; seen.add(id(l)); key = (nm[l['from']], nm[l['to']], l['why'])
                        if key not in done and key[:2] not in checked: done.add(key); print(say(l) + f"   [{nm[o]}: {tx[o]}]")
            if title == 'least linked':  # cards that might have been linked with them
                others = [i for i in nm if i not in top and i not in low]
                print('-- 10 random other cards: should one be linked with a least linked card?')
                for i in random.Random(r['deck'] + ' cards').sample(others, min(10, len(others))):
                    print(f"  {nm[i]} ({deg[i]} lines): {tx[i]}")
        rest = [l for l in d['lines'] if id(l) not in seen and (nm[l['from']], nm[l['to']], l['why']) not in done
                and (nm[l['from']], nm[l['to']]) not in checked]
        print('-- 10 random other lines')
        for l in random.Random(r['deck']).sample(rest, min(10, len(rest))):
            done.add((nm[l['from']], nm[l['to']], l['why'])); print(say(l)); print(f"     {nm[l['from']]}: {tx[l['from']]}\n     {nm[l['to']]}: {tx[l['to']]}")


if __name__ == '__main__': main()
