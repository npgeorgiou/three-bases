"""Experiment (not agreed): factions built from halves of Kaptain's deck archetypes (factions/wheel/deck_archetypes.tsv).
python3 factions/wheel/work/kernel_factions.py [N]  (from the repo; N factions, default 5) -> factions/wheel/work/kernel_factions.md
1. A half: one part of a deck archetype (combo, control_combo and extra_turns are off the list). Each deck archetype is cut
   in two at the two parts real cards link most (strong links of step 4); its half's concept is the part's concept with
   the most strong links into the other half, among concepts 10+ decks lean on (ties: more decks; Claude's).
2. The N factions make N(N-1)/2 pairs; each pair gets one deck archetype, one half to each faction, so each faction holds
   N-1 halves, its kernels. A seeded search picks the deck archetypes and their sides: the most strong card links
   between the two halves of every pair and inside every faction's kernels, no kernel concept in two factions (Claude's).
3. Each faction is filled out from its decks (make_faction.py's rule: the decks that lean on a kernel, the concepts they
   lean on 3 times as often as their games' decks and by 8% of them), up to OWN concepts, kernels first.
4. Card links split them: an engine has a strong card link with another of the faction's concepts, a brick has none.
5. Checks: two factions share at most half of their concepts; per pair, the strong card links between their concepts and
   the deck archetypes they can play together (a half of it in each)."""
import csv, json, math, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, HERE)
import step3_groups
N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
OWN, MIN_LEAN, LIFT, SHARE, MIN_DECKS = 12, 10, 3.0, 0.08, 3  # Claude's
OFF = ('combo', 'control_combo', 'extra_turns')
D = json.load(open(step3_groups.FILE, encoding='utf-8'))
plain, decks, UNIT = D['plain'], D['decks'], set(D['unit'])
lean = {}
for d in decks:
    for c in d['z']: lean[c] = lean.get(c, 0) + 1
strong = {}
for r in csv.DictReader(open(os.path.join(ROOT, 'library/cards_db/wheel/concept_links.tsv'), encoding='utf-8'), delimiter='\t'):
    cards, rare, level = float(r['cards'] or 0), float(r['rare'] or 0), float(r['level'] or 0)
    if cards >= 1.2 or (rare >= 3 and level >= 1): strong[frozenset((r['a'], r['b']))] = (cards, r['texts'].split(' | ')[0])
def linked(a, b): return a != b and frozenset((a, b)) in strong

parts = {}
for r in csv.DictReader(open(os.path.join(HERE, '..', 'deck_archetypes.tsv'), encoding='utf-8'), delimiter='\t'):
    if r['key'] in OFF: continue
    parts.setdefault(r['key'], (r['name'], []))[1].append((r['part'], [c for c in r['concepts'].split(',') if c]))
halves = {}  # deck archetype -> ((part name, concept), (part name, concept), links between the halves)
for k, (name, ps) in parts.items():
    best = None
    for i in range(len(ps)):
        for j in range(i + 1, len(ps)):
            n = sum(linked(a, b) for a in ps[i][1] for b in ps[j][1])
            if n and (best is None or n > best[0]): best = (n, i, j)
    if not best: continue
    _, i, j = best
    def pick(mine, other):
        cs = [c for c in mine if lean.get(c, 0) >= MIN_LEAN]
        return max(cs, key=lambda c: (sum(linked(c, o) for o in other), lean[c])) if cs else None
    a, b = pick(ps[i][1], ps[j][1]), pick(ps[j][1], ps[i][1])
    if a and b and a != b: halves[k] = ((ps[i][0], a), (ps[j][0], b))

pairs = [(x, y) for x in range(N) for y in range(x + 1, N)]
def kernels(state):
    ks = [[] for _ in range(N)]
    for (x, y), (k, flip) in zip(pairs, state):
        h = halves[k]
        ks[x].append((k, h[flip])); ks[y].append((k, h[1 - flip]))
    return ks
def score(state):
    if len({k for k, _ in state}) < len(state): return -1e9
    ks = kernels(state)
    seen, s = {}, 0.0
    for f, kk in enumerate(ks):
        cs = [c for _, (_, c) in kk]
        if len(set(cs)) < len(cs): s -= 50
        for c in set(cs):
            if c in seen: s -= 50
            seen[c] = f
        s += sum(linked(a, b) for i, a in enumerate(cs) for b in cs[i + 1:])
    for k, _ in state:
        a, b = halves[k][0][1], halves[k][1][1]
        s += 2 if linked(a, b) else 0
    return s
rng = random.Random(7)
keys = sorted(halves)
best_state, best_s = None, -1e18
for start in range(40):
    state = [(k, rng.randrange(2)) for k in rng.sample(keys, len(pairs))]
    s = score(state)
    for _ in range(4000):
        t = list(state); q = rng.randrange(len(t))
        t[q] = (rng.choice(keys), rng.randrange(2)) if rng.random() < 0.7 else (t[q][0], 1 - t[q][1])
        ts = score(t)
        if ts >= s: state, s = t, ts
    if s > best_s: best_state, best_s = state, s

games = sorted({d['game'] for d in decks})
game_n = {g: sum(d['game'] == g for d in decks) for g in games}
game_lean = {g: {} for g in games}
for d in decks:
    for c in d['z']: game_lean[d['game']][c] = game_lean[d['game']].get(c, 0) + 1
def fill(kernel):
    """make_faction.py's rule on the decks that lean on any of the kernels"""
    ns = [n for n, d in enumerate(decks) if any(c in d['z'] for c in kernel)]
    by_game = {}
    for n in ns: by_game.setdefault(decks[n]['game'], []).append(n)
    use = {g: v for g, v in by_game.items() if len(v) >= MIN_DECKS} or by_game
    found = []
    for c in D['nodes']:
        if c in UNIT or c in kernel: continue
        shares, lifts = [], []
        for g, v in use.items():
            s = sum(c in decks[n]['z'] for n in v) / len(v); base = game_lean[g].get(c, 0) / game_n[g]
            shares.append(s)
            if base: lifts.append(s / base)
        share, lift = sum(shares) / len(shares), (sum(lifts) / len(lifts) if lifts else 0)
        if share >= SHARE and lift >= LIFT: found.append((share, c))
    return list(kernel) + [c for _, c in sorted(found, reverse=True)][:OWN - len(kernel)], len(ns)

ks = kernels(best_state)
fac = []
for f in range(N):
    kernel = list(dict.fromkeys(c for _, (_, c) in ks[f]))
    cs, nd = fill(kernel)
    eng = [c for c in cs if any(linked(c, o) for o in cs)]
    fac.append({'kernel': kernel, 'concepts': cs, 'decks': nd, 'engines': eng, 'halves': ks[f]})
L = 'ABCDEFGHIJKLMNOPQRST'
out = ['# Factions from halves of the deck archetypes (an experiment; made by kernel_factions.py)', '',
       f'{N} factions; each pair of factions shares one deck archetype, one half in each. Kernels: the concept of each half.',
       'Engines have a strong card link with another of the faction\'s concepts; bricks have none.', '']
for f, x in enumerate(fac):
    out.append(f"## Faction {L[f]} ({x['decks']} decks lean on its kernels)")
    out.append('- Halves: ' + '; '.join(f"{parts[k][0]}: {p} ({plain[c]})" for k, (p, c) in x['halves']))
    out.append('- Engines: ' + '; '.join(plain[c] + (' (kernel)' if c in x['kernel'] else '') for c in x['engines']))
    out.append('- Bricks: ' + ('; '.join(plain[c] + (' (kernel)' if c in x['kernel'] else '') for c in x['concepts'] if c not in x['engines']) or 'none'))
    out.append('')
out.append('## Pairs')
for (x, y), (k, _) in zip(pairs, best_state):
    a, b = fac[x]['concepts'], fac[y]['concepts']
    shared = [c for c in a if c in b]
    links = sorted({frozenset((p, q)) for p in a for q in b if linked(p, q) and p not in b and q not in a}, key=lambda s: -strong[s][0])
    both = [parts[d][0] for d, h in halves.items() if any(h[0][1] == c for c in a) and any(h[1][1] == c for c in b)
            or any(h[1][1] == c for c in a) and any(h[0][1] == c for c in b)]
    ex = links[0] if links else None
    out.append(f"- {L[x]}+{L[y]}: shares {len(shared)} of {min(len(a), len(b))} concepts" + (' (over half)' if len(shared) * 2 > min(len(a), len(b)) else '') +
               f"; {len(links)} strong card links between their own concepts" +
               (f" (strongest: {' + '.join(plain[c] for c in ex)}, \"{strong[ex][1]}\")" if ex else '') +
               f"; deck archetypes they can play: {', '.join(sorted(set(both)))} (planned: {parts[k][0]})")
text = '\n'.join(out) + '\n'
open(os.path.join(HERE, 'kernel_factions.md'), 'w', encoding='utf-8').write(text)
print(text)
