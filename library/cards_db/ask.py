"""Standard questions over cards.sqlite, answered with card names grouped by game. <games> is one game, several joined
by commas (runeterra,stormbound) or all. Every question uses only generic values (vocab.tsv, the concept tree), so the same
question runs across games.
  ask.py <games> cares <happening|concept> [mine|enemy]  cards that wait for, test, count or pick things by it (flat_ref)
  ask.py <games> makes <happening|concept> [mine|enemy]  cards that cause it (kill -> dies, freeze -> disable, ...)
  ask.py <games> concept <concept>                cards with a concept-tree concept (flat_concept), e.g. removal, revive
  ask.py <games> both <A> <B>                     cards that have both A and B (each a concept or a happening the card makes)
  ask.py <games> compare <concept> [...]          per game: how many cards, and examples (how each game does it)
  ask.py <games> combo <card A> <card B>          every way A sets off B, most direct first (both cards of one game)
  ask.py <games> partners <card>                  cards A sets off and cards that set off A, in the chosen games
  ask.py <games> together <concept>               mechanics found on the same cards as this one (what it is built with)
  ask.py <games> feeds <concept>                  mechanics this one sets off, inside each game, added up over games
  ask.py <games> fed <concept>                    mechanics that set this one off
  ask.py <games> chains <concept>                 families of three mechanics: A sets off B, B sets off C
  ask.py <game> deck <card or concept> [size]     cards of one game that feed each other around it, in its faction
  ask.py <game> analyze "<card>, <card>, ..."      a deck: its mechanics, how its cards feed each other, what it lacks
  ask.py <games> card <card>                      the card's text and stored rows (rows.py)
  ask.py <games> list happenings|concepts         the values these questions take
Happenings are the event values of vocab.tsv; concepts are the concept tree's (equal mechanics of different games share
one concept: Stun and Freeze are disable, round_start and turn_start are turn_start)."""
import os, sqlite3, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import connections, mechanics
c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))


def games_of(arg):
    allg = [g for (g,) in c.execute('select distinct game from card order by game')]
    return allg if arg == 'all' else [g for g in arg.split(',') if g in allg]


def ids_of(games, sql, args=()):
    got = {i for (i,) in c.execute(sql, args)}
    marks = ','.join('?' * len(games))
    return {i: (g, n) for i, g, n in c.execute(f'select id, game, name from card where game in ({marks}) and is_keyword=0 and is_stub=0',
                                               games) if i in got}


def names(games, sql, args=(), limit=None):
    found = ids_of(games, sql, args)
    for g in games:
        out = sorted(n for gg, n in found.values() if gg == g)
        if out: print(f'{g}: {len(out)} cards: ' + ', '.join(out[:limit]) + (' ...' if limit and len(out) > limit else ''))
    if not found: print('no cards')


def feature_sql(x):
    """a concept or a happening the card makes"""
    return ("select card from flat_concept where concept=? union select card from flat_ref where happening=? and role='makes'", (x, x))


def side_sql(side):
    return {'mine': " and side in ('mine','any','')", 'enemy': " and side in ('enemy','any','')"}.get(side, '')


def main():
    games, q, args = games_of(sys.argv[1]), sys.argv[2], sys.argv[3:]
    col = 'happening' if args and c.execute("select 1 from vocab where field='event' and value=?", (args[0],)).fetchone() else 'concept'
    if q == 'cares': names(games, f"select card from flat_ref where {col}=? and role!='makes'" + side_sql(args[1] if len(args) > 1 else ''), (args[0],))
    elif q == 'makes': names(games, f"select card from flat_ref where {col}=? and role='makes'" + side_sql(args[1] if len(args) > 1 else ''), (args[0],))
    elif q == 'together':
        for x, per in mechanics.together(c, games, args[0]): print(f'{x}: ' + ', '.join(f'{g} {n} cards' for g, n in per.items()))
    elif q in ('feeds', 'fed'):
        for x, per in mechanics.feeds(c, games, args[0], reverse=q == 'fed'):
            print(f'{x}: ' + '; '.join(f'{g} {n} pairs, e.g. {ex}' for g, (n, ex) in per.items()))
    elif q == 'chains':
        for n, a, b, x, gs in mechanics.chains(c, games, args[0]): print(f'{a} -> {b} -> {x}  (seen in {", ".join(gs)})')
    elif q == 'analyze': print('\n'.join(mechanics.analyze(c, games[0], ' '.join(args))))
    elif q == 'deck':
        size = int(args[1]) if len(args) > 1 else {'stormbound': 12}.get(games[0], 14)
        ids, allowed = mechanics.deck(c, games[0], args[0], size)
        print(f'{games[0]}, factions {", ".join(sorted(allowed))}: ' + ', '.join(mechanics.name(c, i) for i in ids) if ids else 'nothing found')
    elif q == 'concept': names(games, 'select card from flat_concept where concept=?', (args[0],))
    elif q == 'both':
        (sa, pa), (sb, pb) = feature_sql(args[0]), feature_sql(args[1])
        names(games, f'select card from ({sa}) intersect select card from ({sb})', pa + pb)
    elif q == 'compare':
        for x in args:
            print(f'## {x}'); names(games, 'select card from flat_concept where concept=?', (x,), limit=8)
    elif q == 'combo':
        rs = sorted(set(connections.reasons(c, args[0], args[1])))
        print('\n'.join(f'{why}' for _, why in rs) or 'no connection')
    elif q == 'partners':
        me = args[0]; marks = ','.join('?' * len(games))
        all_ = [n for (n,) in c.execute(f'select name from card where game in ({marks}) and is_keyword=0 and is_stub=0', games)]
        out = [n for n in all_ if n != me and connections.explain(c, me, n)][:40]
        inn = [n for n in all_ if n != me and connections.explain(c, n, me)][:40]
        print(f'{me} sets off: ' + ', '.join(out)); print(f'set off {me}: ' + ', '.join(inn))
    elif q == 'card': subprocess.run([sys.executable, os.path.join(HERE, 'rows.py')] + args)
    elif q == 'list':
        sql = "select value from vocab where field='event'" if args[0] == 'happenings' else 'select distinct concept from flat_concept'
        print(', '.join(sorted(v for (v,) in c.execute(sql) if v)))
    else: print(__doc__)

main()
