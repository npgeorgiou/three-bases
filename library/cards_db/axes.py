"""The wheel axes (factions/12-mechanical-wheel.txt) measured on a scale for every real faction of the library.

Run from library/cards_db: python3 axes.py  ->  writes axes.tsv and ../../factions/wheel-axes.html
Each axis has a "high" end and, for most, a "low" end, each a list of library concepts (Claude's choice of concepts,
written below so it can be checked and changed). A card counts for an end if it has any of its concepts.
  score = share of the faction's cards with the high end - share with the low end   (numeric axes: the number itself)
  then centred within its game (minus the mean of that game's factions), then scaled over all factions (z-score).
Two counts: "cards" = every card of the faction once; "decks" = each faction card weighted by how many of the
library's top decks (decks.tsv) play it. Axis 11 has four ends and is four spokes; axis 12's rows part is not measured.
"""
import collections, json, math, os, sqlite3, sys
import faction_asks, mechanics

MIN_DECK_CARDS = 10  # fewer of a faction's cards in decks.tsv than this: no deck measure (Faeria Pandora has 1)
AXES = [  # (key, label, high end, low end, high concepts, low concepts, axis number in factions/12)
    ('spend', 'Spends own units / keeps them', 'spends', 'keeps',
     ['sacrifice', 'self_destruct', 'death_trigger', 'other_death_trigger', 'on_sacrifice', 'death_count', 'friendly_fire'],
     ['heal', 'regeneration', 'shield', 'protection', 'immunity', 'cheat_death', 'damage_reduction', 'block_armor', 'permanent_growth'], 1),
    ('lock', 'Locks enemies / outmoves them', 'locks', 'outmoves',
     ['cant_attack', 'immobilize', 'disable', 'silence', 'stat_loss', 'debuff', 'attack_lock', 'cant_move', 'exhaust', 'attack_zero'],
     ['evasion', 'stealth', 'movement', 'haste', 'ranged', 'cross_lane', 'piercing'], 2),
    ('strikes', 'Damage from strikes / from spells', 'unit strikes', 'spells, fixed damage',
     ['attack_gain', 'on_attack', 'multi_attack', 'first_strike', 'attack_now', 'excess_damage'],
     ['direct_damage', 'ping', 'aoe_damage', 'damage_over_time', 'spell_power', 'board_wipe'], 3),
    ('economy', 'Supply and cards / board now', 'supply, cards', 'board now',
     ['resource_gain', 'base_resource_gain', 'round_carryover', 'resource_banking', 'draw', 'cost_reduction',
      'generate_cards', 'tutor', 'free_play', 'coin_economy', 'shop_gold'], [], 4),
    ('formation', 'Formation / alone', 'formation', 'alone',
     ['adjacency', 'aura', 'link_formation', 'flanking', 'assists_support'], [], 5),
    ('many', 'Many targets / one target', 'many', 'one',
     ['aoe_damage', 'board_wipe', 'count_payoff', 'multi_target_attack', 'rows', 'row_effects', 'area_templates', 'symmetric_effect'],
     ['target_choice', 'mark_target'], 6),
    ('size', 'Unit size (average unit cost)', 'few big', 'many cheap', None, None, 7),
    ('moving', 'Moving / staying', 'moves', 'stays', ['movement', 'forced_movement', 'swap', 'bounce_enemy', 'cross_lane'], [], 8),
    ('repair', 'Repair / prevent', 'repairs', 'prevents',
     ['heal', 'regeneration'], ['shield', 'damage_reduction', 'immunity', 'block_armor', 'protection', 'taunt', 'cheat_death'], 9),
    ('hand', 'Picks and brings back cards / plays what it draws', 'picks, brings back', 'plays its draws',
     ['recycle', 'copy', 'return_to_hand', 'tutor', 'revive', 'retain', 'selection', 'in_hand_buff'], [], 10),
    ('r_place', 'Reacts to: being placed', 'placed', '', ['on_play', 'on_ally_play'], [], 11),
    ('r_attack', 'Reacts to: attacking', 'attacking', '', ['on_attack', 'on_kill', 'on_fight', 'combat_start'], [], 11),
    ('r_hit', 'Reacts to: being hit', 'hit', '', ['on_damaged', 'on_targeted', 'counterattack', 'on_block'], [], 11),
    ('r_death', 'Reacts to: dying', 'dying', '', ['death_trigger', 'other_death_trigger', 'leave_trigger', 'other_leave_trigger'], [], 11),
    ('area', 'Hits a row or area / one cell', 'row, area', 'one cell', ['rows', 'row_effects', 'area_templates'], [], 12),
    ('speed', 'Speed (average card cost, low = fast)', 'fast', 'slow', None, None, 13),
    ('power', 'Strength / defence (unit stats in strength)', 'strength', 'defence', None, None, 14),
    ('pace', 'Sets the pace / answers', 'sets pace', 'answers',
     ['haste', 'attack_now', 'forced_attack', 'nexus_damage_condition'],
     ['reactions', 'counter_spell', 'trap_secret', 'on_targeted', 'counterattack'], 15),
    ('hard', 'Hard to play (choices on cards)', 'many choices', 'few', ['modal_choice', 'target_choice', 'activated', 'combo_sequence',
                                                                        'selection', 'kicker', 'stances'], [], 16),
]


def main():
    c = sqlite3.connect('cards.sqlite')
    games = sorted({g for (g,) in c.execute('select distinct game from card')})
    x = faction_asks.Ctx(c, games, None, {})
    con = collections.defaultdict(set)
    for card, k in c.execute('select card, concept from flat_concept'):
        con[card].add(k)
    stats = {i: (cat, cost, p, h) for i, cat, cost, p, h in c.execute('select id, category, cost, power, health from card')}
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
        pool = x.pool(g)
        for fac in x.factions(g):
            ids = [i for i, v in pool.items() if fac in v[3]]
            w_cards = {i: 1 for i in ids}
            w_decks = {i: deck_n[(g, pool[i][0].lower())] for i in ids if deck_n[(g, pool[i][0].lower())]}
            rec = {'game': g, 'faction': fac, 'n_cards': len(ids), 'deck_cards': len(w_decks)}
            rec['cards'] = measure(w_cards, con, stats)
            rec['decks'] = measure(w_decks, con, stats) if len(w_decks) >= MIN_DECK_CARDS else None
            rows.append(rec)
    for mode in ('cards', 'decks'):
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
    data = {'axes': [{'key': a[0], 'label': a[1], 'hi': a[2], 'lo': a[3], 'hiC': a[4], 'loC': a[5], 'n': a[6]} for a in AXES],
            'factions': [{'game': r['game'], 'faction': r['faction'], 'cards': r['n_cards'], 'deckCards': r['deck_cards'],
                          'cardsZ': zz(r['cards']), 'decksZ': zz(r['decks']),
                          'cardsRaw': raw(r['cards']), 'decksRaw': raw(r['decks'])} for r in rows]}
    tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tools', 'wheel_axes_template.html'), encoding='utf-8').read()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'factions', 'wheel-axes.html')
    open(out, 'w', encoding='utf-8').write(tpl.replace('/*DATA*/null', json.dumps(data, ensure_ascii=False)))
    print(len(rows), 'factions;', sum(1 for r in rows if r['decks']), 'with decks')


def fmt(v): return '' if v is None else f'{v:.4f}'
def zz(m): return None if not m else {a[0]: m.get(a[0] + '_z') for a in AXES}
def raw(m): return None if not m else {a[0]: (None if m[a[0]] is None else round(m[a[0]], 4)) for a in AXES}


def measure(w, con, stats):
    tot = sum(w.values())
    out = {}
    for key, _, _, _, hi, lo, _ in AXES:
        if hi is None: continue
        sh = sum(n for i, n in w.items() if con[i] & set(hi)) / tot
        sl = sum(n for i, n in w.items() if con[i] & set(lo)) / tot if lo else 0
        out[key] = sh - sl
    units = [(i, n) for i, n in w.items() if stats[i][0] in ('unit', 'hero', 'leader') and stats[i][1] is not None]
    allc = [(i, n) for i, n in w.items() if stats[i][1] is not None]
    out['size'] = sum(stats[i][1] * n for i, n in units) / sum(n for _, n in units) if units else None
    out['speed'] = -sum(stats[i][1] * n for i, n in allc) / sum(n for _, n in allc) if allc else None
    ps = [(stats[i][2] or 0, stats[i][3] or 0, n) for i, n in units if (stats[i][2] or 0) + (stats[i][3] or 0) > 0]
    out['power'] = sum(p * n for p, h, n in ps) / sum((p + h) * n for p, h, n in ps) if ps else None
    return out


if __name__ == '__main__':
    main()
