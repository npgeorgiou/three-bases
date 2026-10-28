"""A deck, a faction or a whole game as a network of cards (NETWORK_DRAFT.md), built from the stored rows only, the same way
for every game; lines only join cards of one game.
Nodes: the cards; their level-up forms; cards they make or put into play ("made by the deck").
Lines A -> B, each with a kind and a weight:
  waits     A makes something B waits for, counts or tests (A kills an ally, B acts when allies die)
  levels    as waits, but B's use is a level-up condition (weight x2)
  puts      A summons, creates, copies, revives or plays B
  repeats   A makes B's effects happen again (weight x2)
  rules     A changes how B works for as long as it lasts (cards in hand made Fast or cheaper, units that can't be blocked)
  targets   A's effect on my side is aimed at cards like B (weight x0.5)
  type      A has or makes a type B asks for
  levelsinto  a champion and its level-up form
Weight: 1 / how many cards of the game share the thing the line is about (rarer is stronger).
Usage (through ask.py): ask.py <game> network "<card>, <card>, ..." | network faction <name> | network game  [--json file]"""
import collections, json, math, os
import mechanics, deck_analysis

CACHE = {}
PUTS = ('summon', 'create', 'copy', 'play_card', 'revive')
RULES = ('cost_change', 'cost_set', 'can', 'cant', 'give_keyword', 'give_ability', 'give_type', 'remove_keyword')
KIND_CAT = {'unit': {'unit', 'hero'}, 'landmark': {'building'}, 'spell': {'spell'}, 'equipment': {'item'},
            'unit_or_structure': {'unit', 'hero', 'building'}}
CAT = {'follower': {'unit'}, 'champion': {'hero'}, 'unit': {'unit', 'hero'}, 'spell': {'spell'}, 'skill': {'ability'},
       'landmark': {'building'}, 'equipment': {'item'}}
PLAY_STATE = ('state', 'position', 'targets', 'right_of', 'level', 'origin', 'countdown', 'damage')  # true or not only in play
EVERY_GAME = deck_analysis.EVERY_GAME


def cards_of(c, game):
    """per card: what filters can test before play (category, types, keywords, acts, numbers)"""
    if ('cards', game) in CACHE: return CACHE[('cards', game)]
    d = {}
    for i, n, cat, regions, pw, hp, stats, rar in c.execute("""select id, name, category, regions, power, health, stats, rarity from card
                                                              where game=? and is_keyword=0 and is_stub=0 and category!='tribe'""", (game,)):  # a type's own entry is no card
        try: st = json.loads(stats) if stats else {}
        except ValueError: st = {}
        if not isinstance(st, dict): st = {}
        strength = str(st.get('strength', '')).split('/')[0]
        d[i] = {'id': i, 'name': n, 'cat': cat, 'regions': set((regions or '').split(';')) - {''}, 'rarity': rar,
                'power': pw, 'health': hp, 'strength': float(strength) if strength.replace('.', '').isdigit() else None,
                'types': set(), 'kws': set(), 'acts': set()}
    for i, t in c.execute('select card, type from card_type'):
        if i in d: d[i]['types'].add(t)
    for i, k in c.execute('select card, keyword from card_keyword'):
        if i in d: d[i]['kws'].add(k)
    for i, a, con in c.execute("select card, act, concept from flat_do where origin in ('own','uses_keyword')"):
        if i in d: d[i]['acts'] |= {a, con}
    CACHE[('cards', game)] = d
    return d


def kw_id(c, game, word):
    r = c.execute('select id from card where game=? and is_keyword=1 and lower(name)=?', (game, word.lower())).fetchone()
    return r[0] if r else None


def number(c, n):
    r = c.execute('select x, value from amount where id=?', (n,)).fetchone() if str(n).isdigit() else None
    return r[1] if r and r[0] == 'n' else None


def matches(c, game, card, kind, withs):
    """can card be one of the target's cards (kind plus filters); things only true in play count as possible"""
    if kind in KIND_CAT and card['cat'] not in KIND_CAT[kind]: return False
    if kind in ('player', 'mana', 'spell_mana', 'effect', 'position', None): return False
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


def lines_of(c, game):
    """every waits / levels / puts / repeats / type line of the game: (a, b) -> [(kind, weight, why)]"""
    if ('lines', game) in CACHE: return CACHE[('lines', game)]
    cards = cards_of(c, game)
    out = collections.defaultdict(list)
    lvl = {a for (a,) in c.execute("select ability from flat_do where act='level_up'")}
    makes, takes = collections.defaultdict(set), collections.defaultdict(set)
    for card, origin, ab, role, h, side, kw, pick in c.execute('select card, origin, ability, role, happening, side, keyword, pick from flat_ref'):
        if card not in cards: continue
        if role == 'makes': makes[h].add((card, side, kw)); continue
        if origin != 'own' or (pick == 'self' and h in ('played', 'summoned')): continue
        takes[h].add((card, 'mine' if pick == 'self' else side, kw, ab in lvl))
    for h, ts in takes.items():
        carers = collections.defaultdict(set)
        for t, _, tk, _ in ts: carers[tk].add(t)
        for m, ms, mk in makes.get(h, ()):
            for t, ts_, tk, lv in ts:
                if m != t and mechanics.FIT(ms, ts_) and (mk is None or tk is None or mk == tk):
                    w = 1.0 / len(carers[tk] | (carers[None] if tk else set()))
                    out[(m, t)].append(('levels', 2 * w, deck_analysis.say(c, h, ts_, tk) + ' (levels it up)') if lv else
                                      ('waits', w, deck_analysis.say(c, h, ts_, tk)))
    put = [(m, ref, act) for m, ref, act in c.execute(f"select card, card_ref, act from flat_do where act in ({','.join('?' * len(PUTS))})", PUTS)
           if m in cards and ref in cards and m != ref]
    putters = collections.Counter(ref for _, ref in {(m, ref) for m, ref, _ in put})
    for m, ref, act in put:
        out[(m, ref)].append(('puts', 1.0 / putters[ref], {'summon': 'summons', 'create': 'creates', 'copy': 'copies', 'revive': 'brings back',
                                                           'play_card': 'plays'}[act]))
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
    asks = collections.defaultdict(set)
    for card, w in c.execute("""select card, coalesce(on_with,'') || ';' || coalesce(to_with,'') from flat_do union all select card, obj_with
                                from flat_when union all select card, coalesce(of_with,'') || ';' || coalesce(ev_obj_with,'') from flat_if"""):
        if card not in cards: continue
        for part in (w or '').split(';'):
            b = part.removeprefix('of:').split(' ')
            if len(b) == 3 and b[0] == 'type' and b[1] in ('is', 'in') and b[2].isdigit(): asks[int(b[2])].add(card)
    has = collections.defaultdict(set)
    for i, x in cards.items():
        for t in x['types']: has[t].add((i, 'is'))
    for m, ref in c.execute(f"select card, card_ref from flat_do where act in ({','.join('?' * len(PUTS))}) and card_ref is not null", PUTS):
        if m in cards and ref in cards:
            for t in cards[ref]['types']: has[t].add((m, 'makes'))
    for t, ts in asks.items():
        tn = c.execute('select name from type where id=?', (t,)).fetchone()
        for m, how in has.get(t, ()):
            for x in ts - {m}: out[(m, x)].append(('type', 1.0 / len(ts), f'{"is" if how == "is" else "makes"} {tn[0] if tn else "the type"}'))
    CACHE[('lines', game)] = out
    return out


NOT_AIMED = PUTS + ('repeat', 'increase_effect', 'level_up', 'draw', 'discard', 'shuffle_into_deck', 'put_on_top', 'look', 'reveal',
                    'choose_card', 'choose_one', 'random_one')


def aimed_rows(c, game):
    """effects on my side aimed at cards (not the card itself): (card, act, kind, pick, with, kw, rule) and how many cards of the
    game make the same one (act, kind, keyword, rule or not)"""
    if ('aimed', game) in CACHE: return CACHE[('aimed', game)]
    cards = cards_of(c, game); rows = []
    for a, act, kind, side, pick, w, lasts, kw in c.execute("""select card, act, on_kind, on_side, on_pick, on_with, lasts, keyword_ref
            from flat_do where origin='own' and on_side in ('mine','any') and coalesce(on_pick,'') not in ('self','it','owner','actor')"""):
        if a not in cards or act in NOT_AIMED: continue
        rule = act in RULES and pick == 'all' and lasts in ('while', 'permanent', None)
        narrowed = any(p.split(' ')[0] not in PLAY_STATE + ('card',) for p in (w or '').split(';') if p and not p.startswith('of:'))
        if (side == 'any' and not rule) or (kind not in KIND_CAT and not (kind in ('card', 'any', 'anything') and narrowed)): continue
        rows.append((a, act, kind, w, kw, rule, narrowed))
    makers = collections.defaultdict(set)
    for a, act, kind, w, kw, rule, _ in rows: makers[(act, kind, kw, rule)].add(a)
    CACHE[('aimed', game)] = rows, makers
    return rows, makers


def aimed(c, game, nodes, broad):
    """rules and targets lines from the nodes to the nodes (a filter is checked against each card); broad=False drops lines
    whose target is every card of its kind, which say nothing about which cards belong together"""
    cards = cards_of(c, game); out = collections.defaultdict(list)
    kwn = lambda k: mechanics.name(c, k) if k else ''
    rows, makers = aimed_rows(c, game)
    for a, act, kind, w, kw, rule, narrowed in rows:
        if a not in nodes or (not narrowed and not broad): continue
        hits = [b for b in nodes if b != a and b in cards and matches(c, game, cards[b], kind, w)]
        n = len(makers[(act, kind, kw, rule)])
        what = {'give_keyword': f'gives it {kwn(kw)}', 'cost_change': 'changes its cost', 'cost_set': 'sets its cost',
                'can': 'lets it do more', 'cant': 'stops it doing something', 'give_ability': 'gives it an ability',
                'give_type': 'gives it a type', 'remove_keyword': f'removes {kwn(kw)}'}.get(act, act.replace('_', ' '))
        for b in hits:
            if rule: out[(a, b)].append(('rules', 1.0 / n, what))
            else: out[(a, b)].append(('targets', 0.5 / n, f'can aim {act.replace("_", " ")}{" " + kwn(kw) if kw else ""} at it'))
    return out


def made(c, game, ids):
    """level-up forms and cards the nodes make or put into play, two steps deep"""
    cards = cards_of(c, game); got = set(ids); new = set()
    for _ in range(2):
        q = list(got | new); marks = ','.join('?' * len(q))
        add = {b for (b,) in c.execute(f"select dst from card_link where rel='transforms_into' and src in ({marks})", q)}
        add |= {b for (b,) in c.execute(f"select card_ref from flat_do where act in ({','.join('?' * len(PUTS))}) and card in ({marks})",
                                         list(PUTS) + q)}
        new |= {b for b in add if b in cards} - got
    return new


def network(c, game, ids, broad=True):
    """nodes (id -> made by the deck?) and lines (a, b) -> [(kind, weight, why)] between them"""
    nodes = {i: False for i in ids}
    for i in made(c, game, ids): nodes[i] = True
    allg = lines_of(c, game); lines = collections.defaultdict(list)
    for (a, b), ls in allg.items():
        if a in nodes and b in nodes: lines[(a, b)] += ls
    for k, ls in aimed(c, game, nodes, broad).items(): lines[k] += ls
    return nodes, lines


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


def report(c, game, ids, title, broad=True, limit=10, json_path=None):
    nodes, lines = network(c, game, ids, broad)
    best = best_lines(lines)
    nm = lambda i: mechanics.name(c, i) + (' (made)' if nodes.get(i) else '')
    own = [i for i, m in nodes.items() if not m]
    out = [f'{title}: {len(own)} cards, {sum(nodes.values())} more made by them, {len(best)} lines.']
    if json_path:
        json.dump({'game': game, 'nodes': [{'id': i, 'name': mechanics.name(c, i), 'made': m} for i, m in nodes.items()],
                   'lines': [{'from': a, 'to': b, 'kind': k, 'weight': round(w, 4), 'why': y} for (a, b), ls in lines.items()
                             for k, w, y in sorted(set(ls))]}, open(json_path, 'w'), indent=1)
        out.append(f'Network written to {json_path}.')
    ins, outs, wsum = collections.Counter(), collections.Counter(), collections.Counter()
    for (a, b), (w, kind, _) in best.items():
        outs[a] += 1; ins[b] += 1; wsum[a] += w; wsum[b] += w
    per_node = None if len(nodes) <= 60 else 5
    adj = collections.defaultdict(list)
    for (a, b), (w, kind, _) in sorted(best.items(), key=lambda x: -x[1][0]):
        if per_node is None or len(adj[a]) < per_node: adj[a].append(b)
    bc = betweenness(list(nodes), adj)
    top = sorted(nodes, key=lambda i: -wsum[i])[:limit]
    out.append('Central cards (strongest lines in and out): ' + ', '.join(f'{nm(i)} ({ins[i]} in, {outs[i]} out)' for i in top if wsum[i]) + '.')
    mid = [i for i in sorted(nodes, key=lambda i: -bc[i]) if bc[i] > 0][:5]
    if mid: out.append('Cards most chains pass through: ' + ', '.join(nm(i) for i in mid) + '.')
    out.append('Strongest chains:')
    for s, head, steps, ends in chains(best, list(nodes), limit, per_node):
        path = list(head[1:]) + [', '.join(dict.fromkeys(nm(e) for e in ends))]
        out.append('- ' + nm(head[0]) + ''.join(f' -> {why} -> {b if isinstance(b, str) else nm(b)}' for (w, kind, why), b in zip(steps, path)))
    gs = groups(best, nodes)
    out.append('Groups (cards tightly linked; one group = one plan):')
    for g, why in gs[:limit]:
        names_ = sorted(dict.fromkeys(nm(i) for i in g))
        out.append(f'- {why or "linked"} ({len(g)}): ' + ', '.join(names_[:25]) + (f' and {len(names_) - 25} more' if len(names_) > 25 else ''))
    if len(gs) > limit: out.append(f'- and {len(gs) - limit} smaller groups')
    if len(gs) > 1:
        gid = {n: k for k, (g, _) in enumerate(gs) for n in g}
        joined = {(gid[a], gid[b]) for (a, b) in best if a in gid and b in gid and gid[a] != gid[b]}
        out.append(f'The groups are joined to each other by weaker lines: {"yes" if joined else "no"}.')
    # loose cards: no lines, lines only one way, needs nothing in the set makes
    alone = [i for i in own if not ins[i] and not outs[i]]
    gives = [i for i in own if outs[i] and not ins[i]]
    gets = [i for i in own if ins[i] and not outs[i]]
    makes = collections.defaultdict(set)
    marks = ','.join('?' * len(nodes))
    for card, h, side, kw in c.execute(f"select card, happening, side, keyword from flat_ref where role='makes' and card in ({marks})", list(nodes)):
        makes[h].add((card, side, kw))
    lack = {}
    for card, h, side, kw, pick in c.execute(f"""select card, happening, side, keyword, pick from flat_ref where role!='makes' and origin='own'
                                               and card in ({','.join('?' * len(own))})""", own):
        side = 'mine' if pick == 'self' else side
        if h in EVERY_GAME or side == 'enemy' or (pick == 'self' and h in ('played', 'summoned')): continue
        if not any(m != card and mechanics.FIT(ms, side) and (mk is None or kw is None or mk == kw) for m, ms, mk in makes.get(h, ())):
            lack.setdefault(card, deck_analysis.say(c, h, side, kw))
    cap = lambda xs: ', '.join(sorted(dict.fromkeys(nm(i) for i in xs))[:15]) + (f' and {len(xs) - 15} more' if len(xs) > 15 else '')
    out.append('Loose cards:')
    if alone: out.append(f'- no lines at all ({len(alone)}): {cap(alone)}')
    if gives: out.append(f'- only give to others, nothing gives to them ({len(gives)}): {cap(gives)}')
    if gets: out.append(f'- only get from others, give nothing back ({len(gets)}): {cap(gets)}')
    for card, what in list(lack.items())[:limit]: out.append(f'- {nm(card)} waits for "{what}" and nothing here does it')
    if len(lack) > limit: out.append(f'- and {len(lack) - limit} more cards wait for something nothing here does')
    linked = sum(1 for i in own if ins[i] or outs[i])
    out.append(f'Overall: {linked} of {len(own)} cards ({round(100 * linked / max(1, len(own)))}%) have at least one line; {len(gs)} group{"" if len(gs) == 1 else "s"}.')
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
