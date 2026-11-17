"""Step 6, the archetype map (factions/START_DESIGN-1-wheel.md): each concept of an archetype's parts is a node; between
the concepts of two engine parts of one archetype, an edge with the step 5 numbers (cards, games, level), the top link
text, one real card pair and a note when the edge is weak (about the player, or decks only) (the strongest link of that text). A pair joined only by real decks has no card pair. Bricks are nodes with no edges.
Writes work/archetype_map.tsv, work/archetype_gaps.tsv (engine parts whose concepts have no joined edge) and
factions/wheel-archetypes.html. Run from library/cards_db: python3 ../../factions/wheel/work/archetype_map.py"""
import collections, csv, html, itertools, json, os, sqlite3, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, '..', '..', '..', 'library', 'cards_db')
sys.path.insert(0, DB)
import axes, mechanics_wheel


PLAYER = ('player', 'nexus', 'leader', 'hero', 'face')  # link texts about hitting the player: no player health here


def note(r, pair):
    """why an edge is weak: its top link text is about the player, or only real decks join it (no card pair)"""
    text = (r['texts'].split(' | ')[0] if r['texts'] else '').lower()
    if any(w in text for w in PLAYER): return 'about the player'
    if not pair: return 'decks only'
    return ''


def joined(r):
    """step 5's join: cards 1.2+, or decks 1.5+, or rare 3+ with a level of 1+"""
    f = lambda k: float(r[k]) if r[k] else 0.0
    return f('cards') >= 1.2 or f('decks') >= 1.5 or (f('rare') >= 3 and f('level') >= 1)


def main():
    arch = list(csv.DictReader(open(os.path.join(HERE, '..', 'archetypes.tsv'), encoding='utf-8'), delimiter='\t'))
    links = {}
    for r in csv.DictReader(open(os.path.join(DB, 'wheel', 'concept_links.tsv'), encoding='utf-8'), delimiter='\t'):
        links[frozenset((r['a'], r['b']))] = r
    parts = collections.defaultdict(list)
    for r in arch:
        parts[r['key']].append(r)
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
            if not n:
                linked = sum(1 for a in x['concepts'].split(',') for b in y['concepts'].split(',')
                             if links.get(frozenset((a, b))) and float(links[frozenset((a, b))]['level'] or 0) > 0)
                gaps.append((key, x['part'], y['part'], len(x['concepts'].split(',')) * len(y['concepts'].split(',')), linked))
    examples = card_pairs(wanted)
    behind = collections.Counter()  # the cards behind the most edges (one card can carry many)
    with open(os.path.join(HERE, 'archetype_map.tsv'), 'w', encoding='utf-8') as f:
        f.write('archetype\tpart_a\ta\tpart_b\tb\tcards\tdecks\tgames\tlevel\ttext\tcard_pair\tnote\n')
        for key, pa, a, pb, b, r in edges:
            text = r['texts'].split(' | ')[0] if r['texts'] else ''
            pair = examples.get((frozenset((a, b)), text)) or examples.get((frozenset((a, b)), ''), '')
            f.write('\t'.join([key, pa, a, pb, b, r['cards'], r['decks'], r['games'], r['level'], text, pair, note(r, pair)]) + '\n')
            for card in pair.split(': ', 1)[-1].split(' + ') if pair else (): behind[card] += 1
    with open(os.path.join(HERE, 'archetype_gaps.tsv'), 'w', encoding='utf-8') as f:
        f.write('archetype\tpart_a\tpart_b\tconcept_pairs\tpairs_with_any_link\n')
        for g in gaps: f.write('\t'.join(map(str, g)) + '\n')
    page(arch, edges, examples)
    print(f'{len(edges)} edges, {len(gaps)} engine part pairs with no joined edge')
    print('cards behind the most edges: ' + ', '.join(f'{k} {n}' for k, n in behind.most_common(8)))


def card_pairs(wanted):
    """per concept pair and link text (and per pair alone, text ''): the real card pair of its strongest link, 'game: A + B'"""
    c, games, x, con, pools, stats = mechanics_wheel.setup()
    keys = [(k, 0, '', k, cons, '') for k, _, cons, *_ in mechanics_wheel.concepts(con)]
    name = dict(((i), (g, n)) for i, g, n in c.execute('select id, game, name from card'))
    best = {}
    L = sqlite3.connect(os.path.join(DB, 'links.sqlite'))
    for g, a, b, sa, sb, w, kind, text in L.execute(
            'select l.game, a, b, a_ab, b_ab, weight, p.kind, p.text from link l join phrase p on p.id=l.phrase where a != b'):
        ka, kb = axes.side_keys(a, sa, g, keys, con), axes.side_keys(b, sb, g, keys, con)
        for p in {frozenset((u, v)) for u in ka for v in kb if u != v} & wanted:
            t = (p, f'{kind}: {text}')
            for t in (t, (p, '')):
                if t not in best or (w or 0) > best[t][0]:
                    best[t] = (w or 0, f'{g}: {name[a][1]} + {name[b][1]}')
    return {t: v[1] for t, v in best.items()}


def page(arch, edges, examples):
    """factions/wheel-archetypes.html: pick one archetype or all; nodes are concepts, edges carry the numbers"""
    names = {}
    for line in open(os.path.join(DB, '..', 'concept_tree.txt'), encoding='utf-8'):
        p = line.split(' | ')
        if len(p) > 2 and not line.startswith('#'): names[p[0].strip()] = p[1].strip()
    data = {'archetypes': {}, 'edges': []}
    for r in arch:
        a = data['archetypes'].setdefault(r['key'], {'name': r['name'], 'what': r['in_this_game'], 'parts': []})
        a['parts'].append({'part': r['part'], 'kind': r['kind'], 'concepts': r['concepts'].split(',')})
    for key, pa, a, pb, b, r in edges:
        text = r['texts'].split(' | ')[0] if r['texts'] else ''
        data['edges'].append({'arch': key, 'a': a, 'b': b, 'cards': r['cards'], 'decks': r['decks'], 'games': r['games'], 'level': r['level'],
                              'text': text, 'pair': examples.get((frozenset((a, b)), text)) or examples.get((frozenset((a, b)), ''), ''),
                              'note': note(r, examples.get((frozenset((a, b)), text)) or examples.get((frozenset((a, b)), ''), ''))})
    data['names'] = names
    tpl = open(os.path.join(HERE, 'archetype_map_template.html'), encoding='utf-8').read()
    out = os.path.join(HERE, '..', '..', 'wheel-archetypes.html')
    open(out, 'w', encoding='utf-8').write(tpl.replace('/*DATA*/null', json.dumps(data)))


if __name__ == '__main__':
    main()
