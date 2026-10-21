"""The check after every library change: compares two builds and says what got worse.
Runs on full copies (indexes.py create, compact_text.py expand) in a scratch folder, so the stored form of either input is fine.
Prints, per game: answer-key wrong and missed per 100 entries, real-world cases met per kind (signature, archetype, combo, splash),
then the regression check, combos, the real-world cases newly met or newly missed, and the trigger -> effect pairs the new build lost
(lost_pairs.py). A line is marked WORSE when the new build is worse on it. Exit code 1 if anything is worse.
Usage: compare_builds.py <old.sqlite> <new.sqlite> [scratch dir]"""
import os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
old, new = sys.argv[1:3]
tmp = sys.argv[3] if len(sys.argv) > 3 else tempfile.mkdtemp()
os.makedirs(tmp, exist_ok=True)
run = lambda *a: subprocess.run([sys.executable, '-I', *a], cwd=HERE, capture_output=True, text=True)

def full(src, name):
    dst = os.path.join(tmp, name)
    shutil.copy(src, dst)
    run('indexes.py', dst, 'create'); run('compact_text.py', dst, 'expand')
    return dst

def key_scores(db):
    out = {}
    for l in run(os.path.join('key', 'key.py'), 'score', db).stdout.splitlines():
        m = re.match(r'(\S+)\s+entries\s+\d+\s+wrong/100\s+([\d.]+)\s+missed/100\s+([\d.]+)', l)
        if m: out[m[1]] = (float(m[2]), float(m[3]))
    return out

def realworld(db):
    per, misses, total = {}, set(), ''
    for l in run('realworld.py', db, '-v').stdout.splitlines():
        if l.startswith('  miss '): misses.add(l[7:].strip()); continue
        if l.startswith('real-world cases met'): total = l.split(':', 1)[1].strip(); continue
        m = re.match(r'(\S+)\s+((?:\w+ \d+/\d+\s*)+)$', l)
        if m: per[m[1]] = {k: tuple(map(int, v.split('/'))) for k, v in re.findall(r'(\w+) (\d+/\d+)', m[2])}
    return per, misses, total

def combos(db):
    m = re.search(r'combos found: (\d+)/(\d+).*?new misses: (\d+)', run('combo_check.py', db).stdout)
    return tuple(map(int, m.groups())) if m else None

a, b = full(old, 'old.sqlite'), full(new, 'new.sqlite')
worse = False
ka, kb = key_scores(a), key_scores(b)
ra, rb = realworld(a), realworld(b)
print(f"{'game':17} {'key wrong/100':>16} {'key missed/100':>16}   real-world met")
for g in sorted(set(ka) | set(ra[0])):
    (wa, ma), (wb, mb) = ka.get(g, (0, 0)), kb.get(g, (0, 0))
    rw = []
    for k in sorted(set(ra[0].get(g, {})) | set(rb[0].get(g, {}))):
        x, y = ra[0].get(g, {}).get(k, (0, 0)), rb[0].get(g, {}).get(k, (0, 0))
        rw.append(f'{k} {x[0]}->{y[0]}/{y[1]}' if x[0] != y[0] else f'{k} {y[0]}/{y[1]}')
    bad = wb > wa + 0.05 or mb > ma + 0.05 or any(rb[0].get(g, {}).get(k, (0, 0))[0] < v[0] for k, v in ra[0].get(g, {}).items())
    worse |= bad
    print(f'{g:17} {wa:7.1f} -> {wb:6.1f} {ma:7.1f} -> {mb:6.1f}   {", ".join(rw)}{"  WORSE" if bad else ""}')
print('real-world total:', ra[2], '->', rb[2])
for x in sorted(ra[1] - rb[1]): print('  newly met:', x)
for x in sorted(rb[1] - ra[1]): print('  newly missed:', x); worse = True
reg = run('regression.py', b, 'check')
print((reg.stdout.strip().splitlines() or ['regression: no output'])[-1] + ('  WORSE' if reg.returncode else ''))
worse |= reg.returncode != 0
ca, cb = combos(a), combos(b)
print(f'combos found: {ca[0]}/{ca[1]} -> {cb[0]}/{cb[1]}, new misses {cb[2]}' + ('  WORSE' if cb[0] < ca[0] or cb[2] else ''))
worse |= cb[0] < ca[0] or cb[2] > 0
lp = run('lost_pairs.py', a, b).stdout.strip().splitlines()
print('\n'.join(lp[-6:]))
print('WORSE somewhere' if worse else 'nothing worse')
sys.exit(1 if worse else 0)
