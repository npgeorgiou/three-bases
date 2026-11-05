"""A deck, a faction or a whole game as a network of cards, built from the stored rows only, the same way
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
import collections, json, math, os, re, sys
import mechanics, deck_analysis
SITE = collections.defaultdict(set)  # (a, b, why) -> the network.py lines that made such a reason: one reason sentence can come
# from several rules, each reading other parts of the rows; the line checks judge each (sentence, rule) once


class Out(list):
    """A pair's lines (kind, weight, why); notes the code line of every append in SITE."""
    key = None
    def append(self, x):
        if isinstance(x, tuple) and len(x) == 3 and self.key: SITE[self.key + (x[2],)].add(sys._getframe(1).f_lineno)
        super().append(x)


class Lines(collections.defaultdict):
    """(a, b) -> Out, so each Out knows its pair."""
    def __init__(self, *a): super().__init__(Out, *a[1:] if a and a[0] is Out else a)
    def __missing__(self, key):
        v = self[key] = Out(); v.key = key if isinstance(key, tuple) and len(key) == 2 else None; return v

CACHE = {}
# a unit summoned attacking while its maker attacks ("Attack: summon an attacking Living Shadow", Zed): it attacks too (an
# Ephemeral attacker for Hecarim) but joins the attack under way: no new attack (Poppy), unlike a free attack (Dragon Ambush)
JOINS = """select d.card from flat_do d join flat_when w on w.card=d.card and w.ability=d.ability and w.origin=d.origin
           where d.act='start_attack' and d.on_pick='it' and w.event='attacks' and exists (select 1 from flat_do s where s.card=d.card
           and s.ability=d.ability and s.act='summon')"""
PUTS = ('summon', 'create', 'copy', 'play_card', 'revive', 'keyword_action')  # keyword_action with a card: planting it
RULES = ('cost_change', 'cost_set', 'can', 'cant', 'give_keyword', 'give_ability', 'give_type', 'remove_keyword')
KIND_CAT = {'unit': {'unit', 'hero'}, 'landmark': {'building'}, 'spell': {'spell'}, 'equipment': {'item'},
            'unit_or_structure': {'unit', 'hero', 'building'}, 'player': {'leader'},  # a leader card is its player (Duelyst General)
            'board': {'unit', 'hero', 'leader', 'building'}}  # a target of kind any / anything is on the board: never a spell or an artifact
CAT = {'follower': {'unit'}, 'champion': {'hero'}, 'unit': {'unit', 'hero'}, 'spell': {'spell'}, 'skill': {'ability'},
       'landmark': {'building'}, 'equipment': {'item'}}
PLAY_STATE = ('state', 'position', 'terrain', 'distance', 'targets', 'right_of', 'level', 'origin', 'countdown', 'damage')  # true or not only in play
EVERY_GAME = deck_analysis.EVERY_GAME


# games whose terrain cards are creature cards with a trait (Inscryption wiki Traits: "Terrain: cannot be sacrificed"; a Mox card
# is on the board, has Power and Health and is hit like a creature: Gem Animator gives Mox cards +1 Power)
TERRAIN_CREATURES = ('inscryption',)
# a hero that sits in a unit and is no unit itself (Into the Breach pilots): help aimed at units does not reach it
PILOT_GAMES = ('into_the_breach',)
# a type every deck of the game is made of (every squad is Mechs): "all my Mechs" asks for none, it helps them
EVERY_DECK_TYPE = {'into_the_breach': 'Mech'}


def cards_of(c, game):
    """per card: what filters can test before play (category, types, keywords, acts, numbers)"""
    if ('cards', game) in CACHE: return CACHE[('cards', game)]
    d = {}
    for i, n, cat, regions, pw, hp, stats, rar, cost, cx in c.execute("""select id, name, category, regions, power, health, stats, rarity, cost, cost_x from card
                                                              where game=? and is_keyword=0 and is_stub=0 and category!='tribe'""", (game,)):  # a type's own entry is no card
        try: st = json.loads(stats) if stats else {}
        except ValueError: st = {}
        if not isinstance(st, dict): st = {}
        if pw is None and hp is None and '|' in str(stats or ''):  # a level-up form keeps its stats as "power|health"
            a, b = str(stats).split('|', 1)
            pw, hp = (float(a) if a.strip().isdigit() else None), (float(b) if b.strip().isdigit() else None)
        strength = str(st.get('strength', '')).split('/')[0]
        if cat == 'terrain' and game in TERRAIN_CREATURES: cat = 'unit'  # the Terrain trait marks a creature card (Mox, Boulder)
        if cat == 'hero' and game in PILOT_GAMES: cat = 'pilot'  # a pilot acts through its mech; a shield or heal goes to the mech
        d[i] = {'id': i, 'name': n, 'cat': cat, 'regions': set((regions or '').split(';')) - {''}, 'rarity': rar,
                'power': pw, 'health': hp, 'strength': float(strength) if strength.replace('.', '').isdigit() else None,
                'types': set(), 'kws': set(), 'acts': set(), 'cost': cost,  # cost: "a card that costs 7 or more" (was never read)
                'x_cost': bool(cx)}  # "costs X" (Whirlwind) or "spend all your mana" (Thermogenic Beam): the mana paid has no number
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
    key = ('kw_id', game, word.lower())
    if key not in CACHE:
        r = c.execute('select id from card where game=? and is_keyword=1 and lower(name)=?', (game, word.lower())).fetchone()
        CACHE[key] = r[0] if r else None
    return CACHE[key]


def number(c, n):
    if '.' in str(n): return float(n)  # a number written in by the network itself ("cost ge 7.0"); stored filters hold amount ids
    r = c.execute('select x, value from amount where id=?', (n,)).fetchone() if str(n).isdigit() else None
    return r[1] if r and r[0] == 'n' else None


def amount_kind(c, n):
    r = c.execute('select x from amount where id=?', (n,)).fetchone() if str(n).isdigit() else None
    return r[0] if r else None


# cards a unit carries and acts with (Into the Breach weapons and passives: their "self" is the mech): who does what they do
# is the carrier, so they fit "a Mech that kills" (Viscera Nanobots)
CARRIED = {'into_the_breach': (('ability',), 'Mech')}  # weapons; a passive (item) acts for no one mech


def as_doer(c, game, card):
    """the card as the one who does its effects: a carried card is its carrier (a unit of the carrier's type)"""
    if game not in CARRIED or card['cat'] not in CARRIED[game][0]: return card
    key = ('carrier_type', game)
    if key not in CACHE: CACHE[key] = {t for (t,) in c.execute("select id from type where name=? and game=?", (CARRIED[game][1], game))}
    return dict(card, cat='unit', types=card['types'] | CACHE[key])


def matches(c, game, card, kind, withs):
    """can card be one of the target's cards (kind plus filters); things only true in play count as possible"""
    skill = card['cat'] == 'ability' and kind == 'spell' and 'skill' in (withs or '')  # "spells or Skills": a skill is no spell otherwise
    if kind in KIND_CAT and card['cat'] not in KIND_CAT[kind] and not skill: return False
    if kind in ('mana', 'spell_mana', 'effect', 'position', None): return False
    groups = Lines()  # several rows of one attr with op in = one of them
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
            elif attr == 'keyword': hit.append(v.isdigit() and (int(v) in card['kws'] or (int(v) not in printed_kws(c, game) and
                                               kw_tree(c, int(v)) in STATUS_TREES)))  # a status no card prints (Fire, Smoke on an Into
                # the Breach mech) is only given in play: any unit can have it
            elif attr == 'card': hit.append(v.isdigit() and int(v) == card['id'])
            elif attr == 'does': hit.append(v in card['acts'])
            elif attr == 'region': hit.append(v in card['regions'] or v == 'own_regions')
            elif attr == 'rarity': hit.append(v == card['rarity'])
            elif attr == 'name_has':
                ref = name_word(c, v)
                hit.append(str(ref).lower() in card['name'].lower())
            elif attr == 'cost' and amount_kind(c, v) == 'x_paid': hit.append(card['x_cost'])  # "your cost X cards" (Chemical X)
            elif attr == 'cost' and card['cost'] is None: hit.append(False)  # no number to compare: unplayable, X, a relic
            elif attr in ('power', 'health', 'strength', 'cost'):
                x, have = number(c, v), card.get(attr)
                if x is None or have is None: hit.append(True); continue
                hit.append({'lt': have < x, 'le': have <= x, 'eq': have == x, 'ge': have >= x, 'gt': have > x, 'in': have == x}.get(op, True))
            else: hit.append(True)
        ok = all(hit) if op == 'is' else any(hit)  # "a Mecha Yordle" = type is Mecha and type is Yordle; op in = one of them
        if (op == 'not') == ok: return False
    return True


def name_word(c, v):
    """the text a "name has" filter looks for: a card's name, or a stored name part ("allied Pykes": Pyke)"""
    key = ('name_word', v)
    if key not in CACHE:
        r = v.isdigit() and (c.execute('select name from card where id=?', (int(v),)).fetchone() or
                             c.execute('select word from name_part where id=?', (int(v),)).fetchone())
        CACHE[key] = r[0] if r else v
    return CACHE[key]


STATUS_TREES = ('damage_over_time', 'attack_lock', 'disable', 'immobilize', 'debuff', 'temporary_buff', 'shield')  # statuses put on units


def state_kw(c, game, state):
    """the keyword a state value is (vocab meaning = a keyword's name in this game: ephemeral -> Ephemeral), or None"""
    key = ('state_kw', game, state)
    if key not in CACHE:
        m = c.execute("select meaning from vocab where field='state' and value=?", (state,)).fetchone()
        CACHE[key] = kw_id(c, game, m[0]) if m and m[0] else None
    return CACHE[key]


def printed_kws(c, game):
    """keywords some card of the game has printed; the others are statuses given in play"""
    key = ('printed', game)
    if key not in CACHE: CACHE[key] = {k for (k,) in c.execute("""select distinct ck.keyword from card_keyword ck join card k on k.id=ck.card
                                         where k.game=? and k.is_keyword=0""", (game,))}
    return CACHE[key]


def kw_states(c, game, withs):
    """the keywords a "state is" filter asks for that cards print ("an Ephemeral ally"): a card has them only if it prints them
    or a card gives them; statuses given in play (Frostbite, Stun) any unit can have"""
    ks = [state_kw(c, game, p[9:]) for p in (withs or '').split(';') if p.startswith('state is ')]
    return [k for k in ks if k and k in printed_kws(c, game) and kw_tree(c, k) not in STATUS_TREES]


def who_fits(c, game, card, kind, withs):
    """can this card be the one a need names, keyword states included (Zed is no Ephemeral ally; his Living Shadow is)"""
    return matches(c, game, card, kind, withs) and all(k in card['kws'] for k in kw_states(c, game, withs))


SEND_ACTS = ('strike', 'first_strike', 'double_strike', 'start_attack', 'ready', 'move', 'swap')  # it makes a unit act


def aimed_whos(c, game, acts=None):
    """per card, the filter of each of my units it acts on (not itself), or only those it makes act (acts): "card is Dragonling"
    for Dragon Ambush; what it acts on right after making it ("summon 2 Spectral Riders ... attacking") is the card it made"""
    key = ('aimed_whos', game, acts)
    if key in CACHE: return CACHE[key]
    cards = cards_of(c, game); made = collections.defaultdict(set); out = Lines()
    rows = c.execute("""select card, ability, act, card_ref, on_pick, on_with from flat_do where origin in ('own','uses_keyword','has_keyword')
            and coalesce(on_side,'mine') in ('mine','any') and coalesce(on_pick,'') not in ('self','owner')
            and coalesce(on_kind,'unit') in ('unit','any','anything','hero')""").fetchall()
    for a, ab, act, ref, pick, w in c.execute("select card, ability, act, card_ref, on_pick, on_with from flat_do where act in ('summon','create') and card_ref is not null"):
        made[(a, ab)].add(ref)
    for a, ab, act, ref, pick, w in rows:
        if a not in cards or act in ('summon', 'create') or (acts and act not in acts): continue
        if pick == 'it' and made.get((a, ab)): out[a] += [f'card is {r}' for r in made[(a, ab)]]
        else: out[a].append(w or '')
    if not acts or 'start_attack' in acts:  # Rally (an attack token for my player): any of my units can attack with it
        for (a,) in c.execute("select distinct card from flat_do where act='gain_attack_token' and coalesce(on_side,'mine')='mine'"):
            if a in cards: out[a].append('')
    CACHE[key] = out
    return out


def can_aim_at(c, game, a, kind, withs, acts=None):
    """the card itself is such a card, or something it acts on (acts: makes act) can be one (Ghost gives any ally Elusive: Zed
    too; Dragon Ambush sends only Dragonlings)"""
    cards = cards_of(c, game)
    if who_fits(c, game, cards[a], kind, withs): return True
    named = lambda w: any(p.split(' ')[0] in ('card', 'name_has', 'type') for p in (w or '').split(';'))
    whos = aimed_whos(c, game, acts).get(a, ())
    if not whos and not acts and cards[a]['cat'] not in KIND_CAT['unit']: return True  # help on no unit of mine (Rally: every ally
    # attacks again) can help any; a card that makes no unit act is no doer
    for who in whos:
        if not named(who) and not named(withs) and not kw_states(c, game, withs): return True
        if any(who_fits(c, game, b, 'unit', who) and who_fits(c, game, b, kind, withs) for b in cards.values()): return True
    return False


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
    kinds = [p for p in (want or '').split(';') if p.split(' ')[0] in ('type', 'cost', 'keyword', 'region') and p.split(' ')[1:2] != ['not']]
    have_ = [p for p in (have or '').split(';') if p.split(' ')[:2] in (['type', 'is'], ['name_has', 'is'], ['card', 'is'])]
    if not ref and have_ and [p for p in kinds if p.split(' ')[:2] == ['type', 'is']] and not set(have_) & set(kinds): return False  # it
    # makes a named kind that is not the one asked (Domination summons a Husk: no Poro for The Poro King)
    if ref in cards and kinds and not matches(c, game, cards[ref], 'any', ';'.join(kinds)): return False  # the card it makes must be
    # the kind asked for (Emperor's Divide summons Sand Soldiers: no Elite for For The Fallen)
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
       'trap_activated': 'plants traps that go off later', 'countdown_done': 'finishes countdowns', 'exhausted': 'exhausts cards'}  # the opponent sets traps off
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
    if y.startswith(('can heal it', 'heals it', 'can restore', '{A} heals')): return 'heals'
    if y.startswith('clears its line'): return 'clears'
    if y.startswith(('moves', 'lets it enter')): return 'moves'
    if y.startswith(('another attack', 'more health or protection', 'helps my units', 'helps it hit', 'more damage', 'fills your hand',
                     'empties your hand')): return 'waits'  # makes what it waits for happen more
    g = next((y.split(x, 1)[1] for x in ('can give it ', 'gives it ') if y.startswith(x)), None)
    if g is not None and not (g[:1] in '+-0123456789' or g.startswith(('X|', 'X ', 'more '))): return 'keyword'
    return 'stronger'


OWN_LOSS = ('dies', 'killed', 'damaged', 'survives_damage', 'sacrificed')  # what fights do to my own units


def reacts_against(c, game):
    """abilities that act against what sets them off ("exhaust it") or are a secret the opponent reveals (Sentinel): with no
    side named, they wait for the enemy's cards (L5, L9)"""
    if ('react', game) in CACHE: return CACHE[('react', game)]
    r = {ab for ab, acts in c.execute("""select ability, group_concat(act || ':' || coalesce(on_pick,'') || ':' || coalesce(keyword_ref,''))
                   from flat_do where origin='own' group by ability""") if acts and all(
                   x.split(':')[1] == 'it' and (x.split(':')[0] in ('exhaust', 'damage', 'kill', 'stun', 'silence', 'transform', 'bounce')
                   or (x.split(':')[0] == 'give_keyword' and x.split(':')[2].isdigit() and kw_tree(c, int(x.split(':')[2])) in BAD_STATUS))
                   for x in acts.split(','))}
    r |= {ab for ab, card in c.execute("""select d.ability, d.card from flat_do d where d.origin='own' and d.act='transform'
                    and d.on_pick='self'""") if any(kw_tree(c, k) == 'trap_secret' for k in cards_of(c, game).get(card, {}).get('kws', ()))}
    CACHE[('react', game)] = r
    return r


def lines_of(c, game):
    """every waits / levels / puts / repeats / type line of the game: (a, b) -> [(kind, weight, why)]"""
    if ('lines', game) in CACHE: return CACHE[('lines', game)]
    cards = cards_of(c, game)
    out = Lines()
    lvl = {a for (a,) in c.execute("select ability from flat_do where act='level_up'")}
    makes, takes = collections.defaultdict(set), collections.defaultdict(set)
    react_enemy = reacts_against(c, game)
    own_makes, lvl_needs, made_by = collections.defaultdict(set), collections.defaultdict(set), collections.defaultdict(set)
    ab_card = dict(c.execute('select id, card from ability'))
    helps = adder_abilities(c, game)  # "your spells deal 1 extra damage" waits for nothing: it helps those cards (gives_lines)
    rule_name = {i: n.removeprefix('Game rule: ') for i, n in c.execute("select id, name from card where category='game_rule'")}
    harm_abs = harm_abilities(c)
    land_takers = {a for (a,) in c.execute("select card from flat_do where act='steal' and on_kind='position'")}
    lacks = {(ab, int(p.split(' ')[2])) for ab, w in c.execute("select ability, of_with from flat_if where test='have' and op='not' and of_with like '%keyword is %'")
             for p in (w or '').split(';') if p.startswith('keyword is ') and p.split(' ')[2].isdigit()}
    gives_kw = {(a, k): (ok, os_) for a, k, ok, os_ in c.execute("""select card, keyword_ref, on_kind, coalesce(on_side,'mine') from flat_do
                where act='give_keyword' and origin='own' and coalesce(on_side,'mine')='mine' and coalesce(on_pick,'')!='self'""")}
    cost_rules = {rule_name.get(e) for (e,) in c.execute('select entry from game_rule where cost_has is not null')}
    actor_side = {(a, b): sd for a, b, sd in c.execute("select card, ability, actor_side from flat_when where actor_side is not null")}
    # "when I attack" of a weapon, "when repairing" of a pilot: the holder uses it (Enrage Shot makes a Vek attack, it fires no
    # weapon a mech carries; Force Swap's heal is no repair by Harold Schmidt): only the card itself does it
    own_use = {(a, b) for a, b in c.execute("select card, ability from flat_when where actor_pick='self' and obj_pick is null")
               if a in cards and cards[a]['cat'] in ('ability', 'pilot')}
    doer_helps = doer_help_abilities(c)
    # damage only from bumps ("Vek take +1 damage from Bumps", Force Amp): what pushes enemies into things feeds it, not damage
    bump_abs = {}
    for a_, ab_, w_ in c.execute("select card, ability, of_with from flat_if where test='it_matches' and of_with like '%origin %'"):
        o_ = set(re.findall(r'origin (?:is|in) (\w+)', w_ or ''))
        if o_ and o_ <= {'bump', 'blocking_emerging'}: bump_abs[ab_] = a_
    plain_hits, keepers, cheap_abs = special_abilities(c)
    by_combat = {}  # (card, happening) made only through a combat keyword it has (Overwhelm): combat damage
    grants = {(a, k) for a, k in c.execute("select card, keyword_ref from flat_do where origin='own' and act='give_keyword' and keyword_ref is not null")}
    kw_adds = {ab for _, ab, *_ in keyword_adders(c, game)}  # "apply 1 more Poison" adds to others' Poison: it applies none alone
    gv = collections.defaultdict(set)  # where each card's given abilities go: to my player or itself, or to other cards
    for a_, k_, s_, p_ in c.execute("select card, on_kind, on_side, on_pick from flat_do where act='give_ability' and origin='own'"):
        gv[a_].add((k_ == 'player' and s_ in ('mine', None)) or p_ in ('self', 'owner'))
    self_given = {a_ for a_, x in gv.items() if x == {True}}
    hit_abs = {a_ for (a_,) in c.execute("""select ability from flat_do where origin='own' and act in ('damage','kill','obliterate')
               and coalesce(on_side,'')='' and on_pick='chosen'""")}  # a harm on a unit the player picks, of no named side
    # what a card does to the things a happening left ("revive the strongest dead ally": it brings back what died)
    state_use = {}
    for a_, ab_, act_, kw_ in c.execute("""select card, ability, act, keyword_ref from flat_do where origin='own' and
            (coalesce(on_with,'') like '%state is%' or coalesce(on_zone,'') in ('discard','exhausted')) order by seq"""):  # the act on
        # those very things (not "deal damage equal to your Block": Body Slam does nothing to the Block)
        if act_ == 'strike' and (a_, ab_) not in state_use: state_use[(a_, ab_)] = 'strikes them'; continue  # "I strike it" (Yasuo)
        if (a_, ab_) not in state_use and act_ in AIM:
            v_, _, rest_ = AIM[act_].format(kw=mechanics.name(c, kw_) if kw_ else 'a keyword').removeprefix('can ').replace(' it', ' them').partition(' ')
            state_use[(a_, ab_)] = (v_ if v_.endswith('s') else v_ + 'es' if v_.endswith(('sh', 'ch', 'x')) else v_ + 's') + ' ' + rest_  # "brings them back"
    it_side = {ab_: sd_ for ab_, sd_ in c.execute("select ability, side from flat_ref where role='trigger' and side in ('enemy','mine') and coalesce(pick,'')!='self'")}
    it_side = {ab_: sd_ for ab_, sd_ in it_side.items() if not c.execute("select 1 from flat_do where ability=? and origin='own' and on_pick not in ('self','it') limit 1", (ab_,)).fetchone()}
    self_kw = {(a_, k_) for a_, k_ in c.execute("""select g.card, g.keyword_ref from flat_do g where g.origin='own' and g.act='give_keyword'
               and (g.on_pick='self' or (g.on_pick='it' and exists (select 1 from flat_do d where d.ability=g.ability and d.seq<g.seq
               and d.act in ('copy','create','summon') and d.on_pick='self')))""")}
    for card, origin, ab, role, h, side, kw, pick, kind, w, ref, ak, aw, via in c.execute(
            'select card, origin, ability, role, happening, side, keyword, pick, kind, obj_with, ref, actor_kind, actor_with, via from flat_ref'):
        if card not in cards: continue
        if role == 'makes':
            if ab in kw_adds: continue
            if pick == 'it' and not side and origin == 'own' and ab in it_side: side = it_side[ab]  # "when you Stun an enemy, I strike
            # it" (Yasuo): it is that enemy
            if origin == 'uses_keyword' and pick == 'it' and not side and (card, via) in self_kw: pick = 'self'  # a keyword it gives its own
            # copy (Prancing Sea Spirits' Ephemeral): that death is its own, no kill for other cards (L9, L14)
            if h in ('dies', 'killed') and side == 'enemy' and origin in ('own', 'has_keyword') and ab in plain_hits: continue  # a plain hit on one
            # enemy (Strike) is what every attack does: it feeds no "when an enemy dies" (Kaptain 30 Oct 2026); poison, hits on all,
            # kill effects and damage boosts still do
            if origin == 'has_keyword' and not pick and kw_tree(c, via) in HIT_KW + ('lifesteal', 'deathtouch') and \
                    h in ('strikes', 'strikes_nexus', 'fights', 'attacks', 'nexus_damaged'):
                pick = 'self'  # a fight keyword works for the card that has it (Nasus's Fearsome gets Nasus, not Abyssal Eye, to the Nexus)
            if origin == 'has_keyword' and pick == 'self' and cards[card]['cat'] not in ('unit', 'hero', 'building', 'leader', 'pilot'): continue  # a
            # spell naming a keyword it gives the enemy (Grotesque Gift's Gloom) does not have it: the keyword's own work is no act of the spell (L9, L15)
            if origin == 'has_keyword' and not pick and h in ('moves', 'moves_onto'): pick = 'self'  # a move keyword moves only its own
            # card (Kaptain 3 Nov 2026: Dragonlark's Flying puts no other unit around Vigilator; L20)
            if pick == 'self' and not kind: kind = {'leader': 'player', 'hero': 'unit', 'pilot': 'unit'}.get(cards[card]['cat'], cards[card]['cat'])  # it
            # moves itself as what it is: Azurite Lion moving is no General moving (Zeal)
            makes[h].add((card, side, kw, kind, pick, w, ref, rule_name.get(via, 'rules') if origin == 'game' else False))
            if h == 'attacks' and origin == 'own': makes['strikes'].add((card, side, kw, kind, pick, w, ref, False))  # an attack it gives
            # (Rally) is a strike too: "when I strike" goes off (Golden Aegis -> Akshan; L2, L4)
            if origin != 'game': own_makes[card].add(h); made_by[(card, h)].add('fight_kw' if origin == 'has_keyword' and kw_tree(c, via) in HIT_KW + ('aoe_damage', 'deathtouch', 'lifesteal') else origin)
            ok_ = KW_NEEDS.get(kw_tree(c, via)) if origin == 'has_keyword' or (origin == 'uses_keyword' and (card, via) in grants) else None  # a
            # fight keyword it has or grants (Quick Attack); not one it uses as an action (Drain deals damage itself: Vile Feast)
            if ok_ is not None and by_combat.get((card, h), 1) is not None: by_combat[(card, h)] = set(ok_) | (by_combat.get((card, h)) or set())
            elif origin != 'game': by_combat[(card, h)] = None  # made also by its text, not only by a fight keyword
            continue
        # a keyword condition the card uses (Plunder, Reputation, Deep) is the card's own need (its rows sit on the card's own
        # ability, or on none for a keyword it has); the rows of a keyword it gives or uses on a target are not
        kwcond = role in ('condition', 'state') and ((origin == 'uses_keyword' and ab_card.get(ab) == card) or (origin == 'has_keyword' and ab is None))
        # where a keyword needs its holder to stand (Backstab: behind an enemy; Zeal: near my General): the holder's need, also when
        # the card gives the keyword to my unit or player (Mask of Shadows gives the General Backstab)
        if role == 'state' and h == 'moves' and origin == 'has_keyword' and (pick == 'self' or kind == 'player'): kwcond = True
        if role == 'state' and h == 'moves' and origin == 'uses_keyword' and pick == 'self' and (card, via) in gives_kw:
            kwcond = True; kind, side, pick = gives_kw[(card, via)][0], 'mine', None  # the holder is what the card gives it to
        # a keyword that waits for other units' deaths (Scavenger: Bones when opposing creatures die; Corpse Eater, Double Death):
        # the holder's need, like its own text; other keyword triggers are what the keyword does for every holder
        if role == 'trigger' and origin == 'has_keyword' and h in ('dies', 'killed') and pick not in ('self', 'actor_self', 'attached_to'): kwcond = True
        cost = origin == 'game' and role == 'condition'  # a cost the game's rules set (Inscryption Bones, Blood, Mox): the card needs it
        if origin == 'gives' and card in self_given: origin = 'own'  # "Last Breath: the next time an Ephemeral ally attacks, revive
        # me": an ability it gives its own player or itself is its own need (Hecarim's Ephemeral attackers set off Shark Chariot)
        if (origin != 'own' and not kwcond and not cost) or \
           (pick == 'self' and h in ('played', 'summoned')) or pick == 'actor_self' or (role == 'trigger' and (card, ab) in own_use): continue  # "I've killed 4": only the card itself
        if ab in helps or (role == 'trigger' and (ab in doer_helps or ab in bump_abs)): continue  # "heal the Mech that kills": it helps the killer
        # (doer_help_lines), it waits for no kill
        if ab in harm_abs or (role == 'trigger' and ab in protect_abilities(c)) or (role == 'condition' and (ab, h) in capped(c)): continue  # "take 1 damage when summoned" (Kujata): it
        # hurts my cards, it wants none; "the first time your General takes damage, prevent 2": it protects, it wants no damage. (A
        # trigger that helps the card that sets it off still waits for more of it from other cards: draws for Janna's discounts; the
        # card itself is no enabler of it: played_lines and the type lines skip it, Golem Metallurgist)
        if role == 'state' and ab in keepers: continue  # "Block is not removed" needs no Block: it helps the Block cards (boost_lines)
        if role == 'state' and h == 'given_keyword' and kw and (ab, kw) in lacks: continue  # "if you have no Block, gain 11 Block"
        # (Auto-Shields, Orichalcum): it wants none of it
        if ab in lvl and role != 'state': lvl_needs[card].add(h)  # a state the counted cards must be in ("8 cost reduced cards
        # played", Janna) is no count its own trigger feeds: her discount on drawn cards still needs the player to play them
        # (Kaptain 31 Oct 2026: draws do not level Janna)
        if role == 'trigger' and not side and ab in react_enemy: side = 'enemy'  # it reacts against what sets it off ("whenever ANY player
        # summons a minion with Rush, exhaust it", Night Watcher) or is a secret revealed by the opponent (Sentinel): my own cards
        # set off only a drawback (L5, L9)
        if role == 'state' and not side and ab in hit_abs: side = 'enemy'  # "deal 5 to a Flying unit" (Destructive Volley): a harm aimed
        # by a filter is for the enemy's cards (L9), my Flying units feed it nothing
        takes[h].add((card, 'mine' if pick == 'self' else side, kw, kind, pick, w, ab in lvl, role,
                      (ak, aw, actor_side.get((card, ab)) if role == 'trigger' else None), cost, ab in cheap_abs,
                      state_use.get((card, ab), '') if role == 'state' else ''))
    deck_created_draw = {x for (x,) in c.execute("select distinct card from flat_do where act='draw' and origin='own' and on_zone='deck' and on_with like '%state is created%'")}
    deck_makers = {x for (x,) in c.execute("select distinct card from flat_do where act in ('create','copy','shuffle_into_deck') and origin='own' and (on_zone like 'deck%')")}
    state_ev = collections.defaultdict(set)  # a state and the happenings that put things in it (damaged <- damaged)
    for v, cs in c.execute("select value, causes from vocab where field='state' and coalesce(causes,'')!=''"):
        state_ev[v] |= {x.split(':')[0] for x in cs.split(';')}
    # damage to my side by amount: damage as big as a card's health kills it, so it never survives it (Sunburst deals 6, Braum has 6)
    hits = Lines()
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
    has_units = any(x['cat'] in KIND_CAT['unit'] for x in cards.values())
    # cards whose own text adds a fight keep their rule lines: a strike now, a second strike, a free attack; not a unit summoned
    # attacking while attacking (it joins the attack under way: Zed), not Quick Attack (it changes how one attack goes)
    rule_fighters = {a for (a,) in c.execute(f"""select card from flat_do d where (origin='own' or (origin='uses_keyword' and coalesce(on_pick,'')!='self')) and (act in ('strike','double_strike')
            or (act='start_attack' and card not in ({JOINS})))""")}  # its own text; Ranged Attack only changes how one attack goes
    fight_kw = collections.defaultdict(set)  # a fight keyword it has and what that keyword adds (Overwhelm: only the Nexus hit)
    for a, tree in c.execute("""select ck.card, v.tree from card_keyword ck join card k on k.id=ck.keyword join vocab v on
            v.field='keyword' and v.value in (k.name, k.game || ':' || k.name) where v.tree in ('multi_attack', 'aoe_damage', 'excess_damage')"""):
        fight_kw[a].add(tree)
    def fights_for(m, h, side=None):  # its own text or keyword makes it fight more for this need (Hecarim's Overwhelm kills no more units: Thresh)
        if m in rule_fighters: return True
        ks = fight_kw.get(m, ())
        return ('multi_attack' in ks and h not in ('nexus_damaged', 'strikes_nexus')) or ('aoe_damage' in ks and h in ('damaged', 'dies', 'killed', 'survives_damage') and side == 'enemy') or \
            ('excess_damage' in ks and h in ('nexus_damaged', 'strikes_nexus'))
    # or hits more than one (Celerity, Frenzy, Overwhelm); Ranged or Quick Attack only change how one attack goes; Frenzy's extra
    # hits feed only a need about enemies, not "whenever a unit dies" (Piercing Mantis -> Gate to the Undervault: no line, L21); a
    # second attack gets no unit past blockers to the Nexus (L4: Greathorn Companion's Scout -> Angel's Plunder, no line)
    # cards that make an enemy unit act (strike, attack, turn its attack): only these do what an enemy must do
    enemy_doers = {a for (a,) in c.execute("""select card from flat_do where act in ('strike','start_attack','redirect_attack')
                   and coalesce(on_side,'') in ('enemy','')""")}
    strikers = {a_ for (a_,) in c.execute("""select card from flat_do where origin='own' and act in ('strike','start_attack')
                and coalesce(on_side,'mine')='mine' and on_pick in ('chosen','all','random')""")}

    def doer_fits(m, actor, h=None):
        """who must do it ("an ally deals damage", "allied Pykes"): the card itself, or a card that makes such a unit fight; the
        player does most things through any card ("whenever you replace a card"), but fights only as its leader ("whenever your
        General attacks": the General card, Duelyst)"""
        ak, aw, aside = actor
        if aside == 'enemy': return m in enemy_doers  # "when an enemy damages another enemy" (Vek Hormones): my own damage is not it
        if ak == 'player' and not aw and h not in ('attacks', 'strikes', 'killed', 'strikes_nexus', 'fights') + (('damaged',) if leader_game else ()):
            return True  # "whenever your General deals damage" (Horn of the Forsaken): the General card, not any unit (Duelyst)
        if ak not in KIND_CAT and not aw: return True
        k = ak if ak in KIND_CAT else 'any'
        if who_fits(c, game, as_doer(c, game, cards[m]), k, aw): return True
        # a card that makes units fight: only if a unit it sends can be the one named (Dragon Ambush sends Dragonlings, not Zed)
        if ak in ('unit', None) and m in strikers and can_aim_at(c, game, m, 'unit', aw, ('strike', 'start_attack')): return True  # "an ally
        # strikes" (Bone Skewer) can be a named ally ("allied Pykes have dealt 15+ damage"; L2: a strike now)
        return ak in ('unit', None) and m in fighters and not any(p.split(' ')[0] in ('card', 'name_has', 'type') for p in (aw or '').split(';')) \
            and can_aim_at(c, game, m, 'unit', aw, SEND_ACTS)
    # a card whose own triggers make what its level-up counts (Ashe frostbites when she attacks): feeding the trigger levels it
    selffeed = {t for t in lvl_needs if lvl_needs[t] & own_makes[t]}
    # a stat it tests or uses ("restore that minion's Health"): only a change of that stat feeds it (+Attack adds no Health)
    stat_need = collections.defaultdict(set)
    for t, at in c.execute("select card, attr from flat_if where test in ('stat','amount_stat') and attr in ('health','power')"): stat_need[t].add(at)
    stat_made = collections.defaultdict(set)
    for m, ps in c.execute("select card, params from flat_do where act in ('stat_change','stat_set','grow','swap_stats')"):
        stat_made[m] |= {x.split('=')[0] for x in (ps or '').split(';') if x.split('=')[0] in ('power', 'health', 'strength')
                         and x.split('=', 1)[1].lstrip('-').replace('.', '', 1).strip('0') != ''} or {'power', 'health'}  # "+1|+0" changes no Health
    set_only = {m for m in stat_made if not c.execute("select 1 from flat_do where card=? and act in ('stat_change','grow','swap_stats') limit 1", (m,)).fetchone()}  # a card that only SETS stats (Agent Venom: power 3)
    # what a quarter or more of the game's cards do to enemies (damage them, kill them) is what any deck does: a card that waits
    # for it ("whenever an Attack deals unblocked damage", Envenom) gets no line from each (L1b; Kaptain 2 Nov 2026), unless it
    # levels up from it
    share = collections.Counter((h, ms) for h, ms_ in makes.items() for ms in {(x[1] or '') for x in ms_}
                                for m in {x[0] for x in ms_ if (x[1] or '') == ms and not x[7]})  # by the cards' own text, not the rules' fights
    common = {k for k, v in share.items() if k[0] in ('damaged', 'killed', 'dies', 'survives_damage') and k[1] in ('enemy', '') and v >= 0.25 * len(cards)}
    from_kw = collections.defaultdict(set)  # "when an ally gains Power from Hallowed" (Gwen): only a change Hallowed makes ()
    for t, h, k in c.execute("select w.card, w.event, k.ref_keyword from cond k join flat_when w on w.ability=k.ability where k.test='keyword_condition' and k.ref_keyword is not null and w.event='stat_changed'"):
        from_kw[(t, h)].add(k)
    kw_givers = lambda k: CACHE.setdefault(('kwg', game, k), givers_of(c, game, k, list(cards)))
    home_m = home_only(c)[0]  # it moves units only onto my own land (Desert Twister): no unit reaches enemy land by it
    for h, ts in takes.items():
        carers = collections.defaultdict(set)
        for t, _, tk, *_ in ts: carers[tk].add(t)
        for m, ms, mk, mkind, mpick, mw, mref, rule in makes.get(h, ()):
            for t, ts_, tk, tkind, tpick, tw, lv, role, actor, cost, cheap, use in ts:
                if m == t or not mechanics.FIT(ms, ts_) or not (mk is None or tk is None or mk == tk): continue
                if not rule and not lv and made_by.get((m, h)) == {'fight_kw'} and (h in ('nexus_damaged', 'strikes_nexus', 'strikes', 'fights', 'attacks')
                        or (h in OWN_LOSS and ts_ != 'enemy')):  # Frenzy's hits feed no "whenever a unit dies" (Piercing Mantis -> Gate)
                    continue  # made only by its own fight keyword: an attack any unit makes (L2, L20: Alpha Wildclaw -> Snowy Razorclaw)
                if (h, ms or '') in common and tpick != 'self' and not lv and not (actor and actor[2] == 'enemy'): continue  # an enemy
                # that hits other enemies (Vek Hormones) waits for what few cards do: turning the enemy's attack (Spartan Shield)
                if not kinds_fit(mkind, tkind): continue
                if h == 'created' and not ms and ts_ == 'enemy': continue  # cards I create are mine, never the enemy's created cards a need counts (L9: Beta Ray Bill -> Gorgon)
                if from_kw.get((t, h)) and not any(k in cards.get(m, {}).get('kws', ()) or m in kw_givers(k) for k in from_kw[(t, h)]): continue
                if m in home_m and h in ('moves', 'moves_onto') and 'position enemy' in (tw or ''): continue
                if tpick == 'self' and mkind in KIND_CAT and mkind != 'player' and cards[t]['cat'] not in KIND_CAT[mkind]: continue  # Noxian Fervor hits units:
                # Scrappy Bomb, a landmark, is never its target (L8)
                if h == 'created' and role == 'state' and not tpick and not tkind: tpick = 'self'  # "if I was created" (Cunning Kitten)
                mcats = {x for p_ in (mw or '').split(';') if p_.startswith(('category is ', 'category in ')) for x in p_.split(' ')[2:]}
                if mcats and tkind in KIND_CAT and not {y for x in mcats for y in CAT.get(x, {x})} & (KIND_CAT[tkind] | {tkind}): continue  # Acoustician creates spells, Norra
                # counts created units (L20)
                if tpick == 'self' and h in ('created', 'summoned', 'drawn') and mref and mref != t: continue  # Angel creates Coins, never
                # the Cunning Kitten that waits to be created (L20)
                if tpick == 'self' and mkind == 'player' and h in ('moves', 'moves_onto') and cards[t]['cat'] != 'leader': continue  # done to my General or player, never to
                # this card (L7: Mist Walking moves the General, not Gore Horn)
                if mpick == 'self' and tpick == 'self': continue  # each card about itself ("when I level up"): no link between two cards
                if not names_fit(c, game, cards, tw, mw, mref): continue
                if not terrain_fit(tw, mw): continue
                if tpick == 'self' and mpick != 'self':  # done to one of my units that must be this card ("give the Demon Wing Flying",
                    who = ';'.join(p for p in (mw or '').split(';') if p.split(' ')[:2] in (['card', 'is'], ['type', 'is'], ['type', 'in'],
                                                                                        ['name_has', 'is'], ['keyword', 'is']))  # "another Rakoan";
                    # "ready all Ranged units" (Bombard) reaches only a card with Ranged
                    who = ';'.join(x for x in (who, state_filter(c, game, mw), trig_state_of(c, game, m) if mpick == 'it' else '') if x)  # "an Ephemeral ally" (Soul Shepherd -> Vi: no line)
                    if who and not matches(c, game, cards[t], 'any', who): continue
                if tkind in RESOURCE_WORD and not colour_fit(tw, mw): continue  # a Green Mox cost is paid by a Green gem only
                if mpick == 'self':  # what a card does to itself feeds only a need its own kind fits ("the strongest friendly Dragon")
                    own = ';'.join(p for p in (tw or '').split(';') if p.split(' ')[:2] in (['type', 'is'], ['type', 'in'], ['card', 'is'], ['name_has', 'is'], ['keyword', 'is']))
                    if own and not matches(c, game, cards[m], 'any', own): continue
                if mpick == 'self' and role == 'state' and h in ('moves', 'moves_onto'): continue  # a card moving itself puts no unit
                # where another card acts: every unit moves (Kaptain 3 Nov 2026: Dragonlark -> Vigilator, Azurite Lion -> Roar: no line)
                if role == 'state' and h in ('moves', 'moves_onto') and place_of(tw) == 'on the space it picks': continue  # any space
                # it picks (Chromatic Cold): where units stand does not matter to it
                # a card that only moves itself (Ice Mech's Flying) puts itself, not enemies, where another card hits
                if h == 'survives_damage' and tpick == 'self' and lethal(m, t): continue
                if h == 'dies' and tpick == 'self' and m in hits and m not in killers and weak(m, t): continue  # 1 damage kills no 4-health unit
                if h == 'stat_changed' and role == 'condition' and stat_need.get(t) and stat_made.get(m) and \
                        not (stat_need[t] & stat_made[m]) and 'strength' not in stat_made[m]: continue
                if h == 'stat_changed' and m in set_only and ms != 'enemy' and role in ('condition', 'state'): continue  # a set is no buff and reaches no power threshold above it (Agent Venom -> Wolverine Horseman of War; L4, L18)
                if not doer_fits(m, actor, h): continue
                # my units are hurt or die in fights by the rules: every unit would feed "when a friendly unit dies" (Soul Eater,
                # Shaytan Monstrosity); only cards that hurt or kill my units do (Kaptain 30 Oct 2026); a cost the rules pay stays
                if rule and not cost and h in OWN_LOSS and ms != 'enemy': continue
                # a rule that needs a place ("harvest a well next to it": an enemy well is deep in enemy ground) is done by the units
                # that get there, not by every unit: what moves them is the help (HELPS movement); Gabrian Archon -> Wavecrash Colossus
                if rule and not cost and 'position ' in (mw or ''): continue
                if (rule == 'units fight' or by_combat.get((m, h)) is not None) and 'origin not combat' in (tw or ''): continue  # Overwhelm damage is combat (Captain Farron, Swain)
                if 'origin is combat' in (tw or '') and not (rule == 'units fight' or by_combat.get((m, h)) is not None or m in fighters):
                    continue  # "perishes by combat" (Corpse Eater): a kill by an effect is no combat (Hammer -> Corpse Maggots)
                bc = by_combat.get((m, h))  # made only by a fight keyword (Quick Attack, Fearsome, Overwhelm): only the needs that keyword
                if bc is not None and not (('nexus' in bc and (h in ('nexus_damaged', 'strikes_nexus') or tkind == 'player')) or h in bc): continue
                # really serves: Overwhelm and evasion reach the Nexus, deathtouch kills; Quick Attack adds no strike (Blade of the Exile)  # "non-combat damage": fighting is combat  # "allied Pykes have dealt damage": the damage of a spell or another unit is not it
                if h == 'created' and t in deck_created_draw and m not in deck_makers: continue  # King Eitri draws created cards from the deck:
                # only a card that puts cards into the deck feeds it, not one that creates into the hand (Agent 13)
                need = {e for p in (tw or '').split(';') if p.startswith('state is ') for e in state_ev.get(p[9:], ())} - {h}
                if need and h in ('played', 'summoned', 'drawn', 'created') and not need & own_makes[m]: continue  # "8 cost reduced cards
                # played": playing a card no one made cheaper is not it (a unit healed is damaged by the enemy too: no such need)
                w = 1.0 / len(carers[tk] | (carers[None] if tk else set()))
                say = act_say(c, h, ts_, tk, self_=tpick == 'self')
                if role == 'state' and h in ('moves', 'moves_onto') and 'position is same_lane' in (tw or '') and game == 'marvel_snap': continue  # a lane is a location, not a range: a unit moved in is no help to a card that acts in its lane (Doctor Strange -> Danger)
                if role == 'state' and h in ('moves', 'moves_onto') and place_of(tw): say = moves_said(tw, ts_, tpick == 'self')
                if mpick == 'self' and h == 'dies': say = 'dies, comes back and dies again' if mref == m else 'dies by its own effect'
                if mpick == 'self' and h == 'given_keyword' and mk: say = f'has {mechanics.name(c, mk)}'  # Manta Rider has Flying
                if mpick == 'self' and h == 'trap_activated': say = 'is a trap that goes off'  # the Puffcap itself
                if tkind == 'player' and leader_game: say = one_leader(say)  # "whenever your General attacks"
                if h in ('damaged', 'nexus_damaged') and ts_ == 'mine' and not has_units and not tpick == 'self': say = 'makes you lose HP'  # no
                # units of mine in the game (Slay the Spire): the damage is to me
                if h == 'given_keyword' and mkind == 'player' and not leader_game and (mk or tk):  # the player gets it, not units
                    say = ('gives the enemy player ' if ms == 'enemy' else 'gives you ') + mechanics.name(c, mk or tk)
                if h == 'mana_refilled' and tkind in RESOURCE_WORD: say = RESOURCE_WORD[tkind]  # not mana: say which resource
                if cost and rule in cost_rules: continue  # another card paying its own cost pays nothing for this one
                if cost and h == 'sacrificed': continue  # Blood is paid by the sacrifices made to play the card (wiki Blood), not by
                # an effect that sacrifices (Master Bleene's True Scholar sacrifices itself to draw: it pays no Blood cost)
                # every unit can be sacrificed and every death gives a Bone: what the rules let every unit do pays for nothing
                # (Kaptain 30 Oct 2026: lines are combos between card abilities); a card that pays by its own text keeps its line
                if rule and (cost or tkind in RESOURCE_WORD): continue  # also Bones spent by an ability (Enlarge)
                if cost and h == 'terrain_changed':  # Ring of Dominion -> a card that needs lake lands: it pays the land cost, and
                    # the land it turns can be the enemy's, which it then takes (Kaptain 2 Nov 2026)
                    say = 'turns a land into the colour it needs: helps pay its land cost' + \
                          (', and can take that land from the enemy' if m in land_takers else '')
                elif cost: say += ' (pays its cost)'
                if rule and not cost and h in own_makes[m]: continue  # its own ability does it already (Sejuani hits the Nexus herself)
                if rule and not cost and (rule != 'units fight' or not fights_for(m, h, ts_)) and (h in OWN_LOSS or not any(
                        p.split(' ')[0] in ('card', 'name_has', 'type', 'keyword') for p in (tw or '').split(';'))):  # "kill a Stunned enemy"
                    # (Resonance Scythe) names the victim: fighting gives no Stunned enemy
                    continue  # every unit fights by the rules: that is no combo (Punish waits for damaged enemies; any attacker does it),
                    # not for a level-up either (Kaptain 31 Oct 2026: Poppy, Zed; "we know units can attack"), nor for "whenever your
                    # General attacks" (every General attacks: Lilithe -> Horn of the Forsaken). Only a card whose own ability makes it
                    # fight (Celerity, Ranged, "this fights") keeps the line
                if rule:  # every unit does it by the game's rules (attacks, hits the enemy Nexus): weaker than a card that says so
                    w *= 0.25; say += ' (by fighting)' if rule == 'units fight' else f" (by the game's rule: {rule})"
                if use and not rule and h not in ('moves', 'moves_onto') and not any(x in use for x in ('cheaper', 'cost')):
                    w = max(w, 0.25); say += f': {mechanics.name(c, t)} {use}'  # it acts on them itself: a direct combo (Soul Cleave kills
                # an ally, Undying Revenge brings back the strongest dead ally), not one card among every card that cares about deaths
                if lv: out[(m, t)].append(('levels', 2 * w, say + ' (levels it up)'))
                elif role == 'trigger' and t in selffeed: out[(m, t)].append(('levels', w, say + ' (it levels up from what it then does)'))
                # it reacts to a happening (a death effect, "when an ally dies"): "triggers"; it counts one or needs a thing to be
                # there ("5+ spells played", "while you control another flying creature", "if Krog has died"): "enables"
                elif cheap: out[(m, t)].append(('cheaper', w, say))  # "costs 1 less for each card discarded"
                else: out[(m, t)].append(('waits' if role == 'trigger' else 'type', w, say))  # a reaction is triggered; a count or a
                # state it needs is enabled (Kaptain, 30 Oct 2026: "triggers" and "enables")
    put = [(m, ref, act) for m, ref, act in c.execute(f"""select card, card_ref, act from flat_do where act in ({','.join('?' * len(PUTS))})
           and not (act in ('summon','create','copy') and 'enemy' in (coalesce(on_side,''), coalesce(to_side,'')))""", PUTS)  # a unit made on
           # the enemy's side (Cuckoo's Broken Egg) is not mine; a card planted in the enemy deck (Poison Puffcap) is my act
           if m in cards and ref in cards and m != ref]
    mk_kws = {v for (v,) in c.execute("select distinct via from flat_do where origin='uses_keyword' and act in ('create','summon','choose_card')")}
    for m, kw_, w_ in c.execute("select card, keyword_ref, on_with from flat_do where act='keyword_action' and origin='own' and on_with like '%card is %'"):
        if kw_ in mk_kws and m in cards:  # "Manifest an Otterpus or ...": it makes the card it names
            put += [(m, int(x), 'create') for x in re.findall(r'card is (\d+)', w_) if int(x) in cards and int(x) != m]
    gen_ = {(m, ref) for m, ref in c.execute("select src, dst from card_link where rel='generates'")}
    lv_ = collections.defaultdict(set)
    for m, b in c.execute("select src, dst from card_link where rel='transforms_into'"): lv_[m].add(b)
    named_ = {(m, ref) for m, ref in c.execute("select card, card_ref from flat_do where origin='own' and card_ref is not null")}
    put += [(m, ref, 'skill') for m, ref in c.execute("select l.src, l.dst from card_link l join card d on d.id=l.dst where l.rel='generates' "
                                                       "and d.category='ability'") if m in cards and ref in cards and ref not in unplayable(c)
            and not ((m, ref) not in named_ and any((b, ref) in gen_ for b in lv_[m]))]  # a unit's skill; one only its level-up casts
            # is not the base card's (Gangplank's rows summon Powder Keg; Powderful Explosion is Gangplank level 2's)
    put += [(m, ref, 'own_spell') for m, ref in c.execute("select l.src, l.dst from card_link l join card s on s.id=l.src where l.rel='generates' "
                                                           "and s.category='leader'") if m in cards and ref in cards]  # a General's spell
    # a card made by its name, not its id ("you draw a Pelt card": Skinning Knife; "create a Poro"; one of a set:
    # Kate Bishop's "add 2 Arrows"): the cards whose name fits
    for m, act, k, w in c.execute("""select card, act, on_kind, on_with from flat_do where act in ('create','summon') and card_ref is null
            and origin in ('own','gives') and (on_with like '%name_has is%' or on_with like '%card is%' or on_with like '%card in%')""").fetchall():
        # also inside an ability the card gives ("your cards have: Quickdraw: Thanos loads an Infinity Shot"), as by card_ref above
        if m in cards: put += [(m, t, act) for t, x in cards.items() if t != m and matches(c, game, x, k if k in KIND_CAT else 'any', w)]
    putters = collections.Counter(ref for _, ref in {(m, ref) for m, ref, _ in put})
    for m, ref, act in put:
        out[(m, ref)].append(('puts', 1.0 / putters[ref], {'summon': 'summons', 'create': 'creates', 'copy': 'copies', 'revive': 'brings back',
                                                           'play_card': 'plays', 'keyword_action': 'plants', 'skill': 'casts its skill',
                                                           'own_spell': 'casts its own spell'}[act]))
    # my units put into play by kind, from the discard, deck or hand ("revive the 6 strongest allies", "summon a unit from your
    # deck"): its own "when I'm summoned" goes off again (The Harrowing -> Captain Farron); a Play effect does not
    entry = collections.defaultdict(set)
    for i, e in c.execute("select card, event from flat_when where origin='own' and obj_pick='self' and event in ('summoned','played')"): entry[i].add(e)
    for m, act, k, w, zone in c.execute("""select card, act, on_kind, on_with, on_zone from flat_do where origin='own' and card_ref is null
            and coalesce(on_side,'mine') in ('mine','any') and coalesce(on_pick,'') not in ('self','it') and ((act='revive') or
            (act in ('summon','play_card') and on_zone in ('deck','deck_top','hand','discard','everywhere')) or
            (act='copy' and on_zone='board' and coalesce(eff_zone,'board')='board'))""").fetchall():  # Feel The Rush summons champions
            # from anywhere; Mirror Image copies a unit into play: its summon effect goes off (L17, L19)
        if m not in cards: continue
        want = {'played', 'summoned'} if act == 'play_card' else {'summoned'}
        if act == 'copy': act = 'summon'
        hits = [t for t, x in cards.items() if t != m and entry.get(t, set()) & want and matches(c, game, x, k if k in KIND_CAT else 'unit', w)]
        for t in hits: out[(m, t)].append(('waits', 0.5 / len(hits), {'revive': 'brings it back: its summon effect goes off',
                                           'summon': 'puts it into play: its summon effect goes off', 'play_card': 'plays it: its effect goes off'}[act]))
    # a draw that names what it takes from the deck ("draw the top legend", "draw a Beast") finds those cards
    # (and a summon from the hand or deck by what it is: "summon a minion with Dying Wish from your action bar", Unseven); "a copy
    # of it" is a card the earlier effect can pick (Lifestream heals a minion, then draws a copy of it: minions only)
    # "draw 4, discard those that do not cost 0" (Scrape): it draws and keeps the cards the discard does not hit
    for m, w in c.execute("""select d.card, x.on_with from flat_do d join flat_do x on x.card=d.card and x.ability=d.ability and x.seq>d.seq
            where d.origin='own' and d.act='draw' and coalesce(d.on_side,'mine')='mine' and x.act='discard' and x.on_pick='it'
            and coalesce(x.on_with,'')!=''""").fetchall():
        if m not in cards or all(q.split(' ')[0] in ('category', 'kind') for q in w.split(';') if q): continue  # it keeps cards by kind
        # only (Realm Warp discards the followers drawn): any card of that kind can be drawn (L1b)
        kept = [t for t, x in cards.items() if t != m and x['cat'] in KIND_CAT['spell'] | KIND_CAT['unit'] and x['cost'] is not None
                and not matches(c, game, x, 'any', w)]
        for t in kept: out[(m, t)].append(('puts', 1.0 / max(1, len(kept)), 'draws it and keeps it'))
    tutors = [(m, ab, sq, act, k, z, w) for m, ab, sq, act, k, z, w in c.execute("""select card, ability, seq, act, on_kind, on_zone, on_with from flat_do
              where origin='own' and coalesce(on_side,'mine')='mine' and coalesce(on_with,'')!='' and (act='draw' or (act in
              ('summon','play_card') and on_zone in ('hand','deck') and card_ref is null) or (act='choose_card' and on_zone='deck'))""") if m in cards]
    for m, ab, sq, act, k, z, w in tutors:
        if 'state is copy_of_it' in (w or ''):
            prev = c.execute("select on_kind, on_with from flat_do where card=? and ability=? and seq<? and origin='own' order by seq desc",
                             (m, ab, sq)).fetchone()
            if prev: k, w = prev[0], ';'.join(x for x in (prev[1] or '').split(';') if x.split(' ')[0] in ('card', 'type', 'category', 'keyword', 'name_has'))
        hit = [t for t, x in cards.items() if t != m and matches(c, game, x, k if k in KIND_CAT else 'any', w)]
        if len(hit) >= 0.5 * kind_count(c, game, k if k in KIND_CAT else 'any', None): continue  # "a cheaper card from your deck"
        kw_ = ';'.join(p for p in (w or '').split(';') if p.split(' ')[0] in ('category', 'kind'))  # the share among its own kind
        if kw_ and len(hit) >= 0.5 * sum(1 for t, x in cards.items() if t != m and matches(c, game, x, k if k in KIND_CAT else 'any', kw_)): continue
        # (Zap Sprayfin's "a spell that costs 3 or less": most spells; L21)
        if not [p for p in (w or '').split(';') if p and p.split(' ')[0] not in ('category', 'kind') + PLAY_STATE and not broad_part(c, game, p)]: continue  # "draw a
        # unit" (Channelsong): every unit can be drawn; only a narrower filter (a type, a keyword, a name) makes a line (L1)
        # (Treasurous Bosuns) finds almost any card: every card can be drawn (L1)
        say = 'draws it from the deck' if act == 'draw' else 'picks it from the deck' if act == 'choose_card' else \
            f"puts it into play from {'the hand' if z == 'hand' else 'the deck'}"
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
            has = {t for t in users if k in cards[t]['kws']}  # the cards with that keyword: "repeat all Summon effects" helps the
            # Summon units, not every spell played (Transcendimp -> Imp-pressive)
            for t in (has or users) - {m} - drawback_cards(c):  # a card that only gives itself away: repeating it is no help (L5)
                out[(m, t)].append(('repeats', 2.0 / len(ms), f'repeats its {mechanics.name(c, k)} effects'))
    # types: a card that asks for a type is fed by cards of that type and cards that make them
    asks, named, need_all = collections.defaultdict(set), collections.defaultdict(set), collections.defaultdict(set)  # named: a card it names ("if a Chime is attacked")
    asked = collections.defaultdict(set)  # named by a trigger or condition: it waits for or asks for that card
    making_kws = {v for (v,) in c.execute("""select distinct via from flat_do where origin='uses_keyword' and act in
                  ('create','summon','choose_card','copy','play_card')""")}  # keywords whose action makes the card it names (Invoke)
    cleanup = {a for (a,) in c.execute("""select ability from flat_do group by ability having sum(case when act in
               ('kill','obliterate','sacrifice') and on_pick='self' then 0 else 1 end)=0""")}  # "when Krog comes, destroy this"
    # a card that picks one of my deck's cards and acts on it (Bottled Flame: "choose an Attack"; it starts in hand): help, no ask
    picked = {a for (a,) in c.execute("""select distinct card from flat_do where act='choose_card' and on_zone in ('deck','hand')
              and coalesce(on_side,'mine')='mine'""")}
    # a keyword the card gives my cards as help (Fire Immunity): what the keyword does is that help too, no ask
    kw_help = {(a, k) for a, act, k, ps in c.execute("""select card, act, keyword_ref, params from flat_do where act='give_keyword'
               and origin='own' and coalesce(on_side,'mine')='mine'""") if helps_it(c, act, k, ps)}
    # a count of what my cards of a type do ("every 10th Attack you play"): those cards set it off, it does not ask for them
    counted = {(a, ab): ev for a, ab, ev in c.execute("""select card, ability, event from flat_if where test in ('event_count','amount_event_count')
               and ev_obj_with like '%type %' and event is not null""") if (ab, ev) not in capped(c)}  # played, summoned, drawn: played_lines
    cnt = collections.defaultdict(dict)
    for card, w, src, act, kw, ps, via in c.execute("""select card, coalesce(on_with,'') || ';' || coalesce(to_with,''), 'do', act, keyword_ref, params,
                                case when origin='uses_keyword' then via end from flat_do where coalesce(on_side,'mine')!='enemy'
                                and act not in ('create','summon','transform','copy','choose_card','play_card','revive','repeat','increase_effect')
                                -- what an effect repeats or makes bigger is what it helps (aimed_rows), not what it asks for (Strength: Attacks)
                                union all select card, obj_with, 'when', null, null, ability, null from flat_when
                                where event not in ('played','summoned','drawn')  -- played_lines reads these triggers (one rule per need)
                                union all select card, coalesce(of_with,'') || ';' ||
                                coalesce(ev_obj_with,''), 'if', of_zone, null, ability, null from flat_if where coalesce(of_side,'mine')!='enemy'"""):
        if src == 'when' and ps in help_abilities(c): continue
        if src == 'do' and act == 'keyword_action' and kw in making_kws: continue  # "Invoke a Celestial": what it makes, no ask
        if src == 'do' and card in picked: continue  # Bottled Flame gives the Attack it picked
        # Innate: help for that card (the tutor line), no ask
        if src == 'do' and (helps_it(c, act, kw, ps) or act in HELP_ACTS): continue  # Oakenheart "your Mechs have +1/+1" helps the
        # Mechs (an aimed line from it); it does not ask for them
        if src == 'do' and (act == 'remove_keyword' and kw and not buff_keyword(c, kw) or (card, via) in kw_help): continue  # a passive
        # that clears Fire or Smoke from my Mechs, or gives them Fire Immunity, helps them; they do not enable it (Kaptain 30 Oct 2026)
        if card not in cards: continue
        both = {int(p.split(' ')[2]) for p in (w or '').replace('of:', '').split(';') if p.split(' ')[:2] == ['type', 'is'] and p.split(' ')[2:3] and p.split(' ')[2].isdigit()}
        for part in (w or '').split(';'):
            b = part.removeprefix('of:').split(' ')
            if len(b) == 3 and b[0] == 'type' and b[1] in ('is', 'in') and b[2].isdigit():
                if src == 'if' and counted.get((card, ps)) in ('played', 'summoned', 'drawn'): continue  # played_lines says it, with the type
                asks[int(b[2])].add(card)
                if b[1] == 'is' and len(both) > 1: need_all[(card, int(b[2]))] |= both  # "a Mecha Yordle": both types
                if src == 'if' and (card, ps) in counted: cnt[int(b[2])][card] = counted[(card, ps)]
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
                          "and on_with like '%type is%' and coalesce(on_side,'mine') in ('mine','any') "
                          "and not (act='choose_card' and coalesce(on_zone,'') in ('deck','hand','discard'))", PUTS):  # picking a card
        # already in my deck makes none (Bottled Flame: "choose an Attack" for the run)
        if m in cards:
            for p in w.split(';'):
                b = p.split(' ')
                if len(b) == 3 and b[:2] == ['type', 'is'] and b[2].isdigit(): has[int(b[2])].add((m, 'makes'))
    for t, ts in asks.items():
        tn = c.execute('select name from type where id=?', (t,)).fetchone()
        if tn and EVERY_DECK_TYPE.get(game) == tn[0]: continue  # every squad is Mechs: Psionic Receiver asks for none (L1)
        bt = broad_part(c, game, f'type is {t}')  # a fifth or more of the cards are Skills: "put a Skill into your hand" (Secret
        # Technique) can pick any of them (L14); a count of them ("every 3 Attacks", Kunai, Rage) is a deck choice (Kaptain 30 Oct 2026)
        for m in sorted({m for m, _ in has.get(t, ())}):
            for x in ts - {m}:
                if bt and x not in cnt[t]: continue
                is_ = (m, 'is') in has[t] and need_all.get((x, t), set()) <= set(cards[m]['types'])  # a Yordle that is no Mecha is none
                if not is_ and (m, 'makes') not in has[t]: continue
                how = 'is' if is_ else 'makes'  # it is one itself and makes one too: said once, as "is" (Rek'Sai is a Lurker)
                what = f'{"is" if how == "is" else "makes"} {"an" if tn and tn[0][:1] in "AEIOU" else "a"} {tn[0] if tn else "card of the type"}'
                if x in cnt[t]: out[(m, x)].append(('waits', 1.0 / len(ts), f'{what} it counts when {cnt[t][x]}'))
                else: out[(m, x)].append(('type', 1.0 / len(ts), what + ' it asks for'))
    for t, ts in named.items():  # the named card itself, or a card that makes it
        name = cards[t]['name'] if t in cards else None
        if not name: continue
        own = {m for m, ref, _ in put if ref == t}  # a card naming what it makes itself acts on its own product (Blazing Spines'
        for m, how in [(t, 'is')] + [(m, 'makes') for m in own]:  # walls "can attack")
            for x in ts - {m} - (own - asked[t]):
                if x in asked[t] or not any(l[0] == 'puts' for l in out.get((x, m), ())):  # what it makes itself is no help to it,
                    # unless it asks for another one ("if you have another Wraithling")
                    out[(m, x)].append(('type', 1.0 / len(ts), f'{how} the {name} it names'))
    for k_, ls in out.items():  # one reason said once; a cost cut said as "makes cheaper", not also as "enables"
        cheap = {y for kd, _, y in ls if kd == 'cheaper'}
        keep = []
        for l in ls:
            if l not in keep and not (l[0] != 'cheaper' and l[2] in cheap): keep.append(l)
        out[k_] = keep
    pushers = {a for (a,) in c.execute("""select distinct card from flat_ref where role='makes' and happening='moves' and origin in ('own','uses_keyword')
               and coalesce(side,'') in ('enemy','','any') and coalesce(pick,'') not in ('self')""") if a in cards}
    for t in {a_ for ab_, a_ in bump_abs.items() if ab_ not in protect_abilities(c)} & set(cards):  # Stabilizers keeps damage off
        for m in pushers - {t}: out[(m, t)].append(('waits', 1.0 / len(pushers), '{A} pushes enemy units into things (bump damage)'))
    # a card that puts a status on itself which damage takes off (Cryo-Launcher freezes the Ice Mech; Frozen ends when damaged):
    # a card that can hit my units frees it; a card that shields my units stops it (Energy Shield keeps new bad statuses off)
    freed = {k for (k,) in c.execute("""select distinct w.card from flat_when w join flat_do d on d.card=w.card and d.ability=w.ability
             where w.event='damaged' and w.obj_pick='self' and d.act='remove_keyword' and d.keyword_ref=w.card and d.on_pick='self'""")}
    blockers = {k for (k,) in c.execute("select card from flat_do where act='cant' and param_event='given_keyword' and to_with like '%state is negative%'")}
    selfstat = {(a, k) for a, k in c.execute("select card, keyword_ref from flat_do where act='give_keyword' and on_pick='self' and origin='own'")
                if a in cards and k in freed and kw_tree(c, k) in ('disable', 'immobilize', 'attack_lock', 'damage_over_time', 'debuff')}
    if selfstat:
        hitters_ = {a for (a,) in c.execute("""select distinct card from flat_do where act='damage' and origin='own' and on_side is null
                    and on_pick in ('chosen','nearest','all')""") if a in cards}
        shielders = {a for a, k in c.execute("""select card, keyword_ref from flat_do where act='give_keyword' and origin='own'
                     and coalesce(on_side,'mine')='mine' and coalesce(on_pick,'') not in ('self','it') and coalesce(on_kind,'') not in ('landmark','building')""")
                     if a in cards and k in blockers}  # a shield on buildings (Grid Repulse, Critical Shields) reaches no mech
        for t, k in selfstat:
            kn = mechanics.name(c, k)
            for m in hitters_ - {t}: out[(m, t)].append(('heals', 0.5 / len(hitters_), f'{{A}} can hit {{Bc}} while it is {kn}: the hit frees it'))
            for m in shielders - {t}: out[(m, t)].append(('keyword', 0.5 / max(1, len(shielders)), f'{{A}} can shield {{Bc}}: the Shield keeps {kn} off it'))
    # ground that kills what is pushed onto it (the game's rules, DEADLY_GROUND): a card that makes it enables every pusher
    for m, w_ in c.execute("select card, to_with from flat_do where act='set_terrain' and origin='own'").fetchall():
        say = next((v for k, v in DEADLY_GROUND.get(game, {}).items() if f'terrain is {k}' in (w_ or '')), None)
        if not say or m not in cards: continue
        for t in pushers - {m}: out[(m, t)].append(('type', 1.0 / len(pushers), say))
    CACHE[('lines', game)] = out
    return out


BAD_STATUS = ('disable', 'immobilize', 'attack_lock', 'damage_over_time', 'debuff', 'forced_movement')  # statuses that hurt


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
    if act in ('stat_change', 'grow'): return any(k in p and raises(p[k]) for k in ('power', 'health', 'strength'))
    if act == 'give_keyword': return bool(kw) and (buff_keyword(c, kw) or kw_tree(c, kw) == 'movement')
    if act == 'cost_change': return p.get('cost', '').startswith('-')
    return act in ('cost_set', 'heal', 'negate_damage', 'give_ability', 'damage_reduction', 'countdown_advance', 'ready')


def kw_tree(c, kw):
    """a keyword's concept; the game's own entry first ("into_the_breach:Boost" is a buff, another game's Boost is not)"""
    r = c.execute("""select v.tree from card k join vocab v on v.field='keyword' and v.value in (k.name, k.game || ':' || k.name)
                    where k.id=? order by v.value = k.game || ':' || k.name desc""", (kw,)).fetchone()
    return r[0] if r else None


def buff_keyword(c, kw):
    return kw_tree(c, kw) in BUFFS


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
    """a stat change in one of three families (Kaptain 2 Nov 2026: "+1|+1" and "+2|+2" are one reason): 'gives it more power',
    'gives it more health', 'gives it more power and health' (Stormbound's one stat: 'more strength'), or 'lowers its stats'"""
    d = dict(p.split('=', 1) for p in (ps or '').split(';') if '=' in p)
    up = lambda k: k in d and not d[k].startswith('-') and d[k].replace('.', '').strip('0') != ''
    if up('strength'): return 'gives it more strength'
    if up('power') and up('health'): return 'gives it more power and health'
    if up('power'): return 'gives it more power'
    if up('health'): return 'gives it more health'
    return 'lowers its stats' if any(v.startswith('-') for k, v in d.items() if k in ('power', 'health', 'strength')) else 'gives it more stats'




def aimed_rows(c, game):
    """effects on my side aimed at cards (not the card itself): (card, act, kind, pick, with, kw, rule) and how many cards of the
    game make the same one (act, kind, keyword, rule or not). Effects that repeat, boost or copy a group of cards count on
    either side when the group is named (traps on enemy cards are still mine)."""
    if ('aimed', game) in CACHE: return CACHE[('aimed', game)]
    cards = cards_of(c, game); rows = []
    kw_rows = {(a, act, kind, w): via for a, act, kind, w, via in c.execute(
        "select card, act, on_kind, on_with, via from flat_do where origin='has_keyword'")}
    # a status the card gives my side (Strength, Focus): what the status makes bigger, the card makes bigger (Flex -> Attacks)
    mine_status = {(a, k) for a, k, ps in c.execute("""select card, keyword_ref, params from flat_do where act='give_keyword' and origin='own'
                   and coalesce(on_side,'mine')='mine' and keyword_ref is not null""") if '=-' not in (ps or '')}
    for a, act, kind, side, pick, w, lasts, kw, cref, zone, ps, origin, via, ez in c.execute("""select card, act, on_kind, on_side, on_pick, on_with, lasts,
            keyword_ref, card_ref, on_zone, params, origin, via, eff_zone from flat_do where origin in ('own','has_keyword','uses_keyword') and coalesce(on_pick,'') not in ('self','it','owner','actor')
            and not (act = 'can' and on_kind = 'player' and param_event in ('shuffled','drawn','discarded','played','summoned'))
            and not (act = 'give_ability' and on_kind = 'player')  -- a delayed effect the player gets ("if it dies this turn") is no help to the leader card"""):
        # "you may replace an additional card": the player handles more cards, its leader card gets nothing
        if a not in cards: continue
        if act == 'keyword_action' and kw and kw_tree(c, kw) == 'return_to_hand': act = 'return_to_hand'  # Recall (Will of Ionia) is a return
        kv = via if origin == 'has_keyword' else kw_rows.get((a, act, kind, w)) if origin == 'own' else None  # the card's own
        # keyword does it (Lurk), also where the card's text repeats its keyword's effect (Rek'Sai's "grant Lurker allies +1|+0", L15)
        if act == 'copy': ps = ';'.join(x for x in (ps, f'copy_to={ez or "board"}') if x)  # where the copy goes: a hand or deck copy is
        # one more card of any kind (generic, L14); a copy put on the board sets off its summon and death effects
        if origin == 'uses_keyword' and not (act in BOOST and (a, via) in mine_status): continue
        if act == 'give_keyword' and kind == 'position': kind = 'unit_or_structure'  # a shielded tile shields the unit on it
        if zone in ('hand', 'deck', 'deck_top', 'deck_bottom') or act in ('cost_change', 'cost_set'): CACHE.setdefault(('handrows', game), set()).add((a, act))
        if act == 'return_card' and zone == 'exhausted': CACHE.setdefault(('from_exhaust', game), set()).add(a)  # "a consumed spell"
        if act == 'increase_effect' and kw and 'keyword is' not in (w or ''):  # "Impact deals 2 more": the cards with Impact
            w = ';'.join(x for x in (w, f'keyword is {kw}') if x); kind = kind if kind in KIND_CAT else 'any'
        named = any(p.startswith(NAMES_ONE) or (kind == 'keyword' and p.startswith('keyword in ')) for p in (w or '').split(';'))  # Focus: the Orbs
        if act == 'can' and kind == 'keyword' and named and side in ('mine', None):  # "Lightning now hits ALL enemies": the cards
            rows.append((a, act, kind, w, kw, 'boost', named, ps, kv)); continue  # that put Lightning in play get more from it
        if act in BOOST and '=-' in (ps or ''): continue  # a smaller effect ("Vulnerable takes 25% more rather than 50%", Odd Mushroom)
        if act in BOOST and cref is None and (side in ('mine', 'any', None) or named):
            if kind in KIND_CAT or named or kind in ('card', 'effect', 'any', 'anything'): rows.append((a, act, kind, w, kw, 'boost', named, ps, kv))
            continue
        if act in NOT_AIMED or (side not in ('mine', 'any') and not (side is None and (helps_it(c, act, kw, ps) or act == 'return_to_hand'))): continue  # no side
        # a return to hand of either side: on my unit with a Play or summon effect it is a replay (L14: Defiant Dance -> Dunekeeper)
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
                  and any(x['cat'] == 'leader' for x in cards.values()))) and not (
                kind == 'card' and act == 'stat_change' and 'power=' in (ps or '') and zone in ('hand', 'deck') and power_doublers(c) & set(cards)):
            continue  # "restore 2 Health to anything": a unit or my General; power to cards in hand or deck feeds a card that doubles its power (Okoye -> Black Panther)
        rows.append((a, act, kind, w, kw, rule, narrowed or named or kind == 'player', ps, kv))  # "your General": one card, the leader
    makers = collections.defaultdict(set)
    for a, act, kind, w, kw, rule, *_ in rows: makers[(act, kind, kw, rule if rule in (True, False, 'boost') else True)].add(a)
    CACHE[('aimed', game)] = rows, makers
    return rows, makers


def givers_of(c, game, k, nodes):
    """the nodes that give keyword or status k to my side or use it there (Fledgling Imp applies Rage to friendly units)"""
    marks = ','.join('?' * len(nodes))
    return {a for (a,) in c.execute(f"""select distinct card from flat_do where (keyword_ref=? or (act='keyword_action' and (';' || coalesce(on_with,'') || ';')
            like ? or (';' || coalesce(on_with,'') || ';') like ?)) and act in ('give_keyword','keyword_action')
            and origin='own' and coalesce(on_side,'mine') in ('mine','any') and card in ({marks})""",  # "Channel 1 Lightning": puts Lightning
            [k, f'%;keyword is {k};%', f'%;keyword in {k};%'] + list(nodes))}


def repeaters_of(c, k, nodes):
    """the nodes that set off keyword k's effect again (Loop: "trigger the passive ability of your next Orb")"""
    marks = ','.join('?' * len(nodes))
    return {a for (a,) in c.execute(f"""select distinct card from flat_do where act='repeat' and origin='own' and ((';' || coalesce(on_with,'') || ';')
            like ? or (';' || coalesce(on_with,'') || ';') like ?) and card in ({marks})""", [f'%;keyword is {k};%', f'%;keyword in {k};%'] + list(nodes))}


PLACE_WORDS = {'sides':'next to it', 'bordering': 'next to it', 'surrounding': 'around it', 'same_lane': 'in its lane',
               'in_circuit': 'in its circuit', 'same_space': 'on its space', 'same_row': 'in its row', 'same_column': 'in its column',
               'in_front': 'in front of it', 'behind': 'behind it', 'ahead': 'ahead of it', 'straight_line': 'in a line from it'}


# a place a card picks things by, measured from x ("in a line from it"; "x's" is its possessive)
MOVE_PLACE = {'straight_line': 'in a line from {x}', 'bordering': 'next to {x}', 'sides': 'next to {x}', 'surrounding': 'around {x}',
              'same_lane': "in {xs} lane", 'same_space': "on {xs} space", 'same_row': "in {xs} row", 'same_column': "in {xs} column",
              'in_circuit': "in {xs} circuit", 'in_front': 'in front of {x}', 'behind': 'behind {x}', 'ahead': 'ahead of {x}',
              'behind_all': 'anywhere behind {x}', 'first_in_front': 'first in front of {x}', 'diagonal': 'diagonal to {x}',
              'front_of_lane': 'at the front of a lane', 'most_forward': 'furthest forward', 'area_2x2': 'in a 2x2 area',
              'area_3x3': 'in a 3x3 area around {x}', 'starting_side': "on {xs} starting side"}


def place_of(w):
    """where a filter picks things, in plain words ("in a line from it", "next to its target"); None when no place"""
    for p in (w or '').split(';'):
        b = p.removeprefix('of:').split(' ')
        if b[:2] != ['position', 'is'] or len(b) < 3: continue
        of = b[4:] if b[3:4] == ['of'] else []
        x = ('it' if not of or of[0] == 'self' else 'its target' if of[0] == 'it' else
             'your leader or base' if of[:2] == ['player', 'mine'] else 'the enemy leader or base' if of[:2] == ['player', 'enemy'] else
             'a space it picks' if of[0] == 'position' else 'a card it picks')
        if b[2] == 'same_space' and x in ('a space it picks', 'its target'): return 'on the space it picks'
        xs = {'it': 'its', 'its target': "its target's"}.get(x, x + "'s")
        return MOVE_PLACE.get(b[2], b[2].replace('_', ' ') + ' {x}').format(x=x, xs=xs)
    return None


def moves_said(w, side, self_):
    """a card that picks what it acts on by place, fed by moves: say both halves with both names (Kaptain 30 Oct 2026: one
    card moves, the other cares where things stand): "Combat Mech moves units, and Artillery Mech acts on units in a line
    from it" ({A}, {B}: the two cards' names, filled in by network())"""
    who = 'it' if self_ else {'mine': 'your units', 'enemy': 'enemy units'}.get(side, 'units')
    return f'{{A}} moves {who}, and {{B}} acts on units {place_of(w)}'


def where(w):
    """the place a target filter asks for, measured from the card itself, in plain words (' when next to it')"""
    for p in (w or '').split(';'):
        b = p.split(' ')
        if b[:2] == ['position', 'is'] and (len(b) == 3 or b[3:] == ['of', 'self']) and b[2] in PLACE_WORDS: return f' (when {PLACE_WORDS[b[2]]})'  # "of self" = measured from it
    return ''


# my damage or kill on my own card is a line only when that card gains from it (Kaptain 31 Oct 2026: Hammer -> Bomb Latcher, not Wild Bull)
HARM_GAIN = {'damage': {'dies', 'killed', 'damaged', 'survives_damage'}, 'kill': {'dies', 'killed'}}


def circuit_ends(c, game):
    """the cards that close a circuit (Inscryption's "Conduit card" type): an effect within the circuit does not reach them"""
    key = ('circuit_ends', game)
    if key not in CACHE:
        CACHE[key] = {i for (i,) in c.execute("select ct.card from card_type ct join type t on t.id=ct.type where t.game=? and t.name='Conduit card'", (game,))}
    return CACHE[key]


# Kaptain 1 Nov 2026: help aimed at any card of a kind ("give an ally +2|+0") links only to a card whose own text or keywords use
# it toward its goal (Wuju Style -> Patched Porobot: no line; +power to an Elusive or Overwhelm unit: a line)
POWER_USE = ('lifesteal',)  # keywords whose own text reads the damage dealt (Lifesteal heals by it). More power for anything
# else is generic (Kaptain 2 Nov 2026): Overwhelm, Elusive, Double Attack, "Strike:" or a kill hit harder only by the game's goal,
# not by their text; a text that needs one big strike (Vi: 10+ damage) or gets something from the damage (Reaper) keeps it
GUARD_USE = ('taunt',)  # keywords that make a unit take or seek fights: more health or protection keeps it there
DEFENCE_KW = ('shield', 'damage_reduction', 'immunity', 'regeneration', 'block_armor', 'cheat_death', 'defence_gain', 'protection', 'heal')
FIGHT_EVENTS = ('strikes', 'attacks', 'attack_done', 'fights', 'challenges', 'activated', 'strikes_nexus')
# what each help makes happen, for a card that waits for it or levels from it ("when I'm healed", "Level up: allies given Barrier")
HELP_MAKES = {'stat_change': ('stat_changed',), 'grow': ('stat_changed',), 'give_keyword': ('given_keyword', 'keyword_used'),
              'heal': ('healed',), 'return_to_hand': ('recalled',), 'strike': ('strikes',), 'start_attack': ('attacks', 'strikes'),
              'transform': ('transformed',), 'cost_change': ('cost_changed',), 'cost_set': ('cost_changed',), 'ready': ('attacks',),
              'countdown_advance': ('counts_down', 'countdown_done'), 'move': ('moves',), 'swap': ('moves',),
              'attach': ('equipped',)}


TRIGGER_KW = ('on_attack', 'on_kill', 'on_damaged', 'death_trigger', 'on_play', 'on_fight', 'on_targeted', 'on_discard', 'on_sacrifice',
              'on_spell', 'on_lifegain', 'on_block', 'on_draw', 'on_harvest', 'on_ally_play', 'other_death_trigger', 'territory_trigger',
              'repeat_trigger', 'combat_start', 'turn_start', 'turn_end')  # keyword concepts that are reactions


def drawback_cards(c):
    """cards whose own effects only give the card itself away (Acid Arrow): repeating or replaying them helps nothing (L5)"""
    return {i for (i,) in c.execute("select card from flat_do where origin='own' group by card having sum(act!='donate')=0")}


def generic_use(c, game):
    """per card: its keyword concepts, its own triggers, what it waits for, the keywords it gives itself or my side, and whether it
    strikes by its own effect or has an effect at all"""
    if ('use', game) in CACHE: return CACHE[('use', game)]
    cards = cards_of(c, game); d = collections.defaultdict(lambda: collections.defaultdict(set))
    for i, x in cards.items(): d[i]['trees'] = {kw_tree(c, k) for k in x['kws']}
    for i, k in c.execute("select card, keyword_ref from flat_do where origin='own' and act='give_keyword' and on_pick='self' and keyword_ref is not null"):
        if i in d: d[i]['trees'].add(kw_tree(c, k))  # a keyword it gives itself is its own (Hornbreaker Prince's Multistrike upgrade)
    for i, e, origin, via in c.execute("""select card, event, origin, via from flat_when where origin in ('own','has_keyword')
            and (obj_pick in ('self','actor_self') or (origin='has_keyword' and obj_pick is null))"""):
        if origin == 'own' or kw_tree(c, via) in TRIGGER_KW: d[i]['self_when'].add(e)  # "Strike:", "Slay:" as keywords (Monster Train)
    for i in drawback_cards(c): d[i]['self_when'] -= {'played', 'summoned'}  # its Play effect is a drawback: replaying it is no help (L5)
    kw_stat = {t for (t,) in c.execute("select w.card from cond k join flat_when w on w.ability=k.ability where k.test='keyword_condition' and k.ref_keyword is not null and w.event='stat_changed'")}
    for i, h, origin, via, k, rl, ow in c.execute("""select card, happening, origin, via, keyword, role, obj_with from flat_ref where role!='makes' and origin in ('own','has_keyword')
            and coalesce(side,'') in ('','mine','any')"""):
        if game == 'marvel_snap' and rl == 'state' and h == 'moves' and 'position is same_lane' in (ow or ''): continue  # a lane is a location: a card that acts in its lane needs no move (Doctor Strange -> Danger)
        if origin != 'own' and kw_tree(c, via) not in TRIGGER_KW: continue  # a keyword's inner working (Barrier pops when damaged,
        # Challenger picks when attacking) is no need of the card; a keyword that is a reaction is (Revenge: when damaged)
        if h in ('given_keyword', 'keyword_used', 'keyword_removed'): d[i]['kw_needs'].add((h, k))  # which keyword it waits for
        elif not (h == 'stat_changed' and i in kw_stat): d[i]['needs'].add(h)  # Power gained from Hallowed (Gwen) comes only from Hallowed ()
    for i, k in c.execute("""select card, keyword_ref from flat_do where origin='own' and act='give_keyword' and keyword_ref is not null
            and (coalesce(on_side,'mine') in ('mine','any') or on_pick in ('self','it'))"""): d[i]['gives_kw'].add(k)
    for i, w in c.execute("select card, of_with from flat_if where origin='own' and of_with like '%keyword is %'"):
        d[i]['counts_kw'] |= {int(x) for x in re.findall(r'keyword is (\d+)', w or '')}
    for i, ab in c.execute("select card, ability from flat_do where origin='own' and act in ('start_attack','strike') and on_pick='self'"):
        d[i]['flags'].add('play_fights' if on_play(c, ab) else 'fights')  # a fight when it is played is over before a boost on the board
        # reaches it (Spirit Spice -> Barrensky Vermin); only help that reaches it in hand counts then
    # its own text makes it fight or strike (Deepwood Stalker): the damage is its power
    for (i,) in c.execute("select distinct card from flat_do where origin='own'"): d[i]['flags'].add('acts')
    for (i,) in c.execute("select card from flat_ref where origin='own' and role='trigger' and pick='actor_self' and happening in ('killed','damaged')"):
        d[i]['flags'].add('own_hits')  # "when I kill an enemy" (Pyke level 2): a strike it is made to do sets it off
    for (i,) in c.execute("""select card from flat_if where origin in ('own','has_keyword') and of_kind='player' and coalesce(of_side,'mine')='mine'
            and of_with like '%position %'"""):
        d[i]['flags'].add('near_leader')  # it acts when my leader stands near it (Zeal)
    for (i,) in c.execute("""select card from flat_ref where role!='makes' and origin in ('own','has_keyword') and happening='strikes'
            and coalesce(obj_with,'') || coalesce(actor_with,'') like '%damage ge%'"""):
        d[i]['flags'].add('big_strike')  # it needs one strike of a size (Vi: 10+ damage)
    lvl = level_abilities(c)  # a champion that levels up from Nexus damage and has Overwhelm or Elusive (Darius): more power
    # levels it sooner, its own level text counts that damage (Kaptain's checks n33, n34)
    for i, ab in c.execute("select card, ability from flat_ref where role!='makes' and happening='nexus_damaged' and origin in ('own','has_keyword')"):
        if i in d and ab in lvl and d[i]['trees'] & {'evasion', 'excess_damage'}: d[i]['flags'].add('level_hit')
    for i, w in c.execute("select card, ev_actor_with from flat_if where test='event_count' and attr='damage' and ev_actor_with like 'card is %'"):
        if i in d and f'card is {i}' in w: d[i]['flags'].add('level_hit')  # it counts the damage it deals itself
        # ("Allied Master Yis have done 12+ damage", Kaptain 3 Nov 2026): more power makes that sooner
    for i, ab in c.execute("select card, ability from flat_if where test='event_count' and attr='damage' and ev_actor_pick in ('self','actor_self')"):
        if i in d and ab in lvl: d[i]['flags'].add('level_hit')  # it levels from the damage it deals (Gwen: "I've dealt 10+ damage"; L24)
    CACHE[('use', game)] = d
    return d


def broad_part(c, game, p):
    """a filter part that names no deck choice: a faction, a card kind, a stat, a "not", or a type that a fifth or more of the game's
    cards have (Slay the Spire's Skill, Attack, Power): any card of it can be the target (L1b, L14)"""
    f = p.split(' ')
    if f[0] in ('region', 'category', 'kind', 'power', 'health', 'strength') or f[1:2] == ['not']: return True
    if f[:2] == ['type', 'is'] and f[2:3] and f[2].isdigit():
        key = ('type_share', game, f[2])
        if key not in CACHE:
            cats = collections.Counter(k['cat'] for i, k in cards_of(c, game).items() if i in {x for (x,) in c.execute(
                   "select card from card_type where type=?", (int(f[2]),))})
            cat = cats.most_common(1)[0][0] if cats else None  # its share among cards of its own kind (Attacks among cards, not relics)
            CACHE[key] = sum(cats.values()) / max(1, sum(1 for k in cards_of(c, game).values() if k['cat'] == cat))
        return CACHE[key] >= 0.2
    return False


def raises(v):
    """a stat change that raises the stat: "+2", "X", "stat" (Revna's own stats); "+0" and "-1" raise nothing"""
    v = str(v or '')
    return bool(v) and not v.startswith('-') and v.replace('.', '', 1).strip('0') != ''


def use_of(c, game, b, act, kw, ps, w=None):
    """what card b's own text or keywords do with help of this kind, in a player's words, or None when nothing uses it (rule L14)"""
    u = generic_use(c, game)[b]; cards = cards_of(c, game); p = dict(x.split('=', 1) for x in (ps or '').split(';') if '=' in x)
    pev = p.get('event'); tree = kw_tree(c, kw) if kw else None; kwn = mechanics.name(c, kw) if kw else 'a keyword'
    if act == 'return_to_hand' and u['self_when'] & {'played', 'summoned'}: return 'returns it to hand: its Play or summon effect goes off again'
    # (like a revive: The Harrowing -> Captain Farron, Kaptain 2 Nov 2026); a copy of any ally is generic: any card can be its target
    # (Kaptain 2 Nov 2026); only a filter that names a kind keeps a copy line (aimed rows that are sharp)
    if act == 'sacrifice' and u['self_when'] & {'dies', 'sacrificed'}: return 'sacrifices it: its death effect goes off'
    if act in ('strike', 'start_attack', 'ready') or (act == 'can' and pev in ('attacks', 'strikes')) or (act == 'give_keyword' and tree == 'multi_attack'):
        if u['self_when'] & set(FIGHT_EVENTS): return 'makes it attack or strike again: its own effect goes off'  # "Strike:", "Attack:"
        if act in ('strike', 'start_attack') and 'own_hits' in u['flags']: return 'makes it strike: its effect goes off when it hits or kills'
    made = set(HELP_MAKES.get(act, ())) & u['needs'] | {h for h, k in u['kw_needs'] if h in HELP_MAKES.get(act, ()) and kw and k in (None, kw)}
    if made: return f'does what it waits for or counts ({", ".join(sorted(made)).replace("_", " ")})'
    if 'position ' in (w or '') and ('of player' in w or 'of:kind is player' in w) and 'near_leader' in u['flags']:
        return 'helps it near your leader, where its own effect works'  # Roar -> Windblade Adept's Zeal
    if act == 'give_keyword' and kw and (kw in u['counts_kw'] or 'given_keyword' in u['self_when']): return f'gives it {kwn}, which it counts'
    if act == 'give_keyword' and kw and b in sharers(c): return f'gives it {kwn}, which it passes to its allies'  # Sivir level 2 (L14)
    if act == 'give_keyword' and tree in ('evasion', 'excess_damage') and ('big_strike' in u['flags'] or u['needs'] & {'strikes_nexus', 'nexus_damaged'}):
        return f'gives it {kwn}: its strike gets through in full'  # Sumpworks Map -> Vi: "struck for 10+ damage in one strike"
    up = lambda *ks: act in ('stat_change', 'grow') and any(k in p and raises(p[k]) for k in ks)
    if up('power') and b in power_doublers(c): return 'more power: it doubles its power'  # Okoye -> Black Panther
    if up('power') and b in own_power_readers(c): return 'more power: its text reads its power'  # Poppy: "allies with less power than me" (L18)
    if up('power', 'strength') or (act == 'give_keyword' and tree in ('attack_gain', 'temporary_buff')):
        if u['trees'] & set(POWER_USE) or u['flags'] & {'big_strike', 'fights', 'level_hit'} or ('play_fights' in u['flags'] and 'hand' in (w or '')) or (b in gains_back(c, game) and not fixed_hit(c, b)):
            return 'more power: its text uses the damage it deals'  # a fixed amount is not its power (Path to Paradise -> Enslaved Priest)
    # a heal is no more health (L18): it does not keep a fighting unit alive (Lux Ignis -> Fireblazer)
    if up('health', 'strength') or act in ('negate_damage', 'damage_reduction') or (act == 'give_keyword' and tree in DEFENCE_KW) \
            or (act == 'cant' and pev in ('dies', 'targeted')):  # "can't drop below 1 health" (Survival Skills)
        if u['trees'] & set(GUARD_USE): return 'keeps it alive in the fights it takes on'
    if act == 'repeat' and b in doublers(c, game): return 'plays it again: its doubling doubles again'  # Burst -> Catalyst
    if act == 'increase_effect' and b in gains_back(c, game): return 'its damage is bigger, and so is what it gets back from it'  # Strength -> Reaper
    # a repeat or a bigger effect for any card ("trigger the ability of a friendly unit", "double the buffs") is generic: any card
    # with an effect can be its target (Kaptain 2 Nov 2026); a named keyword or kind keeps it (Strength -> Attacks, Focus -> Orbs)
    if (act in ('remove_keyword', 'remove_keywords') or (act == 'cant' and pev == 'given_keyword')) and kw and kw in u['gives_kw']:
        return f'keeps the {kwn} it gives itself off it'  # it puts that status on my side
    if act == 'countdown_advance' and 'countdown' in u['trees']: return 'speeds up its countdown'
    if act == 'refresh' and cards[b]['cat'] not in KIND_CAT['unit'] and 'acts' in u['flags']: return 'lets you use it again'  # a General's
    # spell refreshed (Cryptographer -> Malice): its effect again
    return None


def trig_state_of(c, game, m):
    """the keyword states its triggers ask of the unit it then acts on ("when an Ephemeral ally is summoned, give it", Soul Shepherd)"""
    return ';'.join(dict.fromkeys(x for (w,) in c.execute("select obj_with from flat_when where card=? and obj_with like 'state is %'", (m,))
                                  for x in [state_filter(c, game, w)] if x))


def state_filter(c, game, w):
    """a filter "state is ephemeral" as the game's keyword of that name ("keyword is <id>"), when the state is a keyword"""
    return ';'.join(f'keyword is {k}' for k in (state_kw(c, game, p[9:]) for p in (w or '').split(';') if p.startswith('state is ')) if k)


def to_hand(c):
    """cards that give stats to my cards in hand"""
    if 'to_hand' not in CACHE:
        CACHE['to_hand'] = {a for (a,) in c.execute("select card from flat_do where origin='own' and act in ('stat_change','grow') and on_zone='hand'")}
    return CACHE['to_hand']


def on_play(c, ab):
    """the ability goes off only when its own card is played or summoned"""
    ws = c.execute("select event, obj_pick from flat_when where ability=?", (ab,)).fetchall()
    return bool(ws) and all(e in ('played', 'summoned') and p == 'self' for e, p in ws)


def fixed_hit(c, b):
    """its own damage is a fixed number ("deal 2 damage, heal that much", Enslaved Priest): more power does not change it"""
    return all(re.match(r'amount=[\d.]+(;|$)', ps or '') for (ps,) in c.execute("select params from flat_do where card=? and origin='own' and act='damage'", (b,))) \
        and bool(c.execute("select 1 from flat_do where card=? and origin='own' and act='damage'", (b,)).fetchone())


def gains_back(c, game):
    """cards that get something back from the damage they deal ("heal HP equal to unblocked damage", Reaper)"""
    if ('back', game) not in CACHE:
        cs = cards_of(c, game)
        CACHE[('back', game)] = {b for (b,) in c.execute("""select d.card from flat_do d join flat_do g on g.card=d.card and g.ability=d.ability
            where d.origin='own' and d.act='damage' and g.act!='damage' and g.params like '%amount=event_amount%'""") if b in cs} | \
            {b for b in cs if generic_use(c, game)[b]['trees'] & {'lifesteal'}}
    return CACHE[('back', game)]


def doublers(c, game):
    """cards that double or triple what is there ("double the enemy's Poison", Catalyst)"""
    if ('dbl', game) not in CACHE:
        cs = cards_of(c, game)
        CACHE[('dbl', game)] = {b for b, ps in c.execute("select card, params from flat_do where origin='own'")
                                if any(x in (ps or '') for x in ('=double', '=triple')) and b in cs} | {b for (b,) in c.execute(
            """select d.card from flat_do d join flat_if f on f.card=d.card and f.ability=d.ability and f.test='amount_count'
            and f.of_with = 'keyword is ' || d.keyword_ref where d.origin='own' and d.act='give_keyword' and d.params='amount=count'""") if b in cs}
        # "double the enemy's Poison" (Catalyst, Limit Break, Entrench): gives as much again as there is
    return CACHE[('dbl', game)]


def sharers(c):
    """cards whose text shares their own keywords with allies (Sivir level 2: "attacking allies have my keywords")"""
    if 'sharers' not in CACHE:
        CACHE['sharers'] = {b for (b,) in c.execute("select card from flat_do where origin='own' and act='copy_keywords' and (on_pick='self' or to_pick='self')")}
    return CACHE['sharers']


def own_power_readers(c):
    """cards whose filter is measured by their own power ("allies with equal or less power than me", Poppy)"""
    if 'pread' not in CACHE:
        ids_ = {str(i) for (i,) in c.execute("select a.id from amount a join target t on t.id=a.of_target where a.attr='power' and t.pick='self'")}
        CACHE['pread'] = {b for b, w_ in c.execute("select card, on_with from flat_do where origin='own' and on_with like '%power %'")
                          if any(re.match(r'power (le|lt|ge|gt|eq) (\d+)$', q) and q.split(' ')[2] in ids_ for q in (w_ or '').split(';'))}
    return CACHE['pread']


def power_doublers(c):
    """cards that set their own power from their power ("double my power", Black Panther): more power in hand or deck feeds it (L18)"""
    if 'pdbl' not in CACHE:
        CACHE['pdbl'] = {b for (b,) in c.execute("""select d.card from flat_do d join flat_if f on f.card=d.card and f.ability=d.ability and f.test='amount_stat'
                         and f.attr='power' and f.of_pick='self' where d.origin='own' and d.act='stat_change' and d.on_pick='self' and d.params like '%power=stat%'""")}
    return CACHE['pdbl']


def all_raisers(c):
    """cards that raise the stats of all my units at once"""
    if 'allr' not in CACHE:
        CACHE['allr'] = {a for (a,) in c.execute("""select card from flat_do where origin='own' and act in ('stat_change','grow')
                         and on_pick='all' and coalesce(on_side,'mine')='mine' and coalesce(on_with,'')=''""")}
    return CACHE['allr']


def numbered(c, game):
    """cards with a number of their own that a bigger effect raises; a harm on my own side is no number to raise (Poison Puffcap)"""
    if ('num', game) not in CACHE:
        cs = cards_of(c, game); keys = ('amount', 'power', 'health', 'strength', 'times', 'cost')
        CACHE[('num', game)] = {b for b, act, sd, ps in c.execute("select card, act, on_side, params from flat_do where origin='own'")
                                if b in cs and any(x.split('=', 1)[0] in keys for x in (ps or '').split(';') if '=' in x)
                                and not (act in ('damage', 'kill', 'discard', 'sacrifice') and sd == 'mine')} | \
            {b for b, x in cs.items() if x['x_cost']}  # an X card's X is its number (Chemical X -> Conjure Blade)
    return CACHE[('num', game)]


def uses_help(c, game, b, act, kw, ps, w=None):
    return use_of(c, game, b, act, kw, ps, w) is not None


def home_only(c):
    """(cards that move units only onto my own land, cards whose move need asks for enemy land): Desert Twister reaches no enemy land"""
    if 'home_only' not in CACHE:
        home = {a for (a,) in c.execute("select card from flat_do where origin='own' and act in ('move','swap') and to_side='mine'")} - \
            {a for (a,) in c.execute("select card from flat_do where origin='own' and act in ('move','swap') and coalesce(to_side,'')!='mine'")}
        far = {a for (a,) in c.execute("""select card from flat_ref where role!='makes' and happening in ('moves','moves_onto')
               and obj_with like '%position enemy%'""")}
        CACHE['home_only'] = (home, far)
    return CACHE['home_only']


def aimed(c, game, nodes, broad):
    """rules and targets lines from the nodes to the nodes (a filter is checked against each card); broad=False drops lines
    whose target is every card of its kind, which say nothing about which cards belong together"""
    cards = cards_of(c, game); out = Lines()
    kwn = lambda k: mechanics.name(c, k) if k else ''
    rows, makers = aimed_rows(c, game); gains = self_gains(c, nodes)
    for a, act, kind, w, kw, rule, narrowed, ps, kv in rows:
        if a not in nodes or (not narrowed and not broad): continue
        if act == 'cost_set' and re.search(r'cost (lt|le) ', w or ''): continue  # it raises costs (Mageseeker Junior): no help
        k = 'any' if kind in ('effect', 'card') else 'board' if kind in ('any', 'anything') else kind
        if kind == 'effect':  # an effect picked by its keyword ("Trap effects"): the cards that carry the keyword
            w = ';'.join(p for p in (w or '').split(';') if p.startswith('keyword'))
        hits = [b for b in nodes if b != a and b in cards and matches(c, game, cards[b], k, w) and (b not in dead_weight(c) or act == 'can')
                and not (kv and kv in cards[b]['kws'])]  # a keyword's effect on cards with the same keyword is the keyword's rule, no combo
        # (Pyke's Lurk grants Lurkers +1|+0: every Lurker does that for every other; Kaptain 2 Nov 2026)  # help on a
        # card that is never played and does nothing (Deadweight) helps nothing; letting it be played does (Blue Candle)
        if 'in_circuit' in (w or ''):  # "other creatures within a circuit": the Conduit cards that close it are its ends, not in it
            hits = [b for b in hits if b not in circuit_ends(c, game)]
        if (a, act) in CACHE.get(('handrows', game), ()):  # a card in hand or a cost: Wraithlings summoned onto the board are never there
            hits = [b for b in hits if not board_only(c, nodes, b)]
        sharp = any(p.startswith(NAMES_ONE) and not broad_part(c, game, p) for p in (w or '').split(';')) or any(
            p.split(' ')[0] not in PLAY_STATE + ('card',) and not broad_part(c, game, p) for p in (w or '').split(';') if p and not p.startswith('of:'))  # a faction or card kind is no narrower
        # than a deck (Oakling's random green creature: any creature of a green deck), nor is a stat (Poppy: allies with less power)
        kc_ = kind if kind in KIND_CAT else 'any'
        if sharp and kind_count(c, game, kc_, w) >= 0.5 * kind_count(c, game, kc_, None): sharp = False  # a filter
        # most cards of the kind pass ("costs 2 or more", Blood Song) is no deck choice
        if (act == 'repeat' or (act == 'increase_effect' and kind != 'spell')) and kind in ('landmark', 'spell', 'equipment') and \
                kind_count(c, game, kind, None) < 0.5 * kind_count(c, game, 'any', None): sharp = True  # a smaller kind of card
        # (Doctor Mia triggers structures; Kaptain's check n17) is a deck choice (L1b); more spell damage is not: only a spell whose
        # text uses its damage (Powder Keg -> Advanced Intel, Crescent Spear -> Phoenix Fire: no line) not when most cards are spells (Slay the Spire)
        if act in ('stat_change', 'grow') and kind != 'player' and not any(p.startswith(('type is', 'type in')) for p in (w or '').split(';')):
            sharp = False  # stats to units with a keyword or a stat go only to a unit whose text uses them (L14, L18: Rek'Sai's Lurkers ->
            # Sharkling: no line); a tribe stays a deck choice (Kaptain's ndu34: Oakenheart helps the Mechs)
        if act == 'increase_effect' and kind == 'spell' and 'keyword i' not in (w or ''): sharp = False  # more spell damage ()
        if act == 'cant' and any(x.startswith('cost ') for x in (w or '').split(';')):
            sharp = False  # a cost is a stat, no narrower than a deck: protection by cost goes only to a card whose text uses it (L14: Caiera -> Broodling)
        if act == 'give_keyword' and kw and kw_tree(c, kw) == 'spell_speed': sharp = False  # a spell's speed is help to a whole kind
        # (Senna makes damage spells Fast): only a card whose text uses it (L14)
        if act == 'increase_effect' and 'keyword i' not in (w or ''):
            hits = [b for b in hits if b in numbered(c, game)]  # no number to make bigger (Alatis -> Dragonling, Powder Keg -> Paralyzing Bite)
        if not sharp and (kind != 'player' or act in ('heal', 'stat_change', 'grow')) and act != 'return_card' and act not in HARM_GAIN:
            # heal or stats for the General go only to a General whose text uses them (Aer Pridebeak -> Argeon Highmayne)  # help to any card of a kind: only
            # cards that use it (Kaptain 1 Nov 2026); "your General" is one card; harm on my card is kept only for its own effect below
            wh = (w or '') + (';zone hand' if a in to_hand(c) else '')  # help to cards in hand reaches a card before it is played (Oakling, nfa01)
            hits = [b for b in hits if uses_help(c, game, b, act, kw, ps, wh)]
            if act in ('stat_change', 'grow') and a in all_raisers(c):  # all my units raised alike: no ally passes a filter by my own
                # power that it failed before (For Demacia! -> Poppy)
                hits = [b for b in hits if use_of(c, game, b, act, kw, ps, w) != 'more power: its text reads its power']
        if act == 'repeat' and 'keyword i' in (w or ''):  # a card with the keyword but no effect of its own has nothing to repeat (Onslaught -> J. Jonah Jameson)
            hits = [b for b in hits if c.execute("select 1 from flat_do where card=? and origin='own' limit 1", (b,)).fetchone()]
        n = len(makers[(act, kind, kw, rule if rule in (True, False, 'boost') else True)])
        if rule == 'boost' and act == 'repeat': hits = [b for b in hits if b not in drawback_cards(c)]  # no line to a card whose effect is a drawback (L5: Acid Arrow)
        if rule == 'boost':
            kind_, x, why = BOOST.get(act, ('boosts', 1.0, 'lets it do more'))
            for b in hits:
                y_ = use_of(c, game, b, act, kw, ps, w) if act == 'copy' or not sharp else why
                if act == 'copy' and not y_: continue  # a copy into hand or deck is one more card: no line (L19: Nautilus -> Alpha Wildclaw)
                out[(a, b)].append((kind_, x / n, y_ or why))  # a copy
            # says why it counts (its summon or death effect goes off)
            for k in (int(p.split(' ')[2]) for p in (w or '').split(';') if p.startswith(('keyword is ', 'keyword in ')) and p.split(' ')[2].isdigit()
                      and (kind in ('keyword', 'effect', 'card', 'any') or int(p.split(' ')[2]) == kw)):  # the keyword made stronger, not a filter on the
                # units it boosts (Heat Engines: Mechs standing on Fire hit harder; Fire is not made stronger)
                for b in givers_of(c, game, k, nodes) - set(hits) - {a}:  # Rage made stronger: the cards that give Rage too
                    out[(a, b)].append((kind_, x / n, f'makes the {kwn(k)} it gives stronger'))
                if act == 'increase_effect':  # Focus: the Orbs Loop sets off again are stronger too
                    for b in repeaters_of(c, k, nodes) - set(hits) - {a}:
                        out[(a, b)].append((kind_, x / n, f'makes the {kwn(k)} it sets off stronger'))
            continue
        what = rule[5:] if isinstance(rule, str) and rule.startswith('help ') else {'give_keyword': f'gives it {kwn(kw)}', 'cost_change': 'changes its cost', 'cost_set': 'sets its cost',
                'can': 'lets it do more', 'cant': 'stops it doing something', 'give_ability': 'gives it an ability',
                'give_type': 'gives it a type', 'remove_keyword': f'removes {kwn(kw)}', 'copy_keywords': 'gives it keywords',
                'mark': 'marks it'}.get(act, act.replace('_', ' '))
        pev = dict(p.split('=', 1) for p in (ps or '').split(';') if '=' in p).get('event')
        if act in ('can', 'cant') and pev:  # say what it may or may not do: "lets it be summoned there", "stops it moving"
            what = {('can', 'summoned'): 'lets it be summoned in more places', ('can', 'played'): 'lets it be played in more places',
                    ('can', 'moves'): 'lets it move more', ('cant', 'moves'): 'stops it moving', ('cant', 'attacks'): 'stops it attacking',
                    ('cant', 'targeted'): 'protects it from targeting', ('cant', 'dies'): 'keeps it from dying', ('cant', 'given_keyword'): f'keeps {kwn(kw) or "a status"} off it'}.get((act, pev), what + f' ({pev})')
        at = where(w)  # who benefits from a place: "when next to it", "in its circuit" (positional games; Inscryption Leader)
        if act == 'return_card':  # "put all cost 0 cards from your discard pile into your hand" (All for One): it brings them back
            if not (narrowed and sharp) and a not in CACHE.get(('from_exhaust', game), ()): continue  # "a Skill" is half the cards  # "return a spell from the discard pile"
            # (Returned Soul): any spell can be returned; only a narrower filter makes a line (L1, like draws)
            if a in CACHE.get(('from_exhaust', game), ()):  # "return a consumed spell" (Echowright): only cards that consume themselves are there
                hits = [b for b in hits if any(kw_tree(c, k) == 'exhaust' for k in cards[b]['kws'])]
            for b in hits: out[(a, b)].append(('puts', 1.0 / max(1, len(hits)), 'brings it back to your hand'))
            continue
        for b in hits:
            if act in ('move', 'swap') and a in home_only(c)[0] and b in home_only(c)[1]: continue  # onto my land, it needs enemy land
            said_ = (use_of(c, game, b, act, kw, ps, w) if not sharp and act == 'give_keyword' and not rule else None)  # a keyword given
            # to any ally: say how its text uses it (L16: Lucky Find -> Sivir level 2)
            if rule and act in ('stat_change', 'grow') and 'level_hit' in generic_use(c, game)[b]['flags'] and \
                    any(raises(v) for k, v in (x.split('=', 1) for x in (ps or '').split(';') if '=' in x) if k in ('power', 'strength')):
                out[(a, b)].append(('levels', 1.0 / n, what + ': helps it level up' + at))  # it levels from the damage it deals (L24)
            elif rule: out[(a, b)].append(('boosts' if isinstance(rule, str) else 'rules', 1.0 / n, what + at))  # stats given make it stronger; the rest change how it works
            elif helps_it(c, act, kw, ps): out[(a, b)].append(('boosts', 0.5 / max(1, len(hits)), (said_ or aim_said(act, kwn(kw), ps)) + at))
            elif act in HARM_GAIN and not gains.get(b, set()) & HARM_GAIN[act]: continue  # my harm on my card: only for its own effect
            elif act == 'give_keyword' and kw_tree(c, kw) in BAD_STATUS: continue  # Sparkly Kitties confuses a friend: a drawback, no help
            elif act in ('remove_keyword', 'remove_keywords') and not kw: continue  # "steal all statuses from friendly units" (Timber Alchemists): every
            # unit can have one (L1); its partners are the cards that give statuses
            else:  # an act on my card that is no help (strike, return, copy, damage): only a card whose own text uses it (L14)
                use = {'damage': 'damages it: its own effect goes off', 'kill': 'kills it: its death effect goes off'}.get(act) \
                    if act in HARM_GAIN else use_of(c, game, b, act, kw, ps, w)  # harm: kept above only when the card gains from it
                if use: out[(a, b)].append(('targets', 0.5 / n, use + at))  # said only when no other reason joins the pair
                continue  # help aimed at one card of a kind helps
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


def boosts_it(act, ps):
    """an effect that repeats what set it off or makes it bigger (not smaller: Weak, Frail)"""
    return act in ('repeat', 'increase_effect') and not any(v.startswith('-') for k, v in (x.split('=', 1) for x in (ps or '').split(';') if '=' in x))


def help_abilities(c):
    """triggers whose effects only help the card that set them off ("the first Golem you summon each turn costs 1 less"): a
    help line from the card to those cards, no wait or ask for them"""
    if 'helpab' in CACHE: return CACHE['helpab']
    hp = collections.defaultdict(set)
    obj = {ab_: (k, sd) for ab_, k, sd in c.execute("select ability, obj_kind, obj_side from flat_when where obj_kind is not null")}
    for ab_, act, p_, k, sd, kw, ps in c.execute("select ability, act, on_pick, on_kind, coalesce(on_side,''), keyword_ref, params from flat_do where origin in ('own','gives')"):
        same = p_ == 'it' or (p_ is None and obj.get(ab_) == (k, sd) and k == 'player')  # "the first time your General takes damage,
        hp[ab_].add(same and sd != 'enemy' and (helps_it(c, act, kw, ps) or act in HELP_ACTS or boosts_it(act, ps)))  # prevent 2 of it";
        # "this turn, your next Skill is played twice" (Burst, given to the player): it helps the Skills, it asks for none
    CACHE['helpab'] = {a for a, v in hp.items() if v == {True}}
    return CACHE['helpab']


def protect_abilities(c):
    """help triggers that only protect what set them off from the damage that did ("prevent 2 of it"): they want no damage"""
    if 'protab' not in CACHE:
        acts = collections.defaultdict(set)
        for ab_, act in c.execute("select ability, act from flat_do where origin='own'"): acts[ab_].add(act)
        for ab_, k_ in c.execute("select ability, keyword_ref from flat_do where origin='own' and act='give_keyword' and on_pick='it'"):
            if kw_tree(c, k_) in ('shield', 'damage_reduction', 'immunity'): acts[ab_] = (acts[ab_] - {'give_keyword'}) | {'negate_damage'}
        CACHE['protab'] = {a for a in help_abilities(c) if acts[a] <= {'negate_damage', 'damage_reduction'}}  # Auto-Shields: a shield on
        # the building that was hit wants no hits
    return CACHE['protab']


# ground a unit pushed onto dies on (Into the Breach, wiki Tiles: "Ground units pushed in will be destroyed"; "Most non-flying
# enemies die in Water"; Lava "behaves like Water"; "Cracked tiles will turn into holes if damaged")
DEADLY_GROUND = {'into_the_breach': {
    'chasm': '{A} makes holes, and {B} pushes enemy units: a ground unit pushed into a hole dies',
    'ocean': '{A} makes water, and {B} pushes enemy units: most Vek pushed into water drown',
    'lava': '{A} makes lava, and {B} pushes enemy units: most Vek pushed into lava die',
    'cracked_space': '{A} cracks the ground (a hole once hit), and {B} pushes enemy units: a ground unit pushed into a hole dies'}}


def doer_help_abilities(c):
    """triggers on what my units of a kind do that only help the unit that did it ("heal any Mech that kills", Viscera
    Nanobots): a help line from the card to those units (doer_help_lines), no wait for it"""
    if 'doerhelp' in CACHE: return CACHE['doerhelp']
    trig = {ab_ for (ab_,) in c.execute("""select ability from flat_when where origin='own' and actor_kind is not null and actor_kind!='player'
            and coalesce(actor_side,'mine')='mine' and coalesce(actor_pick,'') not in ('self','it')""")}
    hp = collections.defaultdict(set)
    for ab_, act, p_, kw, ps in c.execute("select ability, act, on_pick, keyword_ref, params from flat_do where origin='own'"):
        if ab_ in trig: hp[ab_].add(p_ == 'actor' and (helps_it(c, act, kw, ps) or act in HELP_ACTS))
    CACHE['doerhelp'] = {a for a, v in hp.items() if v == {True}}
    return CACHE['doerhelp']


DOES = {'killed': 'kills', 'damaged': 'deals damage', 'attacks': 'attacks', 'strikes': 'strikes', 'moves': 'moves'}


def doer_help_lines(c, game, nodes):
    """the help of doer_help_abilities, to each card of the deck of that kind that does it ("heals it when it kills")"""
    cards = cards_of(c, game); out = Lines(); marks = ','.join('?' * len(nodes)); L = list(nodes)
    abs_ = doer_help_abilities(c)
    for a, ab_, h in c.execute(f"select distinct card, ability, event from flat_when where origin='own' and card in ({marks})", L).fetchall():
        if ab_ not in abs_: continue
        kind, _, _, w = actor_of(c, ab_)
        whys = []
        for act, kw, ps in c.execute("select act, keyword_ref, params from flat_do where card=? and ability=? and origin='own'", (a, ab_)):
            whys.append(aim_said(act, mechanics.name(c, kw) if kw else '', ps).removeprefix('can ').replace('heal it', 'heals it')
                        .replace('give it', 'gives it'))
        doers = {m for (m,) in c.execute(f"""select distinct card from flat_ref where role='makes' and happening=? and origin in
                 ('own','uses_keyword') and card in ({marks})""", [h] + L)}
        for m in doers:
            if m != a and m in cards and matches(c, game, as_doer(c, game, cards[m]), kind if kind in KIND_CAT else 'any', w):
                out[(a, m)].append(('boosts', 1.0 / max(1, len(doers)), '{A} ' + ', '.join(dict.fromkeys(w_.replace(' it', ' {Bc}') for w_ in whys)) + f' when it {DOES.get(h, h.replace("_", " "))}'))
    return out


def harm_abilities(c):
    """abilities whose effects only hurt the card that set them off ("take 1 damage when summoned", Kujata): no want"""
    if 'harm' in CACHE: return CACHE['harm']
    harm = collections.defaultdict(set)
    paid = {a for (a,) in c.execute("select ability from flat_when where event in ('played','activated')")}  # a cost to play or use
    for ab_, act, p_, sd in c.execute("select ability, act, on_pick, coalesce(on_side,'') from flat_do where origin='own'"):
        harm[ab_].add((act in ('damage', 'kill', 'discard', 'sacrifice') and p_ == 'it' and sd != 'enemy') or
                      (act == 'spend_mana' and sd in ('mine', '') and ab_ not in paid))  # Void: "when drawn, lose 1 Energy" wants no
        # draws and no mana; "Pay 2 Bones" to play or activate is a need
    CACHE['harm'] = {a for a, v in harm.items() if v == {True}}
    return CACHE['harm']


def special_abilities(c):
    """abilities read by what they do, not as needs: plain hits (every own effect deals damage to one chosen or random target:
    Strike), keepers (every own effect stops a keyword's removal: Barricade), self cost cuts (every own effect lowers this
    card's cost: Eviscerate)"""
    if 'special' not in CACHE:
        acts = collections.defaultdict(set)
        for ab, act, pk, pev, ps, o in c.execute("select ability, act, on_pick, param_event, params, origin from flat_do where origin in ('own','has_keyword')"):
            if o == 'has_keyword':  # a keyword's one-target hit (Sharp Quills: 1 damage to its attacker)
                acts[ab].add('hit' if act == 'damage' and pk in ('chosen', 'random', 'actor') else 'other'); continue
            acts[ab].add('hit' if act == 'damage' and pk in ('chosen', 'random', 'actor') else
                         'keep' if act == 'cant' and pev == 'keyword_removed' else
                         'cheap' if act == 'cost_change' and pk == 'self' and ('=-' in (ps or '') or 'cost=minus' in (ps or '')) else 'other')
        CACHE['special'] = tuple({a for a, v in acts.items() if v == {x}} for x in ('hit', 'keep', 'cheap'))
    return CACHE['special']


def every_card_kinds(c, game):
    """kinds that every playable card of the game is (Slay the Spire: every card is a spell): "when you play a spell" there
    counts every card, which is no link (Kaptain 30 Oct 2026: links come from what a card's text does, not from playing it)"""
    key = ('everykind', game)
    if key not in CACHE:
        cats = {x['cat'] for x in cards_of(c, game).values() if (x['cost'] is not None or x['x_cost']) and
                any(x['cat'] in v for v in KIND_CAT.values())}
        CACHE[key] = {k for k, v in KIND_CAT.items() if cats and cats <= v}
    return CACHE[key]


def status_damage_givers(c, game, nodes):
    """(card, status name): the card gives a status whose own ability makes damage bigger, on the enemy it is given to (it takes
    more: Vulnerable) or on my side (I deal more: Wrath). Not a status only some damage uses (Lock-On: Orbs)"""
    boost = {}
    for k, ab, ak, aside, oside in c.execute("""select w.card, w.ability, w.actor_kind, coalesce(w.actor_side,''), coalesce(w.obj_side,'')
            from flat_when w join card k on k.id=w.card where k.is_keyword=1 and k.game=? and w.event='damaged' and w.origin='own'""", (game,)):
        dos = c.execute("select act, on_pick, params from flat_do where card=? and ability=? and origin='own'", (k, ab)).fetchall()
        more = lambda a_, pk, ps: (a_ == 'increase_effect' and pk == 'it' and boosts_it(a_, ps)) or \
            (a_ == 'damage' and pk == 'self' and 'amount=event_amount' in (ps or ''))  # A.C.I.D.: "weapon damage against this unit is doubled"
        if not dos or not all(more(a_, pk, ps) for a_, pk, ps in dos): continue
        if ak == 'keyword': boost[k] = 'enemy_keyword'  # Lock-On: the Orbs' damage to its holder is bigger
        elif aside == 'mine': boost[k] = 'mine'  # I deal more
        elif oside != 'mine': boost.setdefault(k, 'enemy')  # its holder takes more
    for k, d in c.execute("""select f.card, f.keyword_ref from flat_do f join card k on k.id=f.card where k.is_keyword=1 and k.game=?
            and f.origin='own' and f.act='give_keyword'""", (game,)).fetchall():  # Mantra: at 10 you enter Divinity
        if d in boost and k not in boost and k != d: boost[k] = boost[d]
    marks = ','.join('?' * len(nodes))
    # a status of no side put on a target the player picks goes on enemies when it hurts (refs.py HARM: A.C.I.D. Projector)
    return {(a, mechanics.name(c, k), boost[k] == 'enemy_keyword') for a, k, side in c.execute(f"""select card, keyword_ref,
            coalesce(on_side, case when on_pick in ('chosen','nearest','random') then 'enemy' else 'mine' end) from flat_do where
            act='give_keyword' and origin='own' and card in ({marks})""", list(nodes)) if k in boost and side == boost[k].split('_')[0]}


def capped(c):
    """(ability, happening) where a count is an upper limit on what other cards do ("if you have played less than 3 cards
    this turn", FTL): it wants fewer of it, nothing feeds it. Not a first-N trigger ("the first 3 times you play a card"),
    which waits for the happening it counts."""
    if 'capped' not in CACHE:
        waits = {(a, e) for a, e in c.execute("select ability, event from flat_when where coalesce(obj_pick,'')!='self'")}
        CACHE['capped'] = {(a, e) for a, e in c.execute("""select ability, event from flat_if where op in ('lt','le') and event is not null
                           and test in ('event_count','count','amount_event_count')""") if (a, e) not in waits}
    return CACHE['capped']


def most_cards(c, game, kind):
    """half or more of the game's cards are of this kind (Monster Train: spells): being one says nothing"""
    key = ('most', game, kind)
    if key not in CACHE:
        allc = [x for x in cards_of(c, game).values() if x['cat'] not in ('keyword',)]
        CACHE[key] = kind in KIND_CAT and sum(1 for x in allc if x['cat'] in KIND_CAT[kind]) >= 0.5 * max(1, len(allc))
    return CACHE[key]


def dead_weight(c):
    """cards never played that do nothing themselves (Deadweight: "Unplayable. Unpurgeable."); a card that acts from the hand
    (Bone Dog's Favor's Reserve) is not one"""
    if 'dead' not in CACHE:
        acting = {a for (a,) in c.execute("select distinct card from flat_do where origin='own' and coalesce(on_pick,'') != 'self'")}
        CACHE['dead'] = unplayable(c) - acting
    return CACHE['dead']


def unplayable(c):
    """cards that can never be played (Unplayable: Void, curses): never a card played"""
    if 'unplayable' not in CACHE:
        CACHE['unplayable'] = {a for (a,) in c.execute("""select card from flat_do where act='cant' and param_event='played' and on_pick='self'
                               and origin in ('own','has_keyword') and coalesce(lasts,'while')='while'""")} | {a for (a,) in c.execute("""select id from card k
                               where category in ('spell','ability') and is_keyword=0 and not exists (select 1 from flat_do d where d.card=k.id)
                               and not exists (select 1 from flat_when w where w.card=k.id) and not exists (select 1 from flat_if f where f.card=k.id)""")}
        # a spell or skill with no rows is a deck rule (Grandmaster at Arms), not a card anyone plays ()
    return CACHE['unplayable']


def planted_only(c):
    """cards that only ever come by being planted in the deck (Chime, Poison Puffcap, Flashbomb Trap): they go off when drawn and
    are never played"""
    if 'planted' not in CACHE:
        planted = {r for (r,) in c.execute("select card_ref from flat_do where act='keyword_action' and card_ref is not null")}
        other = {r for (r,) in c.execute("""select card_ref from flat_do where act in ('create','copy','summon','draw','play_card') and card_ref is not null""")}
        CACHE['planted'] = planted - other
    return CACHE['planted']


GERUND = {'played': 'playing', 'summoned': 'summoning', 'drawn': 'drawing'}


def made_cards(c):
    """cards that make a card by description, not by name: (card, kind, filter) ("Manifest a 6+ cost spell", "create a random
    landmark"); a kind written as a filter ("card", "category is spell") is read as that kind"""
    if 'made_desc' in CACHE: return CACHE['made_desc']
    out = []
    for a, k, w in c.execute("""select card, on_kind, on_with from flat_do where act in ('create','summon','choose_card','random_one')
            and card_ref is null and origin in ('own','uses_keyword','has_keyword') and coalesce(on_side,'mine') in ('mine','any') and coalesce(on_pick,'') != 'it'"""):
        parts = [p for p in (w or '').split(';') if p]
        cat = next((p.split(' ')[2] for p in parts if p.startswith('category is ')), None)
        k = {'spell': 'spell', 'unit': 'unit', 'follower': 'unit', 'landmark': 'landmark', 'equipment': 'equipment'}.get(cat, k) if k in (None, 'card', 'any') else k
        if k in ('unit', 'spell', 'landmark', 'equipment'): out.append((a, k, ';'.join(p for p in parts if not p.startswith('category '))))
    CACHE['made_desc'] = out
    return out


def made_fits(c, kind, w, mk, mw):
    """a card made as (mk, mw) is always one that a need for (kind, w) counts: same kind, and each part of the need is said by the
    making too ("a 6+ cost spell" made fits "6+ cost spells played"; a cost of 7+ fits 6+)"""
    if kind not in (mk, 'card', 'any', None): return False
    have = [p for p in (mw or '').split(';') if p]
    for q in (p for p in (w or '').split(';') if p and not p.startswith(('category ', 'of:'))):
        if q in have: continue
        f = q.split(' ')
        if f[0] == 'cost' and f[1] == 'ge' and any(h.split(' ')[:2] == ['cost', 'ge'] and (number(c, h.split(' ')[2]) or 0) >= (number(c, f[2]) or 99) for h in have): continue
        return False
    return True


def played_lines(c, game, nodes, broad):
    """a card that is itself what another waits for or counts when it is played or summoned ("when you play a spell",
    "Fast spells, Slow spells or Skills you've played"); only when the kind is narrowed past "any card" or "any unit".
    "N cards with different names" is helped by cards that create cards (more different cards to play)."""
    cards = cards_of(c, game); out = Lines(); marks = ','.join('?' * len(nodes)); lvl = level_abilities(c)
    for t, ab, h, kind, side, pick, w, role in c.execute(f"""select card, ability, happening, kind, side, pick, obj_with, role from flat_ref where role!='makes'
            and origin in ('own','gives') and happening in ('played','summoned','drawn','mana_spent') and coalesce(pick,'')!='self' and side in ('mine','any','')
            and card in ({marks})""", list(nodes)).fetchall():
        if ab in harm_abilities(c) or ab in help_abilities(c) or (ab, h) in capped(c): continue
        if not side and role == 'trigger' and ab in reacts_against(c, game): continue  # Sentinel, Night Watcher: the enemy's cards
        if c.execute("select 1 from flat_do f join flat_ref r on r.ability=f.ability and r.card=f.card where f.ability=? and r.origin='gives' "
                     "and f.on_pick='it' limit 1", (ab,)).fetchone(): continue  # a given "your next minion costs 2 less and takes 2 damage"
        # acts on the card that sets it off: it is aimed at that card, not waiting for it (Rage, Choke act on others: they wait)
        if h == 'mana_spent':  # "6+ mana of spells" (Lux): every spell played spends it; a kind it names is needed
            if kind not in KIND_CAT: continue
            h = 'played'
            big = c.execute("select max(n) from flat_if where ability=? and test='amount' and op in ('ge','gt')", (ab,)).fetchone()[0]
            if big and c.execute("select 1 from flat_if where ability=? and test='amount_event_amount'", (ab,)).fetchone():
                w = ';'.join(x for x in ((w or ''), f'cost ge {float(big)}') if x)  # one spell of 6+ mana (Lux level 2): only a card
                # that alone costs that much sets it off (Conchologist's 3-cost spells do not; L17)
        k = kind or ('card' if h in ('played', 'drawn') else 'unit')
        narrowed = any(p and p.split(' ')[0] not in PLAY_STATE and p.split(' ')[1:2] != ['not'] for p in (w or '').split(';'))
        kk = 'any' if k in ('card', None) else k
        if kk in KIND_CAT or kk == 'any':  # most cards pass the filter ("summon a creature with higher Attack than Life", Firebringer)
            narrowed = narrowed and kind_count(c, game, kk, w) < 0.5 * kind_count(c, game, kk, None)
        narrowed = narrowed and any(p and p.split(' ')[0] != 'category' and p.split(' ')[1:2] != ['not'] for p in (w or '').split(';')
                                    if p.split(' ')[0] not in PLAY_STATE)  # "another follower" (Beguiling Cobra) is any unit
        if not narrowed and (k in ('card', 'any', 'anything', None) or k in every_card_kinds(c, game) or (k == 'unit' and h in ('summoned', 'played'))
                             or not broad or most_cards(c, game, k)):  # "whenever you play a spell" where most cards are spells
            # (Monster Train's Incant): being one is no interaction (L1; Kaptain 1 Nov 2026); a minority kind is a deck choice (Annie)
            if h == 'played' and role == 'trigger' and broad:  # "whenever you play a card" (A Thousand Cuts): not every card, but
                # Kaptain's nst26 keeps it (Blade Dance -> A Thousand Cuts)
                # the cards that make more cards to play (Blade Dance's Shivs) set it off more
                mk = {a for a, ref, ok in c.execute(f"""select distinct card, card_ref, on_kind from flat_do where origin='own' and act in ('create','copy')
                      and coalesce(on_side,'mine')='mine' and coalesce(on_zone,'hand') in ('hand') and (params like '%amount=x%' or cast(substr(params,
                      instr(params,'amount=')+7) as real) >= 2) and card in ({marks})""", list(nodes))  # several cards (Blade Dance's 3 Shivs);
                      # one more card is no more plays (Beta -> After Image+, Annie -> Breakneck Husk)
                      if k in ('card', 'any', 'anything', None) or k in every_card_kinds(c, game) or ok == k or (ref in cards and cards[ref]['cat'] in KIND_CAT.get(k, {k}))} - {t}
                # "whenever you play a spell": only what makes spells (Vinemother's Stings) sets it off more
                for a in mk:
                    if ('waits', 0.5 / len(mk), 'makes more cards to play') not in out[(a, t)]: out[(a, t)].append(('waits', 0.5 / len(mk), 'makes more cards to play'))
            continue
        n = kind_count(c, game, 'any' if k == 'card' else k, w)
        for a in nodes:
            if a != t and a in cards and matches(c, game, cards[a], 'any' if k == 'card' else k, w) and \
                    not (h in ('played', 'drawn') and board_only(c, nodes, a)) and not (h == 'played' and (a in unplayable(c) or a in planted_only(c))):  # a token
                # summoned on the board is never played or drawn; an Unplayable card is never played
                tn = next((c.execute('select name from type where id=?', (int(p.split(' ')[2]),)).fetchone() for p in (w or '').split(';')
                           if p.split(' ')[:2] == ['type', 'is'] and p.split(' ')[2].isdigit()), None)
                art = "an" if tn and tn[0][:1] in "AEIOU" else "a"; what_ = tn[0] if tn else ("card" if k in ('card', 'any') else k)
                why = f'is {art} {what_} whose {GERUND.get(h, h)} sets off its effect' if role == 'trigger' else \
                      f'is {art} {what_} it needs played for its count' if h == 'played' else f'is {art} {what_} it needs {h} for its count'
                # a reaction ("when you play a spell", Nami) or a count ("6+ mana of spells", Lux): said as what it is
                kind_ = 'cheaper' if ab in special_abilities(c)[2] else 'waits' if role == 'trigger' else 'type'  # "costs 1 less for each
                # event played": makes cheaper; a reaction ("every 3rd Attack"): triggers; a count it needs: enables (Kaptain 30 Oct)
                line = ('levels', 2.0 / n, why + ' (levels it up)') if ab in lvl else (kind_, 1.0 / n, why)
                have = [l for l in out[(a, t)] if l[2] == line[2]]
                if not have: out[(a, t)].append(line)
                elif line[0] in ('cheaper', 'waits') and all(l[0] == 'type' for l in have):  # said once, by the stronger kind
                    out[(a, t)] = [l for l in out[(a, t)] if l[2] != line[2]] + [line]
        if h in ('played', 'summoned'):  # a card that makes such a card gives it one more to play (Ferros Financier manifests a 6+ cost
            # spell: Jayce counts two 6+ cost spells played, Lux counts 6+ mana of spells)
            for a, mk, mw in made_cards(c):
                if a == t or a not in nodes or a not in cards or not made_fits(c, k, w, mk, mw): continue
                say = f'makes a {mk} whose {GERUND.get(h, h)} sets off its effect' if role == 'trigger' else f'makes a {mk} it needs {h} for its count'
                if not any(l[2].startswith(say) for l in out[(a, t)]):
                    out[(a, t)].append(('levels', 1.0 / n, say + ' (levels it up)') if ab in lvl else ('waits' if role == 'trigger' else 'type', 0.5 / n, say))
    for t, ab in c.execute(f"""select card, ability from flat_if where test in ('amount_distinct','distinct') and attr='region'
            and card in ({marks})""", list(nodes)).fetchall():  # "allies from 10 regions" (The Bandle Tree): cards that make
        # multi-region or other-region cards bring more regions (L17)
        for (a,) in c.execute(f"""select distinct card from flat_do where origin='own' and act in ('create','summon','keyword_action')
                and coalesce(on_side,'mine')='mine' and (on_with like '%multi_region%' or on_with like '%region not own_regions%') and card in ({marks})""", list(nodes)):
            if a != t: out[(a, t)].append(('levels' if ab in lvl else 'type', 0.5, 'makes a card from more regions: more regions for its count' +
                                           (' (levels it up)' if ab in lvl else '')))
    for t, ab in c.execute(f"""select card, ability from flat_if where test in ('amount_distinct','distinct') and event='played'
            and card in ({marks})""", list(nodes)).fetchall():
        # cards that make cards I then play: not planted Chimes or traps, which go off by themselves when drawn and are never
        # played (Esmus plants a Chime: no more names for Zoe)
        for (a,) in c.execute(f"""select distinct d.card from flat_do d where d.act in ('create','copy') and d.origin in ('own','uses_keyword')
                and coalesce(d.on_side,'mine')='mine' and not exists (select 1 from flat_do p where p.card=d.card and p.origin='own'
                and p.act='keyword_action' and p.card_ref is not null and d.origin='uses_keyword' and p.keyword_ref=d.via)
                and d.card in ({marks})""", list(nodes)):
            if a != t: out[(a, t)].append(('levels' if ab in lvl else 'type', 0.2, 'creates cards: more different cards to play' +
                                           (' (levels it up)' if ab in lvl else '')))
    return out


def need_lines(c, game, nodes, broad):
    """a card that needs a kind of card on my side: measured from it ("units surrounding a friendly structure") or counted or
    tested ("if you have a structure"); fed by cards of that kind"""
    cards = cards_of(c, game); out = Lines(); marks = ','.join('?' * len(nodes)); needs = []
    for t, w, side in c.execute(f"select card, coalesce(on_with,'') || ';' || coalesce(to_with,''), on_side from flat_do where card in ({marks})", list(nodes)):
        parts = (w or '').split(';')
        of = [p[3:] for p in parts if p.startswith('of:')]
        kind = next((p.split(' ')[2] for p in of if p.startswith('kind is ')), None)
        rest_ = [p for p in of if not p.startswith('kind')]
        if kind == 'any' and not rest_: continue  # a place measured from any card ("in front of each enemy minion", Star's Fury): no need
        if kind and kind not in ('unit', 'player', 'unit_or_structure'): needs.append((t, kind, ';'.join(rest_)))
        # any unit (or structure) fits a place measured from it ("the tile beyond the pushed unit"): no need
    # a count of what happens to my cards of a kind ("you've destroyed 4+ allied landmarks"): fed by cards of that kind
    for t, kind, w in c.execute(f"""select card, ev_obj_kind, ev_obj_with from flat_if where card in ({marks}) and test in ('event_count','amount_event_count')
            and ev_obj_side='mine' and ev_obj_kind in ('landmark','equipment','spell')
            and coalesce(event,'') not in ('played','summoned','drawn')""", list(nodes)).fetchall():  # played_lines counts those (one rule per need)
        needs.append((t, kind, (w or '') + ';counted'))
    for t, test, kind, side, op, n, w, pick_ in c.execute(f"""select card, test, of_kind, of_side, op, n, of_with, of_pick from flat_if where card in ({marks})
            and test in ('have','count','amount_count','last_card') and coalesce(of_side,'mine') in ('mine','any','')""", list(nodes)):  # last_card: "if the last card played was an Ongoing unit" needs such a card
        if op == 'not' or (op in ('eq', 'le', 'lt') and not n): continue  # "no units around": nothing to feed
        # "non-X" narrows nothing; nor does what a place is measured from ("near your General": of:kind is player)
        narrowed = any(p and not p.startswith('of:') and p.split(' ')[0] not in PLAY_STATE + ('card',) and p.split(' ')[1:2] != ['not'] for p in (w or '').split(';'))
        if kind is None and pick_ == 'it' and 'keyword is ' in (w or ''): kind = 'unit'  # "if that minion has Zeal": cards with Zeal
        own = [p for p in (w or '').split(';') if p and not p.startswith('of:')]
        if own and all(p.split(' ')[0] in ('power', 'health') and p.split(' ')[1:2] == ['eq'] for p in own): continue
        # "the numbers 1 to 5 in the Power and Health of creatures in your deck" (Curious Egg): a stat every creature has is no
        # need (L1); its tribes are
        if narrowed and kind in KIND_CAT and kind_count(c, game, kind, w) >= 0.5 * kind_count(c, game, kind, None): narrowed = False  # most
        # creatures pass the filter ("a creature with higher Attack than Life", Shedim Pest, read as any): no deck choice
        if kind in KIND_CAT and kind != 'player' and (narrowed or kind != 'unit'): needs.append((t, kind, w))  # a player is always there
        elif kind in (None, 'card') and narrowed and kind_count(c, game, 'any', w) < 0.5 * kind_count(c, game, 'any', None):
            needs.append((t, 'any', w))  # "if you have an 8+ cost card" (Faces of the Old Ones), "a Nightfall card" (The Sky Shadows):
            # a minority of cards is a deck choice (L1b, L21)
    # a keyword's effects acted on ("activate the effects of all traps"): the cards that carry the keyword
    for t, k in c.execute(f"""select card, keyword_ref from flat_do where act='keyword_action' and card_ref is null and keyword_ref is not null
            and on_kind is null and origin='own' and card in ({marks})""", list(nodes)).fetchall():
        if any(k in cards[a]['kws'] for a in nodes if a in cards and a != t): needs.append((t, 'any', f'keyword is {k}'))
    # cards that make a card of a kind by description ("create a random landmark that costs 2 or less", Bomber Twins)
    described = collections.defaultdict(set)
    for a, k, _ in made_cards(c):  # "create a random landmark", "Manifest a 6+ cost spell" (a kind written as a filter too)
        if a in nodes: described[k].add(a)
    for t, kind, w in needs:
        counted = (w or '').endswith(';counted'); w = (w or '').removesuffix(';counted')  # "each event you've played": it counts what
        # happens: "enables" (a count, no reaction)
        cnt = kind_count(c, game, kind, w)
        what = ('a card it acts on' if 'keyword_action' in (w or '') or not any(p_.startswith(('cost ', 'keyword ', 'type ')) for p_ in (w or '').split(';'))
                else 'a card it asks for') if kind == 'any' else f'a {"landmark or structure" if kind == "landmark" else kind} it asks for'
        kws_ = [mechanics.name(c, int(p.split(' ')[2])) for p in (w or '').split(';') if p.startswith('keyword is ') and p.split(' ')[2].isdigit()]
        if not kws_ and not counted and any(p.split(' ')[:2] in (['type', 'is'], ['type', 'in']) for p in (w or '').split(';')): continue  # the type line says it ("is a Conduit card it asks for")
        if kind != 'any' and most_cards(c, game, kind) and not [p for p in (w or '').split(';') if p and p.removeprefix('of:').split(' ')[0] not in ('category', 'position', 'distance', 'right_of', 'origin', 'level', 'countdown')]:  # a status ("poisoned units") narrows
            continue  # "the number of spells in your deck" (Ancient Synergy): every spell is one; a kind alone is no need (L1)
        if not counted and kind != 'any' and w and all(p.removeprefix('of:').split(' ')[0] in ('position', 'strength', 'power', 'health', 'cost')
                                                        for p in w.split(';') if p): continue  # "a stronger friendly unit next to it" (Mystwives):
        # any unit can be that; a place or a stat number is no need (L1; Kaptain 31 Oct 2026, Curious Egg)
        if kws_ and kind != 'any': what = what.replace(' it asks for', f' with {", ".join(kws_)} it counts or asks for')  # "a unit with Ant
        for a in nodes:
            if a == t or a not in cards: continue
            if counted:
                if matches(c, game, cards[a], kind, w): out[(a, t)].append(('type', 1.0 / cnt, f'is a {kind} it counts'))
                elif a in described.get(kind, ()) and not any(p.split(' ')[0] in ('card', 'name_has', 'type') for p in (w or '').split(';')):
                    out[(a, t)].append(('type', 0.5 / cnt, f'makes a {"landmark or structure" if kind == "landmark" else kind} it counts'))
                continue
            if matches(c, game, cards[a], kind, w): out[(a, t)].append(('type', 1.0 / cnt, 'is ' + what))
            elif a in described.get(kind, ()) and not any(p.split(' ')[0] in ('card', 'name_has', 'type') for p in (w or '').split(';')):
                out[(a, t)].append(('type', 0.5 / cnt, 'makes ' + what))
    return out


# What helps a card's need, the same in every game: (happenings it needs, sides of the thing it happens to), the concepts that
# help, and why. A card helps when its own rows, or a keyword it gives, have the concept on my side (not only on itself); a
# unit with the concept as its own keyword helps too (an Overwhelm unit gets damage through to the enemy player).
# fight keywords and the only needs each serves by itself (a unit's normal fight is no combo, R2): 'nexus' = the enemy player hit
KW_NEEDS = {'excess_damage': ('nexus',), 'evasion': ('nexus',), 'deathtouch': ('dies', 'killed'), 'lifesteal': ('healed',),
            'first_strike': (), 'piercing': ()}
ATTACK = ('attack_gain', 'temporary_buff', 'multi_attack', 'extra_turn', 'attack_now')
HELPS = [
    # each help must do the very thing needed (Kaptain 31 Oct 2026): power gets no unit past blockers (Zed: Sharpsight, For Demacia!
    # are no help), nor deals a level-up's damage (Gwen: Tybaulk); only evasion, Overwhelm, another attack or strike reach the Nexus
    (('nexus_damaged', 'strikes_nexus'), ('enemy', '', 'mine'), ('excess_damage', 'evasion', 'multi_attack', 'extra_turn', 'start_attack'), 'helps it hit the enemy player'),
    # Overwhelm adds no damage to a unit: its extra goes to the Nexus (L4, L18: Might -> Scorched Earth, Sion -> Ravenous Flock: no line)
    (('killed',), ('enemy', '', 'mine', 'any'), ATTACK + ('first_strike', 'target_choice'), 'helps my units kill'),
    (('strikes',), ('enemy', '', 'mine', 'any'), ('multi_attack', 'extra_turn', 'start_attack'), 'helps my units strike more'),
    # another attack: an attack token (Rally) or a free attack; striking twice, a strike now or a unit summoned attacking is not one
    (('attacks',), ('mine', '', 'any'), ('extra_turn', 'start_attack'), 'another attack'),
    (('survives_damage',), ('mine', ''), ('defence_gain', 'shield', 'damage_reduction', 'immunity', 'regeneration', 'heal',
                                         'cheat_death', 'block_armor', 'lifesteal'), 'more health or protection: survives damage'),
    # where a unit must get to (enemy land, an enemy well, a forest, the enemy god): what moves my units, or units that move
    # well, gets it there (positional games: moving is how a unit reaches the enemy player)
    (('moves_onto', 'harvests', 'fights'), ('mine', '', 'enemy', 'any'), ('movement',), 'moves it where it must be'),
    (('strikes_nexus', 'nexus_damaged'), ('enemy', '', 'mine'), ('movement',), 'moves it within reach of the enemy player'),
]
GIVEN = ('attack_gain', 'defence_gain', 'shield', 'damage_reduction', 'immunity', 'regeneration', 'heal', 'cheat_death', 'block_armor',
         'lifesteal', 'excess_damage', 'evasion')  # help that is a stat or keyword given: it lands where it names
HIT_KW = ('target_choice', 'excess_damage', 'multi_attack', 'first_strike', 'evasion', 'ranged')  # keywords whose use depends on power


def other_resource(c, t):
    """a card paid in a resource that is not the game's mana (Inscryption Bones, Blood or a Mox gem; mana there is Energy)"""
    r = c.execute('select cost_text from card where id=?', (t,)).fetchone()
    return bool(r and r[0] and any(w in r[0] for w in ('Bones', 'Blood', 'Mox')))


# what is an expensive card, per game (each game's import sets it; a game missing here gets no "pays for it" lines). First set
# to each game's top tenth of costs (30 Oct 2026); change one only in that game's chat, with Kaptain.
EXPENSIVE = {'runeterra': 6, 'stormbound': 6, 'monster_train': 3, 'duelyst': 6, 'faeria': 7, 'inscryption': 5, 'sts1': 2}


def boost_lines(c, game, nodes, stat_help=frozenset(), cost_help=frozenset()):
    """help that is no happening (HELPS): more power helps cards that need kills; Overwhelm, Elusive, another attack and units
    that have them help cards that need the enemy player hit; health and protection help cards that need to
    survive damage (damage as big as the card's health is no help). A level-up need makes it a level-up line."""
    cards = cards_of(c, game); out = Lines(); marks = ','.join('?' * len(nodes)); L = list(nodes); lvl = level_abilities(c)
    reach = Lines()  # the targets of each card's stat gains: "the Abomination gains their stats" reaches only it
    def reaches(a, t):
        return not reach.get(a) or any(matches(c, game, cards[t], k if k in KIND_CAT else 'unit', w) for k, w in reach[a])
    joins = {a for (a,) in c.execute(f"select card from ({JOINS}) where card in ({marks})", L)}
    def having(concepts, units_too):
        q = ','.join('?' * len(concepts))
        acting = {a for (a,) in c.execute(f"""select card from flat_do where origin in ('own','uses_keyword') and coalesce(on_side,'mine') in ('mine','any')
                and act not in ('create','summon','choose_card','keyword_action','copy','draw') and coalesce(on_pick,'') not in ('self','owner')
                and not (origin='uses_keyword' and exists (select 1 from flat_do k where k.card=flat_do.card and k.act='keyword_action' and k.keyword_ref=flat_do.via)
                and not exists (select 1 from flat_do k where k.card=flat_do.card and k.act='keyword_action' and k.keyword_ref=flat_do.via and coalesce(k.on_pick,'')!='self'))
                and not (coalesce(on_kind,'') = 'player' and act in ('heal','stat_change','grow',
                'negate_damage','damage_reduction','give_keyword','give_ability')) and card in ({marks})""", L)}  # on my
        # units: healing itself and my Nexus helps no other unit (Cosmic Youngling); Rally on the player does (another attack); making a
        # card is no help, the made card helps; a keyword it uses only on itself (Ornn level 2 forges himself) helps no other ()
        # (L3: Aurelion Sol makes Celestial cards, he does not help Braum); what a keyword the
        # card has does to others is the keyword's rule (L15: Scout readies Scouts: Greathorn Companion -> Greenfang Warden, no line)  # it acts on other cards of mine, not only on itself
        # a gain on the card it is sacrificed for (Mealworm: Morsel) reaches only that card: lines_of draws it, not every unit here
        stat = {'attack_gain': ('power', 'strength'), 'defence_gain': ('health', 'strength')}  # strength is both (Stormbound)
        want = {y for x in concepts if x in stat for y in stat[x]}; rest = tuple(x for x in concepts if x not in stat)
        def gains(act, ps):  # the stat it raises ("+2 Attack" raises no Health)
            p = dict(x.split('=', 1) for x in (ps or '').split(';') if '=' in x)
            return act in ('stat_change', 'grow') and any(k in p and raises(p[k]) for k in want)
        rows = [(a, own) for a, own, act, ps, con, k, w in c.execute(f"""select card, coalesce(on_pick,'') in ('self','owner','actor') or act='counter' or origin='has_keyword'
                or (origin='uses_keyword' and exists (select 1 from flat_do k where k.card=flat_do.card and k.act='keyword_action' and k.keyword_ref=flat_do.via)
                and not exists (select 1 from flat_do k where k.card=flat_do.card and k.act='keyword_action' and k.keyword_ref=flat_do.via and coalesce(k.on_pick,'')!='self'))
                or coalesce(on_side,'mine') not in
                ('mine','any') or (coalesce(on_kind,'') = 'player' and act in ('heal','stat_change','grow','negate_damage','damage_reduction',
                'give_keyword','give_ability')), act, params, concept, on_kind, on_with from flat_do where origin in ('own','uses_keyword','has_keyword') and card in ({marks})""", L)
                if ((con in rest or act in rest) or gains(act, ps)) and (want and gains(act, ps) and reach[a].append((k, w)) or True)
                and not (act == 'start_attack' and a in joins)]  # a unit summoned attacking joins the attack (Zed): no new attack
        other = {a for a, own in rows if not own}
        only_self = {a for a, own in rows if own} - other  # Juggernaut "Grow: +5/+5" makes only itself stronger
        got = other | (acting & {a for (a,) in c.execute(f"select card from flat_concept where concept in ({','.join('?' * len(rest)) or 'null'}) and card in ({marks})",
                list(rest) + L)}) - only_self  # a stat gain is read row by row (its stat); other concepts also by the card's concepts
        own_kw = {a for (a,) in c.execute(f"""select ck.card from card_keyword ck join card k on k.id=ck.keyword join vocab v on v.field='keyword'
                  and v.value in (k.name, k.game || ':' || k.name) where v.tree in ({q}) and ck.card in ({marks})""", list(concepts) + L)}
        got -= own_kw - other  # its own keyword (Young Witch is Elusive) is no help it gives; it counts only as a unit that has it
        if units_too: got |= own_kw  # a unit whose own keyword it is
        return got
    def count(concepts):  # cached: setdefault would run the query on every call
        if ('n', game, concepts) not in CACHE:
            CACHE[('n', game, concepts)] = max(1, len({a for (a,) in c.execute(
                f"select card from flat_concept where concept in ({','.join('?' * len(concepts))})", concepts) if a in cards}))
        return CACHE[('n', game, concepts)]
    needs = c.execute(f"""select card, ability, happening, side, role, pick, actor_kind, actor_with from flat_ref where role!='makes' and origin in
            ('own','uses_keyword','has_keyword') and card in ({marks})""", L).fetchall()
    by_enemy = {(a_, h_) for a_, h_ in c.execute(f"""select ability, event from flat_if where ev_actor_side='enemy' and card in ({marks})""", L)}
    needs = [n_ for n_ in needs if (n_[1], n_[2]) not in by_enemy]  # "if you were attacked last turn" (Defender of the Homeland): the
    # enemy does it, my cards help nothing (L9)
    w_need = {(t_, ab_): w_ for t_, ab_, w_ in c.execute(f"""select card, ability, obj_with from flat_ref where role!='makes' and coalesce(obj_with,'')!=''
              and card in ({marks})""", L)}  # a need that names whom it is about ("an Elite survives damage")
    # "the first time an ally attacks each round" (Hallowed): another attack in that round adds nothing
    once = {(a, ab) for a, ab in c.execute(f"select card, ability from flat_when where lim in ('first_each_round','once_per_round') and card in ({marks})", L)}
    # help given to my player reaches only my leader card (Duelyst: "your General gains +1 Attack"), help given to units only units
    aims = collections.defaultdict(set)
    leaders = any(cards[t]['cat'] == 'leader' for t in L if t in cards)  # only a game whose player is a card on the board
    for a, k in c.execute(f"""select card, coalesce(on_kind,'unit') from flat_do where origin in ('own','uses_keyword') and coalesce(on_side,'mine')
            in ('mine','any') and coalesce(on_pick,'') not in ('self') and act in ('stat_change','give_keyword','heal','move','swap','grow',
            'ready','can','give_ability','first_strike','double_strike','copy_keywords') and card in ({marks})""", L):
        aims[a] |= {'player', 'unit'} if k in ('any', 'anything') else {'player'} if k == 'player' else {'unit'} if k in ('unit', 'hero') else {'other'}  # "a minion or General"
    # help that names whom it lands on ("give a Dragon +2|+2", "your Rakoans get Flying", Lurk: Lurkers +1|+0) reaches only those cards
    ident = Lines()
    for a, w_, origin in c.execute(f"""select card, on_with, origin from flat_do where origin in ('own','uses_keyword','has_keyword') and coalesce(on_side,'mine') in ('mine','any')
            and coalesce(on_pick,'') not in ('self') and act in ('stat_change','give_keyword','heal','grow','copy_keywords','negate_damage')
            and card in ({marks})""", L):
        ident[a].append(';'.join(q_ for q_ in (w_ or '').split(';') if q_.split(' ')[:2] in (['card', 'is'], ['type', 'is'], ['type', 'in'],
                        ['name_has', 'is'], ['keyword', 'is'], ['region', 'is'], ['card', 'not'])))
    for a, w_ in c.execute(f"""select d.card, w.obj_with from flat_do d join flat_when w on w.ability=d.ability where d.on_pick='it' and
            d.origin='own' and d.act in ('stat_change','give_keyword','heal','grow') and w.obj_with like 'state is %' and d.card in ({marks})""", L):
        # "when an Ephemeral ally is summoned, give it +1|+1" (Soul Shepherd): it lands only on Ephemeral units ()
        ks = state_filter(c, game, w_)
        if ks: ident[a] = [w0 for w0 in ident[a] if w0] + [ks]
    def lands_on(a, t):
        return not ident.get(a) or any(not who or matches(c, game, cards[t], 'any', who) for who in ident[a])
    # help a card gives only through a keyword it has, to cards with the same keyword, is that keyword's rule (Lurk: every Lurker
    # grants Lurkers +1|+0), no combo (Kaptain 2 Nov 2026), unless the card's own text uses it (Xerxa'Reth: "If I have 8+ Power")
    kw_only = collections.defaultdict(set); other_help = set()
    for a, origin, via in c.execute(f"""select card, origin, via from flat_do where act in ('stat_change','give_keyword','heal','grow','negate_damage')
            and coalesce(on_side,'mine') in ('mine','any') and coalesce(on_pick,'') not in ('self') and card in ({marks})""", L):
        if origin == 'has_keyword' and via: kw_only[a].add(via)
        else: other_help.add(a)
    def aim_fits(a, t, kw_rule=False, given=True):  # kw_rule: a use by keywords only ("more power: it hits harder"), not by the card's
        # own text; given: the help is a stat or keyword given, which lands only where it names (Lurk: Lurkers), not a Rally
        if kw_rule and a not in other_help and kw_only.get(a, set()) & cards[t]['kws']: return False
        return (not given or lands_on(a, t)) and leader_fits(a, t)
    def leader_fits(a, t):
        if a not in aims or not leaders: return True
        return ('player' in aims[a]) if cards[t]['cat'] == 'leader' else 'unit' in aims[a] or aims[a] == {'other'}
    enemy_movers = {a for (a,) in c.execute(f"""select card from flat_do where origin in ('own','uses_keyword') and act in ('move','swap')
            and coalesce(on_side,'') in ('enemy','any','') and coalesce(on_pick,'') not in ('self') and card in ({marks})""", L)}  # no side: either (N18)
    self_kills = {(t, ab, h) for t, ab, h in c.execute(f"""select card, ability, happening from flat_ref where role='makes' and origin='own'
                  and happening in ('killed','dies') and card in ({marks})""", L)}  # kills its own ability makes
    for hs, sides, concepts, why in HELPS:
        helpers = having(concepts, hs[0] == 'nexus_damaged'); n = count(concepts)
        move_rows = {}
        if concepts == ('movement',):  # what moves another of my units, or gives it a movement keyword (row by row, not "has both somewhere")
            move_rows = Lines()
            for a, w_ in c.execute(f"""select d.card, d.on_with from flat_do d left join card k on k.id=d.keyword_ref left join vocab v on
                    v.field='keyword' and v.value in (k.name, k.game || ':' || k.name) where d.origin='own' and coalesce(d.on_pick,'') not in ('self')
                    and coalesce(d.on_side,'mine') in ('mine','any') and coalesce(d.on_kind,'unit') in ('unit','any') and (d.act in ('move','swap')
                    or (d.act='give_keyword' and v.tree='movement')) and d.ability not in (select ability from flat_do where act='transform')
                    and not (d.act in ('move','swap') and (coalesce(d.eff_zone,'') like 'deck%' or coalesce(d.eff_zone,'') like 'hand%'))
                    and d.card in ({marks})""", L): move_rows[a].append(w_)  # into the deck or hand is no move on the board (Sugary Snare); a transformed unit has lost its text (Frogify -> Oradrim Monk)
            helpers = set(move_rows)  # a card's own move keyword moves only itself: no help to others (Kaptain 3 Nov 2026)
            home_movers = {a for (a,) in c.execute(f"""select card from flat_do where origin='own' and act in ('move','swap') and to_side='mine'
                           and card in ({marks})""", L)}  # it moves units onto my own land (Desert Twister): never onto enemy land
        movers = helpers
        own_kw = helpers - having(concepts, False) if hs[0] == 'nexus_damaged' else set()
        own_reach = {a: 1 for (a,) in c.execute(f"""select ck.card from card_keyword ck join card k on k.id=ck.keyword join vocab v on
                     v.field='keyword' and v.value in (k.name, k.game || ':' || k.name) where v.tree in ('evasion','excess_damage')
                     and ck.card in ({marks})""", L)}  # Elusive, Overwhelm: past blockers; Scout's second attack is no reach (L4)  # helps by its own keyword only (Young
        # Witch is Elusive): it helps a need that it can be the doer of, not "Zed or allied Living Shadows strike the Nexus"
        for t, ab, h, side, role, pick, ak, aw in needs:
            if h not in hs or side not in sides: continue
            if role == 'condition' and h in ('killed', 'dies') and (t, ab, h) in self_kills: continue  # "gain 4 mana for each unit
            # destroyed" by its own damage (Spellbinder Zhevana): its own hit does the killing, more power on my units adds nothing
            if role == 'trigger' and (t, ab) in once and why == 'another attack': continue
            if h in ('killed', 'survives_damage') and pick != 'self' and not aw and not w_need.get((t, ab)) and why in ('helps my units kill',
                    'more health or protection: survives damage'): continue  # "if you've slain a unit" (Ruinous
            # Path): any unit can kill by the rules (L2); only a kill by itself or a named card is helped by more power
            if h == 'nexus_damaged' and side == 'mine': continue  # my own player losing health (Radiance: costs your Life) is no hit
            # on the enemy player: attacks and moves toward the enemy do not help it
            if concepts == ('movement',) and side == 'enemy' and h in ('moves', 'moves_onto'):  # "an enemy moves into the opposing space" (Sentry): what moves enemy
                helpers_t = enemy_movers  # units (Wiseclock turns the board), not my Sprinter moving itself (L9)
            else: helpers_t = helpers  # "whenever THIS moves onto": only what moves it;
            # "my units harvest enemy wells": every mobile unit would link (noise, Gabrian Archon -> Wavecrash Colossus)
            if concepts == ('movement',) and 'position enemy' in (w_need.get((t, ab)) or ''): helpers_t = helpers_t - home_movers
            if concepts == ('movement',):  # what it moves must be able to be this card ("give the Demon Wing Flying", "another Rakoan")
                fits = lambda ws: any(not who or matches(c, game, cards[t], 'any', who) for who in (';'.join(p for p in (w_ or '').split(';')
                       if p.split(' ')[:2] in (['card', 'is'], ['type', 'is'], ['type', 'in'], ['name_has', 'is'])) for w_ in ws))
                helpers_t = {a for a in helpers_t if a not in move_rows or fits(move_rows[a])}
            if role == 'trigger' and pick in ('self', 'actor_self') and h not in ('survives_damage', 'moves_onto', 'harvests') and \
                    not (concepts == ('movement',) and h == 'strikes_nexus'): continue  # getting there is help; a fight effect goes off in
                    # any fight it has anyway: moving it adds none (Kaptain 3 Nov 2026: Windborne Champion -> King's Guard; L2, L4)  # "Strike:" fires on any strike: more of it adds nothing
            if h in ('strikes', 'killed') and role == 'trigger': continue  # only counted strikes and kills grow with more power
            lv = ab in lvl
            if why.endswith('*') and not lv: continue
            for a in helpers_t - {t}:
                if a in own_kw and not (lv and own_reach.get(a) and not (aw and not matches(c, game, cards[a], ak if ak in KIND_CAT else 'any', aw))): continue  # a reach keyword works only for the card that has it (L20: Abyssal Eye -> Dashing
                # Dandy: no line); it does reach the Nexus for a champion's level-up (L2, Kaptain's n12: Amateur Aeronaut -> Darius)
                if not (aim_fits(a, t, given=bool(set(concepts) & set(GIVEN))) if pick == 'self' else leader_fits(a, t)): continue  # help on itself must land on it
                # who must do it ("Zed or allied Living Shadows strike the Nexus"): the help must land on such a card
                if aw and pick != 'self' and not can_aim_at(c, game, a, ak if ak in KIND_CAT else 'any', aw): continue
                out[(a, t)].append(('levels' if lv else 'moves' if concepts == ('movement',) else 'waits' if role == 'trigger' else 'type', (1.0 if lv else 0.5) / n,
                                    why.rstrip('*') + (' (levels it up)' if lv else '')))  # it makes what the card waits for happen more
    # how many cards are in my hand ("played as the last card from your hand", "10+ cards in hand", "for each card in hand")
    hand = lambda acts, zone, kw='': {a for (a,) in c.execute(f"""select card from flat_do where act in ({','.join('?' * len(acts))}) and origin in
            ('own','uses_keyword',?) and coalesce(on_side,'mine')='mine' and (coalesce(on_zone,'')='hand' or coalesce(eff_zone,'')='hand' or ?)
            and card in ({marks})""", list(acts) + [kw, zone] + L)}  # kw: a keyword it has that adds to the hand (Fecundity's copy)
    for t, ab, op, n_, ok_, ow_ in c.execute(f"""select card, ability, op, n, of_kind, of_with from flat_if where of_zone='hand' and coalesce(of_side,'mine')='mine'
            and test in ('count','amount_count','have') and coalesce(of_pick,'') not in ('self','chosen') and card in ({marks})""", L).fetchall():
        # not the card itself in hand (Ethereal: "if this is still in your hand"), nor what it picks there itself (Gambling Chip)
        if op == 'not' and 'card is ' in (ow_ or ''): continue  # "if you don't have Pokey Stick": one missing card, not an empty hand ()
        few = (op in ('eq', 'le', 'lt') and (n_ or 0) <= 1) or op == 'not' or ok_ == 'position'  # "no cards in hand" (have not, N22);
        # "for each empty card space in your hand" (Clap of Thunder): it wants an empty hand
        dos = c.execute("select act, params, coalesce(on_side,'mine') from flat_do where card=? and ability=? and origin='own'", (t, ab)).fetchall()
        if any(a_ == 'draw' and 'amount=sum' in (p_ or '') for a_, p_, _ in dos): few = True  # "draw until you have 6" (Expertise,
        # Scrawl): the fewer cards in hand, the more it draws
        if any(a_ in ('damage', 'lose_life') and s_ == 'mine' for a_, p_, s_ in dos): continue  # "lose 1 HP per card in hand" (Regret):
        # a full hand hurts it, it wants none
        refill = {a for (a,) in c.execute("""select d.card from flat_do d join flat_do x on x.card=d.card and x.ability=d.ability where
                  d.act='discard' and x.act in ('draw','create')""")}  # Rummage discards 2 and draws 2: the hand is never empty (L4)
        helpers = (hand(('discard',), 0) - refill) if few else hand(('create', 'copy', 'return_to_hand'), 0, 'has_keyword') | hand(('draw',), 1)  # a draw goes to hand
        named = [p_ for p_ in (ow_ or '').split(';') if p_.split(' ')[:2] in (['type', 'is'], ['card', 'is'], ['name_has', 'is']) or p_.startswith('cost ')]
        # "cards that cost 8+ in hand" (Trundle level 2): a draw of the top card brings none (L1b)
        if named and not few:  # "for each Pirate in your hand" (Lucky Charmers): only what brings such cards fills it
            helpers = {a for a in helpers if any(all(p_ in (w_ or '') for p_ in named) for (w_,) in c.execute(
                       "select on_with from flat_do where card=? and act in ('draw','create','copy','return_to_hand')", (a,)))}
        for a in helpers - {t}:
            out[(a, t)].append(('levels' if ab in lvl else 'boosts', 0.3, ('empties your hand' if few else 'fills your hand') + (' (levels it up)' if ab in lvl else '')))
    # a stat it tests ("an ally with 5+ Power"): more of that stat
    power = having(('attack_gain',), False)
    unreached = lambda ab, ok: ok == 'player' or c.execute("select 1 from flat_do where ability=? and on_zone='deck' and act!='draw'", (ab,)).fetchone()
    # the General's stat (Drogon) or the stats of units still in the deck (The Tuskraider) are not raised by help to my units ()
    for t, ab, fp, ok, os_, ow_ in c.execute(f"""select card, ability, of_pick, of_kind, of_side, of_with from flat_if where test in ('stat','amount_stat') and attr='power' and card in ({marks}) and not exists (select 1 from flat_do d where d.ability=flat_if.ability and flat_if.of_pick='it' and d.on_pick in ('chosen','random')
            and coalesce(d.on_side,'any')!='mine' and d.act in ('kill','damage','obliterate','sacrifice','return_to_hand','transform','silence'))""", L).fetchall():
        if unreached(ab, ok) or (fp == 'self' and on_play(c, ab)): continue  # its power when it is played: a boost on the board comes
        # too late (Rising Spell Force -> Banana Blaster)
        if os_ == 'enemy': continue  # the power of an enemy it reads (Fin Fang Foom): help to my own units never raises it (L9)
        named_ = [p_ for p_ in (ow_ or '').split(';') if p_.startswith('card is ')]
        for a in power - {t}:
            # it reads the power of one named card (Zombie Giant-Man: Zombie Hulk): only a power gain aimed at that card feeds it
            if named_ and not all(c.execute("select 1 from flat_do where card=? and act='stat_change' and on_with like ?", (a, '%' + p_ + '%')).fetchone() for p_ in named_): continue
            if aim_fits(a, t) and (fp != 'self' or reaches(a, t)) and (a, t) not in stat_help: out[(a, t)].append(('levels' if ab in lvl else 'boosts', 0.5 / count(('attack_gain',)), 'more power' + (' (levels it up)' if ab in lvl else '')))
    # a stat it tests high or uses as an amount ("a creature with 5+ Life", "faeria equal to its Life"): more of that stat
    health = having(('defence_gain',), False)
    for t, ab, fp, ok in c.execute(f"""select card, ability, of_pick, of_kind from flat_if where attr in ('health', 'total_stats') and (test='amount_stat' or
            (test='stat' and coalesce(op,'') in ('ge','gt'))) and coalesce(of_side,'mine')!='enemy' and card in ({marks}) and not exists
            (select 1 from flat_if x where x.card=flat_if.card and x.ability=flat_if.ability and x.test='amount') and not exists (select 1 from flat_do d where d.ability=flat_if.ability and flat_if.of_pick='it' and d.on_pick in ('chosen','random')
            and coalesce(d.on_side,'any')!='mine' and d.act in ('kill','damage','obliterate','sacrifice','return_to_hand','transform','silence'))""", L).fetchall():  # a threshold wants nothing;
        # a stat of what the player picks on either side is the biggest there is (Martyrdom)
        if unreached(ab, ok): continue
        for a in health - {t}:
            if aim_fits(a, t) and (fp != 'self' or reaches(a, t)) and (a, t) not in stat_help:  # its own stat: the gain must reach it
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
        u_ = generic_use(c, game)[t]
        if not (u_['trees'] & set(POWER_USE) or u_['flags'] & {'big_strike', 'fights', 'level_hit'} or t in gains_back(c, game)): continue  # L18: its own text must
        # read the damage it deals (Kaptain 2 Nov 2026)
        for a in power - {t}:
            if not aim_fits(a, t, True) or not reaches(a, t) or (a, t) in stat_help: continue
            if not any(k in ('boosts', 'levels') for k, *_ in out[(a, t)]): out[(a, t)].append(('boosts', 0.25 / count(('attack_gain',)), 'more power: its text uses the damage it deals'))
    q = lambda sql, *a: {x for (x,) in c.execute(sql.format(marks=marks), list(a) + L * sql.count('{marks}'))}
    movers_mine = q("""select card from flat_do where origin='own' and act in ('move','swap') and coalesce(on_side,'mine') in ('mine','any')
            and coalesce(on_kind,'unit') in ('unit','any') and coalesce(on_pick,'') not in ('self') and card in ({marks})""")
    # paying for big cards: more mana, or a cost cut on my cards, helps the game's expensive cards (EXPENSIVE, set per game:
    # Faeria 7+) when it pays at least a third of the card's cost (Red Devil's 5 faeria for Krog's 12; 2 faeria in a fight
    # does not pay for anything), and only the cards the cut names ("Your Krog costs 7 less": Krog only)
    high = EXPENSIVE.get(game)
    if high:
        pays = Lines()
        for a, act, ps, w_, res in c.execute(f"""select card, act, params, on_with, coalesce(on_kind, 'mana') from flat_do where origin='own' and ((act in ('mana_gain','max_mana_change')
                and coalesce(on_side,'mine')='mine') or (act in ('cost_change','cost_set') and coalesce(on_side,'mine') in ('mine','any')
                and coalesce(on_pick,'') not in ('self','it'))) and card in ({marks})""", L):
            p = dict(x.split('=', 1) for x in (ps or '').split(';') if '=' in x)
            x = p.get('amount' if act in ('mana_gain', 'max_mana_change') else 'cost', '')
            n_ = float(x.lstrip('-')) if act != 'cost_set' and x.lstrip('-').replace('.', '', 1).isdigit() else None
            if act == 'mana_gain' and x == 'full': n_ = 99.0  # "refill your mana" / "replenishes Energy up to the maximum" (Extra Battery) pays any card
            if act == 'cost_change' and not x.startswith('-'): continue  # a cost raised pays nothing
            if act == 'cost_set' and re.search(r'cost (lt|le) ', w_ or ''): continue  # "spells under 3 cost 3" (Mageseeker Junior) raises costs
            if act in ('mana_gain', 'max_mana_change') and res in ('secondary_resource', 'gem', 'lane_resource'): continue  # Bones, a Mox gem: the resource lines say
            # it, for the cards paid in that resource (Hoggy Bank's 4 Bones pay no Energy card: Gembound Ripper)
            if act in ('mana_gain', 'max_mana_change') and res == 'spell_mana': w_ = ';'.join(x_ for x_ in (w_, 'category is spell') if x_)
            if act in ('mana_gain', 'max_mana_change'): w_ = ';'.join(x_ for x_ in (w_, 'paid in mana') if x_)
            who = ';'.join(q_ for q_ in (w_ or '').split(';') if q_.split(' ')[:2] in (['card', 'is'], ['type', 'is'], ['type', 'in'],
                           ['name_has', 'is'], ['keyword', 'is'], ['region', 'is'], ['category', 'is']))
            pays[a].append((act, n_, who, 'paid in mana' in (w_ or '')))
        # an Orb the card puts in play that gives energy (Plasma: Meteor Strike channels 3): it pays like energy the card gives
        for a, k, ps, pps in c.execute(f"""select distinct p.card, d.card, d.params, p.params from flat_do p join flat_do d on d.origin='own' and d.act='mana_gain'
                and (';' || coalesce(p.on_with,'') || ';') like '%;keyword is ' || d.card || ';%' join card kk on kk.id=d.card and kk.is_keyword=1
                where p.act='keyword_action' and p.origin='own' and p.card in ({marks})""", L):
            num = lambda t: (lambda x: float(x) if x.replace('.', '', 1).isdigit() else None)(dict(q_.split('=', 1) for q_ in (t or '').split(';') if '=' in q_).get('amount', ''))
            each, orbs = num(ps), num(pps) or 1.0
            pays[a].append(('mana_gain', (each or 1.0) * orbs, '', True))  # an Orb's unstated energy counts as at least 1, once per Orb put in
        # a status the card gives me that sets my drawn cards' costs (Confused, Snecko Eye: a random cost 0-3): it pays for big cards
        for a, via in c.execute(f"""select distinct d.card, d.via from flat_do d where d.origin='uses_keyword' and d.act='cost_set'
                and coalesce(d.on_side,'mine')='mine' and d.card in ({marks})""", L):
            if c.execute("select 1 from flat_do where card=? and act='give_keyword' and keyword_ref=? and origin='own' and coalesce(on_side,'mine')='mine'",
                         (a, via)).fetchone(): pays[a].append(('cost_set', None, '', False))
        for t in nodes:
            cost = cards.get(t, {}).get('cost') or 0
            if t in cards and cards[t]['x_cost']:  # "X times" (Conjure Blade, Whirlwind): every energy gained makes X bigger
                for a, rs in pays.items():
                    if a != t and any(act in ('mana_gain', 'max_mana_change') for act, *_ in rs):
                        out[(a, t)].append(('boosts', 0.5 / max(1, len(pays)), 'more energy: a bigger X'))
                continue
            if t not in cards or cost < high: continue
            for a, rs in pays.items():
                if a == t: continue
                if any((n_ is None and act == 'cost_set') or (n_ is not None and n_ * 3 >= cost) for act, n_, who, mana in rs
                       if (not who or matches(c, game, cards[t], 'any', who)) and not (mana and other_resource(c, t))):
                    if (a, t) not in cost_help: out[(a, t)].append(('boosts', 0.5 / max(1, len(pays)), 'pays for it: more mana or a lower cost'))  # a
                    # cut aimed at it already says so
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
        land_movers = q("""select card from flat_do where origin='own' and act='move' and on_kind='position' and card in ({marks})""")  # moves land
        givers = q("""select d.card from flat_do d join card k on k.id=d.keyword_ref join vocab v on v.field='keyword' and v.value in
                (k.name, k.game || ':' || k.name) where d.origin='own' and d.act='give_keyword' and v.tree='movement' and
                coalesce(d.on_side,'mine') in ('mine','any') and coalesce(d.on_pick,'') not in ('self','it') and d.card in ({marks})""")  # not a
        # token's own keyword ("summon a Manta with Flying")
        # a unit's own move keyword moves only itself, making land moves no unit, and a move to my own land reaches no
        # enemy ground (Kaptain 3 Nov 2026: Ghost Dragon -> Lost Explorer, Wood Elemental, Desert Twister: no line)
        to_mine = q("""select card from flat_do where origin='own' and act in ('move','swap') and to_side='mine' and card in ({marks})""")
        growers = (movers_mine - to_mine) | land_movers | givers  # Syland Horsemaster gives Charge
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
    # a keyword of mine that is not removed any more (Barricade: Block is not removed at turn start): it piles up for the cards
    # that count it (Body Slam deals damage equal to your Block, Entrench doubles it)
    for a, w_ in c.execute(f"""select card, on_with from flat_do where origin='own' and act='cant' and param_event='keyword_removed'
            and coalesce(on_side,'mine')='mine' and on_with like 'keyword is %' and card in ({marks})""", L).fetchall():
        k = w_.split(';')[0].split(' ')[2]
        users = {t for (t,) in c.execute(f"""select distinct card from flat_if where origin='own' and test in ('amount_count','count','have')
                 and coalesce(of_side,'mine')='mine' and coalesce(of_pick,'') not in ('self','chosen') and (';' || of_with || ';') like ?
                 and card in ({marks})""", [f'%;keyword is {k};%'] + L)} - {a}
        for t in users: out[(a, t)].append(('boosts', 0.5 / len(users), f'keeps your {mechanics.name(c, int(k))}: it counts more of it'))
        givers = {m for (m,) in c.execute(f"""select distinct card from flat_ref where role='makes' and happening='given_keyword' and keyword=?
                  and origin='own' and side='mine' and coalesce(pick,'') not in ('self','it') and card in ({marks})""", [int(k)] + L)} - {a} - users
        for m in givers: out[(a, m)].append(('boosts', 0.5 / len(givers), f'keeps the {mechanics.name(c, int(k))} it gives'))
    # more room for what my cards put in a slot (Capacitor: 2 more Orb slots): the cards that put Orbs in keep more of them
    roomy = {a for (a,) in c.execute(f"""select distinct card from flat_do where origin='own' and act='capacity_change' and on_kind='slot'
             and coalesce(on_side,'mine')='mine' and card in ({marks})""", L)}
    if roomy:
        slot_kws = {k for (k,) in c.execute("select distinct d.card from flat_do d join card k on k.id=d.card where k.is_keyword=1 and k.game=? "
                    "and d.act='move' and d.to_kind='slot'", (game,))} | {int(x) for (w,) in c.execute("""select on_with from flat_do where
                    act='move' and on_kind='keyword' and origin='uses_keyword'""") for x in __import__('re').findall(r'keyword is (\d+)', w or '')}
        fillers = set().union(*[givers_of(c, game, k, L) for k in slot_kws]) if slot_kws else set()
        for a in roomy:
            for t in fillers - {a}: out[(a, t)].append(('boosts', 0.5 / len(fillers), 'more slots: it keeps more of what it puts in'))
    # what strips the enemy's Block (Melter) helps the cards that want damage to get through it (Envenom, The Boot: "unblocked")
    strip = {a for (a,) in c.execute(f"""select distinct d.card from flat_do d join card k on k.id=d.keyword_ref where d.origin='own'
             and d.act='remove_keyword' and d.on_side='enemy' and d.card in ({marks}) and exists (select 1 from flat_do g where
             g.card=d.keyword_ref and g.act='negate_damage')""", L)}  # the keyword it strips is one that stops damage (Block)
    wants = {t for (t,) in c.execute(f"""select distinct card from flat_when where event='damaged' and coalesce(obj_side,'enemy')='enemy'
             and obj_with like '%state is unblocked%' and card in ({marks})""", L)} | {t for (t,) in c.execute(f"""select distinct card
             from flat_do where origin='own' and act='damage' and on_side='enemy' and card in ({marks})""", L)}  # and every card of mine
             # that deals damage: with the Block gone it hits in full (Kaptain 30 Oct 2026, Melter)
    for a in strip:
        for t in wants - {a}: out[(a, t)].append(('boosts', 0.5 / len(wants), 'removes their Block: its damage gets through'))
    # a status that makes damage bigger (Vulnerable on an enemy: it takes more; Wrath on me: I deal more): the cards that give it
    # make every card of mine that deals damage stronger
    orbs = {k for (k,) in c.execute("""select distinct d.card from flat_do d join card k on k.id=d.card where k.is_keyword=1 and k.game=?
            and d.origin='own' and d.act='damage' and coalesce(d.on_side,'enemy')='enemy' and exists (select 1 from flat_do p where
            p.act='keyword_action' and p.origin='own' and (';' || coalesce(p.on_with,'') || ';') like '%;keyword is ' || d.card || ';%')""",
            (game,))}  # keywords put in play by an action that deal damage (Channel: Lightning, Dark), not statuses (Poison)
    for a, kname, by_kw in status_damage_givers(c, game, L):
        hitters = set().union(*[givers_of(c, game, o, L) for o in orbs]) - {a} if by_kw else {m for (m,) in c.execute(f"""select distinct
                   card from flat_do where origin='own' and act='damage' and (on_side='enemy'
                   or (on_side is null and on_pick in ('chosen','nearest','random','all'))) and card in ({marks}) and ability not in (select ability
                   from flat_if where test='it_matches' and of_with like '%origin %' and of_with not like '%origin is weapon%')""", L)} - {a}
        # aimed at enemies; damage only from bumps (Force Amp) is no weapon damage
        if not by_kw: hitters &= gains_back(c, game)  # Vulnerable or Wrath makes
        # every damage card hit harder: any card can be the one (L14; Kaptain 2 Nov 2026); kept for a card that gets something back
        # from its damage (Reaper heals by it; Kaptain 30 Oct 2026: Bag of Marbles -> Reaper); one that reads the status (Brilliance:
        # Mantra) has its own line
        for m in hitters: out[(a, m)].append(('boosts', 0.5 / len(hitters), f'gives {kname}: its damage is bigger'))
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


def keyword_adders(c, game):
    """abilities that add to a keyword my cards just gave ("whenever you apply Poison, apply 1 more", Snecko Skull; Dexterity:
    "Block gained from cards is bigger", through a status the card gives my side): (card, ability, keyword, side, kind). They
    make the cards that give it stronger and wait for nothing themselves."""
    if ('kwadders', game) in CACHE: return CACHE[('kwadders', game)]
    cards = cards_of(c, game); out = []
    mine_status = {(a, k) for a, k, ps in c.execute("""select card, keyword_ref, params from flat_do where act='give_keyword' and origin='own'
                   and coalesce(on_side,'mine')='mine' and keyword_ref is not null""") if '=-' not in (ps or '')}
    for a, origin, via, ab, ok, os_, w, ak in c.execute("""select distinct card, origin, via, ability, obj_kind, coalesce(obj_side,'mine'), obj_with, actor_kind
            from flat_when where event='given_keyword' and origin in ('own','gives','uses_keyword') and obj_with like 'keyword is %'
            and coalesce(actor_side,'mine')='mine'""").fetchall():
        if a not in cards or (origin == 'uses_keyword' and (a, via) not in mine_status): continue
        k = next((int(p.split(' ')[2]) for p in w.split(';') if p.startswith('keyword is ') and p.split(' ')[2].isdigit()), None)
        dos = c.execute('select act, params, on_pick, keyword_ref from flat_do where card=? and ability=? and origin=?', (a, ab, origin)).fetchall()
        if k and dos and all(pk == 'it' and (boosts_it(act, ps) or (act == 'give_keyword' and kw == k and '=-' not in (ps or '')))
                             for act, ps, pk, kw in dos):
            out.append((a, ab, k, os_, ok, ak))
    CACHE[('kwadders', game)] = out
    return out


def adder_abilities(c, game):
    return {ab for _, ab, *_ in adders(c, game)} | {ab for _, ab, *_ in keyword_adders(c, game)}


def object_help_lines(c, game, nodes, broad):
    """an ability that acts when my cards of a kind are played, summoned, drawn or created, and helps that card ("When you
    summon an Elite, grant it +1|+1", Battlesmith; "the next card with Nightfall you play costs 1 less", Duskpetal Dust):
    it makes every card of that kind in the deck stronger. broad=False keeps only kinds narrowed past "any unit" or "any card"."""
    cards = cards_of(c, game); out = Lines(); marks = ','.join('?' * len(nodes)); L = list(nodes)
    for a, origin, ab, kind, w in c.execute(f"""select distinct card, origin, ability, obj_kind, obj_with from flat_when where origin in ('own','gives')
            and event in ('played','summoned','drawn','created') and coalesce(obj_side, actor_side, 'mine')='mine' and coalesce(obj_pick,'') not in ('self')
            and card in ({marks})""", L).fetchall():
        # a state that is a keyword ("an Ephemeral ally") is had on arrival only by cards that print it: Zed is no Ephemeral
        # ally, his Living Shadow is (Moonlit Glenkeeper buffs the Shadow, never Zed)
        arrive_kws = [k for k in (state_kw(c, game, p[9:]) for p in (w or '').split(';') if p.startswith('state is ')) if k]
        bt = lambda p: (p.startswith('type ') and broad_part(c, game, p)) or p.startswith('of:')  # "your next Skill" (Burst): half the
        # cards are Skills; "summoned near your General" (Call to Arms): what the place is measured from narrows no card
        narrowed = bool(arrive_kws) or any(p and p.split(' ')[0] not in PLAY_STATE and p.split(' ')[1:2] != ['not'] and not bt(p) for p in (w or '').split(';'))
        if not narrowed and not broad: continue  # Echo Form repeats any card: only the cards that use it (below) get a line
        whys = []
        for act, kw, ps in c.execute("select act, keyword_ref, params from flat_do where card=? and ability=? and origin=? and on_pick='it'", (a, ab, origin)):
            if act in ('stat_change', 'grow') and '=-' not in (ps or ''): whys.append((stats_said(ps), act, kw, ps))
            elif act == 'cost_change' and '=-' in (ps or ''): whys.append(('makes it cheaper', act, kw, ps))
            elif act == 'give_keyword' and kw and buff_keyword(c, kw): whys.append((f'gives it {mechanics.name(c, kw)}', act, kw, ps))
            elif act == 'heal': whys.append(('heals it', act, kw, ps))
            elif act == 'repeat' and boosts_it(act, ps): whys.append(('plays it again', act, kw, ps))
            elif act == 'increase_effect' and boosts_it(act, ps): whys.append(('makes its effect bigger', act, kw, ps))
        if not whys: continue
        sharp = bool(arrive_kws) or any(p and p.split(' ')[0] not in PLAY_STATE + ('region', 'category') and p.split(' ')[1:2] != ['not']
                                        and not bt(p) for p in (w or '').split(';'))  # "a Demacia ally": any ally of the deck
        k = 'any' if kind in (None, 'card', 'any', 'anything') else kind
        hits = [b for b in L if b != a and b in cards and matches(c, game, cards[b], k, w) and all(x in cards[b]['kws'] for x in arrive_kws)]
        for b in hits:
            loose = lambda act: sharp and (act not in ('stat_change', 'grow') or 'type ' in (w or ''))  # stats to "an Elite" or "a Flying unit" go only to a unit
            # whose own text uses them (L14, L18: Drakkar Skycaptain's Flying units -> Airbot: no line); a tribe is a deck choice (ndu34)
            ws = [y if loose(act) else use_of(c, game, b, act, kw, ps) for y, act, kw, ps in whys if loose(act) or uses_help(c, game, b, act, kw, ps)]  # "when
            # you summon an ally, grant it +1|+1": only the units that use it (Kaptain 1 Nov 2026)
            if not ws: continue
            when = '' if all(y.startswith(('plays it again', 'makes its effect bigger', 'hits several', 'its damage is bigger')) for y in ws) else ' when it comes'  # it is played: it comes
            out[(a, b)].append(('boosts', 0.5 / max(1, len(hits)), ', '.join(dict.fromkeys(ws)) + when))
    return out


def state_giver_lines(c, game, nodes):
    """a card that gives my units a keyword another card's need asks for ("You've attacked with 7+ Ephemeral allies": Mark of
    the Isles grants an ally Ephemeral, so it feeds Hecarim's level-up)"""
    cards = cards_of(c, game); out = Lines(); marks = ','.join('?' * len(nodes)); L = list(nodes); lvl = level_abilities(c)
    gives = collections.defaultdict(set)
    for a, k in c.execute(f"""select card, keyword_ref from flat_do where act='give_keyword' and origin='own' and coalesce(on_side,'mine')
            in ('mine','any') and coalesce(on_pick,'') not in ('self','owner') and (coalesce(on_kind,'unit') in ('unit','any','anything')
            or (on_kind='card' and on_pick='it')) and card in ({marks})""", L): gives[k].add(a)  # "copy it, it is Ephemeral" (Stalking
            # Shadows): the follower it draws
    for t, ab, role, aw, ow in c.execute(f"""select card, ability, role, actor_with, obj_with from flat_ref where role in ('condition','trigger')
            and origin='own' and coalesce(side,'mine') in ('mine','any','') and card in ({marks})""", L).fetchall():
        for k in set(kw_states(c, game, aw)) | set(kw_states(c, game, ow)):
            for a in gives.get(k, set()) - {t}:
                if a not in cards: continue
                lv = ab in lvl; say = f'makes your units {mechanics.name(c, k)}' + (' (levels it up)' if lv else '')
                if not any(l[2] == say for l in out[(a, t)]):
                    out[(a, t)].append(('levels' if lv else 'waits' if role == 'trigger' else 'type', 0.5 / len(gives[k]), say))
    return out


def actor_help_lines(c, game, nodes):
    """an ability on what happens to the card itself that acts on the event's actor (Worthy Sacrifice: when it is sacrificed,
    the card it pays for costs 2 less; Morsel: that card gets its stats): it helps every card of the deck that needs that
    happening (the Blood cards that need sacrifices)"""
    cards = cards_of(c, game); out = Lines(); marks = ','.join('?' * len(nodes)); L = list(nodes)
    for a, act, ps, ev in c.execute(f"""select distinct d.card, d.act, d.params, w.event from flat_do d join flat_when w on w.card=d.card
            and w.ability=d.ability where d.on_pick='actor' and w.obj_pick='self' and d.origin in ('own','has_keyword')
            and d.act in ('cost_change','stat_change','give_keyword') and d.card in ({marks})""", L).fetchall():
        takers = {t for (t,) in c.execute(f"""select distinct card from flat_ref where role in ('condition','trigger') and happening=?
                  and coalesce(side,'') in ('mine','any','') and coalesce(pick,'') not in ('self','actor_self') and card in ({marks})""", [ev] + L)} - {a}
        why = 'makes it cheaper' if act == 'cost_change' and '=-' in (ps or '') else ('help ' + stats_said(ps))[5:] if act == 'stat_change' else 'gives it a keyword'
        for t in takers:
            if t in cards: out[(a, t)].append(('boosts', 1.0 / len(takers), why + f' (when it is {ev.replace("_", " ")} for it)'))
    # a card that is sacrificed and does not die (Many Lives: Cat) pays the Blood of every card that needs sacrifices, again and
    # again (Kaptain 31 Oct 2026: Cat -> Urayuli)
    for (a,) in c.execute(f"""select distinct d.card from flat_do d join flat_when w on w.card=d.card and w.ability=d.ability where
            d.act='cant' and d.on_pick='self' and d.params like '%event=dies%' and w.event='sacrificed' and w.obj_pick='self'
            and d.origin in ('own','has_keyword') and d.card in ({marks})""", L).fetchall():
        takers = {t for (t,) in c.execute(f"""select distinct card from flat_ref where role='condition' and happening='sacrificed'
                  and coalesce(side,'') in ('mine','any','') and coalesce(pick,'') not in ('self','actor_self') and card in ({marks})""", L)} - {a}
        for t in takers:
            if t in cards: out[(a, t)].append(('boosts', 1.0 / len(takers), 'pays for it again and again: it is sacrificed and does not die'))
    return out


def gives_lines(c, game, nodes):
    """abilities that act when my cards of a kind do something (the card's own or given to my side). When they add to what
    happened (adders) the card makes every card of that kind in the deck that does it stronger (Tybaulk -> every spell and
    Skill that deals damage, also through a keyword it uses: Drain); otherwise the cards that make that happening feed a
    given ability ("when you summon an ally, grant its keywords": Zoe level 2)"""
    cards = cards_of(c, game); out = Lines(); marks = ','.join('?' * len(nodes)); L = list(nodes)
    doers = lambda h: {m for (m,) in c.execute(f"""select distinct card from flat_ref where role='makes' and happening=? and
            origin in ('own','uses_keyword') and coalesce(pick,'') not in ('self','it') and coalesce(side,'')!='mine' and card in ({marks})""", [h] + L)}
    # damage to my own cards is a drawback: more of it helps nothing (L5: The Dreadway -> Darkwater Scourge, no line)
    found = adders(c, game); n = collections.Counter(h for _, _, h, *_ in found)
    for a, ab, h, kind, w, (act, ps) in found:
        if a not in nodes: continue
        amount = dict(p.split('=', 1) for p in (ps or '').split(';') if '=' in p).get('amount', '').removesuffix('.0')
        why = (f'doubles its {act.replace("_", " ")}' if amount == 'event_amount' else
               f'its {act.replace("_", " ")} gets {amount} more' if amount else f'adds to its {act.replace("_", " ")}')
        units = {b for b in L if b in cards and cards[b]['cat'] in KIND_CAT['unit'] and uses_help(c, game, b, 'stat_change', None, 'power=1')} \
            if kind == 'unit' and h in ('damaged', 'strikes') else set()  # every unit deals damage when it strikes: only units that use
        # more damage (Overwhelm, Elusive; Kaptain 1 Nov 2026), like more power
        for m in doers(h) | units:
            if m != a and m in cards and matches(c, game, cards[m], kind, w): out[(a, m)].append(('boosts', 1.0 / n[h], why))
    for a, ab, k, side, kind, ak in keyword_adders(c, game):  # Snecko Skull -> the cards that apply Poison; Footwork -> the Block cards
        if a not in nodes: continue
        gs = {m for (m,) in c.execute(f"""select distinct card from flat_ref where role='makes' and happening='given_keyword' and keyword=?
              and origin='own' and side=? and coalesce(kind,'')=coalesce(?, kind, '') and coalesce(pick,'') not in ('self','it') and card in ({marks})""",
              [k, side, kind] + L)} - {a}
        if ak in KIND_CAT and ak != 'player':  # "Block gained from cards": a card gives it when played, a fixed amount (not a Power's later Block:
            # After Image, Metallicize; not Entrench's doubling: wiki Dexterity, 30 Oct 2026)
            gs = {m for (m,) in c.execute(f"""select distinct d.card from flat_do d join flat_when w on w.card=d.card and w.ability=d.ability
                  where d.origin='own' and d.act='give_keyword' and d.keyword_ref=? and w.event='played' and w.obj_pick='self'
                  and d.params glob 'amount=[0-9]*' and d.card in ({marks})""", [k] + L)} & gs
            gs = {m for m in gs if m in cards and matches(c, game, cards[m], ak, None)}
        gs = {m for m in gs if c.execute("select 1 from flat_do where card=? and act='give_keyword' and keyword_ref=? and params like '%times=%'",
                                          (m, k)).fetchone()}  # each card that gives Block or Poison gets the same +1: only one that
        # gives it several times in one go gets more from it (Kaptain 2 Nov 2026)
        for m in gs: out[(a, m)].append(('boosts', 1.0 / len(gs), f'makes the {mechanics.name(c, k)} it gives bigger'))
    skip = adder_abilities(c, game)
    named_to = collections.defaultdict(list)
    for a, w_ in c.execute(f"select card, on_with from flat_do where act='give_ability' and origin='own' and on_with like '%card is %' and card in ({marks})", L):
        named_to[a].append(';'.join(p for p in w_.split(';') if p.startswith('card is ')))
    for a, h, ab, akind in c.execute(f"""select distinct card, event, ability, actor_kind from flat_when where origin='gives'
            and coalesce(actor_side,'mine')='mine' and coalesce(obj_pick,'')!='self' and card in ({marks})""", L).fetchall():  # "when this
        # is built" (Manakite Drifter) is about the card itself: Eternity Painter's transform of enemies gives it nothing
        if ab in skip: continue
        say = act_say(c, h, '', None); w = actor_of(c, ab)[3]
        ks = [k for (k,) in c.execute("select ref_keyword from cond where ability=? and test='keyword_condition' and ref_keyword is not null", (ab,))] if h == 'stat_changed' else []
        for m in doers(h):
            if m == a or m not in cards or (akind in KIND_CAT and not matches(c, game, cards[m], akind, w)): continue
            if ks and not any(k in cards[m]['kws'] or m in givers_of(c, game, k, L) for k in ks): continue  # only Power from Hallowed ()
            if named_to.get(a) and not any(matches(c, game, cards[m], 'any', w_) for w_ in named_to[a]): continue  # the ability goes to the
            # cards it names (Twisted Catalyzer: Darkness); only they set it off, not every card that deals damage ()
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
        for (w,) in c.execute(f"select on_with from flat_do where act in ('create','summon','keyword_action') and card_ref is null and card in ({marks}) "
                              "and (on_with like '%card in %' or on_with like '%card is %')", q):  # a new card, one of a set by name
            add |= {int(x) for x in re.findall(r'card (?:in|is) (\d+)', w)}  # (Thanos's Infinity Shots, Kate Bishop's Arrows)
        new |={b for b in add if b in cards} - got
    return new


def forms_of(root, pairs):
    """a card and the forms it turns into are one card (union of the pairs; forms that turn into each other, Swapbot, too)"""
    def fam(n):
        seen = set()
        while root[n] != n and n not in seen: seen.add(n); n = root[n]
        return n
    for a, b in pairs:
        if a in root and b in root and fam(a) != fam(b): root[fam(b)] = fam(a)
    return fam


def families(c, nodes):
    """a champion and its level-up forms are one card in play (a levelled champion is never next to its own level 1)"""
    root = {n: n for n in nodes}
    fam = forms_of(root, c.execute("select src, dst from card_link where rel='transforms_into'").fetchall())
    return {n: fam(n) for n in nodes}


def spent_lines(c, game, nodes):
    """a count of mana spent on a kind of card ("I've seen you play 6+ mana of spells", Lux): a card of that kind that alone pays
    that much (cost 6 or more) or whose cost is variable (Thermogenic Beam spends all your mana) levels it or feeds it; cheaper
    cards add up like every card of the kind and make no line (Kaptain 31 Oct 2026)"""
    cards = cards_of(c, game); out = Lines(); marks = ','.join('?' * len(nodes)); L = list(nodes); lvl = level_abilities(c)
    for t, ab, k, w, n in c.execute(f"""select card, ability, coalesce(ev_obj_kind, of_kind), coalesce(ev_obj_with, of_with), n from flat_if
            where event='mana_spent' and test='event_count' and op in ('ge','gt') and coalesce(ev_actor_side,'mine')!='enemy'
            and card in ({marks})""", L).fetchall():
        k = k if k in KIND_CAT else 'any'
        for a in nodes:
            x = cards.get(a)
            if a == t or not x or not matches(c, game, x, k, w): continue
            if x['x_cost'] or (x['cost'] is not None and n is not None and x['cost'] >= n):
                lv = ab in lvl
                say = ('has a variable cost: pays it alone' if x['x_cost'] else f'costs {int(x["cost"])}: pays it alone') + (' (levels it up)' if lv else '')
                out[(a, t)].append(('levels' if lv else 'type', 1.0 if lv else 0.5, say))
    return out


def stat_reader_lines(c, game, nodes):
    """an effect that raises a unit's stat by another of its stats (Gabrian Enchantment: "a creature's Attack becomes equal to its
    Life"; Bayou Brunch doubles it) gets more from a unit that grows that stat itself (Oak Father: +0/+1 for each forest)"""
    cards = cards_of(c, game); out = Lines(); marks = ','.join('?' * len(nodes)); L = list(nodes)
    readers = c.execute(f"""select distinct b.card, e.act, p.param, a.attr from param p join amount a on a.id=p.amount join effect e on e.id=p.effect
              join ability b on b.id=e.ability join target t on t.id=a.of_target join target o on o.id=e.on_target
              where a.x='stat' and t.pick='it' and o.pick in ('chosen','it','all') and coalesce(o.side,'mine') in ('mine','any')
              and e.act in ('stat_change','stat_set') and p.param in ('power','health') and a.attr in ('power','health')
              and b.card in ({marks})""", L).fetchall()
    # a count of my units with a power floor ("units with 5+ power", Trifarian Assessor, Reckoning): its text reads the stat, so
    # what raises my units' power feeds it (L18 "reads its power"; Kaptain's n16: Fury of the North -> Reckoning)
    floors = {t for (t,) in c.execute(f"""select card from flat_if where test in ('count','amount_count','have') and coalesce(of_side,'mine')='mine'
              and of_with like '%power ge %' and card in ({marks})""", L)} | {t for (t,) in c.execute(f"""select card from flat_do
              where params like '%count of%' and on_with is not null and params like '%power ge %' and card in ({marks})""", L)}
    if floors:
        raisers = {a for a, ps in c.execute(f"""select card, params from flat_do where origin='own' and act in ('stat_change','grow')
                   and coalesce(on_side,'mine')='mine' and coalesce(on_pick,'') not in ('self') and coalesce(on_kind,'unit') in ('unit','any')
                   and card in ({marks})""", L) if re.search(r'power=\d', ps or '')}
        for t in floors:
            for a in raisers - {t}: out[(a, t)].append(('stronger', 0.3, 'raises my units to the power it counts'))
    if not readers: return out
    grows = collections.defaultdict(set)  # unit -> stats it raises on itself
    for t, ps in c.execute(f"""select card, params from flat_do d where origin='own' and on_pick='self' and act in ('stat_change','grow')
            and not exists (select 1 from cond k where k.ability=d.ability and k.test='keyword_condition' and k.ref_keyword is not null)
            and card in ({marks})""", L):  # a growth only from another keyword (Gwen: Power from Hallowed) is not its own ()
        for x in (ps or '').split(';'):
            if '=' in x and not x.split('=', 1)[1].startswith('-'): grows[t].add(x.split('=', 1)[0])
    word = {'power': 'Attack', 'health': 'Life'} if game == 'faeria' else {'power': 'Power', 'health': 'Health'}
    for a, act, stat, read in readers:
        if act == 'stat_set' and stat == read: continue  # "set its Power to its Power" changes nothing
        for t in nodes:
            if t == a or cards.get(t, {}).get('cat') not in KIND_CAT['unit']: continue
            if read in grows.get(t, ()): out[(a, t)].append(('stronger', 0.5, f"turns the {word[read]} it grows into {word[stat]}"))
            # a printed stat is no link: every unit has Life (a line comes from what a card does, not what every card is)
    return out


def self_gains(c, nodes):
    """card -> what done to it sets off its own effect (dies, killed, damaged, survives_damage, sacrificed). A death keyword (Last
    Breath, Dying Wish) is its effect; a shield keyword that fires on damage (Barrier, Forcefield) is no effect anyone damages it for"""
    marks = ','.join('?' * len(nodes)); wants = collections.defaultdict(set)
    shield_ = {ab for (ab,) in c.execute("select ability from flat_do group by ability having min(act in ('negate_damage','damage_reduction'))=1")}
    by_enemy_ = {ab for (ab,) in c.execute("select ability from flat_when where actor_side='enemy'")}
    for t, h, ab_ in c.execute(f"""select card, happening, ability from flat_ref where role='trigger' and pick='self' and (origin='own' or
            (origin='has_keyword' and happening in ('dies','killed'))) and happening in ('dies','killed','damaged','survives_damage','sacrificed')
            and card in ({marks})""", list(nodes)):
        if ab_ in shield_ or ab_ in by_enemy_: continue  # it only stops the damage, or fires only on enemy damage (Petricite Charger)
        wants[t].add(h)
    return wants


def self_harm_lines(c, game, nodes):
    """harm aimed at any unit, of either side ("deal 1 damage to a creature"), or at my own units ("sacrifice another creature"):
    the player aims it at my own unit when that unit's own effect fires on it (Falcon Dive -> a Last Words unit with 1 Life;
    Lord of the Wastes -> Village Elder). A card that counts friendly deaths (Soul Eater) gets nothing from either-side harm."""
    cards = cards_of(c, game); out = Lines(); marks = ','.join('?' * len(nodes)); L = list(nodes)
    wants = self_gains(c, nodes)
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
    allg = lines_of(c, game); lines = Lines()
    for (a, b), ls in allg.items():
        if a in nodes and b in nodes: lines[(a, b)] += ls
    am = aimed(c, game, nodes, broad)
    stat_help = {p for src in (am, lines) for p, ls in src.items() if any(re.search(r'gives? it (more (stats|power|health|strength)|[+-]?\d)|\|', y) for _, _, y in ls)}  # A gives B stats already:
    # "more power / more health" from the same gain says it twice
    for f in (am, played_lines(c, game, nodes, broad), need_lines(c, game, nodes, broad),
              boost_lines(c, game, nodes, stat_help, {p for p, ls in am.items() if any('cheaper' in y or 'cost' in y for _, _, y in ls)}), gives_lines(c, game, nodes), object_help_lines(c, game, nodes, broad),
              actor_help_lines(c, game, nodes), doer_help_lines(c, game, nodes), self_harm_lines(c, game, nodes),
              state_giver_lines(c, game, nodes), stat_reader_lines(c, game, nodes), spent_lines(c, game, nodes)):
        for k, ls in f.items(): lines[k] += ls
    # a need the maker shares with the card it makes is the made card's (The Iron Conquest's stage III is its skill Undying
    # Revenge: Soul Cleave's dead ally feeds the skill, not the landmark too)
    mk_ = collections.defaultdict(set)
    for a, b in c.execute(f"select card, made from flat_made where card in ({','.join('?' * len(nodes))})", list(nodes)):
        if b in nodes and a != b and (c.execute('select category from card where id=?', (b,)).fetchone() or [''])[0] == 'ability':
            mk_[a].add(b)  # a skill it casts: the card's text repeats the skill's effect (a unit it makes has needs of its own)
    plain = lambda y, t: y.replace(mechanics.name(c, t), '*')  # the reason without the card's own name
    for (x, a) in list(lines):
        if x in mk_.get(a, ()):  # its own skill feeds the need the skill itself has: one need, said once (on the skill)
            own = {plain(l[2], x) for (y, z), ls in lines.items() if z == x for l in ls}
            keep = [l for l in lines[(x, a)] if l[0] not in ('type', 'waits', 'levels') or plain(l[2], a) not in own]
            if keep: lines[(x, a)] = keep
            else: del lines[(x, a)]
            continue
        same = {plain(l[2], b) for b in mk_.get(a, ()) if b != x for l in lines.get((x, b), ())}
        if same and a not in mk_.get(x, ()):
            keep = [l for l in lines[(x, a)] if l[0] not in ('type', 'waits', 'levels') or plain(l[2], a) not in same]  # its needs
            # only: help on the maker itself (more power, a move, a keyword) is still help on it
            if keep: lines[(x, a)] = keep
            else: del lines[(x, a)]
    fam = families(c, nodes)
    lines = collections.defaultdict(list, {(a, b): [l for l in ls if l[0] == 'levelsinto'] if fam[a] == fam[b] else ls
                                           for (a, b), ls in lines.items()})
    if broad:
        made_by = collections.defaultdict(set)
        for (a, b), ls in lines.items():
            if nodes.get(b) and any(k == 'puts' and y == 'plants' for k, _, y in ls): made_by[b].add(a)  # plants it: it goes off by itself
    # A makes B, B acts on C: A gets no line to C (Kaptain 31 Oct 2026: Targonian Tellstones -> Blessing of Targon -> Braum, Vikrash ->
    # Slipstream -> Janna); B is played or acts as a card of its own. Only a planted card that goes off when drawn is the planter's
    # act (Kaptain n31, n32: planting Chimes levels Bard)
        for (m, b), ls in list(lines.items()):
            for p in made_by.get(m, ()):
                if p == b or fam[p] == fam[b]: continue
                if any(k == 'levels' for k, *_ in lines.get((p, b), ())): continue  # it levels it up itself already
                for k, w, why in ls:
                    # only what levels a champion up is passed on (other lines through a made card stay on it), one step (not
                    # through two made cards), and only what the maker does not already do itself (Trundle hits the Nexus too)
                    if k == 'levels' and not why.startswith('through '):
                        lines[(p, b)].append((k, w * 0.5, f'through {mechanics.name(c, m)}: {why}'))
    # "makes the Wraithling it asks for": when the Wraithling is drawn too, the maker puts it into play and the Wraithling enables
    # the card; no line from the maker straight to the card (Lilithe -> Wraithling -> Inkling Surge)
    enables_from = collections.defaultdict(set)  # m -> the cards m enables by being there ("is a Wraithling it asks for")
    for (m2, b), ls2 in lines.items():
        if any(k == 'type' and y.startswith('is ') for k, _, y in ls2): enables_from[m2].add(b)
    via_made = {(a, b) for (a, m), ls in lines.items() if nodes.get(m) and any(k == 'puts' for k, *_ in ls) for b in enables_from.get(m, ())}
    lines = collections.defaultdict(list, {(a, b): [l for l in ls if not ((a, b) in via_made and l[0] == 'type' and l[2].startswith('makes '))]
                                           for (a, b), ls in lines.items()})
    lines = collections.defaultdict(list, {(a, b): [l for l in ls if not (nodes.get(b) and l[2] == 'draws it from the deck')]
                                           for (a, b), ls in lines.items()})  # a card the deck only makes is in no deck to draw from
    # a form a card grows or levels into is never played from hand: its cost is never paid (Tadpole -> Bullfrog, Curious Egg ->
    # Hydra; a champion's level-up form)
    grown = {b for (a, b), ls in lines.items() if nodes.get(b) and any(k == 'levelsinto' for k, _, _ in ls)} - \
            {b for (a, b), ls in lines.items() if any(k == 'puts' for k, _, _ in ls)}
    lines = collections.defaultdict(list, {(a, b): [l for l in ls if not (b in grown and ('(pays its cost)' in l[2] or 'cheaper' in l[2]))] for (a, b), ls in lines.items()})
    # a card that draws or puts a kind of card from my deck finds the deck's cards of that kind, not the game's (Time of Legends
    # finds the deck's one legend)
    found = collections.Counter((a, y) for (a, b), ls in lines.items() if nodes.get(b) is False for k, w, y in ls
                                if k == 'puts' and (y == 'draws it from the deck' or y.startswith('puts it into play from')))
    lines = collections.defaultdict(list, {(a, b): [(k, 1.0 / found[(a, y)] if (a, y) in found and k == 'puts' else w, y) for k, w, y in ls]
                                           for (a, b), ls in lines.items()})
    # a unit and what it carries (Into the Breach: a mech, its starting weapon and passive, and one extra weapon; the deck lists
    # each mech, then what it carries): the weapon fires from where its mech stands (Kaptain 30 Oct 2026)
    if game in CARRIED:
        carrier = None; cards = cards_of(c, game)
        for i in ids:
            x = cards.get(i)
            if not x: continue
            if x['cat'] not in CARRIED[game][0] + ('item',): carrier = i
            elif carrier is not None: lines[(carrier, i)].append(('carries', 1.0, '{A} carries {B}'))
    # "helps" says how: cheaper, stronger, a keyword, into place, a clear way (or it makes what the card waits for happen more)
    lines = collections.defaultdict(list, {(a, b): [(help_kind(y), w, y) if k == 'boosts' else (k, w, y) for k, w, y in ls]
                                           for (a, b), ls in lines.items()})
    def unit_name(b):  # the unit itself: a carried weapon is "the mech with Titan Fist"
        x = cards_of(c, game).get(b)
        return f'the {CARRIED[game][1].lower()} with {mechanics.name(c, b)}' if x and game in CARRIED and x['cat'] in CARRIED[game][0] else mechanics.name(c, b)
    named = lambda a, b, y: y.replace('{A}', mechanics.name(c, a)).replace('{Bc}', unit_name(b)).replace('{B}', mechanics.name(c, b))  # names
    # an act on a card kept by rule L14 says why the card uses it: it is a reaction ("triggers"), not a bare "can aim at it"
    return nodes, {(a, b): [('waits' if k == 'targets' else k, w, named(a, b, y)) for k, w, y in one_link(v)] for (a, b), v in lines.items() if v}


# one link per pair of cards (Kaptain, 30 Oct 2026: never two arrows between the same two cards): its kind is the first of
# these the reasons have, its reasons all of them ("is an Imp it asks for; also is a card it counts when played")
KIND_ORDER = ('carries', 'puts', 'levelsinto', 'levels', 'type', 'waits', 'moves', 'clears', 'heals', 'keyword', 'stronger', 'cheaper', 'repeats',
              'rules', 'boosts', 'targets')
KIND_WORD = {'carries': 'carries', 'waits': 'triggers', 'type': 'enables', 'cheaper': 'makes cheaper', 'heals': 'heals', 'stronger': 'makes stronger',
             'keyword': 'gives keyword', 'moves': 'moves into place', 'clears': 'clears the way', 'levels': 'helps it level up',
             'puts': 'puts it into play', 'repeats': 'repeats its effects', 'rules': 'changes how it works', 'boosts': 'helps',
             'levelsinto': 'levels into', 'targets': 'can aim at it'}


MOVE_RE = re.compile(r'\{A\} moves (it|units|enemy units|your units), and \{B\} acts on units (.*)$')


def merge_places(ls):
    """every move reason of a pair is one reason: who is moved, every place ("{A} moves {B} and units, and {B} acts on units
    next to it or around it")"""
    moved, places, w_, k_ = [], [], 0, None
    rest = []
    for k, w, y in ls:
        m = MOVE_RE.match(y)
        if not m: rest.append((k, w, y)); continue
        moved.append(m.group(1)); places += [p for p in m.group(2).split(' or ') if p not in places]; w_ = max(w_, w); k_ = k_ or k
    if not moved: return ls
    others = {x for x in moved if x != 'it'}
    who = ' and '.join((['{Bc}'] if 'it' in moved else []) + ([others.pop() if len(others) == 1 else 'units'] if others else []))
    return [(k_, w_, f'{{A}} moves {who}, and {{B}} acts on units {" or ".join(sorted(places))}')] + rest


TOPICS = (('nexus', r'enemy player|the Nexus'), ('cost', r'cheaper|its cost|pays? '), ('countdown', r'countdown'),
          ('attack', r'attack again|another attack|attack for its effect|Rally|makes? (it|your units) attack'),
          ('power', r'power|stats|health|stronger|strength'), ('stun', r'Stun'), ('lurk', r'Lurk'),
          ('is', r'^is (a|an|the) '), ('puts', r'^(plays|casts its|casts|summons|creates|copies)'))


def topic(y):
    """what a reason is about: two reasons of one pair about the same thing say one fact twice"""
    y = re.sub(r' \(levels it up\)| \(by [^)]*\)', '', y)
    return next((n for n, r in TOPICS if re.search(r, y)), y)


def one_link(ls):
    ls = list({(k, y): (k, w, y) for k, w, y in ls}.values())  # one card doing a thing twice (when summoned, when attacking) is one reason
    ls = merge_places(ls)
    plain = {(k, y) for k, _, y in ls}
    ls = [x for x in ls if not (re.search(r' \(when [^)]*\)$', x[2]) and (x[0], re.sub(r' \(when [^)]*\)$', '', x[2])) in plain)]  # said once (Shield Array)
    if len(ls) > 1: ls = [x for x in ls if x[0] != 'targets'] or ls  # "can aim at it" only when nothing else joins them
    ls.sort(key=lambda x: (KIND_ORDER.index(x[0]) if x[0] in KIND_ORDER else 99, -x[1]))
    seen, kept = set(), []  # one reason is said once, by its strongest kind (L10): one fact read by two rules is one reason
    for x in ls:
        tp = topic(x[2])
        if tp and tp in seen: continue
        seen.add(tp); kept.append(x)
    ls = kept
    k, w, y = ls[0]
    more = [f'{KIND_WORD.get(k2, k2) + ": " if k2 != k else ""}{y2}' for k2, _, y2 in ls[1:]]
    return [(k, max(x[1] for x in ls), '; also '.join([y] + more))]


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
        stack, pred, sigma, dist, q = [], Lines(), collections.Counter({s: 1}), {s: 0}, collections.deque([s])
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
    adj, root = Lines(), {n: n for n in nodes}
    fam = forms_of(root, [(a, b) for (a, b), (w, kind, why) in best.items() if kind == 'levelsinto'])
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
    fam = forms_of(root, [(a, b) for (a, b), (w, kind, why) in best.items() if kind == 'levelsinto'])
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
    adj = Lines()
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
