"""Standard questions over cards.sqlite, answered with card names (the same for every game).
  ask.py <game> cares <happening> [mine|enemy]   cards that wait for, test, count or pick things by a happening (flat_ref)
  ask.py <game> makes <happening> [mine|enemy]   cards that cause it (kill -> dies, summon -> summoned, ...)
  ask.py <game> concept <concept>                cards with a concept-tree concept (flat_concept), e.g. removal, revive
  ask.py <game> combo <card A> <card B>          every way A sets off B, most direct first (connections.reasons)
  ask.py <game> partners <card>                  cards A sets off and cards that set off A (first 40 each)
  ask.py <game> card <card>                      the card's text and stored rows (rows.py)
  ask.py <game> list happenings|concepts         the values these questions take
Happenings are the event values of vocab.tsv."""
import os, sqlite3, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import connections
c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))


def names(game, sql, args=()):
    ids = {i for (i,) in c.execute(sql, args)}
    out = sorted(n for i, n in c.execute('select id, name from card where game=? and is_keyword=0 and is_stub=0', (game,)) if i in ids)
    print(f'{len(out)} cards: ' + ', '.join(out))


def side_sql(side):
    return {'mine': " and side in ('mine','any','')", 'enemy': " and side in ('enemy','any','')"}.get(side, '')


def main():
    game, q, args = sys.argv[1], sys.argv[2], sys.argv[3:]
    if q == 'cares': names(game, "select card from flat_ref where happening=? and role!='makes'" + side_sql(args[1] if len(args) > 1 else ''), (args[0],))
    elif q == 'makes': names(game, "select card from flat_ref where happening=? and role='makes'" + side_sql(args[1] if len(args) > 1 else ''), (args[0],))
    elif q == 'concept': names(game, 'select card from flat_concept where concept=?', (args[0],))
    elif q == 'combo':
        rs = sorted(set(connections.reasons(c, args[0], args[1])))
        print('\n'.join(f'{why}' for _, why in rs) or 'no connection')
    elif q == 'partners':
        me = args[0]
        all_ = [n for (n,) in c.execute('select name from card where game=? and is_keyword=0 and is_stub=0', (game,))]
        out = [n for n in all_ if n != me and connections.explain(c, me, n)][:40]
        inn = [n for n in all_ if n != me and connections.explain(c, n, me)][:40]
        print(f'{me} sets off: ' + ', '.join(out)); print(f'set off {me}: ' + ', '.join(inn))
    elif q == 'card': subprocess.run([sys.executable, os.path.join(HERE, 'rows.py')] + args)
    elif q == 'list':
        sql = "select value from vocab where field='event'" if args[0] == 'happenings' else 'select distinct concept from flat_concept'
        print(', '.join(sorted(v for (v,) in c.execute(sql) if v)))
    else: print(__doc__)


main()
