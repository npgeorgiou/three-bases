"""LINKS_PLAN.md step 3.1 and 3.3: links.sqlite against the decks, and the zero checks.
1. For every deck of decks.tsv and cases/decks.tsv: the table's lines between the deck's cards against network() on the deck
   (pairs and reasons, not weights). Expected: a card the deck only makes gets no "draws it from the deck" in the deck; Into
   the Breach "carries" lines are not stored. Every other difference is printed, grouped by reason.
2. Zero checks: lines between two cards that cannot share a deck; lines with an end that is not a card a player owns.
Usage: links_check.py [game ...]"""
import collections, csv, os, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import deck_analysis, links, network


def main():
    c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite')); c.execute(f"attach database '{os.path.join(HERE, 'links.sqlite')}' as L")
    games = sys.argv[1:] or [g for (g,) in c.execute('select distinct game from L.link order by game')]
    decks = [r for f in ('decks.tsv', os.path.join('cases', 'decks.tsv'))
             for r in csv.DictReader(open(os.path.join(HERE, f), encoding='utf-8'), delimiter='\t')]
    decks = list({(r['game'], r['deck']): r for r in decks}.values())
    for game in games:
        owned = {i for (i,) in c.execute(links.OWNED, (game,))}
        nm = {i: n for i, n in c.execute('select id, name from card where game=?', (game,))}
        table = collections.defaultdict(set)
        for a, b, k, t in c.execute('select l.a, l.b, p.kind, p.text from L.link l join L.phrase p on p.id=l.phrase where l.game=?', (game,)):
            table[(a, b)].add((k, t))
        only_table, only_deck = collections.Counter(), collections.Counter(); ex = {}
        for r in decks:
            if r['game'] != game: continue
            ids = list(dict.fromkeys(deck_analysis.parse_deck(c, game, r['cards'])[0])); D = set(ids)
            nodes, lines = network.network(c, game, ids)
            deck = collections.defaultdict(set)
            for (a, b), ls in lines.items():
                if a not in owned or b not in owned or a == b or not deck_analysis.can_share(c, game, a, b): continue
                kind, w, why = ls[0]
                for k, part in links.reasons(kind, why):
                    if k not in links.NO_STORE: deck[(a, b)].add((k, links.as_phrase(part, nm[a], nm[b])))
            for p in {p for p in table if p[0] in D and p[1] in D} | set(deck):
                for x in table[p] - deck[p]:
                    if nodes.get(p[1]) and x[1] == 'draws it from the deck': continue  # (a) made in the deck
                    only_table[x] += 1; ex.setdefault(('table',) + x, (r['deck'], nm[p[0]], nm[p[1]]))
                for x in deck[p] - table[p]:
                    only_deck[x] += 1; ex.setdefault(('deck',) + x, (r['deck'], nm[p[0]], nm[p[1]]))
        print(f'=== {game}: {sum(only_table.values())} reasons only in the table, {sum(only_deck.values())} only in the decks')
        for side, cnt in (('table', only_table), ('deck', only_deck)):
            for x, n in cnt.most_common(25): print(f'  only in {side} {n}x  {x[0]}: {x[1]}   e.g. {ex[(side,) + x]}')
        bad_share = [(a, b) for (a, b) in table if not deck_analysis.can_share(c, game, a, b)]
        bad_end = [(a, b) for (a, b) in table if a not in owned or b not in owned]
        print(f'  zero checks: {len(bad_share)} lines between cards that cannot share a deck, {len(bad_end)} with an end no player owns')


if __name__ == '__main__': main()
