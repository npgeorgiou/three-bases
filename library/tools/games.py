"""One file per game: tools/games/<game>.md holds the game overview, its factions, the source summary, and two fenced blocks
read by the tools: ```mechanics (name|concept|regex lines and # term: lines) and ```tsv (the real-world cases)."""
import glob, os
HERE = os.path.dirname(os.path.abspath(__file__)); DIR = os.path.join(HERE, 'games')

def path(game): return os.path.join(DIR, game + '.md')

def files():
    """(game, path) for every game file, sorted."""
    return [(os.path.basename(f)[:-3], f) for f in sorted(glob.glob(os.path.join(DIR, '*.md')))]

def block(f, kind):
    """The lines (with newline) of the file's ```<kind> block; a plain .txt/.tsv file is read whole; [] if missing."""
    if not os.path.exists(f): return []
    ls = open(f, encoding='utf-8').readlines()
    if not f.endswith('.md'): return ls
    out, on = [], False
    for l in ls:
        if l.rstrip('\n') == '```' + kind: on = True; continue
        if on and l.rstrip('\n') == '```': break
        if on: out.append(l)
    return out
