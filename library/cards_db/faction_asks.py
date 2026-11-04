"""Faction design questions over cards.sqlite (run through ask.py): palette, curve, spells, removal, protect, ways, scaling,
only, lacks. Every answer comes from the stored rows and the concept tree only, the same way for every game."""
import collections
import mechanics, network

NOT_FACTION = ('neutral', 'boss', 'any', 'colorless', 'curse', 'status', 'token', 'event', 'shared', 'universal', 'tutorial',
               'clanless', 'runeterra')  # no faction of its own
SKIP_CAT = ('game_rule', 'tribe', 'boss', 'monster', 'event', 'modifier')  # not a player's card
MIN_FACTION = 10  # smaller "factions" (Into the Breach's 3-card corporations) are left out of game-wide tables
ROW_ORIGIN = "origin in ('own','has_keyword','gives')"  # the card's own rows, not the rows of keywords it hands to others
ALIAS = {'place': ['on_play'], 'play': ['on_play'], 'death': ['death_trigger'], 'ally_dies': ['other_death_trigger'],
         'spell_cast': ['on_spell'], 'round_end': ['turn_end', 'round_end'], 'round_start': ['turn_start', 'round_start']}
REMOVAL = [('kill', ['destroy', 'banish', 'board_wipe', 'deathtouch']), ('damage', ['damage']),
           ('push away', ['bounce_enemy', 'forced_movement']), ('take strength', ['debuff']), ('stop', ['suppress']),
           ('transform', ['polymorph']), ('steal', ['steal'])]
PROTECT = [('armour', ['damage_reduction']), ('shield', ['shield']), ('immunity', ['immunity']), ('survive death', ['cheat_death']),
           ('guard', ['bodyguard', 'taunt']), ('hide', ['stealth']), ('heal', ['heal'])]
PAID = ('discard', 'sacrifice', 'self_destruct', 'life_payment', 'donate', 'self_mill')  # given up whoever it lands on
HARMED = ('destroy', 'banish', 'damage', 'debuff')  # given up when it lands on my own side
NOT_GIVEN = ('excess_damage', 'lifesteal', 'multi_target_attack')  # under damage, but a gain for the owner
COND_TESTS = ('have', 'event_count', 'count', 'keyword_condition', 'it_matches', 'first_card', 'level', 'stat', 'max_mana', 'upgraded')


class Ctx:
    def __init__(self, c, games, text, sub):
        self.c, self.games, self.text, self.sub = c, games, text, sub
        self.under = lambda v, x: v == x or v in sub.get(x, ())

    def pool(self, game):
        """the player cards of one game: id -> (name, category, cost, factions)"""
        out = {}
        for i, cat, cost, regs in self.c.execute(
                f"select id, category, cost, regions from card where game=? and is_keyword=0 and is_stub=0 and coalesce(category,'') "
                f"not in ({','.join(repr(x) for x in SKIP_CAT)}) and not (category='ability' and id in (select made from flat_made))", (game,)):
            fs = [r for r in (regs or '').split(';') if r and not r.lower().startswith(NOT_FACTION)]
            out[i] = (mechanics.name(self.c, i), cat or '', cost, fs)
        return out

    def factions(self, game):
        n = collections.Counter(f for _, _, _, fs in self.pool(game).values() for f in fs)
        return [f for f, k in n.most_common() if k >= MIN_FACTION]

    def find(self, name):
        """(game, faction, its card ids) for a faction name in the chosen games"""
        for g in self.games:
            for f in sorted({f for _, _, _, fs in self.pool(g).values() for f in fs}):
                if f.lower() == name.lower():
                    return g, f, [i for i, x in self.pool(g).items() if f in x[3]]
        print(f'No faction "{name}" in {", ".join(self.games)}. Factions: ' +
              '; '.join(f'{g}: {", ".join(self.factions(g))}' for g in self.games))
        return None

    def rows(self, ids, extra=''):
        """effect rows of these cards: (card, ability, seq, act, concept, kind, side, pick, link)"""
        if not ids: return []
        return list(self.c.execute(f"select card, ability, seq, act, concept, on_kind, on_side, on_pick, link from flat_do where {ROW_ORIGIN} "
                                   f"and card in ({','.join(map(str, ids))}){extra} order by card, ability, seq"))

    def triggers(self, ids):
        """card, ability -> the trigger's concept (or its event when the event has no concept)"""
        out = {}
        if not ids: return out
        for card, ab, ev, con in self.c.execute(f"select card, ability, event, concept from flat_when where {ROW_ORIGIN} and card in "
                                                f"({','.join(map(str, ids))})"):
            out.setdefault((card, ab), con or ev)
        return out

    def example(self, i, n=80): return f'{mechanics.name(self.c, i)}: {self.text(i, n)}'


def target(kind, side, pick):
    """who an effect lands on, in words: "chosen enemy unit", "itself" """
    if pick == 'self': return 'itself'
    return ' '.join(x for x in ({'mine': 'my', 'enemy': 'enemy'}.get(side, side), kind) if x) if pick in (None, 'it') else \
        ' '.join(x for x in (pick, {'mine': 'my', 'enemy': 'enemy'}.get(side, side), kind) if x)


def gives_up(x, r):
    """an effect row that costs its owner: a drawback, or harm aimed at my own side"""
    _, _, _, act, con, kind, side, pick, _ = r
    if not con or act == 'give_keyword' or con in NOT_GIVEN: return False  # Fleeting on a made card is no payment
    if any(x.under(con, k) for k in PAID): return side != 'enemy'
    return (side == 'mine' or pick == 'self') and kind != 'player' and any(x.under(con, k) for k in HARMED)


def groups_out(x, groups, n_ex=2, total=None):
    """groups: label -> set of card ids; printed biggest first, with a count, share and examples"""
    for label, ids in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        share = f' ({len(ids) / total:.0%})' if total else ''
        print(f'- {label}: {len(ids)} card{'' if len(ids) == 1 else 's'}{share}')
        for i in sorted(ids, key=lambda i: mechanics.name(x.c, i))[:n_ex]: print(f'    {x.example(i)}')


def palette(x, args):
    """ask.py <games> palette <trigger> [faction]: what cards do on one trigger, grouped by what they do"""
    want = ALIAS.get(args[0].lower(), [args[0]])
    fac = ' '.join(args[1:])
    f = x.find(fac) if fac else None
    if fac and not f: return
    found = False
    for g in ([f[0]] if f else x.games):
        pool = x.pool(g)
        if f: pool = {i: pool[i] for i in f[2]}
        trig = {k for k, v in x.triggers(list(pool)).items() if any(x.under(v, w) or v == w for w in want)}
        groups = collections.defaultdict(set)
        for r in x.rows(list(pool)):
            if (r[0], r[1]) in trig and r[4]: groups[r[4]].add(r[0])
        if not groups: continue
        found = True
        print(f'## {g}{", " + fac if fac else ""}: {len({k[0] for k in trig})} cards act on {args[0]}')
        groups_out(x, groups)
    if not found: print(f'no cards act on {args[0]}' + (f' in {fac}' if fac else ''))


def curve(x, args):
    """ask.py <games> curve <faction>: the faction's cards by cost, units and spells, one line each"""
    f = x.find(' '.join(args))
    if not f: return
    g, fac, ids = f
    pool = x.pool(g); trig = x.triggers(ids)
    lines = collections.defaultdict(list)
    for card, ab, seq, act, con, kind, side, pick, link in x.rows(ids):
        if con: lines[card, ab].append(f'{con} -> {target(kind, side, pick) or "-"}')
    by_cost = collections.defaultdict(list)
    for i in ids: by_cost[pool[i][2]].append(i)
    print(f'{g}, {fac}: {len(ids)} cards')
    for cost in sorted(by_cost, key=lambda v: (v is None, v or 0)):
        cs = by_cost[cost]
        kinds = collections.Counter(pool[i][1] or 'other' for i in cs)
        rest = ', '.join(f'{n} {k}' for k, n in kinds.items() if k not in ('unit', 'spell'))
        print(f'## cost {"?" if cost is None else int(cost) if cost == int(cost) else cost}: {kinds["unit"]} units, {kinds["spell"]} spells'
              + (f', {rest}' if rest else ''))
        for i in sorted(cs, key=lambda i: (pool[i][1], pool[i][0])):
            abl = [f'{trig.get(k, "always")} -> ' + ', '.join(dict.fromkeys(v)) for k, v in lines.items() if k[0] == i]
            print(f'  {pool[i][0]} ({pool[i][1]}): ' + ('; '.join(abl) if abl else 'no effect rows'))


def spells(x, args):
    """ask.py <games> spells <faction>: the faction's spells grouped by what they do"""
    f = x.find(' '.join(args))
    if not f: return
    g, fac, ids = f
    pool = x.pool(g); sp = [i for i in ids if pool[i][1] == 'spell']
    groups = collections.defaultdict(set)
    for r in x.rows(sp):
        if r[4]: groups[r[4]].add(r[0])
    print(f'{g}, {fac}: {len(sp)} spells of {len(ids)} cards')
    for label, cs in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        print(f'- {label} ({len(cs)}): ' + ', '.join(sorted(pool[i][0] for i in cs)))


def kinds_of(x, ids, kinds, aimed):
    """card -> the group labels it has; aimed: the side the effect must not land on ('mine' for removal)"""
    out = collections.defaultdict(set)
    for r in x.rows(ids):
        card, _, _, act, con, kind, side, pick, _ = r
        if not con or kind == 'player': continue
        if act != 'give_keyword' and (side == aimed or (aimed == 'mine' and pick == 'self')): continue
        for label, cons in kinds:
            if any(x.under(con, k) for k in cons): out[card].add(label)
    if ids:  # a keyword printed on the card (Barrier, Tough, Deathtouch) works on the card itself
        for card, con in x.c.execute(f"select card, concept from flat_concept where rule='keyword' and card in ({','.join(map(str, ids))})"):
            for label, cons in kinds:
                if any(x.under(con, k) for k in cons): out[card].add(label)
    return out


def shares(x, ids, kinds, aimed, extra=None):
    got = kinds_of(x, ids, kinds, aimed)
    if extra: extra(x, ids, got)
    groups = collections.defaultdict(set)
    for card, ls in got.items():
        for l in ls: groups[l].add(card)
    return groups, len(got)


def sacrifice_to_kill(x, ids, got):
    """removal on a card that also gives up one of my own units"""
    if not ids: return
    sac = {i for (i,) in x.c.execute(f"select card from flat_concept where concept='sacrifice' and card in ({','.join(map(str, ids))})")}
    for i in sac:
        if got.get(i): got[i].add('sacrifice to kill')


def table(x, args, kinds, aimed, what, extra=None):
    """a faction's ways, with shares; given a game name instead, one line per faction of that game"""
    name = ' '.join(args)
    if name.lower() in [g.lower() for g in x.games] or name.lower() in ('game', ''):
        for g in ([name.lower()] if name.lower() in x.games else x.games):
            pool = x.pool(g)
            print(f'## {g}')
            for fac in x.factions(g):
                ids = [i for i, v in pool.items() if fac in v[3]]
                groups, n = shares(x, ids, kinds, aimed, extra)
                print(f'{fac} ({len(ids)} cards, {n} with {what}, {n / len(ids):.0%}): ' +
                      ', '.join(f'{l} {len(c) / max(1, n):.0%}' for l, c in sorted(groups.items(), key=lambda kv: -len(kv[1]))))
        return
    f = x.find(name)
    if not f: return
    g, fac, ids = f
    groups, n = shares(x, ids, kinds, aimed, extra)
    print(f'{g}, {fac}: {n} of {len(ids)} cards ({n / len(ids):.0%}) have {what}; share of those cards per way:')
    groups_out(x, groups, total=n)


def removal(x, args): table(x, args, REMOVAL, 'mine', 'removal', sacrifice_to_kill)


def protect(x, args): table(x, args, PROTECT, 'enemy', 'protection')


def ways(x, args):
    """ask.py <games> ways <faction>: the faction's groups of tightly linked cards (network.py), key cards and what ties each"""
    f = x.find(' '.join(args))
    if not f: return
    g, fac, ids = f
    m = network.measure(x.c, g, ids, broad=False)
    nm = lambda i: mechanics.name(x.c, i) + (' (made)' if m['nodes'].get(i) else '')
    print(f'{g}, {fac}: {len(m["own"])} cards, {len(m["groups"])} ways to play')
    for grp, why in m['groups']:
        w = collections.Counter(); ties = collections.Counter(); best = None
        for (a, b), (wt, kind, y) in m['best'].items():
            if a in grp and b in grp and kind not in ('levelsinto', 'targets'):
                w[a] += wt; w[b] += wt; ties[y] += 1
                if not best or wt > best[0]: best = (wt, a, y, b)
        ns = sorted(nm(i) for i in grp)
        print(f'## {len(grp)} cards: ' + ', '.join(ns[:20]) + (f' and {len(ns) - 20} more' if len(ns) > 20 else ''))
        print('  key cards: ' + ', '.join(nm(i) for i, _ in w.most_common(3)))
        print('  tied by: ' + '; '.join(f'{y} ({n} lines)' for y, n in ties.most_common(3)))
        if best: print(f'  strongest line: {nm(best[1])} -> {best[2]} -> {nm(best[3])}')


def scaling(x, args):
    """ask.py <games> scaling chain|conversion|threshold"""
    kind = args[0] if args else ''
    if kind not in ('chain', 'conversion', 'threshold'): print('scaling takes chain, conversion or threshold'); return
    for g in x.games:
        ids = list(x.pool(g)); groups = collections.defaultdict(set)
        if not ids: continue
        ab_rows = collections.defaultdict(list)
        for r in x.rows(ids): ab_rows[r[0], r[1]].append(r)
        conds = collections.defaultdict(list)
        for card, ab, test, op, n, ev, attr, ok, os_ in x.c.execute(
                f"select card, ability, test, op, n, event, attr, of_kind, of_side from flat_if where {ROW_ORIGIN} and card in ({','.join(map(str, ids))})"):
            conds[card, ab].append((test, op, n, ev, attr, ok, os_))
        for (card, ab), rs in ab_rows.items():
            if kind == 'chain':  # the effect happens again when a condition holds
                if not any(r[3] == 'repeat' or r[4] == 'repeat_trigger' for r in rs): continue
                why = [t for t, op, *_ in conds.get((card, ab), []) if op or t in COND_TESTS]
                if any(r[8] == 'if_done' for r in rs): why.append('if the first part happened')
                for w in why: groups[w].add(card)
            elif kind == 'conversion':  # gives up one thing for another
                give = [r[4] for r in rs if gives_up(x, r)]
                get = [r[4] for r in rs if r[4] and not gives_up(x, r) and (x.under(r[4], 'helps_me') or x.under(r[4], 'hurts_enemy'))]
                for a in dict.fromkeys(give):
                    for b in dict.fromkeys(get): groups[f'{a} -> {b}'].add(card)
            else:  # the effect changes once a number is reached
                for test, op, n, ev, attr, ok, os_ in conds.get((card, ab), []):
                    if op in ('ge', 'gt') and n and n >= 2:
                        what = ' '.join(v for v in (test, ev, attr, {'mine': 'my', 'enemy': 'enemy'}.get(os_, os_), ok) if v)
                        groups[what].add(card)
        if kind == 'conversion':
            for (i,) in x.c.execute(f"select card from flat_concept where concept='resource_conversion' and card in ({','.join(map(str, ids))})"):
                groups['resource_conversion'].add(i)
        if not groups: continue
        n = len(set().union(*groups.values())); print(f"## {g}: {n} card{'' if n == 1 else 's'}")
        top = dict(sorted(groups.items(), key=lambda kv: -len(kv[1]))[:15])
        groups_out(x, top)
        if len(groups) > 15: print(f'- and {len(groups) - 15} smaller groups')


def concept_counts(x, g):
    """faction -> concept -> cards with it, for one game"""
    pool = x.pool(g); facs = x.factions(g)
    per = {f: collections.defaultdict(set) for f in facs}
    for card, con in x.c.execute(f"select card, concept from flat_concept where card in ({','.join(map(str, pool))})"):
        for f in pool[card][3]:
            if f in per and con: per[f][con].add(card)
    return per


def only(x, args):
    """ask.py <games> only <game>: the concepts only one faction of the game has (2 or more cards, every other faction none)"""
    g = (args[0] if args else x.games[0]).lower()
    if g not in [gg.lower() for gg in x.games]: print(f'No game "{g}"; games: {", ".join(x.games)}'); return
    per = concept_counts(x, g)
    out = collections.defaultdict(list)
    for con in {k for m in per.values() for k in m}:
        has = [f for f in per if per[f].get(con)]
        if len(has) == 1 and len(per[has[0]][con]) >= 2: out[has[0]].append((len(per[has[0]][con]), con))
    print(f'{g}: concepts only one faction has (cards with it; one example)')
    for f in per:
        if not out[f]: continue
        print(f'## {f}')
        used = collections.Counter()
        for n, con in sorted(out[f], reverse=True):
            ex = min(per[f][con], key=lambda i: (used[i], i)); used[ex] += 1  # a new example where there is one
            print(f'  {con} ({n}): {x.example(ex, 70)}')


def lacks(x, args):
    """ask.py <games> lacks <faction>: concepts the faction never has while at least half the other factions of its game do"""
    f = x.find(' '.join(args))
    if not f: return
    g, fac, ids = f
    per = concept_counts(x, g)
    others = [o for o in per if o != fac]
    rows = []
    for con in {k for o in others for k in per[o]}:
        if per.get(fac, {}).get(con): continue
        has = [o for o in others if len(per[o].get(con, ())) >= 2]
        if len(has) * 2 >= len(others): rows.append((len(has), sum(len(per[o][con]) for o in has), con, has))
    print(f'{g}, {fac}: concepts it never has while most other factions do ({len(others)} others)')
    for k, n, con, has in sorted(rows, reverse=True):
        print(f'- {con}: {k} of {len(others)} others, {n} cards ({", ".join(has)})')


ASKS = {'palette': palette, 'curve': curve, 'spells': spells, 'removal': removal, 'protect': protect, 'ways': ways,
        'scaling': scaling, 'only': only, 'lacks': lacks}
