"""Step 4 (START_DESIGN-1-wheel.md): the usable concepts. Run from library/cards_db.
Every library concept with 10+ real cards (all games together): its cards, the games it is in, and the share of its cards
on each radius (worked out in each game alone, then averaged over the games that have it); a parent in the concept tree
keeps only the cards none of its children carry. Left out, each with its reason:
the concepts in concept_verdicts.tsv (Claude's); player_<concept> (no player health, Kaptain); a parent left with under 10
cards (its children carry its cards, so no effect counts twice).
python3 ../../factions/wheel/work/concept_catch.py -> factions/wheel/work/concepts.tsv (usable first, then the left out)."""
import collections, csv, os, sqlite3, sys
sys.path.insert(0, os.getcwd())
import axes, faction_asks

HERE = os.path.dirname(os.path.abspath(__file__))
c = sqlite3.connect('cards.sqlite')
games = sorted({g for (g,) in c.execute('select distinct game from card')})
con, pools, _ = axes.tag(c, faction_asks.Ctx(c, games, None, {}), games)
real = {i: g for i, g in c.execute('select id, game from card where coalesce(is_keyword,0)=0 and coalesce(is_stub,0)=0')}
RADII = [s for s in axes.SPOKES if s[0] not in axes.NUMERIC]  # strength and defence come from unit stats, not concepts

cards = collections.defaultdict(list)  # concept -> its real cards
for i, g in real.items():
    for k in con[i]:
        if not k.endswith('*'): cards[k].append(i)
cards = {k: v for k, v in cards.items() if len(v) >= 10}

kids = collections.defaultdict(set)  # concept -> the concepts under it in the tree, at any depth
for line in open('../concept_tree.txt', encoding='utf-8'):
    p = [t.strip() for t in line.split('|')]
    if len(p) > 3 and not line.startswith('#'):
        for par in filter(None, p[3].split(',')): kids[par.strip()].add(p[0])
def below(k, seen=None):
    seen = set() if seen is None else seen
    for x in kids[k] - seen: seen.add(x); below(x, seen)
    return seen

verdict = {r['concept']: r[list(r)[1]] for r in csv.DictReader(open(os.path.join(HERE, 'concept_verdicts.tsv')), delimiter='\t')}
def reason(k):
    if k in verdict: return verdict[k]
    if k.startswith('player_'): return 'not in this game (player health)'
    if len(cards[k]) < 10: return 'a parent: its children carry its cards'
    return ''

for k in list(cards):  # a parent keeps only the cards none of its children carry
    sub = below(k)
    if sub: cards[k] = [i for i in cards[k] if not con[i] & sub]

def shares(k):
    per = collections.defaultdict(list)
    for i in cards[k]: per[real[i]].append(i)
    return {s[0]: sum(sum(axes.counts(con[i], g, s[4]) for i in ids) / len(ids) for g, ids in per.items()) / max(1, len(per)) for s in RADII}, sorted(per)

rows = []
for k in cards:
    sh, gs = shares(k)
    rows.append((reason(k), k, len(cards[k]), ','.join(gs), sh))
rows.sort(key=lambda r: (r[0] != '', r[0], r[1]))
with open(os.path.join(HERE, 'concepts.tsv'), 'w', encoding='utf-8') as o:
    o.write('\t'.join(['concept', 'cards', 'games', 'left out because'] + [s[0] for s in RADII]) + '\n')
    for why, k, n, gs, sh in rows:
        o.write('\t'.join([k, str(n), gs, why] + [f'{sh[s[0]]:.2f}' for s in RADII]) + '\n')
print(sum(1 for r in rows if not r[0]), 'usable,', sum(1 for r in rows if r[0]), 'left out;',
      'verdicts for concepts under 10 cards:', ', '.join(sorted(set(verdict) - set(cards))) or 'none')
