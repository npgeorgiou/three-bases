"""Runs the case tests against cards.sqlite and writes REPORT.md. A case passes when the query finds at least 95% of the
expected cards (mechanics) or the connection exists (combos) or the region shows its mechanic (regions).
  mechanics.tsv  expected cards come from the card texts themselves (text:<regex> on the text without its Keywords field,
                 or kw:<Keyword> in the Keywords field): the query on the records must find them.
  combos.tsv     real combos: the enabler's results must set off the payoff (connections.py).
  regions.tsv    region identity: the query must find at least n cards of that region.
  decks.tsv      decks from players' guides: the deck explanation (ask.py <game> analyze) must contain each 'must' phrase.
  network.tsv    deck networks (network.py) of decks from the web (../decks.tsv, decks.tsv): a line between two cards must be
                 there, or must not (with why_not: no line for that reason); Kaptain's check of the networks.
Usage: run.py <game> [--show N]   (N: misses listed per failing case)"""
import csv, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); DBDIR = os.path.dirname(HERE)
sys.path.insert(0, DBDIR)
from build_input import KWFIELD
import connections
sys.path.insert(0, DBDIR); import source

def main():
    game = sys.argv[1]; show = int(sys.argv[sys.argv.index('--show') + 1]) if '--show' in sys.argv else 8
    c = sqlite3.connect(os.path.join(DBDIR, 'cards.sqlite'))
    lib = source.lib()
    cards = {i: n for i, n in c.execute('select id, name from card where is_keyword=0 and is_stub=0 and game=?', (game,))}
    region = {i: r for i, r in c.execute('select id, regions from card where game=?', (game,))}
    own, kws = {}, {}
    for i, t in lib.execute('select id, text from entities where game=?', (game,)):
        if i not in cards: continue
        t = ' '.join((t or '').split()); m = KWFIELD.match(t)
        own[i] = (t[m.end():] if m else t); kws[i] = {k.strip().lower() for k in m.group(1).split(',')} if m else set()
    out = ['# Case tests: ' + game, '', 'Made by `cases/run.py ' + game + '`.', '']
    total = passed = 0
    # mechanics
    out += ['## Mechanics (expected cards from the texts)', '', '| case | question | expected | found | recall | extra | pass |', '|---|---|---|---|---|---|---|']
    details = []
    for r in csv.DictReader(open(os.path.join(HERE, 'mechanics.tsv')), delimiter='\t'):
        if r['game'] not in ('*', game): continue
        kind, _, val = r['expected'].partition(':')
        exp = {i for i in cards if (re.search(val, own[i], re.I) if kind == 'text' else val.lower() in kws[i])} if kind else set()
        got = {x for (x,) in c.execute(r['query'])} & set(cards)
        hit = exp & got; rec = len(hit) / len(exp) if exp else 1.0; ok = rec >= 0.95
        total += 1; passed += ok
        out.append(f"| {r['id']} | {r['question']} | {len(exp)} | {len(hit)} | {rec:.0%} | {len(got - exp)} | {'yes' if ok else 'NO'} |")
        if not ok: details.append((r['id'], r['question'], sorted(cards[i] for i in exp - got)[:show]))
    if details:
        out += ['', 'Missed cards (first ' + str(show) + ' per failing case):', '']
        out += [f'- {i} {q}: ' + ', '.join(m) for i, q, m in details]
    # combos
    path = os.path.join(HERE, 'combos.tsv')
    if os.path.exists(path):
        out += ['', '## Combos (the enabler must set off the payoff)', '', '| case | enabler | payoff | why | found as | pass |', '|---|---|---|---|---|---|']
        for r in csv.DictReader(open(path), delimiter='\t'):
            if r['game'] != game: continue
            how = connections.explain(c, r['enabler'], r['payoff'])
            total += 1; passed += bool(how)
            out.append(f"| {r['id']} | {r['enabler']} | {r['payoff']} | {r['why']} | {how or '-'} | {'yes' if how else 'NO'} |")
    # regions
    path = os.path.join(HERE, 'regions.tsv')
    if os.path.exists(path):
        out += ['', '## Region identity (signature, splash, archetype)', '', '| case | region | kind | mechanic | need | found | pass |', '|---|---|---|---|---|---|---|']
        for r in csv.DictReader(open(path), delimiter='\t'):
            if r['game'] != game: continue
            got = {x for (x,) in c.execute(r['query'])} & set(cards)
            n = len([i for i in got if r['region'] in (region[i] or '').split(';')])
            ok = n >= int(r['need']); total += 1; passed += ok
            out.append(f"| {r['id']} | {r['region']} | {r['kind']} | {r['mechanic']} | {r['need']} | {n} | {'yes' if ok else 'NO'} |")
    # decks from players' guides: the deck explanation must name what the guide says the deck does
    path = os.path.join(HERE, 'decks.tsv')
    if os.path.exists(path):
        import deck_analysis
        out += ['', '## Guide decks (the explanation must say what the guide says)', '', '| case | deck | must say | missing | pass |', '|---|---|---|---|---|']
        for r in csv.DictReader(open(path), delimiter='\t'):
            if r['game'] != game: continue
            text = '\n'.join(deck_analysis.analyze(c, game, r['cards'])).lower()
            miss = [w for w in r['must'].split(';') if w.strip() and w.strip().lower() not in text]
            total += 1; passed += not miss
            out.append(f"| {r['id']} | {r['deck']} | {r['must']} | {', '.join(miss) or '-'} | {'yes' if not miss else 'NO'} |")
    # deck networks: a line that must be there (or must not) between two cards of a deck from the web (Kaptain's check)
    path = os.path.join(HERE, 'network.tsv')
    if os.path.exists(path):
        import network, mechanics
        decks = {r['deck']: r['cards'] for f in (os.path.join(DBDIR, 'decks.tsv'), os.path.join(HERE, 'decks.tsv')) if os.path.exists(f)
                 for r in csv.DictReader(open(f, encoding='utf-8'), delimiter='\t') if r['game'] == game}
        out += ['', '## Deck networks (a line must be there, or must not)', '', '| case | deck | from | to | expect | found | pass |', '|---|---|---|---|---|---|---|']
        nets = {}
        for r in csv.DictReader(open(path, encoding='utf-8'), delimiter='\t'):
            if r['game'] != game: continue
            if r['deck'] not in nets:
                import deck_analysis
                ids, _ = deck_analysis.parse_deck(c, game, decks.get(r['deck'], ''))
                nodes, lines = network.network(c, game, ids)
                nets[r['deck']] = ({i: mechanics.name(c, i) for i in nodes}, lines)
            nm, lines = nets[r['deck']]
            hit = [f'{k}: {y}' for (a, b), ls in lines.items() if (r['from'] == '*' or nm[a] == r['from']) and nm[b] == r['to']
                   for k, w, y in ls if k != 'targets']  # the line's kind and why ("boosts: gives it +1|+1")
            if r['expect'] == 'line': ok = bool(hit)
            else: ok = not hit if not r['why_not'] else not any(r['why_not'] in y for y in hit)
            total += 1; passed += ok
            out.append(f"| {r['id']} | {r['deck']} | {r['from']} | {r['to']} | {r['expect']} {r['why_not']} | {'; '.join(sorted(set(hit)))[:80] or '-'} | {'yes' if ok else 'NO'} |")
    out.insert(3, f'**{passed} of {total} cases pass.**\n')
    open(os.path.join(HERE, 'REPORT.md'), 'w').write('\n'.join(out) + '\n'); print(f'{passed} of {total} cases pass')

if __name__ == '__main__':
    main()
