"""The rows of chosen cards in cards.sqlite, one table per database table, columns exactly as stored, but every link to a
card, keyword, type or name part shown as its name instead of its id. One file, for Kaptain's check.
Usage: check_table.py <out.md> <card id> [...]     or     check_table.py <out.md> --random <game> <n>"""
import os, random, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__))
c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))
TEXT = {i: ' '.join((t or '').split()) for i, t in sqlite3.connect(os.path.join(HERE, '..', 'three-bases-library.sqlite')).execute('select id, text from entities')}

# column -> table its id points to (rows whose names replace the ids)
NAMED = {('card_keyword', 'card'): 'card', ('card_keyword', 'keyword'): 'card', ('card_type', 'card'): 'card',
         ('card_type', 'type'): 'type', ('card_link', 'src'): 'card', ('card_link', 'dst'): 'card', ('ability', 'card'): 'card',
         ('cond', 'keyword'): 'card', ('cond', 'ref_keyword'): 'card', ('effect', 'card_ref'): 'card',
         ('effect', 'keyword_ref'): 'card', ('effect', 'type_ref'): 'type', ('filter', 'ref_card'): 'card',
         ('filter', 'ref_keyword'): 'card', ('filter', 'ref_type'): 'type', ('filter', 'ref_word'): 'name_part'}
ORDER = ['card', 'card_keyword', 'card_type', 'card_link', 'ability', 'event', 'cond', 'effect', 'param', 'target',
         'filter', 'amount', 'amount_item']

def name(table, i):
    if i is None: return ''
    col = 'word' if table == 'name_part' else 'name'
    r = c.execute(f'select {col} from {table} where id=?', (i,)).fetchone()
    return r[0] if r else f'?{i}'

def collect(cards):
    """Row ids per table reachable from the cards (same walk as raw.py)."""
    got = {t: set() for t in ORDER}
    def target(t):
        if t is None or t in got['target']: return
        got['target'].add(t)
        n = c.execute('select n from target where id=?', (t,)).fetchone(); amount(n and n[0])
        for fid, fn in c.execute('select id, n from filter where target=?', (t,)).fetchall(): got['filter'].add(fid); amount(fn)
    def amount(a):
        if a is None or a in got['amount']: return
        got['amount'].add(a)
        r = c.execute('select of_target, event, inner from amount where id=?', (a,)).fetchone()
        if r: target(r[0]); event(r[1]); amount(r[2])
        for (it,) in c.execute('select item from amount_item where amount=?', (a,)).fetchall(): got['amount_item'].add((a, it)); amount(it)
    def event(e):
        if e is None or e in got['event']: return
        got['event'].add(e)
        r = c.execute('select actor, object from event where id=?', (e,)).fetchone()
        if r: target(r[0]); target(r[1])
    def ability(a):
        got['ability'].add(a)
        event(c.execute('select event from ability where id=?', (a,)).fetchone()[0])
        for cid, t, n, e, v in c.execute('select id, of_target, n, event, value from cond where ability=?', (a,)).fetchall():
            got['cond'].add(cid); target(t); amount(n); event(e); amount(v)
        for eid, t1, t2 in c.execute('select id, on_target, to_target from effect where ability=?', (a,)).fetchall():
            got['effect'].add(eid); target(t1); target(t2)
            for (p, am) in c.execute('select param, amount from param where effect=?', (eid,)).fetchall(): got['param'].add((eid, p)); amount(am)
            for (sub,) in c.execute('select id from ability where given_by_effect=?', (eid,)).fetchall(): ability(sub)
    for cid in cards:
        got['card'].add(cid)
        for t in ('card_keyword', 'card_type'):
            for r in c.execute(f'select rowid from {t} where card=?', (cid,)): got[t].add(r[0])
        for r in c.execute('select rowid from card_link where src=?', (cid,)): got['card_link'].add(r[0])
        for (a,) in c.execute('select id from ability where card=? and given_by_effect is null', (cid,)).fetchall(): ability(a)
    return got

def table(t, keys):
    cur = c.execute(f'select * from {t} limit 0'); cols = [d[0] for d in cur.description]
    if t in ('card_keyword', 'card_type', 'card_link'): where, args = 'rowid in (%s)', list(keys)
    elif t == 'amount_item': where, args = ' or '.join(['(amount=? and item=?)'] * len(keys)) or '0', [x for k in keys for x in k]
    elif t == 'param': where, args = ' or '.join(['(effect=? and param=?)'] * len(keys)) or '0', [x for k in keys for x in k]
    else: where, args = 'id in (%s)', list(keys)
    if '%s' in where: where = where % ','.join('?' * len(args))
    rows = c.execute(f'select * from {t} where {where} order by 1', args).fetchall() if keys else []
    out = [f'## {t} ({len(rows)} rows)', '', '| ' + ' | '.join(cols) + ' |', '|' + '---|' * len(cols)]
    if t == 'card': out[2] = out[2][:-1] + '| text (library, not stored here) |'; out[3] += '---|'
    for r in rows:
        vals = [name(NAMED[(t, k)], v) if (t, k) in NAMED and v is not None else ('' if v is None else str(v)) for k, v in zip(cols, r)]
        if t == 'card': vals.append(TEXT.get(r[0], ''))
        out.append('| ' + ' | '.join(v.replace('|', '/') for v in vals) + ' |')
    return out + ['']

def main():
    out_path, args = sys.argv[1], sys.argv[2:]
    if args[0] == '--random':
        ids = [i for (i,) in c.execute('select id from card where game=? and is_keyword=0 and is_stub=0', (args[1],))]
        random.seed(); cards = random.sample(ids, int(args[2]))
    else: cards = [int(a) for a in args]
    got = collect(cards)
    out = ['# Stored rows of ' + str(len(cards)) + ' cards, made by check_table.py',
           'Every table as stored; card, keyword, type and name-part ids are shown as names. Other ids join the tables.', '']
    for t in ORDER: out += table(t, got[t])
    open(out_path, 'w').write('\n'.join(out))

main()
