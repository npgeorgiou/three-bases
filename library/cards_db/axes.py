"""The wheel axes (factions/12-mechanical-wheel.txt) measured for every real faction of the library, one spoke per end.

Run from library/cards_db: python3 axes.py  ->  axes.tsv and ../../factions/wheel-axes.html
        python3 axes.py --cards <file>  ->  per spoke, concept and game, the cards that concept catches (for the check)
Each spoke is one end of an axis: a list of library concepts (Claude's choice, checked against the cards they catch).
A card counts for a spoke if it has any of its concepts. A faction's value on a spoke = the share of its cards that count,
divided by the average share of the factions of its game (0 = none, 1 = average), then smoothed: each faction counts as if
it had SHRINK more cards at the average, and the value is raised to POWER, so very high and very low values are pulled in.
Unit stats (spokes in NUMERIC) are strength and defence per supply; unit_stats() reads each game's own stat fields.
A game with fewer than MIN_GAME_CARDS cards for a spoke gives its factions no value on it (a gap, not 0).
A game with several kinds of supply (SUPPLIES) has each unit's cost divided by the average cost of its kind.
Axes 4, 5 and 8 have one spoke each: their other end (units now, works alone, plays what it draws) is a low value.
Two counts: "cards" = every card of the faction once; "decks" = each card weighted by how many of the library's top
decks (decks.tsv) play it; factions with fewer than MIN_DECK_CARDS cards in decks get no deck count.
"With others" = the average of two values: position cards (BESIDE, the same in every game) and combos (the share of the faction's card pairs
that links.sqlite links; run links.py first).
"""
import collections, json, math, os, sqlite3, sys
import deck_analysis
import faction_asks, mechanics

STOP_ON_ENEMY = ['disable', 'silence', 'immobilize', 'cant_move', 'attack_lock']  # stops enemy units; the other ways to break their plan follow
STOP_ALWAYS = ['immobilize', 'attack_lock', 'silence', 'disable']
DISRUPT_ON_ENEMY = ['stat_loss', 'forced_attack', 'forced_movement', 'debuff', 'steal', 'attack_zero', 'stat_multiply', 'bounce_enemy',
                    'polymorph', 'discard', 'counter_spell', 'transform', 'return_to_hand']
DISRUPT_ALWAYS = ['hand_disruption', 'mill', 'board_clog', 'cost_increase', 'play_restriction', 'counter_spell', 'steal', 'bounce_enemy', 'junk_cards']
NOT_MEASURED = ('monster_train',)  # Kaptain, 9 Nov 2026: a different kind of game, not on the page (Marvel Snap has no factions)
KILL_ON_ENEMY = ['destroy', 'banish']  # kills outright; damage is its own two radii
DAMAGE_ON_ENEMY = ('damage', 'damage_over_time')  # the card's own text deals damage to an enemy unit or player (a unit's strike is no row)
DAMAGE_NO_SIDE_GAMES = ('into_the_breach',)  # weapon cards (category ability) deal damage to a tile, friend or enemy (Artemis Artillery); the records keep the text and name no side
DAMAGE_BY_CONCEPT = ('fight_enemy',)  # damage to an enemy that no damage row carries: my unit is made to fight / strike a chosen enemy (Faeria Hunt Down, Runeterra Single Combat)
NEAR = ' or '.join("W like '%position " + w + "%'" for w in ('% bordering', '% surrounding', '% sides', '% diagonal', 'is behind', '% in_circuit'))
BESIDE = [  # my own units by where they stand next to this card (any game): an effect on them, a condition on them, an event of theirs
    "select card from flat_do where on_side='mine' and (" + NEAR.replace('W', "(coalesce(on_with,'')||coalesce(to_with,''))") + ") and ",
    "select card from flat_if where of_side='mine' and (" + NEAR.replace('W', "(coalesce(of_with,'')||coalesce(ev_obj_with,''))") + ") and ",
    "select card from flat_when where obj_side='mine' and (" + NEAR.replace('W', "coalesce(obj_with,'')") + ") and ",
    "select card from flat_do where coalesce(on_side,'mine')='mine' and on_pick in ('right_of_self','left_of_self') and "]  # its neighbour in its own row
CANT = ('attacks', 'moves')  # an enemy unit that can't do these is stopped (Kaptain, 9 Nov 2026: "can't block" does not;
# "can't strike" is Inscryption's Waterborne: the enemy can't strike this unit, which protects it)
SUPPLIES = {'inscryption': ('blood', 'energy', 'bones', 'mox')}  # games whose cards are paid in different kinds of supply
UNIT_CATS = ('unit', 'hero', 'leader')
SHOWN = {'multiply_own*': 'a stat of my own unit doubled or multiplied', 'stop*': 'an effect on enemies: ' + ', '.join(STOP_ON_ENEMY) + ', can\'t attack, can\'t move; or any card with: ' + ', '.join(STOP_ALWAYS),
         'disrupt*': 'an effect on enemies: ' + ', '.join(DISRUPT_ON_ENEMY) + '; or any card with: ' + ', '.join(DISRUPT_ALWAYS),
         'kill*': 'an effect on enemies: ' + ', '.join(KILL_ON_ENEMY),
         'weaken*': 'an enemy unit made weaker (debuff on an enemy)',
         'spelldmg*': 'a spell whose text deals damage to an enemy',
         'textdmg*': 'a unit (or building, item, weapon) whose text deals damage to an enemy',
         'position*': 'position: an effect or condition on its own units beside, around or behind it, or on the unit to its right or left',
         'countboard*': 'counts the units on the board',
         'combo*': 'combos: the share of the faction\'s card pairs the library links',
         'cheapunit*': 'a unit in the cheapest third of its game\'s units', 'dearunit*': 'a unit in the dearest third of its game\'s units',
         'strength*': 'its units\' strength per supply (Stormbound: the one number; Gwent: power)',
         'defence*': 'its units\' defence per supply (Stormbound: the one number; Gwent: power + armour)'}
NUMERIC = {'strong': 0, 'tough': 1}  # spokes measured from unit stats per supply, not from card effects
SPELL_SPOKES = ('spelldmg', 'spellpay')  # a game with no spells has no value there (Into the Breach's boosted weapons are no spells)
MIN_GAME_CARDS = 10  # with 5, two cards of a small game gave one of the highest values of the wheel (Inscryption Beast, breaks their plan)
SHRINK = 5  # smoothing: every faction counts as if it had 5 more cards at its game's average (small factions swing less)
POWER = 0.75  # smoothing: values are raised to this power (4 times the average shows as 2.8, a quarter as 0.35)
NO_VALUE = {('into_the_breach', 'strong'): 'its units\' damage comes from weapons, not in the library',
            ('into_the_breach', 'wide'): 'its units have no cost', ('into_the_breach', 'tall'): 'its units have no cost',
            **{(g, k): 'the game has no spells' for g in ('inscryption', 'into_the_breach') for k in ('spelldmg', 'spellpay')},
            **{('sts1', k): 'the player has no units' for k in ('strong', 'tough', 'wide', 'tall', 'spends', 'heals', 'growsdef', 'protects', 'textdmg')}}
CHECKS = [  # Kaptain's points: (game, faction, spoke, lowest value it must have)
    ('faeria', 'Red', 'textdmg', 1.5),  # 9 Nov 2026: Red is Faeria's fixed-damage faction (its units' text deals it)
    ('faeria', 'Red', 'strikes', 1.0),  # and its units strike too; one number used to hide that
    ('faeria', 'Green', 'textdmg', 0.3),  # 14 Nov 2026: Green kills by making its unit fight a chosen enemy (Deepwood Stalker, Frog-Tosser; fight_enemy), 0.13 without
    ('into_the_breach', 'Ranged', 'textdmg', 0.5),  # 14 Nov 2026: weapon damage hits enemies (Artemis Artillery); the radius had no value before
    ('runeterra', 'Demacia', 'many', 0.1),  # 14 Nov 2026: Judgment, one ally strikes all battling enemies (aoe_damage); 0.06 without
    ('inscryption', 'Undead', 'strong', 0.9),  # 0.75 when 4 Bones counted as 4 Blood (SUPPLIES)
]
CARD_CASES = [  # (game, card, starred concept, whether it must have it): every game counts the same (16 Nov 2026)
    ('duelyst', 'Roar', 'position*', True), ('stormbound', 'Doctor Mia', 'position*', True),  # an effect on my own units beside it
    ('duelyst', 'Excelsious', 'position*', False), ('stormbound', 'Dubious Hags', 'position*', False),  # only enemies beside it: an area hit
    ('runeterra', 'Legion Drummer', 'position*', True),  # its neighbour to the right in its own row
    ('runeterra', 'Puffcap Peddler', 'disrupt*', True), ('faeria', None, 'disrupt*', True)]  # junk cards given to the enemy, in every game
GAPS = [('inscryption', 'disrupts'), ('sts1', 'tall'), ('into_the_breach', 'spellpay'), ('inscryption', 'spellpay')]  # must have no value: 5 cards in the whole game; a game with no units; games with no spells
HAS = [('into_the_breach', 'textdmg'),  # weapons' damage on a tile counts as damage on enemies (DAMAGE_NO_SIDE_GAMES, 14 Nov 2026)
       ('gwent', 'grows'), ('gwent', 'growsdef'),  # must have a value: growth of Gwent's one number counts as both
       ('duelyst', 'pos'), ('faeria', 'pos'), ('stormbound', 'pos')]  # position in the board games
MIN_DECK_CARDS = 10
MIN_DECKS_BOTH = 5  # a game gives a decks value for two radii only when at least 5 of its decks hold both
MIN_LINKS_GAME = 5  # a game counts for two radii only when chance alone would give it 5 linked pairs
MIN_LINKS = 20  # two radii get a "work together" number only when chance alone would give 20 linked pairs  # Faeria Pandora has 1 card in decks
SPOKES = [  # (key, axis number, axis name, this radius, concepts, area of the circle); every concept counts in every game
    # in circle order: neighbours belong together, and the radii of one area sit side by side
    ('strong', 9, 'Unit stats', 'strength', ['strength*'], 'Fighting'),
    ('grows', 3, 'Damage', 'grows strength', ['attack_gain', 'multiply_own*'], 'Fighting'),
    ('strikes', 3, 'Damage', 'strikes more or first', ['on_attack',
        'multi_attack', 'first_strike', 'attack_now', 'excess_damage', 'counterattack', 'on_fight', 'piercing'], 'Fighting'),
    ('textdmg', 3, 'Damage', 'damage from units\' text', ['textdmg*'], 'Damage'),
    ('kills', 2, 'Enemy units', 'kills outright', ['kill*', 'removal', 'deathtouch'], 'Damage'),
    ('many', 6, 'Targets', 'many at once', ['aoe_damage',
        'board_wipe', 'multi_target_attack', 'rows', 'row_effects', 'area_templates', 'countboard*'], 'Damage'),
    ('spelldmg', 3, 'Damage', 'damage from spells', ['spelldmg*'], 'Spells'),
    ('spellpay', 3, 'Damage', 'rewards playing spells', ['on_spell', 'spells_played_condition', 'spell_power'], 'Spells'),
    ('stops', 2, 'Enemy units', 'stops them', ['stop*'], 'Control'),
    ('disrupts', 2, 'Enemy units', 'breaks their plan in other ways', ['disrupt*', 'disruption'], 'Control'),
    ('supply', 4, 'Supply and cards', 'more supply', ['base_resource_gain', 'resource_banking', 'coin_economy'], 'Cards and supply'),
    ('cheaper', 4, 'Supply and cards', 'cheaper or stronger hand', ['cost_reduction',
        'free_play', 'cost_set', 'in_hand_buff'], 'Cards and supply'),
    ('cards', 4, 'Supply and cards', 'more cards', ['draw', 'generate_cards'], 'Cards and supply'),
    ('picks', 8, 'Hand and discard pile', 'picks and copies', ['copy', 'tutor', 'retain', 'selection'], 'Cards and supply'),
    ('back', 8, 'Hand and discard pile', 'brings back', ['recycle', 'return_to_hand', 'revive'], 'Cards and supply'),
    ('wide', 7, 'Width', 'many cheap units', ['cheapunit*', 'summon'], 'Many units and dying'),
    ('spends', 1, 'Own units', 'spends them', ['sacrifice', 'self_destruct',
        'death_trigger',
        'other_death_trigger', 'on_sacrifice',
        'death_count', 'friendly_fire'], 'Many units and dying'),
    ('together', 5, 'Works with others', 'position and combos', ['position*', 'combo*'], 'Together'),
    ('heals', 1, 'Own units', 'heals them', ['heal',
        'regeneration'], 'Staying alive'),
    ('growsdef', 1, 'Own units', 'grows defence', ['defence_gain'], 'Staying alive'),
    ('protects', 1, 'Own units', 'protects them', ['shield', 'protection',
        'immunity', 'cheat_death',
        'damage_reduction', 'block_armor', 'tank'], 'Staying alive'),
    ('tough', 9, 'Unit stats', 'defence', ['defence*'], 'Staying alive'),
    ('tall', 7, 'Width', 'a few big units', ['dearunit*'], 'Staying alive'),
]


def unit_stats(game, power, health, st):
    """(strength, defence) of a card: Stormbound has one number for both, Gwent power (defence adds armour), Into the
    Breach only health; other games power and health"""
    try: d = json.loads(st) if st else {}
    except ValueError: d = {}
    num = lambda v: float(str(v).split('/')[0]) if v not in (None, '') and str(v).split('/')[0].replace('.', '').isdigit() else None
    if game == 'stormbound':
        v = num(d.get('strength')); return v, v
    if game == 'gwent':
        p = num(d.get('power')) if power is None else power
        return p, None if p is None else p + (num(d.get('armor')) or 0)
    return power, health


def counts(ks, game, concepts):
    """does a card with concepts ks count for a spoke (the same in every game)"""
    return any(k in ks for k in concepts)


# What of a card makes a link (links.sqlite a_ab / b_ab, written by links.py): an effect row 'ability.seq', an ability, 'kw<id>'
# (a keyword it has), 'c:<concept>' (a concept read from the whole card), 'type' (the card by what it is), 'rule' (the game's
# rules). A link counts for a radius or mechanic only through the concepts of what made it on each side (side_concepts).
SOURCES = collections.defaultdict(lambda: collections.defaultdict(set))  # card -> concept -> what of the card gives it (tag);
# a concept with no source (unit stats, cost, health) belongs to the card by what it is
KW_AB = collections.defaultdict(set)  # (card, ability) -> 'kw<id>' of the keywords it has whose own ability that is
SIDE = {}  # (card, side, keys) -> the keys that side counts for (side_keys)
DO_SRC = "ability || '.' || seq, 'kw' || via"  # flat_do columns naming a row's source
IF_SRC = "ability, 'kw' || via"  # flat_if / flat_when: an ability's conditions and triggers (a keyword's when no ability)


def note_src(card, k, *srcs):
    for x in srcs:
        if x is not None: SOURCES[card][k].add(str(x))


def row_sources(c):
    """SOURCES of the concepts flat.py's derive writes into flat_concept (rows, keywords, its RULES), and KW_AB"""
    import flat
    SOURCES.clear(); KW_AB.clear(); SIDE.clear()
    for t in ('flat_do', 'flat_if', 'flat_when'):
        for card, ab, via in c.execute(f"select distinct card, ability, via from {t} where origin='has_keyword' and ability is not null and via is not null"):
            KW_AB[(card, ab)].add(f'kw{via}')
    for t, cols in (('flat_do', DO_SRC), ('flat_if', IF_SRC), ('flat_when', IF_SRC)):
        for card, k, *src in c.execute(f"select card, concept, {cols} from {t} where coalesce(concept,'')!=''"): note_src(card, k, *src)
    for card, k, kw in c.execute("select distinct ck.card, v.tree, ck.keyword from card_keyword ck join card k on k.id=ck.keyword join vocab v on "
                                 "v.field='keyword' and v.value=coalesce((select s.value from vocab s where s.field='keyword' and s.value=k.game || ':' || k.name), k.name) where v.tree!=''"):
        note_src(card, k, f'kw{kw}')
    for card, k, ab in c.execute("select distinct a.card, v.tree, a.id from cond cd join ability a on a.id=cd.ability join card k on k.id=cd.ref_keyword join vocab v on "
                                 "v.field='keyword' and v.value=coalesce((select s.value from vocab s where s.field='keyword' and s.value=k.game || ':' || k.name), k.name) "
                                 "where cd.test='keyword_condition' and v.tree!=''"):
        note_src(card, k, ab)
    for k, t, cond in flat.RULES:
        for card, *src in c.execute(f"select card, {DO_SRC if t == 'flat_do' else IF_SRC} from {t} where {cond}"): note_src(card, k, *src)


def side_concepts(card, src, con):
    """the concepts of a card that one side of a link comes from (its sources joined by ';'): an effect row gives its own
    concepts and its ability's conditions and triggers; an ability all of them; a keyword's own effect also the keyword"""
    out = set()
    parts = [t for t in (src or '').split(';') if t]
    parts += [k for t in parts if t[0].isdigit() for k in KW_AB.get((card, int(t.split('.')[0])), ())]
    for s in parts:
        if s == 'rule': continue
        if s.startswith('c:'): out.add(s[2:]); continue
        for k in con[card]:
            got = SOURCES[card].get(k)
            if s == 'type': hit = not got
            elif not got: hit = False
            elif s[0].isdigit() and '.' in s: hit = s in got or s.split('.')[0] in got
            elif s[0].isdigit(): hit = s in got or any(t.startswith(s + '.') for t in got)
            else: hit = s in got
            if hit: out.add(k)
    return out


def star_of(card, ks, star, by):
    """a starred concept the card has for holding concepts of `by`: it comes from what gives those"""
    ks.add(star); note_src(card, star, *{t for k in ks & set(by) for t in SOURCES[card].get(k, ())})


def tag(c, x, games):
    """card -> its concepts, plus the starred ones this file adds; SOURCES: what of each card gives each concept"""
    con = collections.defaultdict(set)
    row_sources(c)
    for card, k in c.execute('select card, concept from flat_concept'):
        con[card].add(k)
    for card, k, *src in c.execute(f"select card, concept, {DO_SRC} from flat_do where on_side='enemy' and coalesce(on_kind,'')!='player' and "
                                   + faction_asks.ROW_ORIGIN):
        for star, ks in (('stop*', STOP_ON_ENEMY), ('disrupt*', DISRUPT_ON_ENEMY), ('kill*', KILL_ON_ENEMY)):
            if k in ks: con[card].add(star); note_src(card, star, *src)
    for card, *src in c.execute(f"select card, {DO_SRC} from flat_do where concept='stat_multiply' and coalesce(on_side,'mine')!='enemy' and "
                                + faction_asks.ROW_ORIGIN):  # doubling my own unit's stat grows it (Kaptain)
        con[card].add('multiply_own*'); note_src(card, 'multiply_own*', *src)
    for card, k, side, *src in c.execute(f"select card, concept, on_side, {DO_SRC} from flat_do where concept='debuff' and "
                                         + faction_asks.ROW_ORIGIN):
        if k == 'debuff' and side == 'enemy': con[card].add('weaken*'); note_src(card, 'weaken*', *src)
    for card, *src in c.execute(f"select card, {IF_SRC} from flat_if where test='amount_count' and of_kind='unit' and of_zone='board' and " + faction_asks.ROW_ORIGIN):
        con[card].add('countboard*'); note_src(card, 'countboard*', *src)
    for card, *src in c.execute(f"select card, {DO_SRC} from flat_do where on_side='enemy' and coalesce(on_kind,'')!='player' and act='cant' and param_event in "
                                + repr(CANT) + " and " + faction_asks.ROW_ORIGIN):
        con[card].add('stop*'); note_src(card, 'stop*', *src)
    for q, cols in zip(BESIDE, (DO_SRC, IF_SRC, IF_SRC, DO_SRC)):
        for card, *src in c.execute(q.replace('select card from', f'select card, {cols} from', 1) + faction_asks.ROW_ORIGIN):
            con[card].add('position*'); note_src(card, 'position*', *src)
    dmg = collections.defaultdict(set)
    for card, *src in c.execute(f"select card, {DO_SRC} from flat_do where on_side='enemy' and concept in " + repr(DAMAGE_ON_ENEMY) + " and " + faction_asks.ROW_ORIGIN):
        dmg[card] |= {str(v) for v in src if v is not None}
    # a game whose weapons hit the tile aimed at, whoever stands there: its damage rows name no side and count too
    for card, *src in c.execute(f"select f.card, f.ability || '.' || f.seq, 'kw' || f.via from flat_do f join card k on k.id=f.card where f.on_side is null and k.game in ("
                                + ','.join(repr(g) for g in DAMAGE_NO_SIDE_GAMES) + ") and k.category='ability' and f.concept in " + repr(DAMAGE_ON_ENEMY)):
        dmg[card] |= {str(v) for v in src if v is not None}
    for (card,) in c.execute("select card from flat_concept where concept in (" + ','.join(repr(k) for k in DAMAGE_BY_CONCEPT) + ")"):
        dmg[card] |= {t for k in DAMAGE_BY_CONCEPT for t in SOURCES[card].get(k, ())}
    for i, cat in c.execute('select id, category from card'):
        if i in dmg:
            star = 'spelldmg*' if cat == 'spell' else 'textdmg*'
            con[i].add(star); note_src(i, star, *dmg[i])
    pools = {g: x.pool(g) for g in games}
    raw = {i: (g, cat, cost, unit_stats(g, p, h, st), (ct or '').lower()) for i, g, cat, cost, p, h, st, ct in
           c.execute('select id, game, category, cost, power, health, stats, cost_text from card')}
    kind = lambda i: next((k for k in SUPPLIES.get(raw[i][0], ()) if k in raw[i][4]), '')
    paid = collections.defaultdict(list)  # (game, kind of supply) -> the costs of its units
    for g, pool in pools.items():
        for i in pool:
            if raw[i][1] in UNIT_CATS and raw[i][2]: paid[(g, kind(i))].append(raw[i][2])
    def cost(i):  # in a game with several kinds of supply: the cost against the average cost of its kind
        g, _, v = raw[i][:3]
        return v / (sum(paid[(g, kind(i))]) / len(paid[(g, kind(i))])) if g in SUPPLIES and v and paid[(g, kind(i))] else v
    stats = {i: (r[1], cost(i)) + r[3] for i, r in raw.items()}
    for g, pool in pools.items():
        costs = sorted(stats[i][1] for i in pool if stats[i][0] in UNIT_CATS and stats[i][1] is not None)
        third = lambda n: min(sorted(set(costs)), key=lambda t: abs(n(t) - len(costs) / 3), default=None)
        lo = third(lambda t: sum(1 for v in costs if v <= t))  # the cost up to which the units are nearest to a third of the game's units
        hi = third(lambda t: sum(1 for v in costs if v >= t))  # (when most units share one cost, cheap is under it and dear is over it)
        for i in pool:
            ks, v = con[i], stats[i][1]
            if ks & set(STOP_ALWAYS): star_of(i, ks, 'stop*', STOP_ALWAYS)
            if ks & set(DISRUPT_ALWAYS): star_of(i, ks, 'disrupt*', DISRUPT_ALWAYS)
            if stats[i][0] not in UNIT_CATS or v is None or lo is None or lo >= hi: continue
            if v <= lo: ks.add('cheapunit*')
            if v >= hi: ks.add('dearunit*')
    return con, pools, stats


def main():
    if '--near' in sys.argv: return near(sys.argv[sys.argv.index('--near') + 1])
    c = sqlite3.connect('cards.sqlite')
    games = sorted({g for (g,) in c.execute('select distinct game from card')})
    x = faction_asks.Ctx(c, games, None, {})
    con, pools, stats = tag(c, x, games)
    if '--cards' in sys.argv:
        return dump(c, x, games, con, pools, sys.argv[sys.argv.index('--cards') + 1])
    lacks = {(g, s[0]) for g in games for s in SPOKES if s[0] != 'together' and (
             sum(1 for i in pools[g] if stats[i][2 + NUMERIC[s[0]]] is not None and stats[i][0] in UNIT_CATS) if s[0] in NUMERIC
             else sum(1 for i in pools[g] if counts(con[i], g, s[4]))) < MIN_GAME_CARDS
             or (s[0] in SPELL_SPOKES and sum(1 for i in pools[g] if stats[i][0] == 'spell') < MIN_GAME_CARDS)}
    no_pos = {g for g in games if sum(1 for i in pools[g] if 'position*' in con[i]) < MIN_GAME_CARDS}
    pairs = link_pairs()
    deck_n = collections.Counter()  # card -> decks that play it
    deck_lists = collections.defaultdict(list)  # game -> every deck of decks.tsv, as its set of cards
    unknown = collections.Counter()
    with open('decks.tsv', encoding='utf-8') as f:
        next(f)
        for line in f:
            p = line.rstrip('\n').split('\t')
            if len(p) >= 4 and p[0] in pools:  # parse_deck knows names that hold a comma ("Seifer, Blood Tyrant"); splitting on commas lost them
                ids, bad = deck_analysis.parse_deck(c, p[0], p[3])
                unknown[p[0]] += len(bad)
                deck_lists[p[0]].append({i for i in ids if i in pools[p[0]]})
                for i in deck_lists[p[0]][-1]: deck_n[i] += 1
    if any(unknown.values()): print('deck card names the library does not know:', dict(unknown))
    rows = []
    for g in games:
        pool = pools[g]
        for fac in () if g in NOT_MEASURED else x.factions(g):
            ids = [i for i, v in pool.items() if fac in v[3]]
            w_decks = {i: deck_n[i] for i in ids if deck_n[i]}
            rec = {'game': g, 'faction': fac, 'n_cards': len(ids), 'deck_cards': len(w_decks),
                   'cards': shares({i: 1 for i in ids}, con, pairs, g, stats),
                   'decks': shares(w_decks, con, pairs, g, stats) if len(w_decks) >= MIN_DECK_CARDS else None}
            for m in ('cards', 'decks'):
                for g2, k in lacks | {(p, 'pos') for p in no_pos}:
                    if g2 == g and rec[m]: rec[m][k] = None
            rows.append(rec)
    for mode in ('cards', 'decks'):
        for g in games:
            ms = [r[mode] for r in rows if r['game'] == g and r[mode]]
            for k in [s[0] for s in SPOKES if s[0] != 'together'] + ['pos', 'combo']:
                vals = [q[k] for q in ms if q[k] is not None]
                avg = sum(vals) / len(vals) if vals else 0
                for q in ms:
                    if q[k] is None or not avg: q[k + '_v'] = None; continue
                    share = q[k] if k in ('combo',) + tuple(NUMERIC) else (q[k] * q['_n'] + SHRINK * avg) / (q['_n'] + SHRINK)
                    q[k + '_v'] = share / avg
            for q in ms:
                both = [q[k] for k in ('pos_v', 'combo_v') if q[k] is not None]
                q['together_v'] = sum(both) / len(both) if both else None
                q['together'] = None
                for sk in SPOKES:  # the final smoothing (POWER)
                    v = q[sk[0] + '_v']
                    q[sk[0] + '_v'] = None if v is None else round(v ** POWER, 3)
                q['lean_v'] = None if None in (q['strong_v'], q['tough_v']) else round(q['strong_v'] - q['tough_v'], 3)
    with open('axes.tsv', 'w', encoding='utf-8') as f:
        f.write('game\tfaction\tcards\tdeck_cards\tmode\t' + '\t'.join(f'{s[0]}_share\t{s[0]}_value' for s in SPOKES) + '\tlean\n')
        for r in rows:
            for mode in ('cards', 'decks'):
                if r[mode]:
                    f.write(f"{r['game']}\t{r['faction']}\t{r['n_cards']}\t{r['deck_cards']}\t{mode}\t" +
                            '\t'.join(f"{fmt(r[mode][s[0]])}\t{fmt(r[mode][s[0] + '_v'])}" for s in SPOKES) + '\t' + fmt(r[mode]['lean_v']) + '\n')
    measured = sorted({r['game'] for r in rows})  # the games on the page
    data = {'links': {'cards': radius_links(measured, pools, con, pairs), 'decks': radius_links(measured, pools, con, pairs, {g: v for g, v in deck_lists.items() if g not in NOT_MEASURED})},
            'deckCount': sum(len(v) for g, v in deck_lists.items() if g not in NOT_MEASURED), 'radii': [{'key': s[0], 'n': s[1], 'axis': s[2], 'end': s[3], 'area': s[5], 'concepts': [shown(k) for k in s[4]]} for s in SPOKES],
            'factions': [{'game': r['game'], 'faction': r['faction'], 'cards': r['n_cards'], 'deckCards': r['deck_cards'],
                          'cardsV': per_spoke(r['cards'], '_v'), 'decksV': per_spoke(r['decks'], '_v'),
                          'cardsS': per_spoke(r['cards'], ''), 'decksS': per_spoke(r['decks'], ''),
                          'why': {s[0]: NO_VALUE.get((r['game'], s[0]), 'its game has almost no cards for this') for s in SPOKES}} for r in rows]}
    here = os.path.dirname(os.path.abspath(__file__))
    tpl = open(os.path.join(here, '..', '..', 'tools', 'wheel_axes_template.html'), encoding='utf-8').read()
    with open(os.path.join(here, '..', '..', 'factions', 'wheel-axes.html'), 'w', encoding='utf-8') as f:
        f.write(tpl.replace('/*DATA*/null', json.dumps(data, ensure_ascii=False)))
    for g, fac, key, low in CHECKS:
        v = next((r['cards'][key + '_v'] for r in rows if r['game'] == g and r['faction'] == fac), None)
        if v is None or v < low: print(f'CHECK FAILED: {g} {fac} {key} is {v}, should be at least {low}')
    names = {(g, n): i for i, g, n in c.execute('select id, game, name from card')}
    for g, n, k, want in CARD_CASES:
        ids = [names[(g, n)]] if n else [i for i in pools[g] if 'junk_cards' in con[i]]
        if not ids or any((k in con[i]) != want for i in ids): print(f'CHECK FAILED: {g} {n or "junk cards"} should {"" if want else "not "}have {k}')
    for want, pairs_ in ((False, GAPS), (True, HAS)):
        for g, key in pairs_:
            if any((r['cards'][key + '_v'] is not None) != want for r in rows if r['game'] == g):
                print(f'CHECK FAILED: {g} {key} should have ' + ('a value' if want else 'no value'))
    print(len(rows), 'factions;', sum(1 for r in rows if r['decks']), 'with decks')


def link_pairs():
    """linked card pair (lower id first) -> {(what of the first card made a link, what of the second)}"""
    pairs = collections.defaultdict(set)
    for a, b, sa, sb in sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'links.sqlite')).execute('select a, b, a_ab, b_ab from link'):
        if a != b: pairs[(min(a, b), max(a, b))].add((sa, sb) if a < b else (sb, sa))
    return pairs


def side_keys(card, src, game, keys, con):
    """the radii (or mechanics) one side of a link counts for on this card (side_concepts)"""
    key = (card, src, tuple(k[0] for k in keys))
    if key not in SIDE:
        ks = side_concepts(card, src, con)
        SIDE[key] = [k[0] for k in keys if counts(ks, game, k[4])]
    return SIDE[key]


def radius_links(games, pools, con, pairs, deck_lists=None, seen=None):
    """All cards (no deck_lists): how much more often than chance the library links a card of one radius with a card of the
    other, counted through what of each card made the link (link_pairs, side_concepts). 1 = chance: the share of the game's
    card pairs the library links x the share of A's cards' link ends that A's own part makes x the same share for B.
    Worked out per game, then averaged over the games where chance gives MIN_LINKS_GAME+ pairs: each game counts the same.
    seen (a Counter): filled with the number of games in which real cards link each two radii (sorted keys).
    Decks (deck_lists given; Kaptain, 10 Nov 2026: how often radii appear in the same real decks, linked or not): per deck,
    the share of its cards that count for each radius; for two radii A and B, the average of (A share x B share) over the
    game's decks divided by (average A share x average B share). 1 = decks heavy in A hold as much B as usual; 2 = twice as
    much; below 1 = players keep them apart. "Usual" comes from the real decks, so a radius every deck plays does not look
    combined with everything. Each game counts the same: the value is the average over the games where at least
    MIN_DECKS_BOTH decks hold both radii."""
    keys = [s for s in SPOKES if s[0] != 'together' and s[0] not in NUMERIC]
    if deck_lists is not None:
        per = collections.defaultdict(list); used = {}
        for g in sorted(deck_lists):
            ds = [d for d in deck_lists[g] if d]
            if not ds: continue
            used[g] = len(ds)
            sh = [{k[0]: sum(1 for i in d if counts(con[i], g, k[4])) / len(d) for k in keys} for d in ds]
            mean = {k[0]: sum(x[k[0]] for x in sh) / len(ds) for k in keys}
            for a in keys:
                for b in keys:
                    both = sum(1 for x in sh if x[a[0]] and x[b[0]])
                    if both >= MIN_DECKS_BOTH and mean[a[0]] and mean[b[0]]:
                        per[(a[0], b[0])].append(sum(x[a[0]] * x[b[0]] for x in sh) / len(ds) / (mean[a[0]] * mean[b[0]]))
        print('decks used for radii that work together:', used)
        return {a[0]: {b[0]: round(sum(per[(a[0], b[0])]) / len(per[(a[0], b[0])]), 2) if per[(a[0], b[0])] else None for b in keys}
                for a in keys}
    per = collections.defaultdict(list); total = collections.Counter()
    for g in games:
        obs, exp = collections.Counter(), collections.Counter()
        ids = list(pools[g])
        of = {i: [s[0] for s in keys if counts(con[i], g, s[4])] for i in ids}
        dens = sum(1 for a, b in pairs if a in of and b in of) / (len(ids) * (len(ids) - 1) / 2)
        n = collections.Counter(k for i in ids for k in of[i])
        both = collections.Counter((ka, kb) for i in ids for ka in of[i] for kb in of[i])
        ends, made = collections.Counter(), collections.Counter()  # per radius: link ends on its cards, and those its own part made
        for (a, b), sides in pairs.items():
            if a in of and b in of:
                on = {a: set(), b: set()}; linked = set()
                for sa, sb in sides:
                    ka_, kb_ = side_keys(a, sa, g, keys, con), side_keys(b, sb, g, keys, con)
                    on[a].update(ka_); on[b].update(kb_); linked |= {(ka, kb) for ka in ka_ for kb in kb_}
                for i in (a, b):
                    for k in of[i]: ends[k] += 1; made[k] += k in on[i]
                for ka, kb in linked: obs[(ka, kb)] += 1; obs[(kb, ka)] += 1
        if seen is not None:
            for t in {tuple(sorted(k)) for k, v in obs.items() if v}: seen[t] += 1
        share = {k: made[k] / ends[k] if ends[k] else 0 for k in ends}
        for sa in keys:
            for sb in keys: exp[(sa[0], sb[0])] += (n[sa[0]] * n[sb[0]] - both[(sa[0], sb[0])]) * dens * share.get(sa[0], 0) * share.get(sb[0], 0)
        for k, e in exp.items():
            total[k] += e
            if e >= MIN_LINKS_GAME: per[k].append(obs[k] / e)
    return {a[0]: {b[0]: round(sum(per[(a[0], b[0])]) / len(per[(a[0], b[0])]), 2)
                   if total[(a[0], b[0])] >= MIN_LINKS and per[(a[0], b[0])] else None for b in keys} for a in keys}


def near(arg):
    """python3 axes.py --near "heals=1.6,stops=0.3": the real factions closest to a planned shape, over the radii named."""
    want = {k.strip(): float(v) for k, v in (p.split('=') for p in arg.split(','))}
    bad = set(want) - {s[0] for s in SPOKES}
    if bad: sys.exit('no such radius: ' + ', '.join(sorted(bad)) + '; the radii are: ' + ', '.join(s[0] for s in SPOKES))
    out = []
    with open('axes.tsv', encoding='utf-8') as f:
        head = next(f).rstrip('\n').split('\t')
        for line in f:
            r = dict(zip(head, line.rstrip('\n').split('\t')))
            have = [k for k in want if r[k + '_value']]
            if r['mode'] == 'cards' and len(have) == len(want):
                out.append((sum((float(r[k + '_value']) - want[k]) ** 2 for k in want) ** .5, r))
    for d, r in sorted(out, key=lambda t: t[0])[:10]:
        print(f"{d:.2f}  {r['game']}: {r['faction']}  " + ', '.join(f"{k} {float(r[k + '_value']):.1f}" for k in want))
    print('(factions of games with no value on one of these radii are left out)')


def shown(k):
    return SHOWN.get(k, k)


def fmt(v): return '' if v is None else f'{v:.4f}'
def per_spoke(m, suf): return None if not m else {**{s[0]: m.get(s[0] + suf) for s in SPOKES}, **({'lean': m.get('lean_v')} if suf else {})}


def shares(w, con, pairs, game, stats):
    """per spoke, the share of the faction's cards (weighted) that count for it; unit stats per supply for NUMERIC"""
    tot = sum(w.values())
    out = {'_n': len(w)}
    out.update({s[0]: sum(n for i, n in w.items() if counts(con[i], game, s[4])) / tot for s in SPOKES
                if s[0] != 'together' and s[0] not in NUMERIC})
    for key, j in NUMERIC.items():
        us = [(stats[i][2 + j], stats[i][1], n) for i, n in w.items() if stats[i][0] in UNIT_CATS and stats[i][2 + j] is not None]
        paid = [(v, cost, n) for v, cost, n in us if cost]
        if len(paid) >= len(us) / 2 and paid:  # per supply; a game whose units mostly have no cost (Inscryption): per unit
            out[key] = sum(v * n for v, _, n in paid) / sum(cost * n for _, cost, n in paid)
        else:
            out[key] = sum(v * n for v, _, n in us) / sum(n for *_, n in us) if us else None
    out['pos'] = sum(n for i, n in w.items() if 'position*' in con[i]) / tot
    ids = sorted(w)
    linked = sum(w[a] * w[b] for k, a in enumerate(ids) for b in ids[k + 1:] if (a, b) in pairs)
    allp = (tot * tot - sum(n * n for n in w.values())) / 2
    out['combo'] = linked / allp if allp else 0
    return out


def text(i, n=170):
    """a card's own text, short"""
    import source
    if not TEXTS: TEXTS.append(source.lib())
    r = TEXTS[0].execute('select text from entities where id=?', (i,)).fetchone()
    t = ' '.join(((r[0] if r else '') or '').split())
    return t if len(t) <= n else t[:n - 3] + '...'


TEXTS = []


def dump(c, x, games, con, pools, path, per=4):
    """for the check: per spoke and concept, per game the number of cards it catches and up to `per` of them with text"""
    with open(path, 'w', encoding='utf-8') as f:
        for key, n, axis, end, cons, _ in SPOKES:
            for k in cons:
                if k == 'combo*': continue
                f.write(f'\n## spoke {n} {axis}: {end} | concept {shown(k)}\n')
                for g in games:
                    ids = sorted(i for i in pools[g] if counts(con[i], g, [k]))
                    if not ids: continue
                    f.write(f'{g}: {len(ids)} cards\n')
                    for i in ids[:: max(1, len(ids) // per)][:per]:
                        f.write(f'  {mechanics.name(c, i)} | {text(i)}\n')


if __name__ == '__main__':
    main()
