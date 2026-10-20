#!/usr/bin/env python3
"""Build the downloadable HTML files from src/.

  python3 tools/build.py          build three-bases-game.html and three-bases-scenarios.html
  python3 tools/build.py --check  only verify that both files match src/ (exit 1 if not)

The game is src/game/parts.txt's files joined in that order, byte for byte (parts are
fragments, not standalone files). The scenarios page is the game with its own title,
src/scenarios/scenarios.css before </style> and src/scenarios/scenarios.html after the
game's </script>. Never edit the two HTML files by hand: edit src/ and build.
"""
import os, re, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src')
MAX_LINES = 400  # parts longer than this should be split at a section or function boundary


def read(p):
    with open(p, encoding='utf-8', newline='') as f:
        return f.read()


def build():
    names = [n.strip() for n in read(os.path.join(SRC, 'game', 'parts.txt')).splitlines() if n.strip()]
    warn = []
    texts = []
    for n in names:
        t = read(os.path.join(SRC, 'game', n))
        if n.endswith('.js') and t.count('\n') > MAX_LINES:
            warn.append(f'{n}: {t.count(chr(10))} lines (> {MAX_LINES}); split it')
        texts.append(t)
    game = ''.join(texts)
    scen = game.replace('<title>Three Bases</title>', '<title>Three Bases · scenarios</title>', 1)
    i = scen.index('</style>\n')
    scen = scen[:i] + read(os.path.join(SRC, 'scenarios', 'scenarios.css')) + scen[i:]
    i = scen.rindex('</script>\n') + len('</script>\n')
    scen = scen[:i] + read(os.path.join(SRC, 'scenarios', 'scenarios.html')) + scen[i:]
    return game, scen, warn


def syntax_check(html):
    """node --check on every inline script; returns error text or ''."""
    out = []
    for k, js in enumerate(re.findall(r'<script>\n(.*?)</script>', html, re.S)):
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
            f.write(js)
        try:
            r = subprocess.run(['node', '--check', f.name], capture_output=True, text=True)
            if r.returncode:
                out.append(f'script {k + 1}: ' + r.stderr.strip().splitlines()[-1])
        except FileNotFoundError:
            return ''
        finally:
            os.unlink(f.name)
    return '\n'.join(out)


def main():
    game, scen, warn = build()
    files = {'three-bases-game.html': game, 'three-bases-scenarios.html': scen}
    if '--check' in sys.argv:
        bad = [n for n, t in files.items() if not os.path.exists(os.path.join(ROOT, n)) or read(os.path.join(ROOT, n)) != t]
        print('out of date: ' + ', '.join(bad) if bad else 'ok')
        sys.exit(1 if bad else 0)
    err = syntax_check(scen)
    if err:
        print('SYNTAX ERROR, nothing written:\n' + err)
        sys.exit(1)
    changed = []
    for n, t in files.items():
        p = os.path.join(ROOT, n)
        if not os.path.exists(p) or read(p) != t:
            with open(p, 'w', encoding='utf-8', newline='') as f:
                f.write(t)
            changed.append(n)
    print('built: ' + (', '.join(changed) if changed else 'nothing changed'))
    for w in warn:
        print('warning: ' + w)


if __name__ == '__main__':
    main()
