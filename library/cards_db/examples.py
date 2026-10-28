"""Example questions over cards.sqlite with their real answers, every one asked across all games at once; writes QUERIES.md
(rerun after every rebuild; run.py does it). Answers are grouped by game.
Usage: examples.py"""
import os, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import connections, mechanics, deck_analysis
c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))
name = lambda i: c.execute('select name from card where id=?', (i,)).fetchone()[0]
game = lambda i: c.execute('select game from card where id=?', (i,)).fetchone()[0]
out = ['# Example queries (made by `examples.py` from cards.sqlite)', '',
       'Every question runs across all games: it uses only generic values (vocab.tsv) and concepts (the concept tree), never',
       "a game's own words. The same question in `ask.py` form is given where one exists (`ask.py all ...`). Answers are grouped",
       'by game, first cards only.', '']

def q(title, sql, note='', limit=8, ask=''):
    ids = [r[0] for r in c.execute(sql)]
    out.extend([f'## {title}', ''] + ([f'`ask.py {ask}`', ''] if ask else []) + ['```sql', sql, '```'])
    for g in sorted({game(i) for i in ids}):
        names = sorted({name(i) for i in ids if game(i) == g})
        out.append(f'- {g}: {len(names)} cards: ' + ', '.join(names[:limit]) + (' ...' if len(names) > limit else ''))
    out.append('' if ids else 'no cards\n')
    if note: out.extend([note, ''])
    return ids

q('Cards that stop enemy units acting (Runeterra Stun, Stormbound Freeze, keywords that mean it)',
  "select distinct card from flat_concept where concept in ('disable','cant_attack')", ask='all concept disable')
pay = q('Payoffs: cards that benefit from my other units dying, any way (trigger, condition, count, dead allies picked)',
        "select distinct card from flat_ref where happening='dies' and role!='makes' and side in ('mine','any','') and coalesce(pick,'')!='self'",
        ask='all cares dies mine')
ena = q('Enablers: cards that kill or sacrifice my own units',
        "select distinct card from flat_concept where concept='sacrifice'")
pairs = []
pick = lambda L: [i for g in sorted({game(x) for x in L}) for i in [x for x in L if game(x) == g][:25]]
for e in pick(ena):
    for p in pick(pay):
        how = connections.explain(c, name(e), name(p))
        if how: pairs.append((game(e), name(e), game(p), name(p), how))
out.extend(['## Combos between those two lists, inside each game (connections.explain)', '',
            f'{len(pairs)} pairs, for example:', ''] + [f'- {a}: {b} -> {d} ({h})' for a, b, _, d, h in pairs[:8]] + [''])
q('How each game does "move enemy units" (push, pull, force to move)', "select distinct card from flat_concept where concept='forced_movement'",
  ask='all compare forced_movement')
q('Cards that both move units and care about neighbours (is this combination of mechanics used, and where?)',
  "select card from flat_concept where concept in ('movement','forced_movement') intersect select card from flat_concept where concept='adjacency'",
  ask='all both forced_movement adjacency')
q('Turn-start effects, any game (Runeterra round start, Stormbound start of your turn)', "select distinct card from flat_concept where concept='turn_start'",
  ask='all concept turn_start')
q('Drain: damage, then the same amount to my side (heal the player, or strength to the drainer)',
  "select distinct card from flat_concept where concept='lifesteal'", ask='all concept lifesteal')
q('Cards that care about a unit having a status any game gives (stunned, frozen, poisoned ...)',
  "select distinct card from flat_ref where happening='given_keyword' and role!='makes'", ask='all cares given_keyword')
q('Effects that grow with a count ("for each", "equal to"), any game', "select distinct card from flat_do where params glob '*=[a-z]*'")
games = [g for (g,) in c.execute('select distinct game from card order by game')]
out.extend(['## Mechanics, not cards', '', 'What "disable" (stop a unit acting) is built with, on the same cards (`ask.py all together disable`):', ''] +
           [f'- {x}: ' + ', '.join(f'{g} {n} cards' for g, n in per.items()) for x, per in mechanics.together(c, games, 'disable', top=6)] +
           ['', 'Mechanics that feed "units dying" payoffs, inside each game (`ask.py all fed death_trigger`):', ''] +
           [f'- {x}: ' + '; '.join(f'{g} {n} pairs, e.g. {ex}' for g, (n, ex) in per.items()) for x, per in mechanics.feeds(c, games, 'death_trigger', top=6, reverse=True)] +
           ['', 'Families of three mechanics that feed each other, starting from "summon" (`ask.py all chains summon`):', ''] +
           [f'- {a} -> {b} -> {x} (seen in {", ".join(gs)})' for n, a, b, x, gs in mechanics.chains(c, games, 'summon', top=6)] + [''])
out.extend(['## A deck explained (`ask.py runeterra analyze "..."`), a Lucian/Senna deck from a deck guide', '', '```'] +
           deck_analysis.analyze(c, 'runeterra', 'Lucian, Senna, Glimpse Beyond, Single Combat, Crumble, Piercing Darkness, The Ruination, '
                                 'Ravenous Butcher, Hapless Aristocrat, Cursed Keeper, Lonely Chimeslime, The Undying, Senna, Sentinel of Light, Spirit Leech') + ['```', ''])
out.extend(['## Decks: cards of one game that feed each other', ''])
for g, seed in (('stormbound', 'Wisp Cloud'), ('stormbound', 'Doppelbocks'), ('runeterra', 'Kalista')):
    ids, allowed = mechanics.deck(c, g, seed, 12 if g == 'stormbound' else 14)
    out.append(f'- `ask.py {g} deck "{seed}"` ({", ".join(sorted(allowed))}): ' + ', '.join(mechanics.name(c, i) for i in ids))
out.append('')
q('Same effect, compare cost: deal damage to anything (unit, structure or player), cheapest first',
  "select distinct d.card from flat_do d join card cd on cd.id=d.card where d.act='damage' and d.on_kind in ('any','anything') order by cd.cost")
q('Cards that copy keywords between units (a mechanic found while testing)',
  "select distinct card from flat_do where act='copy_keywords'")
out.extend(["## What each faction or region leans on (concepts with the highest share of its cards vs its game)", ''])
for (gm,) in c.execute('select distinct game from card order by game').fetchall():
    total = c.execute('select count(*) from card where game=? and is_keyword=0 and is_stub=0', (gm,)).fetchone()[0]
    for (reg,) in c.execute("select distinct regions from card where game=? and regions not like '%;%' and regions!='' and is_keyword=0", (gm,)).fetchall():
        n = c.execute('select count(*) from card where game=? and regions=? and is_stub=0', (gm, reg)).fetchone()[0]
        if n < 25: continue
        rows = c.execute("""select f.concept, count(distinct f.card) k, (select count(distinct f2.card) from flat_concept f2 join card c2 on c2.id=f2.card
                            where f2.concept=f.concept and c2.game=?) g from flat_concept f join card cd on cd.id=f.card
                            where cd.game=? and cd.regions=? group by f.concept having k>=4""", (gm, gm, reg)).fetchall()
        top = sorted(rows, key=lambda r: -(r[1] / n) / (r[2] / total))[:5]
        out.append(f'- {gm} {reg}: ' + ', '.join(f'{con} ({k})' for con, k, g in top))
out.append('')
chains = c.execute("""select distinct a.card, d1.card_ref, d2.card_ref from flat_do d1 join ability a on a.id=d1.ability
                      join flat_do d2 on d2.card=d1.card_ref where d1.act='create' and d2.act='create' and d2.card_ref is not null
                      and d1.card_ref!=a.card and d2.card_ref!=d1.card_ref limit 8""").fetchall()
out.extend(['## Created-card chains (A creates B, B creates C)', ''] + [f'- {name(a)} -> {name(b)} -> {name(d)}' for a, b, d in chains] + [''])
open(os.path.join(HERE, 'QUERIES.md'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
