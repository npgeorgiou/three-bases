"""Standard questions over cards.sqlite, answered with card names grouped by game. <games> is one game, several joined
by commas (runeterra,stormbound) or all. Every question uses only generic values (vocab.tsv, the concept tree), so the same
question runs across games.
  ask.py <games> cares <happening|concept> [mine|enemy]  cards that wait for, test, count or pick things by it (flat_ref)
  ask.py <games> makes <happening|concept> [mine|enemy]  cards that cause it (kill -> dies, freeze -> disable, ...)
  ask.py <games> concept <concept>                cards with a concept-tree concept (flat_concept), e.g. removal, revive
  ask.py <games> both <A> <B>                     cards that have both A and B (each a concept or a happening the card makes)
  ask.py <games> compare <concept> [...]          per game: how many cards, and examples (how each game does it)
  ask.py <games> factions <concept>               per game and faction: share of its cards with the concept, highest first
                                                  (which faction is about it: base_resource_gain, sacrifice, movement ...)
  ask.py <games> combo <card A> <card B>          every way A sets off B, most direct first (both cards of one game)
  ask.py <games> partners <card>                  cards A sets off and cards that set off A, in the chosen games
  ask.py <games> together <concept>               mechanics found on the same cards as this one (what it is built with)
  ask.py <games> feeds <concept>                  mechanics this one sets off, inside each game, added up over games
  ask.py <games> fed <concept>                    mechanics that set this one off
  ask.py <games> chains <concept>                 families of three mechanics: A sets off B, B sets off C
  ask.py <game> deck <card or concept> [size]     cards of one game that feed each other around it, in its faction
  ask.py <game> analyze "<card>, <card>, ..."      a deck: its mechanics, how its cards feed each other, what it lacks
  ask.py <game> network "<card>, ..." | faction <name> | game [--json f]  cards as a network: central cards, chains, groups, loose cards
  ask.py <games> card <card>                      the card's text and stored rows (rows.py)
  ask.py <games> kit <concept> [<concept> ...]    a faction built on these: per game the two factions that combine them
                                                  most, their key cards with texts, and what the first concept works with
  ask.py <games> list happenings|concepts         the values these questions take
  --texts: every card found with its short text (a game with 10 or fewer cards always shows them)
Cards that make a card with it count too, named "Zed (via Living Shadow)". The game's enemies, bosses and run events are
left out unless --enemies is given. An unknown concept says so and names the nearest ones.
Happenings are the event values of vocab.tsv; concepts are the concept tree's (equal mechanics of different games share
one concept: Stun and Freeze are disable, round_start and turn_start are turn_start)."""
import os, sqlite3, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import connections, mechanics, deck_analysis, network
c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))


def games_of(arg):
    allg = [g for (g,) in c.execute('select distinct game from card order by game')]
    return allg if arg == 'all' else [g for g in arg.split(',') if g in allg]


def subtree():
    """each concept with every concept under it in library/concept_tree.txt (suppress: disable, silence, immobilize ...)"""
    kids = {}
    for line in open(os.path.join(HERE, '..', 'concept_tree.txt'), encoding='utf-8'):
        if line.startswith('#') or '|' not in line: continue
        f = [x.strip() for x in line.split('|')]
        for p_ in filter(None, (x.strip() for x in f[3].split(','))): kids.setdefault(p_, set()).add(f[0])
        kids.setdefault(f[0], set())
    out = {}
    def walk(x, seen):
        for k in kids.get(x, ()):
            if k not in seen: seen.add(k); walk(k, seen)
        return seen
    for x in kids: out[x] = walk(x, {x})
    return out
SUB = subtree()
c.create_function('under', 2, lambda v, x: v == x or v in SUB.get(x, ()), deterministic=True)  # a concept or one under it


ENEMY = ('boss', 'monster', 'event', 'modifier')  # the game's enemies and run events: no player's cards (--enemies keeps them)
WITH_ENEMIES = '--enemies' in sys.argv
if WITH_ENEMIES: sys.argv.remove('--enemies')


def ids_of(games, sql, args=()):
    """the cards the query finds, plus every card that makes one of them (Zed makes Living Shadow: Zed brings what it has);
    a maker found only through its made card is named with it: "Zed (via Living Shadow)" """
    got = {i for (i,) in c.execute(sql, args)}
    via = {}
    for a, b in c.execute('select card, made from flat_made order by depth'):
        if b in got and a not in got: via.setdefault(a, b)
    marks = ','.join('?' * len(games))
    keep = '' if WITH_ENEMIES else f" and coalesce(category,'') not in ({','.join(repr(x) for x in ENEMY)})"
    out = {}
    for i, g, n in c.execute(f'select id, game, name from card where game in ({marks}) and is_keyword=0 and is_stub=0' + keep, games):
        if i in got: out[i] = (g, n)
        elif i in via: out[i] = (g, f"{n} (via {mechanics.name(c, via[i])})")
    return out


def known(x):
    """a concept or happening the database has; else say so and name the nearest ones"""
    have = set(SUB) | {v for (v,) in c.execute("select distinct concept from flat_concept")} | {v for (v,) in c.execute("select value from vocab where field='event'")}
    if x in have: return True
    import difflib
    print(f'unknown concept or happening "{x}"; nearest: ' + ', '.join(difflib.get_close_matches(x, have, 6, 0.4) or sorted(v for v in have if x.split('_')[0] in v)[:6]))
    return False


TEXTS = '--texts' in sys.argv
if TEXTS: sys.argv.remove('--texts')
LIB = []


def short_text(i, n=90):
    """the card's own text, short (a design question needs to see what the card does, not only its name)"""
    if not LIB:
        import source; LIB.append(source.lib())
    r = LIB[0].execute('select text from entities where id=?', (i,)).fetchone()
    t = ' '.join(((r[0] if r else '') or '').replace('Missing Translation', '').split())
    return t if len(t) <= n else t[:n - 1].rsplit(' ', 1)[0] + '...'


def names(games, sql, args=(), limit=None):
    """per game the cards found; with their short texts when few (10 or less) or with --texts"""
    found = ids_of(games, sql, args)
    for g in games:
        out = sorted((n, i) for i, (gg, n) in found.items() if gg == g)
        if not out: continue
        if TEXTS or len(out) <= 10:
            print(f'{g}: {len(out)} cards:')
            for n, i in out[:limit]: print(f'  {n}: {short_text(i)}')
            if limit and len(out) > limit: print('  ...')
        else: print(f'{g}: {len(out)} cards: ' + ', '.join(n for n, _ in out[:limit]) + (' ...' if limit and len(out) > limit else ''))
    if not found: print('no cards')


def feature_sql(x):
    """a concept or a happening the card makes"""
    return ("select card from flat_concept where under(concept, ?) union select card from flat_ref where happening=? and role='makes' and origin!='game'", (x, x))


def side_sql(side):
    return {'mine': " and side in ('mine','any','')", 'enemy': " and side in ('enemy','any','')"}.get(side, '')


def main():
    games, q, args = games_of(sys.argv[1]), sys.argv[2], sys.argv[3:]
    if q in ('cares', 'makes', 'concept', 'together', 'feeds', 'fed', 'chains', 'factions') and args and not known(args[0]): return
    if q in ('both', 'compare') and not all(known(x) for x in args): return
    col = 'happening' if args and c.execute("select 1 from vocab where field='event' and value=?", (args[0],)).fetchone() else 'concept'
    if q == 'cares': names(games, f"select card from flat_ref where {'under(concept, ?)' if col == 'concept' else col + '=?'} and role!='makes'" + side_sql(args[1] if len(args) > 1 else ''), (args[0],))
    elif q == 'makes': names(games, f"select card from flat_ref where {'under(concept, ?)' if col == 'concept' else col + '=?'} and role='makes' and origin!='game'" + side_sql(args[1] if len(args) > 1 else ''), (args[0],))
    elif q == 'together':
        for x, per in mechanics.together(c, games, args[0]): print(f'{x}: ' + ', '.join(f'{g} {n} cards' for g, n in per.items()))
    elif q in ('feeds', 'fed'):
        for x, per in mechanics.feeds(c, games, args[0], reverse=q == 'fed'):
            print(f'{x}: ' + '; '.join(f'{g} {n} pairs, e.g. {ex}' for g, (n, ex) in per.items()))
    elif q == 'chains':
        for n, a, b, x, gs in mechanics.chains(c, games, args[0]): print(f'{a} -> {b} -> {x}  (seen in {", ".join(gs)})')
    elif q == 'network': print('\n'.join(network.run(c, games[0], args)))
    elif q == 'analyze': print('\n'.join(deck_analysis.analyze(c, games[0], ' '.join(args))))
    elif q == 'deck':
        size = int(args[1]) if len(args) > 1 else {'stormbound': 12}.get(games[0], 14)
        ids, allowed = mechanics.deck(c, games[0], args[0], size)
        print(f'{games[0]}, factions {", ".join(sorted(allowed))}: ' + ', '.join(mechanics.name(c, i) for i in ids) if ids else 'nothing found')
    elif q == 'concept': names(games, 'select card from flat_concept where under(concept, ?)', (args[0],))
    elif q == 'both':
        (sa, pa), (sb, pb) = feature_sql(args[0]), feature_sql(args[1])
        names(games, f'select card from ({sa}) intersect select card from ({sb})', pa + pb)
    elif q == 'compare':
        for x in args:
            print(f'## {x}'); names(games, 'select card from flat_concept where under(concept, ?)', (x,), limit=8)
    elif q == 'kit':  # a faction built on these concepts: per game the factions that combine them most, their key cards, partners
        if not all(known(x) for x in args): return
        got = {x: set(ids_of(games, 'select card from flat_concept where under(concept, ?)', (x,))) for x in args}
        for g in games:
            per = {}
            for i, regs in c.execute("select id, regions from card where game=? and is_keyword=0 and is_stub=0 and coalesce(category,'') not in "
                                     "('game_rule','ability','boss','monster','event','modifier')", (g,)):
                k = sum(i in got[x] for x in args)
                for r in [x for x in (regs or '').split(';') if x and not x.lower().startswith(('neutral', 'boss', 'any'))]:
                    per.setdefault(r, [[0] * len(args), 0, []])
                    per[r][1] += 1
                    for j, x in enumerate(args): per[r][0][j] += i in got[x]
                    if k: per[r][2].append((k, i))
            score = {r: sum(min(1.0, n / max(1, t) * 5) for n in ns) for r, (ns, t, _) in per.items()}  # each concept counts up to a fifth of the faction
            top = [r for r in sorted(score, key=lambda r: -score[r]) if score[r]][:2]
            if not top: continue
            print(f'## {g}')
            for r in top:
                ns, t, cs = per[r]
                print(f'{r} ({t} cards): ' + ', '.join(f'{x} {n}' for x, n in zip(args, ns)))
                for k, i in sorted(cs, key=lambda x: (-x[0], mechanics.name(c, x[1])))[:4]:
                    print(f'  {mechanics.name(c, i)}: {short_text(i)}')
            pairs = [(x, per_) for x, per_ in mechanics.feeds(c, [g], args[0], top=3)]
            if pairs: print('  works with: ' + '; '.join(f'{x} (e.g. {list(p.values())[0][1]})' for x, p in pairs))
    elif q == 'factions':
        got = set(ids_of(games, 'select card from flat_concept where under(concept, ?)', (args[0],)))
        for g in games:
            per = {}
            for i, regs in c.execute("select id, regions from card where game=? and is_keyword=0 and is_stub=0 and coalesce(category,'') not in "
                                     f"('game_rule','ability'{'' if WITH_ENEMIES else ',' + ','.join(repr(x) for x in ENEMY)})", (g,)):
                for r in (regs or '').split(';') or ['']:
                    per.setdefault(r or '(none)', [0, 0]); per[r or '(none)'][1] += 1; per[r or '(none)'][0] += i in got
            rows = sorted(((n / t, n, t, r) for r, (n, t) in per.items() if n), reverse=True)
            if rows: print(f'{g}: ' + '; '.join(f'{r} {n} of {t} ({x:.0%})' for x, n, t, r in rows))
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
