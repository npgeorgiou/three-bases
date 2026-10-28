"""A card's rows in cards.sqlite, one table row per effect, with every id turned back into a name, as Markdown.
Usage: rows.py <card name or id> [...]   |   rows.py --random N [seed]"""
import os, random, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__))
import source
c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))
lib = source.lib()

def nm(i):
    r = c.execute('select name from card where id=?', (i,)).fetchone()
    return r[0] if r else str(i)

def amount(a):
    if a is None: return ''
    x, v, of, attr, ev, span, inner = c.execute('select x, value, of_target, attr, event, span, inner from amount where id=?', (a,)).fetchone()
    if x == 'n': return ('%g' % v)
    s = x + (' ' + attr if attr else '') + (' of (' + target(of) + ')' if of else '') + (' of (' + event(ev) + ')' if ev else '')
    s += (' ' + span if span else '') + (' (' + amount(inner) + ')' if inner else '')
    items = [amount(i) for (i,) in c.execute('select item from amount_item where amount=?', (a,))]
    return s + (' (' + ' + '.join(items) + ')' if items else '')

def target(t):
    if t is None: return ''
    kind, side, pick, n, zone, by = c.execute('select kind, side, pick, n, zone, by_attr from target where id=?', (t,)).fetchone()
    parts = [amount(n)] if n else []
    parts += [p for p in (pick, side, kind) if p]
    if by: parts.append('by ' + by)
    if zone: parts.append('in ' + zone)
    for attr, op, fn, rc, rk, rt, rw, val in c.execute('select attr, op, n, ref_card, ref_keyword, ref_type, ref_word, val from filter where target=?', (t,)):
        ref = nm(rc) if rc else nm(rk) if rk else (c.execute('select name from type where id=?', (rt,)).fetchone() or [''])[0] if rt else \
              (c.execute('select word from name_part where id=?', (rw,)).fetchone() or [''])[0] if rw else val if val else amount(fn)
        parts.append(f'[{attr} {op} {ref}]')
    return ' '.join(parts)

def event(e):
    if e is None: return ''
    ev, actor, obj = c.execute('select event, actor, object from event where id=?', (e,)).fetchone()
    return ev + (' by ' + target(actor) if actor else '') + (' of ' + target(obj) if obj else '')

def conds(aid):
    out = []
    for test, of, attr, op, n, span, ev, rk, val in c.execute('select test, of_target, attr, op, n, span, event, ref_keyword, value from cond where ability=?', (aid,)):
        out.append(' '.join(x for x in (test, nm(rk) if rk else '', amount(val) if val else '', target(of), event(ev), attr or '', op or '', amount(n), span or '') if x))
    return '; '.join(out)

def show(cid):
    name, text = lib.execute('select name, text from entities where id=?', (cid,)).fetchone()
    print(f'**{name}**\nCard text: "{" ".join((text or "").split())}"\n')
    kws = [nm(k) for (k,) in c.execute('select keyword from card_keyword where card=?', (cid,))]
    if kws: print('Keywords (their own rows are on the keyword entries): ' + ', '.join(kws) + '\n')
    rows = []
    for aid, ev, lim in c.execute('select id, event, lim from ability where card=? order by seq', (cid,)):
        for link, act, on, to, zone, cr, kr, tr, lasts, eid in c.execute(
                'select link, act, on_target, to_target, zone, card_ref, keyword_ref, type_ref, lasts, id from effect where ability=? order by seq', (aid,)):
            ps = ', '.join(f'{p}={amount(a) if a else v}' for p, a, v in c.execute('select param, amount, value from param where effect=?', (eid,)))
            ref = ' '.join(x for x in (nm(cr) if cr else '', nm(kr) if kr else '') if x)
            rows.append([event(ev) + (f' [{lim}]' if lim else ''), conds(aid), link or '', act, target(on) + (' to ' + target(to) if to else ''),
                         zone or '', ref, ps, lasts or ''])
    if not rows: print('(no rows of its own)\n'); return
    print('| when | if | link | what | who | where | card/keyword | numbers | lasts |\n|---|---|---|---|---|---|---|---|---|')
    for r in rows: print('| ' + ' | '.join(x.replace('|', '/') for x in r) + ' |')
    print()

if __name__ == '__main__':
    if sys.argv[1] == '--random':
        random.seed(int(sys.argv[3]) if len(sys.argv) > 3 else 1)
        ids = [i for (i,) in c.execute("select a.card from ability a join card cd on cd.id=a.card where cd.is_keyword=0 group by a.card")]
        for i in random.sample(ids, int(sys.argv[2])): show(i)
    else:
        for a in sys.argv[1:]:
            ids = [int(a)] if a.isdigit() else [i for (i,) in c.execute('select id from card where name=? and is_stub=0', (a,))]
            for i in ids: show(i)
