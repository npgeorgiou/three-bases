"""Step 2 (START_DESIGN-1-roster.md): the usable concepts. Run from library/cards_db.
Every library concept with 5+ real cards (all games together): its cards and the games it is in; a parent in the concept tree
keeps only the cards none of its children carry. Each gets a kind with its reason: usable (a faction can build on it),
helper or out, from concept_verdicts.tsv (a concept not in it is usable); player_<concept> is out (no player health,
Kaptain), and so is a parent left with under 5 cards (its children carry its cards, so no effect counts twice).
python3 ../../factions/roster/work/concept_catch.py -> factions/roster/work/concepts.tsv (usable, then helpers, then out) and
concepts.md (the same by kind in plain words: the concept tree's name, cards, games; for Kaptain)."""
import collections, csv, os, sqlite3, sys, textwrap
sys.path.insert(0, os.getcwd())
import concept_tags, faction_asks

HERE = os.path.dirname(os.path.abspath(__file__))
c = sqlite3.connect('cards.sqlite')
games = sorted({g for (g,) in c.execute('select distinct game from card')})
con, pools, _ = concept_tags.tag(c, faction_asks.Ctx(c, games, None, {}), games)
real = {i: g for i, g in c.execute('select id, game from card where coalesce(is_keyword,0)=0 and coalesce(is_stub,0)=0')}

cards = collections.defaultdict(list)  # concept -> its real cards
for i, g in real.items():
    for k in con[i]:
        if not k.endswith('*'): cards[k].append(i)  # the unit numbers of concept_tags.py are no concepts
cards = {k: v for k, v in cards.items() if len(v) >= 5}

kids = collections.defaultdict(set)  # concept -> the concepts under it in the tree, at any depth
for line in open('../concept_tree.txt', encoding='utf-8'):
    p = [t.strip() for t in line.split('|')]
    if len(p) > 3 and not line.startswith('#'):
        for par in filter(None, p[3].split(',')): kids[par.strip()].add(p[0])
def below(k, seen=None):
    seen = set() if seen is None else seen
    for x in kids[k] - seen: seen.add(x); below(x, seen)
    return seen

verdict = {r['concept']: (r['kind'], r[list(r)[2]]) for r in csv.DictReader(open(os.path.join(HERE, 'concept_verdicts.tsv')), delimiter='\t')}
def reason(k):
    if k in verdict: return verdict[k]
    if k.startswith('player_'): return 'out', 'not in this game: player health (Kaptain)'
    if len(cards[k]) < 5: return 'out', 'a parent: its children carry its cards'
    return 'usable', ''

for k in list(cards):  # a parent keeps only the cards none of its children carry
    sub = below(k)
    if sub: cards[k] = [i for i in cards[k] if not con[i] & sub]

rows = []
for k in cards:
    rows.append((reason(k), k, len(cards[k]), ','.join(sorted({real[i] for i in cards[k]}))))
KINDS = ['usable', 'helper', 'out']
rows.sort(key=lambda r: (KINDS.index(r[0][0]), r[0][1], r[1]))
with open(os.path.join(HERE, 'concepts.tsv'), 'w', encoding='utf-8') as o:
    o.write('\t'.join(['concept', 'card_count', 'games', 'kind', 'reason']) + '\n')
    for (kind, why), k, n, gs in rows:
        o.write('\t'.join([k, str(n), gs, kind, why]) + '\n')
print(', '.join(f'{sum(1 for r in rows if r[0][0] == t)} {t}' for t in KINDS) + ';',
      'verdicts for concepts under 5 cards:', ', '.join(sorted(set(verdict) - set(cards))) or 'none')

plain = {}
for line in open('../concept_tree.txt', encoding='utf-8'):
    p = [t.strip() for t in line.split('|')]
    if len(p) > 1 and not line.startswith('#'): plain[p[0]] = p[1]
with open(os.path.join(HERE, 'concepts.md'), 'w', encoding='utf-8') as o:
    o.write('# Step 2: the concepts by kind (made by concept_catch.py; cards, in how many of 10 games)\n')
    for t in KINDS:
        rs = [r for r in rows if r[0][0] == t]
        o.write(f'\n## {t} ({len(rs)})\n')
        for why in sorted({r[0][1] for r in rs}, key=lambda w: [r[0][1] for r in rs].index(w)):
            items = '; '.join(f"{plain.get(k, k)} ({n}, {len(gs.split(','))})" for (_, w), k, n, gs in rs if w == why)
            o.write('\n'.join(textwrap.wrap((why + ': ' if why else '') + items, 118)) + '\n')
