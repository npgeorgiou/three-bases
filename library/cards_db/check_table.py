"""Kaptain's check file: for each chosen card, one line with its name and text, then its stored rows (one row per effect). Columns are the stored fields; links to cards, keywords, types and name parts are shown as names; a target, event,
condition or amount that an effect points to is written out in place as field=value pairs (its stored fields, no prose).
Usage: check_table.py <out.md> <card id> [...]     or     check_table.py <out.md> --random <game> <n>"""
import os, random, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import source
c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))
TEXT = {i: ' '.join((t or '').split()) for i, t in source.lib().execute('select id, text from entities')}
COLS = ['ability', 'when_event', 'when_actor', 'when_object', 'when_limit', 'if', 'effect', 'act', 'on', 'to', 'zone',
        'card', 'keyword', 'type', 'params', 'lasts', 'link']

def name(table, i):
    if i is None: return None
    r = c.execute(f"select {'word' if table == 'name_part' else 'name'} from {table} where id=?", (i,)).fetchone()
    return r[0] if r else f'?{i}'

def pairs(d):
    return ' '.join(f'{k}={v}' for k, v in d.items() if v not in (None, ''))

def target(t):
    if t is None: return ''
    r = c.execute('select kind, side, pick, n, zone, by_attr from target where id=?', (t,)).fetchone()
    s = pairs({'kind': r[0], 'side': r[1], 'pick': r[2], 'n': amount(r[3]) if r[3] else None, 'zone': r[4], 'by': r[5]})
    fs = []
    for attr, op, n, rc, rk, rt, rw, val, of in c.execute('select attr, op, n, ref_card, ref_keyword, ref_type, ref_word, val, of_target '
                                                           'from filter where target=?', (t,)).fetchall():
        v = name('card', rc) or name('card', rk) or name('type', rt) or name('name_part', rw) or val or (amount(n) if n else '')
        fs.append(f'{attr} {op} {v}' + (f' of ({target(of)})' if of else ''))
    return s + (' with[' + '; '.join(fs) + ']' if fs else '')

def event(e):
    if e is None: return ''
    ev, a, o = c.execute('select event, actor, object from event where id=?', (e,)).fetchone()
    return pairs({'event': ev, 'actor': f'({target(a)})' if a else None, 'object': f'({target(o)})' if o else None})

def amount(a):
    if a is None: return ''
    x, v, of, attr, ev, span, inner = c.execute('select x, value, of_target, attr, event, span, inner from amount where id=?', (a,)).fetchone()
    if x == 'n': return f'{v:g}'
    items = [amount(i) for (i,) in c.execute('select item from amount_item where amount=?', (a,))]
    return '{' + pairs({'x': x, 'value': f'{v:g}' if v is not None else None, 'of': f'({target(of)})' if of else None, 'attr': attr,
                        'event': f'({event(ev)})' if ev else None, 'span': span, 'inner': amount(inner) if inner else None,
                        'items': ', '.join(items) if items else None}) + '}'

def conds(ab):
    out = []
    for kw, test, of, attr, op, n, span, ev, rk, val in c.execute(
            'select keyword, test, of_target, attr, op, n, span, event, ref_keyword, value from cond where ability=?', (ab,)):
        out.append('(' + pairs({'test': test, 'keyword': name('card', kw), 'of': f'({target(of)})' if of else None, 'attr': attr,
                                'op': op, 'n': amount(n) if n else None, 'span': span, 'event': f'({event(ev)})' if ev else None,
                                'ref': name('card', rk), 'value': amount(val) if val else None}) + ')')
    return ' and '.join(out)

def ability_rows(ab, label):
    seq, ev, lim = c.execute('select seq, event, lim from ability where id=?', (ab,)).fetchone()
    e = c.execute('select event, actor, object from event where id=?', (ev,)).fetchone() if ev else (None, None, None)
    head = {'ability': label, 'when_event': e[0], 'when_actor': target(e[1]), 'when_object': target(e[2]), 'when_limit': lim, 'if': conds(ab)}
    rows = []
    for eid, eseq, act, on, to, zone, cr, kr, tr, lasts, link in c.execute(
            'select id, seq, act, on_target, to_target, zone, card_ref, keyword_ref, type_ref, lasts, link from effect where ability=? order by seq', (ab,)).fetchall():
        ps = '; '.join(f'{p}={amount(a) if a else v}' for p, a, v in c.execute('select param, amount, value from param where effect=?', (eid,)))
        rows.append({**head, 'effect': eseq, 'act': act, 'on': target(on), 'to': target(to), 'zone': zone, 'card': name('card', cr),
                     'keyword': name('card', kr), 'type': name('type', tr), 'params': ps, 'lasts': lasts, 'link': link})
        for k, (sub,) in enumerate(c.execute('select id from ability where given_by_effect=? order by seq', (eid,)).fetchall(), 1):
            rows += ability_rows(sub, f'{label}.{eseq}.{k} (given by effect {eseq})')
    return rows or [head]

def main():
    out_path, args = sys.argv[1], sys.argv[2:]
    if args[0] == '--random':
        ids = [i for (i,) in c.execute('select distinct k.id from card k join ability a on a.card=k.id where k.game=? and k.is_keyword=0 '
                                       'and k.is_stub=0', (args[1],))]  # cards with rows: a card with no text has nothing to check
        random.seed(); cards = random.sample(ids, int(args[2]))
    else: cards = [int(a) for a in args]
    cell = lambda v: '' if v is None else str(v).replace('|', '/')
    head = ['| ' + ' | '.join(COLS) + ' |', '|' + '---|' * len(COLS)]
    out = [f'# Stored rows of {len(cards)} cards (check_table.py)', '',
           'Each card: its name and text on one line, then its stored rows, one row per effect, then the rows of each keyword it has.',
           '- ability: one numbered "when -> if -> do" unit of the card. Rows with the same ability number are one ability; they '
           'happen together, in effect order.',
           '- effect: the step inside the ability. link says how a step joins the step before it: and = also; then = after it, '
           'using its result; if_done = only if it happened; or = instead (a choice); instead = replaces it.',
           '- pick=it in a target = the thing the step before acted on (the drawn card, the summoned unit, the chosen enemy).',
           '- A row labelled "keyword X" is what keyword X does; the card has it, so the card does it too.',
           '- Targets, events, conditions and amounts are written in place as their stored fields.', '']
    for cid in cards:
        nm = name('card', cid)
        kws = ', '.join(name('card', k) for (k,) in c.execute('select keyword from card_keyword where card=?', (cid,)))
        out.append(f'**{nm}**: {TEXT.get(cid, "")}' + (f' (keywords: {kws})' if kws else ''))
        out.append('')
        abs_ = c.execute('select id, seq from ability where card=? and given_by_effect is null order by seq', (cid,)).fetchall()
        rows = [r for ab, seq in abs_ for r in ability_rows(ab, str(seq))]
        for (k,) in c.execute('select keyword from card_keyword where card=?', (cid,)).fetchall():
            kn = name('card', k); kab = c.execute('select id, seq from ability where card=? and given_by_effect is null order by seq', (k,)).fetchall()
            trig = c.execute('select e.event from keyword_trigger t join event e on e.id=t.event where t.keyword=?', (k,)).fetchone()
            rows += [r for ab, seq in kab for r in ability_rows(ab, f'keyword {kn}: {seq}')]
            if not kab: rows.append({'ability': f'keyword {kn}', 'act': f'(a trigger label: event {trig[0]})' if trig else '(no rows: speed, type or reminder keyword)'})
        out += head + ['| ' + ' | '.join(cell(r.get(k)) for k in COLS) + ' |' for r in rows] if rows else ['(no rows stored)']
        out.append('')
    open(out_path, 'w').write('\n'.join(out) + '\n')

main()
