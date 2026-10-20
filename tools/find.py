#!/usr/bin/env python3
"""Targeted lookups, so a task reads only the lines it needs (output: file:line  text;
code paths are relative to src/game/, other paths to the repository root).

  python3 tools/find.py kw <Keyword or flag>   cards with it, then every code line using its flag(s)
  python3 tools/find.py card <name or id>      the card's data line and its lines in summary/
  python3 tools/find.py where <identifier>     definition and uses of a function/constant/flag in src/game/js
  python3 tools/find.py doc <text>             lines in summary/ and factions/ containing the text (case-insensitive)

A keyword's flag is worked out from the card data: the flags shared by every card whose text shows
[[Keyword]] (e.g. Shield wall -> wall). Card art (js/cards/art.js) is never searched.
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS = os.path.join(ROOT, 'src', 'game', 'js')
CARD_FILES = [os.path.join(JS, 'cards', f + '.js') for f in ('tagma', 'ashfang', 'exanimati')]
BASE_FIELDS = {'name', 'fac', 'size', 'sup', 'str', 'def', 'art', 'text', 'cost', 'tactic', 'costLabel', 'spell', 'shape'}
W = 130


def rel(p):
    r = os.path.relpath(p, ROOT)
    return r[len('src/game/'):] if r.startswith('src/game/') else r


def lines_of(p):
    with open(p, encoding='utf-8') as f:
        return f.read().splitlines()


def js_files():
    order = [n.strip() for n in open(os.path.join(ROOT, 'src', 'game', 'parts.txt')) if n.strip().endswith('.js')]
    return [os.path.join(ROOT, 'src', 'game', n) for n in order if not n.endswith('cards/art.js')]


def cards():
    out = []
    for p in CARD_FILES:
        for i, ln in enumerate(lines_of(p), 1):
            m = re.match(r"\s*(\w+):\{(.*)\},?\s*$", ln)
            if m:
                body = re.sub(r"'(?:[^'\\]|\\.)*'", "''", m.group(2))
                body = re.sub(r"\{[^{}]*\}", "{}", body)
                fields = set(re.findall(r"(?:^|,)\s*(\w+):", body))
                kws = set(k.split('|')[-1] for k in re.findall(r"\[\[([^\]]+)\]\]", m.group(2)))
                out.append((m.group(1), p, i, ln, fields - BASE_FIELDS, kws))
    return out


def show(p, i, ln):
    print(f'{rel(p)}:{i}  {ln.strip()[:W]}')


def grep(pattern, files):
    rx = re.compile(pattern)
    for p in files:
        for i, ln in enumerate(lines_of(p), 1):
            if rx.search(ln):
                show(p, i, ln)


def kw(arg):
    cs = cards()
    having = [c for c in cs if any(k.lower() == arg.lower() for k in c[5])]
    if having:
        flags = set.intersection(*(c[4] for c in having))
        allf = set().union(*(c[4] for c in having))
        guess = re.sub(r'\W', '', arg).lower()
        if guess in {f.lower() for f in allf}:
            flags = {f for f in allf if f.lower() == guess}
        elif not flags:   # a card may name the keyword without having it (e.g. one that gives it)
            flags = {f for f in allf if sum(f in c[4] for c in having) * 2 > len(having)}
        print(f'# {arg}: flag(s) {", ".join(sorted(flags)) or "none found (check the card lines)"}; cards: {", ".join(c[0] for c in having)}')
    else:
        flags = {arg}
        having = [c for c in cs if arg in c[4]]
        print(f'# flag {arg}; cards: {", ".join(c[0] for c in having) or "none"}')
    for f in sorted(flags):
        print(f'# code using {f}:')
        grep(r"(?<![\w$])'?%s'?(?![\w$])" % re.escape(f), [p for p in js_files() if p not in CARD_FILES])


def card(arg):
    a = arg.lower()
    hit = [c for c in cards() if c[0].lower() == a or re.search(r"name:'%s'" % re.escape(arg), c[3], re.I)]
    for c in hit:
        show(c[1], c[2], c[3])
        name = re.search(r"name:'((?:[^'\\]|\\.)*)'", c[3]).group(1)
        grep(r'(?i)\b%s\b' % re.escape(name), sorted(glob.glob(os.path.join(ROOT, 'summary', '*.txt'))))
    if not hit:
        print('no card with that name or id')


def where(arg):
    rx = r'(?<![\w$])%s(?![\w$])' % re.escape(arg)
    files = js_files()
    grep(r'(function\s+|const\s+|let\s+)%s(?![\w$])' % re.escape(arg), files)
    print('# uses:')
    grep(rx, files)


def doc(arg):
    files = sorted(glob.glob(os.path.join(ROOT, 'summary', '*.txt')) + glob.glob(os.path.join(ROOT, 'factions', '**', '*.txt'), recursive=True))
    grep(r'(?i)' + re.escape(arg), files)


if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    if len(sys.argv) < 3 or sys.argv[1] not in ('kw', 'card', 'where', 'doc'):
        print(__doc__)
        sys.exit(1)
    {'kw': kw, 'card': card, 'where': where, 'doc': doc}[sys.argv[1]](' '.join(sys.argv[2:]))
