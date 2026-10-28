"""How one card can set off another, from the query layer (flat_*), for combo searches and the combo tests.
explain(c, enabler, payoff) -> a short description of the most direct connection, or '' if none (reasons() lists all, ranked:
  makes; the enabler is what the payoff waits for; a direct event on another unit; a keyword or type asked for; a condition;
  a happening the payoff counts or picks things by (flat_ref); the same through a card the enabler makes; an event on the
  payoff itself (killing it for its Last Breath); a zone):
  makes      the enabler (or a card it makes) creates, summons or generates the payoff
  event      an effect of the enabler (or of a card it makes) causes an event (table causes) that a trigger or a condition of the
             payoff waits for, on a matching side
  keyword    the enabler makes or gives units with a keyword or type that the payoff's trigger or condition asks for
Sides are compared from the same player's view: 'mine' must not meet 'enemy'; 'any' or empty fits everything."""

def ids(c, name):
    return [i for (i,) in c.execute('select id from card where lower(name)=lower(?) and is_keyword=0', (name.strip(),))]

def agree(a, b):
    return not a or not b or a == b or 'any' in (a, b)

KWC = {}

def kw_concept(c, k):
    if k is None: return None
    if k not in KWC:
        r = c.execute("select v.tree from card k join vocab v on v.field='keyword' and v.value=coalesce((select s.value from vocab s where s.field='keyword' and s.value=k.game || ':' || k.name), k.name) where k.id=?", (k,)).fetchone()
        KWC[k] = (r[0] if r and r[0] else None) or f'keyword {k}'
    return KWC[k]

def same_kw(c, a, b):
    """the same keyword (combos are found inside one game only)"""
    return a is None or b is None or a == b

def narrow_ok(want, have, c=None):
    """the payoff asks for a specific card, type or keyword ('card is 123'): the enabler's target must name the same one
    (a keyword: the same one or one of the same concept)"""
    asks = [p for p in (want or '').split(';') if p.split(' ')[:2] in (['card', 'is'], ['type', 'is'], ['keyword', 'is'])]
    hk = [int(p.split(' ')[2]) for p in (have or '').split(';') if p.startswith('keyword is ') and p.split(' ')[2].isdigit()]
    if c is not None:  # a state a keyword gives ("state is stunned"): the enabler must give that keyword or one of its concept
        for p in (want or '').split(';'):
            bits = p.split(' ')
            if bits[:2] == ['state', 'is'] and len(bits) == 3:
                r = c.execute("select substr(causes, 15) from vocab where field='state' and value=? and causes like 'given_keyword:%'",
                              (bits[2],)).fetchone()
                if r and hk and not any((c.execute('select lower(name) from card where id=?', (k,)).fetchone() or [''])[0] == r[0].lower()
                                        for k in hk): return False
    for a in asks:
        if a in (have or ''): continue
        bits = a.split(' ')
        if c is not None and bits[0] == 'keyword' and bits[2].isdigit() and any(same_kw(c, int(bits[2]), k) for k in hk): continue
        return False
    return True

def made_by(c, card, depth=2):
    """cards a card creates, summons or generates (a few steps deep), including itself"""
    out, todo = {card}, [card]
    for _ in range(depth):
        nxt = []
        for x in todo:
            for (r,) in c.execute("select card_ref from flat_do where card=? and card_ref is not null and act in ('create','summon','copy','transform','play_card')", (x,)):
                if r not in out: out.add(r); nxt.append(r)
            for (r,) in c.execute("select dst from card_link where src=? and rel in ('generates','transforms_into')", (x,)):
                if r not in out: out.add(r); nxt.append(r)
        todo = nxt
    return out

def explain(c, enabler, payoff):
    best = min(reasons(c, enabler, payoff), default=None)
    return best[1] if best else ''

def reasons(c, enabler, payoff):
    for e in ids(c, enabler):
        for p in ids(c, payoff):
            if c.execute('select game from card where id=?', (e,)).fetchone() != c.execute('select game from card where id=?', (p,)).fetchone():
                continue  # each game is its own world: no combos across games
            makers = made_by(c, e)
            if p in makers and p != e: yield (0, 'makes')
            # the enabler itself being played or summoned is what the payoff waits for (spells for spell payoffs, units for summon payoffs)
            cat = (c.execute('select category from card where id=?', (e,)).fetchone() or [''])[0]
            for ev, ok, oside, owith in c.execute("select event, obj_kind, obj_side, obj_with from flat_when where card=? and event in ('played','summoned') "
                                                  "and coalesce(obj_pick,'')!='self'", (p,)).fetchall():
                if (ev == 'played' and cat == 'spell' and (ok == 'spell' or 'spell' in (owith or ''))) or \
                   (ev in ('summoned', 'played') and cat in ('unit', 'hero') and ok == 'unit' and agree(oside, 'mine')):
                    yield (1, f'is: playing {name(c, e)} is a {ev} the payoff waits for')
            for ev, owith in c.execute("select event, of_kind from flat_if where card=? and event in ('played','summoned')", (p,)).fetchall():
                if ev == 'played' and cat == 'spell': yield (2, 'is: counted as a played spell')
            for m in makers:
                for act, side, kind, kref, cref, onw in c.execute('select act, on_side, on_kind, keyword_ref, card_ref, on_with from flat_do where card=?', (m,)).fetchall():
                    # what the effect itself carries: the keyword it gives or uses (a stun is the keyword Stun)
                    kid = kref or (c.execute("select id from card where is_keyword=1 and lower(name)=?", (act,)).fetchone() or [None])[0]
                    if kid: onw = (onw or '') + f';keyword is {kid}'
                    for (ev,) in c.execute('select event from causes where act=?', (act,)).fetchall():
                        for oside, opick, ow in c.execute('select obj_side, obj_pick, obj_with from flat_when where card=? and event=?', (p, ev)).fetchall():
                            if opick == 'self' and m != p and not (side in ('mine', 'any', None) and kind in ('unit', 'any', None)): continue
                            if not narrow_ok(ow, onw, c): continue
                            if agree(side, oside): yield ((7 if opick == 'self' else 5 if m != e else 3), f'event: {act} -> {ev}' + (f' (via {name(c, m)})' if m != e else ''))
                        for oside, ow in c.execute('select ev_obj_side, ev_obj_with from flat_if where card=? and event=?', (p, ev)).fetchall():
                            if agree(side, oside) and narrow_ok(ow, onw, c): yield ((6 if m != e else 4), f'condition: {act} -> {ev}' + (f' (via {name(c, m)})' if m != e else ''))
            # a happening the enabler makes that the payoff counts or picks things by (flat_ref: condition, state)
            made = {(h, sd, k) for x in makers for h, sd, k in c.execute("select happening, side, keyword from flat_ref where card=? and role='makes'", (x,))}
            for h, sd, role, k in c.execute("select happening, side, role, keyword from flat_ref where card=? and role in ('condition','state')", (p,)).fetchall():
                if any(h == mh and agree(ms, sd) and same_kw(c, k, mk) for mh, ms, mk in made): yield (6, f'{role}: {h}')
            # keyword or type the payoff asks for, carried by what the enabler makes or gives
            kw_have = {k for x in makers for (k,) in c.execute('select keyword from card_keyword where card=?', (x,))}
            kw_have |= {k for x in makers for (k,) in c.execute("select keyword_ref from flat_do where card=? and act='give_keyword' and keyword_ref is not null", (x,))}
            ty_have = {t for x in makers for (t,) in c.execute('select type from card_type where card=?', (x,))}
            for x in makers:  # cards made by description ("a random Celestial card") carry their type filter
                for (w,) in c.execute("select on_with from flat_do where card=? and act in ('create','summon','choose_card') and on_with like '%type is%'", (x,)):
                    ty_have |= {int(p.split(' ')[2]) for p in w.split(';') if p.startswith('type is ') and p.split(' ')[2].lstrip('-').isdigit()}
            # emptying or filling a zone that the payoff counts (discarding empties the hand)
            zones = {z for x in makers for (z,) in c.execute("select coalesce(on_zone, eff_zone) from flat_do where card=? and act in "
                                                             "('discard','draw','create','obliterate','play_card','shuffle_into_deck')", (x,)) if z}
            for (z,) in c.execute("select of_zone from flat_if where card=? and test in ('count','have','amount_count') and of_zone is not null", (p,)):
                if z in zones: yield (8, f'zone: {z}')
            asks = [w for (w,) in c.execute('select obj_with from flat_when where card=? and obj_with is not null', (p,))]
            asks += [w for (w,) in c.execute('select coalesce(ev_obj_with, of_with) from flat_if where card=? and coalesce(ev_obj_with, of_with) is not null', (p,))]
            asks += [w for (w,) in c.execute("select f.attr || ' is ' || coalesce(f.ref_keyword, f.ref_type) from cond cd join ability a on a.id=cd.ability "
                                             "join filter f on f.target=cd.of_target where a.card=? and f.attr in ('keyword','type')", (p,))]
            # a keyword or type the payoff's effects pick their targets by (Moonlit Aerie: strength to friendly Satyrs)
            targets = [w for (w,) in c.execute("select on_with from flat_do where card=? and on_with is not null and coalesce(on_side,'') in ('mine','any','')", (p,))]
            targets += [w for (w,) in c.execute("select to_with from flat_do where card=? and to_with is not null", (p,))]
            for w in targets:
                for part in w.split(';'):
                    bits = part.removeprefix('of:').split(' ')
                    if len(bits) == 3 and bits[1] in ('is', 'in') and bits[2].lstrip('-').isdigit():
                        v = int(bits[2])
                        if bits[0] == 'type' and v in ty_have: yield (9, 'target: type ' + (c.execute('select name from type where id=?', (v,)).fetchone() or ['?'])[0])
                        if bits[0] == 'keyword' and any(same_kw(c, v, k) for k in kw_have): yield (9, f'target: keyword {name(c, v)}')
            # what the enabler puts in play or gains that the payoff counts (Excited Mousers: friendly units; Lady Rime: mana)
            MAKES_KIND = {'summon': 'unit', 'revive': 'unit', 'play_card': 'unit', 'mana_gain': 'mana', 'create': 'card', 'draw': 'card'}
            made_kinds = {MAKES_KIND[a] for x in makers for (a,) in c.execute('select act from flat_do where card=?', (x,)) if a in MAKES_KIND}
            made_kinds |= {'landmark' for x in makers if (c.execute('select category from card where id=?', (x,)).fetchone() or [''])[0] == 'building'}
            for k, sd in c.execute("select of_kind, of_side from flat_if where card=? and test in ('count','have','amount_count')", (p,)).fetchall():
                if k in made_kinds and agree(sd, 'mine'): yield (8, f'count: {k}')
            if any('of:kind is landmark' in w for w in targets) and 'landmark' in made_kinds: yield (9, 'target: next to a structure')
            for k, sd in c.execute("select on_kind, on_side from flat_do where card=? and on_kind in ('landmark','unit_or_structure')", (p,)).fetchall():
                if 'landmark' in made_kinds and agree(sd, 'mine'): yield (9, 'target: structure')
            for w in asks:
                for part in w.split(';'):
                    bits = part.removeprefix('of:').split(' ')
                    if len(bits) == 3 and bits[1] in ('is', 'in') and bits[2].lstrip('-').isdigit():
                        v = int(bits[2])
                        if bits[0] == 'keyword' and any(same_kw(c, v, k) for k in kw_have): yield (4, f'keyword: {name(c, v)}')
                        if bits[0] == 'type' and v in ty_have: yield (4, 'type: ' + (c.execute('select name from type where id=?', (v,)).fetchone() or ['?'])[0])

def name(c, i):
    return (c.execute('select name from card where id=?', (i,)).fetchone() or ['?'])[0]
