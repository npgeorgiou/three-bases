"""A deck explained in plain words, from the stored rows only (no reading of texts): its plan (what its cards make and which
cards use it), its champions' level-ups, how it controls the enemy, how it supports its units, its card flow, what repeats
its effects, its key cards and its weak spots. Same code for every game; links only inside the deck's game.
Usage (through ask.py): ask.py <game> analyze "<card>, <card>, ..." """
import collections, os, re
import mechanics

DECK_RULES = {  # the games' own deck-building rules (not card data)
    'runeterra': {'size': 40, 'copies': 3, 'factions': 2, 'neutral': None},
    'stormbound': {'size': 12, 'copies': 1, 'factions': 1, 'neutral': 'Neutral'},
}
SAY = {  # what happens, in plain words; {who} = your / enemy / any
    'dies': '{who} units die', 'killed': '{who} units are killed', 'damaged': '{who} units or players take damage',
    'survives_damage': '{who} units survive damage', 'nexus_damaged': '{whos} takes damage', 'summoned': '{who} units enter play',
    'played': 'cards are played', 'cost_changed': 'card costs are changed', 'drawn': 'you draw cards', 'discarded': 'cards are discarded', 'created': 'cards are created',
    'given_keyword': '{who} units get {kw}', 'stat_changed': '{who} units have their stats changed', 'healed': '{who} units are healed',
    'attacks': '{who} units attack', 'blocks': '{who} units block', 'strikes': '{who} units strike',
    'strikes_nexus': '{who} units hit the enemy player', 'leaves_play': '{who} cards leave play', 'recalled': '{who} units return to hand',
    'revived': '{who} units come back from the dead', 'levels_up': 'champions level up', 'obliterated': 'cards are removed from the game',
    'transformed': 'cards transform', 'mana_refilled': 'you gain mana', 'targeted': '{who} cards are targeted', 'moves': '{who} units move', 'shuffled': 'cards are replaced (shuffled into the deck)',
    'equipped': '{who} units get equipment', 'spell_resolves': 'spells finish', 'keyword_used': '{kw} is used',
    'round_start': 'a round starts', 'round_end': 'a round ends', 'turn_start': 'your turn starts', 'turn_end': 'your turn ends',
    'mana_refilled@secondary_resource': 'you gain the second resource (Bones)', 'mana_refilled@gem': 'you gain a gem (Mox)',
    'mana_refilled@lane_resource': 'you gain the lane resource (Echo)', 'sacrificed': '{who} units are sacrificed'}
RESOURCE_KINDS = ('secondary_resource', 'gem', 'lane_resource')
EVERY_GAME = {'played', 'summoned', 'attacks', 'blocks', 'strikes', 'damaged', 'survives_damage', 'round_start', 'round_end',
              'turn_start', 'turn_end', 'drawn', 'mana_refilled', 'strikes_nexus', 'nexus_damaged', 'always', 'activated', 'moves',
              'attack_done', 'targeted', 'spell_resolves', 'game_start', 'supports', 'combat_start', 'combat_end', 'kept_in_hand'}  # happen in play without a card making them
CONTROL = ('damage', 'ping', 'aoe_damage', 'removal', 'destroy', 'board_wipe', 'banish', 'bounce_enemy', 'disable', 'attack_zero', 'stat_loss', 'silence',
           'attack_lock', 'cant_block', 'immobilize', 'forced_movement', 'steal', 'polymorph', 'damage_over_time')
SUPPORT = ('stat_gain', 'attack_gain', 'defence_gain', 'shield', 'immunity', 'evasion', 'first_strike', 'multi_attack', 'heal',
           'regeneration', 'cheat_death', 'damage_reduction', 'excess_damage', 'lifesteal', 'permanent_growth', 'temporary_buff')
FLOW = ('draw', 'generate_cards', 'selection', 'tutor', 'recycle', 'copy')


def kinds_fit(a, b):
    """a player is never a unit or a structure, a unit never a structure; open kinds fit everything (network.kinds_fit)"""
    if a in (None, '', 'any', 'anything', 'card', 'keyword') or b in (None, '', 'any', 'anything', 'card', 'keyword') or a == b: return True
    if 'unit_or_structure' in (a, b): return {a, b} <= {'unit_or_structure', 'unit', 'landmark'}
    return False


def who(side):
    return {'mine': 'your', 'enemy': 'enemy'}.get(side, 'any')


def say(c, h, side, kw):
    k = c.execute('select name from card where id=?', (kw,)).fetchone()[0] if kw else 'a keyword or status'
    return SAY.get(h, h.replace('_', ' ')).format(who=who(side), whos={'mine': 'your Nexus or base', 'enemy': 'the enemy player'}.get(side, 'a player'), kw=k)


def names(c, ids):
    return ', '.join(sorted({mechanics.name(c, i) for i in ids}))


def parse_deck(c, game, text):
    """card names in a list; a name may itself hold a comma ("Senna, Sentinel of Light"): the longest known name wins"""
    known = sorted({n for (n,) in c.execute('select name from card where game=? and is_keyword=0 and is_stub=0', (game,))}, key=len, reverse=True)
    found, rest, unknown = [], text, []
    while rest.strip(' ,\n'):
        rest = rest.strip(' ,\n'); low = rest.lower()
        m = next((n for n in known if low.startswith(n.lower()) and (len(rest) == len(n) or rest[len(n)] in ',\n')), None)
        if not m:  # the same name written with other spaces ("Fish Bot" for Fishbot)
            cut = rest.find(','); word = (rest if cut < 0 else rest[:cut]).strip()
            m = next((n for n in known if n.lower().replace(' ', '') == word.lower().replace(' ', '')), None)
            if m: found.append(m); rest = '' if cut < 0 else rest[cut:]; continue
            unknown.append(word); rest = '' if cut < 0 else rest[cut:]
            continue
        found.append(m); rest = rest[len(m):]
    ids = [c.execute('select id from card where game=? and name=? and is_keyword=0 and is_stub=0', (game, n)).fetchone()[0] for n in found]
    return ids, unknown


_TEXT = {}
def text_of(card):
    if not _TEXT:
        import source
        for i, t in source.lib().execute('select id, text from entities'): _TEXT[i] = (t or '').lower()
    return _TEXT.get(card, '')


def analyze(c, game, text):
    ids, unknown = parse_deck(c, game, text)
    deck = list(dict.fromkeys(ids)); D = set(deck); out = []
    if not deck: return ['No cards of ' + game + ' found.']
    marks = ','.join('?' * len(deck))
    # the deck and the game's rules
    reg = {i: [r for r in (c.execute('select regions from card where id=?', (i,)).fetchone()[0] or '').split(';') if r] for i in deck}
    rule = DECK_RULES.get(game, {})
    facs = collections.Counter(r for rs in reg.values() for r in rs if r != rule.get('neutral'))
    head = f'{len(deck)} different cards, ' + ', '.join(f'{f} {n}' for f, n in facs.most_common()) + '.'
    import itertools
    own = [set(rs) - {rule.get('neutral')} for rs in reg.values() if set(rs) - {rule.get('neutral')}]
    if rule and not any(all(o & set(pick) for o in own) for pick in itertools.combinations(facs, min(rule['factions'], len(facs)))):
        head += f" The data puts these cards in {len(facs)} factions; {game} decks allow {rule['factions']}."
    out.append(head)
    if unknown: out.append('Not found in ' + game + ': ' + ', '.join(unknown) + '.')

    # what each card makes and what it uses (its own rules only; a keyword's inner rules are not the card's needs)
    # a cost the game's rules set (Bones, Mox) is the card's own need too: rows of origin game with role condition
    rows = c.execute(f"select card, ability, role, happening, side, keyword, pick, origin, kind, obj_with from flat_ref where (origin!='game' or role='condition') and card in ({marks})", deck).fetchall()
    lvl = {a for (a,) in c.execute(f"select ability from flat_do where act='level_up' and card in ({marks})", deck)}
    makes = collections.defaultdict(set); uses = []
    for card, ab, role, h, side, kw, pick, origin, kind, mw in rows:
        if h in ('mana_refilled', 'resource_gained') and kind in RESOURCE_KINDS: h = 'mana_refilled@' + kind  # which resource
        elif h == 'resource_gained': continue
        if role == 'makes': makes[(h, kw)].add((card, side, kind, pick, mw))
        elif origin in ('own', 'game') and not (pick == 'self' and h in ('played', 'summoned')):
            uses.append((card, ab, role, h, 'mine' if pick == 'self' else side, kw, pick, kind, mw))
    # what the game's rules make every card of the deck do (a Skeleton dying gives a Bone, any unit can be sacrificed)
    by_rule = collections.defaultdict(set)
    for card, h, kind, sd in c.execute(f"select card, happening, kind, side from flat_ref where origin='game' and role='makes' and card in ({marks})", deck):
        if sd == 'enemy' or h in ('damaged', 'survives_damage', 'dies'): continue  # fights hurt both sides; every unit would be a
        # maker of deaths, which says nothing about a deck (the network keeps these as weak "by fighting" lines)
        by_rule['mana_refilled@' + kind if h in ('mana_refilled', 'resource_gained') and kind in RESOURCE_KINDS else h].add(card)
    fit = lambda a, b: not a or not b or a == b or 'any' in (a, b)
    import network  # (lazy: network imports this module)
    def names_it(m, tw):
        """the need names a kind of card the maker is ("Gorge: I eat a Morsel" and a Morsel that is eaten): its own happening is it"""
        who = ';'.join(p for p in (tw or '').split(';') if p.split(' ')[:2] in (['card', 'is'], ['type', 'is'], ['type', 'in'], ['name_has', 'is']))
        return bool(who) and can_be(m, who)

    def can_be(card, mw):
        """what a maker does it to ("the Demon Wing", "another Rakoan") can be this card"""
        who = ';'.join(p for p in (mw or '').split(';') if p.split(' ')[:2] in (['card', 'is'], ['type', 'is'], ['type', 'in'], ['name_has', 'is']))
        cs = network.cards_of(c, game)
        return not who or card not in cs or network.matches(c, game, cs[card], 'any', who)
    plan = collections.defaultdict(lambda: [set(), set(), set(), set()])  # makers, own-death users, level-ups, other users
    linked = set(); sides = collections.defaultdict(set)
    actor_side = {(a, b): sd for a, b, sd in c.execute("select card, ability, actor_side from flat_when where actor_side is not null")}
    enemy_doers = {a for (a,) in c.execute("""select card from flat_do where act in ('strike','start_attack','redirect_attack')
                   and coalesce(on_side,'') in ('enemy','')""")}
    for card, ab, role, h, side, kw, pick, kind, tw in uses:  # kinds must fit too: healing a god is no unit healed (as network.kinds_fit)
        mk = {(m, ms) for (hh, k), ms_ in makes.items() if hh == h and (k is None or kw is None or k == kw) for m, ms, mkd, mp, mw in ms_
              if m != card and fit(ms, side) and kinds_fit(mkd, kind) and not (pick == 'self' and mp == 'self' and not names_it(m, tw)) and
              not (pick == 'self' and not can_be(card, mw))}  # "when THIS moves":
              # another card moving itself is no help (network: two cards each about themselves never link)
        if role == 'trigger' and actor_side.get((card, ab)) == 'enemy': mk = {(m, ms) for m, ms in mk if m in enemy_doers}  # "when an
        # enemy damages another enemy" (Vek Hormones): only a card that makes enemies act does it, not my own damage (as network)
        if role == 'condition' and side in ('mine', '', None):  # a cost: the game's rules make it too (any unit can be sacrificed, a Skeleton's death gives a Bone)
            mk |= {(m, 'mine') for m in by_rule.get(h, set()) - {card}}
        if not mk: continue
        key = (h, kw)
        p = plan[key]; p[0] |= {m for m, _ in mk}
        sides[key].add(side if side in ('mine', 'enemy') else '')
        (p[2] if ab in lvl else p[1] if pick == 'self' and h == 'dies' else p[3]).add(card)
        linked |= {card} | {m for m, _ in mk}
    # repeats: a card that makes other cards' triggers happen again (Allied Attack effects activate twice)
    trig = {k: e for k, e in c.execute('select t.keyword, v.event from keyword_trigger t join event v on v.id=t.event')}
    for card, w in c.execute(f"select card, on_with from flat_do where act in ('repeat','increase_effect') and card in ({marks})", deck):
        evs = {trig.get(int(p.split(' ')[2])) for p in (w or '').split(';') if p.startswith('keyword is ') and p.split(' ')[2].isdigit()}
        kws = [mechanics.name(c, int(p.split(' ')[2])) for p in (w or '').split(';') if p.startswith('keyword is ') and p.split(' ')[2].isdigit()]
        got = {t for t in deck if t != card and c.execute(f"select 1 from flat_when where card=? and origin='own' and event in ({','.join('?' * len(evs))})",
                                                           [t] + list(evs)).fetchone()} if evs - {None} else set()
        # a trigger keyword names its own label ("Summon:"): only cards whose text has it (a spell's "when played" is no Summon)
        got = {t for t in got if any(re.search(r'\b' + re.escape(k.lower()) + r'\b', text_of(t)) for k in kws)}
        if got:
            plan[('repeat', card)][0].add(card); plan[('repeat', card)][3] |= got
            linked |= got | {card}

    for m, ref in c.execute(f"select card, card_ref from flat_do where act in ('summon','create','copy','play_card') and card in ({marks})", deck):
        if ref in D and ref != m: plan[('puts', ref)][0].add(m); plan[('puts', ref)][3].add(ref); linked |= {m, ref}
    # spells: every spell in the deck sets off "when you play a spell" triggers (Incant, Runeterra "when you cast a spell")
    spells = {i for i in deck if (c.execute('select category from card where id=?', (i,)).fetchone() or [''])[0] == 'spell'}
    sp_users = {x for (x,) in c.execute(f"select card from flat_when where origin='own' and event='played' and coalesce(obj_pick,'')!='self' "
                                         f"and (obj_kind='spell' or obj_with like '%category is spell%') and card in ({marks})", deck)}
    if spells and sp_users:
        plan[('spells', 0)][0] |= spells; plan[('spells', 0)][3] |= sp_users; linked |= spells | sp_users
    # types: cards that care about a type (target, count or trigger names it) and the cards that are or make it
    tname = {i: n for i, n in c.execute('select id, name from type where game=?', (game,))}
    care = collections.defaultdict(set); have = collections.defaultdict(set)
    for q in ("select card, on_with from flat_do where act not in ('create','summon','transform','copy','choose_card','play_card','revive') and 1",
              "select card, to_with from flat_do where 1", "select card, of_with from flat_if where 1",
              "select card, ev_obj_with from flat_if where 1", "select card, obj_with from flat_when where 1"):  # making one by
        for x, w in c.execute(q + f" and origin='own' and card in ({marks})", deck):                       # description is no caring
            for t in re.findall(r'(?<![a-z:])type is (\d+)', w or ''): care[int(t)].add(x)
    for x, t in c.execute(f'select card, type from card_type where card in ({marks})', deck): have[t].add(x)
    for x, w in c.execute(f"select card, on_with from flat_do where act in ('create','summon') and card in ({marks})", deck):
        for t in re.findall(r'(?<![a-z:])type is (\d+)', w or ''): have[int(t)].add(x)
    for x, t in c.execute(f"select d.card, ct.type from flat_do d join card_type ct on ct.card=d.card_ref where d.act in ('create','summon','copy') "
                          f"and d.card in ({marks})", deck): have[t].add(x)
    for t in care:
        if care[t] and any(have[t] - {x} for x in care[t]):  # another card is or makes one (Rakoans count each other)
            plan[('type', t)][0] |= have[t]; plan[('type', t)][3] |= care[t]; linked |= have[t] | care[t]
    out.append('Plan:')
    order = sorted(plan.items(), key=lambda x: -(len(x[1][0]) + len(x[1][1]) + len(x[1][2]) + len(x[1][3])))
    for key, (mk, own, lv, other) in order:
        if key[0] == 'repeat':
            out.append(f'- {mechanics.name(c, key[1])} makes these cards\' effects happen again: {names(c, other)}.'); continue
        if key[0] == 'spells':
            out.append(f'- Spells you play: {names(c, mk)}. Set off: {names(c, other)}.'); continue
        if key[0] == 'type':
            out.append(f'- {tname.get(key[1], "?")} cards: are or make them: {names(c, mk)}. Care about them: {names(c, other)}.'); continue
        if key[0] == 'puts':
            out.append(f'- More {mechanics.name(c, key[1])} in play: made by {names(c, mk)}.'); continue
        h, kw = key; ss = sides[key] - {''}; side = ss.pop() if len(ss) == 1 else ''
        if len(mk) + len(own) + len(lv) + len(other) < 3 and h in ('damaged', 'played', 'stat_changed'): continue
        line = f'- {(lambda t: t[:1].upper() + t[1:])(say(c, h, side, kw))}: made by {names(c, mk)}.'
        if own: line += f' Get value when they die: {names(c, own)}.'
        if lv: line += f' Level up from it: {names(c, lv)}.'
        if other: line += f' Use it: {names(c, other)}.'
        out.append(line)

    # champions: what levels them up
    for card in deck:
        conds = c.execute("""select i.test, i.event, i.ev_obj_side, i.of_side, i.op, i.n, i.ev_obj_with,
                             (select cd.attr from cond cd where cd.ability=i.ability and cd.test=i.test limit 1) from flat_if i join flat_do d
                             on d.ability=i.ability and d.card=i.card where d.act='level_up' and i.card=? and i.origin='own'""", (card,)).fetchall()
        if conds:
            ws = []
            for test, ev, es, fs, op, n, ew, attr in conds:
                if not ev: continue
                ref = [int(p.split(' ')[2]) for p in (ew or '').split(';') if p.startswith('card is ') and p.split(' ')[2].isdigit()]
                what = (f"{mechanics.name(c, ref[0])} " + say(c, ev, es or fs, None).split(' ', 2)[-1].replace('units ', '').replace('die', 'dies'))\
                    if ref else say(c, ev, es or fs, None)
                unit = f' {attr}' if attr else ' times'  # a total of a stat ("50+ damage"), else a number of times
                times = '' if not n else ' once' if n == 1 and not attr else f" ({int(n)}+{unit})" if op == 'ge' else f" ({int(n)}{unit})"
                ws.append(what + times)
            if ws: out.append(f'- {mechanics.name(c, card)} levels up when ' + ' or '.join(dict.fromkeys(ws)) + '.')

    # roles by mechanic (concepts): control, support for your units, card flow
    con = collections.defaultdict(set)
    for card, x in c.execute(f'select card, concept from flat_concept where card in ({marks})', deck): con[x].add(card)
    def role(title, keys, on_side, acts, extra_sql=''):
        cards = set()
        for k in keys: cards |= con.get(k, set())
        # the card must have an effect of that kind on that side (a landmark that can't block itself is no control)
        rows = lambda x: c.execute(f"""select on_with from flat_do where card=? and coalesce(on_side,'') in ({on_side}) {extra_sql} and
                 (concept in ({','.join('?' * len(keys))}) or act in ({','.join('?' * len(acts))}))""", (x, *keys, *acts)).fetchall()
        # a row that acts only on cards with a keyword no card of the deck has or is given acts on nothing here (Act III's
        # Gemified bonus of Emerald and Ruby Mox in an Act II deck)
        reachable = lambda w: all(int(k) in deck_kws for k in re.findall(r'(?<![a-z:])keyword is (\d+)', w or ''))
        cards = {x for x in cards if any(reachable(w) for (w,) in rows(x))}
        if cards: out.append(f'{title}: {names(c, cards)}.')
        return cards
    deck_kws = {k for (k,) in c.execute(f'select keyword from card_keyword where card in ({marks})', deck)} | \
               {k for (k,) in c.execute(f"select keyword_ref from flat_do where act in ('give_keyword','keyword_action') and keyword_ref is not null and card in ({marks})", deck)}
    # a unit striking enemy units by its own text (Bifurcated Strike, Sniper) controls them too: the strike's "on" is the striker,
    # its "to" the enemy, so it is added here (Inscryption Double Gunner, Sniper Bot)
    con['_strikes'] = {x for (x,) in c.execute(f"""select distinct card from flat_do where act='strike' and to_side='enemy' and to_kind in ('unit','unit_or_structure')
                       and origin in ('own','has_keyword') and card in ({marks})""", deck)}
    ctrl = role('Controls enemy units (damage, remove, stop, weaken)', CONTROL, "'enemy','any'",
                ('kill', 'obliterate', 'capture', 'stat_set', 'stun', 'silence', 'steal', 'transform', 'return_to_hand', 'damage', 'move', 'strike', 'challenge'))
    if con['_strikes'] - ctrl:
        ctrl |= con['_strikes']; out[-1 if out[-1].startswith('Controls enemy units') else len(out):] = [f'Controls enemy units (damage, remove, stop, weaken): {names(c, ctrl)}.']
    sup = role('Supports your units (stats, protection, combat keywords)', SUPPORT, "'mine'",
               ('stat_change', 'give_keyword', 'negate_damage', 'heal', 'grow', 'first_strike', 'double_strike'))
    flow = role('Card flow (draw, create, choose)', FLOW, "'mine','any',''", ('draw', 'create', 'choose_card', 'copy'))
    extra = role('Puts extra units into play', ('summon', 'revive'), "'mine','any',''", ('summon', 'revive'))
    # economy: more mana, or my cards made cheaper (Faeria Bargain: Bold Bargainer, Ogre Dance, Red Devil)
    eco = role('Pays for big cards (more mana, cheaper cards)', ('resource_gain', 'cost_reduction', 'cost_set'), "'mine','any',''",
               ('mana_gain', 'max_mana_change', 'cost_change', 'cost_set'), "and coalesce(on_pick,'')!='it'")  # not the card it just made
    # more or faster of the base resource (mana, Energy, Ember, faeria): its own line, so a ramp deck is named (Kaptain, 29 Oct 2026)
    ramp = {x for (x,) in c.execute(f"select distinct card from flat_concept where concept='base_resource_gain' and card in ({marks})", deck)}
    if ramp: out.append(f'More or faster base resource (ramp): {names(c, ramp)}.')
    big = [i for i in deck if (c.execute('select cost from card where id=?', (i,)).fetchone() or [None])[0] or 0]
    if eco and big:
        top = sorted(big, key=lambda i: -c.execute('select cost from card where id=?', (i,)).fetchone()[0])[:5]
        out.append(f'Most expensive cards they pay for: {names(c, set(top))}.')
    units = {i for i in deck if c.execute("select 1 from card where id=? and category in ('unit','hero','champion')", (i,)).fetchone()}
    if sup and units: out.append(f'Units that support cards can target: {len(units)} ({names(c, units)}).')

    # key cards and weak spots
    deg = collections.Counter()
    for key, (mk, own, lv, other) in plan.items():
        for x in mk | own | lv | other: deg[x] += 1
    if deg: out.append('Key cards (in most of the plan): ' + ', '.join(f'{mechanics.name(c, x)}' for x, _ in deg.most_common(5)) + '.')
    lack = []
    for card, ab, role_, h, side, kw, pick, kind, tw in uses:
        if h in EVERY_GAME or side == 'enemy' or by_rule.get(h, set()) - {card}: continue
        if not any((m != card or pick == 'self') and hh == h and (k is None or kw is None or k == kw) and fit(ms, side) and kinds_fit(mkd, kind) and not (pick == 'self' and mp == 'self' and m != card and not names_it(m, tw)) for (hh, k), ms_ in makes.items() for m, ms, mkd, mp, mw in ms_):
            lack.append(f'{mechanics.name(c, card)} waits for "{say(c, h, side, kw)}" and nothing else in the deck does it')
    alone = [i for i in deck if i not in linked | ctrl | sup | flow | extra | eco]
    weak = list(dict.fromkeys(lack)) + ([f'no clear role: {names(c, alone)}'] if alone else [])
    out.append('Weak spots: ' + ('; '.join(weak) + '.' if weak else 'none found.'))
    return out
