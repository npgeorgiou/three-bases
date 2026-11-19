"""Experiment (not agreed): factions whose kernel is what the faction DOES (Kaptain, 19 Nov 2026), in plain words.
python3 factions/wheel/work/kernel_factions.py  (from the repo, a few seconds) -> factions/wheel/work/kernel_factions.md
1. Each identity (IDENTITIES, Claude's) names families or concepts of library/concept_tree.txt; its kernel is their usable
   concepts (work/concepts.tsv) that are effects, never a trigger, a condition or a drawback (but for Eats its own), that MIN_LEAN+ decks lean on, the KERNEL
   most leaned on. A concept goes to the first identity that names it.
2. Filled out from its decks (make_faction.py's rule: the decks that lean on a kernel concept; the concepts they lean on
   LIFT times as often as their games' decks and by SHARE of them), up to OWN concepts, kernel first, no other faction's
   kernel concept.
3. Card links split them: an engine has a strong card link (step 4) with another of the faction's concepts; a brick none.
4. The answers (work/answer_concepts.tsv): per question the ways its concepts give ('+' all needed, '|' any one).
5. Per pair: concepts shared, strong card links between their own concepts, and the deck archetypes of
   factions/wheel/deck_archetypes.tsv they can play together (each covers a part the other lacks, and together every
   engine part). A partner: 1+ deck archetype and PARTNER_LINKS+ links (Claude's)."""
import csv, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, HERE)
import step3_groups
OWN, KERNEL, MIN_LEAN, LIFT, SHARE, MIN_DECKS, PARTNER_LINKS = 12, 6, 10, 3.0, 0.08, 3, 5  # Claude's
OFF = ('combo', 'control_combo', 'extra_turns')
IDENTITIES = [  # (name, what it does, families or concepts of the concept tree); Claude's
    ("Can't be broken", 'its units do not die', ['protection', 'heal', 'defence_gain']),
    ('Kills brutally', 'removes enemy units, many and hard', ['removal', 'damage']),
    ('Messes you up', "breaks the enemy's units and plans", ['disruption', 'suppress', 'debuff', 'steal']),
    ('Moves', 'wins by where its units and his stand', ['positional']),
    ('Thrives on spells', 'spells that get stronger, cheaper and more of them', ['spell_power', 'card_advantage', 'cost_reduction', 'cost_set']),
    ('Waits', 'gets bigger every round, then plays huge cards', ['base_resource_gain', 'resource_gain', 'high_cost', 'countdown']),
    ('Swarms', 'fills the board with many units', ['summon', 'copy', 'free_play']),
    ('Grows', 'its units get bigger and bigger', ['buff', 'in_hand_buff']),
    ('Comes back', 'what it loses returns', ['revive', 'return_to_hand', 'recycle']),
    ('Eats its own', 'kills and spends its own units and cards for power', ['sacrifice', 'friendly_fire', 'self_destruct', 'discard']),
]
D = json.load(open(step3_groups.FILE, encoding='utf-8'))
plain, decks, UNIT = D['plain'], D['decks'], set(D['unit'])
tree, facet = {}, {}
for line in open(os.path.join(ROOT, 'library/concept_tree.txt'), encoding='utf-8'):
    if line.startswith('#') or '|' not in line: continue
    p = [x.strip() for x in line.split('|')]
    tree[p[0]] = [q for q in p[3].split(',') if q]; facet[p[0]] = p[2]
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
strong = {}
for r in csv.DictReader(open(os.path.join(ROOT, 'library/cards_db/wheel/concept_links.tsv'), encoding='utf-8'), delimiter='\t'):
    cards, rare, level = float(r['cards'] or 0), float(r['rare'] or 0), float(r['level'] or 0)
    if cards >= 1.2 or (rare >= 3 and level >= 1): strong[frozenset((r['a'], r['b']))] = (cards, r['texts'].split(' | ')[0])
def linked(a, b): return a != b and frozenset((a, b)) in strong

games = sorted({d['game'] for d in decks})
game_n = {g: sum(d['game'] == g for d in decks) for g in games}
game_lean = {g: {} for g in games}
for d in decks:
    for c in d['z']: game_lean[d['game']][c] = game_lean[d['game']].get(c, 0) + 1
def fill(kernel, barred):
    ns = [n for n, d in enumerate(decks) if any(c in d['z'] for c in kernel)]
    by_game = {}
    for n in ns: by_game.setdefault(decks[n]['game'], []).append(n)
    use = {g: v for g, v in by_game.items() if len(v) >= MIN_DECKS} or by_game
    found = []
    for c in D['nodes']:
        if c in UNIT or c in kernel or c in barred: continue
        shares, lifts = [], []
        for g, v in use.items():
            s = sum(c in decks[n]['z'] for n in v) / len(v); base = game_lean[g].get(c, 0) / game_n[g]
            shares.append(s)
            if base: lifts.append(s / base)
        share, lift = sum(shares) / len(shares), (sum(lifts) / len(lifts) if lifts else 0)
        if share >= SHARE and lift >= LIFT: found.append((share, c))
    return [c for _, c in sorted(found, reverse=True)][:OWN - len(kernel)], len(ns)

taken, fac = set(), []
for name, does, fams in IDENTITIES:
    cs = set().union(*(under(f) for f in fams)) & usable
    own_cost = name == 'Eats its own'  # only this identity takes drawbacks (losses on my own side)
    cs = [c for c in cs if facet.get(c) not in ('trigger', 'condition') and lean.get(c, 0) >= MIN_LEAN and c not in taken
          and (own_cost or c not in drawbacks)]
    kernel = sorted(cs, key=lambda c: -lean[c])[:KERNEL]
    taken |= set(kernel)
    fac.append({'name': name, 'does': does, 'kernel': kernel})
all_kernel = set(taken)
for x in fac:
    extra, x['decks'] = fill(x['kernel'], all_kernel - set(x['kernel']))
    x['concepts'] = x['kernel'] + extra
    x['engines'] = [c for c in x['concepts'] if any(linked(c, o) for o in x['concepts'])]

ways = {}
for r in csv.DictReader(open(os.path.join(HERE, 'answer_concepts.tsv'), encoding='utf-8'), delimiter='\t'):
    if r['answer'] in ('blind',): continue
    need = [[a.split(' ')[0] for a in part.split('|')] for part in r['concepts'].split('+')]
    ways.setdefault(r['answer'], []).append((r['way'], need))
QUESTION = {'front': 'removes the front unit', 'backrow': 'mainly removes back-row units', 'lanes': 'mainly acts between lanes',
            'holds': 'holds a base', 'cares': 'the game thing it cares about'}
def answers(cs):
    s = set(cs)
    return {q: [w for w, need in ws if all(any(a in s for a in alt) for alt in need)] for q, ws in ways.items() if q in QUESTION}

parts = {}
for r in csv.DictReader(open(os.path.join(HERE, '..', 'deck_archetypes.tsv'), encoding='utf-8'), delimiter='\t'):
    if r['key'] in OFF or r['kind'] != 'engine': continue
    parts.setdefault(r['key'], (r['name'], []))[1].append(set(c for c in r['concepts'].split(',') if c))
def playable(a, b):
    sa, sb, out = set(a), set(b), []
    for k, (name, ps) in parts.items():
        if len(ps) < 2: continue
        ca, cb = [bool(p & sa) for p in ps], [bool(p & sb) for p in ps]
        if all(x or y for x, y in zip(ca, cb)) and any(x and not y for x, y in zip(ca, cb)) and any(y and not x for x, y in zip(ca, cb)):
            out.append(name)
    return out

out = ['# Ten factions from what they do (an experiment; made by kernel_factions.py)', '',
       'Kernel: the concepts that do what the faction does (concept tree families; effects only, never a trigger or a condition, '
       f'{MIN_LEAN}+ decks leaning, the {KERNEL} most leaned on). The rest come from its decks. Engines link to another of its concepts '
       'by real cards; bricks link to none. Answers: the ways its concepts already give; extras fill the rest later.', '']
partners = {i: [] for i in range(len(fac))}
pair_lines = []
for i in range(len(fac)):
    for j in range(i + 1, len(fac)):
        a, b = fac[i]['concepts'], fac[j]['concepts']
        shared = [c for c in a if c in b]
        links = sorted({frozenset((p, q)) for p in a for q in b if linked(p, q) and p not in b and q not in a}, key=lambda s: -strong[s][0])
        dk = playable(a, b)
        if dk and len(links) >= PARTNER_LINKS: partners[i].append(j); partners[j].append(i)
        ex = links[0] if links else None
        pair_lines.append(f"- {fac[i]['name']} + {fac[j]['name']}: {len(links)} card links" +
                          (f" (strongest {plain[list(ex)[0]]} + {plain[list(ex)[1]]}: \"{strong[ex][1]}\")" if ex else '') +
                          f"; deck archetypes: {', '.join(dk) or 'none'}" + (f"; shares {len(shared)}" if shared else ''))
for i, x in enumerate(fac):
    out.append(f"## {x['name']}: {x['does']} ({x['decks']} decks lean on its kernel)")
    out.append('- Kernel: ' + '; '.join(f'{plain[c]} ({lean[c]} decks)' for c in x['kernel']))
    out.append('- From its decks: ' + ('; '.join(plain[c] for c in x['concepts'] if c not in x['kernel']) or 'nothing'))
    out.append('- Engines: ' + ('; '.join(plain[c] for c in x['engines']) or 'none') + '. Bricks: ' +
               ('; '.join(plain[c] for c in x['concepts'] if c not in x['engines']) or 'none'))
    for q, ws in answers(x['concepts']).items():
        out.append(f'- {QUESTION[q]}: ' + ('; '.join(ws) if ws else '**missing**'))
    out.append(f"- Partners ({len(partners[i])}): " + (', '.join(fac[j]['name'] for j in partners[i]) or 'none'))
    out.append('')
out.append('## Pairs')
out += pair_lines
text = '\n'.join(out) + '\n'
open(os.path.join(HERE, 'kernel_factions.md'), 'w', encoding='utf-8').write(text)
print(text)
