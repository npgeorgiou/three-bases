"""The wheel table check (factions/12, method 6): python3 tools/wheel_table_check.py
Reads factions/14-wheel-pool.tsv (mechanics), 15-wheel-factions.tsv (the 20 factions), 16-wheel-joins.tsv (trigger -> payoff
for every two mechanic radii of a faction) and 17-wheel-overlaps.tsv (the combo of each pair of neighbours).
Checks: 20 factions in places 1-20; 3-6 strong radii, all real radii; 2+ blind spots outside the faction's radii and outside
the radii of every mechanic it owns or shares; 2-3 monopolies, each owned once and serving a strong radius; a mechanic is
used only by its owner and the owner's two neighbours; each pair of neighbours shares a strong radius and has one overlap
whose mechanics match both factions' shared columns; one join line for every two mechanic radii of each faction; no two
factions with the same strong radii or the same archetype. Prints each join's library number (the page's "Radii that work
together"; under 0.9 means the join must be argued from this game's rules) and the 2 real factions closest to each shape
(axes.py --near: strong radii 1.8, blind spots 0.2). Exit 1 on any problem."""
import csv, itertools, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, 'factions')
DB = os.path.join(ROOT, 'library', 'cards_db')
SHAPE = {'strong', 'tough', 'wide', 'tall'}  # give a faction its shape; not mechanics (START_DESIGN-1)


def tsv(name):
    with open(os.path.join(F, name), encoding='utf-8') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def words(s):
    return [w.strip() for w in s.split(',') if w.strip() and w.strip() != '-']


def main():
    bad = []
    html = open(os.path.join(F, 'wheel-axes.html'), encoding='utf-8').read()
    i = html.index('const DATA=') + len('const DATA=')
    links = json.JSONDecoder().raw_decode(html[i:])[0]['links']['cards']
    radii = set(links) | SHAPE | {'together'}
    pool = {r['id']: r for r in tsv('14-wheel-pool.tsv')}
    facs = tsv('15-wheel-factions.tsv')
    ids = [f['id'] for f in sorted(facs, key=lambda f: int(f['place']))]
    by = {f['id']: f for f in facs}
    if sorted(int(f['place']) for f in facs) != list(range(1, 21)):
        bad.append('places are not 1-20')
    left = {ids[k]: ids[k - 1] for k in range(len(ids))}
    right = {ids[k]: ids[(k + 1) % len(ids)] for k in range(len(ids))}
    for m, r in pool.items():
        for x in words(r['radii']):
            if x not in radii: bad.append(f'pool {m}: no radius {x}')
    owned = {}
    for f in facs:
        k, strong, blind = f['id'], words(f['strong radii']), words(f['blind spots (radii it never has)'])
        mono = words(f['monopolies'])
        uses = mono + words(f['shared with left']) + words(f['shared with right'])
        if not 3 <= len(strong) <= 6: bad.append(f'{k}: {len(strong)} strong radii')
        for x in strong + blind:
            if x not in radii: bad.append(f'{k}: no radius {x}')
        if len(blind) < 2: bad.append(f'{k}: fewer than 2 blind spots')
        for m in uses:
            if m not in pool: bad.append(f'{k}: mechanic {m} not in the pool'); continue
            for x in set(words(pool[m]['radii'])) & set(blind):
                bad.append(f'{k}: blind spot {x} but uses {m}')
        if not 2 <= len(mono) <= 3: bad.append(f'{k}: {len(mono)} monopolies')
        for m in mono:
            if m in owned: bad.append(f'{m}: monopoly of {owned[m]} and {k}')
            owned[m] = k
            if m in pool and pool[m]['owner'] != k: bad.append(f'{k}: monopoly {m} has owner {pool[m]["owner"]} in the pool')
            if m in pool and not set(words(pool[m]['radii'])) & set(strong): bad.append(f'{k}: monopoly {m} serves none of its strong radii')
        for m in words(f['shared with left']) + words(f['shared with right']):
            o = pool.get(m, {}).get('owner')
            if o not in (k, left[k], right[k]): bad.append(f'{k}: shares {m}, owned by {o}, not a neighbour')
        if not set(strong) & set(words(by[right[k]]['strong radii'])): bad.append(f'{k}-{right[k]}: neighbours share no strong radius')
        if words(f['shared with right']) != words(by[right[k]]['shared with left']): bad.append(f'{k}-{right[k]}: shared columns differ')
    for m, r in pool.items():
        if r['owner'] != '-' and owned.get(m) != r['owner']: bad.append(f'pool {m}: owner {r["owner"]} does not list it')
    for a, b in itertools.combinations(facs, 2):
        if set(words(a['strong radii'])) == set(words(b['strong radii'])): bad.append(f'{a["id"]}, {b["id"]}: same strong radii')
        if a['archetype (how it wins)'] == b['archetype (how it wins)']: bad.append(f'{a["id"]}, {b["id"]}: same archetype')
    over = {r['pair']: r for r in tsv('17-wheel-overlaps.tsv')}
    for k in ids:
        p = f'{k}-{right[k]}'
        if p not in over: bad.append(f'{p}: no overlap'); continue
        if words(over[p]['shared mechanics']) != words(by[k]['shared with right']): bad.append(f'{p}: overlap mechanics differ from the table')
    joins = {}
    for r in tsv('16-wheel-joins.tsv'):
        joins.setdefault(r['faction'], {})[frozenset((r['radius 1'], r['radius 2']))] = r
    low = []
    for k in ids:
        mech = [x for x in words(by[k]['strong radii']) if x not in SHAPE]
        want = {frozenset(p) for p in itertools.combinations(mech, 2)}
        have = set(joins.get(k, {}))
        for p in want - have: bad.append(f'{k}: no join for {" + ".join(sorted(p))}')
        for p in have - want: bad.append(f'{k}: join for {" + ".join(sorted(p))}, not two of its mechanic radii')
        for p in want & have:
            a, b = sorted(p)
            n = links.get(a, {}).get(b)
            if n is not None and n < 0.9: low.append(f'{k} {a}+{b} {n}')
    print('joins under 0.9 (argue from the rules):', '; '.join(low) or 'none')
    for k in ids:
        f = by[k]
        arg = ','.join([f'{x}=1.8' for x in words(f['strong radii'])] + [f'{x}=0.2' for x in words(f['blind spots (radii it never has)'])])
        out = subprocess.run([sys.executable, 'axes.py', '--near', arg], cwd=DB, capture_output=True, text=True).stdout.splitlines()
        print(f'{k} closest: ' + ' | '.join(' '.join(l.split()[:4]) for l in out[:2]))
    for b in bad: print('PROBLEM', b)
    print('wheel table:', 'OK' if not bad else f'{len(bad)} problems')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
