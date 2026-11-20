"""Step 6 of the roster (factions/START_DESIGN-1-roster.md): the factions from what they do.
1. Identity: what the faction DOES, in plain words (IDENTITIES, Claude's), made of families of library/concept_tree.txt.
   Its kernel: their usable concepts that are effects (never a trigger, a condition, or a drawback but for Eats its own)
   and that MIN_LEAN+ decks lean on, at most KERNEL. A concept two identities want goes to the one whose other kernel
   concepts' decks hold it more. A kernel under MIN_KERNEL concepts is marked thin: Kaptain widens it.
2. Engines come from card links: the usable concepts (triggers and conditions too) with a strong card link (step 4) to 2+ kernel
   concepts, that the kernel's decks hold at least PLAYED times as often as their games (real decks play it there too),
   each of those links shown in ENGINE_GAMES+ games (one game's few pairs can be an accident: 8 of 10 such
   pairs read on 20 Nov 2026 did not work together), at most ENGINES, ranked by its kernel links times the share of its links that go to this kernel (so a
   concept real cards link to everything does not join every faction, nor a rare one with two links). Bricks come from decks: the concepts the kernel's decks hold more
   often than their game's cards (share of cards against the game's share, per game with MIN_DECKS+ of its decks,
   averaged; DECK_LIFT+), held by HELD+ of those decks, that no strong card link joins to the kernel (another faction's kernel concepts too: support), the most first,
   until OWN concepts. Each engine shows the real card pair behind its strongest link to the kernel.
   Many-level sharing: the factions are filled together, level by level (engines, then bricks; kernels are never
   shared). A concept more than MAX_SHARE factions want at one level goes to the MAX_SHARE it fits best (most kernel
   links for an engine, most held for a brick) and the others take their next best; it is never dropped.
   A concept is an engine when real cards link it to another of the faction's concepts, else a brick.
3. A faction needs an engine pair (two of its concepts real cards link); one with none is marked.
4. Different enough: two factions share at most half of their concepts.
5. Partners (PARTNERS each, Kaptain): a faction's strongest pairs. A pair's strength: the strong card links between their
   own concepts, plus 3 for each of one's kernel concepts the other's decks hold DECK_LIFT times as often as their games
   (Claude's). Each partner gets a line on how it plays: its strongest card link, or what its decks hold.
6. Design markers: what the kernel's decks are like (step 3's markers): a marker its decks have MARK_FIT times as often
   as their games' decks.
7. A real theme per faction (THEMES, Claude's), with the families it favours; the theme only breaks ties between
   concepts that score within TIE of each other.
8. Its list (concept_list.Library): every concept with 5+ cards but its own, with its score; written to lists/<letter>.tsv.
9. Its extras, EXTRAS for every faction, from its usable list concepts: (a) each board answer (front, back row, between
   lanes, holding) its concepts don't give gets the highest-scoring way that gives it (work/answer_concepts.tsv; a way
   of two concepts takes two extras); (b) a faction with under PARTNERS partners takes concepts that link to the
   kernels of the factions that are not its partners yet; (c) the rest go to the highest-scoring concepts with strong
   links to 2+ of its concepts.
10. Its answers: how it wins (its identity and its strongest engine pair); removing a front unit, removing back-row
   units, acting between lanes and holding a base, each the first way of work/answer_concepts.tsv its own concepts give,
   else the way its extras give; what it cares about most, the first of the game's own things it has, else the one that
   scores highest on its list.
python3 factions/roster/work/kernel_factions.py (from the repo, about a minute; needs links.sqlite) -> kernel_factions.md
(for Kaptain), kernel_factions.tsv (one row per faction, read by concept_list.py) and lists/<letter>.tsv."""
import collections, csv, itertools, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, HERE)
import step3_groups
OWN, KERNEL, MIN_KERNEL, MIN_LEAN, ENGINES, PLAYED, MIN_DECKS = 12, 6, 4, 10, 4, 1.0, 3  # Claude's
PER_QUESTION, SYN, FULL = 2, 1 / 3, 8  # real kernel: concepts per question (Kaptain), fits with another kernel concept, times chance that scores 1 (Claude's)
DECK_LIFT, HELD, MAX_SHARE, PARTNERS = 1.5, 0.25, 3, 5                              # Claude's; 5 partners: Kaptain
EXTRAS, TIE = 10, 0.1                                                                # Claude's (8-12, Kaptain); TIE: Kaptain
IDENTITIES = [  # (name, what it does, families or concepts of the concept tree); Claude's. Waits and Swarms widened by what their decks hold most
    ("Can't be broken", 'its units do not die', ['protection', 'heal', 'defence_gain']),
    ('Kills brutally', 'removes enemy units, many and hard', ['removal', 'damage']),
    ('Messes you up', "breaks the enemy's units and plans", ['disruption', 'suppress', 'debuff', 'steal']),
    ('Moves', 'wins by where its units and his stand', ['positional']),
    ('Thrives on spells', 'spells that get stronger, cheaper and more of them', ['spell_power', 'card_advantage', 'cost_reduction', 'cost_set']),
    ('Waits', 'gets bigger every round, clears the board, then plays huge cards', ['base_resource_gain', 'resource_gain', 'high_cost', 'board_wipe', 'selection']),
    ('Swarms', 'fills the board with many units that hit at once', ['summon', 'copy', 'free_play', 'haste', 'attack_gain']),
    ('Grows', 'its units get bigger and bigger', ['buff', 'in_hand_buff']),
    ('Comes back', 'what it loses returns', ['revive', 'return_to_hand', 'recycle']),
    ('Eats its own', 'kills and spends its own units and cards for power', ['sacrifice', 'friendly_fire', 'self_destruct', 'discard']),
]
LETTERS = 'ABCDEFGHIJKLMNOPQRST'
THEMES = {  # a real theme per faction, and the families of the concept tree it favours in a tie (Claude's)
    "Can't be broken": ('the defenders of the Theodosian Walls of Constantinople', ['protection', 'terrain', 'heal']),
    'Kills brutally': ('the Mongol tumens', ['damage', 'movement', 'removal']),
    'Messes you up': ('the spies and poisoners of the Venetian Council of Ten', ['information', 'damage_over_time', 'steal']),
    'Moves': ('the Comanche horse raiders', ['positional', 'speed']),
    'Thrives on spells': ('the alchemists of Rudolf II in Prague', ['card_flow', 'transform', 'economy']),
    'Waits': ('World War I artillery', ['ranged', 'delayed', 'scope_multi']),
    'Swarms': ('the Zulu regiments', ['board_presence', 'speed', 'adjacency']),
    'Grows': ('the sumo stables of Edo', ['stat_gain', 'card_quality']),
    'Comes back': ('the embalmers of ancient Egypt', ['death', 'card_flow']),
    'Eats its own': ('the sacrifice priests of Tenochtitlan', ['death', 'drawback']),
}
D = json.load(open(step3_groups.FILE, encoding='utf-8'))
plain, decks, UNIT = dict(D['plain']), D['decks'], set(D['unit'])
tree, facet = {}, {}
for line in open(os.path.join(ROOT, 'library/concept_tree.txt'), encoding='utf-8'):
    if line.startswith('#') or '|' not in line: continue
    p = [x.strip() for x in line.split('|')]
    tree[p[0]] = [q for q in p[3].split(',') if q]; facet[p[0]] = p[2]; plain.setdefault(p[0], p[1])
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
    together[frozenset((r['a'], r['b']))] = max(float(r['cards'] or 0), float(r['decks'] or 0))
def fit2(a, b):
    """how well two concepts go together, 0 to 1: the higher of how many times chance real cards link them and real decks
    are built on both (a brick has no card links, so decks alone can carry it); FULL times chance or more is 1"""
    v = together.get(frozenset((a, b)), 0)
    return min(1.0, math.log2(v) / math.log2(FULL)) if v > 1 else 0.0
def cohesion(cs):
    cs = sorted(set(cs))
    ps = [fit2(a, b) for i, a in enumerate(cs) for b in cs[i + 1:]]
    return sum(ps) / len(ps) if ps else 0.0
def wide(a, b): return linked(a, b)
def linked(a, b): return a != b and frozenset((a, b)) in strong
reach = {c: max(1, sum(linked(c, o) for o in usable)) for c in usable}  # how many usable concepts real cards link it to
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
    """the decks built on at least half of the kernel's concepts"""
    return [n for n, d in enumerate(decks) if 2 * sum(c in d['z'] for c in k) >= len(k)]
def candidates(fams, name):
    cs = set().union(*(under(f) for f in fams)) & usable
    return {c for c in cs if facet.get(c) not in ('trigger', 'condition') and lean.get(c, 0) >= MIN_LEAN
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
    x['thin'] = len(x['kernel']) < MIN_KERNEL
def share(pool, room, fit, add=True):
    """many-level sharing: each faction takes its first room(x) of pool(x); a concept that would then be in more than
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
here = os.getcwd(); os.chdir(os.path.join(ROOT, 'library', 'cards_db'))
import archetype_map
os.chdir(here)
def behind(c, k):
    """the real card pair behind c's strongest link to the kernel k"""
    q = max((q for q in k if wide(c, q)), key=lambda q: strong[frozenset((c, q))][0])
    return plain[q], pair_of.get((frozenset((c, q)), ''), 'no card pair')
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
def build():
    """one pass of step 6 on the factions' kernels: engines, bricks, filling, partners, markers, list, extras, answers"""
    global kernels, pair_of, pairs, strengths, partners
    kernels = set().union(*(set(x['kernel']) for x in fac))
    for x in fac:
        k = x['kernel']
        x['decks'] = kernel_decks(k); lift = deck_lift(x['decks']); x['lift'] = lift
        eng = [c for c in usable if c not in kernels and sum(wide(c, q) for q in k) >= 2 and lift.get(c, 0) >= PLAYED]
        x['engine_pool'] = sorted(eng, key=lambda c: (-sum(wide(c, q) for q in k) ** 2 / reach[c], c))
        held = x['held'] = {c: sum(decks[n]['counts'].get(c, 0) > 0 for n in x['decks']) / max(1, len(x['decks'])) for c in lift}
        x['brick_pool'] = [c for c in sorted(lift, key=lambda c: (-lift[c], c)) if lift[c] >= DECK_LIFT and held[c] >= HELD and c not in k
                           and c not in eng and c in usable and not any(linked(c, q) for q in k)]
    took = share(lambda x: x['engine_pool'], lambda x: ENGINES, lambda x, c: sum(wide(c, q) for q in x['kernel']))
    for x in fac: x['from_links'] = took[id(x)]
    took = share(lambda x: x['brick_pool'], lambda x: OWN - len(x['kernel']) - len(x['from_links']), lambda x, c: x['lift'][c])
    for x in fac: x['from_decks'] = took[id(x)]
    for x in fac:  # a faction still short of OWN: what its kernel's decks hold that real cards also link to its concepts
        have = x['concepts']; lift = x['lift']
        x['both_pool'] = [c for c in sorted(lift, key=lambda c: (-lift[c], c)) if lift[c] >= DECK_LIFT and x['held'][c] >= HELD
                          and c in usable and c not in have and any(linked(c, q) for q in have)]
    took = share(lambda x: x['both_pool'], lambda x: OWN - len(x['kernel']) - len(x['from_links']) - len(x['from_decks']), lambda x, c: x['lift'][c])
    for x in fac: x['from_both'] = took[id(x)]
    for x in fac:
        x['engines'] = [c for c in x['concepts'] if any(linked(c, o) for o in x['concepts'])]

    here = os.getcwd(); os.chdir(os.path.join(ROOT, 'library', 'cards_db'))
    wanted = {frozenset((c, q)) for x in fac for c in x['from_links'] for q in x['kernel'] if wide(c, q)}
    pair_of = archetype_map.card_pairs(wanted)[0]
    os.chdir(here)
    pairs, strengths = [], {}
    for i in range(len(fac)):
        for j in range(i + 1, len(fac)):
            a, b = fac[i], fac[j]
            ca, cb = a['concepts'], b['concepts']
            shared = [c for c in ca if c in cb]
            links = sorted({frozenset((p, q)) for p in ca for q in cb if linked(p, q) and p not in cb and q not in ca}, key=lambda s: -strong[s][0])
            sup_ab = [c for c in b['kernel'] if a['lift'].get(c, 0) >= DECK_LIFT]
            sup_ba = [c for c in a['kernel'] if b['lift'].get(c, 0) >= DECK_LIFT]
            strength = len(links) + 3 * (len(sup_ab) + len(sup_ba))
            if links:
                p, q = sorted(links[0]); how = f"{plain[p]} + {plain[q]}: \"{strong[links[0]][1]}\""
            else: how = ''
            if sup_ab or sup_ba:
                s_, f_ = (sup_ab, a) if len(sup_ab) >= len(sup_ba) else (sup_ba, b)
                how += ('; ' if how else '') + f"{f_['name']} decks hold its " + ', '.join(f"{plain[c]} x{f_['lift'][c]:.1f}" for c in s_)
            strengths[(i, j)] = strengths[(j, i)] = (strength, how)
            over = 2 * len(shared) > min(len(ca), len(cb))
            pairs.append(f"- {a['name']} + {b['name']}: {len(links)} card links; decks hold {len(sup_ab)} / {len(sup_ba)} of the other's kernel 2x+"
                         + (f"; shares {len(shared)} of {min(len(ca), len(cb))}" + (' **over half**' if over else '') if shared else '')
                         + f"; strength {strength}")

    partners = {i: sorted((j for j in range(len(fac)) if j != i), key=lambda j: -strengths[(i, j)][0])[:PARTNERS] for i in range(len(fac))}

    for i, x in enumerate(fac):  # design markers: what its kernel's decks are like against their games' decks (step 3)
        gs = {decks[n]['game'] for n in x['decks']}
        x['letter'], (x['theme'], tf) = LETTERS[i], THEMES[x['name']]
        x['theme_likes'] = set().union(*(under(f) for f in tf))
        x['markers'] = {}
        for key in D['markers']:
            here = [decks[n]['marks'][key] for n in x['decks'] if key in decks[n]['marks']]
            every = [d['marks'][key] for d in decks if d['game'] in gs and key in d['marks']]
            if len(here) >= 5 and sum(every) and (sum(here) / len(here)) / (sum(every) / len(every)) >= D['mark_fit']:
                x['markers'][key] = round((sum(here) / len(here)) / (sum(every) / len(every)), 1)
    for i, x in enumerate(fac):
        x['list'] = lib.scores(x['concepts'])
        score = {c: v[0] for c, v in x['list'].items()}
        ex = []
        for q in ('front', 'backrow', 'lanes', 'holds'):  # (a) the board answers its concepts don't give
            if answers(x['concepts'] + ex)[q]: continue
            way, take = best_way(x, q, set(x['concepts'] + ex), score)
            if way: ex += [c for c in take if c not in ex]
        have = [j for j in partners[i] if strengths[(i, j)][0] > 0]
        others = [j for j in range(len(fac)) if j != i and j not in have]
        while len(have) < PARTNERS and others and len(ex) < EXTRAS:  # (b) short of partners: link to a non-partner's kernel
            got = {c: score[c] for c in score if c in usable and c not in ex for j in others if any(linked(c, k) for k in fac[j]['kernel'])}
            c = pick(x, got)
            if not c: break
            ex.append(c)
            new = [j for j in others if any(linked(c, k) for k in fac[j]['kernel'])]
            have += new[:PARTNERS - len(have)]; others = [j for j in others if j not in new]
        while len(ex) < 3 * EXTRAS:  # (c) the highest-scoring concepts that link to 2+ of its concepts (more than it takes, for the sharing)
            got = {c: score[c] for c in score if c in usable and c not in ex and sum(linked(c, k) for k in x['concepts']) >= 2}
            c = pick(x, got)
            if not c: break
            ex.append(c)
        x['wish'], x['score'] = ex, score
    for x in fac: x.pop('extras', None)
    took = share(lambda x: x['wish'], lambda x: EXTRAS, lambda x, c: x['score'].get(c, 0), add=False)  # extras count toward MAX_SHARE too
    for i, x in enumerate(fac):
        x['extras'] = ex = took[id(x)]; score = x['score']
        full = set(x['concepts'] + ex)
        x['answers'] = {}
        for q in ('front', 'backrow', 'lanes', 'holds'):
            own = answers(x['concepts'])[q]
            x['answers'][q] = own[0] if own else (best_way(x, q, full, {})[0] or '**missing**')
        mine = answers(x['concepts'])['cares']
        pool = {w: max((score[a] for alt in need for a in alt if a in score), default=0) for w, need in ways['cares']}
        x['answers']['cares'] = mine[0] if mine else (pick(x, pool) or '**missing**')
        e = sorted((frozenset((a, b)) for a in x['concepts'] for b in x['concepts'] if a < b and linked(a, b)), key=lambda t: -strong[t][0])
        x['wins'] = x['does'] + ('; ' + ' -> '.join(plain.get(c, c) for c in sorted(e[0])) + f": \"{strong[e[0]][1]}\"" if e else '')
        os.makedirs(os.path.join(HERE, 'lists'), exist_ok=True)
        with open(os.path.join(HERE, 'lists', x['letter'] + '.tsv'), 'w', encoding='utf-8') as w:
            w.write('concept\tscore\tlevel\tgames\n')
            for k, (sc, lv, gm) in sorted(x['list'].items(), key=lambda t: (-t[1][0], t[0])): w.write(f'{k}\t{sc}\t{lv}\t{gm}\n')
build()  # first pass: kernels from the identities
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
    """the real kernel: per question the option whose concepts go best together with the other questions' (cohesion)"""
    P = set(x['concepts'] + x['extras']); every = set().union(*ban.values())
    opts = {}
    for q in Q5:
        opts[q] = options(q, P, ban[q] | ban['all'])
        if not opts[q]:  # none of its concepts answers it: the best way from its list
            way, take = best_way(x, q, set(), {c: v for c, v in x['score'].items() if c not in ban[q] | ban['all']})
            opts[q] = [frozenset(take)] if take else []
    cur = {q: (max(o, key=lambda op: (cohesion(op | P), sorted(op))) if o else frozenset()) for q, o in opts.items()}
    for _ in range(10):
        changed = False
        for q in Q5:
            if not opts[q]: continue
            rest = set().union(*(cur[r] for r in Q5 if r != q))
            best = max(opts[q], key=lambda op: (round(cohesion(rest | op), 6), len(op), sorted(op)))
            if best != cur[q]: cur[q], changed = best, True
        if not changed: break
    return cur
def fits_in(c, k): return sum(fit2(c, o) for o in k if o != c) / max(1, len(k) - 1)
bans = {x['name']: {q: set() for q in Q5 + ('all',)} for x in fac}
for _ in range(40):
    cur = {x['name']: choose(x, bans[x['name']]) for x in fac}
    kern = {n: set().union(*c.values()) for n, c in cur.items()}
    moved = False
    for x in fac:  # (a) every kernel concept goes well with at least one other kernel concept
        k = kern[x['name']]
        for c in sorted(k):
            if len(k) > 1 and max(fit2(c, o) for o in k if o != c) < SYN: bans[x['name']]['all'].add(c); moved = True
    for q in Q5[:-1]:  # (b) no two factions answer a question with the same concept: it stays where it fits best
        users = collections.defaultdict(list)
        for n, c in cur.items():
            for k in c[q]: users[k].append(n)
        for k, ns in users.items():
            for n in sorted(ns, key=lambda n: (-fits_in(k, kern[n]), n))[1:]: bans[n][q].add(k); moved = True
    count = collections.defaultdict(list)  # (b) no kernel concept in more than MAX_SHARE factions
    for n, k in kern.items():
        for c in k: count[c].append(n)
    for c, ns in count.items():
        for n in sorted(ns, key=lambda n: (-fits_in(c, kern[n]), n))[MAX_SHARE:]: bans[n]['all'].add(c); moved = True
    if not moved: break
first = {x['name']: {'kernel': x['kernel'], 'concepts': x['concepts'], 'extras': x['extras']} for x in fac}
for x in fac:  # second pass: the real kernel, then everything else again
    x['by_question'] = cur[x['name']]; x['kernel'] = sorted(kern[x['name']]); x['first'] = first[x['name']]
    x['thin'] = False
    for k in ('concepts', 'extras', 'from_links', 'from_decks', 'from_both', 'engines'): x.pop(k, None)
build()
missed = sorted((c for c in usable if lean.get(c, 0) >= MIN_LEAN and not any(c in x['concepts'] + x['extras'] for x in fac)),
                key=lambda c: -lean[c])  # concepts many decks are built on that no faction has
with open(os.path.join(HERE, 'kernel_factions.tsv'), 'w', encoding='utf-8') as w:
    w.write('letter\tname\tdoes\ttheme\tkernel\tengines\tbricks\tconcepts\textras\tmarkers\twins\tfront\tbackrow\tlanes\tholds\tcares\tpartners\n')
    for i, x in enumerate(fac):
        w.write('\t'.join([x['letter'], x['name'], x['does'], x['theme'], ','.join(x['kernel']), ','.join(c for c in x['concepts'] if c in x['engines']),
                           ','.join(c for c in x['concepts'] if c not in x['engines']), ','.join(x['concepts']), ','.join(x['extras']),
                           ','.join(f'{k}:{v}' for k, v in x['markers'].items()), x['wins']] + [x['answers'][q] for q in ('front', 'backrow', 'lanes', 'holds', 'cares')]
                          + [','.join(fac[j]['letter'] for j in partners[i])]) + '\n')

out = ['# The factions from what they do (made by kernel_factions.py)', '',
       'Kernel: per question (removes the front unit, the back row, acts between lanes, holds a base, cares about), up to '
       f'{PER_QUESTION} concepts of the first pass that answer it and go best together (cards linked or decks built on both). Engines: concepts real cards link to 2+ kernel concepts. Bricks: '
       f'what its decks hold {DECK_LIFT:g}x+ as often as their games, with no card link to the kernel. About {OWN} concepts. '
       f"Partners: its {PARTNERS} strongest pairs (card links between their concepts, plus 3 per kernel concept the other's decks hold "
       f'{DECK_LIFT:g}x+). A concept more than {MAX_SHARE} factions want at one level goes to the {MAX_SHARE} it fits best.', '']
for i, x in enumerate(fac):
    out.append(f"## {x['name']}: {x['does']} ({len(x['decks'])} decks built on half its kernel or more)")
    out.append(f"- Kernel (cohesion {cohesion(x['kernel']):.2f}; first pass {', '.join(plain.get(c, c) for c in x['first']['kernel'])}):")
    for q in Q5:
        out.append(f"  - {QUESTION[q]}: " + (', '.join(f'{plain.get(c, c)} ({lean.get(c, 0)} decks)' for c in sorted(x['by_question'][q])) or '**none**'))
    out.append('- From card links:' + ('' if x['from_links'] else ' nothing'))
    for c in x['from_links']:
        q, pair = behind(c, x['kernel'])
        out.append(f"  - {plain[c]} ({sum(wide(c, o) for o in x['kernel'])} kernel links; strongest with {q}: {pair})")
    out.append('- From decks: ' + ('; '.join(f"{plain.get(c, c)} x{x['lift'][c]:.1f}" for c in x['from_decks']) or 'nothing'))
    if x['from_both']: out.append('- From decks and card links: ' + '; '.join(f"{plain.get(c, c)} x{x['lift'][c]:.1f}" for c in x['from_both']))
    out.append(f"- {len(x['concepts'])} concepts. Engines: " + ('; '.join(plain.get(c, c) for c in x['engines']) or '**none: no engine pair**')
               + '. Bricks: ' + ('; '.join(plain.get(c, c) for c in x['concepts'] if c not in x['engines']) or 'none'))
    out.append(f"- Theme: {x['theme']}. Design markers: " + ('; '.join(f"{D['markers'][k]} x{v}" for k, v in x['markers'].items()) or 'none'))
    out.append(f"- Extras ({len(x['extras'])}): " + '; '.join(f"{plain.get(c, c)} {x['list'][c][0]:g}" for c in x['extras']))
    out.append(f"- How it wins: {x['wins']}")
    for q in ('front', 'backrow', 'lanes', 'holds', 'cares'):
        out.append(f"- {QUESTION[q]}: {x['answers'][q]}")
    out.append(f'- Partners (its {PARTNERS} strongest; * = it is in their {PARTNERS} too):')
    for j in partners[i]:
        st, how = strengths[(i, j)]
        out.append(f"  - {fac[j]['name']}{' *' if i in partners[j] else ''} ({st}): {how}")
    out.append('')
out.append('## Concepts 10+ decks are built on that no faction has')
out += [f'- {plain.get(c, c)} ({lean[c]} decks)' for c in missed] or ['- none']
out.append('')
out.append('## Every pair')
out += pairs
text = '\n'.join(out) + '\n'
open(os.path.join(HERE, 'kernel_factions.md'), 'w', encoding='utf-8').write(text)
print(text)
