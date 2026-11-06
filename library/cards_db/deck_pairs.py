"""Deck pairs of library/games/<game>.md ("## Deck pairs", block ```pairs) -> `line` rows of cases/network.tsv.

Usage: python3 deck_pairs.py <game>
Each pair `deck | A | B | the guide's words` becomes one row (expect line). Both cards must be in that deck of decks.tsv;
a pair already in network.tsv (same game, deck, from, to) is skipped. Safe to run twice.
"""
import csv, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
GAMES = os.path.join(HERE, '..', 'games')
NET = os.path.join(HERE, 'cases', 'network.tsv')


def pairs(game):
    text = open(os.path.join(GAMES, game + '.md'), encoding='utf-8').read()
    m = re.search(r'## Deck pairs.*?```pairs\n(.*?)```', text, re.S)
    if not m:
        sys.exit(f'no "## Deck pairs" block in games/{game}.md')
    return [[p.strip() for p in l.split('|')] for l in m.group(1).splitlines() if l.strip()]


def main(game):
    decks = {}
    with open(os.path.join(HERE, 'decks.tsv'), encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            if r['game'] == game:
                decks[r['deck']] = (r['source'].split()[0], [c.strip() for c in r['cards'].split(',')])
    with open(NET, encoding='utf-8') as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    have = {(r['game'], r['deck'], r['from'], r['to']) for r in rows}
    nxt = max(int(r['id'][1:]) for r in rows if re.fullmatch(r'n\d+', r['id'])) + 1
    new, bad = [], []
    for p in pairs(game):
        if len(p) != 4:
            bad.append(' | '.join(p) + ': not 4 parts'); continue
        deck, a, b, words = p
        if deck not in decks:
            bad.append(f'{deck}: no such deck'); continue
        url, cards = decks[deck]
        miss = [x for x in (a, b) if x not in cards]
        if miss:
            bad.append(f'{deck}: {", ".join(miss)} not in the deck'); continue
        if (game, deck, a, b) in have:
            continue
        new.append([f'n{nxt}', game, deck, a, b, 'line', '', f'guide {url} (games/{game}.md Deck pairs): {words}'])
        have.add((game, deck, a, b)); nxt += 1
    if bad:
        sys.exit('not written:\n' + '\n'.join(bad))
    with open(NET, 'a', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerows(new)
    print(f'{len(new)} rows added to cases/network.tsv', file=sys.stderr)


if __name__ == '__main__':
    main(sys.argv[1])
