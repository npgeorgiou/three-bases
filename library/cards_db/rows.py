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

def compact(cid):
    """The card's rows on one line, for the line checks (SYNTAX.md): KW: keywords | WHEN event IF cond DO act who ... ; THEN ..."""
    parts = []
    kws = [nm(k) for (k,) in c.execute('select keyword from card_keyword where card=?', (cid,))]
    if kws: parts.append('KW: ' + ', '.join(kws))
    for aid, ev, lim in c.execute('select id, event, lim from ability where card=? order by seq', (cid,)):
        effs = []
        for link, act, on, to, zone, cr, kr, lasts, eid in c.execute(
                'select link, act, on_target, to_target, zone, card_ref, keyword_ref, lasts, id from effect where ability=? order by seq', (aid,)):
            ps = ', '.join(f'{p}={amount(a) if a else v}' for p, a, v in c.execute('select param, amount, value from param where effect=?', (eid,)))
            ref = ' '.join(x for x in (nm(cr) if cr else '', nm(kr) if kr else '') if x)
            e = ' '.join(x for x in (act, target(on), ('to ' + target(to)) if to else '', ('in ' + zone) if zone else '',
                                     f'<{ref}>' if ref else '', f'({ps})' if ps else '', ('for ' + lasts) if lasts else '') if x)
            effs.append(('OR ' if link == 'or' else 'THEN ' if effs else '') + e)
        cd = conds(aid)
        parts.append('WHEN ' + event(ev) + (f' [{lim}]' if lim else '') + (' IF ' + cd if cd else '') + ' DO ' + ' '.join(effs))
    return ' | '.join(parts) if parts else '(no rows)'


HEAD = """# How to read a card's rows (the line checks; made by `rows.py --syntax`, do not edit by hand)
Each card is printed on one line: `KW: <keywords> | WHEN ... IF ... DO ... | WHEN ...`. The card reading is done: judge lines by the rows only.
- `KW:` the card's keywords. What a keyword does is its own entry's rows, not repeated on the card.
- `WHEN <event> [by <actor>] [of <object>] [<limit>]`: one ability and what sets it off. `always` = on while its IF holds.
- `IF <test> ...`: conditions, joined by `;`. `event_count <event> ... ge 2 this_game` = the event happened 2+ times this game.
- `DO <act> <who> [to <who>] [in <zone>] <card or keyword it names> (numbers) [for <how long>]`: the effect. `THEN` = the next
  effect of the same ability; `OR` = a choice between effects.
- A who (target) is `[number] [pick] [side] [kind] [in zone] [filter]...`: `chosen mine unit` = a unit of mine the player
  picks; `all enemy unit`; `self` = the card itself; `it` = the target of the effect before. A filter is `[attr op value]`:
  `[card in Zed]` = the card named Zed; `[cost ge 6]` = cost 6 or more.
- Numbers: `power=1, health=1` (stats given); `amount=2`; `stat power of (self)` = my power.
Values below: field, value, meaning (vocab.tsv). Only values the database uses.
"""


def syntax():
    used = {'act': 'select distinct act from effect', 'event': 'select distinct event from event', 'test': 'select distinct test from cond',
            'pick': 'select distinct pick from target', 'side': 'select distinct side from target', 'kind': 'select distinct kind from target',
            'zone': 'select distinct zone from target', 'lasts': 'select distinct lasts from effect', 'attr': 'select distinct attr from filter',
            'op': 'select distinct op from filter', 'span': 'select distinct span from cond'}
    out = [HEAD]
    for f, q in used.items():
        vals = {v for (v,) in c.execute(q) if v}
        rows_ = [r for r in c.execute('select value, meaning from vocab where field=? order by value', (f,)) if r[0] in vals]
        if not rows_: continue
        out.append(f'\n**{f}**')
        out += [f'- `{v}`: {(m or "").split(". ")[0][:110]}' for v, m in rows_]
    open(os.path.join(HERE, 'SYNTAX.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')


if __name__ == '__main__':
    if sys.argv[1] == '--syntax': syntax(); sys.exit()
    if sys.argv[1] == '--random':
        random.seed(int(sys.argv[3]) if len(sys.argv) > 3 else 1)
        ids = [i for (i,) in c.execute("select a.card from ability a join card cd on cd.id=a.card where cd.is_keyword=0 group by a.card")]
        for i in random.sample(ids, int(sys.argv[2])): show(i)
    else:
        for a in sys.argv[1:]:
            ids = [int(a)] if a.isdigit() else [i for (i,) in c.execute('select id from card where name=? and is_stub=0', (a,))]
            for i in ids: show(i)
