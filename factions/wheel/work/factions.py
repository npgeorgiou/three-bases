"""The 20 factions (factions/START_DESIGN-1-wheel.md step 6, 6.1 and 6.2), from work/archetype_parts.tsv (step 5),
and library/cards_db/wheel/concept_links.tsv. Every tie is broken by the archetype or concept key in
alphabetical order, so every run gives the same result.
6.1 A group of 2 archetypes scores the strong links between concepts of one archetype and concepts of the other (each two
concepts once), divided by the number of different concepts in the group. Start from the 20 best groups that keep the limits, then swap one group for another while
that lifts the weakest score (the scores from lowest up compared in order), until no swap does. Only groups whose two
archetypes share at least one concept. Limits: no archetype in more than 3 factions; no two factions share more than one
archetype; two factions share at most half of their own concepts (6.2).
6.2 From each engine part, the concept with the most strong links into the other engine parts of the faction's
archetypes (ties: the higher sum of cards, then more games), and the second best when it has at least half as many; from
each brick, the concept with the highest score on the faction's list made from its engine concepts (concept_list.py).
Usage (from library/cards_db): python3 ../../factions/wheel/work/factions.py -> factions/wheel/work/factions.tsv
(letter, archetypes, score, concepts, concepts per part, synergies); it prints the 20 and stops after 6.2."""
import collections, csv, itertools, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
WHEEL = os.path.join(HERE, '..')
LINKS = os.path.join(HERE, '..', '..', '..', 'library', 'cards_db', 'wheel', 'concept_links.tsv')
N = 20


def tsv(path):
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def num(v): return float(v) if v else 0.0


ARCH = collections.defaultdict(list)  # archetype -> [(part, engine|brick, [concepts])]
NAME = {}
for r in tsv(os.path.join(HERE, 'archetype_parts.tsv')):
    ARCH[r['key']].append((r['part'], r['kind'], r['concepts'].split(',')))
    NAME[r['key']] = r['name']
LINK = {}  # (a, b) both orders -> row
for r in tsv(LINKS):
    LINK[(r['a'], r['b'])] = LINK[(r['b'], r['a'])] = r


def strong(a, b):
    r = LINK.get((a, b))
    return bool(r) and a != b and (num(r['cards']) >= 1.2 or (num(r['rare']) >= 3 and num(r['level']) >= 1))


def concepts_of(arch): return {c for _, _, cs in ARCH[arch] for c in cs}


def score(group):
    """strong links between concepts of one archetype and concepts of the other / different concepts in the group"""
    sets = [concepts_of(a) for a in group]
    pairs = set()
    for i, j in itertools.combinations(range(len(sets)), 2):
        for a in sets[i]:
            for b in sets[j]:
                if strong(a, b): pairs.add(tuple(sorted((a, b))))
    return len(pairs) / len(set().union(*sets))


def choose(group, lib, cache={}):
    """6.2: per part of the group's archetypes, the concepts the faction plays"""
    if group in cache: return cache[group]
    engines = [(a, p, cs) for a in group for p, k, cs in ARCH[a] if k == 'engine']
    picked = []
    for a, p, cs in engines:
        others = {c for a2, p2, cs2 in engines if (a2, p2) != (a, p) for c in cs2}
        rank = []
        for c in cs:
            ls = [LINK[(c, o)] for o in others if strong(c, o)]
            rank.append((-len(ls), -sum(num(r['cards']) for r in ls), -sum(int(r['games']) for r in ls), c))
        rank.sort()
        got = [rank[0][3]]
        if len(rank) > 1 and rank[0][0] < 0 and -rank[1][0] * 2 >= -rank[0][0]: got.append(rank[1][3])
        picked.append((a, p, 'engine', got))
    own = {c for *_, got in picked for c in got}
    bricks = [(a, p, cs) for a in group for p, k, cs in ARCH[a] if k == 'brick']
    if bricks:
        sc = lib.scores(own, {c for *_, cs in bricks for c in cs})
        for a, p, cs in bricks:
            best = sorted(cs, key=lambda c: (c not in own, -sc.get(c, (0,))[0], c))[0]
            picked.append((a, p, 'brick', [best]))
    own = sorted({c for *_, got in picked for c in got})
    cache[group] = (picked, own)
    return cache[group]


def ok(groups, extra, lib):
    use = collections.Counter(a for g in groups for a in g) + collections.Counter(extra)
    if use and max(use.values()) > 3: return False
    if any(len(set(extra) & set(g)) > 1 for g in groups): return False
    mine = set(choose(extra, lib)[1])
    for g in groups:
        theirs = set(choose(g, lib)[1])
        if len(mine & theirs) * 2 > min(len(mine), len(theirs)): return False
    return True


def pick(cands, lib):
    """the 20 best groups that keep the limits; then swaps that lift the weakest score (the scores from lowest up
    compared in order)"""
    chosen = []
    for s, g in cands:
        if len(chosen) == N: break
        if not ok([x for _, x in chosen], g, lib): continue
        chosen.append((s, g))
    while True:
        now = sorted(s for s, _ in chosen)
        best = None
        for i in sorted(range(N), key=lambda i: chosen[i][0]):
            rest = chosen[:i] + chosen[i + 1:]
            for s, g in cands:
                if s <= chosen[i][0]: break
                if (s, g) in chosen or not ok([x for _, x in rest], g, lib): continue
                new = sorted([x for x, _ in rest] + [s])
                if new <= now or (best and new <= best[0]): continue
                best = (new, i, (s, g))
        if not best: return chosen
        chosen[best[1]] = best[2]


def main():
    sys.path.insert(0, HERE)
    import concept_list
    lib = concept_list.Library()
    archs = sorted(ARCH)
    cands = [(score(g), g) for g in itertools.combinations(archs, 2)]
    cands = [(round(s, 6), g) for s, g in cands if s > 0 and concepts_of(g[0]) & concepts_of(g[1])]
    cands.sort(key=lambda t: (-t[0], t[1]))
    print(f'{len(cands)} groups share a concept and score above 0')
    chosen = pick(cands, lib)
    chosen.sort(key=lambda t: (-t[0], t[1]))
    with open(os.path.join(HERE, 'factions.tsv'), 'w', encoding='utf-8') as f:
        f.write('letter\tarchetypes\tscore\tconcepts\tparts\tsynergies\n')
        for n, (s, g) in enumerate(chosen):
            picked, own = choose(g, lib)
            parts = ' | '.join(f'{a}/{p} ({k}): {",".join(got)}' for a, p, k, got in picked)
            syn = []
            for a, b in itertools.combinations(own, 2):
                if strong(a, b):
                    r = LINK[(a, b)]
                    t = f"{r['cards']}x" if num(r['cards']) >= 1.2 else f"rare {r['rare']}"
                    syn.append(f"{a}+{b} ({t}, {r['games']} games): {r['texts'].split(' | ')[0]}")
            f.write(f"{chr(65 + n)}\t{','.join(g)}\t{s}\t{','.join(own)}\t{parts}\t{' || '.join(syn)}\n")
            print(f"{chr(65 + n)} {s:.3f} {' + '.join(NAME[a] for a in g)}")
    print('weakest:', min(s for s, _ in chosen))


if __name__ == '__main__':
    main()
