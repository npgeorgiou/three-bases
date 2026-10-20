"""Shared by signature.py and realworld_report.py: which cards belong to which faction (a combined faction's cards count for each
of its factions) and the hypergeometric tail used by the prominence rule."""
import collections, re
from math import lgamma, exp
MIN = 20
CARD = "e.category NOT IN ('keyword','tribe')"
MTG = {'W': 'White', 'U': 'Blue', 'B': 'Black', 'R': 'Red', 'G': 'Green'}

def tail(N, K, n, x):
    """P(X >= x) for X hypergeometric: x successes in n draws from N items of which K are successes"""
    if x <= 0: return 1.0
    lc = lambda a, b: lgamma(a + 1) - lgamma(b + 1) - lgamma(a - b + 1)
    hi = min(K, n); base = lc(N, n)
    terms = [lc(K, i) + lc(N - K, n - i) - base for i in range(x, hi + 1) if n - i <= N - K]
    if not terms: return 0.0
    m = max(terms); return min(1.0, exp(m) * sum(exp(t - m) for t in terms))

def parts(name, plain):
    """the factions a combined faction name stands for, or None"""
    m = re.fullmatch(r'Multicolor \(([WUBRG]+)\)', name or '')
    if m: return [MTG[ch] for ch in m.group(1) if MTG[ch] in plain] or None
    for sep in (' / ', '-'):
        if sep == '-' and ' ' in (name or ''): continue
        ps = (name or '').split(sep)
        if len(ps) > 1 and all(p in plain for p in ps): return ps
    return None

def members(q, g):
    """faction -> set of its card ids (combined cards in each of their factions); all card ids with a faction"""
    rows = q(f'SELECT e.id, e.faction FROM entities e WHERE e.game=? AND {CARD} AND e.faction IS NOT NULL', g)
    names = {f for _, f in rows}; plain = {f for f in names if not parts(f, names - {f})}
    mem = collections.defaultdict(set)
    for i, f in rows:
        for p in (parts(f, plain) or [f]): mem[p].add(i)
    return {f: s for f, s in mem.items() if len(s) >= MIN}, {i for i, _ in rows}

