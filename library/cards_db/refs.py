"""flat_ref: every way a card works with a happening, one row each, so one query finds all cards that care about it.
A happening is an `event` value from vocab.tsv (dies, summoned, damaged, given_keyword, stat_changed, ...). Roles:
  makes      an effect of the card causes it (vocab `causes` of the act), to the effect's target
  trigger    an ability waits for it (flat_when)
  condition  a condition or a counted amount tests that it happened (flat_if with an event)
  state      a target, condition or count picks things it happened to: a state filter whose vocab `causes` names it
             (dead_this_round -> dies), or units in the discard zone (zone discard `causes` dies; units only)
kind/side/pick: the thing it happens to (the event's object, else its actor; for makes the effect's target). side '' = not
limited (either side). keyword: the keyword given or used, when the happening is about one (given_keyword Stun).
Payoff question ("cards that benefit from allies dying"):
  select distinct card from flat_ref where happening='dies' and role!='makes' and side in ('mine','any','')
Called by load.py after flat.build."""
import re

SCHEMA = """create table flat_ref(card integer, origin text, via integer, ability integer, role text, happening text,
  kind text, side text, pick text, keyword integer);
create index frh on flat_ref(happening, role); create index frc on flat_ref(card);"""


def build(c):
    c.executescript(SCHEMA)
    kwid = {n.lower(): i for i, n in c.execute('select id, name from card where is_keyword=1')}
    causes = {}
    for f, v, cs in c.execute("select field, value, causes from vocab where causes!='' and causes is not null"):
        causes[(f, v)] = [x.split(':') for x in cs.split(';')]

    def ins(card, origin, via, ab, role, ev, kind, side, pick, kw=None):
        c.execute('insert into flat_ref values(?,?,?,?,?,?,?,?,?,?)', (card, origin, via, ab, role, ev, kind, side or '', pick, kw))

    def state_rows(card, origin, via, ab, kind, side, pick, withs, zone):
        for st in re.findall(r'state (?:is|in) ([a-z_]+)', withs or ''):
            for ev, *kw in causes.get(('state', st), []):
                ins(card, origin, via, ab, 'state', ev, kind, side, pick, kwid.get(kw[0].lower()) if kw else None)
        if zone and kind == 'unit':
            for ev, *_ in causes.get(('zone', zone), []): ins(card, origin, via, ab, 'state', ev, kind, side, pick)

    def kw_of(withs):
        """the keyword a filter names, or the one that gives the state it names (given_keyword happenings)"""
        m = re.search(r'keyword is (\d+)', withs or '')
        if m: return int(m.group(1))
        for st in re.findall(r'state (?:is|in) ([a-z_]+)', withs or ''):
            for ev, *kw in causes.get(('state', st), []):
                if kw: return kwid.get(kw[0].lower())
        return None

    for r in c.execute('select card, origin, via, ability, event, actor_kind, actor_side, actor_pick, obj_kind, obj_side, '
                       'obj_pick, obj_with from flat_when').fetchall():
        card, o, v, ab, ev, ak, as_, ap, ok, os_, op, ow = r
        obj = ok or os_ or op
        if ev and ev != 'always': ins(card, o, v, ab, 'trigger', ev, ok if obj else ak, os_ if obj else as_, op if obj else ap, kw_of(ow))
        state_rows(card, o, v, ab, ok, os_, op, ow, None)
    for r in c.execute('select card, origin, via, ability, event, of_kind, of_side, of_pick, of_zone, of_with, ev_obj_kind, '
                       'ev_obj_side, ev_obj_with from flat_if').fetchall():
        card, o, v, ab, ev, fk, fs, fp, fz, fw, ek, es, ew = r
        if ev: ins(card, o, v, ab, 'condition', ev, ek or fk, es or fs, fp, kw_of(ew))
        state_rows(card, o, v, ab, fk, fs, fp, fw, fz)
        state_rows(card, o, v, ab, ek, es, None, ew, None)
    for r in c.execute('select card, origin, via, ability, act, on_kind, on_side, on_pick, on_zone, on_with, keyword_ref '
                       'from flat_do').fetchall():
        card, o, v, ab, act, k, s, p, z, w, kw = r
        for ev, *kwn in causes.get(('act', act), []):
            ins(card, o, v, ab, 'makes', ev, k, s, p, kwid.get(kwn[0].lower()) if kwn else kw)
        state_rows(card, o, v, ab, k, s, p, w, z)
