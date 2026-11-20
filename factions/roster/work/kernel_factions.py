"""Step 6 of the roster (factions/START_DESIGN-1-roster.md, which has every rule): the factions from what they do.
1. Identity (IDENTITIES, Claude's): what the faction does, in plain words, made of headings of library/concept_tree.txt.
   Its kernel: their usable concepts (effects and "when..."; a drawback only for Eats its own) that MIN_LEAN+ decks are
   built on, the KERNEL with most decks; a concept two identities want goes to the one whose other concepts' decks
   hold it more.
2. How well two concepts go together (fit2): the higher of how many times chance real cards link them and real decks
   hold both, on a log scale where FULL times chance is 1. A concept's fit to a faction: its average fit2 to the kernel.
3. Its concepts: one ranked list, every other usable concept by its fit, filling the faction to LIST concepts with the
   kernel. A concept is in at most MAX_SHARE factions (share()): it stays where it fits best and the others take their
   next best. A concept COMMON+ decks are built on that no faction has takes the place of the weakest concept of the
   faction it fits best, when it fits at least 0.8 as well.
4. What the faction is about: the kernel and its strong concepts, those with fit STRONG or more (twice chance). Only
   these count below: its decks (the decks whose cards with them make up DECK_SHARE times their game's average share or
   more), its deck style (design markers, deck_scores.json), its partners (its PARTNERS strongest pairs: strong card
   links between the two factions' concepts, plus 3 per kernel concept of one that the other's decks hold DECK_LIFT
   times as often as their games), its list (concept_list.Library -> lists/<letter>.tsv) and what of it acts on enemy
   units (concepts under hurts_enemy in the concept tree; none is flagged for design).
5. Its people (THEMES, Claude's): one new world, WORLD.
python3 factions/roster/work/kernel_factions.py (from the repo, about a minute; needs links.sqlite) -> kernel_factions.md
(one sheet per faction), kernel_factions.tsv (read by make_faction.py and the map), kernel_factions_summary.json (the
numbers to compare runs) and lists/."""
import collections, csv, json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, HERE)
LIST, STRONG, KERNEL, MIN_LEAN, MIN_DECKS, DECK_SHARE, FULL = 22, 1 / 3, 6, 10, 3, 2, 8  # 22 and STRONG: Kaptain; the rest Claude's
COMMON, MAX_SHARE, PARTNERS, DECK_LIFT = 15, 3, 5, 1.5  # 5 partners: Kaptain; the rest Claude's
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
THEMES = {  # per faction: its people in Veyl, the real-world model it is written from (hidden, never shown)
    "Can't be broken": ('The Shellwardens of Kesh: a coastal people who grow living coral over their bodies and hold the tide-gates; '
                        'they do not fall', 'the defenders of the walls of Constantinople'),
    'Kills brutally': ('The Ashen Hunt: riders on burn-scarred lizards who sweep the dune seas and leave nothing standing',
                       'the Mongol tumens'),
    'Messes you up': ('The Whisper Choir: masked singers whose songs unknit memory, break oaths and turn warriors against their orders',
                      'the spies and poisoners of the Venetian Council of Ten'),
    'Moves': ('The Drift Clans: sky-raft nomads who ride the winds between floating islands and shove their foes off the edges',
              'the Comanche horse raiders'),
    'Thrives on spells': ('The Lantern Scribes: scholars who write with ink distilled from starlight; every word they write makes the next one brighter',
                          'the alchemists of Rudolf II in Prague'),
    'Waits': ('The Deep Bell: an old order inside the mountain that winds a vast clockwork for years, then rings the bell that flattens the valley',
              'World War I artillery'),
    'Swarms': ('The Hive of Many Mouths: insect folk who hatch by the thousand from amber nests and cover the ground at once',
               'the Zulu regiments'),
    'Grows': ('The Rootborn: walking tree-giants who swell with every season they survive',
              'the sumo stables of Edo'),
    'Comes back': ('The Returning Tide: drowned sailors the sea sends back to the shore every dawn',
                   'the embalmers of ancient Egypt'),
    'Eats its own': ('The Ember Cult: fire-worshippers who feed their own to the furnace for power',
                     'the sacrifice priests of Tenochtitlan'),
}
D = json.load(open(os.path.join(HERE, 'deck_scores.json'), encoding='utf-8'))
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
def share(pool, room, fit):
    """sharing: each faction takes its first room(x) of pool(x); a concept that would then be in more than MAX_SHARE
    factions (counting the kernels) stays with the ones it fits best (fit(x, c), ties by name), the others take their
    next best"""
    banned = {id(x): set() for x in fac}
    before = collections.Counter(c for x in fac for c in x['kernel'])
    while True:
        took = {id(x): [c for c in pool(x) if c not in banned[id(x)]][:max(0, room(x))] for x in fac}
        crowded = sorted({c for v in took.values() for c in v if before[c] + sum(c in w for w in took.values()) > MAX_SHARE})
        if not crowded: return took
        for c in crowded:
            takers = sorted((x for x in fac if c in took[id(x)]), key=lambda x: (-fit(x, c), x['name']))
            for x in takers[max(0, MAX_SHARE - before[c]):]: banned[id(x)].add(c)
sys.path.insert(0, HERE); import concept_list
lib = concept_list.Library()
hurts = under('hurts_enemy')
def markers_of(ds):
    """design markers: what the decks ds are like against all decks of their games (step 3), times as much"""
    gs, out = {decks[n]['game'] for n in ds}, {}
    for key in D['markers']:
        here = [decks[n]['marks'][key] for n in ds if key in decks[n]['marks']]
        every = [d['marks'][key] for d in decks if d['game'] in gs and key in d['marks']]
        if len(here) >= 5 and sum(every) and (sum(here) / len(here)) / (sum(every) / len(every)) >= D['mark_fit']:
            out[key] = round((sum(here) / len(here)) / (sum(every) / len(every)), 1)
    return out
def fit_to(kernel):
    """every other usable concept's fit to the kernel: its average fit2 to the kernel's concepts"""
    return {c: sum(fit2(c, q) for q in kernel) / len(kernel) for c in usable if c not in kernel}
def about(kernel, concepts, fit):
    """what the faction is about: the kernel and its strong concepts"""
    return list(kernel) + [c for c in concepts if c not in kernel and fit.get(c, 0) >= STRONG]
def holders(c): return sum(c in x['concepts'] for x in fac)
name = lambda c: re.sub(r' \([^)]*\)', '', plain.get(c, c))  # plain name, nothing in brackets
def sheet(title, does, theme, fams, kernel, strong_ones, concepts, enemy, markers, partner_names):
    """one faction's page for Kaptain: a header per part, every item a list, plain names, no numbers"""
    page = [f'## {title}', '']
    if does: page += [f'{does.capitalize()}.', '']
    if theme: page += ['### Who they are', '', f'{theme}.', '']
    if fams: page += ['### Identity: its families of the concept tree', ''] + [f'- {name(f)}' for f in fams] + ['']
    page += ['### Concepts', ''] + [f'- [K] {name(c)}' for c in kernel] + [f'- [S] {name(c)}' for c in strong_ones]
    page += [f'- {name(c)}' for c in concepts if c not in kernel and c not in strong_ones]
    page += ['', '### What of it acts on enemy units', ''] + ([f'- {name(c)}' for c in enemy] or ['- nothing: design must give it a way'])
    page += ['', '### Deck style: what its decks are like', ''] + ([f"- {D['markers'][k]}" for k in markers] or ['- nothing stands out'])
    if partner_names: page += ['', '### Partners', ''] + [f'- {n}' for n in partner_names]
    return page + ['']
KEY = '[K] marks a kernel concept, [S] a strong one: it goes with the kernel twice as often as chance or more.'

def run():
    """step 6 for the roster: the ranked lists, what each faction is about, partners, the pages"""
    global missed
    for x in fac:
        x['fit'] = fit_to(x['kernel']); x['ranked'] = sorted(x['fit'], key=lambda c: (-x['fit'][c], c))
    took = share(lambda x: x['ranked'], lambda x: LIST - len(x['kernel']), lambda x, c: x['fit'][c])
    for x in fac: x['concepts'] = x['kernel'] + took[id(x)]
    for c in sorted((c for c in usable if lean.get(c, 0) >= COMMON and not holders(c)), key=lambda c: -lean[c]):
        x = max(fac, key=lambda x: (x['fit'].get(c, 0), x['name']))  # a common concept no faction has, in the faction it fits best
        weak = min(took[id(x)], key=lambda o: (x['fit'][o], o)) if took[id(x)] else None
        if weak and x['fit'].get(c, 0) >= 0.8 * x['fit'][weak]: x['concepts'][x['concepts'].index(weak)] = c; took[id(x)][took[id(x)].index(weak)] = c
    missed = sorted((c for c in usable if lean.get(c, 0) >= MIN_LEAN and not holders(c)), key=lambda c: -lean[c])
    for i, x in enumerate(fac):
        x['letter'], (x['theme'], x['model']) = LETTERS[i], THEMES[x['name']]
        x['about'] = about(x['kernel'], x['concepts'], x['fit']); x['strong'] = x['about'][len(x['kernel']):]
        x['decks'] = kernel_decks(x['about']); x['lift'] = deck_lift(x['decks']); x['markers'] = markers_of(x['decks'])
        x['enemy'] = [c for c in x['about'] if c in hurts]
        x['list'] = lib.scores(x['about'])
        os.makedirs(os.path.join(HERE, 'lists'), exist_ok=True)
        with open(os.path.join(HERE, 'lists', x['letter'] + '.tsv'), 'w', encoding='utf-8') as w:
            w.write('concept\tscore\tlevel\tgames\n')
            for k, (sc, lv, gm) in sorted(x['list'].items(), key=lambda t: (-t[1][0], t[0])): w.write(f'{k}\t{sc}\t{lv}\t{gm}\n')
    strengths = {}
    for i, a in enumerate(fac):
        for j, b in enumerate(fac):
            if j <= i: continue
            links = {frozenset((p, q)) for p in a['about'] for q in b['about'] if linked(p, q) and p not in b['about'] and q not in a['about']}
            sup = sum(a['lift'].get(c, 0) >= DECK_LIFT for c in b['kernel']) + sum(b['lift'].get(c, 0) >= DECK_LIFT for c in a['kernel'])
            strengths[(i, j)] = strengths[(j, i)] = len(links) + 3 * sup
    partners = {i: sorted((j for j in range(len(fac)) if j != i), key=lambda j: (-strengths[(i, j)], j))[:PARTNERS] for i in range(len(fac))}
    with open(os.path.join(HERE, 'kernel_factions.tsv'), 'w', encoding='utf-8') as w:
        w.write('letter\tname\tdoes\ttheme\tkernel\tstrong\tconcepts\tenemy\tmarkers\tpartners\n')
        for i, x in enumerate(fac):
            w.write('\t'.join([x['letter'], x['name'], x['does'], x['theme'], ','.join(x['kernel']), ','.join(x['strong']), ','.join(x['concepts']),
                               ','.join(x['enemy']), ','.join(f'{k}:{v}' for k, v in x['markers'].items()),
                               ','.join(fac[j]['letter'] for j in partners[i])]) + '\n')
    page = ['# The factions', '', f'The world: {WORLD}.', '', KEY, '']
    for i, x in enumerate(fac):
        page += sheet(x['name'], x['does'], x['theme'], x['fams'], x['kernel'], x['strong'], x['concepts'], x['enemy'], x['markers'],
                      [fac[j]['name'] for j in partners[i]])
    if missed: page += ['## In no faction yet', ''] + [f'- {name(c)}' for c in missed] + ['']
    open(os.path.join(HERE, 'kernel_factions.md'), 'w', encoding='utf-8').write('\n'.join(page) + '\n')
    allc = {x['name']: set(x['concepts']) for x in fac}
    jac = [len(allc[a['name']] & allc[b['name']]) / len(allc[a['name']] | allc[b['name']]) for i, a in enumerate(fac) for b in fac[i + 1:]]
    summary = {'kernel cohesion': round(sum(cohesion(x['kernel']) for x in fac) / len(fac), 3),
               'about cohesion': round(sum(cohesion(x['about']) for x in fac) / len(fac), 3),
               'whole cohesion': round(sum(cohesion(x['concepts']) for x in fac) / len(fac), 3),
               'strong concepts': [len(x['strong']) for x in fac],
               'nothing acts on enemy units': [x['name'] for x in fac if not x['enemy']],
               'common concepts placed': sum(1 for c in usable if lean.get(c, 0) >= COMMON and holders(c)),
               'common concepts': sum(1 for c in usable if lean.get(c, 0) >= COMMON),
               'overlap mean': round(sum(jac) / len(jac), 3), 'overlap max': round(max(jac), 3)}
    json.dump(summary, open(os.path.join(HERE, 'kernel_factions_summary.json'), 'w'))


if __name__ == '__main__':
    run()
