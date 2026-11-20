"""A faction from one or two concepts, made from what real decks play, never from step 3's groups.
python3 factions/roster/work/make_faction.py "attach" ["discard"]  -> prints the faction and writes it to
factions/roster/work/made/<concepts>.md. A concept is named by its key or by words of its plain name. The decks and their
scores come from step 3's json (deck_scores.json).
1. Each named concept: the decks that lean on it (score above the strong mark).
2. Its two archetypes: with two concepts, the decks of each make one archetype; with one, its decks are split into the two
   ways they play it (NMF with 2 groups on those decks' scores, first guess from the data; each deck goes to the way it
   leans on most; Claude's).
3. An archetype's concepts: those its decks lean on at least LIFT times as often as all decks of their game, worked out
   per game and averaged (games with MIN_DECKS+ of its decks, each game the same), and by at least SHARE of its decks;
   the TOP most leaned on (Claude's). The named concept is always in.
4. Cards out of 100: for each concept of the two archetypes, the share of cards with it in the decks of either.
5. The real decks that lean on most concepts of both archetypes, and the real factions whose cards hold the archetypes'
   concepts most often against their game's average."""
import json, math, os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
LIFT, SHARE, MIN_DECKS, TOP = 3.0, 0.08, 3, 12  # Claude's
D = json.load(open(os.path.join(HERE, 'deck_scores.json'), encoding='utf-8'))
plain, decks, UNIT = D['plain'], D['decks'], set(D['unit'])
ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]

def find(word):
    w = word.lower().strip()
    hits = [k for k in D['nodes'] if k.lower() == w] or [k for k in D['nodes'] if w in plain[k].lower() or w in k.lower()]
    if not hits: sys.exit(f'no concept matches "{word}"')
    return hits[0], hits[1:]

def leaning(k): return [n for n, d in enumerate(decks) if k in d['z']]

games = sorted({d['game'] for d in decks})
game_lean = {g: {} for g in games}
for d in decks:
    for c in d['z']: game_lean[d['game']][c] = game_lean[d['game']].get(c, 0) + 1
game_n = {g: sum(d['game'] == g for d in decks) for g in games}

def archetype(ns, kernel):
    """concepts the decks ns lean on LIFT times as often as their games' decks, by SHARE of them"""
    by_game = {}
    for n in ns: by_game.setdefault(decks[n]['game'], []).append(n)
    use = {g: v for g, v in by_game.items() if len(v) >= MIN_DECKS} or by_game
    score = {}
    for c in D['nodes']:
        if c in UNIT: continue
        shares, lifts = [], []
        for g, v in use.items():
            s = sum(c in decks[n]['z'] for n in v) / len(v)
            base = game_lean[g].get(c, 0) / game_n[g]
            shares.append(s)
            if base: lifts.append(s / base)
        share = sum(shares) / len(shares)
        lift = sum(lifts) / len(lifts) if lifts else 0
        if c == kernel or (share >= SHARE and lift >= LIFT): score[c] = (share, lift)
    cs = sorted(score, key=lambda c: (c != kernel, -score[c][0]))[:TOP]
    return cs, score

def split(ns):
    """the decks ns in the two ways they play: NMF with 2 groups on their scores (first guess from the data)"""
    A = np.array([[decks[n]['z'].get(c, 0) for c in D['nodes']] for n in ns]) + 1e-6
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    W = np.abs(U[:, :2]) * np.sqrt(S[:2]) + 1e-3; H = np.abs(Vt[:2]) * np.sqrt(S[:2])[:, None] + 1e-3
    for _ in range(500):
        H *= (W.T @ A) / (W.T @ W @ H + 1e-9); W *= (A @ H.T) / (W @ H @ H.T + 1e-9)
    side = W.argmax(1)
    return [n for n, s in zip(ns, side) if s == 0], [n for n, s in zip(ns, side) if s == 1]

out, names, sides = [], [], []
for word in ARGS[:2]:
    k, other = find(word)
    ns = leaning(k)
    names.append(k)
    out.append(f'**{plain[k]}** (`{k}`): {len(ns)} decks lean on it' + (f'; other matches: {", ".join(plain[o] for o in other[:4])}' if other else ''))
    if len(ns) < 2 * MIN_DECKS: sys.exit('\n'.join(out + [f'Under {2 * MIN_DECKS} decks lean on it: too few to make an archetype.']))
    sides.append((k, ns))
if len(sides) == 1:
    k, ns = sides[0]
    a, b = split(ns)
    sides = [(k, a), (k, b)]
    out.append(f'Its decks play it in two ways: {len(a)} and {len(b)} decks.')
else:
    both = set(sides[0][1]) & set(sides[1][1])
    out.append(f'Real decks that lean on both: {len(both)}' + (' — **no real deck plays this pair**' if not both else ''))
arch = []
for i, (k, ns) in enumerate(sides, 1):
    cs, score = archetype(ns, k)
    arch.append(cs)
    gs = {}
    for n in ns: gs[decks[n]['game']] = gs.get(decks[n]['game'], 0) + 1
    out.append(f"\n## Archetype {i}: {len(ns)} decks ({', '.join(f'{g} {v}' for g, v in sorted(gs.items()))})")
    out.append('- Concepts (share of its decks that lean on each, times as often as their games\' decks): ' +
               '; '.join(f'{plain[c]} {score[c][0]:.0%} x{score[c][1]:.1f}' for c in cs))
shared = [c for c in arch[0] if c in arch[1]]
out.append('\nShared by both archetypes: ' + ('; '.join(plain[c] for c in shared) or 'none'))
concepts = list(dict.fromkeys(arch[0] + arch[1]))
either = sorted(set(sides[0][1]) | set(sides[1][1]))
cards = {c: 100 * sum(decks[n]['counts'].get(c, 0) / int(decks[n]['size']) for n in either) / len(either) for c in concepts}
out.append('\n## Cards out of 100 (share of cards with each concept in the decks of either archetype)')
out.append('; '.join(f'{plain[c]} {cards[c]:.0f}' for c in sorted(concepts, key=lambda c: -cards[c])))
def hold(n, cs): return sum(c in decks[n]['z'] for c in cs)
near = sorted(range(len(decks)), key=lambda n: -(2 * min(hold(n, arch[0]), hold(n, arch[1])) + hold(n, arch[0]) + hold(n, arch[1])))[:6]
out.append('\n## Closest real decks (concepts of archetype 1 and 2 they lean on)')
out.append('; '.join(f"{decks[n]['name']} ({decks[n]['game']}, {hold(n, arch[0])} and {hold(n, arch[1])})" for n in near))
def fit(f):
    tot, gt = sum(f['counts'].values()), sum(D['game_counts'][f['game']].values())
    s = sum(f['counts'].get(c, 0) for c in concepts) / tot if tot else 0
    g = sum(D['game_counts'][f['game']].get(c, 0) for c in concepts) / gt if gt else 0
    return s / g if g else 0
facs = sorted(D['factions'], key=lambda f: -fit(f))[:5]
out.append('\n## Closest real factions (share of their cards on these concepts against their game\'s average)')
out.append('; '.join(f"{f['faction']} ({f['game']}, x{fit(f):.1f})" for f in facs))
text = '\n'.join(out)
os.makedirs(os.path.join(HERE, 'made'), exist_ok=True)
path = os.path.join(HERE, 'made', re.sub(r'[^a-z0-9]+', '_', '_'.join(names).lower()).strip('_') + '.md')
open(path, 'w', encoding='utf-8').write(f"# A faction from {', '.join(plain[k] for k in names)} (made by make_faction.py)\n\n" + text + '\n')
print(text)
print('\nwritten to', os.path.relpath(path, os.path.join(HERE, '..', '..', '..')))
