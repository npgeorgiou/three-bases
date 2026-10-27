"""A card's rows in cards.sqlite exactly as stored (ids, values, numbers), table by table, nothing turned into words.
Usage: raw.py <card id> [...]"""
import os, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__))
c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))

def rows(table, where, args):
    cur = c.execute(f'select * from {table} where {where}', args); cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]

def line(table, r): print(f'  {table} ' + ' '.join(f'{k}={v}' for k, v in r.items() if v is not None))

def target(t, seen):
    if t is None or ('t', t) in seen: return
    seen.add(('t', t))
    for r in rows('target', 'id=?', (t,)): line('target', r); amount(r['n'], seen)
    for r in rows('filter', 'target=?', (t,)): line('filter', r); amount(r['n'], seen)

def amount(a, seen):
    if a is None or ('a', a) in seen: return
    seen.add(('a', a))
    for r in rows('amount', 'id=?', (a,)):
        line('amount', r); target(r['of_target'], seen); event(r['event'], seen); amount(r['inner'], seen)
    for r in rows('amount_item', 'amount=?', (a,)): line('amount_item', r); amount(r['item'], seen)

def event(e, seen):
    if e is None or ('e', e) in seen: return
    seen.add(('e', e))
    for r in rows('event', 'id=?', (e,)): line('event', r); target(r['actor'], seen); target(r['object'], seen)

def ability(a, seen):
    line('ability', a); event(a['event'], seen)
    for r in rows('cond', 'ability=?', (a['id'],)):
        line('cond', r); target(r['of_target'], seen); amount(r['n'], seen); event(r['event'], seen); amount(r['value'], seen)
    for e in rows('effect', 'ability=? order by seq', (a['id'],)):
        line('effect', e); target(e['on_target'], seen); target(e['to_target'], seen)
        for p in rows('param', 'effect=?', (e['id'],)): line('param', p); amount(p['amount'], seen)
        for sub in rows('ability', 'given_by_effect=?', (e['id'],)): ability(sub, seen)

for cid in map(int, sys.argv[1:]):
    seen = set()
    for r in rows('card', 'id=?', (cid,)): line('card', r)
    for t in ('card_keyword', 'card_type', 'card_link'):
        for r in rows(t, ('card' if t != 'card_link' else 'src') + '=?', (cid,)): line(t, r)
    for a in rows('ability', 'card=? and given_by_effect is null order by seq', (cid,)): ability(a, seen)
    print()
