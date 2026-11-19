"""Experiment (process agreed 20 Nov 2026): whole factions from what they do.
python3 factions/wheel/work/kernel_factions.py  (from the repo, a few seconds) -> factions/wheel/work/kernel_factions.md
1. Identity: what the faction DOES, in plain words (IDENTITIES, Claude's), made of families of library/concept_tree.txt.
   Its kernel: their usable concepts that are effects (never a trigger, a condition, or a drawback but for Eats its own)
   and that MIN_LEAN+ decks lean on, at most KERNEL. A concept two identities want goes to the one whose other kernel
   concepts' decks hold it more. A kernel under MIN_KERNEL concepts is marked thin: Kaptain widens it.
2. Engines come from card links: the usable concepts (triggers and conditions too) with a strong card link (step 4) to 2+ kernel
   concepts, at most ENGINES, ranked by its kernel links times the share of its links that go to this kernel (so a
   concept real cards link to everything does not join every faction, nor a rare one with two links). Bricks come from decks: the concepts the kernel's decks hold more
   often than their game's cards (share of cards against the game's share, per game with MIN_DECKS+ of its decks,
   averaged; DECK_LIFT+), held by HELD+ of those decks, that no strong card link joins to the kernel (another faction's kernel concepts too: support), the most first,
   until OWN concepts. A brick more than MAX_BRICK factions would take is dropped from all (too common to tell them
   apart), and the rest refilled. Each engine shows the real card pair behind its strongest link to the kernel.
   A concept is an engine when real cards link it to another of the faction's concepts, else a brick.
3. A faction needs an engine pair (two of its concepts real cards link); one with none is marked.
4. Different enough: two factions share at most half of their concepts.
5. Partners (PARTNERS each, Kaptain): a faction's strongest pairs. A pair's strength: the strong card links between their
   own concepts, plus 3 for each of one's kernel concepts the other's decks hold DECK_LIFT times as often as their games
   (Claude's). Each partner gets a line on how it plays: its strongest card link, or what its decks hold.
6. The answers (work/answer_concepts.tsv): per question the ways its concepts give, and what is missing."""
import collections, csv, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, HERE)
import step3_groups
OWN, KERNEL, MIN_KERNEL, MIN_LEAN, ENGINES, MIN_DECKS = 12, 6, 4, 10, 4, 3  # Claude's
DECK_LIFT, HELD, MAX_BRICK, PARTNERS = 1.5, 0.25, 3, 5                              # Claude's; 5 partners: Kaptain
IDENTITIES = [  # (name, what it does, families or concepts of the concept tree); Claude's
    ("Can't be broken", 'its units do not die', ['protection', 'heal', 'defence_gain']),
    ('Kills brutally', 'removes enemy units, many and hard', ['removal', 'damage']),
    ('Messes you up', "breaks the enemy's units and plans", ['disruption', 'suppress', 'debuff', 'steal']),
    ('Moves', 'wins by where its units and his stand', ['positional']),
    ('Thrives on spells', 'spells that get stronger, cheaper and more of them', ['spell_power', 'card_advantage', 'cost_reduction', 'cost_set']),
    ('Waits', 'gets bigger every round, then plays huge cards', ['base_resource_gain', 'resource_gain', 'high_cost']),
    ('Swarms', 'fills the board with many units', ['summon', 'copy', 'free_play']),
    ('Grows', 'its units get bigger and bigger', ['buff', 'in_hand_buff']),
    ('Comes back', 'what it loses returns', ['revive', 'return_to_hand', 'recycle']),
    ('Eats its own', 'kills and spends its own units and cards for power', ['sacrifice', 'friendly_fire', 'self_destruct', 'discard']),
]
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
strong = {}
for r in csv.DictReader(open(os.path.join(ROOT, 'library/cards_db/wheel/concept_links.tsv'), encoding='utf-8'), delimiter='\t'):
    cards, rare, level = float(r['cards'] or 0), float(r['rare'] or 0), float(r['level'] or 0)
    if cards >= 1.2 or (rare >= 3 and level >= 1): strong[frozenset((r['a'], r['b']))] = (cards, r['texts'].split(' | ')[0])
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
kernels = set().union(*(set(x['kernel']) for x in fac))
for x in fac:
    k = x['kernel']
    eng = [c for c in usable if c not in kernels and sum(linked(c, q) for q in k) >= 2]
    eng = sorted(eng, key=lambda c: (-sum(linked(c, q) for q in k) ** 2 / reach[c], c))[:ENGINES]
    x['decks'] = decks_of(k)
    lift = deck_lift(x['decks']); x['lift'] = lift
    held = {c: sum(decks[n]['counts'].get(c, 0) > 0 for n in x['decks']) / max(1, len(x['decks'])) for c in lift}
    x['brick_pool'] = [c for c in sorted(lift, key=lambda c: (-lift[c], c)) if lift[c] >= DECK_LIFT and held[c] >= HELD and c not in k
                       and c not in eng and c in usable and not any(linked(c, q) for q in k)]
    x['from_links'] = eng
common = set()
while True:  # a brick 4+ factions would take is too common to tell them apart: dropped from all, the rest refilled
    for x in fac:
        x['from_decks'] = [c for c in x['brick_pool'] if c not in common][:max(0, OWN - len(x['kernel']) - len(x['from_links']))]
    count = collections.Counter(c for x in fac for c in x['from_decks'])
    more = {c for c, n in count.items() if n > MAX_BRICK}
    if not more: break
    common |= more
for x in fac:
    x['concepts'] = x['kernel'] + x['from_links'] + x['from_decks']
    x['engines'] = [c for c in x['concepts'] if any(linked(c, o) for o in x['concepts'])]

sys.path.insert(0, os.path.join(ROOT, 'library', 'cards_db'))
here = os.getcwd(); os.chdir(os.path.join(ROOT, 'library', 'cards_db'))
import archetype_map
wanted = {frozenset((c, q)) for x in fac for c in x['from_links'] for q in x['kernel'] if linked(c, q)}
pair_of = archetype_map.card_pairs(wanted)[0]
os.chdir(here)
def behind(c, k):
    """the real card pair behind c's strongest link to the kernel k"""
    q = max((q for q in k if linked(c, q)), key=lambda q: strong[frozenset((c, q))][0])
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

out = ['# Ten whole factions from what they do (an experiment; made by kernel_factions.py)', '',
       'Kernel: the effects that do what the faction does. Engines: concepts real cards link to 2+ kernel concepts. Bricks: '
       f'what its decks hold {DECK_LIFT:g}x+ as often as their games, with no card link to the kernel. About {OWN} concepts. '
       f"Partners: its {PARTNERS} strongest pairs (card links between their concepts, plus 3 per kernel concept the other's decks hold "
       f'{DECK_LIFT:g}x+). Bricks taken by more than {MAX_BRICK} factions are dropped from all: '
       + (', '.join(plain[c] for c in sorted(common)) or 'none') + '.', '']
partners = {i: sorted((j for j in range(len(fac)) if j != i), key=lambda j: -strengths[(i, j)][0])[:PARTNERS] for i in range(len(fac))}
for i, x in enumerate(fac):
    out.append(f"## {x['name']}: {x['does']} ({len(x['decks'])} decks lean on its kernel)")
    if x['thin']: out.append(f"- **Thin kernel: under {MIN_KERNEL} concepts. Kaptain widens it.**")
    out.append('- Kernel: ' + '; '.join(f'{plain[c]} ({lean[c]} decks)' for c in x['kernel']))
    out.append('- From card links:' + ('' if x['from_links'] else ' nothing'))
    for c in x['from_links']:
        q, pair = behind(c, x['kernel'])
        out.append(f"  - {plain[c]} ({sum(linked(c, o) for o in x['kernel'])} kernel links; strongest with {q}: {pair})")
    out.append('- From decks: ' + ('; '.join(f"{plain.get(c, c)} x{x['lift'][c]:.1f}" for c in x['from_decks']) or 'nothing'))
    out.append(f"- {len(x['concepts'])} concepts. Engines: " + ('; '.join(plain.get(c, c) for c in x['engines']) or '**none: no engine pair**')
               + '. Bricks: ' + ('; '.join(plain.get(c, c) for c in x['concepts'] if c not in x['engines']) or 'none'))
    for q, ws in answers(x['concepts']).items():
        out.append(f'- {QUESTION[q]}: ' + ('; '.join(ws) if ws else '**missing**'))
    out.append(f'- Partners (its {PARTNERS} strongest; * = it is in their {PARTNERS} too):')
    for j in partners[i]:
        st, how = strengths[(i, j)]
        out.append(f"  - {fac[j]['name']}{' *' if i in partners[j] else ''} ({st}): {how}")
    out.append('')
out.append('## Every pair')
out += pairs
text = '\n'.join(out) + '\n'
open(os.path.join(HERE, 'kernel_factions.md'), 'w', encoding='utf-8').write(text)
print(text)
