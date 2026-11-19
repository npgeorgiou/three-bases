"""A faction from one or two concepts, out of the NMF groups (deck_groups_nmf.json; run deck_groups_nmf.py first).
python3 factions/wheel/work/make_faction.py "attach" ["discard"]  -> prints the faction and writes it to
factions/wheel/work/made/<concepts>.md. A concept is named by its key or by words of its plain name.
1. Each named concept: the decks that lean on it (score above the strong mark); its group is the one those decks mix in
   most. With one concept, the second group is the one those decks mix in most after it, lowered by the share of
   concepts it shares with the first (Claude's); with two, each concept brings its own group.
2. How often real decks mix the two groups: the decks with 30% or more of each in their mix.
3. Cards out of 100: for each concept of the two groups and their base concepts, the share of cards that have it in the
   decks of either group, times 100 (a card has about 3 concepts, so the numbers add up to more than 100).
4. The real decks with the most of both groups, and the real factions that fit them best."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'deck_groups_nmf.json'), encoding='utf-8'))
plain, groups, decks = D['plain'], {g['key']: g for g in D['groups']}, D['decks']
CARRY = 0.30

def find(word):
    w = word.lower().strip()
    hits = [k for k in D['nodes'] if k.lower() == w] or [k for k in D['nodes'] if w in plain[k].lower() or w in k.lower()]
    if not hits: sys.exit(f'no concept matches "{word}"')
    return hits[0], hits[1:]

def leaning(k): return [n for n, d in enumerate(decks) if k in d['z']]
def avg_mix(ns):
    out = {}
    for n in ns:
        for g, v in decks[n]['mix'].items(): out[g] = out.get(g, 0) + v / len(ns)
    return out

out, names = [], []
picked = []
for word in sys.argv[1:3]:
    k, other = find(word)
    names.append(k)
    ns = leaning(k)
    out.append(f'**{plain[k]}** (`{k}`): {len(ns)} decks lean on it' + (f'; other matches: {", ".join(plain[o] for o in other[:4])}' if other else ''))
    if not ns: sys.exit('\n'.join(out + ['No deck leans on it, so it belongs to no group.']))
    m = avg_mix(ns)
    first = max(m, key=m.get)
    picked.append((k, first, m))
if len(picked) == 1:
    k, a, m = picked[0]
    ca = set(groups[a]['concepts'])
    score = {g: v * (1 - len(ca & set(groups[g]['concepts'])) / len(ca)) for g, v in m.items() if g != a}
    b = max(score, key=score.get) if score else None
else:
    a, b = picked[0][1], picked[1][1]
    if a == b:
        out.append(f'Both concepts are in the same group, {a}; the second group is the one their decks mix in most after it.')
        m = picked[0][2]; ca = set(groups[a]['concepts'])
        score = {g: v * (1 - len(ca & set(groups[g]['concepts'])) / len(ca)) for g, v in m.items() if g != a}
        b = max(score, key=score.get)
both = [n for n, d in enumerate(decks) if d['mix'].get(a, 0) >= CARRY and d['mix'].get(b, 0) >= CARRY]
either = sorted(set(groups[a]['decks']) | set(groups[b]['decks']))
out.append(f'\nArchetypes: **{a}** and **{b}**. Real decks that mix both (30% or more of each): {len(both)}' +
           (' — **no real deck plays this pair**' if not both else ''))
for g in (a, b):
    gr = groups[g]
    out.append(f"\n## {g}" + (' (one game)' if gr['one_game'] else '') + f": {len(gr['decks'])} decks")
    out.append('- Concepts: ' + '; '.join(f"{plain[c]} {gr['lean'][c]:.0%}" for c in gr['concepts']))
    out.append('- Base concepts: ' + ('; '.join(f'{plain[c]} {v:.0%}' for c, v in gr['base'][:8]) or 'none'))
concepts = []
for g in (a, b):
    for c in groups[g]['concepts'] + [c for c, _ in groups[g]['base']]:
        if c not in concepts: concepts.append(c)
for k in names:
    if k not in concepts: concepts.insert(0, k)
cards = {c: 100 * sum(decks[n]['counts'].get(c, 0) / decks[n]['size'] for n in either) / len(either) for c in concepts}
out.append('\n## Cards out of 100 (share of cards with each concept in the decks of either group)')
out.append('; '.join(f'{plain[c]} {cards[c]:.0f}' for c in sorted(concepts, key=lambda c: -cards[c])))
near = sorted(range(len(decks)), key=lambda n: -(min(decks[n]['mix'].get(a, 0), decks[n]['mix'].get(b, 0)) * 2 +
                                                 decks[n]['mix'].get(a, 0) + decks[n]['mix'].get(b, 0)))[:6]
out.append('\n## Closest real decks')
out.append('; '.join(f"{decks[n]['name']} ({decks[n]['game']}, {decks[n]['mix'].get(a, 0):.0%} {a}, {decks[n]['mix'].get(b, 0):.0%} {b})" for n in near))
facs = sorted(D['factions'], key=lambda f: -(f['fit'][a] + f['fit'][b]))[:5]
out.append('\n## Closest real factions (share of the group\'s concepts against their game\'s average)')
out.append('; '.join(f"{f['faction']} ({f['game']}, x{f['fit'][a]:.1f} {a}, x{f['fit'][b]:.1f} {b})" for f in facs))
text = '\n'.join(out)
os.makedirs(os.path.join(HERE, 'made'), exist_ok=True)
path = os.path.join(HERE, 'made', re.sub(r'[^a-z0-9]+', '_', '_'.join(names).lower()).strip('_') + '.md')
open(path, 'w', encoding='utf-8').write(f"# A faction from {', '.join(plain[k] for k in names)} (made by make_faction.py)\n\n" + text + '\n')
print(text)
print('\nwritten to', os.path.relpath(path, os.path.join(HERE, '..', '..', '..')))
