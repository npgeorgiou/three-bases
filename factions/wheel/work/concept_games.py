"""concept_games.py (run from library/cards_db): step 1, does a concept mean the same in every game?
For each suspect concept (suspects.tsv) and each game: its real cards; where its rows act (kind, side, zone of the
target or the trigger); the concepts its cards link to (through what of each card made the link, axes.side_concepts),
as lift over what the game links anyway, and how alike that is to the other games together (cosine, 1 = the same partners). Writes concept_games.tsv;
--all: every concept with 10+ real cards, into concept_games_all.tsv."""
import collections, math, os, sqlite3, sys
sys.path.insert(0, os.getcwd())
import axes, faction_asks

HERE = os.path.dirname(os.path.abspath(__file__))
sus = [l.rstrip('\n').split('\t') for l in open(os.path.join(HERE, 'suspects.tsv'))][1:]
want = {r[0]: set(r[1].split(',')) for r in sus}
c = sqlite3.connect('cards.sqlite')
games = sorted({g for (g,) in c.execute('select distinct game from card')})
con, pools, stats = axes.tag(c, faction_asks.Ctx(c, games, None, {}), games)
real = {i: g for i, g in c.execute('select id, game from card where coalesce(is_keyword,0)=0 and coalesce(is_stub,0)=0')}

where = collections.defaultdict(collections.Counter)  # (concept, game) -> where its rows act
for t, cols in (('flat_do', "coalesce(on_kind,'-') || '/' || coalesce(on_side,'-') || '/' || coalesce(on_zone,'board')"),
                ('flat_when', "'when ' || coalesce(obj_kind,actor_kind,'-') || '/' || coalesce(obj_side,actor_side,'-')"),
                ('flat_if', "'if ' || coalesce(of_kind,'-') || '/' || coalesce(of_side,'-') || '/' || coalesce(of_zone,'-')")):
    for card, k, w in c.execute(f'select distinct card, concept, {cols} from {t} where concept in ({",".join("?" * len(want))})', list(want)):
        if card in real: where[(k, real[card])][w] += 1

ALL = '--all' in sys.argv  # every concept with 10+ real cards, not only the suspects
if ALL:
    n = collections.Counter(k for i in real for k in con[i])
    want = {k: set(games) for k, v in n.items() if v >= 10 and not k.endswith('*')}
kws = collections.defaultdict(collections.Counter)  # (concept, game) -> the keywords that give the concept
for card, k, kw in c.execute("select distinct ck.card, v.tree, k.name from card_keyword ck join card k on k.id=ck.keyword join vocab v on "
                             "v.field='keyword' and v.value=coalesce((select s.value from vocab s where s.field='keyword' and s.value=k.game || ':' || k.name), k.name) where v.tree!=''"):
    if card in real and k in want: kws[(k, real[card])][kw] += 1
partners = collections.defaultdict(collections.Counter)  # (concept, game) -> concepts on the other side of its links
base = collections.defaultdict(collections.Counter)  # game -> concepts on any side of its links (to divide out what the game links anyway)
for (a, b), srcs in axes.link_pairs().items():
    if a not in real or b not in real: continue
    g = real[a]
    for sa, sb in srcs:
        ka, kb = axes.side_concepts(a, sa, con), axes.side_concepts(b, sb, con)
        for mine, other in ((ka, kb), (kb, ka)):
            base[g].update(other)
            for k in mine & want.keys():
                for o in other - {k}: partners[(k, g)][o] += 1
for (k, g), p in partners.items():  # log lift: how much more than the game's usual share each partner concept has (only above it)
    t, bt = sum(p.values()), sum(base[g].values())
    partners[(k, g)] = collections.Counter({o: math.log((v / t) / (base[g][o] / bt)) for o, v in p.items() if v >= 2 and (v / t) > (base[g][o] / bt)})


def cos(p, q):
    d = sum(p[x] * q[x] for x in p)
    n = math.sqrt(sum(v * v for v in p.values())) * math.sqrt(sum(v * v for v in q.values()))
    return d / n if n else 0.0


def norm(p):
    s = sum(p.values()) or 1
    return collections.Counter({x: v / s for x, v in p.items()})


out = open(os.path.join(HERE, 'concept_games_all.tsv' if ALL else 'concept_games.tsv'), 'w')
out.write('concept\tgame\tcounted\tcards\tlinks\tlike_others\twhere\tkeywords\tpartners\n')
for k in want:
    for g in games:
        n = sum(1 for i, gg in real.items() if gg == g and k in con[i])
        if not n: continue
        others = collections.Counter()
        for h in games:
            if h != g: others.update(norm(partners[(k, h)]))
        p = partners[(k, g)]
        w = where[(k, g)]; ws = sum(w.values()) or 1
        out.write('\t'.join([k, g, 'yes' if g in want[k] else 'no', str(n), str(len(p)), f'{cos(norm(p), others):.2f}' if p else '',
                             ', '.join(f'{x} {v / ws:.0%}' for x, v in w.most_common(3)),
                             ', '.join(f'{x} {v}' for x, v in kws[(k, g)].most_common(3)),
                             ', '.join(f'{x} x{v:.1f}' for x, v in p.most_common(4))]) + '\n')
print('written', out.name)
