"""Questions over cards.sqlite.
  queries.py feeds <card name>        cards whose abilities are set off by what this card's effects cause (same player)
  queries.py fed_by <card name>       cards whose effects cause what this card's abilities wait for
  queries.py event <event>            cards that cause the event, and cards that wait for it
  queries.py same <card name>         cards with an effect of the same act on the same kind and side (compare cost and stats)
A connection needs: the effect's act causes the event (table causes), the effect's target and the event's object agree on
kind and side, and an event that is about the card itself (pick self) only connects to that same card."""
import os, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__))
c = sqlite3.connect(os.path.join(HERE, 'cards.sqlite'))

def agree(a, b):
    return a is None or b is None or a == b or 'any' in (a, b)

def target(tid):
    return c.execute('select kind, side, pick from target where id=?', (tid,)).fetchone() if tid else (None, None, None)

def results():
    """(card, ability, effect, act, event, kind, side, pick, via card) for every effect, including effects of cards it creates."""
    out = []
    for cid, aid, eid, act, on, ref, kw in c.execute('select a.card, a.id, e.id, e.act, e.on_target, e.card_ref, e.keyword_ref from effect e join ability a on a.id=e.ability'):
        k, s, p = target(on)
        acts = [act]
        if act in ('keyword_action', 'give_keyword') and kw:  # a keyword used or given causes what the keyword's own record does
            acts += [a for (a,) in c.execute('select e2.act from effect e2 join ability a2 on a2.id=e2.ability where a2.card=?', (kw,))]
        for a in acts:
            for (ev,) in c.execute('select event from causes where act=?', (a,)): out.append((cid, aid, eid, a, ev, k, s, p, cid))
        if ref and act in ('create', 'summon'):
            for cid2, aid2, eid2, act2, on2 in c.execute('select a.card, a.id, e.id, e.act, e.on_target from effect e join ability a on a.id=e.ability where a.card=?', (ref,)):
                k2, s2, p2 = target(on2)
                for (ev,) in c.execute('select event from causes where act=?', (act2,)): out.append((cid, aid2, eid2, act2, ev, k2, s2, p2, ref))
    return out

def waiters():
    out = []
    for cid, aid, ev, actor, obj in c.execute('select a.card, a.id, v.event, v.actor, v.object from ability a join event v on v.id=a.event'):
        out.append((cid, aid, ev, target(actor), target(obj)))
    return out

def connect(src=None, dst=None):
    W = waiters(); seen = set()
    for cid, aid, eid, act, ev, k, s, p, via in results():
        if src and cid != src: continue
        for wc, wa, wev, actor, obj in W:
            if wev != ev or (dst and wc != dst): continue
            ok, os_, op = obj
            if op == 'self' and wc != cid and wc != via: continue
            if actor[2] == 'self' and wc != cid: continue
            if not agree(k, ok) or not agree(s, os_): continue
            key = (cid, via, act, ev, wc)
            if key in seen: continue
            seen.add(key); yield key

def name(i): return c.execute('select name from card where id=?', (i,)).fetchone()[0]
def ids(n): return [r[0] for r in c.execute('select id from card where lower(name)=lower(?) and is_keyword=0', (n,))]

if __name__ == '__main__':
    cmd, arg = sys.argv[1], ' '.join(sys.argv[2:])
    if cmd in ('feeds', 'fed_by'):
        for i in ids(arg):
            for cid, via, act, ev, wc in (connect(src=i) if cmd == 'feeds' else connect(dst=i)):
                print(f'{name(cid)}{" (via " + name(via) + ")" if via != cid else ""} --{act}->{ev}--> {name(wc)}')
    elif cmd == 'event':
        print('cause it:', sorted({name(r[0]) for r in results() if r[4] == arg}))
        print('wait for it:', sorted({name(w[0]) for w in waiters() if w[2] == arg}))
    elif cmd == 'same':
        for i in ids(arg):
            for act, k, s in c.execute('select e.act, t.kind, t.side from effect e join ability a on a.id=e.ability left join target t on t.id=e.on_target where a.card=?', (i,)):
                rows = c.execute('select distinct cd.name, cd.cost, cd.power, cd.health from effect e join ability a on a.id=e.ability join card cd on cd.id=a.card '
                                 'left join target t on t.id=e.on_target where e.act=? and t.kind is ? and t.side is ? and a.card!=? order by cd.cost limit 15', (act, k, s, i)).fetchall()
                print(act, k, s, '->', rows)
