"""Check every game after a change, loading the database ONCE. Use this, never `run.py <game>` once per game: each run.py
reloads all eight games (load.py always loads every game), so eight runs reload eight times (over an hour, 30 Oct 2026).
  check_all.py <game>          a change to records or to shared code: run.py <game> (loads all games once, full checks for
                               it), then cases and link audit for every other game (no reload)
  check_all.py --no-load       a change to network.py only (lines, wording): it reads cards.sqlite, nothing to reload; cases
                               and link audit for every game"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
GAMES = ['runeterra', 'stormbound', 'monster_train', 'duelyst', 'faeria', 'inscryption', 'into_the_breach', 'sts1']


def out(cmd):
    r = subprocess.run([sys.executable] + cmd, cwd=HERE, capture_output=True, text=True)
    return (r.stdout + r.stderr).strip().splitlines()


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else '--no-load'
    rest = GAMES
    if arg != '--no-load':
        print('\n'.join(l for l in out(['run.py', arg]) if not l.startswith(('ok  normalize', 'ok  check'))))
        rest = [g for g in GAMES if g != arg]
    for g in rest:
        cases = [l for l in out(['cases/run.py', g]) if l]
        audit = next((l for l in out(['audit_links.py', g]) if 'link findings' in l), '')
        print(f'{g}: {" | ".join(cases[-2:])} | {audit.strip()}')


main()
