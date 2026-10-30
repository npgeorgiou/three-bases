"""A deck, a faction or a whole game as a network of cards (NETWORK_DRAFT.md), built from the stored rows only, the same way
for every game; lines only join cards of one game.
Nodes: the cards; their level-up forms; cards they make or put into play ("made by the deck").
Lines A -> B, each with a kind and a weight:
  waits     A makes something B waits for, counts or tests (A kills an ally, B acts when allies die)
  levels    as waits, but B's use is a level-up condition (weight x2)
  puts      A summons, creates, copies, revives or plays B
  repeats   A makes B's effects happen again (weight x2)
  rules     A changes how B works for as long as it lasts (cards in hand made Fast or cheaper, units that can't be blocked)
  boosts    A makes B stronger: stats given to it, more damage for it, or help with what B needs (power for damage, health
            for surviving, Overwhelm and Elusive for hitting the enemy player; HELPS)
  targets   A's effect on my side is aimed at cards like B (weight x0.5)
  type      A is or makes a type or kind of card B asks for (a Spider for Elise, a structure for Fortification Tonic)
  boosts    A raises my units' power, B counts damage my side deals (weight x0.5)
  levelsinto  a champion and its level-up form
Weight: 1 / how many cards of the game share the thing the line is about (rarer is stronger).
Usage (through ask.py): ask.py <game> network "<card>, <card>, ..." | network faction <name> | network game  [--json file]"""
import collections, json, math, os, re
import mechanics, deck_analysis

CACHE = {}
PUTS = ('summon', 'create', 'copy', 'play_card', 'revive', 'keyword_action')  # keyword_action with a card: planting it
RULES = ('cost_change', 'cost_set', 'can', 'cant', 'give_keyword', 'give_ability', 'give_type', 'remove_keyword')
KIND_CAT = {'unit': {'unit', 'hero'}, 'landmark': {'building'}, 'spell': {'spell'}, 'equipment': {'item'},
            'unit_or_structure': {'unit', 'hero', 'building'}, 'player': {'leader'},  # a leader card is its player (Duelyst General)
            'board': {'unit', 'hero', 'leader', 'building'}}  # a target of kind any / anything is on the board: never a spell or an artifact
CAT = {'follower': {'unit'}, 'champion': {'hero'}, 'unit': {'unit', 'hero'}, 'spell': {'spell'}, 'skill': {'ability'},
       'landmark': {'building'}, 'equipment': {'item'}}
PLAY_STATE = ('state', 'position', 'terrain', 'distance', 'targets', 'right_of', 'level', 'origin', 'countdown', 'damage')  # true or not only in play
EVERY_GAME = deck_analysis.EVERY_GAME


def cards_of(c, game):
    """per card: what filters can test before play (category, types, keywords, acts, numbers)"""
    if ('cards', game) in CACHE: return CACHE[('cards', game)]
    d = {}
    for i, n, cat, regions, pw, hp, stats, rar, cost in c.execute("""select id, name, category, regions, power, health, stats, rarity, cost from card
                                                              where game=? and is_keyword=0 and is_stub=0 and category!='tribe'""", (game,)):  # a type's own entry is no card
        try: st = json.loads(stats) if stats else {}
        except ValueError: st = {}
        if not isinstance(st, dict): st = {}
        if pw is None and hp is None and '|' in str(stats or ''):  # a level-up form keeps its stats as "power|health"
            a, b = str(stats).split('|', 1)
            pw, hp = (float(a) if a.strip().isdigit() else None), (float(b) if b.strip().isdigit() else None)
        strength = str(st.get('strength', '')).split('/')[0]
        d[i] = {'id': i, 'name': n, 'cat': cat, 'regions': set((regions or '').split(';')) - {''}, 'rarity': rar,
                'power': pw, 'health': hp, 'strength': float(strength) if strength.replace('.', '').isdigit() else None,
                'types': set(), 'kws': set(), 'acts': set(), 'cost': cost}  # cost: "a card that costs 7 or more" (was never read)
    for i, t in c.execute('select card, type from card_type'):
        if i in d: d[i]['types'].add(t)
    for i, k in c.execute('select card, keyword from card_keyword'):
        if i in d: d[i]['kws'].add(k)
    # what the card itself does, and what the keywords it uses as an action do (Drain deals damage); a status it gives (Frostbite
    # that hurts later) is not something the card does
    for i, a, con in c.execute("""select d.card, d.act, d.concept from flat_do d where d.origin='own' or (d.origin='uses_keyword' and exists
            (select 1 from flat_do k where k.card=d.card and k.origin='own' and k.act='keyword_action' and k.keyword_ref=d.via))"""):
        if i in d: d[i]['acts'] |= {a, con}
    # a level-up form is the same champion: it keeps the types of the card it levels from (Pyke (level 2) is still a Lurker)
    for a, b in c.execute("select src, dst from card_link where rel='transforms_into'"):
        if a in d and b in d and not d[b]['types'] and d[b]['name'].startswith(d[a]['name'] + ' (level'): d[b]['types'] |= d[a]['types']
    CACHE[('cards', game)] = d
    return d


def kw_id(c, game, word):
    r = c.execute('select id from card where game=? and is_keyword=1 and lower(name)=?', (game, word.lower())).fetchone()
    return r[0] if r else None


def number(c, n):
    if '.' in str(n): return float(n)  # a number written in by the network itself ("cost ge 7.0"); stored filters hold amount ids
    r = c.execute('select x, value from amount where id=?', (n,)).fetchone() if str(n).isdigit() else None
    return r[1] if r and r[0] == 'n' else None


def matches(c, game, card, kind, withs):
    """can card be one of the target's cards (kind plus filters); things only true in play count as possible"""
    skill = card['cat'] == 'ability' and kind == 'spell' and 'skill' in (withs or '')  # "spells or Skills": a skill is no spell otherwise
    if kind in KIND_CAT and card['cat'] not in KIND_CAT[kind] and not skill: return False
    if kind in ('mana', 'spell_mana', 'effect', 'position', None): return False
    groups = collections.defaultdict(list)  # several rows of one attr with op in = one of them
    for part in (withs or '').split(';'):
        b = part.split(' ')
        if len(b) < 3 or part.startswith('of:'): continue
        groups[(b[0], b[1])].append(b[2])
    for (attr, op), vals in groups.items():
        if attr in PLAY_STATE: continue
        hit = []
        for v in vals:
            if attr == 'category':
                if v.endswith('_spell'):
                    k = kw_id(c, game, v[:-6]); hit.append(card['cat'] == 'spell' and (k is None or k in card['kws']))
                else: hit.append(card['cat'] in CAT.get(v, {v}))
            elif attr == 'type': hit.append(v.isdigit() and int(v) in card['types'])
            elif attr == 'keyword': hit.append(v.isdigit() and int(v) in card['kws'])
            elif attr == 'card': hit.append(v.isdigit() and int(v) == card['id'])
            elif attr == 'does': hit.append(v in card['acts'])
            elif attr == 'region': hit.append(v in card['regions'] or v == 'own_regions')
            elif attr == 'rarity': hit.append(v == card['rarity'])
            elif attr == 'name_has':
                ref = mechanics.name(c, int(v)) if v.isdigit() and c.execute('select 1 from card where id=?', (int(v),)).fetchone() else v
                hit.append(str(ref).lower() in card['name'].lower())
            elif attr in ('power', 'health', 'strength', 'cost'):
                x, have = number(c, v), card.get(attr)
                if x is None or have is None: hit.append(True); continue
                hit.append({'lt': have < x, 'le': have <= x, 'eq': have == x, 'ge': have >= x, 'gt': have > x, 'in': have == x}.get(op, True))
            else: hit.append(True)
        ok = any(hit)
        if (op == 'not') == ok: return False
    return True


def kinds_fit(a, b):
    """a player is never a unit or a structure, a unit never a structure; open kinds fit everything"""
    if a in (None, '', 'any', 'anything', 'card', 'keyword') or b in (None, '', 'any', 'anything', 'card', 'keyword') or a == b: return True  # "used a keyword": matched by the keyword
    if 'unit_or_structure' in (a, b): return {a, b} <= {'unit_or_structure', 'unit', 'landmark'}
    return False


LAND_KINDS = {'land': {'land', 'prairie', 'lake', 'forest', 'mountain', 'desert', 'special_land'},
              'special_land': {'special_land', 'lake', 'forest', 'mountain', 'desert'}}  # terrain values that include others


def terrain_fit(want, have):
    """the ground a card counts or waits for ("a forest", "special lands") and the ground a card makes: one must include the
    other (a lake maker feeds "special lands", not "forests"); no ground named on either side fits"""
    w = {p.split(' ')[2] for p in (want or '').split(';') if p.startswith('terrain is ') or p.startswith('terrain in ')}
    h = {p.split(' ')[2] for p in (have or '').split(';') if p.startswith('terrain is ') or p.startswith('terrain in ')}
    if not w or not h: return True
    grow = lambda s: set().union(*(LAND_KINDS.get(x, {x}) for x in s))
    return bool(grow(w) & h) or bool(w & grow(h))


def names_fit(c, game, cards, want, have, ref):
    """the taker asks for one card or a name family ("an allied Lucian", "a Flashbomb Trap"): the maker must make that one"""
    asks = [p for p in (want or '').split(';') if p.split(' ')[:2] in (['card', 'is'], ['name_has', 'is'])]
    if not asks: return True
    if ref in cards: return matches(c, game, cards[ref], 'any', ';'.join(asks))
    return all(p in (have or '').split(';') for p in asks)


def colour_fit(want, have):
    """a resource of one colour (Inscryption gems: region Green, Orange, Blue): the maker gives that colour, or names none"""
    ask = {p for p in (want or '').split(';') if p.startswith('region ')}
    got = {p for p in (have or '').split(';') if p.startswith('region ')}
    return not ask or not got or bool(ask & got)


RESOURCE_WORD = {'secondary_resource': 'lets you gain the second resource (Bones)', 'gem': 'lets you gain a gem (Mox)',
                 'lane_resource': 'lets you gain the lane resource (Echo)'}
# what the first card of a line does, as an active verb (the line reads "A <does this>" for B)
ACT = {'dies': 'makes {who} units die', 'killed': 'kills {who} units', 'damaged': 'damages {who} units or players',
       'survives_damage': 'damages {who} units without killing them', 'nexus_damaged': 'damages {whos}', 'summoned': 'puts {who} units into play',
       'played': 'is played', 'cost_changed': 'changes card costs', 'drawn': 'makes you draw cards', 'discarded': 'makes you discard cards',
       'created': 'creates cards', 'given_keyword': 'makes {who} units get {kw}', 'stat_changed': "changes {who} units' stats",
       'healed': 'heals {who} units', 'attacks': 'makes {who} units attack', 'blocks': 'makes {who} units block', 'strikes': 'makes {who} units strike',
       'strikes_nexus': 'makes {who} units hit the enemy player', 'leaves_play': 'makes {who} cards leave play', 'recalled': 'returns {who} units to hand',
       'revived': 'brings {who} units back from the dead', 'levels_up': 'makes champions level up', 'obliterated': 'removes cards from the game',
       'transformed': 'transforms cards', 'mana_refilled': 'lets you gain mana', 'targeted': 'targets {who} cards', 'moves': 'makes {who} units move',
       'moves_onto': 'moves {who} units onto spaces', 'shuffled': 'shuffles cards into the deck', 'equipped': 'equips {who} units',
       'spell_resolves': 'casts spells', 'keyword_used': 'uses {kw}', 'sacrificed': 'has {who} units sacrificed', 'fights': 'makes {who} units fight',
       'harvests': 'makes your units harvest {who} wells', 'terrain_changed': 'changes the land', 'mana_refilled@secondary_resource': RESOURCE_WORD['secondary_resource'],
       'mana_refilled@gem': RESOURCE_WORD['gem'], 'mana_refilled@lane_resource': RESOURCE_WORD['lane_resource'],
       'trap_activated': 'activates traps', 'countdown_done': 'finishes countdowns'}
# the same, when the second card waits for it to happen to itself ("Last Words", "when this is damaged")
ACT_SELF = {'dies': 'kills it for its death effect', 'killed': 'kills it for its death effect', 'sacrificed': 'sacrifices it for its effect',
            'damaged': 'damages it for its effect', 'survives_damage': 'damages it without killing it, for its effect',
            'given_keyword': 'gives it {kw} for its effect', 'stat_changed': 'changes its stats for its effect', 'healed': 'heals it for its effect',
            'moves': 'moves it for its effect', 'moves_onto': 'moves it for its effect', 'attacks': 'makes it attack for its effect',
            'strikes': 'makes it strike for its effect', 'fights': 'makes it fight for its effect', 'recalled': 'returns it to hand for its effect',
            'revived': 'brings it back', 'transformed': 'transforms it for its effect', 'targeted': 'targets it for its effect'}


def act_say(c, h, side, kw, self_=False):
    """what the first card of a line does, in an active verb: 'makes your units die', 'kills it for its death effect'"""
    k = c.execute('select name from card where id=?', (kw,)).fetchone()[0] if kw else 'a keyword or status'
    t = ACT_SELF.get(h) if self_ else None
    t = t or ACT.get(h) or 'makes this happen: ' + deck_analysis.SAY.get(h, h.replace('_', ' '))
    return t.format(who=deck_analysis.who(side), whos={'mine': 'your Nexus or base', 'enemy': 'the enemy player'}.get(side, 'a player'),
                    kw=k).replace('any units', 'units').replace('any cards', 'cards')


# the kind of a "helps" line, from what the help does (the page names it): cheaper, stronger, a keyword, into place, a clear way
def help_kind(why):
    y = why.split(': ', 1)[1] if why.startswith('through ') and ': ' in why else why
    if 'cheaper' in y or y.startswith(('pays for it', 'can cost set')): return 'cheaper'
    if y.startswith('clears its line'): return 'clears'
    if y.startswith(('moves', 'lets it enter')): return 'moves'
    if y.startswith(('another attack', 'more health or protection', 'helps my units', 'helps it hit', 'more damage', 'fills your hand',
                     'empties your hand')): return 'waits'  # makes what it waits for happen more
    g = next((y.split(x, 1)[1] for x in ('can give it ', 'gives it ') if y.startswith(x)), None)
    if g is not None and not (g[:1] in '+-0123456789' or g.startswith(('X|', 'X '))): return 'keyword'
    return 'stronger'


OWN_LOSS = ('dies', 'killed', 'damaged', 'survives_damage', 'sacrificed')  # what fights do to my own units


def lines_of(c, game):
    """every waits / levels / puts / repeats / type line of the game: (a, b) -> [(kind, weight, why)]"""
    if ('lines', game) in CACHE: return CACHE[('lines', game)]
    cards = cards_of(c, game)
    out = collections.defaultdict(list)
    lvl = {a for (a,) in c.execute("select ability from flat_do where act='level_up'")}
    makes, takes = collections.defaultdict(set), collections.defaultdict(set)
    own_makes, lvl_needs = collections.defaultdict(set), collections.defaultdict(set)
    ab_card = dict(c.execute('select id, card from ability'))
    helps = adder_abilities(c, game)  # "your spells deal 1 extra damage" waits for nothing: it helps those cards (gives_lines)
    rule_name = {i: n.removeprefix('Game rule: ') for i, n in c.execute("select id, name from card where category='game_rule'")}
    harm_abs = harm_abilities(c)
    gives_kw = {(a, k): (ok, os_) for a, k, ok, os_ in c.execute("""select card, keyword_ref, on_kind, coalesce(on_side,'mine') from flat_do
                where act='give_keyword' and origin='own' and coalesce(on_side,'mine')='mine' and coalesce(on_pick,'')!='self'""")}
    cost_rules = {rule_name.get(e) for (e,) in c.execute('select entry from game_rule where cost_has is not null')}
    for card, origin, ab, role, h, side, kw, pick, kind, w, ref, ak, aw, via in c.execute(
            'select card, origin, ability, role, happening, side, keyword, pick, kind, obj_with, ref, actor_kind, actor_with, via from flat_ref'):
        if card not in cards: continue
        if role == 'makes':
            if pick == 'self' and not kind: kind = {'leader': 'player', 'hero': 'unit'}.get(cards[card]['cat'], cards[card]['cat'])  # it
            # moves itself as what it is: Azurite Lion moving is no General moving (Zeal)
            makes[h].add((card, side, kw, kind, pick, w, ref, rule_name.get(via, 'rules') if origin == 'game' else False))
            if origin != 'game': own_makes[card].add(h)
            continue
        # a keyword condition the card uses (Plunder, Reputation, Deep) is the card's own need (its rows sit on the card's own
        # ability, or on none for a keyword it has); the rows of a keyword it gives or uses on a target are not
        kwcond = role in ('condition', 'state') and ((origin == 'uses_keyword' and ab_card.get(ab) == card) or (origin == 'has_keyword' and ab is None))
        # where a keyword needs its holder to stand (Backstab: behind an enemy; Zeal: near my General): the holder's need, also when
        # the card gives the keyword to my unit or player (Mask of Shadows gives the General Backstab)
        if role == 'state' and h == 'moves' and origin == 'has_keyword' and (pick == 'self' or kind == 'player'): kwcond = True
        if role == 'state' and h == 'moves' and origin == 'uses_keyword' and pick == 'self' and (card, via) in gives_kw:
            kwcond = True; kind, side, pick = gives_kw[(card, via)][0], 'mine', None  # the holder is what the card gives it to
        cost = origin == 'game' and role == 'condition'  # a cost the game's rules set (Inscryption Bones, Blood, Mox): the card needs it
        if (origin != 'own' and not kwcond and not cost) or \
           (pick == 'self' and h in ('played', 'summoned')) or pick == 'actor_self': continue  # "I've killed 4": only the card itself
        if ab in helps: continue
        if role == 'trigger' and (ab in harm_abs or ab in protect_abilities(c)): continue  # "take 1 damage when summoned" (Kujata): it
        # hurts my cards, it wants none; "the first time your General takes damage, prevent 2": it protects, it wants no damage. (A
        # trigger that helps the card that sets it off still waits for more of it from other cards: draws for Janna's discounts; the
        # card itself is no enabler of it: played_lines and the type lines skip it, Golem Metallurgist)
        if ab in lvl: lvl_needs[card].add(h)
        takes[h].add((card, 'mine' if pick == 'self' else side, kw, kind, pick, w, ab in lvl, role, (ak, aw), cost))
    state_ev = collections.defaultdict(set)  # a state and the happenings that put things in it (damaged <- damaged)
    for v, cs in c.execute("select value, causes from vocab where field='state' and coalesce(causes,'')!=''"):
        state_ev[v] |= {x.split(':')[0] for x in cs.split(';')}
    # damage to my side by amount: damage as big as a card's health kills it, so it never survives it (Sunburst deals 6, Braum has 6)
    hits = collections.defaultdict(list)
    for m, ps in c.execute("select card, params from flat_do where act='damage' and origin='own' and coalesce(on_side,'any') in ('mine','any')"):
        x = dict(p.split('=', 1) for p in (ps or '').split(';') if '=' in p).get('amount', '')
        hits[m].append(float(x) if x.replace('.', '').isdigit() else None)
    killers = {a for (a,) in c.execute("select card from flat_do where act in ('kill','sacrifice','strike','start_attack') and origin='own'")}
    def weak(m, t):
        life = cards[t]['health'] or cards[t]['strength']
        return bool(life) and bool(hits.get(m)) and all(x is not None and x < life for x in hits[m])
    def lethal(m, t):
        life = cards[t]['health'] or cards[t]['strength']
        return bool(life) and bool(hits.get(m)) and all(x is not None and x >= life for x in hits[m])
    fighters = {a for (a,) in c.execute("select card from flat_do where act in ('strike','first_strike','double_strike','start_attack')")}
    leader_game = c.execute("select 1 from card where game=? and category='leader' limit 1", (game,)).fetchone() is not None
    rule_fighters = fighters | {a for (a,) in c.execute(f"""select ck.card from card_keyword ck join card k on k.id=ck.keyword join vocab v on
            v.field='keyword' and v.value in (k.name, k.game || ':' || k.name) where v.tree in ('multi_attack', 'aoe_damage', 'excess_damage')""")}  # it fights more
    # or hits more than one (Celerity, Frenzy, Overwhelm); Ranged or Quick Attack only change how one attack goes
    def doer_fits(m, actor, h=None):
        """who must do it ("an ally deals damage", "allied Pykes"): the card itself, or a card that makes such a unit fight; the
        player does most things through any card ("whenever you replace a card"), but fights only as its leader ("whenever your
        General attacks": the General card, Duelyst)"""
        ak, aw = actor
        if ak == 'player' and not aw and h not in ('attacks', 'strikes', 'killed', 'strikes_nexus', 'fights'): return True
        if ak not in KIND_CAT and not aw: return True
        k = ak if ak in KIND_CAT else 'any'
        if matches(c, game, cards[m], k, aw): return True
        return ak in ('unit', None) and m in fighters and not any(p.split(' ')[0] in ('card', 'name_has', 'type') for p in (aw or '').split(';'))
    # a card whose own triggers make what its level-up counts (Ashe frostbites when she attacks): feeding the trigger levels it
    selffeed = {t for t in lvl_needs if lvl_needs[t] & own_makes[t]}
    # a stat it tests or uses ("restore that minion's Health"): only a change of that stat feeds it (+Attack adds no Health)
    stat_need = collections.defaultdict(set)
    for t, at in c.execute("select card, attr from flat_if where test in ('stat','amount_stat') and attr in ('health','power')"): stat_need[t].add(at)
    stat_made = collections.defaultdict(set)
    for m, ps in c.execute("select card, params from flat_do where act in ('stat_change','stat_set','grow','swap_stats')"):
        stat_made[m] |= {x.split('=')[0] for x in (ps or '').split(';') if x.split('=')[0] in ('power', 'health', 'strength')} or {'power', 'health'}
    for h, ts in takes.items():
        carers = collections.defaultdict(set)
        for t, _, tk, *_ in ts: carers[tk].add(t)
        for m, ms, mk, mkind, mpick, mw, mref, rule in makes.get(h, ()):
            for t, ts_, tk, tkind, tpick, tw, lv, role, actor, cost in ts:
                if m == t or not mechanics.FIT(ms, ts_) or not (mk is None or tk is None or mk == tk): continue
                if not kinds_fit(mkind, tkind): continue
                if mpick == 'self' and tpick == 'self': continue  # each card about itself ("when I level up"): no link between two cards
                if not names_fit(c, game, cards, tw, mw, mref): continue
                if not terrain_fit(tw, mw): continue
                if tpick == 'self' and mpick != 'self':  # done to one of my units that must be this card ("give the Demon Wing Flying",
                    who = ';'.join(p for p in (mw or '').split(';') if p.split(' ')[:2] in (['card', 'is'], ['type', 'is'], ['type', 'in'],
                                                                                        ['name_has', 'is']))  # "another Rakoan")
                    if who and not matches(c, game, cards[t], 'any', who): continue
                if tkind in RESOURCE_WORD and not colour_fit(tw, mw): continue  # a Green Mox cost is paid by a Green gem only
                if mpick == 'self':  # what a card does to itself feeds only a need its own kind fits ("the strongest friendly Dragon")
                    own = ';'.join(p for p in (tw or '').split(';') if p.split(' ')[:2] in (['type', 'is'], ['type', 'in'], ['card', 'is'], ['name_has', 'is'], ['keyword', 'is']))
                    if own and not matches(c, game, cards[m], 'any', own): continue
                if h == 'survives_damage' and tpick == 'self' and lethal(m, t): continue
                if h == 'dies' and tpick == 'self' and m in hits and m not in killers and weak(m, t): continue  # 1 damage kills no 4-health unit
                if h == 'stat_changed' and role == 'condition' and stat_need.get(t) and stat_made.get(m) and \
                        not (stat_need[t] & stat_made[m]) and 'strength' not in stat_made[m]: continue
                if not doer_fits(m, actor, h): continue
                # my units are hurt or die in fights by the rules: every unit would feed "when a friendly unit dies" (Soul Eater,
                # Shaytan Monstrosity); only cards that hurt or kill my units do (Kaptain 30 Oct 2026); a cost the rules pay stays
                if rule and not cost and h in OWN_LOSS and ms != 'enemy': continue
                # a rule that needs a place ("harvest a well next to it": an enemy well is deep in enemy ground) is done by the units
                # that get there, not by every unit: what moves them is the help (HELPS movement); Gabrian Archon -> Wavecrash Colossus
                if rule and not cost and 'position ' in (mw or ''): continue
                if rule == 'units fight' and 'origin not combat' in (tw or ''): continue  # "non-combat damage": fighting is combat  # "allied Pykes have dealt damage": the damage of a spell or another unit is not it
                need = {e for p in (tw or '').split(';') if p.startswith('state is ') for e in state_ev.get(p[9:], ())} - {h}
                if need and h in ('played', 'summoned', 'drawn', 'created') and not need & own_makes[m]: continue  # "8 cost reduced cards
                # played": playing a card no one made cheaper is not it (a unit healed is damaged by the enemy too: no such need)
                w = 1.0 / len(carers[tk] | (carers[None] if tk else set()))
                say = act_say(c, h, ts_, tk, self_=tpick == 'self')
                if mpick == 'self' and h == 'dies': say = 'dies, comes back and dies again' if mref == m else 'dies by its own effect'
                if mpick == 'self' and h == 'given_keyword' and mk: say = f'has {mechanics.name(c, mk)}'  # Manta Rider has Flying
                if tkind == 'player' and leader_game: say = one_leader(say)  # "whenever your General attacks"
                if h == 'mana_refilled' and tkind in RESOURCE_WORD: say = RESOURCE_WORD[tkind]  # not mana: say which resource
                if cost and rule in cost_rules: continue  # another card paying its own cost pays nothing for this one
                if cost: say += ' (pays its cost)'
                if rule and not cost and not lv and (rule != 'units fight' or m not in rule_fighters) and actor[0] != 'player' and \
                        not (tkind == 'player' and h in ('attacks', 'strikes', 'fights')) and not any(
                        p.split(' ')[0] in ('card', 'name_has', 'type', 'keyword') for p in (tw or '').split(';')):
                    continue  # every unit fights by the rules: that is no combo (Punish waits for damaged enemies; any attacker does it). A
                    # level-up count stays (Kaptain, n53: attackers hitting the Nexus level Gangplank). Only a
                    # card whose own ability makes it fight (Celerity, Ranged, "this fights") or a need that names who (my General) keeps the line
                if rule:  # every unit does it by the game's rules (attacks, hits the enemy Nexus): weaker than a card that says so
                    w *= 0.25; say += ' (by fighting)' if rule == 'units fight' else f" (by the game's rule: {rule})"
                if lv: out[(m, t)].append(('levels', 2 * w, say + ' (levels it up)'))
                elif role == 'trigger' and t in selffeed: out[(m, t)].append(('levels', w, say + ' (it levels up from what it then does)'))
                # it reacts to or counts a happening: "does what it waits for"; it needs a thing to be there ("while you control
                # another flying creature", "if Krog has died"): "enables"
                else: out[(m, t)].append(('type' if role == 'state' else 'waits', w, say))
    put = [(m, ref, act) for m, ref, act in c.execute(f"select card, card_ref, act from flat_do where act in ({','.join('?' * len(PUTS))})", PUTS)
           if m in cards and ref in cards and m != ref]
    put += [(m, ref, 'skill') for m, ref in c.execute("select l.src, l.dst from card_link l join card d on d.id=l.dst where l.rel='generates' "
                                                       "and d.category='ability'") if m in cards and ref in cards]  # a unit's skill
    put += [(m, ref, 'own_spell') for m, ref in c.execute("select l.src, l.dst from card_link l join card s on s.id=l.src where l.rel='generates' "
                                                           "and s.category='leader'") if m in cards and ref in cards]  # a General's spell
    putters = collections.Counter(ref for _, ref in {(m, ref) for m, ref, _ in put})
    for m, ref, act in put:
        out[(m, ref)].append(('puts', 1.0 / putters[ref], {'summon': 'summons', 'create': 'creates', 'copy': 'copies', 'revive': 'brings back',
                                                           'play_card': 'plays', 'keyword_action': 'plants', 'skill': 'casts its skill',
                                                           'own_spell': 'casts its own spell'}[act]))
    # a draw that names what it takes from the deck ("draw the top legend", "draw a Beast") finds those cards
    # (and a summon from the hand or deck by what it is: "summon a minion with Dying Wish from your action bar", Unseven); "a copy
    # of it" is a card the earlier effect can pick (Lifestream heals a minion, then draws a copy of it: minions only)
    tutors = [(m, ab, sq, act, k, z, w) for m, ab, sq, act, k, z, w in c.execute("""select card, ability, seq, act, on_kind, on_zone, on_with from flat_do
              where origin='own' and coalesce(on_side,'mine')='mine' and coalesce(on_with,'')!='' and (act='draw' or (act in
              ('summon','play_card') and on_zone in ('hand','deck') and card_ref is null))""") if m in cards]
    for m, ab, sq, act, k, z, w in tutors:
        if 'state is copy_of_it' in (w or ''):
            prev = c.execute("select on_kind, on_with from flat_do where card=? and ability=? and seq<? and origin='own' order by seq desc",
                             (m, ab, sq)).fetchone()
            if prev: k, w = prev[0], ';'.join(x for x in (prev[1] or '').split(';') if x.split(' ')[0] in ('card', 'type', 'category', 'keyword', 'name_has'))
        hit = [t for t, x in cards.items() if t != m and matches(c, game, x, k if k in KIND_CAT else 'any', w)]
        say = 'draws it from the deck' if act == 'draw' else f"puts it into play from {'the hand' if z == 'hand' else 'the deck'}"
        for t in hit: out[(m, t)].append(('puts', 1.0 / max(1, len(hit)), say))
    for a, b in c.execute("select src, dst from card_link where rel='transforms_into'"):
        if a in cards and b in cards: out[(a, b)].append(('levelsinto', 1.0, 'levels into'))
    # repeats: Allied Attack effects activate twice -> every card with its own Attack effect
    trig = {k: e for k, e in c.execute('select t.keyword, v.event from keyword_trigger t join event v on v.id=t.event')}
    rep = collections.defaultdict(set)
    for card, w in c.execute("select card, on_with from flat_do where act in ('repeat','increase_effect')"):
        if card not in cards: continue
        for p in (w or '').split(';'):
            b = p.split(' ')
            if len(b) == 3 and b[0] == 'keyword' and b[1] == 'is' and b[2].isdigit() and int(b[2]) in trig: rep[trig[int(b[2])]].add((card, int(b[2])))
    for ev, ms in rep.items():
        users = {t for (t,) in c.execute("select card from flat_when where event=? and origin='own' and (actor_pick='self' or obj_pick='self')", (ev,))
                 if t in cards}
        for m, k in ms:
            for t in users - {m}:
                out[(m, t)].append(('repeats', 2.0 / len(ms), f'repeats its {mechanics.name(c, k)} effects'))
    # types: a card that asks for a type is fed by cards of that type and cards that make them
    asks, named = collections.defaultdict(set), collections.defaultdict(set)  # named: a card it names ("if a Chime is attacked")
    asked = collections.defaultdict(set)  # named by a trigger or condition: it waits for or asks for that card
    cleanup = {a for (a,) in c.execute("""select ability from flat_do group by ability having sum(case when act in
               ('kill','obliterate','sacrifice') and on_pick='self' then 0 else 1 end)=0""")}  # "when Krog comes, destroy this"
    for card, w, src, act, kw, ps in c.execute("""select card, coalesce(on_with,'') || ';' || coalesce(to_with,''), 'do', act, keyword_ref, params
                                from flat_do where coalesce(on_side,'mine')!='enemy'
                                and act not in ('create','summon','transform','copy','choose_card','play_card','revive')
                                union all select card, obj_with, 'when', null, null, ability from flat_when union all select card, coalesce(of_with,'') || ';' ||
                                coalesce(ev_obj_with,''), 'if', of_zone, null, ability from flat_if where coalesce(of_side,'mine')!='enemy'"""):
        if src == 'when' and ps in help_abilities(c): continue
        if src == 'do' and (helps_it(c, act, kw, ps) or act in HELP_ACTS): continue  # Oakenheart "your Mechs have +1/+1" helps the
        # Mechs (an aimed line from it); it does not ask for them
        if card not in cards: continue
        for part in (w or '').split(';'):
            b = part.removeprefix('of:').split(' ')
            if len(b) == 3 and b[0] == 'type' and b[1] in ('is', 'in') and b[2].isdigit(): asks[int(b[2])].add(card)
            if len(b) == 3 and b[0] == 'card' and b[1] in ('is', 'in') and b[2].isdigit():
                named[int(b[2])].add(card)
                if (src == 'when' and ps not in cleanup) or (src == 'if' and act in (None, 'board') and ps not in harm_abilities(c)):  # "if you have another
                    asked[int(b[2])].add(card)  # Wraithling"; not "if Krog is in your deck, draw him", nor "if Krog is here, destroy this"
    has = collections.defaultdict(set)
    for i, x in cards.items():
        for t in x['types']: has[t].add((i, 'is'))
    for m, ref in c.execute(f"select card, card_ref from flat_do where act in ({','.join('?' * len(PUTS))}) and card_ref is not null", PUTS):
        if m in cards and ref in cards:
            for t in cards[ref]['types']: has[t].add((m, 'makes'))
    # cards made by description ("2 random Imps", "a random Celestial card") are of the type they name
    for m, w in c.execute(f"select card, on_with from flat_do where act in ({','.join('?' * len(PUTS))}, 'choose_card') and card_ref is null "
                          "and on_with like '%type is%' and coalesce(on_side,'mine') in ('mine','any')", PUTS):
        if m in cards:
            for p in w.split(';'):
                b = p.split(' ')
                if len(b) == 3 and b[:2] == ['type', 'is'] and b[2].isdigit(): has[int(b[2])].add((m, 'makes'))
    for t, ts in asks.items():
        tn = c.execute('select name from type where id=?', (t,)).fetchone()
        for m, how in has.get(t, ()):
            for x in ts - {m}: out[(m, x)].append(('type', 1.0 / len(ts), f'{"is" if how == "is" else "makes"} {"an" if tn and tn[0][:1] in "AEIOU" else "a"} {tn[0] if tn else "card of the type"} it asks for'))
    for t, ts in named.items():  # the named card itself, or a card that makes it
        name = cards[t]['name'] if t in cards else None
        if not name: continue
        own = {m for m, ref, _ in put if ref == t}  # a card naming what it makes itself acts on its own product (Blazing Spines'
        for m, how in [(t, 'is')] + [(m, 'makes') for m in own]:  # walls "can attack")
            for x in ts - {m} - (own - asked[t]):
                if x in asked[t] or not any(l[0] == 'puts' for l in out.get((x, m), ())):  # what it makes itself is no help to it,
                    # unless it asks for another one ("if you have another Wraithling")
                    out[(m, x)].append(('type', 1.0 / len(ts), f'{how} the {name} it names'))
    CACHE[('lines', game)] = out
    return out


NOT_AIMED = PUTS + ('repeat', 'increase_effect', 'level_up', 'draw', 'discard', 'shuffle_into_deck', 'put_on_top', 'look', 'reveal',
                    'choose_card', 'choose_one', 'random_one')
BOOST = {'repeat': ('repeats', 2.0, 'repeats its effects'), 'increase_effect': ('boosts', 1.0, 'makes its effect bigger'),
         'copy': ('puts', 1.0, 'copies it')}  # effects on a group of cards picked by kind or filter (Doctor Mia, Ava Achiever, Teemo 2)
NAMES_ONE = ('card is', 'keyword is', 'type is', 'name_has is')


HELP_ACTS = ('can', 'ready', 'countdown_advance', 'give_ability', 'heal', 'negate_damage', 'cost_set', 'move', 'swap')
BUFFS = ('stat_gain', 'attack_gain', 'defence_gain', 'temporary_buff', 'permanent_growth', 'shield', 'immunity', 'evasion', 'first_strike',
         'multi_attack', 'regeneration', 'cheat_death', 'damage_reduction', 'excess_damage', 'lifesteal', 'block_armor', 'counterattack',
         'target_choice', 'aoe_damage', 'ranged', 'flanking', 'haste', 'taunt', 'placement_rules')  # keyword concepts that only make a unit stronger


def helps_it(c, act, kw, ps):
    """an effect that leaves my card better off: stats up, a buff or movement keyword, cheaper, healed, protected"""
    p = dict(x.split('=', 1) for x in (ps or '').split(';') if '=' in x)
    if act in ('stat_change', 'grow'): return any(k in p and not p[k].startswith('-') for k in ('power', 'health', 'strength'))
    if act == 'give_keyword': return bool(kw) and (buff_keyword(c, kw) or (c.execute("select v.tree from card k join vocab v on "
        "v.field='keyword' and v.value in (k.name, k.game || ':' || k.name) where k.id=?", (kw,)).fetchone() or [''])[0] == 'movement')
    if act == 'cost_change': return p.get('cost', '').startswith('-')
    return act in ('cost_set', 'heal', 'negate_damage', 'give_ability', 'damage_reduction', 'countdown_advance', 'ready')


def buff_keyword(c, kw):
    r = c.execute("select v.tree from card k join vocab v on v.field='keyword' and v.value in (k.name, k.game || ':' || k.name) where k.id=?", (kw,)).fetchone()
    return bool(r) and r[0] in BUFFS


AIM = {'give_keyword': 'can give it {kw}', 'keyword_action': 'can {kw} it', 'heal': 'can heal it', 'damage': 'can damage it',
       'kill': 'can kill it', 'strike': 'can make it strike', 'return_to_hand': 'can return it to hand', 'start_attack': 'can make it attack',
       'transform': 'can transform it', 'copy': 'can copy it', 'revive': 'can bring it back', 'move': 'can move it',
       'cost_change': 'can make it cheaper', 'stat_set': 'can set its stats', 'give_ability': 'can give it an ability',
       'can': 'lets it do more', 'cant': 'can stop it from acting', 'countdown_advance': 'can speed up its countdown',
       'give_random_keyword': 'can give it a random keyword', 'return_card': 'can bring it back to hand', 'ready': 'can ready it',
       'damage_reduction': 'can shield it from damage', 'capture': 'can take control of it', 'sacrifice': 'can sacrifice it'}


def aim_said(act, kw, ps):
    """a chosen effect on my side in plain words ("can give it +2|+0", "can heal it")"""
    if act in ('stat_change', 'grow'): return 'can ' + stats_said(ps).replace('gives', 'give', 1)
    return AIM.get(act, 'can ' + act.replace('_', ' ') + ' it').format(kw=kw or 'a keyword')


def stats_said(ps):
    """'power=1.0;health=0.0' -> 'gives it +1|+0'; a stat change with other numbers (strength) -> 'gives it +N strength'"""
    d = dict(p.split('=', 1) for p in (ps or '').split(';') if '=' in p)
    num = lambda x: (x.removesuffix('.0') if x.lstrip('-').replace('.', '').isdigit() else 'X')
    sign = lambda x: x if x.startswith('-') or x == 'X' else '+' + x
    if 'power' in d or 'health' in d: return f"gives it {sign(num(d.get('power', '0')))}|{sign(num(d.get('health', '0')))}"
    k = next(iter(d), None)
    return f'gives it {sign(num(d[k]))} {k}' if k else 'changes its stats'


def aimed_rows(c, game):
    """effects on my side aimed at cards (not the card itself): (card, act, kind, pick, with, kw, rule) and how many cards of the
    game make the same one (act, kind, keyword, rule or not). Effects that repeat, boost or copy a group of cards count on
    either side when the group is named (traps on enemy cards are still mine)."""
    if ('aimed', game) in CACHE: return CACHE[('aimed', game)]
    cards = cards_of(c, game); rows = []
    for a, act, kind, side, pick, w, lasts, kw, cref, zone, ps in c.execute("""select card, act, on_kind, on_side, on_pick, on_with, lasts,
            keyword_ref, card_ref, on_zone, params from flat_do where origin in ('own','has_keyword') and coalesce(on_pick,'') not in ('self','it','owner','actor')
            and not (act = 'can' and on_kind = 'player' and param_event in ('shuffled','drawn','discarded','played','summoned'))
            and not (act = 'give_ability' and on_kind = 'player')  -- a delayed effect the player gets ("if it dies this turn") is no help to the leader card"""):
        # "you may replace an additional card": the player handles more cards, its leader card gets nothing
        if a not in cards: continue
        if zone in ('hand', 'deck', 'deck_top', 'deck_bottom') or act in ('cost_change', 'cost_set'): CACHE.setdefault(('handrows', game), set()).add((a, act))
        if act == 'increase_effect' and kw and 'keyword is' not in (w or ''):  # "Impact deals 2 more": the cards with Impact
            w = ';'.join(x for x in (w, f'keyword is {kw}') if x); kind = kind if kind in KIND_CAT else 'any'
        named = any(p.startswith(NAMES_ONE) for p in (w or '').split(';'))
        if act in BOOST and cref is None and (side in ('mine', 'any', None) or named):
            if kind in KIND_CAT or named or kind in ('card', 'effect', 'any', 'anything'): rows.append((a, act, kind, w, kw, 'boost', named, ps))
            continue
        if act in NOT_AIMED or (side not in ('mine', 'any') and not (side is None and helps_it(c, act, kw, ps))): continue  # no side
        # (N18: "a creature", either side): help is aimed at mine (Khalim's Training), harm at enemies
        # a lasting change to all my cards of a kind, or to them in hand and deck too ("grant allies everywhere +1|+0"): it rules them
        rule = pick == 'all' and side == 'mine' and act not in NOT_AIMED and ((act in RULES and lasts in ('while', 'permanent', None)) or
               lasts in ('while', 'permanent') or zone in ('everywhere', 'hand', 'deck'))
        # help, not a rule change: stats given, a cheaper cost, a buff keyword (Rage, Armor, Barrier); these make it stronger
        if rule and act == 'stat_change': rule = 'help ' + stats_said(ps)
        elif rule and act == 'cost_change' and '=-' in (ps or ''): rule = 'help makes it cheaper'
        elif rule and act == 'give_keyword' and kw and buff_keyword(c, kw): rule = f'help gives it {mechanics.name(c, kw)}'
        elif rule and act == 'copy_keywords': rule = 'help gives it keywords'
        narrowed = any(p.split(' ')[0] not in PLAY_STATE + ('card',) and p.split(' ')[1:2] != ['not'] for p in (w or '').split(';') if p and not p.startswith('of:'))
        cut = dict(x.split('=', 1) for x in (ps or '').split(';') if '=' in x).get('cost', '')
        if act == 'cost_change' and not narrowed and kind in ('card', 'any') and cut.startswith('-') and cut[1:].replace('.', '').isdigit() \
                and float(cut[1:]) >= 2:  # "a random card in your hand costs 7 less": a cut that big is used in full by the cards
            w = ';'.join(x for x in (w, f'cost ge {cut[1:]}') if x); narrowed = True  # costing at least that much (Bargain decks)
        if (side == 'any' and not rule and not helps_it(c, act, kw, ps)) or \
                (kind not in KIND_CAT and not (kind in ('card', 'any', 'anything') and (narrowed or named)) and not
                 (kind in ('any', 'anything') and zone in (None, 'board') and pick in ('chosen', 'random')
                  and any(x['cat'] == 'leader' for x in cards.values()))): continue  # "restore 2 Health to anything": a unit or my General
        rows.append((a, act, kind, w, kw, rule, narrowed or named or kind == 'player', ps))  # "your General": one card, the leader
    makers = collections.defaultdict(set)
    for a, act, kind, w, kw, rule, *_ in rows: makers[(act, kind, kw, rule if rule in (True, False, 'boost') else True)].add(a)
    CACHE[('aimed', game)] = rows, makers
    return rows, makers


def givers_of(c, game, k, nodes):
    """the nodes that give keyword or status k to my side or use it there (Fledgling Imp applies Rage to friendly units)"""
    marks = ','.join('?' * len(nodes))
    return {a for (a,) in c.execute(f"""select distinct card from flat_do where keyword_ref=? and act in ('give_keyword','keyword_action')
            and origin='own' and coalesce(on_side,'mine') in ('mine','any') and card in ({marks})""", [k] + list(nodes))}


PLACE_WORDS = {'sides': 'next to it', 'bordering': 'next to it', 'surrounding': 'around it', 'same_lane': 'in its lane',
               'in_circuit': 'in its circuit', 'same_space': 'on its space', 'same_row': 'in its row', 'same_column': 'in its column',
               'in_front': 'in front of it', 'behind': 'behind it', 'ahead': 'ahead of it', 'straight_line': 'in a line from it'}


def where(w):
    """the place a target filter asks for, measured from the card itself, in plain words (' when next to it')"""
    for p in (w or '').split(';'):
        b = p.split(' ')
        if b[:2] == ['position', 'is'] and len(b) == 3 and b[2] in PLACE_WORDS: return f' (when {PLACE_WORDS[b[2]]})'
    return ''


def aimed(c, game, nodes, broad):
    """rules and targets lines from the nodes to the nodes (a filter is checked against each card); broad=False drops lines
    whose target is every card of its kind, which say nothing about which cards belong together"""
    cards = cards_of(c, game); out = collections.defaultdict(list)
    kwn = lambda k: mechanics.name(c, k) if k else ''
    rows, makers = aimed_rows(c, game)
    for a, act, kind, w, kw, rule, narrowed, ps in rows:
        if a not in nodes or (not narrowed and not broad): continue
        k = 'any' if kind in ('effect', 'card') else 'board' if kind in ('any', 'anything') else kind
        if kind == 'effect':  # an effect picked by its keyword ("Trap effects"): the cards that carry the keyword
            w = ';'.join(p for p in (w or '').split(';') if p.startswith('keyword'))
        hits = [b for b in nodes if b != a and b in cards and matches(c, game, cards[b], k, w)]
        if (a, act) in CACHE.get(('handrows', game), ()):  # a card in hand or a cost: Wraithlings summoned onto the board are never there
            hits = [b for b in hits if not board_only(c, nodes, b)]
        n = len(makers[(act, kind, kw, rule if rule in (True, False, 'boost') else True)])
        if rule == 'boost':
            kind_, x, why = BOOST[act]
            for b in hits: out[(a, b)].append((kind_, x / n, why))
            for k in (int(p.split(' ')[2]) for p in (w or '').split(';') if p.startswith('keyword is ') and p.split(' ')[2].isdigit()):
                for b in givers_of(c, game, k, nodes) - set(hits) - {a}:  # Rage made stronger: the cards that give Rage too
                    out[(a, b)].append((kind_, x / n, f'makes the {kwn(k)} it gives stronger'))
            continue
        what = rule[5:] if isinstance(rule, str) and rule.startswith('help ') else {'give_keyword': f'gives it {kwn(kw)}', 'cost_change': 'changes its cost', 'cost_set': 'sets its cost',
                'can': 'lets it do more', 'cant': 'stops it doing something', 'give_ability': 'gives it an ability',
                'give_type': 'gives it a type', 'remove_keyword': f'removes {kwn(kw)}', 'copy_keywords': 'gives it keywords',
                'mark': 'marks it'}.get(act, act.replace('_', ' '))
        pev = dict(p.split('=', 1) for p in (ps or '').split(';') if '=' in p).get('event')
        if act in ('can', 'cant') and pev:  # say what it may or may not do: "lets it be summoned there", "stops it moving"
            what = {('can', 'summoned'): 'lets it be summoned in more places', ('can', 'played'): 'lets it be played in more places',
                    ('can', 'moves'): 'lets it move more', ('cant', 'moves'): 'stops it moving', ('cant', 'attacks'): 'stops it attacking',
                    ('cant', 'targeted'): 'protects it from targeting'}.get((act, pev), what + f' ({pev})')
        at = where(w)  # who benefits from a place: "when next to it", "in its circuit" (positional games; Inscryption Leader)
        for b in hits:
            if rule: out[(a, b)].append(('boosts' if isinstance(rule, str) else 'rules', 1.0 / n, what + at))  # stats given make it stronger; the rest change how it works
            elif helps_it(c, act, kw, ps): out[(a, b)].append(('boosts', 0.5 / max(1, len(hits)), aim_said(act, kwn(kw), ps) + at))
            else: out[(a, b)].append(('targets', 0.5 / n, aim_said(act, kwn(kw), ps) + at))  # help aimed at one card of a kind helps
            # each card it can hit (Oakling's +5|+5 to a random green creature, Horsemaster's Charge, a 7 cost cut), weight shared
    return out


def board_only(c, nodes, b):
    """a card the deck only makes on the board (summoned tokens): never in the hand or deck"""
    if not nodes.get(b) or cards_of(c, c.execute('select game from card where id=?', (b,)).fetchone()[0])[b]['cat'] not in ('unit', 'hero', 'building'):
        return False  # a skill or spell cast is played
    key = ('board_only', b)
    if key not in CACHE:
        CACHE[key] = not c.execute("""select 1 from flat_do where card_ref=? and (act in ('create','copy') and coalesce(eff_zone,'hand')
                in ('hand','deck','deck_top','deck_bottom') or (act='transform' and on_zone in ('hand','deck','everywhere')))""", (b,)).fetchone()
    return CACHE[key]


def kind_count(c, game, kind, w):
    key = ('count', game, kind, w)
    if key not in CACHE: CACHE[key] = max(1, sum(1 for x in cards_of(c, game).values() if matches(c, game, x, kind, w)))
    return CACHE[key]


def level_abilities(c):
    if 'lvl' not in CACHE: CACHE['lvl'] = {a for (a,) in c.execute("select ability from flat_do where act='level_up'")}
    return CACHE['lvl']


def one_leader(say):
    """'your units attack' -> 'your leader attacks' (a need about the player in a game whose player is a leader card)"""
    verb = {'attack': 'attacks', 'die': 'dies', 'take': 'takes', 'move': 'moves', 'are': 'is', 'have': 'has', 'get': 'gets',
            'enter': 'enters', 'strike': 'strikes', 'kill': 'kills', 'survive': 'survives'}
    def fix(m): return m.group(1) + ' leader ' + verb.get(m.group(2), m.group(2))
    say = re.sub(r'\b(your|enemy) units(?: or players)? (\w+)', fix, say).replace('enemy leader', 'the enemy leader')
    say = say.replace('your Nexus or base', 'your leader').replace('the enemy player', 'the enemy leader')
    base = {v: k for k, v in verb.items()}  # "makes your leader move": no -s after "makes"
    return re.sub(r'\b(makes (?:your|the enemy) leader) (\w+)', lambda m: m.group(1) + ' ' + base.get(m.group(2), m.group(2)), say)


def help_abilities(c):
    """triggers whose effects only help the card that set them off ("the first Golem you summon each turn costs 1 less"): a
    help line from the card to those cards, no wait or ask for them"""
    if 'helpab' in CACHE: return CACHE['helpab']
    hp = collections.defaultdict(set)
    obj = {ab_: (k, sd) for ab_, k, sd in c.execute("select ability, obj_kind, obj_side from flat_when where obj_kind is not null")}
    for ab_, act, p_, k, sd, kw, ps in c.execute("select ability, act, on_pick, on_kind, coalesce(on_side,''), keyword_ref, params from flat_do where origin='own'"):
        same = p_ == 'it' or (p_ is None and obj.get(ab_) == (k, sd) and k == 'player')  # "the first time your General takes damage,
        hp[ab_].add(same and sd != 'enemy' and (helps_it(c, act, kw, ps) or act in HELP_ACTS))  # prevent 2 of it
    CACHE['helpab'] = {a for a, v in hp.items() if v == {True}}
    return CACHE['helpab']


def protect_abilities(c):
    """help triggers that only protect what set them off from the damage that did ("prevent 2 of it"): they want no damage"""
    if 'protab' not in CACHE:
        acts = collections.defaultdict(set)
        for ab_, act in c.execute("select ability, act from flat_do where origin='own'"): acts[ab_].add(act)
        CACHE['protab'] = {a for a in help_abilities(c) if acts[a] <= {'negate_damage', 'damage_reduction'}}
    return CACHE['protab']


def harm_abilities(c):
    """abilities whose effects only hurt the card that set them off ("take 1 damage when summoned", Kujata): no want"""
    if 'harm' in CACHE: return CACHE['harm']
    harm = collections.defaultdict(set)
    for ab_, act, p_, sd in c.execute("select ability, act, on_pick, coalesce(on_side,'') from flat_do where origin='own'"):
        harm[ab_].add(act in ('damage', 'kill', 'discard', 'sacrifice') and p_ == 'it' and sd != 'enemy')
    CACHE['harm'] = {a for a, v in harm.items() if v == {True}}
    return CACHE['harm']


def played_lines(c, game, nodes, broad):
    """a card that is itself what another waits for or counts when it is played or summoned ("when you play a spell",
    "Fast spells, Slow spells or Skills you've played"); only when the kind is narrowed past "any card" or "any unit".
    "N cards with different names" is helped by cards that create cards (more different cards to play)."""
    cards = cards_of(c, game); out = collections.defaultdict(list); marks = ','.join('?' * len(nodes)); lvl = level_abilities(c)
    for t, ab, h, kind, side, pick, w in c.execute(f"""select card, ability, happening, kind, side, pick, obj_with from flat_ref where role!='makes'
            and origin='own' and happening in ('played','summoned','drawn') and coalesce(pick,'')!='self' and side in ('mine','any','')
            and card in ({marks})""", list(nodes)).fetchall():
        if ab in harm_abilities(c) or ab in help_abilities(c): continue
        k = kind or ('card' if h in ('played', 'drawn') else 'unit')
        narrowed = any(p and p.split(' ')[0] not in PLAY_STATE and p.split(' ')[1:2] != ['not'] for p in (w or '').split(';'))
        if not narrowed and (k in ('card', 'any', 'anything', None) or (k == 'unit' and h == 'summoned') or not broad): continue
        n = kind_count(c, game, 'any' if k == 'card' else k, w)
        for a in nodes:
            if a != t and a in cards and matches(c, game, cards[a], 'any' if k == 'card' else k, w) and \
                    not (h in ('played', 'drawn') and board_only(c, nodes, a)):  # a token summoned on the board is never played or drawn
                why = f'is a card it counts when {h}'  # "when you draw an event": the deck's events are what it waits to draw
                out[(a, t)].append(('levels', 2.0 / n, why + ' (levels it up)') if ab in lvl else ('waits', 1.0 / n, why))
    for t, ab in c.execute(f"""select card, ability from flat_if where test in ('amount_distinct','distinct') and event='played'
            and card in ({marks})""", list(nodes)).fetchall():
        for (a,) in c.execute(f"select distinct card from flat_concept where concept='generate_cards' and card in ({marks})", list(nodes)):
            if a != t: out[(a, t)].append(('levels' if ab in lvl else 'waits', 0.2, 'creates cards: more different cards to play' +
                                           (' (levels it up)' if ab in lvl else '')))
    return out


def need_lines(c, game, nodes, broad):
    """a card that needs a kind of card on my side: measured from it ("units surrounding a friendly structure") or counted or
    tested ("if you have a structure"); fed by cards of that kind"""
    cards = cards_of(c, game); out = collections.defaultdict(list); marks = ','.join('?' * len(nodes)); needs = []
    for t, w, side in c.execute(f"select card, coalesce(on_with,'') || ';' || coalesce(to_with,''), on_side from flat_do where card in ({marks})", list(nodes)):
        parts = (w or '').split(';')
        of = [p[3:] for p in parts if p.startswith('of:')]
        kind = next((p.split(' ')[2] for p in of if p.startswith('kind is ')), None)
        if kind and kind not in ('unit', 'player'): needs.append((t, kind, ';'.join(p for p in of if not p.startswith('kind'))))
    # a count of what happens to my cards of a kind ("you've destroyed 4+ allied landmarks"): fed by cards of that kind
    for t, kind, w in c.execute(f"""select card, ev_obj_kind, ev_obj_with from flat_if where card in ({marks}) and test in ('event_count','amount_event_count')
            and ev_obj_side='mine' and ev_obj_kind in ('landmark','equipment','spell')""", list(nodes)).fetchall():
        needs.append((t, kind, (w or '') + ';counted'))
    for t, test, kind, side, op, n, w, pick_ in c.execute(f"""select card, test, of_kind, of_side, op, n, of_with, of_pick from flat_if where card in ({marks})
            and test in ('have','count','amount_count') and coalesce(of_side,'mine') in ('mine','any','')""", list(nodes)):
        if op == 'not' or (op in ('eq', 'le', 'lt') and not n): continue  # "no units around": nothing to feed
        narrowed = any(p and p.split(' ')[0] not in PLAY_STATE + ('card',) and p.split(' ')[1:2] != ['not'] for p in (w or '').split(';'))  # "non-X" narrows nothing
        if kind is None and pick_ == 'it' and 'keyword is ' in (w or ''): kind = 'unit'  # "if that minion has Zeal": cards with Zeal
        if kind in KIND_CAT and kind != 'player' and (narrowed or kind != 'unit'): needs.append((t, kind, w))  # a player is always there
    # a keyword's effects acted on ("activate the effects of all traps"): the cards that carry the keyword
    for t, k in c.execute(f"""select card, keyword_ref from flat_do where act='keyword_action' and card_ref is null and keyword_ref is not null
            and on_kind is null and origin='own' and card in ({marks})""", list(nodes)).fetchall():
        if any(k in cards[a]['kws'] for a in nodes if a in cards and a != t): needs.append((t, 'any', f'keyword is {k}'))
    # cards that make a card of a kind by description ("create a random landmark that costs 2 or less", Bomber Twins)
    described = collections.defaultdict(set)
    for a, k in c.execute(f"""select card, on_kind from flat_do where act in ('create','summon','choose_card','random_one') and card_ref is null
            and on_kind in ('landmark','unit','spell','equipment') and coalesce(on_side,'mine') in ('mine','any') and card in ({marks})""", list(nodes)):
        described[k].add(a)
    for t, kind, w in needs:
        counted = (w or '').endswith(';counted'); w = (w or '').removesuffix(';counted')  # "each event you've played": it counts what
        # happens, so it waits for it ("does what it waits for"), it needs nothing to be there
        cnt = kind_count(c, game, kind, w)
        what = 'a card it acts on' if kind == 'any' else f'a {"landmark or structure" if kind == "landmark" else kind} it asks for'
        kws_ = [mechanics.name(c, int(p.split(' ')[2])) for p in (w or '').split(';') if p.startswith('keyword is ') and p.split(' ')[2].isdigit()]
        if kws_ and kind != 'any': what = what.replace(' it asks for', f' with {", ".join(kws_)} it counts or asks for')  # "a unit with Ant
        for a in nodes:
            if a == t or a not in cards: continue
            if counted:
                if matches(c, game, cards[a], kind, w): out[(a, t)].append(('waits', 1.0 / cnt, f'is a {kind} it counts'))
                elif a in described.get(kind, ()) and not any(p.split(' ')[0] in ('card', 'name_has', 'type') for p in (w or '').split(';')):
                    out[(a, t)].append(('waits', 0.5 / cnt, f'makes a {"landmark or structure" if kind == "landmark" else kind} it counts'))
                continue
            if matches(c, game, cards[a], kind, w): out[(a, t)].append(('type', 1.0 / cnt, 'is ' + what))
            elif a in described.get(kind, ()) and not any(p.split(' ')[0] in ('card', 'name_has', 'type') for p in (w or '').split(';')):
                out[(a, t)].append(('type', 0.5 / cnt, 'makes ' + what))
    return out


# What helps a card's need, the same in every game: (happenings it needs, sides of the thing it happens to), the concepts that
# help, and why. A card helps when its own rows, or a keyword it gives, have the concept on my side (not only on itself); a
# unit with the concept as its own keyword helps too (an Overwhelm unit gets damage through to the enemy player).
ATTACK = ('attack_gain', 'temporary_buff', 'multi_attack', 'extra_turn', 'attack_now')
HELPS = [
    (('nexus_damaged', 'strikes_nexus'), ('enemy', '', 'mine'), ATTACK + ('excess_damage', 'evasion'), 'helps it hit the enemy player'),
    (('damaged',), ('enemy', ''), ('excess_damage',), 'more damage'),  # not power: any attacker damages enemies (Punish, Kaptain 30 Oct 2026),
    (('damaged',), ('enemy', ''), ATTACK + ('first_strike',), 'more damage*'),  # except for a level-up count (* = level-ups only, n53)
    (('strikes', 'killed'), ('enemy', '', 'mine', 'any'), ATTACK + ('first_strike', 'target_choice'), 'helps my units strike and kill'),
    (('attacks',), ('mine', '', 'any'), ('multi_attack', 'extra_turn', 'attack_now'), 'another attack'),
    (('survives_damage',), ('mine', ''), ('defence_gain', 'shield', 'damage_reduction', 'immunity', 'regeneration', 'heal',
                                         'cheat_death', 'block_armor', 'lifesteal'), 'more health or protection: survives damage'),
    # where a unit must get to (enemy land, an enemy well, a forest, the enemy god): what moves my units, or units that move
    # well, gets it there (positional games: moving is how a unit reaches the enemy player)
    (('moves_onto', 'harvests', 'fights'), ('mine', '', 'enemy', 'any'), ('movement',), 'moves it where it must be'),
    (('strikes_nexus', 'nexus_damaged'), ('enemy', '', 'mine'), ('movement',), 'moves it within reach of the enemy player'),
]
HIT_KW = ('target_choice', 'excess_damage', 'multi_attack', 'first_strike', 'evasion', 'ranged')  # keywords whose use depends on power


def boost_lines(c, game, nodes):
    """help that is no happening (HELPS): more power helps cards that need damage, strikes or Nexus hits; Overwhelm, Elusive
    and units that have them help cards that need the enemy player hit; health and protection help cards that need to
    survive damage (damage as big as the card's health is no help). A level-up need makes it a level-up line."""
    cards = cards_of(c, game); out = collections.defaultdict(list); marks = ','.join('?' * len(nodes)); L = list(nodes); lvl = level_abilities(c)
    reach = collections.defaultdict(list)  # the targets of each card's stat gains: "the Abomination gains their stats" reaches only it
    def reaches(a, t):
        return not reach.get(a) or any(matches(c, game, cards[t], k if k in KIND_CAT else 'unit', w) for k, w in reach[a])
    def having(concepts, units_too):
        q = ','.join('?' * len(concepts))
        acting = {a for (a,) in c.execute(f"""select card from flat_do where origin in ('own','uses_keyword') and coalesce(on_side,'mine') in ('mine','any')
                and coalesce(on_pick,'') not in ('self') and card in ({marks})""", L)}  # it acts on other cards of mine, not only on itself
        stat = {'attack_gain': ('power', 'strength'), 'defence_gain': ('health', 'strength')}  # strength is both (Stormbound)
        want = {y for x in concepts if x in stat for y in stat[x]}; rest = tuple(x for x in concepts if x not in stat)
        def gains(act, ps):  # the stat it raises ("+2 Attack" raises no Health)
            p = dict(x.split('=', 1) for x in (ps or '').split(';') if '=' in x)
            return act in ('stat_change', 'grow') and any(k in p and not p[k].startswith('-') for k in want)
        rows = [(a, own) for a, own, act, ps, con, k, w in c.execute(f"""select card, coalesce(on_pick,'') = 'self' or coalesce(on_side,'mine') not in
                ('mine','any'), act, params, concept, on_kind, on_with from flat_do where origin in ('own','uses_keyword','has_keyword') and card in ({marks})""", L)
                if ((con in rest or act in rest) or gains(act, ps)) and (want and gains(act, ps) and reach[a].append((k, w)) or True)]
        other = {a for a, own in rows if not own}
        only_self = {a for a, own in rows if own} - other  # Juggernaut "Grow: +5/+5" makes only itself stronger
        got = other | (acting & {a for (a,) in c.execute(f"select card from flat_concept where concept in ({','.join('?' * len(rest)) or 'null'}) and card in ({marks})",
                list(rest) + L)}) - only_self  # a stat gain is read row by row (its stat); other concepts also by the card's concepts
        if units_too:  # a unit whose own keyword it is
            got |= {a for (a,) in c.execute(f"""select ck.card from card_keyword ck join card k on k.id=ck.keyword join vocab v on v.field='keyword'
                    and v.value in (k.name, k.game || ':' || k.name) where v.tree in ({q}) and ck.card in ({marks})""", list(concepts) + L)}
        return got
    count = lambda concepts: CACHE.setdefault(('n', game, concepts), max(1, len({a for (a,) in c.execute(
        f"select card from flat_concept where concept in ({','.join('?' * len(concepts))})", concepts) if a in cards})))
    needs = c.execute(f"""select card, ability, happening, side, role, pick from flat_ref where role!='makes' and origin in
            ('own','uses_keyword','has_keyword') and card in ({marks})""", L).fetchall()
    # help given to my player reaches only my leader card (Duelyst: "your General gains +1 Attack"), help given to units only units
    aims = collections.defaultdict(set)
    leaders = any(cards[t]['cat'] == 'leader' for t in L if t in cards)  # only a game whose player is a card on the board
    for a, k in c.execute(f"""select card, coalesce(on_kind,'unit') from flat_do where origin in ('own','uses_keyword') and coalesce(on_side,'mine')
            in ('mine','any') and coalesce(on_pick,'') not in ('self') and act in ('stat_change','give_keyword','heal','move','swap','grow',
            'ready','can','give_ability','first_strike','double_strike','copy_keywords') and card in ({marks})""", L):
        aims[a] |= {'player', 'unit'} if k in ('any', 'anything') else {'player'} if k == 'player' else {'unit'} if k in ('unit', 'hero') else {'other'}  # "a minion or General"
    # help that names whom it lands on ("give a Dragon +2|+2", "your Rakoans get Flying") reaches only those cards
    ident = collections.defaultdict(list)
    for a, w_ in c.execute(f"""select card, on_with from flat_do where origin in ('own','uses_keyword') and coalesce(on_side,'mine') in ('mine','any')
            and coalesce(on_pick,'') not in ('self') and act in ('stat_change','give_keyword','heal','grow','copy_keywords','negate_damage')
            and card in ({marks})""", L):
        ident[a].append(';'.join(q_ for q_ in (w_ or '').split(';') if q_.split(' ')[:2] in (['card', 'is'], ['type', 'is'], ['type', 'in'],
                        ['name_has', 'is'], ['keyword', 'is'], ['region', 'is'], ['card', 'not'])))
    def lands_on(a, t):
        return not ident.get(a) or any(not who or matches(c, game, cards[t], 'any', who) for who in ident[a])
    def aim_fits(a, t):
        return lands_on(a, t) and leader_fits(a, t)
    def leader_fits(a, t):
        if a not in aims or not leaders: return True
        return ('player' in aims[a]) if cards[t]['cat'] == 'leader' else 'unit' in aims[a] or aims[a] == {'other'}
    for hs, sides, concepts, why in HELPS:
        helpers = having(concepts, hs[0] == 'nexus_damaged'); n = count(concepts)
        move_rows = {}
        if concepts == ('movement',):  # what moves another of my units, or gives it a movement keyword (row by row, not "has both somewhere")
            move_rows = collections.defaultdict(list)
            for a, w_ in c.execute(f"""select d.card, d.on_with from flat_do d left join card k on k.id=d.keyword_ref left join vocab v on
                    v.field='keyword' and v.value in (k.name, k.game || ':' || k.name) where d.origin='own' and coalesce(d.on_pick,'') not in ('self')
                    and coalesce(d.on_side,'mine') in ('mine','any') and coalesce(d.on_kind,'unit') in ('unit','any') and (d.act in ('move','swap')
                    or (d.act='give_keyword' and v.tree='movement')) and d.card in ({marks})""", L): move_rows[a].append(w_)
            helpers = set(move_rows)
            movers = helpers | {a for (a,) in c.execute(f"""select ck.card from card_keyword ck join card k on k.id=ck.keyword join vocab v on
                    v.field='keyword' and v.value in (k.name, k.game || ':' || k.name) where v.tree='movement' and ck.card in ({marks})""", L)}
        else: movers = helpers
        for t, ab, h, side, role, pick in needs:
            if h not in hs or side not in sides: continue
            helpers_t = movers if pick != 'self' and h != 'harvests' else helpers  # "whenever THIS moves onto": only what moves it;
            # "my units harvest enemy wells": every mobile unit would link (noise, Gabrian Archon -> Wavecrash Colossus)
            if concepts == ('movement',):  # what it moves must be able to be this card ("give the Demon Wing Flying", "another Rakoan")
                fits = lambda ws: any(not who or matches(c, game, cards[t], 'any', who) for who in (';'.join(p for p in (w_ or '').split(';')
                       if p.split(' ')[:2] in (['card', 'is'], ['type', 'is'], ['type', 'in'], ['name_has', 'is'])) for w_ in ws))
                helpers_t = {a for a in helpers_t if a not in move_rows or fits(move_rows[a])}
            if role == 'trigger' and pick in ('self', 'actor_self') and h not in ('survives_damage', 'moves_onto', 'harvests') and \
                    not (concepts == ('movement',) and h in ('strikes_nexus', 'fights')): continue  # getting there is help  # "Strike:" fires on any strike: more of it adds nothing
            if h in ('strikes', 'killed') and role == 'trigger': continue  # only counted strikes and kills grow with more power
            lv = ab in lvl
            if why.endswith('*') and not lv: continue
            for a in helpers_t - {t}:
                if not (aim_fits(a, t) if pick == 'self' else leader_fits(a, t)): continue  # help on itself must land on it
                out[(a, t)].append(('levels' if lv else 'moves' if concepts == ('movement',) else 'waits', (1.0 if lv else 0.5) / n,
                                    why.rstrip('*') + (' (levels it up)' if lv else '')))  # it makes what the card waits for happen more
    # how many cards are in my hand ("played as the last card from your hand", "10+ cards in hand", "for each card in hand")
    hand = lambda acts, zone: {a for (a,) in c.execute(f"""select card from flat_do where act in ({','.join('?' * len(acts))}) and origin in
            ('own','uses_keyword') and coalesce(on_side,'mine')='mine' and (coalesce(on_zone,'')='hand' or coalesce(eff_zone,'')='hand' or ?)
            and card in ({marks})""", list(acts) + [zone] + L)}
    for t, ab, op, n_ in c.execute(f"""select card, ability, op, n from flat_if where of_zone='hand' and coalesce(of_side,'mine')='mine'
            and test in ('count','amount_count','have') and card in ({marks})""", L).fetchall():
        few = (op in ('eq', 'le', 'lt') and (n_ or 0) <= 1) or op == 'not'  # "no cards in hand" (have not, N22)
        helpers = hand(('discard',), 0) if few else hand(('create', 'copy', 'return_to_hand'), 0) | hand(('draw',), 1)  # a draw goes to hand
        for a in helpers - {t}:
            out[(a, t)].append(('levels' if ab in lvl else 'boosts', 0.3, ('empties your hand' if few else 'fills your hand') + (' (levels it up)' if ab in lvl else '')))
    # a stat it tests ("an ally with 5+ Power"): more of that stat
    power = having(('attack_gain',), False)
    for t, ab, fp in c.execute(f"""select card, ability, of_pick from flat_if where test in ('stat','amount_stat') and attr='power' and card in ({marks}) and not exists (select 1 from flat_do d where d.ability=flat_if.ability and flat_if.of_pick='it' and d.on_pick in ('chosen','random')
            and coalesce(d.on_side,'any')!='mine' and d.act in ('kill','damage','obliterate','sacrifice','return_to_hand','transform','silence'))""", L).fetchall():
        for a in power - {t}:
            if aim_fits(a, t) and (fp != 'self' or reaches(a, t)): out[(a, t)].append(('levels' if ab in lvl else 'boosts', 0.5 / count(('attack_gain',)), 'more power' + (' (levels it up)' if ab in lvl else '')))
    # a stat it tests high or uses as an amount ("a creature with 5+ Life", "faeria equal to its Life"): more of that stat
    health = having(('defence_gain',), False)
    for t, ab, fp in c.execute(f"""select card, ability, of_pick from flat_if where attr in ('health', 'total_stats') and (test='amount_stat' or
            (test='stat' and coalesce(op,'') in ('ge','gt'))) and coalesce(of_side,'mine')!='enemy' and card in ({marks}) and not exists
            (select 1 from flat_if x where x.card=flat_if.card and x.ability=flat_if.ability and x.test='amount') and not exists (select 1 from flat_do d where d.ability=flat_if.ability and flat_if.of_pick='it' and d.on_pick in ('chosen','random')
            and coalesce(d.on_side,'any')!='mine' and d.act in ('kill','damage','obliterate','sacrifice','return_to_hand','transform','silence'))""", L).fetchall():  # a threshold wants nothing;
        # a stat of what the player picks on either side is the biggest there is (Martyrdom)
        for a in health - {t}:
            if aim_fits(a, t) and (fp != 'self' or reaches(a, t)):  # its own stat: the gain must reach it
                out[(a, t)].append(('levels' if ab in lvl else 'boosts', 0.5 / count(('defence_gain',)), 'more health' + (' (levels it up)' if ab in lvl else '')))
    # where my units may enter (Wind Gate: "summon creatures on spaces adjacent to this"): helps a card whose entry asks for a
    # place ("Gift - gains +1/+1 if summoned adjacent to an opponent's well")
    placers = {a for (a,) in c.execute(f"""select card from flat_do where act='can' and param_event in ('summoned','played') and
            to_kind='position' and coalesce(on_pick,'')!='self' and origin='own' and card in ({marks})""", L)}  # not a keyword's (Wild)
    if placers:
        for (t,) in c.execute(f"""select distinct i.card from flat_if i join flat_when w on w.ability=i.ability where w.event in
                ('played','summoned') and w.obj_pick='self' and (coalesce(i.of_with,'') like '%position %' or i.of_kind='position')
                and i.card in ({marks})""", L).fetchall():
            for a in placers - {t}: out[(a, t)].append(('boosts', 0.5 / len(placers), 'lets it enter where it needs to be'))
    # units whose keywords use their power (Challenger, Overwhelm, Quick Attack, Elusive, Double Attack, Ranged), and units whose
    # own effect makes them fight (Faeria "This fights an enemy creature"): power makes them hit harder
    for (t,) in c.execute(f"""select distinct ck.card from card_keyword ck join card k on k.id=ck.keyword join vocab v on v.field='keyword'
            and v.value in (k.name, k.game || ':' || k.name) where v.tree in ({','.join('?' * len(HIT_KW))}) and ck.card in ({marks})
            union select card from flat_do where origin='own' and act in ('start_attack','strike') and on_pick='self' and card in ({marks})
            union select id from card where category='leader' and id in ({marks})""",  # a leader fights by the rules: power makes it hit harder
            list(HIT_KW) + L + L + L).fetchall():
        for a in power - {t}:
            if not aim_fits(a, t) or not reaches(a, t): continue
            if not any(k in ('boosts', 'levels') for k, *_ in out[(a, t)]): out[(a, t)].append(('boosts', 0.25 / count(('attack_gain',)), 'more power: it hits harder'))
    q = lambda sql, *a: {x for (x,) in c.execute(sql.format(marks=marks), list(a) + L * sql.count('{marks}'))}
    movers_mine = q("""select card from flat_do where origin='own' and act in ('move','swap') and coalesce(on_side,'mine') in ('mine','any')
            and coalesce(on_kind,'unit') in ('unit','any') and coalesce(on_pick,'') not in ('self') and card in ({marks})""")
    # paying for big cards: more mana, or a cost cut on my cards, helps the game's expensive cards (its top tenth of costs:
    # Faeria 7+) when it pays at least a third of the card's cost (Red Devil's 5 faeria for Krog's 12; 2 faeria in a fight
    # does not pay for anything), and only the cards the cut names ("Your Krog costs 7 less": Krog only)
    game_costs = sorted(x['cost'] for x in cards.values() if x.get('cost') and x['cat'] not in ('game_rule',))
    if game_costs:
        high = game_costs[int(len(game_costs) * 0.9)]
        pays = collections.defaultdict(list)
        for a, act, ps, w_ in c.execute(f"""select card, act, params, on_with from flat_do where origin='own' and ((act in ('mana_gain','max_mana_change')
                and coalesce(on_side,'mine')='mine') or (act in ('cost_change','cost_set') and coalesce(on_side,'mine') in ('mine','any')
                and coalesce(on_pick,'') not in ('self','it'))) and card in ({marks})""", L):
            p = dict(x.split('=', 1) for x in (ps or '').split(';') if '=' in x)
            x = p.get('amount' if act in ('mana_gain', 'max_mana_change') else 'cost', '')
            n_ = float(x.lstrip('-')) if act != 'cost_set' and x.lstrip('-').replace('.', '', 1).isdigit() else None
            if act == 'cost_change' and not x.startswith('-'): continue  # a cost raised pays nothing
            who = ';'.join(q_ for q_ in (w_ or '').split(';') if q_.split(' ')[:2] in (['card', 'is'], ['type', 'is'], ['type', 'in'],
                           ['name_has', 'is'], ['keyword', 'is'], ['region', 'is'], ['category', 'is']))
            pays[a].append((act, n_, who))
        for t in nodes:
            cost = cards.get(t, {}).get('cost') or 0
            if t not in cards or cost < high: continue
            for a, rs in pays.items():
                if a == t: continue
                if any((n_ is None and act == 'cost_set') or (n_ is not None and n_ * 3 >= cost) for act, n_, who in rs
                       if not who or matches(c, game, cards[t], 'any', who)):
                    out[(a, t)].append(('boosts', 0.5 / max(1, len(pays)), 'pays for it: more mana or a lower cost'))
    # a straight line of fire (a keyword whose strike hits the nearest enemy in a straight line: Faeria Ranged): what removes or
    # moves enemy units clears the line; what moves my unit by an effect places it without using its move
    line_kw = q("""select distinct d.card from flat_do d join card k on k.id=d.card where k.is_keyword=1 and d.act='strike'
            and d.to_with like '%straight_line%' and d.to_pick='nearest' and 1 in (1) and d.card not in ({marks})""")
    if line_kw:
        shooters = {t for t in nodes if t in cards and cards[t]['kws'] & line_kw}
        clear = q("""select card from flat_do where origin='own' and act in ('damage','kill','obliterate','capture','move','swap','transform',
                'return_to_hand') and (on_side='enemy' or (coalesce(on_side,'')='' and on_pick in ('chosen','all','random')))
                and coalesce(on_kind,'unit') in ('unit','any','anything','unit_or_structure') and card in ({marks})""")
        for t in shooters:
            for a in clear - {t}: out[(a, t)].append(('boosts', 0.5 / max(1, len(clear)), 'clears its line of fire'))
            for a in movers_mine - {t}: out[(a, t)].append(('boosts', 0.5 / max(1, len(movers_mine)), 'moves it without using its move'))
    # a board that grows from my units (a game rule: land or entry spaces next to my units, Faeria): whatever moves my units or
    # my land, or puts units that move far, helps the cards whose entry asks for a place (Bomb Slinger's adjacent enemy, Axe
    # Grinder next to an enemy well, Mistral Guide's units summoned next to it)
    grows = c.execute("""select 1 from game_rule g join flat_do d on d.card=g.entry join card k on k.id=g.entry where d.act='can' and
            d.param_event in ('terrain_changed','summoned','played') and d.to_with like '%bordering%' and k.game=? limit 1""", (game,)).fetchone()
    if grows:
        mobile = q("""select ck.card from card_keyword ck join card k on k.id=ck.keyword join vocab v on v.field='keyword' and v.value in
                (k.name, k.game || ':' || k.name) where v.tree='movement' and ck.card in ({marks})""")
        land_movers = q("""select card from flat_do where origin='own' and act in ('move','set_terrain') and on_kind='position' and card in ({marks})""")
        put_movers = q("""select d.card from flat_do d join flat_do g on g.card=d.card and g.ability=d.ability where d.origin='own' and
                d.act='summon' and g.act='give_keyword' and g.on_pick='it' and g.keyword_ref in (select id from card where is_keyword=1 and
                name in ('Flying','Jump','Charge','Dash')) and d.card in ({marks})""")
        givers = q("""select d.card from flat_do d join card k on k.id=d.keyword_ref join vocab v on v.field='keyword' and v.value in
                (k.name, k.game || ':' || k.name) where d.origin='own' and d.act='give_keyword' and v.tree='movement' and
                coalesce(d.on_side,'mine') in ('mine','any') and coalesce(d.on_pick,'') not in ('self','it') and d.card in ({marks})""")  # not a
        # token's own keyword ("summon a Manta with Flying")
        growers = movers_mine | mobile | land_movers | put_movers | givers  # Syland Horsemaster gives Charge
        place = q("""select distinct d.card from flat_do d join flat_when w on w.ability=d.ability where w.event in ('played','summoned')
                and w.obj_pick='self' and d.origin='own' and coalesce(d.on_with,'') || coalesce(d.to_with,'') like '%position %'
                and coalesce(d.on_with,'') || coalesce(d.to_with,'') not like '%position % % of %' and d.card in ({marks})  -- measured from the card itself
                -- ("an adjacent enemy"), not from another thing ("in its place")
                union select distinct i.card from flat_if i join flat_when w on w.ability=i.ability where w.event in ('played','summoned')
                and w.obj_pick='self' and i.origin='own' and coalesce(i.of_with,'') like '%position %'
                and coalesce(i.of_with,'') not like '%position % % of %' and i.card in ({marks})
""")
        near_me = q("""select card from flat_when where origin='own' and event in ('summoned','played') and coalesce(obj_pick,'')!='self'
                and obj_with like '%position % bordering%' and card in ({marks})""")  # "units summoned next to this" (Mistral Guide)
        place = {t for t in place if cards.get(t, {}).get('cat') in ('unit', 'hero', 'building')}  # a spell enters no board (Firestorm)
        # and cards that need my units deep in enemy ground: harvesting enemy wells (Wavecrash Colossus), moving onto enemy land
        deep = q("""select card from flat_ref where role!='makes' and origin in ('own','has_keyword') and happening in ('harvests','moves_onto')
                and (side='enemy' or coalesce(obj_with,'') like '%enemy%') and card in ({marks})""")
        for t in near_me:  # what moves this card, or lets it move far, chooses where the units summoned next to it appear
            for a in (movers_mine | givers) - {t}: out[(a, t)].append(('boosts', 0.5 / max(1, len(movers_mine | givers)), 'moves it where the units summoned next to it are needed'))
        for t in (place | deep) - near_me:
            why = 'moves my units or land forward: it can enter where it needs to be' if t in place else 'moves my units or land forward: they reach enemy ground'
            for a in growers - {t}: out[(a, t)].append(('boosts', 0.5 / max(1, len(growers)), why))
    return out


def actor_of(c, ab):
    """who does what an ability waits for ("your spells and Skills" deal damage): kind, side, pick and filters"""
    r = c.execute('select t.id, t.kind, t.side, t.pick from ability a join event e on e.id=a.event join target t on t.id=e.actor '
                  'where a.id=?', (ab,)).fetchone()
    if not r: return None, None, None, None
    w = ';'.join(f'{a} {o} {rk or rt or rc or rw or v or n}' for a, o, rk, rt, rc, rw, v, n in c.execute(
        'select attr, op, ref_keyword, ref_type, ref_card, ref_word, val, n from filter where target=? and of_target is null', (r[0],)))
    return r[1], r[2], r[3], w or None


def adders(c, game):
    """abilities that add to what my cards of a kind just did ("your spells and Skills deal 1 extra damage": damage again on
    the thing damaged; Tybaulk, Funsmith): (card, ability, happening, actor kind, actor filters, (act, params)). They make those
    cards stronger and wait for nothing themselves."""
    if ('adders', game) in CACHE: return CACHE[('adders', game)]
    cards = cards_of(c, game); causes = collections.defaultdict(set); out = []
    for act, ev in c.execute('select act, event from causes'): causes[act].add(ev)
    for a, origin, ab, h, apick in c.execute("""select distinct card, origin, ability, event, actor_pick from flat_when where origin in ('own','gives')
            and coalesce(actor_side,'mine')='mine' and actor_kind is not null and actor_kind!='player'""").fetchall():
        if a not in cards or apick in ('self', 'it'): continue
        dos = c.execute('select act, params, on_pick, on_kind from flat_do where card=? and ability=? and origin=? order by seq', (a, ab, origin)).fetchall()
        first = next((i for i, d in enumerate(dos) if d[2] not in (None, 'it') or (d[2] is None and d[3]) or d[0] in PUTS), len(dos))
        add = next(((act, ps) for act, ps, pk, _ in dos[:first] if pk == 'it' and h in causes[act]), None)  # "it" is still what was hit
        if not add: continue
        kind, _, _, w = actor_of(c, ab)
        out.append((a, ab, h, kind, w, add))
    CACHE[('adders', game)] = out
    return out


def adder_abilities(c, game):
    return {ab for _, ab, *_ in adders(c, game)}


def object_help_lines(c, game, nodes, broad):
    """an ability that acts when my cards of a kind are played, summoned, drawn or created, and helps that card ("When you
    summon an Elite, grant it +1|+1", Battlesmith; "the next card with Nightfall you play costs 1 less", Duskpetal Dust):
    it makes every card of that kind in the deck stronger. broad=False keeps only kinds narrowed past "any unit" or "any card"."""
    cards = cards_of(c, game); out = collections.defaultdict(list); marks = ','.join('?' * len(nodes)); L = list(nodes)
    for a, origin, ab, kind, w in c.execute(f"""select distinct card, origin, ability, obj_kind, obj_with from flat_when where origin in ('own','gives')
            and event in ('played','summoned','drawn','created') and coalesce(obj_side, actor_side, 'mine')='mine' and coalesce(obj_pick,'') not in ('self')
            and card in ({marks})""", L).fetchall():
        narrowed = any(p and p.split(' ')[0] not in PLAY_STATE and p.split(' ')[1:2] != ['not'] for p in (w or '').split(';'))
        if not narrowed and not broad: continue
        whys = []
        for act, kw, ps in c.execute("select act, keyword_ref, params from flat_do where card=? and ability=? and origin=? and on_pick='it'", (a, ab, origin)):
            if act in ('stat_change', 'grow') and '=-' not in (ps or ''): whys.append(stats_said(ps))
            elif act == 'cost_change' and '=-' in (ps or ''): whys.append('makes it cheaper')
            elif act == 'give_keyword' and kw and buff_keyword(c, kw): whys.append(f'gives it {mechanics.name(c, kw)}')
            elif act == 'heal': whys.append('heals it')
        if not whys: continue
        k = 'any' if kind in (None, 'card', 'any', 'anything') else kind
        hits = [b for b in L if b != a and b in cards and matches(c, game, cards[b], k, w)]
        for b in hits: out[(a, b)].append(('boosts', 0.5 / max(1, len(hits)), ', '.join(dict.fromkeys(whys)) + ' when it comes'))
    return out


def actor_help_lines(c, game, nodes):
    """an ability on what happens to the card itself that acts on the event's actor (Worthy Sacrifice: when it is sacrificed,
    the card it pays for costs 2 less; Morsel: that card gets its stats): it helps every card of the deck that needs that
    happening (the Blood cards that need sacrifices)"""
    cards = cards_of(c, game); out = collections.defaultdict(list); marks = ','.join('?' * len(nodes)); L = list(nodes)
    for a, act, ps, ev in c.execute(f"""select distinct d.card, d.act, d.params, w.event from flat_do d join flat_when w on w.card=d.card
            and w.ability=d.ability where d.on_pick='actor' and w.obj_pick='self' and d.origin in ('own','has_keyword')
            and d.act in ('cost_change','stat_change','give_keyword') and d.card in ({marks})""", L).fetchall():
        takers = {t for (t,) in c.execute(f"""select distinct card from flat_ref where role in ('condition','trigger') and happening=?
                  and coalesce(side,'') in ('mine','any','') and coalesce(pick,'') not in ('self','actor_self') and card in ({marks})""", [ev] + L)} - {a}
        why = 'makes it cheaper' if act == 'cost_change' and '=-' in (ps or '') else ('help ' + stats_said(ps))[5:] if act == 'stat_change' else 'gives it a keyword'
        for t in takers:
            if t in cards: out[(a, t)].append(('boosts', 1.0 / len(takers), why + f' (when it is {ev.replace("_", " ")} for it)'))
    return out


def gives_lines(c, game, nodes):
    """abilities that act when my cards of a kind do something (the card's own or given to my side). When they add to what
    happened (adders) the card makes every card of that kind in the deck that does it stronger (Tybaulk -> every spell and
    Skill that deals damage, also through a keyword it uses: Drain); otherwise the cards that make that happening feed a
    given ability ("when you summon an ally, grant its keywords": Zoe level 2)"""
    cards = cards_of(c, game); out = collections.defaultdict(list); marks = ','.join('?' * len(nodes)); L = list(nodes)
    doers = lambda h: {m for (m,) in c.execute(f"""select distinct card from flat_ref where role='makes' and happening=? and
            origin in ('own','uses_keyword') and coalesce(pick,'') not in ('self','it') and card in ({marks})""", [h] + L)}
    found = adders(c, game); n = collections.Counter(h for _, _, h, *_ in found)
    for a, ab, h, kind, w, (act, ps) in found:
        if a not in nodes: continue
        amount = dict(p.split('=', 1) for p in (ps or '').split(';') if '=' in p).get('amount', '').removesuffix('.0')
        why = (f'doubles its {act.replace("_", " ")}' if amount == 'event_amount' else
               f'its {act.replace("_", " ")} gets {amount} more' if amount else f'adds to its {act.replace("_", " ")}')
        units = {b for b in L if b in cards and cards[b]['cat'] in KIND_CAT['unit']} if kind == 'unit' and h in ('damaged', 'strikes') else set()
        for m in doers(h) | units:  # every unit deals damage when it strikes
            if m != a and m in cards and matches(c, game, cards[m], kind, w): out[(a, m)].append(('boosts', 1.0 / n[h], why))
    skip = adder_abilities(c, game)
    for a, h, ab, akind in c.execute(f"""select distinct card, event, ability, actor_kind from flat_when where origin='gives'
            and coalesce(actor_side,'mine')='mine' and card in ({marks})""", L).fetchall():
        if ab in skip: continue
        say = act_say(c, h, '', None); w = actor_of(c, ab)[3]
        for m in doers(h):
            if m == a or m not in cards or (akind in KIND_CAT and not matches(c, game, cards[m], akind, w)): continue
            out[(m, a)].append(('waits', 0.1, f'{say} (for the ability it gives)'))
    return out


def made(c, game, ids):
    """level-up forms and cards the nodes make, plant, cast as skills or put into play, two steps deep"""
    cards = cards_of(c, game); got = set(ids); new = set()
    for _ in range(2):
        q = list(got | new); marks = ','.join('?' * len(q))
        add = {b for (b,) in c.execute(f"select dst from card_link where rel='transforms_into' and src in ({marks})", q)}
        add |= {b for (b,) in c.execute(f"select l.dst from card_link l join card d on d.id=l.dst join card s on s.id=l.src where "
                                         f"l.rel='generates' and (d.category='ability' or s.category='leader') and l.src in ({marks})", q)}  # a
        # unit's skill; a leader's own spell (Duelyst General: its Bloodbound Spell)
        add |= {b for (b,) in c.execute(f"select card_ref from flat_do where act in ({','.join('?' * len(PUTS))}) and card in ({marks})",
                                         list(PUTS) + q)}
        new |= {b for b in add if b in cards} - got
    return new


def families(c, nodes):
    """a champion and its level-up forms are one card in play (a levelled champion is never next to its own level 1)"""
    root = {n: n for n in nodes}
    for a, b in c.execute("select src, dst from card_link where rel='transforms_into'"):
        if a in root and b in root: root[b] = a
    fam = lambda n: n if root[n] == n else fam(root[n])
    return {n: fam(n) for n in nodes}


def self_harm_lines(c, game, nodes):
    """harm aimed at any unit, of either side ("deal 1 damage to a creature"), or at my own units ("sacrifice another creature"):
    the player aims it at my own unit when that unit's own effect fires on it (Falcon Dive -> a Last Words unit with 1 Life;
    Lord of the Wastes -> Village Elder). A card that counts friendly deaths (Soul Eater) gets nothing from either-side harm."""
    cards = cards_of(c, game); out = collections.defaultdict(list); marks = ','.join('?' * len(nodes)); L = list(nodes)
    wants = collections.defaultdict(set)
    for t, h in c.execute(f"""select card, happening from flat_ref where role='trigger' and pick='self' and (origin='own' or
            (origin='has_keyword' and happening in ('dies','killed'))) and happening in ('dies','killed','damaged','survives_damage','sacrificed')
            and card in ({marks})""", L): wants[t].add(h)  # a death keyword (Last Breath, Dying Wish) is its effect; a shield keyword
            # that fires on damage (Barrier, Forcefield) is no effect anyone damages it for
    harms = c.execute(f"""select card, act, on_kind, on_with, params from flat_do where origin='own' and act in ('damage','kill','sacrifice')
            and coalesce(on_side,'') in ('','any','mine') and on_pick in ('chosen','random','all') and coalesce(on_kind,'unit') in
            ('unit','any','anything','unit_or_structure') and card in ({marks})""", L).fetchall()
    for t, hs in wants.items():
        life = cards.get(t, {}).get('health') or cards.get(t, {}).get('strength')
        for a, act, k, w, ps in harms:
            if a == t or a not in cards or not matches(c, game, cards[t], 'unit', w): continue
            x = dict(q.split('=', 1) for q in (ps or '').split(';') if '=' in q).get('amount', '')
            dmg = float(x) if x.replace('.', '', 1).isdigit() else None
            kills = act in ('kill', 'sacrifice') or (dmg is not None and life and dmg >= life)
            if kills and hs & {'dies', 'killed'}: out[(a, t)].append(('waits', 0.5, ACT_SELF['dies']))
            elif kills and 'sacrificed' in hs and act == 'sacrifice': out[(a, t)].append(('waits', 0.5, ACT_SELF['sacrificed']))
            elif act == 'damage' and 'damaged' in hs: out[(a, t)].append(('waits', 0.5, ACT_SELF['damaged']))
            elif act == 'damage' and 'survives_damage' in hs and not kills: out[(a, t)].append(('waits', 0.5, ACT_SELF['survives_damage']))
    return out


def network(c, game, ids, broad=True):
    """nodes (id -> made by the deck?) and lines (a, b) -> [(kind, weight, why)] between them"""
    nodes = {i: False for i in ids}
    for i in made(c, game, ids): nodes[i] = True
    allg = lines_of(c, game); lines = collections.defaultdict(list)
    for (a, b), ls in allg.items():
        if a in nodes and b in nodes: lines[(a, b)] += ls
    for f in (aimed(c, game, nodes, broad), played_lines(c, game, nodes, broad), need_lines(c, game, nodes, broad),
              boost_lines(c, game, nodes), gives_lines(c, game, nodes), object_help_lines(c, game, nodes, broad),
              actor_help_lines(c, game, nodes), self_harm_lines(c, game, nodes)):
        for k, ls in f.items(): lines[k] += ls
    fam = families(c, nodes)
    lines = collections.defaultdict(list, {(a, b): [l for l in ls if l[0] == 'levelsinto'] if fam[a] == fam[b] else ls
                                           for (a, b), ls in lines.items()})
    # what a made card does is done by the card that makes it (Cosmic Binding plants Chimes, Chimes level Bard)
    if broad:
        made_by = collections.defaultdict(set)
        for (a, b), ls in lines.items():
            if nodes.get(b) and any(k == 'puts' and y != 'copies it' for k, _, y in ls): made_by[b].add(a)  # makes it, not copies one in play
        for (m, b), ls in list(lines.items()):
            for p in made_by.get(m, ()):
                if p == b or fam[p] == fam[b]: continue
                for k, w, why in ls:
                    if k == 'levels':  # only what levels a champion up is passed on: other lines through a made card stay on it
                        lines[(p, b)].append((k, w * 0.5, f'through {mechanics.name(c, m)}: {why}'))
    # "makes the Wraithling it asks for": when the Wraithling is drawn too, the maker puts it into play and the Wraithling enables
    # the card; no line from the maker straight to the card (Lilithe -> Wraithling -> Inkling Surge)
    via_made = {(a, b) for (a, m), ls in lines.items() if nodes.get(m) and any(k == 'puts' for k, *_ in ls)
                for (m2, b), ls2 in lines.items() if m2 == m and any(k == 'type' and y.startswith('is ') for k, _, y in ls2)}
    lines = collections.defaultdict(list, {(a, b): [l for l in ls if not ((a, b) in via_made and l[0] == 'type' and l[2].startswith('makes '))]
                                           for (a, b), ls in lines.items()})
    lines = collections.defaultdict(list, {(a, b): [l for l in ls if not (nodes.get(b) and l[2] == 'draws it from the deck')]
                                           for (a, b), ls in lines.items()})  # a card the deck only makes is in no deck to draw from
    # a form a card grows or levels into is never played from hand: its cost is never paid (Tadpole -> Bullfrog, Curious Egg ->
    # Hydra; a champion's level-up form)
    grown = {b for (a, b), ls in lines.items() if nodes.get(b) and any(k == 'levelsinto' for k, _, _ in ls)} - \
            {b for (a, b), ls in lines.items() if any(k == 'puts' for k, _, _ in ls)}
    lines = collections.defaultdict(list, {(a, b): [l for l in ls if not (b in grown and '(pays its cost)' in l[2])] for (a, b), ls in lines.items()})
    # a card that draws or puts a kind of card from my deck finds the deck's cards of that kind, not the game's (Time of Legends
    # finds the deck's one legend)
    found = collections.Counter((a, y) for (a, b), ls in lines.items() if nodes.get(b) is False for k, w, y in ls
                                if k == 'puts' and (y == 'draws it from the deck' or y.startswith('puts it into play from')))
    lines = collections.defaultdict(list, {(a, b): [(k, 1.0 / found[(a, y)] if (a, y) in found and k == 'puts' else w, y) for k, w, y in ls]
                                           for (a, b), ls in lines.items()})
    # "helps" says how: cheaper, stronger, a keyword, into place, a clear way (or it makes what the card waits for happen more)
    lines = collections.defaultdict(list, {(a, b): [(help_kind(y), w, y) if k == 'boosts' else (k, w, y) for k, w, y in ls]
                                           for (a, b), ls in lines.items()})
    same = lambda ls: list({(k, y): (k, w, y) for k, w, y in ls}.values())  # one card doing a thing twice (when summoned, when attacking) is one line
    return nodes, {k: same(v) for k, v in lines.items() if v}


# ---- measures, in plain words ----
NO_END = ('levelsinto',)  # a champion's level-up form is a step a chain passes through, never its point


def best_lines(lines):
    """(a, b) -> (weight, kind, why): the strongest reason per pair"""
    out = {}
    for k, ls in lines.items():
        real = [(w, kind, why) for kind, w, why in ls if kind != 'targets']  # "can aim at it" only when nothing else joins them
        out[k] = max(real or [(w, kind, why) for kind, w, why in ls], key=lambda x: x[0])
    return out


def betweenness(nodes, adj):
    """how many shortest paths between other cards pass through each card (Brandes, lines counted as steps)"""
    bc = dict.fromkeys(nodes, 0.0)
    for s in nodes:
        stack, pred, sigma, dist, q = [], collections.defaultdict(list), collections.Counter({s: 1}), {s: 0}, collections.deque([s])
        while q:
            v = q.popleft(); stack.append(v)
            for w in adj.get(v, ()):
                if w not in dist: dist[w] = dist[v] + 1; q.append(w)
                if dist[w] == dist[v] + 1: sigma[w] += sigma[v]; pred[w].append(v)
        delta = collections.Counter()
        while stack:
            w = stack.pop()
            for v in pred[w]: delta[v] += sigma[v] / sigma[w] * (1 + delta[w])
            if w != s: bc[w] += delta[w]
    return bc


def chains(best, nodes, top=10, per_node=None):
    """paths of 2 to 4 cards, strongest first (strength = geometric mean of the line weights; levels-into lines are free;
    targets lines are left out, any card will do for them; a champion and its level-up form count as one card)"""
    adj, root = collections.defaultdict(list), {n: n for n in nodes}
    for (a, b), (w, kind, why) in best.items():
        if kind == 'levelsinto': root[b] = a
    fam = lambda n: n if root[n] == n else fam(root[n])
    for (a, b), (w, kind, why) in best.items():
        if kind != 'targets': adj[a].append((w, b, kind, why))
    for a in adj:
        adj[a].sort(reverse=True)
        if per_node: adj[a] = adj[a][:per_node]
    found = []

    def walk(path, steps):
        ws = [w for w, kind, _ in steps if kind not in NO_END]
        if steps and steps[-1][1] not in NO_END and ws:
            found.append((math.prod(ws) ** (1 / len(ws)), len(path), tuple(path), tuple(steps)))
        if len(path) == 4: return
        for w, b, kind, why in adj.get(path[-1], ()):
            if fam(b) not in {fam(x) for x in path} or kind == 'levelsinto': walk(path + [b], steps + [(w, kind, why)])
    for n in nodes: walk([n], [])
    found.sort(key=lambda x: (-x[0], -x[1]))
    # chains that differ only in their last card are one line ("... -> changes its cost -> Crumble, The Ruination");
    # at most two per first reason and two per end, so every plan shows up
    merged, order = collections.OrderedDict(), []
    for s, _, path, steps in found:
        key = (path[:-1], steps[-1][2])
        if key not in merged: merged[key] = (s, steps, []); order.append(key)
        if path[-1] not in merged[key][2]: merged[key][2].append(path[-1])
    shown, seen, covered, per_why, per_end = [], set(), set(), collections.Counter(), collections.Counter()  # each chain brings a card not shown yet
    for key in order:
        s, steps, ends = merged[key]; head = key[0]
        pairs = {p for p in zip(head, head[1:])} | {(head[-1], e) for e in ends}
        first = next(why for w, kind, why in steps if kind not in NO_END)
        cards = set(head) | set(ends)
        last = tuple(ends)
        if pairs <= seen or per_why[first] >= 2 or per_end[last] >= 2 or cards <= covered: continue
        seen |= pairs; covered |= cards; per_why[first] += 1; per_end[last] += 1; shown.append((s, head, steps, ends))
        if len(shown) == top: break
    lines_of_ = lambda x: set(zip(x[1], x[1][1:])) | {(x[1][-1], e) for e in x[3]}
    return [x for x in shown if not any(y is not x and lines_of_(x) < lines_of_(y) for y in shown)]  # no chain inside another


def groups(best, nodes):
    """cards that share more line weight with each other than with the rest (each card takes the group its neighbours weigh
    most for, until nothing changes; a line counts less the more partners its two cards have); one group = one plan"""
    root = {n: n for n in nodes}
    for (a, b), (w, kind, why) in best.items():
        if kind == 'levelsinto': root[b] = a
    fam = lambda n: n if root[n] == n else fam(root[n])  # a champion and its level-up forms are one card here
    nb = collections.defaultdict(collections.Counter)
    for (a, b), (w, kind, why) in best.items():
        a, b = fam(a), fam(b)
        if kind == 'targets' or a == b: continue
        nb[a][b] += w; nb[b][a] += w
    deg = {n: len(m) for n, m in nb.items()}  # a card linked to everything (an aura) says little about any one partner
    for a in nb:
        for b in nb[a]: nb[a][b] /= math.sqrt(deg[a] * deg[b])
    keep = {(a, b) for a in nb for b, _ in nb[a].most_common(3)}  # each card counts only its three closest partners
    nb = {a: collections.Counter({b: w for b, w in m.items() if (a, b) in keep or (b, a) in keep}) for a, m in nb.items()}
    nb = collections.defaultdict(collections.Counter, nb)
    label = {n: n for n in nodes}
    order = sorted({fam(n) for n in nodes}, key=lambda n: -sum(nb[n].values()))
    for _ in range(30):
        changed = False
        for n in order:
            if not nb[n]: continue
            score = collections.Counter()
            for m, w in nb[n].items(): score[label[m]] += w
            top = max(score.values()); pick = min((l for l, v in score.items() if v == top), key=lambda l: order.index(l))
            if pick != label[n] and score[label[n]] < top: label[n] = pick; changed = True
        if not changed: break
    parts = collections.defaultdict(set)
    for n in nodes: parts[label[fam(n)]].add(n)
    out = []
    for g in parts.values():
        if len(g) < 2: continue
        why = collections.Counter()
        for (a, b), (w, kind, y) in best.items():
            if a in g and b in g and kind not in ('levelsinto', 'targets'): why[y] += 1  # named by its most common reasons
        out.append((g, ', '.join(y for y, _ in why.most_common(2))))
    return sorted(out, key=lambda x: -len(x[0]))


def measure(c, game, ids, broad=True, limit=10):
    """the network and its measures as data: card ids, so a text or a page can show them"""
    nodes, lines = network(c, game, ids, broad)
    best = best_lines(lines)
    own = [i for i, m in nodes.items() if not m]
    ins, outs, wsum = collections.Counter(), collections.Counter(), collections.Counter()
    for (a, b), (w, kind, _) in best.items():
        outs[a] += 1; ins[b] += 1; wsum[a] += w; wsum[b] += w
    per_node = None if len(nodes) <= 60 else 5
    adj = collections.defaultdict(list)
    for (a, b), (w, kind, _) in sorted(best.items(), key=lambda x: -x[1][0]):
        if per_node is None or len(adj[a]) < per_node: adj[a].append(b)
    bc = betweenness(list(nodes), adj)
    gs = groups(best, nodes)
    gid = {n: k for k, (g, _) in enumerate(gs) for n in g}
    # loose cards: no lines, lines only one way, needs nothing in the set makes
    makes = collections.defaultdict(set)
    for card, h, side, kw in c.execute(f"select card, happening, side, keyword from flat_ref where role='makes' and card in ({','.join('?' * len(nodes))})",
                                       list(nodes)):
        makes[h].add((card, side, kw))
    lack = {}
    for card, h, side, kw, pick in c.execute(f"""select card, happening, side, keyword, pick from flat_ref where role!='makes' and origin='own'
                                               and card in ({','.join('?' * len(own))})""", own):
        side = 'mine' if pick == 'self' else side
        if h in EVERY_GAME or side == 'enemy' or (pick == 'self' and h in ('played', 'summoned')): continue
        if not any(mechanics.FIT(ms, side) and (mk is None or kw is None or mk == kw) for m, ms, mk in makes.get(h, ())):  # itself counts too
            lack.setdefault(card, deck_analysis.say(c, h, side, kw))
    return {'nodes': nodes, 'lines': lines, 'best': best, 'own': own,
            'central': [(i, ins[i], outs[i]) for i in sorted(nodes, key=lambda i: -wsum[i])[:limit] if wsum[i]],
            'through': [i for i in sorted(nodes, key=lambda i: -bc[i]) if bc[i] > 0][:5],
            'chains': [(list(head), [why for _, _, why in steps], ends) for _, head, steps, ends in chains(best, list(nodes), limit, per_node)],
            'groups': gs, 'joined': any(gid.get(a, -1) != gid.get(b, -1) and a in gid and b in gid for (a, b) in best),
            'alone': [i for i in own if not ins[i] and not outs[i]], 'gives': [i for i in own if outs[i] and not ins[i]],
            'gets': [i for i in own if ins[i] and not outs[i]], 'lack': list(lack.items()),
            'linked': sum(1 for i in own if ins[i] or outs[i])}


def report(c, game, ids, title, broad=True, limit=10, json_path=None):
    m = measure(c, game, ids, broad, limit)
    nodes, lines = m['nodes'], m['lines']
    nm = lambda i: mechanics.name(c, i) + (' (made)' if nodes.get(i) else '')
    own = m['own']
    out = [f'{title}: {len(own)} cards, {sum(nodes.values())} more made by them, {len(m["best"])} lines.']
    if json_path:
        json.dump({'game': game, 'nodes': [{'id': i, 'name': mechanics.name(c, i), 'made': x} for i, x in nodes.items()],
                   'lines': [{'from': a, 'to': b, 'kind': k, 'weight': round(w, 4), 'why': y} for (a, b), ls in lines.items()
                             for k, w, y in sorted(set(ls))]}, open(json_path, 'w'), indent=1)
        out.append(f'Network written to {json_path}.')
    out.append('Central cards (strongest lines in and out): ' + ', '.join(f'{nm(i)} ({a} in, {b} out)' for i, a, b in m['central']) + '.')
    if m['through']: out.append('Cards most chains pass through: ' + ', '.join(nm(i) for i in m['through']) + '.')
    out.append('Strongest chains:')
    for head, whys, ends in m['chains']:
        path = [nm(x) for x in head[1:]] + [', '.join(dict.fromkeys(nm(e) for e in ends))]
        out.append('- ' + nm(head[0]) + ''.join(f' -> {why} -> {b}' for why, b in zip(whys, path)))
    gs = m['groups']
    out.append('Groups (cards tightly linked; one group = one plan):')
    for g, why in gs[:limit]:
        names_ = sorted(dict.fromkeys(nm(i) for i in g))
        out.append(f'- {why or "linked"} ({len(g)}): ' + ', '.join(names_[:25]) + (f' and {len(names_) - 25} more' if len(names_) > 25 else ''))
    if len(gs) > limit: out.append(f'- and {len(gs) - limit} smaller groups')
    if len(gs) > 1: out.append(f'The groups are joined to each other by weaker lines: {"yes" if m["joined"] else "no"}.')
    cap = lambda xs: ', '.join(sorted(dict.fromkeys(nm(i) for i in xs))[:15]) + (f' and {len(xs) - 15} more' if len(xs) > 15 else '')
    out.append('Loose cards:')
    if m['alone']: out.append(f'- no lines at all ({len(m["alone"])}): {cap(m["alone"])}')
    if m['gives']: out.append(f'- only give to others, nothing gives to them ({len(m["gives"])}): {cap(m["gives"])}')
    if m['gets']: out.append(f'- only get from others, give nothing back ({len(m["gets"])}): {cap(m["gets"])}')
    for card, what in m['lack'][:limit]: out.append(f'- {nm(card)} waits for "{what}" and nothing here does it')
    if len(m['lack']) > limit: out.append(f'- and {len(m["lack"]) - limit} more cards wait for something nothing here does')
    out.append(f'Overall: {m["linked"]} of {len(own)} cards ({round(100 * m["linked"] / max(1, len(own)))}%) have at least one line; '
               f'{len(gs)} group{"" if len(gs) == 1 else "s"}.')
    return out


def run(c, game, args):
    """ask.py <game> network "<cards>" | faction <name> | game  [--json file]"""
    jp = None
    if '--json' in args:
        k = args.index('--json'); jp = args[k + 1]; args = args[:k] + args[k + 2:]
    cards = cards_of(c, game)
    if args[:1] == ['game']:
        return report(c, game, list(cards), f'{game}, whole game', broad=False, json_path=jp)
    if args[:1] == ['faction']:
        f = ' '.join(args[1:])
        ids = [i for i, x in cards.items() if f.lower() in {r.lower() for r in x['regions']}]
        return report(c, game, ids, f'{game}, faction {f}', broad=False, json_path=jp) if ids else [f'No faction {f} in {game}.']
    ids, unknown = deck_analysis.parse_deck(c, game, ' '.join(args))
    out = report(c, game, list(dict.fromkeys(ids)), f'{game} deck', json_path=jp)
    return out + (['Not found in ' + game + ': ' + ', '.join(unknown) + '.'] if unknown else [])
