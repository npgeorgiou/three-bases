"""Tools for the line checks (START_DATABASE.md Part 3; START_DATABASE.md "Token economy"). Scripts cost no tokens; they prepare what readers read.
  audit_pieces.py split <file> [max_bytes=55000]   cut a check output into pieces a reader reads in ONE call (at deck borders;
                                                   each piece shows every card's rows once)
  audit_pieces.py verify <causes.md> <out.md>      under every example line "- A -> B: ..." of a causes file, add both cards'
                                                   rows, the line as it is now (NONE = gone) and the test cases of that pair,
                                                   so a verifier needs no lookups (its "Games: ..." line picks the game)"""
import csv, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
G = {'runeterra': 'runeterra', 'slay the spire': 'sts1', 'sts1': 'sts1', 'faeria': 'faeria', 'duelyst': 'duelyst',
     'stormbound': 'stormbound', 'monster train': 'monster_train', 'inscryption': 'inscryption', 'into the breach': 'into_the_breach',
     'marvel snap': 'marvel_snap', 'marvel_snap': 'marvel_snap', 'gwent': 'gwent'}


def split(f, cap=55000):
    t = open(f, encoding='utf-8').read().split('\n'); parts, cur, n = [], [], 0
    for l in t:
        if (l.startswith(('=== ', '## ')) and cur and n > cap * 0.6) or n > cap: parts.append(cur); cur, n = [], 0
        cur.append(l); n += len(l) + 1
    if cur: parts.append(cur)
    first, R = {}, re.compile(r'^(\s+)(.+?): (.*)$')  # a card's rows as first printed; a later piece repeats them once
    for p in parts:
        told = set()
        for j, l in enumerate(p):
            m = R.match(l)
            if not m: continue
            if m.group(3) == '(rows above)' and m.group(2) not in told and m.group(2) in first:
                p[j] = f'{m.group(1)}{m.group(2)}: {first[m.group(2)]}'
            elif m.group(3) != '(rows above)': first.setdefault(m.group(2), m.group(3))
            told.add(m.group(2))
    for i, p in enumerate(parts, 1):
        nm = f'{f.rsplit(".", 1)[0]}_{i}.txt'; open(nm, 'w', encoding='utf-8').write('\n'.join(p)); print(nm, sum(len(x) + 1 for x in p))


def verify(src, dst):
    import rows
    c = rows.c; c.execute(f"attach '{os.path.join(HERE, 'links.sqlite')}' as L")
    cases = list(csv.DictReader(open(os.path.join(HERE, 'cases', 'network.tsv'), encoding='utf-8'), delimiter='\t'))
    out, games = [], list(dict.fromkeys(G.values()))
    for line in open(src, encoding='utf-8'):
        out.append(line.rstrip('\n'))
        m = re.search(r'Games?: ([^.\n]+)', line)
        if m: games = [G[g.strip().lower()] for g in m.group(1).split(',') if g.strip().lower() in G] or games
        m = re.match(r'\s*[-*] (?:\(no line exists\) )?(.+?) -> (.+?)(?::|$)', line)
        if not m: continue
        A, B = m.group(1).strip(' `*'), m.group(2).strip(' `*')
        for g in games:
            ia = c.execute('select id from card where game=? and name=? and is_stub=0', (g, A)).fetchone()
            ib = c.execute('select id from card where game=? and name=? and is_stub=0', (g, B)).fetchone()
            if not (ia and ib): continue
            now = [f'{k}: {t}' for k, t in c.execute('select p.kind, p.text from L.link l join L.phrase p on p.id=l.phrase where l.a=? and l.b=?', (ia[0], ib[0]))]
            out.append(f'        [{g}] line now: ' + ('; '.join(x.replace('{A}', A).replace('{B}', B) for x in now) or 'NONE'))
            out += [f'        {A}: {rows.compact(ia[0])}', f'        {B}: {rows.compact(ib[0])}']
            out += [f"        case {r['id']}: expect {r['expect']} {r['why_not']} ({r['source'][:90]})" for r in cases
                    if r['game'] == g and r['from'] in (A, '*') and r['to'] == B]
            break
        else: out.append('        (cards not found by these names)')
    open(dst, 'w', encoding='utf-8').write('\n'.join(out) + '\n')


if __name__ == '__main__':
    if sys.argv[1] == 'split': split(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 55000)
    elif sys.argv[1] == 'verify': verify(sys.argv[2], sys.argv[3])
