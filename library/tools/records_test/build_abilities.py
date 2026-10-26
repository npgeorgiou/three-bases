"""Step 1 of the test: cut every entry's stored text into abilities and pieces (library/TAGGING_RECORDS.md, "The structure
under test"). Abilities: cut at sentence ends, line breaks and keyword prefixes; a keyword list gives one ability per keyword.
Pieces: an ability cut at "and" / "then" only when a new effect tag or a number follows.
The cut rules marked "Claude's" below go beyond the agreed list. Usage: build_abilities.py <copy.sqlite>"""
import collections, re, sys
import common as C

PREFIX_WORDS = ['Gift', 'Battlecry', 'Deathrattle', 'Deploy', 'Last Words', 'Fanfare', 'Last Breath', 'Dying Wish', 'Deathwish',
                'On Reveal', 'Opening Gambit', 'Play', 'Slay', 'Strike', 'Nexus Strike', 'Clash', 'Attack', 'Rally', 'Round Start',
                'Round End', 'Start of Turn', 'End of Turn', 'Production', 'When Destroyed']   # the agreed ones + trigger_pairs.py's EXTRA
SENT = re.compile(r'(?<=[.!?;])\s+(?=\S)|\n+')
PREFIX = re.compile(r'(?:^|(?<=\s))(?<!and )(?<!or )(?:(?:' + '|'.join(PREFIX_WORDS) + r')\s*[:\-–—]\s'
                    r'|(?:When|Whenever|At the (?:start|end|beginning))\b'
                    r'|(?:\{[^}]+\}[, ]*)+:)')
# Claude's: a title-case label ("Leader:", "Cry of the Wind:", "When Played:", "Action [Exhaust]:") starts an ability block (40k, AoS, SWU)
LABEL = re.compile(r"(?:^|(?<=[\s■•]))[A-Z][\w'’\-]*(?:\s+(?:of|the|and|in|on|to|a|an|[A-Z][\w'’\-]*)){0,5}(?:\s*\([^)]{1,40}\))?(?:\s*\[[^\]]{1,30}\])?:\s")
LABEL_ONLY = re.compile(r"^[^:]{1,60}:\s*$")
LEAD_LABEL = re.compile(r"^(?:[A-Z][\w'’\-]*(?:\s+[\w'’\-]+){0,3}):\s*")
PW = '(?:' + '|'.join(PREFIX_WORDS) + ')'
TRIG_START = re.compile(r"^(?:" + PW + r"(?:\s+(?:and|or)\s+" + PW + r")*\s*[:\-–—]|(?:When|Whenever|At the|After|Each time|Every time|The first time)\b|[^:]{0,30}—\s*(?:When|Whenever|At)\b)", re.I)
ACT = re.compile(r"^\s*(?:(?:\{[^}]+\}[, ]*)+[^:]{0,60}:|[^:.]{0,40}\{T\}[^:]{0,30}:|Action \[|Activate\b)")
NUM = re.compile(r"(?<![\w/])[+-]?\d+(?![\w/%])(?!\s+(?:other|more|or more|random|target|of|times)\b)")
CONJ = re.compile(r",?\s+(?:and|then)\s+|,\s+then\s+")

def spans(text, rx):
    """cut [0, len) at the zero-width or separator matches of rx; returns (start, end) with outer whitespace trimmed"""
    out, last = [], 0
    for m in rx.finditer(text):
        out.append((last, m.start())); last = m.end()
    out.append((last, len(text)))
    res = []
    for a, b in out:
        while a < b and text[a].isspace(): a += 1
        while b > a and text[b - 1].isspace(): b -= 1
        if b > a: res.append((a, b))
    return res

def cut_before(text, rx):
    """cut at the start of each match of rx (the match stays in the next part)"""
    pts = [0] + [m.start() for m in rx.finditer(text) if m.start() > 0] + [len(text)]
    res = []
    for a, b in zip(pts, pts[1:]):
        while a < b and text[a].isspace(): a += 1
        while b > a and text[b - 1].isspace(): b -= 1
        if b > a: res.append((a, b))
    return res

def abilities(text, kwnames):
    segs = []
    for a, b in spans(text, SENT):
        for x, y in cut_before(text[a:b], PREFIX):
            for u, v in cut_before(text[a + x:a + y], LABEL): segs.append((a + x + u, a + x + v))
    merged = []   # a label with nothing after it belongs to the next block ("Deployed:" + "Action [Exhaust]: ...")
    for s in segs:
        if merged and LABEL_ONLY.match(text[merged[-1][0]:merged[-1][1]]): merged[-1] = (merged[-1][0], s[1])
        else: merged.append(s)
    out = []
    peeled = []   # Claude's: keyword names run together at the start ("Reborn Battlecry and ...", "Taunt Deathrattle: ...") are one ability each
    for a, b in merged:
        while True:
            m = next((m for n in (3, 2, 1) for m in [re.match(r"[A-Z][\w'’\-]*(?: [A-Z][\w'’\-]*){%d}(?=[ ,]+[A-Z{])" % (n - 1), text[a:b])]
                      if m and m.group(0).lower() in kwnames), None)
            if not m: break
            peeled.append((a, a + m.end())); a += m.end()
            while a < b and text[a] in ' ,': a += 1
        peeled.append((a, b))
    for a, b in peeled:
        seg = text[a:b]; lab = LEAD_LABEL.match(seg); off = lab.end() if lab and not TRIG_START.match(seg) else 0
        body = seg[off:]; parts = [(m.start() + off, m.end() + off) for m in re.finditer(r'[^,]+', body)]
        names = [re.sub(r'\([^)]*\)|[\d+X.]+$|\.$', '', seg[p:q]).strip(' .').lower() for p, q in parts]
        names = [re.sub(r'\s+[\dX+]+$', '', n).strip() for n in names]
        if parts and all(n in kwnames for n in names):
            for p, q in parts:
                while p < q and seg[p].isspace(): p += 1
                out.append((a + p, a + q, 'keyword'))
            continue
        kind = 'activated' if ACT.match(seg) else 'triggered' if TRIG_START.match(seg) or TRIG_START.match(seg[off:]) else 'static'
        out.append((a, b, kind))
    return out

def pieces(text, a, b, eff_starts):
    """cut an ability at and/then when the part after it holds a number or the start of an effect not yet in the piece"""
    cuts = [(m.start(), m.end()) for m in CONJ.finditer(text, a, b)]
    bounds = [a] + [e for _, e in cuts] + [b]; ends = [s for s, _ in cuts] + [b]
    res = []; cur = [a, ends[0]]; cur_eff = {k for p, k in eff_starts if a <= p < ends[0]}
    for j in range(1, len(bounds) - 1):
        s, e = bounds[j], ends[j]
        new_eff = {k for p, k in eff_starts if s <= p < e}
        if NUM.search(text, s, e) or (new_eff - cur_eff):
            res.append(tuple(cur)); cur = [s, e]; cur_eff = new_eff
        else:
            cur[1] = e; cur_eff |= new_eff
    res.append(tuple(cur))
    return res

def main(path):
    c = C.connect(path); P = C.Patterns(c); eff, _ = C.concept_kinds(c)
    c.executescript('DROP TABLE IF EXISTS abilities; DROP TABLE IF EXISTS pieces;'
                    'CREATE TABLE abilities(id INTEGER PRIMARY KEY, entity INT, ord INT, ev_pos INT, ev_len INT, kind TEXT);'
                    'CREATE TABLE pieces(id INTEGER PRIMARY KEY, ability INT, ord INT, ev_pos INT, ev_len INT);')
    kw = collections.defaultdict(set)
    for g, n in c.execute("SELECT game, name FROM entities WHERE category='keyword'"):
        n = re.sub(r'\([^)]*\)', '', n or '').strip().lower()
        if n: kw[g].add(n)
    tags = collections.defaultdict(set)
    for e, k, r in c.execute('SELECT entity, concept, role FROM entity_concepts'):
        if k in eff: tags[e].add((k, r))
    na = npc = 0
    for e, g, name, text in c.execute('SELECT id, game, name, text FROM entities WHERE text IS NOT NULL AND trim(text) != ""').fetchall():
        norm, idx = C.read_map(g, name, text)
        starts = [(s, k) for k, r in tags.get(e, ()) for s, _ in C.matches(P, g, k, r, norm, idx, len(text))]
        for i, (a, b, kind) in enumerate(abilities(text, kw[g])):
            aid = c.execute('INSERT INTO abilities(entity, ord, ev_pos, ev_len, kind) VALUES(?,?,?,?,?)', (e, i, a, b - a, kind)).lastrowid; na += 1
            for j, (p, q) in enumerate(pieces(text, a, b, starts)):
                c.execute('INSERT INTO pieces(ability, ord, ev_pos, ev_len) VALUES(?,?,?,?)', (aid, j, p, q - p)); npc += 1
    c.execute('CREATE INDEX IF NOT EXISTS abilities_entity ON abilities(entity)'); c.execute('CREATE INDEX IF NOT EXISTS pieces_ability ON pieces(ability)')
    c.commit(); print('abilities', na, 'pieces', npc)

if __name__ == '__main__': main(sys.argv[1])
