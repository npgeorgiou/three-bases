"""The query layer of cards.sqlite: every card's abilities in general terms, one row per trigger, condition and effect.
Rows come from the card's own abilities (origin own), abilities its effects give (gives), the keywords it has (has_keyword:
Tough on Malphite) and the keywords its effects give or use (uses_keyword: Frostbite used by Ashe, acting on Ashe's target).
Amounts that count or compare things ("for each Celestial card you played", "different subtypes") become condition rows too.
Each row carries its concept-tree concept, so searches run on mechanics, not on keyword names.
  flat_when(card, origin, via, ability, event, concept, actor_kind, actor_side, actor_pick, obj_kind, obj_side, obj_pick, lim, obj_with)
  flat_if(card, origin, via, ability, test, event, concept, of_kind, of_side, of_pick, of_zone, of_with, ev_obj_kind, ev_obj_side,
          ev_obj_with, op, n, span)
  flat_do(card, origin, via, ability, seq, act, concept, on_kind, on_side, on_pick, on_zone, card_ref, keyword_ref, lasts, link,
          on_with, param_event, params, eff_zone)
*_with: a target's filters as 'attr op value' joined by ';' (values are vocab values or ids). Called by load.py."""

SCHEMA = """
create table flat_when(card integer, origin text, via integer, ability integer, event text, concept text, actor_kind text,
  actor_side text, actor_pick text, obj_kind text, obj_side text, obj_pick text, lim text, obj_with text);
create table flat_if(card integer, origin text, via integer, ability integer, test text, event text, concept text, of_kind text,
  of_side text, of_pick text, of_zone text, of_with text, ev_obj_kind text, ev_obj_side text, ev_obj_with text, op text, n real, span text);
create table flat_do(card integer, origin text, via integer, ability integer, seq integer, act text, concept text, on_kind text,
  on_side text, on_pick text, on_zone text, card_ref integer, keyword_ref integer, lasts text, link text, on_with text,
  param_event text, params text, eff_zone text);
create table flat_concept(card integer, concept text, rule text);
create index fw on flat_when(event); create index fd on flat_do(act); create index fi on flat_if(test, event);
create index fwc on flat_when(card); create index fdc on flat_do(card); create index fic on flat_if(card);
"""


def build(c):
    c.executescript(SCHEMA)
    tree = {(f, v): t for f, v, t in c.execute('select field, value, tree from vocab')}
    kwname = {i: n for i, n in c.execute('select id, name from card where is_keyword=1')}
    tgt = lambda t: c.execute('select kind, side, pick, zone from target where id=?', (t,)).fetchone() if t else (None,) * 4

    def withs(t):
        if not t: return None
        parts = [f'{a} {o} {rk or rt or rc or rw or v or n}' for a, o, rk, rt, rc, rw, v, n in
                 c.execute('select attr, op, ref_keyword, ref_type, ref_card, ref_word, val, n from filter where target=?', (t,))]
        return ';'.join(parts) or None

    num = lambda a: (c.execute("select value from amount where id=? and x='n'", (a,)).fetchone() or [None])[0] if a else None

    def event_info(ev):
        if not ev: return (None,) * 6
        e, actor, obj = c.execute('select event, actor, object from event where id=?', (ev,)).fetchone()
        ok, os_, op, _ = tgt(obj)
        return e, ok, os_, op, withs(obj), actor

    def when_concept(e, okind, owith, opick):
        if e in ('played', 'spell_resolves') and (okind == 'spell' or 'spell' in (owith or '')): return 'on_spell'
        if e in ('summoned', 'played') and opick != 'self' and okind == 'unit': return 'on_ally_play'
        return tree.get(('event', e))

    def amounts(aid):
        """amount ids used by an ability's conditions and effect params and targets (one level, then inner and items)"""
        todo = [a for (a,) in c.execute('select n from cond where ability=? union select value from cond where ability=? union '
                                        'select p.amount from param p join effect e on e.id=p.effect where e.ability=? union '
                                        'select t.n from target t join effect e on t.id=e.on_target where e.ability=?', (aid,) * 4) if a]
        seen = set()
        while todo:
            a = todo.pop()
            if a in seen: continue
            seen.add(a)
            r = c.execute('select inner from amount where id=?', (a,)).fetchone()
            if r and r[0]: todo.append(r[0])
            todo += [i for (i,) in c.execute('select item from amount_item where amount=?', (a,))]
        return seen

    def ability_rows(card, aid, origin, via, applied_to=None, seen=()):
        ev, lim = c.execute('select event, lim from ability where id=?', (aid,)).fetchone()
        if ev:
            e, ok, os_, op, ow, actor = event_info(ev); ak, as_, ap, _ = tgt(actor)
            c.execute('insert into flat_when values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                      (card, origin, via, aid, e, when_concept(e, ok, ow, op), ak, as_, ap, ok, os_, op, lim, ow))
        for test, of, op, n, span, cev in c.execute('select test, of_target, op, n, span, event from cond where ability=?', (aid,)).fetchall():
            k, s, p, z = tgt(of); e, ek, es, _, ew, _ = event_info(cev)
            c.execute('insert into flat_if values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                      (card, origin, via, aid, test, e, (when_concept(e, ek, ew, None) if e else None) or tree.get(('test', test)),
                       k, s, p, z, withs(of), ek, es, ew, op, num(n), span))
        for a in amounts(aid):  # counted things: "for each X", "different subtypes", "equal to its Power"
            x, of, cev, span = c.execute('select x, of_target, event, span from amount where id=?', (a,)).fetchone()
            if x == 'n': continue
            k, s, p, z = tgt(of); e, ek, es, _, ew, _ = event_info(cev)
            c.execute('insert into flat_if values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                      (card, origin, via, aid, 'amount_' + x, e, tree.get(('x', x)) or (when_concept(e, ek, ew, None) if e else None),
                       k, s, p, z, withs(of), ek, es, ew, None, None, span))
        for eid, seq, act, on, cref, kref, lasts, link, ez in c.execute(
                'select id, seq, act, on_target, card_ref, keyword_ref, lasts, link, zone from effect where ability=? order by seq', (aid,)).fetchall():
            k, s, p, z = tgt(on); w = withs(on)
            if applied_to and (p in ('self', 'it') or (k, s, p) == (None, None, None)): k, s, p, z, w = applied_to
            pe = (c.execute("select value from param where effect=? and param='event'", (eid,)).fetchone() or [None])[0]
            ps = ';'.join(f'{pn}={num(a) if a else v}' for pn, a, v in c.execute('select param, amount, value from param where effect=?', (eid,))) or None
            concept = (tree.get(('keyword', kwname.get(kref, ''))) if kref else None) or tree.get(('act', act))
            c.execute('insert into flat_do values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                      (card, origin, via, aid, seq, act, concept, k, s, p, z, cref, kref, lasts, link, w, pe, ps, ez))
            if kref and act in ('keyword_action', 'give_keyword') and kref not in seen:  # the keyword's meaning on this target
                for (kab,) in c.execute('select id from ability where card=? and given_by_effect is null', (kref,)).fetchall():
                    ability_rows(card, kab, 'uses_keyword', kref, applied_to=(k, s, p, z, w), seen=tuple(seen) + (kref,))
            for (sub,) in c.execute('select id from ability where given_by_effect=?', (eid,)).fetchall():  # abilities this effect gives
                ability_rows(card, sub, 'gives', eid, seen=seen)

    def keyword_conds(card, kw, aid, origin):
        for test, of, op, n, span, cev in c.execute('select test, of_target, op, n, span, event from cond where keyword=?', (kw,)).fetchall():
            k, s, p, z = tgt(of); e, ek, es, _, ew, _ = event_info(cev)
            c.execute('insert into flat_if values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                      (card, origin, kw, aid, test, e, (when_concept(e, ek, ew, None) if e else None) or tree.get(('test', test)),
                       k, s, p, z, withs(of), ek, es, ew, op, num(n), span))

    for (card,) in c.execute('select id from card').fetchall():
        for (aid,) in c.execute('select id from ability where card=? and given_by_effect is null', (card,)).fetchall():
            ability_rows(card, aid, 'own', None)
        for (kw,) in c.execute('select keyword from card_keyword where card=?', (card,)).fetchall():
            for (aid,) in c.execute('select id from ability where card=? and given_by_effect is null', (kw,)).fetchall():
                ability_rows(card, aid, 'has_keyword', kw)
            keyword_conds(card, kw, None, 'has_keyword')
    for card, aid, kw in c.execute("select a.card, a.id, cd.ref_keyword from cond cd join ability a on a.id=cd.ability "
                                   "where cd.test='keyword_condition' and cd.ref_keyword is not null").fetchall():
        keyword_conds(card, kw, aid, 'uses_keyword')


# Concepts derived from the shape of a row (Claude's rules from the concept tree's definitions, 28 Oct 2026). Each rule: concept,
# table, SQL condition on that table. A card gets the concept when any of its rows matches.
RULES = [
    ('permanent_growth', 'flat_do', "act='stat_change' and on_pick='self' and lasts in ('permanent','while') and params not like '%=-%'"),
    ('temporary_buff', 'flat_do', "act='stat_change' and lasts='this_round' and coalesce(on_side,'mine')!='enemy' and params not like '%=-%'"),
    ('stat_loss', 'flat_do', "(act='stat_change' and params like '%=-%') or (act='stat_set' and on_side='enemy')"),
    ('aoe_damage', 'flat_do', "act='damage' and on_pick='all'"),
    ('direct_damage', 'flat_do', "act in ('damage','excess_damage') and on_kind in ('player','any')"),
    ('ping', 'flat_do', "act='damage' and params like 'amount=1.0%'"),
    ('self_destruct', 'flat_do', "act='kill' and on_pick='self'"),
    ('sacrifice', 'flat_do', "act='kill' and on_side='mine' and coalesce(on_pick,'')!='self'"),
    ('evasion', 'flat_do', "act='cant' and param_event='blocks' and on_side='enemy'"),
    ('cant_block', 'flat_do', "act='cant' and param_event='blocks' and on_pick='self'"),
    ('cant_attack', 'flat_do', "act='cant' and param_event='attacks'"),
    ('bounce_enemy', 'flat_do', "act='return_to_hand' and on_side='enemy'"),
    ('polymorph', 'flat_do', "act='transform' and on_side='enemy'"),
    ('information', 'flat_do', "act in ('reveal','look')"),
    ('random_effect', 'flat_do', "on_pick='random' or act='give_random_keyword'"),
    ('junk_cards', 'flat_do', "act in ('create','keyword_action') and on_side='enemy' and coalesce(on_zone,eff_zone,'') in ('deck','hand','deck_top')"),
    ('hand_disruption', 'flat_do', "act in ('discard','obliterate','steal','draw') and on_side='enemy' and coalesce(on_zone,'') in ('hand','deck','deck_bottom')"),
    ('cost_increase', 'flat_do', "act='cost_change' and params like 'cost=%' and params not like 'cost=-%' and on_side='enemy'"),
    ('aura', 'flat_do', "origin in ('own','has_keyword') and act in ('stat_change','give_keyword') and on_pick='all' and lasts in ('while','permanent') and ability in (select a.id from ability a join event v on v.id=a.event where v.event='always')"),
    ('tribal', 'flat_do', "on_with like '%type is%' or on_with like '%name_has%'"),
    ('tribal', 'flat_when', "obj_with like '%type is%' or obj_with like '%name_has%'"),
    ('variable_stats', 'flat_do', "act='stat_change' and on_pick='self' and params like '%=None%'"),
    ('death_count', 'flat_if', "event='dies' and test in ('event_count','amount_event_count','amount_count')"),
    ('combo_sequence', 'flat_if', "test='first_card' or (event='played' and span in ('this_round','last_round'))"),
    ('adjacency', 'flat_do', "on_pick in ('right_of_self','left_of_self')"),
    ('movement', 'flat_do', "act in ('swap','move') and coalesce(on_zone,eff_zone,'board')='board'"),
    ('board_presence', 'flat_if', "test in ('count','amount_count') and of_zone='board' and of_side='mine'"),
    ('count_payoff', 'flat_if', "test in ('amount_count','amount_event_count')"),
    ('removal', 'flat_do', "act in ('kill','obliterate','capture') and on_side in ('enemy','any')"),
]


def derive(c):
    """flat_concept: concepts of the rows themselves, the keywords' concepts, and the shape rules above."""
    c.execute("insert into flat_concept select distinct card, concept, 'row' from flat_do where concept is not null and concept!=''")
    c.execute("insert into flat_concept select distinct card, concept, 'row' from flat_when where concept is not null and concept!=''")
    c.execute("insert into flat_concept select distinct card, concept, 'row' from flat_if where concept is not null and concept!=''")
    c.execute("insert into flat_concept select distinct ck.card, v.tree, 'keyword' from card_keyword ck join card k on k.id=ck.keyword "
              "join vocab v on v.field='keyword' and v.value=k.name where v.tree!=''")
    for concept, table, cond in RULES:
        c.execute(f"insert into flat_concept select distinct card, ?, ? from {table} where {cond}", (concept, 'rule ' + concept))
