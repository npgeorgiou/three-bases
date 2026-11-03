"""triage.py <cause numbers, comma-separated>: the current line of each example pair of those old-round causes (verdict_1-4.md)"""
import re, sys, os, sqlite3
D=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, D); os.chdir(D)
import network
c = sqlite3.connect('cards.sqlite')
NOT = set(int(x) for x in sys.argv[1].split(','))
def ids(n):
    return c.execute("select id, game from card where name=? and is_keyword=0", (n,)).fetchall()
for f in sorted(os.listdir('audit')):
    if not re.match(r'verdict_\d\.md', f): continue
    for line in open('audit/'+f):
        m = re.match(r'(\d+)\. (\w+( \w+)?):', line)
        if not m or int(m.group(1)) not in NOT: continue
        miss = 'piece 4' in open('audit/'+f).readline()
        w = re.search(r'Wrong examples: (.*?)\. Right examples', line)
        r = re.search(r'Right examples: (.*?)\.?$', line.strip())
        out = []
        for kind, txt in (('W', w.group(1) if w else ''), ('R', r.group(1) if r else '')):
            for p in re.split(r', (?=[^,]*->)', txt):
                if '->' not in p: continue
                a, b = [x.strip() for x in p.split('->', 1)]
                b = re.sub(r' \((?!level).*?\)$', '', b); a = re.sub(r' \((?!level).*?\)$', '', a)
                A, B = ids(a), ids(b)
                pairs = [(x, y, g) for x, g in A for y, g2 in B if g == g2]
                if not pairs: out.append(f'{kind} {a}->{b}: ?'); continue
                x, y, g = pairs[0]
                _, ls = network.network(c, g, [x, y])
                l = '; '.join(z for _, _, z in ls.get((x, y), [])) or 'NONE'
                out.append(f'{kind} {g[:4]} {a}->{b}: {l[:90]}')
        print(f"{m.group(1)} {m.group(2)}{' MISSED' if miss else ''} | " + ' | '.join(out))
