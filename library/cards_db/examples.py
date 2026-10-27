"""Example questions over cards.sqlite with their real answers; writes QUERIES.md (rerun after every rebuild).
Usage: examples.py"""
import os, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import connections
c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))
name = lambda i: c.execute('select name from card where id=?', (i,)).fetchone()[0]
out = ['# Example queries (made by `examples.py` from cards.sqlite)', '']

def q(title, sql, note='', limit=12):
    ids = [r[0] for r in c.execute(sql)]
    names = sorted({name(i) for i in ids})
    out.extend([f'## {title}', '', '```sql', sql, '```', f'{len(names)} cards: ' + ', '.join(names[:limit]) + (' ...' if len(names) > limit else ''), ''])
    if note: out.extend([note, ''])
    return ids

q('Cards that stop enemies attacking or blocking (any game wording: Stun, Frostbite-like, keywords that mean it)',
  "select distinct card from flat_concept where concept in ('disable','cant_attack')")
pay = q('Payoffs: something happens when one of my units dies',
        "select distinct card from flat_when where event='dies' and obj_side='mine' and coalesce(obj_pick,'')!='self'")
ena = q('Enablers: cards that kill or sacrifice my own units',
        "select distinct card from flat_concept where concept='sacrifice'")
pairs = []
for e in ena[:40]:
    for p in pay[:40]:
        how = connections.explain(c, name(e), name(p))
        if how: pairs.append((name(e), name(p), how))
out.extend(['## Combos found between those two lists (connections.explain)', '',
            f'{len(pairs)} pairs among the first 40 x 40, for example:', ''] +
           [f'- {a} -> {b} ({h})' for a, b, h in pairs[:10]] + [''])
q('Same effect, compare cost: deal damage to anything (unit or player), cheapest first',
  "select distinct d.card from flat_do d join card cd on cd.id=d.card where d.act='damage' and d.on_kind='any' order by cd.cost", limit=15)
q('Cards that copy keywords between units (a mechanic found while testing)',
  "select distinct card from flat_do where act='copy_keywords'")
out.extend(['## What each region leans on (concepts with the highest share of the region\'s cards vs the game)', ''])
total = c.execute('select count(*) from card where is_keyword=0 and is_stub=0').fetchone()[0]
for (reg,) in c.execute("select distinct regions from card where regions not like '%;%' and regions!='' and is_keyword=0").fetchall():
    n = c.execute('select count(*) from card where regions=? and is_stub=0', (reg,)).fetchone()[0]
    if n < 30: continue
    rows = c.execute("""select f.concept, count(distinct f.card) k, (select count(distinct card) from flat_concept where concept=f.concept) g
                        from flat_concept f join card cd on cd.id=f.card where cd.regions=? group by f.concept having k>=5""", (reg,)).fetchall()
    top = sorted(rows, key=lambda r: -(r[1] / n) / (r[2] / total))[:5]
    out.append(f'- {reg}: ' + ', '.join(f'{con} ({k})' for con, k, g in top))
out.append('')
chains = c.execute("""select distinct a.card, d1.card_ref, d2.card_ref from flat_do d1 join ability a on a.id=d1.ability
                      join flat_do d2 on d2.card=d1.card_ref where d1.act='create' and d2.act='create' and d2.card_ref is not null
                      and d1.card_ref!=a.card and d2.card_ref!=d1.card_ref limit 8""").fetchall()
out.extend(['## Created-card chains (A creates B, B creates C)', ''] + [f'- {name(a)} -> {name(b)} -> {name(d)}' for a, b, d in chains] + [''])
open(os.path.join(HERE, 'QUERIES.md'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
