"""Step 4: every library concept with real cards that is in no mechanic's concept list, and where its cards land.
For each such concept, per game: the share of its cards that a radius (axes.SPOKES) or a mechanic (mechanics.tsv)
counts; the shares are averaged over the games with 3+ of its cards, so each game counts the same.
Writes factions/wheel/work/concept_sort.tsv: concept, cards, games, caught by any mechanic, the top mechanic,
caught by any radius, the top radius, caught (script), decision. A concept is caught when half its cards are in one mechanic or radius
(script; the radii of stats and "one chosen" catch nothing: Claude's rule); the decisions come from work/concept_verdicts.tsv (concept, decision; Claude's): one for every concept caught
nowhere, and for a catch by chance (the concept's cards share another effect, not this one).
Usage (from library/cards_db): python3 ../../factions/wheel/work/concept_catch.py"""
import collections, os, sys
sys.path.insert(0, os.getcwd())
import axes, mechanics_wheel

HERE = os.path.dirname(os.path.abspath(__file__))
MIN_GAME = 3      # a game counts for a concept when it has 3+ of its cards (a rarer concept: every game that has it)
CAUGHT = 0.5      # half the concept's cards in one mechanic or radius: caught there
NO_CATCH = ('strong', 'tough', 'one')        # radii of stats and of the default target say nothing of what a card does
BY_STATS = ('cheapunit*', 'dearunit*')       # wide and tall catch by what cards do (summon), not by their cost


def main():
    mechs = mechanics_wheel.load()
    c, games, x, con, pools, stats = mechanics_wheel.setup()
    in_mech = {k.partition('@')[0] for _, _, cons, *_ in mechs for k in cons}
    groups = [('m', k, cons) for k, _, cons, *_ in mechs] + [('r', s[0], [k for k in s[4] if k not in BY_STATS])
                                                               for s in axes.SPOKES if s[0] not in NO_CATCH]
    per = collections.defaultdict(lambda: collections.defaultdict(list))  # concept -> game -> card ids
    for g in pools:
        for i in pools[g]:
            for k in con[i]:
                if not k.endswith('*') and k not in in_mech: per[k][g].append(i)
    verdicts = {}
    vf = os.path.join(HERE, 'concept_verdicts.tsv')
    if os.path.exists(vf):
        for line in open(vf, encoding='utf-8').read().splitlines()[1:]:
            k, v = (line.split('\t') + [''])[:2]
            verdicts[k] = v
    rows = []
    for k, bygame in per.items():
        n = sum(len(v) for v in bygame.values())
        gs = [g for g, v in bygame.items() if len(v) >= MIN_GAME]
        if not gs: gs = list(bygame)  # a rare concept: every game that has it
        share = {}
        anym = anyr = 0.0
        for g in gs:
            ids = bygame[g]
            hit = {(t, key): sum(1 for i in ids if axes.counts(con[i], g, cons)) / len(ids) for t, key, cons in groups}
            for key_, v in hit.items(): share[key_] = share.get(key_, 0) + v / len(gs)
            anym += sum(1 for i in ids if any(axes.counts(con[i], g, cons) for t, _, cons in groups if t == 'm')) / len(ids) / len(gs)
            anyr += sum(1 for i in ids if any(axes.counts(con[i], g, cons) for t, _, cons in groups if t == 'r')) / len(ids) / len(gs)
        tm = max(((v, key) for (t, key), v in share.items() if t == 'm'), default=(0, ''))
        tr = max(((v, key) for (t, key), v in share.items() if t == 'r'), default=(0, ''))
        if tm[0] >= CAUGHT: v = 'caught by mechanic ' + tm[1]
        elif tr[0] >= CAUGHT: v = 'caught by radius ' + tr[1]
        else: v = 'none'
        rows.append((n, k, len(gs), anym, tm, anyr, tr, v, verdicts.get(k, 'OPEN' if v == 'none' else '')))
    rows.sort(key=lambda r: -r[0])
    with open(os.path.join(HERE, 'concept_sort.tsv'), 'w', encoding='utf-8') as f:
        f.write('concept\tcards\tgames\tany mechanic\ttop mechanic\tany radius\ttop radius\tcaught (script)\tdecision (Claude\'s)\n')
        for n, k, ng, am, tm, ar, tr, v, d in rows:
            f.write(f'{k}\t{n}\t{ng}\t{am:.2f}\t{tm[1]} {tm[0]:.2f}\t{ar:.2f}\t{tr[1]} {tr[0]:.2f}\t{v}\t{d}\n')
    print(len(rows), 'concepts;', sum(1 for r in rows if r[7].startswith('caught')), 'caught;',
          sum(1 for r in rows if r[8] == 'OPEN'), 'open')


if __name__ == '__main__':
    main()
