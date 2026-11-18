#!/usr/bin/env python3
"""Design gate: a faction is only finished when every check here passes. Prints each check, then PASS or FAIL.
   python3 tools/design_gate.py <faction letter> [--no-play]
Checks (rules from factions/START_DESIGN.md and summary/09; numbers marked "Claude's" are open to Kaptain's change):
  1  count       exactly 100 cards
  2  library     factions/designs/<file>-library.txt: 3-5 ways to play ("WAY <name>" lines), each with 20+ library cards
                 ("<game> | <card> | <play pattern>"); every card found in library/cards_db/cards.sqlite, any of the 8 games
  3  source      every card has src: 'own' (Claude's own idea) or '<game>: <card>' (a library card that exists)
  4  budget      every unit: strength + defence = budget(supply) - size - keyword values - tv (tv = value of its text;
                 negative for a drawback; required when the card has text beyond keywords)
  5  leaders     exactly 5 cards with leader: true
  6  hovers      every keyword word in a card text is linked ([[Word]]) at least once in that text
  7  network     tools/network_check.py on the entry and cards files: 0 problems
  8  play        tools/playtest.js <letter>: real games and every scenario in a browser without script errors
The faction's design files are factions/designs/<name>.txt, <name>-library.txt and <name>-cards.txt, where <name> is
its deck's name in lower case without spaces (DECKS in js/cards/).
"""
import json, os, re, sqlite3, subprocess, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = {'slay the spire': 'sts1', 'slay_the_spire': 'sts1', 'legends of runeterra': 'runeterra'}  # names as written -> library game ids
BUDGET = {0: 0, 1: 3, 2: 5, 3: 7, 4: 8, 5: 10}
SIZE = {1: 0, 2: 1, 3: 2, 4: 3}
# values in the supply budget (summary/06): card property -> value per point (N: n * per + plus)
KW = {'ranged': (3, 0), 'bonus': (3, 0), 'fixed': (-2, 0)}
DUMP = r"""
const fs=require('fs'),vm=require('vm'),P=process.argv[1]+'/src/game/';
const parts=fs.readFileSync(P+'parts.txt','utf8').split('\n').map(s=>s.trim()).filter(n=>/^js\/cards\//.test(n));
const ctx={};vm.createContext(ctx);vm.runInContext(parts.map(n=>fs.readFileSync(P+n,'utf8')).join('\n')+';globalThis.C=CARDS;globalThis.K=KEYWORDS;globalThis.D=DECKS;',ctx);
const out=[];for(const [k,c] of Object.entries(ctx.C)){if(c.fac===process.argv[2])out.push(Object.assign({},c,{key:k}));}
const deck=Object.values(ctx.D).find(d=>d.fac===process.argv[2]);
console.log(JSON.stringify({cards:out,kw:Object.keys(ctx.K),name:deck?deck.name:null}));
"""


def budget(s):
    return BUDGET.get(s, 2 * s)


def kwvalue(c):
    v = 0
    for k, (per, plus) in KW.items():
        n = c.get(k)
        if n:
            n = 1 if n is True else n
            v += n * per + plus
    return v


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print(__doc__); sys.exit(2)
    letter = args[0]
    data = json.loads(subprocess.run(['node', '-e', DUMP, ROOT, letter], capture_output=True, text=True, check=True).stdout)
    if not data['name']:
        print(f'no deck of faction {letter} in the game'); sys.exit(2)
    file = re.sub(r'[^a-z0-9]', '', data['name'].lower())
    cards = units = data['cards']
    results = []

    def check(name, problems, note=''):
        results.append((name, problems))
        print(f"{'ok  ' if not problems else 'FAIL'} {name}{': ' + note if note else ''}")
        for p in problems[:12]:
            print('       ' + p)
        if len(problems) > 12:
            print(f'       ... {len(problems) - 12} more')

    check('count', [] if len(cards) == 100 else [f'{len(cards)} cards, must be exactly 100'], f'{len(cards)} cards')

    db = os.path.join(ROOT, 'library', 'cards_db', 'cards.sqlite')
    con = sqlite3.connect(db) if os.path.exists(db) else None
    def exists(game, name):
        return con is not None and con.execute('select 1 from card where lower(game)=? and lower(name)=?',
                                               (GAME.get(game.lower(), game.lower().replace(' ', '_')), name.lower())).fetchone() is not None
    lib = os.path.join(ROOT, 'factions', 'designs', f'{file}-library.txt')
    probs = []
    if con is None:
        probs.append('library missing: clone with the library (git sparse-checkout disable)')
    if not os.path.exists(lib):
        probs.append(f'{os.path.relpath(lib, ROOT)} missing')
    else:
        ways, cur = defaultdict(list), None
        for line in open(lib, encoding='utf-8'):
            line = line.strip()
            if line.startswith('WAY '):
                cur = line[4:]
            elif cur and line.count('|') >= 2:
                g, n, pat = [x.strip() for x in line.split('|', 2)]
                ways[cur].append(n)
                if not exists(g, n):
                    probs.append(f'not in the library: {g} | {n}')
                if len(pat) < 15:
                    probs.append(f'no play pattern written: {n}')
        if not 3 <= len(ways) <= 5:
            probs.append(f'{len(ways)} ways to play, need 3-5')
        probs += [f'way "{w}": {len(ns)} library cards, need 20' for w, ns in ways.items() if len(ns) < 20]
    check('library', probs)

    probs, own = [], 0
    for c in cards:
        src = c.get('src')
        if not src:
            probs.append(f"{c['name']}: no src")
        elif src == 'own':
            own += 1
        elif ':' not in src or not exists(*[x.strip() for x in src.split(':', 1)]):
            probs.append(f"{c['name']}: src not found in the library: {src}")
    check('source', probs, f'{own} of {len(cards)} are Claude\'s own')

    probs = []
    for c in units:
        text = re.sub(r'\[\[[^\]]*\]\]\.?', '', c.get('text', '')).strip(' .')
        tv = c.get('tv')
        if tv is None and text:
            probs.append(f"{c['name']}: has text, no tv (value of the text)")
            continue
        want = budget(c['sup']) - SIZE.get(c.get('size', 1), 0) - kwvalue(c) - (tv or 0)
        if c['str'] + c['def'] != want:
            probs.append(f"{c['name']} {c['sup']} - {c['str']}|{c['def']}: strength + defence {c['str'] + c['def']}, budget gives {want}")
    check('budget', probs)

    ch = [c['name'] for c in cards if c.get('leader') is True]
    check('leaders', [] if len(ch) == 5 else [f'{len(ch)} cards with leader: true, need 5'])

    probs = []
    for c in cards:
        t = c.get('text', '')
        linked = {(b or a).lower() for a, b in re.findall(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', t)}  # [[shown|Key]]: the key counts
        bare = re.sub(r'\{\{[^}]*\}\}', '', re.sub(r'\[\[[^\]]*\]\]', '', t))
        for k in data['kw']:
            forms = {'Strike': r'strike|strikes'}.get(k, re.escape(k))
            if re.search(r'\b(' + forms + r')\b', bare, re.I) and k.lower() not in linked:
                probs.append(f"{c['name']}: '{k}' without [[{k}]]")
    check('hovers', probs)

    entry = os.path.join(ROOT, 'factions', 'designs', f'{file}.txt')
    cf = os.path.join(ROOT, 'factions', 'designs', f'{file}-cards.txt')
    lines = subprocess.run(['node', os.path.join(ROOT, 'tools', 'design_cards.js'), letter], capture_output=True, text=True, check=True).stdout
    open(cf, 'w', encoding='utf-8').write(lines)  # the cards file always follows the game
    r = subprocess.run(['python3', os.path.join(ROOT, 'tools', 'network_check.py'), entry, cf, '--quiet'], capture_output=True, text=True)
    last = (r.stdout.strip().split('\n') or [''])[-1]
    check('network', [] if last.strip() == '0 problems' else [last or r.stderr.strip()[:200]])

    if '--no-play' in sys.argv:
        check('play', ['skipped (--no-play): not a pass'])
    else:
        r = subprocess.run(['node', os.path.join(ROOT, 'tools', 'playtest.js'), letter], capture_output=True, text=True)
        bad = [l for l in r.stdout.split('\n') if 'FAIL' in l]
        check('play', bad if r.returncode or bad else [])

    failed = [n for n, p in results if p]
    print(f"\n{data['name']}: {'PASS' if not failed else 'FAIL (' + ', '.join(failed) + ')'}")
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
