"""causes.py <verdict file> [...] [--out FILE]: the fixer's sheet for verified causes (run after the verifiers, before any fix).

For every REAL or PARTLY cause it adds what a fixer would otherwise look up one by one:
  - each example pair's game, its current line (NONE = gone) and the network.py lines that made it;
  - the rows of both cards (when / if / do), short;
  - the cases in cases/*.tsv with both cards, and a CONFLICT mark when a case says the opposite (the case wins: skip the cause);
  - how many lines of the whole table (links.sqlite, build it first with links.py) come from the same network.py lines:
    lines with the same reason from the same code: the lines one fix there can change. Causes are sorted by it, biggest first.
Writes the sheet to --out (default causes_sheet.md) and prints one short line per cause: number, worth, games, state.
Verdict format (VERIFIER_JOB.md): "N. VERDICT: why. Wrong examples: A -> B, ... Right examples: A -> B, ..."
"""
import collections, csv, glob, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import network

c = sqlite3.connect('cards.sqlite')
args = [a for a in sys.argv[1:] if not a.startswith('--')]
out_path = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else 'causes_sheet.md'
args = [a for a in args if a != out_path]
links = sqlite3.connect('links.sqlite') if os.path.exists('links.sqlite') else None
site_n = collections.Counter()  # (game, network.py line, reason) -> lines in the table with that reason from that code line
if links:
    for g, s, t, n in links.execute('select l.game, l.site, p.text, count(*) from link l join phrase p on p.id=l.phrase group by 1, 2, 3'):
        for x in re.findall(r'\d+', str(s)):
            for part in re.split(r'; also [^:]*: |; ', t): site_n[(g, int(x), part)] += n
cases = [r for f in glob.glob('cases/*.tsv') for r in csv.DictReader(open(f, encoding='utf-8'), delimiter='\t')
         if r.get('from') and r.get('to') and r.get('expect')]


def ids(name):
    name = re.sub(r' \((?!level).*?\)$', '', name.strip())
    return name, c.execute('select id, game from card where name=? and is_keyword=0', (name,)).fetchall()


def rows(i):
    q = lambda sql: [' '.join(str(x) for x in r if x not in (None, '')) for r in c.execute(sql, (i,))]
    return (['when ' + x for x in q("select ability, event, obj_kind, obj_side, obj_pick, obj_with from flat_when where card=?")] +
            ['if ' + x for x in q("select ability, test, attr, op, n, of_kind, of_side, of_pick, of_zone, of_with from flat_if where card=?")] +
            ['do ' + x for x in q("select ability, origin, act, on_kind, on_side, on_pick, on_zone, on_with, params from flat_do where card=?")])


def pair(a, b, wrong):
    (an, A), (bn, B) = ids(a), ids(b)
    ps = [(x, y, g) for x, g in A for y, g2 in B if g == g2]
    if not ps: return None
    x, y, g = ps[0]
    network.SITE.clear()
    _, ls = network.network(c, g, [x, y])
    why = '; '.join(z for _, _, z in ls.get((x, y), [])) or 'NONE'
    sites = sorted({s for k, v in network.SITE.items() if k[:2] == (x, y) for s in v})
    cs = [r for r in cases if r['game'] == g and r['from'] in (an, '*') and r['to'] == bn]
    clash = [r['id'] for r in cs if (r['expect'] == 'line') == wrong]
    return dict(a=an, b=bn, x=x, y=y, game=g, why=why, sites=sites, cases=cs, clash=clash, wrong=wrong,
                open=(why != 'NONE') == wrong)


sheet = []
for f in args:
    for line in open(f, encoding='utf-8'):
        m = re.match(r'(\d+)\. (REAL|PARTLY)\b:? ?(.*?)(?: Wrong examples: (.*?)\.)?(?: Right examples: (.*?)\.?)?$', line.strip())
        if not m: continue
        n, verdict, why, w, r = m.groups()
        ps = []
        for txt, wrong in ((w or '', True), (r or '', False)):
            for p in re.split(r', (?=[^,]*->)', txt):
                if '->' in p: ps.append(pair(*[s.strip() for s in p.split('->', 1)], wrong))
        ps = [p for p in ps if p]
        worth = sum(site_n[(p['game'], s, part)] for p in ps if p['wrong'] and p['open'] for s in p['sites']
                    for part in set(re.split(r'; also [^:]*: |; ', p['why'])))  # the same reason from the same code line
        state = 'CONFLICT ' + ','.join(sorted({x for p in ps for x in p['clash']})) if any(p['clash'] for p in ps) else \
            'open' if any(p['wrong'] and p['open'] for p in ps) else 'gone'
        sheet.append((worth, f, n, verdict, why, ps, state))

sheet.sort(key=lambda s: (s[6] != 'open', -s[0]))
with open(out_path, 'w', encoding='utf-8') as o:
    for worth, f, n, verdict, why, ps, state in sheet:
        o.write(f'## {os.path.basename(f)} {n} ({verdict}, {state}, {worth} table lines from the same code)\n{why}\n')
        for p in ps:
            o.write(f"- {'W' if p['wrong'] else 'R'} {p['game']}: {p['a']} -> {p['b']}: {p['why'][:160]} | network.py {p['sites']}"
                    + (f" | cases {', '.join(r['id'] + ' ' + r['expect'] for r in p['cases'])}" if p['cases'] else '') + '\n')
        seen = set()
        for p in ps:
            if not (p['wrong'] and p['open']): continue
            for name, i in ((p['a'], p['x']), (p['b'], p['y'])):
                if i in seen: continue
                seen.add(i)
                o.write(f'  {name}:\n' + ''.join(f'    {r_[:200]}\n' for r_ in rows(i)))
        o.write('\n')
for worth, f, n, verdict, why, ps, state in sheet:
    print(f"{os.path.basename(f).split('.')[0]} {n}: {worth} {state} {','.join(sorted({p['game'][:4] for p in ps}))}")
print(out_path)
