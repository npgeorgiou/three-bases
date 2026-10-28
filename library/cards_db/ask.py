"""Standard questions over cards.sqlite, answered with card names grouped by game. <games> is one game, several joined
by commas (runeterra,stormbound) or all. Every question uses only generic values (vocab.tsv, the concept tree), so the same
question runs across games.
  ask.py <games> cares <happening> [mine|enemy]   cards that wait for, test, count or pick things by a happening (flat_ref)
  ask.py <games> makes <happening> [mine|enemy]   cards that cause it (kill -> dies, summon -> summoned, ...)
  ask.py <games> concept <concept>                cards with a concept-tree concept (flat_concept), e.g. removal, revive
  ask.py <games> both <A> <B>                     cards that have both A and B (each a concept or a happening the card makes)
  ask.py <games> compare <concept> [...]          per game: how many cards, and examples (how each game does it)
  ask.py <games> combo <card A> <card B>          every way A sets off B, most direct first (both cards of one game)
  ask.py <games> partners <card>                  cards A sets off and cards that set off A, in the chosen games
  ask.py <games> card <card>                      the card's text and stored rows (rows.py)
  ask.py <games> list happenings|concepts         the values these questions take
Happenings are the event values of vocab.tsv; concepts are the concept tree's (equal mechanics of different games share
one concept: Stun and Freeze are disable, round_start and turn_start are turn_start)."""
import os, sqlite3, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import connections
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
    if q == 'cares': names(games, "select card from flat_ref where happening=? and role!='makes'" + side_sql(args[1] if len(args) > 1 else ''), (args[0],))
    elif q == 'makes': names(games, "select card from flat_ref where happening=? and role='makes'" + side_sql(args[1] if len(args) > 1 else ''), (args[0],))
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
