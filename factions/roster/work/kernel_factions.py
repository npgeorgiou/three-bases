"""Step 6 of the roster (factions/START_DESIGN-1-roster.md, which has every rule): the factions from what they do.
1. Identity (IDENTITIES, Claude's): what the faction does, in plain words, made of headings of library/concept_tree.txt.
   Its core: their usable concepts (effects and "when..."; a drawback only for Eats its own) that MIN_LEAN+ decks are
   built on, the KERNEL with most decks; a concept two identities want goes to the one whose other concepts' decks
   hold it more.
2. Its decks: the decks whose cards with the kernel's concepts make up DECK_SHARE times its game's average share or more.
3. How well two concepts go together (fit2): the higher of how many times chance real cards link them and real decks
   hold both, on a log scale where FULL times chance is 1. The ranked fill: every other usable concept by its average
   fit2 to the core; the best fill the faction to OWN concepts, then its extras to OWN + EXTRAS. A concept is in at most
   MAX_SHARE factions (kernels, concepts and extras together; share()): it stays where it fits best.
4. The real kernel: the core, plus for each question the core does not answer (work/answer_concepts.tsv: removes a front
   unit, the back row, holds a base, what it cares about) up to PER_QUESTION concepts of the fill or
   the top WHOLE_LIST of its list that answer it, the ones that go best with the core and the other answers (choose());
   each added concept fits another kernel concept at SYN or more; no two factions answer a question with the same added
   concept. Between lanes is answered by the core alone (lane_way()): the core concept whose real cards most often act
   in another lane (a row of the card on a unit or place in another lane than its own, LANE_CARDS+ cards; under a
   concept counts its narrower concepts too), "<it> in another lane"; when no core concept has such cards it stays open.
   Then 2 and 3 again on the real kernel.
5. A concept COMMON+ decks are built on that no faction has replaces the weakest extra of the faction it fits best.
6. Partners: its PARTNERS strongest pairs (strong card links between their concepts, plus 3 per kernel concept the
   other's decks hold DECK_LIFT times as often as their games). Design markers: what its decks are like (deck_scores.json).
   Its people (THEMES, Claude's): one new world, WORLD; their families break ties within TIE. Its list
   (concept_list.Library) -> lists/<letter>.tsv.
python3 factions/roster/work/kernel_factions.py (from the repo, about 2 minutes; needs links.sqlite) -> kernel_factions.md
(one sheet per faction), kernel_factions.tsv (read by make_faction.py, the map
and concept_list.py), kernel_factions_summary.json (the numbers to compare runs) and lists/."""
import collections, csv, itertools, json, math, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, HERE)
OWN, EXTRAS, KERNEL, MIN_LEAN, MIN_DECKS, DECK_SHARE, FULL = 12, 10, 6, 10, 3, 2, 8  # Claude's (EXTRAS 8-12: Kaptain)
PER_QUESTION, SYN, WHOLE_LIST, COMMON = 2, 1 / 3, 30, 15  # 2 per question: Kaptain; the rest Claude's
MAX_SHARE, PARTNERS, DECK_LIFT, TIE = 3, 5, 1.5, 0.1  # 5 partners and TIE: Kaptain; 3 and 1.5 Claude's
IDENTITIES = [  # (name, what it does, families or concepts of the concept tree); Claude's
    ("Can't be broken", 'its units do not die', ['protection', 'heal', 'defence_gain']),
    ('Kills brutally', 'removes enemy units, many and hard', ['removal', 'damage']),
    ('Messes you up', "breaks the enemy's units and plans", ['disruption', 'suppress', 'debuff', 'steal']),
    ('Moves', 'wins by where its units and his stand', ['positional']),
    ('Thrives on spells', 'spells that get stronger, cheaper and more of them', ['spell_power', 'card_advantage', 'cost_reduction', 'cost_set', 'on_spell']),
    ('Waits', 'gets bigger every round, clears the board, then plays huge cards', ['base_resource_gain', 'resource_gain', 'high_cost', 'board_wipe', 'selection']),
    ('Swarms', 'fills the board with many units that hit at once', ['summon', 'copy', 'free_play', 'haste', 'attack_gain']),
    ('Grows', 'its units get bigger and bigger', ['buff', 'in_hand_buff']),
    ('Comes back', 'what it loses returns', ['revive', 'return_to_hand', 'recycle']),
    ('Eats its own', 'kills and spends its own units and cards for power', ['sacrifice', 'friendly_fire', 'self_destruct', 'discard']),
]
LETTERS = 'ABCDEFGHIJKLMNOPQRST'
WORLD = ('Veyl, a world of drowned continents, floating islands and storm-rivers, where ten peoples fight over the three '
         'Wells that still give water')  # Claude's
THEMES = {  # per faction: its people in Veyl, the real-world model it is written from (hidden, never shown), the families it favours in a tie
    "Can't be broken": ('The Shellwardens of Kesh: a coastal people who grow living coral over their bodies and hold the tide-gates; '
                        'they do not fall', 'the defenders of the walls of Constantinople', ['protection', 'terrain', 'heal']),
    'Kills brutally': ('The Ashen Hunt: riders on burn-scarred lizards who sweep the dune seas and leave nothing standing',
                       'the Mongol tumens', ['damage', 'movement', 'removal']),
    'Messes you up': ('The Whisper Choir: masked singers whose songs unknit memory, break oaths and turn warriors against their orders',
                      'the spies and poisoners of the Venetian Council of Ten', ['information', 'damage_over_time', 'steal']),
    'Moves': ('The Drift Clans: sky-raft nomads who ride the winds between floating islands and shove their foes off the edges',
              'the Comanche horse raiders', ['positional', 'speed']),
    'Thrives on spells': ('The Lantern Scribes: scholars who write with ink distilled from starlight; every word they write makes the next one brighter',
                          'the alchemists of Rudolf II in Prague', ['card_flow', 'transform', 'economy']),
    'Waits': ('The Deep Bell: an old order inside the mountain that winds a vast clockwork for years, then rings the bell that flattens the valley',
              'World War I artillery', ['ranged', 'delayed', 'scope_multi']),
    'Swarms': ('The Hive of Many Mouths: insect folk who hatch by the thousand from amber nests and cover the ground at once',
               'the Zulu regiments', ['board_presence', 'speed', 'adjacency']),
    'Grows': ('The Rootborn: walking tree-giants who swell with every season they survive',
              'the sumo stables of Edo', ['stat_gain', 'card_quality']),
    'Comes back': ('The Returning Tide: drowned sailors the sea sends back to the shore every dawn',
                   'the embalmers of ancient Egypt', ['death', 'card_flow']),
    'Eats its own': ('The Ember Cult: fire-worshippers who feed their own to the furnace for power',
                     'the sacrifice priests of Tenochtitlan', ['death', 'drawback']),
}
D = json.load(open(os.path.join(HERE, 'deck_scores.json'), encoding='utf-8'))
plain, decks, UNIT = dict(D['plain']), D['decks'], set(D['unit'])
tree, facet = {}, {}
for line in open(os.path.join(ROOT, 'library/concept_tree.txt'), encoding='utf-8'):
    if line.startswith('#') or '|' not in line: continue
    p = [x.strip() for x in line.split('|')]
    tree[p[0]] = [q for q in p[3].split(',') if q]; facet[p[0]] = p[2]; plain.setdefault(p[0], p[1])
LANE_CARDS = 2  # Claude's
OTHER_LANE = re.compile(r'position (not same_lane|is lane_right|in lane_right|is lane_left|in lane_left|is previous_lane|is next_lane|is each_lane|is edge_lane)')
def lane_cards():
    """concept -> the real cards with a row of it on a unit or place in another lane than the card's own"""
    con = sqlite3.connect(os.path.join(ROOT, 'library', 'cards_db', 'cards.sqlite')); out = collections.defaultdict(set)
    for card, c, on, to in con.execute('select d.card, d.concept, d.on_with, d.to_with from flat_do d join card k on k.id = d.card where k.is_keyword = 0'):
        if c and OTHER_LANE.search((on or '') + ';' + (to or '')): out[c].add(card)
    return out
LANE = lane_cards()
usable = {r['concept'] for r in csv.DictReader(open(os.path.join(HERE, 'concepts.tsv'), encoding='utf-8'), delimiter='\t') if r['kind'] == 'usable'}
def under(x):
    out, grew = {x}, True
    while grew:
        grew = False
        for k, ps in tree.items():
            if k not in out and any(p in out for p in ps): out.add(k); grew = True
    return out
drawbacks = under('drawback')
lean = {}
for d in decks:
    for c in d['z']: lean[c] = lean.get(c, 0) + 1
strong, together = {}, {}
for r in csv.DictReader(open(os.path.join(ROOT, 'library/cards_db/roster/concept_links.tsv'), encoding='utf-8'), delimiter='\t'):
    cards, rare, level = float(r['cards'] or 0), float(r['rare'] or 0), float(r['level'] or 0)
    if cards >= 1.2 or (rare >= 3 and level >= 1):
        strong[frozenset((r['a'], r['b']))] = (cards, r['texts'].split(' | ')[0], int(float(r['games'] or 0)))
    together[frozenset((r['a'], r['b']))] = float(r['cards'] or 0)
def deck_together():
    """how many times chance real decks hold both concepts: a deck holds a concept when its share of cards with it is
    DECK_SHARE times its game's average or more"""
    import numpy as np
    cs = sorted(usable); ix = {c: i for i, c in enumerate(cs)}
    M = np.zeros((len(decks), len(cs)))
    for n, d in enumerate(decks):
        tot = sum(d['counts'].values()) or 1
        for c, v in d['counts'].items():
            if c in ix: M[n, ix[c]] = v / tot
    for g in {d['game'] for d in decks}:
        rows = [n for n, d in enumerate(decks) if d['game'] == g]
        avg = M[rows].mean(0); M[rows] = (M[rows] >= DECK_SHARE * avg) & (avg > 0)
    p = M.mean(0); both = (M.T @ M) / len(decks)
    lift = both / np.maximum(np.outer(p, p), 1e-9)
    return {frozenset((cs[i], cs[j])): float(lift[i, j]) for i in range(len(cs)) for j in range(i + 1, len(cs)) if both[i, j] * len(decks) >= MIN_DECKS}
def fit2(a, b):
    """how well two concepts go together, 0 to 1: the higher of how many times chance real cards link them and real decks
    hold both (a brick has no card links, so decks alone can carry it); FULL times chance or more is 1"""
    v = max(together.get(frozenset((a, b)), 0), in_decks.get(frozenset((a, b)), 0))
    return min(1.0, math.log2(v) / math.log2(FULL)) if v > 1 else 0.0
def cohesion(cs):
    cs = sorted(set(cs))
    ps = [fit2(a, b) for i, a in enumerate(cs) for b in cs[i + 1:]]
    return sum(ps) / len(ps) if ps else 0.0
def linked(a, b): return a != b and frozenset((a, b)) in strong
in_decks = deck_together()
game_tot = {g: sum(v.values()) for g, v in D['game_counts'].items()}

_lift_cache = {}
def deck_lift(ns):
    """per concept: how many times as often the decks ns hold it as their game's cards (per game, then averaged)"""
    key = tuple(ns)
    if key in _lift_cache: return _lift_cache[key]
    by_game = {}
    for n in ns: by_game.setdefault(decks[n]['game'], []).append(n)
    use = {g: v for g, v in by_game.items() if len(v) >= MIN_DECKS} or by_game
    tots = {g: sum(sum(decks[n]['counts'].values()) for n in v) for g, v in use.items()}
    out = {}
    for c in D['nodes']:
        if c in UNIT: continue
        rs = []
        for g, v in use.items():
            base = D['game_counts'][g].get(c, 0) / game_tot[g] if game_tot[g] else 0
            if tots[g] and base: rs.append(sum(decks[n]['counts'].get(c, 0) for n in v) / tots[g] / base)
        out[c] = sum(rs) / len(rs) if rs else 0
    _lift_cache[key] = out
    return out
def decks_of(cs): return [n for n, d in enumerate(decks) if any(c in d['z'] for c in cs)]
def kernel_decks(k):
    """the decks whose cards with the kernel's concepts make up twice the share its game's decks average or more"""
    k, share = set(k), {}
    for n, d in enumerate(decks):
        tot = sum(d['counts'].values())
        share[n] = sum(v for c, v in d['counts'].items() if c in k) / tot if tot else 0
    avg = collections.defaultdict(list)
    for n, d in enumerate(decks): avg[d['game']].append(share[n])
    avg = {g: sum(v) / len(v) for g, v in avg.items()}
    return [n for n, d in enumerate(decks) if avg[d['game']] and share[n] >= DECK_SHARE * avg[d['game']]]
def candidates(fams, name):
    cs = set().union(*(under(f) for f in fams)) & usable
    return {c for c in cs if facet.get(c) != 'condition' and lean.get(c, 0) >= MIN_LEAN  # a 'when...' under its headings may be kernel
            and (name == 'Eats its own' or c not in drawbacks)}

fac = [{'name': n, 'does': does, 'fams': list(fams), 'cand': candidates(fams, n)} for n, does, fams in IDENTITIES]
for x in fac:  # a shared concept goes to the identity whose other concepts' decks hold it more
    for c in sorted(x['cand']):
        for y in fac:
            if y is x or c not in y['cand'] or c not in x['cand']: continue
            mine = deck_lift(decks_of(x['cand'] - {c})).get(c, 0); theirs = deck_lift(decks_of(y['cand'] - {c})).get(c, 0)
            (x if theirs > mine else y)['cand'].discard(c)
for x in fac:
    x['kernel'] = sorted(x['cand'], key=lambda c: -lean[c])[:KERNEL]
def share(pool, room, fit, add=True):
    """sharing: each faction takes its first room(x) of pool(x); a concept that would then be in more than
    MAX_SHARE factions (counting those that have it from an earlier level) stays with the ones it fits best (fit(x, c),
    ties by name) and the others take their next best"""
    banned = {id(x): set() for x in fac}
    before = collections.Counter(c for x in fac for c in x.get('concepts', x['kernel']) + x.get('extras', []))
    while True:
        took = {id(x): [c for c in pool(x) if c not in banned[id(x)]][:max(0, room(x))] for x in fac}
        crowded = sorted({c for v in took.values() for c in v if before[c] + sum(c in w for w in took.values()) > MAX_SHARE})
        if not crowded: break
        for c in crowded:
            takers = sorted((x for x in fac if c in took[id(x)]), key=lambda x: (-fit(x, c), x['name']))
            for x in takers[max(0, MAX_SHARE - before[c]):]: banned[id(x)].add(c)
    if add:
        for x in fac: x['concepts'] = x.get('concepts', x['kernel']) + took[id(x)]
    return took
sys.path.insert(0, os.path.join(ROOT, 'library', 'cards_db'))
ways = {}
for r in csv.DictReader(open(os.path.join(HERE, 'answer_concepts.tsv'), encoding='utf-8'), delimiter='\t'):
    if r['answer'] == 'blind': continue
    ways.setdefault(r['answer'], []).append((r['way'], [[a.split(' ')[0] for a in part.split('|')] for part in r['concepts'].split('+')]))
QUESTION = {'front': 'removes the front unit', 'backrow': 'mainly removes back-row units', 'lanes': 'mainly acts between lanes',
            'holds': 'holds a base', 'cares': 'the game thing it cares about'}
def answers(cs):
    s = set(cs)
    return {q: [w for w, need in ws if all(any(a in s for a in alt) for alt in need)] for q, ws in ways.items() if q in QUESTION}

sys.path.insert(0, HERE); import concept_list
lib = concept_list.Library()
def pick(x, cands):
    """the best of cands (concept -> score): within TIE of the top score, the theme's concept first, then the score, then the key"""
    if not cands: return None
    top = max(cands.values())
    return min((c for c in cands if cands[c] >= top - TIE), key=lambda c: (c not in x['theme_likes'], -cands[c], c))
def lane_way(core):
    """the core concept whose real cards most often act in another lane (with its narrower concepts), or None"""
    n = {c: len(set().union(*(LANE.get(k, set()) for k in under(c)))) for c in core}
    best = sorted((c for c in core if n[c] >= LANE_CARDS), key=lambda c: (-n[c], c))
    return best[0] if best else None
def best_way(x, q, have, score):
    """the way of question q that the concepts have give, or that takes the fewest, highest-scoring extras: (way, extras)"""
    found = []
    for way, need in ways[q]:
        take = []
        for alt in need:
            if any(a in have for a in alt): continue
            got = {a: score[a] for a in alt if a in score and a in usable}
            if not got: break
            take.append(pick(x, got))
        else: found.append((len(take), -sum(score[a] for a in take) / max(1, len(take)), way, take))
    return min(found, key=lambda t: t[:3])[2:] if found else (None, [])
def markers_of(ds):
    """design markers: what the decks ds are like against all decks of their games (step 3), times as much"""
    gs, out = {decks[n]['game'] for n in ds}, {}
    for key in D['markers']:
        here = [decks[n]['marks'][key] for n in ds if key in decks[n]['marks']]
        every = [d['marks'][key] for d in decks if d['game'] in gs and key in d['marks']]
        if len(here) >= 5 and sum(every) and (sum(here) / len(here)) / (sum(every) / len(every)) >= D['mark_fit']:
            out[key] = round((sum(here) / len(here)) / (sum(every) / len(every)), 1)
    return out
def build():
    """one pass of step 6 on the factions' kernels: one ranked fill (concepts, then extras), partners, markers, list, answers"""
    global kernels, strengths, partners
    kernels = set().union(*(set(x['kernel']) for x in fac))
    for x in fac:
        k = x['kernel']
        x['decks'] = kernel_decks(k); lift = deck_lift(x['decks']); x['lift'] = lift
        base = x.get('core', k)
        x['fit'] = {c: sum(fit2(c, q) for q in base) / len(base) for c in usable if c not in k}  # how well it goes with the core
        x['ranked'] = sorted(x['fit'], key=lambda c: (-x['fit'][c], c))
    took = share(lambda x: x['ranked'], lambda x: OWN - len(x['kernel']), lambda x, c: x['fit'][c])  # one ranked fill
    for x in fac:
        x['linked'] = [c for c in took[id(x)] if any(linked(c, q) for q in x['kernel'])]
    for x in fac:
        x['engines'] = [c for c in x['concepts'] if any(linked(c, o) for o in x['concepts'])]

    strengths = {}
    for i in range(len(fac)):
        for j in range(i + 1, len(fac)):
            a, b = fac[i], fac[j]
            ca, cb = a['concepts'], b['concepts']
            links = sorted({frozenset((p, q)) for p in ca for q in cb if linked(p, q) and p not in cb and q not in ca}, key=lambda s: -strong[s][0])
            sup_ab = [c for c in b['kernel'] if a['lift'].get(c, 0) >= DECK_LIFT]
            sup_ba = [c for c in a['kernel'] if b['lift'].get(c, 0) >= DECK_LIFT]
            strength = len(links) + 3 * (len(sup_ab) + len(sup_ba))
            strengths[(i, j)] = strengths[(j, i)] = strength

    partners = {i: sorted((j for j in range(len(fac)) if j != i), key=lambda j: -strengths[(i, j)])[:PARTNERS] for i in range(len(fac))}

    for i, x in enumerate(fac):
        x['letter'], (x['theme'], x['model'], tf) = LETTERS[i], THEMES[x['name']]
        x['theme_likes'] = set().union(*(under(f) for f in tf))
        x['markers'] = markers_of(x['decks'])
    for i, x in enumerate(fac):
        x['list'] = lib.scores(x['concepts'])
        x['score'] = {c: v[0] for c, v in x['list'].items()}
        x['wish'] = [c for c in x['ranked'] if c not in x['concepts']]  # extras: the ranked fill goes on
    for x in fac: x.pop('extras', None)
    took = share(lambda x: x['wish'], lambda x: OWN + EXTRAS - len(x['concepts']), lambda x, c: x['fit'][c], add=False)  # extras count toward MAX_SHARE too
    for i, x in enumerate(fac):
        x['extras'] = ex = took[id(x)]; score = x['score']
        full = set(x['concepts'] + ex)
        x['answers'] = {}
        for q in ('front', 'backrow', 'holds'):
            own = answers(x['concepts'])[q]
            x['answers'][q] = own[0] if own else (best_way(x, q, full, {})[0] or '**missing**')
        lw = lane_way(x.get('core', x['kernel']))
        x['answers']['lanes'] = f'{plain.get(lw, lw)} in another lane' if lw else 'nothing in real cards'
        mine = answers(x['concepts'])['cares']
        pool = {w: max((score[a] for alt in need for a in alt if a in score), default=0) for w, need in ways['cares']}
        x['answers']['cares'] = mine[0] if mine else (pick(x, pool) or '**missing**')
        e = sorted((frozenset((a, b)) for a in x['concepts'] for b in x['concepts'] if a < b and linked(a, b)), key=lambda t: -strong[t][0])
        x['wins'] = x['does'] + ('; ' + ' -> '.join(plain.get(c, c) for c in sorted(e[0])) + f": \"{strong[e[0]][1]}\"" if e else '')
        os.makedirs(os.path.join(HERE, 'lists'), exist_ok=True)
        with open(os.path.join(HERE, 'lists', x['letter'] + '.tsv'), 'w', encoding='utf-8') as w:
            w.write('concept\tscore\tlevel\tgames\n')
            for k, (sc, lv, gm) in sorted(x['list'].items(), key=lambda t: (-t[1][0], t[0])): w.write(f'{k}\t{sc}\t{lv}\t{gm}\n')
Q5 = ('front', 'backrow', 'lanes', 'holds', 'cares')
def options(q, P, banned):
    """the ways the concepts P answer question q: one way (1-2 concepts), or two one-concept ways; at most PER_QUESTION"""
    one = set()
    for way, need in ways[q]:
        alts = [[a for a in alt if a in P and a not in banned] for alt in need]
        if all(alts): one |= {frozenset(t) for t in itertools.product(*alts) if len(set(t)) <= PER_QUESTION}
    single = [o for o in one if len(o) == 1]
    return sorted(one | {a | b for a, b in itertools.combinations(single, 2)}, key=sorted)
def choose(x, ban):
    """the real kernel: the core, plus per question the core does not answer the option that goes best with the core and
    the other answers (cohesion)"""
    core = set(x['core']); P = set(x['concepts'] + x['extras']) - core
    top = [c for c, _ in sorted(x['score'].items(), key=lambda t: -t[1]) if c in usable][:WHOLE_LIST]
    have = answers(sorted(core))
    opts = {}
    for q in Q5:
        if q == 'lanes':
            lw = lane_way(sorted(core)); opts[q] = [frozenset([lw])] if lw else []
            continue
        if have[q]:
            opts[q] = [frozenset(c for way, need in ways[q] if way == have[q][0] for alt in need for c in alt if c in core)]
            continue
        opts[q] = options(q, P, ban[q] | ban['all'])
        if len(opts[q]) < 3: opts[q] = options(q, P | set(top), ban[q] | ban['all'])  # few options: the top of its whole list too
        if not opts[q]:  # none of its concepts answers it: the best way from its list
            way, take = best_way(x, q, set(), {c: v for c, v in x['score'].items() if c not in ban[q] | ban['all']})
            opts[q] = [frozenset(take)] if take else []
    cur = {q: (max(o, key=lambda op: (cohesion(op | core), sorted(op))) if o else frozenset()) for q, o in opts.items()}
    for _ in range(10):
        changed = False
        for q in Q5:
            if not opts[q]: continue
            rest = core | set().union(*(cur[r] for r in Q5 if r != q))
            best = max(opts[q], key=lambda op: (round(cohesion(rest | op), 6), len(op), sorted(op)))
            if best != cur[q]: cur[q], changed = best, True
        if not changed: break
    return cur
def fits_in(c, k): return sum(fit2(c, o) for o in k if o != c) / max(1, len(k) - 1)
def holders(c): return sum(c in x['concepts'] + x['extras'] for x in fac)

name = lambda c: re.sub(r' \([^)]*\)', '', plain.get(c, c))  # plain name, nothing in brackets
def sheet(title, does, theme, fams, kernel, others, by_q, markers, partner_names):
    """one faction's page for Kaptain: a header per part, every item a list, plain names, no numbers"""
    page = [f'## {title}', '']
    if does: page += [f'{does.capitalize()}.', '']
    if theme: page += ['### Who they are', '', f'{theme}.', '']
    if fams: page += ['### Identity: its families of the concept tree', ''] + [f'- {name(f)}' for f in fams] + ['']
    page += ['### Concepts', ''] + [f'- [K] {name(c)}' for c in kernel] + [f'- {name(c)}' for c in others if c not in kernel]
    page += ['', '### Design answers', ''] + ([f'- How it wins: {does}'] if does else [])
    for q in Q5:
        add = ' in another lane' if q == 'lanes' else ''
        page += [f'- {QUESTION[q].capitalize()}:'] + ([f'  - {name(c)}{add}' for c in sorted(by_q[q])]
                                                      or ['  - nothing in real cards' if q == 'lanes' else '  - none yet'])
    page += ['', '### Deck style: what its decks are like', ''] + ([f"- {D['markers'][k]}" for k in markers] or ['- nothing stands out'])
    if partner_names: page += ['', '### Partners', ''] + [f'- {n}' for n in partner_names]
    return page + ['']

def run():
    """step 6 for the roster: the fill from the core, the kernels, the fill again from the kernels, the pages"""
    global cur, kern, missed
    build()  # the fill from the identities' cores
    for x in fac: x['core'] = list(x['kernel'])
    core_of = {x['name']: set(x['core']) for x in fac}
    bans = {x['name']: {q: set() for q in Q5 + ('all',)} for x in fac}
    for _ in range(40):
        cur = {x['name']: choose(x, bans[x['name']]) for x in fac}
        kern = {x['name']: set(x['core']).union(*cur[x['name']].values()) for x in fac}
        moved = False
        for x in fac:  # (a) every kernel concept goes well with at least one other kernel concept
            k = kern[x['name']]
            for c in sorted(k - set(x['core'])):
                if max(fit2(c, o) for o in k if o != c) < SYN: bans[x['name']]['all'].add(c); moved = True
        for q in Q5[:-1]:  # (b) no two factions answer a question with the same concept: it stays where it fits best
            users = collections.defaultdict(list)
            for n, c in cur.items():
                for k in c[q] - core_of[n]: users[k].append(n)
            for k, ns in users.items():
                for n in sorted(ns, key=lambda n: (-fits_in(k, kern[n]), n))[1:]: bans[n][q].add(k); moved = True
        count = collections.defaultdict(list)  # (b) no kernel concept in more than MAX_SHARE factions
        for n, k in kern.items():
            for c in k: count[c].append(n)
        for c, ns in count.items():
            added = sorted((n for n in ns if c not in core_of[n]), key=lambda n: (-fits_in(c, kern[n]), n))
            for n in added[max(0, MAX_SHARE - (len(ns) - len(added))):]: bans[n]['all'].add(c); moved = True
        if not moved: break
    first = {x['name']: {'kernel': x['kernel'], 'concepts': x['concepts'], 'extras': x['extras']} for x in fac}
    for x in fac:  # the kernel, then the fill again
        x['by_question'] = cur[x['name']]; x['kernel'] = x['core'] + sorted(kern[x['name']] - set(x['core'])); x['first'] = first[x['name']]
        for k in ('concepts', 'extras', 'linked', 'engines'): x.pop(k, None)
    build()
    for c in sorted((c for c in usable if lean.get(c, 0) >= COMMON and not holders(c)), key=lambda c: -lean[c]):
        x = max(fac, key=lambda x: (x['fit'].get(c, 0), x['name']))  # a common concept no faction has replaces the weakest extra
        weak = min(x['extras'], key=lambda o: x['fit'][o]) if x['extras'] else None  # of the faction it fits best, if it fits nearly as well
        if weak and x['fit'].get(c, 0) >= 0.8 * x['fit'][weak]: x['extras'][x['extras'].index(weak)] = c
    missed = sorted((c for c in usable if lean.get(c, 0) >= MIN_LEAN and not holders(c)), key=lambda c: -lean[c])  # still in no faction
    with open(os.path.join(HERE, 'kernel_factions.tsv'), 'w', encoding='utf-8') as w:
        w.write('letter\tname\tdoes\ttheme\tkernel\tengines\tbricks\tconcepts\textras\tmarkers\twins\tfront\tbackrow\tlanes\tholds\tcares\tpartners\tby_question\n')
        for i, x in enumerate(fac):
            w.write('\t'.join([x['letter'], x['name'], x['does'], x['theme'], ','.join(x['kernel']), ','.join(c for c in x['concepts'] if c in x['engines']),
                               ','.join(c for c in x['concepts'] if c not in x['engines']), ','.join(x['concepts']), ','.join(x['extras']),
                               ','.join(f'{k}:{v}' for k, v in x['markers'].items()), x['wins']] + [x['answers'][q] for q in ('front', 'backrow', 'lanes', 'holds', 'cares')]
                              + [','.join(fac[j]['letter'] for j in partners[i])] + [';'.join(q + ':' + '+'.join(sorted(x['by_question'][q])) for q in Q5)]) + '\n')

    page = ['# The factions', '', f'The world: {WORLD}.', '', '[K] marks a kernel concept.', '']
    for i, x in enumerate(fac):
        page += sheet(x['name'], x['does'], x['theme'], x['fams'], x['kernel'], x['concepts'] + x['extras'], x['by_question'],
                      x['markers'], [fac[j]['name'] for j in partners[i]])
    if missed: page += ['## In no faction yet', ''] + [f'- {name(c)}' for c in missed] + ['']
    open(os.path.join(HERE, 'kernel_factions.md'), 'w', encoding='utf-8').write('\n'.join(page) + '\n')
    allc = {x['name']: set(x['concepts'] + x['extras']) for x in fac}
    jac = [len(allc[a['name']] & allc[b['name']]) / len(allc[a['name']] | allc[b['name']]) for i, a in enumerate(fac) for b in fac[i + 1:]]
    summary = {               'kernel cohesion': round(sum(cohesion(x['kernel']) for x in fac) / len(fac), 3),
               'whole cohesion': round(sum(cohesion(allc[x['name']]) for x in fac) / len(fac), 3),
               'questions answered': sum(bool(x['by_question'][q]) for x in fac for q in Q5),
               'answers from rare concepts': sum(any(lean.get(c, 0) < MIN_LEAN for c in x['by_question'][q]) for x in fac for q in Q5),
               'common concepts placed': sum(1 for c in usable if lean.get(c, 0) >= COMMON and holders(c)),
               'common concepts': sum(1 for c in usable if lean.get(c, 0) >= COMMON),
               'overlap mean': round(sum(jac) / len(jac), 3), 'overlap max': round(max(jac), 3),
               'kernel size': [len(x['kernel']) for x in fac]}
    json.dump(summary, open(os.path.join(HERE, 'kernel_factions_summary.json'), 'w'))



if __name__ == '__main__':
    run()
