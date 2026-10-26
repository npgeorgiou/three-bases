"""Shared helpers for the tagging-per-effect test (library/TAGGING_RECORDS.md): the patterns that made the tags, the entry's
text as the patterns read it with a map back to the stored text, and the concept roots. Works on a copy of the database only."""
import ast, collections, os, re, sqlite3, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.dirname(HERE)
sys.path.insert(0, TOOLS)
import reading as RD

def connect(path):
    real = os.path.abspath(os.path.join(TOOLS, '..', 'three-bases-library.sqlite'))
    if os.path.abspath(path) == real: sys.exit('refusing to write to the real database; use a copy')
    return sqlite3.connect(path)

def extra_triggers():
    """the trigger wording list of trigger_pairs.py (EXTRA), read without running that script"""
    src = open(os.path.join(TOOLS, 'trigger_pairs.py'), encoding='utf-8').read()
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], 'id', '') == 'EXTRA': return ast.literal_eval(node.value)
    return {}

def exclusions():
    excl = collections.defaultdict(set)
    pd = os.path.join(TOOLS, 'patterns')
    for f in os.listdir(pd):
        if f.endswith('.txt'):
            for line in open(os.path.join(pd, f), encoding='utf-8'):
                if line.startswith('!'): excl[f[:-4]].add(tuple(line[1:].rstrip('\n').split('|', 1)))
    return excl

class Patterns:
    """the wording patterns of a concept in a game (general + the game's own, minus the game's exclusions), by role"""
    def __init__(self, c):
        self.excl = exclusions(); self.raw = collections.defaultdict(list); self.cache = {}
        for con, role, p, g in c.execute('SELECT concept, role, pattern, game FROM concept_patterns'):
            self.raw[con].append((role, p, g))
        for con, ps in extra_triggers().items():
            for p in ps: self.raw[con].append(('does', p, None))
    def get(self, con, game, role=None):
        k = (con, game, role)
        if k not in self.cache:
            X = self.excl.get(game, set()) | (self.excl.get('_all', set()) if game != 'marvel_snap' else set())
            out = []
            for r, p, g in self.raw.get(con, []):
                if g not in (None, '_all', game) or (con, p) in X: continue
                if p.startswith('(?s)^(?!'): continue   # whole-entry patterns name no words
                if role and r != role: continue
                try: out.append(re.compile(p, re.I))
                except re.error: pass
            if role and not out: out = self.get(con, game)
            self.cache[k] = out
        return self.cache[k]

def read_map(game, name, text):
    """the text as patterns read it (compact_text.read_text) and, for each of its characters, the index in the stored text"""
    s = list((text or '').lower()); idx = list(range(len(s)))
    def sub(rx, rep, literal=False):
        nonlocal s, idx
        cur = ''.join(s); ns, ni, last = [], [], 0
        it = (m.span() for m in re.finditer(re.escape(rx) if literal else rx, cur))
        for a, b in it:
            ns += s[last:a]; ni += idx[last:a]
            ns += list(rep); ni += [idx[a] if a < len(idx) else len(text)] * len(rep); last = b
        ns += s[last:]; ni += idx[last:]; s, idx = ns, ni
    if game in RD.NO_REMINDER: sub(r'\([^()]*\)', ' ')
    for x in [name] + (name or '').split(' // '):
        if x and len(x) > 2: sub(x.lower(), 'name', literal=True)
    return ''.join(s), idx

def roots(c):
    R = collections.defaultdict(set)
    for i, r in c.execute('SELECT id, root FROM concept_tree'): R[i].add(r)
    return R

def subtree(c, cid):
    return {i for (i,) in c.execute('SELECT id FROM concept_tree WHERE root=?', (cid,))}

TRIGGER_ROOT_SKIP = {'passive', 'aura', 'trigger'}
def concept_kinds(c):
    """effect concepts and trigger concepts, as trigger_pairs.py reads them"""
    root = dict(c.execute("SELECT id, root FROM concept_tree WHERE root IN ('trigger','effect') ORDER BY root DESC"))
    eff = {k for k, r in root.items() if r == 'effect'}
    trig = {k for k, r in root.items() if r == 'trigger'} - TRIGGER_ROOT_SKIP
    for k in ('death_trigger', 'other_death_trigger', 'leave_trigger', 'other_leave_trigger'):
        if k not in eff: trig.add(k)
    return eff, trig

def to_raw(idx, a, b, rawlen):
    """a span of the read text -> the span of the stored text"""
    if not idx: return (0, 0)
    ra = idx[a] if a < len(idx) else rawlen
    rb = (idx[b - 1] + 1) if b - 1 < len(idx) and b > a else ra
    return (ra, max(ra, rb))

def matches(P, game, con, role, norm, idx, rawlen):
    """every place a concept's patterns match the entry's text, as spans of the stored text (non-empty matches only)"""
    out = []
    for rx in P.get(con, game, role):
        for m in rx.finditer(norm):
            if m.end() > m.start(): out.append(to_raw(idx, m.start(), m.end(), rawlen))
    return sorted(set(out))
