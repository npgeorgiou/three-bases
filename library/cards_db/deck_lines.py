"""Every deck's network as terse text, the same text the page copies on a right click (network_page.py): for each deck, each
card with its tags and text, then its lines "A -> B: <line kind as the page names it>: <why>". Read decks like a player from
this, not from ad hoc exports. Usage: deck_lines.py <game|all> [deck name part] > out.txt"""
import csv, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import network_page, source
LINE = dict(re.findall(r"(\w+):\['#\w+','([^']+)'\]", network_page.PAGE.split('const LINE=')[1].split(';')[0]))


def main():
    game, part = sys.argv[1], (sys.argv[2].lower() if len(sys.argv) > 2 else '')
    c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite')); lib = source.lib()
    rows = [r for f in ('decks.tsv', os.path.join('cases', 'decks.tsv'))
            for r in csv.DictReader(open(os.path.join(HERE, f), encoding='utf-8'), delimiter='\t')]
    rows = list({(r['game'], r['deck']): r for r in rows}.values())
    for r in rows:
        if game not in ('all', r['game']) or part not in r['deck'].lower(): continue
        d = network_page.deck_data(c, lib, r['game'], r['deck'], r['source'], r['cards'])
        nm = {n['id']: n['name'] for n in d['nodes']}
        print(f"=== {r['game']} / {r['deck']}")
        for n in d['nodes']:
            tag = ', '.join([n['cat']] + n['types'] + n['keywords'])
            print(f"{n['name']}{' (made)' if n['made'] else ''} [{tag}]: {n['text']}")
            for l in d['lines']:
                if l['from'] == n['id']: print(f"  {nm[l['from']]} -> {nm[l['to']]}: {LINE[l['kind']]}: {l['why']}")


main()
