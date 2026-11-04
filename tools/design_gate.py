#!/usr/bin/env python3
"""Design gate: a faction is only finished when every check here passes. Prints each check, then PASS or FAIL.
   python3 tools/design_gate.py <faction letter> [--no-play]
Checks (rules from factions/START_DESIGN.md and summary/09; numbers marked "Claude's" are open to Kaptain's change):
  1  count       exactly 100 cards (tokens not counted)
  2  library     factions/designs/<file>-library.txt: 5+ ways to play ("WAY <name>" lines), each with 30+ library cards
                 ("<game> | <card> | <play pattern>"); every card found in library/cards_db/cards.sqlite, any of the 8 games
  3  source      every card has src: 'own' (Claude's own idea) or '<game>: <card>' (a library card that exists)
  4  budget      every unit: strength + defence = budget(supply) - size - keyword values - tv (tv = value of its text;
                 negative for a drawback; required when the card has text beyond keywords)
  5  twins       START_DESIGN step 9: no two cards whose WHEN + WHAT + ON WHOM parts are all the same; no WHEN + WHAT on more than 3 cards
                 (read from the cards' effect data; keyword effects not counted)
  6  spells      at each cost 1-5 with 4+ cards, the spell share is within 15 points of the faction's share (Claude's 15)
  7  champions   exactly 5 cards with champion: true
  8  hovers      every keyword word in a card text is linked ([[Word]]) at least once in that text
  9  network     tools/network_check.py on the entry and cards files: 0 problems
  10 play        tools/playtest.js <letter>: real games and every scenario in a browser without script errors
"""
import json, os, re, sqlite3, subprocess, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAC = {'c': 'horologers', 'd': 'sunfeeders', 'a': 'impi', 'b': 'hospice', 's': 'starpriests', 'o': 'rootkin', 'l': 'longguns'}
GAME = {'slay the spire': 'sts1', 'slay_the_spire': 'sts1', 'legends of runeterra': 'runeterra'}  # names as written -> library game ids
BUDGET = {0: 0, 1: 3, 2: 5, 3: 7, 4: 8, 5: 10}
SIZE = {1: 0, 2: 1, 3: 2, 4: 3}
# keyword values (summary/11 and the faction files): card property -> value per point (N keywords: n * per + plus)
KW = {'ranged': (3, 0), 'bonus': (3, 0), 'armoured': (2, 0), 'charge': (2, 0), 'riposte': (2, 0), 'flurry': (3, 0),
      'reach': (1, 0), 'lightfooted': (1, 0), 'wall': (1, 0), 'push': (1, 0), 'outrider': (1, 0), 'guard': (1, 0),
      'fixed': (-2, 0), 'fade': (-2, 0), 'reckless': (-2, 0), 'geared': (0, 0), 'wound': (1, 0), 'salvage': (1, 0),
      'toll': (1, 0), 'obsidian': (1, 0), 'onrush': (1, 0), 'flanker': (1, 0), 'reserve': (1, 0), 'harden': (1, 0),
      'retaliate': (1, 0), 'vigil': (1, 0), 'augur': (2, 0), 'perennial': (3, 0), 'seeds': (1, 1), 'roots': (1, 1),
      'entrench': (1, 0), 'barrage': (1, 1)}
DUMP = r"""
const fs=require('fs'),vm=require('vm'),P=process.argv[1]+'/src/game/';
const parts=fs.readFileSync(P+'parts.txt','utf8').split('\n').map(s=>s.trim()).filter(n=>/^js\/cards\//.test(n));
const ctx={};vm.createContext(ctx);vm.runInContext(parts.map(n=>fs.readFileSync(P+n,'utf8')).join('\n')+';globalThis.C=CARDS;globalThis.K=KEYWORDS;globalThis.F=kwFx;',ctx);
const out=[];for(const [k,c] of Object.entries(ctx.C)){if(c.fac!==process.argv[2])continue;
 const kw=ctx.F(Object.assign({},c,{fx:[],aura:[]})), kws=new Set((kw.fx||[]).map(f=>JSON.stringify(f)));
 out.push(Object.assign({},c,{key:k,own:(c.fx||[]).filter(f=>!kws.has(JSON.stringify(f))),kwfx:kw.fx||[]}));}
console.log(JSON.stringify({cards:out,kw:Object.keys(ctx.K)}));
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


def ops(f):  # (trigger, effect, target) for each op of an fx entry
    on = f.get('on', 'spell')
    for o in f.get('do', []):
        if not isinstance(o, dict):
            continue
        name = next((k for k in o if k not in ('to', 'n', 'if', 'max', 'per')), next(iter(o), '?'))
        val = o.get(name)
        tgt = o.get('to') or (val if isinstance(val, str) else '') or ('nearest' if name == 'strike' else '')
        yield (on, name, tgt)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args or args[0] not in FAC:
        print(__doc__); sys.exit(2)
    letter, file = args[0], FAC[args[0]]
    data = json.loads(subprocess.run(['node', '-e', DUMP, ROOT, letter], capture_output=True, text=True, check=True).stdout)
    cards = [c for c in data['cards'] if not c.get('token')]
    units = [c for c in cards if not c.get('tactic')]
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
        if len(ways) < 5:
            probs.append(f'{len(ways)} ways to play, need 5')
        probs += [f'way "{w}": {len(ns)} library cards, need 30' for w, ns in ways.items() if len(ns) < 30]
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

    sig, pair = defaultdict(list), defaultdict(set)  # START_DESIGN step 9: a card's WHEN + WHAT + ON WHOM parts
    for c in cards:
        parts = frozenset(t for f in c['own'] for t in ops(f))
        if parts:
            sig[parts].append(c['name'])
        for t in parts:
            pair[t[:2]].add(c['name'])
    probs = [f"same card: {', '.join(ns)} ({'; '.join(' -> '.join(x for x in t if x) for t in sorted(p))})" for p, ns in sig.items() if len(ns) > 1]
    probs += [f"{t[0]} -> {t[1]} on {len(ns)} cards: {', '.join(sorted(ns)[:6])}..." for t, ns in sorted(pair.items(), key=lambda x: -len(x[1])) if len(ns) > 3]
    check('twins', probs)

    cost = lambda c: c['cost'] if c.get('tactic') else c['sup']
    share = sum(1 for c in cards if c.get('tactic')) / max(1, len(cards))
    probs = []
    for k in range(1, 6):
        at = [c for c in cards if cost(c) == k]
        if len(at) >= 4:
            sh = sum(1 for c in at if c.get('tactic')) / len(at)
            if abs(sh - share) > 0.15:
                probs.append(f'cost {k}: {round(100 * sh)}% spells, faction {round(100 * share)}%')
    check('spells', probs, f'{round(100 * share)}% spells')

    ch = [c['name'] for c in cards if c.get('champion') is True]
    check('champions', [] if len(ch) == 5 else [f'{len(ch)} cards with champion: true, need 5'])

    probs = []
    for c in cards:
        t = c.get('text', '')
        linked = set(re.findall(r'\[\[([^\]|]+)', t))
        bare = re.sub(r'\b(is|are|was|been|gets) wound\b', '', re.sub(r'\[\[[^\]]*\]\]', '', t), flags=re.I)  # the verb, not the keyword
        for k in data['kw']:
            if re.search(r'\b' + re.escape(k) + r'\b', bare, re.I) and k not in linked:
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
    print(f"\n{FAC[letter]}: {'PASS' if not failed else 'FAIL (' + ', '.join(failed) + ')'}")
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
