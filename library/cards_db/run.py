"""The whole build of one game in one command, in the only safe order. Stops at the first failing step.
  1 refuses to start while a reader is writing (part files in read/<game>/)
  2 normalize.py on every record file (one canonical form for equal meanings)
  3 check.py on every batch (0 problems required)
  4 load.py (cards.sqlite and the query layer)
  5 cases/run.py (all cases must pass)
  6 pattern_check.py (word check; open flags are listed, not a failure)
  7 status.py, examples.py (STATUS.md, QUERIES.md)
Usage: run.py <game>"""
import glob, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))


def step(name, cmd, ok=lambda out: True):
    r = subprocess.run([sys.executable] + cmd, cwd=HERE, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip()
    last = out.splitlines()[-1] if out else ''
    if r.returncode or not ok(out):
        print(f'FAILED {name}:\n{out[-3000:]}'); sys.exit(1)
    print(f'ok  {name}: {last}')
    return out


def main():
    game = sys.argv[1]
    read = os.path.join(HERE, 'read', game)
    parts = glob.glob(os.path.join(read, '*.part*.jsonl'))
    if parts: print('A reader is still writing (part files): ' + ', '.join(map(os.path.basename, parts))); sys.exit(1)
    recs = sorted(f for f in glob.glob(os.path.join(read, '*.jsonl')) if not f.endswith(('proposals.jsonl', 'rejected.jsonl'))
                  and not os.path.basename(f).startswith('keywords'))
    step('normalize', ['normalize.py', game] + recs)
    for f in sorted(glob.glob(os.path.join(read, 'batch_*.jsonl'))) + [os.path.join(read, 'keywords.jsonl')]:
        if f.endswith('proposals.jsonl'): continue
        inp = os.path.join(HERE, 'input', game, os.path.basename(f))
        step('check ' + os.path.basename(f), ['check.py', game, f, '--input', inp], lambda o: ' 0 problems' in o)
    if os.path.exists(os.path.join(read, 'keywords_stub.jsonl')):  # only games with keywords defined by name
        step('check keywords_stub.jsonl', ['check.py', game, os.path.join(read, 'keywords_stub.jsonl')], lambda o: ' 0 problems' in o)
    games = sorted(d for d in os.listdir(os.path.join(HERE, 'read')) if os.path.isdir(os.path.join(HERE, 'read', d)))
    step('load', ['load.py'] + games)  # cards.sqlite holds every game
    step('cases', ['cases/run.py', game], lambda o: (lambda w: w[0] == w[2])(o.splitlines()[-1].split()))  # "N of N cases pass"
    step('word check', ['pattern_check.py', game])
    step('status', ['status.py', game]); step('examples', ['examples.py'])


main()
