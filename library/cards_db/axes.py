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
"With others" = the average of two values: position cards (POSITION, and BESIDE in every game) and combos (the share of the faction's card pairs
that links.sqlite links; run links.py first).
"""
import collections, json, math, os, sqlite3, sys
import faction_asks, mechanics

DISRUPT_ON_ENEMY = ['stat_loss', 'disable', 'forced_attack', 'forced_movement', 'debuff', 'steal',
                    'attack_zero', 'silence', 'stat_multiply', 'bounce_enemy', 'polymorph', 'discard', 'immobilize', 'cant_move',
                    'attack_lock', 'counter_spell', 'transform', 'return_to_hand']
DISRUPT_ALWAYS = ['hand_disruption', 'mill', 'board_clog', 'cost_increase', 'play_restriction', 'counter_spell',
                  'steal', 'immobilize', 'attack_lock', 'silence', 'disable', 'bounce_enemy']
KILL_ON_ENEMY = ['damage', 'excess_damage', 'destroy', 'banish', 'damage_over_time', 'aoe_damage', 'ping', 'direct_damage', 'board_wipe']
POSITION = ['adjacency', 'aura', 'link_formation', 'flanking', 'assists_support']
POSITION_GAMES = ('gwent', 'runeterra', 'marvel_snap')  # elsewhere these concepts are area hits and pushes (check of 9 Nov 2026)
NEAR = ' or '.join("W like '%position " + w + "%'" for w in ('% bordering', '% surrounding', '% sides', '% diagonal', 'is behind', '% in_circuit'))
BESIDE = [  # my own units by where they stand next to this card (any game): an effect on them, a condition on them, an event of theirs
    "select card from flat_do where on_side='mine' and (" + NEAR.replace('W', "(coalesce(on_with,'')||coalesce(to_with,''))") + ") and ",
    "select card from flat_if where of_side='mine' and (" + NEAR.replace('W', "(coalesce(of_with,'')||coalesce(ev_obj_with,''))") + ") and ",
    "select card from flat_when where obj_side='mine' and (" + NEAR.replace('W', "coalesce(obj_with,'')") + ") and "]
SUPPLIES = {'inscryption': ('blood', 'energy', 'bones', 'mox')}  # games whose cards are paid in different kinds of supply
JUNK_GAMES = ('marvel_snap', 'stormbound', 'gwent')  # junk cards that go to the enemy; in Slay the Spire they hurt my own deck
UNIT_CATS = ('unit', 'hero', 'leader')
SHOWN = {'disrupt*': 'an effect on enemies: ' + ', '.join(DISRUPT_ON_ENEMY) + '; or any card with: ' + ', '.join(DISRUPT_ALWAYS),
         'kill*': 'an effect on enemies: ' + ', '.join(KILL_ON_ENEMY),
         'position*': 'position: an effect or condition on its own units beside, around or behind it; in Gwent, Runeterra, Marvel Snap also: ' + ', '.join(POSITION),
         'countboard*': 'counts the units on the board',
         'combo*': 'combos: the share of the faction\'s card pairs the library links',
         'cheapunit*': 'a unit in the cheapest third of its game\'s units', 'dearunit*': 'a unit in the dearest third of its game\'s units',
         'strength*': 'its units\' strength per supply (Stormbound: the one number; Gwent: power)',
         'defence*': 'its units\' defence per supply (Stormbound: the one number; Gwent: power + armour)'}
NUMERIC = {'strong': 0, 'tough': 1}  # spokes measured from unit stats per supply, not from card effects
MIN_GAME_CARDS = 10  # with 5, two cards of a small game gave one of the highest values of the wheel (Inscryption Beast, breaks their plan)
SHRINK = 5  # smoothing: every faction counts as if it had 5 more cards at its game's average (small factions swing less)
POWER = 0.75  # smoothing: values are raised to this power (4 times the average shows as 2.8, a quarter as 0.35)
NO_VALUE = {('into_the_breach', 'strong'): 'its units\' damage comes from weapons, not in the library',
            ('into_the_breach', 'wide'): 'its units have no cost', ('into_the_breach', 'tall'): 'its units have no cost',
            **{('sts1', k): 'the player has no units' for k in ('strong', 'tough', 'wide', 'tall', 'spends', 'keeps')}}
CHECKS = [  # Kaptain's points: (game, faction, spoke, lowest value it must have)
    ('faeria', 'Red', 'fixed', 1.5),  # 9 Nov 2026: Red is Faeria's fixed-damage faction
    ('faeria', 'Red', 'strikes', 1.0),  # and its units strike too; one number used to hide that
    ('inscryption', 'Undead', 'strong', 0.9),  # 0.75 when 4 Bones counted as 4 Blood (SUPPLIES)
]
GAPS = [('inscryption', 'disrupts'), ('sts1', 'tall')]  # must have no value: 5 cards in the whole game; a game with no units
HAS = [('monster_train', 'wide'), ('monster_train', 'tall'), ('gwent', 'strikes'), ('gwent', 'keeps'),  # must have a value:
       ('duelyst', 'pos'), ('faeria', 'pos'), ('stormbound', 'pos')]  # width by unit cost; growth of Gwent's one number; position in the board games
MIN_DECK_CARDS = 10  # Faeria Pandora has 1 card in decks
SPOKES = [  # (key, axis number, axis name, this end, concepts); "concept@game,game" counts only in those games (the check of 9 Nov 2026)  # in circle order: neighbours belong together
    ('strong', 9, 'Unit stats', 'strength', ['strength*']),
    ('strikes', 3, 'Damage', 'units\' own strikes', ['attack_gain@duelyst,faeria,gwent,inscryption,monster_train,runeterra,stormbound,sts1',
        'on_attack@duelyst,faeria,into_the_breach,monster_train,runeterra,stormbound,sts1', 'multi_attack', 'first_strike',
        'attack_now', 'excess_damage', 'counterattack', 'on_fight', 'piercing']),
    ('kills', 2, 'Enemy units', 'kills them', ['kill*', 'removal', 'deathtouch']),
    ('fixed', 3, 'Damage', 'fixed damage', ['direct_damage@duelyst,faeria,stormbound',
        'ping@duelyst,faeria,gwent,inscryption,monster_train,runeterra,stormbound',
        'aoe_damage@faeria,gwent,inscryption,into_the_breach,runeterra,stormbound,sts1', 'damage_over_time',
        'spell_power@duelyst,monster_train,runeterra,sts1', 'board_wipe@duelyst,faeria,gwent,into_the_breach,runeterra,stormbound']),
    ('many', 6, 'Targets', 'many at once', ['aoe_damage@faeria,gwent,inscryption,into_the_breach,runeterra,stormbound,sts1',
        'board_wipe', 'multi_target_attack@into_the_breach,runeterra', 'rows@duelyst,into_the_breach', 'row_effects', 'area_templates', 'countboard*']),
    ('disrupts', 2, 'Enemy units', 'breaks their plan', ['disrupt*', 'disruption']),
    ('one', 6, 'Targets', 'one chosen', ['target_choice', 'mark_target@duelyst,gwent,runeterra,sts1']),
    ('hand', 8, 'Hand and discard pile', 'picks, brings back', ['recycle', 'copy', 'return_to_hand', 'tutor', 'revive',
        'retain', 'selection@faeria,gwent,runeterra,sts1']),
    ('economy', 4, 'Supply and cards', 'more supply, cards', ['resource_gain', 'base_resource_gain', 'resource_banking', 'draw',
        'cost_reduction@duelyst,faeria,gwent,marvel_snap,monster_train,runeterra,stormbound,sts1', 'generate_cards',
        'free_play@gwent,inscryption,monster_train,runeterra,stormbound,sts1', 'coin_economy', 'cost_set', 'in_hand_buff']),
    ('wide', 7, 'Width', 'many cheap units', ['cheapunit*', 'summon@duelyst,faeria,gwent,inscryption,marvel_snap,monster_train,runeterra,stormbound']),
    ('spends', 1, 'Own units', 'spends them', ['sacrifice@duelyst,faeria,gwent,inscryption,into_the_breach,marvel_snap,monster_train,runeterra,stormbound', 'self_destruct@gwent,into_the_breach,stormbound',
        'death_trigger@duelyst,faeria,gwent,inscryption,marvel_snap,monster_train,runeterra,stormbound',
        'other_death_trigger@duelyst,faeria,gwent,inscryption,marvel_snap,monster_train,runeterra', 'on_sacrifice',
        'death_count@faeria,gwent,marvel_snap,monster_train,runeterra', 'friendly_fire@inscryption,runeterra,stormbound']),
    ('together', 5, 'Works with others', 'position and combos', ['position*', 'combo*']),
    ('keeps', 1, 'Own units', 'keeps them alive', ['heal@duelyst,gwent,into_the_breach,monster_train,runeterra,stormbound',
        'regeneration@duelyst,gwent,into_the_breach,monster_train,runeterra,stormbound',
        'defence_gain@duelyst,faeria,gwent,inscryption,into_the_breach,monster_train,runeterra,stormbound',
        'shield@duelyst,faeria,gwent,inscryption,into_the_breach,monster_train,runeterra', 'protection',
        'immunity@duelyst,faeria,gwent,inscryption,into_the_breach', 'cheat_death',
        'damage_reduction@duelyst,faeria,gwent,inscryption,monster_train,runeterra', 'block_armor@gwent,monster_train', 'tank']),
    ('tough', 9, 'Unit stats', 'defence', ['defence*']),
    ('tall', 7, 'Width', 'a few big units', ['dearunit*']),
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
    """does a card with concepts ks, of this game, count for a spoke"""
    for k in concepts:
        name, _, only = k.partition('@')
        if name in ks and (not only or game in only.split(',')): return True
    return False


def tag(c, x, games):
    """card -> its concepts, plus the starred ones this file adds"""
    con = collections.defaultdict(set)
    for card, k in c.execute('select card, concept from flat_concept'):
        con[card].add(k)
    for card, k in c.execute("select card, concept from flat_do where on_side='enemy' and coalesce(on_kind,'')!='player' and "
                             + faction_asks.ROW_ORIGIN):
        if k in DISRUPT_ON_ENEMY: con[card].add('disrupt*')
        if k in KILL_ON_ENEMY: con[card].add('kill*')
    for (card,) in c.execute("select card from flat_if where test='amount_count' and of_kind='unit' and of_zone='board' and " + faction_asks.ROW_ORIGIN):
        con[card].add('countboard*')
    for q in BESIDE:
        for (card,) in c.execute(q + faction_asks.ROW_ORIGIN): con[card].add('position*')
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
        hi = third(lambda t: sum(1 for v in costs if v >= t))  # (most Monster Train units cost 1: cheap is 0, dear is 2 and more)
        for i in pool:
            ks, v = con[i], stats[i][1]
            if ks & set(DISRUPT_ALWAYS) or ('junk_cards' in ks and g in JUNK_GAMES): ks.add('disrupt*')
            if ks & set(POSITION) and g in POSITION_GAMES: ks.add('position*')
            if stats[i][0] not in UNIT_CATS or v is None or lo is None or lo >= hi: continue
            if v <= lo: ks.add('cheapunit*')
            if v >= hi: ks.add('dearunit*')
    return con, pools, stats


def main():
    c = sqlite3.connect('cards.sqlite')
    games = sorted({g for (g,) in c.execute('select distinct game from card')})
    x = faction_asks.Ctx(c, games, None, {})
    con, pools, stats = tag(c, x, games)
    if '--cards' in sys.argv:
        return dump(c, x, games, con, pools, sys.argv[sys.argv.index('--cards') + 1])
    lacks = {(g, s[0]) for g in games for s in SPOKES if s[0] != 'together' and (
             sum(1 for i in pools[g] if stats[i][2 + NUMERIC[s[0]]] is not None and stats[i][0] in UNIT_CATS) if s[0] in NUMERIC
             else sum(1 for i in pools[g] if counts(con[i], g, s[4]))) < MIN_GAME_CARDS}
    no_pos = {g for g in games if sum(1 for i in pools[g] if 'position*' in con[i]) < MIN_GAME_CARDS}
    pairs = set()
    for a, b in sqlite3.connect('links.sqlite').execute('select a, b from link'):
        if a != b: pairs.add((min(a, b), max(a, b)))
    deck_n = collections.Counter()  # (game, card name) -> decks that play it
    with open('decks.tsv', encoding='utf-8') as f:
        next(f)
        for line in f:
            p = line.rstrip('\n').split('\t')
            if len(p) >= 4:
                for nm in {n.strip().lower() for n in p[3].split(',') if n.strip()}:
                    deck_n[(p[0], nm)] += 1
    rows = []
    for g in games:
        pool = pools[g]
        for fac in x.factions(g):
            ids = [i for i, v in pool.items() if fac in v[3]]
            w_decks = {i: deck_n[(g, pool[i][0].lower())] for i in ids if deck_n[(g, pool[i][0].lower())]}
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
    data = {'spokes': [{'key': s[0], 'n': s[1], 'axis': s[2], 'end': s[3], 'concepts': [shown(k) for k in s[4]]} for s in SPOKES],
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
    for want, pairs_ in ((False, GAPS), (True, HAS)):
        for g, key in pairs_:
            if any((r['cards'][key + '_v'] is not None) != want for r in rows if r['game'] == g):
                print(f'CHECK FAILED: {g} {key} should have ' + ('a value' if want else 'no value'))
    print(len(rows), 'factions;', sum(1 for r in rows if r['decks']), 'with decks')


def shown(k):
    name, _, only = k.partition('@')
    return SHOWN.get(name, name) + (' (only ' + ', '.join(only.split(',')) + ')' if only else '')


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
        for key, n, axis, end, cons in SPOKES:
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
