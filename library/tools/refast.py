"""Faster regex searching for the build: Fast(rx).search(text) answers exactly like rx.search(text) but first checks, with a plain
substring test, a literal the pattern must contain (found from the parsed pattern); most patterns are rejected without running the
regex engine. Patterns with no usable literal (character classes only, top-level alternatives without one) run as before.
Texts must be lower case, as the build's texts are; a pattern written with capitals is compared in lower case."""
import re
try: import re._parser as sp
except ImportError: import sre_parse as sp
MINLEN = 3

def _need(items):
    """the best literal requirement of a sequence: a list of alternatives, any one of which must occur in the text, or None"""
    best, run = None, ''
    def offer(alts):
        nonlocal best
        if alts and all(len(a) >= MINLEN for a in alts):
            if best is None or min(map(len, alts)) > min(map(len, best)): best = alts
    for op, av in items:
        if op == sp.LITERAL: run += chr(av); continue
        offer([run.lower()] if run else None); run = ''
        if op == sp.SUBPATTERN: offer(_need(av[-1]))
        elif op == sp.BRANCH:
            alts = []
            for br in av[1]:
                n = _need(br)
                if not n: alts = None; break
                alts += n
            offer(alts)
        elif op in (sp.MAX_REPEAT, sp.MIN_REPEAT) and av[0] >= 1: offer(_need(av[2]))
    offer([run.lower()] if run else None)
    return best

class Fast:
    __slots__ = ('rx', 'pattern', 'flags', 'lits')
    def __init__(self, rx):
        self.rx, self.pattern, self.flags = rx, rx.pattern, rx.flags
        try: self.lits = _need(sp.parse(rx.pattern, rx.flags)) if not rx.flags & re.MULTILINE else None
        except Exception: self.lits = None
        if self.lits and not rx.flags & re.IGNORECASE and any(a != a.lower() for a in self.lits): self.lits = None
    def search(self, text):
        l = self.lits
        if l is not None and not any(a in text for a in l): return None
        return self.rx.search(text)
    def maybe(self, text):
        """False only when the text lacks the literal the pattern needs, so no clause of it can match"""
        return self.lits is None or any(a in text for a in self.lits)
    def __getattr__(self, k): return getattr(self.rx, k)
