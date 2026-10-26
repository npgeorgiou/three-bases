"""Step 1 of the test: find the words that made each tag. The tag's own patterns are re-run inside its stored text position (inside
one sentence first, so a match cannot run into the next one); a tag from a keyword is placed at that keyword's name in the text;
a tag stored without a position (a note) is placed where its patterns match, else at its excerpt or its trigger_pairs clause.
Tags with no words (hand-mapped whole-card tags) and cost/structure tags (data_rule, game_structure) get no position.
-> tag_words(rid, how, pos, len): rid = entity_concepts rowid, pos/len in the stored text. Usage: words.py <copy.sqlite>"""
import bisect, collections, difflib, re, sys
import common as C

ENTRY_LEVEL = {'data_rule', 'game_structure'}
VIA = re.compile(r'^via keyword ([^:]+):', re.I)
SENT = re.compile(r'(?<=[.!?;])\s+|\n+')

def sentences(text):
    out, last = [], 0
    for m in SENT.finditer(text): out.append((last, m.start())); last = m.end()
    out.append((last, len(text)))
    return [(a, b) for a, b in out if b > a]

def main(path):
    c = C.connect(path); P = C.Patterns(c)
    c.executescript('DROP TABLE IF EXISTS tag_words; CREATE TABLE tag_words(rid INT PRIMARY KEY, how TEXT, pos INT, len INT);')
    notes = dict(c.execute('SELECT id, note FROM text_notes'))
    ent = {i: (g, n, t or '') for i, g, n, t in c.execute('SELECT id, game, name, text FROM entities')}
    kwcon = collections.defaultdict(set)   # keyword entity -> its concepts
    for e, k in c.execute("SELECT ec.entity, ec.concept FROM entity_concepts ec JOIN entities x ON x.id=ec.entity WHERE x.category='keyword'"): kwcon[e].add(k)
    haskw = collections.defaultdict(list)
    for s, d, n in c.execute("SELECT l.src, l.dst, k.name FROM entity_links l JOIN entities k ON k.id=l.dst WHERE l.rel IN ('has_keyword','grants_keyword') AND k.category='keyword'"):
        haskw[s].append((d, re.sub(r'\([^)]*\)', '', (n or '').lower()).strip()))
    clauses = collections.defaultdict(list)
    for e, t, f, cf, cp, cl in c.execute('SELECT entity, trigger, effect, cl_form, cl_pos, cl_len FROM trigger_effect WHERE cl_form IN (0, 1)'):
        clauses[(e, t)].append((cf, cp, cl)); clauses[(e, f)].append((cf, cp, cl))
    def at_word(text, word):
        i = text.lower().find(word) if word else -1
        return (i, i + len(word)) if i >= 0 else None
    cache = {}
    def prep(e):
        if e not in cache:
            if len(cache) > 2000: cache.clear()
            g, n, t = ent[e]; norm, idx = C.read_map(g, n, t); cache[e] = (norm, idx, sentences(t))
        return cache[e]
    def hits(e, k, role):
        """the concept's matches, sentence by sentence first, then on the whole text"""
        g, _, t = ent[e]; norm, idx, sents = prep(e); out = []
        for a, b in sents:
            na, nb = bisect.bisect_left(idx, a), bisect.bisect_left(idx, b)
            for rx in P.get(k, g, role):
                out += [C.to_raw(idx, m.start(), m.end(), len(t)) for m in rx.finditer(norm, na, nb) if m.end() > m.start()]
        return sorted(set(out)) + C.matches(P, g, k, role, norm, idx, len(t))
    log = []
    for rid, e, k, role, meth, form, pos, ln in c.execute('SELECT rowid, entity, concept, role, method, ev_form, ev_pos, ev_len FROM entity_concepts ORDER BY entity').fetchall():
        g, name, text = ent.get(e, ('', '', ''))
        if meth in ENTRY_LEVEL: log.append((rid, 'entry_level', None, None)); continue
        if not text.strip(): log.append((rid, 'no_text', None, None)); continue
        norm, idx, _ = prep(e); span = how = None
        if form == 0: span = (pos, pos + ln)
        elif form == 1: span = C.to_raw(idx, pos, pos + ln, len(text))
        H = hits(e, k, role)
        if span:
            inside = [h for h in H if h[0] < max(span[1], span[0] + 1) and h[1] > span[0]]
            span, how = (inside[0], 'narrowed') if inside else (span, 'excerpt')
        else:
            note = notes.get(pos, '') if form == 2 else ''
            m = VIA.match(note or '')
            if m: span = at_word(text, m.group(1).strip().lower()); how = 'keyword' if span else None
            if not span and H: span, how = H[0], 'pattern'
            if not span:
                for d, kn in haskw.get(e, []):
                    if k in kwcon.get(d, ()) and at_word(text, kn): span, how = at_word(text, kn), 'keyword'; break
            if not span and note and len(note) >= 15:   # a copied excerpt in another spelling ('namedcard'): its longest run in the text
                nt = note.lower().replace('namedcard', 'name'); mm = difflib.SequenceMatcher(None, nt, norm, autojunk=False).find_longest_match(0, len(nt), 0, len(norm))
                if mm.size >= min(20, int(len(nt) * 0.6)): span, how = C.to_raw(idx, mm.b, mm.b + mm.size, len(text)), 'note_text'
            if not span:   # the clause trigger_pairs.py paired this concept in
                for cf, cp, cl in clauses.get((e, k), []):
                    span = (cp, cp + cl) if cf == 0 else C.to_raw(idx, cp, cp + cl, len(text)); how = 'pair_clause'; break
        if not span: log.append((rid, 'wordless', None, None)); continue
        log.append((rid, how, span[0], span[1] - span[0]))
    c.executemany('INSERT INTO tag_words VALUES(?,?,?,?)', log); c.commit()
    print(collections.Counter(h for _, h, _, _ in log))

if __name__ == '__main__': main(sys.argv[1])
