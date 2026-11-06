"""Writes checks/gwent/lr_misses.md: one numbered entry per failing gwent case (cases/run_report.md) and per real-world MISS (rw.txt)."""
import csv, os, re
H = os.path.dirname(os.path.abspath(__file__)); DB = os.path.join(H, '..', '..'); G = 'gwent'
def tsv(f): return list(csv.DictReader(open(os.path.join(DB, 'cases', f), encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE))
def cut(s): return s.strip().rstrip('.')
fails = {}  # section -> rows of the report that do not pass
sec = None
for l in open(os.path.join(DB, 'cases', 'run_report.md'), encoding='utf-8'):
    if l.startswith('## '): sec = l[3:].split(' (')[0].strip()
    elif l.startswith('| ') and sec and l.rstrip().endswith('| NO |') or (l.startswith('| ') and l.rstrip().endswith('| no |')):
        fails.setdefault(sec, []).append([x.strip() for x in l.strip().strip('|').split('|')])
out = {'combos': [], 'pairs': [], 'decks': [], 'keywords': [], 'other': [], 'rw': []}
combos = {r['id']: r for r in tsv('combos.tsv')}; net = {r['id']: r for r in tsv('network.tsv')}
decks = {r['id']: r for r in tsv('decks.tsv')}; mech = {r['id']: r for r in tsv('mechanics.tsv')}; regs = {r['id']: r for r in tsv('regions.tsv')}
for s, rows in fails.items():
    for r in rows:
        i = r[0]
        if i in combos: out['combos'].append((combos[i]['why'], f"{combos[i]['enabler']} -> {combos[i]['payoff']}"))
        elif i in net: out['pairs'].append((net[i]['source'].split('): ', 1)[-1], f"{net[i]['from']} -> {net[i]['to']}"))
        elif i in decks:
            names = {c.strip().lower(): c.strip() for c in decks[i]['cards'].split(',')}
            nm = lambda x: names.get(x.strip(), x.strip().title())
            ps, ws = [], []
            for it in decks[i]['must'].split(';'):
                if it not in r[3]: continue
                m = re.match(r'(.*?)\. (?:use it|care about them|set off): (.*)$', it)
                if not m: continue
                a, b = nm(m.group(1)), nm(m.group(2)); ps.append(f"{a} -> {b}")
                ws += [cut(n['source'].split('): ', 1)[-1]) for n in net.values()
                       if n['deck'] == decks[i]['deck'] and n['from'].lower() == a.lower() and n['to'].lower() == b.lower()]
            why = '; '.join(dict.fromkeys(ws))
            out['decks'].append((why or cut(decks[i]['source']), ', '.join(ps) or r[1]))
        elif i in mech: out['keywords' if mech[i]['query'].count('is_keyword=1') else 'other'].append((mech[i]['question'], i))
        elif i in regs: out['other'].append((f"{regs[i]['region']} {regs[i]['kind']}: {regs[i]['mechanic']}", i))
        else: out['other'].append((r[1], i))
gm = {}
t = open(os.path.join(DB, '..', 'games', G + '.md'), encoding='utf-8').read()
for b in re.findall(r'```tsv\n(.*?)```', t, re.S):
    for l in b.splitlines():
        p = l.split('\t')
        if len(p) > 3 and p[0] in ('signature', 'archetype', 'splash'): gm[tuple(p[:3])] = p[3]
for l in open(os.path.join(H, 'rw.txt'), encoding='utf-8'):
    m = re.match(r'\s*MISS (\w+) \| (.*?) \| (.*?) \| (.*)', l)
    if not m: continue
    k, a, b, w = m.groups()
    sh = re.match(r'.*?: (\d+%, rank \d+ of \d+)', w)
    out['rw'].append((gm.get((k, a, b), f'{k} {a} {b}'), f"{a} -> {b} ({sh.group(1)})" if sh else f"{a} -> {b} ({w})"))
n = 0
with open(os.path.join(H, 'lr_misses.md'), 'w', encoding='utf-8') as o:
    for key in out:
        for why, ex in out[key]:
            n += 1; o.write(f"{n}. MISSED CAUSE: {cut(why)}. Wrong examples: {ex}. Right examples: none.\n")
print(n, {k: len(v) for k, v in out.items()})
