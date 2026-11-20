"""Step 5, the archetype map (factions/START_DESIGN-1-wheel.md), from the archetypes of step 3 (step3_groups.py). A part
whose concepts have a joined link with another part of the same archetype is an engine, any other part a brick; the parts
with their kind go to work/archetype_parts.tsv. Each concept of an archetype's parts is a node; between
the concepts of two engine parts of one archetype, an edge with the step 4 numbers (cards, decks, games, level), the top
link text, the real card pair of its strongest link (none when only real decks join them) and a note when the edge is
weak (about the player, or decks only). Bricks are nodes with no edges.
Step 6's factions (work/kernel_factions.tsv) are on the page too: each concept a part (core and engines blue, bricks
grey, extras dashed), its lines the joined links between its core and engine concepts.
Writes work/archetype_parts.tsv, work/archetype_map.tsv, work/archetype_gaps.tsv (engine parts whose concepts have no joined edge) and
factions/wheel-archetypes.html (every concept of step 3 at a fixed place, laid out from the real decks that lean on
it; every joined pair between them for the links between ticked archetypes; two ticked archetypes as one faction, as
step 6 makes it; concepts picked by hand checked against the real decks and factions, as step 3 does). Run from library/cards_db: python3 ../../factions/wheel/work/archetype_map.py"""
import collections, csv, itertools, json, math, os, re, sqlite3, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, '..', '..', '..', 'library', 'cards_db')
sys.path.insert(0, DB)
import concept_tags, mechanics_wheel
sys.path.insert(0, HERE)
import step3_groups


PLAYER = ('player', 'nexus', 'leader', 'hero', 'face')  # link texts about hitting the player: no player health here


def note(p, pair, player):
    """why an edge is weak: most of its card links are about the player, or only real decks join it (no card pair)"""
    if player.get(p, 0) > 0.5: return 'about the player'
    if not pair: return 'decks only'
    return ''


def joined(r):
    """step 4's join: cards 1.2+, or decks 1.5+, or rare 3+ with a level of 1+"""
    f = lambda k: float(r[k]) if r[k] else 0.0
    return f('cards') >= 1.2 or f('decks') >= 1.5 or (f('rare') >= 3 and f('level') >= 1)


def main():
    arch = step3_groups.rows()
    links = {}
    for r in csv.DictReader(open(os.path.join(DB, 'wheel', 'concept_links.tsv'), encoding='utf-8'), delimiter='\t'):
        links[frozenset((r['a'], r['b']))] = r
    parts = collections.defaultdict(list)
    for r in arch:
        parts[r['key']].append(r)
    for ps in parts.values():  # engine: a joined link from one of its concepts to a concept of another part of the archetype
        for x in ps:
            x['kind'] = 'engine' if any(links.get(frozenset((a, b))) and joined(links[frozenset((a, b))])
                                        for y in ps if y is not x for a in x['concepts'].split(',')
                                        for b in y['concepts'].split(',') if a != b) else 'brick'
    with open(os.path.join(HERE, 'archetype_parts.tsv'), 'w', encoding='utf-8') as f:
        f.write('key\tname\tpart\tkind\tconcepts\n')
        for r in arch: f.write('\t'.join([r['key'], r['name'], r['part'], r['kind'], r['concepts']]) + '\n')
    for f in csv.DictReader(open(os.path.join(HERE, 'kernel_factions.tsv'), encoding='utf-8'), delimiter='\t'):  # step 6's factions
        key, eng = 'F' + f['letter'], f['engines'].split(',')
        for c in f['concepts'].split(',') + [x for x in f['extras'].split(',') if x]:
            level = 'core' if c in f['kernel'].split(',') else 'engine' if c in eng else 'brick' if c in f['bricks'].split(',') else 'extra'
            r = {'key': key, 'name': f"Faction {f['letter']}: {f['name']}", 'part': level, 'concepts': c, 'in_this_game': f['does'],
                 'kind': 'engine' if level in ('core', 'engine') else level, 'faction': True,
                 'markers': dict(m.split(':') for m in f['markers'].split(',') if m)}
            arch.append(r); parts[key].append(r)
    wanted, edges, gaps = set(), [], []
    for key, ps in parts.items():
        for x, y in itertools.combinations(ps, 2):
            if x['kind'] != 'engine' or y['kind'] != 'engine': continue
            n = 0
            for a in x['concepts'].split(','):
                for b in y['concepts'].split(','):
                    r = links.get(frozenset((a, b)))
                    if a == b or not r or not joined(r): continue
                    edges.append((key, x['part'], a, y['part'], b, r)); wanted.add(frozenset((a, b))); n += 1
            if not n and not x.get('faction'):
                linked = sum(1 for a in x['concepts'].split(',') for b in y['concepts'].split(',')
                             if links.get(frozenset((a, b))) and float(links[frozenset((a, b))]['level'] or 0) > 0)
                gaps.append((key, x['part'], y['part'], len(x['concepts'].split(',')) * len(y['concepts'].split(',')), linked))
    usable = [r['concept'] for r in csv.DictReader(open(os.path.join(HERE, 'concepts.tsv'), encoding='utf-8'), delimiter='\t')
              if r['kind'] == 'usable']
    every = [(p, r) for p, r in links.items() if len(p) == 2 and p <= set(usable) and joined(r)]
    wanted |= {p for p, _ in every}
    examples, player = card_pairs(wanted)
    behind = collections.Counter()  # the cards behind the most edges (one card can carry many)
    with open(os.path.join(HERE, 'archetype_map.tsv'), 'w', encoding='utf-8') as f:
        f.write('archetype\tpart_a\ta\tpart_b\tb\tcards\tdecks\tgames\tlevel\ttext\tcard_pair\tnote\n')
        for key, pa, a, pb, b, r in edges:
            text = r['texts'].split(' | ')[0] if r['texts'] else ''
            pair = examples.get((frozenset((a, b)), text)) or examples.get((frozenset((a, b)), ''), '')
            f.write('\t'.join([key, pa, a, pb, b, r['cards'], r['decks'], r['games'], r['level'], text, pair, note(frozenset((a, b)), pair, player)]) + '\n')
            for card in pair.split(': ', 1)[-1].split(' + ') if pair else (): behind[card] += 1
    with open(os.path.join(HERE, 'archetype_gaps.tsv'), 'w', encoding='utf-8') as f:
        f.write('archetype\tpart_a\tpart_b\tconcept_pairs\tpairs_with_any_link\n')
        for g in gaps: f.write('\t'.join(map(str, g)) + '\n')
    page(arch, edges, examples, player, usable, every)
    print(f'{len(edges)} edges, {len(gaps)} engine part pairs with no joined edge')
    print('cards behind the most edges: ' + ', '.join(f'{k} {n}' for k, n in behind.most_common(8)))


def card_pairs(wanted):
    """per concept pair and link text (and per pair alone, text ''): the real card pair of its strongest link, 'game: A + B';
    per concept pair, the share of its card links whose text is about hitting the player"""
    c, games, x, con, pools, stats = mechanics_wheel.setup()
    keys = mechanics_wheel.concepts(con)
    name = dict(((i), (g, n)) for i, g, n in c.execute('select id, game, name from card'))
    best, total, onplayer = {}, collections.Counter(), collections.Counter()
    L = sqlite3.connect(os.path.join(DB, 'links.sqlite'))
    for g, a, b, sa, sb, w, kind, text in L.execute(
            'select l.game, a, b, a_ab, b_ab, weight, p.kind, p.text from link l join phrase p on p.id=l.phrase where a != b'):
        ka, kb = concept_tags.side_keys(a, sa, g, keys, con), concept_tags.side_keys(b, sb, g, keys, con)
        about = any(x in text.lower() for x in PLAYER)
        for p in {frozenset((u, v)) for u in ka for v in kb if u != v} & wanted:
            total[p] += 1; onplayer[p] += about
            t = (p, f'{kind}: {text}')
            for t in (t, (p, '')):
                if t not in best or (w or 0) > best[t][0]:
                    best[t] = (w or 0, f'{g}: {name[a][1]} + {name[b][1]}')
    return {t: v[1] for t, v in best.items()}, {p: onplayer[p] / total[p] for p in total}


def layout(D):
    """fixed places for the concepts of step 3, by the groups of step 3 (Claude's): each concept is the list, per
    group, of how much more often the group's decks lean on it than all decks do; two concepts are as close as those
    lists are alike (cosine), so the concepts of one group sit together; t-SNE (seeded) lays them out. A concept no
    deck leans on sits on a ring around the rest"""
    import numpy as np
    from sklearn.manifold import TSNE
    nodes, decks, groups = D['nodes'], D['decks'], D['groups']
    lean = np.array([[c in d['z'] for c in nodes] for d in decks], dtype=float)
    every = lean.mean(0)
    M = np.array([lean[g['decks']].mean(0) for g in groups]).T  # concept x group: share of the group's decks leaning on it
    with np.errstate(divide='ignore', invalid='ignore'):
        M = np.where(every[:, None] > 0, M / every[:, None], 0)
    M = np.maximum(M - 1, 0)  # only what a group leans on more than all decks do
    used = [i for i in range(len(nodes)) if M[i].any()]
    U = M[used] / np.linalg.norm(M[used], axis=1, keepdims=True)
    dist = np.clip(1 - U @ U.T, 0, None)
    np.fill_diagonal(dist, 0)
    xy = TSNE(n_components=2, metric='precomputed', init='random', perplexity=8, random_state=7).fit_transform(dist).astype(float)
    lo, hi = np.percentile(xy, 2, axis=0), np.percentile(xy, 98, axis=0)  # a few far concepts are pulled to the edge
    fit = lambda v, a, b, w: round(float(60 + w * min(1, max(0, (v - a) / (b - a)))), 1)
    out = {nodes[i]: [fit(xy[n, 0], lo[0], hi[0], 760), fit(xy[n, 1], lo[1], hi[1], 860)] for n, i in enumerate(used)}
    alone = [c for c in nodes if c not in out]
    for i, c in enumerate(alone):
        t = 2 * math.pi * i / max(1, len(alone))
        out[c] = [round(440 + 420 * math.cos(t), 1), round(490 + 460 * math.sin(t), 1)]
    return out


def unclash(pos, names, rounds=3000):
    """move dots apart until no two names on the page overlap (each name a box beside its dot, about 6.2 units a
    letter); a little at a time, along the side where the boxes overlap least (Claude's)"""
    short = lambda c: re.sub(r' \(.*\)$', '', names.get(c, c))
    ks = sorted(pos)
    w = {k: 14 + 6.2 * len(short(k)) for k in ks}
    box = lambda k: (pos[k][0] - 6, pos[k][1] - 9, pos[k][0] + w[k], pos[k][1] + 7)
    for _ in range(rounds):
        moved = False
        for i, a in enumerate(ks):
            A = box(a)
            for b in ks[i + 1:]:
                B = box(b)
                ox, oy = min(A[2], B[2]) - max(A[0], B[0]), min(A[3], B[3]) - max(A[1], B[1])
                if ox <= 0 or oy <= 0: continue
                moved = True
                if oy <= ox:
                    d = (oy / 2 + 0.5) * (1 if pos[b][1] >= pos[a][1] else -1)
                    pos[a][1] -= d; pos[b][1] += d
                else:
                    d = (ox / 2 + 0.5) * (1 if pos[b][0] >= pos[a][0] else -1)
                    pos[a][0] -= d; pos[b][0] += d
                A = box(a)
        if not moved: break
    xs = [v[0] for v in pos.values()]; ys = [v[1] for v in pos.values()]
    right = max(pos[k][0] + w[k] for k in ks)
    for k in ks: pos[k] = [round(pos[k][0], 1), round(pos[k][1], 1)]
    return [round(min(xs) - 20, 1), round(min(ys) - 20, 1), round(right - min(xs) + 40, 1), round(max(ys) - min(ys) + 40, 1)]


def page(arch, edges, examples, player, usable, every):
    """factions/wheel-archetypes.html: every usable concept at a fixed place; tick archetypes to light their concepts,
    their lines, and the real links between the ticked archetypes"""
    names = {}
    for line in open(os.path.join(DB, '..', 'concept_tree.txt'), encoding='utf-8'):
        p = line.split(' | ')
        if len(p) > 2 and not line.startswith('#'): names[p[0].strip()] = p[1].strip()
    data = {'archetypes': {}, 'edges': []}
    for r in arch:
        a = data['archetypes'].setdefault(r['key'], {'name': r['name'], 'what': r['in_this_game'], 'parts': [],
                                                     'faction': r.get('faction', False), 'markers': r.get('markers', {})})
        a['parts'].append({'part': r['part'], 'kind': r['kind'], 'concepts': r['concepts'].split(',')})
    for key, pa, a, pb, b, r in edges:
        text = r['texts'].split(' | ')[0] if r['texts'] else ''
        data['edges'].append({'arch': key, 'a': a, 'b': b, 'cards': r['cards'], 'decks': r['decks'], 'games': r['games'], 'level': r['level'],
                              'text': text, 'pair': examples.get((frozenset((a, b)), text)) or examples.get((frozenset((a, b)), ''), ''),
                              'note': note(frozenset((a, b)), examples.get((frozenset((a, b)), text)) or examples.get((frozenset((a, b)), ''), ''), player)})
    D = json.load(open(step3_groups.FILE, encoding='utf-8'))
    names.update({c: D['plain'][c] for c in D['nodes'] if c not in names})
    data['names'] = names
    data['pos'] = {c: v for c, v in layout(D).items() if c not in D['unit']}  # design markers are no dots
    data['view'] = unclash(data['pos'], names)
    col = {c: i for i, c in enumerate(D['nodes'])}
    data['nodes'] = D['nodes']
    data['markerNames'] = D['markers']
    for k, m in step3_groups.markers().items(): data['archetypes'][k]['markers'] = m
    for a in data['archetypes'].values():
        if a['faction']: a['markers'] = {k: float(v) for k, v in a['markers'].items()}
    data['decks'] = [[d['game'], d['name'], sorted(col[c] for c in d['z'])] for d in D['decks']]
    data['factions'] = [[f['game'], f['faction'], f['counts']] for f in D['factions']]
    data['gameCounts'] = D['game_counts']
    data['links'] = []
    for p, r in every:
        a, b = sorted(p)
        text = r['texts'].split(' | ')[0] if r['texts'] else ''
        pair = examples.get((p, text)) or examples.get((p, ''), '')
        data['links'].append({'a': a, 'b': b, 'cards': r['cards'], 'decks': r['decks'], 'games': r['games'], 'rare': r['rare'],
                              'level': r['level'], 'text': text,
                              'pair': pair, 'note': note(p, pair, player)})
    tpl = open(os.path.join(HERE, 'archetype_map_template.html'), encoding='utf-8').read()
    out = os.path.join(HERE, '..', '..', 'wheel-archetypes.html')
    open(out, 'w', encoding='utf-8').write(tpl.replace('/*DATA*/null', json.dumps(data)))


if __name__ == '__main__':
    main()
