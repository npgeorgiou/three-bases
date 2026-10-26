"""Step 2 of the test: put every tag in the ability and piece holding the words that made it. The tag's own patterns are re-run
inside its stored span to find the exact words; a tag from a keyword goes to that keyword's ability; a tag stored without
a position (a note) is placed where its patterns match the text, else at a keyword of the entry that carries the concept.
Cost and structure tags (methods data_rule, game_structure) describe the whole entry and are not placed.
Writes entity_concepts.ability / .piece and table place_log(rid, how, cross). Usage: place_tags.py <copy.sqlite>"""
import bisect, collections, difflib, re, sys
import common as C

ENTRY_LEVEL = {'data_rule', 'game_structure'}
VIA = re.compile(r'^via keyword ([^:]+):', re.I)

def main(path):
    c = C.connect(path); P = C.Patterns(c)
    cols = [r[1] for r in c.execute('PRAGMA table_info(entity_concepts)')]
    for col in ('ability', 'piece'):
        if col not in cols: c.execute(f'ALTER TABLE entity_concepts ADD COLUMN {col} INT')
    c.executescript('DROP TABLE IF EXISTS place_log; CREATE TABLE place_log(rid INT PRIMARY KEY, how TEXT, cross INT);')
    notes = dict(c.execute('SELECT id, note FROM text_notes'))
    ab = collections.defaultdict(list)
    for i, e, a, n, k in c.execute('SELECT id, entity, ev_pos, ev_len, kind FROM abilities ORDER BY entity, ord'): ab[e].append((a, a + n, i, k))
    pc = collections.defaultdict(list)
    for i, a, p, n in c.execute('SELECT id, ability, ev_pos, ev_len FROM pieces ORDER BY ability, ord'): pc[a].append((p, p + n, i))
    ent = {i: (g, n, t or '') for i, g, n, t in c.execute('SELECT id, game, name, text FROM entities')}
    kwcon = collections.defaultdict(set)   # keyword entity -> its concepts
    for e, k in c.execute("SELECT ec.entity, ec.concept FROM entity_concepts ec JOIN entities x ON x.id=ec.entity WHERE x.category='keyword'"): kwcon[e].add(k)
    haskw = collections.defaultdict(list)
    for s, d, n in c.execute("SELECT l.src, l.dst, k.name FROM entity_links l JOIN entities k ON k.id=l.dst WHERE l.rel IN ('has_keyword','grants_keyword') AND k.category='keyword'"):
        haskw[s].append((d, (n or '').lower()))
    def locate(lst, s):
        starts = [x[0] for x in lst]; j = bisect.bisect_right(starts, s) - 1
        if j < 0: j = 0
        if j < len(lst) and s >= lst[j][1] and j + 1 < len(lst): j += 1   # between two parts: the next one
        return lst[j]
    def at_word(e, word):
        t = ent[e][2].lower()
        for a, b, i, k in ab[e]:
            if word and word in t[a:b]: return (t.find(word, a, b), t.find(word, a, b) + len(word))
        return None
    norm_cache = {}
    def local(e, k, role, norm, idx, rawlen):
        """the concept's matches run on each ability's own words, so a match cannot run into the next ability"""
        out = []
        for a0, a1, _, _ in ab[e]:
            na = bisect.bisect_left(idx, a0); nb = bisect.bisect_left(idx, a1)
            for rx in P.get(k, ent[e][0], role):
                for m in rx.finditer(norm, na, nb):
                    if m.end() > m.start(): out.append(C.to_raw(idx, m.start(), m.end(), rawlen))
        return sorted(set(out))
    _, trig = C.concept_kinds(c)
    clauses = collections.defaultdict(list)
    for e, t, f, cf, cp, cl in c.execute('SELECT entity, trigger, effect, cl_form, cl_pos, cl_len FROM trigger_effect WHERE cl_form IN (0, 1)'):
        clauses[(e, t)].append((cf, cp, cl)); clauses[(e, f)].append((cf, cp, cl))
    rows = c.execute('SELECT rowid, entity, concept, role, method, ev_form, ev_pos, ev_len FROM entity_concepts ORDER BY entity').fetchall()
    upd, log = [], []
    for rid, e, k, role, meth, form, pos, ln in rows:
        g, name, text = ent.get(e, ('', '', ''))
        if meth in ENTRY_LEVEL: log.append((rid, 'entry_level', 0)); continue
        if not text.strip() or not ab.get(e): log.append((rid, 'no_text', 0)); continue
        if e not in norm_cache:
            if len(norm_cache) > 2000: norm_cache.clear()
            norm_cache[e] = C.read_map(g, name, text)
        norm, idx = norm_cache[e]
        span = None; how = None
        if form == 0: span = (pos, pos + ln)
        elif form == 1: span = C.to_raw(idx, pos, pos + ln, len(text))
        hits = local(e, k, role, norm, idx, len(text)) + C.matches(P, g, k, role, norm, idx, len(text))   # inside one ability first
        if span:
            inside = [h for h in hits if h[0] < max(span[1], span[0] + 1) and h[1] > span[0]]
            if inside: span, how = inside[0], 'narrowed'
            else: how = 'span'
        else:
            note = notes.get(pos, '') if form == 2 else ''
            m = VIA.match(note or '')
            if m: span = at_word(e, m.group(1).strip().lower()); how = 'keyword' if span else None
            if not span and hits: span, how = hits[0], 'pattern'
            if not span:
                for d, kn in haskw.get(e, []):
                    if k in kwcon.get(d, ()):
                        span = at_word(e, re.sub(r'\([^)]*\)', '', kn).strip())
                        if span: how = 'keyword'; break
            if not span and note and len(note) >= 15:   # a copied excerpt in another spelling ('namedcard'): its longest run in the text
                nt = note.lower().replace('namedcard', 'name'); sm = difflib.SequenceMatcher(None, nt, norm, autojunk=False)
                mm = sm.find_longest_match(0, len(nt), 0, len(norm))
                if mm.size >= min(20, int(len(nt) * 0.6)): span = C.to_raw(idx, mm.b, mm.b + mm.size, len(text)); how = 'note_text'
            if not span:   # the clause trigger_pairs.py paired this concept in
                for cf, cp, cl in clauses.get((e, k), []):
                    span = (cp, cp + cl) if cf == 0 else C.to_raw(idx, cp, cp + cl, len(text)); how = 'pair_clause'; break
            if not span and len(ab[e]) == 1: span = (ab[e][0][0], ab[e][0][1]); how = 'only_ability'
            if not span and k in trig:
                tr = [x for x in ab[e] if x[3] == 'triggered']
                if len(tr) == 1: span = (tr[0][0], tr[0][1]); how = 'only_trigger'
        if not span: log.append((rid, 'nowhere', 0)); continue
        a0, a1, aid, kind = locate(ab[e], span[0])
        p0, p1, pid = locate(pc[aid], max(span[0], a0))
        cross = 2 if span[1] > a1 else 1 if span[1] > p1 else 0
        upd.append((aid, pid, rid)); log.append((rid, how, cross))
    c.executemany('UPDATE entity_concepts SET ability=?, piece=? WHERE rowid=?', upd)
    c.executemany('INSERT INTO place_log VALUES(?,?,?)', log)
    c.commit()
    print(collections.Counter(h for _, h, _ in log))

if __name__ == '__main__': main(sys.argv[1])
