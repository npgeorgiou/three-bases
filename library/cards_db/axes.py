"""The wheel axes (factions/12-mechanical-wheel.txt) measured on a scale for every real faction of the library.

Run from library/cards_db: python3 axes.py  ->  writes axes.tsv and ../../factions/wheel-axes.html
Each axis has a "high" end and, for most, a "low" end, each a list of library concepts (Claude's choice of concepts,
written below so it can be checked and changed). A card counts for an end if it has any of its concepts.
  score = share of the faction's cards with the high end - share with the low end   (numeric axes: the number itself)
  then centred within its game (minus the mean of that game's factions), then scaled over all factions (z-score).
Two counts: "cards" = every card of the faction once; "decks" = each faction card weighted by how many of the
library's top decks (decks.tsv) play it. Axis 5 (works with others) = the average of two scales: the share of position cards and the share of the faction's card
pairs that links.sqlite links (run links.py first). speed_test() checks axis 9 against deck names; it is not proven, so the page starts with it off.
A game with fewer than MIN_GAME_CARDS cards for both ends of an axis gives its factions no value on it (a gap).
Disruption (axis 2): a card breaks the enemy's plan if one of its effects lands on the enemy (side 'enemy') with a concept of
DISRUPT_ON_ENEMY, or it has a concept of DISRUPT_ALWAYS; it only kills if an effect on the enemy is in KILL_ON_ENEMY.
"""
import collections, json, math, os, re, sqlite3
import faction_asks, mechanics

DISRUPT_ON_ENEMY = ['cant_attack', 'stat_gain', 'stat_loss', 'disable', 'forced_attack', 'forced_movement', 'debuff', 'steal',
                    'attack_zero', 'silence', 'stat_multiply', 'bounce_enemy', 'polymorph', 'discard', 'immobilize', 'cant_move',
                    'attack_lock', 'counter_spell', 'transform', 'return_to_hand']
DISRUPT_ALWAYS = ['hand_disruption', 'mill', 'junk_cards', 'board_clog', 'cost_increase', 'play_restriction', 'counter_spell',
                  'steal', 'immobilize', 'attack_lock', 'silence', 'disable', 'bounce_enemy']
KILL_ON_ENEMY = ['damage', 'excess_damage', 'destroy', 'banish', 'damage_over_time', 'aoe_damage', 'ping', 'direct_damage', 'board_wipe']
SHOWN = {'disrupt*': 'on enemies: ' + ', '.join(DISRUPT_ON_ENEMY) + '; any card with: ' + ', '.join(DISRUPT_ALWAYS),
         'kill*': 'on enemies: ' + ', '.join(KILL_ON_ENEMY)}
POSITION = ['adjacency', 'aura', 'link_formation', 'flanking', 'assists_support']
GROWS_LATE = ['permanent_growth', 'round_carryover', 'resource_banking', 'base_resource_gain', 'resource_gain', 'countdown', 'delayed']
SHOWN.update({'position*': 'position: ' + ', '.join(POSITION),
              'combo*': 'combos: how many pairs of the faction\'s cards the library links (links.sqlite), out of all pairs',
              'cheap*': 'any card in the cheapest third of its game', 'dear*': 'any card in the dearest third of its game',
              'cheapunit*': 'a unit in the cheapest third of its game', 'dearunit*': 'a unit in the dearest third of its game'})
UNIT_CATS = ('unit', 'hero', 'leader')
SHOWN.update({'threat*': 'a unit in the cheapest third of its game with more strength than defence',
              'grows*': 'grows for good at the start or end of every round (must be answered)',
              'enemy_sets_off*': 'its effect is set off by something the enemy does'})
MIN_GAME_CARDS = 5  # a game with fewer cards than this for both ends of an axis gives its factions no value on it
MIN_DECK_CARDS = 10  # fewer of a faction's cards in decks.tsv than this: no deck measure (Faeria Pandora has 1)
AXES = [  # (key, label, high end, low end, high concepts, low concepts, axis number in factions/12)
    ('spend', 'Spends own units / keeps them', 'spends', 'keeps',
     ['sacrifice', 'self_destruct', 'death_trigger', 'other_death_trigger', 'on_sacrifice', 'death_count', 'friendly_fire'],
     ['heal', 'regeneration', 'shield', 'protection', 'immunity', 'cheat_death', 'damage_reduction', 'block_armor', 'permanent_growth'], 1),
    ('disrupt', 'Breaks the enemy\'s plan / only kills its units', 'breaks plan', 'only kills', ['disrupt*'], ['kill*'], 2),
    ('strikes', 'Damage from strikes / from spells', 'unit strikes', 'spells, fixed damage',
     ['attack_gain', 'on_attack', 'multi_attack', 'first_strike', 'attack_now', 'excess_damage'],
     ['direct_damage', 'ping', 'aoe_damage', 'damage_over_time', 'spell_power', 'board_wipe'], 3),
    ('economy', 'Supply and cards / board now', 'supply, cards', 'board now',
     ['resource_gain', 'base_resource_gain', 'round_carryover', 'resource_banking', 'draw', 'cost_reduction',
      'generate_cards', 'tutor', 'free_play', 'coin_economy', 'shop_gold'], [], 4),
    ('together', 'Works with other cards (position and combos) / alone', 'with others', 'alone', ['position*', 'combo*'], [], 5),
    ('many', 'Many targets / one target', 'many', 'one',
     ['aoe_damage', 'board_wipe', 'count_payoff', 'multi_target_attack', 'rows', 'row_effects', 'area_templates', 'symmetric_effect'],
     ['target_choice', 'mark_target'], 6),
    ('size', 'Many cheap units / few big', 'many cheap', 'few big', ['cheapunit*', 'summon'], ['dearunit*'], 7),
    ('hand', 'Picks and brings back cards / plays what it draws', 'picks, brings back', 'plays its draws',
     ['recycle', 'copy', 'return_to_hand', 'tutor', 'revive', 'retain', 'selection', 'in_hand_buff'], [], 8),
    ('speed', 'Strongest early / late (not proven)', 'early', 'late', ['cheap*', 'haste', 'attack_now', 'threat*'],
     ['dear*'] + GROWS_LATE, 9),
    ('power', 'Strength / defence (unit stats in strength)', 'strength', 'defence', None, None, 10),
    ('pace', 'Sets the pace / answers', 'sets pace', 'answers',
     ['haste', 'attack_now', 'forced_attack', 'threat*', 'grows*'],
     ['reactions', 'counter_spell', 'trap_secret', 'on_targeted', 'counterattack', 'spell_speed', 'enemy_sets_off*'], 11),
]


def main():
    c = sqlite3.connect('cards.sqlite')
    games = sorted({g for (g,) in c.execute('select distinct game from card')})
    x = faction_asks.Ctx(c, games, None, {})
    con = collections.defaultdict(set)
    for card, k in c.execute('select card, concept from flat_concept'):
        con[card].add(k)
    for card, k in c.execute("select card, concept from flat_do where on_side='enemy' and " + faction_asks.ROW_ORIGIN):
        if k in DISRUPT_ON_ENEMY: con[card].add('disrupt*')
        if k in KILL_ON_ENEMY: con[card].add('kill*')
    for card, ks in list(con.items()):
        if ks & set(DISRUPT_ALWAYS): ks.add('disrupt*')
    stats = {i: (cat, cost, p, h) for i, cat, cost, p, h in c.execute('select id, category, cost, power, health from card')}
    pools = {g: x.pool(g) for g in games}
    for g, pool in pools.items():
        costs = sorted(v[2] for v in pool.values() if v[2] is not None)
        if not costs: continue
        lo, hi = costs[len(costs) // 3], costs[2 * len(costs) // 3]
        for i, v in pool.items():
            if v[2] is None or lo == hi: continue
            unit = stats[i][0] in UNIT_CATS
            if v[2] <= lo: con[i].add('cheap*'); unit and con[i].add('cheapunit*')
            if v[2] >= hi: con[i].add('dear*'); unit and con[i].add('dearunit*')
    for i, ks in con.items():
        if ks & set(POSITION): ks.add('position*')
        if 'permanent_growth' in ks and ks & {'turn_start', 'turn_end'}: ks.add('grows*')
        if 'cheapunit*' in ks and (stats[i][2] or 0) > (stats[i][3] or 0): ks.add('threat*')
    for (i,) in c.execute("select distinct card from flat_when where actor_side='enemy'"):
        con[i].add('enemy_sets_off*')
    lacks = {(g, a[0]) for g in games for a in AXES if a[4] is not None and a[0] != 'together'
             and sum(1 for i in pools[g] if con[i] & set(a[4] + a[5])) < MIN_GAME_CARDS}
    pairs = set()
    L = sqlite3.connect('links.sqlite')
    for a, b in L.execute('select a, b from link'):
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
            w_cards = {i: 1 for i in ids}
            w_decks = {i: deck_n[(g, pool[i][0].lower())] for i in ids if deck_n[(g, pool[i][0].lower())]}
            rec = {'game': g, 'faction': fac, 'n_cards': len(ids), 'deck_cards': len(w_decks)}
            rec['cards'] = measure(w_cards, con, stats, pairs)
            rec['decks'] = measure(w_decks, con, stats, pairs) if len(w_decks) >= MIN_DECK_CARDS else None
            for m in ('cards', 'decks'):
                for g2, k in lacks:
                    if g2 == g and rec[m]: rec[m][k] = None
            rows.append(rec)
    for mode in ('cards', 'decks'):
        ms = [r[mode] for r in rows if r[mode]]
        for part in ('pos', 'combo'):  # "works with others": the two parts on one footing, then averaged
            for g in games:
                gm = [r[mode] for r in rows if r['game'] == g and r[mode]]
                m = sum(q[part] for q in gm) / len(gm) if gm else 0
                for q in gm: q[part + '_c'] = q[part] - m
            sd = math.sqrt(sum(q[part + '_c'] ** 2 for q in ms) / len(ms)) or 1
            for q in ms: q[part + '_z'] = q[part + '_c'] / sd
        for q in ms: q['together'] = (q['pos_z'] + q['combo_z']) / 2
        for a in AXES:
            k = a[0]
            for g in games:
                vals = [r[mode][k] for r in rows if r['game'] == g and r[mode] and r[mode][k] is not None]
                m = sum(vals) / len(vals) if vals else 0
                for r in rows:
                    if r['game'] == g and r[mode] and r[mode][k] is not None:
                        r[mode][k + '_c'] = r[mode][k] - m
            cs = [r[mode][k + '_c'] for r in rows if r[mode] and k + '_c' in r[mode]]
            sd = math.sqrt(sum(v * v for v in cs) / len(cs)) or 1
            for r in rows:
                if r[mode] and k + '_c' in r[mode]:
                    r[mode][k + '_z'] = round(r[mode][k + '_c'] / sd, 3)
    with open('axes.tsv', 'w', encoding='utf-8') as f:
        f.write('game\tfaction\tcards\tdeck_cards\tmode\t' + '\t'.join(f'{a[0]}_raw\t{a[0]}_scale' for a in AXES) + '\n')
        for r in rows:
            for mode in ('cards', 'decks'):
                if not r[mode]: continue
                f.write(f"{r['game']}\t{r['faction']}\t{r['n_cards']}\t{r['deck_cards']}\t{mode}\t" +
                        '\t'.join(f"{fmt(r[mode][a[0]])}\t{fmt(r[mode].get(a[0] + '_z'))}" for a in AXES) + '\n')
    data = {'axes': [{'key': a[0], 'label': a[1], 'hi': a[2], 'lo': a[3], 'hiC': a[4] and [SHOWN.get(k, k) for k in a[4]], 'loC': a[5] and [SHOWN.get(k, k) for k in a[5]], 'n': a[6], 'off': a[0] == 'speed'} for a in AXES],
            'factions': [{'game': r['game'], 'faction': r['faction'], 'cards': r['n_cards'], 'deckCards': r['deck_cards'],
                          'cardsZ': zz(r['cards']), 'decksZ': zz(r['decks']),
                          'cardsRaw': raw(r['cards']), 'decksRaw': raw(r['decks'])} for r in rows]}
    tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'wheel_axes_template.html'), encoding='utf-8').read()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'factions', 'wheel-axes.html')
    open(out, 'w', encoding='utf-8').write(tpl.replace('/*DATA*/null', json.dumps(data, ensure_ascii=False)))
    speed_test(con, stats, pools, pairs)
    print(len(rows), 'factions;', sum(1 for r in rows if r['decks']), 'with decks')


DECK_LEAN = [(re.compile(r'\b(aggro|rush|tempo)\b', re.I), 0), (re.compile(r'\bmidrange\b', re.I), 1),
             (re.compile(r'\b(control|ramp)\b', re.I), 2)]  # the deck author's own word: 0 early, 1 middle, 2 late


def speed_test(con, stats, pools, pairs):
    """The early/late axis checked against deck authors' own words (DECK_LEAN): of two decks of one game with different
    words, the earlier-named one should score earlier. Prints, per game, how many such pairs the axis orders right, and
    the same for plain average cost (lower = earlier) to compare."""
    got = collections.defaultdict(list)
    with open('decks.tsv', encoding='utf-8') as f:
        next(f)
        for line in f:
            g, name, _, cards = (line.rstrip('\n').split('\t') + [''] * 4)[:4]
            lean = {v for rx, v in DECK_LEAN if rx.search(name)}
            if len(lean) != 1: continue
            by = {v[0].lower(): i for i, v in pools.get(g, {}).items()}
            w = {by[n.strip().lower()]: 1 for n in cards.split(',') if n.strip().lower() in by}
            if len(w) < 5: continue
            cs = [stats[i][1] for i in w if stats[i][1] is not None]
            got[g].append((lean.pop(), measure(w, con, stats, pairs)['speed'], -sum(cs) / len(cs), name))
    tot = collections.Counter()
    for g, ds in sorted(got.items()):
        n = ax = cost = 0
        for i, d in enumerate(ds):
            for e in ds[i + 1:]:
                if d[0] == e[0]: continue
                early, late = (d, e) if d[0] < e[0] else (e, d)
                n += 1; ax += early[1] > late[1]; cost += early[2] > late[2]
        if not n: continue
        tot['n'] += n; tot['ax'] += ax; tot['cost'] += cost
        print(f'early/late check {g}: {len(ds)} named decks, {n} pairs; axis right {ax}, average cost right {cost}')
    if tot['n']:
        print(f"early/late check, all: {tot['n']} pairs; axis right {tot['ax'] / tot['n']:.0%}, average cost right {tot['cost'] / tot['n']:.0%}")


def fmt(v): return '' if v is None else f'{v:.4f}'
def zz(m): return None if not m else {a[0]: m.get(a[0] + '_z') for a in AXES}
def raw(m): return None if not m else {a[0]: (None if m[a[0]] is None else round(m[a[0]], 4)) for a in AXES}


def measure(w, con, stats, pairs):
    tot = sum(w.values())
    out = {}
    for key, _, _, _, hi, lo, _ in AXES:
        if hi is None or key == 'together': continue
        sh = sum(n for i, n in w.items() if con[i] & set(hi)) / tot
        sl = sum(n for i, n in w.items() if con[i] & set(lo)) / tot if lo else 0
        out[key] = sh - sl
    out['pos'] = sum(n for i, n in w.items() if 'position*' in con[i]) / tot
    ids = sorted(w)
    linked = sum(w[a] * w[b] for k, a in enumerate(ids) for b in ids[k + 1:] if (a, b) in pairs)
    allp = (tot * tot - sum(n * n for n in w.values())) / 2
    out['combo'] = linked / allp if allp else 0
    out['together'] = None
    units = [(i, n) for i, n in w.items() if stats[i][0] in UNIT_CATS and stats[i][1] is not None]
    ps = [(stats[i][2] or 0, stats[i][3] or 0, n) for i, n in units if (stats[i][2] or 0) + (stats[i][3] or 0) > 0]
    out['power'] = sum(p * n for p, h, n in ps) / sum((p + h) * n for p, h, n in ps) if ps else None
    return out


if __name__ == '__main__':
    main()
