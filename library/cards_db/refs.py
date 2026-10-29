"""flat_ref: every way a card works with a happening, one row each, so one query finds all cards that care about it.
A happening is an `event` value from vocab.tsv (dies, summoned, damaged, given_keyword, stat_changed, ...). Roles:
  makes      an effect of the card causes it (vocab `causes` of the act), to the effect's target
  trigger    an ability waits for it (flat_when)
  condition  a condition or a counted amount tests that it happened (flat_if with an event)
  state      a target, condition or count picks things it happened to: a state filter whose vocab `causes` names it
             (dead_this_round -> dies), or units in the discard zone (zone discard `causes` dies; units only)
kind/side/pick: the thing it happens to (the event's object, else its actor; for makes the effect's target). side '' = not
limited (either side). keyword: the keyword given or used, when the happening is about one (given_keyword Stun).
concept: the same thing as a concept-tree concept, equal in every game: the keyword's concept (Stun, Freeze: disable), else
the state's (stunned, frozen: disable), else the event's (round_start, turn_start: turn_start).
Payoff question ("cards that benefit from allies dying"):
  select distinct card from flat_ref where happening='dies' and role!='makes' and side in ('mine','any','')
Called by load.py after flat.build."""
import re

SCHEMA = """create table flat_ref(card integer, origin text, via integer, ability integer, role text, happening text,
  kind text, side text, pick text, keyword integer, concept text, obj_with text, ref integer);
create index frh on flat_ref(happening, role); create index frc on flat_ref(card); create index frk on flat_ref(concept, role);"""


UNIT_ONLY = {'dies', 'killed', 'survives_damage', 'summoned', 'revived', 'leaves_play', 'strikes', 'attacks', 'blocks'}  # never a player's
PLAYER_ONLY = {'nexus_damaged'}  # only a player's
OPEN_KINDS = {None, '', 'player', 'any', 'anything'}  # kinds a player can be
BOARD_KINDS = {'unit', 'landmark', 'unit_or_structure', 'anything', 'any', None}
# a stat tested or counted, and the happenings that change it, for a player and for a unit
STAT_EVENTS = {'health': {'player': ('nexus_damaged', 'healed'), 'unit': ('stat_changed', 'damaged', 'healed')},
               'power': {'unit': ('stat_changed',)}, 'strength': {'unit': ('stat_changed', 'damaged'), 'player': ('nexus_damaged', 'healed')},
               'total_stats': {'unit': ('stat_changed',)}, 'cost': {'unit': (), 'player': ()}}


def build(c):
    c.executescript(SCHEMA)
    kwid = {n.lower(): i for i, n in c.execute('select id, name from card where is_keyword=1')}
    causes = {}
    for f, v, cs in c.execute("select field, value, causes from vocab where causes!='' and causes is not null"):
        causes[(f, v)] = [x.split(':') for x in cs.split(';')]

    tree = {(f, v): t for f, v, t in c.execute("select field, value, tree from vocab where tree!=''")}
    kwname = {i: (f'{g}:{n}' if ('keyword', f'{g}:{n}') in tree else n) for i, g, n in c.execute('select id, game, name from card where is_keyword=1')}

    def ins(card, origin, via, ab, role, ev, kind, side, pick, kw=None, state=None, w=None, ref=None):
        if role == 'makes' and ((kind == 'player' and ev in UNIT_ONLY) or (kind not in OPEN_KINDS and ev in PLAYER_ONLY)): return
        con = (tree.get(('keyword', kwname.get(kw, ''))) if kw else None) or (tree.get(('state', state)) if state else None) \
            or tree.get(('event', ev))
        c.execute('insert into flat_ref values(?,?,?,?,?,?,?,?,?,?,?,?,?)', (card, origin, via, ab, role, ev, kind, side or '', pick, kw, con, w, ref))

    def state_rows(card, origin, via, ab, kind, side, pick, withs, zone):
        for st in re.findall(r'state (?:is|in) ([a-z_]+)', withs or ''):
            for ev, *kw in causes.get(('state', st), []):
                ins(card, origin, via, ab, 'state', ev, kind, side, pick, kwid.get(kw[0].lower()) if kw else None, state=st)
        if zone and kind == 'unit':
            for ev, *_ in causes.get(('zone', zone), []): ins(card, origin, via, ab, 'state', ev, kind, side, pick)
        # units picked by a keyword they have ("friendly units with Rage", "the amount of Armor"): fed by giving that keyword
        for k in (re.findall(r'(?<![a-z:])keyword is (\d+)', withs or '') if kind != 'effect' else []):  # repeating Summon effects is no unit with Summon
            ins(card, origin, via, ab, 'state', 'given_keyword', kind, side, pick, int(k))
        # things picked by where they stand ("the enemy in front", "bordering units"): moving units changes who that is
        if re.search(r'(?<![a-z:])position ', withs or '') and kind in BOARD_KINDS:
            ins(card, origin, via, ab, 'state', 'moves', kind, side, pick, w=withs)

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
        if ev and ev != 'always': ins(card, o, v, ab, 'trigger', ev, ok if obj else ak, os_ if obj else as_, op if obj else ap, kw_of(ow), w=ow)
        state_rows(card, o, v, ab, ok, os_, op, ow, None)
    for r in c.execute('select card, origin, via, ability, event, of_kind, of_side, of_pick, of_zone, of_with, ev_obj_kind, '
                       'ev_obj_side, ev_obj_with, ev_obj_pick, test, attr from flat_if').fetchall():
        card, o, v, ab, ev, fk, fs, fp, fz, fw, ek, es, ew, ep, test, at = r
        # the thing the counted event happens to ("I've survived 10+ damage": of self) decides whose it is
        if ev: ins(card, o, v, ab, 'condition', ev, ek or fk, es or fs, ep or fp, kw_of(ew), w=ew or fw)
        elif fk == 'mana': ins(card, o, v, ab, 'condition', 'mana_refilled', fk, fs, fp)  # counts my mana: fed by mana gain
        # a stat tested or counted ("the enemy Nexus has half its Health or less", "a unit with 5+ Power"): fed by what changes it
        if test in ('stat', 'amount_stat', 'count', 'have', 'amount_count') and at in STAT_EVENTS and not ev:
            for sev in STAT_EVENTS[at].get(fk if fk == 'player' else 'unit', ()):
                ins(card, o, v, ab, 'condition', sev, fk, fs, fp, w=fw)
        state_rows(card, o, v, ab, fk, fs, fp, fw, fz)
        state_rows(card, o, v, ab, ek, es, None, ew, None)
    # a card that has an action keyword uses it (Lurk, Support, Evolve, Fury on the unit itself), and does what the keyword is
    for card, kw in c.execute('select card, keyword from card_keyword').fetchall():
        ins(card, 'has_keyword', kw, None, 'makes', 'keyword_used', None, 'mine', 'self', kw)
        for ev, *kwn in causes.get(('keyword', kwname.get(kw, '')), []): ins(card, 'has_keyword', kw, None, 'makes', ev, None, 'mine', 'self', kw)
    for r in c.execute('select card, origin, via, ability, act, on_kind, on_side, on_pick, on_zone, on_with, keyword_ref, card_ref, '
                       'param_event, to_kind, to_with from flat_do').fetchall():
        card, o, v, ab, act, k, s, p, z, w, kw, cref, pev, to_k, to_w = r
        for ev, *kwn in causes.get(('act', act), []):
            ins(card, o, v, ab, 'makes', ev, k, s, p, kwid.get(kwn[0].lower()) if kwn else kw, w=w, ref=cref)
        if act == 'keyword_action' and cref:  # a card planted or placed to go off later (a trap, a Chime): it goes off
            ins(card, o, v, ab, 'makes', 'trap_activated', 'card', s, None, w=f'card is {cref}', ref=cref)
        if kw and act in ('keyword_action', 'give_keyword'):  # what the keyword itself is (Predict: predicts)
            for ev, *kwn in causes.get(('keyword', kwname.get(kw, '')), []): ins(card, o, v, ab, 'makes', ev, k, s, p, kw)
        if act == 'cant' and pev == 'blocks' and s == 'enemy' and (p == 'self' or k in ('unit', None)):  # can't be blocked: hits the enemy player
            for ev in ('nexus_damaged', 'damaged'): ins(card, o, v, ab, 'makes', ev, 'player', 'enemy', None)
            ins(card, o, v, ab, 'makes', 'strikes_nexus', 'unit', 'mine', p)  # the unit itself strikes the Nexus
        if act in ('first_strike', 'double_strike', 'strike_with') and s in ('mine', None) and p in ('self', 'all', 'chosen', None):  # my unit strikes: an enemy takes damage
            ins(card, o, v, ab, 'makes', 'damaged', 'unit', 'enemy', None)
        state_rows(card, o, v, ab, k, s, p, w, z)
        if to_w and re.search(r'(?<![a-z:])position ', to_w): ins(card, o, v, ab, 'state', 'moves', to_k, s, None, w=to_w)  # "attack a bordering enemy"
