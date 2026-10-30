"""flat_ref: every way a card works with a happening, one row each, so one query finds all cards that care about it.
A happening is an `event` value from vocab.tsv (dies, summoned, damaged, given_keyword, stat_changed, ...). Roles:
  makes      an effect of the card causes it (vocab `causes` of the act), to the effect's target
  trigger    an ability waits for it (flat_when)
  condition  a condition or a counted amount tests that it happened (flat_if with an event)
  state      a target, condition or count picks things it happened to: a state filter whose vocab `causes` names it
             (dead_this_round -> dies), or units in the discard zone (zone discard `causes` dies; units only)
kind/side/pick: the thing it happens to (the event's object, else its actor; for makes the effect's target). actor_kind,
actor_with: who must do it, when the text says ("allied Pykes have dealt 15+ damage": actor unit, name_has Pyke). side '' = not
limited (either side). keyword: the keyword given or used, when the happening is about one (given_keyword Stun).
concept: the same thing as a concept-tree concept, equal in every game: the keyword's concept (Stun, Freeze: disable), else
the state's (stunned, frozen: disable), else the event's (round_start, turn_start: turn_start).
Payoff question ("cards that benefit from allies dying"):
  select distinct card from flat_ref where happening='dies' and role!='makes' and side in ('mine','any','')
Called by load.py after flat.build."""
import re

SCHEMA = """create table flat_ref(card integer, origin text, via integer, ability integer, role text, happening text,
  kind text, side text, pick text, keyword integer, concept text, obj_with text, ref integer, actor_kind text, actor_with text);
create index frh on flat_ref(happening, role); create index frc on flat_ref(card); create index frk on flat_ref(concept, role);"""


PLACES = {'summon', 'play_card', 'create', 'copy', 'revive', 'transform', 'keyword_action'}  # acts that put a card somewhere
UNIT_ONLY = {'dies', 'killed', 'survives_damage', 'summoned', 'revived', 'leaves_play', 'strikes', 'attacks', 'blocks'}  # never a player's
PLAYER_ONLY = {'nexus_damaged'}  # only a player's
OPEN_KINDS = {None, '', 'player', 'any', 'anything'}
DONE_BY = {'attacks', 'strikes', 'fights', 'challenges'}  # the side of these is the doer's (the actor), not the unit it is done to
BY_ME = {'killed', 'damaged', 'nexus_damaged', 'challenges'}  # done by the card to something else: only the card itself can do it
# (attacks and strikes by the card: other cards can make it attack or strike: Rally, "an ally strikes")  # kinds a player can be
HARM = {'damage', 'kill', 'obliterate', 'capture', 'stun', 'silence', 'transform'}  # harm aimed at a chosen target of either side
TO_OBJECT = {('harvest', 'harvests'), ('set_terrain', 'terrain_changed')}  # "X harvests from a well": the unit is the actor, the space the object (like strikes)
BOARD_KINDS = {'unit', 'landmark', 'unit_or_structure', 'anything', 'any', None, 'player'}  # a player on the board: a leader (Duelyst General)
KIND_OF_CAT = {'unit': 'unit', 'hero': 'unit', 'leader': 'player'}  # the kind a card of a category is on the board
NOT_UNIT_DEATH = {'dies', 'killed', 'survives_damage', 'damaged'}  # destroying an artifact or equipment kills no unit (Duelyst EMP)
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

    def ins(card, origin, via, ab, role, ev, kind, side, pick, kw=None, state=None, w=None, ref=None, ak=None, aw=None):
        if role == 'makes' and pick == 'self' and not side: side = 'mine'  # what a card does to itself happens on my side
        if ev == 'strikes_nexus' and kind == 'player': kind, side = 'unit', 'mine'  # one way: the unit that strikes, never the player struck
        if role == 'makes' and ((kind == 'player' and ev in UNIT_ONLY) or (kind not in OPEN_KINDS and ev in PLAYER_ONLY)): return
        if role == 'makes' and kind == 'equipment' and ev in NOT_UNIT_DEATH: return
        if role == 'makes' and ev in ('summoned', 'revived') and not side: side = 'mine'  # a summon puts the unit on its owner's side
        con = (tree.get(('keyword', kwname.get(kw, ''))) if kw else None) or (tree.get(('state', state)) if state else None) \
            or tree.get(('event', ev))
        c.execute('insert into flat_ref values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (card, origin, via, ab, role, ev, kind, side or '', pick, kw, con, w, ref, ak, aw))

    cat = dict(c.execute('select id, category from card'))
    it_side = {(a, b): sd for a, b, sd in c.execute("select card, ability, on_side from flat_do where coalesce(seq,0)=0 and coalesce(on_pick,'') not in ('it','self')")}

    def helps(act, ps):
        """an effect that leaves the cards it picks better off (stats up, cheaper, healed, sped up)"""
        p = dict(x.split('=', 1) for x in (ps or '').split(';') if '=' in x)
        if act in ('stat_change', 'grow'): return any(k in p and not p[k].startswith('-') for k in ('power', 'health', 'strength'))
        if act == 'cost_change': return p.get('cost', '').startswith('-')
        return act in ('countdown_advance', 'heal', 'ready', 'can', 'give_ability', 'negate_damage', 'cost_set', 'damage_reduction')  # not increase_effect: a card that makes Rage stronger wants Rage (Deranged Brute)

    def state_rows(card, origin, via, ab, kind, side, pick, withs, zone, entering=False, helpful=False):
        for st in re.findall(r'state (?:is|in) ([a-z_]+)', withs or ''):
            for ev, *kw in causes.get(('state', st), []):
                ins(card, origin, via, ab, 'state', ev, kind, side, pick, kwid.get(kw[0].lower()) if kw else None, state=st)
        if zone and kind == 'unit':
            for ev, *_ in causes.get(('zone', zone), []): ins(card, origin, via, ab, 'state', ev, kind, side, pick, w=withs)  # "if Krog has
            # died": Krog's death, not any death (the filter was dropped)
        # units picked by a keyword they have ("friendly units with Rage", "the amount of Armor"): fed by giving that keyword
        for k in (re.findall(r'(?<![a-z:])keyword is (\d+)', withs or '') if kind != 'effect' and not helpful and zone not in ('deck', 'deck_top', 'deck_bottom') else []):  # help to
            # the cards with a keyword ("your Build minions progress by 1 turn") is no need for that keyword: it helps them  # repeating Summon effects is no unit with Summon; a card in the deck has its keyword, nothing gives it (Iona's Smile draws Flying creatures)
            ins(card, origin, via, ab, 'state', 'given_keyword', kind, side, pick, int(k))
        # things picked by where they stand ("the enemy in front", "bordering units"): moving units changes who that is
        if re.search(r'(?<![a-z:])position ', withs or '') and kind in BOARD_KINDS and not entering and \
                not re.search(r'(?<![a-z:])position \w+ \w+ of position(?: \w+)? chosen', withs or ''):  # around a space the player picks
            # ("all enemies on or adjacent to a chosen space"): the player aims it where units are; moving them is no help
            ins(card, origin, via, ab, 'state', 'moves', kind, side, pick, w=withs)
            if re.search(r'(?<![a-z:])position \w+ \w+ of self\b', withs or '') and pick != 'self' and side == 'mine':  # from the card itself (Zeal:
                ins(card, origin, via, ab, 'state', 'moves', None, 'mine', 'self', w=withs)  # "near your General"): moving it changes it too
            # measured from my unit: the card itself ("each enemy around this one", Bonereaper) or my unit the ability picked first
            # ("restore 4 Health to a friendly minion, deal 4 to enemies around it", Holy Immolation): moving that unit changes who it hits
            elif side != 'mine' and pick != 'self' and origin == 'own' and cat.get(card) in ('unit', 'hero', 'leader', 'building') and \
                    re.search(r'(?<![a-z:])position \w+ \w+(?: of self)?(?:;|$)', withs or ''):
                ins(card, origin, via, ab, 'state', 'moves', None, 'mine', 'self', w=withs)
            elif side != 'mine' and re.search(r'(?<![a-z:])position \w+ \w+ of it\b', withs or '') and it_side.get((card, ab)) == 'mine':
                ins(card, origin, via, ab, 'state', 'moves', 'unit', 'mine', None, w=withs)
        # where the card itself stands ("while on the enemy side": a space with same_space and no "of"): moving it is its need
        elif kind == 'position' and not entering and re.search(r'(?<![a-z:])position is same_space(?! of)', withs or '') and \
                re.search(r'(?<![a-z:])position \w+ \w+ of ', withs or ''):
            ins(card, origin, via, ab, 'state', 'moves', None, 'mine', 'self', w=withs)

    def kws_of(withs):
        """every keyword a filter names: "keyword is X", or "keyword in X" rows (one of them: traps or boons)"""
        return [int(k) for k in re.findall(r'(?<![a-z:])keyword (?:is|in) (\d+)', withs or '')]

    def kw_of(withs):
        """the keyword a filter names, or the one that gives the state it names (given_keyword happenings)"""
        m = re.search(r'keyword is (\d+)', withs or '')
        if m: return int(m.group(1))
        for st in re.findall(r'state (?:is|in) ([a-z_]+)', withs or ''):
            for ev, *kw in causes.get(('state', st), []):
                if kw: return kwid.get(kw[0].lower())
        return None

    cleanup = {a for (a,) in c.execute("""select ability from flat_do group by ability having sum(case when act in
               ('kill','obliterate','sacrifice') and on_pick='self' then 0 else 1 end)=0""")}
    for r in c.execute('select card, origin, via, ability, event, actor_kind, actor_side, actor_pick, obj_kind, obj_side, '
                       'obj_pick, obj_with, actor_with from flat_when').fetchall():
        card, o, v, ab, ev, ak, as_, ap, ok, os_, op, ow, aw = r
        obj = ok or os_ or op
        if ab in cleanup: continue  # "When you summon Krog, destroy this": it only removes itself; it waits for nothing
        if ev and ev != 'always':
            pk = op if obj else ap
            side = os_ if obj else as_
            if ev in DONE_BY and as_ == 'enemy' and ap != 'self': side = 'enemy'  # "if a Chime is attacked": an enemy attacks, not mine
            if ap == 'self' and op != 'self':  # "Strike: ... the attacked unit": it is about the card striking, not the unit hit
                pk = 'actor_self' if ev in BY_ME else 'self'
            for k in (kws_of(ow) if len(kws_of(ow)) > 1 else [kw_of(ow)]):  # "traps or boons": one row per keyword, never "any keyword"
                ins(card, o, v, ab, 'trigger', ev, ok if obj else ak, side, pk, k, w=ow if obj else aw, ak=ak if obj else None, aw=aw if obj else None)
        state_rows(card, o, v, ab, ok, os_, op, ow, 'deck' if ev in ('drawn', 'played', 'discarded') else None,  # "draw a Flying
                   entering=ev in ('summoned', 'played'))  # "summoned adjacent to this": where it enters; moving is no help
        # creature": the card has Flying already; nothing given in play makes it one
    r_op = {(a, b, t, at): op for a, b, t, at, op in c.execute('select card, ability, test, attr, op from flat_if')}
    compared = {(a, b) for a, b in c.execute("select card, ability from flat_if where test='amount'")}
    picked_any = {(a, b) for a, b in c.execute("""select card, ability from flat_do where on_pick in ('chosen','random') and coalesce(on_side,'any')!='mine'
                  and act in ('kill','damage','obliterate','sacrifice','return_to_hand','transform','silence')""")}  # harm on either side goes to enemies
    costs = {(a, b) for a, b in c.execute("select card, ability from flat_do where act in ('cost_set','cost_change') and on_pick='self'")}
    for r in c.execute('select card, origin, via, ability, event, of_kind, of_side, of_pick, of_zone, of_with, ev_obj_kind, '
                       'ev_obj_side, ev_obj_with, ev_obj_pick, test, attr, ev_actor_pick, ev_actor_kind, ev_actor_with from flat_if').fetchall():
        card, o, v, ab, ev, fk, fs, fp, fz, fw, ek, es, ew, ep, test, at, eap, eak, eaw = r
        if eap == 'self' and ep != 'self': ep = 'actor_self' if ev in BY_ME else 'self'  # "I've killed": only the card itself does it
        # the thing the counted event happens to ("I've survived 10+ damage": of self) decides whose it is
        if ev:
            for k in (kws_of(ew) if len(kws_of(ew)) > 1 else [kw_of(ew)]):
                ins(card, o, v, ab, 'condition', ev, ek or fk, es or fs, ep or fp, k, w=ew or fw, ak=eak, aw=eaw)
        elif fk in ('mana', 'secondary_resource', 'gem', 'lane_resource'): ins(card, o, v, ab, 'condition', 'mana_refilled', fk, fs, fp, w=fw)  # counts my mana or another resource: fed by gaining it
        elif fk == 'position' and fw and 'terrain is ' in fw and 'position ' not in fw and test in ('count', 'have', 'amount_count'):  # (where a unit stands is no ground made)  # "for each forest you control":
            ins(card, o, v, ab, 'condition', 'terrain_changed', 'position', fs, fp, w=fw)                 # fed by making that ground
        # a stat tested or counted ("the enemy Nexus has half its Health or less", "a unit with 5+ Power"): fed by what changes it
        if test in ('stat', 'amount_stat', 'count', 'have', 'amount_count') and at in STAT_EVENTS and not ev:
            sevs = STAT_EVENTS[at].get(fk if fk == 'player' else 'unit', ())
            # the direction it wants: "5+ Life", "faeria equal to its Life" want more (stat changes, healing), "half its Health or
            # less" wants less (damage, stat changes); damage never feeds a need for more (Feed the Forest)
            op = r_op.get((card, ab, test, at))
            if test == 'amount_stat' and fp == 'it' and (card, ab) in picked_any: continue  # "destroy ANY minion, restore its Health":
            # the player picks the biggest there is; nothing has to grow it (Martyrdom)
            if test == 'amount_stat' and (card, ab) in compared: continue  # a stat used as a threshold ("lethal damage": damage >= my
            # Life) is no stat the card wants more or less of (Divine Guardian)
            if test == 'amount_stat' and (card, ab) in costs:  # a cost equal to a stat ("costs your General's Health"): less of it
                sevs = tuple(e for e in sevs if e != 'healed')  # makes it cheaper (Blood Taura): damage feeds it, healing does not
            elif test == 'amount_stat': sevs = ()  # a number taken from a stat ("Attack becomes equal to its Life") waits for nothing;
            # what raises that stat makes the card stronger (network.py boost_lines: more health, more power)
            elif op in ('ge', 'gt'): sevs = tuple(e for e in sevs if e not in ('damaged', 'nexus_damaged'))
            elif op in ('le', 'lt'): sevs = tuple(e for e in sevs if e != 'healed')
            for sev in sevs:
                ins(card, o, v, ab, 'condition', sev, fk or 'unit', fs, fp, w=fw)  # a unit's stat unless a player's is named ("its Life" of "it")
        state_rows(card, o, v, ab, fk, fs, fp, fw, fz)
        state_rows(card, o, v, ab, ek, es, None, ew, None)
    # a card that has an action keyword uses it (Lurk, Support, Evolve, Fury on the unit itself), and does what the keyword is
    for card, kw in c.execute('select card, keyword from card_keyword').fetchall():
        ins(card, 'has_keyword', kw, None, 'makes', 'keyword_used', None, 'mine', 'self', kw)
        for ev, *kwn in causes.get(('keyword', kwname.get(kw, '')), []): ins(card, 'has_keyword', kw, None, 'makes', ev, None, 'mine', 'self', kw)
    # "the attacker", "that enemy" (pick actor): who it is is the event's actor (the counterattack rule strikes the enemy that
    # attacked, never my own unit)
    actor_of = {(a, b): (ak, as_) for a, b, ak, as_ in c.execute('select card, ability, actor_kind, actor_side from flat_when')}
    entry_abs = {(a, b) for a, b in c.execute("select card, ability from flat_when where event in ('played','summoned') and obj_pick='self'")}
    ev_of = {(a, b): e for a, b, e in c.execute("select card, ability, event from flat_when where actor_pick='self' and obj_pick is null")}
    for r in c.execute('select card, origin, via, ability, act, on_kind, on_side, on_pick, on_zone, on_with, keyword_ref, card_ref, '
                       'param_event, to_kind, to_with, to_side, to_pick, params from flat_do').fetchall():
        card, o, v, ab, act, k, s, p, z, w, kw, cref, pev, to_k, to_w, to_s, to_p, ps = r
        if not s and p == 'chosen' and act in HARM and k in ('unit', 'any', 'anything', 'unit_or_structure', None):
            s = 'enemy'  # "deal 2 to a creature" (either side): the player aims it at an enemy; it makes no friendly deaths
        if p == 'actor' and not (k or s): k, s = actor_of.get((card, ab), (None, None))
        if to_p == 'actor' and not (to_k or to_s): to_k, to_s = actor_of.get((card, ab), (None, None))
        if act == 'can' and k == 'player' and pev not in (None, 'played', 'summoned', 'targeted'):  # "you may replace an additional
            ins(card, o, v, ab, 'makes', pev, 'card' if pev in ('shuffled', 'drawn', 'discarded') else k, s or 'mine', None)  # card": more of it
        # "it" in an ability on my own attack or strike ("Backstab: deals extra damage to it") is what I attack: an enemy
        if p == 'it' and not s and ev_of.get((card, ab)) in ('attacks', 'strikes'): k, s = k or 'any', 'enemy'
        for ev, *kwn in causes.get(('act', act), []):
            if (act, ev) in TO_OBJECT and (to_k or to_s or to_p):  # the space it happens on is the event's object, the mover its actor
                if act == 'set_terrain':  # the space now has the new ground ("to"), on the side of the space changed (mine when unsaid)
                    ins(card, o, v, ab, 'makes', ev, 'position', s or 'mine', p, w=to_w); continue
                ins(card, o, v, ab, 'makes', ev, to_k, to_s, 'self' if p == 'self' else to_p, w=to_w, ak=k or 'unit', aw=w); continue  # "I harvest": self, as for strikes
            if act == 'strike' and ev != 'strikes' and (to_k or to_s or to_p):  # "A strikes B": A strikes, B takes the damage
                if to_k == 'player':
                    if ev == 'damaged': ins(card, o, v, ab, 'makes', 'nexus_damaged', 'player', to_s, None)
                    else: continue
                ins(card, o, v, ab, 'makes', ev, to_k, to_s, to_p, w=to_w); continue
            if act == 'give_ability' and ev == 'given_keyword' and k == 'player': continue  # an ability given to the player is no keyword
            ins(card, o, v, ab, 'makes', ev, k, s, p, kwid.get(kwn[0].lower()) if kwn else kw, w=w, ref=cref)
        if act == 'strike' and to_k == 'player': ins(card, o, v, ab, 'makes', 'strikes_nexus', k or 'unit', s or 'mine', p)
        if act == 'keyword_action' and cref:  # a card planted or placed to go off later (a trap, a Chime): it goes off
            ins(card, o, v, ab, 'makes', 'trap_activated', 'card', s, None, w=f'card is {cref}', ref=cref)
        if kw and act in ('keyword_action', 'give_keyword'):  # what the keyword itself is (Predict: predicts)
            for ev, *kwn in causes.get(('keyword', kwname.get(kw, '')), []): ins(card, o, v, ab, 'makes', ev, k, s, p, kw, w=w)  # on what it is given to ("give the Demon Wing Flying")
        if act == 'cant' and pev == 'blocks' and s == 'enemy' and (p == 'self' or k in ('unit', None)):  # can't be blocked: hits the enemy player
            for ev in ('nexus_damaged', 'damaged'): ins(card, o, v, ab, 'makes', ev, 'player', 'enemy', None)
            ins(card, o, v, ab, 'makes', 'strikes_nexus', 'unit', 'mine', p)  # the unit itself strikes the Nexus
        if act == 'gain_attack_token':  # the attack token (Rally): my units attack again, their Attack effects happen again
            ins(card, o, v, ab, 'makes', 'attacks', 'unit', 'mine', None)
        if act in ('first_strike', 'double_strike', 'strike_with') and s in ('mine', None) and p in ('self', 'all', 'chosen', None):  # my unit strikes: an enemy takes damage
            ins(card, o, v, ab, 'makes', 'damaged', 'unit', 'enemy', None)
        if act == 'spend_mana' and k in ('mana', 'secondary_resource', 'gem', 'lane_resource') and s in ('mine', None):
            # an ability that spends a resource needs it ("Activate: Pay 2 Bones"): fed by gaining it; the card's own need
            ins(card, o, v, None if o == 'has_keyword' else ab, 'condition', 'mana_refilled', k, 'mine', None, w=w)
        # an effect when the card enters on a unit next to it ("Opening Gambit: give a nearby minion +2"): where it enters decides
        state_rows(card, o, v, ab, k, s, p, w, z, entering=(card, ab) in entry_abs and not re.search(r'(?<![a-z:])position \w+ \w+ of ', w or ''),
                   helpful=s in ('mine', None) and helps(act, ps))
        if to_w and to_k != 'position' and re.search(r'(?<![a-z:])position ', to_w) and act not in PLACES:  # a space is not moved into place  # "attack a bordering enemy"; where a new card is put
            ins(card, o, v, ab, 'state', 'moves', to_k, s, None, w=to_w)                # ("Pelt Lice in adjacent slots") needs no moves
    # the game's rules (read/<game>/game_rules.jsonl): what every card of a category does without its text saying so (an
    # attacking unit hits the enemy Nexus when it is not blocked); its makes rows, about "self", become every such card's own
    for e, cat, cost_has in c.execute('select entry, category, cost_has from game_rule').fetchall():
        # a rule about a cost ("Bones costs": the card needs Bones) is a need of every card whose cost names it; other rules make
        rows = c.execute("select ability, happening, kind, side, pick, keyword, concept, obj_with, ref, role from flat_ref where card=? and role in "
                         + ("('makes','condition','trigger')" if cost_has else "('makes')"), (e,)).fetchall()
        # a unit that can never do what the rule makes does not follow it: Immobile, Inert, "I can't attack" skip the fight rule,
        # "Can't harvest faeria" the harvest rule; a "can't" limited to some targets ("can only attack gods") skips nothing
        made = {r[1] for r in rows}
        fights = bool(made & {'attacks', 'strikes', 'strikes_nexus', 'fights'})
        never = {a for (a,) in c.execute("""select ck.card from card_keyword ck join card k on k.id=ck.keyword join vocab v on v.field='keyword'
                 and v.value in (k.name, k.game || ':' || k.name) where v.tree='cant_attack'""")} if fights else set()
        never |= {a for (a, ev) in c.execute("""select card, param_event from flat_do where origin='own' and act='cant' and on_pick='self'
                 and to_kind is null and coalesce(lasts,'while') in ('while','permanent')""") if ev in made or (fights and ev == 'attacks')}
        for (card,) in c.execute("select id from card where category=? and game=(select game from card where id=?) and is_stub=0 and "
                                 "(? is null or (lower(coalesce(cost_text,'')) like '%' || lower(?) || '%' and coalesce(cost, 1) > 0))",  # "0 Blood" costs nothing
                                 (cat, e, cost_has, cost_has)).fetchall():
            if card in never: continue
            ckind = KIND_OF_CAT.get(c.execute('select category from card where id=?', (card,)).fetchone()[0])
            for ab, h, k, sd, pk, kw, con, w, ref, role in rows:
                if pk == 'self' and not sd: sd = 'mine'  # what the card does to itself is on its owner's side
                if pk == 'self' and not k: k = ckind  # a unit fights as a unit, a leader (Duelyst General) as its player
                # (a leader attacks, strikes and kills as its player: "whenever your General attacks" waits for exactly that)
                c.execute('insert into flat_ref values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (card, 'game', e, ab, role, h, k, sd, pk, kw, con, w, ref, None, None))
    # a unit that comes back when it dies (Ruunin: "Last Words - return Ruunin to your hand") dies again and again: its deaths
    # feed what counts my units dying (Shaytan Monstrosity), as a card that kills my units does (ref: the card itself)
    for card, ab in c.execute("""select distinct w.card, w.ability from flat_when w join flat_do d on d.card=w.card where w.event='dies'
            and w.obj_pick='self' and w.origin='own' and d.origin in ('own','gives') and d.act in ('return_card','return_to_hand','revive','summon')
            and (d.on_with like '%card is ' || w.card || '%' or d.card_ref=w.card or (d.on_pick='self' and d.ability=w.ability))""").fetchall():
        ins(card, 'own', None, ab, 'makes', 'dies', 'unit', 'mine', 'self', ref=card)
    # what an ability kills and then uses ("destroy all friendly minions to summon an Abomination that gains their Attack"): its
    # own deaths, it waits for none
    c.execute("""delete from flat_ref where role in ('state','condition') and happening='dies' and exists (select 1 from flat_ref m
                 where m.card=flat_ref.card and m.ability=flat_ref.ability and m.role='makes' and m.happening='dies'
                 and coalesce(m.kind,'')=coalesce(flat_ref.kind,'') and m.side=flat_ref.side and coalesce(m.pick,'')=coalesce(flat_ref.pick,''))""")
