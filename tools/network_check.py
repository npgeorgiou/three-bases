#!/usr/bin/env python3
"""Network check for Three Bases faction designs: are the mechanics and cards a thick web?

Reads a design file (factions/designs/<faction>.txt). Lines it reads (anything else is ignored):
  MECHANIC <name> | makes: a, b | needs: c, d
  CARD <name> | <cost - str|def, size> | <text> | mech: M1, M2 | makes: a, b | needs: c
  DECK <name>: card, card x3, ...
"makes" and "needs" are short tags for things in play (projectile-dies, lodged, enemy-front-packed ...).
Usage: python3 tools/network_check.py factions/designs/<faction>.txt [--quiet]
"""
import re, sys
from collections import defaultdict

def parse(path):
    mechs, cards, decks = {}, {}, {}
    for raw in open(path, encoding='utf-8'):
        line = raw.strip()
        if line.startswith('MECHANIC ') or line.startswith('CARD '):
            kind, rest = line.split(' ', 1)
            parts = [p.strip() for p in rest.split(' | ')]
            e = {'name': parts[0], 'makes': set(), 'needs': set(), 'mech': [], 'cost': '', 'text': ''}
            free = []
            for p in parts[1:]:
                m = re.match(r'(makes|needs|mech):\s*(.*)$', p)
                if m:
                    vals = [v.strip() for v in m.group(2).split(',') if v.strip()]
                    if m.group(1) == 'mech': e['mech'] = vals
                    else: e[m.group(1)] = set(vals)
                else: free.append(p)
            if kind == 'CARD':
                e['cost'] = free[0] if free else ''
                e['text'] = free[1] if len(free) > 1 else ''
                cards[e['name']] = e
            else: mechs[e['name']] = e
        elif line.startswith('DECK '):
            name, lst = line[5:].split(':', 1)
            items = []
            for it in lst.split(','):
                it = it.strip()
                if not it: continue
                m = re.match(r'(.*?)\s+x(\d)$', it)
                items.append((m.group(1), int(m.group(2))) if m else (it, 1))
            decks[name.strip()] = items
    return mechs, cards, decks

def web(entries, label, out):
    """Setup/cash-in counts over one set of entries (mechanics, a faction's cards, or a deck)."""
    makers, users = defaultdict(list), defaultdict(list)
    for e in entries:
        for t in e['makes']: makers[t].append(e['name'])
        for t in e['needs']: users[t].append(e['name'])
    problems = []
    for t in sorted(users):
        if not makers[t]: problems.append(f"need with no maker: {t} (needed by {', '.join(users[t])})")
    if label != 'mechanics':
        for e in entries:
            for t in e['needs']:
                base = lambda x: x.split('#')[0]
                n = len([m for m in makers[t] if base(m) != base(e['name'])])
                if 0 < n < 3: problems.append(f"cash-in with fewer than 3 setups: {e['name']} needs {t} ({n})")
            fed = {u.split('#')[0] for t in e['makes'] for u in users[t] if u.split('#')[0] != e['name'].split('#')[0]}
            if e['makes'] and len(fed) < 2: problems.append(f"setup feeding fewer than 2 cards: {e['name']} ({len(fed)})")
            if not e['makes'] and not e['needs']: problems.append(f"no line at all: {e['name']}")
    out.append(f"\n== {label}: {len(entries)} entries, {len(makers)} things made, {len(users)} things needed")
    for t in sorted(set(makers) | set(users)):
        out.append(f"  {t}: made by {len(makers[t])}, used by {len(users[t])}")
    return problems

def main():
    path = sys.argv[1]; quiet = '--quiet' in sys.argv
    mechs, cards, decks = parse(path)
    out, problems = [], []
    if mechs:
        problems += web(list(mechs.values()), 'mechanics', out)
        for m in mechs.values():
            feeds = sorted(o['name'] for o in mechs.values() if o is not m and m['makes'] & o['needs'])
            fedby = sorted(o['name'] for o in mechs.values() if o is not m and o['makes'] & m['needs'])
            out.append(f"  {m['name']}: feeds {', '.join(feeds) or '-'}; fed by {', '.join(fedby) or '-'}")
            if not feeds: problems.append(f"mechanic feeds no other mechanic: {m['name']}")
            if not fedby: problems.append(f"mechanic fed by no other mechanic: {m['name']}")
    if cards:
        cl = list(cards.values())
        problems += web(cl, 'cards', out)
        two = [c for c in cl if len(c['mech']) >= 2]
        out.append(f"  cards in two or more mechanics: {len(two)} of {len(cl)} ({100*len(two)//len(cl)}%)")
        if len(two) * 3 < len(cl): problems.append("fewer than a third of the cards are in two mechanics")
        unknown = sorted({m for c in cl for m in c['mech']} - set(mechs)) if mechs else []
        if unknown: problems.append(f"cards name mechanics not listed: {', '.join(unknown)}")
        seen = defaultdict(list)
        for c in cl:
            key = (c['cost'].split(' - ')[0], tuple(sorted(c['makes'])), tuple(sorted(c['needs'])))
            seen[key].append(c['name'])
        for k, names in seen.items():
            if len(names) > 1 and (k[1] or k[2]): problems.append(f"possible twins (same cost, same lines): {', '.join(names)}")
        if mechs:
            for m in mechs:
                n = len([c for c in cl if m in c['mech']])
                out.append(f"  cards in {m}: {n}")
    for d, items in decks.items():
        missing = [n for n, _ in items if n not in cards]
        if missing: problems.append(f"deck {d}: cards not in the file: {', '.join(missing)}")
        entries = []
        for n, k in items:
            if n in cards:
                for i in range(k): entries.append(dict(cards[n], name=f"{n}#{i+1}" if k > 1 else n))
        total = sum(k for _, k in items)
        out.append(f"\n== deck {d}: {total} cards")
        dp = web(entries, f"deck {d}", out)
        problems += sorted({f"deck {d}: {re.sub(r'#[0-9]+', '', p)}" for p in dp if 'fewer than 3 setups' in p or 'no maker' in p})
    if not quiet: print('\n'.join(out))
    print(f"\n{len(problems)} problems" + (':' if problems else ''))
    for p in problems: print('  - ' + p)
    sys.exit(1 if problems else 0)

if __name__ == '__main__':
    main()
